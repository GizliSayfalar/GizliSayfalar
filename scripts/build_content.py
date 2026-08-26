from pathlib import Path
import re
import html
import markdown

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "icerik"
OUT = ROOT / "pages" / "icerik"
OUT.mkdir(parents=True, exist_ok=True)

STYLE = """<link rel="stylesheet" href="../../css/style.css">"""

def parse_md(path):
    text = path.read_text(encoding="utf-8")
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = parts[2].strip()
    return meta, body

def layout(title, content):
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(title)} — Gizli Sayfalar">
<title>{html.escape(title)} — Gizli Sayfalar</title>
{STYLE}
</head>
<body>
<header class="site-header"><div class="container nav-wrap">
<a class="brand" href="../../index.html"><img src="../../assets/logo.svg" alt="Gizli Sayfalar"></a>
<a class="button button-light" href="../../index.html">ANA SAYFA →</a>
</div></header>
<main class="reader"><div class="container"><article class="reader-page">{content}</article></div></main>
</body>
</html>"""

all_items = []

for category_dir in sorted(CONTENT.iterdir()):
    if not category_dir.is_dir():
        continue
    category = category_dir.name
    for md_file in sorted(category_dir.glob("*.md")):
        meta, body = parse_md(md_file)
        title = meta.get("baslik", md_file.stem.replace("-", " ").title())
        author = meta.get("yazar", "Gizli Sayfalar")
        date = meta.get("tarih", "")
        cat = meta.get("kategori", category.title())
        excerpt = meta.get("ozet", "")
        rendered = markdown.markdown(body, extensions=["extra", "sane_lists"])
        article = f"""
<div class="meta">{html.escape(cat)} · {html.escape(author)} {("· " + html.escape(date)) if date else ""}</div>
<h1>{html.escape(title)}</h1>
{rendered}
<p><a class="button button-dark" href="../../index.html">← GİZLİ SAYFALAR</a></p>
"""
        out_file = OUT / f"{md_file.stem}.html"
        out_file.write_text(layout(title, article), encoding="utf-8")
        all_items.append((cat, title, author, date, excerpt, out_file.name))

# Generate a simple content index.
cards = []
for cat, title, author, date, excerpt, filename in all_items:
    cards.append(f"""
<article class="card">
<small>{html.escape(cat.upper())}</small>
<h3>{html.escape(title)}</h3>
<p>{html.escape(excerpt)}</p>
<p><small>{html.escape(author)}{(" · " + html.escape(date)) if date else ""}</small></p>
<a class="button button-dark" href="{html.escape(filename)}">OKU →</a>
</article>""")

index_body = f"""
<section class="content-section"><div class="container">
<h2>Yayınlanan eserler</h2>
<div class="cards">
{''.join(cards) if cards else '<div class="notice">Henüz eser yayınlanmadı.</div>'}
</div>
</div></section>
"""
# Use a page-hero wrapper compatible with the site's CSS.
index_html = f"""<!doctype html><html lang="tr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Yazılar — Gizli Sayfalar</title>{STYLE}</head><body>
<header class="site-header"><div class="container nav-wrap">
<a class="brand" href="../../index.html"><img src="../../assets/logo.svg" alt="Gizli Sayfalar"></a>
<a class="button button-light" href="../../index.html">ANA SAYFA →</a>
</div></header>
<main><section class="page-hero"><div class="container"><p class="eyebrow">GİZLİ SAYFALAR</p><h1>Yayınlanan Eserler</h1><p>Şiirler, öyküler ve diğer metinler.</p></div></section>
{index_body}</main></body></html>"""
(OUT / "index.html").write_text(index_html, encoding="utf-8")
