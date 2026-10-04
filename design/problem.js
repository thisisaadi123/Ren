// Ren — a problem (problem.html?id=…): the statement, an editor in each
// language, test cases you can edit, and Run / Submit against the judge
// (/api/dsa/run and /api/dsa/submit). Code, cases and the pane sizes are
// kept in this browser. Ren's pane has a chat tab (blank for now) and the
// problem's full solution (solution.js), shown only when asked for.
// sql-problem.html uses the same workspace for SQL: tables instead of
// arguments, SQLite as the only language, and /api/sql for the judge.
(() => {
  const main = document.getElementById("ws");
  const $ = (sel, root = main) => root.querySelector(sel);
  const id = new URLSearchParams(location.search).get("id") || "";
  const SQL = main.dataset.track === "sql";
  // A SQL "change" problem is answered with an UPDATE, DELETE or INSERT and
  // judged on the table it leaves behind.
  const CHANGE = () => SQL && problem && problem.mode === "change";
  const API = SQL ? "/api/sql" : "/api/dsa";
  const SHEET = SQL ? "sql.html" : "dsa.html";
  const sid = SQL ? `sql:${id}` : id; // what this browser keys the problem's code, cases and timer by

  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const show = (v) => JSON.stringify(v);
  const store = {
    get(key, fallback = null) {
      try {
        const v = localStorage.getItem(key);
        return v === null ? fallback : JSON.parse(v);
      } catch {
        return fallback;
      }
    },
    set(key, value) {
      try {
        localStorage.setItem(key, JSON.stringify(value));
      } catch {}
    },
  };

  let problem;

  /* Statement --------------------------------------------------------------- */

  // The small Markdown the statements use: paragraphs, "- " lists, a
  // **Label** line on its own, **bold** and `code`.
  function inline(text) {
    return text
      .split(/(`[^`]*`)/)
      .map((part) =>
        part.startsWith("`") && part.endsWith("`") && part.length > 1
          ? `<code>${esc(part.slice(1, -1))}</code>`
          : esc(part).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
      )
      .join("");
  }

  function markdown(md) {
    const out = [];
    for (const block of md.split(/\n\s*\n/)) {
      const lines = block.split("\n").filter((l) => l.trim());
      let i = 0;
      while (i < lines.length) {
        const label = lines[i].match(/^\*\*([^*]+)\*\*\s*$/);
        if (label) {
          out.push(`<h2 class="prob-label">${esc(label[1])}</h2>`);
          i++;
        } else if (lines[i].startsWith("- ")) {
          const items = [];
          while (i < lines.length && lines[i].startsWith("- ")) items.push(`<li>${inline(lines[i++].slice(2))}</li>`);
          out.push(`<ul>${items.join("")}</ul>`);
        } else {
          const para = [];
          while (i < lines.length && !lines[i].startsWith("- ") && !/^\*\*[^*]+\*\*\s*$/.test(lines[i])) para.push(lines[i++]);
          out.push(`<p>${inline(para.join(" "))}</p>`);
        }
      }
    }
    return out.join("");
  }

  /* SQL: the tables a problem works with, and data as grids ------------------ */

  const ICON_TABLE = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 10v10"/></svg>';

  // A table's columns, the way the landing's SQL window lists them.
  function schemaHTML(t) {
    const cols = t.columns
      .map(([name, type, key = ""]) => {
        const ref = key.startsWith("fk ") ? `<em class="col-ref" title="Refers to ${esc(key.slice(3))}">→ ${esc(key.slice(3))}</em>` : "";
        const pk = key === "pk" ? '<em class="col-key" title="Primary key: unique for every row">key</em>' : "";
        return `<li><span>${esc(name)}${pk}${ref}</span><i>${esc(type.toLowerCase())}</i></li>`;
      })
      .join("");
    return `<div class="schema-table"><b>${ICON_TABLE}${esc(t.name)}</b><ul>${cols}</ul></div>`;
  }

  const cellHTML = (v) =>
    v === null ? '<td class="null">NULL</td>' : `<td${typeof v === "number" ? ' class="num"' : ""}>${esc(v)}</td>`;

  // Rows as a grid, cut off past `max` rows.
  function tableHTML(t, { max = 40, bad = false } = {}) {
    const head = t.columns.map((c) => `<th>${esc(c)}</th>`).join("");
    const body = t.rows.length
      ? t.rows.slice(0, max).map((r) => `<tr>${r.map(cellHTML).join("")}</tr>`).join("")
      : `<tr><td class="empty" colspan="${Math.max(1, t.columns.length)}">No rows</td></tr>`;
    const more = t.rows.length > max ? `<p class="rtable-more">${t.rows.length - max} more ${t.rows.length - max === 1 ? "row" : "rows"} not shown</p>` : "";
    return `<div class="rtable${bad ? " bad" : ""}"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>${more}`;
  }

  // A dataset: every table of the problem, with its rows.
  const datasetHTML = (data) =>
    problem.tables
      .map((t) => `<div class="data-table"><h3>${esc(t.name)}</h3>${tableHTML({ columns: t.columns.map((c) => c[0]), rows: data[t.name] || [] })}</div>`)
      .join("");

  const argsText = (args) =>
    problem.params.map((p) => `${p.name} = ${show(args[p.name])}`).join(", ");

  function renderProblem() {
    const DIFF = { easy: "Easy", medium: "Medium", hard: "Hard" };
    document.title = `${problem.title} — Ren`;
    $("[data-meta]").innerHTML = [
      `<span class="diff ${esc(problem.difficulty)}">${DIFF[problem.difficulty] || esc(problem.difficulty)}</span>`,
      problem.topic && esc(problem.topic.name),
      problem.pattern && esc(problem.pattern.name),
    ]
      .filter(Boolean)
      .join(" · ");
    $("[data-title]").textContent = problem.title;
    $("[data-statement]").innerHTML = markdown(problem.statement);
    $("[data-notes]").innerHTML = markdown(problem.notes);
    if (SQL) {
      $("[data-tables]").innerHTML = `<h2 class="prob-label">Tables</h2><div class="schema">${problem.tables.map(schemaHTML).join("")}</div>`;
      $("[data-examples]").innerHTML = problem.examples
        .map(
          (ex, i) => `
          <h2 class="prob-label">Example ${i + 1}</h2>
          <div class="sql-example">
            ${datasetHTML(ex.data)}
            <div class="data-table"><h3>${CHANGE() ? `${esc(problem.result_table)} afterwards` : "Output"}</h3>${tableHTML(ex.expected)}</div>
            ${ex.explanation ? `<p class="sql-why">${inline(ex.explanation)}</p>` : ""}
          </div>`
        )
        .join("");
    } else $("[data-examples]").innerHTML = problem.examples
      .map(
        (ex, i) => `
          <h2 class="prob-label">Example ${i + 1}</h2>
          <div class="example">
            ${window.renVisual ? renVisual.exampleFigure(problem, ex) : ""}
            <div class="ex-row"><b>Input</b><span>${esc(argsText(ex.args))}</span></div>
            <div class="ex-row"><b>Output</b><span>${esc(show(ex.expected))}</span></div>
            ${ex.explanation ? `<div class="ex-row why"><b>Why</b><span>${inline(ex.explanation)}</span></div>` : ""}
          </div>`
      )
      .join("");

    // The walkthrough runs the solution step by step, so it stays behind a
    // spoiler warning until the reader asks for it (remembered per problem).
    const walk = $("[data-walk]");
    const spec = problem.visual && problem.visual.walkthrough;
    const walkKey = `ren:walk:${id}`;
    if (walk && spec && window.renVisual) {
      const paint = (state) => {
        store.set(walkKey, state);
        if (state === "shown") {
          walk.innerHTML = `<h2 class="prob-label">Walkthrough</h2>${spec.title ? `<p class="walk-intro">${inline(spec.title)}</p>` : ""}<div data-walk-player></div>`;
          renVisual.walkthrough($("[data-walk-player]"), spec);
        } else if (state === "hidden") {
          walk.innerHTML = `<h2 class="prob-label">Walkthrough</h2><button type="button" class="ghost-btn walk-reopen" data-walk-show>Show walkthrough</button>`;
        } else {
          walk.innerHTML = `<h2 class="prob-label">Walkthrough</h2>
            <div class="walk-gate">
              <p>The walkthrough steps through a solution, so it may give away how to solve this problem.</p>
              <div class="walk-gate-btns">
                <button type="button" class="btn btn-primary btn-sm" data-walk-show>Show walkthrough</button>
                <button type="button" class="ghost-btn" data-walk-hide>Not now</button>
              </div>
            </div>`;
        }
        const yes = walk.querySelector("[data-walk-show]");
        const no = walk.querySelector("[data-walk-hide]");
        if (yes) yes.onclick = () => paint("shown");
        if (no) no.onclick = () => paint("hidden");
      };
      paint(store.get(walkKey, "ask"));
    } else if (walk) {
      walk.innerHTML = "";
    }

    document.querySelector("[data-crumb-title]").textContent = problem.title;
    const topicLink = document.querySelector("[data-topic-link]");
    if (problem.topic) {
      topicLink.textContent = problem.topic.name;
      topicLink.href = `${SHEET}?q=${encodeURIComponent(problem.topic.name)}`;
    } else {
      document.querySelectorAll(".ws-topic").forEach((el) => el.remove());
    }
  }

  /* Editor ------------------------------------------------------------------ */

  const editorEl = $("[data-editor]");
  const input = $(".code-input");
  const hl = $(".code-hl");
  const gutter = $(".gutter");
  const langSelect = $("[data-lang]");
  const fileLabel = $("[data-file]");
  const savedNote = $("[data-saved]");

  const KEYWORDS = [
    "def", "return", "if", "elif", "else", "for", "while", "in", "and", "or", "not", "is", "lambda", "class",
    "import", "from", "as", "with", "try", "except", "finally", "raise", "pass", "break", "continue", "yield",
    "None", "True", "False", "self", "function", "const", "let", "var", "of", "new", "this", "typeof",
    "public", "private", "protected", "static", "final", "int", "long", "double", "float", "char", "boolean",
    "void", "auto", "bool", "string", "vector", "unordered_map", "unordered_set", "map", "set", "pair",
    "null", "nullptr", "true", "false", "func", "range", "package", "struct", "switch", "case", "default",
    "do", "using", "namespace", "template", "typename", "include", "sizeof", "unsigned", "typedef", "enum",
    "extends", "implements", "interface", "throw", "throws", "assert", "del", "nonlocal", "global",
  ].join("|");

  const tokensFor = (comment) =>
    new RegExp(
      [
        `(${comment === "#" ? "#" : "//"}[^\\n]*)`, // 1 comment
        "(\"(?:[^\"\\\\\\n]|\\\\.)*\"|'(?:[^'\\\\\\n]|\\\\.)*')", // 2 string
        `\\b(${KEYWORDS})\\b`, // 3 keyword
        "\\b(\\d+(?:\\.\\d+)?)\\b", // 4 number
        "\\b([A-Za-z_]\\w*)(?=\\()", // 5 function call
      ].join("|"),
      "g"
    );
  const SQL_KEYWORDS = [
    "select", "from", "where", "and", "or", "not", "in", "is", "null", "as", "on", "join", "left", "right", "full",
    "inner", "outer", "cross", "natural", "using", "group", "by", "order", "having", "limit", "offset", "distinct",
    "union", "all", "intersect", "except", "case", "when", "then", "else", "end", "with", "recursive", "over",
    "partition", "rows", "range", "between", "preceding", "following", "current", "row", "unbounded", "asc", "desc",
    "like", "glob", "exists", "values", "cast", "filter", "window", "nulls", "first", "last", "true", "false",
  ].join("|");
  const SQL_TOKENS = new RegExp(
    [
      "(--[^\\n]*)", // 1 comment
      "('(?:[^']|'')*')", // 2 string
      `\\b(${SQL_KEYWORDS})\\b`, // 3 keyword
      "\\b(\\d+(?:\\.\\d+)?)\\b", // 4 number
      "\\b([A-Za-z_]\\w*)(?=\\()", // 5 function call
    ].join("|"),
    "gi"
  );
  const CLASS = [null, "tk-c", "tk-s", "tk-k", "tk-n", "tk-f"];
  let tokens = tokensFor("#");
  let lang;

  const highlight = (src, re = tokens) => {
    let out = "";
    let last = 0;
    for (const m of src.matchAll(re)) {
      out += esc(src.slice(last, m.index));
      const group = m.findIndex((g, i) => i > 0 && g !== undefined);
      out += `<span class="${CLASS[group]}">${esc(m[0])}</span>`;
      last = m.index + m[0].length;
    }
    return out + esc(src.slice(last));
  };

  // Any language's code, highlighted (the Solution tab's code blocks).
  const LANG_TOKENS = { python: tokensFor("#"), other: tokensFor("//") };
  const highlightAs = (src, l) => highlight(src, l === "python" ? LANG_TOKENS.python : LANG_TOKENS.other);

  const render = () => {
    const src = input.value;
    hl.innerHTML = highlight(src) + "\n "; // keeps the last line's height
    gutter.textContent = Array.from({ length: src.split("\n").length }, (_, i) => i + 1).join("\n");
    input.style.height = `${hl.offsetHeight}px`;
  };

  const codeKey = (l) => `ren:code:${sid}:${l}`;
  const language = () => problem.languages.find((l) => l.id === lang);

  let saveTimer;
  input.addEventListener("input", () => {
    render();
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      store.set(codeKey(lang), input.value);
      savedNote.textContent = "Saved in this browser";
    }, 400);
  });

  // Replace a range, keeping native undo where the browser allows it.
  function replaceRange(start, end, text, selStart, selEnd) {
    input.focus();
    input.setSelectionRange(start, end);
    if (!document.execCommand("insertText", false, text)) {
      input.setRangeText(text, start, end, "end");
      input.dispatchEvent(new Event("input"));
    }
    if (selStart !== undefined) input.setSelectionRange(selStart, selEnd ?? selStart);
  }

  const INDENT = "    ";
  const lineStart = (pos) => input.value.lastIndexOf("\n", pos - 1) + 1;

  // Indent or outdent every line the selection touches.
  function shiftLines(outdent) {
    const { selectionStart: s, selectionEnd: e, value } = input;
    const from = lineStart(s);
    const to = value.indexOf("\n", e - (e > s && value[e - 1] === "\n" ? 1 : 0));
    const end = to < 0 ? value.length : to;
    const lines = value.slice(from, end).split("\n");
    let firstDelta = 0;
    let total = 0;
    const next = lines.map((line, i) => {
      if (!outdent) {
        if (i === 0) firstDelta = INDENT.length;
        total += INDENT.length;
        return INDENT + line;
      }
      const cut = line.match(/^ {1,4}|^\t/)?.[0].length ?? 0;
      if (i === 0) firstDelta = -cut;
      total -= cut;
      return line.slice(cut);
    });
    replaceRange(from, end, next.join("\n"), Math.max(from, s + firstDelta), Math.max(from, e + total));
  }

  input.addEventListener("keydown", (e) => {
    const mod = e.metaKey || e.ctrlKey;
    if (mod && e.key === "Enter") {
      e.preventDefault();
      e.shiftKey ? submit() : runCases();
      return;
    }
    if (mod && e.key.toLowerCase() === "s") {
      e.preventDefault();
      store.set(codeKey(lang), input.value);
      savedNote.textContent = "Saved in this browser";
      return;
    }
    const { selectionStart: s, selectionEnd: end, value } = input;
    if (e.key === "Tab") {
      e.preventDefault();
      if (e.shiftKey || value.slice(s, end).includes("\n")) shiftLines(e.shiftKey);
      else replaceRange(s, end, INDENT);
    } else if (e.key === "Enter" && !mod && !e.altKey) {
      // Carry the indent forward; one level deeper after ":", "{", "(" or "[".
      e.preventDefault();
      const line = value.slice(lineStart(s), s);
      let indent = line.match(/^\s*/)[0];
      const opens = /[:{([]\s*$/.test(line);
      if (opens) indent += INDENT;
      // Between a pair, put the closer on its own line.
      if (opens && /^[}\])]/.test(value.slice(end))) {
        const outer = indent.slice(INDENT.length);
        replaceRange(s, end, `\n${indent}\n${outer}`, s + 1 + indent.length);
      } else {
        replaceRange(s, end, `\n${indent}`);
      }
    } else if (e.key === "Backspace" && s === end && s > 0) {
      // In leading spaces, one press removes one indent level.
      const before = value.slice(lineStart(s), s);
      if (/^ +$/.test(before) && before.length % INDENT.length === 0) {
        e.preventDefault();
        replaceRange(s - INDENT.length, s, "");
      }
    }
  });

  editorEl.addEventListener("mousedown", (e) => {
    if (e.target !== input) {
      e.preventDefault();
      input.focus();
    }
  });

  function setLanguage(next, { focus = false } = {}) {
    lang = next;
    if (!SQL) store.set("ren:lang", lang);
    const l = language();
    langSelect.value = lang;
    fileLabel.textContent = l.file;
    tokens = SQL ? SQL_TOKENS : tokensFor(lang === "python" ? "#" : "//");
    input.value = store.get(codeKey(lang), l.starter);
    savedNote.textContent = store.get(codeKey(lang)) ? "Saved in this browser" : "";
    render();
    if (focus) caretToBody();
  }

  // The caret goes where the answer starts: the starter's blank line.
  function caretToBody() {
    const at = input.value === language().starter ? bodyAt(input.value) : input.value.length;
    input.focus({ preventScroll: true });
    input.setSelectionRange(at, at);
  }
  const bodyAt = (code) => {
    const m = code.match(/\n( +)\n|\n( +)$/);
    return m ? m.index + 1 + (m[1] ?? m[2]).length : code.length;
  };

  langSelect.addEventListener("change", () => setLanguage(langSelect.value, { focus: true }));

  $("[data-reset]").addEventListener("click", () => {
    const starter = language().starter;
    replaceRange(0, input.value.length, starter);
    const at = bodyAt(starter);
    input.setSelectionRange(at, at);
    try {
      localStorage.removeItem(codeKey(lang));
    } catch {}
    savedNote.textContent = "Back to the starter code. Undo brings yours back.";
    editorEl.classList.remove("flash");
    void editorEl.offsetWidth;
    editorEl.classList.add("flash");
  });

  /* Console: tabs ----------------------------------------------------------- */

  const consoleTabs = [...main.querySelectorAll("[data-console]")];
  const panels = {
    cases: $('[data-panel="cases"]'),
    result: $('[data-panel="result"]'),
  };

  consoleTabs.forEach((tab) =>
    tab.addEventListener("click", () => {
      Object.entries(panels).forEach(([key, panel]) => (panel.hidden = key !== tab.dataset.console));
    })
  );
  const showPanel = (key) => consoleTabs.find((t) => t.dataset.console === key).click();

  /* Test cases ---------------------------------------------------------------- */

  const casesKey = `ren:cases:${sid}`;
  const MAX_CASES = 8;
  // Each case keeps its fields as text, so a half-typed value survives.
  let cases = [];
  let caseAt = 0;
  let caseErrors = new Map(); // index -> message

  const icons = {
    plus: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M8 3v10M3 8h10"/></svg>',
  };

  const fromArgs = (args) => Object.fromEntries(problem.params.map((p) => [p.name, show(args[p.name])]));
  const defaultCases = () => problem.cases.map((c) => fromArgs(c.args));

  function saveCases() {
    const same = JSON.stringify(cases) === JSON.stringify(defaultCases());
    if (same) {
      try {
        localStorage.removeItem(casesKey);
      } catch {}
    } else store.set(casesKey, cases);
  }

  // SQL cases are the examples' tables, to look at (not edit).
  function renderSqlCases() {
    const bar = problem.examples
      .map((_, i) => `<button type="button" class="case-btn" role="tab" aria-selected="${i === caseAt}" data-case="${i}">Case ${i + 1}</button>`)
      .join("");
    panels.cases.innerHTML = `
      <div class="cases-bar" role="tablist" aria-label="Test cases">${bar}</div>
      <div class="sql-cases">${datasetHTML(problem.examples[caseAt].data)}</div>
      <p class="result-note sql-cases-note">Run checks your ${CHANGE() ? "statement" : "query"} on these tables. Submit also runs it on hidden ones.</p>`;
  }

  function renderCases() {
    if (SQL) return renderSqlCases();
    const panel = panels.cases;
    const bar = cases
      .map(
        (_, i) =>
          `<button type="button" class="case-btn" role="tab" aria-selected="${i === caseAt}" data-case="${i}">Case ${i + 1}</button>`
      )
      .join("");
    const add = cases.length < MAX_CASES ? `<button type="button" class="case-add" data-add-case aria-label="Add a case" title="Add a case">${icons.plus}</button>` : "";
    const remove = cases.length > 1 ? `<button type="button" class="ghost-btn case-remove" data-remove-case>Remove case ${caseAt + 1}</button>` : "";
    const current = cases[caseAt];
    const error = caseErrors.get(caseAt);
    panel.innerHTML = `
      <div class="cases-bar" role="tablist" aria-label="Test cases">${bar}${add}</div>
      ${problem.params
        .map(
          (p) => `
          <div class="field">
            <label class="field-label" for="field-${esc(p.name)}">${esc(p.name)} =</label>
            <textarea class="field-input${error ? " invalid" : ""}" id="field-${esc(p.name)}" data-param="${esc(p.name)}" rows="1" spellcheck="false" autocapitalize="off" autocomplete="off">${esc(current[p.name] ?? "")}</textarea>
          </div>`
        )
        .join("")}
      ${error ? `<p class="field-error" role="alert">${esc(error)}</p>` : ""}
      ${remove}`;
    panel.querySelectorAll(".field-input").forEach(grow);
    // Keep the chosen case in view when the row scrolls.
    const row = panel.querySelector(".cases-bar");
    const pick = row.querySelector('[aria-selected="true"]');
    if (pick.offsetLeft + pick.offsetWidth > row.scrollLeft + row.clientWidth || pick.offsetLeft < row.scrollLeft) {
      row.scrollLeft = pick.offsetLeft - 16;
    }
  }

  function grow(el) {
    el.style.height = "auto";
    el.style.height = `${el.scrollHeight}px`;
  }

  panels.cases.addEventListener("click", (e) => {
    const pick = e.target.closest("[data-case]");
    if (pick) {
      caseAt = Number(pick.dataset.case);
      renderCases();
    } else if (e.target.closest("[data-add-case]")) {
      cases.push({ ...cases[caseAt] });
      caseAt = cases.length - 1;
      saveCases();
      renderCases();
      panels.cases.querySelector(".field-input")?.focus();
    } else if (e.target.closest("[data-remove-case]")) {
      cases.splice(caseAt, 1);
      caseErrors = new Map();
      caseAt = Math.min(caseAt, cases.length - 1);
      saveCases();
      renderCases();
    }
  });

  panels.cases.addEventListener("input", (e) => {
    const field = e.target.closest("[data-param]");
    if (!field) return;
    cases[caseAt][field.dataset.param] = field.value;
    grow(field);
    if (caseErrors.has(caseAt)) {
      caseErrors.delete(caseAt);
      field.classList.remove("invalid");
      panels.cases.querySelector(".field-error")?.remove();
    }
    saveCases();
  });

  panels.cases.addEventListener("keydown", (e) => {
    if (e.target.closest("[data-param]") && (e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      e.shiftKey ? submit() : runCases();
    }
  });

  // The cases as values, or the first one that doesn't parse.
  function parseCases() {
    const out = [];
    for (const [i, c] of cases.entries()) {
      const args = {};
      for (const p of problem.params) {
        try {
          args[p.name] = JSON.parse(c[p.name]);
        } catch {
          return { error: { index: i, message: `${p.name} isn't valid. Write it as JSON, like ${exampleOf(p.type)}.` } };
        }
      }
      out.push({ args });
    }
    return { cases: out };
  }
  const exampleOf = (type) =>
    ({ "int[]": "[1, 2, 3]", "int[][]": "[[1, 2], [3, 4]]", string: '"abc"', "string[]": '["a", "b"]', bool: "true", double: "1.5" })[type] ?? "5";

  /* Run and Submit ------------------------------------------------------------- */

  const runBtn = $("[data-run]");
  const submitBtn = $("[data-submit]");
  const codePane = $(".pane-code");
  const resultPanel = panels.result;
  let busy = false;

  const TITLES = {
    passed: "Accepted",
    accepted: "Accepted",
    wrong: "Wrong answer",
    error: "Runtime error",
    time: "Time limit exceeded",
    compile: "Compile error",
  };

  function setBusy(on, btn) {
    busy = on;
    codePane.classList.toggle("busy", on);
    [runBtn, submitBtn].forEach((b) => {
      b.disabled = on;
      b.classList.toggle("loading", on && b === btn);
    });
  }

  const block = (label, text, cls = "") =>
    `<div class="out-block${cls === "error" ? " error" : ""}"><h3>${esc(label)}</h3><pre${cls && cls !== "error" ? ` class="${cls}"` : ""}>${esc(text)}</pre></div>`;

  function message(text) {
    resultPanel.innerHTML = `<div class="result-empty">${esc(text)}</div>`;
  }

  async function send(path, body) {
    try {
      const res = await renApi(path, body);
      if (!res.ok) return { error: res.data.error || "Something went wrong. Try again." };
      return res.data;
    } catch {
      return { error: "Can't reach the Ren server." };
    }
  }

  async function runCases() {
    if (busy) return;
    if (SQL) {
      const n = problem.examples.length;
      setBusy(true, runBtn);
      showPanel("result");
      message(`Running your ${CHANGE() ? "statement" : "query"} on ${n} example ${n === 1 ? "dataset" : "datasets"}…`);
      const data = await send(`${API}/run`, { id, code: input.value });
      setBusy(false);
      if (data.error) return message(data.error);
      return renderRun(data, Math.max(0, data.cases.findIndex((c) => c.verdict !== "passed")));
    }
    const parsed = parseCases();
    if (parsed.error) {
      caseErrors = new Map([[parsed.error.index, parsed.error.message]]);
      caseAt = parsed.error.index;
      showPanel("cases");
      renderCases();
      return;
    }
    caseErrors = new Map();
    renderCases();
    setBusy(true, runBtn);
    showPanel("result");
    message(`Running your code on ${parsed.cases.length} ${parsed.cases.length === 1 ? "case" : "cases"}…`);
    const data = await send("/api/dsa/run", { id, lang, code: input.value, cases: parsed.cases });
    setBusy(false);

    if (data.error) return message(data.error);
    if (data.invalid) {
      caseErrors = new Map(data.invalid.map((x) => [x.index, x.message]));
      caseAt = data.invalid[0].index;
      showPanel("cases");
      renderCases();
      message("Fix the highlighted case, then run again.");
      return;
    }
    // Open on the first case that didn't pass.
    renderRun(data, Math.max(0, data.cases.findIndex((c) => c.verdict !== "passed")));
  }

  // How answers are checked decides what "Expected" means.
  const SUP = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
  function expectedLabel() {
    if (CHANGE()) return `Expected ${problem.result_table} (rows in any order)`;
    if (SQL) return problem.ordered ? "Expected (rows in this order)" : "Expected (rows in any order)";
    const c = problem.checker || { type: "exact" };
    if (c.type === "unordered") return "Expected (in any order)";
    if (c.type === "custom") return "One right answer";
    if (c.type === "float") {
      const exp = Math.round(Math.log10(Number(c.tolerance)));
      return `Expected (within 10${String(exp).replace(/./g, (d) => SUP[d] ?? d)})`;
    }
    return "Expected";
  }

  const ms = (n) => (n < 1 ? "under 1 ms" : `${Math.round(n)} ms`);
  // A query that SQLite rejects is a query error, not a runtime error.
  const titleOf = (verdict) => (SQL && verdict === "error" ? "Query error" : TITLES[verdict]);
  const outputHTML = (c) =>
    `<div class="out-block"><h3>${CHANGE() ? `Your ${esc(problem.result_table)} afterwards` : "Output"}${c.why ? ` <span class="why">· ${esc(c.why)}</span>` : ""}</h3>${tableHTML(c.output, { bad: c.verdict === "wrong" })}</div>`;

  let runView = { data: null, at: 0 };

  function renderRun(data, at = 0) {
    runView = { data, at };
    const list = data.cases;
    const worst = ["compile", "error", "time", "wrong"].find((v) => list.some((c) => c.verdict === v)) || "passed";
    const passed = list.filter((c) => c.verdict === "passed").length;
    const times = list.map((c) => c.ms).filter((ms) => ms != null);
    const time = times.length ? ` · ${ms(Math.max(...times))}` : "";

    if (worst === "compile") {
      const c = list.find((x) => x.verdict === "compile");
      resultPanel.innerHTML = `
        <div class="verdict"><h2 class="bad">Compile error</h2></div>
        ${block("Error", c.error, "error")}`;
      return;
    }

    const c = list[at];
    const bar = list
      .map(
        (x, i) =>
          `<button type="button" class="case-btn" role="tab" aria-selected="${i === at}" data-result-case="${i}"><span class="dot ${x.verdict === "passed" ? "ok" : "bad"}" aria-hidden="true"></span>Case ${i + 1}<span class="sr-only">, ${x.verdict === "passed" ? "passed" : "failed"}</span></button>`
      )
      .join("");
    if (SQL) {
      resultPanel.innerHTML = `
        <div class="verdict">
          <h2 class="${worst === "passed" ? "ok" : "bad"}">${titleOf(worst)}</h2>
          <span>${passed} of ${list.length} ${list.length === 1 ? "case" : "cases"} passed${time}</span>
        </div>
        <div class="cases-bar" role="tablist" aria-label="Results">${bar}</div>
        ${c.error ? block("Error", c.error, "error") : ""}
        ${c.verdict === "time" ? `<p class="result-note">The query ran for too long and was stopped. Look for a recursive query that never ends, or a join that multiplies rows.</p>` : ""}
        ${c.output ? outputHTML(c) : ""}
        <div class="out-block"><h3>${expectedLabel()}</h3>${tableHTML(c.expected)}</div>`;
      return;
    }
    resultPanel.innerHTML = `
      <div class="verdict">
        <h2 class="${worst === "passed" ? "ok" : "bad"}">${TITLES[worst]}</h2>
        <span>${passed} of ${list.length} ${list.length === 1 ? "case" : "cases"} passed${time}</span>
      </div>
      <div class="cases-bar" role="tablist" aria-label="Results">${bar}</div>
      ${problem.params.map((p) => block(`${p.name} =`, show(c.args[p.name]))).join("")}
      ${c.output !== undefined ? block("Output", c.output, c.verdict === "wrong" ? "bad" : "") : ""}
      ${block(expectedLabel(), c.expected)}
      ${c.stdout ? block("Printed", c.stdout) : ""}
      ${c.error ? block("Error", c.error, "error") : ""}`;
  }

  resultPanel.addEventListener("click", (e) => {
    const pick = e.target.closest("[data-result-case]");
    if (pick && runView.data) renderRun(runView.data, Number(pick.dataset.resultCase));
  });

  async function submit() {
    if (busy) return;
    setBusy(true, submitBtn);
    showPanel("result");
    message("Submitting: running every test, hidden ones included…");
    const data = await send(`${API}/submit`, SQL ? { id, code: input.value } : { id, lang, code: input.value });
    setBusy(false);
    runView = { data: null, at: 0 };
    if (data.error) return message(data.error);

    const ok = data.verdict === "accepted";
    const time = data.ms != null ? ` · ${ms(data.ms)}` : "";
    let body = "";
    if (ok) {
      const hidden = data.total - (SQL ? problem.examples : problem.cases).length;
      body = `<p class="result-note">Your code passed every test${hidden > 0 ? `, including ${hidden} hidden ones` : ""}.</p>`;
      store.set(`ren:solved:${sid}`, Date.now());
      timer.finish();
    } else if (SQL && data.verdict === "time") {
      body = `<p class="result-note">The query ran for too long and was stopped. Look for a recursive query that never ends, or a join that multiplies rows.</p>`;
    } else if (SQL && data.failed) {
      const f = data.failed;
      const where = `<p class="result-note">Failed on test ${f.number} of ${data.total}${f.hidden ? ", a hidden test" : ""}.</p>`;
      if (f.error) body = where + block("Error", f.error, "error");
      else {
        const input = f.data
          ? `<div class="out-block"><h3>Tables</h3><div class="sql-cases">${datasetHTML(f.data)}</div></div>`
          : `<p class="result-note">This test's tables hold ${f.rows} rows, too many to show here.</p>`;
        body = where + input + outputHTML(f) + `<div class="out-block"><h3>${expectedLabel()}</h3>${tableHTML(f.expected)}</div>`;
      }
    } else if (data.failed) {
      const f = data.failed;
      const where = data.verdict === "compile" ? "" : `<p class="result-note">Failed on test ${f.number} of ${data.total}${f.hidden ? ", a hidden test" : ""}.</p>`;
      body =
        where +
        (data.verdict === "compile"
          ? block("Error", f.error, "error")
          : [
              ...problem.params.map((p) => block(`${p.name} =`, f.args[p.name])),
              f.output !== undefined ? block("Output", f.output, "bad") : "",
              block(expectedLabel(), f.expected),
              f.stdout ? block("Printed", f.stdout) : "",
              f.error ? block("Error", f.error, "error") : "",
            ].join(""));
    }
    resultPanel.innerHTML = `
      <div class="verdict">
        <h2 class="${ok ? "ok" : "bad"}">${titleOf(data.verdict) || "Not accepted"}</h2>
        ${data.verdict === "compile" ? "" : `<span>${data.passed} of ${data.total} tests passed${time}</span>`}
      </div>
      ${body}`;
  }

  runBtn.addEventListener("click", runCases);
  submitBtn.addEventListener("click", submit);

  /* Timer -------------------------------------------------------------------- */

  // Counts up while you work on the problem. Select it to pause; it stops
  // for good once a submission is accepted.
  const timer = (() => {
    const el = document.querySelector("[data-timer]");
    const key = `ren:timer:${sid}`;
    let { spent = 0, paused = false, done = false } = store.get(key, {}) || {};
    let tick;
    const fmt = (s) => {
      const h = Math.floor(s / 3600);
      const m = String(Math.floor((s % 3600) / 60)).padStart(2, "0");
      const sec = String(s % 60).padStart(2, "0");
      return h ? `${h}:${m}:${sec}` : `${m}:${sec}`;
    };
    const paint = () => {
      el.textContent = fmt(spent);
      el.classList.toggle("paused", paused && !done);
      el.classList.toggle("done", done);
      el.setAttribute("aria-label", done ? `Solved in ${fmt(spent)}` : `Timer ${fmt(spent)}. Select to ${paused ? "resume" : "pause"}.`);
    };
    const save = () => store.set(key, { spent, paused, done });
    const start = () => {
      clearInterval(tick);
      if (paused || done) return;
      tick = setInterval(() => {
        if (document.hidden) return;
        spent++;
        paint();
        if (spent % 5 === 0) save();
      }, 1000);
    };
    el.addEventListener("click", () => {
      if (done) return;
      paused = !paused;
      save();
      paint();
      start();
    });
    addEventListener("pagehide", save);
    return {
      begin() {
        paint();
        start();
      },
      finish() {
        done = true;
        clearInterval(tick);
        save();
        paint();
      },
    };
  })();

  /* Pane sizes ---------------------------------------------------------------- */

  const LAYOUT_KEY = "ren:ws:layout";
  // Big screens start with more room for reading.
  const DEFAULTS = innerWidth >= 1600 ? { prob: 480, ren: 480, console: 240 } : { prob: 440, ren: 360, console: 240 };
  const layout = { ...DEFAULTS, ...(store.get(LAYOUT_KEY, {}) || {}) };

  function limits(which) {
    const w = main.clientWidth;
    if (which === "prob") return [280, Math.max(280, Math.min(w * 0.5, w - 560))];
    // Ren can grow until the code has 420px left, up to 820px.
    if (which === "ren") return [260, Math.max(260, Math.min(820, w - 32 - clamp("prob", layout.prob) - 420))];
    const h = codePane.clientHeight;
    return [96, Math.max(96, h - 48 - 56 - 120)];
  }
  const clamp = (which, v) => {
    const [lo, hi] = limits(which);
    return Math.round(Math.min(hi, Math.max(lo, v)));
  };

  function applyLayout() {
    main.style.setProperty("--prob-w", `${clamp("prob", layout.prob)}px`);
    main.style.setProperty("--ren-w", `${clamp("ren", layout.ren)}px`);
    main.style.setProperty("--console-h", `${clamp("console", layout.console)}px`);
    const wide = clamp("ren", layout.ren) >= limits("ren")[1] - 4;
    widenBtn.setAttribute("aria-pressed", String(wide));
    widenBtn.title = wide ? "Narrow Ren's pane" : "Widen Ren's pane";
    widenBtn.querySelector(".sr-only").textContent = wide ? "Narrow" : "Widen";
  }

  // Widen gives Ren all the room the code can spare; pressed again, back to the default.
  const widenBtn = document.querySelector("[data-widen]");
  widenBtn.addEventListener("click", () => {
    layout.ren = widenBtn.getAttribute("aria-pressed") === "true" ? DEFAULTS.ren : limits("ren")[1];
    applyLayout();
    store.set(LAYOUT_KEY, layout);
    dispatchEvent(new Event("resize"));
  });

  main.querySelectorAll("[data-split]").forEach((handle) => {
    const which = handle.dataset.split;
    const axis = which === "console" ? "y" : "x";

    const valueAt = (e) => {
      const box = main.getBoundingClientRect();
      if (which === "prob") return e.clientX - box.left - 8 - 4;
      if (which === "ren") return box.right - 8 - e.clientX - 4;
      const pane = codePane.getBoundingClientRect();
      const foot = $(".code-foot").offsetHeight;
      return pane.bottom - foot - e.clientY;
    };

    handle.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      handle.setPointerCapture(e.pointerId);
      handle.classList.add("dragging");
      document.body.classList.add("resizing", axis);
      const move = (ev) => {
        layout[which] = clamp(which, valueAt(ev));
        applyLayout();
      };
      const up = () => {
        handle.classList.remove("dragging");
        document.body.classList.remove("resizing", axis);
        handle.removeEventListener("pointermove", move);
        store.set(LAYOUT_KEY, layout);
        dispatchEvent(new Event("resize"));
      };
      handle.addEventListener("pointermove", move);
      handle.addEventListener("pointerup", up, { once: true });
      handle.addEventListener("pointercancel", up, { once: true });
    });

    // Arrow keys move it; a double-click puts it back.
    handle.addEventListener("keydown", (e) => {
      const grow = { x: { ArrowRight: 1, ArrowLeft: -1 }, y: { ArrowUp: 1, ArrowDown: -1 } }[axis][e.key];
      if (!grow) return;
      e.preventDefault();
      const dir = which === "ren" ? -grow : grow;
      layout[which] = clamp(which, clamp(which, layout[which]) + dir * 24);
      applyLayout();
      store.set(LAYOUT_KEY, layout);
    });
    handle.addEventListener("dblclick", () => {
      layout[which] = DEFAULTS[which];
      applyLayout();
      store.set(LAYOUT_KEY, layout);
    });
  });
  addEventListener("resize", applyLayout);

  /* Laptops: problem or Ren beside the code. Phones: one pane at a time ---------- */

  const paneTabs = [...main.querySelectorAll("[data-pane]")];
  paneTabs.forEach((tab) =>
    tab.addEventListener("click", () => {
      main.dataset.view = tab.dataset.pane;
      if (tab.dataset.pane === "ren") renPane.shown();
      // The console tabs measure themselves once they can be seen.
      requestAnimationFrame(() => {
        dispatchEvent(new Event("resize"));
        if (tab.dataset.pane === "code") render();
      });
    })
  );

  // On laptops the code is always in view, so its tab goes; Problem stands in.
  const laptop = matchMedia("(min-width: 861px) and (max-width: 1179px)");
  const fitView = () => {
    if (laptop.matches && main.dataset.view === "code") paneTabs.find((t) => t.dataset.pane === "prob").click();
  };
  laptop.addEventListener?.("change", fitView);

  /* Ren: chat and solution tabs ------------------------------------------------------ */

  const renPane = (() => {
    const renTabs = [...document.querySelectorAll("[data-ren-tab]")];
    const panelsOf = Object.fromEntries([...document.querySelectorAll("[data-ren-panel]")].map((p) => [p.dataset.renPanel, p]));
    const wide = matchMedia("(min-width: 1180px)");
    let solution = null;
    let current = "chat";

    function pick(name) {
      current = name;
      if (solution || name === "solution") store.set("ren:ren-tab", name);
      const tab = renTabs.find((t) => t.dataset.renTab === name);
      if (tab.getAttribute("aria-selected") !== "true") tab.click(); // moves the underline
      Object.entries(panelsOf).forEach(([k, p]) => (p.hidden = k !== name));
      if (name === "solution" && solution && visible()) solution.open();
    }
    // The pane is on screen: always on wide screens, else when its view is picked.
    const visible = () => wide.matches || main.dataset.view === "ren";

    renTabs.forEach((t) => t.addEventListener("click", () => current !== t.dataset.renTab && pick(t.dataset.renTab)));
    panelsOf.solution?.addEventListener("sol:close", () => pick("chat"));
    wide.addEventListener?.("change", () => current === "solution" && solution && visible() && solution.open());

    return {
      start() {
        if (panelsOf.solution && window.renSolution) {
          solution = renSolution.mount(panelsOf.solution, { id, problem, highlight: highlightAs, lang });
        }
        pick(solution && store.get("ren:ren-tab") === "solution" ? "solution" : "chat");
      },
      shown() {
        if (current === "solution" && solution) solution.open();
      },
    };
  })();

  /* Load ----------------------------------------------------------------------- */

  function state(title, line) {
    main.classList.add("is-state");
    main.innerHTML = `
      <div class="state">
        <h1>${esc(title)}</h1>
        <p>${esc(line)}</p>
        <a href="${SHEET}" class="btn btn-secondary">Back to ${SQL ? "SQL" : "DSA"}</a>
      </div>`;
  }

  const request = id
    ? renApi(`${API}/problem?id=${encodeURIComponent(id)}`).catch(() => ({ ok: false, status: 0 }))
    : Promise.resolve({ ok: false, status: 404 });

  Promise.all([renSession(main), request, renLoader.page]).then(([, res]) => {
    if (res.ok) {
      problem = res.data;
      renderProblem();

      langSelect.innerHTML = problem.languages
        .map((l) => `<option value="${l.id}"${l.available ? "" : " disabled"}>${esc(l.label)}${l.available ? "" : " (soon)"}</option>`)
        .join("");
      const ready = problem.languages.filter((l) => l.available);
      const saved = store.get("ren:lang");
      setLanguage(ready.some((l) => l.id === saved) ? saved : (ready[0] || problem.languages[0]).id);

      if (!SQL) {
        cases = store.get(casesKey) || defaultCases();
        if (!Array.isArray(cases) || !cases.length) cases = defaultCases();
      }
      renderCases();
      message(CHANGE() ? "Run your statement to see the table it leaves behind." : SQL ? "Run your query to see its rows here." : "Run your code to see the results here.");
      renPane.start();
      fitView();
      applyLayout();
      timer.begin();
    } else if (res.status === 404) {
      state("Problem not found", "It may have moved. Pick another one from the sheet.");
    } else {
      state("Couldn't load the problem", "Something went wrong on our side. Give it another try.");
    }
    renLoader.done().then(() => {
      renReveal(main);
      dispatchEvent(new Event("resize"));
      if (problem) render();
    });
  });
})();
