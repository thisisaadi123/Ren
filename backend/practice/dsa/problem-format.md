# Problem format

Every problem is one folder, and every file in it is checked in to git:

```
problems/<topic>/<pattern>/<slug>/
├── problem.yaml        metadata: see the fields below, validated by problem.schema.json
├── statement.md        the description and constraints, with {{examples}} where the examples go
├── reference.py        the fast solution the answers come from
├── brute.py            a simple, obviously correct solution, used only to cross-check
├── validator.py        rejects any input that breaks the stated constraints
├── gen.py              builds the tests from fixed seeds
├── checker.py          only when checker.type is custom
├── wrong/              common mistakes; each one must fail at least one test
│   ├── off_by_one.py
│   └── too_slow.py
├── solutions/          the reference solution in the other three languages
│   ├── Reference.java
│   ├── reference.cpp
│   └── reference.c     not for design problems (C has no classes)
└── tests.json          the built tests (see test-cases.md)
```

- `<topic>` and `<pattern>` are ids from `taxonomy.yaml`, and `<slug>` is the problem's `id`.
- The pipeline refuses a folder whose path doesn't match its `problem.yaml`.
- The Python files are the source of truth for answers. The `solutions/` files have to produce the same answers, which proves the harness for each language works (see `pipeline.md`).

## Writing problems quickly
`tools/author.py` writes a whole problem folder from one Python call: signature, statement, solutions, validator, generator, wrong solutions and tests. `npm run check:dsa -- --write-expected` then fills in every expected answer from the reference. `gen.py` and `validator.py` can import shared helpers:
- `from ren_gen import ints, distinct, word, matrix, grid, tree, bst, graph, dag`
- `from ren_check import integer, ints, matrix, text, char_grid, tree, is_bst, edges`

Python solutions can use `ListNode`, `TreeNode`, `List`, `Optional`, `collections`, `heapq`, `math` and `bisect` without importing them, as on most judges.

## How the code files are written
They follow the conventions users will see in the editor:

| File | Shape |
|---|---|
| `reference.py`, `brute.py`, `wrong/*.py` | `class Solution:` with the signature's method, e.g. `def minDailyLimit(self, pages, days)` |
| `solutions/Reference.java` | `class Solution { public int minDailyLimit(int[] pages, int days) { … } }`. `java.util.*` is imported for you, and list types are arrays (`int[]`, `int[][]`, `String[]`) |
| `solutions/reference.cpp` | `class Solution { public: int minDailyLimit(vector<int>& pages, int days) { … } };` with no includes, as on most judges. `<bits/stdc++.h>` also works |
| `solutions/reference.c` | LeetCode's C shape: `int minDailyLimit(int* pages, int pagesSize, int days)`. An array comes with its size (`int** grid, int gridSize, int* gridColSize`); an array answer sets `*returnSize` (and `*returnColumnSizes` for 2D) and is `malloc`ed. The standard headers are included |
| `validator.py` | `def validate(pages, days):` using `assert condition, "the constraint in words"` |
| `gen.py` | `def small(rng)` returns random inputs small enough for `brute.py`. `def build(rng, **opts)` returns the input for a `generate` recipe (`--n 50000 --shape uniform` becomes `n=50000, shape="uniform"`). `rng` is a seeded `random.Random` |
| `checker.py` | `def check(args, expected, actual):` returns `True`, or a string saying what's wrong |

## `problem.yaml` fields

| Field | Required | Meaning |
|---|---|---|
| `schema_version` | yes | Always `1` for now |
| `id` | yes | A kebab-case slug, the same as the folder name. Permanent: never reused, even after the problem is retired |
| `title` | yes | Shown to users. Our own wording, never another site's title |
| `topic`, `pattern` | yes | Ids from `taxonomy.yaml`. `pattern` is the one primary pattern that counts for progress |
| `tags` | no | Up to 6 secondary tags (e.g. `hash-map`, `prefix-sums`) for search |
| `difficulty` | yes | `easy`, `medium` or `hard` |
| `status` | yes | `draft` → `review` → `published`. A problem that's pulled becomes `retired` and stays in git |
| `version` | yes | Starts at 1. Bumped whenever the statement or tests change after publishing |
| `kind` | yes | `function` (implement one function) or `design` (implement a class) |
| `signature` | when `kind: function` | The function name, typed parameters and return type |
| `design` | when `kind: design` | The class name, constructor parameters and methods |
| `limits` | yes | `time_ms` (the C++ baseline per test) and `memory_mb` |
| `checker` | yes | `exact`, `unordered`, `float` (needs `tolerance`) or `custom` (uses `checker.py`) |
| `hints` | yes | Ren's help ladder: `hint` (a gentle direction) and `nudge` (the key idea), written by hand. `explain` is optional |
| `authors`, `reviewed_by` | no / yes before publishing | Who wrote the problem and who reviewed it |

### Types in signatures
The allowed types are `int`, `long`, `double`, `bool`, `char`, `string`, `ListNode` and `TreeNode`, plus arrays of them with up to two `[]` (`int[]`, `string[][]`). `void` is allowed only as a design method's return type.

| Type | Python | Java | C++ | C |
|---|---|---|---|---|
| `int` | `int` | `int` | `int` | `int` |
| `long` | `int` | `long` | `long long` | `long long` |
| `double` | `float` | `double` | `double` | `double` |
| `bool` | `bool` | `boolean` | `bool` | `bool` |
| `string` | `str` | `String` | `string` | `char*` |
| `int[]` | `List[int]` | `int[]` | `vector<int>` | `int*` + `int size` |
| `ListNode` / `TreeNode` | class | class | pointer | `struct` pointer |

- **Graphs** are passed as `n: int` plus `edges: int[][]` (each edge is `[u, v]` or `[u, v, w]`), never as a custom type.
- **Grids** are `int[][]` or `char[][]`.

## `statement.md`
- It's written in Markdown, in our own words: a short setup, the task, then the constraints.
- Wherever the examples go, it has the marker `{{examples}}`. The pipeline fills it with each test marked `"example": true` in `tests.json`. The input and output are rendered from the test, and the output always comes from `reference.py`. The explanation is the hand-written `explanation` field on that test.
- The constraints section must match `validator.py`. Reviewers check this, since the pipeline can't.

## Example

A **search-on-the-answer** problem. The idea is a classic one, but the wording, story and numbers are ours.

`problems/binary-search/search-on-answer/print-shop-daily-limit/problem.yaml`

```yaml
schema_version: 1
id: print-shop-daily-limit
title: Print Shop Daily Limit
topic: binary-search
pattern: search-on-answer
tags: [greedy-check]
difficulty: medium
status: draft
version: 1
kind: function
signature:
  function: minDailyLimit
  params:
    - { name: pages, type: "int[]" }
    - { name: days, type: int }
  returns: int
limits:
  time_ms: 1000
  memory_mb: 256
checker:
  type: exact
hints:
  hint: "If a daily limit works, does every bigger limit also work?"
  nudge: "Binary search on the limit. For a given limit, fill each day greedily in order and count how many days you need."
authors: [ren]
reviewed_by: []
```

`statement.md`

```markdown
A print shop has a queue of jobs. Job `i` has `pages[i]` pages, and jobs must be printed in the order they arrive. A job can't be split across two days.

The shop sets one daily page limit and prints as many whole jobs as fit under it each day. Return the smallest daily limit that finishes every job within `days` days.

{{examples}}

**Constraints**
- `1 ≤ pages.length ≤ 5 × 10⁴`
- `1 ≤ pages[i] ≤ 500`
- `1 ≤ days ≤ pages.length`
```
