// Runs in <head>, before the page paints: applies the theme you chose last time, if any.
// Otherwise the page follows the system setting through CSS.
(function () {
  var KEY = "dbms-100-theme";
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) { /* storage blocked: follow the system */ }
  if (saved === "light" || saved === "dark") document.documentElement.setAttribute("data-theme", saved);

  function current() {
    var set = document.documentElement.getAttribute("data-theme");
    if (set) return set;
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function label(button) {
    var dark = current() === "dark";
    button.textContent = dark ? "Day" : "Night";
    button.setAttribute("aria-label", dark ? "Switch to the light theme" : "Switch to the dark theme");
  }
  document.addEventListener("DOMContentLoaded", function () {
    var button = document.getElementById("theme");
    if (!button) return;
    label(button);
    button.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try { localStorage.setItem(KEY, next); } catch (e) { /* not kept, still switched */ }
      label(button);
    });
  });
})();
