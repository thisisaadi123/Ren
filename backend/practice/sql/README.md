# Ren SQL bank

Original SQL practice problems for the SQL sheet (`design/sql.html`) and the SQL workspace (`design/sql-problem.html`).

## Decisions

- **Original problems.** Every scenario, table and statement is written for Ren. Concepts are standard interview
  topics; no wording or data is taken from any problem site or sheet.
- **SQLite.** Queries run on Node's built-in SQLite (`node:sqlite`, SQLite 3.5x): window functions, CTEs,
  `RIGHT`/`FULL JOIN` all work. Dates are `YYYY-MM-DD` text, so `date()`, `strftime()` and `julianday()` apply.
- **Read-only.** A query must be one `SELECT` / `WITH` statement. SQLite's authorizer refuses anything else
  (writes, `PRAGMA`, `ATTACH`). Queries run in a child process that is killed after 4 s (Run) or 8 s (Submit).
- **Judging.** Each test is a fresh in-memory database. The answer must have the same number of columns and the same
  rows; column names don't count. Rows are compared in order only when the problem says how to order them
  (`"ordered": true`); numbers match within 1e-6.

## Layout

- `taxonomy.yaml`: tracks, topics, patterns and planned counts (the sheet shows unwritten ones as locked).
- `problems/<topic>/<pattern>/<id>/problem.json`: statement, tables, reference query, wrong queries.
- `problems/.../tests.json`: example and hidden datasets with expected answers, one test per line.
- `tools/author.py` + `tools/worlds.py`: write problems (`P(...)`) and build random datasets.
- `tools/authors/*.py`: the problems, one file per group of topics.
- `tools/engine.mjs`: database setup, the read-only query runner and result comparison.
- `tools/judge.mjs`: what the page and server need (problem view, run, submit).
- `tools/check.mjs`: `npm run check:sql -- [--write-expected] [id|dir ...]`.

## Writing problems

1. Add `P(...)` calls to a file in `tools/authors/` and run it with `python3`.
2. `npm run check:sql -- --write-expected` fills in expected answers and checks that:
   - the reference runs everywhere,
   - an ordered problem's `ORDER BY` decides the order completely (tables loaded backwards give the same rows),
   - every wrong query fails at least one test,
   - there are enough hidden tests (easy 8, medium 10, hard 12) and at most a third expect no rows.
