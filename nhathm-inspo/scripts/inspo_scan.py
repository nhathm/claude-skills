#!/usr/bin/env python3
"""Hash + dedupe for an Inspiration vault, so Claude never re-reads old material.

Usage:
  inspo_scan.py <Inspiration dir> [--by NAME]                 # scan _inbox/ (images + videos)
  inspo_scan.py <Inspiration dir> --file X [--by NAME]        # one image or video
  inspo_scan.py <Inspiration dir> --url URL [--by NAME]       # one link
  inspo_scan.py <Inspiration dir> --file X --url URL          # video/image with its post link

New ids: INS-YYYYMMDD-HHMM-<who> (local time from config.md `timezone`, default
Asia/Saigon; <who> from --by or config.md `owner`). Unique when several people share
a vault. Old INS-0001-style ids are still indexed for dedupe and never renamed.

Video: extracts ~6 evenly spaced frames into a contact sheet (<file>.sheet.jpg)
with ffmpeg; that sheet is what Claude looks at and what gets committed.

Prints JSON: kind, sha256, phash, url_norm, sheet, next free id, and the closest
existing note (exact sha256, same normalised URL, or pHash Hamming <= 8).
Reads only note frontmatter.
"""
import sys, os, re, json, glob, hashlib, subprocess, unicodedata, datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
try:
    import imagehash
    from PIL import Image
except ImportError:
    sys.exit("pip install --break-system-packages imagehash pillow")

IMG = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".gif")
VID = (".mp4", ".mov", ".m4v", ".webm", ".mkv")
THRESH = 2  # same-template carousel cards sit at 4–8 apart; true re-uploads/recompressions at 0–2
DROP_Q = re.compile(r"^(utm_.*|fbclid|gclid|igshid|mibextid|si|ref|ref_src|s|t|__cft__.*|__tn__)$")

def norm_url(u):
    if not u:
        return ""
    p = urlsplit(u.strip())
    host = p.netloc.lower().removeprefix("www.").removeprefix("m.").removeprefix("mobile.")
    q = urlencode([(k, v) for k, v in parse_qsl(p.query) if not DROP_Q.match(k)])
    return urlunsplit(("https", host, p.path.rstrip("/"), q, ""))

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
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = _val(v)
    return out

def who_slug(name):
    """'Hoàng Minh Nhật' -> 'hmn', 'Rio' -> 'rio'."""
    t = unicodedata.normalize("NFKD", (name or "").replace("đ", "d").replace("Đ", "D"))
    words = re.findall(r"[a-z0-9]+", "".join(c for c in t if not unicodedata.combining(c)).lower())
    if not words:
        return "x"
    return words[0][:8] if len(words) == 1 else "".join(w[0] for w in words)[:8]

def config(root):
    p = f"{root}/config.md"
    return fm(p) if os.path.exists(p) else {}

def now_local(tz):
    try:
        return datetime.datetime.now(ZoneInfo(tz)) if ZoneInfo else datetime.datetime.utcnow()
    except Exception:
        return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))

def index(root):
    idx, ids = [], set()
    for p in glob.glob(f"{root}/notes/*.md") + glob.glob(f"{root}/_archive/*.md"):
        d = fm(p)
        if d.get("id"):
            ids.add(d["id"])
        idx.append({"note": os.path.relpath(p, root), "id": d.get("id"), "title": d.get("title"),
                    "status": d.get("status"), "sha256": d.get("sha256", ""),
                    "phash": d.get("phash", ""), "url": norm_url(d.get("source", ""))})
    return idx, ids

def sheet(video):
    out = os.path.splitext(video)[0] + ".sheet.jpg"
    try:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                    "-of", "csv=p=0", video], capture_output=True, text=True).stdout or 0)
    except ValueError:
        dur = 0
    fps = 6 / dur if dur > 0 else 1
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf",
                    f"fps={fps:.4f},scale=360:-2,tile=3x2", "-frames:v", "1", "-q:v", "4", out],
                   check=False)
    return (out if os.path.exists(out) else None), round(dur, 1)

def phash(img):
    try:
        return str(imagehash.phash(Image.open(img)))
    except Exception:
        return ""

def match(item, idx):
    best = None
    for n in idx:
        if item.get("sha256") and n["sha256"] == item["sha256"]:
            return {**n, "reason": "sha256", "distance": 0}
        if item.get("url_norm") and n["url"] and n["url"] == item["url_norm"]:
            return {**n, "reason": "url", "distance": 0}
        if item.get("phash") and n["phash"]:
            d = imagehash.hex_to_hash(item["phash"]) - imagehash.hex_to_hash(n["phash"])
            if d <= THRESH and (best is None or d < best["distance"]):
                best = {**n, "reason": "phash", "distance": int(d)}
    return best

def describe(path, url=None):
    item = {"kind": "link", "url_norm": norm_url(url)}
    if path:
        ext = os.path.splitext(path)[1].lower()
        item["file"] = path
        item["sha256"] = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if ext in VID:
            item["kind"] = "video"
            sh, dur = sheet(path)
            item.update(sheet=sh, duration_s=dur, phash=phash(sh) if sh else "")
        else:
            item["kind"] = "image"
            item["phash"] = phash(path)
        stem = os.path.splitext(path)[0]
        side = next((stem + e for e in (".md", ".txt") if os.path.exists(stem + e)), None)
        if side:
            item["sidecar"] = side
            if not url:
                m = re.search(r"https?://\S+", open(side, encoding="utf-8").read())
                if m:
                    item["url_norm"] = norm_url(m.group(0))
    return item

def main():
    a = sys.argv
    root = a[1].rstrip("/")
    idx, ids = index(root)
    cfg = config(root)
    who = who_slug(a[a.index("--by") + 1] if "--by" in a else cfg.get("owner", ""))
    base = f"INS-{now_local(cfg.get('timezone') or 'Asia/Saigon'):%Y%m%d-%H%M}-{who}"
    f = a[a.index("--file") + 1] if "--file" in a else None
    u = a[a.index("--url") + 1] if "--url" in a else None
    if f or u:
        items = [describe(f, u)]
    else:
        items = [describe(p) for p in sorted(glob.glob(f"{root}/_inbox/*"))
                 if p.lower().endswith(IMG + VID) and ".sheet." not in p]
    seen = []
    for it in items:
        it["duplicate"] = match(it, idx + seen)
        if not it["duplicate"]:
            nid, n = base, 1
            while nid in ids:
                n += 1
                nid = f"{base}-{n}"
            ids.add(nid)
            it["new_id"] = nid
            seen.append({"note": "(this batch)", "id": it["new_id"], "title": it.get("file") or u,
                         "status": "new", "sha256": it.get("sha256", ""),
                         "phash": it.get("phash", ""), "url": it.get("url_norm", "")})
    print(json.dumps({"known_notes": len(idx), "items": items}, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
