// Spawn a runner, stream its JSON-lines output, and kill it if it goes quiet
// for too long (an infinite loop or a far-too-slow solution).
import { spawn } from "node:child_process";
import { existsSync, lstatSync, readlinkSync } from "node:fs";

/* The sandbox ------------------------------------------------------------------ */

// On the judge server (judge/README.md) REN_SANDBOX=1, and every program that
// runs people's code starts inside bubblewrap: no network, no environment
// variables, its own process tree, the system's /usr read-only, and only the
// folders the call names (`jail.ro` read-only, `jail.rw` writable). Inside,
// prlimit caps memory, processes, CPU time and file size, and timeout caps the
// wall clock. Killing the spawned bwrap kills everything inside it.
// Without REN_SANDBOX (on your own machine) programs run as they always have.
const SANDBOX = process.env.REN_SANDBOX === "1";
const WALL_S = 50;
const LIMITS = ["--as=6442450944", "--nproc=256", "--cpu=50", "--fsize=67108864"];

// /bin, /lib and friends are links into /usr on current Ubuntu; keep them so.
const rootLinks = () =>
  ["/bin", "/sbin", "/lib", "/lib32", "/lib64"].filter(existsSync).flatMap((p) =>
    lstatSync(p).isSymbolicLink() ? ["--symlink", readlinkSync(p), p] : ["--ro-bind", p, p]
  );

function jailed(cmd, args, jail) {
  if (!SANDBOX || !jail) return [cmd, args];
  const etc = ["/etc/alternatives", "/etc/ld.so.cache", "/etc/java-21-openjdk"].filter(existsSync);
  return [
    "bwrap",
    [
      "--unshare-all",
      "--die-with-parent",
      "--new-session",
      "--clearenv",
      "--setenv", "PATH", "/usr/local/bin:/usr/bin:/bin",
      "--setenv", "HOME", "/tmp",
      "--setenv", "LANG", "C.UTF-8",
      "--ro-bind", "/usr", "/usr",
      ...rootLinks(),
      ...etc.flatMap((p) => ["--ro-bind", p, p]),
      "--proc", "/proc",
      "--dev", "/dev",
      "--tmpfs", "/tmp",
      ...(jail.ro ?? []).flatMap((p) => ["--ro-bind", p, p]),
      ...(jail.rw ?? []).flatMap((p) => ["--bind", p, p]),
      ...(jail.cwd ? ["--chdir", jail.cwd] : []),
      "--",
      "timeout", "-s", "KILL", String(WALL_S),
      "prlimit", ...LIMITS, "--",
      cmd, ...args,
    ],
  ];
}

/* Running ---------------------------------------------------------------------- */

/**
 * @param {string} cmd
 * @param {string[]} args
 * @param {object} o
 * @param {string} [o.input]      written to stdin, then stdin is closed
 * @param {number} [o.quietMs]    kill after this long with no output line
 * @param {string} [o.cwd]
 * @param {{ro?: string[], rw?: string[], cwd?: string}} [o.jail]  what the program may see, on the judge server
 * @returns {Promise<{lines: object[], killed: boolean, code: number|null, signal: string|null, stderr: string}>}
 */
export function runLines(cmd, args, { input = "", quietMs = 60_000, cwd, jail } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(...jailed(cmd, args, jail), { cwd, stdio: ["pipe", "pipe", "pipe"] });
    const lines = [];
    let buf = "";
    let stderr = "";
    let killed = false;
    let timer;
    const arm = () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        killed = true;
        child.kill("SIGKILL");
      }, quietMs);
    };
    arm();
    child.stdout.on("data", (chunk) => {
      buf += chunk;
      let i;
      while ((i = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, i).trim();
        buf = buf.slice(i + 1);
        if (!line) continue;
        // Runner messages are objects with an id or a start marker; anything
        // else is a stray print from the solution, kept as its text.
        let msg;
        try {
          msg = parseLossless(line);
        } catch {}
        const own = msg && typeof msg === "object" && !Array.isArray(msg) && ("id" in msg || "start" in msg);
        lines.push(own ? msg : { raw: line });
        arm();
      }
    });
    child.stderr.on("data", (chunk) => (stderr += chunk));
    child.on("error", reject);
    child.on("close", (code, signal) => {
      clearTimeout(timer);
      resolve({ lines, killed, code, signal, stderr: stderr.slice(-4000) });
    });
    child.stdin.on("error", () => {}); // the child may exit before reading everything
    child.stdin.end(input);
  });
}

// JSON.parse, but integers too big for a double come back as BigInt so a long
// answer like 9007199254740993 isn't silently rounded.
export function parseLossless(text) {
  return JSON.parse(text, (_key, value, context) =>
    typeof value === "number" && Number.isInteger(value) && !Number.isSafeInteger(value) && context?.source
      ? BigInt(context.source)
      : value
  );
}

// One-shot command (compilers); resolves with {code, out}.
export function runOnce(cmd, args, { cwd, timeoutMs = 120_000, jail } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(...jailed(cmd, args, jail), { cwd, stdio: ["ignore", "pipe", "pipe"] });
    let out = "";
    child.stdout.on("data", (c) => (out += c));
    child.stderr.on("data", (c) => (out += c));
    const timer = setTimeout(() => child.kill("SIGKILL"), timeoutMs);
    child.on("error", reject);
    child.on("close", (code) => {
      clearTimeout(timer);
      resolve({ code, out: out.slice(-6000) });
    });
  });
}
