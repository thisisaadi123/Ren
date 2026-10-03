// Ren — a practice sheet: every topic, pattern and problem, in study order.
// The DSA sheet (dsa.html, /api/dsa) and the SQL sheet (sql.html, /api/sql)
// both use it; the page's <main> says which API and problem page to use. Problems that exist are links; the rest of each pattern's
// planned count stays in the sheet, greyed out and locked. Search, the track
// tabs and the filters narrow it, every count on the page follows them, and
// they're kept in the URL so a filtered sheet can be shared.
(() => {
  const main = document.getElementById("dsa");
  const tools = main.querySelector(".dsa-tools");
  const sheet = main.querySelector("[data-sheet]");
  const search = main.querySelector("[data-q]");
  const searchClear = main.querySelector("[data-q-clear]");
  const selects = [...main.querySelectorAll("[data-filter]")];
  const tabs = [...main.querySelectorAll("[data-track]")];
  const thumb = main.querySelector(".seg-thumb");
  const count = main.querySelector("[data-count]");
  const clearBtn = main.querySelector("[data-clear]");
  const expandBtn = main.querySelector("[data-expand]");

  const API = main.dataset.api || "/api/dsa";
  const PROBLEM_PAGE = main.dataset.problemPage || "problem.html";
  let TYPES = ["Array", "String", "Matrix", "Number", "Linked list", "Tree", "Design"];
  const DIFF = { easy: "Easy", medium: "Medium", hard: "Hard" };
  const KEYS = ["track", "q", "difficulty", "type", "status"];

  const ICON = {
    chev: '<svg class="topic-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
    go: '<svg class="prob-go" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>',
    lock: '<svg class="lock-i" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="7" width="10" height="7" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2"/></svg>',
  };

  /* State ------------------------------------------------------------------ */

  const params = new URLSearchParams(location.search);
  const state = Object.fromEntries(KEYS.map((k) => [k, params.get(k) || ""]));
  const filtering = () => Boolean(state.q.trim() || state.difficulty || state.type || state.status);

  // Which topics are open. The sheet opens folded; within the tab it keeps
  // what you opened, so coming back from a problem lands where you were.
  // Filtering opens every match for the moment without touching this.
  const OPEN_KEY = main.dataset.openKey || "ren:dsa:open";
  let open = new Set();
  try {
    localStorage.removeItem(OPEN_KEY); // was kept across visits before
    const saved = JSON.parse(sessionStorage.getItem(OPEN_KEY));
    if (Array.isArray(saved)) open = new Set(saved);
  } catch {}
  const saveOpen = () => {
    try {
      sessionStorage.setItem(OPEN_KEY, JSON.stringify([...open]));
    } catch {}
  };

  let data;
  const order = new Map(); // topic id -> its place in the study order

  /* Text helpers ------------------------------------------------------------ */

  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const has = (text, q) => text.toLowerCase().includes(q);

  // Escaped text with the search match marked.
  const hl = (text, q) => {
    const i = q ? text.toLowerCase().indexOf(q) : -1;
    if (i < 0) return esc(text);
    return `${esc(text.slice(0, i))}<mark>${esc(text.slice(i, i + q.length))}</mark>${esc(text.slice(i + q.length))}`;
  };

  const plural = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`;
  const sum = (list, fn) => list.reduce((n, x) => n + fn(x), 0);
  const ready = (p) => Math.min(p.problems.length, p.count);
  const missing = (p) => Math.max(0, p.count - p.problems.length);

  /* What to show ------------------------------------------------------------ */

  // The sheet narrowed by the current state: topics > patterns > problems.
  // Each pattern carries `shown` (its matching problems) and `soon` (how
  // many locked slots it still shows); each topic carries its patterns in
  // `shown` and their totals.
  function view(track = state.track) {
    const q = state.q.trim().toLowerCase();
    const byProblem = state.difficulty || state.type;

    return data.topics
      .filter((t) => !track || t.track === track)
      .map((t) => {
        const topicHit = q && has(t.name, q);
        const patterns = t.patterns
          .map((p) => {
            const patternHit = topicHit || (q && has(p.name, q));
            let problems = p.problems.filter(
              (x) =>
                (!state.difficulty || x.difficulty === state.difficulty) &&
                (!state.type || x.type === state.type) &&
                (!q || patternHit || has(x.title, q))
            );
            // Locked slots have no difficulty or type yet, so those filters
            // hide them; a search shows them only under a matching pattern.
            let soon = byProblem || (q && !patternHit) ? 0 : missing(p);
            if (state.status === "ready") soon = 0;
            if (state.status === "locked") problems = [];
            return problems.length || soon ? { ...p, shown: problems, soon } : null;
          })
          .filter(Boolean);
        if (!patterns.length) return null;
        return {
          ...t,
          shown: patterns,
          nShown: sum(patterns, (p) => p.shown.length),
          nSoon: sum(patterns, (p) => p.soon),
        };
      })
      .filter(Boolean);
  }

  // What a count means under the Status filter: ready problems, or the
  // locked ones when only those are showing.
  const tally = (topics) =>
    state.status === "locked" ? sum(topics, (t) => t.nSoon) : sum(topics, (t) => t.nShown);

  /* Render ------------------------------------------------------------------- */

  // Unfiltered, a topic reads as planned: "8 patterns · 33 problems", or how
  // much of it is ready. Filtered, every number is what matches.
  function topicMeta(t) {
    const locked = !t.patterns.some(ready);
    const lock = locked ? ICON.lock : "";
    if (!filtering()) {
      const done = sum(t.patterns, ready);
      const total = sum(t.patterns, (p) => p.count);
      const patterns = plural(t.patterns.length, "pattern");
      if (!done) return `${lock}${patterns} · Coming soon`;
      if (done < total) return `${patterns} · ${done} of ${total} ready`;
      return `${patterns} · ${plural(total, "problem")}`;
    }
    const parts = [plural(t.shown.length, "pattern")];
    if (t.nShown) parts.push(plural(t.nShown, "problem"));
    if (t.nSoon) parts.push(`${t.nSoon} coming soon`);
    return `${t.nShown ? "" : ICON.lock}${parts.join(" · ")}`;
  }

  function patternCount(p) {
    if (!filtering()) {
      const done = ready(p);
      return done && done < p.count ? `${done} of ${p.count} ready` : plural(p.count, "problem");
    }
    if (!p.shown.length) return `${p.soon} coming soon`;
    return plural(p.shown.length, "problem") + (p.soon ? ` · ${p.soon} coming soon` : "");
  }

  function patternHTML(p, q) {
    const locked = !ready(p);
    const rows = p.shown.map(
      (x) => `
        <li>
          <a class="prob" href="${PROBLEM_PAGE}?id=${encodeURIComponent(x.id)}" data-id="${esc(x.id)}">
            <span class="prob-title">${hl(x.title, q)}</span>
            <span class="prob-meta">
              <span class="prob-diff ${esc(x.difficulty)}">${DIFF[x.difficulty] || esc(x.difficulty)}</span>
              <span class="prob-type">${esc(x.type)}</span>
            </span>
            ${ICON.go}
          </a>
        </li>`
    );
    if (p.soon) {
      const text = locked ? "Coming soon" : `${p.soon} more coming soon`;
      rows.push(`<li class="prob soon">${ICON.lock}<span>${text}</span></li>`);
    }

    return `
      <div class="pattern${locked ? " locked" : ""}">
        <div class="pattern-head">
          <div>
            <h4>${hl(p.name, q)}</h4>
            <p>${esc(p.about)}</p>
          </div>
          <span class="pattern-count">${patternCount(p)}</span>
        </div>
        <ul class="probs">${rows.join("")}</ul>
      </div>`;
  }

  function topicHTML(t, q, isOpen) {
    const locked = !t.patterns.some(ready);
    const id = `topic-${esc(t.id)}`;
    const num = String(order.get(t.id)).padStart(2, "0");
    return `
      <div class="topic${locked ? " locked" : ""}${isOpen ? " open" : ""}" data-topic="${esc(t.id)}">
        <h3>
          <button type="button" class="topic-btn" aria-expanded="${isOpen}" aria-controls="${id}">
            <span class="topic-num" aria-hidden="true">${num}</span>
            <span class="topic-text">
              <span class="topic-name">${hl(t.name, q)}</span>
              <span class="topic-meta">${topicMeta(t)}</span>
            </span>
            ${ICON.chev}
          </button>
        </h3>
        <div class="topic-panel" id="${id}"${isOpen ? "" : " inert"}>
          <div class="topic-clip">
            <div class="topic-body">${t.shown.map((p) => patternHTML(p, q)).join("")}</div>
          </div>
        </div>
      </div>`;
  }

  function renderTabs() {
    tabs.forEach((tab) => {
      const n = tally(view(tab.dataset.track));
      tab.querySelector(".tab-n").textContent = n;
    });
    placeThumb();
  }

  function placeThumb() {
    const active = tabs.find((t) => t.getAttribute("aria-selected") === "true") || tabs[0];
    thumb.style.width = `${active.offsetWidth}px`;
    thumb.style.transform = `translateX(${active.offsetLeft}px)`;
  }

  function renderCount(topics) {
    const shown = sum(topics, (t) => t.nShown);
    const soon = sum(topics, (t) => t.nSoon);
    const b = (n) => `<b>${n}</b>`;
    let text;
    if (!filtering()) text = `${b(shown)} of ${shown + soon} problems ready`;
    else if (!shown) text = soon ? `${b(soon)} ${soon === 1 ? "problem" : "problems"} coming soon` : "";
    else {
      const patterns = sum(topics, (t) => t.shown.length);
      text = `${b(shown)} ${shown === 1 ? "problem" : "problems"} in ${plural(patterns, "pattern")}` +
        (soon ? `, ${soon} more coming soon` : "");
    }
    count.innerHTML = text;
  }

  function render() {
    const q = state.q.trim().toLowerCase();
    const topics = view();
    const all = filtering();

    renderTabs();
    renderCount(topics);
    clearBtn.hidden = !all;
    expandBtn.hidden = !topics.length;
    searchClear.hidden = !search.value;

    if (!topics.length) {
      sheet.innerHTML = `
        <div class="sheet-empty">
          <h2>No problems match.</h2>
          <p>Try another search, or clear the filters.</p>
          <button type="button" class="btn btn-secondary" data-clear>Clear filters</button>
        </div>`;
      return;
    }

    sheet.innerHTML = data.tracks
      .map((track) => {
        const list = topics.filter((t) => t.track === track.id);
        if (!list.length) return "";
        const n = tally(list);
        const meta = all
          ? `${plural(list.length, "topic")} · ${plural(n, "problem")}`
          : plural(list.length, "topic");
        return `
          <section class="sheet-track" aria-labelledby="track-${esc(track.id)}">
            <div class="sheet-track-head">
              <h2 id="track-${esc(track.id)}">${esc(track.name)}</h2>
              <span>${meta}</span>
            </div>
            <div class="sheet-card">
              ${list.map((t) => topicHTML(t, q, all || open.has(t.id))).join("")}
            </div>
          </section>`;
      })
      .join("");
    syncExpand();
  }

  function syncExpand() {
    const btns = [...sheet.querySelectorAll(".topic-btn")];
    const allOpen = btns.length && btns.every((b) => b.getAttribute("aria-expanded") === "true");
    expandBtn.textContent = allOpen ? "Collapse all" : "Expand all";
  }

  function setOpen(btn, on) {
    const topic = btn.closest(".topic");
    btn.setAttribute("aria-expanded", String(on));
    topic.classList.toggle("open", on);
    document.getElementById(btn.getAttribute("aria-controls")).inert = !on;
    // While filtering, opening and closing is just for the moment.
    if (filtering()) return;
    on ? open.add(topic.dataset.topic) : open.delete(topic.dataset.topic);
    saveOpen();
  }

  /* State <-> controls <-> URL ----------------------------------------------- */

  function syncControls() {
    search.value = state.q;
    selects.forEach((s) => {
      s.value = state[s.dataset.filter];
      // A value the list doesn't have (an old link) counts as no filter.
      if (s.value !== state[s.dataset.filter]) state[s.dataset.filter] = "";
      s.classList.toggle("set", Boolean(s.value));
    });
    if (!tabs.some((t) => t.dataset.track === state.track)) state.track = "";
    tabs.forEach((t) => t.setAttribute("aria-selected", String(t.dataset.track === state.track)));
  }

  function syncUrl() {
    const p = new URLSearchParams();
    KEYS.forEach((k) => state[k] && p.set(k, state[k]));
    const qs = p.toString();
    history.replaceState(null, "", qs ? `?${qs}` : location.pathname);
  }

  const update = () => {
    syncUrl();
    render();
  };

  function clear() {
    Object.assign(state, { q: "", difficulty: "", type: "", status: "" });
    syncControls();
    update();
  }

  /* Events -------------------------------------------------------------------- */

  let typing;
  search.addEventListener("input", () => {
    searchClear.hidden = !search.value;
    clearTimeout(typing);
    typing = setTimeout(() => {
      state.q = search.value;
      update();
    }, 120);
  });

  const clearSearch = () => {
    clearTimeout(typing);
    search.value = "";
    state.q = "";
    update();
  };

  search.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && search.value) {
      e.preventDefault();
      clearSearch();
    }
  });

  searchClear.addEventListener("click", () => {
    clearSearch();
    search.focus();
  });

  // "/" jumps to the search from anywhere that isn't a text field.
  document.addEventListener("keydown", (e) => {
    if (e.key !== "/" || e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.target.closest("input, textarea, select, [contenteditable]")) return;
    e.preventDefault();
    search.focus();
  });

  selects.forEach((s) =>
    s.addEventListener("change", () => {
      state[s.dataset.filter] = s.value;
      s.classList.toggle("set", Boolean(s.value));
      update();
    })
  );

  // app.js moves the tab thumb; this narrows the sheet.
  tabs.forEach((t) =>
    t.addEventListener("click", () => {
      if (state.track === t.dataset.track || !data) return;
      state.track = t.dataset.track;
      update();
    })
  );
  addEventListener("resize", placeThumb);

  // A shorter placeholder where the full one would be cut off.
  const narrow = matchMedia("(max-width: 420px)");
  const placeholder = () =>
    (search.placeholder = narrow.matches ? "Search problems" : "Search problems, patterns or topics");
  placeholder();
  narrow.addEventListener("change", placeholder);

  expandBtn.addEventListener("click", () => {
    const on = expandBtn.textContent === "Expand all";
    sheet.querySelectorAll(".topic-btn").forEach((b) => setOpen(b, on));
    syncExpand();
  });

  main.addEventListener("click", (e) => {
    if (e.target.closest("[data-clear]")) return clear();

    const btn = e.target.closest(".topic-btn");
    if (btn) {
      setOpen(btn, btn.getAttribute("aria-expanded") !== "true");
      syncExpand();
      return;
    }

  });

  // The tools get their own ground once they stick under the nav.
  const NAV_H = 64;
  const onScroll = () => {
    const stuck = getComputedStyle(tools).position === "sticky" && tools.getBoundingClientRect().top <= NAV_H + 0.5;
    tools.classList.toggle("stuck", stuck);
  };
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", onScroll);

  /* Load ---------------------------------------------------------------------- */

  function failed() {
    main.classList.add("is-state");
    main.innerHTML = `
      <div class="state">
        <h1>Couldn't load the problems</h1>
        <p>Something went wrong on our side. Give it another try.</p>
        <button type="button" class="btn btn-secondary" data-retry>Try again</button>
      </div>`;
    main.querySelector("[data-retry]").addEventListener("click", () => location.reload());
  }

  // No server at all is renSession's to show, so a failed request only
  // counts once the session is in.
  const sheetReq = renApi(API).catch(() => ({ ok: false }));

  Promise.all([renSession(main), sheetReq, renLoader.page]).then(([, res]) => {
    if (res.ok) {
      data = res.data;
      data.topics.forEach((t, i) => order.set(t.id, i + 1));
      if (Array.isArray(data.types)) TYPES = data.types;
      const types = new Set(data.topics.flatMap((t) => t.patterns.flatMap((p) => p.problems.map((x) => x.type))));
      const typeSelect = selects.find((s) => s.dataset.filter === "type");
      TYPES.filter((t) => types.has(t)).forEach((t) => typeSelect.add(new Option(t, t)));
      syncControls();
      render();
      onScroll();
    } else {
      failed();
    }
    renLoader.done().then(() => {
      renReveal(main);
      placeThumb();
    });
  });
})();
