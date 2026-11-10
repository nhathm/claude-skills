#!/usr/bin/env python3
"""Hash + dedupe for the Inspiration vault, so Claude never re-reads old images.

Usage:
  inspo_scan.py <Inspiration dir>            # scan _inbox/, print JSON plan
  inspo_scan.py <Inspiration dir> --file X   # hash one external image (instant mode)

For each image prints: sha256, phash, next free id, and the closest existing
note (exact sha256 match, or pHash Hamming <= 8). Reads only note frontmatter.
"""
import sys, os, re, json, glob, hashlib
try:
    import imagehash
    from PIL import Image
except ImportError:
    sys.exit("pip install --user imagehash pillow")

IMG = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".gif")
THRESH = 8

def fm(path):
    with open(path, encoding="utf-8") as f:
        txt = f.read(4000)
    m = re.match(r"---\n(.*?)\n---", txt, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip().strip('"')
    return out

def index(root):
    idx, max_id = [], 0
    for p in glob.glob(f"{root}/notes/*.md") + glob.glob(f"{root}/_archive/*.md"):
        d = fm(p)
        m = re.match(r"INS-(\d+)", d.get("id", ""))
        if m:
            max_id = max(max_id, int(m.group(1)))
        idx.append({"note": os.path.relpath(p, root), "id": d.get("id"),
                    "title": d.get("title"), "status": d.get("status"),
                    "sha256": d.get("sha256", ""), "phash": d.get("phash", "")})
    return idx, max_id

def hashes(path):
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    try:
        ph = str(imagehash.phash(Image.open(path)))
    except Exception as e:
        ph = ""
    return sha, ph

def match(sha, ph, idx):
    best = None
    for n in idx:
        if n["sha256"] and n["sha256"] == sha:
            return {**n, "reason": "sha256", "distance": 0}
        if ph and n["phash"]:
            d = imagehash.hex_to_hash(ph) - imagehash.hex_to_hash(n["phash"])
            if d <= THRESH and (best is None or d < best["distance"]):
                best = {**n, "reason": "phash", "distance": d}
    return best

def main():
    root = sys.argv[1].rstrip("/")
    idx, max_id = index(root)
    if "--file" in sys.argv:
        files = [sys.argv[sys.argv.index("--file") + 1]]
    else:
        files = sorted(p for p in glob.glob(f"{root}/_inbox/*") if p.lower().endswith(IMG))
    plan, seen = [], []
    for p in files:
        sha, ph = hashes(p)
        dup = match(sha, ph, idx + seen)
        stem = os.path.splitext(p)[0]
        side = next((stem + e for e in (".md", ".txt") if os.path.exists(stem + e)), None)
        item = {"file": os.path.relpath(p, root) if p.startswith(root) else p,
                "sha256": sha, "phash": ph, "sidecar": side and os.path.relpath(side, root),
                "duplicate": dup}
        if not dup:
            max_id += 1
            item["new_id"] = f"INS-{max_id:04d}"
            seen.append({"note": "(this batch)", "id": item["new_id"], "title": p,
                         "status": "new", "sha256": sha, "phash": ph})
        plan.append(item)
    print(json.dumps({"inbox": len(files), "known_notes": len(idx), "items": plan},
                     ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
