// Ren SQL judge: what the SQL problem page needs from the bank.
//   problemView(id)        the statement, tables, examples and starter query
//   run({ id, code })      the query on the example datasets
//   submit({ id, code })   the query on every dataset, hidden ones included
// Queries run in a child process (query.mjs) that is killed if it takes too
// long, using the same engine and comparison as the checks (engine.mjs).
import { spawn } from "node:child_process";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import YAML from "yaml";
import { compare } from "./engine.mjs";

const TOOLS = path.dirname(fileURLToPath(import.meta.url));
const SQL = path.dirname(TOOLS);
const PROBLEMS = path.join(SQL, "problems");
const LIMIT_MS = { run: 4000, submit: 8000 };
const STARTER = "-- Write your query here. It runs on SQLite.\nSELECT\n  \n";

export class JudgeError extends Error {
  constructor(status, message) {
    super(message);
    this.name = "JudgeError";
    this.status = status;
  }
}

/* Finding a problem --------------------------------------------------------- */

export function problemDirs() {
  const out = [];
  for (const topic of readdirSync(PROBLEMS, { withFileTypes: true })) {
    if (!topic.isDirectory()) continue;
    for (const pattern of readdirSync(path.join(PROBLEMS, topic.name), { withFileTypes: true })) {
      if (!pattern.isDirectory()) continue;
      for (const slug of readdirSync(path.join(PROBLEMS, topic.name, pattern.name))) {
        const dir = path.join(PROBLEMS, topic.name, pattern.name, slug);
        if (existsSync(path.join(dir, "problem.json"))) out.push(dir);
      }
    }
  }
  return out;
}

function findDir(id) {
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(String(id))) return null;
  return problemDirs().find((d) => path.basename(d) === id) || null;
}

export function load(id) {
  const dir = findDir(id);
  if (!dir) throw new JudgeError(404, "No such problem.");
  const meta = JSON.parse(readFileSync(path.join(dir, "problem.json"), "utf8"));
  const tests = JSON.parse(readFileSync(path.join(dir, "tests.json"), "utf8")).tests;
  return { dir, meta, tests };
}

export const taxonomy = () => YAML.parse(readFileSync(path.join(SQL, "taxonomy.yaml"), "utf8"));

/* The page's view of a problem ------------------------------------------------ */

export function problemView(id) {
  const { meta, tests } = load(id);
  const tax = taxonomy();
  const topic = tax.topics.find((t) => t.id === meta.topic);
  const pattern = topic?.patterns.find((p) => p.id === meta.pattern);
  const examples = tests.filter((t) => t.example);
  return {
    id: meta.id,
    title: meta.title,
    difficulty: meta.difficulty,
    topic: topic && { id: topic.id, name: topic.name },
    pattern: pattern && { id: pattern.id, name: pattern.name },
    statement: meta.statement,
    notes: meta.notes || "",
    tables: meta.tables,
    ordered: meta.ordered,
    examples: examples.map((t) => ({ data: t.data, expected: t.expected, explanation: t.explanation || "" })),
    languages: [{ id: "sql", label: "SQLite", file: "query.sql", available: true, starter: STARTER }],
    solution: false,
  };
}

/* Running a query ------------------------------------------------------------- */

function execute(tables, datasets, sql, limitMs) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, ["--no-warnings", path.join(TOOLS, "query.mjs")], {
      cwd: TOOLS,
      stdio: ["pipe", "pipe", "pipe"],
    });
    let out = "";
    let err = "";
    let timedOut = false;
    const timer = setTimeout(() => {
      timedOut = true;
      child.kill("SIGKILL");
    }, limitMs);
    child.stdout.on("data", (d) => (out += d));
    child.stderr.on("data", (d) => (err += d));
    child.on("close", () => {
      clearTimeout(timer);
      if (timedOut) return resolve({ timedOut: true });
      try {
        resolve({ results: JSON.parse(out) });
      } catch {
        resolve({ crashed: err.trim().split("\n").pop() || "The query runner stopped unexpectedly." });
      }
    });
    child.stdin.end(JSON.stringify({ tables, datasets, sql }));
  });
}

function verdictFor(result, test, ordered) {
  if (result.error) return { verdict: "error", error: result.error };
  const c = compare(result, test.expected, ordered);
  const out = { verdict: c.ok ? "passed" : "wrong", output: { columns: result.columns, rows: result.rows }, ms: result.ms };
  if (!c.ok) out.why = c.why;
  return out;
}

const checkCode = (code) => {
  if (typeof code !== "string" || !code.trim()) throw new JudgeError(400, "Write a query first.");
};

export async function run({ id, code }) {
  checkCode(code);
  const { meta, tests } = load(id);
  const examples = tests.filter((t) => t.example);
  const res = await execute(meta.tables, examples.map((t) => t.data), code, LIMIT_MS.run);
  if (res.timedOut) return { cases: examples.map((t) => ({ verdict: "time", expected: t.expected })) };
  if (res.crashed) throw new JudgeError(500, res.crashed);
  return {
    cases: examples.map((t, i) => ({ ...verdictFor(res.results[i], t, meta.ordered), expected: t.expected })),
  };
}

// A failing dataset is shown in full when it's small enough to read.
const rowsIn = (data) => Object.values(data).reduce((n, rows) => n + rows.length, 0);

export async function submit({ id, code }) {
  checkCode(code);
  const { meta, tests } = load(id);
  if (!tests.length) throw new JudgeError(503, "This problem isn't ready to submit yet.");
  const res = await execute(meta.tables, tests.map((t) => t.data), code, LIMIT_MS.submit);
  const total = tests.length;
  if (res.timedOut) return { verdict: "time", passed: 0, total };
  if (res.crashed) throw new JudgeError(500, res.crashed);

  let passed = 0;
  let failed = null;
  let ms = 0;
  res.results.forEach((r, i) => {
    const v = verdictFor(r, tests[i], meta.ordered);
    ms = Math.max(ms, r.ms || 0);
    if (v.verdict === "passed") return passed++;
    if (failed) return;
    const t = tests[i];
    failed = {
      number: i + 1,
      hidden: !t.example,
      verdict: v.verdict,
      data: rowsIn(t.data) <= 60 ? t.data : null,
      rows: rowsIn(t.data),
      output: v.output,
      expected: t.expected,
      why: v.why,
      error: v.error,
    };
  });
  const verdict = failed ? failed.verdict : "accepted";
  return { verdict, passed, total, ms: failed ? undefined : ms, failed };
}
