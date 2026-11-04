// Progress, shared by every page, kept only in this browser (localStorage). No accounts, no server.
//   { days:   { "4": { done: "2026-11-04", files: { "0-cheap_routes.sql": true } } },
//     extras: { "phase-4-normalisation/worked-examples.md": { done: "2026-11-05" } } }
(function () {
  var KEY = "dbms-100-progress";
  var C = window.DBMS_COURSE;

  function load() {
    var s = {};
    try { s = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { s = {}; }
    if (typeof s.days !== "object" || !s.days) s.days = {};
    if (typeof s.extras !== "object" || !s.extras) s.extras = {};
    return s;
  }
  function save(s) {
    try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) { /* private window: not kept */ }
  }
  function today() {
    var d = new Date();
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  }
  function dayDone(s, n) { return !!(s.days[n] && s.days[n].done); }
  function extraDone(s, path) { return !!(s.extras[path] && s.extras[path].done); }
  function setDay(s, n, done) {
    var d = s.days[n] || (s.days[n] = {});
    if (done) d.done = d.done || today(); else delete d.done;
    save(s);
  }
  function setExtra(s, path, done) {
    if (done) s.extras[path] = { done: (s.extras[path] && s.extras[path].done) || today() };
    else delete s.extras[path];
    save(s);
  }
  function setFile(s, n, file, ticked) {
    var d = s.days[n] || (s.days[n] = {});
    d.files = d.files || {};
    if (ticked) d.files[file] = true; else delete d.files[file];
    save(s);
  }
  function fileTicked(s, n, file) { return !!(s.days[n] && s.days[n].files && s.days[n].files[file]); }

  function phaseCounts(s, p) {
    var days = C.days.filter(function (d) { return d.phase === p.phase; });
    return { total: days.length, done: days.filter(function (d) { return dayDone(s, d.day); }).length };
  }
  // The first day not yet posted, or null when all hundred are.
  function nextDay(s) {
    return C.days.find(function (d) { return !dayDone(s, d.day); }) || null;
  }
  function totalDone(s) { return C.days.filter(function (d) { return dayDone(s, d.day); }).length; }

  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  function stampDate(iso) {
    var p = (iso || "").split("-");
    return p.length === 3 ? Number(p[2]) + " " + MONTHS[Number(p[1]) - 1] + " " + p[0] : "";
  }
  function esc(t) {
    return String(t).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  // Inline `code` in syllabus text.
  function md(t) { return esc(t).replace(/`([^`]+)`/g, "<code>$1</code>"); }
  function stamp(iso) {
    return '<span class="stamp"><b>Done</b><small>' + esc(stampDate(iso)) + "</small></span>";
  }
  function dayUrl(n) { return "day.html?d=" + n; }
  function docUrl(path) { return "day.html?doc=" + encodeURIComponent(path); }

  window.DBMS_PROGRESS = {
    load: load, save: save, today: today, dayDone: dayDone, extraDone: extraDone, setDay: setDay,
    setExtra: setExtra, setFile: setFile, fileTicked: fileTicked, phaseCounts: phaseCounts,
    nextDay: nextDay, totalDone: totalDone, stampDate: stampDate, stamp: stamp, esc: esc, md: md,
    dayUrl: dayUrl, docUrl: docUrl
  };
})();
