"""Lesson: Character mapping (Strings, pattern 6)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

SHAPE = {
    "python": """
        def same_shape(s, t):
            if len(s) != len(t):                            #@len
                return False                                #@len
            to_t, to_s = {}, {}                             #@maps
            for a, b in zip(s, t):                          #@pairs
                if to_t.setdefault(a, b) != b:              #@fwd
                    return False                            #@fwd
                if to_s.setdefault(b, a) != a:              #@back
                    return False                            #@back
            return True                                     #@ret
    """,
    "java": """
        static boolean sameShape(String s, String t) {
            if (s.length() != t.length()) return false;     //@len
            int[] toT = new int[128], toS = new int[128];   //@maps
            Arrays.fill(toT, -1);                           //@maps
            Arrays.fill(toS, -1);                           //@maps
            for (int i = 0; i < s.length(); i++) {          //@pairs
                char a = s.charAt(i), b = t.charAt(i);      //@pairs
                if (toT[a] == -1) toT[a] = b;               //@fwd
                else if (toT[a] != b) return false;         //@fwd
                if (toS[b] == -1) toS[b] = a;               //@back
                else if (toS[b] != a) return false;         //@back
            }
            return true;                                    //@ret
        }
    """,
    "cpp": """
        bool sameShape(const string& s, const string& t) {
            if (s.size() != t.size()) return false;         //@len
            array<int, 128> toT, toS;                       //@maps
            toT.fill(-1);                                   //@maps
            toS.fill(-1);                                   //@maps
            for (size_t i = 0; i < s.size(); i++) {         //@pairs
                int a = s[i], b = t[i];                     //@pairs
                if (toT[a] == -1) toT[a] = b;               //@fwd
                else if (toT[a] != b) return false;         //@fwd
                if (toS[b] == -1) toS[b] = a;               //@back
                else if (toS[b] != a) return false;         //@back
            }
            return true;                                    //@ret
        }
    """,
    "c": """
        bool sameShape(const char* s, const char* t) {
            if (strlen(s) != strlen(t)) return false;       //@len
            int toT[128], toS[128];                         //@maps
            for (int k = 0; k < 128; k++) toT[k] = toS[k] = -1;     //@maps
            for (int i = 0; s[i] != '\\0'; i++) {            //@pairs
                int a = s[i], b = t[i];                     //@pairs
                if (toT[a] == -1) toT[a] = b;               //@fwd
                else if (toT[a] != b) return false;         //@fwd
                if (toS[b] == -1) toS[b] = a;               //@back
                else if (toS[b] != a) return false;         //@back
            }
            return true;                                    //@ret
        }
    """,
}
SHAPE_RUN = {
    "python": """
        for s, t in [("paper", "title"), ("foo", "bar"), ("badc", "baba"), ("ab", "ab"), ("ab", "a")]:
            print(str(same_shape(s, t)).lower())
    """,
    "java": """
        public static void main(String[] args) {
            String[][] tests = {{"paper", "title"}, {"foo", "bar"}, {"badc", "baba"}, {"ab", "ab"}, {"ab", "a"}};
            for (String[] t : tests) System.out.println(sameShape(t[0], t[1]));
        }
    """,
    "cpp": """
        int main() {
            vector<pair<string, string>> tests = {{"paper", "title"}, {"foo", "bar"}, {"badc", "baba"}, {"ab", "ab"}, {"ab", "a"}};
            for (auto& [s, t] : tests) cout << (sameShape(s, t) ? "true" : "false") << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* tests[][2] = {{"paper", "title"}, {"foo", "bar"}, {"badc", "baba"}, {"ab", "ab"}, {"ab", "a"}};
            for (int i = 0; i < 5; i++) printf("%s\\n", sameShape(tests[i][0], tests[i][1]) ? "true" : "false");
            return 0;
        }
    """,
}

INTO = {
    "python": """
        def maps_into(s, t):
            if len(s) != len(t):                            #@len
                return False                                #@len
            to_t = {}                                       #@map
            for a, b in zip(s, t):                          #@pairs
                if to_t.setdefault(a, b) != b:              #@fwd
                    return False                            #@fwd
            return True                                     #@ret
    """,
    "java": """
        static boolean mapsInto(String s, String t) {
            if (s.length() != t.length()) return false;     //@len
            int[] toT = new int[128];                       //@map
            Arrays.fill(toT, -1);                           //@map
            for (int i = 0; i < s.length(); i++) {          //@pairs
                char a = s.charAt(i), b = t.charAt(i);      //@pairs
                if (toT[a] == -1) toT[a] = b;               //@fwd
                else if (toT[a] != b) return false;         //@fwd
            }
            return true;                                    //@ret
        }
    """,
    "cpp": """
        bool mapsInto(const string& s, const string& t) {
            if (s.size() != t.size()) return false;         //@len
            array<int, 128> toT;                            //@map
            toT.fill(-1);                                   //@map
            for (size_t i = 0; i < s.size(); i++) {         //@pairs
                int a = s[i], b = t[i];                     //@pairs
                if (toT[a] == -1) toT[a] = b;               //@fwd
                else if (toT[a] != b) return false;         //@fwd
            }
            return true;                                    //@ret
        }
    """,
    "c": """
        bool mapsInto(const char* s, const char* t) {
            if (strlen(s) != strlen(t)) return false;       //@len
            int toT[128];                                   //@map
            for (int k = 0; k < 128; k++) toT[k] = -1;      //@map
            for (int i = 0; s[i] != '\\0'; i++) {            //@pairs
                int a = s[i], b = t[i];                     //@pairs
                if (toT[a] == -1) toT[a] = b;               //@fwd
                else if (toT[a] != b) return false;         //@fwd
            }
            return true;                                    //@ret
        }
    """,
}
INTO_RUN = {
    "python": """
        for s, t in [("foo", "bar"), ("abc", "xxy"), ("aa", "ab"), ("badc", "baba")]:
            print(str(maps_into(s, t)).lower())
    """,
    "java": """
        public static void main(String[] args) {
            String[][] tests = {{"foo", "bar"}, {"abc", "xxy"}, {"aa", "ab"}, {"badc", "baba"}};
            for (String[] t : tests) System.out.println(mapsInto(t[0], t[1]));
        }
    """,
    "cpp": """
        int main() {
            vector<pair<string, string>> tests = {{"foo", "bar"}, {"abc", "xxy"}, {"aa", "ab"}, {"badc", "baba"}};
            for (auto& [s, t] : tests) cout << (mapsInto(s, t) ? "true" : "false") << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* tests[][2] = {{"foo", "bar"}, {"abc", "xxy"}, {"aa", "ab"}, {"badc", "baba"}};
            for (int i = 0; i < 4; i++) printf("%s\\n", mapsInto(tests[i][0], tests[i][1]) ? "true" : "false");
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

same_shape = py(SHAPE["python"], "same_shape")
maps_into = py(INTO["python"], "maps_into")


def shape(w):
    first = {}
    return [first.setdefault(c, len(first)) for c in w]


for s, t in [("paper", "title"), ("foo", "bar"), ("badc", "baba"), ("ab", "ab"), ("ab", "a"), ("egg", "add"), ("abca", "zbxz")]:
    assert same_shape(s, t) == (len(s) == len(t) and shape(s) == shape(t))
    assert maps_into(s, t) == (len(s) == len(t) and all(t[i] == t[j] for i in range(len(s)) for j in range(len(s)) if s[i] == s[j]))


def map_walk(s, t, title):
    w = Steps(title)
    to_t, to_s = {}, {}

    def panels(i=None, bad=False):
        st_s = {k: "found" for k in range(i if i is not None else 0)}
        st_t = dict(st_s)
        if i is not None:
            st_s[i] = st_t[i] = "mark" if bad else "active"
        return (Row(list(s), st=st_s, slots=True, label="s"), Row(list(t), st=st_t, slots=True, label="t"),
                M({k: v for k, v in to_t.items()} or {"–": "empty"}, "s → t"), M({k: v for k, v in to_s.items()} or {"–": "empty"}, "t → s"))

    w.step("Both maps start empty. Each position pairs a letter of `s` with the letter of `t` below it.", *panels())
    for i, (a, b) in enumerate(zip(s, t)):
        fa, fb = to_t.get(a), to_s.get(b)
        if fa is not None and fa != b:
            w.step(f"Position {i}: '{a}' over '{b}', but '{a}' already stands for '{fa}'. One letter can't stand for two. Not the same shape.",
                   *panels(i, bad=True), result="false")
            return w, False
        if fb is not None and fb != a:
            w.step(f"Position {i}: '{a}' over '{b}'. Going forward '{a}' is new, but '{b}' in `t` already comes from '{fb}' in `s`. "
                   f"Two letters of `s` can't share one letter of `t`. Not the same shape.", *panels(i, bad=True), result="false")
            return w, False
        new = fa is None
        to_t[a], to_s[b] = b, a
        w.step(f"Position {i}: '{a}' over '{b}'. " + (f"New pair: record '{a}' → '{b}' and '{b}' → '{a}'." if new else "This pair was seen before, and it agrees."),
               *panels(i))
    w.steps[-1]["text"] += " Every position agreed with both maps: the same shape."
    w.steps[-1]["result"] = "true"
    return w, True


tw1, ok1 = map_walk("paper", "title", "`same_shape(\"paper\", \"title\")`. One map from `s` to `t` and one from `t` back to `s`.")
assert ok1
A_LEGEND = {"active": "the pair being checked", "found": "checked, consistent"}
tw2, ok2 = map_walk("badc", "baba", "`same_shape(\"badc\", \"baba\")`. The forward map alone wouldn't catch the problem.")
assert not ok2
B_LEGEND = {"active": "the pair being checked", "found": "checked, consistent", "mark": "the pair that breaks a map"}

WORDS = ["moon", "feet", "noon", "abcd", "deed", "loop"]
shape_rows = [(w, " ".join(map(str, shape(w)))) for w in WORDS]
PATTERN_OF = shape("moon")
MATCHES = [w for w in WORDS if shape(w) == PATTERN_OF]

KEY = "the quick brown fox jumps over lazy dog"
cipher = {}
for ch in KEY:
    if ch != " " and ch not in cipher:
        cipher[ch] = chr(ord("a") + len(cipher))
assert len(cipher) == 26
SECRET = "vkbs bs t suepuv"
DECODED = "".join(cipher.get(c, c) for c in SECRET)

KINDS = [
    ("`s` letters to `t` letters, one-to-one", "two maps (or a map and a set of used targets)", "same shape: \"paper\" / \"title\""),
    ("`s` letters to `t` letters, many-to-one allowed", "one map, `s` to `t`", "\"abc\" can become \"xxy\""),
    ("letters to whole words, one-to-one", "two maps: letter to word, word to letter", "\"abba\" / \"dog cat cat dog\""),
    ("a fixed substitution you're given", "one lookup table, built once", "decoding with a key"),
]

lesson(
    "strings",
    "char-mapping",
    """
    Some questions ask whether one string can be turned into another by consistently replacing letters: every `a`
    becomes the same thing, every time. Walk the two strings side by side, record each letter's partner in a map, and
    stop at the first pair that contradicts what's already recorded. When the replacement has to be one-to-one, keep a
    second map going the other way.
    """,
    [
        ("idea", "The idea", [
            """
            Picture two seating charts for the same dinner, one written with guests' first names and one with initials
            someone made up. If the same person always gets the same initials, and no two people share initials, the
            charts describe the same seating. To check, read them side by side, seat by seat, and keep a list: "Ana is
            AK, Ben is BJ…". The moment Ana shows up as somebody else, or AK shows up for someone who isn't Ana, the
            charts disagree.

            Strings work the same way. `"paper"` and `"title"` have the same *shape*: p→t, a→i, e→l, r→e, and the second
            p is a t again. `"foo"` and `"bar"` don't: the two o's would have to become both a and r.
            """,
            fig(Row(list("paper"), slots=True, label="s"), Row(list("title"), slots=True, label="t"),
                M({"p": "t", "a": "i", "e": "l", "r": "e"}, "s → t"),
                caption="Each letter of s always sits over the same letter of t, and no two letters of s share one."),
            key("""
            Walk both strings together. For each pair `(a, b)`: if `a` already maps to something other than `b`, fail; if
            `b` is already the image of something other than `a`, fail (only when the mapping must be one-to-one).
            Otherwise record the pair. O(n) time, space bounded by the alphabet.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            "Isomorphic", "follows the pattern", "consistent replacement", "cipher", "substitution", "rename every letter".
            The two sequences have the same length (or the same number of words), and the question is whether position
            `i` in one can be explained by a fixed rule from position `i` in the other.
            """,
            table(["what's being mapped", "what to keep", "example"], *KINDS),
            """
            Not a fit:

            - The mapping can change over time (repaint every `x` as `y`, then later every `y` as `z`). That's a question
              about chains and cycles of replacements, closer to a graph problem.
            - Order doesn't matter, only counts (anagrams). Use a signature.
            - Close but not exact matches (spelling suggestions). That's edit distance.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### A function, checked as you go

            "Replace letters consistently" means there's a function `f` from letters of `s` to letters of `t` with
            `f(s[i]) = t[i]` at every position. A function is only defined by the pairs it's forced to have, so walk the
            positions and record `f(s[i]) = t[i]` the first time `s[i]` appears. Every later appearance must agree. If all
            positions agree, the recorded pairs *are* such a function; if one disagrees, no function can satisfy both
            positions.

            ### One-to-one needs the other direction too

            "Different letters must stay different" means `f` must never send two letters to the same place. The forward
            map can't see that: in `"badc"` and `"baba"`, b→b, a→a, d→b, c→a is a perfectly good function, but b and d
            both land on b. Keeping a second map from `t` back to `s` catches it the moment it happens.
            """,
            walk(tw2, legend=B_LEGEND),
            """
            ### The shape code

            Another way to see the same thing: replace every letter by the order in which it first appeared. `"paper"`
            becomes 0 1 0 2 3, and so does `"title"`. Two strings have the same shape exactly when their codes match,
            which turns the question into comparing (or hashing) the codes. That's handy for grouping many words by
            shape at once.

            ### Space

            With an alphabet of size σ, each map needs at most σ entries, and fixed-size arrays (128 for ASCII) beat hash
            maps. With words instead of letters, use hash maps.
            """,
        ]),
        ("template", "The template", [
            """
            Do `s` and `t` have the same shape? That is, can each letter of `s` be replaced by a letter of `t`,
            consistently and one-to-one, to turn `s` into `t`? Characters are ASCII.
            """,
            code(
                "Same shape (isomorphic strings)",
                SHAPE,
                [
                    ("len", "Different lengths can't line up position by position."),
                    ("maps", "What each letter of `s` has become, and what each letter of `t` came from. Nothing yet.",
                     {"java": "-1 means \"no partner yet\"; character codes are 0 to 127.",
                      "cpp": "-1 means \"no partner yet\"; character codes are 0 to 127.",
                      "c": "-1 means \"no partner yet\"; character codes are 0 to 127."}),
                    ("pairs", "Walk both strings together."),
                    ("fwd", "The first time `a` appears, record its partner. After that, it must be the same partner.",
                     {"python": "`setdefault` stores `b` only if `a` is new, and returns whatever is stored."}),
                    ("back", "The same check from `t`'s side: `b` must always come from the same letter. This is what makes "
                             "the mapping one-to-one."),
                    ("ret", "Every position agreed with both maps."),
                ],
                SHAPE_RUN,
                'same_shape("paper", "title"); ("foo", "bar"); ("badc", "baba"); ("ab", "ab"); ("ab", "a")',
            ),
        ]),
        ("trace", "Trace it by hand", [
            "The first example, which passes:",
            walk(tw1, legend=A_LEGEND),
            """
            On paper, draw two columns, `s → t` and `t → s`. Each new pair adds a line to both. Before adding, look the
            letter up in its column; a different partner already written there is your answer.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Grouping words by shape

            Which of `{WORDS}` have the same shape as `moon`? Work out each word's shape code once:
            """,
            table(["word", "shape code"], *shape_rows),
            f"""
            `moon` is 0 1 1 2, so the matches are {', '.join(MATCHES)}. With many words, put the codes in a hash map
            (see *Group by key*) instead of comparing pairs.

            ### Letters to words

            The same check works when one side is letters and the other is whole words: `"abba"` against
            `"dog cat cat dog"`. Split the sentence into words, check the counts match, then run the two maps with
            words as the values. Hash maps replace the fixed arrays.

            ### Decoding with a key

            A substitution key like `"{KEY}"` defines a cipher: the first new letter in the key stands for `a`, the next
            new one for `b`, and so on. Build the table once by walking the key and skipping letters you've already
            assigned, then decode by looking each letter up: `"{SECRET}"` reads `"{DECODED}"`. Building the table is the
            same first-appearance bookkeeping as the shape code.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Many-to-one allowed

            Sometimes different letters *may* merge: "can `s` be turned into `t` by replacing each letter with some
            letter, the same one every time?". Then only the forward check matters. `"abc"` can become `"xxy"` (a and b
            both become x), but `"aa"` can't become `"ab"`.
            """,
            code(
                "Can s be mapped onto t (merging allowed)?",
                INTO,
                [
                    ("len", "Lengths must match."),
                    ("map", "Only the forward map."),
                    ("pairs", "Walk both strings together."),
                    ("fwd", "Each letter of `s` must always become the same letter of `t`."),
                    ("ret", "A consistent function exists."),
                ],
                INTO_RUN,
                'maps_into("foo", "bar"); ("abc", "xxy"); ("aa", "ab"); ("badc", "baba")',
            ),
            """
            `"badc"` → `"baba"` passes here: merging b and d into b is allowed. That's exactly the case the backward map
            exists to reject.

            ### A set instead of the second map

            For one-to-one, the backward map can be replaced by a set of letters already used as targets: when `a` is new,
            its target `b` must not be in the set yet. It catches the same cases.

            ### Mapping both ways at once

            When either string may be rewritten, ask whether both reduce to the same shape code. That's symmetric and
            avoids deciding which direction the mapping goes.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            One pass over `n` positions with O(1) work each: O(n) time. Space is O(σ) for alphabet size σ, which is
            constant for ASCII. With words instead of letters, it's O(total length of the words) for hashing them.
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Try every possible mapping", "exponential", "O(σ)"],
                ["Compare every pair of positions", "O(n²)", "O(1)"],
                ["Two maps, one pass", "O(n)", "O(σ)"],
                ["Shape codes, then compare", "O(n)", "O(n) for the codes"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `dict.setdefault(a, b)` stores and returns in one call. `zip(s, t)` pairs positions (and silently stops at the
            shorter one, so check lengths first). For the shape code, `[first.setdefault(c, len(first)) for c in w]`.

            ### Java

            `int[128]` filled with -1 via `Arrays.fill`. With words, `HashMap<String, String>` and `equals`, never `==`,
            to compare strings.

            ### C++

            `array<int, 128>` with `fill(-1)`. Store characters as `int` (or `unsigned char`) so a non-ASCII byte doesn't
            index with a negative number. `unordered_map<string, string>` for words.

            ### C

            `int map[128]` initialised in a loop (`memset` with -1 also works, since every byte becomes 0xFF). Check
            `strlen` of both before the loop.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Checking only one direction when the mapping must be one-to-one.
            - Checking only that each letter maps consistently, but forgetting the lengths.
            - Comparing words with `==` in Java.
            - Indexing an array with a `char` that can be negative (bytes above 127 in C and C++).
            - Treating matching letter counts as the same shape. `"aab"` and `"abb"` both have one letter twice and one
              once, but their shape codes are 0 0 1 and 0 1 1. Compare positions, not counts.
            - Empty strings: two empty strings have the same shape.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why isn't a map from `s` to `t` enough for \"same shape\"?",
                 "It checks that each letter of s always becomes the same letter, but not that different letters stay different. Two letters of s could both become the same letter of t."),
                ("Do \"egg\" and \"add\" have the same shape? \"egg\" and \"adb\"?",
                 "\"egg\" and \"add\": yes, e→a, g→d. \"egg\" and \"adb\": no, the two g's would have to become both d and b."),
                ("What's the shape code of \"banana\"?",
                 "0 1 2 1 2 1: b first, then a, then n, repeating."),
                ("maps_into(\"abc\", \"zzz\"): true or false?",
                 "True. Merging is allowed, so a, b and c can all become z."),
                ("How much memory do the two maps need for ASCII strings of length 10⁶?",
                 "Two arrays of 128 entries. The size depends on the alphabet, not the length."),
            ),
        ]),
    ],
)
