// A lesson page: day.html?d=4 shows a day; day.html?doc=path/to/file.md shows any other Markdown in the repo.
// The README is fetched from the repository's own files and rendered here, so the site never drifts from them.
(function () {
  var C = window.DBMS_COURSE, P = window.DBMS_PROGRESS;
  var esc = P.esc, state = P.load();
  var params = new URLSearchParams(location.search);
  var margin = document.getElementById("margin"), sheet = document.getElementById("sheet"), pager = document.getElementById("pager");

  // Served from the repo (python -m http.server, then /site/day.html) the files are one level up;
  // on GitHub Pages they're published next to the site.
  var BASE = /\/site\//.test(location.pathname) ? "../" : "";
  var BLOB = C.repo + "/blob/" + C.branch + "/", TREE = C.repo + "/tree/" + C.branch + "/";

  var n = parseInt(params.get("d"), 10);
  var day = C.days.find(function (d) { return d.day === n; }) || null;
  var docPath = day ? day.dir + "/README.md" : clean(params.get("doc") || "");
  if (!day && !docPath) { day = C.days[0]; docPath = day.dir + "/README.md"; }
  var extra = C.extras.find(function (x) { return x.path === docPath; }) || null;
  if (!day) {   // a day's README opened by path still gets the day's margin
    day = C.days.find(function (d) { return d.dir + "/README.md" === docPath; }) || null;
  }

  // ---------- paths ----------
  function clean(p) {
    var out = [];
    p.replace(/^\/+/, "").split("/").forEach(function (part) {
      if (part === "..") out.pop(); else if (part && part !== ".") out.push(part);
    });
    var joined = out.join("/");
    return /\/$/.test(p) && joined ? joined + "/" : joined;
  }
  function dirOf(p) { return p.indexOf("/") < 0 ? "" : p.slice(0, p.lastIndexOf("/") + 1); }
  function siteHref(target) {
    // target is a repo path with an optional #hash
    var hash = "", i = target.indexOf("#");
    if (i >= 0) { hash = target.slice(i); target = target.slice(0, i); }
    if (/\.md$/i.test(target)) {
      var d = C.days.find(function (x) { return x.dir + "/README.md" === target; });
      return (d ? P.dayUrl(d.day) : P.docUrl(target)) + hash;
    }
    if (/\.md\//.test(target)) return null;
    if (/\.(svg|png|jpe?g|gif|webp)$/i.test(target)) return BASE + target;   // images are published with the site
    var isDir = /\/$/.test(target) || !/\.[a-z0-9]+$/i.test(target.split("/").pop());
    return (isDir ? TREE : BLOB) + target.replace(/\/$/, "") + hash;
  }
  function slug(text) {
    return text.trim().toLowerCase().replace(/<[^>]+>/g, "").replace(/[^\w\- ]+/g, "").replace(/ /g, "-");
  }

  // ---------- the margin ----------
  function phaseOf(num) { return C.phases.find(function (p) { return p.phase === num; }); }
  function command() { return "pytest " + day.dir; }

  function marginForDay() {
    var p = phaseOf(day.phase), done = P.dayDone(state, day.day);
    var files = day.files.map(function (f, i) {
      var id = "f" + i, ticked = P.fileTicked(state, day.day, f);
      return '<li><input type="checkbox" id="' + id + '" data-file="' + esc(f) + '"' + (ticked ? " checked" : "") + '>' +
        '<label for="' + id + '"><code>' + esc(f) + "</code></label></li>";
    }).join("");
    margin.innerHTML =
      '<p class="m-day"><span class="m-word">Day</span> <span class="m-num">' + day.day + "</span></p>" +
      '<p class="m-phase"><a href="index.html#phase-' + p.phase + '">Phase ' + p.phase + ": " + esc(p.title) + "</a></p>" +
      (day.files.length ? '<div class="m-block"><h2 class="m-h">Your files</h2><ul class="files">' + files + "</ul></div>" : "") +
      '<div class="m-block"><h2 class="m-h">Check your work</h2><pre class="cmd"><code>' + esc(command()) + "</code></pre></div>" +
      '<div class="m-block post" id="post">' + postHtml(done, done && state.days[day.day].done) + "</div>";
    margin.querySelectorAll("[data-file]").forEach(function (box) {
      box.addEventListener("change", function () { P.setFile(state, day.day, box.getAttribute("data-file"), box.checked); });
    });
    wirePost(function (on) { P.setDay(state, day.day, on); return on && state.days[day.day].done; });
  }
  function marginForExtra() {
    var p = phaseOf(extra.phase), done = P.extraDone(state, extra.path);
    margin.innerHTML =
      '<p class="m-extra">Outside the hundred</p>' +
      '<p class="m-phase"><a href="index.html#phase-' + p.phase + '">Phase ' + p.phase + ": " + esc(p.title) + "</a>, after " +
      '<a href="' + P.dayUrl(extra.after) + '">Day ' + extra.after + "</a></p>" +
      (/README\.md$/.test(extra.path) ? '<div class="m-block"><h2 class="m-h">Check your answers</h2><pre class="cmd"><code>' +
        esc("pytest " + dirOf(extra.path).replace(/\/$/, "")) + "</code></pre></div>" : "") +
      '<div class="m-block post" id="post">' + postHtml(done, done && state.extras[extra.path].done, "Mark it done") + "</div>";
    wirePost(function (on) { P.setExtra(state, extra.path, on); return on && state.extras[extra.path].done; });
  }
  function marginForDoc() {
    var links = C.guides.map(function (g) {
      var here = g.path === docPath;
      return '<li><a href="' + P.docUrl(g.path) + '"' + (here ? ' aria-current="page"' : "") + ">" + esc(g.title) + "</a></li>";
    }).join("");
    margin.innerHTML = '<p class="m-extra">The guides</p><ul class="guides">' + links + "</ul>";
  }

  function postHtml(done, date, label) {
    if (done) return P.stamp(date) + '<p><button type="button" class="linkish" id="unpost">Take the stamp off</button></p>';
    return '<button type="button" class="btn" id="mark">' + (label || "Mark day done") + "</button>" +
      '<p class="m-note">Do this when the tests pass. It stamps the day in your ledger, in this browser.</p>';
  }
  function wirePost(apply) {
    var post = document.getElementById("post");
    post.addEventListener("click", function (e) {
      var t = e.target;
      if (t.id === "mark") {
        var date = apply(true);
        post.innerHTML = postHtml(true, date);
        var s = post.querySelector(".stamp");
        s.classList.add("landing");
        document.getElementById("unpost").focus();
      } else if (t.id === "unpost") {
        apply(false);
        post.innerHTML = postHtml(false, null, extra ? "Mark it done" : null);
        document.getElementById("mark").focus();
      }
    });
  }

  // ---------- previous / next ----------
  function pagerHtml() {
    var items = [];   // the reading order: days, with extras after the day they follow
    C.days.forEach(function (d) {
      items.push({ href: P.dayUrl(d.day), label: "Day " + d.day + ": " + d.title, key: d.dir + "/README.md" });
      C.extras.filter(function (x) { return x.after === d.day; }).forEach(function (x) {
        items.push({ href: P.docUrl(x.path), label: x.title, key: x.path });
      });
    });
    var at = items.findIndex(function (it) { return it.key === docPath; });
    if (at < 0) { pager.hidden = true; return; }
    var prev = items[at - 1], next = items[at + 1];
    pager.innerHTML =
      (prev ? '<a class="prev" href="' + prev.href + '"><span>Before</span> ' + esc(prev.label) + "</a>" : "<span></span>") +
      (next ? '<a class="next" href="' + next.href + '"><span>Next</span> ' + esc(next.label) + "</a>" : "<span></span>");
  }

  // ---------- the sheet ----------
  function render(md) {
    var html = window.marked ? marked.parse(md, { gfm: true }) : "<pre>" + esc(md) + "</pre>";
    sheet.innerHTML = html;
    var dir = dirOf(docPath), used = {};
    sheet.querySelectorAll("h1, h2, h3, h4").forEach(function (h) {
      var id = slug(h.textContent), k = id, i = 1;
      while (used[k]) k = id + "-" + i++;
      used[k] = true; h.id = k;
    });
    sheet.querySelectorAll("a[href]").forEach(function (a) {
      var href = a.getAttribute("href");
      if (/^(https?:|mailto:)/i.test(href)) { a.rel = "noopener"; return; }
      if (href.charAt(0) === "#") return;
      var target = siteHref(clean(dir + href));
      if (target) a.setAttribute("href", target);
    });
    sheet.querySelectorAll("img[src]").forEach(function (img) {
      var src = img.getAttribute("src");
      if (!/^(https?:|data:)/i.test(src)) img.src = BASE + clean(dir + src);
      img.loading = "lazy";
    });
    sheet.querySelectorAll("table").forEach(function (t) {   // wide tables scroll inside the sheet, not the page
      var w = document.createElement("div"); w.className = "table-scroll"; w.tabIndex = 0;
      t.parentNode.insertBefore(w, t); w.appendChild(t);
    });
    var h1 = sheet.querySelector("h1");
    document.title = (h1 ? h1.textContent : docPath) + " · Database Management Systems";
    var src = document.createElement("p");
    src.className = "source";
    src.innerHTML = 'This page is <a href="' + BLOB + docPath + '"><code>' + esc(docPath) + "</code></a> in the repository.";
    sheet.appendChild(src);
    if (location.hash) {
      var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target) target.scrollIntoView();
    }
  }

  if (day) marginForDay(); else if (extra) marginForExtra(); else marginForDoc();
  pagerHtml();

  fetch(BASE + docPath).then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.text();
  }).then(render).catch(function () {
    sheet.innerHTML = "<h1>That page isn't here</h1><p>There's no <code>" + esc(docPath) +
      '</code> on this site. <a href="index.html#ledger">Back to the ledger</a>, or look for it <a href="' + TREE + '">on GitHub</a>.</p>';
  });
})();
