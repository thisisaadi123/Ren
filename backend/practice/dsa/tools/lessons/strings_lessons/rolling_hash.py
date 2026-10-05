"""Lesson: Rolling hash (Strings, pattern 2)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

PREFIX = {
    "python": """
        MOD = 1_000_000_007                                 #@consts
        BASE = 131                                          #@consts


        def build(s):
            h = [0] * (len(s) + 1)                          #@arrays
            pw = [1] * (len(s) + 1)                         #@arrays
            for i, ch in enumerate(s):                      #@fill
                h[i + 1] = (h[i] * BASE + ord(ch)) % MOD    #@fill
                pw[i + 1] = pw[i] * BASE % MOD              #@fill
            return h, pw                                    #@fill


        def window(h, pw, a, length):
            return (h[a + length] - h[a] * pw[length]) % MOD    #@window


        def same(h, pw, a, b, length):
            return window(h, pw, a, length) == window(h, pw, b, length)    #@same
    """,
    "java": """
        static final long MOD = 1_000_000_007L, BASE = 131;     //@consts

        static long[][] build(String s) {
            int n = s.length();
            long[] h = new long[n + 1], pw = new long[n + 1];   //@arrays
            pw[0] = 1;                                          //@arrays
            for (int i = 0; i < n; i++) {                       //@fill
                h[i + 1] = (h[i] * BASE + s.charAt(i)) % MOD;   //@fill
                pw[i + 1] = pw[i] * BASE % MOD;                 //@fill
            }
            return new long[][] {h, pw};                        //@fill
        }

        static long window(long[] h, long[] pw, int a, int len) {
            return ((h[a + len] - h[a] * pw[len] % MOD) % MOD + MOD) % MOD;     //@window
        }

        static boolean same(long[] h, long[] pw, int a, int b, int len) {
            return window(h, pw, a, len) == window(h, pw, b, len);  //@same
        }
    """,
    "cpp": """
        const long long MOD = 1000000007LL, BASE = 131;         //@consts

        void build(const string& s, vector<long long>& h, vector<long long>& pw) {
            h.assign(s.size() + 1, 0);                          //@arrays
            pw.assign(s.size() + 1, 1);                         //@arrays
            for (size_t i = 0; i < s.size(); i++) {             //@fill
                h[i + 1] = (h[i] * BASE + s[i]) % MOD;          //@fill
                pw[i + 1] = pw[i] * BASE % MOD;                 //@fill
            }
        }

        long long window(const vector<long long>& h, const vector<long long>& pw, int a, int len) {
            return ((h[a + len] - h[a] * pw[len] % MOD) % MOD + MOD) % MOD;     //@window
        }

        bool same(const vector<long long>& h, const vector<long long>& pw, int a, int b, int len) {
            return window(h, pw, a, len) == window(h, pw, b, len);  //@same
        }
    """,
    "c": """
        #define MOD 1000000007LL                                //@consts
        #define BASE 131LL                                      //@consts

        void build(const char* s, int n, long long* h, long long* pw) {
            h[0] = 0;                                           //@arrays
            pw[0] = 1;                                          //@arrays
            for (int i = 0; i < n; i++) {                       //@fill
                h[i + 1] = (h[i] * BASE + (unsigned char)s[i]) % MOD;  //@fill
                pw[i + 1] = pw[i] * BASE % MOD;                 //@fill
            }
        }

        long long window(const long long* h, const long long* pw, int a, int len) {
            return ((h[a + len] - h[a] * pw[len] % MOD) % MOD + MOD) % MOD;     //@window
        }

        bool same(const long long* h, const long long* pw, int a, int b, int len) {
            return window(h, pw, a, len) == window(h, pw, b, len);  //@same
        }
    """,
}
PREFIX_RUN = {
    "python": """
        h, pw = build("abracadabra")
        for a, b, length in [(0, 7, 4), (1, 8, 3), (0, 3, 2), (4, 6, 1), (0, 0, 11)]:
            print(str(same(h, pw, a, b, length)).lower())
    """,
    "java": """
        public static void main(String[] args) {
            long[][] t = build("abracadabra");
            int[][] qs = {{0, 7, 4}, {1, 8, 3}, {0, 3, 2}, {4, 6, 1}, {0, 0, 11}};
            for (int[] q : qs) System.out.println(same(t[0], t[1], q[0], q[1], q[2]));
        }
    """,
    "cpp": """
        int main() {
            vector<long long> h, pw;
            build("abracadabra", h, pw);
            int qs[5][3] = {{0, 7, 4}, {1, 8, 3}, {0, 3, 2}, {4, 6, 1}, {0, 0, 11}};
            for (auto& q : qs) cout << (same(h, pw, q[0], q[1], q[2]) ? "true" : "false") << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* s = "abracadabra";
            long long h[12], pw[12];
            build(s, 11, h, pw);
            int qs[5][3] = {{0, 7, 4}, {1, 8, 3}, {0, 3, 2}, {4, 6, 1}, {0, 0, 11}};
            for (int i = 0; i < 5; i++) printf("%s\\n", same(h, pw, qs[i][0], qs[i][1], qs[i][2]) ? "true" : "false");
            return 0;
        }
    """,
}

RK = {
    "python": """
        MOD = 1_000_000_007                                 #@consts
        BASE = 131                                          #@consts


        def count_occurrences(text, pat):
            n, m = len(text), len(pat)                      #@sizes
            if m == 0 or m > n:                             #@sizes
                return 0                                    #@sizes
            top = 1                                         #@top
            for _ in range(m - 1):                          #@top
                top = top * BASE % MOD                      #@top
            hp = ht = 0                                     #@first
            for i in range(m):                              #@first
                hp = (hp * BASE + ord(pat[i])) % MOD        #@first
                ht = (ht * BASE + ord(text[i])) % MOD       #@first
            count = 0                                       #@scan
            for i in range(n - m + 1):                      #@scan
                if ht == hp and text[i:i + m] == pat:       #@check
                    count += 1                              #@check
                if i + m < n:                               #@roll
                    ht = (ht - ord(text[i]) * top) % MOD    #@roll
                    ht = (ht * BASE + ord(text[i + m])) % MOD   #@roll
            return count                                    #@ret
    """,
    "java": """
        static final long MOD = 1_000_000_007L, BASE = 131;     //@consts

        static int countOccurrences(String text, String pat) {
            int n = text.length(), m = pat.length();            //@sizes
            if (m == 0 || m > n) return 0;                      //@sizes
            long top = 1;                                       //@top
            for (int k = 0; k < m - 1; k++) top = top * BASE % MOD;     //@top
            long hp = 0, ht = 0;                                //@first
            for (int i = 0; i < m; i++) {                       //@first
                hp = (hp * BASE + pat.charAt(i)) % MOD;         //@first
                ht = (ht * BASE + text.charAt(i)) % MOD;        //@first
            }
            int count = 0;                                      //@scan
            for (int i = 0; i + m <= n; i++) {                  //@scan
                if (ht == hp && text.startsWith(pat, i)) count++;   //@check
                if (i + m < n) {                                //@roll
                    ht = (ht - text.charAt(i) * top % MOD + MOD) % MOD;    //@roll
                    ht = (ht * BASE + text.charAt(i + m)) % MOD;        //@roll
                }
            }
            return count;                                       //@ret
        }
    """,
    "cpp": """
        const long long MOD = 1000000007LL, BASE = 131;         //@consts

        int countOccurrences(const string& text, const string& pat) {
            int n = text.size(), m = pat.size();                //@sizes
            if (m == 0 || m > n) return 0;                      //@sizes
            long long top = 1;                                  //@top
            for (int k = 0; k < m - 1; k++) top = top * BASE % MOD;     //@top
            long long hp = 0, ht = 0;                           //@first
            for (int i = 0; i < m; i++) {                       //@first
                hp = (hp * BASE + pat[i]) % MOD;                //@first
                ht = (ht * BASE + text[i]) % MOD;               //@first
            }
            int count = 0;                                      //@scan
            for (int i = 0; i + m <= n; i++) {                  //@scan
                if (ht == hp && text.compare(i, m, pat) == 0) count++;  //@check
                if (i + m < n) {                                //@roll
                    ht = (ht - text[i] * top % MOD + MOD) % MOD;    //@roll
                    ht = (ht * BASE + text[i + m]) % MOD;       //@roll
                }
            }
            return count;                                       //@ret
        }
    """,
    "c": """
        #define MOD 1000000007LL                                //@consts
        #define BASE 131LL                                      //@consts

        int countOccurrences(const char* text, const char* pat) {
            int n = strlen(text), m = strlen(pat);              //@sizes
            if (m == 0 || m > n) return 0;                      //@sizes
            long long top = 1;                                  //@top
            for (int k = 0; k < m - 1; k++) top = top * BASE % MOD;     //@top
            long long hp = 0, ht = 0;                           //@first
            for (int i = 0; i < m; i++) {                       //@first
                hp = (hp * BASE + (unsigned char)pat[i]) % MOD; //@first
                ht = (ht * BASE + (unsigned char)text[i]) % MOD;    //@first
            }
            int count = 0;                                      //@scan
            for (int i = 0; i + m <= n; i++) {                  //@scan
                if (ht == hp && strncmp(text + i, pat, m) == 0) count++;    //@check
                if (i + m < n) {                                //@roll
                    ht = (ht - (unsigned char)text[i] * top % MOD + MOD) % MOD;    //@roll
                    ht = (ht * BASE + (unsigned char)text[i + m]) % MOD;    //@roll
                }
            }
            return count;                                       //@ret
        }
    """,
}
RK_RUN = {
    "python": """
        for text, pat in [("abababa", "aba"), ("aaaa", "aa"), ("abc", "d"), ("ab", "abc")]:
            print(count_occurrences(text, pat))
    """,
    "java": """
        public static void main(String[] args) {
            String[][] tests = {{"abababa", "aba"}, {"aaaa", "aa"}, {"abc", "d"}, {"ab", "abc"}};
            for (String[] t : tests) System.out.println(countOccurrences(t[0], t[1]));
        }
    """,
    "cpp": """
        int main() {
            vector<pair<string, string>> tests = {{"abababa", "aba"}, {"aaaa", "aa"}, {"abc", "d"}, {"ab", "abc"}};
            for (auto& [text, pat] : tests) cout << countOccurrences(text, pat) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* tests[][2] = {{"abababa", "aba"}, {"aaaa", "aa"}, {"abc", "d"}, {"ab", "abc"}};
            for (int i = 0; i < 4; i++) printf("%d\\n", countOccurrences(tests[i][0], tests[i][1]));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

build = py(PREFIX["python"], "build")
window = py(PREFIX["python"], "window")
same = py(PREFIX["python"], "same")
MOD = py(PREFIX["python"], "MOD")
count_occurrences = py(RK["python"], "count_occurrences")

S = "abracadabra"
H, PW = build(S)
for a in range(len(S)):
    for b in range(len(S)):
        for L in range(1, len(S) - max(a, b) + 1):
            assert same(H, PW, a, b, L) == (S[a:a + L] == S[b:b + L])
for text, pat in [("abababa", "aba"), ("aaaa", "aa"), ("abc", "d"), ("ab", "abc"), ("mississippi", "issi")]:
    assert count_occurrences(text, pat) == sum(1 for i in range(len(text) - len(pat) + 1) if len(pat) and text[i:i + len(pat)] == pat)

# Theory walk: digits, base 10, no modulus, so the numbers are readable.
DG, W = "31415926", 3
dw = Steps(f"A window of {W} digits sliding over {DG}. With base 10 the hash of a window is just the number it spells.")
val = int(DG[:W])
dw.step(f"The first window reads {DG[:W]}, so its value is {val}.",
        Row(list(DG), st={k: "active" for k in range(W)}, slots=True, label="digits"), M({"window": val, "worked out as": "read directly"}))
for i in range(1, len(DG) - W + 1):
    old, new = DG[i - 1], DG[i + W - 1]
    nv = (val - int(old) * 10 ** (W - 1)) * 10 + int(new)
    dw.step(f"Slide right: take away the leading {old} (worth {int(old) * 10 ** (W - 1)}), shift everything up one place (× 10), and add {new}. "
            f"That's {nv}, without reading the middle digits again.",
            Row(list(DG), st={i - 1: "dim", **{k: "active" for k in range(i, i + W)}}, slots=True, label="digits"),
            M({"window": nv, "worked out as": f"({val} - {old}·100)·10 + {new}"}))
    assert nv == int(DG[i:i + W])
    val = nv
D_LEGEND = {"active": "the window", "dim": "the digit that just left"}

# Trace walk: answering the template's queries with two subtractions.
QS = [(0, 7, 4), (1, 8, 3), (0, 3, 2), (4, 6, 1)]
tw = Steps(f"`same` on \"{S}\". `build` ran once; every question below costs two `window` calls.")
tw.step(f"The prefix hashes are ready: `h[i]` is the hash of the first `i` letters. Now compare pieces of \"{S}\".",
        Row(list(S), slots=True, label="s"), M({"first piece": "–", "second piece": "–", "verdict": "–"}))
for a, b, L in QS:
    x, y = window(H, PW, a, L), window(H, PW, b, L)
    eq = x == y
    st = {k: "answer" for k in list(range(a, a + L)) + list(range(b, b + L))} if eq else {**{k: "active" for k in range(a, a + L)}, **{k: "mark" for k in range(b, b + L)}}
    tw.step(f"\"{S[a:a + L]}\" at {a} against \"{S[b:b + L]}\" at {b}: hashes {x} and {y}. " + ("Equal, so the pieces are (almost certainly) equal." if eq else "Different, so the pieces are definitely different."),
            Row(list(S), st=st, slots=True, label="s"), M({"first piece": x, "second piece": y, "verdict": "same" if eq else "different"}))
T_LEGEND = {"active": "first piece", "mark": "second piece", "answer": "both pieces, equal hashes"}

# Collisions: expected number among many windows with one modulus.
N = 10**5
PAIRS = N * (N - 1) // 2
EXPECT = PAIRS / MOD
TWO = PAIRS / (MOD * 998244353)

lesson(
    "strings",
    "rolling-hash",
    """
    Turn every substring into a number you can compute in O(1), so comparing two substrings is comparing two numbers.
    Read the string as digits of a big base, keep prefix values, and get any substring's value by subtracting. Sliding
    a window by one letter updates its value in O(1) too.
    """,
    [
        ("idea", "The idea", [
            f"""
            Think of the digits `{DG}`. The three digits starting at index 1 spell the number 141. You can read that off
            directly, but there's another way that doesn't look at the middle digits: the first four digits spell 3141,
            the first one spells 3, and `3141 - 3 × 1000 = 141`. Prefix values plus one subtraction give any piece.

            Strings work the same way if each letter is treated as a "digit" in a big base, say 131. The prefix value of
            "abc" is `a·131² + b·131 + c`, using each letter's character code. These numbers get enormous, so everything
            is kept modulo a large prime. Two equal substrings always get equal values. Two different ones almost
            always get different values; when they don't, that's a *collision*, and handling that risk is part of the
            pattern.
            """,
            fig(Row(list(DG), st={1: "active", 2: "active", 3: "active"}, slots=True, label="digits"),
                caption="Prefix 3141 minus prefix 3 shifted up three places gives 141, the highlighted window."),
            key("""
            `h[i + 1] = h[i]·B + s[i]` and `pw[i + 1] = pw[i]·B`, all mod `M`. The hash of `s[a : a + L]` is
            `h[a + L] - h[a]·pw[L]` (mod `M`). Equal hashes mean "probably equal"; different hashes mean "definitely
            different". O(n) to build, O(1) per comparison.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            Lots of substring comparisons: "do these two pieces match?", "has this window appeared before?", "how many
            different substrings of length k?", "the longest substring that appears twice". Comparing character by
            character would cost O(length) each time; hashing makes it O(1).
            """,
            table(
                ["The problem says…", "what the hash buys"],
                ["many questions: is `s[a..]` equal to `s[b..]` for length `L`?", "O(1) per question after O(n) setup"],
                ["how many different windows of length `k`", "put each window's hash in a set"],
                ["find a pattern in a text", "slide a window, compare hashes, confirm on a match"],
                ["the longest substring that repeats", "for a guessed length, hash every window; binary search the length"],
                ["is `s[i..j]` a palindrome, many times", "compare the forward hash with the hash of the reversed string"],
            ),
            """
            Not a fit:

            - A single search for one pattern. KMP or the Z-function (*KMP and Z-function*) are exact and just as fast,
              with no collision risk.
            - An answer that has to be exactly right on adversarial input, with no time to double-check matches.
              Hashing is probabilistic.
            - Short strings and few comparisons. Just compare them.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### A string as a number

            Read `s` as a number in base `B`: the hash of `s[0..k-1]` is `s[0]·B^(k-1) + s[1]·B^(k-2) + … + s[k-1]`.
            Building it one letter at a time is Horner's rule: multiply what you have by `B`, add the next letter. So
            `h[i + 1] = h[i]·B + s[i]` gives every prefix hash in one pass.

            ### Any substring from two prefixes

            `h[a + L]` is the number spelled by the first `a + L` letters. `h[a]` is the first `a` letters, and those
            same letters sit `L` places further up inside `h[a + L]`, so they're worth `h[a]·B^L` there. Subtract that
            and what's left is exactly the number spelled by `s[a..a + L - 1]`. All of it works the same modulo `M`, as
            long as you fix up a negative result by adding `M`.

            ### Sliding a window

            To move a window of length `m` one step right: subtract the leaving letter times `B^(m-1)` (its place
            value), multiply by `B`, and add the new letter. That's the same subtraction as above, done one step at a
            time.
            """,
            walk(dw, legend=D_LEGEND),
            f"""
            ### Collisions

            Different substrings can share a hash, because there are far more strings than values below `M`. With a good
            random-looking base, two different strings collide with probability about `1/M`. That's tiny for one
            comparison, but it adds up: among {N:,} windows there are about {PAIRS:,} pairs, so with
            `M = 1,000,000,007` you'd expect around {EXPECT:.0f} colliding pairs. Three ways to deal with that:

            - Confirm every hash match by comparing the actual characters (Rabin-Karp does this). Exact, and cheap
              when real matches are rare.
            - Use two independent moduli and compare both hashes. The expected number of collisions drops to about {TWO * 1e9:.0f} in a billion.
            - Use one very large modulus such as `2⁶¹ - 1`, which needs 128-bit multiplication.

            Equal hashes say "probably equal". Different hashes always mean different strings, so a mismatch never
            needs checking.

            ### Choosing B and M

            `M` should be a large prime that keeps `M²` within 64 bits, so products don't overflow before the `%`:
            `10⁹ + 7` is the usual choice. `B` should be bigger than the alphabet (131 is above every ASCII code) and
            ideally random, so nobody can build inputs that collide on purpose.
            """,
        ]),
        ("template", "The template", [
            """
            Build prefix hashes for `s` once, then answer "is `s[a : a + L]` the same as `s[b : b + L]`?" in O(1) per
            question.
            """,
            code(
                "Prefix hashes and O(1) substring comparison",
                PREFIX,
                [
                    ("consts", "A prime modulus whose square fits in 64 bits, and a base bigger than any character code."),
                    ("arrays", "`h[i]` will be the hash of the first `i` letters (`h[0] = 0`). `pw[i]` is `B^i` mod `M`."),
                    ("fill", "Horner's rule: shift the prefix up one place and add the next letter.",
                     {"c": "Casting to `unsigned char` keeps characters above 127 from turning negative."}),
                    ("window", "The hash of `s[a : a + L]`: the longer prefix minus the shorter one shifted up `L` places.",
                     {"python": "Python's `%` never returns a negative number, so no fix-up is needed.",
                      "java": "`%` can return a negative number in Java. Adding `MOD` and taking `%` again fixes it.",
                      "cpp": "`%` can return a negative number in C++. Adding `MOD` and taking `%` again fixes it.",
                      "c": "`%` can return a negative number in C. Adding `MOD` and taking `%` again fixes it."}),
                    ("same", "Equal hashes: almost certainly equal pieces. Different hashes: certainly different."),
                ],
                PREFIX_RUN,
                'build("abracadabra"); same for (0, 7, 4), (1, 8, 3), (0, 3, 2), (4, 6, 1), (0, 0, 11)',
            ),
        ]),
        ("trace", "Trace it by hand", [
            "The first four questions from the example run. Each is two subtractions, however long the pieces are:",
            walk(tw, legend=T_LEGEND),
            """
            To check a hash by hand, use base 10 and digit strings, as in the theory walkthrough. The arithmetic is the
            same; only the base and the modulus change.
            """,
        ]),
        ("examples", "More examples", [
            """
            ### Palindromes in O(1) per question

            Build prefix hashes of `s` and of `s` reversed. `s[i..j]` is a palindrome exactly when it equals its own
            reverse, and its reverse is a substring of the reversed string (starting at `n - 1 - j`). So one comparison of
            two hashes answers it, after O(n) setup.

            ### Different windows of length k

            Slide a window of length `k` across the string, keeping its hash, and add each hash to a set. The set's size
            is the number of different windows, as long as there are no collisions; with two moduli, store the pair.

            ### Lengths you can binary search

            "The longest substring that appears at least twice" has a useful shape: if some length `L` works, every
            shorter length works too (take a piece of the repeat). So binary search on `L`, and for each guess hash every
            window of length `L` and look for a repeat. That's O(n log n) instead of trying every length.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Rabin-Karp search

            To count where a pattern appears in a text, slide a window the pattern's length across the text, updating
            its hash in O(1) per step. When the window's hash equals the pattern's, compare the characters to rule out
            a collision. Expected time O(n + m) when real matches are few.
            """,
            code(
                "Count a pattern's occurrences with a rolling window",
                RK,
                [
                    ("consts", "The same modulus and base as the template."),
                    ("sizes", "An empty pattern, or one longer than the text, has no occurrences here."),
                    ("top", "`B^(m-1)`: the place value of the letter that leaves the window."),
                    ("first", "Hash the pattern and the first window of the text."),
                    ("scan", "Every window start, left to right."),
                    ("check", "Equal hashes: confirm with a real comparison, so a collision can't produce a wrong count.",
                     {"java": "`startsWith(pat, i)` compares the characters starting at `i`.",
                      "cpp": "`compare(i, m, pat)` compares `m` characters starting at `i`.",
                      "c": "`strncmp` compares the first `m` characters."}),
                    ("roll", "Slide one place: remove the leaving letter, shift up, add the new letter."),
                    ("ret", "The number of occurrences. Overlapping ones count."),
                ],
                RK_RUN,
                'count_occurrences("abababa", "aba"); ("aaaa", "aa"); ("abc", "d"); ("ab", "abc")',
            ),
            """
            `"aaaa"` contains `"aa"` three times: at 0, 1 and 2. Overlaps count because the window moves one step at a
            time.

            ### Double hashing

            Run everything twice with two different moduli (say `10⁹ + 7` and `998244353`) and treat the pair of
            values as the hash. Collisions become negligible for any input size you'll meet, at twice the work.

            ### Hashing other sequences

            Nothing here is specific to letters. Arrays of numbers, rows of a grid, or paths in a tree can be hashed the
            same way, as long as each element maps to a number smaller than the base (or the base is large and random).
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Building prefix hashes is O(n) time and O(n) space. Each substring comparison is O(1). A rolling window over
            a text of length `n` is O(n) in total. Rabin-Karp with confirmation is O(n + m) expected, and O(n · m) in the
            unlucky worst case where many windows collide or match.
            """,
            table(
                ["Task", "Direct", "With hashing"],
                ["q substring comparisons of length up to L", "O(q · L)", "O(n + q)"],
                ["distinct windows of length k", "O(n · k) with a set of strings", "O(n) expected"],
                ["find a pattern", "O(n · m)", "O(n + m) expected"],
                ["longest repeated substring", "O(n³) naively", "O(n log n) with binary search"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            Integers never overflow, so you could skip the modulus, but huge numbers make every operation slow. Keep the
            `% MOD`. `ord(ch)` gives the character code.

            ### Java

            `long` everywhere, and keep products below 2⁶³: with `MOD` around 10⁹, `h * BASE` and `h * pw` are fine. Fix
            negative results of `%`. Don't use `String.hashCode()`: it uses a fixed base and int overflow, and colliding
            strings are easy to construct.

            ### C++

            `long long`, with the same negative fix-up. For a modulus of `2⁶¹ - 1`, multiply in `__int128`.
            `std::hash<string>` hashes a whole string, not a substring, so it doesn't help with windows.

            ### C

            `long long` and `%`. Cast characters to `unsigned char` before using them as numbers. Arrays of `n + 1` for
            the prefixes and powers.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Treating equal hashes as proof. Confirm, or use two moduli.
            - Negative values from `%` in Java, C and C++.
            - Overflow from multiplying before taking the modulus, when `M²` doesn't fit in 64 bits.
            - Off-by-one in prefixes: the window `s[a : a + L]` uses `h[a + L]` and `h[a]`, not `h[a + L - 1]`.
            - Forgetting `pw[L]` and subtracting `h[a]` unshifted.
            - Using letter values that can be 0 (like `ch - 'a'` with `a = 0`): then "a", "aa" and "aaa" all hash to 0. Use
              the character code, or `ch - 'a' + 1`.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("How is the hash of `s[a : a + L]` computed from the prefix hashes?",
                 "`h[a + L] - h[a] · B^L`, modulo M. The first `a` letters are inside `h[a + L]` shifted up `L` places, and the subtraction removes them."),
                ("Two substrings have different hashes. Do you need to compare them character by character?",
                 "No. Equal strings always have equal hashes, so different hashes mean the strings differ."),
                ("Why can't letters be numbered from 0?",
                 "A letter worth 0 adds nothing, so strings of different lengths made of it (\"a\", \"aa\") all hash the same. Starting from 1 (or using character codes) avoids that."),
                ("With one modulus near 10⁹, why do collisions become likely among 10⁵ windows?",
                 "There are about 5 × 10⁹ pairs of windows, and each pair collides with probability about 1 in 10⁹. So a handful of collisions is expected."),
                ("How does the window update when it slides one step right?",
                 "Subtract the leaving letter times B^(m-1), multiply by B, and add the new letter, all modulo M."),
            ),
        ]),
    ],
)
