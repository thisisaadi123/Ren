// Ren — problem visuals, drawn here from the problem's own data (no images).
//   renVisual.exampleFigure(problem, example)  an SVG figure for one example, or ""
//   renVisual.walkthrough(el, spec)            a step-by-step player for visual.walkthrough
// Trees come in as level-order arrays (null for gaps). Optional hints live in a
// problem's visual.json: { mark: ["p", "q"], answer: "nodes", walkthrough: {...} }.
(() => {
  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  const R = 15; // node radius
  const DX = 36; // horizontal step between in-order neighbours
  const DY = 50; // vertical step between levels
  const PAD = 4;
  const MAX_NODES = 40;
  const MAX_DEPTH = 7;

  /* Trees ------------------------------------------------------------------- */

  // Level order -> nodes with x (in-order index) and depth, plus parent links.
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

  // states: Map value -> "mark" | "answer" | "active" | "found" | "dim"
  function treeSvg(t, states = new Map(), label = "") {
    if (!t.nodes.length) {
      return `<svg class="vz-tree" width="${2 * R + 2 * PAD}" height="${2 * R + 2 * PAD}" role="img" aria-label="${esc(label || "empty tree")}"></svg>`;
    }
    const w = (Math.max(...t.nodes.map((n) => n.x)) + 1) * DX - DX + 2 * (R + PAD);
    const h = Math.max(...t.nodes.map((n) => n.depth)) * DY + 2 * (R + PAD);
    const cx = (n) => R + PAD + n.x * DX;
    const cy = (n) => R + PAD + n.depth * DY;
    const edges = [];
    for (const n of t.nodes) {
      for (const c of [n.left, n.right]) {
        if (c < 0) continue;
        const k = t.nodes[c];
        // Stop the line at the circles' edges.
        const dx = cx(k) - cx(n);
        const dy = cy(k) - cy(n);
        const len = Math.hypot(dx, dy);
        const ux = dx / len;
        const uy = dy / len;
        edges.push(
          `<line class="vz-edge" x1="${(cx(n) + ux * R).toFixed(1)}" y1="${(cy(n) + uy * R).toFixed(1)}" x2="${(cx(k) - ux * R).toFixed(1)}" y2="${(cy(k) - uy * R).toFixed(1)}"/>`
        );
      }
    }
    const nodes = t.nodes.map((n, i) => {
      const s = states.get(String(n.val));
      const text = String(n.val);
      const small = text.length > 3 ? " small" : "";
      return `<g class="vz-node${s ? ` is-${s}` : ""}" data-i="${i}" data-val="${esc(text)}">
        <circle cx="${cx(n)}" cy="${cy(n)}" r="${R}"/>
        <text class="${small.trim()}" x="${cx(n)}" y="${cy(n)}" dy="0.35em">${esc(text)}</text>
      </g>`;
    });
    return `<svg class="vz-tree" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(label)}">${edges.join("")}${nodes.join("")}</svg>`;
  }

  /* Example figures ------------------------------------------------------------ */

  const ARROW = `<svg class="vz-arrow" width="28" height="12" viewBox="0 0 28 12" aria-hidden="true"><path d="M1 6h24M20 1.5 25.5 6 20 10.5"/></svg>`;

  function exampleFigure(problem, ex) {
    if (!problem || !ex || problem.kind !== "function") return "";
    const hints = problem.visual || {};
    const treeParams = problem.params.filter((p) => p.type === "TreeNode");
    if (!treeParams.length) return "";

    const states = new Map();
    for (const name of hints.mark || []) {
      const v = ex.args[name];
      if (v !== undefined && v !== null) states.set(String(v), "mark");
    }
    if (hints.answer === "nodes" && ex.expected !== undefined && ex.expected !== null) {
      for (const v of [].concat(ex.expected)) states.set(String(v), "answer");
    }

    const parts = [];
    for (const p of treeParams) {
      const t = layout(ex.args[p.name]);
      if (!drawable(t)) return "";
      parts.push(figure(treeSvg(t, states, `${p.name} as a tree`), t.nodes.length ? p.name : `${p.name} (empty)`));
    }
    if (problem.returns === "TreeNode") {
      const t = layout(ex.expected);
      if (!drawable(t)) return "";
      parts.push(ARROW, figure(treeSvg(t, new Map(), "the output tree"), t.nodes.length ? "output" : "output (empty)"));
    }
    return `<div class="ex-figure">${parts.join("")}</div>`;
  }

  const figure = (svg, caption) => `<figure class="vz-fig">${svg}<figcaption>${esc(caption)}</figcaption></figure>`;

  /* Walkthroughs ---------------------------------------------------------------- */

  // spec.kind "tree":  { tree: [...], steps: [{ text, nodes: { "5": "active", ... } }] }
  // spec.kind "cells": { size, steps: [{ call, result, text, cells: [...], active: [i], pointers: { front: i, rear: i } }] }
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
    let at = 0;
    let timer = null;

    if (spec.kind === "tree") {
      stage.innerHTML = treeSvg(layout(spec.tree), new Map(), "walkthrough tree");
    } else if (spec.kind === "cells") {
      stage.innerHTML = cellsSvg(spec.size);
    }

    function paint() {
      const step = spec.steps[at];
      if (spec.kind === "tree") {
        const map = step.nodes || {};
        stage.querySelectorAll(".vz-node").forEach((g) => {
          g.setAttribute("class", `vz-node${map[g.dataset.val] ? ` is-${map[g.dataset.val]}` : ""}`);
        });
      } else if (spec.kind === "cells") {
        paintCells(stage, spec.size, step);
      }
      const call = step.call ? `<code>${esc(step.call)}</code>${step.result !== undefined ? ` → <code>${esc(step.result)}</code>` : ""}` : "";
      textEl.innerHTML = [call, esc(step.text || "")].filter(Boolean).join(" ");
      count.textContent = `${at + 1} / ${spec.steps.length}`;
      prev.disabled = at === 0;
      next.disabled = at === spec.steps.length - 1;
    }

    function stop() {
      clearInterval(timer);
      timer = null;
      play.textContent = at === spec.steps.length - 1 ? "Replay" : "Play";
    }

    prev.addEventListener("click", () => {
      stop();
      at = Math.max(0, at - 1);
      paint();
      stop();
    });
    next.addEventListener("click", () => {
      stop();
      at = Math.min(spec.steps.length - 1, at + 1);
      paint();
      stop();
    });
    play.addEventListener("click", () => {
      if (timer) return stop();
      if (at === spec.steps.length - 1) {
        at = 0;
        paint();
      }
      play.textContent = "Pause";
      timer = setInterval(() => {
        if (at >= spec.steps.length - 1) return stop();
        at++;
        paint();
        if (at === spec.steps.length - 1) stop();
      }, reduce ? 2600 : 1800);
    });

    paint();
    stop();
  }

  /* Cells: a row of slots with pointer labels underneath (ring buffers, stacks, arrays). */

  const CW = 52;
  const CH = 40;

  function cellsSvg(size) {
    const w = size * CW + 2 * PAD;
    const h = CH + 44 + 2 * PAD;
    const cells = [];
    for (let i = 0; i < size; i++) {
      const x = PAD + i * CW;
      cells.push(`<g class="vz-cell" data-i="${i}">
        <rect x="${x + 2}" y="${PAD}" width="${CW - 4}" height="${CH}" rx="8"/>
        <text x="${x + CW / 2}" y="${PAD + CH / 2}" dy="0.35em"></text>
        <text class="vz-index" x="${x + CW / 2}" y="${PAD + CH + 14}">${i}</text>
        <text class="vz-ptr" x="${x + CW / 2}" y="${PAD + CH + 32}"></text>
      </g>`);
    }
    return `<svg class="vz-cells" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="buffer slots">${cells.join("")}</svg>`;
  }

  function paintCells(stage, size, step) {
    const active = new Set(step.active || []);
    const labels = Array.from({ length: size }, () => []);
    for (const [name, i] of Object.entries(step.pointers || {})) {
      if (i !== null && i !== undefined && labels[i]) labels[i].push(name);
    }
    stage.querySelectorAll(".vz-cell").forEach((g) => {
      const i = Number(g.dataset.i);
      const v = (step.cells || [])[i];
      const empty = v === null || v === undefined;
      g.setAttribute("class", `vz-cell${empty ? " is-empty" : ""}${active.has(i) ? " is-active" : ""}`);
      const [value, , ptr] = g.querySelectorAll("text");
      value.textContent = empty ? "" : String(v);
      ptr.textContent = labels[i].join(" · ");
    });
  }

  window.renVisual = { exampleFigure, walkthrough };
})();
