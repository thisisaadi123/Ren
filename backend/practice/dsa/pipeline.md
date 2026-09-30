# Checking pipeline

> **Status (2026-09-29):** built in `tools/`. `npm run check:dsa` runs checks 1–5 and the gate for 6–7, plus the bank-wide checks; `npm run test:dsa` is the self-test. It isn't wired into CI yet, and when it is, **CI blocks any merge where a check fails.**
>
> - **Languages:** Python, Java, C++ and C (2026-09-30: JavaScript and Go were dropped). Python runs through `runners/py_runner.py`; Java (OpenJDK 21), C++ (clang++, C++17) and C (clang, C11) compile with a generated harness from `lib/java.mjs`, `lib/cpp.mjs` and `lib/c.mjs`. A language whose toolchain is missing is reported as "not checked", and then the problem can't be published. C doesn't take design problems.
> - **Types:** `int`, `long`, `double`, `bool`, `char`, `string` and arrays of them. `ListNode`, `TreeNode` and design problems come with the topics that need them.
> - **Code runs locally,** because the pipeline only runs our own solutions. The sandbox (Judge0 or Piston) is needed for users' code, in the app.

A problem can be set to `status: published` only after it passes every check below. Checks 1–5 are automatic, check 6 is semi-automatic, and check 7 is a person.

| # | Check | Fails when |
|---|---|---|
| 1 | **Schema and paths** | `problem.yaml` doesn't validate against `problem.schema.json`; `topic` or `pattern` isn't in `taxonomy.yaml`; the folder path doesn't match `<topic>/<pattern>/<id>`; a file is missing; `statement.md` has no `{{examples}}` |
| 2 | **Validator** | Any stored or generated test input is rejected by `validator.py` |
| 3 | **Reference vs brute force** | The two disagree on any of 2,000+ random small inputs, or on any stored test small enough for the brute force |
| 4 | **Wrong solutions** | Any file in `wrong/` passes every test |
| 5 | **Every language** | Any solution in `solutions/` gives a different answer from the reference; the reference uses more than half of the time limit in any language; `wrong/too_slow*` doesn't time out |
| 6 | **Blind solve** | A second solver shown only `statement.md` (no reference, no hints) can't solve it, or reads it differently from what the tests expect. The reviewer has to rewrite the statement |
| 7 | **Human review** | Not approved. The reviewer confirms the wording is original and clear, the constraints match `validator.py`, and the difficulty and pattern are right, and adds their name to `reviewed_by` |

## Bank-wide checks
Run on every change:
- The topic counts in `taxonomy.yaml` add up to `total`, pattern ids are unique, and a topic's filled-in pattern counts add up to its count.
- The published problems in each pattern don't go over its target count. Each pattern has at least one Easy problem once it's complete.
- The difficulty mix stays within ±5% of 30 / 50 / 20. This is checked per finished batch, not per problem.
- **Near-duplicate check:** a new statement too similar to any existing problem gets flagged for review.
- `sheets/*.yaml` are valid (see `sheets.md`).

## Where code runs
The pipeline runs **our own** solutions, so it runs them directly on the machine. **Users' code** (the Run and Submit buttons in the app) must run in an open-source sandbox, **Judge0 or Piston**, picked when the Practice backend is built. We don't build our own sandbox: running strangers' code safely (time and memory limits, no network, isolation) is hard to get right. The language runners in `tools/runners/` follow the same one-result-per-test protocol, so they can move into the sandbox.

## Benchmark: proving the pipeline works
**Done as a self-test** (`npm run test:dsa`). It copies a known-good problem into a temporary bank, plants one bug at a time, and confirms `check.mjs` fails at the right check, and no earlier one. The 12 cases are a clean copy (which must pass) plus 11 planted bugs: a missing `{{examples}}`, a pattern from another topic, an input that breaks the constraints, a wrong stored answer, a subtly wrong reference, a far-too-slow reference, a wrong solution the tests miss, a wrong Java answer, a wrong C answer, a C++ compile error, and publishing without a review. All 12 pass.

Running it on `open-r1/codeforces` problems (ODC-By, credited) is still planned, as a check on real-world tests. Those problems read input and print output instead of calling a function, so it needs a small adapter first. That run would plant the same kinds of bug:
- a wrong expected answer
- an input that breaks the constraints
- a test set too weak to catch a known-wrong solution
- a reference solution that's too slow

The pipeline must catch all four. These benchmark problems are **never** shown to users.

## Changing a published problem
- **Any edit bumps `version`.**
- If the tests change, the pipeline reruns every stored accepted solution for that problem against the new tests. Users whose solutions now fail keep their "solved" status, and the answer is flagged "passed an earlier version".
- A problem is never deleted. It's set to `status: retired`, so old progress still resolves.

## After launch
- Every problem has a "Report a problem" link, and reports open an issue against the problem's folder.
- Automatic flags go up when a problem's pass rate is 0% or 100%, or when many users fail the same hidden test. Any of those usually means a bad test or unclear wording.
