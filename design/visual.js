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
//   { type: "grid",  label, cells: [[...]], states: { "r,c": state } }
//   { type: "bars",  label, values, labels, states, pointers, height, max, min }  (max/min fix the scale across steps)
//   { type: "ntree", label, nodes: [{ id, label, parent }], states: { id: state }, notes }
//   { type: "vars",  label, items: { name: value } }
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

  // Nodes are circles like tree nodes, joined by thin arrows. A link to the
  // previous node is a straight arrow pointing back; a loop or a longer jump is
  // a soft arc (back links below, forward skips above).
  const LS = 62; // centre-to-centre spacing

  function chevron(x, y, dir) {
    // An open arrowhead pointing in direction dir (radians) with its tip at (x, y).
    const a = 0.5;
    const len = 5.5;
    const p1 = [x - len * Math.cos(dir - a), y - len * Math.sin(dir - a)];
    const p2 = [x - len * Math.cos(dir + a), y - len * Math.sin(dir + a)];
    return `<path class="vz-head" d="M${p1[0].toFixed(1)} ${p1[1].toFixed(1)}L${x.toFixed(1)} ${y.toFixed(1)}L${p2[0].toFixed(1)} ${p2[1].toFixed(1)}"/>`;
  }

  function listSvg(values, opts = {}) {
    const n = values.length;
    if (!n) {
      return `<svg class="vz-list" width="40" height="${2 * (R + PAD)}" role="img" aria-label="empty list"><text class="vz-null" x="${PAD}" y="${R + PAD}" dy="0.35em">null</text></svg>`;
    }
    const states = opts.states || {};
    const pointers = opts.pointers || {};
    const links = (opts.links || values.slice(1).map((_, i) => [i, i + 1])).slice();
    if (opts.cycleAt !== undefined && opts.cycleAt !== null) links.push([n - 1, opts.cycleAt]);
    const randoms = (opts.randoms || []).filter(([, b]) => b !== null && b !== undefined);
    const far = (a, b) => b !== null && b !== undefined && Math.abs(b - a) > 1;
    const above = links.some(([a, b]) => far(a, b) && b > a) || randoms.some(([a, b]) => b >= a);
    const below = links.some(([a, b]) => far(a, b) && b < a) || randoms.some(([a, b]) => b < a);
    const labels = {};
    for (const [name, i] of Object.entries(pointers)) if (i !== null && i !== undefined && i >= 0 && i < n) (labels[i] = labels[i] || []).push(name);
    const rows = Math.max(0, ...Object.values(labels).map((l) => l.length));
    const cy = PAD + R + (above ? 22 : 0);
    const cx = (i) => PAD + R + i * LS;
    const arcDepth = 26;
    const labelTop = cy + R + (below ? arcDepth + 4 : 0) + 15;
    const w = cx(n - 1) + R + PAD;
    const h = (rows ? labelTop + (rows - 1) * 13 + 6 : cy + R + (below ? arcDepth + 6 : 0)) + PAD;

    const parts = [];
    for (const [a, b] of links) {
      if (b === null || b === undefined) continue;
      if (Math.abs(b - a) === 1) {
        const dir = b > a ? 1 : -1;
        const x1 = cx(a) + dir * (R + 3);
        const x2 = cx(b) - dir * (R + 3);
        parts.push(`<path class="vz-link" d="M${x1} ${cy}H${x2}"/>`, chevron(x2, cy, dir > 0 ? 0 : Math.PI));
      } else {
        // An arc from the bottom (or top) of a to the bottom (or top) of b.
        const up = b > a;
        const sy = up ? -1 : 1;
        const x1 = cx(a);
        const x2 = cx(b);
        const y0 = cy + sy * (R + 2);
        const yc = cy + sy * (R + arcDepth);
        parts.push(`<path class="vz-link" d="M${x1} ${y0}C${x1} ${yc} ${x2} ${yc} ${x2} ${y0 + sy * 2}"/>`, chevron(x2, y0 + sy * 1, up ? Math.PI / 2 : -Math.PI / 2));
      }
    }
    // Random pointers: dashed arcs, forward (and self) above, backward below.
    for (const [a, b] of randoms) {
      if (a === b) {
        const x = cx(a);
        parts.push(`<path class="vz-rand" d="M${x - 6} ${cy - R}C${x - 14} ${cy - R - 20} ${x + 14} ${cy - R - 20} ${x + 6} ${cy - R - 1}"/>`, chevron(x + 6, cy - R - 1, Math.PI / 2.4).replace("vz-head", "vz-rand-head"));
        continue;
      }
      const up = b > a;
      const sy = up ? -1 : 1;
      const x1 = cx(a);
      const x2 = cx(b);
      const y0 = cy + sy * (R + 2);
      const yc = cy + sy * (R + arcDepth + (Math.abs(b - a) > 2 ? 4 : 0));
      parts.push(`<path class="vz-rand" d="M${x1} ${y0}C${x1} ${yc} ${x2} ${yc} ${x2} ${y0 + sy * 2}"/>`, chevron(x2, y0 + sy * 1, up ? Math.PI / 2 : -Math.PI / 2).replace("vz-head", "vz-rand-head"));
    }
    values.forEach((v, i) => {
      parts.push(`<g class="${cls("vz-node", states[i])}">
        <circle cx="${cx(i)}" cy="${cy}" r="${R}"/>
        <text${small(v)} x="${cx(i)}" y="${cy}" dy="0.35em">${esc(v)}</text>
      </g>`);
      (labels[i] || []).forEach((name, k) => parts.push(`<text class="vz-tag" x="${cx(i)}" y="${labelTop + k * 13}">${esc(name)}</text>`));
    });
    return `<svg class="vz-list" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(opts.label || "linked list")}">${parts.join("")}</svg>`;
  }

  /* Rows of cells (arrays, stacks, queues, buffers) ------------------------------ */

  const CELL_W = 44;
  const CH = 34;

  function rowSvg(cells, opts = {}) {
    const states = opts.states || {};
    const pointers = opts.pointers || {};
    const n = Math.max(cells.length, 1);
    const hasBelow = Object.keys(pointers).length > 0;
    // Widen the cells when a value is too long to fit the standard width.
    const longest = cells.reduce((m, v) => Math.max(m, v === null || v === undefined ? 0 : String(v).length), 0);
    const CW = longest > 5 ? 7 * longest + 16 : CELL_W;
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

  /* Grids (matrices, boards) ------------------------------------------------------ */

  function gridSvg(rows, opts = {}) {
    const states = opts.states || {};
    const m = rows.length;
    const n = m ? Math.max(...rows.map((r) => r.length)) : 0;
    const longest = rows.reduce((mx, r) => r.reduce((a, v) => Math.max(a, v === null || v === undefined ? 0 : String(v).length), mx), 0);
    const CW = longest > 5 ? 7 * longest + 16 : CELL_W;
    const w = n * CW + 2 * PAD;
    const h = m * CH + 2 * PAD;
    const out = [];
    rows.forEach((row, r) =>
      row.forEach((v, c) => {
        const x = PAD + c * CW;
        const y = PAD + r * CH;
        out.push(`<g class="${cls("vz-cell", states[`${r},${c}`])}">
          <rect x="${x + 2}" y="${y + 2}" width="${CW - 4}" height="${CH - 4}" rx="6"/>
          <text${small(v)} x="${x + CW / 2}" y="${y + CH / 2}" dy="0.35em">${esc(v)}</text>
        </g>`);
      })
    );
    return `<svg class="vz-cells" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(opts.label || "grid")}">${out.join("")}</svg>`;
  }

  /* Bars: counts, running totals, heights -------------------------------------- */

  // Values as bars on a zero line (negative ones hang below it), each with its
  // value and a label (the index, or labels[i]) underneath.
  function barsSvg(values, opts = {}) {
    const states = opts.states || {};
    const pointers = opts.pointers || {};
    const labels = opts.labels || values.map((_, i) => i);
    const BW = Math.max(36, 8 * Math.max(...labels.map((l) => String(l).length), ...values.map((v) => String(v ?? "").length)) + 12);
    const nums = values.map((v) => (typeof v === "number" ? v : 0));
    const up = Math.max(0, opts.max || 0, ...nums);
    const down = Math.max(0, opts.min ? -opts.min : 0, ...nums.map((v) => -v));
    const scale = (opts.height || 96) / (up + down || 1);
    const top = PAD + 16;
    const base = top + up * scale;
    const below = base + down * scale + (down ? 16 : 0);
    const named = {};
    for (const [name, i] of Object.entries(pointers)) if (i !== null && i !== undefined && i >= 0) (named[i] = named[i] || []).push(name);
    const hasPtr = Object.keys(named).length > 0;
    const w = values.length * BW + 2 * PAD;
    const h = below + 18 + (hasPtr ? 16 : 0) + PAD;
    const out = [`<line class="vz-axis" x1="${PAD}" y1="${base}" x2="${w - PAD}" y2="${base}"/>`];
    values.forEach((v, i) => {
      const x = PAD + i * BW;
      const cx = x + BW / 2;
      const empty = v === null || v === undefined;
      const n = empty ? 0 : nums[i];
      const len = Math.max(Math.abs(n) * scale, empty ? 0 : 1.5);
      const y = n >= 0 ? base - len : base;
      const valueY = n >= 0 ? y - 5 : base + len + 12;
      out.push(`<g class="${cls("vz-bar", states[i])}">
        ${empty ? "" : `<rect x="${x + 6}" y="${y.toFixed(1)}" width="${BW - 12}" height="${len.toFixed(1)}" rx="3"/>`}
        ${empty ? "" : `<text class="vz-bar-v" x="${cx}" y="${valueY.toFixed(1)}">${esc(v)}</text>`}
        <text class="vz-index" x="${cx}" y="${below + 13}">${esc(labels[i])}</text>
        ${named[i] ? `<text class="vz-ptr" x="${cx}" y="${below + 29}">${esc(named[i].join(" · "))}</text>` : ""}
      </g>`);
    });
    return `<svg class="vz-bars" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(opts.label || "bars")}">${out.join("")}</svg>`;
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
      case "grid":
        return figure(gridSvg(p.cells || [], p), p.label);
      case "bars":
        return figure(barsSvg(p.values || [], p), p.label);
      case "vars": {
        const dl = `<dl class="vz-vars">${Object.entries(p.items || {})
          .map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${esc(typeof v === "string" ? v : JSON.stringify(v))}</dd></div>`)
          .join("")}</dl>`;
        return p.label ? figure(dl, p.label) : dl;
      }
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
    // A list written {"values", "join_at": i} continues into node i of the list before it.
    const listParams = problem.params.filter((p) => p.type === "ListNode");
    const joins = {};
    listParams.forEach((p, k) => {
      const v = ex.args[p.name];
      if (k && v && !Array.isArray(v) && v.join_at != null) joins[listParams[k - 1].name] = v.join_at;
    });
    let prevList = null;
    for (const p of problem.params) {
      const v = ex.args[p.name];
      if (p.type === "ListNode" && v && !Array.isArray(v) && v.join_at != null && prevList) {
        const own = v.values || [];
        const all = own.concat(prevList.slice(v.join_at));
        if (all.length > 14) return "";
        const st = {};
        for (let i = own.length; i < all.length; i++) st[i] = "found";
        parts.push(figure(listSvg(all, { states: st, label: p.name }), `${p.name} (shaded stops are shared)`));
        prevList = all;
        continue;
      }
      if (p.type === "RandomNode") {
        if (!Array.isArray(v) || v.length > 10) return "";
        parts.push(figure(listSvg(v.map((x) => x[0]), { randoms: v.map((x, i) => [i, x[1]]), label: p.name }), v.length ? `${p.name} (dashed = random)` : `${p.name} (empty)`));
        continue;
      }
      if (p.type === "TreeNode") {
        const t = layout(v);
        if (!drawable(t)) return "";
        t.nodes.forEach((n, i) => markValues.has(String(n.val)) && (states[i] = markValues.get(String(n.val))));
        parts.push(figure(treeSvg(t, states, {}, `${p.name} as a tree`), t.nodes.length ? p.name : `${p.name} (empty)`));
      } else if (p.type === "ListNode") {
        const l = listValues(v);
        if (!l || l.values.length > 12) return "";
        const st = {};
        if (joins[p.name] != null) for (let i = joins[p.name]; i < l.values.length; i++) st[i] = "found";
        parts.push(figure(listSvg(l.values, { cycleAt: l.cycleAt, states: st, label: p.name }), l.values.length ? p.name : `${p.name} (empty)`));
        prevList = l.values;
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
    } else if (problem.returns === "RandomNode") {
      if (!Array.isArray(out) || out.length > 10) return parts.length ? `<div class="ex-figure">${parts.join("")}</div>` : "";
      parts.push(...(parts.length ? [ARROW] : []), figure(listSvg(out.map((x) => x[0]), { randoms: out.map((x, i) => [i, x[1]]), label: "output" }), out.length ? "copy" : "output (empty)"));
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
