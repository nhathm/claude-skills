#!/usr/bin/env python3
"""One-time, idempotent upgrade of an Inspiration vault to the v2 note format.

Usage: migrate_v2.py <Inspiration dir> --owner NAME [--dry-run]

- frontmatter `author:` -> `source_author:`; adds `captured_by: NAME` when missing
- English section headings -> Vietnamese (Rio note/Summary/Analysis/Research/Next action
  -> Ghi chú/Tóm tắt/Phân tích/Nguồn/Việc tiếp theo)
- status to-try -> inbox, tried -> done
Ids and file names are left alone. Prints a JSON summary.
"""
import sys, re, glob, json

HEAD = {"Rio note": "Ghi chú", "Summary": "Tóm tắt", "Analysis": "Phân tích",
        "Research": "Nguồn", "Next action": "Việc tiếp theo"}
STATUS = {"to-try": "inbox", "tried": "done"}


def upgrade(txt, owner):
    m = re.match(r"(---\n)(.*?)(\n---\n?)(.*)", txt, re.S)
    if not m:
        return txt
    head, body = m.group(2), m.group(4)
    head = re.sub(r"^author:", "source_author:", head, flags=re.M)
    if not re.search(r"^captured_by:", head, re.M):
        if re.search(r"^source_author:.*$", head, re.M):
            head = re.sub(r"^(source_author:.*)$", rf"\1\ncaptured_by: {owner}", head, count=1, flags=re.M)
        else:
            head += f"\ncaptured_by: {owner}"
    head = re.sub(r"^status:\s*(\S+)", lambda s: "status: " + STATUS.get(s.group(1), s.group(1)), head, count=1, flags=re.M)
    for en, vi in HEAD.items():
        body = re.sub(rf"^## {re.escape(en)}\s*$", f"## {vi}", body, flags=re.M)
    return m.group(1) + head + m.group(3) + body


def main():
    a = sys.argv
    root = a[1].rstrip("/")
    owner = a[a.index("--owner") + 1]
    dry = "--dry-run" in a
    changed = []
    for p in sorted(glob.glob(f"{root}/notes/*.md") + glob.glob(f"{root}/_archive/*.md")):
        old = open(p, encoding="utf-8").read()
        new = upgrade(old, owner)
        if new != old:
            changed.append(p.rsplit("/", 1)[-1])
            if not dry:
                open(p, "w", encoding="utf-8").write(new)
    print(json.dumps({"changed": len(changed), "dry_run": dry, "files": changed[:5]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
