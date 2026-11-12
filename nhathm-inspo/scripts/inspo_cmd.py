#!/usr/bin/env python3
"""Small, deterministic edits on an Inspiration vault, so Claude never rewrites notes by hand.

Usage:
  inspo_cmd.py <Inspiration dir> find <query> [--limit 5]
      Match <query> against id (exact or suffix, e.g. 0012 / 20261112-2119) or, word by
      word, against title, tags, category, topic, source_author, captured_by.
      Reads frontmatter only. Prints JSON list (notes/ first, then _archive/).
  inspo_cmd.py <Inspiration dir> status <id> <raw|inbox|later|done|dropped>
      Sets `status:` and logs "- YYYY-MM-DD: trạng thái → X" at the end of `## Ghi chú`.
  inspo_cmd.py <Inspiration dir> append <id> <text>
      Adds "- YYYY-MM-DD: <text>" at the end of `## Ghi chú`.

Exit code 2 with JSON {"error": ...} when the id is not found or is ambiguous.
"""
import sys, os, re, json, glob, datetime, unicodedata

STATUSES = ("raw", "inbox", "later", "done", "dropped", "archived")
FIELDS = ("title", "tags", "category", "topic", "source_author", "captured_by")


def fold(s):
    s = unicodedata.normalize("NFKD", str(s).replace("đ", "d").replace("Đ", "D"))
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def _val(v):
    v = v.strip()
    if v.startswith('"'):
        end = v.find('"', 1)
        return v[1:end] if end > 0 else v.strip('"')
    return v.split(" #", 1)[0].strip()

def fm(path):
    with open(path, encoding="utf-8") as f:
        txt = f.read(4000)
    m = re.match(r"---\n(.*?)\n---", txt, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                out[k.strip()] = _val(v)
    return out


def notes(root):
    for p in sorted(glob.glob(f"{root}/notes/*.md")) + sorted(glob.glob(f"{root}/_archive/*.md")):
        d = fm(p)
        if d.get("id"):
            yield p, d


def row(root, p, d):
    return {"id": d["id"], "title": d.get("title", ""), "status": d.get("status", ""),
            "category": d.get("category", ""), "captured": d.get("captured", ""),
            "note": os.path.relpath(p, root)}


def by_id(root, ref):
    ref = ref.strip().upper().removeprefix("INS-")
    hits = [(p, d) for p, d in notes(root)
            if d["id"].upper() == "INS-" + ref or d["id"].upper().endswith(ref)
            or d["id"].upper().removeprefix("INS-").lstrip("0") == ref.lstrip("0")]
    exact = [h for h in hits if h[1]["id"].upper() == "INS-" + ref]
    return exact or hits


def find(root, q, limit):
    q = q.strip()
    hits = by_id(root, q) if re.fullmatch(r"(?i)(ins-)?[\w-]*\d[\w-]*", q) else []
    if not hits:
        words = fold(q).split()
        hits = [(p, d) for p, d in notes(root)
                if all(w in fold(" ".join(d.get(f, "") for f in FIELDS)) for w in words)]
    return [row(root, p, d) for p, d in hits[:limit]], len(hits)


def one(root, ref):
    hits = by_id(root, ref)
    if len(hits) != 1:
        print(json.dumps({"error": "not found" if not hits else "ambiguous",
                          "candidates": [row(root, p, d) for p, d in hits[:5]]}, ensure_ascii=False))
        sys.exit(2)
    return hits[0]


def log_line(path, text):
    txt = open(path, encoding="utf-8").read()
    line = f"- {datetime.date.today():%Y-%m-%d}: {text}"
    m = re.search(r"^## Ghi chú[^\n]*\n", txt, re.M)
    if not m:  # no section yet: add one right after the frontmatter/embed block
        fm_end = re.match(r"---\n.*?\n---\n", txt, re.S).end()
        nxt = re.search(r"^## ", txt[fm_end:], re.M)
        at = fm_end + (nxt.start() if nxt else len(txt) - fm_end)
        txt = txt[:at].rstrip("\n") + f"\n\n## Ghi chú\n{line}\n\n" + txt[at:]
    else:
        nxt = re.search(r"^## ", txt[m.end():], re.M)
        at = m.end() + nxt.start() if nxt else len(txt)
        txt = txt[:at].rstrip("\n") + "\n" + line + ("\n\n" if nxt else "\n") + txt[at:]
    open(path, "w", encoding="utf-8").write(txt)


def main():
    a = sys.argv
    if len(a) < 4:
        sys.exit(__doc__)
    root, cmd = a[1].rstrip("/"), a[2]
    if cmd == "find":
        limit = int(a[a.index("--limit") + 1]) if "--limit" in a else 5
        q = " ".join(x for i, x in enumerate(a[3:], 3) if x != "--limit" and a[i - 1] != "--limit")
        res, total = find(root, q, limit)
        print(json.dumps({"total": total, "items": res}, ensure_ascii=False, indent=1))
    elif cmd == "status":
        new = a[4]
        if new not in STATUSES:
            sys.exit(f"status must be one of {STATUSES}")
        p, d = one(root, a[3])
        txt = open(p, encoding="utf-8").read()
        txt = re.sub(r"^status:.*$", f"status: {new}", txt, count=1, flags=re.M)
        open(p, "w", encoding="utf-8").write(txt)
        log_line(p, f"trạng thái {d.get('status', '?')} → {new}")
        print(json.dumps({**row(root, p, d), "status": new, "was": d.get("status")}, ensure_ascii=False))
    elif cmd == "append":
        p, d = one(root, a[3])
        log_line(p, " ".join(a[4:]).strip())
        print(json.dumps(row(root, p, d), ensure_ascii=False))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
