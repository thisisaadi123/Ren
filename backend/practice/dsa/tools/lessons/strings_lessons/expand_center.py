"""Lesson: Expand around center (Strings, pattern 1)."""
from lesson import Bars, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

CENTERS = {
    "python": """
        def longest_at_centers(s):
            n = len(s)                                      #@n
            out = []                                        #@n
            for c in range(2 * n - 1):                      #@centers
                lo, hi = c // 2, c // 2 + c % 2             #@start
                while lo >= 0 and hi < n and s[lo] == s[hi]:    #@grow
                    lo, hi = lo - 1, hi + 1                 #@grow
                out.append(hi - lo - 1)                     #@len
            return out                                      #@ret
    """,
    "java": """
        static int[] longestAtCenters(String s) {
            int n = s.length();                             //@n
            int[] out = new int[Math.max(0, 2 * n - 1)];    //@n
            for (int c = 0; c < 2 * n - 1; c++) {           //@centers
                int lo = c / 2, hi = c / 2 + c % 2;         //@start
                while (lo >= 0 && hi < n && s.charAt(lo) == s.charAt(hi)) {     //@grow
                    lo--;                                   //@grow
                    hi++;                                   //@grow
                }
                out[c] = hi - lo - 1;                       //@len
            }
            return out;                                     //@ret
        }
    """,
    "cpp": """
        vector<int> longestAtCenters(const string& s) {
            int n = s.size();                               //@n
            vector<int> out;                                //@n
            for (int c = 0; c < 2 * n - 1; c++) {           //@centers
                int lo = c / 2, hi = c / 2 + c % 2;         //@start
                while (lo >= 0 && hi < n && s[lo] == s[hi]) {   //@grow
                    lo--;                                   //@grow
                    hi++;                                   //@grow
                }
                out.push_back(hi - lo - 1);                 //@len
            }
            return out;                                     //@ret
        }
    """,
    "c": """
        int longestAtCenters(const char* s, int* out) {
            int n = strlen(s);                              //@n
            for (int c = 0; c < 2 * n - 1; c++) {           //@centers
                int lo = c / 2, hi = c / 2 + c % 2;         //@start
                while (lo >= 0 && hi < n && s[lo] == s[hi]) {   //@grow
                    lo--;                                   //@grow
                    hi++;                                   //@grow
                }
                out[c] = hi - lo - 1;                       //@len
            }
            return n > 0 ? 2 * n - 1 : 0;                   //@ret
        }
    """,
}
CENTERS_RUN = {
    "python": """
        for s in ["abaab", "aaaa", "x", ""]:
            print(*longest_at_centers(s))
    """,
    "java": """
        public static void main(String[] args) {
            for (String s : new String[] {"abaab", "aaaa", "x", ""}) {
                StringBuilder sb = new StringBuilder();
                for (int x : longestAtCenters(s)) sb.append(sb.length() > 0 ? " " : "").append(x);
                System.out.println(sb);
            }
        }
    """,
    "cpp": """
        int main() {
            for (string s : {"abaab", "aaaa", "x", ""}) {
                vector<int> v = longestAtCenters(s);
                for (size_t i = 0; i < v.size(); i++) cout << (i ? " " : "") << v[i];
                cout << "\\n";
            }
        }
    """,
    "c": """
        int main(void) {
            const char* tests[] = {"abaab", "aaaa", "x", ""};
            int out[16];
            for (int t = 0; t < 4; t++) {
                int m = longestAtCenters(tests[t], out);
                for (int i = 0; i < m; i++) printf(i ? " %d" : "%d", out[i]);
                printf("\\n");
            }
            return 0;
        }
    """,
}

ONEFIX = {
    "python": """
        def longest_one_fix(s):
            n, best = len(s), 0                             #@init
            for c in range(2 * n - 1):                      #@centers
                lo, hi = c // 2, c // 2 + c % 2             #@centers
                fixes = 0                                   #@fixes
                while lo >= 0 and hi < n:                   #@grow
                    if s[lo] != s[hi]:                      #@miss
                        if fixes == 1:                      #@miss
                            break                           #@miss
                        fixes += 1                          #@miss
                    lo, hi = lo - 1, hi + 1                 #@grow
                best = max(best, hi - lo - 1)               #@best
            return best                                     #@ret
    """,
    "java": """
        static int longestOneFix(String s) {
            int n = s.length(), best = 0;                   //@init
            for (int c = 0; c < 2 * n - 1; c++) {           //@centers
                int lo = c / 2, hi = c / 2 + c % 2;         //@centers
                int fixes = 0;                              //@fixes
                while (lo >= 0 && hi < n) {                 //@grow
                    if (s.charAt(lo) != s.charAt(hi)) {     //@miss
                        if (fixes == 1) break;              //@miss
                        fixes++;                            //@miss
                    }
                    lo--;                                   //@grow
                    hi++;                                   //@grow
                }
                best = Math.max(best, hi - lo - 1);         //@best
            }
            return best;                                    //@ret
        }
    """,
    "cpp": """
        int longestOneFix(const string& s) {
            int n = s.size(), best = 0;                     //@init
            for (int c = 0; c < 2 * n - 1; c++) {           //@centers
                int lo = c / 2, hi = c / 2 + c % 2;         //@centers
                int fixes = 0;                              //@fixes
                while (lo >= 0 && hi < n) {                 //@grow
                    if (s[lo] != s[hi]) {                   //@miss
                        if (fixes == 1) break;              //@miss
                        fixes++;                            //@miss
                    }
                    lo--;                                   //@grow
                    hi++;                                   //@grow
                }
                best = max(best, hi - lo - 1);              //@best
            }
            return best;                                    //@ret
        }
    """,
    "c": """
        int longestOneFix(const char* s) {
            int n = strlen(s), best = 0;                    //@init
            for (int c = 0; c < 2 * n - 1; c++) {           //@centers
                int lo = c / 2, hi = c / 2 + c % 2;         //@centers
                int fixes = 0;                              //@fixes
                while (lo >= 0 && hi < n) {                 //@grow
                    if (s[lo] != s[hi]) {                   //@miss
                        if (fixes == 1) break;              //@miss
                        fixes++;                            //@miss
                    }
                    lo--;                                   //@grow
                    hi++;                                   //@grow
                }
                if (hi - lo - 1 > best) best = hi - lo - 1; //@best
            }
            return best;                                    //@ret
        }
    """,
}
ONEFIX_RUN = {
    "python": """
        for s in ["abcda", "abcd", "racecar", "ab", ""]:
            print(longest_one_fix(s))
    """,
    "java": """
        public static void main(String[] args) {
            for (String s : new String[] {"abcda", "abcd", "racecar", "ab", ""}) System.out.println(longestOneFix(s));
        }
    """,
    "cpp": """
        int main() {
            for (string s : {"abcda", "abcd", "racecar", "ab", ""}) cout << longestOneFix(s) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* tests[] = {"abcda", "abcd", "racecar", "ab", ""};
            for (int t = 0; t < 5; t++) printf("%d\\n", longestOneFix(tests[t]));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

longest_at_centers = py(CENTERS["python"], "longest_at_centers")
longest_one_fix = py(ONEFIX["python"], "longest_one_fix")


def is_pal(t):
    return t == t[::-1]


for s in ["abaab", "aaaa", "x", "", "abacdcaba", "banana"]:
    best = max((j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if is_pal(s[i:j])), default=0)
    assert max(longest_at_centers(s), default=0) == best
for s in ["abcda", "abcd", "racecar", "ab", "", "abxyba", "aaab"]:
    best = max((j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1)
                if sum(s[i + k] != s[j - 1 - k] for k in range((j - i) // 2)) <= 1), default=0)
    assert longest_one_fix(s) == best, s

# Theory walk: growing one odd center.
ES = "xabacabay"
EC = 4
ew = Steps(f"Growing the palindrome centred on the '{ES[EC]}' at index {EC} of \"{ES}\".")
lo, hi = EC, EC
ew.step(f"A single letter is a palindrome on its own. Start with `lo` and `hi` both on index {EC}.",
        Row(list(ES), st={EC: "found"}, ptr={"lo": lo, "hi": hi}, slots=True, label="s"), M({"palindrome": ES[EC]}))
while True:
    lo, hi = lo - 1, hi + 1
    if lo < 0 or hi >= len(ES):
        break
    if ES[lo] == ES[hi]:
        ew.step(f"Step out one place each way: '{ES[lo]}' and '{ES[hi]}' match, so \"{ES[lo:hi + 1]}\" is a palindrome too.",
                Row(list(ES), st={**{k: "found" for k in range(lo + 1, hi)}, lo: "active", hi: "active"}, ptr={"lo": lo, "hi": hi}, slots=True, label="s"),
                M({"palindrome": ES[lo:hi + 1]}))
    else:
        ew.step(f"Step out again: '{ES[lo]}' and '{ES[hi]}' differ. Stop. Every longer string around this center would contain this mismatched pair, "
                f"so \"{ES[lo + 1:hi]}\" (length {hi - lo - 1}) is the longest palindrome here.",
                Row(list(ES), st={**{k: "found" for k in range(lo + 1, hi)}, lo: "mark", hi: "mark"}, ptr={"lo": lo, "hi": hi}, slots=True, label="s"),
                M({"palindrome": ES[lo + 1:hi]}))
        break
E_LEGEND = {"found": "known to be a palindrome", "active": "the new pair: equal", "mark": "the new pair: different"}

# Trace walk: the template on "abaab", one center per step.
TS = "abaab"
TL = longest_at_centers(TS)
tw = Steps(f"`longest_at_centers(\"{TS}\")`: {len(TS)} letter centers and {len(TS) - 1} gap centers, {2 * len(TS) - 1} in all.")
done = []
tw.step("Center `c` sits on letter `c // 2` when `c` is even, and in the gap after that letter when `c` is odd.",
        Row(list(TS), slots=True, label="s"), Bars([None] * len(TL), labels=range(len(TL)), label="longest palindrome at each center", top=max(TL)))
for c in range(2 * len(TS) - 1):
    L = TL[c]
    lo = c // 2 - (L - 1) // 2 if c % 2 == 0 else c // 2 - L // 2 + 1
    span = range(lo, lo + L)
    where = f"on '{TS[c // 2]}' (index {c // 2})" if c % 2 == 0 else f"in the gap between index {c // 2} and {c // 2 + 1}"
    if L == 0:
        what = f"'{TS[c // 2]}' and '{TS[c // 2 + 1]}' differ, so nothing even-length is centred here: 0."
    elif L == 1 and c // 2 in (0, len(TS) - 1):
        what = "it's at the end of the string, so it can't grow past the letter itself: 1."
    elif L == 1:
        what = "the neighbours don't match, so just the letter itself: 1."
    else:
        what = f"it grows to \"{TS[lo:lo + L]}\": {L}."
    done.append(L)
    tw.step(f"Center {c}, {where}: {what}", Row(list(TS), st={k: "answer" for k in span}, slots=True, label="s"),
            Bars(done + [None] * (len(TL) - len(done)), labels=range(len(TL)), st={c: "active"}, label="longest palindrome at each center", top=max(TL)))
tw.steps[-1]["text"] += f" The tallest bar, {max(TL)}, is the longest palindrome in the whole string."
T_LEGEND = {"answer": "the palindrome found at this center", "active": "the value just recorded"}

# Example: DNA, where a "palindrome" pairs each base with its complement.
COMP = {"A": "T", "T": "A", "C": "G", "G": "C"}
DNA = "TGAATTCAGCTGCA"


def dna_best(s):
    best = (0, 0)
    for c in range(len(s) - 1):
        lo, hi = c, c + 1
        while lo >= 0 and hi < len(s) and COMP[s[lo]] == s[hi]:
            lo, hi = lo - 1, hi + 1
        if hi - lo - 1 > best[1] - best[0]:
            best = (lo + 1, hi)
    return best


DB = dna_best(DNA)
DSITE = DNA[DB[0]:DB[1]]
assert DSITE == "".join(COMP[x] for x in reversed(DSITE))

# Work on the worst case.
N = 2000

lesson(
    "strings",
    "expand-center",
    """
    Every palindrome has a middle: a letter for odd lengths, a gap between two letters for even ones. Stand at each
    of the 2n - 1 possible middles and grow outward while the two ends match. That finds the longest palindrome around
    every center in O(n²) time and O(1) space, with no table.
    """,
    [
        ("idea", "The idea", [
            f"""
            Fold a strip of paper with a word on it. If the letters that land on top of each other all match, the word
            is a palindrome, and the fold line is its middle. "racecar" folds on the "e". "noon" folds in the gap
            between the two o's.

            Turn that around. Pick a fold line anywhere in a string, and check the letters on either side: one step out,
            two steps out, and so on, for as long as they match. The stretch you've covered is the longest palindrome
            with that middle. The first mismatch ends it, because any longer stretch around the same middle contains
            the mismatched pair.

            A string of `n` letters has `n` letter middles and `n - 1` gap middles. Grow from each one and you've seen
            the longest palindrome around every possible middle, which means you've seen every palindrome there is.
            """,
            fig(Row(list("racecar"), st={3: "active"}, slots=True, label="odd length: the middle is a letter"),
                Row(list("noon"), st={1: "active", 2: "active"}, slots=True, label="even length: the middle is a gap"),
                caption="Two kinds of middle. Forgetting the gaps is the classic bug: it misses every even-length palindrome."),
            key("""
            For each of the `2n - 1` centers, start `lo` and `hi` on it (the same letter, or the two letters around a gap)
            and move them outward while `s[lo] == s[hi]`. The palindrome is `s[lo + 1 .. hi - 1]`, length `hi - lo - 1`.
            O(n²) time worst case, O(1) extra space.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The question is about palindromic *substrings* (contiguous pieces): the longest one, how many there are, the
            longest around a position, or palindromes with a twist (one mismatch allowed, a custom notion of
            "matching"). With `n` up to a few thousand, O(n²) is fine.
            """,
            table(
                ["The problem says…", "at each center"],
                ["the longest palindromic substring", "keep the longest span"],
                ["how many palindromic substrings", "every step of growth is one more palindrome"],
                ["palindromes allowing one mismatch", "grow past the first mismatch, stop at the second"],
                ["pairs that \"match\" in a custom way", "replace `==` with your own test"],
            ),
            """
            Not a fit:

            - Palindromic *subsequences* (letters may be skipped). Growing from a center only sees contiguous text.
              That's dynamic programming.
            - Is the whole string a palindrome? Two pointers from the ends (*Palindrome checks*) is simpler.
            - `n` around 10⁵ or more and you need every center. O(n²) is too slow; Manacher's algorithm gets the same
              answers in O(n) by reusing work, or use hashing with binary search.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Every palindrome has exactly one center

            A palindrome of odd length `2r + 1` is centred on its middle letter, and one of even length `2r` on the gap
            between its two middle letters. Number the centers `0, 1, …, 2n - 2`: even `c` is the letter `c / 2`, odd
            `c` is the gap after letter `c / 2`. So "every palindrome" means "every center, and every radius up to the
            longest at that center".

            ### Palindromes around one center are nested

            If `s[lo..hi]` is a palindrome, so is `s[lo + 1..hi - 1]`: strip one letter from each end and the rest still
            reads the same both ways. So the palindromes at one center are a nested family, and growing outward finds
            them in order. The first mismatch ends the family, since every longer candidate contains that pair.
            """,
            walk(ew, legend=E_LEGEND),
            """
            ### Starting positions

            For center `c`, the code starts with `lo = c // 2` and `hi = c // 2 + c % 2`. On a letter center that's the
            same index twice (a single letter always matches itself, so the first step grows to length 1). On a gap
            center it's the two letters around the gap, which might not match, giving length 0. After the loop, the
            palindrome is everything strictly between `lo` and `hi`, so its length is `hi - lo - 1`.

            ### Cost

            Each center grows at most to the nearer end of the string, so the total is O(n²) in the worst case. That
            happens on strings like `"aaaa…"`, where every center grows all the way. On ordinary text most centers stop
            after a step or two, so it's usually much faster than the bound. No arrays are needed beyond the answer.
            """,
        ]),
        ("template", "The template", [
            """
            For every center of `s`, the length of the longest palindrome centred there. This one array answers most
            questions about palindromic substrings.
            """,
            code(
                "Longest palindrome at every center",
                CENTERS,
                [
                    ("n", "The string's length, and room for one answer per center.",
                     {"java": "`Math.max(0, …)` keeps an empty string from asking for an array of size -1."}),
                    ("centers", "`2n - 1` centers: `n` letters and `n - 1` gaps between them."),
                    ("start", "On a letter (even `c`), both pointers start on it. On a gap (odd `c`), they start on the two "
                              "letters around it."),
                    ("grow", "Move outward while both pointers are inside the string and their letters match."),
                    ("len", "The palindrome is strictly between `lo` and `hi`."),
                    ("ret", "One length per center.", {"c": "C writes into the caller's `out` and returns how many centers there were."}),
                ],
                CENTERS_RUN,
                'longest_at_centers("abaab"); ("aaaa"); ("x"); ("")',
            ),
            """
            In `"aaaa"` every center grows to the edge: 1, 2, 3, 4, 3, 2, 1. That's the worst case for the running time.
            An empty string has no centers and prints an empty line.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "The first example, one center per step. The bars collect the answer:",
            walk(tw, legend=T_LEGEND),
            """
            On paper, write the string with a small gap between letters and number the 2n - 1 positions (letters and
            gaps). At each one, draw an arc outward as far as the letters match.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### A different kind of "match"

            In DNA, a stretch is called palindromic when reading one strand forwards gives the same as reading its
            partner strand backwards: each base pairs with its complement (A with T, C with G). So the check at each
            step is `comp[s[lo]] == s[hi]` instead of `s[lo] == s[hi]`. A base is never its own complement, so only gap
            centers can grow. In `{DNA}` the longest such stretch is `{DSITE}`, at index {DB[0]}. Nothing else about the
            loop changes.

            ### Comparing to checking every substring

            The direct approach checks every substring for being a palindrome: O(n²) substrings, O(n) to check each,
            O(n³) total. For `n = {N:,}` that's billions of steps against at most about {N * N // 2:,} for growing from
            centers. The saving comes from nesting: a center reuses the check of the smaller palindrome inside, instead
            of starting over for each length.

            ### Manacher's algorithm

            When a center sits inside a big palindrome found earlier, its mirror image on the other side of that
            palindrome has already been grown, and the two must look the same as far as the big palindrome reaches.
            Manacher's algorithm uses that to skip ahead, and gets every center's answer in O(n) total. It's worth
            knowing exists for `n` around 10⁵; for interviews the plain version is usually what's expected.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### One mismatch allowed

            The longest substring that becomes a palindrome if you change at most one letter. Growing still works,
            because the property is still nested: if a stretch has at most one mismatched pair, so does every stretch
            inside it with the same center. So grow past the first mismatch, counting it, and stop at the second.
            """,
            code(
                "Longest palindrome with one letter changed",
                ONEFIX,
                [
                    ("init", "Length and best answer so far."),
                    ("centers", "Every letter and every gap, starting the same way as the template."),
                    ("fixes", "How many mismatched pairs this center has used."),
                    ("grow", "Move outward while inside the string."),
                    ("miss", "A mismatched pair. The first one is allowed (change one of the two letters); the second one ends "
                             "this center."),
                    ("best", "Everything strictly between `lo` and `hi` has at most one mismatched pair."),
                    ("ret", "The longest such substring."),
                ],
                ONEFIX_RUN,
                'longest_one_fix("abcda"); ("abcd"); ("racecar"); ("ab"); ("")',
            ),
            """
            `"abcd"` gives 3: `"abc"` becomes `"aba"` by changing one letter. Any two letters can become a
            palindrome with one change, so `"ab"` gives 2.

            ### Counting instead of measuring

            The growth loop passes through every palindrome at its center, one per step. So questions that count
            palindromic substrings, or need all of them, can do their work inside the loop instead of only at the end.

            ### Using the radius array

            Many problems need "is `s[i..j]` a palindrome?" for lots of pairs. A substring is a palindrome exactly when
            the longest palindrome at its center is at least as long as the substring, so after one O(n²) (or Manacher
            O(n)) pass, each such question is a single lookup.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            O(n²) time in the worst case (every center grows to an edge, as in `"aaaa…"`), usually far less on real text.
            O(1) extra space besides the answer. Manacher's algorithm brings the time down to O(n).
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Check every substring", "O(n³)", "O(1)"],
                ["Dynamic programming table `pal[i][j]`", "O(n²)", "O(n²)"],
                ["Expand around every center", "O(n²) worst, often near O(n)", "O(1)"],
                ["Manacher's algorithm", "O(n)", "O(n)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `s[lo + 1:hi]` gives the palindrome after the loop. Building the answer as a slice each time is O(n); store the
            indices and slice once at the end. `s == s[::-1]` checks a whole string, but inside the loop compare single
            characters.

            ### Java

            `charAt` in the loop; `substring(lo + 1, hi)` at the end. Avoid building substrings inside the loop, which
            makes it O(n³).

            ### C++

            `s.substr(start, length)` takes a length, not an end index: `s.substr(lo + 1, hi - lo - 1)`. Cast `size()`
            to `int` before computing `2 * n - 1`, or an empty string wraps around to a huge unsigned number.

            ### C

            `strlen` once, before the loop. Copy a palindrome out with `memcpy` plus a `'\\0'`, or just report its start
            and length.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Only trying letter centers, which misses every even-length palindrome.
            - Off by one in the length: after the loop the palindrome is `hi - lo - 1` long, not `hi - lo + 1`.
            - Checking bounds after reading `s[lo]` and `s[hi]` instead of before.
            - Building substrings inside the growth loop, which adds a factor of `n`.
            - `2 * n - 1` with an unsigned length in C++ on an empty string.
            - Using it for subsequences, where letters can be skipped.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("How many centers does a string of length 6 have, and why?",
                 "11: six letters for odd-length palindromes, and five gaps between letters for even-length ones."),
                ("Why can growing stop at the first mismatch?",
                 "Every longer stretch around the same center contains that mismatched pair at matching positions, so none of them can be a palindrome."),
                ("After the loop, `lo = 1` and `hi = 6`. Where is the palindrome and how long is it?",
                 "Strictly between them: indices 2 to 5, length 6 - 1 - 1 = 4."),
                ("What input makes this O(n²), and what makes it fast?",
                 "A string of one repeated letter, where every center grows to the edge. Text where neighbours rarely match stops almost every center after one step."),
                ("Why does \"one mismatch allowed\" still work with growing?",
                 "Mismatched pairs only accumulate as you grow, so if a stretch has at most one, every smaller stretch around the same center does too. The valid stretches are still nested."),
            ),
        ]),
    ],
)
