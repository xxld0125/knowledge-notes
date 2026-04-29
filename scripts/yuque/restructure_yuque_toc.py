#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TocItem:
    title: str
    doc_id: int | None
    level: int
    visible: bool


def _sanitize_segment(name: str) -> str:
    """
    Make a safe directory segment while preserving Chinese.
    """
    name = name.strip()
    name = re.sub(r"[\\\\/:*?\"<>|]", "-", name)
    name = re.sub(r"\s+", " ", name)
    name = name.strip(". ")
    return name or "未命名"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _build_toc_items(raw: list[dict[str, Any]]) -> list[TocItem]:
    items: list[TocItem] = []
    for it in raw:
        doc_id = it.get("doc_id")
        if doc_id in ("", None):
            doc_id_int = None
        else:
            doc_id_int = int(doc_id)
        items.append(
            TocItem(
                title=str(it.get("title", "")).strip(),
                doc_id=doc_id_int,
                level=int(it.get("level", 0)),
                visible=bool(it.get("visible", True)),
            )
        )
    return items


def _has_children(items: list[TocItem], idx: int) -> bool:
    cur_level = items[idx].level
    j = idx + 1
    if j >= len(items):
        return False
    return items[j].level > cur_level


def _build_id_index(raw: list[dict[str, Any]]) -> dict[int, dict[str, str]]:
    out: dict[int, dict[str, str]] = {}
    for d in raw:
        _id = int(d["id"])
        out[_id] = {"slug": str(d["slug"]), "title": str(d["title"])}
    return out


def _find_existing_doc_file(docs_root: Path, slug: str) -> Path | None:
    # current convention: <slug>-<title>.md or <slug>.md (fallback)
    candidates = list(docs_root.glob(f"{slug}-*.md"))
    if candidates:
        # if multiple (shouldn't), choose the shortest name for stability
        return sorted(candidates, key=lambda p: (len(p.name), p.name))[0]
    p2 = docs_root / f"{slug}.md"
    return p2 if p2.exists() else None


def _safe_move(src: Path, dst: Path) -> None:
    if src.resolve() == dst.resolve():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        raise RuntimeError(f"Destination exists: {dst}")
    shutil.move(str(src), str(dst))


def main() -> None:
    repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd())).resolve()
    kb_root = repo_root / "knowledge-base/面试训练"
    meta_dir = kb_root / "_meta"
    docs_root = kb_root / "docs"

    toc_path = meta_dir / "toc.json"
    index_path = meta_dir / "docs-index.json"
    if not toc_path.exists():
        raise SystemExit(f"Missing {toc_path}")
    if not index_path.exists():
        raise SystemExit(f"Missing {index_path}")

    toc_items = _build_toc_items(_load_json(toc_path))
    id_index = _build_id_index(_load_json(index_path))

    # level -> list[str] segments (current directory stack)
    stack: list[str] = []
    stack_levels: list[int] = []

    moves: list[tuple[Path, Path]] = []
    link_lines: list[str] = []

    link_lines.extend(
        [
            "# 目录（从语雀 TOC 生成）",
            "",
            f"- 生成来源：`{toc_path.relative_to(repo_root)}`",
            f"- 映射来源：`{index_path.relative_to(repo_root)}`",
            "- 目录规则：按 TOC `level` 生成子目录；如果某篇文档在 TOC 中还有子节点，则为其建立同名目录并把该文档放在该目录下。",
            "",
            "## 目录树",
            "",
        ]
    )

    def current_dir_segments() -> list[str]:
        return stack.copy()

    for i, it in enumerate(toc_items):
        # adjust stack to current level
        while stack_levels and stack_levels[-1] >= it.level:
            stack.pop()
            stack_levels.pop()

        indent = "  " * it.level

        if it.doc_id is None:
            seg = _sanitize_segment(it.title)
            stack.append(seg)
            stack_levels.append(it.level)
            link_lines.append(f"{indent}- {it.title}")
            continue

        doc_meta = id_index.get(it.doc_id)
        if not doc_meta:
            # keep in toc but mark missing mapping
            link_lines.append(f"{indent}- {it.title} **（缺少索引映射）**")
            continue

        slug = doc_meta["slug"]
        title = doc_meta["title"]

        src = _find_existing_doc_file(docs_root, slug)
        if src is None:
            link_lines.append(f"{indent}- {it.title} **（本地缺失）**")
            continue

        # if this doc has children, create a directory for it
        extra_dir = _sanitize_segment(it.title) if _has_children(toc_items, i) else None
        dest_dir = docs_root.joinpath(*current_dir_segments(), *( [extra_dir] if extra_dir else [] ))
        dst = dest_dir / src.name

        moves.append((src, dst))

        rel_link = dst.relative_to(docs_root).as_posix()
        flags = []
        if not it.visible:
            flags.append("语雀隐藏")
        if flags:
            link_lines.append(f"{indent}- [{it.title}](./{rel_link}) **（{' / '.join(flags)}）**")
        else:
            link_lines.append(f"{indent}- [{it.title}](./{rel_link})")

        # if it has children, push its dir onto stack for following descendants
        if extra_dir:
            stack.append(extra_dir)
            stack_levels.append(it.level)

    # execute moves
    moved = 0
    for src, dst in moves:
        if src.exists():
            _safe_move(src, dst)
            moved += 1

    # rebuild toc markdown
    toc_md_path = docs_root / "000_目录.md"
    _write_text(toc_md_path, "\n".join(link_lines).rstrip() + "\n")

    print(f"Moved files: {moved}")
    print(f"Updated: {toc_md_path}")


if __name__ == "__main__":
    main()

