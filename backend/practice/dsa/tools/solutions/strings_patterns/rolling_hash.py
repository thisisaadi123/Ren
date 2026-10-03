"""Strings: rolling (polynomial) hashes, often with binary search on the length."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

M1, M2, B = 1_000_000_007, 1_000_000_009, 131


def h(t, mod):
    v = 0
    for c in t:
        v = (v * B + ord(c)) % mod
    return v


def longest_repeat_ref(s):
    n = len(s)
    best = 0
    for d in range(1, n):
        run = 0
        for i in range(n - d):
            run = run + 1 if s[i] == s[i + d] else 0
            best = max(best, run)
    return best


def shared_ref(a, b):
    best = 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best


HASH_IDEA = """
            A polynomial hash reads a string as a number in base `B`: `h("abc") = a·B² + b·B + c` (mod a large prime). Moving
            a window one step is O(1): subtract the leaving letter times `B^(k−1)`, multiply by `B`, add the new letter.
            Two different primes together make an accidental collision about as likely as guessing a random 60-bit number.
"""


@problem
def distinct_windows():
    s, k = "abcabcba", 3
    wins = [s[i:i + k] for i in range(len(s) - k + 1)]
    want = len(set(wins))

    w1 = Steps("Put every window's text in a set.")
    seen = []
    for i, x in enumerate(wins):
        new = x not in seen
        if new:
            seen.append(x)
        w1.step(f"Window {i}: '{x}' {'is new' if new else 'was seen before'}.", Row(list(s), st={t: ("found" if new else "dim") for t in range(i, i + k)}), Vars(distinct=len(seen)))
    w1.step(f"{want} different windows.", result=want)

    w2 = Steps("Keep the window's hash as a number and update it in O(1) per step; store the pair of hashes in a set.")
    seen_h = []
    for i, x in enumerate(wins):
        key = (h(x, M1), h(x, M2))
        new = key not in seen_h
        if new:
            seen_h.append(key)
        how = "computed from scratch" if i == 0 else f"rolled: drop '{s[i - 1]}', add '{s[i + k - 1]}'"
        w2.step(f"Window '{x}': hash {key[0]} ({how}); {'new' if new else 'already in the set'}.", Row(list(s), st={t: ("found" if new else "dim") for t in range(i, i + k)}), Vars(distinct=len(seen_h)))
    w2.step(f"{want} different hash pairs, so {want} different windows.", result=want)

    sol(
        "distinct-windows",
        summary="""
            Hash each window instead of storing its text. A polynomial rolling hash moves from one window to the next in
            O(1): remove the leaving letter's contribution, shift by the base, add the new letter. Two hashes with
            different primes, packed into one 64-bit key, go into a set; its size is the answer. O(n) expected.
        """,
        question=[
            """
            Count the different strings seen by a window of exactly `k` letters sliding across `s`.

            - **n up to 10⁵**, and `k` can be large too, so storing every window's text can take billions of characters.
            """
        ],
        think=[
            f"""
            `"{s}"` with `k = {k}`: windows {wins} → **{want}** different.

            Comparing windows as text costs O(k) each. Instead, give each window a fingerprint that updates in O(1) as the
            window slides, and compare fingerprints.
            """,
            HASH_IDEA,
            fig(Row(list(s), label="s")),
        ],
        approaches=[
            approach(
                "Set of window strings",
                "brute",
                "O(n · k)",
                "O(n · k)",
                idea=["Slice every window and insert it into a hash set."],
                walk=w1,
                build=["All windows.", "Set of strings."],
                code={
                    "python": """
                        class Solution:
                            def distinctWindows(self, s: str, k: int) -> int:
                                return len({s[i:i + k] for i in range(len(s) - k + 1)})  #@set
                    """,
                    "java": """
                        class Solution {
                            public int distinctWindows(String s, int k) {
                                Set<String> seen = new HashSet<>();  //@set
                                for (int i = 0; i + k <= s.length(); i++) seen.add(s.substring(i, i + k));  //@set
                                return seen.size();  //@set
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int distinctWindows(string& s, int k) {
                                unordered_set<string> seen;  //@set
                                for (int i = 0; i + k <= (int) s.size(); i++) seen.insert(s.substr(i, k));  //@set
                                return seen.size();  //@set
                            }
                        };
                    """,
                    "c": """
                        static int K;  //@sort

                        static int by_window(const void* x, const void* y) {  //@sort
                            return strncmp(*(char* const*) x, *(char* const*) y, K);  //@sort
                        }  //@sort

                        int distinctWindows(char* s, int k) {
                            int count = strlen(s) - k + 1, distinct = 1;  //@set
                            char** starts = malloc(count * sizeof(char*));  //@set
                            for (int i = 0; i < count; i++) starts[i] = s + i;  //@set
                            K = k;  //@sort
                            qsort(starts, count, sizeof(char*), by_window);  //@sort
                            for (int i = 1; i < count; i++) if (strncmp(starts[i - 1], starts[i], k) != 0) distinct++;  //@count
                            free(starts);  //@count
                            return distinct;  //@count
                        }
                    """,
                },
                lines=[
                    ("set", "Every window's text, de-duplicated by a set.", {"c": "C has no string set: point at every window start instead."}),
                    ("sort", "Sort the windows by their first `k` letters, so equal windows sit next to each other."),
                    ("count", "Count the places where neighbours differ."),
                ],
                complexity=["**Time O(n · k)** to slice and hash the windows (C: O(n · k · log n) for the sort). **Space O(n · k)** for the stored text (C stores only pointers)."],
                limits=["Each window costs O(k). With `n = 10⁵` and `k = 5 × 10⁴`, that's billions of character operations."],
                slow=True,
            ),
            approach(
                "Rolling double hash",
                "best",
                "O(n)",
                "O(n)",
                idea=["Compute both hashes of the first window. For each next window: `h = ((h − out · B^(k−1)) · B + in) mod M` for both moduli. Insert `(h1 << 32) | h2` into a set."],
                walk=w2,
                build=["`B^(k−1)` for both moduli.", "Hash the first window.", "Roll, insert, count."],
                code={
                    "python": """
                        class Solution:
                            def distinctWindows(self, s: str, k: int) -> int:
                                M1, M2, B = 1_000_000_007, 1_000_000_009, 131  #@init
                                top1, top2 = pow(B, k - 1, M1), pow(B, k - 1, M2)  #@init
                                h1 = h2 = 0  #@first
                                for c in s[:k]:  #@first
                                    h1, h2 = (h1 * B + ord(c)) % M1, (h2 * B + ord(c)) % M2  #@first
                                seen = {(h1, h2)}  #@first
                                for i in range(k, len(s)):  #@roll
                                    out, c = ord(s[i - k]), ord(s[i])  #@roll
                                    h1 = ((h1 - out * top1) * B + c) % M1  #@roll
                                    h2 = ((h2 - out * top2) * B + c) % M2  #@roll
                                    seen.add((h1, h2))  #@roll
                                return len(seen)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int distinctWindows(String s, int k) {
                                final long M1 = 1_000_000_007L, M2 = 1_000_000_009L, B = 131;  //@init
                                long top1 = 1, top2 = 1;  //@init
                                for (int i = 1; i < k; i++) { top1 = top1 * B % M1; top2 = top2 * B % M2; }  //@init
                                long h1 = 0, h2 = 0;  //@first
                                for (int i = 0; i < k; i++) { h1 = (h1 * B + s.charAt(i)) % M1; h2 = (h2 * B + s.charAt(i)) % M2; }  //@first
                                Set<Long> seen = new HashSet<>();  //@first
                                seen.add(h1 << 32 | h2);  //@first
                                for (int i = k; i < s.length(); i++) {  //@roll
                                    long out = s.charAt(i - k), c = s.charAt(i);  //@roll
                                    h1 = ((h1 - out * top1 % M1 + M1) * B + c) % M1;  //@roll
                                    h2 = ((h2 - out * top2 % M2 + M2) * B + c) % M2;  //@roll
                                    seen.add(h1 << 32 | h2);  //@roll
                                }
                                return seen.size();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int distinctWindows(string& s, int k) {
                                const long long M1 = 1000000007LL, M2 = 1000000009LL, B = 131;  //@init
                                long long top1 = 1, top2 = 1;  //@init
                                for (int i = 1; i < k; i++) { top1 = top1 * B % M1; top2 = top2 * B % M2; }  //@init
                                long long h1 = 0, h2 = 0;  //@first
                                for (int i = 0; i < k; i++) { h1 = (h1 * B + s[i]) % M1; h2 = (h2 * B + s[i]) % M2; }  //@first
                                unordered_set<long long> seen;  //@first
                                seen.insert(h1 << 32 | h2);  //@first
                                for (int i = k; i < (int) s.size(); i++) {  //@roll
                                    long long out = s[i - k], c = s[i];  //@roll
                                    h1 = ((h1 - out * top1 % M1 + M1) * B + c) % M1;  //@roll
                                    h2 = ((h2 - out * top2 % M2 + M2) * B + c) % M2;  //@roll
                                    seen.insert(h1 << 32 | h2);  //@roll
                                }
                                return seen.size();  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int by_key(const void* x, const void* y) {  //@ret
                            unsigned long long a = *(const unsigned long long*) x, b = *(const unsigned long long*) y;  //@ret
                            return a < b ? -1 : a > b;  //@ret
                        }  //@ret

                        int distinctWindows(char* s, int k) {
                            const long long M1 = 1000000007LL, M2 = 1000000009LL, B = 131;  //@init
                            int n = strlen(s), count = n - k + 1, distinct = 1;  //@init
                            long long top1 = 1, top2 = 1;  //@init
                            for (int i = 1; i < k; i++) { top1 = top1 * B % M1; top2 = top2 * B % M2; }  //@init
                            long long h1 = 0, h2 = 0;  //@first
                            for (int i = 0; i < k; i++) { h1 = (h1 * B + s[i]) % M1; h2 = (h2 * B + s[i]) % M2; }  //@first
                            unsigned long long* keys = malloc(count * sizeof(unsigned long long));  //@first
                            keys[0] = (unsigned long long) h1 << 32 | h2;  //@first
                            for (int i = k; i < n; i++) {  //@roll
                                long long out = s[i - k], c = s[i];  //@roll
                                h1 = ((h1 - out * top1 % M1 + M1) * B + c) % M1;  //@roll
                                h2 = ((h2 - out * top2 % M2 + M2) * B + c) % M2;  //@roll
                                keys[i - k + 1] = (unsigned long long) h1 << 32 | h2;  //@roll
                            }
                            qsort(keys, count, sizeof(unsigned long long), by_key);  //@ret
                            for (int i = 1; i < count; i++) if (keys[i] != keys[i - 1]) distinct++;  //@ret
                            free(keys);  //@ret
                            return distinct;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Two primes and a base larger than any letter code. `top = B^(k−1)` is the weight of a window's first letter."),
                    ("first", "Hash the first window and record it. Both hashes are below 2³⁰, so they pack into one 64-bit key."),
                    ("roll", "Remove the leaving letter (`out · top`), shift everything one place (`· B`), add the new letter. Adding `M` before the `%` keeps it non-negative.", {"python": "Python's `%` is always non-negative, so no adjustment is needed."}),
                    ("ret", "The number of different keys.", {"c": "Sort the keys and count where neighbours differ."}),
                ],
                complexity=["**Time O(n)** expected (O(n log n) with the sort in C). **Space O(n)** for the keys."],
            ),
        ],
        takeaways=[
            """
            - **Rolling hash:** fixed-length windows get an O(1) fingerprint update.
            - **Double hashing** (two primes) makes collisions negligible; pack both into one 64-bit key.
            - Keep the arithmetic in range: products below 2⁶³, and add the modulus before `%` after subtracting.
            """
        ],
    )


PREFIX_IDEA = """
            With prefix hashes `pre[i]` (the hash of the first `i` letters) and powers `pw[L] = B^L`, the hash of any
            substring is O(1): `hash(s[i..i+L)) = pre[i+L] − pre[i] · pw[L]` (mod M).
"""


@problem
def longest_repeat():
    s = "mississippi"
    n = len(s)
    want = longest_repeat_ref(s)

    w1 = Steps("Compare s with itself shifted by d. A run of positions where s[i] = s[i + d] is a substring that appears twice, d apart.")
    best = 0
    for d in range(1, n):
        run, top, end = 0, 0, 0
        for i in range(n - d):
            run = run + 1 if s[i] == s[i + d] else 0
            if run > top:
                top, end = run, i
        if top > best:
            best = top
            w1.step(f"Shift {d}: longest run {top}, '{s[end - top + 1:end + 1]}' at {end - top + 1} and {end - top + 1 + d}.", Row(list(s), st={**{x: "found" for x in range(end - top + 1, end + 1)}, **{x: "active" for x in range(end - top + 1 + d, end + 1 + d)}}), Vars(best=best))
    w1.step(f"No shift does better: {want}.", result=want)

    w2 = Steps("If some length L repeats, every shorter length does too (take a prefix of both copies). So binary search on L, testing each length with substring hashes in a set.")
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        subs = [s[i:i + mid] for i in range(n - mid + 1)]
        dup = next((x for i, x in enumerate(subs) if x in subs[:i]), None)
        w2.step(f"Try L = {mid} (range {lo}..{hi}): " + (f"'{dup}' appears twice, so L ≥ {mid}." if dup else f"no repeat, so L < {mid}."), Vars(lo=lo, hi=hi, mid=mid))
        if dup:
            lo = mid
        else:
            hi = mid - 1
    w2.step(f"lo = hi = {lo}.", result=want)

    sol(
        "longest-repeat",
        summary="""
            Binary search on the answer: if a substring of length `L` appears twice, so does one of length `L − 1`, so the
            lengths that repeat form a prefix 0..answer. To test a length, compute every window's hash in O(1) from prefix
            hashes and look for a duplicate in a set. O(n log n) expected.
        """,
        question=[
            """
            Return the length of the longest substring that occurs at least twice in `s` (the copies may overlap), or 0.

            - **n up to 3 × 10⁴**: comparing all pairs of positions is ~4.5 × 10⁸ steps.
            """
        ],
        think=[
            f"""
            `"{s}"` → **{want}** (`issi` appears at 1 and 4, overlapping).

            Two observations. First, the answer is monotone: a repeated substring's prefixes also repeat, so "does some
            length-`L` substring repeat?" is true up to the answer and false after it, which suits binary search. Second,
            for a fixed `L`, all `n − L + 1` windows can be fingerprinted in O(n) total, and a duplicate fingerprint means
            a repeat.
            """,
            PREFIX_IDEA,
            fig(Row(list(s), label="s")),
        ],
        approaches=[
            approach(
                "Compare s with every shift of itself",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each shift `d ≥ 1`, scan `i` and track the run of positions with `s[i] == s[i + d]`. The longest run over all shifts is the answer."],
                walk=w1,
                build=["Loop over shifts.", "Longest run of agreements."],
                code={
                    "python": """
                        class Solution:
                            def longestRepeat(self, s: str) -> int:
                                n, best = len(s), 0  #@init
                                for d in range(1, n):  #@shift
                                    run = 0  #@shift
                                    for i in range(n - d):  #@run
                                        run = run + 1 if s[i] == s[i + d] else 0  #@run
                                        best = max(best, run)  #@run
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestRepeat(String s) {
                                int n = s.length(), best = 0;  //@init
                                for (int d = 1; d < n; d++) {  //@shift
                                    int run = 0;  //@shift
                                    for (int i = 0; i + d < n; i++) {  //@run
                                        run = s.charAt(i) == s.charAt(i + d) ? run + 1 : 0;  //@run
                                        best = Math.max(best, run);  //@run
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestRepeat(string& s) {
                                int n = s.size(), best = 0;  //@init
                                for (int d = 1; d < n; d++) {  //@shift
                                    int run = 0;  //@shift
                                    for (int i = 0; i + d < n; i++) {  //@run
                                        run = s[i] == s[i + d] ? run + 1 : 0;  //@run
                                        best = max(best, run);  //@run
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestRepeat(char* s) {
                            int n = strlen(s), best = 0;  //@init
                            for (int d = 1; d < n; d++) {  //@shift
                                int run = 0;  //@shift
                                for (int i = 0; i + d < n; i++) {  //@run
                                    run = s[i] == s[i + d] ? run + 1 : 0;  //@run
                                    if (run > best) best = run;  //@run
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "No repeat yet."),
                    ("shift", "Two copies of a repeated substring start `d` apart, for some `d ≥ 1`."),
                    ("run", "Consecutive positions where `s` agrees with itself shifted by `d` form a substring that occurs at `i` and `i + d`."),
                    ("ret", "The longest such run over all shifts."),
                ],
                complexity=["**Time O(n²):** ~4.5 × 10⁸ comparisons at the limit. **Space O(1).**"],
                limits=["Quadratic. Binary search on the length plus O(n) hashing per length gives O(n log n)."],
                slow=True,
            ),
            approach(
                "Binary search on the length + rolling hash",
                "best",
                "O(n log n)",
                "O(n)",
                idea=["Precompute prefix hashes and powers for two primes. `repeats(L)`: insert each window's packed key into a set; a duplicate means yes. Binary search the largest `L` with `repeats(L)`."],
                walk=w2,
                build=["Prefix hashes and powers.", "Test one length with a set.", "Binary search the largest passing length."],
                code={
                    "python": """
                        class Solution:
                            def longestRepeat(self, s: str) -> int:
                                M1, M2, B, n = 1_000_000_007, 1_000_000_009, 131, len(s)  #@prefix
                                pre1, pre2, pw1, pw2 = [0] * (n + 1), [0] * (n + 1), [1] * (n + 1), [1] * (n + 1)  #@prefix
                                for i, c in enumerate(s):  #@prefix
                                    pre1[i + 1], pre2[i + 1] = (pre1[i] * B + ord(c)) % M1, (pre2[i] * B + ord(c)) % M2  #@prefix
                                    pw1[i + 1], pw2[i + 1] = pw1[i] * B % M1, pw2[i] * B % M2  #@prefix

                                def repeats(L):  #@test
                                    seen = set()  #@test
                                    for i in range(n - L + 1):  #@test
                                        key = ((pre1[i + L] - pre1[i] * pw1[L]) % M1, (pre2[i + L] - pre2[i] * pw2[L]) % M2)  #@test
                                        if key in seen:  #@test
                                            return True  #@test
                                        seen.add(key)  #@test
                                    return False  #@test

                                lo, hi = 0, n - 1  #@search
                                while lo < hi:  #@search
                                    mid = (lo + hi + 1) // 2  #@search
                                    if repeats(mid):  #@search
                                        lo = mid  #@search
                                    else:  #@search
                                        hi = mid - 1  #@search
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            static final long M1 = 1_000_000_007L, M2 = 1_000_000_009L, B = 131;  //@prefix
                            long[] pre1, pre2, pw1, pw2;  //@prefix

                            private boolean repeats(int n, int L) {  //@test
                                Set<Long> seen = new HashSet<>();  //@test
                                for (int i = 0; i + L <= n; i++) {  //@test
                                    long a = (pre1[i + L] - pre1[i] * pw1[L] % M1 + M1) % M1;  //@test
                                    long b = (pre2[i + L] - pre2[i] * pw2[L] % M2 + M2) % M2;  //@test
                                    if (!seen.add(a << 32 | b)) return true;  //@test
                                }
                                return false;  //@test
                            }  //@test

                            public int longestRepeat(String s) {
                                int n = s.length();  //@prefix
                                pre1 = new long[n + 1]; pre2 = new long[n + 1]; pw1 = new long[n + 1]; pw2 = new long[n + 1];  //@prefix
                                pw1[0] = pw2[0] = 1;  //@prefix
                                for (int i = 0; i < n; i++) {  //@prefix
                                    pre1[i + 1] = (pre1[i] * B + s.charAt(i)) % M1;  //@prefix
                                    pre2[i + 1] = (pre2[i] * B + s.charAt(i)) % M2;  //@prefix
                                    pw1[i + 1] = pw1[i] * B % M1;  //@prefix
                                    pw2[i + 1] = pw2[i] * B % M2;  //@prefix
                                }
                                int lo = 0, hi = n - 1;  //@search
                                while (lo < hi) {  //@search
                                    int mid = (lo + hi + 1) / 2;  //@search
                                    if (repeats(n, mid)) lo = mid; else hi = mid - 1;  //@search
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static constexpr long long M1 = 1000000007LL, M2 = 1000000009LL, B = 131;  //@prefix
                            vector<long long> pre1, pre2, pw1, pw2;  //@prefix

                            bool repeats(int n, int L) {  //@test
                                unordered_set<long long> seen;  //@test
                                seen.reserve(2 * n);  //@test
                                for (int i = 0; i + L <= n; i++) {  //@test
                                    long long a = (pre1[i + L] - pre1[i] * pw1[L] % M1 + M1) % M1;  //@test
                                    long long b = (pre2[i + L] - pre2[i] * pw2[L] % M2 + M2) % M2;  //@test
                                    if (!seen.insert(a << 32 | b).second) return true;  //@test
                                }
                                return false;  //@test
                            }  //@test

                        public:
                            int longestRepeat(string& s) {
                                int n = s.size();  //@prefix
                                pre1.assign(n + 1, 0); pre2.assign(n + 1, 0); pw1.assign(n + 1, 1); pw2.assign(n + 1, 1);  //@prefix
                                for (int i = 0; i < n; i++) {  //@prefix
                                    pre1[i + 1] = (pre1[i] * B + s[i]) % M1;  //@prefix
                                    pre2[i + 1] = (pre2[i] * B + s[i]) % M2;  //@prefix
                                    pw1[i + 1] = pw1[i] * B % M1;  //@prefix
                                    pw2[i + 1] = pw2[i] * B % M2;  //@prefix
                                }
                                int lo = 0, hi = n - 1;  //@search
                                while (lo < hi) {  //@search
                                    int mid = (lo + hi + 1) / 2;  //@search
                                    if (repeats(n, mid)) lo = mid; else hi = mid - 1;  //@search
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        #define M1 1000000007LL
                        #define M2 1000000009LL
                        #define BASE 131LL

                        static int by_key(const void* x, const void* y) {  //@test
                            unsigned long long a = *(const unsigned long long*) x, b = *(const unsigned long long*) y;  //@test
                            return a < b ? -1 : a > b;  //@test
                        }  //@test

                        static bool repeats(long long* pre1, long long* pre2, long long* pw1, long long* pw2, int n, int L, unsigned long long* keys) {  //@test
                            int count = n - L + 1;  //@test
                            for (int i = 0; i < count; i++) {  //@test
                                long long a = (pre1[i + L] - pre1[i] * pw1[L] % M1 + M1) % M1;  //@test
                                long long b = (pre2[i + L] - pre2[i] * pw2[L] % M2 + M2) % M2;  //@test
                                keys[i] = (unsigned long long) a << 32 | b;  //@test
                            }
                            qsort(keys, count, sizeof(unsigned long long), by_key);  //@test
                            for (int i = 1; i < count; i++) if (keys[i] == keys[i - 1]) return true;  //@test
                            return false;  //@test
                        }  //@test

                        int longestRepeat(char* s) {
                            int n = strlen(s);  //@prefix
                            long long *pre1 = calloc(n + 1, sizeof(long long)), *pre2 = calloc(n + 1, sizeof(long long));  //@prefix
                            long long *pw1 = malloc((n + 1) * sizeof(long long)), *pw2 = malloc((n + 1) * sizeof(long long));  //@prefix
                            unsigned long long* keys = malloc((n + 1) * sizeof(unsigned long long));  //@prefix
                            pw1[0] = pw2[0] = 1;  //@prefix
                            for (int i = 0; i < n; i++) {  //@prefix
                                pre1[i + 1] = (pre1[i] * BASE + s[i]) % M1;  //@prefix
                                pre2[i + 1] = (pre2[i] * BASE + s[i]) % M2;  //@prefix
                                pw1[i + 1] = pw1[i] * BASE % M1;  //@prefix
                                pw2[i + 1] = pw2[i] * BASE % M2;  //@prefix
                            }
                            int lo = 0, hi = n - 1;  //@search
                            while (lo < hi) {  //@search
                                int mid = (lo + hi + 1) / 2;  //@search
                                if (repeats(pre1, pre2, pw1, pw2, n, mid, keys)) lo = mid; else hi = mid - 1;  //@search
                            }
                            free(pre1); free(pre2); free(pw1); free(pw2); free(keys);  //@ret
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[
                    ("prefix", "Prefix hashes and powers for both primes, so any substring's hash is O(1)."),
                    ("test", "Does some length-`L` substring occur twice? Hash every window; a key seen before means yes.", {"c": "Sort the keys and look for equal neighbours."}),
                    ("search", "Lengths that repeat are 0..answer, so find the last `true`. `mid` rounds up so `lo = mid` always makes progress. The answer is at most `n − 1` (two copies need two different starts)."),
                    ("ret", "The longest repeated length."),
                ],
                complexity=["**Time O(n log n)** expected (C: O(n log² n) with sorting). **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - **"Longest X that appears twice"** is monotone in the length → binary search on the answer.
            - **Prefix hashes** give any substring's fingerprint in O(1).
            - Suffix arrays solve it exactly in O(n log n) as well; hashing is the shortest to write.
            """
        ],
    )


@problem
def shared_tune():
    a, b = "abcdxyz", "xyzabcq"
    want = shared_ref(a, b)

    w1 = Steps("run[i][j] = length of the common run ending at a[i−1] and b[j−1]: one more than the diagonal when the letters match, else 0.")
    prev = [0] * (len(b) + 1)
    best = 0
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        w1.step(f"Row for a[{i - 1}] = '{a[i - 1]}'.", Row(list(b), label="b"), Row(cur[1:], label="run"), Vars(best=best))
        prev = cur
    w1.step(f"The largest run is {want}.", result=want)

    w2 = Steps("Binary search on the length L; for each L, put the hashes of all of a's windows in a set and look up b's windows.")
    lo, hi = 0, min(len(a), len(b))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        sa = {a[i:i + mid] for i in range(len(a) - mid + 1)}
        hit = next((b[j:j + mid] for j in range(len(b) - mid + 1) if b[j:j + mid] in sa), None)
        w2.step(f"L = {mid}: " + (f"'{hit}' is in both, so L ≥ {mid}." if hit else f"nothing shared, so L < {mid}."), Vars(lo=lo, hi=hi, mid=mid))
        if hit:
            lo = mid
        else:
            hi = mid - 1
    w2.step(f"Longest shared run: {lo}.", result=want)

    sol(
        "shared-tune",
        summary="""
            Longest common substring. Shared runs are monotone in length (a shared run's prefix is shared too), so binary
            search the length. For a length `L`, hash every window of `a` into a set and check whether any window of `b`
            is in it, using prefix hashes with two primes. O((n + m) log min(n, m)) expected.
        """,
        question=[
            """
            Return the length of the longest substring that appears in both `a` and `b` (0 if none).

            - **Both up to 2 × 10⁴ letters**: the classic table is 4 × 10⁸ cells.
            """
        ],
        think=[
            f"""
            `a = "{a}"`, `b = "{b}"` → **{want}** (`abc` and `xyz` are both shared).

            For a fixed length `L`, the question "is there a common window of length `L`?" is a set-intersection between
            the windows of `a` and of `b`, which hashing answers in linear time. Since the answer to that question is yes
            for every length up to the true answer and no beyond it, binary search finds the answer with about 15 tests.
            """,
            PREFIX_IDEA,
            fig(Row(list(a), label="a"), Row(list(b), label="b")),
        ],
        approaches=[
            approach(
                "Dynamic programming on common runs",
                "brute",
                "O(n · m)",
                "O(m)",
                idea=["`run[i][j] = run[i−1][j−1] + 1` if `a[i−1] == b[j−1]`, else 0. The answer is the largest cell. Only the previous row is needed."],
                walk=w1,
                build=["Two rows.", "Fill from the diagonal.", "Track the maximum."],
                code={
                    "python": """
                        class Solution:
                            def sharedTune(self, a: str, b: str) -> int:
                                m, best = len(b), 0  #@init
                                prev = [0] * (m + 1)  #@init
                                for x in a:  #@fill
                                    cur = [0] * (m + 1)  #@fill
                                    for j in range(1, m + 1):  #@fill
                                        if x == b[j - 1]:  #@rule
                                            cur[j] = prev[j - 1] + 1  #@rule
                                            best = max(best, cur[j])  #@rule
                                    prev = cur  #@fill
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int sharedTune(String a, String b) {
                                int m = b.length(), best = 0;  //@init
                                int[] prev = new int[m + 1], cur = new int[m + 1];  //@init
                                for (int i = 0; i < a.length(); i++) {  //@fill
                                    char x = a.charAt(i);  //@fill
                                    for (int j = 1; j <= m; j++) {  //@fill
                                        cur[j] = x == b.charAt(j - 1) ? prev[j - 1] + 1 : 0;  //@rule
                                        best = Math.max(best, cur[j]);  //@rule
                                    }
                                    int[] t = prev; prev = cur; cur = t;  //@fill
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int sharedTune(string& a, string& b) {
                                int m = b.size(), best = 0;  //@init
                                vector<int> prev(m + 1, 0), cur(m + 1, 0);  //@init
                                for (char x : a) {  //@fill
                                    for (int j = 1; j <= m; j++) {  //@fill
                                        cur[j] = x == b[j - 1] ? prev[j - 1] + 1 : 0;  //@rule
                                        best = max(best, cur[j]);  //@rule
                                    }
                                    swap(prev, cur);  //@fill
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int sharedTune(char* a, char* b) {
                            int n = strlen(a), m = strlen(b), best = 0;  //@init
                            int* prev = calloc(m + 1, sizeof(int));  //@init
                            int* cur = calloc(m + 1, sizeof(int));  //@init
                            for (int i = 0; i < n; i++) {  //@fill
                                for (int j = 1; j <= m; j++) {  //@fill
                                    cur[j] = a[i] == b[j - 1] ? prev[j - 1] + 1 : 0;  //@rule
                                    if (cur[j] > best) best = cur[j];  //@rule
                                }
                                int* t = prev; prev = cur; cur = t;  //@fill
                            }
                            free(prev); free(cur);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "The previous row of the table (all zeros before the first letter of `a`)."),
                    ("fill", "One row per letter of `a`; swap rows when done."),
                    ("rule", "A matching pair extends the run that ended one step earlier in both strings; a mismatch breaks it."),
                    ("ret", "The longest run anywhere."),
                ],
                complexity=["**Time O(n · m):** 4 × 10⁸ cells at the limit. **Space O(m).**"],
                limits=["Quadratic. Binary search on the length with hashing needs only ~15 linear passes."],
                slow=True,
            ),
            approach(
                "Binary search on the length + rolling hash",
                "best",
                "O((n + m) log min(n, m))",
                "O(n + m)",
                idea=["Prefix hashes for both strings (two primes). `shared(L)`: all length-`L` keys of `a` in a set; any length-`L` key of `b` in the set means yes. Binary search the largest `L` that passes."],
                walk=w2,
                build=["Prefix hashes for `a` and `b`.", "Test a length with a set.", "Binary search."],
                code={
                    "python": """
                        class Solution:
                            def sharedTune(self, a: str, b: str) -> int:
                                M1, M2, B = 1_000_000_007, 1_000_000_009, 131  #@prefix
                                top = max(len(a), len(b))  #@prefix
                                pw1, pw2 = [1] * (top + 1), [1] * (top + 1)  #@prefix
                                for i in range(top):  #@prefix
                                    pw1[i + 1], pw2[i + 1] = pw1[i] * B % M1, pw2[i] * B % M2  #@prefix

                                def prefix(s, M):  #@prefix
                                    pre = [0] * (len(s) + 1)  #@prefix
                                    for i, c in enumerate(s):  #@prefix
                                        pre[i + 1] = (pre[i] * B + ord(c)) % M  #@prefix
                                    return pre  #@prefix

                                a1, a2, b1, b2 = prefix(a, M1), prefix(a, M2), prefix(b, M1), prefix(b, M2)  #@prefix

                                def keys(p1, p2, n, L):  #@test
                                    return ((((p1[i + L] - p1[i] * pw1[L]) % M1), (p2[i + L] - p2[i] * pw2[L]) % M2) for i in range(n - L + 1))  #@test

                                def shared(L):  #@test
                                    seen = set(keys(a1, a2, len(a), L))  #@test
                                    return any(k in seen for k in keys(b1, b2, len(b), L))  #@test

                                lo, hi = 0, min(len(a), len(b))  #@search
                                while lo < hi:  #@search
                                    mid = (lo + hi + 1) // 2  #@search
                                    if shared(mid):  #@search
                                        lo = mid  #@search
                                    else:  #@search
                                        hi = mid - 1  #@search
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            static final long M1 = 1_000_000_007L, M2 = 1_000_000_009L, B = 131;  //@prefix
                            long[] pw1, pw2;  //@prefix

                            private long[] prefix(String s, long M) {  //@prefix
                                long[] pre = new long[s.length() + 1];  //@prefix
                                for (int i = 0; i < s.length(); i++) pre[i + 1] = (pre[i] * B + s.charAt(i)) % M;  //@prefix
                                return pre;  //@prefix
                            }  //@prefix

                            private long key(long[] p1, long[] p2, int i, int L) {  //@test
                                long x = (p1[i + L] - p1[i] * pw1[L] % M1 + M1) % M1;  //@test
                                long y = (p2[i + L] - p2[i] * pw2[L] % M2 + M2) % M2;  //@test
                                return x << 32 | y;  //@test
                            }  //@test

                            public int sharedTune(String a, String b) {
                                int n = a.length(), m = b.length(), top = Math.max(n, m);  //@prefix
                                pw1 = new long[top + 1]; pw2 = new long[top + 1];  //@prefix
                                pw1[0] = pw2[0] = 1;  //@prefix
                                for (int i = 0; i < top; i++) { pw1[i + 1] = pw1[i] * B % M1; pw2[i + 1] = pw2[i] * B % M2; }  //@prefix
                                long[] a1 = prefix(a, M1), a2 = prefix(a, M2), b1 = prefix(b, M1), b2 = prefix(b, M2);  //@prefix
                                int lo = 0, hi = Math.min(n, m);  //@search
                                while (lo < hi) {  //@search
                                    int mid = (lo + hi + 1) / 2;  //@search
                                    Set<Long> seen = new HashSet<>();  //@test
                                    for (int i = 0; i + mid <= n; i++) seen.add(key(a1, a2, i, mid));  //@test
                                    boolean found = false;  //@test
                                    for (int j = 0; j + mid <= m && !found; j++) found = seen.contains(key(b1, b2, j, mid));  //@test
                                    if (found) lo = mid; else hi = mid - 1;  //@search
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static constexpr long long M1 = 1000000007LL, M2 = 1000000009LL, B = 131;  //@prefix
                            vector<long long> pw1, pw2;  //@prefix

                            static vector<long long> prefix(const string& s, long long M) {  //@prefix
                                vector<long long> pre(s.size() + 1, 0);  //@prefix
                                for (size_t i = 0; i < s.size(); i++) pre[i + 1] = (pre[i] * B + s[i]) % M;  //@prefix
                                return pre;  //@prefix
                            }  //@prefix

                            long long key(const vector<long long>& p1, const vector<long long>& p2, int i, int L) {  //@test
                                long long x = (p1[i + L] - p1[i] * pw1[L] % M1 + M1) % M1;  //@test
                                long long y = (p2[i + L] - p2[i] * pw2[L] % M2 + M2) % M2;  //@test
                                return x << 32 | y;  //@test
                            }  //@test

                        public:
                            int sharedTune(string& a, string& b) {
                                int n = a.size(), m = b.size(), top = max(n, m);  //@prefix
                                pw1.assign(top + 1, 1); pw2.assign(top + 1, 1);  //@prefix
                                for (int i = 0; i < top; i++) { pw1[i + 1] = pw1[i] * B % M1; pw2[i + 1] = pw2[i] * B % M2; }  //@prefix
                                auto a1 = prefix(a, M1), a2 = prefix(a, M2), b1 = prefix(b, M1), b2 = prefix(b, M2);  //@prefix
                                int lo = 0, hi = min(n, m);  //@search
                                while (lo < hi) {  //@search
                                    int mid = (lo + hi + 1) / 2;  //@search
                                    unordered_set<long long> seen;  //@test
                                    seen.reserve(2 * n);  //@test
                                    for (int i = 0; i + mid <= n; i++) seen.insert(key(a1, a2, i, mid));  //@test
                                    bool found = false;  //@test
                                    for (int j = 0; j + mid <= m && !found; j++) found = seen.count(key(b1, b2, j, mid));  //@test
                                    if (found) lo = mid; else hi = mid - 1;  //@search
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        #define M1 1000000007LL
                        #define M2 1000000009LL
                        #define BASE 131LL

                        static long long* pw1;  //@prefix
                        static long long* pw2;  //@prefix

                        static long long* prefix(const char* s, int n, long long M) {  //@prefix
                            long long* pre = calloc(n + 1, sizeof(long long));  //@prefix
                            for (int i = 0; i < n; i++) pre[i + 1] = (pre[i] * BASE + s[i]) % M;  //@prefix
                            return pre;  //@prefix
                        }  //@prefix

                        static unsigned long long key(long long* p1, long long* p2, int i, int L) {  //@test
                            long long x = (p1[i + L] - p1[i] * pw1[L] % M1 + M1) % M1;  //@test
                            long long y = (p2[i + L] - p2[i] * pw2[L] % M2 + M2) % M2;  //@test
                            return (unsigned long long) x << 32 | y;  //@test
                        }  //@test

                        static int by_key(const void* x, const void* y) {  //@test
                            unsigned long long a = *(const unsigned long long*) x, b = *(const unsigned long long*) y;  //@test
                            return a < b ? -1 : a > b;  //@test
                        }  //@test

                        int sharedTune(char* a, char* b) {
                            int n = strlen(a), m = strlen(b), top = n > m ? n : m;  //@prefix
                            pw1 = malloc((top + 1) * sizeof(long long));  //@prefix
                            pw2 = malloc((top + 1) * sizeof(long long));  //@prefix
                            pw1[0] = pw2[0] = 1;  //@prefix
                            for (int i = 0; i < top; i++) { pw1[i + 1] = pw1[i] * BASE % M1; pw2[i + 1] = pw2[i] * BASE % M2; }  //@prefix
                            long long *a1 = prefix(a, n, M1), *a2 = prefix(a, n, M2), *b1 = prefix(b, m, M1), *b2 = prefix(b, m, M2);  //@prefix
                            unsigned long long* keys = malloc((n + 1) * sizeof(unsigned long long));  //@prefix
                            int lo = 0, hi = n < m ? n : m;  //@search
                            while (lo < hi) {  //@search
                                int mid = (lo + hi + 1) / 2, count = n - mid + 1;  //@search
                                for (int i = 0; i < count; i++) keys[i] = key(a1, a2, i, mid);  //@test
                                qsort(keys, count, sizeof(unsigned long long), by_key);  //@test
                                bool found = false;  //@test
                                for (int j = 0; j + mid <= m && !found; j++) {  //@test
                                    unsigned long long k = key(b1, b2, j, mid);  //@test
                                    found = bsearch(&k, keys, count, sizeof(unsigned long long), by_key) != NULL;  //@test
                                }
                                if (found) lo = mid; else hi = mid - 1;  //@search
                            }
                            free(pw1); free(pw2); free(a1); free(a2); free(b1); free(b2); free(keys);  //@ret
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[
                    ("prefix", "Powers of `B` up to the longer string, and prefix hashes of both strings for both primes."),
                    ("test", "For length `L`: collect every window key of `a`, then check `b`'s windows against them.", {"c": "Sort `a`'s keys once per length and binary-search each of `b`'s keys."}),
                    ("search", "Find the largest `L` that is shared; `mid` rounds up so `lo = mid` makes progress."),
                    ("ret", "The longest shared run."),
                ],
                complexity=["**Time O((n + m) log min(n, m))** expected (an extra log factor with C's sorting). **Space O(n + m).**"],
            ),
        ],
        takeaways=[
            """
            - **Longest common substring:** binary search on the length + hashing beats the O(n · m) table.
            - The same template as "longest repeated substring", with two strings instead of one.
            - Hash comparison is probabilistic; double hashing makes a false match negligible.
            """
        ],
    )
