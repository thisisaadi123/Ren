// Run a solution in any supported language against a list of tests.
// Every language answers the same way: one result per test, in order.
// Python runs through runners/py_runner.py; C++, Java and C are compiled with
// a generated harness (lib/cpp.mjs, lib/java.mjs, lib/c.mjs), cached by hash.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { harness as cHarness, supported as cSupported } from "./c.mjs";
import { BITS_STDCXX, harness as cppHarness } from "./cpp.mjs";
import { JAVA_IMPORTS, harness as javaHarness } from "./java.mjs";
import { runLines, runOnce } from "./run.mjs";
import { encodeTests } from "./tokens.mjs";

const TOOLS = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const PY_RUNNER = path.join(TOOLS, "runners", "py_runner.py");

export const LANGS = {
  python: { file: "reference.py", label: "Python" },
  java: { file: "solutions/Reference.java", label: "Java" },
  cpp: { file: "solutions/reference.cpp", label: "C++" },
  c: { file: "solutions/reference.c", label: "C" },
};

// The JDK: JAVA_HOME if set, else Homebrew's, else whatever is on PATH.
// (macOS ships a /usr/bin/javac stub that fails when no JDK is installed.)
const JAVA_BINS = [
  process.env.JAVA_HOME && path.join(process.env.JAVA_HOME, "bin"),
  "/opt/homebrew/opt/openjdk@21/bin",
  "/opt/homebrew/opt/openjdk/bin",
  "/usr/local/opt/openjdk@21/bin",
  "",
].filter((d) => d !== undefined && d !== null && d !== false);
let javaBin;
async function findJava() {
  if (javaBin !== undefined) return javaBin;
  for (const dir of JAVA_BINS) {
    const javac = dir ? path.join(dir, "javac") : "javac";
    if (dir && !existsSync(javac)) continue;
    const { code } = await runOnce(javac, ["-version"], { timeoutMs: 20_000 }).catch(() => ({ code: 1 }));
    if (code === 0) return (javaBin = dir);
  }
  return (javaBin = null);
}
const javaTool = (name) => (javaBin ? path.join(javaBin, name) : name);

// Toolchains that can run here.
const probes = {
  python: () => runOnce("python3", ["--version"], { timeoutMs: 10_000 }),
  cpp: () => runOnce("clang++", ["--version"], { timeoutMs: 10_000 }),
  c: () => runOnce("clang", ["--version"], { timeoutMs: 10_000 }),
  java: async () => ({ code: (await findJava()) === null ? 1 : 0 }),
};
const availability = new Map();
export async function available(lang) {
  if (!availability.has(lang)) {
    const probe = probes[lang];
    availability.set(lang, probe ? (await probe().catch(() => ({ code: 1 }))).code === 0 : false);
  }
  return availability.get(lang);
}

export const whyUnavailable = (lang) => `${LANGS[lang]?.label ?? lang} toolchain not found`;

// Whether a language can take this problem at all (C has no classes).
export const handles = (lang, meta) => (lang === "c" ? cSupported(meta) : true);

/**
 * Run `file` in `lang` on `tests` ([{id, args}]). `meta` is the problem.yaml (its kind and signature).
 * @returns {Promise<Array<{id, out?, ms?, error?, tle?, notRun?, stdout?}>>} one entry per test, in order
 */
export async function runSolution({ lang, file, meta, tests, limitMs, buildDir }) {
  // Compiled languages get room for starting up (the JVM takes a moment).
  const quietMs = limitMs * 2 + (lang === "java" ? 4000 : 1500);
  let proc;
  if (lang === "python") {
    const input = tests.map((t) => JSON.stringify({ id: t.id, args: t.args })).join("\n") + "\n";
    proc = await runLines("python3", [PY_RUNNER, "solve", file, specOf(meta)], { input, quietMs });
  } else if (lang === "cpp" || lang === "c" || lang === "java") {
    if (!handles(lang, meta)) return tests.map((t) => ({ id: t.id, error: `${LANGS[lang].label} can't run this kind of problem` }));
    const built = await BUILDERS[lang]({ file, meta, buildDir });
    if (built.error) return tests.map((t) => ({ id: t.id, error: built.error }));
    proc = await runLines(built.cmd, built.args, { input: encodeTests(tests, meta), quietMs });
  } else {
    throw new Error(whyUnavailable(lang));
  }
  return collect(tests, proc);
}

// Why a compiled solution died, in words.
const SIGNALS = {
  SIGSEGV: "segmentation fault (a bad pointer, or an index out of range)",
  SIGBUS: "bus error (a bad pointer)",
  SIGABRT: "aborted",
  SIGFPE: "arithmetic error (division by zero?)",
  SIGILL: "illegal instruction",
};

function collect(tests, { lines, killed, signal, stderr }) {
  const byId = new Map(lines.filter((l) => l.id !== undefined).map((l) => [l.id, l]));
  // What the solution printed, per test: the lines between its start marker and its result.
  const printed = new Map();
  let current;
  for (const l of lines) {
    if (l.start !== undefined) current = l.start;
    else if (l.raw !== undefined && current !== undefined) printed.set(current, [...(printed.get(current) ?? []), l.raw]);
  }
  for (const [id, out] of printed) if (byId.has(id)) byId.get(id).stdout = out.join("\n");
  const results = [];
  let stopped = false;
  for (const t of tests) {
    const r = byId.get(t.id);
    if (r) {
      results.push(r);
    } else if (!stopped) {
      stopped = true;
      results.push(
        killed
          ? { id: t.id, tle: true, error: "killed: far over the time limit" }
          : {
              id: t.id,
              error: `crashed${SIGNALS[signal] ? `: ${SIGNALS[signal]}` : ""}${stderr.trim() ? `: ${stderr.trim().split("\n").slice(-3).join(" | ")}` : ""}`,
            }
      );
    } else {
      results.push({ id: t.id, notRun: true });
    }
  }
  return results;
}

// The signature the runners need: {"kind": "function", function, params, returns} or {"kind": "design", class, constructor, methods}.
const specOf = (meta) => JSON.stringify(meta.kind === "design" ? { kind: "design", ...meta.design } : { kind: "function", ...meta.signature });

// Compile once per (solution, harness) pair; later runs reuse the binary.
function buildDirFor(buildDir, lang, ...parts) {
  const hash = createHash("sha256");
  parts.forEach((p) => hash.update(p));
  return path.join(buildDir, lang, hash.digest("hex").slice(0, 16));
}

const compileError = (out) =>
  `compile error: ${out.trim().split("\n").filter((l) => !/^In file included from/.test(l)).slice(0, 14).join("\n")}`;

const BUILDERS = {
  async cpp({ file, meta, buildDir }) {
    const source = readFileSync(file, "utf8");
    const main = cppHarness(meta);
    const dir = buildDirFor(buildDir, "cpp", source, main);
    const bin = path.join(dir, "run");
    if (existsSync(bin)) return { cmd: bin, args: [] };
    mkdirSync(path.join(dir, "include", "bits"), { recursive: true });
    writeFileSync(path.join(dir, "include", "bits", "stdc++.h"), BITS_STDCXX);
    writeFileSync(path.join(dir, "solution.cpp"), source);
    writeFileSync(path.join(dir, "main.cpp"), main);
    const { code, out } = await runOnce("clang++", ["-std=c++17", "-O2", "-I", path.join(dir, "include"), "-o", bin, "main.cpp"], { cwd: dir });
    return code === 0 ? { cmd: bin, args: [] } : { error: compileError(out) };
  },

  async c({ file, meta, buildDir }) {
    const source = readFileSync(file, "utf8");
    const main = cHarness(meta);
    const dir = buildDirFor(buildDir, "c", source, main);
    const bin = path.join(dir, "run");
    if (existsSync(bin)) return { cmd: bin, args: [] };
    mkdirSync(dir, { recursive: true });
    writeFileSync(path.join(dir, "solution.c"), source);
    writeFileSync(path.join(dir, "main.c"), main);
    const { code, out } = await runOnce("clang", ["-std=c11", "-O2", "-o", bin, "main.c", "-lm"], { cwd: dir });
    return code === 0 ? { cmd: bin, args: [] } : { error: compileError(out) };
  },

  async java({ file, meta, buildDir }) {
    await findJava();
    const source = readFileSync(file, "utf8");
    const main = javaHarness(meta);
    const dir = buildDirFor(buildDir, "java", source, main);
    const run = { cmd: javaTool("java"), args: ["-XX:+UseSerialGC", "-cp", dir, "Main"] };
    if (existsSync(path.join(dir, "Main.class"))) return run;
    mkdirSync(dir, { recursive: true });
    // The imports go on the solution's first line, so its line numbers stay put.
    writeFileSync(path.join(dir, "Solution.java"), JAVA_IMPORTS + source);
    writeFileSync(path.join(dir, "Main.java"), main);
    const { code, out } = await runOnce(javaTool("javac"), ["-encoding", "UTF-8", "-nowarn", "-d", dir, "Main.java", "Solution.java"], { cwd: dir });
    return code === 0 ? run : { error: compileError(out) };
  },
};

export const PY_RUNNER_PATH = PY_RUNNER;
