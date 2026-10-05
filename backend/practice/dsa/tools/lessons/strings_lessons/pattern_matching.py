"""Lesson: KMP and Z-function (Strings, pattern 3)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

ZF = {
    "python": """
        def z_array(s):
            n = len(s)                                          #@init
            z = [0] * n                                         #@init
            l = r = 0                                           #@box
            for i in range(1, n):                               #@each
                if i < r:                                       #@reuse
                    z[i] = min(r - i, z[i - l])                 #@reuse
                while i + z[i] < n and s[z[i]] == s[i + z[i]]:  #@extend
                    z[i] += 1                                   #@extend
                if i + z[i] > r:                                #@move
                    l, r = i, i + z[i]                          #@move
            if n:                                               #@whole
                z[0] = n                                        #@whole
            return z                                            #@whole


        def longest_prefix_in(word, text):
            z = z_array(word + "#" + text)                      #@join
            return max(z[len(word) + 1:], default=0)            #@best
    """,
    "java": """
        static int[] zArray(String s) {
            int n = s.length();                                 //@init
            int[] z = new int[n];                               //@init
            int l = 0, r = 0;                                   //@box
            for (int i = 1; i < n; i++) {                       //@each
                if (i < r) z[i] = Math.min(r - i, z[i - l]);    //@reuse
                while (i + z[i] < n && s.charAt(z[i]) == s.charAt(i + z[i])) z[i]++;  //@extend
                if (i + z[i] > r) {                             //@move
                    l = i;                                      //@move
                    r = i + z[i];                               //@move
                }
            }
            if (n > 0) z[0] = n;                                //@whole
            return z;                                           //@whole
        }

        static int longestPrefixIn(String word, String text) {
            int[] z = zArray(word + "#" + text);                //@join
            int best = 0;                                       //@best
            for (int i = word.length() + 1; i < z.length; i++) best = Math.max(best, z[i]);  //@best
            return best;                                        //@best
        }
    """,
    "cpp": """
        vector<int> zArray(const string& s) {
            int n = s.size();                                   //@init
            vector<int> z(n, 0);                                //@init
            int l = 0, r = 0;                                   //@box
            for (int i = 1; i < n; i++) {                       //@each
                if (i < r) z[i] = min(r - i, z[i - l]);         //@reuse
                while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;  //@extend
                if (i + z[i] > r) {                             //@move
                    l = i;                                      //@move
                    r = i + z[i];                               //@move
                }
            }
            if (n > 0) z[0] = n;                                //@whole
            return z;                                           //@whole
        }

        int longestPrefixIn(const string& word, const string& text) {
            vector<int> z = zArray(word + "#" + text);          //@join
            int best = 0;                                       //@best
            for (size_t i = word.size() + 1; i < z.size(); i++) best = max(best, z[i]);  //@best
            return best;                                        //@best
        }
    """,
    "c": """
        void zArray(const char* s, int n, int* z) {
            for (int i = 0; i < n; i++) z[i] = 0;               //@init
            int l = 0, r = 0;                                   //@box
            for (int i = 1; i < n; i++) {                       //@each
                if (i < r) z[i] = (r - i < z[i - l]) ? r - i : z[i - l];   //@reuse
                while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;  //@extend
                if (i + z[i] > r) {                             //@move
                    l = i;                                      //@move
                    r = i + z[i];                               //@move
                }
            }
            if (n > 0) z[0] = n;                                //@whole
        }

        int longestPrefixIn(const char* word, const char* text) {
            int w = strlen(word), t = strlen(text), n = w + 1 + t;  //@join
            char* s = malloc(n + 1);                            //@join
            int* z = malloc(n * sizeof(int));                   //@join
            memcpy(s, word, w);                                 //@join
            s[w] = '#';                                         //@join
            memcpy(s + w + 1, text, t + 1);                     //@join
            zArray(s, n, z);                                    //@join
            int best = 0;                                       //@best
            for (int i = w + 1; i < n; i++) if (z[i] > best) best = z[i];  //@best
            free(s);                                            //@best
            free(z);                                            //@best
            return best;                                        //@best
        }
    """,
}
ZF_RUN = {
    "python": """
        print(*z_array("aabxaabxaa"))
        for word, text in [("abcab", "xxabcxabca"), ("aab", "baaab"), ("z", "abc")]:
            print(longest_prefix_in(word, text))
    """,
    "java": """
        public static void main(String[] args) {
            StringBuilder sb = new StringBuilder();
            for (int x : zArray("aabxaabxaa")) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
            String[][] tests = {{"abcab", "xxabcxabca"}, {"aab", "baaab"}, {"z", "abc"}};
            for (String[] t : tests) System.out.println(longestPrefixIn(t[0], t[1]));
        }
    """,
    "cpp": """
        int main() {
            vector<int> z = zArray("aabxaabxaa");
            for (size_t i = 0; i < z.size(); i++) cout << (i ? " " : "") << z[i];
            cout << "\\n";
            vector<pair<string, string>> tests = {{"abcab", "xxabcxabca"}, {"aab", "baaab"}, {"z", "abc"}};
            for (auto& [word, text] : tests) cout << longestPrefixIn(word, text) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int z[10];
            zArray("aabxaabxaa", 10, z);
            for (int i = 0; i < 10; i++) printf(i ? " %d" : "%d", z[i]);
            printf("\\n");
            const char* tests[][2] = {{"abcab", "xxabcxabca"}, {"aab", "baaab"}, {"z", "abc"}};
            for (int i = 0; i < 3; i++) printf("%d\\n", longestPrefixIn(tests[i][0], tests[i][1]));
            return 0;
        }
    """,
}

PI = {
    "python": """
        def prefix_function(s):
            pi = [0] * len(s)                                   #@init
            for i in range(1, len(s)):                          #@each
                k = pi[i - 1]                                   #@start
                while k > 0 and s[i] != s[k]:                   #@fall
                    k = pi[k - 1]                               #@fall
                if s[i] == s[k]:                                #@grow
                    k += 1                                      #@grow
                pi[i] = k                                       #@store
            return pi                                           #@ret


        def borders(s):
            pi = prefix_function(s)                             #@chain
            out = []                                            #@chain
            k = pi[-1] if s else 0                              #@chain
            while k > 0:                                        #@walk
                out.append(k)                                   #@walk
                k = pi[k - 1]                                   #@walk
            return out                                          #@done
    """,
    "java": """
        static int[] prefixFunction(String s) {
            int[] pi = new int[s.length()];                     //@init
            for (int i = 1; i < s.length(); i++) {              //@each
                int k = pi[i - 1];                              //@start
                while (k > 0 && s.charAt(i) != s.charAt(k)) k = pi[k - 1];  //@fall
                if (s.charAt(i) == s.charAt(k)) k++;            //@grow
                pi[i] = k;                                      //@store
            }
            return pi;                                          //@ret
        }

        static List<Integer> borders(String s) {
            int[] pi = prefixFunction(s);                       //@chain
            List<Integer> out = new ArrayList<>();              //@chain
            int k = s.isEmpty() ? 0 : pi[s.length() - 1];       //@chain
            while (k > 0) {                                     //@walk
                out.add(k);                                     //@walk
                k = pi[k - 1];                                  //@walk
            }
            return out;                                         //@done
        }
    """,
    "cpp": """
        vector<int> prefixFunction(const string& s) {
            vector<int> pi(s.size(), 0);                        //@init
            for (size_t i = 1; i < s.size(); i++) {             //@each
                int k = pi[i - 1];                              //@start
                while (k > 0 && s[i] != s[k]) k = pi[k - 1];    //@fall
                if (s[i] == s[k]) k++;                          //@grow
                pi[i] = k;                                      //@store
            }
            return pi;                                          //@ret
        }

        vector<int> borders(const string& s) {
            vector<int> pi = prefixFunction(s);                 //@chain
            vector<int> out;                                    //@chain
            int k = s.empty() ? 0 : pi.back();                  //@chain
            while (k > 0) {                                     //@walk
                out.push_back(k);                               //@walk
                k = pi[k - 1];                                  //@walk
            }
            return out;                                         //@done
        }
    """,
    "c": """
        void prefixFunction(const char* s, int n, int* pi) {
            if (n > 0) pi[0] = 0;                               //@init
            for (int i = 1; i < n; i++) {                       //@each
                int k = pi[i - 1];                              //@start
                while (k > 0 && s[i] != s[k]) k = pi[k - 1];    //@fall
                if (s[i] == s[k]) k++;                          //@grow
                pi[i] = k;                                      //@store
            }
        }

        int borders(const char* s, int* out) {
            int n = strlen(s), m = 0;                           //@chain
            int* pi = malloc((n > 0 ? n : 1) * sizeof(int));    //@chain
            prefixFunction(s, n, pi);                           //@chain
            int k = n > 0 ? pi[n - 1] : 0;                      //@chain
            while (k > 0) {                                     //@walk
                out[m++] = k;                                   //@walk
                k = pi[k - 1];                                  //@walk
            }
            free(pi);                                           //@done
            return m;                                           //@done
        }
    """,
}
PI_RUN = {
    "python": """
        print(*prefix_function("abacaba"))
        for s in ["abacaba", "aaaa", "abc"]:
            print(*borders(s))
    """,
    "java": """
        public static void main(String[] args) {
            StringBuilder sb = new StringBuilder();
            for (int x : prefixFunction("abacaba")) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
            for (String s : new String[] {"abacaba", "aaaa", "abc"}) {
                StringBuilder b = new StringBuilder();
                for (int x : borders(s)) b.append(b.length() > 0 ? " " : "").append(x);
                System.out.println(b);
            }
        }
    """,
    "cpp": """
        void show(const vector<int>& v) {
            for (size_t i = 0; i < v.size(); i++) cout << (i ? " " : "") << v[i];
            cout << "\\n";
        }

        int main() {
            show(prefixFunction("abacaba"));
            for (string s : {"abacaba", "aaaa", "abc"}) show(borders(s));
        }
    """,
    "c": """
        int main(void) {
            int pi[7], out[8];
            prefixFunction("abacaba", 7, pi);
            for (int i = 0; i < 7; i++) printf(i ? " %d" : "%d", pi[i]);
            printf("\\n");
            const char* tests[] = {"abacaba", "aaaa", "abc"};
            for (int t = 0; t < 3; t++) {
                int m = borders(tests[t], out);
                for (int i = 0; i < m; i++) printf(i ? " %d" : "%d", out[i]);
                printf("\\n");
            }
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

import random  # noqa: E402

z_array = py(ZF["python"], "z_array")
longest_prefix_in = py(ZF["python"], "longest_prefix_in")
prefix_function = py(PI["python"], "prefix_function")
borders = py(PI["python"], "borders")

rng = random.Random(9)
for _ in range(300):
    s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 12)))
    z = z_array(s)
    for i in range(1, len(s)):
        k = 0
        while i + k < len(s) and s[k] == s[i + k]:
            k += 1
        assert z[i] == k
    pi = prefix_function(s)
    for i in range(len(s)):
        assert pi[i] == max([k for k in range(i + 1) if s[:k] == s[i + 1 - k:i + 1]])
    assert borders(s) == [k for k in range(len(s) - 1, 0, -1) if s[:k] == s[-k:]]


def z_walk(s, title):
    """One step per position: what z[i] is and whether the box was reused."""
    w = Steps(title)
    n = len(s)
    z = [0] * n
    shown = [None] * n
    if n:
        shown[0] = "–"
    l = r = 0
    w.step(f"`z[i]` will be how many letters starting at `i` match the start of the string. `z[0]` is the whole string by convention.",
           Row(list(s), slots=True, label="s"), Row(list(shown), slots=True, label="z"), M({"box [l, r)": "empty"}))
    for i in range(1, n):
        reused = 0
        if i < r:
            reused = min(r - i, z[i - l])
            z[i] = reused
        start = z[i]
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        extra = z[i] - start
        if i < r:
            how = (f"`i` is inside the box [{l}, {r}), which copies the start of the string, so position {i} looks like position {i - l}: "
                   f"at least min({r - i}, z[{i - l}] = {z[i - l]}) = {reused} letter{'s' if reused != 1 else ''} match{'' if reused != 1 else 'es'} for free.")
            how += f" Comparing onward adds {extra} more." if extra else " Comparing onward adds nothing."
        else:
            how = f"`i` is outside the box, so compare from scratch: {z[i]} letter{'s' if z[i] != 1 else ''} match{'' if z[i] != 1 else 'es'}."
        if i + z[i] > r:
            l, r = i, i + z[i]
            if z[i]:
                how += f" The match reaches further right than the box did, so the box becomes [{l}, {r})."
        shown[i] = z[i]
        st = {**{k: "mark" for k in range(z[i])}, **{k: "answer" for k in range(i, i + z[i])}}
        w.step(f"`i` = {i}: " + how, Row(list(s), st=st, ptr={"i": i}, slots=True, label="s"),
               Row(list(shown), st={i: "active"}, slots=True, label="z"), M({"box [l, r)": f"[{l}, {r})" if r > l else "empty"}))
    return w, z


ZS = "aabxaabxaa"
zw, ZV = z_walk(ZS, f"`z_array(\"{ZS}\")`. The box [l, r) is the rightmost stretch known to copy the start of the string.")
assert ZV[1:] == z_array(ZS)[1:]
Z_LEGEND = {"answer": "the stretch starting at `i` that matches the start", "mark": "the start of the string it matches", "active": "the value just worked out"}

TWORD, TTEXT = "aab", "baaab"
JS = TWORD + "#" + TTEXT
tw, TZ = z_walk(JS, f"`longest_prefix_in(\"{TWORD}\", \"{TTEXT}\")` works on \"{JS}\". The `#` stops any match from running past the word.")
TBEST = max(TZ[len(TWORD) + 1:])
tw.steps[-1]["text"] += f" The biggest `z` value after the `#` is {TBEST}: the first {TBEST} letters of \"{TWORD}\" appear in the text."
assert TBEST == longest_prefix_in(TWORD, TTEXT)

# Variation walk: the prefix function.
PS = "abacaba"
pw = Steps(f"`prefix_function(\"{PS}\")`. `pi[i]` is the longest proper prefix of `s[0..i]` that is also a suffix of it.")
pi = [0] * len(PS)
pshow = [0] + [None] * (len(PS) - 1)
pw.step("`pi[0]` is 0: a single letter has no proper prefix that's also a suffix.",
        Row(list(PS), slots=True, label="s"), Row(list(pshow), st={0: "active"}, slots=True, label="pi"), M({"k": 0}))
for i in range(1, len(PS)):
    k = pi[i - 1]
    tried = [k]
    while k > 0 and PS[i] != PS[k]:
        k = pi[k - 1]
        tried.append(k)
    grew = PS[i] == PS[k]
    if grew:
        k += 1
    pi[i] = k
    pshow[i] = k
    if len(tried) > 1:
        how = f"Start from `pi[{i - 1}]` = {tried[0]}. '{PS[i]}' doesn't extend it, so fall back through " + " → ".join(map(str, tried)) + ". "
    else:
        how = f"Start from `pi[{i - 1}]` = {tried[0]}. "
    how += (f"'{PS[i]}' matches `s[{k - 1}]`, so the border grows to {k}: \"{PS[:k]}\"." if grew else f"'{PS[i]}' doesn't match '{PS[k]}', so `pi[{i}]` = 0.")
    pw.step(how, Row(list(PS), st={i: "active", **({k - 1: "mark"} if grew else {})}, ptr={"i": i}, slots=True, label="s"),
            Row(list(pshow), st={i: "active"}, slots=True, label="pi"), M({"k": k}))
assert pi == prefix_function(PS)
P_LEGEND = {"active": "position `i` and its value", "mark": "the letter `s[k - 1]` it matched"}

# Naive search cost on a bad case.
NT, NP = "a" * 30 + "b", "a" * 5 + "b"
NAIVE = sum(min(len(NP), next((k + 1 for k in range(len(NP)) if NT[i + k] != NP[k]), len(NP))) for i in range(len(NT) - len(NP) + 1))
N = 10**5

lesson(
    "strings",
    "pattern-matching",
    """
    Searching a text for a pattern by trying every start position can cost O(n · m). KMP and the Z-function get it
    down to O(n + m) by remembering how much of the pattern has already matched, so no character is compared from
    scratch twice. The same tables also answer questions about a string's own structure: its repeats, borders and
    periods.
    """,
    [
        ("idea", "The idea", [
            f"""
            Look for `{NP}` in `{NT}`. The obvious way tries each start: compare `a`, `a`, `a`, `a`, `a`, then `b`
            against `a`, fail, move one place right, and compare the same `a`s all over again. That's {NAIVE} comparisons
            here, and on texts of length 10⁵ it becomes billions.

            The wasted work is re-reading text you've already matched. After matching five `a`s, you *know* the next
            window starts with four `a`s. A good matcher keeps that knowledge in a table built from the pattern alone,
            so it never steps back in the text.

            Two tables do this job:

            - The Z-function: `z[i]` is how many letters starting at `i` match the start of the string.
            - The prefix function (KMP): `pi[i]` is the length of the longest proper prefix of `s[0..i]` that's also a
              suffix of it (a *border*).

            Both are built in O(n) by reusing what's already known, and both turn "find the pattern in the text" into
            "build a table for `pattern + '#' + text`".
            """,
            fig(Row(list(ZS), slots=True, label="s"), Row([len(ZS)] + z_array(ZS)[1:], slots=True, label="z"),
                caption="z[4] = 7: the 7 letters from index 4 repeat the start of the string."),
            key("""
            Z-function: keep the box `[l, r)`, the rightmost stretch known to match the start. Inside it, start `z[i]` at
            `min(r - i, z[i - l])` and extend. Prefix function: `k = pi[i - 1]`; while `s[i] != s[k]`, fall back to
            `k = pi[k - 1]`; if they match, `k + 1`. Both O(n). For search, run them on `pattern + '#' + text`.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            Exact string search with a guaranteed O(n + m) bound, or questions about how a string overlaps with itself:
            repeating units, borders (prefix = suffix), periods, rotations, the longest prefix that's also a suffix.
            """,
            table(
                ["The problem says…", "use"],
                ["every place the pattern appears in the text", "Z or prefix function on `pattern + '#' + text`"],
                ["the longest prefix of `p` that occurs in `t`", "Z on `p + '#' + t`, the largest value after `#`"],
                ["the longest prefix that's also a suffix", "`pi` of the last position"],
                ["is `s` some block repeated several times?", "the period `n - pi[n - 1]`, if it divides `n`"],
                ["is `b` a rotation of `a`?", "search for `b` in `a + a`"],
                ["for every position, how much matches the start", "the Z-array itself"],
            ),
            """
            Not a fit:

            - Many different patterns against one text. Build a trie or an Aho-Corasick automaton (Tries topic), or hash.
            - Approximate matching (a few typos allowed). That's dynamic programming or more specialised algorithms.
            - One short search where the language's built-in search is fine. Most library searches are fast in
              practice; they just don't promise O(n + m) on every input.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### The Z-box

            While computing `z[1], z[2], …`, keep the stretch `[l, r)` that reaches furthest right among all matches
            found so far. By definition, `s[l..r-1]` is a copy of `s[0..r-l-1]`.

            Now take a position `i` inside that box. Its letters up to `r` are a copy of the letters at `i - l`. So
            whatever `z[i - l]` found is also true at `i`, at least up to the box's edge: `z[i]` is at least
            `min(r - i, z[i - l])`. Start from there and compare only beyond it. If the match runs past `r`, the box
            moves.
            """,
            walk(zw, legend=Z_LEGEND),
            """
            ### Why the Z-function is O(n)

            Each comparison that succeeds while extending past the box pushes `r` one step right, and `r` never moves
            left, so there are at most `n` of those overall. Each position also has at most one failed comparison. So
            the whole array costs O(n), even though there's a `while` loop inside the `for`.

            ### Searching with a separator

            Join the pattern, a character that appears in neither string (`#`), and the text. At a position in the text
            part, `z` measures how much matches the start of the joined string, which is the pattern. The `#` can't
            match anything, so no value goes beyond the pattern's length. `z[i]` equal to the pattern's length means the
            pattern occurs there.

            ### Borders and the prefix function

            A *border* of a string is a proper prefix that's also a suffix: `"aba"` is a border of `"abacaba"`, and so is
            `"a"`. The prefix function stores the longest border of every prefix. The trick that makes it fast: the
            borders of a string are its longest border, the longest border *of that*, and so on. So when the next letter
            doesn't extend the current border `k`, the next candidate is `pi[k - 1]`, not something found by searching
            again.

            Each step adds at most 1 to `k`, and every fallback lowers it, so the total number of fallbacks across the
            whole string is at most `n`. O(n) again.

            ### Periods

            If `s` has a border of length `b`, it also has period `p = n - b`: `s[i] = s[i + p]` everywhere. The longest
            border gives the shortest period. That's why so many "repeating" questions reduce to `pi[n - 1]`.
            """,
        ]),
        ("template", "The template", [
            """
            The Z-array of a string, and one use of it: the longest prefix of `word` that appears anywhere in `text`.
            Both strings are lowercase letters, so `#` is safe as a separator.
            """,
            code(
                "Z-function, and the longest prefix found in a text",
                ZF,
                [
                    ("init", "One value per position, all 0 to start."),
                    ("box", "`[l, r)` is the rightmost stretch known to match the start of the string. Empty for now."),
                    ("each", "Positions 1 onward; `z[0]` is set at the end."),
                    ("reuse", "Inside the box, position `i` mirrors position `i - l`, so its match is at least `z[i - l]` long, "
                              "but only as far as the box is known to go: `r - i`."),
                    ("extend", "Compare onward from what's already known. Every success here pushes past the old box."),
                    ("move", "A match that reaches further right becomes the new box."),
                    ("whole", "By convention `z[0]` is the whole length."),
                    ("join", "Pattern, separator, text. The separator stops any match from running past the word.",
                     {"c": "Build the joined string by hand with `malloc` and `memcpy` (copying the text's `'\\0'` too)."}),
                    ("best", "The largest `z` value in the text part is the longest prefix of `word` found there.",
                     {"c": "Free both buffers before returning."}),
                ],
                ZF_RUN,
                'z_array("aabxaabxaa"); longest_prefix_in("abcab", "xxabcxabca"); ("aab", "baaab"); ("z", "abc")',
            ),
            """
            In `"xxabcxabca"`, `"abc"` appears at index 2 but then a `x` breaks it; at index 6, `"abca"` matches before
            the text ends. So 4 letters of `"abcab"` can be found.
        """,
        ]),
        ("trace", "Trace it by hand", [
            "The second search from the example run, on the joined string:",
            walk(tw, legend=Z_LEGEND),
            """
            On paper, keep three things visible: the string, the `z` row, and the current box drawn as a bracket under
            the string. At each `i`, first write down the free part from the box, then compare onward.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Is one string a rotation of another?

            `"cdeab"` is a rotation of `"abcde"`: cut it after `"ab"` and swap the pieces. Every rotation of `a` appears
            inside `a + a` (`"abcdeabcde"` contains `"cdeab"` at index 2). So: same length, and `b` occurs in `a + a`.
            With Z or KMP that's O(n).

            ### Counting how often each prefix appears

            The Z-array says, for every position, how long a prefix starts there. A prefix of length `L` appears at
            every position with `z[i] ≥ L`. So with one pass over the Z-array (plus a running total from the longest
            lengths down), you can count every prefix's occurrences at once.

            ### Why not just use the language's search?

            Built-in searches like `str.find` or `indexOf` are usually fast, but most don't guarantee linear time. On
            inputs like `{NP}` inside a long run of `a`s, a naive search does about `n · m` comparisons: for
            `n = {N:,}` and `m = 5,000` that's hundreds of millions. When the bound matters, or when you need the
            tables themselves, write Z or KMP.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### The prefix function and every border

            KMP's table, and the list of every border of a string, longest first. Each border is found from the previous
            one with a single table lookup.
            """,
            walk(pw, legend=P_LEGEND),
            code(
                "Prefix function and all borders",
                PI,
                [
                    ("init", "`pi[0] = 0`: one letter has no proper border."),
                    ("each", "Fill the table left to right."),
                    ("start", "The best candidate is the previous border, extended by one letter."),
                    ("fall", "If the next letter doesn't extend border `k`, try the next shorter border, `pi[k - 1]`."),
                    ("grow", "It matches: the border grows by one."),
                    ("store", "The longest border of `s[0..i]`."),
                    ("ret", "The whole table."),
                    ("chain", "Start from the longest border of the whole string.",
                     {"c": "A scratch array for `pi`, freed at the end."}),
                    ("walk", "Each border's own longest border is the next one down."),
                    ("done", "Every border, longest first.", {"c": "C returns how many there are."}),
                ],
                PI_RUN,
                'prefix_function("abacaba"); borders("abacaba"); ("aaaa"); ("abc")',
            ),
            """
            `"abc"` has no border, so its line is empty. `"aaaa"` has three: `"aaa"`, `"aa"` and `"a"`.

            ### KMP search

            To search with the prefix function, either build `pi` for `pattern + '#' + text` and look for values equal to
            the pattern's length, or build `pi` for the pattern alone and walk the text with `k` as "how much of the
            pattern is currently matched", falling back the same way on a mismatch. The second form uses only O(m)
            memory, which matters for a long text or a stream.

            ### Z or KMP?

            They're interchangeable for search. Z is often easier to think about ("how much matches the start
            here?"). KMP fits streams and automata, and its borders answer period questions directly.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Both tables are O(n) time and O(n) space for a string of length `n`. Search with a separator is O(n + m) time
            and space; KMP search with the pattern's table alone needs O(m) extra space.
            """,
            table(
                ["Approach", "Time", "Extra space", "Exact?"],
                ["Try every start", "O(n · m) worst case", "O(1)", "yes"],
                ["Rolling hash (Rabin-Karp)", "O(n + m) expected", "O(1)", "with a check"],
                ["Z-function on p + # + t", "O(n + m)", "O(n + m)", "yes"],
                ["KMP with the pattern's table", "O(n + m)", "O(m)", "yes"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `str.find` and `in` are fast C code, often quicker than a Python-level KMP for one search. Write Z or KMP
            when you need the table itself, or overlapping matches (`str.count` doesn't count overlaps).

            ### Java

            `indexOf` is a simple loop with no linear-time guarantee. Turn strings into `char[]` for tight loops.

            ### C++

            `string::find` has no linear-time guarantee either. `std::boyer_moore_searcher` (C++17) is fast in practice.
            Watch `size_t` versus `int` when you compare `i + z[i] < n`.

            ### C

            `strstr` has no complexity guarantee. Build the joined string yourself, and remember the separator byte and
            the final `'\\0'`.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - A separator that can appear in the strings. Pick something outside the alphabet.
            - Forgetting that `z[0]` is special (it's undefined or `n` by convention, not a real match).
            - In the prefix function, falling back to `pi[k]` instead of `pi[k - 1]`.
            - Taking `n - pi[n - 1]` as the repeating unit without checking that it divides `n`.
            - Counting overlapping matches with a library function that skips overlaps.
            - Empty strings: the arrays are empty, and `pi[n - 1]` doesn't exist.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Inside the Z-box, why is `z[i]` at least `min(r - i, z[i - l])`?",
                 "The box `s[l..r-1]` copies the start of the string, so the letters from `i` up to `r` copy the letters from `i - l`. Whatever matched at `i - l` matches at `i` too, as far as the box goes."),
                ("Why is the Z-function O(n) despite the inner loop?",
                 "Every successful comparison past the box moves `r` right, and `r` never moves back, so there are at most n of them in total."),
                ("What is the prefix function of \"aabaa\"?",
                 "0 1 0 1 2. The last value 2 is the border \"aa\"."),
                ("Why put `#` between the pattern and the text?",
                 "So a match starting in the text can't run on into the pattern or past its end; no z value in the text part can exceed the pattern's length."),
                ("\"abcabcabc\" has longest border \"abcabc\". What's its shortest repeating unit?",
                 "Length 9 - 6 = 3, which divides 9, so \"abc\" repeated three times."),
            ),
        ]),
    ],
)
