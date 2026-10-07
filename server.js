// Ren — dev server: serves design/ and a small auth API.
// Run with `npm start`, then open http://localhost:3000. The only package it
// uses is `yaml`, to read the DSA and SQL banks. On Vercel, vercel.json sends
// every request to this file, which exports the same handler `npm start` uses.
//
//   POST /api/signup   { email, password }  -> 201 { user }  (signs in)
//   POST /api/login    { email, password }  -> 200 { user }
//   POST /api/logout                        -> 204
//   GET  /api/me                            -> 200 { user } | 401
//   GET  /api/dsa                           -> 200 { tracks, topics } | 401
//   GET  /api/dsa/problem?id=               -> 200 { problem for the page } | 401 | 404
//   GET  /api/dsa/solution?id=              -> 200 { the written-out solution } | 401 | 404
//   GET  /api/dsa/lesson?id=<pattern>       -> 200 { the pattern's lesson, its problems } | 401 | 404
//   POST /api/dsa/run    { id, lang, code, cases } -> 200 { cases } (this machine only)
//   POST /api/dsa/submit { id, lang, code }        -> 200 { verdict, passed, total }
//   GET  /api/sql                           -> 200 { tracks, topics } | 401
//   GET  /api/sql/problem?id=               -> 200 { problem for the page } | 401 | 404
//   POST /api/sql/run    { id, code }       -> 200 { cases } (this machine only)
//   POST /api/sql/submit { id, code }       -> 200 { verdict, passed, total }
//
// Accounts are kept in memory only: nothing is written to disk, and every
// account except the seed user is forgotten when the server stops.
// Settings, including the seed test user, come from .env (gitignored; copy
// .env.example to start).

const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const ROOT = __dirname;
const PUBLIC = path.join(ROOT, "design");

/* Settings --------------------------------------------------------------- */

// Minimal .env reader: KEY=value lines, # comments, optional quotes.
function loadEnv(file) {
  if (!fs.existsSync(file)) return;
  for (const line of fs.readFileSync(file, "utf8").split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/);
    if (!m || line.trim().startsWith("#")) continue;
    const value = m[2].replace(/^(['"])(.*)\1$/, "$2");
    if (!(m[1] in process.env)) process.env[m[1]] = value;
  }
}
loadEnv(path.join(ROOT, ".env"));

const PORT = Number(process.env.PORT) || 3000;
const SESSION_DAYS = 7;
let SECRET = process.env.SESSION_SECRET;
if (!SECRET) {
  SECRET = crypto.randomBytes(32).toString("hex");
  console.warn("SESSION_SECRET is not set in .env; sessions will end when the server restarts.");
}

/* Users ------------------------------------------------------------------ */

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

// In memory only, on purpose: no emails, names or passwords are stored anywhere.
const USERS = [];
const readUsers = () => USERS;

function hashPassword(password, salt = crypto.randomBytes(16).toString("hex")) {
  const hash = crypto.scryptSync(password, salt, 64).toString("hex");
  return `${salt}:${hash}`;
}

function checkPassword(password, stored) {
  const [salt, hash] = stored.split(":");
  const a = Buffer.from(hash, "hex");
  const b = crypto.scryptSync(password, salt, 64);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

// What the browser gets: never the password hash.
const publicUser = (u) => ({
  id: u.id,
  email: u.email,
  name: u.name || "",
  createdAt: u.createdAt,
  progress: u.progress || null,
});

// Sample history so the seed account's home page has something to show.
// Dates are relative to today, so the week strip always looks lived in.
function seedProgress() {
  const day = (n) => new Date(Date.now() - n * 864e5).toISOString().slice(0, 10);
  return {
    continue: {
      track: "DSA",
      title: "Merge Intervals",
      difficulty: "Medium",
      topic: "Arrays",
      language: "Python",
      passed: 2,
      total: 4,
      opened: "Yesterday",
    },
    practice: { dsa: 14, sql: 5, design: 1 },
    resume: { file: "alex_morgan.pdf", checked: "2 days ago" },
    interview: { done: 3, last: "Backend Engineer, Sep 24" },
    activeDays: [day(1), day(2), day(3), day(5)],
  };
}

// The seed user is rebuilt from .env on every start. Its id comes from the
// email, so a session stays valid when a different server instance (Vercel
// runs several) answers the next request.
function ensureSeedUser() {
  const email = (process.env.SEED_EMAIL || "").trim().toLowerCase();
  const password = process.env.SEED_PASSWORD || "";
  if (!email || !password) {
    console.warn("No SEED_EMAIL / SEED_PASSWORD in .env; skipping the seed user.");
    return;
  }
  USERS.push({
    id: crypto.createHash("sha256").update(`seed:${email}`).digest("hex").slice(0, 32),
    email,
    name: process.env.SEED_NAME || "",
    password: hashPassword(password),
    createdAt: new Date().toISOString(),
    progress: seedProgress(),
    seed: true,
  });
  console.log(`Seed user ready: ${email}`);
}

/* Sessions: a signed cookie holding the user id and an expiry ------------ */

const COOKIE = "ren_session";
const sign = (payload) => crypto.createHmac("sha256", SECRET).update(payload).digest("base64url");

function sessionCookie(userId) {
  const exp = Date.now() + SESSION_DAYS * 864e5;
  const payload = `${userId}.${exp}`;
  return `${COOKIE}=${payload}.${sign(payload)}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${SESSION_DAYS * 86400}`;
}

const clearCookie = `${COOKIE}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0`;

function currentUser(req) {
  const raw = (req.headers.cookie || "")
    .split(";")
    .map((c) => c.trim())
    .find((c) => c.startsWith(`${COOKIE}=`));
  if (!raw) return null;
  const [id, exp, sig] = raw.slice(COOKIE.length + 1).split(".");
  if (!id || !exp || !sig) return null;
  const expected = Buffer.from(sign(`${id}.${exp}`));
  const given = Buffer.from(sig);
  if (expected.length !== given.length || !crypto.timingSafeEqual(expected, given)) return null;
  if (Number(exp) < Date.now()) return null;
  return readUsers().find((u) => u.id === id) || null;
}

/* HTTP helpers ------------------------------------------------------------ */

function send(res, status, body, headers = {}) {
  const json = body === undefined ? "" : JSON.stringify(body);
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    ...headers,
  });
  res.end(json);
}

// JSON bodies only: a cross-site form can't send one without a CORS preflight.
function readJson(req, limit = 10_000) {
  return new Promise((resolve, reject) => {
    if (!(req.headers["content-type"] || "").startsWith("application/json")) {
      return reject(Object.assign(new Error("Expected JSON"), { status: 415 }));
    }
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

/* API --------------------------------------------------------------------- */

const api = {
  "GET /api/me": (req, res) => {
    const user = currentUser(req);
    if (!user) return send(res, 401, { error: "Not signed in." });
    send(res, 200, { user: publicUser(user) });
  },

  "POST /api/signup": async (req, res) => {
    // The name never reaches the server: sign up keeps it in the browser.
    const { email = "", password = "" } = await readJson(req);
    const clean = String(email).trim().toLowerCase();
    if (!EMAIL.test(clean)) return send(res, 400, { error: "Enter a valid email address.", field: "email" });
    if (String(password).length < 8) return send(res, 400, { error: "Use at least 8 characters.", field: "password" });

    const users = readUsers();
    if (users.some((u) => u.email === clean)) {
      return send(res, 409, { error: "An account with this email already exists.", field: "email" });
    }
    const user = {
      id: crypto.randomUUID(),
      email: clean,
      name: "",
      password: hashPassword(String(password)),
      createdAt: new Date().toISOString(),
      progress: null,
    };
    users.push(user);
    send(res, 201, { user: publicUser(user) }, { "Set-Cookie": sessionCookie(user.id) });
  },

  "POST /api/login": async (req, res) => {
    const { email = "", password = "" } = await readJson(req);
    const user = readUsers().find((u) => u.email === String(email).trim().toLowerCase());
    // Same answer whether the email or the password is wrong.
    if (!user || !checkPassword(String(password), user.password)) {
      return send(res, 401, { error: "Incorrect email or password." });
    }
    send(res, 200, { user: publicUser(user) }, { "Set-Cookie": sessionCookie(user.id) });
  },

  "POST /api/logout": (req, res) => {
    send(res, 204, undefined, { "Set-Cookie": clearCookie });
  },

  "GET /api/dsa": (req, res) => {
    if (!currentUser(req)) return send(res, 401, { error: "Not signed in." });
    send(res, 200, dsaSheet());
  },

  "GET /api/dsa/problem": async (req, res) => {
    if (!currentUser(req)) return send(res, 401, { error: "Not signed in." });
    const id = new URL(req.url, "http://localhost").searchParams.get("id");
    const judge = await import("./backend/practice/dsa/tools/judge.mjs");
    send(res, 200, await judge.problemView(id));
  },

  "GET /api/dsa/solution": async (req, res) => {
    if (!currentUser(req)) return send(res, 401, { error: "Not signed in." });
    const id = new URL(req.url, "http://localhost").searchParams.get("id");
    const judge = await import("./backend/practice/dsa/tools/judge.mjs");
    send(res, 200, judge.solutionView(id));
  },

  "GET /api/dsa/lesson": (req, res) => {
    if (!currentUser(req)) return send(res, 401, { error: "Not signed in." });
    const id = new URL(req.url, "http://localhost").searchParams.get("id") || "";
    const lesson = dsaLesson(id);
    if (!lesson) return send(res, 404, { error: "This lesson isn't written yet." });
    send(res, 200, lesson);
  },

  "POST /api/dsa/run": (req, res) => judgeCode(req, res, "run"),
  "POST /api/dsa/submit": (req, res) => judgeCode(req, res, "submit"),

  "GET /api/sql": (req, res) => {
    if (!currentUser(req)) return send(res, 401, { error: "Not signed in." });
    send(res, 200, sqlSheet());
  },

  "GET /api/sql/problem": async (req, res) => {
    if (!currentUser(req)) return send(res, 401, { error: "Not signed in." });
    const id = new URL(req.url, "http://localhost").searchParams.get("id");
    const judge = await import(SQL_JUDGE);
    try {
      send(res, 200, judge.problemView(id));
    } catch (err) {
      if (err.name === "JudgeError") return send(res, err.status, { error: err.message });
      throw err;
    }
  },

  "POST /api/sql/run": (req, res) => judgeCode(req, res, "run", SQL_JUDGE),
  "POST /api/sql/submit": (req, res) => judgeCode(req, res, "submit", SQL_JUDGE),
};

/* Running code ---------------------------------------------------------------- */

// Run and Submit execute the code people type, so they only answer requests
// from this machine (a dev server can be reachable from the local network),
// and each account runs one thing at a time. They're off on Vercel: its
// runtime hands requests to the function over localhost, so the address
// check alone would let anyone on the internet run code there.
const running = new Set();
const HOSTED = Boolean(process.env.VERCEL);
const fromThisMachine = (req) => !HOSTED && ["127.0.0.1", "::1", "::ffff:127.0.0.1"].includes(req.socket.remoteAddress);

const DSA_JUDGE = "./backend/practice/dsa/tools/judge.mjs";
const SQL_JUDGE = "./backend/practice/sql/tools/judge.mjs";

async function judgeCode(req, res, action, module = DSA_JUDGE) {
  const user = currentUser(req);
  if (!user) return send(res, 401, { error: "Not signed in." });
  if (!fromThisMachine(req)) {
    const error = HOSTED ? "Running code isn't available on the hosted site yet." : "Code only runs on the machine the server is on.";
    return send(res, 403, { error });
  }
  if (running.has(user.id)) return send(res, 429, { error: "Your last run is still going." });
  const body = await readJson(req, 200_000);
  running.add(user.id);
  try {
    const judge = await import(module);
    send(res, 200, await judge[action]({ id: body.id, lang: body.lang, code: body.code, cases: body.cases }));
  } catch (err) {
    if (err.name === "JudgeError") return send(res, err.status, { error: err.message });
    throw err;
  } finally {
    running.delete(user.id);
  }
}

/* DSA sheet ----------------------------------------------------------------- */

// The whole DSA bank as one sheet: every topic and pattern from the taxonomy,
// with the problems that exist on disk. A pattern with fewer problems than
// its count shows the rest as locked. Read fresh on every request, so new
// problems show up without a restart.
const DSA = path.join(ROOT, "backend", "practice", "dsa");
const DIFFICULTY = { easy: 0, medium: 1, hard: 2 };

// What the problem hands you, from its signature: the first parameter's type.
function problemType(p) {
  if (p.kind === "design") return "Design";
  const t = String(p.signature?.params?.[0]?.type ?? "");
  if (t === "ListNode") return "Linked list";
  if (t === "TreeNode") return "Tree";
  if (t.endsWith("[][]")) return "Matrix";
  if (t.startsWith("string") || t === "char[]") return "String";
  if (t.endsWith("[]")) return "Array";
  return "Number";
}

function dsaSheet() {
  // The YAML parser is the dev dependency the DSA tools already use.
  const YAML = require("yaml");
  const read = (file) => YAML.parse(fs.readFileSync(file, "utf8"));
  const taxonomy = read(path.join(DSA, "taxonomy.yaml"));

  const problems = new Map(); // pattern id -> problems
  const dir = path.join(DSA, "problems");
  for (const topic of fs.readdirSync(dir, { withFileTypes: true })) {
    if (!topic.isDirectory()) continue;
    for (const pattern of fs.readdirSync(path.join(dir, topic.name), { withFileTypes: true })) {
      if (!pattern.isDirectory()) continue;
      for (const slug of fs.readdirSync(path.join(dir, topic.name, pattern.name))) {
        const file = path.join(dir, topic.name, pattern.name, slug, "problem.yaml");
        if (!fs.existsSync(file)) continue;
        const p = read(file);
        const list = problems.get(p.pattern) || [];
        list.push({ id: p.id, title: p.title, difficulty: p.difficulty, type: problemType(p) });
        problems.set(p.pattern, list);
      }
    }
  }

  return {
    tracks: taxonomy.tracks.map(({ id, name }) => ({ id, name })),
    topics: taxonomy.topics.map((t) => ({
      id: t.id,
      name: t.name,
      track: t.track,
      count: t.count,
      patterns: t.patterns.map((p) => ({
        id: p.id,
        name: p.name,
        about: p.about,
        count: p.count,
        lesson: lessonMinutes(t.id, p.id),
        problems: (problems.get(p.id) || []).sort(
          (a, b) => DIFFICULTY[a.difficulty] - DIFFICULTY[b.difficulty] || a.title.localeCompare(b.title)
        ),
      })),
    })),
  };
}

/* Pattern lessons ------------------------------------------------------------ */

// A pattern's lesson (lessons/<topic>/<pattern>.json, written by
// tools/lessons/build.py): the theory and practice to read before its problems.
const lessonFile = (topic, pattern) => path.join(DSA, "lessons", topic, `${pattern}.json`);

function lessonMinutes(topic, pattern) {
  const file = lessonFile(topic, pattern);
  if (!fs.existsSync(file)) return null;
  try {
    return JSON.parse(fs.readFileSync(file, "utf8")).minutes || null;
  } catch {
    return null;
  }
}

// The lesson with what the page shows around it: the topic and pattern, the
// pattern's problems to practise, and the lessons before and after it.
function dsaLesson(id) {
  if (!/^[a-z0-9-]+$/.test(id)) return null;
  const sheet = dsaSheet();
  const all = sheet.topics.flatMap((t) => t.patterns.map((p) => ({ topic: t, pattern: p })));
  const at = all.findIndex((x) => x.pattern.id === id && x.pattern.lesson);
  if (at < 0) return null;
  const { topic, pattern } = all[at];
  const near = (x) => x && { id: x.pattern.id, name: x.pattern.name, minutes: x.pattern.lesson };
  const withLesson = all.filter((x) => x.pattern.lesson);
  const i = withLesson.findIndex((x) => x.pattern.id === id);
  return {
    ...JSON.parse(fs.readFileSync(lessonFile(topic.id, id), "utf8")),
    topic: { id: topic.id, name: topic.name },
    pattern: { id, name: pattern.name, about: pattern.about, count: pattern.count },
    problems: pattern.problems,
    prev: near(withLesson[i - 1]),
    next: near(withLesson[i + 1]),
  };
}

/* SQL sheet ------------------------------------------------------------------ */

// The same shape as the DSA sheet, from backend/practice/sql: the taxonomy,
// plus each problem's problem.json. A problem's type is how many tables it
// works with.
const SQL_BANK = path.join(ROOT, "backend", "practice", "sql");
const TABLE_TYPES = ["One table", "Two tables", "Three or more"];

function sqlSheet() {
  const YAML = require("yaml");
  const taxonomy = YAML.parse(fs.readFileSync(path.join(SQL_BANK, "taxonomy.yaml"), "utf8"));
  const problems = new Map(); // "topic/pattern" -> problems
  const dir = path.join(SQL_BANK, "problems");
  const subdirs = (d) => (fs.existsSync(d) ? fs.readdirSync(d, { withFileTypes: true }).filter((e) => e.isDirectory()) : []);
  for (const topic of subdirs(dir)) {
    for (const pattern of subdirs(path.join(dir, topic.name))) {
      for (const slug of subdirs(path.join(dir, topic.name, pattern.name))) {
        const file = path.join(dir, topic.name, pattern.name, slug.name, "problem.json");
        if (!fs.existsSync(file)) continue;
        const p = JSON.parse(fs.readFileSync(file, "utf8"));
        const key = `${p.topic}/${p.pattern}`;
        const list = problems.get(key) || [];
        const type = TABLE_TYPES[Math.min(p.tables.length, 3) - 1];
        list.push({ id: p.id, title: p.title, difficulty: p.difficulty, type });
        problems.set(key, list);
      }
    }
  }
  return {
    types: TABLE_TYPES,
    tracks: taxonomy.tracks.map(({ id, name }) => ({ id, name })),
    topics: taxonomy.topics.map((t) => ({
      id: t.id,
      name: t.name,
      track: t.track,
      patterns: t.patterns.map((p) => ({
        id: p.id,
        name: p.name,
        about: p.about,
        count: Math.max(p.count, (problems.get(`${t.id}/${p.id}`) || []).length),
        problems: (problems.get(`${t.id}/${p.id}`) || []).sort(
          (a, b) => DIFFICULTY[a.difficulty] - DIFFICULTY[b.difficulty] || a.title.localeCompare(b.title)
        ),
      })),
    })),
  };
}

/* Static files ------------------------------------------------------------ */

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".ico": "image/x-icon",
  ".json": "application/json; charset=utf-8",
  ".woff2": "font/woff2",
};

// Pages that need a session, and pages that make no sense with one.
const PRIVATE = new Set(["/app.html", "/practice.html", "/dsa.html", "/problem.html", "/learn.html", "/sql.html", "/sql-problem.html"]);
const GUEST_ONLY = new Set(["/login.html", "/signup.html"]);

// Any missing page gets the 404 page (design/404.html), with a 404 status.
function notFound(res) {
  fs.readFile(path.join(PUBLIC, "404.html"), (err, data) => {
    if (err) {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      return res.end("Not found");
    }
    res.writeHead(404, { "Content-Type": TYPES[".html"], "Cache-Control": "no-store" });
    res.end(data);
  });
}

function serveStatic(req, res, pathname) {
  if (pathname === "/") pathname = "/index.html";
  if (pathname === "/app") pathname = "/app.html";
  if (pathname === "/practice") pathname = "/practice.html";
  if (pathname === "/dsa") pathname = "/dsa.html";
  if (pathname === "/learn") pathname = "/learn.html";
  if (pathname === "/sql") pathname = "/sql.html";

  if (PRIVATE.has(pathname) && !currentUser(req)) {
    res.writeHead(302, { Location: "/login.html" });
    return res.end();
  }
  if (GUEST_ONLY.has(pathname) && currentUser(req)) {
    res.writeHead(302, { Location: "/app.html" });
    return res.end();
  }

  const file = path.normalize(path.join(PUBLIC, pathname));
  const inside = file.startsWith(PUBLIC + path.sep);
  const hidden = path.basename(file).startsWith(".");
  if (!inside || hidden) return notFound(res);

  fs.readFile(file, (err, data) => {
    if (err) return notFound(res);
    res.writeHead(200, {
      "Content-Type": TYPES[path.extname(file)] || "application/octet-stream",
      "Cache-Control": "no-store",
    });
    res.end(data);
  });
}

/* Server ------------------------------------------------------------------ */

async function handler(req, res) {
  let pathname;
  try {
    pathname = decodeURIComponent(new URL(req.url, "http://localhost").pathname);
  } catch {
    return send(res, 400, { error: "Bad request." });
  }

  if (pathname.startsWith("/api/")) {
    const handler = api[`${req.method} ${pathname}`];
    if (!handler) return send(res, 404, { error: "Not found." });
    try {
      await handler(req, res);
    } catch (err) {
      if (!res.headersSent) send(res, err.status || 500, { error: err.status ? err.message : "Something went wrong." });
      if (!err.status) console.error(err);
    }
    return;
  }

  if (req.method !== "GET" && req.method !== "HEAD") return send(res, 405, { error: "Method not allowed." });
  serveStatic(req, res, pathname);
}

ensureSeedUser();

// Vercel imports this file and calls the handler; `npm start` runs it.
module.exports = handler;

if (require.main === module) {
  const server = http.createServer(handler);
  server.on("error", (err) => {
    if (err.code !== "EADDRINUSE") throw err;
    console.error(`Port ${PORT} is already in use; Ren may already be running at http://localhost:${PORT}.`);
    console.error(`Stop the other server, or set a different PORT in .env.`);
    process.exit(1);
  });
  server.listen(PORT, () => console.log(`Ren is running at http://localhost:${PORT}`));
}
