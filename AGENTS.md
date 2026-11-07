# asafelobotomy.github.io

Static personal developer site on GitHub Pages (branch `main`, root folder, `.nojekyll`, no Jekyll build). The homepage and per-app pages are generated from `projects.json`.

## Commands
- Regenerate pages: `python3 scripts/build_site.py`. Check for drift (exits non-zero if stale): `python3 scripts/build_site.py --check`.
- Preview locally: `python3 -m http.server 8411` (see `.claude/launch.json`).
- cursorAssistant install page: `bash scripts/sync-cursorassistant-install.sh` (clones the cursorassistant repo from GitHub and regenerates; needs network). `python3 scripts/check_cursorassistant_install.py` regenerates and fails on drift.
- No package manager, tests or linter. `.github/workflows` does not exist in this repo (the README mentions a weekly sync workflow that is not present).

## Layout
- `projects.json`: the single source for apps, categories, archive and the Ko-fi link.
- `scripts/`: `build_site.py` plus the cursorassistant sync/check/generate scripts.
- Generated: `index.html`, `404.html`, `sitemap.xml`, and `<app-id>/index.html` for each app in `projects.json`. Do not hand-edit these.
- `assets/css/site.css`, `assets/css/legacy.css` (for archived cursorassistant pages), `assets/js/site.js`, `assets/img/` (icons, screenshots).
- `cursorassistant/`: archived pages kept so old links work; `cursorassistant/install/index.html` and `deeplinks.json` are generated from the template in the cursorassistant repo (edit the template there, not here). `docs/INSTALL_WEBSITE.md` describes this.

## Conventions
- To add or update an app: edit its entry in `projects.json` (its `id` becomes the URL), put images in `assets/img/`, run `build_site.py`, and commit the regenerated files together with the JSON change.
- Retire an app by moving it from `apps` to `archive` in `projects.json`, rebuilding, and deleting its folder.
- Work on `main`; pushing to main publishes the site.
