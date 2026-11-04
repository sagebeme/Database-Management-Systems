// The home page: the ledger of folios, the carried-forward line, the "continue" action and the query box.
(function () {
  var C = window.DBMS_COURSE, P = window.DBMS_PROGRESS, Q = window.DBMS_QUERY;
  var state = P.load();
  var esc = P.esc;

  var KIND = { checkpoint: "Practice test", extra: "Drill", notes: "Notes" };

  function row(d) {
    var done = P.dayDone(state, d.day);
    return '<li class="row' + (done ? " is-done" : "") + '">' +
      '<span class="n">' + d.day + "</span>" +
      '<a class="t" href="' + P.dayUrl(d.day) + '">' + esc(d.title) + "</a>" +
      '<span class="what">' + P.md(d.teaches) + "</span>" +
      '<span class="st">' + (done ? P.stamp(state.days[d.day].done) : "") + "</span></li>";
  }
  function extraRow(x) {
    var done = P.extraDone(state, x.path);
    return '<li class="row extra' + (done ? " is-done" : "") + '">' +
      '<span class="n" aria-hidden="true"></span>' +
      '<a class="t" href="' + P.docUrl(x.path) + '">' + esc(x.title) + "</a>" +
      '<span class="what">' + KIND[x.kind] + ", outside the hundred</span>" +
      '<span class="st">' + (done ? P.stamp(state.extras[x.path].done) : "") + "</span></li>";
  }

  function folios() {
    var html = C.phases.map(function (p) {
      var c = P.phaseCounts(state, p);
      var rows = C.days.filter(function (d) { return d.phase === p.phase; }).map(function (d) {
        return row(d) + C.extras.filter(function (x) { return x.after === d.day; }).map(extraRow).join("");
      }).join("");
      return '<section class="folio" id="phase-' + p.phase + '" aria-labelledby="phase-' + p.phase + '-h">' +
        '<div class="wrap folio-grid">' +
          '<div class="folio-label">' +
            '<p class="folio-n" aria-hidden="true">' + p.phase + "</p>" +
            '<h3 id="phase-' + p.phase + '-h"><span class="vh">Phase ' + p.phase + ': </span>' + esc(p.title) + "</h3>" +
            '<p class="folio-learn">' + esc(p.learn) + ".</p>" +
            '<p class="folio-ends">Ends with ' + esc(p.ends) + '. <a href="' + P.docUrl(p.dir + "/README.md") + '">About this phase</a></p>' +
          "</div>" +
          '<div class="folio-rows">' +
            '<p class="cols" aria-hidden="true"><span>Day</span><span>Project</span><span class="what">What it teaches</span><span>Posted</span></p>' +
            "<ol>" + rows + "</ol>" +
            '<p class="total"><span>Carried forward</span><span><b>' + c.done + "</b> of " + c.total + "</span></p>" +
          "</div>" +
        "</div></section>";
    }).join("");
    document.getElementById("folios").innerHTML = html;
  }

  function summary() {
    var total = P.totalDone(state), next = P.nextDay(state), cta = document.getElementById("cta");
    var carried = document.getElementById("carried");
    if (!next) {
      cta.textContent = "Read the capstone again";
      cta.href = P.dayUrl(100);
      carried.textContent = "All hundred days posted.";
    } else if (total === 0) {
      cta.textContent = "Start Day 1";
      cta.href = P.dayUrl(1);
      carried.textContent = "Nothing posted yet.";
    } else {
      cta.textContent = "Continue: Day " + next.day;
      cta.href = P.dayUrl(next.day);
      carried.textContent = total + " of 100 days posted. Next: " + next.title + ".";
    }
  }

  function render() { state = P.load(); folios(); summary(); }

  function console_() {
    var box = document.getElementById("console");
    if (!box || !Q) return;
    box.hidden = false;
    var form = document.getElementById("query-form"), input = document.getElementById("query"), out = document.getElementById("result");
    function go() {
      state = P.load();
      out.innerHTML = Q.run(input.value, state, render);
    }
    form.addEventListener("submit", function (e) { e.preventDefault(); go(); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); go(); }
    });
    box.querySelectorAll("[data-q]").forEach(function (a) {
      a.addEventListener("click", function (e) { e.preventDefault(); input.value = a.getAttribute("data-q"); go(); input.focus(); });
    });
    go();
  }

  render();
  console_();
  // Another tab posted a day: keep this one honest.
  window.addEventListener("storage", function (e) { if (e.key === "dbms-100-progress") render(); });
})();
