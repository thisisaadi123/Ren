// Ren SQL engine: builds a test database in memory and runs one query on it
// with Node's built-in SQLite. Most problems ask for a SELECT (read-only);
// "change" problems ask for one UPDATE, DELETE or INSERT, and are judged on
// the table it leaves behind. Used by the judge (through
// query.mjs, in a child process that can be killed on a timeout) and by the
// checks, so a query is judged exactly the way the checks judge it.
import { DatabaseSync, constants as C } from "node:sqlite";

export const MAX_ROWS = 5000;

// A query may only read: SELECT, the tables it reads, functions and WITH
// RECURSIVE. Anything else (writes, PRAGMA, ATTACH…) is refused by SQLite.
const READ_ONLY = new Set([C.SQLITE_SELECT, C.SQLITE_READ, C.SQLITE_FUNCTION, C.SQLITE_RECURSIVE]);
// A change problem may also write rows, but never touch SQLite's own tables.
const WRITES = new Set([C.SQLITE_INSERT, C.SQLITE_UPDATE, C.SQLITE_DELETE]);

const quote = (name) => `"${String(name).replace(/"/g, '""')}"`;

// tables: [{ name, columns: [[name, type, key?], …] }]; data: { table: [[…row], …] }
export function createDb(tables, data, { writable = false } = {}) {
  const db = new DatabaseSync(":memory:");
  for (const t of tables) {
    const cols = t.columns.map(([name, type, key]) => `${quote(name)} ${type}${key === "pk" ? " PRIMARY KEY" : ""}`);
    db.exec(`CREATE TABLE ${quote(t.name)} (${cols.join(", ")})`);
    const rows = data[t.name] || [];
    if (!rows.length) continue;
    const insert = db.prepare(`INSERT INTO ${quote(t.name)} VALUES (${t.columns.map(() => "?").join(", ")})`);
    db.exec("BEGIN");
    for (const row of rows) insert.run(...row);
    db.exec("COMMIT");
  }
  db.setAuthorizer((code, target) => {
    if (READ_ONLY.has(code)) return C.SQLITE_OK;
    if (writable && WRITES.has(code) && !String(target).startsWith("sqlite_")) return C.SQLITE_OK;
    return C.SQLITE_DENY;
  });
  return db;
}

// The query with comments and string contents blanked out, so checks on
// its shape can't be fooled by a semicolon inside a string.
function skeleton(sql) {
  return sql.replace(/--[^\n]*|\/\*[\s\S]*?(\*\/|$)|'(?:[^']|'')*'?|"(?:[^"]|"")*"?/g, (m) =>
    m.startsWith("'") || m.startsWith('"') ? m[0].repeat(2) : " "
  );
}

// One query, nothing else. Returns the query to run, or why it can't run.
export function vet(sql, mode = "query") {
  const text = String(sql ?? "");
  if (text.length > 20_000) return { error: "Your query is too long." };
  const bare = skeleton(text).trim().replace(/;\s*$/, "");
  if (!bare) return { error: "Write a query first." };
  if (bare.includes(";")) return { error: "Write one query: there's more than one statement here." };
  if (mode === "change") {
    if (!/^(update|delete|insert|replace|with)\b/i.test(bare)) {
      return { error: "This problem changes a table: write one UPDATE, DELETE or INSERT statement." };
    }
  } else if (!/^(select|with|values)\b/i.test(bare)) {
    return { error: "Only SELECT queries run here: start with SELECT or WITH." };
  }
  return { sql: text };
}

const tidy = (message, mode = "query") =>
  String(message)
    .replace(/^SqliteError:\s*/, "")
    .replace(
      /^not authorized$/,
      mode === "change"
        ? "That statement isn't allowed here: change rows with UPDATE, DELETE or INSERT, nothing else."
        : "Only SELECT queries run here: this one tries to change or inspect the database."
    );

// Runs a vetted query. Returns { columns, rows } or { error }.
export function runQuery(db, sql) {
  let stmt;
  try {
    stmt = db.prepare(sql);
  } catch (err) {
    return { error: tidy(err.message) };
  }
  try {
    stmt.setReturnArrays(true);
    const columns = stmt.columns().map((c) => c.name);
    if (!columns.length) return { error: "Your query doesn't return any columns." };
    const rows = [];
    for (const row of stmt.iterate()) {
      if (rows.length >= MAX_ROWS) return { error: `Your query returned more than ${MAX_ROWS} rows.` };
      rows.push(row.map((v) => (typeof v === "bigint" ? Number(v) : v instanceof Uint8Array ? "<blob>" : v)));
    }
    return { columns, rows };
  } catch (err) {
    return { error: tidy(err.message) };
  }
}

// Runs a change statement, then reads back the table it was meant to change.
export function runChange(db, sql, table) {
  try {
    db.prepare(sql).run();
  } catch (err) {
    return { error: tidy(err.message, "change") };
  }
  return runQuery(db, `SELECT * FROM "${table}"`);
}

// Runs the query on each dataset, each in a fresh database. A change
// problem (mode "change") reports the result table's rows afterwards.
export function runAll(tables, datasets, sql, { mode = "query", table } = {}) {
  const v = vet(sql, mode);
  if (v.error) return datasets.map(() => ({ error: v.error }));
  return datasets.map((data) => {
    const db = createDb(tables, data, { writable: mode === "change" });
    const t = performance.now();
    const out = mode === "change" ? runChange(db, v.sql, table) : runQuery(db, v.sql);
    out.ms = performance.now() - t;
    db.close();
    return out;
  });
}

/* Comparing results ----------------------------------------------------------- */

// Values match when they're the same, or numbers within 1e-6 (so 3 and 3.0
// are equal, and float rounding noise doesn't matter).
function sameValue(a, b) {
  if (a === b) return true;
  if (typeof a === "number" && typeof b === "number") return Math.abs(a - b) <= 1e-6 * Math.max(1, Math.abs(a), Math.abs(b));
  return false;
}
const sameRow = (a, b) => a.length === b.length && a.every((v, i) => sameValue(v, b[i]));

// A sortable key for a row, so unordered results can be compared in order.
const key = (row) =>
  JSON.stringify(row.map((v) => (v === null ? [0] : typeof v === "number" ? [1, Math.round(v * 1e6) / 1e6] : [2, String(v)])));

// The verdict for one result against the expected one. Column names don't
// count, only how many columns there are and the values, in order.
export function compare(got, want, ordered) {
  if (got.columns.length !== want.columns.length) {
    return { ok: false, why: `Expected ${want.columns.length} ${want.columns.length === 1 ? "column" : "columns"}, got ${got.columns.length}.` };
  }
  if (got.rows.length !== want.rows.length) {
    return { ok: false, why: `Expected ${want.rows.length} ${want.rows.length === 1 ? "row" : "rows"}, got ${got.rows.length}.` };
  }
  let a = got.rows;
  let b = want.rows;
  if (!ordered) {
    const sort = (rows) => rows.map((r) => [key(r), r]).sort((x, y) => (x[0] < y[0] ? -1 : x[0] > y[0] ? 1 : 0)).map((x) => x[1]);
    a = sort(a);
    b = sort(b);
  }
  for (let i = 0; i < a.length; i++) {
    if (!sameRow(a[i], b[i])) return { ok: false, why: ordered ? `Row ${i + 1} is different.` : "Some rows are different." };
  }
  return { ok: true };
}
