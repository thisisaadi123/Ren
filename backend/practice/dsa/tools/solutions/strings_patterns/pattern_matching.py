"""Strings: pattern matching with the prefix function (KMP)."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def prefix_function(t):
    pi = [0] * len(t)
    k = 0
    for i in range(1, len(t)):
        while k and t[i] != t[k]:
            k = pi[k - 1]
        if t[i] == t[k]:
            k += 1
        pi[i] = k
    return pi


def table_walk(w, t, label="pattern"):
    """Add steps that build the prefix function of t."""
    pi = prefix_function(t)
    for i in range(1, len(t)):
        w.step(f"Position {i} ('{t[i]}'): the longest proper prefix of '{t[:i + 1]}' that is also its suffix has length {pi[i]}.", Row(list(t), st={**{x: "found" for x in range(pi[i])}, **{x: "active" for x in range(i + 1 - pi[i], i + 1)}}, label=label), Row(pi[:i + 1] + ["·"] * (len(t) - i - 1), label="prefix fn"))
    return pi


@problem
def find_every_tag():
    text, tag = "abababcabab", "abab"
    m = len(tag)
    want = [i for i in range(len(text) - m + 1) if text[i:i + m] == tag]

    w1 = Steps("Line the tag up at every start and compare character by character.")
    for i in range(len(text) - m + 1):
        ok = text[i:i + m] == tag
        w1.step(f"Start {i}: '{text[i:i + m]}' {'matches' if ok else 'differs'}.", Row(list(text), st={x: ("found" if ok else "dim") for x in range(i, i + m)}))
    w1.step(f"Starts: {want}.", result=want)

    w2 = Steps("Build the prefix function of the tag, then stream the text keeping k = how much of the tag currently matches. On a mismatch (or a full match) fall back to the longest border instead of restarting.")
    pi = table_walk(w2, tag, "tag")
    k = 0
    for i, c in enumerate(text):
        while k and c != tag[k]:
            k = pi[k - 1]
        if c == tag[k]:
            k += 1
        hit = k == m
        w2.step(f"Text[{i}] = '{c}': matched length k = {k}." + (f" Full match at {i - m + 1}; fall back to k = {pi[k - 1]}." if hit else ""), Row(list(text), st={x: ("found" if hit else "active") for x in range(i - k + 1, i + 1)}), Vars(k=k))
        if hit:
            k = pi[k - 1]
    w2.step(f"Starts: {want}.", result=want)

    sol(
        "find-every-tag",
        summary="""
            Knuth–Morris–Pratt. The prefix function of the tag says, for each prefix, the longest proper prefix that is
            also a suffix (its border). Scan the text once, tracking how many tag characters currently match; on a
            mismatch, fall back to the border instead of restarting, and after a full match fall back the same way so
            overlapping copies are found. O(n + m).
        """,
        question=[
            """
            Return every start index where `tag` occurs in `text`, overlaps included, left to right.

            - **Both up to 10⁵ lowercase letters.**
            - Checking every start costs O(n · m) on inputs like `aaaa…a` / `aaa…ab`.
            """
        ],
        think=[
            f"""
            `text = "{text}"`, `tag = "{tag}"` → **{want}** (overlapping copies count).

            When a partial match `abab` breaks, the naive method slides by one and re-reads text it has already seen. But
            we already know those characters: they're the matched part of the tag. If the matched part `abab` ends with
            `ab`, which is also how the tag starts, then the next possible match already has 2 characters matched. The
            prefix function precomputes this "how much survives" for every prefix length, so the text pointer never moves
            back.
            """,
            fig(Row(list(text), label="text"), Row(list(tag), label="tag"), Row(prefix_function(tag), label="prefix fn")),
        ],
        approaches=[
            approach(
                "Check every start",
                "brute",
                "O(n · m)",
                "O(1)",
                idea=["For each `i` in `0..n−m`, compare `text[i..i+m)` with `tag`; record `i` on a full match."],
                walk=w1,
                build=["Loop over starts.", "Compare until a mismatch."],
                code={
                    "python": """
                        class Solution:
                            def findAll(self, text: str, tag: str) -> List[int]:
                                n, m = len(text), len(tag)  #@init
                                out = []  #@init
                                for i in range(n - m + 1):  #@starts
                                    j = 0  #@cmp
                                    while j < m and text[i + j] == tag[j]:  #@cmp
                                        j += 1  #@cmp
                                    if j == m:  #@hit
                                        out.append(i)  #@hit
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] findAll(String text, String tag) {
                                int n = text.length(), m = tag.length();  //@init
                                List<Integer> out = new ArrayList<>();  //@init
                                for (int i = 0; i + m <= n; i++) {  //@starts
                                    int j = 0;  //@cmp
                                    while (j < m && text.charAt(i + j) == tag.charAt(j)) j++;  //@cmp
                                    if (j == m) out.add(i);  //@hit
                                }
                                return out.stream().mapToInt(x -> x).toArray();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findAll(string& text, string& tag) {
                                int n = text.size(), m = tag.size();  //@init
                                vector<int> out;  //@init
                                for (int i = 0; i + m <= n; i++) {  //@starts
                                    int j = 0;  //@cmp
                                    while (j < m && text[i + j] == tag[j]) j++;  //@cmp
                                    if (j == m) out.push_back(i);  //@hit
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* findAll(char* text, char* tag, int* returnSize) {
                            int n = strlen(text), m = strlen(tag), count = 0;  //@init
                            int* out = malloc((n + 1) * sizeof(int));  //@init
                            for (int i = 0; i + m <= n; i++) {  //@starts
                                int j = 0;  //@cmp
                                while (j < m && text[i + j] == tag[j]) j++;  //@cmp
                                if (j == m) out[count++] = i;  //@hit
                            }
                            *returnSize = count;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "Lengths and the result list."), ("starts", "Every place the tag fits."), ("cmp", "Compare until a mismatch or the whole tag matched."), ("hit", "Full match."), ("ret", "Starts in increasing order.")],
                complexity=["**Time O(n · m)** in the worst case (`aaaa…` vs `aa…ab`): 10¹⁰ steps. **Space O(1)** besides the output."],
                limits=["After a partial match breaks, it re-reads text it has already matched. The prefix function tells exactly how much of the match survives."],
                slow=True,
            ),
            approach(
                "KMP: prefix function, then one pass",
                "best",
                "O(n + m)",
                "O(m)",
                idea=["`fail[i]` = length of the longest proper prefix of `tag[0..i]` that's also its suffix. Scan the text with `k` = matched length: on a mismatch set `k = fail[k−1]` until it fits or `k = 0`; on a full match record it and set `k = fail[m−1]`."],
                walk=w2,
                build=["Prefix function of the tag.", "Stream the text with fallbacks.", "Record matches and fall back for overlaps."],
                code={
                    "python": """
                        class Solution:
                            def findAll(self, text: str, tag: str) -> List[int]:
                                m = len(tag)  #@table
                                fail, k = [0] * m, 0  #@table
                                for i in range(1, m):  #@table
                                    while k and tag[i] != tag[k]:  #@table
                                        k = fail[k - 1]  #@table
                                    if tag[i] == tag[k]:  #@table
                                        k += 1  #@table
                                    fail[i] = k  #@table
                                out, k = [], 0  #@scan
                                for i, c in enumerate(text):  #@scan
                                    while k and c != tag[k]:  #@back
                                        k = fail[k - 1]  #@back
                                    if c == tag[k]:  #@scan
                                        k += 1  #@scan
                                    if k == m:  #@hit
                                        out.append(i - m + 1)  #@hit
                                        k = fail[k - 1]  #@hit
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] findAll(String text, String tag) {
                                int n = text.length(), m = tag.length(), k = 0;  //@table
                                int[] fail = new int[m];  //@table
                                for (int i = 1; i < m; i++) {  //@table
                                    while (k > 0 && tag.charAt(i) != tag.charAt(k)) k = fail[k - 1];  //@table
                                    if (tag.charAt(i) == tag.charAt(k)) k++;  //@table
                                    fail[i] = k;  //@table
                                }
                                List<Integer> out = new ArrayList<>();  //@scan
                                k = 0;  //@scan
                                for (int i = 0; i < n; i++) {  //@scan
                                    char c = text.charAt(i);  //@scan
                                    while (k > 0 && c != tag.charAt(k)) k = fail[k - 1];  //@back
                                    if (c == tag.charAt(k)) k++;  //@scan
                                    if (k == m) { out.add(i - m + 1); k = fail[k - 1]; }  //@hit
                                }
                                return out.stream().mapToInt(x -> x).toArray();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findAll(string& text, string& tag) {
                                int n = text.size(), m = tag.size(), k = 0;  //@table
                                vector<int> fail(m, 0);  //@table
                                for (int i = 1; i < m; i++) {  //@table
                                    while (k > 0 && tag[i] != tag[k]) k = fail[k - 1];  //@table
                                    if (tag[i] == tag[k]) k++;  //@table
                                    fail[i] = k;  //@table
                                }
                                vector<int> out;  //@scan
                                k = 0;  //@scan
                                for (int i = 0; i < n; i++) {  //@scan
                                    while (k > 0 && text[i] != tag[k]) k = fail[k - 1];  //@back
                                    if (text[i] == tag[k]) k++;  //@scan
                                    if (k == m) { out.push_back(i - m + 1); k = fail[k - 1]; }  //@hit
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* findAll(char* text, char* tag, int* returnSize) {
                            int n = strlen(text), m = strlen(tag), k = 0, count = 0;  //@table
                            int* fail = calloc(m, sizeof(int));  //@table
                            for (int i = 1; i < m; i++) {  //@table
                                while (k > 0 && tag[i] != tag[k]) k = fail[k - 1];  //@table
                                if (tag[i] == tag[k]) k++;  //@table
                                fail[i] = k;  //@table
                            }
                            int* out = malloc((n + 1) * sizeof(int));  //@scan
                            k = 0;  //@scan
                            for (int i = 0; i < n; i++) {  //@scan
                                while (k > 0 && text[i] != tag[k]) k = fail[k - 1];  //@back
                                if (text[i] == tag[k]) k++;  //@scan
                                if (k == m) { out[count++] = i - m + 1; k = fail[k - 1]; }  //@hit
                            }
                            free(fail);  //@ret
                            *returnSize = count;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("table", "The prefix function of the tag: the same matching process, run on the tag against itself."),
                    ("scan", "`k` is how many tag characters end at the current text position; it grows by at most 1 per character."),
                    ("back", "Mismatch: the longest border of the matched part is the most that can still be extended. Each fallback shrinks `k`, so the total work is O(n)."),
                    ("hit", "A full match starts at `i − m + 1`. Falling back to `fail[m−1]` (not 0) keeps the overlap, so the next copy can share characters."),
                    ("ret", "All starts, left to right."),
                ],
                complexity=["**Time O(n + m):** `k` rises at most once per character, so it can't fall more often than that. **Space O(m)** for the table."],
            ),
        ],
        takeaways=[
            """
            - **KMP = prefix function + a scan that never moves backwards** in the text.
            - The prefix function (longest border of every prefix) is the reusable tool.
            - After a full match, fall back to the border to catch overlaps.
            """
        ],
    )


@problem
def front_padding():
    s = "aacecaaab"
    rev = s[::-1]
    keep = max(k for k in range(len(s) + 1) if s[:k] == s[:k][::-1])
    want = s[keep:][::-1] + s

    w1 = Steps("Find the longest prefix of s that is a palindrome, testing from the full length down.")
    for k in range(len(s), keep - 1, -1):
        ok = s[:k] == s[:k][::-1]
        w1.step(f"Prefix '{s[:k]}' is {'a palindrome' if ok else 'not a palindrome'}.", Row(list(s), st={x: ("found" if ok else "dim") for x in range(k)}))
    w1.step(f"Mirror the rest '{s[keep:]}' onto the front: {want}.", result=want)

    t = s + "#" + rev
    pi = prefix_function(t)
    w2 = Steps("In s + '#' + reverse(s), the prefix function's last value is the length of the longest prefix of s that equals a suffix of reverse(s), i.e. the longest palindromic prefix.")
    w2.step(f"Glued: {t}.", Row(list(t)))
    w2.step(f"Prefix function's last value: {pi[-1]}. So '{s[:pi[-1]]}' is the longest palindromic prefix.", Row(list(t), st={**{x: "found" for x in range(pi[-1])}, **{x: "found" for x in range(len(t) - pi[-1], len(t))}}), Row(pi, label="prefix fn"))
    w2.step(f"Prepend reverse('{s[keep:]}') = '{s[keep:][::-1]}': {want}.", result=want)

    sol(
        "front-padding",
        summary="""
            Letters added to the front mirror the end of `s`, so keep the longest palindromic prefix of `s` as the centre
            and prepend the reverse of what follows it. The longest palindromic prefix is the last value of the prefix
            function of `s + '#' + reverse(s)`. O(n).
        """,
        question=[
            """
            Add letters only to the front of `s` to make the shortest possible palindrome. Return it.

            - **Up to 10⁵ letters**, possibly empty.
            """
        ],
        think=[
            f"""
            `"{s}"` → **`{want}`**.

            In the result, the original `s` sits at the end, so the palindrome's mirror image of the front is `s`'s tail.
            Whatever prefix of `s` is already a palindrome can serve as the middle; everything after it must be mirrored
            onto the front. Fewer added letters means a longer palindromic prefix, so we need the **longest** one.

            A palindromic prefix of `s` equals its own reverse, which is a suffix of `reverse(s)`. In `s # reverse(s)`, the
            longest prefix that's also a suffix is exactly that (the `#` stops it from spilling across).
            """,
            fig(Row(list(s), label="s"), Row(list(rev), label="reverse")),
        ],
        approaches=[
            approach(
                "Test prefixes from longest to shortest",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For `k = n, n−1, …`, check whether `s[0..k)` is a palindrome with two pointers. The first hit is the longest; prepend `reverse(s[k:])`."],
                walk=w1,
                build=["Lengths from long to short.", "Two-pointer palindrome test.", "Prepend the reversed tail."],
                code={
                    "python": """
                        class Solution:
                            def padToPalindrome(self, s: str) -> str:
                                k = len(s)  #@search
                                while k > 0:  #@search
                                    i, j = 0, k - 1  #@test
                                    while i < j and s[i] == s[j]:  #@test
                                        i, j = i + 1, j - 1  #@test
                                    if i >= j:  #@test
                                        break  #@test
                                    k -= 1  #@search
                                return s[k:][::-1] + s  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String padToPalindrome(String s) {
                                int k = s.length();  //@search
                                for (; k > 0; k--) {  //@search
                                    int i = 0, j = k - 1;  //@test
                                    while (i < j && s.charAt(i) == s.charAt(j)) { i++; j--; }  //@test
                                    if (i >= j) break;  //@test
                                }
                                return new StringBuilder(s.substring(k)).reverse() + s;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string padToPalindrome(string& s) {
                                int k = s.size();  //@search
                                for (; k > 0; k--) {  //@search
                                    int i = 0, j = k - 1;  //@test
                                    while (i < j && s[i] == s[j]) { i++; j--; }  //@test
                                    if (i >= j) break;  //@test
                                }
                                return string(s.rbegin(), s.rend() - k) + s;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* padToPalindrome(char* s) {
                            int n = strlen(s), k = n;  //@search
                            for (; k > 0; k--) {  //@search
                                int i = 0, j = k - 1;  //@test
                                while (i < j && s[i] == s[j]) { i++; j--; }  //@test
                                if (i >= j) break;  //@test
                            }
                            int add = n - k, pos = 0;  //@ret
                            char* out = malloc(add + n + 1);  //@ret
                            for (int i = n - 1; i >= k; i--) out[pos++] = s[i];  //@ret
                            memcpy(out + pos, s, n + 1);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("search", "Longest candidate first; `k = 0` (empty prefix) always works."), ("test", "Two pointers on `s[0..k)`."), ("ret", "Mirror the tail `s[k:]` onto the front.")],
                complexity=["**Time O(n²)** in the worst case (e.g. `aaa…ab`). **Space O(1)** besides the output."],
                limits=["Each length is tested from scratch. The prefix function finds the longest palindromic prefix in one pass."],
                slow=True,
            ),
            approach(
                "Prefix function of s # reverse(s)",
                "best",
                "O(n)",
                "O(n)",
                idea=["`t = s + '#' + reverse(s)`. The last prefix-function value of `t` is the longest palindromic prefix length `p`. Return `reverse(s[p:]) + s`."],
                walk=w2,
                build=["Glue with a separator.", "Prefix function.", "Prepend the reversed tail."],
                code={
                    "python": """
                        class Solution:
                            def padToPalindrome(self, s: str) -> str:
                                t = s + "#" + s[::-1]  #@glue
                                fail, k = [0] * len(t), 0  #@table
                                for i in range(1, len(t)):  #@table
                                    while k and t[i] != t[k]:  #@table
                                        k = fail[k - 1]  #@table
                                    if t[i] == t[k]:  #@table
                                        k += 1  #@table
                                    fail[i] = k  #@table
                                keep = fail[-1]  #@ret
                                return s[keep:][::-1] + s  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String padToPalindrome(String s) {
                                String rev = new StringBuilder(s).reverse().toString();  //@glue
                                String t = s + "#" + rev;  //@glue
                                int[] fail = new int[t.length()];  //@table
                                for (int i = 1, k = 0; i < t.length(); i++) {  //@table
                                    while (k > 0 && t.charAt(i) != t.charAt(k)) k = fail[k - 1];  //@table
                                    if (t.charAt(i) == t.charAt(k)) k++;  //@table
                                    fail[i] = k;  //@table
                                }
                                int keep = fail[t.length() - 1];  //@ret
                                return rev.substring(0, s.length() - keep) + s;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string padToPalindrome(string& s) {
                                string rev(s.rbegin(), s.rend());  //@glue
                                string t = s + "#" + rev;  //@glue
                                vector<int> fail(t.size(), 0);  //@table
                                for (int i = 1, k = 0; i < (int) t.size(); i++) {  //@table
                                    while (k > 0 && t[i] != t[k]) k = fail[k - 1];  //@table
                                    if (t[i] == t[k]) k++;  //@table
                                    fail[i] = k;  //@table
                                }
                                int keep = fail.back();  //@ret
                                return rev.substr(0, s.size() - keep) + s;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* padToPalindrome(char* s) {
                            int n = strlen(s), len = 2 * n + 1;  //@glue
                            char* t = malloc(len);  //@glue
                            for (int i = 0; i < n; i++) { t[i] = s[i]; t[len - 1 - i] = s[i]; }  //@glue
                            t[n] = '#';  //@glue
                            int* fail = calloc(len, sizeof(int));  //@table
                            for (int i = 1, k = 0; i < len; i++) {  //@table
                                while (k > 0 && t[i] != t[k]) k = fail[k - 1];  //@table
                                if (t[i] == t[k]) k++;  //@table
                                fail[i] = k;  //@table
                            }
                            int keep = fail[len - 1], add = n - keep;  //@ret
                            char* out = malloc(add + n + 1);  //@ret
                            memcpy(out, t + n + 1, add);  //@ret
                            memcpy(out + add, s, n + 1);  //@ret
                            free(t); free(fail);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("glue", "`s`, a separator that never matches a letter, then `reverse(s)`.", {"c": "Write `s` and its reverse into one buffer."}),
                    ("table", "Standard prefix function."),
                    ("ret", "`keep` = longest palindromic prefix. The letters to add are `reverse(s[keep:])`, which is the first `n − keep` letters of `reverse(s)`."),
                ],
                complexity=["**Time O(n).** **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - **Shortest palindrome by prepending** = keep the longest palindromic prefix, mirror the rest.
            - **`s # reverse(s)` + prefix function** finds palindromic prefixes in O(n).
            - The separator prevents a border from spanning both halves.
            """
        ],
    )


@problem
def repeating_unit():
    s = "abcabcabcabc"
    n = len(s)
    pi = prefix_function(s)
    p = n - pi[-1]
    want = p if n % p == 0 else n

    w1 = Steps("Try each divisor p of n as the block length: the string is p-periodic when every character equals the one p positions earlier.")
    for q in range(1, n + 1):
        if n % q:
            continue
        ok = s[q:] == s[:n - q]
        bad = next((i for i in range(q, n) if s[i] != s[i - q]), None)
        w1.step(f"p = {q}: " + ("every s[i] equals s[i − p]. Found it." if ok else f"s[{bad}] = '{s[bad]}' but s[{bad - q}] = '{s[bad - q]}'."), Row(list(s), st=({x: "found" for x in range(q)} if ok else {bad: "mark", bad - q: "mark"})))
        if ok:
            break
    w1.step(f"Shortest block: {want}.", result=want)

    w2 = Steps("The longest border b of s (proper prefix = suffix) means s has period n − b. If that period divides n, it's the shortest block; otherwise no shorter block tiles s.")
    table_walk(w2, s, "s")
    w2.step(f"Longest border b = {pi[-1]}, so the period is {n} − {pi[-1]} = {p}. {n} % {p} = {n % p}, so the answer is {want}.", result=want)

    sol(
        "repeating-unit",
        summary="""
            If `s` has a border (a proper prefix that's also a suffix) of length `b`, then `s` repeats with period `n − b`;
            the longest border gives the smallest period. The prefix function's last value is that border. If the period
            divides `n`, it's the block length; otherwise no shorter block tiles `s` exactly, and the answer is `n`. O(n).
        """,
        question=[
            """
            Return the length of the shortest block `u` such that `s` is `u` repeated a whole number of times (`s.length`
            if nothing shorter works).

            - **Up to 10⁵ letters.**
            """
        ],
        think=[
            f"""
            `"{s}"` is `abc` four times: **{want}**. `"abcab"` has period 3, but 3 doesn't divide 5, so it's **5**.

            A block length must divide `n`, and `s` repeats with block `p` exactly when `s[i] == s[i − p]` for all `i ≥ p`,
            which is the same as saying `s` without its first `p` letters equals `s` without its last `p` letters. That is a
            border of length `n − p`. So the smallest period comes from the longest border.
            """,
            fig(Row(list(s), label="s"), Row(pi, label="prefix fn")),
        ],
        approaches=[
            approach(
                "Try the divisors of n",
                "better",
                "O(n · d(n))",
                "O(1)",
                idea=["For each divisor `p` of `n` in increasing order, check `s[i] == s[i − p]` for all `i ≥ p`. The first that passes is the answer."],
                walk=w1,
                build=["Loop over lengths that divide `n`.", "Periodicity check."],
                code={
                    "python": """
                        class Solution:
                            def shortestUnit(self, s: str) -> int:
                                n = len(s)  #@loop
                                for p in range(1, n + 1):  #@loop
                                    if n % p == 0 and s[p:] == s[:n - p]:  #@check
                                        return p  #@check
                                return n  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestUnit(String s) {
                                int n = s.length();  //@loop
                                for (int p = 1; p < n; p++) {  //@loop
                                    if (n % p != 0) continue;  //@loop
                                    int i = p;  //@check
                                    while (i < n && s.charAt(i) == s.charAt(i - p)) i++;  //@check
                                    if (i == n) return p;  //@check
                                }
                                return n;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestUnit(string& s) {
                                int n = s.size();  //@loop
                                for (int p = 1; p < n; p++) {  //@loop
                                    if (n % p != 0) continue;  //@loop
                                    int i = p;  //@check
                                    while (i < n && s[i] == s[i - p]) i++;  //@check
                                    if (i == n) return p;  //@check
                                }
                                return n;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int shortestUnit(char* s) {
                            int n = strlen(s);  //@loop
                            for (int p = 1; p < n; p++) {  //@loop
                                if (n % p != 0) continue;  //@loop
                                int i = p;  //@check
                                while (i < n && s[i] == s[i - p]) i++;  //@check
                                if (i == n) return p;  //@check
                            }
                            return n;  //@ret
                        }
                    """,
                },
                lines=[
                    ("loop", "Only divisors of `n` can tile it exactly; smallest first."),
                    ("check", "Every character equals the one a block earlier.", {"python": "Comparing `s[p:]` with `s[:n−p]` is the same check, done by fast slice comparison."}),
                    ("ret", "Nothing shorter works: the whole string is the block."),
                ],
                complexity=["**Time O(n · d(n)):** `d(n)`, the number of divisors, is at most 128 for n ≤ 10⁵. **Space O(1).**"],
                limits=["Each divisor is checked from scratch. The prefix function produces the smallest period directly."],
            ),
            approach(
                "Smallest period from the prefix function",
                "best",
                "O(n)",
                "O(n)",
                idea=["Compute the prefix function; `b = fail[n−1]`, `p = n − b`. Return `p` if `n % p == 0`, else `n`."],
                walk=w2,
                build=["Prefix function.", "Period from the longest border.", "Divisibility check."],
                code={
                    "python": """
                        class Solution:
                            def shortestUnit(self, s: str) -> int:
                                n = len(s)  #@table
                                fail, k = [0] * n, 0  #@table
                                for i in range(1, n):  #@table
                                    while k and s[i] != s[k]:  #@table
                                        k = fail[k - 1]  #@table
                                    if s[i] == s[k]:  #@table
                                        k += 1  #@table
                                    fail[i] = k  #@table
                                p = n - fail[-1]  #@period
                                return p if n % p == 0 else n  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestUnit(String s) {
                                int n = s.length();  //@table
                                int[] fail = new int[n];  //@table
                                for (int i = 1, k = 0; i < n; i++) {  //@table
                                    while (k > 0 && s.charAt(i) != s.charAt(k)) k = fail[k - 1];  //@table
                                    if (s.charAt(i) == s.charAt(k)) k++;  //@table
                                    fail[i] = k;  //@table
                                }
                                int p = n - fail[n - 1];  //@period
                                return n % p == 0 ? p : n;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestUnit(string& s) {
                                int n = s.size();  //@table
                                vector<int> fail(n, 0);  //@table
                                for (int i = 1, k = 0; i < n; i++) {  //@table
                                    while (k > 0 && s[i] != s[k]) k = fail[k - 1];  //@table
                                    if (s[i] == s[k]) k++;  //@table
                                    fail[i] = k;  //@table
                                }
                                int p = n - fail[n - 1];  //@period
                                return n % p == 0 ? p : n;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int shortestUnit(char* s) {
                            int n = strlen(s);  //@table
                            int* fail = calloc(n, sizeof(int));  //@table
                            for (int i = 1, k = 0; i < n; i++) {  //@table
                                while (k > 0 && s[i] != s[k]) k = fail[k - 1];  //@table
                                if (s[i] == s[k]) k++;  //@table
                                fail[i] = k;  //@table
                            }
                            int p = n - fail[n - 1];  //@period
                            free(fail);  //@period
                            return n % p == 0 ? p : n;  //@ret
                        }
                    """,
                },
                lines=[
                    ("table", "Prefix function of `s`."),
                    ("period", "The longest border `b` gives the smallest period `n − b`: shifting `s` by `p` lines the border up with itself."),
                    ("ret", "A period that divides `n` tiles `s` exactly. If the smallest period doesn't divide `n`, no larger period below `n` does either (any such period would combine with it into a smaller one that divides `n`), so the answer is `n`."),
                ],
                complexity=["**Time O(n).** **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - **Border ↔ period:** a border of length `b` means period `n − b`.
            - Smallest period = `n − prefix_function[n−1]`; it tiles `s` only if it divides `n`.
            - The same fact answers "is s a repetition of a smaller string?".
            """
        ],
    )
