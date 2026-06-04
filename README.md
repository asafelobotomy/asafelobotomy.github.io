# asafelobotomy.github.io

Personal developer site hosted on [GitHub Pages](https://asafelobotomy.github.io/).

## Live URLs

| Page | URL |
| --- | --- |
| Home | https://asafelobotomy.github.io/ |
| cursorAssistant overview | https://asafelobotomy.github.io/cursorassistant/ |
| cursorAssistant setup (MCP install) | https://asafelobotomy.github.io/cursorassistant/install/ |

The setup URL is linked from the [cursorAssistant](https://github.com/asafelobotomy/cursorassistant) README install badge.

## Enable GitHub Pages

1. Open **Settings → Pages** for this repository.
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Choose branch **`main`** (or your default) and folder **`/ (root)`**.
4. Save. The site is available at `https://asafelobotomy.github.io/` after a minute or two.

No Jekyll build is required: `.nojekyll` at the repo root disables Jekyll processing.

## Add a new project

1. Edit [`projects.json`](projects.json) — add an entry with `name`, `description`, `repo`, `docs`, and optional `install`.
2. Create a folder such as `my-project/index.html` using [`cursorassistant/index.html`](cursorassistant/index.html) as a template (shared styles live in [`assets/css/site.css`](assets/css/site.css)).
3. Link the new project from the homepage automatically via `projects.json`.

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
index.html                 # Homepage (loads projects from projects.json)
projects.json              # Project registry for the homepage
assets/css/site.css        # Shared styles
assets/js/site.js          # Homepage project cards
cursorassistant/
  index.html               # Project overview & setup instructions
  install/                 # Generated install page (template + deeplinks)
scripts/
  generate_cursorassistant_install.py
  sync-cursorassistant-install.sh
docs/
  INSTALL_WEBSITE.md
```

## License

Site content: MIT. Third-party project docs remain under their respective repositories.
