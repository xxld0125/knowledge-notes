#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"文件不存在：{path}")
    except json.JSONDecodeError as e:
        die(f"JSON 解析失败：{path} ({e})")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


_TAG_RE = re.compile(r"<[^>]+>")
_DIV_LIKE_RE = re.compile(r"</?(div|p|br)\b[^>]*>", re.IGNORECASE)
_ANGLE_TOKEN_RE = re.compile(r"</?[\w-]+[^>]*?>")


def html_to_text(s: str) -> str:
    """
    Lakeboard 节点内容通常在 html 字段里（含 span/div/br）。
    这里做纯文本抽取，并对 Obsidian Canvas 的渲染做兼容处理：
    - <head>/<script> 等会被当成 HTML 标签，可能导致显示/样式不一致；统一包成行内代码。
    """
    if not s:
        return ""
    s = s.replace("\u200b", "")  # 语雀里常见的零宽字符
    s = _DIV_LIKE_RE.sub("\n", s)
    s = _TAG_RE.sub("", s)
    s = html.unescape(s)
    s = re.sub(r"\n{3,}", "\n\n", s).strip()
    s = _ANGLE_TOKEN_RE.sub(lambda m: f"`{m.group(0)}`", s)
    return s


@dataclass(frozen=True)
class EdgeSpec:
    parent_id: str
    child_id: str


@dataclass
class TreeNode:
    id: str
    text: str
    children: list["TreeNode"]
    raw_x: float | None = None
    raw_y: float | None = None
    depth: int = 0
    x: float = 0.0
    y: float = 0.0


def _iter_children(raw: Any) -> Iterable[dict[str, Any]]:
    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for it in raw:
        if isinstance(it, dict):
            out.append(it)
    return out


def extract_mindmap_root(doc: dict[str, Any]) -> dict[str, Any]:
    if str(doc.get("format")) != "lakeboard":
        die("不是 lakeboard 文件：format != lakeboard")
    diagram = doc.get("diagramData") or {}
    body = diagram.get("body") or []
    if not isinstance(body, list) or not body:
        die("lakeboard 缺少 diagramData.body")
    for el in body:
        if isinstance(el, dict) and el.get("type") == "mindmap":
            return el
    raise MindmapNotFound("未找到 type=mindmap 的根节点（diagramData.body 内）")


class MindmapNotFound(Exception):
    pass


def extract_diagram_body(doc: dict[str, Any]) -> list[dict[str, Any]]:
    if str(doc.get("format")) != "lakeboard":
        die("不是 lakeboard 文件：format != lakeboard")
    diagram = doc.get("diagramData") or {}
    body = diagram.get("body") or []
    if not isinstance(body, list):
        return []
    return [it for it in body if isinstance(it, dict)]


def build_tree(root: dict[str, Any]) -> TreeNode:
    def walk(n: dict[str, Any], depth: int) -> TreeNode:
        nid = str(n.get("id", "")).strip()
        txt = html_to_text(str(n.get("html", ""))) or nid
        raw_x = n.get("x")
        raw_y = n.get("y")
        node = TreeNode(
            id=nid,
            text=txt,
            children=[],
            raw_x=float(raw_x) if isinstance(raw_x, (int, float)) else None,
            raw_y=float(raw_y) if isinstance(raw_y, (int, float)) else None,
            depth=depth,
        )
        for ch in _iter_children(n.get("children")):
            node.children.append(walk(ch, depth + 1))
        return node

    return walk(root, 0)


def flatten_tree(root: TreeNode) -> tuple[list[TreeNode], list[EdgeSpec]]:
    nodes: list[TreeNode] = []
    edges: list[EdgeSpec] = []

    def walk(p: TreeNode | None, n: TreeNode) -> None:
        nodes.append(n)
        if p is not None:
            edges.append(EdgeSpec(parent_id=p.id, child_id=n.id))
        for ch in n.children:
            walk(n, ch)

    walk(None, root)
    return nodes, edges


def count_leaves(n: TreeNode) -> int:
    if not n.children:
        return 1
    return sum(count_leaves(ch) for ch in n.children)


def layout_tree(root: TreeNode, *, x0: float, y0: float, x_gap: float = 420.0, y_gap: float = 160.0) -> None:
    """
    将 mindmap（树）排成 Obsidian canvas 可读布局：
    - x：按深度递增
    - y：按叶子顺序分配，内部节点取子树中心
    - 最后整体平移，确保根节点坐标不变
    """
    leaves = count_leaves(root)
    cursor_y = y0 - (leaves - 1) * y_gap / 2.0

    def walk(n: TreeNode) -> float:
        nonlocal cursor_y
        n.x = x0 + n.depth * x_gap
        if not n.children:
            n.y = cursor_y
            cursor_y += y_gap
            return n.y
        child_ys = [walk(ch) for ch in n.children]
        n.y = sum(child_ys) / len(child_ys)
        return n.y

    walk(root)

    dy = y0 - root.y

    def shift(n: TreeNode) -> None:
        n.y += dy
        for ch in n.children:
            shift(ch)

    shift(root)


def guess_side(px: float, cx: float) -> tuple[str, str]:
    if cx >= px:
        return "right", "left"
    return "left", "right"


def build_canvas(nodes: list[TreeNode], edges: list[EdgeSpec], *, color: str) -> dict[str, Any]:
    default_w = 320
    default_h = 120

    canvas_nodes: list[dict[str, Any]] = []
    for n in nodes:
        if not n.id:
            continue
        canvas_nodes.append(
            {
                "id": n.id,
                "type": "text",
                "x": float(n.x),
                "y": float(n.y),
                "width": default_w,
                "height": default_h,
                "text": n.text or n.id,
                # Obsidian Canvas 内置调色板（字符串数字）。统一给一个颜色，保证视觉一致。
                "color": color,
            }
        )

    pos_index: dict[str, tuple[float, float]] = {n.id: (n.x, n.y) for n in nodes}
    canvas_edges: list[dict[str, Any]] = []
    for e in edges:
        p = pos_index.get(e.parent_id, (0.0, 0.0))
        c = pos_index.get(e.child_id, (0.0, 0.0))
        from_side, to_side = guess_side(p[0], c[0])
        canvas_edges.append(
            {
                "id": uuid.uuid4().hex,
                "fromNode": e.parent_id,
                "fromSide": from_side,
                "toNode": e.child_id,
                "toSide": to_side,
            }
        )

    return {"nodes": canvas_nodes, "edges": canvas_edges}


def build_canvas_from_body(body: list[dict[str, Any]], *, color: str) -> dict[str, Any]:
    """
    兜底：当 lakeboard 不是 mindmap（例如自由画板/流程图）时，
    将 diagramData.body 的元素直接映射为 canvas 节点。
    """
    nodes: list[dict[str, Any]] = []

    # 简易网格排布，用于缺少坐标的元素
    grid_x0 = 0.0
    grid_y0 = 0.0
    grid_dx = 380.0
    grid_dy = 180.0
    grid_i = 0

    for el in body:
        el_id = str(el.get("id", "")).strip()
        if not el_id:
            continue

        raw_x = el.get("x")
        raw_y = el.get("y")
        if isinstance(raw_x, (int, float)) and isinstance(raw_y, (int, float)):
            x = float(raw_x)
            y = float(raw_y)
        else:
            x = grid_x0 + (grid_i % 6) * grid_dx
            y = grid_y0 + (grid_i // 6) * grid_dy
            grid_i += 1

        w = el.get("width")
        h = el.get("height")
        width = float(w) if isinstance(w, (int, float)) and float(w) > 0 else 320.0
        height = float(h) if isinstance(h, (int, float)) and float(h) > 0 else 120.0

        text = html_to_text(str(el.get("html", ""))) or html_to_text(str(el.get("text", ""))) or el_id
        nodes.append(
            {
                "id": el_id,
                "type": "text",
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "text": text,
                "color": color,
            }
        )

    return {"nodes": nodes, "edges": []}


def main() -> None:
    ap = argparse.ArgumentParser(description="将语雀 Lakeboard(mindmap) JSON 转换为 Obsidian Canvas(.canvas)")
    ap.add_argument("input", type=Path, help="输入 lakeboard 文件路径（通常扩展名是 .md 但内容为 JSON）")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="输出 .canvas 路径（默认与输入同目录同名，仅扩展名改为 .canvas）",
    )
    ap.add_argument(
        "--color",
        type=str,
        default="5",
        help='统一节点颜色（Obsidian canvas 调色板编号字符串，如 "1".."6"），默认 "5"',
    )
    args = ap.parse_args()

    src: Path = args.input
    dst: Path = args.output or src.with_suffix(".canvas")

    doc = read_json(src)
    try:
        raw_root = extract_mindmap_root(doc)
        tree_root = build_tree(raw_root)

        anchor_x = tree_root.raw_x if tree_root.raw_x is not None else 0.0
        anchor_y = tree_root.raw_y if tree_root.raw_y is not None else 0.0
        layout_tree(tree_root, x0=anchor_x, y0=anchor_y)

        nodes, edges = flatten_tree(tree_root)
        canvas = build_canvas(nodes, edges, color=str(args.color))
    except MindmapNotFound:
        # 非 mindmap 类型：走兜底转换
        body = extract_diagram_body(doc)
        canvas = build_canvas_from_body(body, color=str(args.color))

    write_json(dst, canvas)
    print(f"OK: {src} -> {dst} (nodes={len(canvas['nodes'])}, edges={len(canvas['edges'])})")


if __name__ == "__main__":
    main()

