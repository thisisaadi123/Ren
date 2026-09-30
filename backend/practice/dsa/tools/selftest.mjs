#!/usr/bin/env node
// Proves the pipeline catches real mistakes: copies a known-good problem into a
// temporary bank, plants one bug at a time, and checks that check.mjs fails at
// the right check (and not before it). See ../pipeline.md, "Benchmark".
//
//   npm run test:dsa
import { spawnSync } from "node:child_process";
import { cpSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const TOOLS = path.dirname(fileURLToPath(import.meta.url));
const DSA = path.dirname(TOOLS);
const REL = "problems/binary-search/search-on-answer/print-shop-daily-limit";

const edit = (file, fn) => writeFileSync(file, fn(readFileSync(file, "utf8")));
const editTests = (dir, fn) =>
  edit(path.join(dir, "tests.json"), (s) => {
    const doc = JSON.parse(s);
    fn(doc.tests);
    return JSON.stringify(doc, null, 2);
  });

// [name, check number that must fail, how to plant the bug]
const CASES = [
  ["clean copy passes", null, () => {}],
  ["statement without {{examples}}", 1, (d) => edit(path.join(d, "statement.md"), (s) => s.replace("{{examples}}", ""))],
  ["pattern from another topic", 1, (d) => edit(path.join(d, "problem.yaml"), (s) => s.replace("pattern: search-on-answer", "pattern: top-k"))],
  ["input breaks the constraints", 2, (d) => editTests(d, (t) => (t.find((x) => x.id === "edge-single").input.pages = [501]))],
  ["wrong stored answer", 3, (d) => editTests(d, (t) => (t.find((x) => x.id === "ex1").expected = 7))],
  ["reference with a subtle bug", 3, (d) => edit(path.join(d, "reference.py"), (s) => s.replace("if days_needed(mid) <= days:", "if days_needed(mid) < days:"))],
  ["reference far too slow", 3, (d) => cpSync(path.join(d, "wrong", "too_slow.py"), path.join(d, "reference.py"))],
  [
    "tests too weak for a wrong solution",
    4,
    (d) =>
      writeFileSync(
        path.join(d, "wrong", "sneaky.py"),
        [
          "import importlib.util, os",
          "_s = importlib.util.spec_from_file_location('r', os.path.join(os.path.dirname(__file__), '..', 'reference.py'))",
          "_r = importlib.util.module_from_spec(_s); _s.loader.exec_module(_r)",
          "class Solution:",
          "    # Wrong only for exactly 3 jobs: no test has 3 jobs, so nothing catches it.",
          "    def minDailyLimit(self, pages, days):",
          "        answer = _r.Solution().minDailyLimit(pages, days)",
          "        return answer + 1 if len(pages) == 3 else answer",
          "",
        ].join("\n")
      ),
  ],
  ["Java solution returns a wrong answer", 5, (d) => edit(path.join(d, "solutions", "Reference.java"), (s) => s.replace("return lo;", "return lo + (pages.length == 1 ? 1 : 0);"))],
  ["C solution returns a wrong answer", 5, (d) => edit(path.join(d, "solutions", "reference.c"), (s) => s.replace("return lo;", "return lo + (pagesSize == 1 ? 1 : 0);"))],
  ["C++ solution doesn't compile", 5, (d) => edit(path.join(d, "solutions", "reference.cpp"), (s) => s.replace("return lo;", "return lo"))],
  ["published without a review", 6, (d) => edit(path.join(d, "problem.yaml"), (s) => s.replace("status: draft", "status: published"))],
];

let failures = 0;
for (const [name, mustFail, plant] of CASES) {
  const root = mkdtempSync(path.join(tmpdir(), "ren-dsa-selftest-"));
  try {
    for (const f of ["taxonomy.yaml", "problem.schema.json"]) cpSync(path.join(DSA, f), path.join(root, f));
    cpSync(path.join(DSA, REL), path.join(root, REL), { recursive: true });
    plant(path.join(root, REL));
    const run = spawnSync(process.execPath, [path.join(TOOLS, "check.mjs")], {
      env: { ...process.env, REN_DSA_ROOT: root },
      encoding: "utf8",
    });
    // Which numbered checks failed ("  ✗ 3 Reference vs brute force", "  ✗ 6–7 …")
    const failed = [...run.stdout.matchAll(/^ {2}✗ (\d+)/gm)].map((m) => Number(m[1]));
    const ok = mustFail === null ? run.status === 0 && !failed.length : run.status === 1 && failed[0] === mustFail;
    console.log(`${ok ? "✓" : "✗"} ${name}: ${mustFail === null ? "passes" : `fails at check ${mustFail}`}${ok ? "" : ` (got exit ${run.status}, failed checks: ${failed.join(", ") || "none"})`}`);
    if (!ok) {
      failures++;
      console.log(run.stdout.split("\n").map((l) => `    ${l}`).join("\n"));
    }
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}
console.log(`\n${CASES.length - failures} of ${CASES.length} self-test cases behave as expected.`);
process.exit(failures ? 1 : 0);
