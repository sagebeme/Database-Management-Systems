// A small SQL engine over the course itself, answering the way the mysql client does.
// Tables: days, phases, extras. Statements: SELECT (WHERE, GROUP BY, HAVING, ORDER BY, LIMIT, DISTINCT,
// COUNT/MIN/MAX/SUM/AVG), UPDATE ... SET status = 'done' | 'todo', SHOW TABLES, DESCRIBE.
// It isn't MySQL: it's enough of it to ask the course questions, and it says so when you go further.
(function () {
  var C = window.DBMS_COURSE, P = window.DBMS_PROGRESS;

  // ---------- the tables, built fresh from the course data and your progress ----------
  var SCHEMA = {
    days: [["day", "int"], ["phase", "int"], ["title", "varchar(60)"], ["teaches", "varchar(120)"],
           ["status", "enum('todo','done')"], ["posted", "date"], ["kata", "tinyint(1)"], ["files", "int"]],
    phases: [["phase", "int"], ["title", "varchar(40)"], ["first_day", "int"], ["last_day", "int"],
             ["days", "int"], ["done", "int"]],
    extras: [["title", "varchar(60)"], ["kind", "enum('checkpoint','extra','notes')"], ["phase", "int"],
             ["after_day", "int"], ["status", "enum('todo','done')"], ["posted", "date"]]
  };
  function tables(state) {
    return {
      days: C.days.map(function (d) {
        var done = P.dayDone(state, d.day);
        return { day: d.day, phase: d.phase, title: d.title, teaches: d.teaches.replace(/`/g, ""),
                 status: done ? "done" : "todo", posted: done ? state.days[d.day].done : null,
                 kata: d.kata ? 1 : 0, files: d.files.length, _ref: d };
      }),
      phases: C.phases.map(function (p) {
        var c = P.phaseCounts(state, p);
        return { phase: p.phase, title: p.title, first_day: p.first, last_day: p.last, days: c.total, done: c.done };
      }),
      extras: C.extras.map(function (x) {
        var done = P.extraDone(state, x.path);
        return { title: x.title, kind: x.kind, phase: x.phase, after_day: x.after,
                 status: done ? "done" : "todo", posted: done ? state.extras[x.path].done : null, _ref: x };
      })
    };
  }

  // ---------- errors, worded like MySQL's ----------
  function SqlError(code, state, msg) { this.text = "ERROR " + code + " (" + state + "): " + msg; }
  function syntax(src, pos) {
    var near = src.slice(pos).trim();
    return new SqlError(1064, "42000", "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '" + near.slice(0, 60) + "' at line 1");
  }

  // ---------- tokens ----------
  function tokenize(src) {
    var out = [], i = 0, m;
    var re = {
      space: /^\s+/, comment: /^(--[^\n]*|#[^\n]*)/, num: /^\d+(\.\d+)?/, ident: /^[A-Za-z_][A-Za-z0-9_]*/,
      quoted: /^`([^`]*)`/, op: /^(<=|>=|<>|!=|=|<|>|\(|\)|,|\*|;|\.)/
    };
    while (i < src.length) {
      var rest = src.slice(i);
      if ((m = rest.match(re.space)) || (m = rest.match(re.comment))) { i += m[0].length; continue; }
      if (rest[0] === "'" || rest[0] === '"') {
        var q = rest[0], j = 1, v = "";
        while (j < rest.length) {
          if (rest[j] === q && rest[j + 1] === q) { v += q; j += 2; continue; }
          if (rest[j] === q) break;
          v += rest[j++];
        }
        if (j >= rest.length) throw syntax(src, i);
        out.push({ k: "str", v: v, pos: i, end: i + j + 1 }); i += j + 1; continue;
      }
      if ((m = rest.match(re.num))) { out.push({ k: "num", v: Number(m[0]), pos: i, end: i + m[0].length }); i += m[0].length; continue; }
      if ((m = rest.match(re.quoted))) { out.push({ k: "id", v: m[1], pos: i, end: i + m[0].length }); i += m[0].length; continue; }
      if ((m = rest.match(re.ident))) { out.push({ k: "id", v: m[0], up: m[0].toUpperCase(), pos: i, end: i + m[0].length }); i += m[0].length; continue; }
      if ((m = rest.match(re.op))) { out.push({ k: "op", v: m[0], pos: i, end: i + m[0].length }); i += m[0].length; continue; }
      throw syntax(src, i);
    }
    return out;
  }

  // ---------- parser ----------
  var AGG = { COUNT: 1, MIN: 1, MAX: 1, SUM: 1, AVG: 1 }, FN = { UPPER: 1, LOWER: 1, LENGTH: 1 };
  var RESERVED = { SELECT: 1, FROM: 1, WHERE: 1, GROUP: 1, BY: 1, HAVING: 1, ORDER: 1, LIMIT: 1, OFFSET: 1, AND: 1, OR: 1,
                   NOT: 1, AS: 1, ASC: 1, DESC: 1, LIKE: 1, IN: 1, IS: 1, NULL: 1, BETWEEN: 1, DISTINCT: 1, SET: 1 };

  function Parser(src, toks) { this.src = src; this.t = toks; this.i = 0; }
  Parser.prototype = {
    peek: function () { return this.t[this.i]; },
    kw: function (word) { var t = this.peek(); return t && t.k === "id" && t.up === word; },
    op: function (o) { var t = this.peek(); return t && t.k === "op" && t.v === o; },
    eat: function (word) { if (this.kw(word)) { return this.t[this.i++]; } return null; },
    eatOp: function (o) { if (this.op(o)) { return this.t[this.i++]; } return null; },
    fail: function () { var t = this.peek(); throw syntax(this.src, t ? t.pos : this.src.length); },
    need: function (word) { return this.eat(word) || this.fail(); },
    needOp: function (o) { return this.eatOp(o) || this.fail(); },
    ident: function () { var t = this.peek(); if (t && t.k === "id" && !RESERVED[t.up]) { this.i++; return t.v; } this.fail(); },
    text: function (from) { return this.src.slice(this.t[from].pos, this.t[this.i - 1].end); },

    expr: function () { return this.or(); },
    or: function () { var a = this.and(); while (this.eat("OR")) a = { t: "or", a: a, b: this.and() }; return a; },
    and: function () { var a = this.not(); while (this.eat("AND")) a = { t: "and", a: a, b: this.not() }; return a; },
    not: function () { if (this.eat("NOT")) return { t: "not", a: this.not() }; return this.cmp(); },
    cmp: function () {
      var a = this.primary(), t = this.peek(), neg;
      if (t && t.k === "op" && /^(=|<>|!=|<|>|<=|>=)$/.test(t.v)) { this.i++; return { t: "cmp", op: t.v, a: a, b: this.primary() }; }
      if (this.eat("IS")) { neg = !!this.eat("NOT"); this.need("NULL"); return { t: "isnull", neg: neg, a: a }; }
      neg = !!this.eat("NOT");
      if (this.eat("LIKE")) return { t: "like", neg: neg, a: a, b: this.primary() };
      if (this.eat("IN")) {
        this.needOp("("); var list = [this.primary()];
        while (this.eatOp(",")) list.push(this.primary());
        this.needOp(")"); return { t: "in", neg: neg, a: a, list: list };
      }
      if (this.eat("BETWEEN")) { var lo = this.primary(); this.need("AND"); return { t: "between", neg: neg, a: a, lo: lo, hi: this.primary() }; }
      if (neg) this.fail();
      return a;
    },
    primary: function () {
      var t = this.peek();
      if (!t) this.fail();
      if (t.k === "num") { this.i++; return { t: "val", v: t.v }; }
      if (t.k === "str") { this.i++; return { t: "val", v: t.v }; }
      if (this.eat("NULL")) return { t: "val", v: null };
      if (this.eat("TRUE")) return { t: "val", v: 1 };
      if (this.eat("FALSE")) return { t: "val", v: 0 };
      if (this.eatOp("(")) { var e = this.expr(); this.needOp(")"); return e; }
      if (t.k === "id" && (AGG[t.up] || FN[t.up]) && this.t[this.i + 1] && this.t[this.i + 1].v === "(") {
        this.i += 2;
        var node = { t: AGG[t.up] ? "agg" : "fn", fn: t.up, distinct: !!this.eat("DISTINCT") };
        if (t.up === "COUNT" && this.eatOp("*")) node.star = true; else node.a = this.expr();
        this.needOp(")"); return node;
      }
      if (t.k === "id" && !RESERVED[t.up]) {
        this.i++;
        if (this.eatOp(".")) return { t: "col", table: t.v, name: this.ident() };
        return { t: "col", name: t.v };
      }
      this.fail();
    },

    statement: function () {
      if (this.eat("SELECT")) return this.select();
      if (this.eat("UPDATE")) return this.update();
      if (this.eat("SHOW")) { this.need("TABLES"); return { t: "show" }; }
      if (this.eat("DESCRIBE") || this.eat("DESC") || this.eat("EXPLAIN")) return { t: "describe", table: this.ident() };
      var t = this.peek();
      if (t && t.k === "id" && /^(INSERT|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|GRANT)$/.test(t.up)) {
        var word = t.up; this.i = this.t.length;
        throw new SqlError(1142, "42000", word + " command denied to user 'you'@'localhost'. This copy of the course is read-only, apart from UPDATE ... SET status");
      }
      this.fail();
    },
    select: function () {
      var q = { t: "select", distinct: !!this.eat("DISTINCT"), items: [] };
      if (this.eatOp("*")) q.star = true;
      else {
        do {
          var from = this.i, e = this.expr(), text = this.text(from), alias = null;
          if (this.eat("AS")) alias = this.ident();
          else if (this.peek() && this.peek().k === "id" && !RESERVED[this.peek().up]) alias = this.ident();
          q.items.push({ e: e, name: alias || text });
        } while (this.eatOp(","));
      }
      this.need("FROM"); q.table = this.ident();
      if (this.eat("WHERE")) q.where = this.expr();
      if (this.eat("GROUP")) { this.need("BY"); q.group = [this.primary()]; while (this.eatOp(",")) q.group.push(this.primary()); }
      if (this.eat("HAVING")) q.having = this.expr();
      if (this.eat("ORDER")) {
        this.need("BY"); q.order = [];
        do { var oe = this.primary(), desc = !!this.eat("DESC"); if (!desc) this.eat("ASC"); q.order.push({ e: oe, desc: desc }); } while (this.eatOp(","));
      }
      if (this.eat("LIMIT")) {
        var n = this.peek(); if (!n || n.k !== "num") this.fail(); this.i++; q.limit = n.v; q.offset = 0;
        if (this.eatOp(",")) { var m = this.peek(); if (!m || m.k !== "num") this.fail(); this.i++; q.offset = q.limit; q.limit = m.v; }
        else if (this.eat("OFFSET")) { var o = this.peek(); if (!o || o.k !== "num") this.fail(); this.i++; q.offset = o.v; }
      }
      return q;
    },
    update: function () {
      var q = { t: "update", table: this.ident() };
      this.need("SET"); q.col = this.ident(); this.needOp("="); q.value = this.primary();
      if (this.eat("WHERE")) q.where = this.expr();
      return q;
    }
  };

  // ---------- evaluation, with SQL's three-valued logic ----------
  function num(v) { return typeof v === "number" ? v : (v !== null && v !== "" && !isNaN(v) ? Number(v) : null); }
  function compare(a, b) {
    if (a === null || b === null) return null;
    var na = num(a), nb = num(b);
    if (typeof a === "number" || typeof b === "number") { if (na !== null && nb !== null) return na < nb ? -1 : na > nb ? 1 : 0; }
    a = String(a).toLowerCase(); b = String(b).toLowerCase();   // case-insensitive, like MySQL's default collation
    return a < b ? -1 : a > b ? 1 : 0;
  }
  function likeRe(p) {
    return new RegExp("^" + String(p).replace(/[.+?^${}()|[\]\\*]/g, "\\$&").replace(/%/g, ".*").replace(/_/g, ".") + "$", "is");
  }
  function truth(v) { return v === null ? null : !!(typeof v === "number" ? v : num(v)); }

  function evaluate(n, row, ctx) {
    switch (n.t) {
      case "val": return n.v;
      case "col": {
        var name = n.name.toLowerCase();
        if (n.table && n.table.toLowerCase() !== ctx.table) throw new SqlError(1054, "42S22", "Unknown column '" + n.table + "." + n.name + "' in 'field list'");
        if (ctx.aliases && name in ctx.aliases && !(name in (row || {}))) return ctx.aliases[name];
        if (!ctx.columns.includes(name)) throw new SqlError(1054, "42S22", "Unknown column '" + n.name + "' in '" + (ctx.where ? "where clause" : "field list") + "'");
        return row ? row[name] : null;
      }
      case "agg": {
        if (!ctx.group) throw new SqlError(1111, "HY000", "Invalid use of group function");
        if (n.star) return ctx.group.length;
        var vals = ctx.group.map(function (r) { return evaluate(n.a, r, ctx); }).filter(function (v) { return v !== null; });
        if (n.distinct) vals = vals.filter(function (v, i) { return vals.indexOf(v) === i; });
        if (n.fn === "COUNT") return vals.length;
        if (!vals.length) return null;
        if (n.fn === "MIN") return vals.reduce(function (a, b) { return compare(a, b) <= 0 ? a : b; });
        if (n.fn === "MAX") return vals.reduce(function (a, b) { return compare(a, b) >= 0 ? a : b; });
        var sum = vals.reduce(function (a, b) { return a + (num(b) || 0); }, 0);
        return n.fn === "SUM" ? sum : Math.round(sum / vals.length * 10000) / 10000;
      }
      case "fn": {
        var v = evaluate(n.a, row, ctx);
        if (v === null) return null;
        return n.fn === "UPPER" ? String(v).toUpperCase() : n.fn === "LOWER" ? String(v).toLowerCase() : String(v).length;
      }
      case "cmp": {
        var c = compare(evaluate(n.a, row, ctx), evaluate(n.b, row, ctx));
        if (c === null) return null;
        return ({ "=": c === 0, "<>": c !== 0, "!=": c !== 0, "<": c < 0, ">": c > 0, "<=": c <= 0, ">=": c >= 0 })[n.op] ? 1 : 0;
      }
      case "isnull": { var isn = evaluate(n.a, row, ctx) === null; return (n.neg ? !isn : isn) ? 1 : 0; }
      case "like": {
        var s = evaluate(n.a, row, ctx), p = evaluate(n.b, row, ctx);
        if (s === null || p === null) return null;
        var hit = likeRe(p).test(String(s)); return (n.neg ? !hit : hit) ? 1 : 0;
      }
      case "in": {
        var x = evaluate(n.a, row, ctx), unknown = false;
        if (x === null) return null;
        for (var i = 0; i < n.list.length; i++) {
          var c2 = compare(x, evaluate(n.list[i], row, ctx));
          if (c2 === 0) return n.neg ? 0 : 1;
          if (c2 === null) unknown = true;
        }
        return unknown ? null : (n.neg ? 1 : 0);   // the NOT IN trap from Day 22, faithfully
      }
      case "between": {
        var y = evaluate(n.a, row, ctx), lo = compare(y, evaluate(n.lo, row, ctx)), hi = compare(y, evaluate(n.hi, row, ctx));
        if (lo === null || hi === null) return null;
        var inside = lo >= 0 && hi <= 0; return (n.neg ? !inside : inside) ? 1 : 0;
      }
      case "not": { var t = truth(evaluate(n.a, row, ctx)); return t === null ? null : (t ? 0 : 1); }
      case "and": {
        var l = truth(evaluate(n.a, row, ctx)), r = truth(evaluate(n.b, row, ctx));
        if (l === false || r === false) return 0; if (l === null || r === null) return null; return 1;
      }
      case "or": {
        var l2 = truth(evaluate(n.a, row, ctx)), r2 = truth(evaluate(n.b, row, ctx));
        if (l2 === true || r2 === true) return 1; if (l2 === null || r2 === null) return null; return 0;
      }
    }
  }
  function hasAgg(n) {
    if (!n || typeof n !== "object") return false;
    if (n.t === "agg") return true;
    return ["a", "b", "lo", "hi"].some(function (k) { return hasAgg(n[k]); }) || (n.list || []).some(hasAgg);
  }
  function bareColumns(n, out) {
    if (!n || typeof n !== "object" || n.t === "agg") return out;
    if (n.t === "col") out.push(n.name.toLowerCase());
    ["a", "b", "lo", "hi"].forEach(function (k) { bareColumns(n[k], out); });
    (n.list || []).forEach(function (x) { bareColumns(x, out); });
    return out;
  }

  function runSelect(q, data) {
    var rows = data[q.table.toLowerCase()];
    if (!rows) throw new SqlError(1146, "42S02", "Table 'course." + q.table + "' doesn't exist");
    var table = q.table.toLowerCase(), columns = SCHEMA[table].map(function (c) { return c[0]; });
    var ctx = { table: table, columns: columns };
    if (q.where) {
      if (hasAgg(q.where)) throw new SqlError(1111, "HY000", "Invalid use of group function");
      ctx.where = true;
      rows = rows.filter(function (r) { return truth(evaluate(q.where, r, ctx)) === true; });
      ctx.where = false;
    }
    var items = q.star ? columns.map(function (c) { return { e: { t: "col", name: c }, name: c }; }) : q.items;
    var grouped = !!q.group || items.some(function (it) { return hasAgg(it.e); }) || hasAgg(q.having);
    var out = [];
    if (grouped) {
      var keys = (q.group || []).map(function (g) { return g.t === "col" ? g.name.toLowerCase() : null; });
      items.forEach(function (it, i) {
        bareColumns(it.e, []).forEach(function (c) {
          if (!columns.includes(c)) throw new SqlError(1054, "42S22", "Unknown column '" + c + "' in 'field list'");
          if (!keys.includes(c)) throw new SqlError(1055, "42000", "Expression #" + (i + 1) + " of SELECT list is not in GROUP BY clause and contains nonaggregated column 'course." + table + "." + c + "' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by");
        });
      });
      var groups = [], index = {};
      if (!q.group) groups.push(rows);
      else rows.forEach(function (r) {
        var k = JSON.stringify(q.group.map(function (g) { return evaluate(g, r, ctx); }));
        if (!(k in index)) { index[k] = groups.length; groups.push([]); }
        groups[index[k]].push(r);
      });
      groups.forEach(function (g) {
        var gctx = { table: table, columns: columns, group: g };
        var o = { values: items.map(function (it) { return evaluate(it.e, g[0] || null, gctx); }), first: g[0], group: g };
        if (q.having) {
          gctx.aliases = {}; items.forEach(function (it, i) { gctx.aliases[it.name.toLowerCase()] = o.values[i]; });
          if (truth(evaluate(q.having, g[0] || null, gctx)) !== true) return;
        }
        out.push(o);
      });
    } else {
      out = rows.map(function (r) { return { values: items.map(function (it) { return evaluate(it.e, r, ctx); }), first: r }; });
    }
    if (q.distinct) {
      var seen = {};
      out = out.filter(function (o) { var k = JSON.stringify(o.values); if (seen[k]) return false; seen[k] = true; return true; });
    }
    if (q.order) {
      var keyOf = function (o, spec) {
        var e = spec.e;
        if (e.t === "val" && typeof e.v === "number") {
          if (e.v < 1 || e.v > items.length) throw new SqlError(1054, "42S22", "Unknown column '" + e.v + "' in 'order clause'");
          return o.values[e.v - 1];
        }
        if (e.t === "col") {
          var at = items.findIndex(function (it) { return it.name.toLowerCase() === e.name.toLowerCase(); });
          if (at >= 0) return o.values[at];
        }
        return evaluate(e, o.first || null, { table: table, columns: columns, group: o.group });
      };
      out = out.map(function (o, i) { return { o: o, i: i, k: q.order.map(function (s) { return keyOf(o, s); }) }; })
        .sort(function (x, y) {
          for (var j = 0; j < q.order.length; j++) {
            var a = x.k[j], b = y.k[j], c;
            if (a === null && b === null) c = 0; else if (a === null) c = -1; else if (b === null) c = 1; else c = compare(a, b);
            if (c) return q.order[j].desc ? -c : c;       // NULLs first going up, last going down, as in MySQL
          }
          return x.i - y.i;
        }).map(function (x) { return x.o; });
    }
    if (q.limit !== undefined) out = out.slice(q.offset, q.offset + q.limit);
    return { names: items.map(function (it) { return it.name; }), rows: out.map(function (o) { return o.values; }),
             refs: out.map(function (o) { return o.first && o.first._ref; }), table: table };
  }

  function runUpdate(q, data, state) {
    var table = q.table.toLowerCase();
    if (!data[table]) throw new SqlError(1146, "42S02", "Table 'course." + q.table + "' doesn't exist");
    if (table === "phases") throw new SqlError(1288, "HY000", "The target table phases of the UPDATE is not updatable: its counts come from days");
    var col = q.col.toLowerCase();
    if (!SCHEMA[table].some(function (c) { return c[0] === col; })) throw new SqlError(1054, "42S22", "Unknown column '" + q.col + "' in 'field list'");
    if (col !== "status") throw new SqlError(1348, "HY000", "Column '" + q.col + "' is not updatable");
    var value = evaluate(q.value, null, { table: table, columns: [] });
    if (value !== "done" && value !== "todo") throw new SqlError(1265, "01000", "Data truncated for column 'status' at row 1: it takes 'done' or 'todo'");
    var ctx = { table: table, columns: SCHEMA[table].map(function (c) { return c[0]; }), where: true };
    var matched = 0, changed = 0;
    data[table].forEach(function (r) {
      if (q.where && truth(evaluate(q.where, r, ctx)) !== true) return;
      matched++;
      if (r.status === value) return;
      changed++;
      if (table === "days") P.setDay(state, r.day, value === "done");
      else P.setExtra(state, r._ref.path, value === "done");
    });
    return { matched: matched, changed: changed };
  }

  // ---------- the mysql client's box-drawn tables ----------
  function cell(v) { return v === null ? "NULL" : String(v); }
  function box(res) {
    var w = res.names.map(function (n, i) {
      return Math.max(n.length, res.rows.reduce(function (m, r) { return Math.max(m, cell(r[i]).length); }, 0));
    });
    var line = "+" + w.map(function (x) { return "-".repeat(x + 2); }).join("+") + "+";
    var numeric = res.names.map(function (_, i) { return res.rows.every(function (r) { return r[i] === null || typeof r[i] === "number"; }); });
    var dayCol = res.names.findIndex(function (n) { return n.toLowerCase() === "day" || n.toLowerCase() === "after_day"; });
    var head = "| " + res.names.map(function (n, i) { return P.esc(n.padEnd(w[i])); }).join(" | ") + " |";
    var body = res.rows.map(function (r, ri) {
      return "| " + r.map(function (v, i) {
        var s = cell(v), pad = numeric[i] ? s.padStart(w[i]) : s.padEnd(w[i]), html = P.esc(pad);
        if (i === dayCol && typeof v === "number") html = html.replace(String(v), '<a href="' + P.dayUrl(v) + '">' + v + "</a>");
        else if (res.table === "extras" && res.names[i].toLowerCase() === "title" && res.refs[ri]) html = '<a href="' + P.docUrl(res.refs[ri].path) + '">' + P.esc(s) + "</a>" + P.esc(pad.slice(s.length));
        return html;
      }).join(" | ") + " |";
    });
    return [line, head, line].concat(body, [line]).join("\n");
  }
  function secs(t0) { return "(" + ((performance.now() - t0) / 1000).toFixed(2) + " sec)"; }

  function run(src, state, onChange) {
    var out = [];
    var toks;
    try { toks = tokenize(src); } catch (e) { if (e instanceof SqlError) return e.text; throw e; }
    var stmts = [[]];
    toks.forEach(function (t) { if (t.k === "op" && t.v === ";") stmts.push([]); else stmts[stmts.length - 1].push(t); });
    stmts = stmts.filter(function (s) { return s.length; });
    if (!stmts.length) return "ERROR 1065 (42000): Query was empty";
    for (var i = 0; i < stmts.length; i++) {
      var t0 = performance.now();
      try {
        var p = new Parser(src, stmts[i]), q = p.statement();
        if (p.i < stmts[i].length) p.fail();
        var data = tables(state);
        if (q.t === "select") {
          var res = runSelect(q, data);
          out.push(res.rows.length ? box(res) + "\n" + res.rows.length + " row" + (res.rows.length === 1 ? "" : "s") + " in set " + secs(t0) : "Empty set " + secs(t0));
        } else if (q.t === "update") {
          var u = runUpdate(q, data, state);
          out.push("Query OK, " + u.changed + " row" + (u.changed === 1 ? "" : "s") + " affected " + secs(t0) + "\nRows matched: " + u.matched + "  Changed: " + u.changed + "  Warnings: 0");
          if (u.changed && onChange) onChange();
        } else if (q.t === "show") {
          out.push(box({ names: ["Tables_in_course"], rows: [["days"], ["extras"], ["phases"]], refs: [] }) + "\n3 rows in set " + secs(t0));
        } else if (q.t === "describe") {
          var cols = SCHEMA[q.table.toLowerCase()];
          if (!cols) throw new SqlError(1146, "42S02", "Table 'course." + q.table + "' doesn't exist");
          out.push(box({ names: ["Field", "Type"], rows: cols.map(function (c) { return [c[0], c[1]]; }), refs: [] }) + "\n" + cols.length + " rows in set " + secs(t0));
        }
      } catch (e) {
        if (e instanceof SqlError) { out.push(e.text); break; }
        throw e;
      }
    }
    return out.join("\n\n");
  }

  window.DBMS_QUERY = { run: run };
})();
