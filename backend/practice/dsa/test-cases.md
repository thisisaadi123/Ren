# Test cases

Every problem ships with two sets of tests in `tests.json`.

| Set | What's in it | How many | Where users see it |
|---|---|---|---|
| **Visible** | The statement's examples, plus 1–2 extra samples | 3–5 | The "Test cases" tab, run by **Run** |
| **Hidden** | Hand-picked edge cases, random cases and max-size cases | Easy ≈ 25 · Medium ≈ 50 · Hard ≈ 80+ | Run by **Submit** |

## Rules
1. **Every expected answer comes from `reference.py`.** None are typed by hand. Whenever an input is small enough, the answer is also compared with `brute.py`.
2. **Every input passes `validator.py`,** including hand-written edge cases. A test that breaks the problem's own constraints is a bug.
3. **Random tests use fixed seeds,** so a rebuild gives the same tests. The seed is stored in `tests.json`.
4. **Max-size tests** hit the largest allowed input, and at least one of them is shaped to be worst-case: sorted, all equal, a long chain, or whatever is slowest for a naive solution.
   - The fast solution must pass in **every language** using at most half of the time limit.
   - The known-slow solution in `wrong/` must time out.
5. **Every file in `wrong/` fails at least one test.** Otherwise the tests are too weak, and the pipeline fails the problem.
6. **When several answers are valid** (any order, any valid index, a decimal answer), `checker.type` must be `unordered`, `float` or `custom`. It's never `exact`.

## Edge-case checklists
Each pattern keeps a checklist, and every problem must cover every item on it that applies. The lists grow as each topic's batch is written. Binary Search comes first:

| Pattern | Edge cases that must be covered |
|---|---|
| All binary search | 1 element · target below the first or above the last element · all elements equal · the answer at index 0 · the answer at the last index · values large enough that `(lo + hi)` overflows 32-bit ints |
| `bounds` | Duplicates at both ends · target missing but between two values · the whole array equal to the target |
| `rotated-array` | Rotated by 0 (not rotated at all) · rotated by n − 1 · 2 elements · the target is the pivot · duplicates (only in problems that allow them) |
| `peak-finding` | Strictly increasing · strictly decreasing · peak at either end · plateaus (only if allowed) |
| `matrix-search` | 1 × n and n × 1 · target at a corner · target missing |
| `search-on-answer` | The answer is the lowest possible value · the answer is the highest possible value · exactly one feasible value · the feasibility check at its limits |
| `real-valued` | Answers near 0 · very large answers · stops at the tolerance, not at an exact value |
| `unknown-size` | Target at index 0 · target at the last index · target missing |
| `kth-element` | k = 1 · k = n · one array empty · arrays of very different lengths · duplicates across both arrays |

## `tests.json`
```json
{
  "problem": "print-shop-daily-limit",
  "version": 1,
  "seed": 20260929,
  "tests": [
    {
      "id": "ex1",
      "visible": true,
      "example": true,
      "kind": "example",
      "input": { "pages": [4, 2, 7, 3, 5], "days": 3 },
      "expected": 8,
      "explanation": "With a limit of 8 the days are [4, 2], [7] and [3, 5]. With 7, [3, 5] needs a fourth day."
    },
    {
      "id": "edge-single",
      "visible": false,
      "kind": "edge",
      "input": { "pages": [500], "days": 1 },
      "expected": 500
    },
    {
      "id": "max-uniform",
      "visible": false,
      "kind": "max",
      "generate": { "args": "--n 50000 --shape uniform" }
    }
  ]
}
```

- `kind` is one of `example`, `sample`, `edge`, `random` or `max`.
- `"no_brute": true` on a stored test skips the brute-force cross-check. Use it for tests with a short input but huge values, where `brute.py` would take forever; the reference still answers them.
- Small tests are stored in full.
- A recipe with `"count": n` stands for `n` tests (`<id>-1` … `<id>-n`), each with its own seed: `{"id": "random", "kind": "random", "generate": {"args": "--n 50", "count": 10}}`.
- Large tests store only a `generate` recipe: `gen.py` arguments, with the file's `seed`. The pipeline builds them, and their expected answers, into a gitignored `build/` folder, so the repo stays small.
- `expected` is omitted for `generate` tests. It always comes from the reference at build time.

## Input formats
- Arguments are named JSON values that match the signature.
- **Linked lists:** a JSON array, e.g. `[1, 2, 3]`. A list with a cycle adds `"cycle_at": index` next to the argument.
- **Trees:** a level-order array with `null` for missing children, e.g. `[3, 9, 20, null, null, 15, 7]`.
- **Graphs:** `n` plus an `edges` array of `[u, v]` or `[u, v, w]`. Nodes are numbered from 0.
- **Design problems:** a list of calls, and the expected result of each call, e.g. `{"calls": [["LRUCache", 2], ["put", 1, 1], ["get", 1]], "expected": [null, null, 1]}`.

## Time limits across languages
`limits.time_ms` is the C++ baseline. The other languages multiply it: C ×1, Java ×2, Python ×4. The pipeline tunes these multipliers during the benchmark run, and they live in one config file, not in each problem.

## Run, Submit and custom tests
- **Run** executes only the visible tests, and shows the input, expected output and actual output side by side for each one.
- **Submit** runs every test and stops at the first failure.
  - If the failing input is small (about 1 KB), it's shown in full.
  - A larger input is summarized instead (e.g. "n = 50,000, uniform"), so hidden tests can't be copied out wholesale.
- **Custom tests:** users can add their own inputs on the Test cases tab.
  - `validator.py` checks the input first, and an invalid one explains which constraint it breaks.
  - The expected answer comes from the reference, so a custom test can never have a wrong answer.
