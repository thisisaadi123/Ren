// Ren — home page demos: practice tracks with Ren, resume builder, interview lobby
const escapeHtml = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// Run `fn` once, the first time `el` is mostly on screen.
const whenVisible = (el, fn, threshold = 0.35) => {
  if (!("IntersectionObserver" in window)) return fn();
  const io = new IntersectionObserver((entries) => {
    if (entries.some((e) => e.isIntersecting)) {
      io.disconnect();
      fn();
    }
  }, { threshold });
  io.observe(el);
};

// Count-up session timer (mm:ss), started once.
const startTimer = (el) => {
  if (!el || el.dataset.started) return;
  el.dataset.started = "1";
  let seconds = 0;
  setInterval(() => {
    seconds += 1;
    el.textContent = `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;
  }, 1000);
};

const ai = (html, label) => ({ who: "ai", html, label });
const me = (text) => ({ who: "me", html: escapeHtml(text) });

/* ==========================================================================
   Chat engine shared by every Ren chat on the page.

   - Only the first conversation a visitor sees animates (typing indicator,
     one message at a time, input disabled until it finishes). Every other
     conversation appears fully written, so nobody waits twice.
   - After that the visitor can send one message. Ren replies, and from then
     on every chat on the page is locked into a "Join Ren" button.
   ========================================================================== */
const CHAT = { animated: false, chatted: false, all: [] };

const createChat = (msgs, form, { reply }) => {
  const input = form.querySelector("input");
  let send = form.querySelector(".send");
  const idle = input.placeholder;
  let token = 0;
  let playing = false;
  let locked = false;

  const scroll = () => requestAnimationFrame(() => msgs.scrollTo({ top: msgs.scrollHeight, behavior: "smooth" }));

  const bubble = (who, html, label, follow = true) => {
    const el = document.createElement("div");
    el.className = `msg msg-${who}`;
    el.innerHTML = who === "ai" && label ? `<span class="msg-label">${label}</span>${html}` : html;
    msgs.appendChild(el);
    if (follow) scroll();
    return el;
  };

  const typing = () => {
    const el = document.createElement("div");
    el.className = "msg msg-ai typing";
    el.setAttribute("aria-label", "Ren is typing");
    el.innerHTML = "<i></i><i></i><i></i>";
    msgs.appendChild(el);
    scroll();
    return el;
  };

  const setInput = (enabled, placeholder) => {
    if (locked) return;
    input.disabled = !enabled;
    send.disabled = !enabled;
    input.placeholder = placeholder;
  };

  const lock = () => {
    if (locked) return;
    locked = true;
    input.value = "";
    input.disabled = true;
    input.placeholder = "Get started with Ren";
    const join = document.createElement("a");
    join.href = "signup.html";
    join.className = "btn btn-primary btn-sm";
    join.textContent = "Join Ren";
    send.replaceWith(join);
    send = join;
    form.classList.add("locked");
  };

  // Resolves true if this playback is still the current one.
  const wait = (ms, t) => new Promise((r) => setTimeout(() => r(t === token), ms));

  const play = async (script) => {
    const t = ++token;
    msgs.innerHTML = "";
    msgs.scrollTop = 0;

    if (CHAT.animated || CHAT.chatted) {
      script.forEach((item) => {
        bubble(item.who, item.html, item.label, false);
        item.then?.();
      });
      msgs.scrollTop = 0;
      playing = false;
      setInput(true, idle);
      return;
    }

    CHAT.animated = true; // this is the one animated conversation
    playing = true;
    setInput(false, "Ren is typing…");
    for (const item of script) {
      if (item.who === "ai") {
        if (!(await wait(300, t))) return;
        const dots = typing();
        const still = await wait(650 + Math.min(item.html.length * 5, 900), t);
        dots.remove();
        if (!still) return;
        bubble("ai", item.html, item.label);
      } else {
        if (!(await wait(450 + item.html.length * 12, t))) return;
        bubble("me", item.html);
      }
      item.then?.();
    }
    playing = false;
    setInput(true, idle);
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if (!q || playing || locked) return;
    token += 1; // nothing else may write into this chat now
    playing = true;
    bubble("me", escapeHtml(q));
    input.value = "";
    setInput(false, "Ren is typing…");
    await new Promise((r) => setTimeout(r, 300));
    const dots = typing();
    await new Promise((r) => setTimeout(r, 900));
    dots.remove();
    bubble("ai", reply(q), "Ren");
    playing = false;
    CHAT.chatted = true;
    CHAT.all.forEach((c) => c.lock()); // one free message across the whole page
  });

  // Nothing to type into until a conversation has played.
  input.disabled = true;
  send.disabled = true;

  CHAT.all.push({ lock });
  return { play };
};

// A Ren panel with Hint / Nudge / Explain / Solve conversations.
const mountRev = ({ msgs, form, levelEl, tabs, conv, reply }) => {
  const chat = createChat(msgs, form, { reply });
  let level = "nudge";
  const show = (key = level) => {
    level = key;
    const c = conv(key);
    levelEl.textContent = `Level ${c.level} of 4`;
    chat.play(c.msgs);
  };
  tabs.forEach((t) => t.addEventListener("click", () => show(t.dataset.level)));
  return { show };
};

// What kind of message did the visitor send? Ren's reply should fit it.
const messageKind = (q) => {
  if (/^(hi|hey|hello|hiya|yo|sup|good (morning|afternoon|evening))\b/i.test(q)) return "greeting";
  if (/\?\s*$/.test(q) || /^(how|what|why|when|where|which|who|can|could|should|would|is|are|do|does|did|will|am)\b/i.test(q)) return "question";
  return "statement";
};

// Replies for the practice tracks, e.g. "your code and this exact problem".
const REV_REPLY = (what) => (q) => {
  const lead = {
    greeting: `Hi there. With an account, I can work through this with ${what}.`,
    question: `Good question. With an account, I'd answer it using ${what}.`,
    statement: `Got it. With an account, I'll pick this up with ${what}.`,
  }[messageKind(q)];
  return `<p>${lead} <a href="signup.html">Get started</a> to keep going.</p>`;
};

/* ==========================================================================
   Coding: editable (not executable) editor in five languages + Ren
   ========================================================================== */
(() => {
  const editor = document.getElementById("editor");
  if (!editor) return;

  // Each language: starter code with one blank to fill, and the filled answer.
  const LANGS = {
    python: {
      file: "solution.py",
      comment: "#",
      blank: "merged[-1][1] = ",
      fill: "max(merged[-1][1], end)",
      code: [
        "def merge(intervals):",
        "    intervals.sort(key=lambda x: x[0])",
        "    merged = []",
        "",
        "    for start, end in intervals:",
        "        if merged and start <= merged[-1][1]:",
        "            merged[-1][1] = ",
        "        else:",
        "            merged.append([start, end])",
        "",
        "    return merged",
      ],
    },
    javascript: {
      file: "solution.js",
      comment: "//",
      blank: "merged.at(-1)[1] = ",
      fill: "Math.max(merged.at(-1)[1], end);",
      code: [
        "function merge(intervals) {",
        "    intervals.sort((a, b) => a[0] - b[0]);",
        "    const merged = [];",
        "",
        "    for (const [start, end] of intervals) {",
        "        if (merged.length && start <= merged.at(-1)[1]) {",
        "            merged.at(-1)[1] = ",
        "        } else {",
        "            merged.push([start, end]);",
        "        }",
        "    }",
        "    return merged;",
        "}",
      ],
    },
    java: {
      file: "Solution.java",
      comment: "//",
      blank: "last[1] = ",
      fill: "Math.max(last[1], cur[1]);",
      code: [
        "class Solution {",
        "    public int[][] merge(int[][] intervals) {",
        "        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);",
        "        List<int[]> merged = new ArrayList<>();",
        "        for (int[] cur : intervals) {",
        "            int[] last = merged.isEmpty() ? null : merged.get(merged.size() - 1);",
        "            if (last != null && cur[0] <= last[1]) {",
        "                last[1] = ",
        "            } else {",
        "                merged.add(cur);",
        "            }",
        "        }",
        "        return merged.toArray(new int[0][]);",
        "    }",
        "}",
      ],
    },
    cpp: {
      file: "solution.cpp",
      comment: "//",
      blank: "merged.back()[1] = ",
      fill: "max(merged.back()[1], cur[1]);",
      code: [
        "class Solution {",
        "public:",
        "    vector<vector<int>> merge(vector<vector<int>>& intervals) {",
        "        sort(intervals.begin(), intervals.end());",
        "        vector<vector<int>> merged;",
        "        for (auto& cur : intervals) {",
        "            if (!merged.empty() && cur[0] <= merged.back()[1])",
        "                merged.back()[1] = ",
        "            else",
        "                merged.push_back(cur);",
        "        }",
        "        return merged;",
        "    }",
        "};",
      ],
    },
    go: {
      file: "solution.go",
      comment: "//",
      blank: "merged[n-1][1] = ",
      fill: "max(merged[n-1][1], cur[1])",
      code: [
        "func merge(intervals [][]int) [][]int {",
        "    sort.Slice(intervals, func(i, j int) bool {",
        "        return intervals[i][0] < intervals[j][0]",
        "    })",
        "    merged := [][]int{}",
        "    for _, cur := range intervals {",
        "        if n := len(merged); n > 0 && cur[0] <= merged[n-1][1] {",
        "            merged[n-1][1] = ",
        "        } else {",
        "            merged = append(merged, cur)",
        "        }",
        "    }",
        "    return merged",
        "}",
      ],
    },
  };

  const KEYWORDS = [
    "def", "return", "if", "elif", "else", "for", "while", "in", "and", "or", "not", "lambda", "class",
    "import", "from", "as", "with", "try", "except", "pass", "break", "continue", "None", "True", "False",
    "function", "const", "let", "var", "of", "new", "public", "private", "static", "int", "void", "auto",
    "null", "true", "false", "func", "range", "package", "struct", "bool",
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
  const CLASS = [null, "tk-c", "tk-s", "tk-k", "tk-n", "tk-f"];

  const input = document.getElementById("code-input");
  const hl = document.getElementById("code-hl");
  const gutter = document.getElementById("gutter");
  const fileLabel = document.getElementById("editor-file");
  const langSelect = document.getElementById("editor-lang");

  let lang = "python";
  let tokens = tokensFor("#");

  const starter = () => LANGS[lang].code.join("\n");
  const blankLine = () => LANGS[lang].code.findIndex((l) => l.includes(LANGS[lang].blank)) + 1;
  const caretAfterBlank = () => starter().indexOf(LANGS[lang].blank) + LANGS[lang].blank.length;

  const highlight = (src) => {
    let out = "";
    let last = 0;
    for (const m of src.matchAll(tokens)) {
      out += escapeHtml(src.slice(last, m.index));
      const group = m.findIndex((g, i) => i > 0 && g !== undefined);
      out += `<span class="${CLASS[group]}">${escapeHtml(m[0])}</span>`;
      last = m.index + m[0].length;
    }
    return out + escapeHtml(src.slice(last));
  };

  const render = () => {
    const src = input.value;
    hl.innerHTML = highlight(src) + "\n "; // keeps the last line's height
    gutter.textContent = Array.from({ length: src.split("\n").length }, (_, i) => i + 1).join("\n");
    input.style.height = `${hl.offsetHeight}px`;
  };

  // Insert at the caret, keeping native undo where supported.
  const insert = (text) => {
    if (!document.execCommand("insertText", false, text)) {
      input.setRangeText(text, input.selectionStart, input.selectionEnd, "end");
      render();
    }
  };

  input.addEventListener("keydown", (e) => {
    if (e.key === "Tab" && !e.shiftKey) {
      e.preventDefault();
      insert("    ");
    } else if (e.key === "Enter" && !e.metaKey && !e.ctrlKey) {
      // Carry indentation forward; one level deeper after ":" or "{".
      e.preventDefault();
      const before = input.value.slice(0, input.selectionStart);
      const line = before.slice(before.lastIndexOf("\n") + 1);
      let indent = line.match(/^\s*/)[0];
      if (/[:{]\s*$/.test(line)) indent += "    ";
      insert("\n" + indent);
    }
  });
  input.addEventListener("input", render);

  editor.addEventListener("mousedown", (e) => {
    if (e.target !== input) {
      e.preventDefault();
      input.focus();
    }
  });

  const setCode = (code, caretAt, focus = true) => {
    input.value = code;
    render();
    if (focus) {
      input.focus({ preventScroll: true });
      const pos = caretAt ?? code.length;
      input.setSelectionRange(pos, pos);
    }
    editor.classList.remove("flash");
    void editor.offsetWidth; // restart the flash
    editor.classList.add("flash");
  };

  document.getElementById("editor-reset").addEventListener("click", () => setCode(starter(), caretAfterBlank()));

  // Ren: each help level has its own conversation.
  const conv = (key) => {
    const n = blankLine();
    return {
      hint: { level: 1, msgs: [
        ai(`<span class="msg-label">Hint</span><p>What does sorting by start give you? Once the intervals are in order, where can an overlap show up?</p>`),
        me("Only between neighbours?"),
        ai(`<p>Exactly. So you only ever need to compare with the last interval you merged.</p>`),
      ] },
      nudge: { level: 2, msgs: [
        ai(`<span class="msg-label">Read your code · line ${n}</span><p>Sorting by start was the right call. On line ${n}, when the next interval overlaps the last merged one, which end should survive?</p>`),
        me("The bigger one?"),
        ai(`<p>Right. Take the max there, then check it against <code>[[1,10],[2,3]]</code>.</p>`),
      ] },
      explain: { level: 3, msgs: [
        ai(`<span class="msg-label">From an empty editor</span><ol><li><b>Sort by start.</b> Overlaps end up next to each other.</li><li><b>Walk once,</b> keeping a list of merged intervals.</li><li><b>Compare with the last one.</b> If the current interval starts before it ends, extend it. Otherwise, start a new one.</li></ol>`),
        ai(`<p>Example: <code>[1,3]</code> and <code>[2,6]</code> overlap, so they become <code>[1,6]</code>. <code>[8,10]</code> starts after 6, so it stands alone.</p>`),
        me("Why sort first?"),
        ai(`<p>Unsorted, an overlap could hide anywhere, so you'd compare every pair: O(n²). Sorted, it's one pass after an O(n log n) sort.</p>`),
      ] },
      solve: { level: 4, msgs: [
        ai(`<span class="msg-label">Full solution</span><p>Line ${n} is the key: keep the larger end, so a short interval inside a longer one can't shrink it.</p><pre>${escapeHtml(LANGS[lang].blank.trim() + " " + LANGS[lang].fill)}</pre>`),
        me(`Why the max on line ${n}?`),
        ai(`<p>Take <code>[1,10]</code> then <code>[2,3]</code>. Without it, the end drops to 3 and you lose everything from 4 to 10.</p>`),
      ] },
    }[key];
  };

  const rev = mountRev({
    msgs: document.getElementById("coach-msgs"),
    form: document.getElementById("coach-form"),
    levelEl: document.getElementById("coach-level"),
    tabs: document.querySelectorAll("#coach-tabs [data-level]"),
    conv,
    reply: REV_REPLY("your code and this exact problem"),
  });

  langSelect.addEventListener("change", () => {
    lang = langSelect.value;
    tokens = tokensFor(LANGS[lang].comment);
    fileLabel.textContent = LANGS[lang].file;
    setCode(starter(), caretAfterBlank(), false);
    rev.show();
  });

  input.value = starter();
  render();
  document.fonts?.ready.then(render);

  // Timer and Ren's first conversation start once the window is on screen.
  whenVisible(editor, () => {
    startTimer(document.getElementById("practice-timer"));
    rev.show("nudge");
  });
})();

/* ==========================================================================
   Practice carousel: Coding / SQL / System design, moved only by the visitor
   ========================================================================== */
(() => {
  const car = document.getElementById("practice-carousel");
  if (!car) return;

  const tabs = [...car.querySelectorAll(".car-tabs [data-slide]")];
  const thumb = car.querySelector(".car-tabs .seg-thumb");
  const slides = [...car.querySelectorAll(".car-slide")];
  const track = document.getElementById("car-track");
  const [prev, next] = car.querySelectorAll(".car-arrow");
  const indexLabel = document.getElementById("car-index");
  let current = 0;

  const placeThumb = () => {
    const t = tabs[current];
    thumb.style.width = `${t.offsetWidth}px`;
    thumb.style.transform = `translateX(${t.offsetLeft}px)`;
  };

  const go = (i) => {
    current = Math.max(0, Math.min(slides.length - 1, i));
    track.style.transform = `translateX(calc(${-current} * (100% + var(--gap))))`;
    slides.forEach((s, j) => {
      const on = j === current;
      s.setAttribute("aria-hidden", String(!on));
      s.toggleAttribute("inert", !on);
    });
    tabs.forEach((t, j) => t.setAttribute("aria-selected", String(j === current)));
    placeThumb();
    indexLabel.textContent = current + 1;
    prev.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    window.dispatchEvent(new CustomEvent("car:shown", { detail: current }));
  };

  tabs.forEach((t, i) => t.addEventListener("click", () => go(i)));
  prev.addEventListener("click", () => go(current - 1));
  next.addEventListener("click", () => go(current + 1));

  car.querySelector(".car-bar").addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") go(current + 1);
    else if (e.key === "ArrowLeft") go(current - 1);
    else return;
    e.preventDefault();
    tabs[current].focus();
  });

  // Swipe on touch screens (never while typing or drawing on the canvas).
  const viewport = car.querySelector(".car-viewport");
  let startX = null;
  viewport.addEventListener("pointerdown", (e) => {
    if (e.pointerType !== "touch" || e.target.closest("textarea, input, .sd-canvas")) return;
    startX = e.clientX;
  });
  viewport.addEventListener("pointerup", (e) => {
    if (startX === null) return;
    const dx = e.clientX - startX;
    startX = null;
    if (Math.abs(dx) > 50) go(current + (dx < 0 ? 1 : -1));
  });

  window.addEventListener("resize", placeThumb);
  document.fonts?.ready.then(placeThumb);
  go(0);
})();

// Run `fn` the first time carousel slide `index` is shown while on screen.
const onSlide = (index, el, fn) => {
  let shown = false;
  let visible = false;
  const tryRun = () => {
    if (shown || !visible || el.closest("[inert]")) return;
    shown = true;
    fn();
  };
  whenVisible(el, () => {
    visible = true;
    tryRun();
  }, 0.2);
  window.addEventListener("car:shown", (e) => e.detail === index && setTimeout(tryRun, 350));
};

/* ==========================================================================
   SQL: layered editor with SQL highlighting + Ren
   ========================================================================== */
(() => {
  const root = document.getElementById("sql-editor");
  if (!root) return;

  const input = root.querySelector(".code-input");
  const hl = root.querySelector(".code-hl");
  const gutter = root.querySelector(".gutter");

  const START = [
    "SELECT d.name AS department,",
    "       e.name,",
    "       e.salary",
    "FROM employees e",
    "JOIN departments d ON d.id = e.department_id",
    "WHERE e.salary > (",
    "    SELECT AVG(salary)",
    "    FROM employees",
    "    WHERE department_id = e.department_id",
    ")",
    "ORDER BY d.name, e.salary DESC;",
  ].join("\n");

  const SOLUTION = [
    "WITH dept_avg AS (",
    "  SELECT department_id,",
    "         AVG(salary) AS avg",
    "  FROM employees",
    "  GROUP BY department_id",
    ")",
    "SELECT d.name, e.name, e.salary",
    "FROM employees e",
    "JOIN dept_avg a USING (department_id)",
    "JOIN departments d",
    "  ON d.id = e.department_id",
    "WHERE e.salary > a.avg;",
  ].join("\n");

  const KEYWORDS =
    "select|from|where|join|inner|left|right|outer|full|on|as|and|or|not|in|exists|group|by|order|having|limit|offset|desc|asc|distinct|with|union|all|case|when|then|else|end|is|null|between|like|using";
  const TOKENS = new RegExp(
    [
      "(--[^\\n]*)", // 1 comment
      "('(?:[^'\\n]|'')*')", // 2 string
      `\\b(${KEYWORDS})\\b`, // 3 keyword
      "\\b(\\d+(?:\\.\\d+)?)\\b", // 4 number
      "\\b([A-Za-z_]\\w*)(?=\\()", // 5 function
    ].join("|"),
    "gi"
  );
  const CLASS = [null, "tk-c", "tk-s", "tk-k", "tk-n", "tk-f"];

  const highlight = (src) => {
    let out = "";
    let last = 0;
    for (const m of src.matchAll(TOKENS)) {
      out += escapeHtml(src.slice(last, m.index));
      const group = m.findIndex((g, i) => i > 0 && g !== undefined);
      out += `<span class="${CLASS[group]}">${escapeHtml(m[0])}</span>`;
      last = m.index + m[0].length;
    }
    return out + escapeHtml(src.slice(last));
  };

  const render = () => {
    const src = input.value;
    hl.innerHTML = highlight(src) + "\n ";
    gutter.textContent = Array.from({ length: src.split("\n").length }, (_, i) => i + 1).join("\n");
    input.style.height = `${hl.offsetHeight}px`;
  };

  const insert = (text) => {
    if (!document.execCommand("insertText", false, text)) {
      input.setRangeText(text, input.selectionStart, input.selectionEnd, "end");
      render();
    }
  };

  input.addEventListener("keydown", (e) => {
    if (e.key === "Tab" && !e.shiftKey) {
      e.preventDefault();
      insert("    ");
    } else if (e.key === "Enter" && !e.metaKey && !e.ctrlKey) {
      e.preventDefault();
      const before = input.value.slice(0, input.selectionStart);
      const line = before.slice(before.lastIndexOf("\n") + 1);
      let indent = line.match(/^\s*/)[0];
      if (/\(\s*$/.test(line)) indent += "    ";
      insert("\n" + indent);
    }
  });
  input.addEventListener("input", render);
  root.addEventListener("mousedown", (e) => {
    if (e.target !== input) {
      e.preventDefault();
      input.focus();
    }
  });

  input.value = START;
  render();
  document.fonts?.ready.then(render);

  const conv = (key) => ({
    hint: { level: 1, msgs: [
      ai(`<span class="msg-label">Hint</span><p>Does each employee need the company's average, or their own department's?</p>`),
      me("Their own department's."),
      ai(`<p>Right. So the average has to be worked out per department, not once for the whole table.</p>`),
    ] },
    nudge: { level: 2, msgs: [
      ai(`<span class="msg-label">Read your query · line 9</span><p>Line 9 ties the subquery to each employee's department. What would you get without it?</p>`),
      me("Everyone above the company average."),
      ai(`<p>Exactly, so your query is right. Next, think about how many times that subquery runs.</p>`),
    ] },
    explain: { level: 3, msgs: [
      ai(`<span class="msg-label">From an empty editor</span><ol><li><b>Average per department.</b> Group salaries by <code>department_id</code>.</li><li><b>Compare.</b> Keep employees above their own department's number.</li><li><b>Present.</b> Join departments for the name, then sort.</li></ol>`),
      me("Subquery or a join?"),
      ai(`<p>Both work. A CTE with <code>GROUP BY</code> works out each average once, which holds up better on big tables.</p>`),
    ] },
    solve: { level: 4, msgs: [
      ai(`<span class="msg-label">Full solution</span><p>This version works out each average once, then joins.</p><pre>${escapeHtml(SOLUTION)}</pre>`),
      me("Why is that faster?"),
      ai(`<p>The correlated subquery can run once per employee. The CTE runs once per department, then it's a plain join.</p>`),
    ] },
  }[key]);

  const rev = mountRev({
    msgs: document.getElementById("sql-rev-msgs"),
    form: document.getElementById("sql-rev-form"),
    levelEl: document.getElementById("sql-rev-level"),
    tabs: document.querySelectorAll("#sql-rev-tabs [data-level]"),
    conv,
    reply: REV_REPLY("your query and this exact schema"),
  });

  onSlide(1, document.getElementById("sql-demo"), () => {
    startTimer(document.querySelector("#sql-demo .timer[data-count]"));
    rev.show("nudge");
  });
})();

/* ==========================================================================
   System design: an editable board (select, move, rename, delete, draw
   boxes / diamonds / arrows / text / freehand, pan, zoom) + Ren
   ========================================================================== */
(() => {
  const canvas = document.getElementById("sd-canvas");
  if (!canvas) return;

  const board = document.getElementById("sd-board");
  const wires = document.getElementById("sd-wires");
  const selbar = document.getElementById("sd-selbar");
  const zoomLabel = document.getElementById("sd-zoom");
  const NS = "http://www.w3.org/2000/svg";
  const BOARD_W = 800;
  const BOARD_H = 480;

  const INITIAL = {
    nodes: [
      { id: "client", x: 36, y: 212, html: "Client" },
      { id: "lb", x: 196, y: 212, html: "Load balancer" },
      { id: "api", x: 388, y: 212, html: "API servers", cls: "accent" },
      { id: "cache", x: 584, y: 120, html: "Cache<small>Redis</small>", cls: "db" },
      { id: "db", x: 584, y: 304, html: "Database<small>PostgreSQL</small>", cls: "db" },
      { id: "note", x: 372, y: 336, html: "Hot links stay in cache. Most reads never touch the DB.", kind: "note" },
    ],
    links: [["client", "lb"], ["lb", "api"], ["api", "cache"], ["api", "db"]],
  };

  const nodes = new Map();
  let links = [];
  let seq = 0;
  let tool = "select";
  let selected = null;
  let editing = null;
  let zoom = 100;
  let panX = 0;
  let panY = 0;

  /* View ---------------------------------------------------------------- */

  const scale = () => Math.min(1, canvas.clientWidth / BOARD_W) * (zoom / 100);
  const applyView = () => {
    const k = scale();
    const x = (canvas.clientWidth - BOARD_W * k) / 2 + panX;
    const y = (canvas.clientHeight - BOARD_H * k) / 2 + 16 + panY;
    board.style.transform = `translate(${x}px, ${y}px) scale(${k})`;
    zoomLabel.textContent = `${zoom}%`;
    placeSelbar();
  };

  // Pointer position in board coordinates.
  const toBoard = (e) => {
    const r = board.getBoundingClientRect();
    const k = scale();
    return { x: (e.clientX - r.left) / k, y: (e.clientY - r.top) / k };
  };

  /* Arrows -------------------------------------------------------------- */

  const box = (el) => ({ x: el.offsetLeft, y: el.offsetTop, w: el.offsetWidth, h: el.offsetHeight });

  // Where a line from a box's centre toward (tx, ty) leaves the box.
  const edge = (b, tx, ty, pad = 5) => {
    const cx = b.x + b.w / 2, cy = b.y + b.h / 2;
    const dx = tx - cx, dy = ty - cy;
    const t = Math.min((b.w / 2 + pad) / Math.abs(dx || 1e-6), (b.h / 2 + pad) / Math.abs(dy || 1e-6));
    return [cx + dx * t, cy + dy * t];
  };

  const draw = () => {
    links = links.filter((l) => {
      if (nodes.has(l.a) && nodes.has(l.b)) return true;
      l.line.remove();
      return false;
    });
    links.forEach((l) => {
      const A = box(nodes.get(l.a)), B = box(nodes.get(l.b));
      const [x1, y1] = edge(A, B.x + B.w / 2, B.y + B.h / 2);
      const [x2, y2] = edge(B, A.x + A.w / 2, A.y + A.h / 2);
      l.line.setAttribute("x1", x1);
      l.line.setAttribute("y1", y1);
      l.line.setAttribute("x2", x2);
      l.line.setAttribute("y2", y2);
    });
  };

  const svgLine = () => {
    const line = document.createElementNS(NS, "line");
    line.setAttribute("marker-end", "url(#sd-arrow)");
    wires.appendChild(line);
    return line;
  };

  const link = (a, b) => {
    if (a === b || links.some((l) => l.a === a && l.b === b)) return;
    links.push({ a, b, line: svgLine() });
    draw();
  };

  /* Selection and editing ----------------------------------------------- */

  function placeSelbar() {
    if (!selected || editing) {
      selbar.hidden = true;
      return;
    }
    const r = selected.getBoundingClientRect();
    const c = canvas.getBoundingClientRect();
    selbar.style.left = `${r.left - c.left + r.width / 2}px`;
    selbar.style.top = `${r.top - c.top}px`;
    selbar.hidden = false;
  }

  const select = (el) => {
    selected?.classList.remove("selected");
    selected = el;
    selected?.classList.add("selected");
    placeSelbar();
  };

  const remove = (el) => {
    if (!el) return;
    nodes.delete(el.dataset.id);
    el.remove();
    if (selected === el) select(null);
    draw();
  };

  const edit = (el) => {
    if (!el) return;
    editing = el;
    el.contentEditable = "true";
    el.classList.add("editing");
    el.focus();
    const range = document.createRange();
    range.selectNodeContents(el);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    placeSelbar();
  };

  const commit = () => {
    if (!editing) return;
    const el = editing;
    editing = null;
    el.contentEditable = "false";
    el.classList.remove("editing");
    window.getSelection().removeAllRanges();
    if (!el.textContent.trim()) remove(el);
    else {
      draw();
      placeSelbar();
    }
  };

  /* Elements ------------------------------------------------------------ */

  const bind = (el) => {
    el.addEventListener("pointerdown", (e) => {
      if (tool !== "select" || editing === el) return; // other tools draw from here; editing places the caret
      e.stopPropagation();
      e.preventDefault();
      if (editing) editing.blur();
      select(el);
      el.setPointerCapture(e.pointerId);
      el.classList.add("dragging");
      const k = scale();
      const start = { x: e.clientX, y: e.clientY, left: el.offsetLeft, top: el.offsetTop };
      const move = (ev) => {
        el.style.left = `${Math.max(0, Math.min(BOARD_W - el.offsetWidth, start.left + (ev.clientX - start.x) / k))}px`;
        el.style.top = `${Math.max(0, Math.min(BOARD_H - el.offsetHeight, start.top + (ev.clientY - start.y) / k))}px`;
        draw();
        placeSelbar();
      };
      const up = () => {
        el.classList.remove("dragging");
        el.removeEventListener("pointermove", move);
        el.removeEventListener("pointerup", up);
        el.removeEventListener("pointercancel", up);
      };
      el.addEventListener("pointermove", move);
      el.addEventListener("pointerup", up);
      el.addEventListener("pointercancel", up);
    });
    el.addEventListener("dblclick", () => tool === "select" && edit(el));
    el.addEventListener("blur", commit);
    el.addEventListener("input", () => draw());
    el.addEventListener("keydown", (e) => {
      if ((e.key === "Enter" && !e.shiftKey) || e.key === "Escape") {
        e.preventDefault();
        el.blur();
      }
    });
  };

  const makeNode = ({ id, x, y, html, cls = "", kind = "box", w, h }) => {
    const el = document.createElement("div");
    el.className = kind === "note" ? "sd-note" : kind === "text" ? "sd-text" : `sd-node ${cls}`.trim();
    el.dataset.id = id || `n${++seq}`;
    el.style.left = `${x}px`;
    el.style.top = `${y}px`;
    if (w) el.style.width = `${w}px`;
    if (h) el.style.minHeight = `${h}px`;
    el.innerHTML = html;
    board.appendChild(el);
    nodes.set(el.dataset.id, el);
    bind(el);
    return el;
  };

  const nodeAt = (p) =>
    [...nodes.values()].reverse().find((el) => {
      const b = box(el);
      return p.x >= b.x && p.x <= b.x + b.w && p.y >= b.y && p.y <= b.y + b.h;
    });

  const build = () => {
    board.querySelectorAll(".sd-node, .sd-note, .sd-text, .sd-draft").forEach((el) => el.remove());
    wires.querySelectorAll(":scope > line, :scope > path").forEach((el) => el.remove()); // keep the arrowhead in <defs>
    nodes.clear();
    links = [];
    selected = null;
    editing = null;
    INITIAL.nodes.forEach(makeNode);
    INITIAL.links.forEach(([a, b]) => link(a, b));
    panX = panY = 0;
    zoom = 100;
    applyView();
    draw();
  };

  /* Tools --------------------------------------------------------------- */

  const toolButtons = canvas.querySelectorAll("[data-tool]");
  const setTool = (name) => {
    tool = name;
    canvas.dataset.tool = name;
    toolButtons.forEach((b) => b.classList.toggle("on", b.dataset.tool === name));
    if (name !== "select") select(null);
  };
  toolButtons.forEach((b) => b.addEventListener("click", () => setTool(b.dataset.tool)));

  canvas.addEventListener("pointerdown", (e) => {
    if (e.target.closest(".sd-tools, .sd-zoom, .sd-prompt, .sd-selbar")) return;
    if (editing) editing.blur();
    if (tool === "select") {
      select(null);
      return;
    }
    e.preventDefault();
    canvas.setPointerCapture(e.pointerId);
    const p = toBoard(e);
    let move = () => {};
    let up = () => {};

    if (tool === "hand") {
      const start = { x: e.clientX, y: e.clientY, panX, panY };
      board.style.transition = "none";
      canvas.classList.add("panning");
      move = (ev) => {
        panX = start.panX + ev.clientX - start.x;
        panY = start.panY + ev.clientY - start.y;
        applyView();
      };
      up = () => {
        board.style.transition = "";
        canvas.classList.remove("panning");
      };
    } else if (tool === "text") {
      const el = makeNode({ x: p.x, y: p.y - 14, html: "Text", kind: "text" });
      setTool("select");
      select(el);
      edit(el);
      return;
    } else if (tool === "rect" || tool === "diamond") {
      const draft = document.createElement("div");
      draft.className = `sd-draft ${tool === "diamond" ? "diamond" : ""}`;
      board.appendChild(draft);
      let q = p;
      const place = () => {
        draft.style.left = `${Math.min(p.x, q.x)}px`;
        draft.style.top = `${Math.min(p.y, q.y)}px`;
        draft.style.width = `${Math.abs(q.x - p.x)}px`;
        draft.style.height = `${Math.abs(q.y - p.y)}px`;
      };
      place();
      move = (ev) => {
        q = toBoard(ev);
        place();
      };
      up = () => {
        draft.remove();
        let w = Math.abs(q.x - p.x), h = Math.abs(q.y - p.y);
        let x = Math.min(p.x, q.x), y = Math.min(p.y, q.y);
        if (w < 24 || h < 24) { // a click: drop a default-sized shape
          w = tool === "diamond" ? 140 : 130;
          h = tool === "diamond" ? 76 : 56;
          x = p.x - w / 2;
          y = p.y - h / 2;
        }
        const el = makeNode({ x, y, w, h, html: tool === "diamond" ? "Decision" : "New box", cls: tool === "diamond" ? "diamond" : "" });
        setTool("select");
        select(el);
        edit(el);
      };
    } else if (tool === "arrow") {
      const line = svgLine();
      line.classList.add("sd-preview");
      line.setAttribute("x1", p.x);
      line.setAttribute("y1", p.y);
      line.setAttribute("x2", p.x);
      line.setAttribute("y2", p.y);
      let q = p;
      move = (ev) => {
        q = toBoard(ev);
        line.setAttribute("x2", q.x);
        line.setAttribute("y2", q.y);
      };
      up = () => {
        line.classList.remove("sd-preview");
        const from = nodeAt(p), to = nodeAt(q);
        if (from && to && from !== to) {
          line.remove();
          link(from.dataset.id, to.dataset.id); // attached: follows the boxes
        } else if (Math.hypot(q.x - p.x, q.y - p.y) < 12) {
          line.remove();
        }
        setTool("select");
      };
    } else if (tool === "pen") {
      const path = document.createElementNS(NS, "path");
      path.classList.add("sd-ink");
      wires.appendChild(path);
      let d = `M${p.x.toFixed(1)} ${p.y.toFixed(1)}`;
      path.setAttribute("d", d);
      move = (ev) => {
        const q = toBoard(ev);
        d += ` L${q.x.toFixed(1)} ${q.y.toFixed(1)}`;
        path.setAttribute("d", d);
      };
    }

    const onMove = (ev) => move(ev);
    const onUp = () => {
      up();
      canvas.removeEventListener("pointermove", onMove);
      canvas.removeEventListener("pointerup", onUp);
      canvas.removeEventListener("pointercancel", onUp);
    };
    canvas.addEventListener("pointermove", onMove);
    canvas.addEventListener("pointerup", onUp);
    canvas.addEventListener("pointercancel", onUp);
  });

  // Selection bar: edit / delete.
  selbar.addEventListener("click", (e) => {
    const b = e.target.closest("[data-sel]");
    if (!b) return;
    if (b.dataset.sel === "edit") edit(selected);
    else remove(selected);
  });

  // Keyboard: Delete removes, letters pick tools (only while this board is showing).
  const KEYS = { v: "select", h: "hand", r: "rect", d: "diamond", a: "arrow", t: "text", p: "pen" };
  document.addEventListener("keydown", (e) => {
    if (editing || canvas.closest("[inert]") || e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.target.closest?.("input, textarea, select, [contenteditable='true']")) return;
    const r = canvas.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) return;
    if ((e.key === "Delete" || e.key === "Backspace") && selected) {
      e.preventDefault();
      remove(selected);
    } else if (KEYS[e.key.toLowerCase()]) {
      setTool(KEYS[e.key.toLowerCase()]);
    }
  });

  // Zoom and reset.
  canvas.querySelectorAll("[data-sd-zoom]").forEach((b) =>
    b.addEventListener("click", () => {
      zoom = Math.max(60, Math.min(140, zoom + Number(b.dataset.sdZoom) * 10));
      applyView();
    })
  );
  document.getElementById("sd-reset").addEventListener("click", build);

  window.addEventListener("resize", () => {
    applyView();
    draw();
  });
  window.addEventListener("car:shown", () => {
    applyView();
    draw();
  });
  document.fonts?.ready.then(() => {
    applyView();
    draw();
  });
  setTool("select");
  build();

  const conv = (key) => ({
    hint: { level: 1, msgs: [
      ai(`<span class="msg-label">Hint</span><p>Start with the numbers. 100M links a month is about 40 writes a second. What about reads?</p>`),
      me("Ten times that, so around 400 a second."),
      ai(`<p>Right, so it's read-heavy. That tells you where the cache pays off.</p>`),
    ] },
    nudge: { level: 2, msgs: [
      ai(`<span class="msg-label">Looked at your board</span><p>You have a cache next to the API servers. What's the key, and what happens on a miss?</p>`),
      me("The key is the short code. On a miss, read Postgres and fill the cache."),
      ai(`<p>Good. Next: how do you generate short codes without collisions?</p>`),
    ] },
    explain: { level: 3, msgs: [
      ai(`<span class="msg-label">From a blank board</span><ol><li><b>Estimate load.</b> About 40 writes and 400 reads a second.</li><li><b>Write path.</b> The API stores code → URL in Postgres.</li><li><b>Read path.</b> Redis first; misses fall back to Postgres.</li><li><b>Short codes.</b> A counter encoded in base62, or random codes with a retry.</li></ol>`),
      me("Why base62?"),
      ai(`<p>Seven base62 characters give about 3.5 trillion codes, enough for decades at this rate.</p>`),
    ] },
    solve: { level: 4, msgs: [
      ai(`<span class="msg-label">Reference design</span><p>Your board is close. The missing piece is how short codes get made: an ID generator behind the API servers, handing out base62 codes.</p>`),
      me("What if the generator goes down?"),
      ai(`<p>Give each API server a block of IDs up front. It keeps working through a short outage.</p>`),
    ] },
  }[key]);

  const rev = mountRev({
    msgs: document.getElementById("sd-rev-msgs"),
    form: document.getElementById("sd-rev-form"),
    levelEl: document.getElementById("sd-rev-level"),
    tabs: document.querySelectorAll("#sd-rev-tabs [data-level]"),
    conv,
    reply: REV_REPLY("your board and this exact prompt"),
  });

  onSlide(2, document.getElementById("design-demo"), () => {
    startTimer(document.querySelector("#design-demo .timer[data-count]"));
    rev.show("nudge");
  });
})();

/* ==========================================================================
   Resume builder: chat with Ren on the left, live preview on the right
   ========================================================================== */
(() => {
  const root = document.getElementById("builder");
  if (!root) return;

  const paper = document.getElementById("bd-paper");
  const acme = paper.querySelector("[data-acme]");
  const src = document.getElementById("bd-src");
  const status = document.getElementById("bd-status");

  // The Acme internship arrives through the conversation.
  acme.classList.add("bd-pending");

  // LaTeX source for the LaTeX tab, in Jake's Resume macros.
  const texLines = (withAcme) => [
    "\\documentclass[letterpaper,11pt]{article}",
    "\\begin{document}",
    "",
    "\\begin{center}",
    "  \\textbf{\\Huge \\scshape Alex Morgan} \\\\",
    "  (555) 012-3456 $|$ alex@email.com $|$ github.com/alexm",
    "\\end{center}",
    "",
    "\\section{Education}",
    "  \\resumeSubheading",
    "    {University of Washington}{Seattle, WA}",
    "    {B.S. in Computer Science}{Sep 2022 -- May 2026}",
    "",
    "\\section{Experience}",
    ...(withAcme
      ? [
          ["  \\resumeSubheading", true],
          ["    {Software Engineering Intern}{May 2025 -- Aug 2025}", true],
          ["    {Acme}{Remote}", true],
          ["    \\resumeItem{Built the billing API in Go and PostgreSQL,", true],
          ["      serving 2M+ requests a day}", true],
          ["    \\resumeItem{Cut failed payments by 18\\%}", true],
        ]
      : []),
    "  \\resumeSubheading",
    "    {Backend Developer (Part-time)}{Jan 2024 -- Dec 2024}",
    "    {Campus Labs}{Seattle, WA}",
    "",
    "\\section{Projects}",
    "  \\resumeProjectHeading",
    "    {\\textbf{Distributed Rate Limiter} $|$ \\emph{Go, Redis}}{Mar 2025}",
    "",
    "\\section{Technical Skills}",
    "  \\textbf{Languages}{: Go, Python, TypeScript, Java, SQL}",
    "",
    "\\end{document}",
  ];

  const renderSource = (withAcme) => {
    src.innerHTML = texLines(withAcme)
      .map((l) => {
        const [text, isNew] = Array.isArray(l) ? l : [l, false];
        const html = escapeHtml(text)
          .replace(/(^|[^\\])(%.*)$/, '$1<span class="tk-c">$2</span>') // unescaped % starts a comment
          .replace(/(\\[A-Za-z]+)/g, '<span class="tk-k">$1</span>');
        return `<span class="ln${isNew ? " hl" : ""}">${html}</span>`;
      })
      .join("");
  };

  const revealAcme = () => {
    acme.classList.remove("bd-pending");
    acme.classList.add("bd-added");
    renderSource(true);
    status.textContent = "Saved";
    setTimeout(() => acme.classList.add("settled"), 2600);
  };

  const chat = createChat(document.getElementById("bd-chat"), document.getElementById("bd-form"), {
    reply: (q) => `<p>${{
      greeting: "Hi there. Tell me about your work and I'll turn it into bullet points.",
      question: "Good question. I'll answer it with your resume open.",
      statement: "Got it. I'll add that to your resume.",
    }[messageKind(q)]} <a href="signup.html">Get started</a> to keep building.</p>`,
  });

  const SCRIPT = [
    ai("<p>Hi Alex. What roles are you going for?</p>", "Ren"),
    me("Backend roles, new grad."),
    ai("<p>Jake's Resume suits that: one page and easy for ATS to read. I've added your education, projects and skills. Where did you intern last summer?</p>", "Ren"),
    me("Acme. I built their billing API in Go."),
    ai("<p>Nice. How much traffic did it handle, and what changed after it shipped?</p>", "Ren"),
    { ...me("About 2M requests a day. Failed payments dropped 18%."), then: () => (status.textContent = "Compiling…") },
    { ...ai("<p>Added your Acme internship to Experience, with both numbers.</p>", "Ren"), then: revealAcme },
  ];

  renderSource(false);
  whenVisible(root, () => chat.play(SCRIPT));

  // Chat / LaTeX tabs
  const panels = root.querySelectorAll(".bd-panel");
  root.querySelectorAll("#bd-tabs [data-panel]").forEach((tab) =>
    tab.addEventListener("click", () => panels.forEach((p) => (p.hidden = p.dataset.panel !== tab.dataset.panel)))
  );

  // Template switch
  const tpl = document.getElementById("bd-template");
  tpl.addEventListener("change", () => {
    paper.style.opacity = "0";
    setTimeout(() => {
      paper.classList.remove("tpl-jake", "tpl-awesome", "tpl-deedy");
      paper.classList.add(`tpl-${tpl.value}`);
      paper.style.opacity = "";
    }, 200);
  });

  // Zoom
  let zoom = 100;
  const zoomLabel = document.getElementById("bd-zoom");
  root.querySelectorAll("[data-zoom]").forEach((b) =>
    b.addEventListener("click", () => {
      zoom = Math.max(70, Math.min(140, zoom + Number(b.dataset.zoom) * 10));
      paper.style.zoom = zoom / 100;
      zoomLabel.textContent = `${zoom}%`;
    })
  );
})();

/* ==========================================================================
   Interview: the call before joining, with a short chat from Ren
   ========================================================================== */
(() => {
  const root = document.getElementById("meet");
  if (!root) return;

  const tileMe = document.getElementById("tile-me");

  const mic = document.getElementById("mt-mic");
  mic.addEventListener("click", () => {
    const off = mic.getAttribute("aria-pressed") !== "true";
    mic.setAttribute("aria-pressed", String(off));
    mic.setAttribute("aria-label", off ? "Unmute microphone" : "Mute microphone");
    tileMe.querySelector(".mt-muted").hidden = !off;
  });

  const cam = document.getElementById("mt-cam");
  cam.addEventListener("click", () => {
    const off = cam.getAttribute("aria-pressed") !== "true";
    cam.setAttribute("aria-pressed", String(off));
    cam.setAttribute("aria-label", off ? "Turn on camera" : "Turn off camera");
    tileMe.classList.toggle("cam-off", off);
  });

  const role = document.getElementById("mt-role");
  const crumb = document.getElementById("mt-crumb");
  role.addEventListener("change", () => (crumb.textContent = role.value));

  // Chat / Notes tabs
  const panels = root.querySelectorAll(".mt-side > [data-panel]");
  root.querySelectorAll("#mt-tabs [data-panel]").forEach((tab) =>
    tab.addEventListener("click", () => panels.forEach((p) => (p.hidden = p.dataset.panel !== tab.dataset.panel)))
  );

  const chat = createChat(document.getElementById("mt-msgs"), document.getElementById("mt-form"), {
    reply: (q) => `<p>${{
      greeting: "Hi! Looking forward to it.",
      question: "Good question. I'll answer that once we're in the call.",
      statement: "Noted. We can pick that up in the call.",
    }[messageKind(q)]} <a href="signup.html">Get started</a> to join.</p>`,
  });

  whenVisible(root, () =>
    chat.play([
      ai(`<p>Hi Alex, I'm Ren. I'll be your interviewer for the ${escapeHtml(role.value)} role today.</p>`, "Ren"),
      ai("<p>We'll start with a quick intro, then a coding round and a short system design discussion. About 45 minutes.</p>", "Ren"),
      me("Sounds good. Can I code in Python?"),
      ai("<p>Of course. Use whatever you're most comfortable with. Join when you're ready.</p>", "Ren"),
    ])
  );
})();
