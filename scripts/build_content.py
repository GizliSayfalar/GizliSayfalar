from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]

CONTENT = ROOT / "icerik"
PAGES = ROOT / "pages"
CONTENT_OUT = PAGES / "icerik"

CATEGORIES = {
    "siir": {
        "title": "Şiir",
        "description": "Duyguların en yalın hâli."
    },
    "oyku": {
        "title": "Öykü",
        "description": "Başka hayatların izinde."
    },
    "deneme": {
        "title": "Deneme",
        "description": "Düşünmek, yazmak, anlamak."
    },
    "elestiri": {
        "title": "Eleştiri",
        "description": "Edebiyatın aynasında biz."
    }
}


def parse_file(path):
    """
    Markdown dosyasındaki bilgileri ve metni ayırır.
    """

    text = path.read_text(encoding="utf-8")
    text = text.replace("\r\n", "\n")

    meta = {}
    body = text

    if text.startswith("---\n") and "\n---\n" in text:

        front_matter, body = text[4:].split("\n---\n", 1)

        for line in front_matter.splitlines():

            if ":" in line:

                key, value = line.split(":", 1)

                meta[key.strip()] = (
                    value.strip()
                    .strip('"')
                    .strip("'")
                )

    return meta, body.strip()


def markdown_to_html(text):
    """
    Basit Markdown -> HTML dönüştürücü.
    Harici Python kütüphanesi gerektirmez.
    """

    lines = text.splitlines()

    result = []

    paragraph = []

    in_list = False

    def flush_paragraph():

        nonlocal paragraph

        if not paragraph:
            return

        text_block = "\n".join(paragraph)

        text_block = html.escape(text_block)

        # Kalın
        text_block = re.sub(
            r"\*\*(.+?)\*\*",
            r"<strong>\1</strong>",
            text_block
        )

        # İtalik
        text_block = re.sub(
            r"\*(.+?)\*",
            r"<em>\1</em>",
            text_block
        )

        text_block = text_block.replace(
            "\n",
            "<br>"
        )

        result.append(
            "<p>" + text_block + "</p>"
        )

        paragraph = []

    def close_list():

        nonlocal in_list

        if in_list:

            result.append("</ul>")

            in_list = False

    for line in lines:

        stripped = line.strip()

        # Boş satır
        if not stripped:

            flush_paragraph()
            close_list()

            continue

        # H3
        if stripped.startswith("### "):

            flush_paragraph()
            close_list()

            result.append(
                "<h3>" +
                html.escape(stripped[4:]) +
                "</h3>"
            )

            continue

        # H2
        if stripped.startswith("## "):

            flush_paragraph()
            close_list()

            result.append(
                "<h2>" +
                html.escape(stripped[3:]) +
                "</h2>"
            )

            continue

        # H1
        if stripped.startswith("# "):

            flush_paragraph()
            close_list()

            result.append(
                "<h2>" +
                html.escape(stripped[2:]) +
                "</h2>"
            )

            continue

        # Alıntı
        if stripped.startswith("> "):

            flush_paragraph()
            close_list()

            result.append(
                "<blockquote>" +
                html.escape(stripped[2:]) +
                "</blockquote>"
            )

            continue

        # Liste
        if stripped.startswith("- ") or stripped.startswith("* "):

            flush_paragraph()

            if not in_list:

                result.append("<ul>")

                in_list = True

            result.append(
                "<li>" +
                html.escape(stripped[2:]) +
                "</li>"
            )

            continue

        # Normal satır
        close_list()

        paragraph.append(line)

    flush_paragraph()
    close_list()

    return "\n".join(result)


def create_article(meta, body, category, filename):

    title = meta.get(
        "baslik",
        Path(filename).stem
        .replace("-", " ")
        .replace("_", " ")
        .title()
    )

    author = meta.get(
        "yazar",
        "Gizli Sayfalar"
    )

    date = meta.get(
        "tarih",
        ""
    )

    summary = meta.get(
        "ozet",
        ""
    )

    date_html = ""

    if date:

        date_html = (
            " · " +
            html.escape(date)
        )

    lead_html = ""

    if summary:

        lead_html = (
            '<p class="lead">' +
            html.escape(summary) +
            "</p>"
        )

    article = f"""<!doctype html>

<html lang="tr">

<head>

<meta charset="utf-8">

<meta
    name="viewport"
    content="width=device-width,initial-scale=1"
>

<meta
    name="description"
    content="{html.escape(summary)}"
>

<title>
{html.escape(title)} — Gizli Sayfalar
</title>

<link
    rel="stylesheet"
    href="../../css/style.css"
>

<link
    rel="stylesheet"
    href="../../css/reader.css"
>

</head>


<body class="reader-shell">


<header class="reader-top">

<div class="container reader-bar">

<a
    class="reader-brand"
    href="../../index.html"
>
GİZLİ SAYFALAR
</a>

<span class="reader-title">
{html.escape(title)}
</span>

<a
    class="reader-icon"
    href="../../pages/{'siir' if category == 'Şiir' else 'oyku' if category == 'Öykü' else 'deneme' if category == 'Deneme' else 'elestiri'}.html"
    aria-label="Geri"
>
×
</a>

</div>

</header>


<main>

<div
    class="reader-layout"
    style="display:block;max-width:900px"
>

<article class="mag-page">


<div class="mag-meta">

{html.escape(category)}
·
{html.escape(author)}
{date_html}

</div>


<h1>
{html.escape(title)}
</h1>


{lead_html}


{markdown_to_html(body)}


<p style="margin-top:45px">

<a
    class="button button-dark"
    href="../../pages/{'siir' if category == 'Şiir' else 'oyku' if category == 'Öykü' else 'deneme' if category == 'Deneme' else 'elestiri'}.html"
>
← {html.escape(category.upper())} SAYFASINA DÖN
</a>

</p>


</article>

</div>

</main>


</body>

</html>
"""

    return article


def create_category_page(
    slug,
    category,
    description,
    items
):

    cards = []

    for meta, filename in items:

        title = meta.get(
            "baslik",
            Path(filename)
            .stem
            .replace("-", " ")
            .replace("_", " ")
            .title()
        )

        author = meta.get(
            "yazar",
            "Gizli Sayfalar"
        )

        summary = meta.get(
            "ozet",
            ""
        )

        href = (
            "icerik/" +
            Path(filename).stem +
            ".html"
        )

        card = f"""
<a
    class="card"
    href="{html.escape(href)}"
>

<small>
{html.escape(category.upper())}
</small>

<h3>
{html.escape(title)}
</h3>

<p>
{html.escape(summary)}
</p>

<p>
<small>
{html.escape(author)}
</small>
</p>

</a>
"""

        cards.append(card)

    if cards:

        cards_html = "\n".join(cards)

    else:

        cards_html = """
<div class="notice">

Bu kategoride henüz yayımlanmış
eser bulunmuyor.

</div>
"""

    page = f"""<!doctype html>

<html lang="tr">

<head>

<meta charset="utf-8">

<meta
    name="viewport"
    content="width=device-width,initial-scale=1"
>

<meta
    name="description"
    content="{html.escape(description)}"
>

<title>
{html.escape(category)} — Gizli Sayfalar
</title>

<link
    rel="stylesheet"
    href="../css/style.css"
>

</head>


<body>


<header class="site-header">

<div class="container nav-wrap">


<a
    class="brand"
    href="../index.html"
>

<img
    src="../assets/logo.svg"
    alt="Gizli Sayfalar"
>

</a>


<button
    class="menu-toggle"
    aria-label="Menüyü aç/kapat"
    aria-expanded="false"
>
☰
</button>


<nav
    class="nav"
    aria-label="Ana menü"
>


<a href="../index.html">
Ana Sayfa
</a>


<a href="e-dergi.html">
E-Dergi
</a>


<a
    class="active"
    href="{slug}.html"
>
{html.escape(category)}
</a>


<a href="yazarlar.html">
Yazarlar
</a>


<a href="ekip.html">
Ekip
</a>


<a href="bilgi.html">
Bilgi
</a>


<a
    class="nav-submit"
    href="gonder.html"
>
Eser Gönder
</a>


</nav>


</div>

</header>


<main>


<section class="page-hero">

<div class="container">

<p class="eyebrow">
GİZLİ SAYFALAR
</p>

<h1>
{html.escape(category)}
</h1>

<p>
{html.escape(description)}
</p>

</div>

</section>


<section class="content-section">

<div class="container">


<div class="section-heading">

<h2>
Yayınlanan eserler
</h2>

<span>
{len(items)} eser
</span>

</div>


<div class="cards">

{cards_html}

</div>


</div>

</section>


</main>


<footer class="site-footer">

<div class="container footer-grid">


<div>

<img
    src="../assets/logo.svg"
    class="footer-logo"
    alt="Gizli Sayfalar"
>

<p>
Gizli kalmış kalemler için bir sayfa.
</p>

</div>


<div>

<h3>
Keşfet
</h3>

<a href="e-dergi.html">
E-Dergi
</a>

<a href="siir.html">
Şiir
</a>

<a href="oyku.html">
Öykü
</a>

<a href="yazarlar.html">
Yazarlar
</a>

</div>


<div>

<h3>
Gizli Sayfalar
</h3>

<a href="ekip.html">
Ekip
</a>

<a href="bilgi.html">
Bilgi
</a>

<a href="gonder.html">
Eser Gönder
</a>

</div>


<div>

<h3>
Bizi takip et
</h3>

<div class="socials">

<a
href="https://discord.gg/N4m8sy9b"
target="_blank"
rel="noopener"
>
Discord
</a>

<a
href="https://www.instagram.com/gizlisayfalardergisi?igsi=eDFiaDN3czNrcjU2"
target="_blank"
rel="noopener"
>
Instagram
</a>

<a
href="https://substack.com/@lebklebkral?utm_source=share&utm_medium=android&r=7fsu47"
target="_blank"
rel="noopener"
>
Substack
</a>

<a
href="https://www.reddit.com/r/GizliSayfalar/s/rLZT53cDWE"
target="_blank"
rel="noopener"
>
Reddit
</a>

<a
href="mailto:gizlisayfalardergisi@gmail.com"
>
E-posta
</a>

</div>

</div>


</div>


<div class="container footer-bottom">

<span>
© 2026 Gizli Sayfalar
</span>

<span>
Bağımsız Edebiyat Dergisi
</span>

</div>


</footer>


<script src="../js/main.js"></script>


</body>

</html>
"""

    return page


def build():

    CONTENT_OUT.mkdir(
        parents=True,
        exist_ok=True
    )

    total = 0

    for slug, info in CATEGORIES.items():

        category = info["title"]

        description = info["description"]

        source_folder = (
            CONTENT /
            slug
        )

        source_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        items = []

        for md_file in sorted(
            source_folder.glob("*.md")
        ):

            meta, body = parse_file(
                md_file
            )

            output_file = (
                CONTENT_OUT /
                (md_file.stem + ".html")
            )

            output_file.write_text(
                create_article(
                    meta,
                    body,
                    category,
                    md_file.name
                ),
                encoding="utf-8"
            )

            items.append(
                (
                    meta,
                    md_file.name
                )
            )

            total += 1

        category_file = (
            PAGES /
            (slug + ".html")
        )

        category_file.write_text(
            create_category_page(
                slug,
                category,
                description,
                items
            ),
            encoding="utf-8"
        )

        print(
            f"{category}: {len(items)} eser"
        )

    print(
        f"Toplam {total} eser işlendi."
    )


if __name__ == "__main__":
    build()
