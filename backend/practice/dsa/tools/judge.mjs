// Ren DSA judge: what the problem page needs from the bank.
//   problemView(id)              the statement, examples, starter code and languages
//   run({ id, lang, code, cases })   the code on the visible or custom cases
//   submit({ id, lang, code })       the code on every test, hidden ones included
// It reuses the pipeline's runners (lib/langs.mjs) and answer comparison
// (lib/compare.mjs), so a solution is judged exactly as the checks judge it.
import { randomUUID } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import YAML from "yaml";
import { same } from "./lib/compare.mjs";
import { cParams, cReturn } from "./lib/c.mjs";
import { available, handles, LANGS, PY_RUNNER_PATH, runSolution } from "./lib/langs.mjs";
import { parseLossless, runLines } from "./lib/run.mjs";

const TOOLS = path.dirname(fileURLToPath(import.meta.url));
const DSA = path.dirname(TOOLS);
const PROBLEMS = path.join(DSA, "problems");
const BUILD = path.join(DSA, "build");
const config = JSON.parse(readFileSync(path.join(TOOLS, "config.json"), "utf8"));

const ORDER = ["python", "java", "cpp", "c"];
const LABEL = { python: "Python 3", java: "Java", cpp: "C++", c: "C" };
const FILE = { python: "solution.py", java: "Solution.java", cpp: "solution.cpp", c: "solution.c" };

export class JudgeError extends Error {
  constructor(status, message) {
    super(message);
    this.name = "JudgeError";
    this.status = status;
  }
}

/* Finding a problem --------------------------------------------------------- */

function findDir(id) {
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(String(id))) return null;
  for (const topic of readdirSync(PROBLEMS, { withFileTypes: true })) {
    if (!topic.isDirectory()) continue;
    for (const pattern of readdirSync(path.join(PROBLEMS, topic.name), { withFileTypes: true })) {
      if (!pattern.isDirectory()) continue;
      const dir = path.join(PROBLEMS, topic.name, pattern.name, id);
      if (existsSync(path.join(dir, "problem.yaml"))) return dir;
    }
  }
  return null;
}

function load(id) {
  const dir = findDir(id);
  if (!dir) throw new JudgeError(404, "No such problem.");
  const meta = YAML.parse(readFileSync(path.join(dir, "problem.yaml"), "utf8"));
  // The built tests have the generated ones expanded and every expected
  // answer filled in; the source file only has the hand-written ones.
  const built = path.join(BUILD, "tests", `${id}.json`);
  const source = JSON.parse(readFileSync(path.join(dir, "tests.json"), "utf8")).tests;
  const tests = existsSync(built)
    ? parseLossless(readFileSync(built, "utf8")).tests
    : source.filter((t) => t.input && "expected" in t).map((t) => ({ ...t, args: t.input }));
  return { dir, meta, tests };
}

/* Starter code ---------------------------------------------------------------- */

const TYPES = {
  python: { int: "int", long: "int", double: "float", bool: "bool", string: "str", char: "str", ListNode: "Optional[ListNode]", TreeNode: "Optional[TreeNode]", RandomNode: "Optional[RandomNode]", list: (t) => `List[${t}]` },
  java: { int: "int", long: "long", double: "double", bool: "boolean", string: "String", char: "char", ListNode: "ListNode", TreeNode: "TreeNode", RandomNode: "RandomNode", list: (t) => `${t}[]` },
  cpp: { int: "int", long: "long long", double: "double", bool: "bool", string: "string", char: "char", ListNode: "ListNode*", TreeNode: "TreeNode*", RandomNode: "RandomNode*", list: (t) => `vector<${t}>` },
};

function typeIn(lang, type) {
  const map = TYPES[lang];
  if (type.endsWith("[]")) return map.list(typeIn(lang, type.slice(0, -2)));
  return map[type] ?? type;
}

// What ListNode and TreeNode look like, as a comment above the starter (as on LeetCode).
const NODES = {
  python: { ListNode: ["class ListNode:", "    def __init__(self, val=0, next=None):", "        self.val = val", "        self.next = next"], TreeNode: ["class TreeNode:", "    def __init__(self, val=0, left=None, right=None):", "        self.val = val", "        self.left = left", "        self.right = right"], RandomNode: ["class RandomNode:", "    def __init__(self, val=0, next=None, random=None):", "        self.val = val", "        self.next = next", "        self.random = random"] },
  java: { ListNode: ["class ListNode {", "    int val;", "    ListNode next;", "}"], TreeNode: ["class TreeNode {", "    int val;", "    TreeNode left;", "    TreeNode right;", "}"], RandomNode: ["class RandomNode {", "    int val;", "    RandomNode next;", "    RandomNode random;", "}"] },
  cpp: { ListNode: ["struct ListNode {", "    int val;", "    ListNode *next;", "};"], TreeNode: ["struct TreeNode {", "    int val;", "    TreeNode *left;", "    TreeNode *right;", "};"], RandomNode: ["struct RandomNode {", "    int val;", "    RandomNode *next;", "    RandomNode *random;", "};"] },
  c: { ListNode: ["struct ListNode {", "    int val;", "    struct ListNode *next;", "};"], TreeNode: ["struct TreeNode {", "    int val;", "    struct TreeNode *left;", "    struct TreeNode *right;", "};"], RandomNode: ["struct RandomNode {", "    int val;", "    struct RandomNode *next;", "    struct RandomNode *random;", "};"] },
};

function nodeComment(lang, sig) {
  const used = ["ListNode", "TreeNode", "RandomNode"].filter((n) => [sig.returns, ...sig.params.map((p) => p.type)].some((t) => t.replace(/(\[\])+$/, "") === n));
  if (!used.length) return "";
  const lines = used.flatMap((n, i) => [...(i ? [""] : []), ...NODES[lang][n]]);
  if (lang === "python") return `# Given:\n${lines.map((l) => `# ${l}`).join("\n")}\n\n`;
  return `/* Given:\n${lines.map((l) => ` * ${l}`).join("\n")}\n */\n`;
}

// A design problem's starter: the class with its constructor and every method.
function designStarter(lang, design) {
  const t = (type) => typeIn(lang, type);
  const ms = design.methods;
  const ctor = design.constructor.params;
  if (lang === "python") {
    const sig = (params) => ["self", ...params.map((p) => `${p.name}: ${t(p.type)}`)].join(", ");
    const ret = (type) => (type === "void" ? "None" : t(type));
    const body = [`    def __init__(${sig(ctor)}):\n        pass`, ...ms.map((m) => `    def ${m.name}(${sig(m.params)}) -> ${ret(m.returns)}:\n        pass`)];
    return `class ${design.class}:\n\n${body.join("\n\n")}\n`;
  }
  if (lang === "java") {
    const sig = (params) => params.map((p) => `${t(p.type)} ${p.name}`).join(", ");
    const ret = (type) => (type === "void" ? "void" : t(type));
    const body = [`    public ${design.class}(${sig(ctor)}) {\n        \n    }`, ...ms.map((m) => `    public ${ret(m.returns)} ${m.name}(${sig(m.params)}) {\n        \n    }`)];
    return `class ${design.class} {\n\n${body.join("\n\n")}\n}`;
  }
  if (lang === "cpp") {
    const ref = (type) => (type.endsWith("[]") || type === "string" ? "&" : "");
    const sig = (params) => params.map((p) => `${t(p.type)}${ref(p.type)} ${p.name}`).join(", ");
    const ret = (type) => (type === "void" ? "void" : t(type));
    const body = [`    ${design.class}(${sig(ctor)}) {\n        \n    }`, ...ms.map((m) => `    ${ret(m.returns)} ${m.name}(${sig(m.params)}) {\n        \n    }`)];
    return `class ${design.class} {\npublic:\n${body.join("\n\n")}\n};`;
  }
  return "";
}

function starter(lang, meta) {
  if (!handles(lang, meta)) return "";
  if (meta.kind === "design") return designStarter(lang, meta.design);
  if (meta.kind !== "function") return "";
  const sig = meta.signature;
  const { function: fn, params, returns } = sig;
  const t = (type) => typeIn(lang, type);
  const given = nodeComment(lang, sig);
  if (lang === "python") {
    const args = params.map((p) => `${p.name}: ${t(p.type)}`).join(", ");
    return `${given}class Solution:\n    def ${fn}(self, ${args}) -> ${t(returns)}:\n        `;
  }
  if (lang === "java") {
    const args = params.map((p) => `${t(p.type)} ${p.name}`).join(", ");
    return `${given}class Solution {\n    public ${t(returns)} ${fn}(${args}) {\n        \n    }\n}`;
  }
  if (lang === "cpp") {
    // Containers and strings by reference, as LeetCode does.
    const ref = (type) => (type.endsWith("[]") || type === "string" ? "&" : "");
    const args = params.map((p) => `${t(p.type)}${ref(p.type)} ${p.name}`).join(", ");
    return `${given}class Solution {\npublic:\n    ${t(returns)} ${fn}(${args}) {\n        \n    }\n};`;
  }
  // C: arrays come with their sizes; an array answer reports its size.
  const notes = [];
  if (returns.endsWith("[]")) notes.push("Set *returnSize to the answer's length.");
  if (returns.endsWith("[][]")) notes.push("Set (*returnColumnSizes)[i] to each row's length.");
  if (returns.endsWith("[]") || returns === "string") notes.push("Return memory from malloc; the caller frees it.");
  const note = notes.length ? `/*\n${notes.map((n) => ` * ${n}`).join("\n")}\n */\n` : "";
  return `${given}${note}${cReturn(sig)} ${fn}(${cParams(sig).join(", ")}) {\n    \n}`;
}

/* The page's view of a problem ---------------------------------------------------- */

export async function problemView(id) {
  const { meta, tests, dir } = load(id);
  const taxonomy = YAML.parse(readFileSync(path.join(DSA, "taxonomy.yaml"), "utf8"));
  const topic = taxonomy.topics.find((t) => t.id === meta.topic);
  const pattern = topic?.patterns.find((p) => p.id === meta.pattern);
  const [intro, rest = ""] = readFileSync(path.join(dir, "statement.md"), "utf8").split("{{examples}}");

  const languages = await Promise.all(
    ORDER.map(async (lang) => ({
      id: lang,
      label: LABEL[lang],
      file: FILE[lang],
      available: handles(lang, meta) && (await available(lang)),
      starter: starter(lang, meta),
    }))
  );

  const visible = tests.filter((t) => t.visible);
  // Optional drawing hints and a step-by-step walkthrough, written per problem.
  const visualFile = path.join(dir, "visual.json");
  const visual = existsSync(visualFile) ? JSON.parse(readFileSync(visualFile, "utf8")) : null;
  return {
    // A written-out solution (solution.json) the page fetches only when asked.
    solution: existsSync(path.join(dir, "solution.json")),
    id: meta.id,
    title: meta.title,
    difficulty: meta.difficulty,
    kind: meta.kind,
    topic: topic && { id: topic.id, name: topic.name },
    // The pattern's lesson (tools/lessons), when it's written: the page links to it.
    pattern: pattern && {
      id: pattern.id,
      name: pattern.name,
      lesson: existsSync(path.join(DSA, "lessons", meta.topic, `${pattern.id}.json`)),
    },
    params: paramsOf(meta),
    returns: meta.kind === "function" ? meta.signature.returns : null,
    visual,
    checker: meta.checker,
    statement: intro.trim(),
    notes: rest.trim(),
    examples: visible.filter((t) => t.example).map((t) => ({ args: t.args, expected: t.expected, explanation: t.explanation || "" })),
    cases: visible.map((t) => ({ args: t.args })),
    languages,
  };
}

// The full solution: every approach explained, with code in each language.
// Written ahead of time (tools/solutions), so showing it costs nothing.
export function solutionView(id) {
  const dir = findDir(id);
  const file = dir && path.join(dir, "solution.json");
  if (!file || !existsSync(file)) throw new JudgeError(404, "This problem's solution isn't written yet.");
  return JSON.parse(readFileSync(file, "utf8"));
}

/* Checking custom input -------------------------------------------------------------- */

// A design problem takes one argument, `calls`: [["ClassName", ...args], ["method", ...args], ...].
const paramsOf = (meta) => (meta.kind === "design" ? [{ name: "calls", type: "calls" }] : meta.signature.params);

// Why a list of design calls is malformed, or null when it's fine.
function badCalls(calls, design) {
  if (!Array.isArray(calls) || !calls.length) return "calls should be a list of calls, starting with the constructor.";
  if (!calls.every((c) => Array.isArray(c) && typeof c[0] === "string")) return 'each call should look like ["name", arguments...].';
  const [ctor, ...rest] = calls;
  const argsOk = (params, args, what) =>
    args.length !== params.length
      ? `${what} takes ${params.length} argument${params.length === 1 ? "" : "s"}.`
      : params.map((p, i) => (fits(args[i], p.type) ? null : `${what}: ${p.name} should be ${describe(p.type)}.`)).find(Boolean) ?? null;
  if (ctor[0] !== design.class) return `The first call should create ${design.class}.`;
  const ctorBad = argsOk(design.constructor.params, ctor.slice(1), design.class);
  if (ctorBad) return ctorBad;
  for (const [name, ...args] of rest) {
    const m = design.methods.find((x) => x.name === name);
    if (!m) return `${design.class} has no method ${name}.`;
    const bad = argsOk(m.params, args, name);
    if (bad) return bad;
  }
  return null;
}

const INT32 = 2 ** 31;
function fits(value, type) {
  if (type.endsWith("[]")) return Array.isArray(value) && value.every((v) => fits(v, type.slice(0, -2)));
  switch (type) {
    case "int":
      return Number.isInteger(value) && value >= -INT32 && value < INT32;
    case "long":
      return Number.isSafeInteger(value);
    case "double":
      return typeof value === "number" && Number.isFinite(value);
    case "bool":
      return typeof value === "boolean";
    case "string":
      return typeof value === "string";
    case "char":
      return typeof value === "string" && value.length === 1;
    case "ListNode":
      // A list with a cycle is {"values": [...], "cycle_at": index}; one that joins the
      // list before it is {"values": [...], "join_at": index}.
      if (value && !Array.isArray(value) && typeof value === "object") {
        return fits(value.values, "int[]") && Number.isInteger(value.cycle_at ?? -1) && Number.isInteger(value.join_at ?? 0);
      }
      return Array.isArray(value) && value.every((v) => Number.isInteger(v));
    case "TreeNode":
      return Array.isArray(value) && value.every((v) => v === null || Number.isInteger(v));
    case "RandomNode":
      // [[value, index of the random target or null], ...]
      return Array.isArray(value) && value.every((p) => Array.isArray(p) && p.length === 2 && Number.isInteger(p[0]) && (p[1] === null || (Number.isInteger(p[1]) && p[1] >= 0 && p[1] < value.length)));
    default:
      return false;
  }
}

const TYPE_WORDS = { int: "an integer", long: "an integer", double: "a number", bool: "true or false", string: "a string in quotes", char: "one character in quotes" };
const describe = (type) =>
  type.endsWith("[]") ? `a list of ${describe(type.slice(0, -2)).replace(/^an? /, "")}s` : TYPE_WORDS[type] ?? `a ${type}`;

const jsonl = (items) => items.map((x) => exactJson(x)).join("\n") + "\n";

// Each case must have every parameter, of the right type, within the
// problem's constraints (its validator.py). Returns a message per bad case.
async function checkCases(meta, dir, cases) {
  const problems = new Map();
  cases.forEach((c, i) => {
    if (meta.kind === "design") {
      const bad = badCalls(c.args.calls, meta.design);
      if (bad) problems.set(i, bad);
      return;
    }
    for (const p of meta.signature.params) {
      if (!(p.name in c.args)) problems.set(i, `${p.name} is missing.`);
      else if (!fits(c.args[p.name], p.type)) problems.set(i, `${p.name} should be ${describe(p.type)}.`);
    }
  });
  const typed = cases.map((c, i) => ({ id: `c${i}`, args: c.args })).filter((_, i) => !problems.has(i));
  if (typed.length) {
    const { lines } = await runLines("python3", [PY_RUNNER_PATH, "validate", path.join(dir, "validator.py")], {
      input: jsonl(typed),
      quietMs: 10_000,
    });
    for (const v of lines.filter((l) => l.id !== undefined && !l.ok)) {
      problems.set(Number(v.id.slice(1)), `Outside the constraints: ${v.msg}`);
    }
  }
  return problems;
}

/* Running code ---------------------------------------------------------------------- */

const MAX_CODE = 100_000;
const MAX_CASES = 8;
const MAX_CASE_CHARS = 20_000;

function prepare({ id, lang, code }) {
  const { dir, meta, tests } = load(id);
  if (meta.kind !== "function" && meta.kind !== "design") throw new JudgeError(400, "This problem can't be run here yet.");
  if (!LANGS[lang]) throw new JudgeError(400, "Pick a language.");
  if (!handles(lang, meta)) throw new JudgeError(400, `${LABEL[lang]} can't take this problem. Pick another language.`);
  if (typeof code !== "string" || !code.trim()) throw new JudgeError(400, "Write some code first.");
  if (code.length > MAX_CODE) throw new JudgeError(400, "That's too much code for one solution.");
  return { dir, meta, tests, limitMs: meta.limits.time_ms * config.timeMultipliers[lang] };
}

// The code goes in its own folder for the run, and the folder goes after.
async function withSolution(lang, code, fn) {
  if (!(await available(lang))) throw new JudgeError(400, `${LABEL[lang]} can't run on this server yet.`);
  const dir = path.join(os.tmpdir(), `ren-run-${randomUUID()}`);
  mkdirSync(dir, { recursive: true });
  const file = path.join(dir, FILE[lang]);
  writeFileSync(file, code);
  try {
    return await fn(file);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

// Whether each answer is right. Most problems compare with the expected
// answer (exactly, in any order, or within a tolerance); a problem that
// accepts several answers has its own checker.py, run once for all tests.
async function correct(meta, dir, items) {
  if (meta.checker.type !== "custom") return items.map((it) => same(meta.checker, it.actual, it.expected));
  if (!items.length) return [];
  const { lines } = await runLines("python3", [PY_RUNNER_PATH, "check", path.join(dir, "checker.py")], {
    input: jsonl(items.map((it, i) => ({ id: `t${i}`, args: it.args, expected: it.expected, actual: it.actual }))),
    quietMs: 30_000,
  });
  const ok = new Map(lines.filter((l) => l.id !== undefined).map((l) => [l.id, l.ok === true]));
  return items.map((_, i) => ok.get(`t${i}`) === true);
}

// One result per test: passed, and why not when it didn't.
async function judge(meta, dir, limitMs, tests, runs) {
  const answered = [];
  tests.forEach((t, i) => {
    const r = runs[i] ?? {};
    const timedOut = r.tle || (r.ms != null && r.ms > limitMs);
    if (!r.notRun && !timedOut && !r.error) answered.push(i);
  });
  const verdicts = await correct(meta, dir, answered.map((i) => ({ args: tests[i].args, expected: tests[i].expected, actual: runs[i].out })));
  const right = new Map(answered.map((i, k) => [i, verdicts[k]]));
  return tests.map((t, i) => {
    const r = runs[i] ?? {};
    const base = { ms: r.ms == null ? null : Math.round(r.ms * 10) / 10, stdout: r.stdout || "" };
    if (r.notRun) return { ...base, verdict: "skipped" };
    if (r.tle || (r.ms != null && r.ms > limitMs)) return { ...base, verdict: "time", error: `Took longer than ${limitMs} ms.` };
    if (r.error?.startsWith("compile error")) {
      const error = r.error.replace(/^compile error: /, "").replace(/\.\/(solution\.(?:cpp|c))/g, "$1");
      return { ...base, verdict: "compile", error };
    }
    if (r.error) return { ...base, verdict: "error", error: r.error };
    return { ...base, verdict: right.get(i) ? "passed" : "wrong", output: r.out };
  });
}

const safe = (v) => JSON.parse(JSON.stringify(v, (_k, x) => (typeof x === "bigint" ? Number(x) : x)));

// JSON text with every integer exact, even past 2^53 (answers can be longs).
const exactJson = (v) =>
  v === undefined ? undefined : JSON.stringify(v, (_k, x) => (typeof x === "bigint" ? `\u0000${x}` : x)).replace(/"\\u0000(-?\d+)"/g, "$1");

export async function run({ id, lang, code, cases }) {
  const { dir, meta, tests, limitMs } = prepare({ id, lang, code });
  if (!Array.isArray(cases) || !cases.length) throw new JudgeError(400, "Add a test case first.");
  if (cases.length > MAX_CASES) throw new JudgeError(400, `Run at most ${MAX_CASES} cases at a time.`);
  if (cases.some((c) => !c?.args || typeof c.args !== "object" || exactJson(c.args).length > MAX_CASE_CHARS)) {
    throw new JudgeError(400, "One of the cases is too big to run here. Submit to try the large tests.");
  }

  const bad = await checkCases(meta, dir, cases);
  if (bad.size) {
    return { invalid: [...bad].map(([index, message]) => ({ index, message })) };
  }

  // Expected answers: the stored one for a visible case, else the reference's.
  const key = (args) => exactJson(args);
  const known = new Map(tests.filter((t) => t.visible).map((t) => [key(t.args), t.expected]));
  const list = cases.map((c, i) => ({ id: `case-${i + 1}`, args: c.args, expected: known.get(key(c.args)) }));
  const unknown = list.filter((c) => c.expected === undefined);
  if (unknown.length) {
    const refs = await runSolution({ lang: "python", file: path.join(dir, "reference.py"), meta, tests: unknown, limitMs: 10_000, buildDir: BUILD });
    unknown.forEach((c, i) => (c.expected = refs[i].out));
  }

  const runs = await withSolution(lang, code, (file) => runSolution({ lang, file, meta, tests: list, limitMs, buildDir: BUILD }));
  const results = await judge(meta, dir, limitMs, list, runs);
  return safe({
    limitMs,
    // Answers go to the page as exact JSON text.
    cases: list.map((c, i) => ({ args: c.args, ...results[i], expected: exactJson(c.expected), output: exactJson(results[i].output) })),
  });
}

export async function submit({ id, lang, code }) {
  const { dir, meta, tests, limitMs } = prepare({ id, lang, code });
  // No tests means the problem was never built; never call that "Accepted".
  if (!tests.length || !tests.some((t) => !t.visible)) throw new JudgeError(503, "This problem isn't ready to submit yet.");
  const runs = await withSolution(lang, code, (file) => runSolution({ lang, file, meta, tests, limitMs, buildDir: BUILD }));
  const results = await judge(meta, dir, limitMs, tests, runs);
  const passed = results.filter((r) => r.verdict === "passed").length;
  const failedAt = results.findIndex((r) => r.verdict !== "passed");
  const times = results.map((r) => r.ms).filter((ms) => ms != null);

  const out = {
    limitMs,
    total: tests.length,
    passed,
    verdict: failedAt < 0 ? "accepted" : results[failedAt].verdict,
    ms: times.length ? Math.max(...times) : null,
  };
  if (failedAt >= 0) {
    const t = tests[failedAt];
    const r = results[failedAt];
    // A big hidden input is shortened for the page; it's still the real test.
    const clip = (v) => {
      const s = exactJson(v);
      return s === undefined ? undefined : s.length > 600 ? `${s.slice(0, 600)}…` : s;
    };
    out.failed = {
      number: failedAt + 1,
      hidden: !t.visible,
      args: Object.fromEntries(Object.entries(t.args).map(([k, v]) => [k, clip(v)])),
      expected: clip(t.expected),
      output: r.output === undefined ? undefined : clip(r.output),
      error: r.error,
      stdout: r.stdout,
    };
  }
  return safe(out);
}

// Every test for one solution, judged one by one (tools/check-solutions.mjs).
// `maxChars` keeps only the tests whose input is at most that long, for
// approaches that are meant to be too slow for the big ones.
export async function check({ id, lang, code, maxChars, limitMs: override }) {
  const { dir, meta, tests, limitMs } = prepare({ id, lang, code });
  const list = maxChars ? tests.filter((t) => exactJson(t.args).length <= maxChars) : tests;
  const limit = override ?? limitMs;
  const runs = await withSolution(lang, code, (file) => runSolution({ lang, file, meta, tests: list, limitMs: limit, buildDir: BUILD }));
  const results = await judge(meta, dir, limit, list, runs);
  return { total: list.length, results: results.map((r, i) => ({ ...r, args: list[i].args, expected: list[i].expected })) };
}
