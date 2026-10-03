"""In-depth text for the group-by-key problems (merged into their sol() calls via sol.EXTRA)."""
from collections import Counter, defaultdict

from sol import EXTRA, table

KEYS = """
**Group by a canonical key.** When "belongs together" is an equivalence (anagrams, same shape, shift-equivalent),
find a **key** that every member of a group shares and no other item has. Then grouping is just a hash map from key
to items: one pass, no pairwise comparisons. The art is in choosing the key:

- it must be **identical** for items that belong together (otherwise one group splits in two);
- it must **differ** for items that don't (otherwise two groups merge);
- it should be cheap to compute.
"""


# ---------------------------------------------------------------- anagram-groups
words = ["pots", "tea", "stop", "eat", "opts", "tan", "ate"]
groups = defaultdict(list)
for w in words:
    groups["".join(sorted(w))].append(w)
result = sorted(sorted(g) for g in groups.values())
EXTRA["anagram-groups"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The empty word is a valid word; all empty words form one group.
        - Duplicates stay: two copies of `"tea"` both appear in their group.
        - Output order is fixed: words sorted within each group, groups sorted by their first word.
        """
    ],
    "think": [
        KEYS,
        """
        **The key for anagrams.** Rearranging letters doesn't change *which* letters there are or how many. Two keys
        capture exactly that: the sorted letters (`"tea" → "aet"`) or the 26 letter counts. Counts cost O(L) per word,
        sorting O(L log L).
        """,
        f"**Keys for `{words}`:**",
        table(["word", "sorted-letter key", "26-count key (non-zero letters)"], *[(w, "".join(sorted(w)), " ".join(f"{c}{n}" for c, n in sorted(Counter(w).items()))) for w in words]),
        f"Grouped and ordered: **`{result}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["Keep a list of groups with their letter counts. For each word, compare its counts with every existing group's counts; join the first match or start a new group. Finally sort."],
            "build": ["Letter counts per word.", "Linear search through existing groups.", "Join or create.", "Sort the output."],
            "complexity": ["**Time O(n · g · 26)** for `g` groups, up to O(n²) when most words are in their own group. **Space O(n · L).**"],
            "limits": ["Each word is compared with every group. A hash map keyed by the counts finds the right group in O(1) expected time."],
        },
        1: {
            "idea": ["Pair each word with its sorted-letter key and sort the pairs. Words with the same key become one consecutive run; cut the runs into groups, then sort the groups by first word."],
            "build": ["Key = sorted letters.", "Sort (key, word) pairs.", "Cut equal-key runs.", "Order groups by first word."],
            "complexity": ["**Time O(n · L log L + n log n · L).** **Space O(n · L).**"],
            "limits": ["Sorting all words costs O(n log n) comparisons of strings; a hash map groups them in one pass."],
        },
        2: {
            "idea": [
                """
                For each word, build its 26 letter counts and use them (as a tuple or a string) as a hash-map key; append
                the word to that key's list. Then sort each group and order the groups by first word.

                **Why it's correct.** Two words have equal count vectors exactly when they're anagrams, so each map entry
                is exactly one anagram group.
                """
            ],
            "build": ["Empty map key → list.", "Count letters for each word; append to its key's list.", "Sort inside groups, then the groups."],
            "complexity": ["**Time O(n · L)** to build the groups, plus sorting for the required output order. **Space O(n · L).**"],
        },
    },
    "takeaways": [
        """
        - **Group anagrams:** key = letter counts (or sorted letters), hash map key → list.
        - Pick a key that is equal exactly for items that belong together.
        - **Pitfall:** using a set of letters as the key (it ignores counts: `"aab"` and `"abb"` would merge).
        """
    ],
}


# ---------------------------------------------------------------- matching-rows-and-columns
grid = [[3, 1, 2, 2], [1, 4, 4, 5], [2, 4, 2, 2], [2, 4, 2, 2]]
n = len(grid)
cols = [[grid[r][c] for r in range(n)] for c in range(n)]
rowc = Counter(tuple(r) for r in grid)
mrows = [(c, cols[c], rowc[tuple(cols[c])]) for c in range(n)]
EXTRA["matching-rows-and-columns"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Equal rows count separately: two identical rows matching one column give two pairs.
        - `n = 1`: the single row and column are the same cell, so the answer is 1.
        - Comparing a row and a column means comparing `n` values in order.
        """
    ],
    "think": [
        KEYS,
        """
        **The key is the row itself.** A row matches a column when they hold the same values in the same order, so use
        the whole sequence (as a tuple) as the key. Count how many rows have each sequence, then, for each column, look
        up how many rows equal it.
        """,
        "**The grid's rows:**",
        table(["row", "values"], *[(r, grid[r]) for r in range(n)]),
        "**Each column and the number of equal rows:**",
        table(["column", "values (top to bottom)", "equal rows"], *mrows),
        f"Total **{sum(r[2] for r in mrows)}** pairs.",
    ],
    "approaches": {
        0: {
            "idea": ["Compare every row with every column element by element. `n²` pairs, each up to `n` comparisons."],
            "build": ["Loop over rows and columns.", "Compare the `n` values.", "Count equal pairs."],
            "complexity": ["**Time O(n³):** 2.16 × 10⁸ comparisons for `n = 600`. **Space O(1).**"],
            "limits": ["Each column is compared against every row. Grouping identical rows lets one lookup per column answer it."],
        },
        1: {
            "idea": ["Sort the rows (as tuples). For each column, binary-search the range of rows equal to it; its size is that column's count."],
            "build": ["Sort the rows.", "For each column, find the equal range by binary search.", "Add the range sizes."],
            "complexity": ["**Time O(n² log n):** sorting compares rows of length `n`. **Space O(n²)** for the row copies."],
            "limits": ["Sorting and binary search compare whole rows `log n` times per lookup. Hashing the rows makes each lookup O(n)."],
        },
        2: {
            "idea": [
                """
                Count the rows in a hash map keyed by the row tuple. Then for each column, add the count of rows equal to
                it.

                **Why it's O(n²).** Hashing a row or a column costs O(n), and there are `2n` of them: about `2n²` work,
                which is the size of the grid itself.
                """
            ],
            "build": ["Hash map row → count.", "For each column, look up its count.", "Sum."],
            "complexity": ["**Time O(n²)** expected. **Space O(n²)** for the stored rows."],
        },
    },
    "takeaways": [
        """
        - **Matching whole sequences:** hash the sequence and count; look up instead of comparing pairwise.
        - Equal keys with multiplicity → store counts, not just presence.
        - **Pitfall:** using a set of rows, which counts duplicate rows once.
        """
    ],
}


# ---------------------------------------------------------------- same-shape-words
pattern, sw = "boot", ["feet", "moon", "moan", "deed", "abba", "keep"]


def shape(s):
    first = {}
    return [first.setdefault(ch, len(first)) for ch in s]


target = shape(pattern)
EXTRA["same-shape-words"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Words of a different length can never match.
        - The mapping must be one-to-one: `"aaaa"` doesn't match `"abcd"` (several letters can't map to one).
        - A word always has the same shape as itself.
        """
    ],
    "think": [
        KEYS,
        f"""
        **The key for shapes.** Replace each letter by the order in which it first appeared: the first new letter is 0,
        the next new letter 1, and so on; a repeated letter reuses its number. Two words have the same shape exactly when
        these number lists are equal. Pattern `"{pattern}"` → `{target}`:
        """,
        table(["word", "shape", "matches?"], *[(w, shape(w), "yes" if shape(w) == target else "no") for w in sw]),
        f"""
        **{sum(shape(w) == target for w in sw)}** words match.

        **Why the numbering works.** It records exactly *which positions hold equal letters*. A one-to-one renaming of
        letters keeps that information unchanged, and two words with the same equal-position pattern can be renamed into
        each other.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For each word of the right length, check every pair of positions: the letters are equal in the word exactly when they're equal in the pattern."],
            "build": ["Skip words of a different length.", "Compare all pairs of positions.", "Count words with no disagreement."],
            "complexity": ["**Time O(W · L²)** for `W` words of length `L`. **Space O(1).**"],
            "limits": ["Quadratic in the word length. Two maps, or a canonical shape, check a word in O(L)."],
        },
        1: {
            "idea": [
                """
                For each word, walk it together with the pattern using two maps (word letter → pattern letter and back). A
                conflict in either direction means a different shape.

                Both directions are needed: one map alone would accept `"aaaa"` against `"abcd"`.
                """
            ],
            "build": ["Skip words of a different length.", "Two maps per word.", "Fail on any conflict."],
            "complexity": ["**Time O(W · L).** **Space O(L)** for the maps."],
            "limits": ["It re-walks the pattern for every word. Computing the pattern's canonical shape once lets each word be compared directly."],
        },
        2: {
            "idea": [
                """
                Compute the pattern's shape once. For each word, compute its shape and compare.

                **Why it's correct.** Equal shapes ⇔ the same positions hold equal letters ⇔ a one-to-one letter mapping
                exists.
                """
            ],
            "build": ["Shape function (first-appearance numbering).", "Pattern's shape once.", "Count words with the same shape."],
            "complexity": ["**Time O(W · L).** **Space O(L).**"],
        },
    },
    "takeaways": [
        """
        - **Isomorphism / same pattern:** canonical form by first-appearance numbering.
        - Equivalent to two maps, but the canonical form can be reused as a hash key for grouping.
        - **Pitfall:** checking only one direction of the mapping.
        """
    ],
}


# ---------------------------------------------------------------- shift-families
fw = ["abc", "bcd", "xyz", "az", "ba", "a", "z", "acd"]


def normal(w):
    return "".join(chr((ord(c) - ord(w[0])) % 26 + 97) for c in w)


fams = defaultdict(list)
for w in fw:
    fams[normal(w)].append(w)
EXTRA["shift-families"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Words of different lengths are never in the same family.
        - Wrap-around: `"az"` and `"ba"` are one family (shift by 1, `z` wraps to `a`).
        - All one-letter words form one family.
        """
    ],
    "think": [
        KEYS,
        """
        **The key for shifts.** Shifting changes every letter by the same amount, so shift each word so that its first
        letter becomes `a`. Words in the same family land on the same normalised word; words in different families don't
        (the gaps between consecutive letters, mod 26, are what's left, and shifting can't change them).
        """,
        f"**Normalised forms of `{fw}`:**",
        table(["word", "shift by", "normalised"], *[(w, (ord(w[0]) - 97), normal(w)) for w in fw]),
        "**Families:**",
        table(["normalised key", "members"], *[(k, ", ".join(v)) for k, v in fams.items()]),
        f"**{len(fams)}** families.",
    ],
    "approaches": {
        0: {
            "idea": ["Keep one representative per family. For each word, try all 26 shifts against every representative of the same length; if none matches, it starts a new family."],
            "build": ["Representatives list.", "Try 26 shifts per representative.", "New family if nothing matches."],
            "complexity": ["**Time O(n · f · 26 · L)** for `f` families: quadratic when most words are in their own family. **Space O(n · L).**"],
            "limits": ["Searching families by trial is slow. Normalising each word gives a key that identifies its family directly."],
        },
        1: {
            "idea": ["Normalise every word (shift so it starts with `a`), sort the normalised words, and count the distinct ones."],
            "build": ["Normalise each word.", "Sort the keys.", "Count distinct keys."],
            "complexity": ["**Time O(n · L + n log n · L).** **Space O(n · L).**"],
            "limits": ["Sorting just to count distinct keys; a hash set counts them in one pass."],
        },
        2: {
            "idea": [
                """
                Normalise each word and add it to a hash set. The set's size is the number of families.

                **Why it's correct.** Two words are in the same family exactly when they have the same length and the same
                normalised form.
                """
            ],
            "build": ["Empty set.", "Add each word's normalised form.", "Return the set's size."],
            "complexity": ["**Time O(n · L)** expected. **Space O(n · L).**"],
        },
    },
    "takeaways": [
        """
        - **Shift-equivalence:** normalise so the first letter is `a`; use mod 26 for wrap-around.
        - Counting groups = size of the set of keys.
        - **Pitfall:** forgetting the wrap-around (negative differences without `mod 26`).
        """
    ],
}
