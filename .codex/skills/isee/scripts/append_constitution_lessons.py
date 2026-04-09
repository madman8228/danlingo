#!/usr/bin/env python3
"""Preview and optionally append user-specified lessons to constitution files."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".next",
    ".expo",
    "dist",
    "build",
    "coverage",
}


def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def discover_targets(workspace: Path) -> List[Path]:
    targets: List[Path] = []
    agents = workspace / "AGENTS.md"
    if agents.exists():
        targets.append(agents)

    for md in workspace.rglob("*.md"):
        if should_skip(md):
            continue
        if "CONSTITUTION" in md.name.upper():
            targets.append(md)

    seen = set()
    deduped: List[Path] = []
    for p in targets:
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        deduped.append(p)
    return deduped


def truncate_text(text: str, max_chars: int) -> str:
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "..."


def normalize_lessons(lessons: Iterable[str], max_lessons: int, max_chars: int) -> List[str]:
    out: List[str] = []
    seen = set()
    for raw in lessons:
        text = " ".join(raw.strip().split())
        if not text:
            continue
        text = truncate_text(text, max_chars)
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(text)
        if len(out) >= max_lessons:
            break
    return out


def append_block(content: str, section: str, source_label: str, lessons: List[str]) -> str:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    section_header = f"## {section}"

    lines = [
        f"### {stamp}",
        f"- Source: {source_label}",
    ]
    lines.extend(f"- {lesson}" for lesson in lessons)
    block = "\n".join(lines)

    base = content.rstrip("\n")
    if section_header not in base:
        if base:
            base += "\n\n"
        base += f"{section_header}\n"
        base += block + "\n"
        return base

    anchor = base.rfind(section_header)
    insert_at = len(base)
    return base[:insert_at].rstrip("\n") + "\n\n" + block + "\n"


def print_preview(lessons: List[str], targets: List[Path]) -> None:
    print("[ISEE PREVIEW] Key lessons:")
    for idx, lesson in enumerate(lessons, start=1):
        print(f"{idx}. {lesson}")
    print("")
    print("[ISEE PREVIEW] Target files:")
    for path in targets:
        print(f"- {path}")
    print("")
    print("[ISEE PREVIEW] No files written. Re-run with --apply after user confirmation.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Append lessons to constitution markdown files.")
    parser.add_argument("--workspace", required=True, help="Workspace root path")
    parser.add_argument("--lesson", action="append", default=[], help="Lesson line (repeatable)")
    parser.add_argument("--section", default="ISee Lessons", help="Section title")
    parser.add_argument("--source-label", default="User-specified text", help="Source label")
    parser.add_argument("--max-lessons", type=int, default=3, help="Max key lessons to keep")
    parser.add_argument("--max-chars", type=int, default=90, help="Max chars per lesson line")
    parser.add_argument("--apply", action="store_true", help="Write changes to files")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    if not workspace.exists():
        raise SystemExit(f"Workspace not found: {workspace}")

    lessons = normalize_lessons(
        args.lesson,
        max_lessons=max(1, int(args.max_lessons)),
        max_chars=max(20, int(args.max_chars)),
    )
    if not lessons:
        raise SystemExit("No valid lessons provided. Use --lesson at least once.")

    targets = discover_targets(workspace)
    if not targets:
        print("No constitution targets found (AGENTS.md or *CONSTITUTION*.md).")
        return 0

    print_preview(lessons, targets)
    if not args.apply:
        return 0

    for target in targets:
        content = target.read_text(encoding="utf-8") if target.exists() else ""
        updated = append_block(content, args.section, args.source_label, lessons)
        target.write_text(updated, encoding="utf-8")
        print(f"[UPDATED] {target}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

