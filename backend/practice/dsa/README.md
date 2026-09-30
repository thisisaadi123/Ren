# Ren Practice: DSA problem bank

This folder holds the problem bank behind Ren's DSA practice: which problems exist, how each one is stored, and how it's checked, tracked and unlocked. The checking pipeline runs (see `pipeline.md`); the problem-writing workflow and the Practice UI come later.

```sh
npm run check:dsa                    # check every problem, plus the bank-wide checks
npm run check:dsa -- <problem-dir>   # check one problem
npm run check:dsa -- --write-expected   # fill in missing expected answers from the reference
npm run test:dsa                     # self-test: plant known bugs and confirm the pipeline catches each one
```

| File | What it defines |
|---|---|
| [`taxonomy.yaml`](taxonomy.yaml) | Topics → patterns → target counts (522 problems, 133 patterns). The single source of truth |
| [`problem-format.md`](problem-format.md) | The folder and files for one problem, and the `problem.yaml` fields |
| [`problem.schema.json`](problem.schema.json) | JSON Schema for `problem.yaml` |
| [`test-cases.md`](test-cases.md) | Visible vs hidden tests, edge cases, speed tests, Run vs Submit |
| [`pipeline.md`](pipeline.md) | The checks a problem must pass before it's published |
| [`progress.md`](progress.md) | What we record per user, pattern mastery and topic rollups |
| [`sheets.md`](sheets.md) | The LeetCode link sheets a user unlocks by finishing a topic |
| `problems/` | The problems, one folder each. Written so far: **Arrays & Hashing (33/33)** and **Binary Search (35/35)**, plus one each in Linked List, Binary Trees and Design |
| `tools/` | The checking pipeline (`check.mjs`), its self-test, the language runners, `author.py` (writes a whole problem folder from one call) and `pylib/` (shared helpers for `gen.py` and `validator.py`) |
| `build/` | Generated: built tests and rendered statements (gitignored) |
| `sheets/` | One sheet per topic (only `_example.yaml` for now) |

## Decisions

### We write our own problems
- Every problem statement, example, constraint and test in this bank is **original**.
- Copyright covers *wording*, not *ideas*. Classic ideas (search a rotated array, the minimum capacity to finish in D days) are fine **in our own words**, with our own story, names, examples and constraints.
- Never copy or lightly reword a problem from LeetCode, GeeksforGeeks, HackerRank or any other site.
- Never write "LeetCode #1011" or anything that suggests a partnership. Plain "similar problem" links to other sites are fine (see `sheets.md`).
- Open datasets are **not** a source of problems:
  - `open-r1/codeforces` (ODC-By) is used only to benchmark the checking pipeline.
  - TACO is not used, because it includes text scraped from LeetCode and GeeksforGeeks.
- Text written by AI is always reviewed and edited by a person before it's published. That's for quality, and it also strengthens our claim to own it.

### Structure
**Topic → Pattern → Problem.**
- Each problem has exactly one **primary pattern**, which drives progress.
- It can also have secondary **tags** (e.g. `hash-map`) for search and filtering.
- Pattern ids are unique across the whole taxonomy.

### Size and difficulty
- **522 problems, 23 topics, 133 patterns.** Topic names follow the popular sheets (NeetCode, Striver A2Z, LeetCode Top Interview).
- Difficulty mix across the bank: **about 30% Easy (150), 50% Medium (250), 20% Hard (100)**, each within ±5%.
- Every pattern starts with at least one Easy problem and gets harder from there.

### Tracks (the suggested order)
1. **Foundations:** Arrays & Hashing, Sorting, Two Pointers, Strings, Sliding Window, Stack & Queue, Binary Search, Linked List
2. **Core:** Binary Trees, Binary Search Trees, Tries, Heap / Priority Queue, Recursion & Backtracking, Intervals, Greedy
3. **Advanced:** Graphs, Advanced Graphs, 1-D Dynamic Programming, 2-D Dynamic Programming, Bit Manipulation, Math & Geometry, Design, Range Queries

Each topic's `prerequisites` in `taxonomy.yaml` say which topics to recommend first. They're suggestions, not locks.

### Languages
Python, Java, C++ and C. Every problem must run in all four (C only for `kind: function`; it has no classes).

## Phases
1. **Format + pipeline:** the problem format, a harness per language, the checking code, and a benchmark run on open-r1/codeforces.
2. **Pilot: Binary Search,** its 35 problems plus its LeetCode sheet, fully checked. It's reviewed before anything scales up.
3. **Foundations** (the rest of track 1)
4. **Core**
5. **Advanced**
6. **Practice UI and progress storage** (a database is still to be chosen)

Each batch goes through: set per-pattern counts in `taxonomy.yaml` → write the problems → automatic checks → human review → publish.
