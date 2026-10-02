// Checks the written-out solutions (each problem's solution.json): every
// approach's code, in every language, must pass the problem's tests. An
// approach marked slow is meant to time out on the big tests, so it runs on
// the small ones only (up to 2500 characters of input, or its own "slow"
// number), with a generous limit.
//   node tools/check-solutions.mjs [--jobs 4] [problem dir or id ...]
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { check } from "./judge.mjs";

const DSA = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const PROBLEMS = path.join(DSA, "problems");
const SMALL_CHARS = 2500;
const SLOW_LIMIT_MS = 20_000;

const argv = process.argv.slice(2);
let jobs = 4;
const targets = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === "--jobs") jobs = Number(argv[++i]) || jobs;
  else targets.push(argv[i]);
}

function solutionsUnder(dir) {
  if (existsSync(path.join(dir, "solution.json"))) return [dir];
  return readdirSync(dir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .flatMap((d) => solutionsUnder(path.join(dir, d.name)));
}

function resolve(t) {
  for (const p of [t, path.join(PROBLEMS, t)]) if (existsSync(p) && statSync(p).isDirectory()) return solutionsUnder(path.resolve(p));
  const hit = solutionsUnder(PROBLEMS).find((d) => path.basename(d) === t);
  if (!hit) throw new Error(`no solution.json for ${t}`);
  return [hit];
}

const dirs = [...new Set((targets.length ? targets : [PROBLEMS]).flatMap(resolve))].sort();
const work = [];
for (const dir of dirs) {
  const sol = JSON.parse(readFileSync(path.join(dir, "solution.json"), "utf8"));
  sol.approaches.forEach((a, k) => {
    for (const [lang, code] of Object.entries(a.code)) work.push({ id: path.basename(dir), k: k + 1, title: a.title, slow: a.slow, lang, code });
  });
}

const clip = (v) => {
  const s = JSON.stringify(v);
  return s && s.length > 160 ? `${s.slice(0, 160)}…` : s;
};

const failures = [];
let done = 0;
async function one(w) {
  try {
    const { total, results } = await check({ id: w.id, lang: w.lang, code: w.code, ...(w.slow ? { maxChars: typeof w.slow === "number" ? w.slow : SMALL_CHARS, limitMs: SLOW_LIMIT_MS } : {}) });
    const bad = results.findIndex((r) => r.verdict !== "passed");
    if (!total) failures.push({ ...w, why: "no tests to run" });
    else if (bad >= 0) {
      const r = results[bad];
      failures.push({ ...w, why: `${r.verdict} on test ${bad + 1}/${total}${r.error ? `: ${r.error.split("\n").slice(0, 6).join("\n    ")}` : ""}\n    args ${clip(r.args)}\n    got ${clip(r.output)} want ${clip(r.expected)}` });
    }
  } catch (err) {
    failures.push({ ...w, why: err.message });
  }
  done++;
}

const queue = work.slice();
await Promise.all(Array.from({ length: Math.min(jobs, queue.length) }, async () => {
  while (queue.length) await one(queue.shift());
}));

for (const f of failures) console.log(`FAIL ${f.id} #${f.k} ${f.title} [${f.lang}${f.slow ? ", small tests" : ""}]: ${f.why}`);
console.log(`${dirs.length} problems, ${done} solutions run, ${failures.length} failing.`);
process.exit(failures.length ? 1 : 0);
