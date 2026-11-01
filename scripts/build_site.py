#!/usr/bin/env python3
"""Generate the homepage, one page per app, 404.html and sitemap.xml from projects.json.

Usage: python3 scripts/build_site.py [--check]

--check exits non-zero if any generated file is out of date (for CI).
"""

from __future__ import annotations

import json
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://asafelobotomy.github.io"
GH = "https://github.com/asafelobotomy/"

CUP = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round" aria-hidden="true"><path d="M17 8h1a4 4 0 0 1 0 8h-1"/>'
    '<path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"/><path d="M10 11.5c-.8-.9-2.4-.4-2.4.9 0 1.1 2.4 '
    '2.6 2.4 2.6s2.4-1.5 2.4-2.6c0-1.3-1.6-1.8-2.4-.9Z" fill="currentColor"/></svg>'
)
DOWNLOAD = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 21h16"/></svg>'
)
GITHUB = (
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5a11.5 11.5 0 0 0-3.6 '
    "22.4c.6.1.8-.3.8-.6v-2c-3.2.7-3.9-1.5-3.9-1.5-.5-1.3-1.3-1.7-1.3-1.7-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 "
    "1.2 1 1.8 2.8 1.3 3.4 1 .1-.8.4-1.3.8-1.6-2.6-.3-5.3-1.3-5.3-5.7 0-1.3.5-2.3 1.2-3.1-.1-.3-.5-1.5.1-3.1 "
    "0 0 1-.3 3.2 1.2a11 11 0 0 1 5.8 0C17.3 4.8 18.3 5 18.3 5c.6 1.6.2 2.8.1 3.1.8.8 1.2 1.9 1.2 3.1 0 "
    "4.4-2.7 5.4-5.3 5.7.4.4.8 1.1.8 2.2v3.2c0 .3.2.7.8.6A11.5 11.5 0 0 0 12 .5Z\"/></svg>"
)

FONTS = (
    "https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400"
    "&family=JetBrains+Mono:wght@400;600&family=Syne:wght@600;700;800&display=swap"
)


def e(value: object) -> str:
    return escape(str(value), quote=True)


def fmt_date(iso: str | None, year: bool = True) -> str:
    if not iso:
        return ""
    d = date.fromisoformat(iso)
    return f"{d.day} {d:%b}" + (f" {d.year}" if year else "")


def icon(app: dict, cls: str = "") -> str:
    if app.get("icon"):
        return f'<img src="{e(app["icon"])}" alt="" loading="lazy" class="{cls}">'
    return f'<span class="glyph {cls}" aria-hidden="true">{e(app["name"][0].upper())}</span>'


def kofi(url: str, label: str = "Support on Ko-fi", extra: str = "") -> str:
    return f'<a class="btn btn-kofi {extra}" href="{e(url)}">{CUP}{e(label)}</a>'


def layout(data: dict, *, title: str, description: str, path: str, body: str) -> str:
    kofi_url = data["kofi"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{SITE_URL}{path}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{SITE_URL}{path}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{FONTS}">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script src="/assets/js/site.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
  <a class="logo" href="/">a<i>safe</i>lobotomy</a>
  <nav class="main" aria-label="Primary">
    <a href="/#apps">Apps</a>
    <a href="/#shipping">Releases</a>
    <a href="/#support">Support</a>
    <a href="{GH.rstrip('/')}">GitHub</a>
  </nav>
  <a class="btn btn-kofi btn-sm" href="{e(kofi_url)}">{CUP}Ko-fi</a>
</div></header>
<main id="main">
{body}
</main>
<footer class="site"><div class="wrap">
  <span>Made by <a href="{GH.rstrip('/')}">@asafelobotomy</a>. Apps are open source under their own licences.</span>
  <span><a href="{e(kofi_url)}">Ko-fi</a> · <a href="{GH.rstrip('/')}?tab=repositories">All repositories</a></span>
</div></footer>
</body>
</html>
"""


def card(app: dict, cats: dict) -> str:
    state = (
        f'<span class="state rel">{e(app["ver"])}</span>'
        if app.get("ver")
        else '<span class="state dev">in development</span>'
    )
    stars = f'<span class="tag">★ {app["stars"]}</span>' if app.get("stars") else ""
    return f"""<a class="card" href="/{app['id']}/" data-cat="{app['cat']}">
      <div class="top">{icon(app)}<div><h3>{e(app['name'])}</h3><div class="cat">{e(cats[app['cat']])}</div></div></div>
      <p>{e(app['tag'])}</p>
      <div class="meta">{state}<span class="tag">{e(app['lang'])}</span>{stars}</div>
    </a>"""


def home(data: dict) -> str:
    apps, cats = data["apps"], data["categories"]
    released = sorted((a for a in apps if a.get("ver")), key=lambda a: a["date"], reverse=True)
    this_month = date.today().strftime("%Y-%m")
    shipped_now = sum(a["date"].startswith(this_month) for a in released)
    month_name = date.today().strftime("%B")

    tickets = "".join(
        f'<a class="ticket" href="/{a["id"]}/">{icon(a)}<div style="min-width:0"><div class="t-name">{e(a["name"])}</div>'
        f'<div class="t-sub">{e(a["tag"])}</div></div><div class="t-ver">{e(a["ver"])}<small>{fmt_date(a["date"], False)}</small></div></a>'
        for a in released[:4]
    )
    chips = "".join(
        f'<button class="chip" type="button" aria-pressed="false" data-filter="{k}">{e(v)}</button>' for k, v in cats.items()
    )
    log = "".join(
        f'<a href="/{a["id"]}/"><span class="l-date">{fmt_date(a["date"])}</span><span><span class="l-name">{e(a["name"])}</span> '
        f'<span class="l-ver">{e(a["ver"])}</span></span><span class="l-what">{e(a["tag"])}</span></a>'
        for a in released
    )
    archive = "".join(
        f'<div><a href="{GH}{e(r["repo"])}">{e(r["repo"])}</a> <span>{e(r["stars"])}</span><br><span>{e(r["description"])}</span></div>'
        for r in data["archive"]
    )
    shipped_fact = f'<span><b>{shipped_now}</b> shipped in {month_name}</span>' if shipped_now else ""

    return f"""<section class="hero"><div class="wrap">
  <div>
    <p class="eyebrow">aSafeLobotomy · Linux-first open source</p>
    <h1 style="margin-top:.9rem">I make things from my brain come <span class="safe">to life.</span></h1>
    <p class="lede"><strong>Desktop apps, CLIs and daemons</strong> for the stuff I actually use: ROM libraries, downloads, antivirus, swap, CPU scheduling, emoji, and my TV.</p>
    <div class="ctas"><a class="btn btn-primary" href="#apps">Browse the apps</a>{kofi(data['kofi'], 'Buy me a coffee', 'btn-ghost')}</div>
    <p class="facts"><span><b>{len(apps)}</b> active apps</span><span><b>{len(released)}</b> with releases</span>{shipped_fact}<span>Rust · Python · Kotlin · TS</span></p>
  </div>
  <div class="tickets"><p class="eyebrow">Now shipping</p>{tickets}</div>
</div></section>

<section class="block" id="apps"><div class="wrap">
  <div class="sec-head"><div><h2>Apps</h2><p>Every active project, each with its own page: screenshots, install steps and docs.</p></div>
    <div class="chips" role="group" aria-label="Filter by category">
      <button class="chip" type="button" aria-pressed="true" data-filter="all">All</button>{chips}
    </div></div>
  <div class="grid">{''.join(card(a, cats) for a in apps)}</div>
</div></section>

<section class="block" id="shipping"><div class="wrap">
  <div class="sec-head"><div><h2>Release log</h2><p>Latest tagged release of each app, newest first.</p></div></div>
  <div class="log">{log}</div>
</div></section>

<section class="block" id="support"><div class="wrap">
  <div class="support">
    <div><p class="eyebrow" style="color:inherit;opacity:.7">Support</p><h2 style="margin-top:.6rem">Keep the brain fed.</h2>
      <p>Everything here is free and open source, made in spare hours. If an app saved you time, a coffee on Ko-fi keeps the next release coming.</p>
      <a class="btn btn-primary" href="{e(data['kofi'])}">{CUP}Support on Ko-fi</a></div>
    <ul>
      <li><b>★</b><span>Star the repos you use. It helps other people find them.</span></li>
      <li><b>!</b><span>File bugs and ideas on each app's GitHub issues.</span></li>
      <li><b>↗</b><span>Share an app page with someone who'd like it.</span></li>
    </ul>
  </div>
</div></section>

<section class="block"><div class="wrap">
  <details class="archive"><summary>Archive · {len(data['archive'])} retired projects</summary>
    <div class="arch">{archive}</div>
  </details>
</div></section>"""


def code(text: str) -> str:
    lines = (f'<span class="c">{e(l)}</span>' if l.lstrip().startswith("#") else e(l) for l in text.split("\n"))
    return "\n".join(lines)


def app_page(app: dict, data: dict) -> str:
    cats, kofi_url = data["categories"], data["kofi"]
    url = GH + app.get("repo", app["id"])
    related = [a for a in data["apps"] if a["cat"] == app["cat"] and a["id"] != app["id"]]

    if app.get("shots"):
        shots = '<div class="gallery">' + "".join(
            f'<figure><img src="{e(s["src"])}" alt="{e(s["caption"])}" loading="lazy"><figcaption>{e(s["caption"])}</figcaption></figure>'
            for s in app["shots"]
        ) + "</div>"
    else:
        shots = '<div class="noshot"><b>Screenshots coming soon.</b> Until then, the README on GitHub has the full tour.</div>'

    segmap = (
        '<div><p class="eyebrow" style="margin-bottom:.6rem">How a download fills in</p>'
        '<div class="segmap" id="segmap" role="img" aria-label="Illustration of segments downloading in parallel"></div></div>'
        if app.get("extra") == "segmap"
        else ""
    )
    themes = (
        f'<section><h2>Community themes</h2><p>The fullscreen mode takes themes from <a href="{GH}romforge-themes">romforge-themes</a>: '
        "console-inspired looks such as NES, SNES, N64, GameCube, Game Boy, Genesis, Saturn, Dreamcast and PlayStation, plus layouts "
        "like grid, cover flow, wheel, shelves and bookshelf. Get them from <b>Settings → Display → Get themes…</b></p></section>"
        if app.get("extra") == "themes"
        else ""
    )
    features = "".join(f'<div><b>{e(f["title"])}</b><span>{e(f["text"])}</span></div>' for f in app["features"])
    tabs = "".join(
        f'<button role="tab" type="button" aria-selected="{str(i == 0).lower()}">{e(t["label"])}</button>'
        for i, t in enumerate(app["install"])
    )
    panels = "".join(
        f'<div role="tabpanel"><p class="eyebrow" style="margin:.4rem 0">{e(t["label"])}</p>'
        f'<div class="codebox"><pre>{code(t["code"])}</pre></div></div>'
        for t in app["install"]
    )
    note = f'<p class="inst-note">{e(app["installNote"])}</p>' if app.get("installNote") else ""
    steps = (
        '<section><h2>Getting started</h2><ol class="steps">'
        + "".join(f"<li><span>{e(s)}</span></li>" for s in app["steps"])
        + "</ol></section>"
        if app.get("steps")
        else ""
    )
    docs = "".join(f'<a href="{e(d["url"])}">{e(d["title"])}<small>{e(d["path"])}</small></a>' for d in app["docs"])
    primary = (
        f'<a class="btn btn-primary" href="{url}/releases/latest">{DOWNLOAD}Download {e(app["ver"])}</a>'
        if app.get("ver")
        else f'<a class="btn btn-primary" href="{url}#readme">{DOWNLOAD}Build from source</a>'
    )
    released = f'<dt>Released</dt><dd>{fmt_date(app["date"])}</dd>' if app.get("date") else ""
    related_html = (
        f'<div><p class="eyebrow" style="margin-bottom:.7rem">Also in {e(cats[app["cat"]])}</p><div class="related">'
        + "".join(f'<a href="/{r["id"]}/">{icon(r)}{e(r["name"])}</a>' for r in related)
        + "</div></div>"
        if related
        else ""
    )

    return f"""<div class="app-head"><div class="wrap">
  <div class="crumb"><a href="/#apps">Apps</a> / {e(cats[app['cat']])}</div>
  <div class="app-title">{icon(app)}<div><h1>{e(app['name'])}</h1><p class="tl">{e(app['tag'])}</p></div></div>
  <div class="ctas">{primary}<a class="btn btn-ghost" href="{url}">{GITHUB}Source on GitHub</a>{kofi(kofi_url, 'Support', 'btn-ghost')}</div>
</div></div>
<div class="wrap app-body">
  <div class="doc">
    <section><h2>What it does</h2><p>{e(app['what'])}</p></section>
    {segmap}
    <section><h2>Screenshots</h2>{shots}</section>
    <section><h2>Features</h2><div class="features">{features}</div></section>
    <section data-tabs><h2>Install</h2>
      <div class="tabs" role="tablist" hidden>{tabs}</div>
      {panels}
      {note}
    </section>
    {steps}
    {themes}
    <section><h2>Documentation</h2><div class="doclinks">
      <a href="{url}#readme">README<small>full reference</small></a>{docs}<a href="{url}/issues">Issues<small>bugs &amp; ideas</small></a>
    </div></section>
  </div>
  <aside class="side">
    <div class="factbox"><dl>
      <dt>Version</dt><dd>{e(app.get('ver') or 'unreleased')}</dd>{released}
      <dt>Built with</dt><dd>{e(app['lang'])}</dd>
      <dt>Licence</dt><dd>{e(app['lic'])}</dd>
      <dt>Runs on</dt><dd>{e(', '.join(app['platforms']))}</dd>
    </dl></div>
    <div class="kofi-card"><p>Free and open source. If {e(app['name'])} helps you, a coffee helps the next release.</p>{kofi(kofi_url)}</div>
    {related_html}
  </aside>
</div>"""


NOT_FOUND = """<section class="hero"><div class="wrap">
  <div><p class="eyebrow">404</p><h1 style="margin-top:.9rem">This page wandered off.</h1>
  <p class="lede">The app may have been renamed or archived.</p>
  <div class="ctas"><a class="btn btn-primary" href="/#apps">See all apps</a></div></div>
</div></section>"""


def build() -> dict[Path, str]:
    data = json.loads((ROOT / "projects.json").read_text())
    desc = "Linux-first desktop apps, CLIs and daemons by aSafeLobotomy: ROM libraries, downloads, security, swap, scheduling, emoji and more."
    out = {
        ROOT / "index.html": layout(data, title="aSafeLobotomy Apps", description=desc, path="/", body=home(data)),
        ROOT / "404.html": layout(data, title="Page not found · aSafeLobotomy", description=desc, path="/404.html", body=NOT_FOUND),
    }
    for app in data["apps"]:
        out[ROOT / app["id"] / "index.html"] = layout(
            data, title=f"{app['name']} · aSafeLobotomy", description=app["tag"], path=f"/{app['id']}/", body=app_page(app, data)
        )
    urls = ["/"] + [f"/{a['id']}/" for a in data["apps"]]
    out[ROOT / "sitemap.xml"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE_URL}{u}</loc></url>\n" for u in urls)
        + "</urlset>\n"
    )
    return out


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    for path, content in build().items():
        if path.exists() and path.read_text() == content:
            continue
        if check:
            stale.append(path.relative_to(ROOT))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            print(f"wrote {path.relative_to(ROOT)}")
    if stale:
        print("out of date, run scripts/build_site.py:", *stale, sep="\n  ")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
