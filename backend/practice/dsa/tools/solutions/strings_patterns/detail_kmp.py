"""In-depth text for the KMP / prefix-function problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table
from strings_patterns.pattern_matching import prefix_function

BORDER = """
**Borders and the prefix function.** A *border* of a string is a proper prefix that is also a suffix: `ab` is a border
of `abab`, and `a` is a border of `aba`. The **prefix function** `pi[i]` is the length of the longest border of the
first `i + 1` characters. It is computed left to right: to extend a border of length `k` by the next character, check
`t[i] == t[k]`; if not, the next shorter candidate is the border of the border, `pi[k − 1]`, and so on until a match
or `k = 0`.
"""


def pi_rows(t):
    pi = prefix_function(t)
    return [(i, t[:i + 1], pi[i], t[:pi[i]] or "—") for i in range(len(t))]


# ---------------------------------------------------------------- find-every-tag
text, tag = "abababcabab", "abab"
m = len(tag)
fail = prefix_function(tag)
scan, k = [], 0
for i, c in enumerate(text):
    before, chain = k, []
    while k and c != tag[k]:
        k = fail[k - 1]
        chain.append(k)
    if c == tag[k]:
        k += 1
    hit = k == m
    after = k
    if hit:
        k = fail[k - 1]
    scan.append((i, c, before, " → ".join(map(str, chain)) or "—", after, f"match at {i - m + 1}, keep {k}" if hit else ""))
hits = [i for i in range(len(text) - m + 1) if text[i:i + m] == tag]
EXTRA["find-every-tag"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Overlapping copies all count: `aaaa` contains `aa` at 0, 1 and 2.
        - The tag may equal the whole text (one match) or never appear (empty list).
        - Worst case for naive matching: `text = aaaa…a`, `tag = aa…ab`, where every start compares almost the whole tag.
        """
    ],
    "think": [
        """
        **Restating it.** Report every start index `i` with `text[i .. i+m) = tag`, in increasing order, overlaps
        included.

        **What the naive method throws away.** Comparing at each start, a partial match of `j` characters that breaks
        means we slide by one and compare again from scratch, re-reading `j − 1` characters we have already seen. But
        those characters are known: they are `tag[0 .. j)`. So how much of the next attempt already matches depends
        only on the tag, and can be computed in advance.
        """,
        BORDER,
        f"**Prefix function of `\"{tag}\"`:**",
        table(["i", "prefix", "pi[i]", "longest border"], *pi_rows(tag)),
        f"""
        **The scan.** Keep `k` = how many tag characters match, ending at the current text position. On a mismatch,
        fall back from `k` to `pi[k − 1]` (the longest border of what matched) and try again; that's the most of the
        tag that can still be matched. After a full match, fall back the same way to catch overlapping copies. Trace on
        `"{text}"`:
        """,
        table(["i", "char", "k before", "fallbacks", "k after", "event"], *scan),
        f"Matches at **{hits}**.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Line the tag up at every start `0 … n − m` and compare character by character until a mismatch or a full
                match. Record full matches.

                Correct and easy to trust, but every start begins comparing from the tag's first character.
                """
            ],
            "build": ["Loop over starts.", "Compare until mismatch or `m` matches.", "Record full matches."],
            "complexity": ["**Time O(n · m)** worst case: about 10¹⁰ comparisons for `n = 10⁵` with long near-matches. **Space O(1)** besides the output."],
            "limits": ["After a partial match breaks, the next start re-reads text that was already matched. The prefix function tells exactly how much of that match can be kept, so the text pointer never moves back."],
            "lines": {
                "init": "Lengths and the list of match positions.",
                "starts": "Every position where the whole tag still fits.",
                "cmp": "Compare until the first mismatch or until all `m` characters have matched.",
                "hit": "All `m` characters matched: the tag occurs at `i`.",
                "ret": "The starts, already in increasing order.",
            },
        },
        1: {
            "idea": [
                """
                **Phase 1:** compute the prefix function `fail` of the tag (the same matching process, run on the tag
                against itself).

                **Phase 2:** scan the text with `k`. For each character: while `k > 0` and it doesn't match `tag[k]`,
                set `k = fail[k − 1]`. If it matches, `k += 1`. If `k == m`, record `i − m + 1` and set `k = fail[m − 1]`.

                **Invariant.** After processing text position `i`, `k` is the length of the longest prefix of the tag that
                ends exactly at `i`. Every occurrence of the tag ends at some `i` with `k = m`, so none is missed.
                """
            ],
            "build": [
                "Build `fail` for the tag.",
                "Scan the text keeping `k`; fall back through `fail` on mismatches.",
                "On a full match, record and fall back to `fail[m − 1]`.",
            ],
            "complexity": [
                """
                **Time O(n + m).** `k` grows by at most 1 per character and each fallback shrinks it, so the total number
                of fallbacks can't exceed the total growth: at most `n` in the scan and `m` in the table. **Space O(m)**
                for the table.
                """
            ],
            "lines": {
                "table": "The prefix function of the tag: for each prefix, the longest border. It's the scan below applied to the tag itself.",
                "scan": "`k` = tag characters matched so far, ending at this text position. A match extends it by one.",
                "back": "On a mismatch, the longest border of the matched part is the largest piece that could still be extended. Keep falling back until the next character fits or nothing is left.",
                "hit": "A full match starts at `i − m + 1`. Falling back to `fail[m − 1]` instead of 0 keeps the overlap, so a copy sharing characters with this one is still found.",
                "ret": "All starts, left to right.",
            },
        },
    },
    "takeaways": [
        """
        - **Recognise it:** find all occurrences of a pattern, or anything about prefixes that are also suffixes.
        - **Template:** build `pi` for the pattern; scan with `k`, fall back via `pi[k − 1]`.
        - **Pitfalls:** resetting `k` to 0 after a match (misses overlaps); using `pi[k]` instead of `pi[k − 1]`.
        - **Related:** the Z-function solves the same problems; rolling hashes give a probabilistic alternative.
        """
    ],
}


# ---------------------------------------------------------------- front-padding
s = "aacecaaab"
n = len(s)
prows = [(k, s[:k] or "(empty)", "yes" if s[:k] == s[:k][::-1] else "no") for k in range(n, -1, -1)]
keep = max(k for k in range(n + 1) if s[:k] == s[:k][::-1])
glued = s + "#" + s[::-1]
gpi = prefix_function(glued)
want = s[keep:][::-1] + s
EXTRA["front-padding"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Empty `s`: the answer is empty.
        - `s` already a palindrome: nothing is added.
        - Worst case for direct checking: `aaa…ab`, where many long prefixes almost pass.
        """
    ],
    "think": [
        f"""
        **What the result looks like.** We only add letters to the front, so the original `s` sits at the end of the
        result. In a palindrome the front mirrors the back, so the added letters must be the reverse of some tail of
        `s`, and what's left in front of that tail, a prefix of `s`, must be a palindrome by itself (it becomes the
        middle). To add as little as possible, keep the **longest palindromic prefix** and mirror the rest.

        **Checking prefixes of `"{s}"` from longest to shortest:**
        """,
        table(["length", "prefix", "palindrome?"], *[r for r in prows if r[0] >= keep]),
        f"""
        The longest palindromic prefix is `{s[:keep]}` (length {keep}). Mirroring the rest gives `{s[keep:][::-1]}` + `{s}`
        = **`{want}`**.

        **Finding it in linear time.** A palindromic prefix of `s` reads the same reversed, so it's also a suffix of
        `reverse(s)`. In `s + "#" + reverse(s)`, a border (prefix that's also a suffix) is therefore a prefix of `s` that
        equals a suffix of `reverse(s)`: a palindromic prefix. The `#` stops a border from running across both halves.
        The longest border is the last value of the prefix function:
        """,
        table(["position"] + list(range(len(glued))), ["char"] + list(glued), ["pi"] + gpi),
        f"Last value {gpi[-1]} = length of the longest palindromic prefix.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Try prefix lengths from `n` down to 0 and test each with two pointers; the first palindrome is the
                longest. Return the reverse of the remaining tail followed by `s`. Length 0 always works, so the loop
                always finishes.
                """
            ],
            "build": ["Lengths from `n` down.", "Two-pointer palindrome test.", "Prepend the reversed tail."],
            "complexity": ["**Time O(n²)** worst case: up to `n` tests of up to `n/2` comparisons. **Space O(1)** besides the output."],
            "limits": ["Each candidate prefix is tested from scratch. The prefix function of `s # reverse(s)` finds the longest palindromic prefix in one pass."],
            "lines": {
                "search": "Longest candidate first; length 0 (the empty prefix) is always a palindrome.",
                "test": "Compare the prefix's ends moving inward; meeting without a mismatch means it's a palindrome, and it's the longest one.",
                "ret": "Mirror the tail after the palindromic prefix onto the front.",
            },
        },
        1: {
            "idea": [
                """
                Build `t = s + "#" + reverse(s)` and its prefix function. `keep = pi[last]` is the longest palindromic
                prefix. The answer is `reverse(s[keep:]) + s`, and `reverse(s[keep:])` is simply the first `n − keep`
                characters of `reverse(s)`.

                **Why the border is a palindrome.** A border of `t` of length `L ≤ n` is `s[0..L)` and also the last `L`
                characters of `reverse(s)`, which are `reverse(s[0..L))`. So `s[0..L)` equals its own reverse.
                """
            ],
            "build": ["Glue `s`, `#`, `reverse(s)`.", "Prefix function of the glued string.", "Prepend the first `n − keep` letters of `reverse(s)`."],
            "complexity": ["**Time O(n).** **Space O(n)** for the glued string and the table."],
            "lines": {
                "glue": "`s`, a separator that can't match any letter, then `reverse(s)`. C writes both halves into one buffer directly.",
                "table": "The standard prefix function; only its last value is needed.",
                "ret": "`keep` is the longest palindromic prefix. The letters to add are the reversed tail `s[keep:]`, which is the start of `reverse(s)`.",
            },
        },
    },
    "takeaways": [
        """
        - **Shortest palindrome by adding to the front** = keep the longest palindromic prefix, mirror the rest.
        - **`s # reverse(s)` + prefix function** finds palindromic prefixes in O(n).
        - **Pitfall:** forgetting the separator, which lets a border span both halves.
        """
    ],
}


# ---------------------------------------------------------------- repeating-unit
s3 = "abcabcabcabc"
n3 = len(s3)
pi3 = prefix_function(s3)
drows = []
for p in range(1, n3 + 1):
    if n3 % p:
        continue
    bad = next((i for i in range(p, n3) if s3[i] != s3[i - p]), None)
    drows.append((p, s3[:p], "works" if bad is None else f"fails at {bad}: {s3[bad]} ≠ {s3[bad - p]}"))
    if bad is None:
        break
EXTRA["repeating-unit"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One letter, or no repetition at all: the answer is `n`.
        - A string with a period that doesn't divide its length (`abcab`, period 3, length 5) isn't a repetition:
          the answer is `n`.
        - All letters equal: the answer is 1.
        """
    ],
    "think": [
        f"""
        **When does block length `p` work?** `s` is a block of length `p` repeated exactly when `p` divides `n` and every
        character equals the one `p` places earlier: `s[i] = s[i − p]` for all `i ≥ p`. The second condition says `s`
        has *period* `p`.

        **Trying divisors of `n = {n3}` in increasing order:**
        """,
        table(["p", "block", "check"], *drows),
        BORDER,
        f"""
        **Period and border are two views of the same thing.** `s[i] = s[i − p]` for all `i ≥ p` means `s` without its
        first `p` letters equals `s` without its last `p` letters: a border of length `n − p`. So the **longest** border
        gives the **smallest** period: `p = n − pi[n − 1]`. For `"{s3}"`:
        """,
        table(["i"] + list(range(n3)), ["char"] + list(s3), ["pi"] + pi3),
        f"""
        `pi[n − 1] = {pi3[-1]}`, so the smallest period is {n3} − {pi3[-1]} = {n3 - pi3[-1]}, which divides {n3}: the
        answer is **{n3 - pi3[-1]}**.

        **If the smallest period doesn't divide `n`, the answer is `n`.** Suppose the smallest period `p` doesn't divide
        `n`, but some larger `q < n` divides `n` and is also a period. Then `q ≤ n/2` and `p < q`, so `p + q ≤ n`, and a
        classic fact about periods (Fine and Wilf) says `gcd(p, q)` is also a period. It's at most `p`, so by minimality
        it equals `p`, which means `p` divides `q` and therefore `n`, a contradiction.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Only divisors of `n` can be block lengths. Try them from smallest to largest; for each, check that every
                character equals the one a block earlier. The first that passes is the answer, and `n` itself always
                passes.
                """
            ],
            "build": ["Loop `p = 1, 2, …`, skipping non-divisors.", "Check `s[i] = s[i − p]` for all `i ≥ p`.", "Return the first `p` that passes, else `n`."],
            "complexity": ["**Time O(n · d(n))**, where `d(n)` (the number of divisors) is at most 128 for `n ≤ 10⁵`: fast in practice. **Space O(1).**"],
            "limits": ["Each divisor is checked from scratch. The prefix function produces the smallest period directly in one pass, without trying candidates."],
            "lines": {
                "loop": "Block lengths must divide `n`; trying them smallest first means the first success is the answer.",
                "check": "Every character must equal the one exactly one block earlier. Python compares `s[p:]` with `s[:n−p]`, which is the same test done as a fast slice comparison.",
                "ret": "No shorter block works: the whole string is the block.",
            },
        },
        1: {
            "idea": [
                """
                Compute the prefix function. `p = n − pi[n − 1]` is the smallest period. If `p` divides `n`, `s` is `n / p`
                copies of `s[0..p)`; otherwise no proper block works and the answer is `n`.
                """
            ],
            "build": ["Prefix function of `s`.", "Smallest period from the longest border.", "Check divisibility."],
            "complexity": ["**Time O(n).** **Space O(n)** for the table."],
            "lines": {
                "table": "The prefix function of the whole string; only its last value is needed.",
                "period": "The longest border has length `pi[n−1]`, so shifting `s` by `n − pi[n−1]` lines it up with itself: that's the smallest period.",
                "ret": "A period that divides `n` tiles the string exactly. Otherwise no proper block works (see the proof above), so the answer is `n`.",
            },
        },
    },
    "takeaways": [
        """
        - **Border ↔ period:** a border of length `b` means period `n − b`; smallest period = `n − pi[n − 1]`.
        - A period tiles the string only if it divides the length.
        - **Pitfall:** returning the period without checking divisibility (`abcab` would wrongly give 3).
        - **Related:** "is `s` a repetition?" is the same test; so is checking whether `s` occurs inside `s + s` starting
          before position `n`.
        """
    ],
}
