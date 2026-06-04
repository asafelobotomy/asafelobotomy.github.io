/**
 * Load projects.json and render project cards on the homepage.
 * Other pages can include this script with data-render="projects".
 */
(function () {
  const grid = document.querySelector("[data-projects-grid]");
  if (!grid) return;

  fetch("/projects.json")
    .then((r) => {
      if (!r.ok) throw new Error("Failed to load projects");
      return r.json();
    })
    .then((data) => {
      const tagline = document.querySelector("[data-site-tagline]");
      if (tagline && data.tagline) tagline.textContent = data.tagline;

      const projects = (data.projects || []).filter((p) => p.featured !== false);
      grid.innerHTML = projects
        .map(
          (p) => `
        <li class="project-card">
          <h2>
            <a href="${p.docs || p.repo}">${escapeHtml(p.name)}</a>
            ${p.badge ? `<span class="badge">${escapeHtml(p.badge)}</span>` : ""}
          </h2>
          <p>${escapeHtml(p.description || "")}</p>
          <div class="project-card__actions">
            ${
              p.install
                ? `<a class="btn btn--primary" href="${p.install}">Set up</a>`
                : ""
            }
            <a class="btn btn--secondary" href="${p.docs || p.repo}">Overview</a>
            <a class="btn btn--secondary" href="${p.repo}" rel="noopener">GitHub</a>
          </div>
        </li>`
        )
        .join("");
    })
    .catch(() => {
      grid.innerHTML =
        '<li class="project-card"><p>Could not load projects. See <a href="https://github.com/asafelobotomy">GitHub</a>.</p></li>';
    });

  function escapeHtml(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }
})();
