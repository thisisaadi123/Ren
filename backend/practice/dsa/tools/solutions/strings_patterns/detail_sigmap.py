"""In-depth text for anagram/signature and character-mapping problems (merged into their sol() calls via sol.EXTRA)."""
from collections import Counter

from sol import EXTRA, table

SIGNATURE = """
**Signatures.** When a question only cares about *which letters and how many*, not their order, give every string a
**signature** that ignores order: its letters sorted (`"dormitory" → "dimoorrty"`) or its 26 letter counts. Two strings
are rearrangements of each other exactly when their signatures are equal. Counts are cheaper to build (O(n) instead of
O(n log n)) and to update when one letter changes.
"""

# ---------------------------------------------------------------- scrambled-name-tag
a, b = "Dormitory", "dirty room"
ca = Counter(c.lower() for c in a if c != " ")
cb = Counter(c.lower() for c in b if c != " ")
EXTRA["scrambled-name-tag"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Different numbers of spaces don't matter; spaces are ignored entirely.
        - `A` and `a` are the same letter.
        - Same letters in different amounts (`"aab"` vs `"abb"`) are **not** scrambles.
        """
    ],
    "think": [
        SIGNATURE,
        f"""
        **Normalise first.** Drop spaces and lowercase everything; then compare signatures. For `"{a}"` and `"{b}"`:
        """,
        table(["letter"] + sorted(ca | cb), ["count in a"] + [ca[x] for x in sorted(ca | cb)], ["count in b"] + [cb[x] for x in sorted(ca | cb)]),
        f"""
        Every count matches, so the answer is **{str(ca == cb).lower()}**.

        **One array instead of two.** Add 1 for each letter of `a` and subtract 1 for each letter of `b`. The phrases are
        scrambles exactly when every counter ends at 0.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Normalise both phrases (no spaces, lowercase), sort the letters, and compare the sorted lists. Equal sorted letters means equal multisets of letters."],
            "build": ["Filter out spaces and lowercase.", "Sort both.", "Compare."],
            "complexity": ["**Time O(n log n)** for the sorts. **Space O(n)** for the normalised copies."],
            "limits": ["Sorting does more than needed: only the counts of 26 letters matter, which one pass can collect."],
            "lines": {
                "norm": "Keep letters only, lowercased, and sort them. The sorted list is the phrase's signature; Java, C++ and C build it in a buffer.",
                "cmp": "Equal signatures mean the same letters with the same counts.",
            },
        },
        1: {
            "idea": [
                """
                One array of 26 counters. Each letter of `a` adds 1, each letter of `b` subtracts 1 (spaces skipped, case
                folded). Return whether all counters are 0.

                **Why it's right.** Counter `x` ends at `(count of x in a) − (count of x in b)`, which is 0 for every `x`
                exactly when the letter counts agree.
                """
            ],
            "build": ["26 zeros.", "Add for `a`, subtract for `b`.", "Check that all are 0."],
            "complexity": ["**Time O(n + m).** **Space O(1).**"],
            "lines": {
                "count": "Up for every letter of `a`, down for every letter of `b`, ignoring spaces and case.",
                "ret": "Any non-zero counter means some letter appears a different number of times.",
            },
        },
    },
    "takeaways": [
        """
        - **Rearrangement checks → compare signatures** (sorted letters or counts).
        - **One signed counter array** handles both strings.
        - **Pitfall:** comparing before normalising (spaces, case).
        """
    ],
}


# ---------------------------------------------------------------- swap-and-relabel
sa, sb = "aabcc", "ccaba"
la, lb = Counter(sa), Counter(sb)
letters = sorted(set(sa) | set(sb))
EXTRA["swap-and-relabel"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Different lengths: impossible, neither move changes the length.
        - A letter used in `b` but not in `a` can never be created: relabel needs both letters to be present already.
        - Equal words: zero moves.
        """
    ],
    "think": [
        f"""
        **What each move preserves.**

        - **Swap** only rearranges positions, so after swaps the order is irrelevant: a word is fully described by its
          letter counts. (Any arrangement of the same letters is reachable with swaps.)
        - **Relabel** of two present letters `x` and `y` exchanges their counts. It never adds a new letter or removes one,
          so the **set of letters** stays the same. And the counts are only moved between letters, so the **collection of
          count values** (sorted) stays the same.

        **Those two invariants are also enough.** Relabels are transpositions of counts among the present letters, and
        any rearrangement can be built from transpositions. So if `a` and `b` use the same letters and their sorted counts
        agree, relabels can move each count to the right letter, and swaps fix the order.

        **Example** `a = "{sa}"`, `b = "{sb}"`:
        """,
        table(["letter"] + letters, ["count in a"] + [la[x] for x in letters], ["count in b"] + [lb[x] for x in letters]),
        f"""
        Same letters ({', '.join(letters)}); sorted counts {sorted(la.values())} and {sorted(lb.values())}: **true**.
        Relabelling `a ↔ c` turns `aabcc` into `ccbaa`, and swaps rearrange it into `ccaba`.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Check the three conditions: equal lengths, the same set of letters, and the same sorted list of counts.

                Simulating moves is hopeless (the number of reachable words is enormous), which is why the reasoning
                about invariants is the whole solution.
                """
            ],
            "build": ["Compare lengths.", "Count letters of both words.", "Every letter must be present in both or in neither.", "Compare the sorted count arrays."],
            "complexity": ["**Time O(n):** counting, plus sorting 26 numbers. **Space O(1).**"],
            "lines": {
                "len": "Neither move changes the length.",
                "count": "Swaps make order irrelevant, so each word is summarised by its 26 letter counts.",
                "set": "Relabel needs both letters to be present already, so it can never introduce or remove a letter: the sets of letters must match.",
                "counts": "Relabels only move counts between letters, so the multiset of count values must match. Sorting the 26 counts compares them as multisets.",
            },
        },
    },
    "takeaways": [
        """
        - **When moves are free to repeat, look for invariants:** what can't any move change?
        - Then argue the invariants are enough (here, transpositions generate every rearrangement).
        - **Pitfall:** only comparing sorted counts and forgetting that new letters can't appear.
        """
    ],
}


# ---------------------------------------------------------------- anagram-twins-in-a-word
st = "abba"
trows = []
for L in range(1, len(st)):
    groups = Counter("".join(sorted(st[i:i + L])) for i in range(len(st) - L + 1))
    wins = [st[i:i + L] for i in range(len(st) - L + 1)]
    pairs = sum(k * (k - 1) // 2 for k in groups.values())
    trows.append((L, ", ".join(wins), ", ".join(f"{g}×{k}" for g, k in groups.items()), pairs))
total = sum(r[3] for r in trows)
EXTRA["anagram-twins-in-a-word"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Twins must have the **same length** (rearrangements always do) and different starting positions.
        - Equal substrings at different positions are twins too.
        - Length `n` has only one substring, so it can't form a pair.
        - The count can reach about `n³/6 ≈ 2 × 10⁷` for `n = 500`; it fits in 32 bits.
        """
    ],
    "think": [
        SIGNATURE,
        f"""
        **Group by signature, then count pairs.** For each length `L`, compute the signature of every window of length
        `L`. Windows with the same signature are all twins of each other; a group of `k` windows contributes
        `k · (k − 1) / 2` pairs. For `"{st}"`:
        """,
        table(["length", "windows", "signature groups", "pairs"], *trows),
        f"""
        Total **{total}**.

        **Updating a signature in O(1).** Within one length, sliding the window right changes two letters: one count goes
        up, one goes down. So the 26-count signature of the next window costs O(1) to update (plus O(26) to use it as a
        dictionary key), instead of sorting each window again.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                For each length, sort every window's letters to get its signature, then compare every pair of windows and
                count equal signatures.
                """
            ],
            "build": ["Loop over lengths.", "Sorted signature per window.", "Compare all pairs of windows."],
            "complexity": ["**Time O(n³)** pair comparisons (plus sorting), around 2 × 10⁷ signature comparisons for `n = 500`, each costing up to O(n). **Space O(n²)** for the signatures of one length."],
            "limits": ["Comparing every pair is wasteful: grouping equal signatures and counting `k(k − 1)/2` per group needs one pass. Sorting each window is also unnecessary when counts can slide."],
            "lines": {
                "init": "The running total of pairs.",
                "len": "Twins have equal lengths, so each length is handled separately. Length `n` is skipped: one window can't pair.",
                "sigs": "The sorted letters of each window: equal for rearrangements, different otherwise.",
                "pairs": "Compare every pair of windows of this length and count matching signatures.",
                "ret": "Pairs over all lengths.",
            },
        },
        1: {
            "idea": [
                """
                For each length `L`: build the 26 counts of the first window, then slide, adding the entering letter and
                removing the leaving one. Count how many windows have each signature in a dictionary keyed by the count
                tuple. Add `k(k − 1)/2` for every group.

                **Why grouping counts every pair once.** Each unordered pair of twins sits in exactly one group (their
                common signature), and a group of `k` has `k(k − 1)/2` unordered pairs.
                """
            ],
            "build": ["Loop over lengths `1 … n − 1`.", "Counts of the first window.", "Slide and record each window's count tuple.", "Add `k(k − 1)/2` per group."],
            "complexity": ["**Time O(n² · 26):** about `n²/2` windows over all lengths, each turned into a 26-entry key. **Space O(n · 26)** for one length's groups."],
            "lines": {
                "init": "The running total.",
                "len": "Each window length on its own.",
                "first": "Letter counts of the first window of this length.",
                "slide": "Move right: one letter's count rises, another's falls. Record the new signature's group size. C keeps the signatures in an array and sorts them to find groups.",
                "pairs": "A group of `k` equal signatures holds `k(k − 1)/2` twin pairs.",
                "ret": "Pairs over all lengths.",
            },
        },
    },
    "takeaways": [
        """
        - **Count pairs of "equivalent" items:** group by a signature, add `k(k − 1)/2` per group.
        - Sliding counts give each window's signature cheaply.
        - **Pitfall:** comparing all pairs instead of grouping.
        """
    ],
}


# ---------------------------------------------------------------- crack-the-cipher
plain, coded, message = "the cab", "xli gef", "fex lev"
back = {}
for p, c in zip(plain, coded):
    if c != " ":
        back[c] = p
mrows = [(c, back.get(c, "?") if c != " " else " ", "learned from the sample" if c in back else ("space" if c == " " else "never seen")) for c in message]
EXTRA["crack-the-cipher"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A coded letter that never appears in the sample decodes to `?`.
        - With exactly 25 coded letters learned, the 26th is forced: it must stand for the only unused plain letter.
        - Spaces stay spaces; they aren't letters of the cipher.
        """
    ],
    "think": [
        f"""
        **What the sample tells us.** Each aligned pair `(plain[i], coded[i])` reveals that `coded[i]` stands for
        `plain[i]`, and since the cipher is fixed, that holds everywhere. So one pass over the sample builds a
        **decoding table** from coded letters to plain letters.

        From `"{plain}"` ↔ `"{coded}"`: {', '.join(f'{c}→{p}' for c, p in back.items())}.

        **Decoding `"{message}"`:**
        """,
        table(["coded", "plain", "why"], *mrows),
        f"""
        Result **`{''.join(r[1] for r in mrows)}`**.

        **The 25-letter rule.** The cipher is one-to-one on 26 letters. If 25 coded letters are known, they use 25
        different plain letters, so the remaining coded letter must map to the remaining plain letter. With 24 or fewer
        known, at least two pairings remain possible, so nothing more can be deduced.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                For each letter of the message, search the coded sample for it; if found, output the plain letter at the
                same position. Handle the 25-letter case by finding the missing coded and plain letters up front.
                """
            ],
            "build": ["Prepare the forced pair if 25 letters are known.", "For each message letter, search the sample.", "Emit the plain letter, `?`, or a space."],
            "complexity": ["**Time O(|message| · |sample|):** up to 10¹⁰ steps. **Space O(1)** besides the output."],
            "limits": ["The same search is repeated for every message letter. A table built once answers each lookup in O(1)."],
            "lines": {
                "rule": "If the sample reveals exactly 25 coded letters, pair the missing coded letter with the unused plain letter.",
                "each": "Decode the message one character at a time.",
                "find": "Look for this letter in the coded sample; the plain sample at the same position is its meaning.",
                "emit": "A space stays a space; a found letter is decoded; an unknown letter becomes `?` unless it's the forced 26th.",
                "ret": "The decoded message.",
            },
        },
        1: {
            "idea": [
                """
                Build `back[coded] = plain` from the aligned sample. If it has exactly 25 entries, add the forced pair.
                Map spaces to spaces. Then translate the message with one table lookup per character, using `?` for missing
                letters.
                """
            ],
            "build": ["Fill the table from the sample.", "Apply the 25-letter rule.", "Translate the message."],
            "complexity": ["**Time O(|sample| + |message|).** **Space O(1):** at most 27 table entries."],
            "lines": {
                "table": "Each aligned pair of letters is one entry of the decoding table; spaces are skipped.",
                "rule": "With 25 entries, the missing coded letter must stand for the one plain letter not yet used.",
                "ret": "Translate every character with the table; missing letters become `?`, spaces stay.",
            },
        },
    },
    "takeaways": [
        """
        - **Fixed substitutions → build the mapping once, then translate.**
        - **One-to-one maps on a finite alphabet:** knowing all but one pair forces the last.
        - **Pitfall:** applying the 25-letter rule with fewer known letters, where it doesn't follow.
        """
    ],
}


# ---------------------------------------------------------------- repaint-the-letters
rs, rt, rm = "abca", "bbcb", 3
paint = {}
for x, y in zip(rs, rt):
    paint.setdefault(x, y)
cyc_steps = [("ab", "start"), ("cb", "a → c (c is free: not in the target)"), ("ca", "b → a (a is now free)"), ("ba", "c → b")]
EXTRA["repaint-the-letters"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `s = t`: always possible with zero steps.
        - Two tiles with the same colour in `s` but different colours in `t`: impossible, they're always repainted together.
        - Every one of the `m` colours used in `t`, with `s ≠ t`: impossible (no free colour to work with).
        """
    ],
    "think": [
        f"""
        **First requirement: one target per colour.** A step repaints *every* tile of a colour, so tiles that share a
        colour in `s` always share a colour afterwards. So each colour of `s` must go to a single colour of `t`: the pairs
        `(s[i], t[i])` must define a function. For `s = "{rs}"`, `t = "{rt}"`: {', '.join(f'{x}→{y}' for x, y in paint.items())},
        consistent.

        **Second requirement: a free colour, unless nothing changes.** If `t` uses all `m` colours, then (since it's the
        image of the function) so does `s`, and every step merges two colour classes, permanently reducing the number of
        colours present. But `t` needs all `m`, so no step may happen at all, meaning `s` must already equal `t`.

        **Why a free colour is enough.** Think of the function as arrows `x → f(x)`. Repaint along chains from the far
        end first, so a colour is never overwritten while some tile still needs it. A cycle (like `a → b → a`) needs one
        temporary colour; a colour missing from `t` can be freed and used for that. For example, `s = "ab"`, `t = "ba"`,
        `m = 3`:
        """,
        table(["sign", "step"], *cyc_steps),
        "With `m = 2` there's no spare colour and this swap is impossible.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Return true if `s = t`. Otherwise check that the colour mapping is consistent, and that `t` uses fewer than
                `m` colours.

                Searching over repaint sequences directly would explode; the two conditions capture exactly what's
                possible (see the reasoning above).
                """
            ],
            "build": ["Equal signs: true.", "Build the mapping from `s`-colour to `t`-colour; a conflict means false.", "Require a colour unused by `t`."],
            "complexity": ["**Time O(n).** **Space O(m):** at most 26 entries."],
            "lines": {
                "same": "Nothing to change: zero steps.",
                "map": "Each colour of `s` must always go to the same colour of `t`; a second, different target makes it impossible.",
                "spare": "With `s ≠ t`, at least one colour must be free (unused in `t`) to break cycles; if `t` uses all `m` colours, the number of colours can only shrink.",
            },
        },
    },
    "takeaways": [
        """
        - **"Recolour all of x" operations** → the mapping must be a function; check it with one map.
        - **Cycles in a mapping need a temporary slot** (like swapping two variables).
        - **Pitfall:** forgetting the `s = t` case, which needs no free colour.
        """
    ],
}


# ---------------------------------------------------------------- rhythm-of-words
pat, sen = "abca", "sun moon star sun"
words = sen.split()
fails = [("abba", "sun sun sun sun", "a and b both → sun (two letters, one word)"), ("aaaa", "sun moon sun moon", "a → sun and moon (one letter, two words)"), ("ab", "sun moon star", "different numbers of letters and words")]
EXTRA["rhythm-of-words"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Different numbers of letters and words: false.
        - Two letters mapped to the same word: false (the map must be one-to-one both ways).
        - A single letter and a single word: true.
        """
    ],
    "think": [
        f"""
        **One-to-one means two checks.** "Same letter → same word" is a function from letters to words. "Different
        letters → different words" means no two letters share a word, which is a function from words back to letters.
        Checking only one direction misses half the failures.

        **Example** `"{pat}"` with `"{sen}"`: {', '.join(f'{p}↔{w}' for p, w in zip(pat, words))}: every letter keeps its
        word and every word keeps its letter, so **true**.

        **How it can fail:**
        """,
        table(["pattern", "sentence", "problem"], *fails),
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Split the sentence. For every pair of positions `i < j`, the letters are equal exactly when the words are
                equal. If any pair breaks that, the sentence doesn't follow the pattern.

                It checks both directions at once, which makes it a neat correctness reference.
                """
            ],
            "build": ["Split and compare lengths.", "Check every pair of positions.", "True if no pair disagrees."],
            "complexity": ["**Time O(n² · w)** for `n` words of length up to `w` (word comparisons). **Space O(n)** for the words."],
            "limits": ["Quadratic in the number of words. Two maps check each position once."],
            "lines": {
                "split": "Words separated by single spaces; the counts must match the pattern length.",
                "pairs": "For every pair of positions, \"same letter\" must agree with \"same word\".",
                "ret": "No disagreement found.",
            },
        },
        1: {
            "idea": [
                """
                Walk letters and words together with two maps: letter → word and word → letter. At each position, the
                stored partner (if any) must equal the current one in **both** maps.

                **Why both maps.** The first catches a letter that changes words; the second catches two letters sharing a
                word. Together they guarantee a one-to-one correspondence.
                """
            ],
            "build": ["Split and compare lengths.", "Two empty maps.", "For each position, check or store both directions."],
            "complexity": ["**Time O(n · w)** (hashing the words). **Space O(n · w)** for the maps."],
            "lines": {
                "split": "Words, and the length check.",
                "maps": "Letter → word and word → letter.",
                "check": "A letter seen before must come with the same word.",
                "unique": "A word seen before must come with the same letter; this is what stops two letters sharing a word. Python does both checks with `setdefault` in one line.",
                "ret": "Every position was consistent both ways.",
            },
        },
    },
    "takeaways": [
        """
        - **One-to-one correspondence = two maps** (or one map plus a set of used targets).
        - **Pitfall:** checking only letter → word.
        - Same pattern as isomorphic strings.
        """
    ],
}
