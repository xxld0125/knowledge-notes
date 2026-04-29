#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any


INVALID_CHARS_RE = re.compile(r"[\\/:*?\"<>|]")
WS_RE = re.compile(r"\s+")


def sanitize_name(name: str) -> str:
    name = name.strip()
    name = INVALID_CHARS_RE.sub("-", name)
    name = WS_RE.sub(" ", name)
    name = name.strip(". ")
    return name or "未命名"


def ensure_trailing_newline(p: Path) -> None:
    txt = p.read_text(encoding="utf-8")
    if not txt.endswith("\n"):
        p.write_text(txt + "\n", encoding="utf-8")


def json_load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")


def generate_readme(book_dir: Path) -> None:
    meta = book_dir / "_meta"
    status_path = meta / "migration-status.json"
    docs_index_path = meta / "docs-index.json"

    status = json_load(status_path) if status_path.exists() else {}
    docs_index = json_load(docs_index_path) if docs_index_path.exists() else []

    repo_id = status.get("repo_id", "")
    book_name = status.get("book_name", book_dir.name)
    updated_at = status.get("updated_at", "")
    total_docs = status.get("total_docs", len(docs_index))
    migrated_docs = status.get("migrated_docs", None)

    docs_root = book_dir / "docs"
    toc_entry = "docs/000_目录.md" if (docs_root / "000_目录.md").exists() else ""

    lines = [
        f"# {book_name}（语雀迁移）",
        "",
        f"- 来源知识库：`{repo_id}`" if repo_id else "- 来源知识库：",
        f"- 更新时间：{updated_at}" if updated_at else "- 更新时间：",
        f"- 文档数：{total_docs}" if total_docs is not None else "- 文档数：",
    ]
    if migrated_docs is not None:
        lines.append(f"- 已迁移：{migrated_docs}")

    lines.extend(
        [
            "",
            "## 目录入口",
            "",
            f"- `{toc_entry}`" if toc_entry else "- （未生成）",
            "",
            "## 结构说明",
            "",
            "- `docs/`：Markdown 正文（可按语雀 TOC 生成层级目录）",
            "- `_meta/`：语雀 toc / docs 索引 / 迁移状态",
            "",
        ]
    )
    write_text(book_dir / "README.md", "\n".join(lines))


def main() -> None:
    p = argparse.ArgumentParser(description="Normalize filenames/newlines and generate per-book README.")
    p.add_argument("--book-dir", required=True, help="知识库目录，如 knowledge-base/面试训练")
    args = p.parse_args()

    repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd())).resolve()
    book_dir = (repo_root / args.book_dir).resolve()
    docs_root = book_dir / "docs"

    if not docs_root.exists():
        raise SystemExit(f"Missing docs: {docs_root}")

    # Normalize all markdown files newline
    for md in docs_root.rglob("*.md"):
        ensure_trailing_newline(md)

    # (Optional) sanitize filenames in-place within docs tree
    # NOTE: we intentionally avoid auto-renaming here because link rewriting is non-trivial;
    # use remove_slug_prefix_filenames.py / restructure_yuque_toc.py for structural renames.

    generate_readme(book_dir)
    print(f"normalized={docs_root}")


if __name__ == "__main__":
    main()

