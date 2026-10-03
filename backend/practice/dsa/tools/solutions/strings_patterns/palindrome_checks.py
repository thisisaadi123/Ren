"""Strings: checking palindromes with two pointers."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def is_pal(t):
    return t == t[::-1]


@problem
def mirror_sentence():
    text = "Step on no pets!"
    kept = [c.lower() for c in text if c.isalnum()]
    want = kept == kept[::-1]

    w1 = Steps("Keep only letters and digits, lowercase them, and compare the result with its reverse.")
    w1.step(f"Cleaned: {''.join(kept)}.", Row(kept))
    w1.step(f"Reversed: {''.join(kept[::-1])}. Equal: {str(want).lower()}.", Row(kept), Row(kept[::-1], label="reversed"), result=str(want).lower())

    w2 = Steps("Two pointers from the ends skip anything that isn't a letter or digit, and compare letters ignoring case.")
    i, j = 0, len(text) - 1
    while i < j:
        if not text[i].isalnum():
            i += 1
        elif not text[j].isalnum():
            j -= 1
        else:
            w2.step(f"'{text[i]}' and '{text[j]}' match (ignoring case).", Row(list(text), st={i: "active", j: "active"}, ptr={"i": i, "j": j}))
            i += 1
            j -= 1
    w2.step("The pointers met without a mismatch: true.", result=str(want).lower())

    sol(
        "mirror-sentence",
        summary="""
            Two pointers from both ends: each skips characters that aren't letters or digits, then the two characters are
            compared case-insensitively. A mismatch means no; meeting in the middle means yes. O(n), no extra memory.
        """,
        question=[
            """
            Ignoring everything except letters and digits, and ignoring case, does `text` read the same both ways?

            - **No letters or digits at all** counts as a mirror.
            - **Up to 2 × 10⁵ characters.**
            """
        ],
        think=[
            f"""
            `"{text}"` → `{''.join(kept)}`, which reads the same backwards: **{str(want).lower()}**.

            Building the cleaned string costs memory; instead, let the pointers simply step over the characters that don't
            count.
            """,
            fig(Row(list(text), label="text")),
        ],
        approaches=[
            approach(
                "Clean, then compare with the reverse",
                "better",
                "O(n)",
                "O(n)",
                idea=["Build the lowercase string of letters and digits; compare it with its reverse."],
                walk=w1,
                build=["Filter and lowercase.", "Compare with the reverse."],
                code={
                    "python": """
                        class Solution:
                            def isMirror(self, text: str) -> bool:
                                kept = [c.lower() for c in text if c.isalnum()]  #@clean
                                return kept == kept[::-1]  #@cmp
                    """,
                    "java": """
                        class Solution {
                            public boolean isMirror(String text) {
                                StringBuilder kept = new StringBuilder();  //@clean
                                for (char c : text.toCharArray()) if (Character.isLetterOrDigit(c)) kept.append(Character.toLowerCase(c));  //@clean
                                String a = kept.toString();  //@cmp
                                return a.equals(kept.reverse().toString());  //@cmp
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool isMirror(string& text) {
                                string kept;  //@clean
                                for (char c : text) if (isalnum((unsigned char) c)) kept += tolower((unsigned char) c);  //@clean
                                return kept == string(kept.rbegin(), kept.rend());  //@cmp
                            }
                        };
                    """,
                    "c": """
                        #include <ctype.h>

                        bool isMirror(char* text) {
                            int n = strlen(text), m = 0;  //@clean
                            char* kept = malloc(n + 1);  //@clean
                            for (int i = 0; i < n; i++) if (isalnum((unsigned char) text[i])) kept[m++] = tolower((unsigned char) text[i]);  //@clean
                            bool ok = true;  //@cmp
                            for (int i = 0; i < m / 2 && ok; i++) if (kept[i] != kept[m - 1 - i]) ok = false;  //@cmp
                            free(kept);  //@cmp
                            return ok;  //@cmp
                        }
                    """,
                },
                lines=[("clean", "Only letters and digits, lowercased."), ("cmp", "A palindrome equals its reverse.")],
                complexity=["**Time O(n).** **Space O(n)** for the cleaned copy."],
                limits=["The cleaned copy is unnecessary: the pointers can skip ignored characters as they go."],
            ),
            approach(
                "Two pointers that skip",
                "best",
                "O(n)",
                "O(1)",
                idea=["`i` from the left, `j` from the right. Skip non-alphanumeric characters on either side; compare lowercase letters; move inward."],
                walk=w2,
                build=["Pointers at both ends.", "Skip, compare, move."],
                code={
                    "python": """
                        class Solution:
                            def isMirror(self, text: str) -> bool:
                                i, j = 0, len(text) - 1  #@init
                                while i < j:  #@loop
                                    if not text[i].isalnum():  #@skip
                                        i += 1  #@skip
                                    elif not text[j].isalnum():  #@skip
                                        j -= 1  #@skip
                                    elif text[i].lower() != text[j].lower():  #@cmp
                                        return False  #@cmp
                                    else:  #@cmp
                                        i += 1  #@cmp
                                        j -= 1  #@cmp
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean isMirror(String text) {
                                int i = 0, j = text.length() - 1;  //@init
                                while (i < j) {  //@loop
                                    char a = text.charAt(i), b = text.charAt(j);  //@loop
                                    if (!Character.isLetterOrDigit(a)) i++;  //@skip
                                    else if (!Character.isLetterOrDigit(b)) j--;  //@skip
                                    else if (Character.toLowerCase(a) != Character.toLowerCase(b)) return false;  //@cmp
                                    else { i++; j--; }  //@cmp
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool isMirror(string& text) {
                                int i = 0, j = (int) text.size() - 1;  //@init
                                while (i < j) {  //@loop
                                    unsigned char a = text[i], b = text[j];  //@loop
                                    if (!isalnum(a)) i++;  //@skip
                                    else if (!isalnum(b)) j--;  //@skip
                                    else if (tolower(a) != tolower(b)) return false;  //@cmp
                                    else { i++; j--; }  //@cmp
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        #include <ctype.h>

                        bool isMirror(char* text) {
                            int i = 0, j = (int) strlen(text) - 1;  //@init
                            while (i < j) {  //@loop
                                unsigned char a = text[i], b = text[j];  //@loop
                                if (!isalnum(a)) i++;  //@skip
                                else if (!isalnum(b)) j--;  //@skip
                                else if (tolower(a) != tolower(b)) return false;  //@cmp
                                else { i++; j--; }  //@cmp
                            }
                            return true;  //@ret
                        }
                    """,
                },
                lines=[("init", "Pointers at both ends."), ("loop", "Until they meet."), ("skip", "Characters that don't count are stepped over, one side at a time."), ("cmp", "Two counted characters must match ignoring case."), ("ret", "No mismatch (including text with nothing to compare).")],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Filtered palindrome = two pointers that skip** ignored characters.
            - Normalise case at comparison time instead of building a copy.
            - Empty or all-ignored input is a palindrome.
            """
        ],
    )


@problem
def one_slip_palindrome():
    s = "racecxar"
    n = len(s)
    want = any(is_pal(s[:k] + s[k + 1:]) for k in range(n)) or is_pal(s)

    w1 = Steps("Try deleting each character in turn and check whether the rest is a palindrome.")
    for k in range(n):
        t = s[:k] + s[k + 1:]
        w1.step(f"Delete position {k} ('{s[k]}'): {t} is {'a palindrome' if is_pal(t) else 'not a palindrome'}.", Row(list(s), st={k: "mark"}))
        if is_pal(t):
            break
    w1.step(f"Answer: {str(want).lower()}.", result=str(want).lower())

    w2 = Steps("Match from both ends. At the first mismatch, the extra character is one of the two; check both remaining middles.")
    i, j = 0, n - 1
    while i < j and s[i] == s[j]:
        w2.step(f"'{s[i]}' = '{s[j]}'.", Row(list(s), st={i: "found", j: "found"}, ptr={"i": i, "j": j}))
        i += 1
        j -= 1
    if i < j:
        a, b = s[i + 1:j + 1], s[i:j]
        w2.step(f"Mismatch '{s[i]}' ≠ '{s[j]}'. Skip the left one: '{a}' is {'a palindrome' if is_pal(a) else 'not'}; skip the right one: '{b}' is {'a palindrome' if is_pal(b) else 'not'}.", Row(list(s), st={i: "mark", j: "mark"}, ptr={"i": i, "j": j}))
    w2.step(f"Answer: {str(want).lower()}.", result=str(want).lower())

    sol(
        "one-slip-palindrome",
        summary="""
            Compare from both ends. If everything matches, it's already a palindrome. At the first mismatch, the extra
            character must be one of the two mismatched ones (all outer pairs already match), so check whether the middle
            without the left one, or without the right one, is a palindrome. O(n).
        """,
        question=[
            """
            Can `s` become a palindrome by deleting **at most one** character?

            - **Zero deletions** is fine if `s` is already a palindrome.
            - **Up to 10⁵ letters.**
            """
        ],
        think=[
            f"""
            `"{s}"`: deleting the `x` leaves `racecar`: **{str(want).lower()}**.

            Matching pairs from the outside in, the first mismatching pair `s[i] ≠ s[j]` can't both stay. Deleting a
            character outside `[i, j]` would break a pair that already matched, so the deletion is `s[i]` or `s[j]`, and
            only two checks are needed.
            """,
            fig(Row(list(s), label="s")),
        ],
        approaches=[
            approach(
                "Try every deletion",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["If `s` is a palindrome, true. Otherwise try removing each position and test the rest."],
                walk=w1,
                build=["Palindrome check helper (skipping one index).", "Try every index."],
                code={
                    "python": """
                        class Solution:
                            def oneSlip(self, s: str) -> bool:
                                def pal_without(skip):  #@check
                                    t = s[:skip] + s[skip + 1:]  #@check
                                    return t == t[::-1]  #@check
                                if s == s[::-1]:  #@zero
                                    return True  #@zero
                                return any(pal_without(k) for k in range(len(s)))  #@try
                    """,
                    "java": """
                        class Solution {
                            private boolean palWithout(String s, int skip) {  //@check
                                int i = 0, j = s.length() - 1;  //@check
                                while (i < j) {  //@check
                                    if (i == skip) { i++; continue; }  //@check
                                    if (j == skip) { j--; continue; }  //@check
                                    if (s.charAt(i++) != s.charAt(j--)) return false;  //@check
                                }
                                return true;  //@check
                            }  //@check

                            public boolean oneSlip(String s) {
                                if (palWithout(s, -1)) return true;  //@zero
                                for (int k = 0; k < s.length(); k++) if (palWithout(s, k)) return true;  //@try
                                return false;  //@try
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static bool palWithout(const string& s, int skip) {  //@check
                                int i = 0, j = (int) s.size() - 1;  //@check
                                while (i < j) {  //@check
                                    if (i == skip) { i++; continue; }  //@check
                                    if (j == skip) { j--; continue; }  //@check
                                    if (s[i++] != s[j--]) return false;  //@check
                                }
                                return true;  //@check
                            }  //@check

                        public:
                            bool oneSlip(string& s) {
                                if (palWithout(s, -1)) return true;  //@zero
                                for (int k = 0; k < (int) s.size(); k++) if (palWithout(s, k)) return true;  //@try
                                return false;  //@try
                            }
                        };
                    """,
                    "c": """
                        static bool pal_without(const char* s, int n, int skip) {  //@check
                            int i = 0, j = n - 1;  //@check
                            while (i < j) {  //@check
                                if (i == skip) { i++; continue; }  //@check
                                if (j == skip) { j--; continue; }  //@check
                                if (s[i++] != s[j--]) return false;  //@check
                            }
                            return true;  //@check
                        }  //@check

                        bool oneSlip(char* s) {
                            int n = strlen(s);  //@zero
                            if (pal_without(s, n, -1)) return true;  //@zero
                            for (int k = 0; k < n; k++) if (pal_without(s, n, k)) return true;  //@try
                            return false;  //@try
                        }
                    """,
                },
                lines=[("check", "Is `s` a palindrome when position `skip` is ignored?"), ("zero", "No deletion needed."), ("try", "Every possible single deletion.")],
                complexity=["**Time O(n²).** **Space O(1)** (O(n) in Python for the sliced copies)."],
                limits=["Tries n deletions, each with an O(n) check. Only the two characters at the first mismatch are real candidates."],
                slow=True,
            ),
            approach(
                "Two pointers, branch once at the first mismatch",
                "best",
                "O(n)",
                "O(1)",
                idea=["Move `i`, `j` inward while they match. At the first mismatch, return whether `s[i+1..j]` or `s[i..j−1]` is a palindrome."],
                walk=w2,
                build=["Range palindrome helper.", "Match from both ends.", "At the mismatch, try skipping either side."],
                code={
                    "python": """
                        class Solution:
                            def oneSlip(self, s: str) -> bool:
                                def mirror(i, j):  #@helper
                                    while i < j:  #@helper
                                        if s[i] != s[j]:  #@helper
                                            return False  #@helper
                                        i, j = i + 1, j - 1  #@helper
                                    return True  #@helper
                                i, j = 0, len(s) - 1  #@match
                                while i < j:  #@match
                                    if s[i] != s[j]:  #@branch
                                        return mirror(i + 1, j) or mirror(i, j - 1)  #@branch
                                    i, j = i + 1, j - 1  #@match
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            private boolean mirror(String s, int i, int j) {  //@helper
                                while (i < j) if (s.charAt(i++) != s.charAt(j--)) return false;  //@helper
                                return true;  //@helper
                            }  //@helper

                            public boolean oneSlip(String s) {
                                int i = 0, j = s.length() - 1;  //@match
                                while (i < j) {  //@match
                                    if (s.charAt(i) != s.charAt(j)) return mirror(s, i + 1, j) || mirror(s, i, j - 1);  //@branch
                                    i++;  //@match
                                    j--;  //@match
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static bool mirror(const string& s, int i, int j) {  //@helper
                                while (i < j) if (s[i++] != s[j--]) return false;  //@helper
                                return true;  //@helper
                            }  //@helper

                        public:
                            bool oneSlip(string& s) {
                                int i = 0, j = (int) s.size() - 1;  //@match
                                while (i < j) {  //@match
                                    if (s[i] != s[j]) return mirror(s, i + 1, j) || mirror(s, i, j - 1);  //@branch
                                    i++;  //@match
                                    j--;  //@match
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static bool mirror(const char* s, int i, int j) {  //@helper
                            while (i < j) if (s[i++] != s[j--]) return false;  //@helper
                            return true;  //@helper
                        }  //@helper

                        bool oneSlip(char* s) {
                            int i = 0, j = (int) strlen(s) - 1;  //@match
                            while (i < j) {  //@match
                                if (s[i] != s[j]) return mirror(s, i + 1, j) || mirror(s, i, j - 1);  //@branch
                                i++;  //@match
                                j--;  //@match
                            }
                            return true;  //@ret
                        }
                    """,
                },
                lines=[("helper", "Is `s[i..j]` a palindrome?"), ("match", "Matching outer pairs never need a deletion."), ("branch", "First mismatch: one of these two characters is the slip. Each option is checked once, with no further deletions allowed."), ("ret", "Already a palindrome.")],
                complexity=["**Time O(n):** one pass plus at most two range checks. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **"Palindrome with k deletions":** two pointers, and branch only at a mismatch.
            - With one deletion allowed, only the two mismatched characters are candidates.
            - Larger k needs dynamic programming (longest palindromic subsequence).
            """
        ],
    )


@problem
def cut_out_the_middle():
    s = "abcxyzcba"
    n = len(s)
    best = min(j - i for i in range(n + 1) for j in range(i, n + 1) if is_pal(s[:i] + s[j:]))
    want = best

    l = 0
    while l < n - 1 - l and s[l] == s[n - 1 - l]:
        l += 1
    mid = s[l:n - l]

    w1 = Steps("Try every block [i, j) to cut and check whether what remains is a palindrome.")
    shown = 0
    for i in range(n + 1):
        for j in range(i, n + 1):
            if j - i == want and is_pal(s[:i] + s[j:]) and shown == 0:
                w1.step(f"Cut positions {i}..{j - 1}: '{s[:i]}' + '{s[j:]}' = '{s[:i] + s[j:]}', a palindrome. Length {j - i}.", Row(list(s), st={t: "mark" for t in range(i, j)}))
                shown = 1
    w1.step(f"There are about n²/2 = {n * (n + 1) // 2} blocks; the shortest that works has length {want}.", result=want)

    w2 = Steps("Peel matching letters off both ends. Whatever is left in the middle starts and ends with different letters, so the kept part of it must be a palindromic prefix or a palindromic suffix of the middle.")
    w2.step(f"Peel {l} matching pair(s): '{s[:l]}' ... '{s[n - l:]}'. Middle: '{mid}'.", Row(list(s), st={**{t: "found" for t in range(l)}, **{t: "found" for t in range(n - l, n)}}))
    pre = max(k for k in range(len(mid) + 1) if is_pal(mid[:k]))
    suf = max(k for k in range(len(mid) + 1) if is_pal(mid[len(mid) - k:]))
    w2.step(f"Longest palindromic prefix of the middle: '{mid[:pre]}' ({pre}); longest palindromic suffix: '{mid[len(mid) - suf:]}' ({suf}).", Row(list(mid), label="middle"))
    w2.step(f"Keep the longer one; cut the remaining {len(mid)} − {max(pre, suf)} = {len(mid) - max(pre, suf)}.", result=len(mid) - max(pre, suf))

    w3 = Steps("Find the longest palindromic prefix in linear time: in t + '#' + reverse(t), the longest prefix that is also a suffix is exactly that palindrome (the prefix-function / KMP failure table).")
    u = mid + "#" + mid[::-1]
    pi = [0] * len(u)
    for i in range(1, len(u)):
        k = pi[i - 1]
        while k and u[i] != u[k]:
            k = pi[k - 1]
        if u[i] == u[k]:
            k += 1
        pi[i] = k
    w3.step(f"For the middle '{mid}': '{u}'. The prefix-function's last value is {pi[-1]}.", Row(list(u)), Row(pi, label="prefix function"))
    w3.step(f"Do the same for the reversed middle to get the palindromic suffix, take the larger, and cut the rest: {want}.", result=want)

    sol(
        "cut-out-the-middle",
        summary="""
            Peel off matching letters from both ends (they can always stay). The remaining middle starts and ends with
            different letters, so what we keep from it must be a palindromic prefix or a palindromic suffix of the middle.
            The longest palindromic prefix of `t` is the longest border of `t + '#' + reverse(t)`, found with the KMP prefix
            function in linear time. Answer: middle length minus the longer of the two. O(n).
        """,
        question=[
            """
            Cut one contiguous block (possibly empty) out of `s` so the rest (a prefix plus a suffix) is a palindrome.
            Return the shortest block length.

            - **The kept part is prefix + suffix** of `s`.
            - **Up to 10⁵ letters**: trying every block is ~5 × 10⁹ options.
            """
        ],
        think=[
            f"""
            `"{s}"`: keep `abc` + `cba` around a cut of `xyz`... or better, keep a little more: the answer is **{want}**.

            The outer letters that already match (`{s[:l]}` with `{s[n - l:]}`) can always be kept. In the middle
            `"{mid}"`, the first and last letters differ, so we can't keep both: the kept text inside the middle is entirely
            at its start or entirely at its end, and it has to be a palindrome on its own. So the question becomes: the
            longest palindromic prefix (or suffix) of the middle.

            A palindromic prefix of `t` is a prefix of `t` that equals a suffix of `reverse(t)`. Glue them with a separator,
            `t # reverse(t)`, and the longest prefix that is also a suffix of the whole thing is exactly the longest
            palindromic prefix. The KMP prefix function computes that in O(length).
            """,
            fig(Row(list(s), label="s"), Row(list(mid), label="middle after peeling")),
        ],
        approaches=[
            approach(
                "Try every block",
                "brute",
                "O(n³)",
                "O(n)",
                idea=["For every `i ≤ j`, check whether `s[:i] + s[j:]` is a palindrome; keep the smallest `j − i`."],
                walk=w1,
                build=["Two loops over the block's ends.", "Palindrome check on the kept text without building it."],
                code={
                    "python": """
                        class Solution:
                            def shortestCut(self, s: str) -> int:
                                n, best = len(s), len(s)  #@init
                                for i in range(n + 1):  #@blocks
                                    for j in range(i, n + 1):  #@blocks
                                        if j - i < best:  #@check
                                            kept = s[:i] + s[j:]  #@check
                                            if kept == kept[::-1]:  #@check
                                                best = j - i  #@check
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestCut(String s) {
                                int n = s.length(), best = n;  //@init
                                for (int i = 0; i <= n; i++)  //@blocks
                                    for (int j = i; j <= n; j++) {  //@blocks
                                        if (j - i >= best) continue;  //@check
                                        int m = n - (j - i), a = 0, b = m - 1;  //@check
                                        boolean ok = true;  //@check
                                        while (a < b && ok) {  //@check
                                            char x = s.charAt(a < i ? a : a + j - i), y = s.charAt(b < i ? b : b + j - i);  //@check
                                            if (x != y) ok = false;  //@check
                                            a++; b--;  //@check
                                        }
                                        if (ok) best = j - i;  //@check
                                    }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestCut(string& s) {
                                int n = s.size(), best = n;  //@init
                                for (int i = 0; i <= n; i++)  //@blocks
                                    for (int j = i; j <= n; j++) {  //@blocks
                                        if (j - i >= best) continue;  //@check
                                        int m = n - (j - i), a = 0, b = m - 1;  //@check
                                        bool ok = true;  //@check
                                        while (a < b && ok) {  //@check
                                            char x = s[a < i ? a : a + j - i], y = s[b < i ? b : b + j - i];  //@check
                                            if (x != y) ok = false;  //@check
                                            a++; b--;  //@check
                                        }
                                        if (ok) best = j - i;  //@check
                                    }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int shortestCut(char* s) {
                            int n = strlen(s), best = n;  //@init
                            for (int i = 0; i <= n; i++)  //@blocks
                                for (int j = i; j <= n; j++) {  //@blocks
                                    if (j - i >= best) continue;  //@check
                                    int m = n - (j - i), a = 0, b = m - 1, ok = 1;  //@check
                                    while (a < b && ok) {  //@check
                                        char x = s[a < i ? a : a + j - i], y = s[b < i ? b : b + j - i];  //@check
                                        if (x != y) ok = 0;  //@check
                                        a++; b--;  //@check
                                    }
                                    if (ok) best = j - i;  //@check
                                }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Cutting everything always works (the empty text is a palindrome)."), ("blocks", "Every block `[i, j)` to cut."), ("check", "Only blocks shorter than the best matter. Position `a` of the kept text is `s[a]` before the cut and `s[a + (j − i)]` after it."), ("ret", "The shortest cut.")],
                complexity=["**Time O(n³)** in the worst case. **Space O(1)** (O(n) in Python for the copies)."],
                limits=["Billions of blocks for 10⁵ letters. Peeling the matching ends first shows the kept part of the middle is just a palindromic prefix or suffix, so only those need finding."],
                slow=True,
            ),
            approach(
                "Peel the ends, test prefixes and suffixes directly",
                "better",
                "O(n²)",
                "O(1)",
                idea=["Peel matching end pairs. In the middle, find the longest palindromic prefix by testing lengths from longest down, and the same for suffixes. Cut the rest of the middle."],
                walk=w2,
                build=["Peel matching ends.", "Longest palindromic prefix and suffix of the middle by direct checks.", "Middle length minus the larger."],
                code={
                    "python": """
                        class Solution:
                            def shortestCut(self, s: str) -> int:
                                n, l = len(s), 0  #@peel
                                while l < n - 1 - l and s[l] == s[n - 1 - l]:  #@peel
                                    l += 1  #@peel
                                mid = s[l:n - l]  #@peel
                                def pal(t):  #@longest
                                    return t == t[::-1]  #@longest
                                pre = next(k for k in range(len(mid), -1, -1) if pal(mid[:k]))  #@longest
                                suf = next(k for k in range(len(mid), -1, -1) if pal(mid[len(mid) - k:]))  #@longest
                                return len(mid) - max(pre, suf)  #@ret
                    """,
                    "java": """
                        class Solution {
                            private boolean pal(String s, int i, int j) {  //@longest
                                while (i < j) if (s.charAt(i++) != s.charAt(j--)) return false;  //@longest
                                return true;  //@longest
                            }  //@longest

                            public int shortestCut(String s) {
                                int n = s.length(), l = 0;  //@peel
                                while (l < n - 1 - l && s.charAt(l) == s.charAt(n - 1 - l)) l++;  //@peel
                                int lo = l, hi = n - 1 - l, m = hi - lo + 1;  //@peel
                                int pre = 0, suf = 0;  //@longest
                                for (int k = m; k > 0 && pre == 0; k--) if (pal(s, lo, lo + k - 1)) pre = k;  //@longest
                                for (int k = m; k > 0 && suf == 0; k--) if (pal(s, hi - k + 1, hi)) suf = k;  //@longest
                                return m - Math.max(pre, suf);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static bool pal(const string& s, int i, int j) {  //@longest
                                while (i < j) if (s[i++] != s[j--]) return false;  //@longest
                                return true;  //@longest
                            }  //@longest

                        public:
                            int shortestCut(string& s) {
                                int n = s.size(), l = 0;  //@peel
                                while (l < n - 1 - l && s[l] == s[n - 1 - l]) l++;  //@peel
                                int lo = l, hi = n - 1 - l, m = hi - lo + 1;  //@peel
                                int pre = 0, suf = 0;  //@longest
                                for (int k = m; k > 0 && pre == 0; k--) if (pal(s, lo, lo + k - 1)) pre = k;  //@longest
                                for (int k = m; k > 0 && suf == 0; k--) if (pal(s, hi - k + 1, hi)) suf = k;  //@longest
                                return m - max(pre, suf);  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int pal(const char* s, int i, int j) {  //@longest
                            while (i < j) if (s[i++] != s[j--]) return 0;  //@longest
                            return 1;  //@longest
                        }  //@longest

                        int shortestCut(char* s) {
                            int n = strlen(s), l = 0;  //@peel
                            while (l < n - 1 - l && s[l] == s[n - 1 - l]) l++;  //@peel
                            int lo = l, hi = n - 1 - l, m = hi - lo + 1;  //@peel
                            int pre = 0, suf = 0;  //@longest
                            for (int k = m; k > 0 && pre == 0; k--) if (pal(s, lo, lo + k - 1)) pre = k;  //@longest
                            for (int k = m; k > 0 && suf == 0; k--) if (pal(s, hi - k + 1, hi)) suf = k;  //@longest
                            return m - (pre > suf ? pre : suf);  //@ret
                        }
                    """,
                },
                lines=[("peel", "Matching outer pairs are always kept; the middle `s[lo..hi]` starts and ends with different letters (or is tiny)."), ("longest", "The longest palindromic prefix and suffix of the middle, by testing lengths from the longest down."), ("ret", "Keep the longer; cut the rest of the middle.")],
                complexity=["**Time O(n²)** in the worst case (many lengths, each tested in O(n)). **Space O(1).**"],
                limits=["Each length is tested from scratch. The KMP prefix function finds the longest palindromic prefix in one linear pass."],
                slow=True,
            ),
            approach(
                "Peel the ends, KMP for the palindromic prefix",
                "best",
                "O(n)",
                "O(n)",
                idea=["Peel matching ends to get the middle `t`. The longest palindromic prefix of `t` is the last value of the prefix function of `t + '#' + reverse(t)`; the longest palindromic suffix is the same for `reverse(t)`. Answer: `len(t) − max` of the two."],
                walk=w3,
                build=["Peel.", "Prefix function helper.", "Apply to `t` and its reverse."],
                code={
                    "python": """
                        class Solution:
                            def shortestCut(self, s: str) -> int:
                                n, l = len(s), 0  #@peel
                                while l < n - 1 - l and s[l] == s[n - 1 - l]:  #@peel
                                    l += 1  #@peel
                                mid = s[l:n - l]  #@peel
                                if len(mid) <= 1:  #@peel
                                    return 0  #@peel
                                def pal_prefix(t):  #@kmp
                                    u = t + "#" + t[::-1]  #@kmp
                                    pi = [0] * len(u)  #@kmp
                                    for i in range(1, len(u)):  #@kmp
                                        k = pi[i - 1]  #@kmp
                                        while k and u[i] != u[k]:  #@kmp
                                            k = pi[k - 1]  #@kmp
                                        if u[i] == u[k]:  #@kmp
                                            k += 1  #@kmp
                                        pi[i] = k  #@kmp
                                    return pi[-1]  #@kmp
                                return len(mid) - max(pal_prefix(mid), pal_prefix(mid[::-1]))  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int palPrefix(String t) {  //@kmp
                                String u = t + "#" + new StringBuilder(t).reverse();  //@kmp
                                int[] pi = new int[u.length()];  //@kmp
                                for (int i = 1; i < u.length(); i++) {  //@kmp
                                    int k = pi[i - 1];  //@kmp
                                    while (k > 0 && u.charAt(i) != u.charAt(k)) k = pi[k - 1];  //@kmp
                                    if (u.charAt(i) == u.charAt(k)) k++;  //@kmp
                                    pi[i] = k;  //@kmp
                                }
                                return pi[u.length() - 1];  //@kmp
                            }  //@kmp

                            public int shortestCut(String s) {
                                int n = s.length(), l = 0;  //@peel
                                while (l < n - 1 - l && s.charAt(l) == s.charAt(n - 1 - l)) l++;  //@peel
                                String mid = s.substring(l, n - l);  //@peel
                                if (mid.length() <= 1) return 0;  //@peel
                                return mid.length() - Math.max(palPrefix(mid), palPrefix(new StringBuilder(mid).reverse().toString()));  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static int palPrefix(const string& t) {  //@kmp
                                string u = t + "#" + string(t.rbegin(), t.rend());  //@kmp
                                vector<int> pi(u.size(), 0);  //@kmp
                                for (size_t i = 1; i < u.size(); i++) {  //@kmp
                                    int k = pi[i - 1];  //@kmp
                                    while (k > 0 && u[i] != u[k]) k = pi[k - 1];  //@kmp
                                    if (u[i] == u[k]) k++;  //@kmp
                                    pi[i] = k;  //@kmp
                                }
                                return pi.back();  //@kmp
                            }  //@kmp

                        public:
                            int shortestCut(string& s) {
                                int n = s.size(), l = 0;  //@peel
                                while (l < n - 1 - l && s[l] == s[n - 1 - l]) l++;  //@peel
                                string mid = s.substr(l, n - 2 * l);  //@peel
                                if (mid.size() <= 1) return 0;  //@peel
                                return mid.size() - max(palPrefix(mid), palPrefix(string(mid.rbegin(), mid.rend())));  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int pal_prefix(const char* t, int m, int reversed) {  //@kmp
                            int len = 2 * m + 1;  //@kmp
                            char* u = malloc(len);  //@kmp
                            for (int i = 0; i < m; i++) {  //@kmp
                                char c = reversed ? t[m - 1 - i] : t[i];  //@kmp
                                u[i] = c;  //@kmp
                                u[len - 1 - i] = c;  //@kmp
                            }
                            u[m] = '#';  //@kmp
                            int* pi = calloc(len, sizeof(int));  //@kmp
                            for (int i = 1; i < len; i++) {  //@kmp
                                int k = pi[i - 1];  //@kmp
                                while (k > 0 && u[i] != u[k]) k = pi[k - 1];  //@kmp
                                if (u[i] == u[k]) k++;  //@kmp
                                pi[i] = k;  //@kmp
                            }
                            int answer = pi[len - 1];  //@kmp
                            free(u); free(pi);  //@kmp
                            return answer;  //@kmp
                        }  //@kmp

                        int shortestCut(char* s) {
                            int n = strlen(s), l = 0;  //@peel
                            while (l < n - 1 - l && s[l] == s[n - 1 - l]) l++;  //@peel
                            int m = n - 2 * l;  //@peel
                            if (m <= 1) return 0;  //@peel
                            int a = pal_prefix(s + l, m, 0), b = pal_prefix(s + l, m, 1);  //@ret
                            return m - (a > b ? a : b);  //@ret
                        }
                    """,
                },
                lines=[
                    ("peel", "Keep matching outer pairs; a middle of length 0 or 1 is already a palindrome, so nothing needs cutting."),
                    ("kmp", "Prefix function of `t # reverse(t)`: its last value is the longest prefix of `t` that equals a suffix of `reverse(t)`, which is the longest palindromic prefix of `t`. The `#` stops the match from running past `t`.", {"c": "Build `t # reverse(t)` directly (or from `t` reversed, for the suffix case)."}),
                    ("ret", "Run it on the middle (palindromic prefix) and its reverse (palindromic suffix); keep the longer and cut the rest."),
                ],
                complexity=["**Time O(n).** **Space O(n)** for the glued string and the table."],
            ),
        ],
        takeaways=[
            """
            - **Longest palindromic prefix** = prefix function of `t + '#' + reverse(t)`, O(n).
            - Peel matching ends first: they can always stay, and what remains has mismatched ends.
            - Reducing a two-sided choice to "prefix or suffix" is the key insight.
            """
        ],
    )
