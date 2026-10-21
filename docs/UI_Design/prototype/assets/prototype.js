/* Lightweight, front-end-only interactions for the design preview.
   No network, no storage of patient data, no production integration. */
(function () {
  const root = document.documentElement;

  function applyTheme(theme) {
    document.body.dataset.theme = theme;
    try { localStorage.setItem("ncc-preview-theme", theme); } catch (_) {}
    document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
      button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
      button.title = theme === "dark" ? "Use light theme" : "Use dark theme";
    });
  }

  try {
    const saved = localStorage.getItem("ncc-preview-theme");
    if (saved === "dark") document.body.dataset.theme = "dark";
  } catch (_) {}

  document.addEventListener("click", function (event) {
    const toggle = event.target.closest("[data-theme-toggle]");
    if (toggle) {
      event.preventDefault();
      applyTheme(document.body.dataset.theme === "dark" ? "light" : "dark");
      return;
    }

    const dismiss = event.target.closest("[data-dismiss]");
    if (dismiss) {
      const target = document.querySelector(dismiss.getAttribute("data-dismiss"));
      if (target) target.remove();
      return;
    }

    const filter = event.target.closest("[data-filter-target]");
    if (filter) {
      const target = document.querySelector(filter.getAttribute("data-filter-target"));
      if (target) target.classList.toggle("filter-open");
    }
  });

  document.addEventListener("keydown", function (event) {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      const search = document.querySelector(".search-shell");
      if (search) {
        event.preventDefault();
        search.focus();
      }
    }
  });
})();
