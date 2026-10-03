"""In-depth text for the expand-around-centre problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, Row, fig, table


def is_pal(t):
    return t == t[::-1]


def centre_rows(s):
    """One row per centre: where it is, palindromes found there, widest one, and what stopped it."""
    n, rows = len(s), []
    for c in range(2 * n - 1):
        i, j = c // 2, c // 2 + c % 2
        found = []
        while i >= 0 and j < n and s[i] == s[j]:
            found.append(s[i:j + 1])
            i, j = i - 1, j + 1
        where = f"letter {c // 2} ({s[c // 2]})" if c % 2 == 0 else f"gap {c // 2}|{c // 2 + 1}"
        stop = f"{s[i]} ≠ {s[j]}" if i >= 0 and j < n else "edge"
        rows.append((where, ", ".join(found) or "—", len(found), stop))
    return rows


CENTRES = """
**Every palindrome has a centre.** Fold a palindrome in half: an odd-length one folds on its middle letter
(`aba` on `b`), an even-length one folds on the gap between its two middle letters (`abba` between the `b`s). A string
of length `n` has `n` letters and `n − 1` gaps, so **2n − 1 centres**. Every palindromic substring belongs to exactly
one of them.

**Growing from a centre.** If `s[i..j]` is a palindrome, then `s[i−1..j+1]` is one exactly when `s[i−1] = s[j+1]`.
So from a centre we compare the two letters just outside, extend if they match, and stop at the first mismatch: a
mismatch at distance `d` means nothing wider around this centre can be a palindrome, because it would contain that
mismatched pair at mirrored positions.
"""

# ---------------------------------------------------------------- count-mirrors
s = "abaab"
n = len(s)
rows = centre_rows(s)
total = sum(r[2] for r in rows)
grid_head = ["i \\ j"] + [f"{j} ({s[j]})" for j in range(n)]
grid = [[f"{i} ({s[i]})"] + [("✓" if is_pal(s[i:j + 1]) else "·") if j >= i else "" for j in range(n)] for i in range(n)]

EXTRA["count-mirrors"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A single letter counts, so the answer is at least `n`.
        - Equal substrings at different positions count separately: `"aaa"` has 6 (three `a`, two `aa`, one `aaa`).
        - All letters equal is the worst case: every substring is a palindrome, `n(n + 1)/2` of them.
        """
    ],
    "think": [
        f"""
        **Restating it.** Count the pairs `(i, j)` with `i ≤ j` such that `s[i..j]` reads the same both ways.
        """,
        CENTRES,
        f"**All 2n − 1 = {2 * n - 1} centres of `\"{s}\"`:**",
        table(["centre", "palindromes found", "count", "stopped by"], *rows),
        f"""
        Adding the counts gives **{total}**.

        **Where brute force wastes work.** Testing each substring separately re-checks its inside: to test `abaab` you
        compare `a…b`, and to test `baa` you compare `b…a`, again and again for overlapping substrings. Growing outward
        from centres tests each matching pair of letters exactly once per centre.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Enumerate every substring `s[i..j]` and test it with two pointers moving inward. Count the ones that
                pass.

                It's a correct baseline: every substring is examined, so nothing is missed or double-counted.
                """
            ],
            "build": [
                "Two nested loops pick `i ≤ j`.",
                "Two pointers `a = i`, `b = j` move inward while `s[a] = s[b]`.",
                "If they meet or cross, the substring is a palindrome: count it.",
            ],
            "complexity": [
                "**Time O(n³):** about `n²/2` substrings, each tested in up to `n/2` comparisons; all-equal strings hit the worst case. For `n = 2000` that's around 10⁹ steps. **Space O(1).**"
            ],
            "limits": ["Each substring is tested from scratch, although its inside is a shorter substring that was already tested. Either remember those results (a table) or grow palindromes from their centres."],
            "lines": {
                "init": "The number of palindromic substrings found so far.",
                "all": "Every substring `s[i..j]`, including single letters (`i = j`).",
                "test": "Compare from both ends toward the middle. If a mismatch appears, `a < b` stays true and the substring isn't counted. If the pointers meet or cross, every mirrored pair matched.",
                "ret": "The total.",
            },
        },
        1: {
            "idea": [
                """
                Let `pal[i][j]` say whether `s[i..j]` is a palindrome. Then:

                - substrings of length 1 or 2: `pal[i][j]` is `s[i] == s[j]`;
                - longer ones: `pal[i][j]` is `s[i] == s[j]` **and** `pal[i+1][j−1]`.

                Fill the table so that `pal[i+1][j−1]` is ready before `pal[i][j]`: rows from the bottom (`i` from `n − 1`
                down to 0), and within a row `j` from `i` upwards. Count the true cells. For `"{s}"` the table is:
                """.replace("{s}", s),
                table(grid_head, *grid),
                f"There are {total} ticks, matching the centre count.",
            ],
            "build": [
                "An `n × n` table of booleans.",
                "For `i` from `n − 1` down to 0, for `j` from `i` to `n − 1`: apply the rule.",
                "Count every true cell as it's set.",
            ],
            "complexity": ["**Time O(n²):** one O(1) rule per cell. **Space O(n²):** 4 × 10⁶ cells for `n = 2000`, which is 4 MB as bytes but much more if stored as objects."],
            "limits": ["The table holds `n²` entries, yet each cell is read only once, by the cell diagonally outside it. Expanding from centres follows exactly those diagonals without storing them."],
            "lines": {
                "init": "The table, initially all false, and the count. C uses one flat array of `n · n` bytes.",
                "fill": "Rows from the bottom up guarantee that row `i + 1` is complete when row `i` needs `pal[i+1][j−1]`.",
                "rule": "The two ends must match, and what's inside them must be a palindrome. For lengths 1 and 2 the inside is empty, so `j − i < 2` skips the lookup.",
                "ret": "Every true cell is one palindromic substring.",
            },
        },
        2: {
            "idea": [
                """
                Loop over centres `c = 0 … 2n − 2`. Even `c` sits on letter `c/2` (start with `i = j = c/2`); odd `c` sits
                on the gap after letter `c/2` (start with `i = c/2`, `j = c/2 + 1`). While `i ≥ 0`, `j < n` and
                `s[i] = s[j]`, the substring `s[i..j]` is a palindrome: count it and widen by one on each side.

                **Why every palindrome is counted exactly once.** A palindrome `s[i..j]` has one centre, `c = i + j`. At
                that centre the expansion reaches `s[i..j]` because every inner mirrored pair also matches, and no other
                centre can produce the same `(i, j)`.
                """
            ],
            "build": [
                "Loop over the `2n − 1` centres and compute the starting `i`, `j` from `c`.",
                "Expand while the letters match, counting each step.",
                "Return the total.",
            ],
            "complexity": [
                """
                **Time O(n²) worst case, often much less.** Each centre does as many steps as there are palindromes around
                it, so the total work equals the answer plus `2n − 1` failed checks. For all-equal strings that's
                `n(n + 1)/2`; for typical text it's close to linear. **Space O(1).**
                """
            ],
            "lines": {
                "init": "The count.",
                "centre": "`c // 2` is the left starting index; `c % 2` adds 1 for gap centres, so odd `c` starts with two different letters `s[i]`, `s[i + 1]`.",
                "expand": "Each successful comparison confirms one more palindrome around this centre. The first mismatch, or the edge of the string, ends this centre for good.",
                "ret": "The total.",
            },
        },
    },
    "takeaways": [
        """
        - **Recognise it:** anything about palindromic substrings: counting them, the longest one, checking many.
        - **Template:** loop `c` over `0..2n−2`, set `i = c/2`, `j = i + c%2`, expand while they match.
        - **Pitfalls:** forgetting even-length palindromes (gap centres); using the DP table when memory is tight.
        - **Related:** Manacher's algorithm reuses mirror information to make the same count O(n).
        """
    ],
}


# ---------------------------------------------------------------- longest-echo and longest-echo-text
def longest_detail(pid, s, as_text):
    rows = centre_rows(s)
    best_len, best_i = 1, 0
    widest = []
    for c in range(2 * len(s) - 1):
        i, j = c // 2, c // 2 + c % 2
        while i >= 0 and j < len(s) and s[i] == s[j]:
            i, j = i - 1, j + 1
        widest.append(s[i + 1:j] or "—")
        if j - i - 1 > best_len:
            best_len, best_i = j - i - 1, i + 1
    want = s[best_i:best_i + best_len]
    shown = f"`\"{want}\"`" if as_text else f"**{best_len}**"
    tie = """
        - **Ties:** if two palindromes share the greatest length, return the one that starts first. Centres are visited
          left to right, and a strictly longer palindrome is needed to replace the best, so the first one found stays.
        """ if as_text else """
        - Only the length is asked for, so ties don't matter.
        """
    EXTRA[pid] = {
        "question_more": [
            """
            **Edge cases to keep in mind**

            - A single letter is a palindrome, so the answer is at least 1 letter long.
            - All letters equal: the whole string.
            """ + tie
        ],
        "think": [
            f"""
            **Restating it.** Among all substrings that read the same both ways, find the longest
            ({"return the substring itself" if as_text else "return its length"}).
            """,
            CENTRES,
            f"**The widest palindrome around each centre of `\"{s}\"`:**",
            table(["centre", "widest palindrome", "length", "stopped by"], *[(r[0], w, len(w) if w != "—" else 0, r[3]) for r, w in zip(rows, widest)]),
            f"""
            The longest is `{want}`, so the answer is {shown}.

            **Only the widest per centre matters.** Every palindrome around a centre is contained in the widest one, so
            for the longest overall we just need, for each centre, how far it expands. And the brute-force idea of
            testing substrings from the longest down wastes time re-checking insides that the expansion verifies once.
            """,
        ],
        "approaches": {
            0: {
                "idea": [
                    """
                    For each start `i`, test ends `j` that would beat the current best (`j ≥ i + best`), each with a
                    two-pointer palindrome test. Record a palindrome when it's strictly longer than the best.

                    Skipping ends that can't beat the best already prunes a lot, but each test is still O(n).
                    """
                ],
                "build": [
                    "The best starts as the first letter (length 1).",
                    "For each `i`, for each `j ≥ i + best`, test `s[i..j]` with two pointers.",
                    "On success, set the best to `(j − i + 1, i)`.",
                ],
                "complexity": ["**Time O(n³)** in the worst case (many long near-palindromes). **Space O(1).**"],
                "limits": ["Every test starts again from the ends of the substring. Growing outward from centres verifies each mirrored pair once."],
                "lines": {
                    "init": "One letter is always a palindrome, so the best is length 1 at position 0.",
                    "all": "Only ends far enough to beat the best are worth testing; this also keeps the leftmost of equal-length palindromes.",
                    "test": "Two pointers from the ends inward; meeting without a mismatch means a palindrome, which is strictly longer than the best by construction.",
                    "ret": "Return " + ("the substring (C copies it into a new buffer)." if as_text else "the length."),
                },
            },
            1: {
                "idea": [
                    """
                    For each centre, expand while the letters match. When it stops, the palindrome is `s[i+1 .. j−1]` with
                    length `j − i − 1`. Keep it if it's strictly longer than the best.

                    **Why it's correct.** The longest palindrome has some centre, and expanding from that centre reaches
                    its full width (all its mirrored pairs match). So it's measured at its centre and kept.
                    """
                ],
                "build": [
                    "Best = (1, 0).",
                    "For each centre `c`, set `i = c/2`, `j = i + c%2` and expand.",
                    "After expanding, compare `j − i − 1` with the best length.",
                    "Return " + ("the best substring." if as_text else "the best length."),
                ],
                "complexity": ["**Time O(n²)** worst case: the expansions add up to at most the number of palindromic substrings. **Space O(1)**: only indices are stored, and the substring is cut once at the end."],
                "lines": {
                    "init": "The best palindrome so far: one letter at position 0.",
                    "centre": "Even `c` starts on a letter, odd `c` on a gap.",
                    "expand": "Widen while the outer letters match. When the loop ends, `s[i]` and `s[j]` are the mismatched (or missing) pair, so the palindrome is the part strictly between them.",
                    "keep": "Only a strictly longer palindrome replaces the best, so " + ("the leftmost one wins ties." if as_text else "the stored length is the maximum."),
                    "ret": "Return " + ("the substring, cut out once at the end (C copies it into a new buffer)." if as_text else "the length."),
                },
            },
        },
        "takeaways": [
            """
            - **Longest palindromic substring:** expand around all `2n − 1` centres, O(n²) time, O(1) memory.
            - Track `(length, start)` and cut the substring once at the end.
            - **Pitfalls:** missing even-length centres; off-by-one in `j − i − 1`.
            - **Related:** Manacher's algorithm gives the same answer in O(n).
            """
        ],
    }


longest_detail("longest-echo", "abacdcaba", False)
longest_detail("longest-echo-text", "xabbaycdcz", True)


# ---------------------------------------------------------------- palindrome-census
s4 = "aabaa"
t = "^#" + "#".join(s4) + "#$"
p = [0] * len(t)
c0 = r0 = 0
mirror_note = None
for i in range(1, len(t) - 1):
    head = 0
    if i < r0:
        head = min(r0 - i, p[2 * c0 - i])
        p[i] = head
    while t[i + p[i] + 1] == t[i - p[i] - 1]:
        p[i] += 1
    if head and mirror_note is None:
        mirror_note = (i, 2 * c0 - i, c0, r0, head, p[i])
    if i + p[i] > r0:
        c0, r0 = i, i + p[i]
census = sum((x + 1) // 2 for x in p)
mi, mm, mc, mr, mh, mp = mirror_note
EXTRA["palindrome-census"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - All letters equal is the worst case for centre expansion: `n(n + 1)/2` palindromes, about 2 × 10¹⁰ for
          `n = 2 × 10⁵`, which also means the count needs 64 bits.
        - A single letter: the answer is 1.
        """
    ],
    "think": [
        """
        **Why expansion is too slow here.** Counting by centre expansion costs as much as the answer itself, and the
        answer can be 2 × 10¹⁰. We need each centre's palindrome radius without walking it step by step.
        """,
        CENTRES,
        f"""
        **Step 1: one kind of centre.** Insert `#` between letters and at both ends, plus distinct sentinels `^` and `$`:
        `"{s4}"` becomes `{t}`. Now every palindrome of the original string corresponds to an odd-length palindrome
        centred on a character of `t` (a letter for odd lengths, a `#` for even lengths), so one loop handles both.

        **Step 2: the radius array.** `p[i]` is how far the palindrome centred at `i` in `t` reaches on each side. A
        radius `r` in `t` is a palindrome of length `r` in the original string, and around that centre the original has
        palindromes of lengths `r, r − 2, r − 4, …`, which is `(r + 1) / 2` of them (integer division).
        """,
        table(["i"] + list(range(len(t))), ["t"] + list(t), ["p"] + p),
        f"""
        Summing `(p[i] + 1) / 2` gives **{census}**.

        **Step 3: mirror reuse (Manacher).** Keep the palindrome that reaches furthest right, centred at `C` and
        ending at `R`. For a position `i` inside it (`i < R`), its mirror is `2C − i`, and the text around `i` mirrors the
        text around the mirror, as long as we stay inside `[2C − R, R]`. So `p[i]` is at least
        `min(R − i, p[2C − i])`, and only the part beyond `R` needs real comparisons.

        In this example, at `i = {mi}` the mirror is `{mm}` (inside the palindrome centred at {mc} reaching {mr}), so the
        radius starts at {mh} without any comparisons and ends up at {mp}.

        **Why it's linear.** Every successful comparison beyond `R` pushes `R` further right, and `R` only moves right,
        at most `|t|` times in total. Failed comparisons happen at most once per position.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Expand around each of the `2n − 1` centres, counting each successful step in a 64-bit counter. It's correct, but its running time equals the answer."],
            "build": ["Loop over centres.", "Expand and count each step.", "Return the 64-bit total."],
            "complexity": ["**Time O(n²)** worst case: 2 × 10¹⁰ steps for 2 × 10⁵ equal letters. **Space O(1).**"],
            "limits": ["Inside a long palindrome, neighbouring centres redo the same comparisons on mirrored text. Manacher reuses the mirrored radius so that each comparison advances the right edge."],
            "lines": {
                "init": "A 64-bit total, because the count can exceed 2³¹.",
                "centre": "Letters (even `c`) and gaps (odd `c`).",
                "expand": "Each matching pair is one more palindrome around this centre.",
                "ret": "The total.",
            },
        },
        1: {
            "idea": [
                """
                Build `t`, then for each position `i` (between the sentinels):

                1. If `i < R`, start `p[i]` at `min(R − i, p[2C − i])`: the mirror's radius, capped at the part we've
                   verified.
                2. Expand while `t[i + p[i] + 1] = t[i − p[i] − 1]`. The sentinels `^` and `$` differ from everything,
                   so this stops at the ends without bounds checks.
                3. If `i + p[i] > R`, this palindrome reaches further: set `C = i`, `R = i + p[i]`.
                4. Add `(p[i] + 1) / 2` to the total.

                **Correctness of the head start.** Within `[2C − R, R]` the text is symmetric about `C`. If the mirror's
                palindrome fits inside that range, `i`'s palindrome is its exact reflection; if it reaches the edge, we
                only know `i`'s palindrome reaches `R` and must check beyond it, which step 2 does.
                """
            ],
            "build": [
                "Transformed string `^#a#b#…#$` of length `2n + 3`.",
                "Radius array `p`, and `C = R = 0`.",
                "Head start from the mirror, expand, update `C`/`R`.",
                "Add `(p[i] + 1) / 2` for every position.",
            ],
            "complexity": ["**Time O(n):** `R` moves right at most `2n + 3` times, and each position has at most one failed comparison. **Space O(n)** for `t` and `p`."],
            "lines": {
                "build": "Separators make every palindrome odd-length in `t`; the different sentinels at both ends stop expansion without index checks. `p[i]` will hold the radius at `i`.",
                "loop": "Every real position of `t` (the sentinels are skipped).",
                "mirror": "Inside the rightmost palindrome, position `i` reflects to `2C − i`. Its radius is at least the mirror's, but anything beyond `R` hasn't been verified, hence the cap `R − i`.",
                "expand": "Compare only beyond what's already known. Each success extends this palindrome by one on each side.",
                "edge": "Keep the palindrome that reaches furthest right; it gives the biggest head starts later.",
                "ret": "Radius `r` in `t` means palindromes of lengths `r, r − 2, …` in the original: `(r + 1) / 2` of them. The sum is 64-bit.",
            },
        },
    },
    "takeaways": [
        """
        - **Manacher's algorithm:** all palindrome radii in O(n) by reflecting inside the rightmost palindrome.
        - Separators unify odd and even lengths; distinct sentinels remove bounds checks.
        - From radii: count palindromes (`Σ (r + 1) / 2`) or find the longest (`max r`).
        - **Pitfalls:** the cap `R − i` (forgetting it uses unverified text); 32-bit totals.
        """
    ],
}
