/**
 * Progressive enhancements for the generated pages (they work without it):
 * category filter on the homepage, install tabs and copy buttons on app pages,
 * and hauler's segment map illustration.
 */
(function () {
  const filters = document.querySelectorAll("[data-filter]");
  filters.forEach((chip) =>
    chip.addEventListener("click", () => {
      filters.forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
      document.querySelectorAll("[data-cat]").forEach((card) => {
        card.hidden = !(chip.dataset.filter === "all" || card.dataset.cat === chip.dataset.filter);
      });
    })
  );

  document.querySelectorAll("[data-tabs]").forEach((group) => {
    const tabs = group.querySelectorAll("[role=tab]");
    const panels = group.querySelectorAll("[role=tabpanel]");
    const show = (i) => {
      tabs.forEach((t, j) => t.setAttribute("aria-selected", String(i === j)));
      panels.forEach((p, j) => (p.hidden = i !== j));
    };
    tabs.forEach((t, i) => t.addEventListener("click", () => show(i)));
    group.querySelector(".tabs").hidden = false;
    show(0);
  });

  document.querySelectorAll(".codebox").forEach((box) => {
    const pre = box.querySelector("pre");
    const btn = document.createElement("button");
    btn.className = "copy";
    btn.type = "button";
    btn.textContent = "Copy";
    btn.addEventListener("click", () => {
      const done = () => {
        btn.textContent = "Copied";
        setTimeout(() => (btn.textContent = "Copy"), 1400);
      };
      if (!navigator.clipboard) return getSelection().selectAllChildren(pre);
      navigator.clipboard.writeText(pre.textContent).then(done, () => getSelection().selectAllChildren(pre));
    });
    box.prepend(btn);
  });

  // 8 connections, each filling its own slice of 32 blocks
  const map = document.getElementById("segmap");
  if (map) {
    map.innerHTML = Array.from({ length: 32 }, (_, i) =>
      `<i class="${i % 4 === 0 ? "f" : i % 4 < 2 + (i % 3) ? "d" : ""}"></i>`
    ).join("");
  }
})();
