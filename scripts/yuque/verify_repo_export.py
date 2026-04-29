#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any


LINK_RE = re.compile(r"\]\(\./(?P<path>[^)\n]+?\.md)\)")


def json_load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    p = argparse.ArgumentParser(description="Verify exported Yuque knowledge-base consistency.")
    p.add_argument("--book-dir", required=True, help="知识库目录，如 knowledge-base/面试训练")
    args = p.parse_args()

    repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd())).resolve()
    book_dir = (repo_root / args.book_dir).resolve()
    docs_root = book_dir / "docs"
    meta_root = book_dir / "_meta"

    if not docs_root.exists():
        raise SystemExit(f"Missing docs: {docs_root}")
    if not meta_root.exists():
        raise SystemExit(f"Missing _meta: {meta_root}")

    docs_index_path = meta_root / "docs-index.json"
    status_path = meta_root / "migration-status.json"
    toc_md_path = docs_root / "000_目录.md"

    if not docs_index_path.exists():
        raise SystemExit(f"Missing {docs_index_path}")
    if not status_path.exists():
        raise SystemExit(f"Missing {status_path}")
    if not toc_md_path.exists():
        raise SystemExit(f"Missing {toc_md_path}")

    docs_index = json_load(docs_index_path)
    status = json_load(status_path)

    # 1) list_docs count == local md count (excluding 000_目录.md)
    local_docs = [p for p in docs_root.rglob("*.md") if p.name != "000_目录.md"]
    if len(docs_index) != len(local_docs):
        raise RuntimeError(f"文档数量不一致：docs-index={len(docs_index)} local_md={len(local_docs)}")

    # 2) migration-status json parse & counts
    total_docs = int(status.get("total_docs", -1))
    migrated_docs = int(status.get("migrated_docs", -1))
    remaining_docs = int(status.get("remaining_docs", -1))
    if total_docs != len(docs_index):
        raise RuntimeError(f"migration-status.total_docs 不一致：{total_docs} vs {len(docs_index)}")
    if migrated_docs != len(docs_index) or remaining_docs != 0:
        raise RuntimeError(f"migration-status 计数异常：migrated={migrated_docs} remaining={remaining_docs}")

    # 3) TOC links all exist
    toc = toc_md_path.read_text(encoding="utf-8")
    broken: list[str] = []
    for m in LINK_RE.finditer(toc):
        rel = m.group("path")
        pth = docs_root / rel
        if not pth.exists():
            broken.append(rel)
    if broken:
        raise RuntimeError(f"目录存在断链（示例前10个）：{broken[:10]}")

    print("OK")


if __name__ == "__main__":
    main()

