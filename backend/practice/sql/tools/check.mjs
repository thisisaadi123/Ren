// Checks the SQL bank. For every problem (or the ones named):
//   1. problem.json is complete and its topic and pattern are in the taxonomy
//   2. the reference query runs on every dataset (and, with --write-expected,
//      its results become the expected answers; otherwise they must match)
//   3. an ordered problem's ORDER BY decides the order completely: the
//      reference gives the same rows when the tables are loaded backwards
//   4. every wrong query in the problem fails at least one dataset
//   5. there are enough hidden datasets, and not too many empty answers
// Usage: node backend/practice/sql/tools/check.mjs [--write-expected] [--quiet] [id|dir ...]
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { compare, runAll } from "./engine.mjs";
import { problemDirs, taxonomy } from "./judge.mjs";

const args = process.argv.slice(2);
const write = args.includes("--write-expected");
const quiet = args.includes("--quiet");
const only = args.filter((a) => !a.startsWith("--"));

const MIN_HIDDEN = { easy: 8, medium: 10, hard: 12 };
const tax = taxonomy();
const patterns = new Map(tax.topics.flatMap((t) => t.patterns.map((p) => [`${t.id}/${p.id}`, p])));

const dirs = problemDirs().filter(
  (d) => !only.length || only.some((o) => path.basename(d) === o || path.resolve(d).startsWith(path.resolve(o)))
);

// One test per line keeps the files readable and their diffs small.
const format = (suite) =>
  `{"problem": ${JSON.stringify(suite.problem)}, "tests": [\n${suite.tests.map((t) => `  ${JSON.stringify(t)}`).join(",\n")}\n]}\n`;

let bad = 0;
const ids = new Map();
for (const dir of dirs) {
  const problems = [];
  const fail = (msg) => problems.push(msg);
  const meta = JSON.parse(readFileSync(path.join(dir, "problem.json"), "utf8"));
  const file = path.join(dir, "tests.json");
  const suite = JSON.parse(readFileSync(file, "utf8"));
  const tests = suite.tests;

  // 1. The problem itself.
  if (meta.id !== path.basename(dir)) fail(`id ${meta.id} doesn't match its folder`);
  if (ids.has(meta.id)) fail(`id ${meta.id} is also used by ${ids.get(meta.id)}`);
  ids.set(meta.id, dir);
  if (!patterns.has(`${meta.topic}/${meta.pattern}`)) fail(`${meta.topic}/${meta.pattern} isn't in the taxonomy`);
  if (path.basename(path.dirname(dir)) !== meta.pattern || path.basename(path.dirname(path.dirname(dir))) !== meta.topic) {
    fail("the folder isn't problems/<topic>/<pattern>/<id>");
  }
  for (const k of ["title", "statement", "reference"]) if (!meta[k]) fail(`missing ${k}`);
  if (!["easy", "medium", "hard"].includes(meta.difficulty)) fail(`difficulty ${meta.difficulty}?`);
  if (typeof meta.ordered !== "boolean") fail("ordered must be true or false");
  if (!Array.isArray(meta.tables) || !meta.tables.length) fail("no tables");
  const examples = tests.filter((t) => t.example);
  if (!examples.length) fail("no examples");

  // 2. The reference on every dataset.
  const datasets = tests.map((t) => t.data);
  const ref = runAll(meta.tables, datasets, meta.reference);
  ref.forEach((r, i) => {
    if (r.error) return fail(`reference fails on test ${i + 1}: ${r.error}`);
    const want = { columns: r.columns, rows: r.rows };
    if (write) tests[i].expected = want;
    else if (!tests[i].expected) fail(`test ${i + 1} has no expected answer (run with --write-expected)`);
    else if (!compare(want, tests[i].expected, meta.ordered).ok) fail(`test ${i + 1}: expected answer is out of date`);
  });

  // 3. A full ORDER BY: the same answer with every table loaded backwards.
  if (meta.ordered && !problems.length) {
    const backwards = datasets.map((d) => Object.fromEntries(Object.entries(d).map(([t, rows]) => [t, [...rows].reverse()])));
    runAll(meta.tables, backwards, meta.reference).forEach((r, i) => {
      if (!r.error && !compare(r, ref[i], true).ok) fail(`test ${i + 1}: the order isn't fully decided (ties in ORDER BY)`);
    });
  }

  // 4. Wrong queries must be caught.
  for (const [w, sql] of (meta.wrong || []).entries()) {
    const results = runAll(meta.tables, datasets, sql);
    const caught = results.some((r, i) => r.error || !compare(r, ref[i], meta.ordered).ok);
    if (!caught) fail(`wrong query ${w + 1} passes every test`);
    if (results.every((r) => r.error)) fail(`wrong query ${w + 1} doesn't even run: ${results[0].error}`);
  }

  // 5. Enough hidden data, and answers worth checking.
  const hidden = tests.length - examples.length;
  if (hidden < (MIN_HIDDEN[meta.difficulty] || 8)) fail(`only ${hidden} hidden tests`);
  const empty = ref.filter((r) => !r.error && !r.rows.length).length;
  if (empty > tests.length * 0.34) fail(`${empty} of ${tests.length} tests expect no rows`);

  if (write && !problems.some((m) => m.startsWith("reference"))) writeFileSync(file, format(suite));
  if (problems.length) {
    bad++;
    console.log(`FAIL ${meta.id}`);
    problems.forEach((m) => console.log(`  - ${m}`));
  } else if (!quiet) {
    console.log(`ok   ${meta.id} (${tests.length} tests, ${(meta.wrong || []).length} wrong queries caught)`);
  }
}
console.log(`${dirs.length} problems, ${bad} failing.`);
process.exit(bad ? 1 : 0);
