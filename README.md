# asafelobotomy.github.io

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/U5R225QZH3)

Personal developer site hosted on [GitHub Pages](https://asafelobotomy.github.io/).

## Live URLs

| Page | URL |
| --- | --- |
| Home | https://asafelobotomy.github.io/ |
| One page per app | `https://asafelobotomy.github.io/<app-id>/` (e.g. [/romforge/](https://asafelobotomy.github.io/romforge/)) |
| cursorAssistant (archived) | https://asafelobotomy.github.io/cursorassistant/ |

## Enable GitHub Pages

1. Open **Settings → Pages** for this repository.
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Choose branch **`main`** (or your default) and folder **`/ (root)`**.
4. Save. The site is available at `https://asafelobotomy.github.io/` after a minute or two.

No Jekyll build is required: `.nojekyll` at the repo root disables Jekyll processing.

## Add or update an app

Everything on the homepage and the app pages comes from [`projects.json`](projects.json).

1. Edit the app's entry in `projects.json` (or add one; `id` becomes its URL). Put icons and screenshots in `assets/img/`.
2. Regenerate the pages:

   ```bash
   python3 scripts/build_site.py
   ```

3. Commit the regenerated `index.html`, `<app-id>/index.html`, `404.html` and `sitemap.xml` with it.

`python3 scripts/build_site.py --check` exits non-zero when a generated file is out of date.
To retire an app, move it from `apps` to `archive` in `projects.json`, rebuild, and delete its folder.

## Keep cursorAssistant install page in sync

The MCP setup page under `cursorassistant/install/` is **generated in this repo** from:

- Template: [cursorassistant/install/index.template.html](https://github.com/asafelobotomy/cursorassistant/blob/master/install/index.template.html) (edit in **cursorassistant** repo)
- Generated here: `cursorassistant/install/index.html`, `deeplinks.json`

**Locally:**

```bash
bash scripts/sync-cursorassistant-install.sh
```

**CI:** [.github/workflows/sync-cursorassistant-install.yml](.github/workflows/sync-cursorassistant-install.yml) runs weekly (and on demand).

See [docs/INSTALL_WEBSITE.md](docs/INSTALL_WEBSITE.md).

## Structure

```text
projects.json              # Apps, categories, archive and Ko-fi link
scripts/build_site.py      # Generates the pages below from projects.json
index.html                 # Homepage (generated)
<app-id>/index.html        # One page per app (generated)
404.html, sitemap.xml      # Generated
assets/css/site.css        # Site styles (light + dark)
assets/css/legacy.css      # Old styles, used by the archived cursorassistant pages
assets/js/site.js          # Filters, install tabs, copy buttons
assets/img/                # App icons and screenshots
cursorassistant/           # Archived project pages, kept so old links work
```

## License

Site content: MIT. Third-party project docs remain under their respective repositories.
