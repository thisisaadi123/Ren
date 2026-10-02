// Ren — problem visuals, drawn here from the problem's own data (no images).
//   renVisual.exampleFigure(problem, example)  an SVG figure for one example, or ""
//   renVisual.walkthrough(el, spec)            a step-by-step player for visual.walkthrough
//
// Trees come in as level-order arrays (null for gaps); lists as arrays, or
// { values, cycle_at }. A problem's visual.json may add hints and a walkthrough:
//   { mark: ["p", "q"], answer: "nodes", walkthrough: { title, steps: [...] } }
// Each walkthrough step is { text, call?, result?, panels: [...] }, and a panel is one of
//   { type: "tree",  label, tree, states: { index: state }, notes: { index: text } }
//   { type: "list",  label, values, states, pointers: { name: index }, links: [[from, to]], cycleAt }
//   { type: "row",   label, cells, states, pointers, slots }
//   { type: "ntree", label, nodes: [{ id, label, parent }], states: { id: state }, notes }
//   { type: "vars",  items: { name: value } }
// Tree states are keyed by the node's position in level order, counting real nodes only.
// States: active (being looked at), found (has reported), mark (named in the question),
// answer, dim (ruled out), new (just changed).
(() => {
  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  const R = 15; // node radius
  const DX = 36; // horizontal step between in-order neighbours
  const DY = 50; // vertical step between levels
  const PAD = 4;
  const MAX_NODES = 40;
  const MAX_DEPTH = 7;
  const cls = (base, state) => `${base}${state ? ` is-${state}` : ""}`;
  const small = (text) => (String(text).length > 3 ? ' class="small"' : "");

  /* Binary trees --------------------------------------------------------------- */

  // Level order -> nodes with x (in-order index) and depth.
  function layout(level) {
    if (!Array.isArray(level) || !level.length || level[0] === null) return { nodes: [] };
    const nodes = [{ val: level[0], left: -1, right: -1, depth: 0 }];
    const queue = [0];
    let qi = 0;
    let i = 1;
    while (i < level.length && qi < queue.length) {
      const p = queue[qi++];
      for (const side of ["left", "right"]) {
        if (i >= level.length) break;
        const v = level[i++];
        if (v === null) continue;
        nodes.push({ val: v, left: -1, right: -1, depth: nodes[p].depth + 1 });
        nodes[p][side] = nodes.length - 1;
        queue.push(nodes.length - 1);
      }
    }
    // In-order index gives each node its own column, so subtrees never overlap.
    let x = 0;
    const stack = [];
    let cur = 0;
    while (stack.length || cur !== -1) {
      while (cur !== -1) {
        stack.push(cur);
        cur = nodes[cur].left;
      }
      cur = stack.pop();
      nodes[cur].x = x++;
      cur = nodes[cur].right;
    }
    return { nodes };
  }

  const drawable = (t) => t.nodes.length <= MAX_NODES && Math.max(0, ...t.nodes.map((n) => n.depth)) < MAX_DEPTH;

  function edge(x1, y1, x2, y2, r1 = R, r2 = R) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const len = Math.hypot(dx, dy) || 1;
    const ux = dx / len;
    const uy = dy / len;
    return `<line class="vz-edge" x1="${(x1 + ux * r1).toFixed(1)}" y1="${(y1 + uy * r1).toFixed(1)}" x2="${(x2 - ux * r2).toFixed(1)}" y2="${(y2 - uy * r2).toFixed(1)}"/>`;
  }

  // Positioned nodes [{ x, y, label, state, note }] and edges [[a, b]] -> SVG.
  function graphSvg(pts, edges, label) {
    if (!pts.length) {
      return `<svg class="vz-tree" width="${2 * (R + PAD)}" height="${2 * (R + PAD)}" role="img" aria-label="${esc(label || "empty")}"></svg>`;
    }
    const noteW = pts.some((p) => p.note !== undefined && p.note !== "") ? 34 : 0;
    const w = Math.max(...pts.map((p) => p.x)) + R + PAD + noteW;
    const h = Math.max(...pts.map((p) => p.y)) + R + PAD + (noteW ? 10 : 0);
    const lines = edges.map(([a, b]) => edge(pts[a].x, pts[a].y, pts[b].x, pts[b].y)).join("");
    const nodes = pts
      .map(
        (p) => `<g class="${cls("vz-node", p.state)}">
          <circle cx="${p.x}" cy="${p.y}" r="${R}"/>
          <text${small(p.label)} x="${p.x}" y="${p.y}" dy="0.35em">${esc(p.label)}</text>
          ${p.note !== undefined && p.note !== "" ? `<text class="vz-note" x="${p.x + R + 3}" y="${p.y + R + 4}">${esc(p.note)}</text>` : ""}
        </g>`
      )
      .join("");
    return `<svg class="vz-tree" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(label)}">${lines}${nodes}</svg>`;
  }

  function treeSvg(t, states = {}, notes = {}, label = "") {
    const pts = t.nodes.map((n, i) => ({
      x: R + PAD + n.x * DX,
      y: R + PAD + n.depth * DY,
      label: String(n.val),
      state: states[i],
      note: notes[i],
    }));
    const edges = [];
    t.nodes.forEach((n, i) => [n.left, n.right].forEach((c) => c >= 0 && edges.push([i, c])));
    return graphSvg(pts, edges, label);
  }

  /* General trees (tries, parent arrays) ------------------------------------------ */

  function ntreeSvg(nodes, states = {}, notes = {}, label = "") {
    const kids = new Map(nodes.map((n) => [n.id, []]));
    let root = null;
    for (const n of nodes) {
      if (n.parent === null || n.parent === undefined || !kids.has(n.parent)) root = root ?? n.id;
      else kids.get(n.parent).push(n.id);
    }
    const pos = new Map();
    let leaf = 0;
    const place = (id, depth) => {
      const ch = kids.get(id);
      if (!ch.length) pos.set(id, { x: leaf++, depth });
      else {
        ch.forEach((c) => place(c, depth + 1));
        const xs = ch.map((c) => pos.get(c).x);
        pos.set(id, { x: (Math.min(...xs) + Math.max(...xs)) / 2, depth });
      }
    };
    if (root !== null) place(root, 0);
    const index = new Map(nodes.map((n, i) => [n.id, i]));
    const pts = nodes.map((n) => ({
      x: R + PAD + pos.get(n.id).x * DX,
      y: R + PAD + pos.get(n.id).depth * DY,
      label: n.label ?? String(n.id),
      state: states[n.id],
      note: notes[n.id],
    }));
    const edges = [];
    for (const n of nodes) if (n.parent !== null && n.parent !== undefined && index.has(n.parent)) edges.push([index.get(n.parent), index.get(n.id)]);
    return graphSvg(pts, edges, label);
  }

  /* Linked lists ---------------------------------------------------------------- */

  const LW = 40; // node box
  const LH = 32;
  const LG = 24; // gap for the arrow

  function listSvg(values, opts = {}) {
    const n = values.length;
    const states = opts.states || {};
    const pointers = opts.pointers || {};
    const links = opts.links || values.slice(1).map((_, i) => [i, i + 1]);
    const hasBelow = Object.keys(pointers).length > 0;
    const back = links.some(([a, b]) => b !== null && b <= a) || (opts.cycleAt !== undefined && opts.cycleAt !== null);
    const top = PAD + (links.some(([a, b]) => b !== null && b > a + 1) ? 22 : 0);
    const x = (i) => PAD + i * (LW + LG);
    const w = Math.max(LW + 2 * PAD, x(n - 1) + LW + PAD + 18);
    const h = top + LH + (back ? 24 : 0) + (hasBelow ? 22 : 0) + PAD;
    if (!n) {
      return `<svg class="vz-list" width="${LW + 2 * PAD}" height="${LH + 2 * PAD}" role="img" aria-label="empty list"><text class="vz-null" x="${PAD}" y="${PAD + LH / 2}" dy="0.35em">null</text></svg>`;
    }
    const arrows = [];
    const all = links.slice();
    if (opts.cycleAt !== undefined && opts.cycleAt !== null) all.push([n - 1, opts.cycleAt]);
    for (const [a, b] of all) {
      if (b === null || b === undefined) continue;
      const y = top + LH / 2;
      if (b === a + 1) {
        arrows.push(`<path class="vz-link" d="M${x(a) + LW + 2} ${y}H${x(b) - 4}"/><path class="vz-head" d="M${x(b) - 8} ${y - 4}L${x(b) - 3} ${y}L${x(b) - 8} ${y + 4}"/>`);
      } else if (b > a) {
        const x1 = x(a) + LW / 2;
        const x2 = x(b) + LW / 2;
        arrows.push(`<path class="vz-link" d="M${x1} ${top - 2}C${x1} ${top - 20} ${x2} ${top - 20} ${x2} ${top - 4}"/><path class="vz-head" d="M${x2 - 4} ${top - 9}L${x2} ${top - 3}L${x2 + 4} ${top - 9}"/>`);
      } else {
        const x1 = x(a) + LW / 2;
        const x2 = x(b) + LW / 2;
        const y0 = top + LH + 2;
        arrows.push(`<path class="vz-link" d="M${x1} ${y0}C${x1} ${y0 + 20} ${x2} ${y0 + 20} ${x2} ${y0 + 4}"/><path class="vz-head" d="M${x2 - 4} ${y0 + 9}L${x2} ${y0 + 3}L${x2 + 4} ${y0 + 9}"/>`);
      }
    }
    // The last node of a plain chain points at null.
    const tailsOut = new Set(all.map(([a, b]) => (b === null || b === undefined ? -1 : a)));
    const ends = opts.links ? [] : [n - 1].filter((i) => !tailsOut.has(i));
    const nulls = ends.map((i) => `<path class="vz-link" d="M${x(i) + LW + 2} ${top + LH / 2}h10"/><path class="vz-end" d="M${x(i) + LW + 12} ${top + LH / 2 - 6}v12"/>`);
    const labels = {};
    for (const [name, i] of Object.entries(pointers)) if (i !== null && i !== undefined && i >= 0 && i < n) (labels[i] = labels[i] || []).push(name);
    const boxes = values
      .map(
        (v, i) => `<g class="${cls("vz-box", states[i])}">
          <rect x="${x(i)}" y="${top}" width="${LW}" height="${LH}" rx="8"/>
          <text${small(v)} x="${x(i) + LW / 2}" y="${top + LH / 2}" dy="0.35em">${esc(v)}</text>
          ${labels[i] ? `<text class="vz-ptr" x="${x(i) + LW / 2}" y="${top + LH + (back ? 24 : 0) + 16}">${esc(labels[i].join(" · "))}</text>` : ""}
        </g>`
      )
      .join("");
    return `<svg class="vz-list" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(opts.label || "linked list")}">${arrows.join("")}${nulls.join("")}${boxes}</svg>`;
  }

  /* Rows of cells (arrays, stacks, queues, buffers) ------------------------------ */

  const CW = 44;
  const CH = 34;

  function rowSvg(cells, opts = {}) {
    const states = opts.states || {};
    const pointers = opts.pointers || {};
    const n = Math.max(cells.length, 1);
    const hasBelow = Object.keys(pointers).length > 0;
    const w = n * CW + 2 * PAD;
    const h = CH + (opts.slots ? 16 : 0) + (hasBelow ? 18 : 0) + 2 * PAD;
    const labels = {};
    for (const [name, i] of Object.entries(pointers)) if (i !== null && i !== undefined && i >= 0) (labels[i] = labels[i] || []).push(name);
    const out = [];
    for (let i = 0; i < n; i++) {
      const v = cells[i];
      const empty = v === null || v === undefined;
      if (!cells.length && !opts.slots) {
        out.push(`<text class="vz-null" x="${PAD}" y="${PAD + CH / 2}" dy="0.35em">empty</text>`);
        break;
      }
      const x = PAD + i * CW;
      out.push(`<g class="${cls(`vz-cell${empty ? " is-empty" : ""}`, states[i])}">
        <rect x="${x + 2}" y="${PAD}" width="${CW - 4}" height="${CH}" rx="7"/>
        <text${small(empty ? "" : v)} x="${x + CW / 2}" y="${PAD + CH / 2}" dy="0.35em">${empty ? "" : esc(v)}</text>
        ${opts.slots ? `<text class="vz-index" x="${x + CW / 2}" y="${PAD + CH + 13}">${i}</text>` : ""}
        ${labels[i] ? `<text class="vz-ptr" x="${x + CW / 2}" y="${PAD + CH + (opts.slots ? 29 : 15)}">${esc(labels[i].join(" · "))}</text>` : ""}
      </g>`);
    }
    return `<svg class="vz-cells" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(opts.label || "cells")}">${out.join("")}</svg>`;
  }

  /* Panels ------------------------------------------------------------------------ */

  const figure = (svg, caption) =>
    `<figure class="vz-fig">${svg}${caption ? `<figcaption>${esc(caption)}</figcaption>` : ""}</figure>`;

  function panel(p) {
    switch (p.type) {
      case "tree":
        return figure(treeSvg(layout(p.tree), p.states, p.notes, p.label || "tree"), p.label);
      case "ntree":
        return figure(ntreeSvg(p.nodes || [], p.states, p.notes, p.label || "tree"), p.label);
      case "list":
        return figure(listSvg(p.values || [], p), p.label);
      case "row":
        return figure(rowSvg(p.cells || [], p), p.label);
      case "vars":
        return `<dl class="vz-vars">${Object.entries(p.items || {})
          .map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${esc(typeof v === "string" ? v : JSON.stringify(v))}</dd></div>`)
          .join("")}</dl>`;
      default:
        return "";
    }
  }

  /* Example figures ------------------------------------------------------------ */

  const ARROW = `<svg class="vz-arrow" width="28" height="12" viewBox="0 0 28 12" aria-hidden="true"><path d="M1 6h24M20 1.5 25.5 6 20 10.5"/></svg>`;

  const listValues = (v) => (Array.isArray(v) ? { values: v } : v && Array.isArray(v.values) ? { values: v.values, cycleAt: v.cycle_at } : null);

  function exampleFigure(problem, ex) {
    if (!problem || !ex || problem.kind !== "function") return "";
    const hints = problem.visual || {};
    const states = {};
    const markValues = new Map();
    for (const name of hints.mark || []) {
      const v = ex.args[name];
      if (v !== undefined && v !== null) markValues.set(String(v), "mark");
    }
    if (hints.answer === "nodes" && ex.expected !== undefined && ex.expected !== null) {
      for (const v of [].concat(ex.expected)) markValues.set(String(v), "answer");
    }

    const parts = [];
    for (const p of problem.params) {
      const v = ex.args[p.name];
      if (p.type === "TreeNode") {
        const t = layout(v);
        if (!drawable(t)) return "";
        t.nodes.forEach((n, i) => markValues.has(String(n.val)) && (states[i] = markValues.get(String(n.val))));
        parts.push(figure(treeSvg(t, states, {}, `${p.name} as a tree`), t.nodes.length ? p.name : `${p.name} (empty)`));
      } else if (p.type === "ListNode") {
        const l = listValues(v);
        if (!l || l.values.length > 12) return "";
        parts.push(figure(listSvg(l.values, { cycleAt: l.cycleAt, label: p.name }), l.values.length ? p.name : `${p.name} (empty)`));
      } else if (p.type === "ListNode[]" && Array.isArray(v)) {
        if (v.length > 6 || v.some((l) => (l || []).length > 12)) return "";
        v.forEach((l, i) => parts.push(figure(listSvg(l || [], { label: `${p.name}[${i}]` }), `${p.name}[${i}]`)));
      }
    }
    const out = ex.expected;
    if (problem.returns === "TreeNode") {
      const t = layout(out);
      if (!drawable(t)) return "";
      parts.push(...(parts.length ? [ARROW] : []), figure(treeSvg(t, {}, {}, "the output tree"), t.nodes.length ? "output" : "output (empty)"));
    } else if (problem.returns === "ListNode") {
      const l = listValues(out);
      if (!l || l.values.length > 12) return parts.length ? `<div class="ex-figure">${parts.join("")}</div>` : "";
      parts.push(...(parts.length ? [ARROW] : []), figure(listSvg(l.values, { label: "output" }), l.values.length ? "output" : "output (empty)"));
    }
    return parts.length ? `<div class="ex-figure">${parts.join("")}</div>` : "";
  }

  /* Walkthroughs ---------------------------------------------------------------- */

  function walkthrough(el, spec) {
    if (!spec || !Array.isArray(spec.steps) || !spec.steps.length) return;
    const reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    el.innerHTML = `
      <div class="walk">
        <div class="walk-stage" data-stage></div>
        <p class="walk-text" data-text aria-live="polite"></p>
        <div class="walk-bar">
          <button type="button" class="ghost-btn" data-prev>Back</button>
          <button type="button" class="ghost-btn" data-play>Play</button>
          <button type="button" class="ghost-btn" data-next>Next</button>
          <span class="walk-count" data-count></span>
        </div>
      </div>`;
    const stage = el.querySelector("[data-stage]");
    const textEl = el.querySelector("[data-text]");
    const count = el.querySelector("[data-count]");
    const prev = el.querySelector("[data-prev]");
    const next = el.querySelector("[data-next]");
    const play = el.querySelector("[data-play]");
    const last = spec.steps.length - 1;
    let at = 0;
    let timer = null;

    // The stage keeps the height of its tallest step, so the controls never jump.
    let tallest = 0;

    function paint() {
      const step = spec.steps[at];
      stage.style.minHeight = "";
      stage.innerHTML = (step.panels || []).map(panel).join("");
      tallest = Math.max(tallest, stage.offsetHeight);
      stage.style.minHeight = `${tallest}px`;
      const call = step.call ? `<code>${esc(step.call)}</code>${step.result !== undefined ? ` → <code>${esc(step.result)}</code>` : ""}` : "";
      textEl.innerHTML = [call, esc(step.text || "")].filter(Boolean).join(" ");
      count.textContent = `${at + 1} / ${spec.steps.length}`;
      prev.disabled = at === 0;
      next.disabled = at === last;
    }

    function stop() {
      clearInterval(timer);
      timer = null;
      play.textContent = at === last ? "Replay" : "Play";
    }

    const go = (to) => {
      stop();
      at = Math.max(0, Math.min(last, to));
      paint();
      stop();
    };
    prev.addEventListener("click", () => go(at - 1));
    next.addEventListener("click", () => go(at + 1));
    play.addEventListener("click", () => {
      if (timer) return stop();
      if (at === last) {
        at = 0;
        paint();
      }
      play.textContent = "Pause";
      timer = setInterval(() => {
        if (at >= last) return stop();
        at++;
        paint();
        if (at === last) stop();
      }, reduce ? 2600 : 1800);
    });

    paint();
    stop();
  }

  window.renVisual = { exampleFigure, walkthrough, panel };
})();
