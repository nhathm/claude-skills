#!/usr/bin/env python3
"""Build a single-file HTML gallery of Rio's Inspiration vault.

Usage: python3 -I build_report.py <vault>/Inspiration --out <file.html>

Reads only note frontmatter + sections and the first attachment per note (shrunk to a
thumbnail and inlined as a data URI). No network, no AI. Output is self-contained and
meets the claude.ai Artifact page contract (no <html>/<head>/<body>, theme tokens).
"""
import argparse, base64, datetime, glob, html, io, json, os, re, sys

try:
    from PIL import Image
except ImportError:
    Image = None

SECTIONS = ["Rio note", "Summary", "Analysis", "Research", "Next action"]
THUMB_W = 480


def parse_note(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n?(.*)", txt, re.S)
    fm, body = {}, txt
    if m:
        body = m.group(2)
        for line in m.group(1).splitlines():
            if ":" not in line or line.startswith(" "):
                continue
            k, v = line.split(":", 1)
            v = v.split(" #", 1)[0].strip()
            if v.startswith("[") and v.endswith("]"):
                v = [t.strip().strip('"') for t in v[1:-1].split(",") if t.strip()]
            else:
                v = v.strip('"')
            fm[k.strip()] = v
    sec, cur = {}, None
    for line in body.splitlines():
        h = re.match(r"##\s+(.+)", line)
        if h:
            cur = h.group(1).strip()
            sec[cur] = []
        elif cur:
            sec[cur].append(line)
    sec = {k: "\n".join(v).strip() for k, v in sec.items()}
    embeds = re.findall(r"!\[\[([^|\]]+)", body)
    return fm, sec, embeds


def thumb(path):
    if not path or not os.path.exists(path):
        return ""
    if Image is None:
        raw = open(path, "rb").read()
        return "data:image/jpeg;base64," + base64.b64encode(raw).decode()
    im = Image.open(path).convert("RGB")
    if im.width > THUMB_W:
        im = im.resize((THUMB_W, round(im.height * THUMB_W / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=72, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def inline_md(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[\[([^|\]]+)(?:\|[^\]]*)?\]\]", r"<span class='wl'>\1</span>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(https?://[^\s<)]+)", r"<a href='\1' target='_blank' rel='noopener'>\1</a>", s)
    return s


def md_block(s):
    """Tiny markdown: bullets, checkboxes, paragraphs."""
    out, lst = [], None
    for line in s.splitlines():
        t = line.strip()
        cb = re.match(r"- \[( |x)\] (.*)", t)
        li = re.match(r"[-*] (.*)", t)
        if cb or li:
            if lst is None:
                out.append("<ul>"); lst = True
            if cb:
                done = cb.group(1) == "x"
                out.append(f"<li class='todo{' done' if done else ''}'><span class='box' aria-hidden='true'></span>{inline_md(cb.group(2))}</li>")
            else:
                out.append(f"<li>{inline_md(li.group(1))}</li>")
            continue
        if lst:
            out.append("</ul>"); lst = None
        if t:
            out.append(f"<p>{inline_md(t)}</p>")
    if lst:
        out.append("</ul>")
    return "".join(out)


def load_categories(ins):
    """Read the slug -> name table from Inspiration/categories.md (order kept)."""
    cats = {}
    p = f"{ins}/categories.md"
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            m = re.match(r"\|\s*([a-z0-9-]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|", line)
            if m and m.group(1) != "slug" and re.search(r"[a-z]", m.group(1)):
                cats[m.group(1)] = {"name": m.group(2), "desc": m.group(3)}
    return cats


def build(ins):
    items = []
    for p in sorted(glob.glob(f"{ins}/notes/*.md")):
        fm, sec, embeds = parse_note(p)
        if not fm.get("id"):
            continue
        img = next((e for e in embeds if re.search(r"\.(jpe?g|png|webp|gif)$", e, re.I)), None)
        todos = re.findall(r"- \[( |x)\]", sec.get("Next action", ""))
        items.append({
            "id": fm.get("id"), "title": fm.get("title", ""), "status": fm.get("status", ""),
            "kind": fm.get("kind", ""), "type": fm.get("type", ""), "topic": fm.get("topic", ""),
            "effort": fm.get("effort", ""), "review": fm.get("review", ""),
            "captured": fm.get("captured", ""), "author": fm.get("author", ""),
            "source": fm.get("source", ""), "tags": fm.get("tags") or [],
            "category": (fm.get("category") if isinstance(fm.get("category"), list) else [fm["category"]] if fm.get("category") else ["khac"]),
            "dup": re.sub(r"[\[\]\"]", "", fm.get("duplicate_of", "") or ""),
            "thumb": thumb(f"{ins}/attachments/{img}") if img else "",
            "more": max(0, len([e for e in embeds if re.search(r'\.(jpe?g|png|webp)$', e, re.I)]) - 1),
            "todo_open": todos.count(" "), "todo_done": todos.count("x"),
            "html": {k: md_block(sec[k]) for k in SECTIONS if sec.get(k)},
        })
    return items


TEMPLATE = r"""<title>Inspiration Vault</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Layout: sticky filter bar over a responsive card grid; a side sheet opens one idea. */
:root{
  --bg:#f5f6f3; --surface:#ffffff; --ink:#1b1f1d; --muted:#5e6762; --line:#dfe3dd;
  --accent:#2f6b4f; --accent-soft:#e3efe8; --warn:#a45a12; --warn-soft:#f6e9d9;
  --font:"Be Vietnam Pro",ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#121614; --surface:#1a201d; --ink:#e7ebe8; --muted:#9aa49f; --line:#2b332f;
  --accent:#7cc4a0; --accent-soft:#1f3329; --warn:#e3a35e; --warn-soft:#352717; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#121614; --surface:#1a201d; --ink:#e7ebe8; --muted:#9aa49f; --line:#2b332f;
  --accent:#7cc4a0; --accent-soft:#1f3329; --warn:#e3a35e; --warn-soft:#352717; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:15px/1.55 var(--font);
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 48px}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.wrap{max-width:1240px;margin:0 auto}
header{padding-block:28px 12px;display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:12px 24px}
h1{font-size:28px;line-height:1.15;margin:0;font-weight:700;letter-spacing:-.01em;text-wrap:balance}
.sub{color:var(--muted);margin:4px 0 0;font-size:14px}
.stats{display:flex;gap:8px;flex-wrap:wrap}
.stat{border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:4px 12px;font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}
.stat b{color:var(--ink);font-weight:600}
.stat.due{border-color:var(--warn);color:var(--warn);background:var(--warn-soft)}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);padding-block:10px;border-bottom:1px solid var(--line);display:grid;gap:8px}
.row{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.row .lbl{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);width:58px;flex:none}
input[type=search],select{font:inherit;font-size:14px;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:7px 10px}
input[type=search]{flex:1 1 220px;min-width:0}
.chip{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:3px 10px;cursor:pointer}
.chip[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:var(--surface)}
.chip:focus-visible,.card:focus-visible,button:focus-visible,select:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.count{color:var(--muted);font-size:13px;margin:14px 0 10px;font-variant-numeric:tabular-nums}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px}
.card{all:unset;cursor:pointer;display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden;min-width:0;transition:transform .15s,border-color .15s}
.card:hover{border-color:var(--accent);transform:translateY(-2px)}
.thumb{aspect-ratio:4/3;max-width:100%;background:var(--line) center top/cover no-repeat;position:relative}
.thumb .more{position:absolute;right:8px;bottom:8px;background:rgba(0,0,0,.6);color:#fff;font-size:11px;border-radius:6px;padding:1px 6px}
.noimg{display:grid;place-items:center;color:var(--muted);font-family:var(--mono);font-size:13px}
.cb{padding:10px 12px 12px;display:grid;gap:6px;min-width:0}
.meta{display:flex;gap:6px;align-items:center;font-size:12px;color:var(--muted);flex-wrap:wrap}
.id{font-family:var(--mono);font-size:11.5px;color:var(--muted)}
.ct{font-weight:600;font-size:14.5px;line-height:1.35;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.pill{font-size:11.5px;border-radius:999px;padding:1px 8px;background:var(--accent-soft);color:var(--accent)}
.pill.st-raw,.pill.st-archived{background:var(--line);color:var(--muted)}
.pill.st-to-try{background:var(--warn-soft);color:var(--warn)}
.cats{display:flex;gap:4px;flex-wrap:wrap}.cat{font-size:11.5px;border:1px solid var(--line);border-radius:4px;padding:0 6px;color:var(--ink)}
.pill.dup{background:var(--line);color:var(--muted)}
.duefl{color:var(--warn);font-weight:600}
.empty{padding:48px 0;text-align:center;color:var(--muted)}
/* sheet */
.scrim{position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:20}
.sheet{position:fixed;top:0;right:0;bottom:0;width:min(680px,100%);background:var(--surface);z-index:21;overflow:auto;border-left:1px solid var(--line);
  padding:calc(20px + env(safe-area-inset-top,0px)) max(20px,env(safe-area-inset-right,0px)) calc(32px + env(safe-area-inset-bottom,0px)) 20px}
.sheet img{display:block;width:100%;border-radius:8px;border:1px solid var(--line)}
.sheet h2{font-size:21px;line-height:1.3;margin:10px 0 6px;text-wrap:balance}
.sheet h3{font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:22px 0 6px}
.sheet p{margin:0 0 8px}.sheet ul{margin:0;padding-left:18px}.sheet li{margin:3px 0}
.sheet li.todo{list-style:none;margin-left:-18px;display:flex;gap:8px}
.box{flex:none;width:14px;height:14px;border:1.5px solid var(--muted);border-radius:3px;margin-top:4px}
.todo.done .box{background:var(--accent);border-color:var(--accent)}.todo.done{color:var(--muted);text-decoration:line-through}
.sheet a{color:var(--accent);overflow-wrap:anywhere}
code{font-family:var(--mono);font-size:.88em;background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:0 4px;overflow-wrap:anywhere}
.wl{color:var(--accent);font-weight:500}
.close{position:sticky;top:0;float:right;font:inherit;font-size:14px;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:4px 12px;cursor:pointer}
.kv{display:grid;grid-template-columns:auto 1fr;gap:2px 14px;font-size:13.5px;margin-top:8px}.kv dt{color:var(--muted)}.kv dd{margin:0;min-width:0;overflow-wrap:anywhere}
footer{margin-top:28px;color:var(--muted);font-size:12.5px}
@media (prefers-reduced-motion:reduce){.card{transition:none}.card:hover{transform:none}}
@media (max-width:480px){h1{font-size:23px}.row .lbl{width:100%}}
</style>

<div class="wrap">
  <header>
    <div><h1>Inspiration Vault</h1><p class="sub" id="sub"></p></div>
    <div class="stats" id="stats"></div>
  </header>
  <div class="bar">
    <div class="row">
      <input type="search" id="q" placeholder="Tìm tiêu đề, tag, tác giả…" aria-label="Tìm kiếm">
      <select id="sort" aria-label="Sắp xếp">
        <option value="new">Mới nhất</option><option value="review">Review sớm nhất</option><option value="id">Theo ID</option>
      </select>
    </div>
    <div class="row" id="f-category"><span class="lbl">Category</span></div>
    <div class="row" id="f-topic"><span class="lbl">Chủ đề</span></div>
    <div class="row" id="f-type"><span class="lbl">Loại</span></div>
    <div class="row" id="f-status"><span class="lbl">Trạng thái</span></div>
  </div>
  <p class="count" id="count"></p>
  <div class="grid" id="grid"></div>
  <p class="empty" id="empty" hidden>Không có ý tưởng nào khớp bộ lọc.</p>
  <footer id="foot"></footer>
</div>
<div class="scrim" id="scrim" hidden></div>
<aside class="sheet" id="sheet" hidden role="dialog" aria-modal="true" aria-labelledby="sh-title"></aside>

<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent);
const items=D.items, today=D.today;
const L={topic:{"ai-agent":"AI agent","personal-ai":"AI cá nhân","claude-skill":"Claude skill",video:"Video",dev:"Dev",ios:"iOS",design:"Design",other:"Khác"},
 type:{skill:"Skill",project:"Project",tool:"Tool","design-pattern":"Design pattern",idea:"Ý tưởng",setup:"Setup"},
 status:{raw:"Raw",inbox:"Inbox","to-try":"Sẽ thử",tried:"Đã thử",archived:"Lưu trữ"},
 effort:{"15-phut":"15 phút","1-buoi":"1 buổi","1-tuan":"1 tuần"}};
L.category=Object.fromEntries(Object.entries(D.categories||{}).map(([k,v])=>[k,v.name]));
const lab=(g,v)=>(L[g]&&L[g][v])||v||'—';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const isDue=it=>it.review&&it.review<=today&&!['archived','tried'].includes(it.status);
const sel={category:new Set(),topic:new Set(),type:new Set(),status:new Set()};
let st={};try{st=JSON.parse(localStorage.getItem('inspo-filters')||'{}')}catch(e){}
for(const g in sel)(st[g]||[]).forEach(v=>sel[g].add(v));
const qEl=document.getElementById('q'),sortEl=document.getElementById('sort');
if(st.sort)sortEl.value=st.sort;
function save(){try{localStorage.setItem('inspo-filters',JSON.stringify({category:[...sel.category],topic:[...sel.topic],type:[...sel.type],status:[...sel.status],sort:sortEl.value}))}catch(e){}}

function chips(g){
  const box=document.getElementById('f-'+g), counts={};
  items.forEach(it=>[].concat(it[g]).forEach(v=>{counts[v]=(counts[v]||0)+1}));
  const keys=g==='category'?[...new Set([...Object.keys(L.category),...Object.keys(counts)])]:Object.keys(counts).sort((a,b)=>counts[b]-counts[a]);
  keys.forEach(v=>{
    const b=document.createElement('button');b.className='chip';b.type='button';b.id=`chip-${g}-${v}`;
    b.textContent=`${lab(g,v)} · ${counts[v]||0}`;if(g==='category'&&D.categories[v])b.title=D.categories[v].desc;b.setAttribute('aria-pressed',sel[g].has(v));
    b.onclick=()=>{sel[g].has(v)?sel[g].delete(v):sel[g].add(v);b.setAttribute('aria-pressed',sel[g].has(v));save();render()};
    box.appendChild(b)});
}
function stats(){
  const n=s=>items.filter(i=>i.status===s).length, due=items.filter(isDue).length;
  document.getElementById('stats').innerHTML=
    `<span class="stat"><b>${items.length}</b> ý tưởng</span><span class="stat"><b>${n('inbox')}</b> inbox</span>`+
    `<span class="stat"><b>${n('to-try')}</b> sẽ thử</span>`+(due?`<span class="stat due"><b>${due}</b> đến hạn review</span>`:'');
  document.getElementById('sub').textContent=`Cập nhật ${D.generated} · nguồn: claude-vault/Inspiration`;
  document.getElementById('foot').textContent=`Trang chỉ để xem. Sửa ý tưởng trong Obsidian; chạy lại nhathm-inspo-report để cập nhật.`;
}
function match(it){
  for(const g in sel) if(sel[g].size&&![].concat(it[g]).some(v=>sel[g].has(v)))return false;
  const q=qEl.value.trim().toLowerCase(); if(!q)return true;
  return [it.id,it.title,it.author,it.topic,it.type,...it.category.map(c=>lab('category',c)),...(it.tags||[])].join(' ').toLowerCase().includes(q);
}
function render(){
  const s=sortEl.value;
  const list=items.filter(match).sort((a,b)=>s==='review'?(a.review||'9').localeCompare(b.review||'9'):s==='id'?a.id.localeCompare(b.id):(b.captured+b.id).localeCompare(a.captured+a.id));
  document.getElementById('count').textContent=`${list.length} / ${items.length} ý tưởng`;
  document.getElementById('empty').hidden=list.length>0;
  document.getElementById('grid').innerHTML=list.map(it=>`
   <button class="card" type="button" data-id="${esc(it.id)}">
    <div class="thumb${it.thumb?'':' noimg'}" ${it.thumb?`style="background-image:url('${it.thumb}')"`:''}>${it.thumb?'':esc(it.kind||'link')}${it.more?`<span class="more">+${it.more} ảnh</span>`:''}</div>
    <div class="cb">
     <div class="meta"><span class="id">${esc(it.id)}</span><span class="pill st-${esc(it.status)}">${esc(lab('status',it.status))}</span>${it.dup?'<span class="pill dup">trùng</span>':''}</div>
     <div class="ct">${esc(it.title)}</div>
     <div class="cats">${it.category.map(c=>`<span class="cat">${esc(lab('category',c))}</span>`).join('')}</div>
     <div class="meta"><span>${esc(lab('topic',it.topic))}</span>·<span>${esc(lab('type',it.type))}</span>·<span>${esc(lab('effort',it.effort))}</span>
      ${it.todo_open?`·<span>${it.todo_open} việc</span>`:''}${isDue(it)?'·<span class="duefl">đến hạn</span>':''}</div>
    </div></button>`).join('');
}
const sheet=document.getElementById('sheet'),scrim=document.getElementById('scrim');let lastFocus=null;
const NAMES={"Rio note":"Ghi chú của Rio","Summary":"Tóm tắt","Analysis":"Phân tích","Research":"Nguồn","Next action":"Việc tiếp theo"};
function openSheet(id){
  const it=items.find(i=>i.id===id);if(!it)return;lastFocus=document.activeElement;
  sheet.innerHTML=`<button class="close" type="button" id="close">Đóng</button>
   <span class="id">${esc(it.id)}</span>
   <h2 id="sh-title">${esc(it.title)}</h2>
   <dl class="kv"><dt>Trạng thái</dt><dd>${esc(lab('status',it.status))}${it.dup?` · trùng ${esc(it.dup)}`:''}</dd>
    <dt>Category</dt><dd>${it.category.map(c=>esc(lab('category',c))).join(', ')}</dd>
    <dt>Chủ đề</dt><dd>${esc(lab('topic',it.topic))} · ${esc(lab('type',it.type))} · ${esc(lab('effort',it.effort))}</dd>
    <dt>Nguồn</dt><dd>${it.source?`<a href="${esc(it.source)}" target="_blank" rel="noopener">${esc(it.source)}</a>`:esc(it.author||'—')}</dd>
    <dt>Lưu / review</dt><dd>${esc(it.captured)} · <span class="${isDue(it)?'duefl':''}">${esc(it.review||'—')}</span></dd>
    ${it.tags.length?`<dt>Tag</dt><dd>${it.tags.map(t=>'#'+esc(t)).join(' ')}</dd>`:''}</dl>
   ${it.thumb?`<h3>Ảnh</h3><img src="${it.thumb}" alt="">`:''}
   ${Object.entries(it.html).map(([k,v])=>`<h3>${NAMES[k]||k}</h3>${v}`).join('')}`;
  sheet.hidden=scrim.hidden=false;document.getElementById('close').onclick=closeSheet;document.getElementById('close').focus();
  try{history.replaceState(null,'','#'+id)}catch(e){}
}
function closeSheet(){sheet.hidden=scrim.hidden=true;try{history.replaceState(null,'',location.pathname+location.search)}catch(e){};lastFocus&&lastFocus.focus()}
document.getElementById('grid').onclick=e=>{const c=e.target.closest('.card');c&&openSheet(c.dataset.id)};
scrim.onclick=closeSheet;document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!sheet.hidden)closeSheet()});
qEl.oninput=render;sortEl.onchange=()=>{save();render()};
['category','topic','type','status'].forEach(chips);stats();render();
if(location.hash.length>1)openSheet(decodeURIComponent(location.hash.slice(1)));
</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ins", help="path to <vault>/Inspiration")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    items = build(a.ins)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    data = {"categories": load_categories(a.ins), "items": items, "today": now.strftime("%Y-%m-%d"), "generated": now.strftime("%Y-%m-%d %H:%M")}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(TEMPLATE.replace("__DATA__", blob))
    size = os.path.getsize(a.out)
    print(json.dumps({"out": a.out, "items": len(items), "bytes": size,
                      "due": sum(1 for i in items if i["review"] and i["review"] <= data["today"])}))
    if size > 15_000_000:
        sys.exit("report exceeds 15MB; lower THUMB_W")


if __name__ == "__main__":
    main()
