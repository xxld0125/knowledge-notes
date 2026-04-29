#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


API_BASE = os.environ.get("YUQUE_API_BASE", "https://www.yuque.com/api/v2").rstrip("/")


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def sanitize_segment(name: str) -> str:
    name = name.strip()
    name = re.sub(r"[\\/:*?\"<>|]", "-", name)
    name = re.sub(r"\s+", " ", name)
    name = name.strip(". ")
    return name or "未命名"


def json_dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")


def http_get(token: str, url: str, params: dict[str, Any] | None = None) -> Any:
    if params:
        qs = urllib.parse.urlencode(params)
        url = f"{url}?{qs}"
    req = urllib.request.Request(
        url,
        headers={
            "X-Auth-Token": token,
            "User-Agent": "knowledge-notes-yuque-export/1.0",
            "Accept": "application/json",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def api_get(token: str, path: str, params: dict[str, Any] | None = None) -> Any:
    return http_get(token, f"{API_BASE}{path}", params=params)


@dataclass(frozen=True)
class TocItem:
    title: str
    doc_id: int | None
    level: int
    visible: bool


def build_toc_items(raw: list[dict[str, Any]]) -> list[TocItem]:
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


def has_children(items: list[TocItem], idx: int) -> bool:
    j = idx + 1
    return j < len(items) and items[j].level > items[idx].level


def find_doc_file_flat(docs_root: Path, slug: str) -> Path | None:
    candidates = list(docs_root.glob(f"{slug}-*.md"))
    if candidates:
        return sorted(candidates, key=lambda p: (len(p.name), p.name))[0]
    p2 = docs_root / f"{slug}.md"
    return p2 if p2.exists() else None


def safe_move(src: Path, dst: Path) -> None:
    if src.resolve() == dst.resolve():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        die(f"目标文件已存在，无法移动：{dst}")
    src.rename(dst)


def restructure_by_toc(repo_root: Path, book_dir: Path) -> None:
    meta_dir = book_dir / "_meta"
    docs_root = book_dir / "docs"
    toc_items = build_toc_items(json.loads((meta_dir / "toc.json").read_text(encoding="utf-8")))
    docs_index = json.loads((meta_dir / "docs-index.json").read_text(encoding="utf-8"))
    id_index: dict[int, dict[str, str]] = {int(d["id"]): {"slug": d["slug"], "title": d["title"]} for d in docs_index}

    stack: list[str] = []
    stack_levels: list[int] = []

    lines: list[str] = []
    lines.extend(
        [
            "# 目录",
            "",
            f"- 生成来源：`{(meta_dir / 'toc.json').relative_to(repo_root)}`",
            f"- 映射来源：`{(meta_dir / 'docs-index.json').relative_to(repo_root)}`",
            "- 目录规则：按 TOC `level` 生成子目录；如果某篇文档在 TOC 中还有子节点，则为其建立同名目录并把该文档放在该目录下。",
            "",
            "## 目录树",
            "",
        ]
    )

    moves: list[tuple[Path, Path]] = []

    for i, it in enumerate(toc_items):
        while stack_levels and stack_levels[-1] >= it.level:
            stack.pop()
            stack_levels.pop()

        indent = "  " * it.level

        if it.doc_id is None:
            seg = sanitize_segment(it.title)
            stack.append(seg)
            stack_levels.append(it.level)
            lines.append(f"{indent}- {it.title}")
            continue

        meta = id_index.get(it.doc_id)
        if not meta:
            lines.append(f"{indent}- {it.title} **（缺少索引映射）**")
            continue

        slug = meta["slug"]
        src = find_doc_file_flat(docs_root, slug)
        if src is None:
            lines.append(f"{indent}- {it.title} **（本地缺失）**")
            continue

        extra_dir = sanitize_segment(it.title) if has_children(toc_items, i) else None
        dest_dir = docs_root.joinpath(*stack, *( [extra_dir] if extra_dir else [] ))
        dst = dest_dir / src.name
        moves.append((src, dst))

        rel_link = dst.relative_to(docs_root).as_posix()
        lines.append(f"{indent}- [{it.title}](./{rel_link})")

        if extra_dir:
            stack.append(extra_dir)
            stack_levels.append(it.level)

    for src, dst in moves:
        if src.exists():
            safe_move(src, dst)

    write_text(docs_root / "000_目录.md", "\n".join(lines))


def export_repo(repo_id: str, out_root: Path, token: str, sleep_ms: int = 150) -> Path:
    # repo meta
    repo = api_get(token, f"/repos/{urllib.parse.quote(repo_id, safe='/')}")
    data = repo.get("data") if isinstance(repo, dict) and "data" in repo else repo
    book_name = sanitize_segment(str(data.get("name") or data.get("title") or repo_id))
    book_dir = out_root / book_name

    # toc
    toc = api_get(token, f"/repos/{urllib.parse.quote(repo_id, safe='/')}/toc")
    toc_data = toc.get("data") if isinstance(toc, dict) and "data" in toc else toc
    json_dump(book_dir / "_meta/toc.json", toc_data)

    # docs list (paginated)
    docs_index: list[dict[str, Any]] = []
    offset = 0
    limit = 100
    while True:
        docs = api_get(
            token,
            f"/repos/{urllib.parse.quote(repo_id, safe='/')}/docs",
            params={"offset": offset, "limit": limit},
        )
        docs_data = docs.get("data") if isinstance(docs, dict) and "data" in docs else docs
        if not isinstance(docs_data, list):
            die(f"Unexpected docs list response: {type(docs_data)}")
        batch = [{"id": int(d["id"]), "slug": d["slug"], "title": d["title"]} for d in docs_data]
        docs_index.extend(batch)
        if len(docs_data) < limit:
            break
        offset += limit
    json_dump(book_dir / "_meta/docs-index.json", docs_index)

    # export docs
    docs_dir = book_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    for d in docs_index:
        slug = d["slug"]
        title = d["title"]
        doc = api_get(
            token,
            f"/repos/{urllib.parse.quote(repo_id, safe='/')}/docs/{urllib.parse.quote(slug, safe='')}",
            params={"include_lake": "true"},
        )
        doc_data = doc.get("data") if isinstance(doc, dict) and "data" in doc else doc
        body = doc_data.get("body") or ""
        fn = f"{slug}-{sanitize_segment(title)}.md"
        write_text(docs_dir / fn, body)
        time.sleep(max(0.0, sleep_ms / 1000.0))

    # status
    status = {
        "repo_id": repo_id,
        "book_name": book_name,
        "total_docs": len(docs_index),
        "migrated_docs": len(docs_index),
        "remaining_docs": 0,
        "migrated_slugs": [d["slug"] for d in docs_index],
        "updated_at": time.strftime("%Y-%m-%d"),
    }
    json_dump(book_dir / "_meta/migration-status.json", status)

    # README
    readme = "\n".join(
        [
            f"# {book_name}（语雀迁移）",
            "",
            f"- 来源知识库：`{repo_id}`",
            f"- 迁移时间：{time.strftime('%Y-%m-%d')}",
            f"- 本次已迁移正文：{len(docs_index)} 篇",
            "",
            "## 目录",
            "",
            "- `docs/`：迁移后的 Markdown 文档（入口为 `docs/000_目录.md`）",
            "- `_meta/`：toc/docs 索引与迁移状态",
            "",
        ]
    )
    write_text(book_dir / "README.md", readme)

    return book_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a Yuque repo/book to local markdown files.")
    parser.add_argument("--repo-id", required=True, help='语雀知识库 namespace，如 "u25370234/mkhi8l"')
    parser.add_argument("--out", default="knowledge-base", help="输出目录（相对于仓库根）")
    parser.add_argument("--token", default=os.environ.get("YUQUE_TOKEN") or os.environ.get("YUQUE_API_TOKEN"), help="语雀 Token（也可用环境变量 YUQUE_TOKEN）")
    parser.add_argument("--sleep-ms", type=int, default=150, help="每篇文档请求间隔，避免触发限流")
    parser.add_argument("--restructure", action="store_true", help="按 TOC 生成目录树，并生成 docs/000_目录.md")
    args = parser.parse_args()

    if not args.token:
        die("缺少 Token：请传 --token 或设置环境变量 YUQUE_TOKEN")

    repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd())).resolve()
    out_root = (repo_root / args.out).resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    book_dir = export_repo(args.repo_id, out_root, args.token, sleep_ms=args.sleep_ms)
    if args.restructure:
        restructure_by_toc(repo_root, book_dir)
    print(f"Exported to: {book_dir}")


if __name__ == "__main__":
    main()

