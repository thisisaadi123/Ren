"""Strings: comparing strings by a signature (letter counts and friends)."""
from collections import Counter

from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def scrambled_name_tag():
    a, b = "Dormitory", "dirty room"
    norm = lambda s: sorted(c.lower() for c in s if c != " ")  # noqa: E731
    want = norm(a) == norm(b)

    w1 = Steps("Normalise both phrases (drop spaces, lowercase), sort the letters, and compare.")
    w1.step(f"'{a}' → {''.join(norm(a))}.", Row(norm(a), label="a sorted"))
    w1.step(f"'{b}' → {''.join(norm(b))}.", Row(norm(a), label="a sorted"), Row(norm(b), label="b sorted"))
    w1.step(f"Identical: {str(want).lower()}.", result=str(want).lower())

    w2 = Steps("26 counters: add 1 for every letter of a, subtract 1 for every letter of b. Scrambles leave every counter at zero.")
    cnt = Counter(c.lower() for c in a if c != " ")
    w2.step("After a.", Row([f"{k}{v}" for k, v in sorted(cnt.items())], label="counts"))
    cnt.subtract(Counter(c.lower() for c in b if c != " "))
    w2.step("After subtracting b: all zero.", Row([f"{k}{v}" for k, v in sorted(cnt.items())], label="counts"), result=str(want).lower())

    sol(
        "scrambled-name-tag",
        summary="""
            Two phrases are scrambles exactly when they have the same letter counts, after dropping spaces and ignoring
            case. Count with 26 counters: +1 for each letter of `a`, −1 for each letter of `b`; every counter must end at 0.
            O(n + m).
        """,
        question=[
            """
            Ignoring spaces and case, does `b` use exactly the same letters as `a`, the same number of times?

            - **Spaces don't count**, and lengths with spaces may differ.
            - **Up to 10⁵ characters each.**
            """
        ],
        think=[
            f"""
            `"{a}"` and `"{b}"` both reduce to the letters d, i, m, o, o, r, r, t, y: **{str(want).lower()}**.

            Order doesn't matter, only how many of each letter. That's a signature: sorted letters, or 26 counts. Counts
            are cheaper.
            """,
            fig(Row(list(a), label="a"), Row(list(b), label="b")),
        ],
        approaches=[
            approach(
                "Normalise and sort",
                "better",
                "O(n log n)",
                "O(n)",
                idea=["Lowercase, drop spaces, sort both, compare."],
                walk=w1,
                build=["Normalise each phrase.", "Sort.", "Compare."],
                code={
                    "python": """
                        class Solution:
                            def isScramble(self, a: str, b: str) -> bool:
                                norm = lambda s: sorted(c.lower() for c in s if c != " ")  #@norm
                                return norm(a) == norm(b)  #@cmp
                    """,
                    "java": """
                        class Solution {
                            private char[] norm(String s) {  //@norm
                                char[] c = s.replace(" ", "").toLowerCase().toCharArray();  //@norm
                                Arrays.sort(c);  //@norm
                                return c;  //@norm
                            }  //@norm

                            public boolean isScramble(String a, String b) {
                                return Arrays.equals(norm(a), norm(b));  //@cmp
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static string norm(const string& s) {  //@norm
                                string out;  //@norm
                                for (char c : s) if (c != ' ') out += tolower((unsigned char) c);  //@norm
                                sort(out.begin(), out.end());  //@norm
                                return out;  //@norm
                            }  //@norm

                        public:
                            bool isScramble(string& a, string& b) {
                                return norm(a) == norm(b);  //@cmp
                            }
                        };
                    """,
                    "c": """
                        #include <ctype.h>

                        static int cmp_char(const void* x, const void* y) { return *(const char*) x - *(const char*) y; }  //@norm

                        static char* norm(const char* s) {  //@norm
                            char* out = malloc(strlen(s) + 1);  //@norm
                            int w = 0;  //@norm
                            for (; *s; s++) if (*s != ' ') out[w++] = tolower((unsigned char) *s);  //@norm
                            out[w] = '\\0';  //@norm
                            qsort(out, w, 1, cmp_char);  //@norm
                            return out;  //@norm
                        }  //@norm

                        bool isScramble(char* a, char* b) {
                            char *x = norm(a), *y = norm(b);  //@cmp
                            bool same = strcmp(x, y) == 0;  //@cmp
                            free(x); free(y);  //@cmp
                            return same;  //@cmp
                        }
                    """,
                },
                lines=[("norm", "Lowercase letters without spaces, sorted: a canonical form."), ("cmp", "Scrambles have the same canonical form.")],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Sorting does more than needed. Only the letter counts matter, and 26 counters give them in linear time."],
            ),
            approach(
                "26 counters",
                "best",
                "O(n + m)",
                "O(1)",
                idea=["`cnt[letter] += 1` over `a`, `−= 1` over `b` (skipping spaces, folding case). True if all counts are 0."],
                walk=w2,
                build=["Count up over a.", "Count down over b.", "Check all zero."],
                code={
                    "python": """
                        class Solution:
                            def isScramble(self, a: str, b: str) -> bool:
                                cnt = [0] * 26  #@count
                                for c in a:  #@count
                                    if c != " ":  #@count
                                        cnt[ord(c.lower()) - 97] += 1  #@count
                                for c in b:  #@count
                                    if c != " ":  #@count
                                        cnt[ord(c.lower()) - 97] -= 1  #@count
                                return not any(cnt)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean isScramble(String a, String b) {
                                int[] cnt = new int[26];  //@count
                                for (char c : a.toCharArray()) if (c != ' ') cnt[Character.toLowerCase(c) - 'a']++;  //@count
                                for (char c : b.toCharArray()) if (c != ' ') cnt[Character.toLowerCase(c) - 'a']--;  //@count
                                for (int x : cnt) if (x != 0) return false;  //@ret
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool isScramble(string& a, string& b) {
                                int cnt[26] = {};  //@count
                                for (char c : a) if (c != ' ') cnt[tolower((unsigned char) c) - 'a']++;  //@count
                                for (char c : b) if (c != ' ') cnt[tolower((unsigned char) c) - 'a']--;  //@count
                                for (int x : cnt) if (x != 0) return false;  //@ret
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        #include <ctype.h>

                        bool isScramble(char* a, char* b) {
                            int cnt[26] = {0};  //@count
                            for (; *a; a++) if (*a != ' ') cnt[tolower((unsigned char) *a) - 'a']++;  //@count
                            for (; *b; b++) if (*b != ' ') cnt[tolower((unsigned char) *b) - 'a']--;  //@count
                            for (int x = 0; x < 26; x++) if (cnt[x]) return false;  //@ret
                            return true;  //@ret
                        }
                    """,
                },
                lines=[("count", "Letters of `a` add, letters of `b` subtract; spaces skipped, case folded."), ("ret", "Every letter balanced: same multiset.")],
                complexity=["**Time O(n + m).** **Space O(1):** 26 counters."],
            ),
        ],
        takeaways=[
            """
            - **Anagram test = equal letter counts.** One counter array: add for one string, subtract for the other.
            - Normalise first (case, spaces) so the signature captures exactly what "same" means.
            - Sorting works too, at O(n log n).
            """
        ],
    )


@problem
def swap_and_relabel():
    a, b = "aabcc", "ccaba"
    ca, cb = Counter(a), Counter(b)
    want = len(a) == len(b) and set(a) == set(b) and sorted(ca.values()) == sorted(cb.values())

    w = Steps("Swaps let letters move anywhere, so only counts matter. Relabels exchange the counts of two letters that both exist. So: same letters used, and the same collection of counts.")
    w.step(f"Counts in a: {dict(sorted(ca.items()))}; in b: {dict(sorted(cb.items()))}.", Row(list(a), label="a"), Row(list(b), label="b"))
    w.step(f"Same letters ({''.join(sorted(set(a)))}) on both sides: {str(set(a) == set(b)).lower()}.", Vars(letters_a="".join(sorted(set(a))), letters_b="".join(sorted(set(b)))))
    w.step(f"Sorted counts: {sorted(ca.values())} vs {sorted(cb.values())}.", Vars(a=str(sorted(ca.values())), b=str(sorted(cb.values()))))
    w.step(f"Reachable: {str(want).lower()}.", result=str(want).lower())

    sol(
        "swap-and-relabel",
        summary="""
            Swaps make positions irrelevant, so only letter counts matter. A relabel exchanges the counts of two letters that
            both appear, so the set of letters never changes and the counts can be permuted freely among them. Hence `a`
            can become `b` exactly when they have the same length, the same set of letters, and the same multiset of counts.
            O(n).
        """,
        question=[
            """
            Moves: swap any two positions; or relabel, exchanging two letters that **both** appear. Can `a` become `b`?

            - **Relabels can't introduce a new letter** (both letters must already appear).
            - **Up to 10⁵ letters.**
            """
        ],
        think=[
            f"""
            `a = "{a}"` (counts {dict(sorted(ca.items()))}), `b = "{b}"` (counts {dict(sorted(cb.items()))}): **{str(want).lower()}**.

            What can't change? With swaps, the arrangement is free, so think of a word as its letter counts. A relabel of x
            and y exchanges their counts and keeps both letters present. So the set of letters is fixed, and the counts can
            be moved between those letters in any arrangement (any permutation is a sequence of exchanges). That gives two
            invariants, and when both match, the moves can reach `b`.
            """,
            fig(Row(list(a), label="a"), Row(list(b), label="b")),
        ],
        approaches=[
            approach(
                "Compare letter sets and sorted counts",
                "best",
                "O(n)",
                "O(1)",
                idea=["Lengths equal; for every letter, present in `a` iff present in `b`; and the sorted 26-count lists are equal."],
                walk=w,
                build=["Count both words.", "Same letters present.", "Same sorted counts."],
                code={
                    "python": """
                        class Solution:
                            def canReshape(self, a: str, b: str) -> bool:
                                if len(a) != len(b):  #@len
                                    return False  #@len
                                ca, cb = [0] * 26, [0] * 26  #@count
                                for c in a:  #@count
                                    ca[ord(c) - 97] += 1  #@count
                                for c in b:  #@count
                                    cb[ord(c) - 97] += 1  #@count
                                for x, y in zip(ca, cb):  #@set
                                    if (x > 0) != (y > 0):  #@set
                                        return False  #@set
                                return sorted(ca) == sorted(cb)  #@counts
                    """,
                    "java": """
                        class Solution {
                            public boolean canReshape(String a, String b) {
                                if (a.length() != b.length()) return false;  //@len
                                int[] ca = new int[26], cb = new int[26];  //@count
                                for (char c : a.toCharArray()) ca[c - 'a']++;  //@count
                                for (char c : b.toCharArray()) cb[c - 'a']++;  //@count
                                for (int x = 0; x < 26; x++) if ((ca[x] > 0) != (cb[x] > 0)) return false;  //@set
                                Arrays.sort(ca);  //@counts
                                Arrays.sort(cb);  //@counts
                                return Arrays.equals(ca, cb);  //@counts
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool canReshape(string& a, string& b) {
                                if (a.size() != b.size()) return false;  //@len
                                vector<int> ca(26, 0), cb(26, 0);  //@count
                                for (char c : a) ca[c - 'a']++;  //@count
                                for (char c : b) cb[c - 'a']++;  //@count
                                for (int x = 0; x < 26; x++) if ((ca[x] > 0) != (cb[x] > 0)) return false;  //@set
                                sort(ca.begin(), ca.end());  //@counts
                                sort(cb.begin(), cb.end());  //@counts
                                return ca == cb;  //@counts
                            }
                        };
                    """,
                    "c": """
                        static int cmp_int(const void* x, const void* y) {  //@counts
                            int a = *(const int*) x, b = *(const int*) y;  //@counts
                            return (a > b) - (a < b);  //@counts
                        }  //@counts

                        bool canReshape(char* a, char* b) {
                            if (strlen(a) != strlen(b)) return false;  //@len
                            int ca[26] = {0}, cb[26] = {0};  //@count
                            for (; *a; a++) ca[*a - 'a']++;  //@count
                            for (; *b; b++) cb[*b - 'a']++;  //@count
                            for (int x = 0; x < 26; x++) if ((ca[x] > 0) != (cb[x] > 0)) return false;  //@set
                            qsort(ca, 26, sizeof(int), cmp_int);  //@counts
                            qsort(cb, 26, sizeof(int), cmp_int);  //@counts
                            return memcmp(ca, cb, sizeof ca) == 0;  //@counts
                        }
                    """,
                },
                lines=[("len", "Neither move changes the length."), ("count", "Letter counts of each word."), ("set", "Relabels never add or remove a letter: the same letters must appear in both."), ("counts", "Relabels permute counts among those letters: the same counts must appear, in any order.")],
                complexity=["**Time O(n).** **Space O(1):** 26-entry arrays (sorting them is constant work)."],
            ),
        ],
        takeaways=[
            """
            - Find the **invariants** of the allowed moves; if they match and the moves are flexible enough, that's the
              answer.
            - Free swaps reduce a string to its letter counts.
            - Label exchanges keep the set of labels and permute the counts.
            """
        ],
    )


@problem
def anagram_twins_in_a_word():
    s = "abba"
    n = len(s)
    total, per = 0, []
    for L in range(1, n):
        seen = Counter("".join(sorted(s[i:i + L])) for i in range(n - L + 1))
        c = sum(v * (v - 1) // 2 for v in seen.values())
        per.append((L, c, dict(seen)))
        total += c
    want = total

    w1 = Steps("Every length, every pair of windows of that length: compare their sorted letters.")
    for L, c, seen in per:
        w1.step(f"Length {L}: signatures {seen}; {c} twin pair(s).", Row(list(s)), Vars(length=L, pairs=c))
    w1.step(f"Total: {want}.", result=want)

    w2 = Steps("For each length, slide a window keeping 26 letter counts; group windows by their counts and add k(k−1)/2 per group.")
    acc = 0
    for L, c, seen in per:
        acc += c
        w2.step(f"Length {L}: slide the window, update two counters per step. Groups by signature: {seen} → +{c}.", Row(list(s), st={i: "active" for i in range(L)}), Vars(total=acc))
    w2.step(f"Total: {acc}.", result=acc)

    sol(
        "anagram-twins-in-a-word",
        summary="""
            Twins have the same length and the same letter counts. For each length L, slide a window across `s`, updating
            its 26 counts in O(1) per step, and count how many windows share each count vector; a group of k windows gives
            k(k − 1)/2 pairs. O(n² · 26) for n ≤ 500.
        """,
        question=[
            """
            Count unordered pairs of equal-length substrings, at different start positions, that are anagrams of each other.

            - **Equal substrings** at different positions count as twins too.
            - **n ≤ 500**: about 125,000 substrings; comparing all pairs directly would be far too slow.
            """
        ],
        think=[
            f"""
            `"{s}"`: length 1 has the pairs (a, a) and (b, b); length 2 has `ab` and `ba`; length 3 has `abb` and `bba`.
            Total **{want}**.

            Anagram pairs = equal signatures. For a fixed length, sliding the window changes just two counters, so every
            window's signature costs O(1) to update (plus 26 to record). Then count equal signatures with a hash map.
            """,
            table(["length", "twin pairs"], *[(L, c) for L, c, _ in per]),
        ],
        approaches=[
            approach(
                "Compare every pair of windows",
                "brute",
                "O(n³ · L log L)",
                "O(n)",
                idea=["For each length, compare every pair of windows by their sorted letters."],
                walk=w1,
                build=["For each length L, list the windows' sorted forms.", "Count equal pairs directly."],
                code={
                    "python": """
                        class Solution:
                            def anagramTwins(self, s: str) -> int:
                                n, total = len(s), 0  #@init
                                for L in range(1, n):  #@len
                                    sigs = ["".join(sorted(s[i:i + L])) for i in range(n - L + 1)]  #@sigs
                                    for i in range(len(sigs)):  #@pairs
                                        for j in range(i + 1, len(sigs)):  #@pairs
                                            if sigs[i] == sigs[j]:  #@pairs
                                                total += 1  #@pairs
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int anagramTwins(String s) {
                                int n = s.length(), total = 0;  //@init
                                for (int L = 1; L < n; L++) {  //@len
                                    String[] sigs = new String[n - L + 1];  //@sigs
                                    for (int i = 0; i + L <= n; i++) {  //@sigs
                                        char[] c = s.substring(i, i + L).toCharArray();  //@sigs
                                        Arrays.sort(c);  //@sigs
                                        sigs[i] = new String(c);  //@sigs
                                    }
                                    for (int i = 0; i < sigs.length; i++)  //@pairs
                                        for (int j = i + 1; j < sigs.length; j++)  //@pairs
                                            if (sigs[i].equals(sigs[j])) total++;  //@pairs
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int anagramTwins(string& s) {
                                int n = s.size(), total = 0;  //@init
                                for (int L = 1; L < n; L++) {  //@len
                                    vector<string> sigs;  //@sigs
                                    for (int i = 0; i + L <= n; i++) {  //@sigs
                                        string w = s.substr(i, L);  //@sigs
                                        sort(w.begin(), w.end());  //@sigs
                                        sigs.push_back(w);  //@sigs
                                    }
                                    for (size_t i = 0; i < sigs.size(); i++)  //@pairs
                                        for (size_t j = i + 1; j < sigs.size(); j++)  //@pairs
                                            if (sigs[i] == sigs[j]) total++;  //@pairs
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int anagramTwins(char* s) {
                            int n = strlen(s), total = 0;  //@init
                            int (*cnt)[26] = malloc((n + 1) * sizeof *cnt);  //@init
                            for (int L = 1; L < n; L++) {  //@len
                                int m = n - L + 1;  //@sigs
                                for (int i = 0; i < m; i++) {  //@sigs
                                    memset(cnt[i], 0, sizeof cnt[i]);  //@sigs
                                    for (int k = i; k < i + L; k++) cnt[i][s[k] - 'a']++;  //@sigs
                                }
                                for (int i = 0; i < m; i++)  //@pairs
                                    for (int j = i + 1; j < m; j++)  //@pairs
                                        if (memcmp(cnt[i], cnt[j], sizeof cnt[i]) == 0) total++;  //@pairs
                            }
                            free(cnt);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("init", "The running total."), ("len", "Twins must have the same length."), ("sigs", "A signature for every window: its sorted letters.", {"c": "C uses each window's 26 letter counts as its signature."}), ("pairs", "Every pair of windows with equal signatures is a twin pair."), ("ret", "Total.")],
                complexity=["**Time O(n³)** pair comparisons (each costing up to O(L) or 26). **Space O(n)** signatures per length."],
                limits=["Comparing all pairs is cubic. Grouping equal signatures with a hash map (or sorting them) counts pairs per group in one go: k(k − 1)/2."],
                slow=True,
            ),
            approach(
                "Sliding counts, grouped by signature",
                "best",
                "O(n² · 26)",
                "O(n · 26)",
                idea=["For each length L: counts of the first window; then slide, adding the new letter and removing the old. Record each window's 26-count tuple in a hash map. Add `k(k − 1)/2` for every group of size k."],
                walk=w2,
                build=["For each length, initial counts.", "Slide and record signatures.", "Sum pairs per group."],
                code={
                    "python": """
                        from collections import Counter

                        class Solution:
                            def anagramTwins(self, s: str) -> int:
                                n, total = len(s), 0  #@init
                                codes = [ord(c) - 97 for c in s]  #@init
                                for L in range(1, n):  #@len
                                    cnt = [0] * 26  #@first
                                    for c in codes[:L]:  #@first
                                        cnt[c] += 1  #@first
                                    seen = Counter([tuple(cnt)])  #@first
                                    for i in range(L, n):  #@slide
                                        cnt[codes[i]] += 1  #@slide
                                        cnt[codes[i - L]] -= 1  #@slide
                                        seen[tuple(cnt)] += 1  #@slide
                                    total += sum(k * (k - 1) // 2 for k in seen.values())  #@pairs
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int anagramTwins(String s) {
                                int n = s.length(), total = 0;  //@init
                                for (int L = 1; L < n; L++) {  //@len
                                    int[] cnt = new int[26];  //@first
                                    for (int i = 0; i < L; i++) cnt[s.charAt(i) - 'a']++;  //@first
                                    Map<String, Integer> seen = new HashMap<>();  //@first
                                    seen.merge(Arrays.toString(cnt), 1, Integer::sum);  //@first
                                    for (int i = L; i < n; i++) {  //@slide
                                        cnt[s.charAt(i) - 'a']++;  //@slide
                                        cnt[s.charAt(i - L) - 'a']--;  //@slide
                                        seen.merge(Arrays.toString(cnt), 1, Integer::sum);  //@slide
                                    }
                                    for (int k : seen.values()) total += k * (k - 1) / 2;  //@pairs
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int anagramTwins(string& s) {
                                int n = s.size(), total = 0;  //@init
                                for (int L = 1; L < n; L++) {  //@len
                                    array<int, 26> cnt{};  //@first
                                    for (int i = 0; i < L; i++) cnt[s[i] - 'a']++;  //@first
                                    map<array<int, 26>, int> seen;  //@first
                                    seen[cnt]++;  //@first
                                    for (int i = L; i < n; i++) {  //@slide
                                        cnt[s[i] - 'a']++;  //@slide
                                        cnt[s[i - L] - 'a']--;  //@slide
                                        seen[cnt]++;  //@slide
                                    }
                                    for (auto& [sig, k] : seen) total += k * (k - 1) / 2;  //@pairs
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int by_counts(const void* x, const void* y) { return memcmp(x, y, 26 * sizeof(int)); }  //@pairs

                        int anagramTwins(char* s) {
                            int n = strlen(s), total = 0;  //@init
                            int (*sig)[26] = malloc((n + 1) * sizeof *sig);  //@init
                            for (int L = 1; L < n; L++) {  //@len
                                int cnt[26] = {0}, m = 0;  //@first
                                for (int i = 0; i < L; i++) cnt[s[i] - 'a']++;  //@first
                                memcpy(sig[m++], cnt, sizeof cnt);  //@first
                                for (int i = L; i < n; i++) {  //@slide
                                    cnt[s[i] - 'a']++;  //@slide
                                    cnt[s[i - L] - 'a']--;  //@slide
                                    memcpy(sig[m++], cnt, sizeof cnt);  //@slide
                                }
                                qsort(sig, m, sizeof *sig, by_counts);  //@pairs
                                for (int i = 0, j; i < m; i = j) {  //@pairs
                                    for (j = i; j < m && memcmp(sig[i], sig[j], sizeof cnt) == 0; j++);  //@pairs
                                    total += (j - i) * (j - i - 1) / 2;  //@pairs
                                }
                            }
                            free(sig);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "The running total."),
                    ("len", "Twins have the same length, so handle each length separately."),
                    ("first", "Counts of the first window, recorded as a signature."),
                    ("slide", "Moving the window one step changes two counters; record the new signature."),
                    ("pairs", "k windows sharing a signature give k(k − 1)/2 pairs.", {"c": "No hash map: sort the signatures and count runs of equal ones."}),
                    ("ret", "Total over all lengths."),
                ],
                complexity=["**Time O(n² · 26)** (C: O(n² log n · 26) with sorting). **Space O(n · 26)** per length."],
            ),
        ],
        takeaways=[
            """
            - **Anagram grouping = group by letter-count signature.**
            - Fixed-length windows update their signature in O(1) per slide.
            - k items in a group form k(k − 1)/2 pairs.
            """
        ],
    )
