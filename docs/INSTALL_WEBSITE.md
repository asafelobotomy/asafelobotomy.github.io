# cursorAssistant install page (this repo)

Canonical URL: [https://asafelobotomy.github.io/cursorassistant/install/](https://asafelobotomy.github.io/cursorassistant/install/)

The install UX lives in **asafelobotomy.github.io** so one Pages site can host multiple projects. The [cursorassistant](https://github.com/asafelobotomy/cursorassistant) repo supplies **VERSION** and **catalog.json** only.

## Regenerate

```sh
bash scripts/sync-cursorassistant-install.sh
# or: CURSOR_ASSISTANT_REF=v0.13.0 bash scripts/sync-cursorassistant-install.sh
```

Edits to copy or layout: change `install/index.template.html` in the **cursorassistant** repo, then merge the bot PR or run sync.

## CI

`.github/workflows/sync-cursorassistant-install.yml` clones upstream and runs the generator weekly or on demand.
