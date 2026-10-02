#!/usr/bin/env node
// Ren DSA pipeline: checks problems and the bank. See ../pipeline.md.
//
//   npm run check:dsa                      every problem + bank-wide checks
//   npm run check:dsa -- <problem-dir>...  just these problems (+ bank checks)
//   npm run check:dsa -- --write-expected  fill in missing "expected" values from the reference
//   npm run check:dsa -- --jobs 4          check 4 problems at a time
//   npm run check:dsa -- --quiet           print only failing problems
//
// Exits 1 if anything fails. Built tests and rendered statements go to ../build/ (gitignored).
import Ajv2020 from "ajv/dist/2020.js";
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import YAML from "yaml";
import { same, show } from "./lib/compare.mjs";
import { available, LANGS, PY_RUNNER_PATH, runSolution, whyUnavailable } from "./lib/langs.mjs";
import { parseLossless, runLines } from "./lib/run.mjs";

const TOOLS = path.dirname(fileURLToPath(import.meta.url));
// REN_DSA_ROOT points the pipeline at another copy of the bank (used by selftest.mjs).
const DSA = process.env.REN_DSA_ROOT ? path.resolve(process.env.REN_DSA_ROOT) : path.dirname(TOOLS);
const PROBLEMS = path.join(DSA, "problems");
const BUILD = path.join(DSA, "build");
const config = JSON.parse(readFileSync(path.join(TOOLS, "config.json"), "utf8"));

const argv = process.argv.slice(2);
const jobsAt = argv.indexOf("--jobs");
const JOBS = jobsAt >= 0 ? Math.max(1, Number(argv[jobsAt + 1]) || 1) : 1;
const flags = new Set(argv.filter((a) => a.startsWith("--")));
const targets = argv.filter((a, i) => !a.startsWith("--") && argv[i - 1] !== "--jobs").map((a) => path.resolve(a));
const QUIET = flags.has("--quiet");
const WRITE_EXPECTED = flags.has("--write-expected");

/* Reporting -------------------------------------------------------------- */

const MARK = { pass: "✓", fail: "✗", skip: "–", info: "·" };
class Report {
  constructor(title) {
    this.title = title;
    this.rows = [];
  }
  add(status, check, notes = []) {
    this.rows.push({ status, check, notes: [notes].flat().filter(Boolean) });
  }
  get failed() {
    return this.rows.some((r) => r.status === "fail");
  }
  print() {
    console.log(`\n${this.failed ? "✗" : "✓"} ${this.title}`);
    for (const r of this.rows) {
      console.log(`  ${MARK[r.status]} ${r.check}`);
      for (const n of r.notes.slice(0, 12)) console.log(`      ${n}`);
      if (r.notes.length > 12) console.log(`      … and ${r.notes.length - 12} more`);
    }
  }
}

/* Loading ---------------------------------------------------------------- */

const read = (f) => readFileSync(f, "utf8");
const readYaml = (f) => YAML.parse(read(f));

const taxonomy = readYaml(path.join(DSA, "taxonomy.yaml"));
const topicsById = new Map(taxonomy.topics.map((t) => [t.id, t]));
const patternTopic = new Map(taxonomy.topics.flatMap((t) => t.patterns.map((p) => [p.id, t.id])));

const ajv = new Ajv2020({ strict: true, strictRequired: false, allErrors: true });
const validateSchema = ajv.compile(JSON.parse(read(path.join(DSA, "problem.schema.json"))));

function findProblems(dir) {
  if (!existsSync(dir)) return [];
  if (existsSync(path.join(dir, "problem.yaml"))) return [dir];
  return readdirSync(dir)
    .filter((n) => !n.startsWith(".") && statSync(path.join(dir, n)).isDirectory())
    .flatMap((n) => findProblems(path.join(dir, n)));
}

// "--n 50000 --shape uniform" -> { n: 50000, shape: "uniform" }
function parseGenArgs(text) {
  const opts = {};
  const parts = String(text).trim().split(/\s+/).filter(Boolean);
  for (let i = 0; i < parts.length; i++) {
    if (!parts[i].startsWith("--")) throw new Error(`bad generate args: ${text}`);
    const key = parts[i].slice(2);
    const next = parts[i + 1];
    if (next === undefined || next.startsWith("--")) opts[key] = true;
    else {
      opts[key] = /^-?\d+(\.\d+)?$/.test(next) ? Number(next) : next;
      i++;
    }
  }
  return opts;
}

async function python(mode, file, extra, input) {
  const { lines, killed, stderr } = await runLines("python3", [PY_RUNNER_PATH, mode, file, ...extra], {
    input,
    quietMs: 120_000,
  });
  if (killed) throw new Error(`${path.basename(file)} (${mode}) timed out`);
  const results = lines.filter((l) => l.id !== undefined);
  if (!results.length && stderr.trim()) throw new Error(`${path.basename(file)} (${mode}): ${stderr.trim().split("\n").slice(-2).join(" | ")}`);
  return results;
}
const jsonl = (items) => items.map((x) => exactJson(x)).join("\n") + "\n";

// A recipe with "count": n stands for n tests, <id>-1 … <id>-n, each with its own seed.
function expandTests(tests) {
  return (tests ?? []).flatMap((t) => {
    const n = t.generate?.count;
    if (!n) return [t];
    return Array.from({ length: n }, (_, i) => ({ ...t, id: `${t.id}-${i + 1}`, generate: { args: t.generate.args } }));
  });
}

/* Comparing answers --------------------------------------------------------- */

// items: [{id, args, expected, actual}] -> Map(id -> {ok, msg})
async function compareMany(meta, dir, items) {
  if (meta.checker.type !== "custom") {
    return new Map(items.map((it) => [it.id, { ok: same(meta.checker, it.actual, it.expected) }]));
  }
  const out = await python("check", path.join(dir, "checker.py"), [], jsonl(items));
  return new Map(out.map((r) => [r.id, r]));
}

/* One problem ------------------------------------------------------------- */

async function checkProblem(dir) {
  const rel = path.relative(DSA, dir);
  const report = new Report(rel);
  let meta;

  // 1. Schema and paths --------------------------------------------------------
  const problems1 = [];
  try {
    meta = readYaml(path.join(dir, "problem.yaml"));
  } catch (e) {
    report.add("fail", "1 Schema and paths", `problem.yaml doesn't parse: ${e.message}`);
    return { report };
  }
  report.title = `${meta.id ?? rel} (${meta.difficulty ?? "?"}, ${meta.status ?? "?"})`;
  if (!validateSchema(meta)) {
    for (const e of validateSchema.errors) problems1.push(`problem.yaml${e.instancePath} ${e.message}`);
  }
  if (!topicsById.has(meta.topic)) problems1.push(`topic "${meta.topic}" isn't in taxonomy.yaml`);
  if (patternTopic.get(meta.pattern) !== meta.topic) problems1.push(`pattern "${meta.pattern}" isn't a pattern of topic "${meta.topic}"`);
  const expectedPath = path.join(PROBLEMS, String(meta.topic), String(meta.pattern), String(meta.id));
  if (path.resolve(dir) !== expectedPath) problems1.push(`folder should be problems/${meta.topic}/${meta.pattern}/${meta.id}`);

  const need = ["statement.md", "reference.py", "brute.py", "validator.py", "gen.py", "tests.json"];
  if (meta.checker?.type === "custom") need.push("checker.py");
  for (const f of need) if (!existsSync(path.join(dir, f))) problems1.push(`missing ${f}`);
  const wrongDir = path.join(dir, "wrong");
  const wrongFiles = existsSync(wrongDir) ? readdirSync(wrongDir).filter((f) => f.endsWith(".py")).sort() : [];
  if (!wrongFiles.length) problems1.push("wrong/ needs at least one known-wrong solution");
  if (existsSync(path.join(dir, "statement.md")) && !read(path.join(dir, "statement.md")).includes("{{examples}}")) {
    problems1.push("statement.md has no {{examples}} marker");
  }

  let testsDoc;
  try {
    testsDoc = parseLossless(read(path.join(dir, "tests.json")));
  } catch (e) {
    problems1.push(`tests.json doesn't parse: ${e.message}`);
  }
  const params = meta.kind === "design" ? [] : meta.signature?.params ?? [];
  const names = meta.kind === "design" ? "calls" : params.map((p) => p.name).sort().join(",");
  if (testsDoc) testsDoc.expanded = expandTests(testsDoc.tests);
  if (testsDoc) {
    if (testsDoc.problem !== meta.id) problems1.push(`tests.json "problem" should be "${meta.id}"`);
    if (testsDoc.version !== meta.version) problems1.push(`tests.json version ${testsDoc.version} ≠ problem version ${meta.version}`);
    if (!Number.isInteger(testsDoc.seed)) problems1.push("tests.json needs an integer seed");
    const ids = new Set();
    for (const t of testsDoc.expanded) {
      if (ids.has(t.id)) problems1.push(`duplicate test id ${t.id}`);
      ids.add(t.id);
      if (!["example", "sample", "edge", "random", "max"].includes(t.kind)) problems1.push(`${t.id}: unknown kind "${t.kind}"`);
      if (t.example && !t.visible) problems1.push(`${t.id}: examples must be visible`);
      if (t.example && !t.explanation) problems1.push(`${t.id}: examples need an explanation`);
      if (t.generate) {
        if (t.visible) problems1.push(`${t.id}: generated tests can't be visible`);
        if (t.expected !== undefined) problems1.push(`${t.id}: generated tests get "expected" from the reference, so don't store one`);
      } else if (Object.keys(t.input ?? {}).sort().join(",") !== names) {
        problems1.push(`${t.id}: input keys should be exactly: ${names}`);
      }
    }
    const tests = testsDoc.expanded;
    const visible = tests.filter((t) => t.visible).length;
    const { min, max } = config.visibleTests;
    if (visible < min || visible > max) problems1.push(`${visible} visible tests; want ${min}–${max}`);
    if (!tests.some((t) => t.example)) problems1.push("no examples (tests with \"example\": true)");
    const hidden = tests.length - visible;
    const target = config.hiddenTests[meta.difficulty];
    if (target && hidden < Math.floor(target * config.hiddenTestsFloor)) {
      problems1.push(`${hidden} hidden tests; a ${meta.difficulty} problem wants about ${target}`);
    }
  }
  report.add(problems1.length ? "fail" : "pass", "1 Schema and paths", problems1);
  if (problems1.length) return { report, meta };

  const langLimit = (lang) => meta.limits.time_ms * config.timeMultipliers[lang];

  // Build the full test list: stored tests + generated recipes.
  let tests;
  try {
    const recipes = testsDoc.expanded.filter((t) => t.generate);
    const built = recipes.length
      ? await python(
          "build",
          path.join(dir, "gen.py"),
          [],
          jsonl(recipes.map((t) => ({ id: t.id, seed: testsDoc.seed, opts: parseGenArgs(t.generate.args) })))
        )
      : [];
    const builtArgs = new Map(built.map((b) => [b.id, b.args]));
    tests = testsDoc.expanded.map((t) => ({
      ...t,
      args: t.generate ? builtArgs.get(t.id) : t.input,
      generated: Boolean(t.generate),
    }));
    const missing = tests.filter((t) => !t.args).map((t) => t.id);
    if (missing.length) throw new Error(`gen.py build() returned nothing for ${missing.join(", ")}`);
  } catch (e) {
    report.add("fail", "2 Validator", `couldn't build generated tests: ${e.message}`);
    return { report, meta };
  }

  // Small random inputs for the brute-force cross-check.
  let small = [];
  try {
    small = await python("small", path.join(dir, "gen.py"), [String(testsDoc.seed), String(config.smallRandomTests)], "");
  } catch (e) {
    report.add("fail", "2 Validator", `gen.py small() failed: ${e.message}`);
    return { report, meta };
  }

  // 2. Validator ---------------------------------------------------------------
  const toValidate = [...tests.map((t) => ({ id: t.id, args: t.args })), ...small];
  const verdicts = await python("validate", path.join(dir, "validator.py"), [], jsonl(toValidate));
  const rejected = verdicts.filter((v) => !v.ok).map((v) => `${v.id}: ${v.msg}`);
  if (verdicts.length !== toValidate.length) rejected.push(`validator answered ${verdicts.length} of ${toValidate.length} inputs`);
  report.add(rejected.length ? "fail" : "pass", "2 Validator", rejected.length ? rejected : `${tests.length} tests + ${small.length} random small inputs accepted`);
  if (rejected.length) return { report, meta };

  // 3. Reference vs brute force ----------------------------------------------------
  const notes3 = [];
  const pyLimit = langLimit("python");
  const refRuns = await runSolution({ lang: "python", file: path.join(dir, "reference.py"), meta, tests, limitMs: pyLimit, buildDir: BUILD });
  const refOut = new Map();
  for (const r of refRuns) {
    if (r.error || r.tle || r.notRun) notes3.push(`reference on ${r.id}: ${r.error ?? "not run"}`);
    else refOut.set(r.id, r.out);
  }
  let rewrote = false;
  if (!notes3.length) {
    const stored = tests.filter((t) => !t.generated && t.expected !== undefined);
    const cmp = await compareMany(meta, dir, stored.map((t) => ({ id: t.id, args: t.args, expected: t.expected, actual: refOut.get(t.id) })));
    for (const t of stored) {
      const c = cmp.get(t.id);
      if (!c?.ok) notes3.push(`${t.id}: stored expected ${show(t.expected)} but the reference returns ${show(refOut.get(t.id))}${c?.msg ? ` (${c.msg})` : ""}`);
    }
    for (const t of tests) {
      if (t.generated) t.expected = refOut.get(t.id);
      else if (t.expected === undefined) {
        if (WRITE_EXPECTED) {
          const doc = testsDoc.tests.find((x) => x.id === t.id); // stored tests aren't expanded, so the ids match
          doc.expected = t.expected = refOut.get(t.id);
          rewrote = true;
        } else notes3.push(`${t.id}: no "expected" stored (run with --write-expected to fill it from the reference)`);
      }
    }
  }
  if (!notes3.length) {
    // Brute force on the random small inputs and on stored tests that are small enough.
    // Small stored tests also go through the brute force, unless marked "no_brute" (short input, huge values).
    const bruteOk = (t) => !t.no_brute && exactJson(t.args).length <= config.bruteMaxInputChars;
    const cases = [...small, ...tests.filter((t) => !t.generated && bruteOk(t)).map((t) => ({ id: t.id, args: t.args }))];
    const quiet = 30_000;
    const [bruteRuns, refSmall] = await Promise.all([
      runSolution({ lang: "python", file: path.join(dir, "brute.py"), meta, tests: cases, limitMs: quiet, buildDir: BUILD }),
      runSolution({ lang: "python", file: path.join(dir, "reference.py"), meta, tests: cases, limitMs: quiet, buildDir: BUILD }),
    ]);
    const refById = new Map(refSmall.map((r) => [r.id, r]));
    const errs = [...bruteRuns, ...refSmall].filter((r) => r.error || r.notRun);
    for (const r of errs.slice(0, 5)) notes3.push(`${r.id}: ${r.error ?? "not run"}`);
    if (!errs.length) {
      const items = bruteRuns.map((b) => ({ id: b.id, args: cases.find((c) => c.id === b.id).args, expected: b.out, actual: refById.get(b.id).out }));
      const cmp = await compareMany(meta, dir, items);
      const differ = items.filter((it) => !cmp.get(it.id)?.ok);
      for (const it of differ.slice(0, 5)) {
        notes3.push(`${it.id}: brute ${show(it.expected)} vs reference ${show(it.actual)} on ${show(it.args, 120)}`);
      }
      if (!differ.length) notes3.unshift(`agree on ${items.length} inputs (${small.length} random + ${items.length - small.length} stored)`);
    }
  }
  const failed3 = notes3.some((n) => !n.startsWith("agree on"));
  report.add(failed3 ? "fail" : "pass", "3 Reference vs brute force", notes3);
  if (failed3) return { report, meta };

  // 4. Wrong solutions must fail ---------------------------------------------------
  const notes4 = [];
  let failed4 = false;
  for (const f of wrongFiles) {
    const runs = await runSolution({ lang: "python", file: path.join(wrongDir, f), meta, tests, limitMs: pyLimit, buildDir: BUILD });
    const answered = runs.filter((r) => !r.error && !r.tle && !r.notRun && r.ms <= pyLimit);
    const cmp = await compareMany(meta, dir, answered.map((r) => ({ id: r.id, args: tests.find((t) => t.id === r.id).args, expected: tests.find((t) => t.id === r.id).expected, actual: r.out })));
    const caught = runs.find((r) => r.error || r.tle || r.ms > pyLimit || (cmp.has(r.id) && !cmp.get(r.id).ok));
    const timedOut = runs.some((r) => r.tle || r.ms > pyLimit);
    if (!caught) {
      failed4 = true;
      notes4.push(`wrong/${f} passes every test: the tests are too weak`);
    } else if (f.startsWith("too_slow") && !timedOut) {
      failed4 = true;
      notes4.push(`wrong/${f} fails on ${caught.id} but never times out: add bigger max-size tests`);
    } else {
      const why = caught.tle || caught.ms > pyLimit ? "time limit" : caught.error ? "error" : "wrong answer";
      notes4.push(`wrong/${f} caught by ${caught.id} (${why})`);
    }
  }
  report.add(failed4 ? "fail" : "pass", "4 Wrong solutions fail", notes4);

  // 5. Every language ----------------------------------------------------------------
  const notes5 = [];
  let failed5 = false;
  const skipped = [];
  const missingLangs = [];
  for (const lang of config.languages) {
    const file = path.join(dir, LANGS[lang].file);
    const limit = langLimit(lang);
    const budget = limit * config.referenceBudget;
    if (!(await available(lang))) {
      skipped.push(LANGS[lang].label);
      notes5.push(`${LANGS[lang].label}: not checked (${whyUnavailable(lang)})`);
      continue;
    }
    if (!existsSync(file)) {
      // Drafts can be checked before every language is written; publishing needs all of them.
      if (meta.status === "published" || meta.status === "review") failed5 = true;
      missingLangs.push(LANGS[lang].label);
      notes5.push(`${LANGS[lang].label}: ${LANGS[lang].file} not written yet`);
      continue;
    }
    const runs = lang === "python" ? refRuns : await runSolution({ lang, file, meta, tests, limitMs: limit, buildDir: BUILD });
    const bad = runs.filter((r) => r.error || r.tle || r.notRun);
    const answered = runs.filter((r) => !bad.includes(r));
    const cmp = await compareMany(meta, dir, answered.map((r) => ({ id: r.id, args: tests.find((t) => t.id === r.id).args, expected: tests.find((t) => t.id === r.id).expected, actual: r.out })));
    const wrong = answered.filter((r) => !cmp.get(r.id)?.ok);
    const slow = answered.filter((r) => r.ms > budget);
    const worst = answered.reduce((m, r) => (r.ms > m.ms ? r : m), { ms: 0, id: "-" });
    if (bad.length || wrong.length || slow.length) failed5 = true;
    const status = bad.length || wrong.length || slow.length ? "✗" : "✓";
    notes5.push(`${status} ${LANGS[lang].label}: slowest ${worst.ms.toFixed(1)} ms on ${worst.id} (budget ${budget} ms, limit ${limit} ms)`);
    for (const r of bad.slice(0, 3)) notes5.push(`    ${r.id}: ${r.error ?? "not run"}`);
    for (const r of wrong.slice(0, 3)) notes5.push(`    ${r.id}: returned ${show(r.out)}, expected ${show(tests.find((t) => t.id === r.id).expected)}`);
    for (const r of slow.slice(0, 3)) notes5.push(`    ${r.id}: ${r.ms.toFixed(1)} ms is over half the limit`);
  }
  report.add(failed5 ? "fail" : skipped.length || missingLangs.length ? "info" : "pass", "5 Every language", notes5);

  // 6–7. Blind solve and human review ----------------------------------------------------
  if (meta.status === "published") {
    const why = [];
    if (!meta.reviewed_by?.length) why.push("published without reviewed_by");
    if (skipped.length) why.push(`published but not checked in ${skipped.join(", ")}`);
    report.add(why.length ? "fail" : "pass", "6–7 Blind solve and review", why.length ? why : `reviewed by ${meta.reviewed_by.join(", ")}`);
  } else {
    report.add("info", "6–7 Blind solve and review", `pending (status: ${meta.status}); a reviewer blind-solves it, then adds their name to reviewed_by`);
  }

  // Outputs: fill-ins, built tests and the rendered statement.
  if (rewrote) writeFileSync(path.join(dir, "tests.json"), formatTests(testsDoc));
  writeBuild(meta, dir, tests);
  return { report, meta };
}

/* Build outputs ----------------------------------------------------------------- */

function writeBuild(meta, dir, tests) {
  mkdirSync(path.join(BUILD, "tests"), { recursive: true });
  mkdirSync(path.join(BUILD, "statements"), { recursive: true });
  const out = tests.map(({ id, kind, visible, example, explanation, args, expected }) => ({ id, kind, visible: Boolean(visible), example: Boolean(example), explanation, args, expected }));
  writeFileSync(path.join(BUILD, "tests", `${meta.id}.json`), exactJson({ problem: meta.id, version: meta.version, tests: out }));
  const params = meta.kind === "design" ? ["calls"] : meta.signature.params.map((p) => p.name);
  const examples = tests
    .filter((t) => t.example)
    .map((t, i) => {
      const input = params.map((p) => `${p} = ${pretty(t.args[p])}`).join(", ");
      return `**Example ${i + 1}**\n\n\`\`\`\nInput: ${input}\nOutput: ${pretty(t.expected)}\n\`\`\`\n\n${t.explanation}`;
    })
    .join("\n\n");
  const statement = read(path.join(dir, "statement.md")).replace("{{examples}}", examples);
  writeFileSync(path.join(BUILD, "statements", `${meta.id}.md`), `# ${meta.title}\n\n${statement}`);
}

// Values as people read them: [4, 2, 7] rather than [4,2,7].
// JSON with integers past 2^53 written as exact digits (read back with parseLossless).
const exactJson = (v) => JSON.stringify(v, (_k, x) => (typeof x === "bigint" ? `\u0000${x}` : x)).replace(/"\\u0000(-?\d+)"/g, "$1");

const pretty = (v) => (Array.isArray(v) ? `[${v.map(pretty).join(", ")}]` : typeof v === "bigint" ? v.toString() : JSON.stringify(v));

// tests.json with one line per field, values kept compact.
function formatTests(doc) {
  const inline = (v) => exactJson(v);
  const test = (t) => `    {\n${Object.entries(t).map(([k, v]) => `      ${JSON.stringify(k)}: ${inline(v)}`).join(",\n")}\n    }`;
  const head = Object.entries(doc)
    .filter(([k]) => k !== "tests" && k !== "expanded")
    .map(([k, v]) => `  ${JSON.stringify(k)}: ${inline(v)}`);
  return `{\n${head.join(",\n")},\n  "tests": [\n${doc.tests.map(test).join(",\n")}\n  ]\n}\n`;
}

/* Bank-wide checks --------------------------------------------------------------- */

function checkBank(loaded) {
  const report = new Report("Bank");

  // Taxonomy
  const tax = [];
  const sum = taxonomy.topics.reduce((s, t) => s + t.count, 0);
  if (sum !== taxonomy.total) tax.push(`topic counts add up to ${sum}, not ${taxonomy.total}`);
  const ids = taxonomy.topics.flatMap((t) => t.patterns.map((p) => p.id));
  const dup = ids.filter((id, i) => ids.indexOf(id) !== i);
  if (dup.length) tax.push(`duplicate pattern ids: ${[...new Set(dup)].join(", ")}`);
  for (const t of taxonomy.topics) {
    for (const p of t.prerequisites) if (!topicsById.has(p)) tax.push(`${t.id}: unknown prerequisite ${p}`);
    if (t.patterns.every((p) => Number.isInteger(p.count))) {
      const s = t.patterns.reduce((a, p) => a + p.count, 0);
      if (s !== t.count) tax.push(`${t.id}: pattern counts add up to ${s}, not ${t.count}`);
    }
  }
  report.add(tax.length ? "fail" : "pass", "Taxonomy", tax.length ? tax : `${taxonomy.topics.length} topics, ${ids.length} patterns, ${sum} problems`);

  // Problems across the bank
  const bank = [];
  const metas = loaded.filter((l) => l.meta?.id);
  const seen = new Map();
  for (const { meta } of metas) {
    if (seen.has(meta.id)) bank.push(`problem id ${meta.id} is used twice`);
    seen.set(meta.id, meta);
  }
  const published = metas.filter((l) => l.meta.status === "published");
  for (const t of taxonomy.topics) {
    for (const p of t.patterns) {
      const n = published.filter((l) => l.meta.pattern === p.id).length;
      if (Number.isInteger(p.count) && n > p.count) bank.push(`${p.id}: ${n} published, target is ${p.count}`);
    }
  }
  // Near-duplicate statements (word 3-gram overlap)
  const grams = (text) => {
    const w = text.toLowerCase().replace(/[^a-z0-9 ]+/g, " ").split(/\s+/).filter(Boolean);
    return new Set(w.slice(2).map((_, i) => `${w[i]} ${w[i + 1]} ${w[i + 2]}`));
  };
  const statements = metas.map((l) => ({ id: l.meta.id, g: grams(read(path.join(l.dir, "statement.md"))) }));
  for (let i = 0; i < statements.length; i++) {
    for (let j = i + 1; j < statements.length; j++) {
      const a = statements[i].g;
      const b = statements[j].g;
      const inter = [...a].filter((x) => b.has(x)).length;
      const score = inter / (a.size + b.size - inter || 1);
      if (score >= config.nearDuplicateThreshold) bank.push(`${statements[i].id} and ${statements[j].id} look alike (${Math.round(score * 100)}% overlap)`);
    }
  }
  report.add(bank.length ? "fail" : "pass", "Problems", bank.length ? bank : `${metas.length} problems (${published.length} published)`);

  // Sheets
  const sheetNotes = [];
  const sheetDir = path.join(DSA, "sheets");
  const files = existsSync(sheetDir) ? readdirSync(sheetDir).filter((f) => f.endsWith(".yaml")) : [];
  for (const f of files) {
    let sheet;
    try {
      sheet = readYaml(path.join(sheetDir, f));
    } catch (e) {
      sheetNotes.push(`${f}: doesn't parse (${e.message})`);
      continue;
    }
    const topic = topicsById.get(sheet?.topic);
    if (!topic) {
      sheetNotes.push(`${f}: unknown topic ${sheet?.topic}`);
      continue;
    }
    if (!f.startsWith("_") && f !== `${topic.id}.yaml`) sheetNotes.push(`${f}: should be named ${topic.id}.yaml`);
    const entries = sheet.entries ?? [];
    const slugs = new Set();
    for (const e of entries) {
      const at = `${f} ${e.slug}`;
      if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(e.slug ?? "")) sheetNotes.push(`${at}: bad slug`);
      if (slugs.has(e.slug)) sheetNotes.push(`${at}: listed twice`);
      slugs.add(e.slug);
      if (!e.title) sheetNotes.push(`${at}: missing title`);
      if (!["easy", "medium", "hard"].includes(e.difficulty)) sheetNotes.push(`${at}: difficulty must be easy, medium or hard`);
      if (patternTopic.get(e.pattern) !== topic.id) sheetNotes.push(`${at}: pattern ${e.pattern} isn't in ${topic.id}`);
      if (typeof e.premium !== "boolean") sheetNotes.push(`${at}: premium must be true or false`);
      if (!String(e.note ?? "").trim()) sheetNotes.push(`${at}: missing note`);
      if (e.ren_problem) {
        const m = seen.get(e.ren_problem);
        if (!m) sheetNotes.push(`${at}: ren_problem ${e.ren_problem} doesn't exist`);
        else if (m.pattern !== e.pattern) sheetNotes.push(`${at}: ren_problem ${e.ren_problem} is ${m.pattern}, not ${e.pattern}`);
      }
    }
    const premium = entries.filter((e) => e.premium).length;
    if (entries.length && premium / entries.length > config.sheetPremiumMax) sheetNotes.push(`${f}: ${premium} of ${entries.length} are Premium (max ${config.sheetPremiumMax * 100}%)`);
  }
  report.add(sheetNotes.length ? "fail" : "pass", "Sheets", sheetNotes.length ? sheetNotes : `${files.length} sheet file(s)`);
  return report;
}

/* Main ------------------------------------------------------------------------ */

const dirs = targets.length ? targets.flatMap(findProblems) : findProblems(PROBLEMS);
if (targets.length && !dirs.length) {
  console.error(`No problems found under: ${targets.join(", ")}`);
  process.exit(1);
}
const loaded = new Array(dirs.length);
let next = 0;
async function worker() {
  while (next < dirs.length) {
    const i = next++;
    const started = Date.now();
    const result = await checkProblem(dirs[i]);
    result.report.title += `  [${((Date.now() - started) / 1000).toFixed(1)}s]`;
    if (!QUIET || result.report.failed) result.report.print();
    loaded[i] = { ...result, dir: dirs[i] };
  }
}
await Promise.all(Array.from({ length: Math.min(JOBS, dirs.length || 1) }, worker));
// Bank checks always look at every problem, even when only some were checked above.
const all = targets.length
  ? findProblems(PROBLEMS).map((dir) => {
      try {
        return { dir, meta: readYaml(path.join(dir, "problem.yaml")) };
      } catch {
        return { dir };
      }
    })
  : loaded;
const bank = checkBank(all);
bank.print();

const failing = loaded.filter((l) => l.report.failed).length;
console.log(`\n${loaded.length} problem(s) checked, ${failing} failing${bank.failed ? ", bank checks failing" : ""}.`);
process.exit(failing || bank.failed ? 1 : 0);
