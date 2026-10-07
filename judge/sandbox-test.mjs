// Ren judge: check the sandbox on the server, by sending the judge code that
// tries to get out. Every attempt must fail, and the secret must never show up
// in anything the judge answers. Run on the server, after judge/deploy.sh:
//
//   cd /srv/ren/app && sudo -u ren-judge env $(sudo cat /etc/ren-judge.env | xargs) node judge/sandbox-test.mjs
//
// It exits with 1 if anything got through.

import * as judge from "../backend/practice/dsa/tools/judge.mjs";

if (process.env.REN_SANDBOX !== "1") {
  console.error("REN_SANDBOX isn't 1, so nothing is sandboxed. Run it with /etc/ren-judge.env, as the comment at the top says.");
  process.exit(1);
}
const SECRET = process.env.JUDGE_SECRET || "";
const ID = "same-shape-words";
const CASE = [{ args: { words: ["feet", "moon"], pattern: "boot" } }];

// Python that tries something, then prints OK (blocked) or LEAK (it worked).
const py = (body) => `import os, socket, sys
class Solution:
    def countSameShape(self, words, pattern):
${body
  .trim()
  .split("\n")
  .map((l) => `        ${l}`)
  .join("\n")}
        return 0
`;

const tests = [
  {
    name: "Python can't read the judge's secret file",
    lang: "python",
    code: py(`
try:
    open("/etc/ren-judge.env").read(); print("LEAK")
except OSError:
    print("OK")`),
  },
  {
    name: "Python can't read /etc/passwd",
    lang: "python",
    code: py(`
try:
    open("/etc/passwd").read(); print("LEAK")
except OSError:
    print("OK")`),
  },
  {
    name: "Python sees no environment variables from the judge",
    lang: "python",
    code: py(`
print("LEAK" if any(k.startswith("JUDGE") or k == "REN_SANDBOX" for k in os.environ) else "OK")`),
  },
  {
    name: "Python has no network",
    lang: "python",
    code: py(`
try:
    socket.create_connection(("1.1.1.1", 80), timeout=3); print("LEAK")
except OSError:
    print("OK")`),
  },
  {
    name: "Python can't see the hidden tests",
    lang: "python",
    code: py(`
print("LEAK" if os.path.exists("/srv/ren/build/tests") else "OK")`),
  },
  {
    name: "Python can't write into the judge's code",
    lang: "python",
    code: py(`
import glob
try:
    target = glob.glob("/srv/ren/app/backend/practice/dsa/tools/*.mjs")[0]
    open(target, "a").write("#"); print("LEAK")
except (OSError, IndexError):
    print("OK")`),
  },
  {
    name: "Python can't start a program outside its jail",
    lang: "python",
    code: py(`
import subprocess
try:
    out = subprocess.run(["cat", "/etc/ren-judge.env"], capture_output=True, text=True).stdout
    print("LEAK" if out else "OK")
except OSError:
    print("OK")`),
  },
  {
    name: "A fork bomb is contained",
    lang: "python",
    code: py(`
kids = 0
try:
    for _ in range(100000):
        if os.fork() == 0:
            import time; time.sleep(30); os._exit(0)
        kids += 1
    print("LEAK")
except OSError:
    print("OK")`),
    verdicts: ["passed", "wrong", "error", "time"],
    stdoutOptional: true,
  },
  {
    name: "A memory hog is stopped",
    lang: "python",
    code: py(`
try:
    x = bytearray(16 * 1024 ** 3); print("LEAK")
except MemoryError:
    print("OK")`),
  },
  {
    name: "An infinite loop is a time limit, not a hang",
    lang: "python",
    code: py(`
while True:
    pass`),
    verdicts: ["time", "error"],
    stdoutOptional: true,
  },
  {
    name: "C++ can't #include the secret file",
    lang: "cpp",
    code: `#include "/etc/ren-judge.env"\nclass Solution { public: int countSameShape(vector<string>& w, string& p) { return 0; } };`,
    verdicts: ["compile"],
    stdoutOptional: true,
  },
  {
    name: "Java can't run commands outside its jail",
    lang: "java",
    code: `class Solution {
    public int countSameShape(String[] words, String pattern) {
        try {
            Process p = Runtime.getRuntime().exec(new String[] {"cat", "/etc/ren-judge.env"});
            String out = new String(p.getInputStream().readAllBytes());
            System.out.println(out.isEmpty() ? "OK" : "LEAK");
        } catch (Exception e) {
            System.out.println("OK");
        }
        return 0;
    }
}`,
  },
];

let failed = 0;
for (const t of tests) {
  let verdict;
  let text;
  let stdout = "";
  try {
    const out = await judge.run({ id: ID, lang: t.lang, code: t.code, cases: CASE });
    const c = out.cases[0];
    verdict = c.verdict;
    text = JSON.stringify(out);
    stdout = c.stdout || "";
  } catch (err) {
    verdict = `threw ${err.message}`;
    text = String(err.stack);
  }
  const problems = [];
  if (SECRET && text.includes(SECRET)) problems.push("the secret is in the answer");
  if (/LEAK/.test(stdout)) problems.push("the attempt worked");
  if (!t.stdoutOptional && !/OK/.test(stdout)) problems.push(`expected OK in its output, got verdict ${verdict}`);
  if (t.verdicts && !t.verdicts.includes(verdict)) problems.push(`verdict ${verdict}, expected ${t.verdicts.join(" or ")}`);
  console.log(`${problems.length ? "✗" : "✓"} ${t.name}${problems.length ? `: ${problems.join("; ")}` : ""}`);
  if (problems.length) failed++;
}

console.log(failed ? `\n${failed} check(s) failed. Don't point the site at this judge until they pass.` : "\nThe sandbox holds.");
process.exit(failed ? 1 : 0);
