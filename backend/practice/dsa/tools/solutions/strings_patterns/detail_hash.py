"""In-depth text for the rolling-hash problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

digits, kd = "31415926", 3
roll_rows = []
v = int(digits[:kd])
roll_rows.append((digits[:kd], "—", "—", "—", v))
for i in range(kd, len(digits)):
    out, inc = int(digits[i - kd]), int(digits[i])
    dropped = v - out * 10 ** (kd - 1)
    nv = dropped * 10 + inc
    roll_rows.append((digits[i - kd + 1:i + 1], f"{v} − {out}·100 = {dropped}", f"{dropped}·10 = {dropped * 10}", f"+ {inc}", nv))
    v = nv

POLY = """
**A string as a number.** Read the letters as digits of a number in some base `B`:
`hash("abc") = a·B² + b·B + c`, taken modulo a large prime `M` so it stays small. Equal strings always get equal
hashes. Different strings *usually* get different hashes; a **collision** (different strings, same hash) is possible
but rare when `M` is large.

**Why it's called rolling.** Moving a length-`k` window one step right is the same as what happens to a number
when you drop its leading digit and append a new one. With base 10 and digits, the window `314` becomes `141`:
"""

ROLL_TABLE = table(["window", "remove the leading digit", "shift left", "append", "value"], *roll_rows)

AFTER_ROLL = """
With letters it's the same: `h = (h − out · B^(k−1)) · B + in`, all modulo `M`. One subtraction, one multiplication and
one addition, whatever `k` is.

**Making collisions negligible.** With one prime near 10⁹, about 10¹⁰ pairs of windows could accidentally collide
with chance around 1/10⁹ each, which is too risky. Using **two different primes** and comparing both hashes makes a
collision as unlikely as a random guess in about 10¹⁸. Both hashes are below 2³⁰, so they pack into one 64-bit key
`(h1 << 32) | h2`.

**Keeping arithmetic in range.** Products like `h · B` and `out · B^(k−1)` stay below about 1.3 × 10¹¹, safely inside
64 bits. After subtracting, add `M` before taking `% M` so the value can't go negative (Python's `%` is already
non-negative).
"""

PREFIX = """
**Any substring's hash in O(1).** Store prefix hashes `pre[i]` (the hash of the first `i` letters) and powers
`pw[L] = B^L`. Then `hash(s[i .. i+L)) = pre[i+L] − pre[i] · pw[L]` (mod `M`): the prefix up to `i + L`, minus the
part before `i` shifted up by `L` places, exactly like removing the leading digits of a number.
"""

MONO = """
**Why binary search on the length is allowed.** If some substring of length `L` works, then dropping its last letter
gives a substring of length `L − 1` that also works (both copies lose the same letter). So the lengths that work are
exactly `0, 1, …, answer`, and the question "does length `L` work?" is **true up to the answer and false after it**.
That monotone shape is what binary search needs: about `log₂ n ≈ 15` tests instead of `n`.
"""


# ---------------------------------------------------------------- distinct-windows
s, k = "abcabcba", 3
wins = [s[i:i + k] for i in range(len(s) - k + 1)]
seen, drow = [], []
for i, w in enumerate(wins):
    new = w not in seen
    if new:
        seen.append(w)
    drow.append((i, w, "new" if new else "seen before", len(seen)))
EXTRA["distinct-windows"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `k = n`: one window, answer 1.
        - All letters equal: every window is the same, answer 1.
        - Large `k`: storing each window's text costs `(n − k + 1) · k` characters, up to 2.5 × 10⁹.
        """
    ],
    "think": [
        f"""
        **Restating it.** There are `n − k + 1` windows; count how many different strings appear among them.

        **By hand** for `"{s}"`, `k = {k}`:
        """,
        table(["start", "window", "status", "different so far"], *drow),
        f"""
        Answer **{len(seen)}**.

        **The bottleneck.** A set of window strings works, but every window costs O(k) to copy and hash. We want a
        fingerprint per window that updates in O(1) as the window slides.
        """,
        POLY,
        ROLL_TABLE,
        AFTER_ROLL,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Put each window's text in a hash set and return its size. C has no string set, so it sorts pointers to
                the windows by their first `k` letters and counts where neighbours differ.

                It's exact (no collisions), which makes it a good reference.
                """
            ],
            "build": [
                "Slice or point at every window.",
                "De-duplicate with a set (or sort and compare neighbours in C).",
                "Return the number of different windows.",
            ],
            "complexity": ["**Time O(n · k)** to build and hash the windows (C: O(n · k · log n) for the sort). **Space O(n · k)** for the copies (C keeps only pointers)."],
            "limits": ["Each window costs O(k) to hash or compare. With `n = 10⁵` and `k = 5 × 10⁴` that's billions of character operations. A rolling hash gives each window a fingerprint in O(1)."],
            "lines": {
                "set": "Every window's text goes into a set, which keeps one copy of each distinct string. C points at each window's start instead of copying it.",
                "sort": "C only: sorting the window pointers with `strncmp` over `k` letters puts equal windows next to each other.",
                "count": "C only: every place where neighbours differ starts a new distinct window.",
            },
        },
        1: {
            "idea": [
                """
                Compute two hashes of the first window, then roll both across the string. Pack each pair into a 64-bit key
                and insert it into a set; the set's size is the answer.

                **Invariant.** After processing position `i`, `(h1, h2)` are the hashes of `s[i − k + 1 .. i]`. They start
                correct for the first window, and the rolling formula keeps them correct for each next one.
                """
            ],
            "build": [
                "Choose two primes and a base larger than any letter code; precompute `B^(k−1)` mod each prime.",
                "Hash the first window and insert its key.",
                "For each next letter: roll both hashes, insert the key.",
                "Return the number of distinct keys (C: sort the keys and count changes).",
            ],
            "complexity": ["**Time O(n)** expected with a hash set (C: O(n log n) with the sort). **Space O(n)** for the keys."],
            "lines": {
                "init": "Two primes, a base (131 is larger than any letter code), and `top = B^(k−1)`, the weight of a window's first letter.",
                "first": "Hash the first window like reading a number digit by digit, and record its key. Both hashes are below 2³⁰, so `(h1 << 32) | h2` is a unique 64-bit key for the pair.",
                "roll": "Remove the leaving letter's weight (`out · top`), shift everything up one place (`· B`), add the new letter. Adding `M` before `% M` keeps the value non-negative in Java, C++ and C.",
                "ret": "The number of different keys, which (barring a negligible collision) is the number of different windows.",
            },
        },
    },
    "takeaways": [
        """
        - **Recognise it:** many comparisons of equal-length substrings.
        - **Template:** hash the first window, then `h = (h − out·B^(k−1))·B + in` mod `M`.
        - **Pitfalls:** a single small modulus (collisions); negative values after subtracting; overflow from multiplying
          two values that are each near 10⁹ without 64 bits.
        - **Related:** Rabin–Karp pattern search uses the same rolling hash to find a pattern.
        """
    ],
}


# ---------------------------------------------------------------- longest-repeat
s2 = "mississippi"
n2 = len(s2)


def repeat_of(L):
    first = {}
    for i in range(n2 - L + 1):
        w = s2[i:i + L]
        if w in first:
            return w, first[w], i
        first[w] = i
    return None


brow, lo, hi = [], 0, n2 - 1
while lo < hi:
    mid = (lo + hi + 1) // 2
    r = repeat_of(mid)
    brow.append((f"{lo}..{hi}", mid, f"yes: '{r[0]}' at {r[1]} and {r[2]}" if r else "no", f"answer ≥ {mid}" if r else f"answer < {mid}"))
    lo, hi = (mid, hi) if r else (lo, mid - 1)
ans2 = lo
shift_rows = []
for d in range(1, n2):
    run = top = end = 0
    for i in range(n2 - d):
        run = run + 1 if s2[i] == s2[i + d] else 0
        if run > top:
            top, end = run, i
    shift_rows.append((d, top, s2[end - top + 1:end + 1] if top else "—"))
EXTRA["longest-repeat"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - All letters different: no repeat, answer 0.
        - The two copies may overlap: in `"aaaa"` the answer is 3 (`aaa` at 0 and 1).
        - The answer is at most `n − 1`, since two copies need two different starts.
        """
    ],
    "think": [
        f"""
        **Restating it.** Find the largest `L` such that two different starting positions have the same length-`L`
        substring.

        **A first view: compare the string with its shifts.** If a substring occurs at `i` and at `i + d`, then `s` and
        `s` shifted by `d` agree on a run of `L` positions. So the answer is the longest run of agreement over all
        shifts `d`:
        """,
        table(["shift d", "longest agreeing run", "substring"], *shift_rows),
        f"""
        The best is {ans2} (`issi`). That view is exact but costs O(n²).
        """,
        MONO,
        f"**Binary search on `\"{s2}\"`:**",
        table(["range", "try L", "repeated?", "conclusion"], *brow),
        f"Answer **{ans2}**.",
        PREFIX,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                For every shift `d ≥ 1`, walk `i` from 0 and track the current run of positions where
                `s[i] = s[i + d]`. Each run is a substring that appears at `i − run + 1` and `d` places later. The longest
                run over all shifts is the answer.
                """
            ],
            "build": ["Loop over shifts `d = 1 … n − 1`.", "Track the run of agreements.", "Keep the longest run."],
            "complexity": ["**Time O(n²):** `n − d` comparisons for each shift, about 4.5 × 10⁸ for `n = 3 × 10⁴`. **Space O(1).**"],
            "limits": ["Every shift is scanned in full. Binary search needs only about 15 length tests, each linear with hashing."],
            "lines": {
                "init": "No repeat found yet.",
                "shift": "Two copies of a repeated substring are `d` apart for some `d ≥ 1`; reset the run for each shift.",
                "run": "Extend the run when `s` agrees with its shift, reset it on a mismatch. A run of length `r` ending at `i` means `s[i−r+1..i]` equals `s[i−r+1+d..i+d]`.",
                "ret": "The longest agreement over all shifts.",
            },
        },
        1: {
            "idea": [
                """
                Precompute prefix hashes and powers for two primes. `repeats(L)` hashes all `n − L + 1` windows of length
                `L` in O(1) each and reports whether any key appears twice. Binary search finds the largest `L` with
                `repeats(L)` true.

                **Search details.** Keep `lo` = a length known to work (0 always does) and `hi` = the largest length still
                possible. Test `mid = (lo + hi + 1) / 2`, rounding up so `lo = mid` always makes progress.
                """
            ],
            "build": [
                "Prefix hashes and powers for both primes.",
                "`repeats(L)`: compute each window key; a duplicate means yes.",
                "Binary search `lo = 0`, `hi = n − 1` for the last `true`.",
            ],
            "complexity": ["**Time O(n log n)** expected: about 15 tests of O(n) each (C sorts the keys: O(n log² n)). **Space O(n).**"],
            "lines": {
                "prefix": "Prefix hashes for both primes and the matching powers of `B`, so any substring's key costs O(1).",
                "test": "For length `L`, compute each window's key from the prefixes. A key seen before means a repeated substring of that length. C sorts the keys and looks for equal neighbours.",
                "search": "The lengths that repeat are `0 … answer`, so binary search the last one that does. `mid` rounds up so the loop always shrinks the range.",
                "ret": "The longest repeated length.",
            },
        },
    },
    "takeaways": [
        """
        - **"Longest X that appears twice / in both" → binary search on the length + a linear test.**
        - Prefix hashes give every substring's fingerprint in O(1).
        - **Pitfalls:** rounding `mid` down (infinite loop with `lo = mid`); collisions with one small modulus.
        - **Related:** suffix arrays with LCP answer it exactly in O(n log n).
        """
    ],
}


# ---------------------------------------------------------------- shared-tune
a, b = "abcdxyz", "xyzabcq"
dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
for i in range(1, len(a) + 1):
    for j in range(1, len(b) + 1):
        if a[i - 1] == b[j - 1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
ans3 = max(max(r) for r in dp)
grid = [[a[i - 1]] + [dp[i][j] or "·" for j in range(1, len(b) + 1)] for i in range(1, len(a) + 1)]


def shared_of(L):
    sa = {a[i:i + L] for i in range(len(a) - L + 1)}
    return next((b[j:j + L] for j in range(len(b) - L + 1) if b[j:j + L] in sa), None)


srow, lo, hi = [], 0, min(len(a), len(b))
while lo < hi:
    mid = (lo + hi + 1) // 2
    r = shared_of(mid)
    srow.append((f"{lo}..{hi}", mid, f"yes: '{r}'" if r else "no", f"answer ≥ {mid}" if r else f"answer < {mid}"))
    lo, hi = (mid, hi) if r else (lo, mid - 1)
EXTRA["shared-tune"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No letter in common: 0.
        - One song inside the other: the shorter song's length.
        - Several equally long shared runs: only the length is needed.
        """
    ],
    "think": [
        f"""
        **Restating it.** The longest common substring of `a` and `b` (contiguous, unlike a subsequence).

        **The table view.** Let `run[i][j]` be the length of the common run that **ends** at `a[i−1]` and `b[j−1]`. If
        those letters match, it extends the run ending one step earlier in both strings; otherwise it's 0. For
        `a = "{a}"` (rows) and `b = "{b}"` (columns):
        """,
        table(["a \\ b"] + list(b), *grid),
        f"""
        The largest cell is **{ans3}** (both `abc` and `xyz`). The table is exact but has `|a| · |b|` cells: 4 × 10⁸ at
        the limits.
        """,
        MONO.replace("both copies lose the same letter", "the shared run stays shared without its last letter"),
        "**Binary search here:**",
        table(["range", "try L", "shared?", "conclusion"], *srow),
        PREFIX,
        """
        **Testing one length.** Put the keys of all length-`L` windows of `a` into a set, then look up every length-`L`
        window of `b`. Any hit means a shared run of length `L`.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Fill the `run` table row by row, keeping only the previous row, and track the largest value. Each cell is
                O(1), so it's simple and exact, but the number of cells is the problem.
                """
            ],
            "build": ["Two rows of length `|b| + 1`.", "`cur[j] = prev[j−1] + 1` on a match, else 0.", "Track the maximum; swap rows."],
            "complexity": ["**Time O(|a| · |b|):** 4 × 10⁸ cells at the limits. **Space O(|b|).**"],
            "limits": ["Quadratic in the input size. Binary search on the length needs about 15 linear hash passes."],
            "lines": {
                "init": "The previous row of the table, all zeros (no letters of `a` used yet).",
                "fill": "One row per letter of `a`; when a row is finished it becomes the previous row.",
                "rule": "Matching letters extend the run ending one step earlier in both strings; a mismatch breaks it to 0. Track the largest cell.",
                "ret": "The longest shared run.",
            },
        },
        1: {
            "idea": [
                """
                Build prefix hashes (two primes) for both songs and shared powers of `B`. For a length `L`, insert all of
                `a`'s window keys into a set and check `b`'s windows against it. Binary search the largest `L` that is
                shared.

                **Why the lookup direction doesn't matter.** We could store `b`'s windows and scan `a` instead; storing the
                shorter song's windows uses less memory.
                """
            ],
            "build": [
                "Powers up to the longer song; prefix hashes of both songs for both primes.",
                "`shared(L)`: set of `a`'s keys, then look up `b`'s keys.",
                "Binary search `lo = 0`, `hi = min(|a|, |b|)`.",
            ],
            "complexity": ["**Time O((|a| + |b|) · log min(|a|, |b|))** expected (an extra log factor in C, which sorts and binary-searches). **Space O(|a| + |b|).**"],
            "lines": {
                "prefix": "Powers of `B` up to the longer song, and prefix hashes of both songs for both primes.",
                "test": "For length `L`, collect every window key of `a`, then check whether any window of `b` has a key in that collection. C sorts `a`'s keys and binary-searches each of `b`'s.",
                "search": "Shared lengths are `0 … answer`; find the last one. `mid` rounds up so `lo = mid` makes progress.",
                "ret": "The longest shared run.",
            },
        },
    },
    "takeaways": [
        """
        - **Longest common substring:** binary search on the length + hashing beats the O(n·m) table.
        - It's the same template as "longest repeated substring", with two strings instead of one.
        - **Pitfalls:** confusing substring (contiguous) with subsequence; comparing hashes from different moduli.
        """
    ],
}
