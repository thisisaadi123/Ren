// Ren — the Solution tab in Ren's pane: a problem's full, written-out solution
// (GET /api/dsa/solution?id=), fetched only after the person asks to see it.
// It opens one part at a time: the question, an example thought through, each
// approach from slowest to best, then takeaways. Every approach has its idea,
// a step-by-step walkthrough, how to build it, the code in Python, Java, C++
// and C, a line-by-line breakdown, and its time and space.
//   renSolution.mount(el, { id, problem, highlight, lang, source })
//   source: optional () => Promise<{ ok, status, data }>, in place of the API
//   (the landing page reads a saved copy of one solution).
(() => {
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

  const LANGS = [
    { id: "python", label: "Python" },
    { id: "java", label: "Java" },
    { id: "cpp", label: "C++" },
    { id: "c", label: "C" },
  ];
  const KIND = { brute: "Brute force", better: "Better", best: "Best" };

  /* Text: paragraphs, "- " and "1. " lists, **bold**, `code` ---------------------- */

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
        const bullet = /^\s*- /;
        const number = /^\s*\d+\. /;
        if (bullet.test(lines[i]) || number.test(lines[i])) {
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
          while (i < lines.length && !bullet.test(lines[i]) && !number.test(lines[i])) para.push(lines[i++].trim());
          out.push(`<p>${inline(para.join(" "))}</p>`);
        }
      }
    }
    return out.join("");
  }

  function blocks(list = []) {
    return list
      .map((b) => {
        if (b.md !== undefined) return `<div class="sol-text">${markdown(b.md)}</div>`;
        if (b.panels) {
          const panels = window.renVisual ? b.panels.map(renVisual.panel).join("") : "";
          return `<figure class="sol-fig"><div class="sol-fig-stage">${panels}</div>${b.caption ? `<figcaption>${inline(b.caption)}</figcaption>` : ""}</figure>`;
        }
        if (b.table) {
          const head = b.table.head.map((h) => `<th scope="col">${inline(h)}</th>`).join("");
          const rows = b.table.rows.map((r) => `<tr>${r.map((c, i) => (i ? `<td>${inline(c)}</td>` : `<th scope="row">${inline(c)}</th>`)).join("")}</tr>`).join("");
          return `<div class="sol-table-wrap"><table class="sol-table"><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table></div>`;
        }
        return "";
      })
      .join("");
  }

  /* Mount ---------------------------------------------------------------------- */

  function mount(el, { id, problem, highlight, lang: editorLang, source }) {
    const key = `ren:sol:${id}`;
    let data = null;
    let loading = null;
    // The code follows the editor's language (renSolution's language() is called when it changes).
    let lang = editorLang || "python";
    if (!LANGS.some((l) => l.id === lang)) lang = "python";

    const quiet = (title, line, actions = "") => {
      el.innerHTML = `
        <div class="sol-gate">
          <h2>${esc(title)}</h2>
          ${line ? `<p>${esc(line)}</p>` : ""}
          ${actions}
        </div>`;
    };

    function gate() {
      quiet(
        "Reveal the full solution?",
        "Ren walks you through it step by step: the question, an example, every approach from brute force to best, with code in Python, Java, C++ and C, a line-by-line breakdown and the complexity of each.",
        `<div class="sol-gate-actions">
          <button type="button" class="btn btn-primary btn-sm" data-reveal>Reveal</button>
          <button type="button" class="btn btn-secondary btn-sm" data-not-yet>Not yet</button>
        </div>`
      );
    }

    async function load() {
      if (data) return data;
      const get = source || (() => renApi(`/api/dsa/solution?id=${encodeURIComponent(id)}`));
      loading = loading || get().catch(() => ({ ok: false, status: 0 }));
      const res = await loading;
      loading = null;
      if (res.ok) data = res.data;
      return res;
    }

    async function reveal(shown) {
      quiet("Loading the solution…", "");
      el.querySelector(".sol-gate").classList.add("is-loading");
      const res = await load();
      if (!data) {
        loading = null;
        return quiet(
          res.status === 404 ? "Not written yet" : "Couldn't load the solution",
          res.status === 404 ? "The full solution for this problem is still being written." : "Something went wrong. Give it another try.",
          res.status === 404 ? "" : `<div class="sol-gate-actions"><button type="button" class="btn btn-secondary btn-sm" data-reveal>Try again</button></div>`
        );
      }
      render(Math.max(1, shown || 1));
    }

    /* The parts, in order ------------------------------------------------------- */

    const parts = () => [
      { id: "question", name: "The question", html: () => section("question", "The question", blocks(data.question)) },
      { id: "think", name: "Think it through", html: () => section("think", "Think it through", blocks(data.think)) },
      ...data.approaches.map((a, i) => ({ id: `a${i + 1}`, name: a.title, html: () => approach(a, i) })),
      { id: "takeaways", name: "Takeaways", html: () => section("takeaways", "Takeaways", compare() + blocks(data.takeaways)) },
    ];

    const section = (sid, title, body) => `
      <section class="sol-part" id="sol-${esc(id)}-${sid}" data-part="${sid}">
        <h2 class="sol-h">${esc(title)}</h2>
        ${body}
      </section>`;

    function compare() {
      if (data.approaches.length < 2) return "";
      return blocks([
        {
          table: {
            head: ["Approach", "Time", "Space"],
            rows: data.approaches.map((a, i) => [`${i + 1}. ${a.title}`, a.time, a.space]),
          },
        },
      ]);
    }

    function approach(a, i) {
      const sub = [KIND[a.kind], `${a.time} time`, `${a.space} space`].filter(Boolean).join(" · ");
      return `
        <section class="sol-part sol-approach" id="sol-${esc(id)}-a${i + 1}" data-part="a${i + 1}">
          <h2 class="sol-h"><span class="sol-n">${i + 1}.</span> ${esc(a.title)}</h2>
          <p class="sol-sub">${esc(sub)}</p>
          ${blocks(a.idea)}
          ${a.walk ? `<h3 class="sol-label">Step by step</h3>${a.walk.title ? `<p class="walk-intro">${inline(a.walk.title)}</p>` : ""}<div class="sol-walk" data-sol-walk="${i}"></div>` : ""}
          <h3 class="sol-label">Build it</h3>
          <ol class="sol-build">${a.build.map((s) => `<li>${inline(s)}</li>`).join("")}</ol>
          <h3 class="sol-label">Code</h3>
          <div class="sol-code" data-code="${i}">${codeBlock(a)}</div>
          <h3 class="sol-label">Line by line</h3>
          <div class="sol-lines" data-lines="${i}">${lineRows(a)}</div>
          <h3 class="sol-label">Complexity</h3>
          <dl class="sol-cx"><div><dt>Time</dt><dd>${esc(a.time)}</dd></div><div><dt>Space</dt><dd>${esc(a.space)}</dd></div></dl>
          ${blocks(a.complexity)}
          ${a.limits ? `<h3 class="sol-label">Where it falls short</h3>${blocks(a.limits)}` : ""}
        </section>`;
    }

    /* Code in each language --------------------------------------------------------- */

    const tabs = () =>
      `<div class="sol-langs" role="tablist" aria-label="Language">${LANGS.map(
        (l) => `<button type="button" role="tab" class="case-btn" aria-selected="${l.id === lang}" data-sol-lang="${l.id}">${l.label}</button>`
      ).join("")}</div>`;

    // Class-based (design) problems have no C version.
    const missing = (a) =>
      `<p class="sol-missing">${esc(LANGS.find((l) => l.id === lang).label)} isn't available for this problem: it asks you to build a class, and C has no classes. Pick another language above.</p>`;

    function codeBlock(a) {
      if (!a.code[lang]) {
        return `
          <div class="sol-code-head">${tabs()}</div>
          ${missing(a)}`;
      }
      const src = (a.code[lang] || "").replace(/\n$/, "");
      const lines = src.split("\n");
      return `
        <div class="sol-code-head">
          ${tabs()}
          <button type="button" class="ghost-btn sol-copy" data-copy>Copy</button>
        </div>
        <div class="sol-pre-wrap"><pre class="sol-pre"><code>${lines
          .map((l, n) => `<span class="ln" aria-hidden="true">${n + 1}</span>${highlight(l, lang)}`)
          .join("\n")}</code></pre></div>`;
    }

    function lineRows(a) {
      if (!a.code[lang]) return missing(a);
      const src = (a.code[lang] || "").replace(/\n$/, "").split("\n");
      const rows = a.lines.filter((r) => r.at[lang]);
      return rows
        .map((r) => {
          const pieces = r.at[lang].map(([s, e]) =>
            src
              .slice(s - 1, e)
              .map((l, k) => `<span class="ln" aria-hidden="true">${s + k}</span>${highlight(l, lang)}`)
              .join("\n")
          );
          const note = r.notes && r.notes[lang] ? `<div class="sol-text sol-note">${markdown(r.notes[lang])}</div>` : "";
          return `
            <div class="sol-line">
              <pre class="sol-pre sol-snip"><code>${pieces.join('\n<span class="gap" aria-hidden="true">⋯</span>\n')}</code></pre>
              <div class="sol-line-text"><div class="sol-text">${markdown(r.text)}</div>${note}</div>
            </div>`;
        })
        .join("");
    }

    function setLang(next) {
      lang = next;
      el.querySelectorAll("[data-code]").forEach((box) => (box.innerHTML = codeBlock(data.approaches[Number(box.dataset.code)])));
      el.querySelectorAll("[data-lines]").forEach((box) => (box.innerHTML = lineRows(data.approaches[Number(box.dataset.lines)])));
    }

    /* Rendering, part by part ------------------------------------------------------- */

    let shown = 0;
    let picked = null; // the part chosen in the nav, until the reader scrolls by hand
    let markNow = null;

    function render(count) {
      const list = parts();
      shown = Math.min(count, list.length);
      store.set(key, shown);
      el.innerHTML = `
        <div class="sol-scroll">
          <nav class="sol-nav" aria-label="Solution parts"></nav>
          <div class="sol-body">
            <p class="sol-lead">${inline(data.summary)}</p>
            <div data-parts></div>
            <div class="sol-next" data-sol-next></div>
          </div>
        </div>`;
      const holder = el.querySelector("[data-parts]");
      list.slice(0, shown).forEach((p, i) => append(holder, p, i));
      paintNav();
      paintNext();
      watchScroll();
    }

    function append(holder, part) {
      holder.insertAdjacentHTML("beforeend", part.html());
      const sec = holder.lastElementChild;
      sec.querySelectorAll("[data-sol-walk]").forEach((w) => {
        const a = data.approaches[Number(w.dataset.solWalk)];
        if (window.renVisual && a.walk) renVisual.walkthrough(w, a.walk);
      });
      return sec;
    }

    function paintNav() {
      const nav = el.querySelector(".sol-nav");
      nav.innerHTML = parts()
        .map(
          (p, i) =>
            `<button type="button" class="case-btn" data-go="${p.id}"${i >= shown ? " disabled" : ""}>${esc(i >= 2 && i < parts().length - 1 ? `${i - 1}. ${p.name}` : p.name)}</button>`
        )
        .join("");
    }

    function paintNext() {
      const list = parts();
      const box = el.querySelector("[data-sol-next]");
      if (shown >= list.length) {
        box.innerHTML = "";
        return;
      }
      const next = list[shown];
      box.innerHTML = `
        <button type="button" class="btn btn-secondary btn-sm" data-more>Next: ${esc(next.name)}</button>
        <button type="button" class="ghost-btn" data-all>Show all</button>`;
    }

    function more(all) {
      const list = parts();
      const holder = el.querySelector("[data-parts]");
      const from = shown;
      const to = all ? list.length : shown + 1;
      let first;
      for (let i = from; i < to; i++) {
        const sec = append(holder, list[i]);
        first = first || sec;
      }
      shown = to;
      store.set(key, shown);
      paintNav();
      paintNext();
      if (first) {
        picked = first.dataset.part;
        scrollTo(first);
        if (markNow) markNow();
      }
    }

    function scrollTo(sec) {
      const box = el.querySelector(".sol-scroll");
      const nav = el.querySelector(".sol-nav");
      const top = sec.getBoundingClientRect().top - box.getBoundingClientRect().top + box.scrollTop - nav.offsetHeight - 8;
      const reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
      box.scrollTo({ top, behavior: reduce ? "auto" : "smooth" });
    }

    // The nav underlines the part being read.
    function watchScroll() {
      const box = el.querySelector(".sol-scroll");
      const nav = el.querySelector(".sol-nav");
      let raf = 0;
      const mark = () => {
        raf = 0;
        const line = box.getBoundingClientRect().top + nav.offsetHeight + 40;
        let current = null;
        el.querySelectorAll(".sol-part").forEach((sec) => {
          if (sec.getBoundingClientRect().top <= line) current = sec.dataset.part;
        });
        current = current || "question";
        // A short last part can't scroll up to the line; at the bottom it's the one being read.
        const parts = el.querySelectorAll(".sol-part");
        if (parts.length && box.scrollTop + box.clientHeight >= box.scrollHeight - 4) current = parts[parts.length - 1].dataset.part;
        if (picked) current = picked;
        nav.querySelectorAll("[data-go]").forEach((b) => {
          const on = b.dataset.go === current;
          b.setAttribute("aria-current", on ? "true" : "false");
          if (on && (b.offsetLeft < nav.scrollLeft || b.offsetLeft + b.offsetWidth > nav.scrollLeft + nav.clientWidth)) {
            nav.scrollLeft = b.offsetLeft - 16;
          }
        });
      };
      box.addEventListener("scroll", () => (raf = raf || requestAnimationFrame(mark)), { passive: true });
      // A click on the nav marks that part at once; the next user scroll returns to position-based marking.
      const release = () => {
        if (!picked) return;
        picked = null;
        mark();
      };
      box.addEventListener("wheel", release, { passive: true });
      box.addEventListener("touchmove", release, { passive: true });
      box.addEventListener("keydown", release);
      markNow = mark;
      mark();
    }

    /* Events -------------------------------------------------------------------------- */

    el.addEventListener("click", (e) => {
      const t = e.target;
      if (t.closest("[data-reveal]")) return reveal(store.get(key, 0));
      if (t.closest("[data-not-yet]")) return el.dispatchEvent(new CustomEvent("sol:close", { bubbles: true }));
      if (t.closest("[data-more]")) return more(false);
      if (t.closest("[data-all]")) return more(true);
      const go = t.closest("[data-go]");
      if (go && !go.disabled) {
        const sec = el.querySelector(`[data-part="${go.dataset.go}"]`);
        if (sec) {
          picked = go.dataset.go;
          scrollTo(sec);
          if (markNow) markNow();
        }
        return;
      }
      const pick = t.closest("[data-sol-lang]");
      if (pick && pick.dataset.solLang !== lang) {
        // Keep the tab that was clicked where it was on screen.
        const box = el.querySelector(".sol-scroll");
        const before = pick.getBoundingClientRect().top;
        const which = pick.closest("[data-code]").dataset.code;
        setLang(pick.dataset.solLang);
        const again = el.querySelector(`[data-code="${which}"] [data-sol-lang="${lang}"]`);
        if (again && box) box.scrollTop += again.getBoundingClientRect().top - before;
        return;
      }
      const copy = t.closest("[data-copy]");
      if (copy) {
        const a = data.approaches[Number(copy.closest("[data-code]").dataset.code)];
        const done = (ok) => {
          copy.textContent = ok ? "Copied" : "Couldn't copy";
          setTimeout(() => (copy.textContent = "Copy"), 1600);
        };
        if (navigator.clipboard) navigator.clipboard.writeText(a.code[lang]).then(() => done(true), () => done(false));
        else done(false);
      }
    });

    // Arrow keys move between language tabs.
    el.addEventListener("keydown", (e) => {
      const tab = e.target.closest("[data-sol-lang]");
      if (!tab || (e.key !== "ArrowRight" && e.key !== "ArrowLeft")) return;
      e.preventDefault();
      const i = LANGS.findIndex((l) => l.id === tab.dataset.solLang);
      const next = LANGS[(i + (e.key === "ArrowRight" ? 1 : LANGS.length - 1)) % LANGS.length].id;
      const which = tab.closest("[data-code]").dataset.code;
      setLang(next);
      el.querySelector(`[data-code="${which}"] [data-sol-lang="${next}"]`)?.focus();
    });

    /* Opening the tab ------------------------------------------------------------------- */

    let opened = false;
    return {
      // The editor switched language: show the code in that language too.
      language(next) {
        if (next !== lang && LANGS.some((l) => l.id === next)) setLang(next);
      },
      // Called each time the Solution tab is shown.
      open() {
        if (opened) return;
        opened = true;
        if (!problem.solution) return quiet("Not written yet", "The full solution for this problem is still being written.");
        const seen = store.get(key, 0);
        if (seen > 0) reveal(seen);
        else gate();
      },
    };
  }

  window.renSolution = { mount };
})();
