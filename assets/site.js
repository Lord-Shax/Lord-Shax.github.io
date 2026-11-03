// Small enhancements only; every page works without this file.
(function () {
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });


  // Boxes lean gently toward the pointer, with a soft orange spotlight.
  if (window.matchMedia("(hover: hover) and (pointer: fine)").matches &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    document.querySelectorAll(".spec, .pillar, .contact").forEach(function (el) {
      var max = el.classList.contains("contact") ? 2 : 5;
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        el.style.setProperty("--mx", (x * 100).toFixed(1) + "%");
        el.style.setProperty("--my", (y * 100).toFixed(1) + "%");
        el.style.setProperty("--ry", ((x - .5) * max).toFixed(2) + "deg");
        el.style.setProperty("--rx", ((.5 - y) * max).toFixed(2) + "deg");
      });
      el.addEventListener("pointerleave", function () {
        el.style.setProperty("--rx", "0deg"); el.style.setProperty("--ry", "0deg");
      });
    });
  }

  var items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    items.forEach(function (el) { el.classList.add("in"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -8% 0px" });
  items.forEach(function (el) { io.observe(el); });
})();
