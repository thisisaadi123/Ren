"""In-depth text for the palindrome-check problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table
from strings_patterns.pattern_matching import prefix_function


def is_pal(t):
    return t == t[::-1]


TWO_ENDS = """
**Checking a palindrome from both ends.** Put `i` at the start and `j` at the end. If `s[i] ≠ s[j]`, it isn't a
palindrome. If they match, that pair is settled forever, so move both inward. When the pointers meet or cross, every
mirrored pair has matched. That's `n/2` comparisons and no extra memory, and it's the base of every problem in this
pattern.
"""

# ---------------------------------------------------------------- mirror-sentence
text = "Step on no pets!"
mrows, i, j = [], 0, len(text) - 1
while i < j:
    if not text[i].isalnum():
        mrows.append((i, j, repr(text[i]), repr(text[j]), "skip left (not a letter or digit)"))
        i += 1
    elif not text[j].isalnum():
        mrows.append((i, j, repr(text[i]), repr(text[j]), "skip right (not a letter or digit)"))
        j -= 1
    else:
        mrows.append((i, j, repr(text[i]), repr(text[j]), "match ignoring case" if text[i].lower() == text[j].lower() else "mismatch"))
        i, j = i + 1, j - 1
EXTRA["mirror-sentence"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Text with no letters or digits at all (`"!? ."`) counts as a mirror.
        - Digits count: `"1a1"` is a mirror, `"12"` is not.
        - Case is ignored: `A` matches `a`.
        """
    ],
    "think": [
        TWO_ENDS,
        f"""
        **Skipping instead of cleaning.** Only letters and digits matter. Rather than building a cleaned copy, let each
        pointer step over characters that don't count. Trace on `"{text}"`:
        """,
        table(["i", "j", "s[i]", "s[j]", "action"], *mrows),
        "The pointers met with no mismatch: **true**.",
    ],
    "approaches": {
        0: {
            "idea": ["Build the cleaned string (letters and digits, lowercased) and compare it with its reverse. Simple and clearly correct."],
            "build": ["Filter and lowercase.", "Compare with the reverse."],
            "complexity": ["**Time O(n).** **Space O(n)** for the cleaned copy."],
            "limits": ["The copy isn't needed: pointers can skip ignored characters as they go, using O(1) memory."],
            "lines": {
                "clean": "Keep only letters and digits, lowercased: the text the question actually compares.",
                "cmp": "A palindrome equals its reverse. C compares the cleaned buffer's two ends instead of building a reversed copy.",
            },
        },
        1: {
            "idea": [
                """
                Two pointers. Each loop step does exactly one thing: skip an ignored character on the left, or on the
                right, or compare two counted characters case-insensitively and move both inward.

                **Why one action per step.** After a skip, the other side might also need skipping, and the loop handles
                that naturally. A pointer never skips a counted character, so every mirrored pair of counted characters
                is compared exactly once.
                """
            ],
            "build": ["Pointers at both ends.", "Skip ignored characters one side at a time.", "Compare counted characters ignoring case.", "True when the pointers meet."],
            "complexity": ["**Time O(n):** each step moves a pointer. **Space O(1).**"],
            "lines": {
                "init": "Pointers at the two ends of the text.",
                "loop": "Continue while there are at least two characters between them.",
                "skip": "A character that isn't a letter or digit doesn't take part; step past it on that side only.",
                "cmp": "Two counted characters must match ignoring case; then both pointers move inward.",
                "ret": "Every pair matched, including the case with nothing to compare.",
            },
        },
    },
    "takeaways": [
        """
        - **Filtered palindrome checks: two pointers that skip.**
        - Normalise (case) at comparison time instead of copying.
        - **Pitfall:** skipping on both sides in one step and jumping past a character that should be compared.
        """
    ],
}


# ---------------------------------------------------------------- one-slip-palindrome
s = "racecxar"
orows, i, j = [], 0, len(s) - 1
while i < j and s[i] == s[j]:
    orows.append((i, j, s[i], s[j], "match"))
    i, j = i + 1, j - 1
left, right = s[i + 1:j + 1], s[i:j]
orows.append((i, j, s[i], s[j], f"mismatch: try '{left}' (drop left) → {is_pal(left)}, '{right}' (drop right) → {is_pal(right)}"))
EXTRA["one-slip-palindrome"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Already a palindrome: true with zero deletions.
        - Both branches must be tried at a mismatch: `"abbca"` works only by dropping the `c` near the end, and `"acbba"` only by dropping the `c` near the start.
        - After the one deletion, no further mismatch is allowed.
        """
    ],
    "think": [
        TWO_ENDS,
        f"""
        **Where can the deletion be?** Match pairs from the outside in. Pairs that match are fine and don't need a
        deletion. At the **first** mismatching pair `s[i] ≠ s[j]`, one of these two characters has to go: deleting a
        character outside `[i, j]` would shift the matched outer pairs out of alignment, and deleting one strictly inside
        leaves `s[i]` and `s[j]` still facing each other. So only two candidates remain: the middle without `s[i]`, or
        without `s[j]`, and each must be a palindrome on its own.

        **Trace on `"{s}"`:**
        """,
        table(["i", "j", "s[i]", "s[j]", "result"], *orows),
        "One branch works, so the answer is **true**.",
    ],
    "approaches": {
        0: {
            "idea": ["If `s` is already a palindrome, true. Otherwise try deleting each position and test whether the rest is a palindrome."],
            "build": ["Palindrome test that ignores one index.", "Zero deletions first.", "Then every single deletion."],
            "complexity": ["**Time O(n²):** `n` deletions, each with an O(n) test. **Space O(1)** (Python's slices cost O(n))."],
            "limits": ["Only two deletions can possibly help: the characters at the first mismatch. Testing all `n` is wasted work."],
            "lines": {
                "check": "Is `s` a palindrome when position `skip` is ignored? Pointers jump over that index when they reach it.",
                "zero": "Already a palindrome: no deletion needed.",
                "try": "Every possible deletion position, until one leaves a palindrome.",
            },
        },
        1: {
            "idea": [
                """
                Match from both ends while the characters agree. At the first mismatch, return whether `s[i+1..j]` or
                `s[i..j−1]` is a palindrome (no further deletions). If the pointers meet without a mismatch, it's already a
                palindrome.

                Each branch is a single linear check, so at most three passes over the string in total.
                """
            ],
            "build": ["Range palindrome helper.", "Match pairs from the outside in.", "At the first mismatch, try both branches."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "lines": {
                "helper": "Is `s[i..j]` a palindrome? A plain two-pointer check on a range, with no deletions allowed.",
                "match": "Matching outer pairs never need a deletion; keep moving inward.",
                "branch": "First mismatch: one of these two characters is the slip. Try dropping either one; the rest must then be a palindrome as is.",
                "ret": "No mismatch at all: already a palindrome.",
            },
        },
    },
    "takeaways": [
        """
        - **Palindrome with one deletion:** match from both ends, branch once at the first mismatch.
        - The argument "only the mismatched pair can be the culprit" is the whole speed-up.
        - **Pitfall:** trying only one of the two branches.
        - More deletions need dynamic programming (longest palindromic subsequence).
        """
    ],
}


# ---------------------------------------------------------------- cut-out-the-middle
def cut_answer(t):
    n = len(t)
    return min(j - i for i in range(n + 1) for j in range(i, n + 1) if is_pal(t[:i] + t[j:]))


def cut_rows(t):
    n, l = len(t), 0
    while l < n - 1 - l and t[l] == t[n - 1 - l]:
        l += 1
    mid = t[l:n - l]
    pre = max(k for k in range(len(mid) + 1) if is_pal(mid[:k]))
    suf = max(k for k in range(len(mid) + 1) if is_pal(mid[len(mid) - k:]))
    return (t, t[:l] or "—", mid or "—", mid[:pre] or "—", mid[len(mid) - suf:] or "—", len(mid) - max(pre, suf), cut_answer(t))


s3 = "abcxyzcba"
examples = [s3, "abxyxcba", "racecar", "abcd"]
n3, l3 = len(s3), 0
while l3 < n3 - 1 - l3 and s3[l3] == s3[n3 - 1 - l3]:
    l3 += 1
mid3 = s3[l3:n3 - l3]
glue = mid3 + "#" + mid3[::-1]
EXTRA["cut-out-the-middle"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Already a palindrome: cut nothing (0).
        - The kept text is a prefix plus a suffix of `s`; either may be empty.
        - Cutting everything always works, so the answer is at most `n`.
        """
    ],
    "think": [
        TWO_ENDS,
        """
        **Step 1: peel the matching ends.** Match `s[0]` with `s[n−1]`, `s[1]` with `s[n−2]`, and so on, as long as they
        agree. Those pairs can always be kept: they already mirror each other. What remains in the middle starts and ends
        with **different** letters (or is tiny).

        **Step 2: the kept part of the middle is a prefix or a suffix of it.** The kept text is "start of `s`" + "end of
        `s`". If it kept letters from both sides of the middle, the first kept letter of the middle (its first letter)
        would have to mirror the last kept letter (its last letter), but those differ. So everything we keep from the
        middle sits entirely at its start or entirely at its end, and that piece must be a palindrome by itself.

        So: **answer = middle length − longest palindromic prefix-or-suffix of the middle.**
        """,
        table(["s", "peeled pairs", "middle", "longest pal. prefix", "longest pal. suffix", "cut", "check (brute force)"], *[cut_rows(t) for t in examples]),
        f"""
        **Finding the longest palindromic prefix in linear time.** A palindromic prefix of `t` equals its reverse, which
        is a suffix of `reverse(t)`. In `t + "#" + reverse(t)` that's a border (a prefix that's also a suffix), and the
        prefix function's last value gives the longest one. For the middle `"{mid3}"`: `{glue}` has prefix function
        {prefix_function(glue)}, last value {prefix_function(glue)[-1]}. Running the same on `reverse(t)` gives the longest
        palindromic suffix.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Try every block `[i, j)` to cut, check whether `s[:i] + s[j:]` is a palindrome, and keep the shortest block that works. Only blocks shorter than the current best are checked."],
            "build": ["Two loops over the block's ends.", "Palindrome check on the kept text without building it.", "Keep the shortest."],
            "complexity": ["**Time O(n³)** worst case: O(n²) blocks, each checked in O(n). **Space O(1).**"],
            "limits": ["Billions of blocks for `n = 10⁵`. Peeling the matching ends reduces the question to a palindromic prefix or suffix of the middle."],
            "lines": {
                "init": "Cutting everything leaves the empty text, which is a palindrome, so `n` always works.",
                "blocks": "Every block `[i, j)` that could be cut.",
                "check": "Only blocks shorter than the best matter. Position `a` of the kept text is `s[a]` before the cut and `s[a + (j − i)]` after it, so no copy is needed.",
                "ret": "The shortest cut.",
            },
        },
        1: {
            "idea": [
                """
                Peel matching ends to get the middle. Then find its longest palindromic prefix by testing lengths from the
                longest down, and the same for suffixes. The answer is the middle length minus the larger.
                """
            ],
            "build": ["Peel the matching ends.", "Longest palindromic prefix of the middle (direct tests).", "Longest palindromic suffix.", "Middle length minus the larger."],
            "complexity": ["**Time O(n²)** worst case: up to `n` lengths, each tested in O(n). **Space O(1).**"],
            "limits": ["Every candidate length is tested from scratch. The prefix function finds the longest palindromic prefix in one linear pass."],
            "lines": {
                "peel": "Keep stepping inward while the outer letters match. These pairs are always kept; the middle that's left has mismatched ends.",
                "longest": "The longest palindromic prefix and suffix of the middle, by testing lengths from the longest down.",
                "ret": "Keep the longer palindrome; everything else in the middle is cut.",
            },
        },
        2: {
            "idea": [
                """
                Peel the matching ends. For the middle `t`, compute the prefix function of `t + "#" + reverse(t)`: its last
                value is the longest palindromic prefix. Do the same for `reverse(t)` to get the longest palindromic suffix.
                The answer is `len(t) − max(prefix, suffix)`.

                **Why the border is a palindrome.** A border of length `L ≤ |t|` is `t[0..L)` and also the last `L`
                characters of `reverse(t)`, which are `reverse(t[0..L))`. So `t[0..L)` equals its own reverse. The `#`
                guarantees `L ≤ |t|`.
                """
            ],
            "build": ["Peel the matching ends.", "Prefix-function helper for `t # reverse(t)`.", "Apply it to the middle and to its reverse.", "Middle length minus the larger."],
            "complexity": ["**Time O(n).** **Space O(n)** for the glued string and the table."],
            "lines": {
                "peel": "Keep stepping inward while the outer letters match. A middle of length 0 or 1 is already a palindrome, so nothing is cut.",
                "kmp": "The prefix function of `t # reverse(t)`: its last value is the longest palindromic prefix of `t`. C builds the glued string directly (from `t` or from `t` reversed).",
                "ret": "Run it on the middle (prefix) and its reverse (suffix), keep the longer, and cut the rest of the middle.",
            },
        },
    },
    "takeaways": [
        """
        - **Peel matching ends first:** they can always stay, and what's left has mismatched ends.
        - **Mismatched ends force a one-sided choice:** keep a palindromic prefix or a palindromic suffix.
        - **Longest palindromic prefix = prefix function of `t # reverse(t)`.**
        - **Pitfall:** keeping letters from both sides of the middle, which can't be mirrored.
        """
    ],
}
