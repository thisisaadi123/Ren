// Ren — a pattern lesson (learn.html?id=<pattern>): the theory and practice to
// read before solving a pattern's problems. GET /api/dsa/lesson?id= gives the
// lesson's sections (written ahead of time by tools/lessons), the pattern's
// problems and the lessons before and after it. The contents rail follows the
// reader; code comes in Python, Java, C++ and C, one choice for the whole page.
(() => {
  const main = document.getElementById("learn");
  const body = main.querySelector("[data-body]");
  const toc = main.querySelector("[data-toc]");
  const PROBLEM_PAGE = "problem.html";

  const LANGS = [
    { id: "python", label: "Python" },
    { id: "java", label: "Java" },
    { id: "cpp", label: "C++" },
    { id: "c", label: "C" },
  ];
  const DIFF = { easy: "Easy", medium: "Medium", hard: "Hard" };

  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
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
  const plural = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`;

  // The page's language: the last one picked here, else the editor's.
  let lang = store.get("ren:learn:lang") || store.get("ren:lang") || "python";
  if (!LANGS.some((l) => l.id === lang)) lang = "python";

  /* Text: ### headings, > quotes, "- " and "1. " lists, **bold**, *italic*, `code` ---- */

  function inline(text) {
    return text
      .split(/(`[^`]*`)/)
      .map((part) =>
        part.startsWith("`") && part.endsWith("`") && part.length > 1
          ? `<code>${esc(part.slice(1, -1))}</code>`
          : esc(part)
              .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
              .replace(/(^|[^\w*])\*(?!\s)(.+?)\*(?!\w)/g, "$1<i>$2</i>")
      )
      .join("");
  }

  function markdown(md) {
    const out = [];
    for (const block of md.split(/\n\s*\n/)) {
      const lines = block.split("\n").filter((l) => l.trim());
      let i = 0;
      while (i < lines.length) {
        const bullet = /^\s*- /;
        const number = /^\s*\d+\. /;
        if (/^###\s/.test(lines[i])) {
          out.push(`<h3 class="learn-h3">${inline(lines[i++].replace(/^###\s+/, ""))}</h3>`);
        } else if (/^>\s?/.test(lines[i])) {
          const quote = [];
          while (i < lines.length && /^>\s?/.test(lines[i])) quote.push(lines[i++].replace(/^>\s?/, "").trim());
          out.push(`<blockquote>${inline(quote.join(" "))}</blockquote>`);
        } else if (bullet.test(lines[i]) || number.test(lines[i])) {
          const kind = bullet.test(lines[i]) ? bullet : number;
          const items = [];
          while (i < lines.length && (kind.test(lines[i]) || (/^\s{2,}\S/.test(lines[i]) && !bullet.test(lines[i]) && !number.test(lines[i])))) {
            if (kind.test(lines[i])) items.push(lines[i].replace(kind, ""));
            else items[items.length - 1] += ` ${lines[i].trim()}`;
            i++;
          }
          const tag = kind === bullet ? "ul" : "ol";
          out.push(`<${tag}>${items.map((it) => `<li>${inline(it)}</li>`).join("")}</${tag}>`);
        } else {
          const para = [];
          while (i < lines.length && !bullet.test(lines[i]) && !number.test(lines[i]) && !/^(###\s|>)/.test(lines[i])) para.push(lines[i++].trim());
          out.push(`<p>${inline(para.join(" "))}</p>`);
        }
      }
    }
    return out.join("");
  }

  /* Blocks -------------------------------------------------------------------- */

  let codeBlocks = []; // every code block on the page, by index
  let walks = []; // walkthrough specs, by index

  function block(b) {
    if (b.md !== undefined) return `<div class="learn-text">${markdown(b.md)}</div>`;
    if (b.key !== undefined) return `<div class="learn-key">${markdown(b.key)}</div>`;
    if (b.panels) {
      const panels = window.renVisual ? b.panels.map(renVisual.panel).join("") : "";
      return `<figure class="learn-fig"><div class="learn-fig-stage">${panels}</div>${b.caption ? `<figcaption>${inline(b.caption)}</figcaption>` : ""}</figure>`;
    }
    if (b.table) {
      const head = b.table.head.map((h) => `<th scope="col">${inline(h)}</th>`).join("");
      const rows = b.table.rows.map((r) => `<tr>${r.map((c, i) => (i ? `<td>${inline(c)}</td>` : `<th scope="row">${inline(c)}</th>`)).join("")}</tr>`).join("");
      return `<div class="learn-table-wrap"><table class="learn-table"><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table></div>`;
    }
    if (b.walk) {
      walks.push(b.walk);
      return `${b.walk.title ? `<p class="walk-intro">${inline(b.walk.title)}</p>` : ""}<div class="learn-walk" data-walk="${walks.length - 1}"></div>`;
    }
    if (b.quiz) {
      return `<div class="learn-quiz">${b.quiz
        .map(
          (x, i) => `
          <details class="learn-q">
            <summary><span class="learn-q-n">${i + 1}</span><span class="learn-q-text">${inline(x.q)}</span><span class="learn-q-show" aria-hidden="true"></span></summary>
            <div class="learn-text learn-a">${markdown(x.a)}</div>
          </details>`
        )
        .join("")}</div>`;
    }
    if (b.code) {
      codeBlocks.push(b);
      const n = codeBlocks.length - 1;
      return `
        <div class="learn-code-block">
          <h3 class="learn-code-title">${inline(b.title)}</h3>
          <div class="learn-code" data-code="${n}">${codeHTML(b)}</div>
          <div class="learn-run">
            <div class="learn-run-row"><span>Runs</span><code>${esc(b.run.call)}</code></div>
            <div class="learn-run-row"><span>Prints</span><pre>${esc(b.run.output)}</pre></div>
          </div>
          <details class="learn-lines-box">
            <summary>Line by line</summary>
            <div class="learn-lines" data-lines="${n}">${linesHTML(b)}</div>
          </details>
        </div>`;
    }
    return "";
  }

  const tabs = () =>
    `<div class="learn-langs" role="tablist" aria-label="Language">${LANGS.map(
      (l) => `<button type="button" role="tab" class="learn-lang" aria-selected="${l.id === lang}" data-lang="${l.id}">${l.label}</button>`
    ).join("")}</div>`;

  const numbered = (lines, from = 1) =>
    lines.map((l, k) => `<span class="ln" aria-hidden="true">${from + k}</span>${renCode.as(l, lang)}`).join("\n");

  function codeHTML(b) {
    const src = b.code[lang].replace(/\n$/, "");
    return `
      <div class="learn-code-head">
        ${tabs()}
        <button type="button" class="ghost-btn learn-copy" data-copy>Copy</button>
      </div>
      <div class="learn-pre-wrap"><pre class="learn-pre"><code>${numbered(src.split("\n"))}</code></pre></div>`;
  }

  function linesHTML(b) {
    const src = b.code[lang].replace(/\n$/, "").split("\n");
    return b.lines
      .filter((r) => r.at[lang])
      .map((r) => {
        const pieces = r.at[lang].map(([s, e]) => numbered(src.slice(s - 1, e), s));
        const note = r.notes && r.notes[lang] ? `<div class="learn-text learn-note">${markdown(r.notes[lang])}</div>` : "";
        return `
          <div class="learn-line">
            <pre class="learn-pre learn-snip"><code>${pieces.join('\n<span class="gap" aria-hidden="true">⋯</span>\n')}</code></pre>
            <div class="learn-line-text"><div class="learn-text">${markdown(r.text)}</div>${note}</div>
          </div>`;
      })
      .join("");
  }

  function setLang(next) {
    lang = next;
    store.set("ren:learn:lang", lang);
    body.querySelectorAll("[data-code]").forEach((box) => (box.innerHTML = codeHTML(codeBlocks[Number(box.dataset.code)])));
    body.querySelectorAll("[data-lines]").forEach((box) => (box.innerHTML = linesHTML(codeBlocks[Number(box.dataset.lines)])));
  }

  /* The page -------------------------------------------------------------------- */

  let data;
  const sectionId = (id) => `s-${id}`;

  function practiceHTML() {
    const rows = data.problems.map(
      (x) => `
        <li>
          <a class="learn-prob" href="${PROBLEM_PAGE}?id=${encodeURIComponent(x.id)}">
            <span class="learn-prob-title">${esc(x.title)}</span>
            <span class="learn-prob-diff ${esc(x.difficulty)}">${DIFF[x.difficulty] || esc(x.difficulty)}</span>
            <span class="learn-prob-type">${esc(x.type)}</span>
            <svg class="learn-prob-go" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
          </a>
        </li>`
    );
    const left = Math.max(0, data.pattern.count - data.problems.length);
    if (left) rows.push(`<li class="learn-prob soon">${plural(left, "more problem")} coming soon</li>`);
    return `
      <section class="learn-sec" id="${sectionId("practice")}" data-sec="practice">
        <h2 class="learn-h2">Practice</h2>
        <div class="learn-text"><p>Now put it to work. The problems below all use ${esc(data.pattern.name.toLowerCase())}, easiest first. Try each one before opening its solution.</p></div>
        <ul class="learn-probs">${rows.join("")}</ul>
      </section>`;
  }

  function nearHTML() {
    const link = (x, dir) =>
      x
        ? `<a class="learn-near ${dir}" href="learn.html?id=${encodeURIComponent(x.id)}">
             <span>${dir === "prev" ? "Previous lesson" : "Next lesson"}</span>
             <b>${esc(x.name)}</b>
           </a>`
        : "<span></span>";
    if (!data.prev && !data.next) return "";
    return `<nav class="learn-nears" aria-label="More lessons">${link(data.prev, "prev")}${link(data.next, "next")}</nav>`;
  }

  function render() {
    document.title = `${data.pattern.name} — Ren`;
    main.querySelector("[data-title]").textContent = data.pattern.name;
    main.querySelector("[data-summary]").innerHTML = inline(data.summary);
    const topic = main.querySelector("[data-topic]");
    topic.textContent = data.topic.name;
    topic.href = `dsa.html?q=${encodeURIComponent(data.topic.name)}`;
    main.querySelector("[data-meta]").textContent = `${data.minutes} min read · ${plural(data.problems.length, "problem")} to practise`;

    codeBlocks = [];
    walks = [];
    const sections = data.sections
      .map(
        (s) => `
        <section class="learn-sec" id="${sectionId(s.id)}" data-sec="${esc(s.id)}">
          <h2 class="learn-h2">${esc(s.title)}</h2>
          ${s.blocks.map(block).join("")}
        </section>`
      )
      .join("");
    body.innerHTML = `
      <details class="learn-toc-m">
        <summary>Contents</summary>
        <nav aria-label="Contents" data-toc-m></nav>
      </details>
      ${sections}
      ${practiceHTML()}
      ${nearHTML()}`;
    body.querySelectorAll("[data-walk]").forEach((el) => window.renVisual && renVisual.walkthrough(el, walks[Number(el.dataset.walk)]));

    const items = [...data.sections.map((s) => ({ id: s.id, title: s.title })), { id: "practice", title: "Practice" }];
    const links = items
      .map(
        (s, i) =>
          `<a href="#${sectionId(s.id)}" data-go="${esc(s.id)}"><span class="learn-toc-n" aria-hidden="true">${String(i + 1).padStart(2, "0")}</span>${esc(s.title)}</a>`
      )
      .join("");
    toc.innerHTML = links;
    body.querySelector("[data-toc-m]").innerHTML = links;
    watchScroll();
  }

  /* Following the reader ---------------------------------------------------------- */

  function watchScroll() {
    const secs = [...body.querySelectorAll(".learn-sec")];
    let raf = 0;
    const mark = () => {
      raf = 0;
      const line = 140;
      let current = secs[0] && secs[0].dataset.sec;
      for (const s of secs) if (s.getBoundingClientRect().top <= line) current = s.dataset.sec;
      if (innerHeight + scrollY >= document.documentElement.scrollHeight - 4) current = secs[secs.length - 1].dataset.sec;
      toc.querySelectorAll("[data-go]").forEach((a) => a.setAttribute("aria-current", a.dataset.go === current ? "true" : "false"));
      // Reaching the practice list counts as having read the lesson.
      if (current === "practice") store.set(`ren:learned:${data.id}`, true);
    };
    addEventListener("scroll", () => (raf = raf || requestAnimationFrame(mark)), { passive: true });
    addEventListener("resize", mark);
    mark();
  }

  /* Events -------------------------------------------------------------------------- */

  body.addEventListener("click", (e) => {
    const t = e.target;
    const pick = t.closest("[data-lang]");
    if (pick && pick.dataset.lang !== lang) {
      // Keep the clicked tab where it was on screen while every block switches.
      const before = pick.getBoundingClientRect().top;
      const which = pick.closest("[data-code]").dataset.code;
      setLang(pick.dataset.lang);
      const again = body.querySelector(`[data-code="${which}"] [data-lang="${lang}"]`);
      if (again) scrollBy(0, again.getBoundingClientRect().top - before);
      return;
    }
    const copy = t.closest("[data-copy]");
    if (copy) {
      const b = codeBlocks[Number(copy.closest("[data-code]").dataset.code)];
      const done = (ok) => {
        copy.textContent = ok ? "Copied" : "Couldn't copy";
        setTimeout(() => (copy.textContent = "Copy"), 1600);
      };
      if (navigator.clipboard) navigator.clipboard.writeText(b.code[lang]).then(() => done(true), () => done(false));
      else done(false);
      return;
    }
    // The phone contents list closes once a section is picked.
    if (t.closest("[data-toc-m] a")) body.querySelector(".learn-toc-m").open = false;
  });

  // Arrow keys move between language tabs.
  body.addEventListener("keydown", (e) => {
    const tab = e.target.closest("[data-lang]");
    if (!tab || (e.key !== "ArrowRight" && e.key !== "ArrowLeft")) return;
    e.preventDefault();
    const i = LANGS.findIndex((l) => l.id === tab.dataset.lang);
    const next = LANGS[(i + (e.key === "ArrowRight" ? 1 : LANGS.length - 1)) % LANGS.length].id;
    const which = tab.closest("[data-code]").dataset.code;
    setLang(next);
    body.querySelector(`[data-code="${which}"] [data-lang="${next}"]`)?.focus();
  });

  /* Load ------------------------------------------------------------------------------ */

  function failed(status) {
    main.classList.add("is-state");
    main.innerHTML =
      status === 404
        ? `<div class="state">
            <h1>This lesson isn't written yet</h1>
            <p>Lessons are being added pattern by pattern. The problems are ready on the sheet.</p>
            <a class="btn btn-secondary" href="dsa.html">Back to DSA</a>
          </div>`
        : `<div class="state">
            <h1>Couldn't load the lesson</h1>
            <p>Something went wrong on our side. Give it another try.</p>
            <button type="button" class="btn btn-secondary" data-retry>Try again</button>
          </div>`;
    main.querySelector("[data-retry]")?.addEventListener("click", () => location.reload());
  }

  const id = new URLSearchParams(location.search).get("id") || "";
  const req = renApi(`/api/dsa/lesson?id=${encodeURIComponent(id)}`).catch(() => ({ ok: false, status: 0 }));

  Promise.all([renSession(main), req, renLoader.page]).then(([, res]) => {
    if (res.ok) {
      data = res.data;
      render();
    } else {
      failed(res.status);
    }
    renLoader.done().then(() => {
      renReveal(main);
      // A link straight to a section (learn.html?id=…#s-template) lands on it once drawn.
      const target = location.hash && document.getElementById(location.hash.slice(1));
      if (target) target.scrollIntoView();
    });
  });
})();
