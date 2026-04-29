#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path


SLUG_PREFIX_RE = re.compile(r"^(?P<slug>[a-z0-9]{6,})-", re.I)
MD_LINK_PATH_RE = re.compile(r"(\]\(\./)([^)\n]+?\.md)(\))", re.I)


@dataclass(frozen=True)
class RenamePlan:
    src: Path
    dst: Path
    slug: str


def _casefold_path_key(p: Path) -> str:
    # macOS default filesystem is often case-insensitive
    return str(p).casefold()


def _compute_dst_name(src_name: str) -> tuple[str, str] | None:
    """
    Return (slug, new_filename_without_slug_prefix). None if not match.
    """
    m = SLUG_PREFIX_RE.match(src_name)
    if not m:
        return None
    slug = m.group("slug")
    new_name = SLUG_PREFIX_RE.sub("", src_name, count=1)
    return slug, new_name


def _with_disambiguator(filename: str, slug: str) -> str:
    """
    If name conflicts (case-insensitive), append (slug) before extension.
    """
    p = Path(filename)
    stem = p.stem
    suffix = p.suffix or ".md"
    return f"{stem}（{slug}）{suffix}"


def main() -> None:
    repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd())).resolve()
    p = argparse.ArgumentParser(description="Remove yuque slug prefix in filenames and update docs/000_目录.md links.")
    p.add_argument("--book-dir", required=True, help="知识库目录，如 knowledge-base/面试训练 或 knowledge-base/项目")
    args = p.parse_args()

    book_dir = (repo_root / args.book_dir).resolve()
    docs_root = book_dir / "docs"
    toc_md = docs_root / "000_目录.md"

    if not docs_root.exists():
        raise SystemExit(f"Missing docs dir: {docs_root}")

    # Build current occupancy map (case-insensitive)
    all_md = [p for p in docs_root.rglob("*.md") if p.name != "000_目录.md"]
    occupied_keys = {_casefold_path_key(p): p for p in all_md}

    # Build rename plans first (do not execute yet)
    plans: list[RenamePlan] = []
    for src in sorted(all_md):
        computed = _compute_dst_name(src.name)
        if not computed:
            continue
        slug, base_dst_name = computed
        dst = src.with_name(base_dst_name)
        # If destination equals source (already renamed), skip
        if _casefold_path_key(dst) == _casefold_path_key(src):
            continue

        dst_key = _casefold_path_key(dst)
        if dst_key in occupied_keys and occupied_keys[dst_key].resolve() != src.resolve():
            # Disambiguate (e.g. Promise.md vs promise.md on case-insensitive FS)
            dst = src.with_name(_with_disambiguator(base_dst_name, slug))
            dst_key = _casefold_path_key(dst)
            if dst_key in occupied_keys and occupied_keys[dst_key].resolve() != src.resolve():
                raise RuntimeError(f"仍然冲突，无法重命名：{src} -> {dst}")

        plans.append(RenamePlan(src=src, dst=dst, slug=slug))
        occupied_keys[dst_key] = dst

    # Execute renames and collect mapping for TOC updates (relative to docs_root)
    rel_map: dict[str, str] = {}
    renamed = 0
    for plan in plans:
        # Build map from old basename to new basename
        rel_map[plan.src.name] = plan.dst.name
        plan.src.rename(plan.dst)
        renamed += 1

    # Update toc links basenames (keep directories)
    if toc_md.exists():
        content = toc_md.read_text(encoding="utf-8")

        def repl(m: re.Match[str]) -> str:
            prefix, path, suffix = m.group(1), m.group(2), m.group(3)
            p = Path(path)
            new_name = rel_map.get(p.name)
            if not new_name:
                # If it still contains slug prefix but wasn't renamed (already renamed earlier),
                # strip slug prefix directly.
                computed = _compute_dst_name(p.name)
                if computed:
                    _, base = computed
                    new_name = base
            if new_name:
                new_path = (p.parent / new_name).as_posix()
                return f"{prefix}{new_path}{suffix}"
            return m.group(0)

        new_content = MD_LINK_PATH_RE.sub(repl, content)
        if new_content != content:
            toc_md.write_text(new_content, encoding="utf-8")

    print(f"renamed_files={renamed}")
    print(f"updated_toc={toc_md}")


if __name__ == "__main__":
    main()

