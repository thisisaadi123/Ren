"""Fuller explanations for the frequency-map window problems (merged into their sol() calls via sol.EXTRA)."""
from collections import Counter

from sol import EXTRA, Row, fig, table


def text_of(part):
    return "".join(part) if all(isinstance(x, str) for x in part) else " ".join(map(str, part))


TRANSITIONS = """
**Maintaining a summary in O(1).** Recomputing "how many distinct values" or "is anything repeated" from the whole
window costs O(k). Instead keep a count per value plus one summary number, and change the summary only when a count
**crosses a threshold**:

- distinct values change when a count goes 0 → 1 (one more) or 1 → 0 (one fewer);
- repeated values change when a count goes 1 → 2 (one more duplicate) or 2 → 1 (one fewer).

Every other change to a count leaves the summary alone. One value enters and one leaves per slide, so the summary is
updated in O(1).
"""


# ---------------------------------------------------------------- best-unique-bundle
pr, k = [4, 2, 4, 5, 3, 3, 1, 6, 1], 3
cnt, dup, tot, best, brow = Counter(), 0, 0, 0, []
for i, v in enumerate(pr):
    cnt[v] += 1
    dup += cnt[v] == 2
    tot += v
    if i >= k:
        u = pr[i - k]
        cnt[u] -= 1
        dup -= cnt[u] == 1
        tot -= u
    if i >= k - 1:
        if dup == 0:
            best = max(best, tot)
        brow.append((i - k + 1, text_of(pr[i - k + 1:i + 1]), tot, dup, "yes" if dup == 0 else "no", best))
EXTRA["best-unique-bundle"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No window without repeats: return 0.
        - `k = 1`: every single price is a bundle; the answer is the largest price.
        - Totals reach 10¹⁰: use 64 bits.
        """
    ],
    "think": [
        """
        **Two things per window.** Each window of `k` prices needs its total (easy to slide) and a yes/no for "all prices
        different". The second is the new part.
        """,
        TRANSITIONS,
        f"**Every window** for `prices = {pr}`, `k = {k}` (`dup` = how many prices appear twice or more):",
        table(["start", "window", "total", "dup", "all different?", "best"], *brow),
        f"""
        Best bundle **{best}**.

        **Why not just a set?** A set can't handle removals correctly when a value appears twice in the window: removing
        one copy would delete it from the set even though another copy remains. Counts fix that.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For each window, build a set of its prices and add them up; if the set has `k` elements, compare the total with the best. O(k) per window."],
            "complexity": ["**Time O(n · k).** **Space O(k).**"],
        },
        1: {
            "idea": [
                """
                Slide once, keeping `count[price]`, `dup` and `total`. Adding price `v`: `count[v] += 1`, and if it became
                2, `dup += 1`. Removing price `u`: `count[u] −= 1`, and if it became 1, `dup −= 1`. A full window with
                `dup == 0` is a valid bundle.

                **Invariant.** After processing index `i`, the counts, `dup` and `total` describe exactly
                `prices[i − k + 1 .. i]`.
                """
            ],
            "build": [
                "Count array (prices ≤ 10⁵), `dup = 0`, `total = 0`, `best = 0`.",
                "Add `prices[i]`: update count, `dup` on 1 → 2, total.",
                "If `i ≥ k`, remove `prices[i − k]`: update count, `dup` on 2 → 1, total.",
                "If `i ≥ k − 1` and `dup == 0`: `best = max(best, total)`.",
            ],
            "complexity": ["**Time O(n).** **Space O(V)** for the counts (V = 10⁵), or O(k) with a hash map."],
        },
    },
    "takeaways": [
        """
        - **Fixed window + "all distinct":** counts and a duplicate counter.
        - Update summaries only on threshold crossings.
        - **Pitfall:** using a set, which breaks when a value appears twice in the window.
        """
    ],
}


# ---------------------------------------------------------------- every-word-once
ws, words = "catdogcatcatdogdog", ["cat", "dog"]
L = len(words[0])
off_rows = [(off, " | ".join(ws[j:j + L] for j in range(off, len(ws) - L + 1, L))) for off in range(L)]
need = Counter(words)
hits = [i for i in range(len(ws) - len(words) * L + 1) if Counter(ws[i + j * L:i + (j + 1) * L] for j in range(len(words))) == need]
EXTRA["every-word-once"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Duplicate words in the list must be used as many times as they appear.
        - A chunk that isn't a word breaks every chain through it.
        - Results from different offsets interleave, so they must be sorted.
        """
    ],
    "think": [
        f"""
        **Chains are made of fixed-size chunks.** All words have length `L = {L}`, so a chain starting at `i` consists of
        the chunks at `i, i + L, i + 2L, …`. A start `i` and a start `i + L` share every chunk but one: a sliding
        window, but stepping a whole word at a time.

        **Split by offset.** Starts with different remainders mod `L` never share chunks. So run `L` separate windows,
        one per offset. Here are the chunk sequences for `s = "{ws}"`:
        """,
        table(["offset", "chunks"], *off_rows),
        f"""
        In each sequence we look for `{len(words)}` consecutive chunks that use every word the right number of times.
        That's an anagram-style window over words. Matches start at **{hits}**.

        **Three moves per chunk:**

        1. **Unknown chunk:** no chain can contain it, so empty the window and restart after it.
        2. **Over-used word:** the window holds this word more often than allowed; drop words from the left until it
           doesn't. Every chain containing the current chunk must start after the dropped part.
        3. **Window holds all words:** record its start, then drop its first word to keep searching.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For every start, cut the next `w` chunks and compare their counts with the word counts. Correct, but neighbouring starts that share almost every chunk are checked from scratch."],
            "complexity": ["**Time O(n · w · L):** `n` starts, `w` chunks each, `L` characters to hash per chunk. **Space O(w · L).**"],
        },
        1: {
            "idea": [
                """
                For each offset `0..L−1`: walk the chunks, keeping `have[word]`, `used` (words in the window) and `left`.
                Apply the three moves above. Collect every recorded `left`, then sort.

                **Invariant per offset.** The window `s[left .. j + L)` consists of known words, none used more often
                than required. When `used == w` it uses every word exactly as required, which is a chain.

                **Why no chain is missed.** A chain starting at `x` lies on offset `x mod L`. While the window's right end
                walks through the chain, `left` never passes `x` (nothing inside the chain is unknown or over-used), so
                when the last chunk of the chain arrives, the window is exactly that chain.
                """
            ],
            "build": [
                "Word counts `need`.",
                "For each offset: `have = {}`, `left = offset`, `used = 0`.",
                "Unknown chunk → reset. Known → `have[chunk] += 1`, `used += 1`, then drop from the left while over-used.",
                "If `used == w`: record `left`, drop the first word.",
                "Sort and return the starts.",
            ],
            "complexity": [
                """
                **Time O(n · L):** each offset visits about `n / L` chunks; each enters and leaves once and costs O(L) to
                hash. That's `L · (n / L) · L = n · L`. **Space O(w · L)** for the word table.
                """
            ],
        },
    },
    "takeaways": [
        """
        - **Fixed-length tokens → split starts by offset mod `L`** and slide over whole tokens.
        - It's an anagram window over words: counts, shrink on over-use, reset on unknown.
        - Sort at the end when results come from several independent passes.
        """
    ],
}


# ---------------------------------------------------------------- repeat-within-reach
codes, kr = [5, 1, 8, 2, 1, 9, 8, 3], 2
lastpos, rrow = {}, []
for i, c in enumerate(codes):
    prev = lastpos.get(c)
    gap = i - prev if prev is not None else "—"
    rrow.append((i, c, prev if prev is not None else "—", gap, "yes" if prev is not None and i - prev <= kr else "no"))
    lastpos[c] = i
EXTRA["repeat-within-reach"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `k = 0`: two different indexes are never 0 apart, so the answer is false.
        - Codes can be negative and up to 10⁹ in size; no direct array indexing.
        - A code seen long ago but repeated far away doesn't count.
        """
    ],
    "think": [
        f"""
        **Look back, not forward.** At position `j`, the question is whether `codes[j]` occurred among the previous `k`
        positions. Among all earlier copies, the **most recent** one is the closest, so it's the only one worth
        checking. A map from code to last index answers that in O(1).

        **Trace** for `codes = {codes}`, `k = {kr}`:
        """,
        table(["i", "code", "last seen", "gap", "within k?"], *rrow),
        """
        No gap is at most `k`, so the answer is **false**.

        **The window view.** Equivalently, keep a set of the last `k` codes: add the new code after checking it, and
        remove the code that falls out of reach. That uses O(k) memory instead of O(n); the last-index map is simpler
        to write.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For each position, compare its code with the next `k` codes. Up to `n · k` comparisons."],
            "complexity": ["**Time O(n · k).** **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Sort positions by `(code, position)`. Equal codes become neighbours, in increasing position order, and for
                each code the closest pair of positions is adjacent in that order. So one pass over neighbours checks
                every candidate pair.
                """
            ],
            "complexity": ["**Time O(n log n)** for the sort. **Space O(n).**"],
        },
        2: {
            "idea": [
                """
                Scan left to right with `last[code]`. If the code was seen and `i − last[code] ≤ k`, return true; then set
                `last[code] = i`.

                **Why updating to the newest index is safe.** For any future position, a newer index of the same code is
                always at least as close as an older one, so the older index can be forgotten.

                In C, a small open-addressing hash table plays the role of the map.
                """
            ],
            "build": [
                "Empty map `last`.",
                "For each `i`: look up `codes[i]`; if found and `i − last ≤ k`, return true.",
                "Store `last[codes[i]] = i`.",
                "Return false after the scan.",
            ],
            "complexity": ["**Time O(n)** expected. **Space O(n)** (O(k) for the set-of-last-k variant)."],
        },
    },
    "takeaways": [
        """
        - **"Duplicate within distance k":** last-index map, or a sliding set of the last `k` items.
        - Only the most recent occurrence matters.
        - Sorting `(value, index)` pairs is the fallback when hashing isn't available.
        """
    ],
}


# ---------------------------------------------------------------- scrambled-copies
tx, wd = "baacabcaab", "abc"
m = len(wd)
nd, hv, srow = Counter(wd), Counter(), []
letters = sorted(set(wd) | set(tx))
for i, c in enumerate(tx):
    hv[c] += 1
    if i >= m:
        hv[tx[i - m]] -= 1
    if i >= m - 1:
        diff = sum(1 for x in letters if hv[x] != nd[x])
        srow.append((i - m + 1, tx[i - m + 1:i + 1], " ".join(f"{x}{hv[x] - nd[x]:+d}" for x in letters), diff, "match" if diff == 0 else ""))
EXTRA["scrambled-copies"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `word` longer than `text`: no matches.
        - Overlapping matches all count (`"abab"` with `"ab"` gives 0, 1 and 2).
        - Letters that aren't in `word` at all make a window fail.
        """
    ],
    "think": [
        f"""
        **Rearrangements share letter counts.** A window is a scrambled copy of `word` exactly when it contains each
        letter the same number of times. All candidate windows have length `m = {m}`: a fixed-size window.

        **One signed array.** Keep `delta[c] = (count of c in window) − (count of c in word)`. A window matches when every
        `delta` is 0. Instead of checking 26 entries, keep `diff` = how many letters have a non-zero `delta`; a change to
        one letter's `delta` moves `diff` only when that `delta` leaves 0 or arrives at 0.

        **Every window** of `"{tx}"` (deltas shown for the letters involved):
        """,
        table(["start", "window", "delta", "diff", ""], *srow),
        f"Matches start at **{[r[0] for r in srow if r[3] == 0]}**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each start, count the window's letters into a fresh 26-array and compare it with the word's array. O(m) per window."],
            "complexity": ["**Time O(n · m).** **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Start with `delta[c] = −(count of c in word)` and `diff` = number of letters in `word`'s alphabet. A helper
                `bump(c, ±1)` adjusts `delta[c]` and fixes `diff`: if it was 0 before, `diff += 1`; if it's 0 after,
                `diff −= 1`. Slide: bump the entering letter by +1 and the leaving one by −1. A full window with
                `diff == 0` is a match.

                **Invariant.** `diff` always equals the number of letters whose window count differs from the word's
                count.
                """
            ],
            "build": [
                "`delta` from the word (negative counts) and the initial `diff`.",
                "`bump(c, by)` keeps `diff` in sync on 0 crossings.",
                "For each `i`: bump `text[i]` by +1; if `i ≥ m`, bump `text[i − m]` by −1.",
                "If `i ≥ m − 1` and `diff == 0`, record `i − m + 1`.",
            ],
            "complexity": ["**Time O(n + m).** **Space O(1)**: 26 counters."],
        },
    },
    "takeaways": [
        """
        - **Anagram windows:** fixed size + letter balance.
        - **A mismatch counter** turns a 26-way comparison into O(1).
        - One signed `delta` array replaces separate "need" and "have" arrays.
        """
    ],
}


# ---------------------------------------------------------------- variety-per-window
it, kv = [4, 1, 4, 4, 7, 1, 7, 2], 3
cv, dist, vrow = Counter(), 0, []
for i, v in enumerate(it):
    cv[v] += 1
    entered = cv[v] == 1
    dist += entered
    left_txt = "—"
    if i >= kv:
        u = it[i - kv]
        cv[u] -= 1
        gone = cv[u] == 0
        dist -= gone
        left_txt = f"{u}" + (" (gone)" if gone else " (still present)")
    if i >= kv - 1:
        vrow.append((i - kv + 1, text_of(it[i - kv + 1:i + 1]), f"{v}" + (" (new)" if entered else " (already present)"), left_txt, dist))
EXTRA["variety-per-window"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `k = 1`: every answer is 1.
        - `k = n`: a single answer, the number of distinct values overall.
        - Values up to 10⁹: hash map or compression, not a direct array.
        """
    ],
    "think": [
        """
        **What changes per slide.** One item enters and one leaves, and the number of distinct types changes only if
        the entering type wasn't in the window or the leaving item was the last of its type.
        """,
        TRANSITIONS,
        f"**Trace** for `items = {it}`, `k = {kv}`:",
        table(["window start", "window", "entered", "left", "distinct"], *vrow),
        """
        **Order of operations.** Add the entering item first and remove the leaving one second (or the reverse); both give
        the right count, as long as each update adjusts `distinct` on its own 0 ↔ 1 crossing.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For each window, build a set and take its size. O(k) per window."],
            "complexity": ["**Time O(n · k).** **Space O(k).**"],
        },
        1: {
            "idea": [
                """
                Keep `count[type]` and `distinct`. For each `i`: add `items[i]` (0 → 1 raises `distinct`); if `i ≥ k`,
                remove `items[i − k]` (1 → 0 lowers it); if `i ≥ k − 1`, append `distinct`.

                **Invariant.** After step `i`, the counts describe `items[i − k + 1 .. i]` and `distinct` is the number of
                positive counts.
                """
            ],
            "build": [
                "Map of counts, `distinct = 0`, output list.",
                "Add the entering item; adjust `distinct` on 0 → 1.",
                "Remove the leaving item (once the window is longer than `k`); adjust on 1 → 0.",
                "Append `distinct` for every full window.",
            ],
            "complexity": ["**Time O(n)** expected (C sorts once to compress values: O(n log n)). **Space O(k)** for the map."],
        },
    },
    "takeaways": [
        """
        - **Distinct count per window:** counts + a counter updated on 0 ↔ 1.
        - The same machinery powers "at most k distinct" and "exactly k distinct".
        - Large values: hash map, or compress once.
        """
    ],
}
