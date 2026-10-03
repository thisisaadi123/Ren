"""Strings: palindromes by expanding around centres (and Manacher)."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def centres_walk(title, s, mode):
    """Walkthrough of expansion around every centre. mode: count | longest."""
    w = Steps(title)
    n = len(s)
    total, best = 0, (1, 0)
    for c in range(2 * n - 1):
        i, j = c // 2, c // 2 + c % 2
        found = 0
        while i >= 0 and j < n and s[i] == s[j]:
            found += 1
            i -= 1
            j += 1
        total += found
        length = j - i - 1
        new_best = length > best[0]
        if new_best:
            best = (length, i + 1)
        if found:
            where = f"letter {c // 2} ('{s[c // 2]}')" if c % 2 == 0 else f"the gap between {c // 2} and {c // 2 + 1}"
            stop = f"'{s[i]}' ≠ '{s[j]}'" if i >= 0 and j < n else "the edge of the string"
            gain = f" +{found} palindromes." if mode == "count" else (" New longest." if new_best else "")
            w.step(f"Centre on {where}: expands {found} step(s) to '{s[i + 1:j]}', then stops at {stop}.{gain}", Row(list(s), st={**{t: "found" for t in range(i + 1, j)}, **({i: "mark"} if i >= 0 else {}), **({j: "mark"} if j < n else {})}, ptr={"i": max(i, 0), "j": min(j, n - 1)}), Vars(**({"palindromes": total} if mode == "count" else {"longest": best[0]})))
    return w, total, best


@problem
def count_mirrors():
    s = "abaab"
    n = len(s)
    want = sum(1 for i in range(n) for j in range(i + 1, n + 1) if s[i:j] == s[i:j][::-1])

    w1 = Steps("Check every substring directly.")
    pals = [s[i:j] for i in range(n) for j in range(i + 1, n + 1) if s[i:j] == s[i:j][::-1]]
    w1.step(f"{n * (n + 1) // 2} substrings to test.", Row(list(s)))
    w1.step(f"The palindromes: {pals}.", Row(list(s)), result=len(pals))

    w2 = Steps("dp[i][j] says whether s[i..j] is a palindrome: true when the ends match and the inside is a palindrome.")
    w2.step("Length 1: every letter. Length 2: equal neighbours.", Row(list(s)))
    w2.step(f"Longer lengths reuse shorter results; counting the true cells gives {want}.", Row(list(s)), result=want)

    w3, total, _ = centres_walk("Every palindrome has a centre (a letter or a gap). Expand around each of the 2n − 1 centres, counting each successful step.", s, "count")
    w3.step(f"Total: {total}.", result=total)

    sol(
        "count-mirrors",
        summary="""
            Every palindromic substring has a centre: a letter (odd length) or the gap between two letters (even length).
            From each of the 2n − 1 centres, expand outward while the two ends match; every successful step is one more
            palindrome. O(n²) time, O(1) space.
        """,
        question=[
            """
            Count palindromic substrings of `s`; equal substrings at different positions count separately.

            - **Single letters count.**
            - **n ≤ 2000**: about 2 × 10⁶ substrings.
            """
        ],
        think=[
            f"""
            `"{s}"` has **{want}** palindromic substrings: {pals}.

            Checking each substring separately repeats work: if `s[i..j]` is a palindrome, then `s[i−1..j+1]` is one exactly
            when its two new ends match. So grow palindromes outward from their centres, and stop at the first mismatch.
            """,
            fig(Row(list(s), label="s")),
        ],
        approaches=[
            approach(
                "Check every substring",
                "brute",
                "O(n³)",
                "O(1)",
                idea=["For every pair `i ≤ j`, test `s[i..j]` with two pointers."],
                walk=w1,
                build=["All substrings.", "Two-pointer palindrome test."],
                code={
                    "python": """
                        class Solution:
                            def countMirrors(self, s: str) -> int:
                                n, total = len(s), 0  #@init
                                for i in range(n):  #@all
                                    for j in range(i, n):  #@all
                                        a, b = i, j  #@test
                                        while a < b and s[a] == s[b]:  #@test
                                            a, b = a + 1, b - 1  #@test
                                        if a >= b:  #@test
                                            total += 1  #@test
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countMirrors(String s) {
                                int n = s.length(), total = 0;  //@init
                                for (int i = 0; i < n; i++)  //@all
                                    for (int j = i; j < n; j++) {  //@all
                                        int a = i, b = j;  //@test
                                        while (a < b && s.charAt(a) == s.charAt(b)) { a++; b--; }  //@test
                                        if (a >= b) total++;  //@test
                                    }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countMirrors(string& s) {
                                int n = s.size(), total = 0;  //@init
                                for (int i = 0; i < n; i++)  //@all
                                    for (int j = i; j < n; j++) {  //@all
                                        int a = i, b = j;  //@test
                                        while (a < b && s[a] == s[b]) { a++; b--; }  //@test
                                        if (a >= b) total++;  //@test
                                    }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countMirrors(char* s) {
                            int n = strlen(s), total = 0;  //@init
                            for (int i = 0; i < n; i++)  //@all
                                for (int j = i; j < n; j++) {  //@all
                                    int a = i, b = j;  //@test
                                    while (a < b && s[a] == s[b]) { a++; b--; }  //@test
                                    if (a >= b) total++;  //@test
                                }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("init", "The count."), ("all", "Every substring `s[i..j]`."), ("test", "Two pointers from its ends; it's a palindrome if they meet without a mismatch."), ("ret", "Total.")],
                complexity=["**Time O(n³)** in the worst case (e.g. all one letter). **Space O(1).**"],
                limits=["Re-tests the inside of every substring. A palindrome's inside is a smaller palindrome, which a table or centre expansion reuses."],
                slow=True,
            ),
            approach(
                "Dynamic programming table",
                "better",
                "O(n²)",
                "O(n²)",
                idea=["`pal[i][j]` is true when `s[i] == s[j]` and (`j − i < 2` or `pal[i+1][j−1]`). Fill by increasing length (or `i` from the end) and count the true cells."],
                walk=w2,
                build=["Table of booleans.", "Fill from short to long substrings.", "Count."],
                code={
                    "python": """
                        class Solution:
                            def countMirrors(self, s: str) -> int:
                                n, total = len(s), 0  #@init
                                pal = [[False] * n for _ in range(n)]  #@init
                                for i in range(n - 1, -1, -1):  #@fill
                                    for j in range(i, n):  #@fill
                                        if s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1]):  #@rule
                                            pal[i][j] = True  #@rule
                                            total += 1  #@rule
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countMirrors(String s) {
                                int n = s.length(), total = 0;  //@init
                                boolean[][] pal = new boolean[n][n];  //@init
                                for (int i = n - 1; i >= 0; i--)  //@fill
                                    for (int j = i; j < n; j++)  //@fill
                                        if (s.charAt(i) == s.charAt(j) && (j - i < 2 || pal[i + 1][j - 1])) { pal[i][j] = true; total++; }  //@rule
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countMirrors(string& s) {
                                int n = s.size(), total = 0;  //@init
                                vector<vector<char>> pal(n, vector<char>(n, 0));  //@init
                                for (int i = n - 1; i >= 0; i--)  //@fill
                                    for (int j = i; j < n; j++)  //@fill
                                        if (s[i] == s[j] && (j - i < 2 || pal[i + 1][j - 1])) { pal[i][j] = 1; total++; }  //@rule
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countMirrors(char* s) {
                            int n = strlen(s), total = 0;  //@init
                            char* pal = calloc((size_t) n * n, 1);  //@init
                            for (int i = n - 1; i >= 0; i--)  //@fill
                                for (int j = i; j < n; j++)  //@fill
                                    if (s[i] == s[j] && (j - i < 2 || pal[(i + 1) * n + j - 1])) { pal[i * n + j] = 1; total++; }  //@rule
                            free(pal);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("init", "A table for every substring.", {"c": "A flat n × n array."}), ("fill", "Rows from the bottom up, so `pal[i+1][…]` is ready when row `i` needs it."), ("rule", "Matching ends around a palindromic (or empty / single) inside."), ("ret", "Count of true cells.")],
                complexity=["**Time O(n²).** **Space O(n²):** 4 × 10⁶ cells for n = 2000."],
                limits=["The table is only read one diagonal step away. Expanding from each centre gets the same answers with O(1) memory."],
            ),
            approach(
                "Expand around every centre",
                "best",
                "O(n²)",
                "O(1)",
                idea=["For each centre `c` in `0..2n−2` (`i = c / 2`, `j = i + c % 2`): while `s[i] == s[j]`, count one and widen."],
                walk=w3,
                build=["Loop over 2n − 1 centres.", "Expand while the ends match.", "Count every step."],
                code={
                    "python": """
                        class Solution:
                            def countMirrors(self, s: str) -> int:
                                n, total = len(s), 0  #@init
                                for c in range(2 * n - 1):  #@centre
                                    i, j = c // 2, c // 2 + c % 2  #@centre
                                    while i >= 0 and j < n and s[i] == s[j]:  #@expand
                                        total += 1  #@expand
                                        i, j = i - 1, j + 1  #@expand
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countMirrors(String s) {
                                int n = s.length(), total = 0;  //@init
                                for (int c = 0; c < 2 * n - 1; c++) {  //@centre
                                    int i = c / 2, j = c / 2 + c % 2;  //@centre
                                    while (i >= 0 && j < n && s.charAt(i) == s.charAt(j)) { total++; i--; j++; }  //@expand
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countMirrors(string& s) {
                                int n = s.size(), total = 0;  //@init
                                for (int c = 0; c < 2 * n - 1; c++) {  //@centre
                                    int i = c / 2, j = c / 2 + c % 2;  //@centre
                                    while (i >= 0 && j < n && s[i] == s[j]) { total++; i--; j++; }  //@expand
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countMirrors(char* s) {
                            int n = strlen(s), total = 0;  //@init
                            for (int c = 0; c < 2 * n - 1; c++) {  //@centre
                                int i = c / 2, j = c / 2 + c % 2;  //@centre
                                while (i >= 0 && j < n && s[i] == s[j]) { total++; i--; j++; }  //@expand
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("init", "The count."), ("centre", "Even `c`: centre on letter `c/2` (odd-length palindromes). Odd `c`: centre on the gap after it (even lengths)."), ("expand", "Each matching step outward is one more palindrome; the first mismatch ends this centre."), ("ret", "Total.")],
                complexity=["**Time O(n²)** in the worst case (all one letter), much less typically. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Palindromic substrings ↔ centres:** 2n − 1 of them (letters and gaps).
            - Expansion is O(n²) with O(1) memory; the DP table is the same idea with O(n²) memory.
            - Manacher's algorithm counts them in O(n) (see Palindrome Census).
            """
        ],
    )


def longest_common(s):
    n = len(s)
    best_len, best_i = 1, 0
    for c in range(2 * n - 1):
        i, j = c // 2, c // 2 + c % 2
        while i >= 0 and j < n and s[i] == s[j]:
            i -= 1; j += 1
        if j - i - 1 > best_len:
            best_len, best_i = j - i - 1, i + 1
    return best_len, best_i


EXPAND_BEST = {
    "python": """
                        class Solution:
                            def {fn}(self, s: str) -> {ret}:
                                n = len(s)  #@init
                                best_len, best_i = 1, 0  #@init
                                for c in range(2 * n - 1):  #@centre
                                    i, j = c // 2, c // 2 + c % 2  #@centre
                                    while i >= 0 and j < n and s[i] == s[j]:  #@expand
                                        i, j = i - 1, j + 1  #@expand
                                    if j - i - 1 > best_len:  #@keep
                                        best_len, best_i = j - i - 1, i + 1  #@keep
                                return {result}  #@ret
    """,
    "java": """
                        class Solution {{
                            public {jret} {fn}(String s) {{
                                int n = s.length(), bestLen = 1, bestI = 0;  //@init
                                for (int c = 0; c < 2 * n - 1; c++) {{  //@centre
                                    int i = c / 2, j = c / 2 + c % 2;  //@centre
                                    while (i >= 0 && j < n && s.charAt(i) == s.charAt(j)) {{ i--; j++; }}  //@expand
                                    if (j - i - 1 > bestLen) {{ bestLen = j - i - 1; bestI = i + 1; }}  //@keep
                                }}
                                return {jresult};  //@ret
                            }}
                        }}
    """,
    "cpp": """
                        class Solution {{
                        public:
                            {cret} {fn}(string& s) {{
                                int n = s.size(), bestLen = 1, bestI = 0;  //@init
                                for (int c = 0; c < 2 * n - 1; c++) {{  //@centre
                                    int i = c / 2, j = c / 2 + c % 2;  //@centre
                                    while (i >= 0 && j < n && s[i] == s[j]) {{ i--; j++; }}  //@expand
                                    if (j - i - 1 > bestLen) {{ bestLen = j - i - 1; bestI = i + 1; }}  //@keep
                                }}
                                return {cresult};  //@ret
                            }}
                        }};
    """,
    "c": """
                        {ccret} {fn}(char* s) {{
                            int n = strlen(s), bestLen = 1, bestI = 0;  //@init
                            for (int c = 0; c < 2 * n - 1; c++) {{  //@centre
                                int i = c / 2, j = c / 2 + c % 2;  //@centre
                                while (i >= 0 && j < n && s[i] == s[j]) {{ i--; j++; }}  //@expand
                                if (j - i - 1 > bestLen) {{ bestLen = j - i - 1; bestI = i + 1; }}  //@keep
                            }}
                    {ctail}
                        }}
    """,
}

BRUTE_LONGEST = {
    "python": """
                        class Solution:
                            def {fn}(self, s: str) -> {ret}:
                                n = len(s)  #@init
                                best_len, best_i = 1, 0  #@init
                                for i in range(n):  #@all
                                    for j in range(i + best_len, n):  #@all
                                        a, b = i, j  #@test
                                        while a < b and s[a] == s[b]:  #@test
                                            a, b = a + 1, b - 1  #@test
                                        if a >= b:  #@test
                                            best_len, best_i = j - i + 1, i  #@test
                                return {result}  #@ret
    """,
    "java": """
                        class Solution {{
                            public {jret} {fn}(String s) {{
                                int n = s.length(), bestLen = 1, bestI = 0;  //@init
                                for (int i = 0; i < n; i++)  //@all
                                    for (int j = i + bestLen; j < n; j++) {{  //@all
                                        int a = i, b = j;  //@test
                                        while (a < b && s.charAt(a) == s.charAt(b)) {{ a++; b--; }}  //@test
                                        if (a >= b) {{ bestLen = j - i + 1; bestI = i; }}  //@test
                                    }}
                                return {jresult};  //@ret
                            }}
                        }}
    """,
    "cpp": """
                        class Solution {{
                        public:
                            {cret} {fn}(string& s) {{
                                int n = s.size(), bestLen = 1, bestI = 0;  //@init
                                for (int i = 0; i < n; i++)  //@all
                                    for (int j = i + bestLen; j < n; j++) {{  //@all
                                        int a = i, b = j;  //@test
                                        while (a < b && s[a] == s[b]) {{ a++; b--; }}  //@test
                                        if (a >= b) {{ bestLen = j - i + 1; bestI = i; }}  //@test
                                    }}
                                return {cresult};  //@ret
                            }}
                        }};
    """,
    "c": """
                        {ccret} {fn}(char* s) {{
                            int n = strlen(s), bestLen = 1, bestI = 0;  //@init
                            for (int i = 0; i < n; i++)  //@all
                                for (int j = i + bestLen; j < n; j++) {{  //@all
                                    int a = i, b = j;  //@test
                                    while (a < b && s[a] == s[b]) {{ a++; b--; }}  //@test
                                    if (a >= b) {{ bestLen = j - i + 1; bestI = i; }}  //@test
                                }}
                    {ctail}
                        }}
    """,
}


def fill(tmpl, text):
    return {k: v.format(**text) for k, v in tmpl.items()}


LEN_TEXT = {"fn": "longestEcho", "ret": "int", "result": "best_len", "jret": "int", "jresult": "bestLen", "cret": "int", "cresult": "bestLen", "ccret": "int",
            "ctail": "        (void) bestI;  //@ret\n                            return bestLen;  //@ret"}
TEXT_TEXT = {"fn": "longestEchoText", "ret": "str", "result": "s[best_i:best_i + best_len]", "jret": "String", "jresult": "s.substring(bestI, bestI + bestLen)", "cret": "string", "cresult": "s.substr(bestI, bestLen)", "ccret": "char*",
             "ctail": "        char* out = malloc(bestLen + 1);  //@ret\n                            memcpy(out, s + bestI, bestLen);  //@ret\n                            out[bestLen] = '\\0';  //@ret\n                            return out;  //@ret"}


def longest_problem(pid, s, as_text):
    best_len, best_i = longest_common(s)
    want = s[best_i:best_i + best_len] if as_text else best_len
    shown = f"'{want}'" if as_text else str(want)
    n = len(s)

    w1 = Steps("Check substrings from each start, longest-first candidates only: a substring is worth testing only if it would beat the best so far.")
    w1.step(f"Up to {n * (n + 1) // 2} substrings in '{s}'.", Row(list(s)))
    w1.step(f"The longest palindrome found is '{s[best_i:best_i + best_len]}' (length {best_len}).", Row(list(s), st={t: "found" for t in range(best_i, best_i + best_len)}), result=shown)
    w2, _, _ = centres_walk("Expand around each of the 2n − 1 centres; the widest expansion wins (the earliest one on ties, since later ties don't replace it).", s, "longest")
    w2.step(f"Longest: '{s[best_i:best_i + best_len]}'.", result=shown)

    ret_line = "the longest palindrome itself" if as_text else "its length"
    sol(
        pid,
        summary=f"""
            Every palindrome has a centre, a letter or a gap between letters. Expand from each of the 2n − 1 centres while
            the ends match, and remember the widest expansion (only a strictly longer one replaces it, so the leftmost wins
            ties). Return {ret_line}. O(n²) time, O(1) space.
        """,
        question=[
            f"""
            Find the longest substring of `s` that reads the same both ways, and return {ret_line}.

            - **Single letters** are palindromes, so the answer is at least 1.
            - {"**Ties go to the leftmost** palindrome of the greatest length." if as_text else "**Only the length** is needed."}
            - **n ≤ 2000.**
            """
        ],
        think=[
            f"""
            `"{s}"` → {shown}.

            Instead of testing substrings, grow palindromes from their middle. From a centre, extending one letter on each
            side keeps the palindrome as long as the two new letters match, and the first mismatch means nothing wider at
            this centre can work. Even-length palindromes centre on a gap, so there are 2n − 1 centres in total.
            """,
            fig(Row(list(s), label="s")),
        ],
        approaches=[
            approach(
                "Check substrings that could beat the best",
                "brute",
                "O(n³)",
                "O(1)",
                idea=["For each start `i`, test every end `j` that would give a longer palindrome than the best so far, with a two-pointer check."],
                walk=w1,
                build=["Loop over starts and longer-than-best ends.", "Two-pointer test.", "Keep the longest (first found on ties)."],
                code=fill(BRUTE_LONGEST, TEXT_TEXT if as_text else LEN_TEXT),
                lines=[("init", "A single letter is always a palindrome."), ("all", "Only ends that would beat the current best need testing."), ("test", "Two pointers from both ends of `s[i..j]`."), ("ret", f"Return {ret_line}.", {"c": "The text version copies it into a new string." if as_text else "Only the length is returned."})],
                complexity=["**Time O(n³)** in the worst case. **Space O(1).**"],
                limits=["Each substring is re-tested from its ends. Growing palindromes from their centres reuses the inner match."],
                slow=True,
            ),
            approach(
                "Expand around every centre",
                "best",
                "O(n²)",
                "O(1)",
                idea=["For each centre `c` (`i = c / 2`, `j = i + c % 2`), widen while `s[i] == s[j]`. The palindrome is `s[i+1..j−1]`; keep it if strictly longer than the best."],
                walk=w2,
                build=["Loop over centres.", "Expand.", "Keep the longest (strictly longer replaces)."],
                code=fill(EXPAND_BEST, TEXT_TEXT if as_text else LEN_TEXT),
                lines=[("init", "The best so far: a single letter at position 0."), ("centre", "Letters (even `c`) and gaps (odd `c`)."), ("expand", "Widen while the ends match; afterwards the palindrome is `s[i+1..j−1]`, of length `j − i − 1`."), ("keep", "Strictly longer only, so earlier palindromes win ties (centres are visited left to right)."), ("ret", f"Return {ret_line}.", {"c": "The text version copies it into a new string." if as_text else "Only the length is returned."})],
                complexity=["**Time O(n²)** in the worst case. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Longest palindromic substring = expand around 2n − 1 centres**, O(n²) and O(1) memory.
            - Track the start and length, not the string, until the end.
            - Manacher's algorithm does it in O(n) when n is large.
            """
        ],
    )


@problem
def longest_echo():
    longest_problem("longest-echo", "abacdcaba", False)


@problem
def longest_echo_text():
    longest_problem("longest-echo-text", "xabbaycdcz", True)


@problem
def palindrome_census():
    s = "aabaa"
    n = len(s)
    want = sum(1 for i in range(n) for j in range(i + 1, n + 1) if s[i:j] == s[i:j][::-1])

    w1, total, _ = centres_walk("Expand around each centre and count every successful step (O(n²) in the worst case).", s, "count")
    w1.step(f"Total: {total}.", result=total)

    t = "^#" + "#".join(s) + "#$"
    p = [0] * len(t)
    center = right = 0
    w2 = Steps("Manacher: put # between letters so every palindrome has odd length, and reuse the mirror image of the current widest palindrome to start each expansion far out.")
    w2.step(f"Transformed: {t}.", Row(list(t)))
    for i in range(1, len(t) - 1):
        mirrored = 0
        if i < right:
            p[i] = min(right - i, p[2 * center - i])
            mirrored = p[i]
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > right:
            center, right = i, i + p[i]
        if i in (5, 6, 7):
            w2.step(f"Position {i}: the mirror gives a head start of {mirrored}; expanding reaches radius {p[i]}.", Row(list(t), st={x: "found" for x in range(i - p[i], i + p[i] + 1)}), Row(p[:i + 1] + ["·"] * (len(t) - i - 1), label="radius"))
    got = sum((r + 1) // 2 for r in p)
    w2.step(f"Each radius r covers (r + 1) // 2 palindromes centred there. Sum: {got}.", Row(p, label="radius"), result=got)

    sol(
        "palindrome-census",
        summary="""
            Manacher's algorithm. Insert `#` between letters (and sentinels at the ends) so every palindrome has odd length.
            For each centre, start its radius from the mirror image inside the rightmost palindrome found so far, then
            expand. Each radius `r` accounts for `(r + 1) / 2` palindromic substrings of `s`. O(n), with a 64-bit total.
        """,
        question=[
            """
            Count every palindromic substring of `s` (single letters included; equal substrings at different positions
            count separately).

            - **n up to 2 × 10⁵**: centre expansion is O(n²) on inputs like `aaaa…a`, too slow.
            - **The count can reach ~2 × 10¹⁰**, beyond 32 bits.
            """
        ],
        think=[
            f"""
            `"{s}"` has **{want}** palindromic substrings.

            Expanding from every centre is quadratic on repetitive strings because neighbouring centres redo the same
            comparisons. Manacher's trick: inside a big palindrome centred at `C`, the picture is mirrored, so the radius at
            position `i` is at least the radius at its mirror `2C − i` (capped at the big palindrome's edge). Only the part
            beyond the right edge needs new comparisons, and that edge only moves right: O(n) total.

            The `#` separators make even and odd palindromes look the same: every palindrome in the new string has a
            centre on a character.
            """,
            fig(Row(list(s), label="s"), Row(list(t), label="with separators")),
        ],
        approaches=[
            approach(
                "Expand around every centre",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each of the 2n − 1 centres, expand while the ends match and count each step."],
                walk=w1,
                build=["Loop over centres.", "Expand and count (64-bit)."],
                code={
                    "python": """
                        class Solution:
                            def palindromeCensus(self, s: str) -> int:
                                n, total = len(s), 0  #@init
                                for c in range(2 * n - 1):  #@centre
                                    i, j = c // 2, c // 2 + c % 2  #@centre
                                    while i >= 0 and j < n and s[i] == s[j]:  #@expand
                                        total += 1  #@expand
                                        i, j = i - 1, j + 1  #@expand
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long palindromeCensus(String s) {
                                int n = s.length();  //@init
                                long total = 0;  //@init
                                for (int c = 0; c < 2 * n - 1; c++) {  //@centre
                                    int i = c / 2, j = c / 2 + c % 2;  //@centre
                                    while (i >= 0 && j < n && s.charAt(i) == s.charAt(j)) { total++; i--; j++; }  //@expand
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long palindromeCensus(string& s) {
                                int n = s.size();  //@init
                                long long total = 0;  //@init
                                for (int c = 0; c < 2 * n - 1; c++) {  //@centre
                                    int i = c / 2, j = c / 2 + c % 2;  //@centre
                                    while (i >= 0 && j < n && s[i] == s[j]) { total++; i--; j++; }  //@expand
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long palindromeCensus(char* s) {
                            int n = strlen(s);  //@init
                            long long total = 0;  //@init
                            for (int c = 0; c < 2 * n - 1; c++) {  //@centre
                                int i = c / 2, j = c / 2 + c % 2;  //@centre
                                while (i >= 0 && j < n && s[i] == s[j]) { total++; i--; j++; }  //@expand
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("init", "A 64-bit total."), ("centre", "Letters and gaps."), ("expand", "Each matching step outward is one palindrome."), ("ret", "Total.")],
                complexity=["**Time O(n²)** worst case: 2 × 10¹⁰ steps on 2 × 10⁵ equal letters. **Space O(1).**"],
                limits=["Neighbouring centres inside a long palindrome repeat the same comparisons. Manacher reuses the mirrored radius so every comparison moves the right edge forward."],
                slow=True,
            ),
            approach(
                "Manacher's algorithm",
                "best",
                "O(n)",
                "O(n)",
                idea=["Build `t = ^#a#b#…#$`. Keep the palindrome reaching furthest right (`center`, `right`). For each `i`: start `p[i]` at `min(right − i, p[2·center − i])` if `i < right`, expand while the neighbours match, and update `center/right`. The answer is `Σ (p[i] + 1) / 2`."],
                walk=w2,
                build=["Transformed string with sentinels.", "Radius array with mirror reuse.", "Sum of `(r + 1) / 2`."],
                code={
                    "python": """
                        class Solution:
                            def palindromeCensus(self, s: str) -> int:
                                t = "^#" + "#".join(s) + "#$"  #@build
                                p = [0] * len(t)  #@build
                                center = right = 0  #@build
                                for i in range(1, len(t) - 1):  #@loop
                                    if i < right:  #@mirror
                                        p[i] = min(right - i, p[2 * center - i])  #@mirror
                                    while t[i + p[i] + 1] == t[i - p[i] - 1]:  #@expand
                                        p[i] += 1  #@expand
                                    if i + p[i] > right:  #@edge
                                        center, right = i, i + p[i]  #@edge
                                return sum((r + 1) // 2 for r in p)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long palindromeCensus(String s) {
                                int n = s.length(), m = 2 * n + 3;  //@build
                                char[] t = new char[m];  //@build
                                t[0] = '^';  //@build
                                t[m - 1] = '$';  //@build
                                for (int i = 0; i < n; i++) { t[2 * i + 1] = '#'; t[2 * i + 2] = s.charAt(i); }  //@build
                                t[2 * n + 1] = '#';  //@build
                                int[] p = new int[m];  //@build
                                int center = 0, right = 0;  //@build
                                long total = 0;  //@build
                                for (int i = 1; i < m - 1; i++) {  //@loop
                                    if (i < right) p[i] = Math.min(right - i, p[2 * center - i]);  //@mirror
                                    while (t[i + p[i] + 1] == t[i - p[i] - 1]) p[i]++;  //@expand
                                    if (i + p[i] > right) { center = i; right = i + p[i]; }  //@edge
                                    total += (p[i] + 1) / 2;  //@ret
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long palindromeCensus(string& s) {
                                string t = "^#";  //@build
                                for (char c : s) { t += c; t += '#'; }  //@build
                                t += '$';  //@build
                                int m = t.size(), center = 0, right = 0;  //@build
                                vector<int> p(m, 0);  //@build
                                long long total = 0;  //@build
                                for (int i = 1; i < m - 1; i++) {  //@loop
                                    if (i < right) p[i] = min(right - i, p[2 * center - i]);  //@mirror
                                    while (t[i + p[i] + 1] == t[i - p[i] - 1]) p[i]++;  //@expand
                                    if (i + p[i] > right) { center = i; right = i + p[i]; }  //@edge
                                    total += (p[i] + 1) / 2;  //@ret
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long palindromeCensus(char* s) {
                            int n = strlen(s), m = 2 * n + 3;  //@build
                            char* t = malloc(m + 1);  //@build
                            t[0] = '^';  //@build
                            for (int i = 0; i < n; i++) { t[2 * i + 1] = '#'; t[2 * i + 2] = s[i]; }  //@build
                            t[2 * n + 1] = '#';  //@build
                            t[m - 1] = '$';  //@build
                            t[m] = '\\0';  //@build
                            int* p = calloc(m, sizeof(int));  //@build
                            int center = 0, right = 0;  //@build
                            long long total = 0;  //@build
                            for (int i = 1; i < m - 1; i++) {  //@loop
                                if (i < right) p[i] = right - i < p[2 * center - i] ? right - i : p[2 * center - i];  //@mirror
                                while (t[i + p[i] + 1] == t[i - p[i] - 1]) p[i]++;  //@expand
                                if (i + p[i] > right) { center = i; right = i + p[i]; }  //@edge
                                total += (p[i] + 1) / 2;  //@ret
                            }
                            free(t); free(p);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("build", "`#` between letters makes every palindrome odd-length; the distinct sentinels `^` and `$` stop expansion without bounds checks. `p[i]` will be the radius at `i`."),
                    ("loop", "Every position of the transformed string."),
                    ("mirror", "Inside the rightmost palindrome, position `i` mirrors `2·center − i`, so its radius is at least the mirror's (but not past `right`, which we haven't verified)."),
                    ("expand", "Compare beyond what's known. Every successful comparison pushes the right edge further, so all expansions together are O(n)."),
                    ("edge", "Track the palindrome reaching furthest right."),
                    ("ret", "A radius `r` in `t` is a palindrome of length `r` in `s`; centred there are `(r + 1) / 2` palindromes of `s` (lengths r, r − 2, …). Sum in 64 bits."),
                ],
                complexity=["**Time O(n).** **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - **Manacher** gives every centre's palindrome radius in O(n), via mirror reuse.
            - Separators unify odd and even palindromes; sentinels remove bounds checks.
            - From radii you can count palindromes or find the longest one.
            """
        ],
    )
