(function () {
  const root = document.documentElement;
  const saved = localStorage.getItem("ntrs-zib-theme") || "system";

  function apply(mode) {
    if (mode === "light" || mode === "dark") root.setAttribute("data-theme", mode);
    else root.removeAttribute("data-theme");
    document.querySelectorAll(".theme button").forEach(function (btn) {
      btn.setAttribute("aria-pressed", String(btn.getAttribute("data-theme") === mode));
    });
    localStorage.setItem("ntrs-zib-theme", mode);
  }
  apply(saved);
  document.querySelectorAll(".theme button").forEach(function (btn) {
    btn.addEventListener("click", function () { apply(btn.getAttribute("data-theme")); });
  });

  const q = document.getElementById("q");
  const sort = document.getElementById("sort");
  const universe = document.getElementById("universe");
  const count = document.getElementById("count");
  if (!universe) return;

  function cards() { return Array.prototype.slice.call(universe.querySelectorAll(".card")); }

  function render() {
    const query = (q && q.value || "").trim().toLowerCase();
    const mode = sort ? sort.value : "fresh";
    const items = cards();
    items.sort(function (a, b) {
      if (mode === "ticker") return a.dataset.ticker.localeCompare(b.dataset.ticker);
      return (b.dataset.sort || "").localeCompare(a.dataset.sort || "");
    });
    let visible = 0;
    items.forEach(function (card) {
      const hay = (card.dataset.ticker + " " + card.dataset.name + " " + card.innerText).toLowerCase();
      const show = !query || hay.indexOf(query) !== -1;
      card.style.display = show ? "" : "none";
      if (show) {
        universe.appendChild(card);
        visible += 1;
      }
    });
    if (count) count.textContent = visible + (visible === 1 ? " name" : " names");
  }
  if (q) q.addEventListener("input", render);
  if (sort) sort.addEventListener("change", render);
  render();
})();
