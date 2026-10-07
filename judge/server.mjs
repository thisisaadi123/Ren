// Ren judge server: runs DSA Run and Submit for the hosted site.
// The website (server.js on Vercel) sends it what the person typed; it judges
// it with the same judge as `npm start` (backend/practice/dsa/tools/judge.mjs)
// and answers with the same JSON. Set up and deployed as judge/README.md says.
//
//   POST /run     { userId, id, lang, code, cases }  -> what judge.run returns
//   POST /submit  { userId, id, lang, code }         -> what judge.submit returns
//   GET  /languages                                  -> { languages: ["python", ...] }
//   GET  /health                                     -> { ok, running, waiting }
//
// Every request but /health needs `Authorization: Bearer $JUDGE_SECRET`.
// With REN_SANDBOX=1 every program that runs people's code is sandboxed
// (tools/lib/run.mjs).

import crypto from "node:crypto";
import { readdirSync, rmSync, statSync } from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import * as judge from "../backend/practice/dsa/tools/judge.mjs";
import { available, LANGS } from "../backend/practice/dsa/tools/lib/langs.mjs";

const PORT = Number(process.env.PORT) || 8080;
const HOST = process.env.HOST || "127.0.0.1"; // Caddy, in front, handles HTTPS
const SECRET = process.env.JUDGE_SECRET || "";
if (SECRET.length < 32) {
  console.error("Set JUDGE_SECRET to a random string of at least 32 characters.");
  process.exit(1);
}

/* Limits ------------------------------------------------------------------- */

// Runs at once (one core stays free for this server), and how many may wait.
const SLOTS = Number(process.env.JUDGE_SLOTS) || Math.max(1, os.cpus().length - 1);
const MAX_WAITING = 20;
// Per person: one run at a time, and at most RUNS_PER_WINDOW in WINDOW_MS.
const RUNS_PER_WINDOW = 60;
const WINDOW_MS = 10 * 60_000;

let active = 0;
const waiting = [];
const busyUsers = new Set();
const recentRuns = new Map(); // user id -> times of their runs in the window

// A finished run hands its slot straight to the next one waiting.
async function inTurn(fn) {
  if (active < SLOTS) active++;
  else {
    if (waiting.length >= MAX_WAITING) throw Object.assign(new Error("Busy, try again in a moment."), { status: 503 });
    await new Promise((resolve) => waiting.push(resolve));
  }
  try {
    return await fn();
  } finally {
    const next = waiting.shift();
    if (next) next();
    else active--;
  }
}

function tooManyRuns(userId) {
  const now = Date.now();
  const times = (recentRuns.get(userId) || []).filter((t) => now - t < WINDOW_MS);
  const over = times.length >= RUNS_PER_WINDOW;
  if (!over) times.push(now);
  recentRuns.set(userId, times);
  return over;
}

/* HTTP helpers ------------------------------------------------------------- */

function send(res, status, body) {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" });
  res.end(JSON.stringify(body));
}

function authorized(req) {
  const given = Buffer.from(String(req.headers.authorization || ""));
  const expected = Buffer.from(`Bearer ${SECRET}`);
  return given.length === expected.length && crypto.timingSafeEqual(given, expected);
}

function readJson(req, limit = 250_000) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on("data", (c) => {
      size += c.length;
      if (size > limit) {
        reject(Object.assign(new Error("Body too large"), { status: 413 }));
        req.destroy();
      } else chunks.push(c);
    });
    req.on("end", () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}"));
      } catch {
        reject(Object.assign(new Error("Invalid JSON"), { status: 400 }));
      }
    });
  });
}

/* Routes ------------------------------------------------------------------- */

async function judgeCode(req, res, action) {
  const body = await readJson(req);
  const userId = String(body.userId || "");
  if (!userId) return send(res, 400, { error: "userId is missing." });
  if (busyUsers.has(userId)) return send(res, 429, { error: "Your last run is still going." });
  if (tooManyRuns(userId)) return send(res, 429, { error: "That's a lot of runs. Wait a few minutes, then try again." });
  busyUsers.add(userId);
  try {
    const input = { id: body.id, lang: body.lang, code: body.code, cases: body.cases };
    send(res, 200, await inTurn(() => judge[action](input)));
  } catch (err) {
    if (err.name === "JudgeError" || err.status) return send(res, err.status, { error: err.message });
    throw err;
  } finally {
    busyUsers.delete(userId);
  }
}

const routes = {
  "GET /health": (req, res) => send(res, 200, { ok: true, running: active, waiting: waiting.length }),
  "GET /languages": async (req, res) => {
    const ids = Object.keys(LANGS);
    const ok = await Promise.all(ids.map((id) => available(id)));
    send(res, 200, { languages: ids.filter((_, i) => ok[i]) });
  },
  "POST /run": (req, res) => judgeCode(req, res, "run"),
  "POST /submit": (req, res) => judgeCode(req, res, "submit"),
};

const server = http.createServer(async (req, res) => {
  const pathname = new URL(req.url, "http://localhost").pathname;
  const route = routes[`${req.method} ${pathname}`];
  if (!route) return send(res, 404, { error: "Not found." });
  if (pathname !== "/health" && !authorized(req)) return send(res, 401, { error: "Wrong or missing JUDGE_SECRET." });
  try {
    await route(req, res);
  } catch (err) {
    if (!res.headersSent) send(res, err.status || 500, { error: err.status ? err.message : "Something went wrong." });
    if (!err.status) console.error(err);
  }
});

/* Compile cache ------------------------------------------------------------ */

// Compiled solutions are kept by a hash of their code (tools/lib/langs.mjs),
// so Submit after Run doesn't compile again. Anything not used for a day goes.
const BUILD = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "backend", "practice", "dsa", "build");
function sweepCache() {
  const cutoff = Date.now() - 24 * 3600_000;
  for (const lang of ["cpp", "c", "java"]) {
    const dir = path.join(BUILD, lang);
    let entries = [];
    try {
      entries = readdirSync(dir);
    } catch {
      continue;
    }
    for (const name of entries) {
      const entry = path.join(dir, name);
      try {
        if (statSync(entry).mtimeMs < cutoff) rmSync(entry, { recursive: true, force: true });
      } catch {}
    }
  }
}
setInterval(sweepCache, 3600_000).unref();

server.listen(PORT, HOST, () => {
  console.log(`Ren judge listening on ${HOST}:${PORT}, ${SLOTS} at a time, sandbox ${process.env.REN_SANDBOX === "1" ? "on" : "OFF"}`);
});
