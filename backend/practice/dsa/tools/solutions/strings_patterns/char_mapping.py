"""Strings: mapping characters one to one."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def crack_the_cipher():
    plain, coded, message = "the cab", "xli gef", "fex lev"
    back = {}
    for p, c in zip(plain, coded):
        if c != " ":
            back[c] = p
    want = "".join(" " if c == " " else back.get(c, "?") for c in message)

    w1 = Steps("For each message letter, search the coded sentence for that letter and read the plain letter at the same spot.")
    for k, c in enumerate(message):
        if c == " ":
            continue
        at = coded.find(c)
        w1.step(f"'{c}': " + (f"found at position {at} of the coded sentence; the plain letter there is '{plain[at]}'." if at >= 0 else "never appears in the coded sentence: '?'."), Row(list(coded), st={at: "found"} if at >= 0 else None, label="coded"), Row(list(plain), st={at: "found"} if at >= 0 else None, label="plain"))
    w1.step(f"Decoded: '{want}'.", result=want)

    w2 = Steps("Build the decoding table once: coded letter → plain letter. Then translate the message letter by letter.")
    w2.step("Table from the sample: " + ", ".join(f"{c}→{p}" for c, p in sorted(back.items())) + ".", Row(list(coded), label="coded"), Row(list(plain), label="plain"))
    w2.step(f"{len(back)} coded letters are known (not 25, so no letter can be deduced). Translate, writing '?' for unknown letters: '{want}'.", Row(list(message), label="message"), Row(list(want), label="decoded"), result=want)

    sol(
        "crack-the-cipher",
        summary="""
            Read the sample pair once to build a 26-entry table `coded letter → plain letter`. If exactly 25 coded letters
            are known, the missing one must map to the only plain letter not yet used. Then decode the message through the
            table, writing `?` for unknown letters. O(n + m).
        """,
        question=[
            """
            The cipher is a one-to-one letter substitution; spaces stay. From one sample sentence in both forms, decode a new
            message: known letters are translated, unknown ones become `?`.

            - **The 25-letter rule:** knowing 25 pairs pins down the 26th, since each plain letter is used exactly once.
            - **Up to 10⁵ characters** in each string.
            """
        ],
        think=[
            f"""
            Sample `"{plain}"` ↔ `"{coded}"`, message `"{message}"` → `"{want}"`.

            Every coded letter in the sample tells us its plain letter, and that never changes. So one pass builds the full
            decoding table, and the message is translated with lookups. The deduction rule only applies when 25 coded
            letters are known: the 26th coded letter has to be the remaining plain letter.
            """,
            fig(Row(list(coded), label="coded"), Row(list(plain), label="plain")),
        ],
        approaches=[
            approach(
                "Search the sample for every letter",
                "brute",
                "O(m · n)",
                "O(1)",
                idea=["For each message letter, find it in `coded` and output the `plain` letter at that position. Handle the 25-letter rule with an extra count of distinct coded letters."],
                walk=w1,
                build=["Count the distinct coded letters (for the deduction rule).", "For each message letter, search `coded`.", "Output the plain letter, or the deduced one, or `?`."],
                code={
                    "python": """
                        class Solution:
                            def crackCipher(self, plain: str, coded: str, message: str) -> str:
                                letters = "abcdefghijklmnopqrstuvwxyz"  #@rule
                                known = set(coded) - {" "}  #@rule
                                spare_c = spare_p = None  #@rule
                                if len(known) == 25:  #@rule
                                    spare_c = next(x for x in letters if x not in known)  #@rule
                                    spare_p = next(x for x in letters if x not in set(plain))  #@rule
                                out = []  #@each
                                for c in message:  #@each
                                    at = coded.find(c)  #@find
                                    if c == " ":  #@emit
                                        out.append(" ")  #@emit
                                    elif at >= 0:  #@emit
                                        out.append(plain[at])  #@emit
                                    else:  #@emit
                                        out.append(spare_p if c == spare_c else "?")  #@emit
                                return "".join(out)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String crackCipher(String plain, String coded, String message) {
                                boolean[] seenC = new boolean[26], seenP = new boolean[26];  //@rule
                                int known = 0;  //@rule
                                for (int i = 0; i < coded.length(); i++) {  //@rule
                                    char c = coded.charAt(i);  //@rule
                                    if (c == ' ') continue;  //@rule
                                    if (!seenC[c - 'a']) { seenC[c - 'a'] = true; known++; }  //@rule
                                    seenP[plain.charAt(i) - 'a'] = true;  //@rule
                                }
                                char spareC = 0, spareP = 0;  //@rule
                                if (known == 25)  //@rule
                                    for (int x = 0; x < 26; x++) { if (!seenC[x]) spareC = (char) ('a' + x); if (!seenP[x]) spareP = (char) ('a' + x); }  //@rule
                                StringBuilder out = new StringBuilder();  //@each
                                for (char c : message.toCharArray()) {  //@each
                                    int at = coded.indexOf(c);  //@find
                                    if (c == ' ') out.append(' ');  //@emit
                                    else if (at >= 0) out.append(plain.charAt(at));  //@emit
                                    else out.append(c == spareC ? spareP : '?');  //@emit
                                }
                                return out.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string crackCipher(string& plain, string& coded, string& message) {
                                bool seenC[26] = {}, seenP[26] = {};  //@rule
                                int known = 0;  //@rule
                                for (size_t i = 0; i < coded.size(); i++) {  //@rule
                                    if (coded[i] == ' ') continue;  //@rule
                                    if (!seenC[coded[i] - 'a']) { seenC[coded[i] - 'a'] = true; known++; }  //@rule
                                    seenP[plain[i] - 'a'] = true;  //@rule
                                }
                                char spareC = 0, spareP = 0;  //@rule
                                if (known == 25)  //@rule
                                    for (int x = 0; x < 26; x++) { if (!seenC[x]) spareC = 'a' + x; if (!seenP[x]) spareP = 'a' + x; }  //@rule
                                string out;  //@each
                                for (char c : message) {  //@each
                                    size_t at = coded.find(c);  //@find
                                    if (c == ' ') out += ' ';  //@emit
                                    else if (at != string::npos) out += plain[at];  //@emit
                                    else out += c == spareC ? spareP : '?';  //@emit
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* crackCipher(char* plain, char* coded, char* message) {
                            int seenC[26] = {0}, seenP[26] = {0}, known = 0;  //@rule
                            for (int i = 0; coded[i]; i++) {  //@rule
                                if (coded[i] == ' ') continue;  //@rule
                                if (!seenC[coded[i] - 'a']) { seenC[coded[i] - 'a'] = 1; known++; }  //@rule
                                seenP[plain[i] - 'a'] = 1;  //@rule
                            }
                            char spareC = 0, spareP = 0;  //@rule
                            if (known == 25)  //@rule
                                for (int x = 0; x < 26; x++) { if (!seenC[x]) spareC = 'a' + x; if (!seenP[x]) spareP = 'a' + x; }  //@rule
                            int m = strlen(message);  //@each
                            char* out = malloc(m + 1);  //@each
                            for (int k = 0; k < m; k++) {  //@each
                                char c = message[k];  //@each
                                char* at = strchr(coded, c);  //@find
                                if (c == ' ') out[k] = ' ';  //@emit
                                else if (at) out[k] = plain[at - coded];  //@emit
                                else out[k] = c == spareC ? spareP : '?';  //@emit
                            }
                            out[m] = '\\0';  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("rule", "Which coded and plain letters appear in the sample; with exactly 25 coded letters known, the unseen coded letter maps to the unseen plain letter."), ("each", "Build the output letter by letter."), ("find", "Search the whole coded sentence for this letter: O(n) each time."), ("emit", "Space stays a space; a found letter gives its plain partner; otherwise the deduced letter or `?`."), ("ret", "The decoded message.")],
                complexity=["**Time O(m · n):** a search of the sample per message letter, up to 10¹⁰. **Space O(1)** besides the output."],
                limits=["The same letter is searched for again and again. A 26-entry table built in one pass answers each lookup in O(1)."],
                slow=True,
            ),
            approach(
                "Decoding table",
                "best",
                "O(n + m)",
                "O(1)",
                idea=["`back[c] = p` for every non-space pair in the sample. If 25 entries are filled, set the empty one to the unused plain letter. Translate the message through `back`."],
                walk=w2,
                build=["Fill the 26-entry table from the sample.", "Apply the 25-letter rule.", "Translate."],
                code={
                    "python": """
                        class Solution:
                            def crackCipher(self, plain: str, coded: str, message: str) -> str:
                                back = {}  #@table
                                for p, c in zip(plain, coded):  #@table
                                    if c != " ":  #@table
                                        back[c] = p  #@table
                                if len(back) == 25:  #@rule
                                    letters = "abcdefghijklmnopqrstuvwxyz"  #@rule
                                    missing = next(x for x in letters if x not in back)  #@rule
                                    used = set(back.values())  #@rule
                                    back[missing] = next(x for x in letters if x not in used)  #@rule
                                back[" "] = " "  #@ret
                                return "".join(back.get(c, "?") for c in message)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String crackCipher(String plain, String coded, String message) {
                                char[] back = new char[26];  //@table
                                boolean[] used = new boolean[26];  //@table
                                int known = 0;  //@table
                                for (int i = 0; i < coded.length(); i++) {  //@table
                                    char c = coded.charAt(i);  //@table
                                    if (c == ' ') continue;  //@table
                                    if (back[c - 'a'] == 0) known++;  //@table
                                    back[c - 'a'] = plain.charAt(i);  //@table
                                    used[plain.charAt(i) - 'a'] = true;  //@table
                                }
                                if (known == 25) {  //@rule
                                    int spare = 0;  //@rule
                                    while (used[spare]) spare++;  //@rule
                                    for (int x = 0; x < 26; x++) if (back[x] == 0) back[x] = (char) ('a' + spare);  //@rule
                                }
                                StringBuilder out = new StringBuilder();  //@ret
                                for (char c : message.toCharArray()) out.append(c == ' ' ? ' ' : (back[c - 'a'] != 0 ? back[c - 'a'] : '?'));  //@ret
                                return out.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string crackCipher(string& plain, string& coded, string& message) {
                                char back[26] = {};  //@table
                                bool used[26] = {};  //@table
                                int known = 0;  //@table
                                for (size_t i = 0; i < coded.size(); i++) {  //@table
                                    if (coded[i] == ' ') continue;  //@table
                                    if (!back[coded[i] - 'a']) known++;  //@table
                                    back[coded[i] - 'a'] = plain[i];  //@table
                                    used[plain[i] - 'a'] = true;  //@table
                                }
                                if (known == 25) {  //@rule
                                    int spare = 0;  //@rule
                                    while (used[spare]) spare++;  //@rule
                                    for (int x = 0; x < 26; x++) if (!back[x]) back[x] = 'a' + spare;  //@rule
                                }
                                string out;  //@ret
                                for (char c : message) out += c == ' ' ? ' ' : (back[c - 'a'] ? back[c - 'a'] : '?');  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* crackCipher(char* plain, char* coded, char* message) {
                            char back[26] = {0};  //@table
                            int used[26] = {0}, known = 0;  //@table
                            for (int i = 0; coded[i]; i++) {  //@table
                                if (coded[i] == ' ') continue;  //@table
                                if (!back[coded[i] - 'a']) known++;  //@table
                                back[coded[i] - 'a'] = plain[i];  //@table
                                used[plain[i] - 'a'] = 1;  //@table
                            }
                            if (known == 25) {  //@rule
                                int spare = 0;  //@rule
                                while (used[spare]) spare++;  //@rule
                                for (int x = 0; x < 26; x++) if (!back[x]) back[x] = 'a' + spare;  //@rule
                            }
                            int m = strlen(message);  //@ret
                            char* out = malloc(m + 1);  //@ret
                            for (int k = 0; k < m; k++) out[k] = message[k] == ' ' ? ' ' : (back[message[k] - 'a'] ? back[message[k] - 'a'] : '?');  //@ret
                            out[m] = '\\0';  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("table", "One pass over the sample: each coded letter's plain partner, and which plain letters are taken."), ("rule", "With 25 coded letters known, the one unknown coded letter must map to the one unused plain letter."), ("ret", "Translate: spaces stay, known letters convert, unknown ones become `?`.")],
                complexity=["**Time O(n + m).** **Space O(1):** two 26-entry tables."],
            ),
        ],
        takeaways=[
            """
            - **One-to-one substitutions = a lookup table** built in one pass.
            - Bijection logic lets you deduce the last pair when all but one are known.
            - Prefer a 26-slot array over a hash map for lowercase letters.
            """
        ],
    )


@problem
def repaint_the_letters():
    s, t, m = "abca", "bbcb", 3
    w = Steps("Each colour in s must become exactly one colour in t. Then we need one spare colour to break cycles like a→b→a.")
    paint = {}
    ok = True
    for i, (x, y) in enumerate(zip(s, t)):
        if paint.setdefault(x, y) != y:
            ok = False
        w.step(f"Tile {i}: '{x}' must become '{y}'." + ("" if paint[x] == y else f" But '{x}' already has to become '{paint[x]}': impossible."), Row(list(s), st={i: "active"}, label="s"), Row(list(t), st={i: "active"}, label="t"), Vars(**{k: v for k, v in sorted(paint.items())}))
        if not ok:
            break
    used = len(set(t))
    want = s == t or (ok and used < m)
    w.step(f"The target uses {used} of the {m} colours, so {'a spare colour exists' if used < m else 'no colour is spare'}: {str(want).lower()}.", result=str(want).lower())

    sol(
        "repaint-the-letters",
        summary="""
            A repaint changes all tiles of one colour together, so tiles that share a colour in `s` must share a colour in
            `t`: the map `s-colour → t-colour` must be consistent. If it is, the recolouring can always be carried out, as
            long as at least one colour is unused in `t` to act as a temporary colour (cycles like a → b, b → a need it).
            If `s == t`, no steps are needed. O(n).
        """,
        question=[
            """
            One step repaints **every** tile of colour `x` with colour `y`. Can `s` be turned into `t` with `m` colours
            available?

            - **Repaints are all-or-nothing:** two tiles with the same colour can never be separated.
            - **Swapping two colours** needs a third, temporary colour.
            """
        ],
        think=[
            f"""
            `s = "{s}"`, `t = "{t}"`, m = {m}: **{str(want).lower()}**.

            First requirement: same colour in `s` ⇒ same colour in `t`, because tiles of one colour are always repainted
            together. That's a function from `s`-colours to `t`-colours.

            Is a consistent function always achievable? Merging colours (a → b when b → b) is easy. The trouble is cycles,
            like a → b and b → a: repainting a first destroys the a/b distinction. A free colour fixes it: a → spare, b → a,
            spare → b. A colour is free exactly when `t` doesn't use all `m` colours. If `t` uses all `m` colours, the
            function is a permutation of all colours, and any real change is impossible without a free colour.
            """,
            fig(Row(list(s), label="s"), Row(list(t), label="t")),
        ],
        approaches=[
            approach(
                "Consistent mapping plus a spare colour",
                "best",
                "O(n)",
                "O(1)",
                idea=["If `s == t`, true. Otherwise build `paint[x] = y` for each tile; any conflict means false. Finally require that `t` uses fewer than `m` distinct colours."],
                walk=w,
                build=["Equal strings need nothing.", "Check the colour mapping is a function.", "Check for a spare colour."],
                code={
                    "python": """
                        class Solution:
                            def canRepaint(self, s: str, t: str, m: int) -> bool:
                                if s == t:  #@same
                                    return True  #@same
                                paint = {}  #@map
                                for x, y in zip(s, t):  #@map
                                    if paint.setdefault(x, y) != y:  #@map
                                        return False  #@map
                                return len(set(t)) < m  #@spare
                    """,
                    "java": """
                        class Solution {
                            public boolean canRepaint(String s, String t, int m) {
                                if (s.equals(t)) return true;  //@same
                                int[] paint = new int[26];  //@map
                                Arrays.fill(paint, -1);  //@map
                                for (int i = 0; i < s.length(); i++) {  //@map
                                    int x = s.charAt(i) - 'a', y = t.charAt(i) - 'a';  //@map
                                    if (paint[x] == -1) paint[x] = y;  //@map
                                    else if (paint[x] != y) return false;  //@map
                                }
                                boolean[] used = new boolean[26];  //@spare
                                int distinct = 0;  //@spare
                                for (char c : t.toCharArray()) if (!used[c - 'a']) { used[c - 'a'] = true; distinct++; }  //@spare
                                return distinct < m;  //@spare
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool canRepaint(string& s, string& t, int m) {
                                if (s == t) return true;  //@same
                                int paint[26];  //@map
                                fill(paint, paint + 26, -1);  //@map
                                for (size_t i = 0; i < s.size(); i++) {  //@map
                                    int x = s[i] - 'a', y = t[i] - 'a';  //@map
                                    if (paint[x] == -1) paint[x] = y;  //@map
                                    else if (paint[x] != y) return false;  //@map
                                }
                                set<char> used(t.begin(), t.end());  //@spare
                                return (int) used.size() < m;  //@spare
                            }
                        };
                    """,
                    "c": """
                        bool canRepaint(char* s, char* t, int m) {
                            if (strcmp(s, t) == 0) return true;  //@same
                            int paint[26];  //@map
                            for (int x = 0; x < 26; x++) paint[x] = -1;  //@map
                            for (int i = 0; s[i]; i++) {  //@map
                                int x = s[i] - 'a', y = t[i] - 'a';  //@map
                                if (paint[x] == -1) paint[x] = y;  //@map
                                else if (paint[x] != y) return false;  //@map
                            }
                            int used[26] = {0}, distinct = 0;  //@spare
                            for (int i = 0; t[i]; i++) if (!used[t[i] - 'a']) { used[t[i] - 'a'] = 1; distinct++; }  //@spare
                            return distinct < m;  //@spare
                        }
                    """,
                },
                lines=[("same", "Nothing to do."), ("map", "Every tile of colour `x` must end with the same colour: a second, different target for `x` makes it impossible."), ("spare", "Some change is needed, and changes involving cycles need a temporary colour: one must be unused by `t`.")],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Global replacements** (all copies at once) require a consistent many-to-one map.
            - Swapping two labels needs a free third label; check whether one exists.
            - Handle "already equal" first: it needs zero operations even without a free label.
            """
        ],
    )


@problem
def rhythm_of_words():
    pattern, sentence = "abca", "sun moon star sun"
    words = sentence.split(" ")
    want = len(words) == len(pattern) and len(set(zip(pattern, words))) == len(set(pattern)) == len(set(words))

    w1 = Steps("Compare every pair of positions: the letters must be equal exactly when the words are equal.")
    pairs = [(i, j) for i in range(len(pattern)) for j in range(i + 1, len(pattern))]
    for i, j in pairs[:6]:
        same_l, same_w = pattern[i] == pattern[j], words[i] == words[j]
        w1.step(f"Positions {i} and {j}: letters {'equal' if same_l else 'different'}, words {'equal' if same_w else 'different'}{' ✓' if same_l == same_w else ' ✗'}.", Row(list(pattern), st={i: "active", j: "active"}, label="pattern"), Row(words, st={i: "active", j: "active"}, label="words"))
    w1.step(f"Every pair agrees: {str(want).lower()}.", result=str(want).lower())

    w2 = Steps("Two dictionaries: letter → word and word → letter. Each pair must agree with both.")
    to_word, to_letter = {}, {}
    for i, (p, w_) in enumerate(zip(pattern, words)):
        to_word.setdefault(p, w_)
        to_letter.setdefault(w_, p)
        w2.step(f"'{p}' ↔ '{w_}': consistent with both maps.", Row(list(pattern), st={i: "active"}, label="pattern"), Row(words, st={i: "active"}, label="words"), Vars(**{f"{k}→": v for k, v in to_word.items()}))
    w2.step(f"Follows the rhythm: {str(want).lower()}.", result=str(want).lower())

    sol(
        "rhythm-of-words",
        summary="""
            Split the sentence into words; the counts must match. Then the letter ↔ word correspondence must be one-to-one
            in **both** directions: keep a map letter → word and a map word → letter, and reject any pair that contradicts
            either. O(total length).
        """,
        question=[
            """
            Does `sentence` follow `pattern`: one word per letter, same letter ↔ same word, different letters ↔ different
            words?

            - **Both directions matter:** `"abba"` vs `"sun sun sun sun"` fails because a and b map to the same word.
            - **Word count must equal pattern length.**
            """
        ],
        think=[
            f"""
            Pattern `"{pattern}"`, sentence `"{sentence}"`: a ↔ sun, b ↔ moon, c ↔ star, and the last `a` is `sun` again.
            **{str(want).lower()}**.

            One map from letters to words catches "same letter, different words". It doesn't catch "different letters, same
            word"; that needs the reverse map too. Together they check a bijection.
            """,
            fig(Row(list(pattern), label="pattern"), Row(words, label="words")),
        ],
        approaches=[
            approach(
                "Compare every pair of positions",
                "brute",
                "O(n² · L)",
                "O(n)",
                idea=["For all `i < j`: `pattern[i] == pattern[j]` must hold exactly when `words[i] == words[j]`."],
                walk=w1,
                build=["Split; compare counts.", "Check every pair of positions."],
                code={
                    "python": """
                        class Solution:
                            def followsRhythm(self, pattern: str, sentence: str) -> bool:
                                words = sentence.split(" ")  #@split
                                if len(words) != len(pattern):  #@split
                                    return False  #@split
                                for i in range(len(words)):  #@pairs
                                    for j in range(i + 1, len(words)):  #@pairs
                                        if (pattern[i] == pattern[j]) != (words[i] == words[j]):  #@pairs
                                            return False  #@pairs
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean followsRhythm(String pattern, String sentence) {
                                String[] words = sentence.split(" ");  //@split
                                if (words.length != pattern.length()) return false;  //@split
                                for (int i = 0; i < words.length; i++)  //@pairs
                                    for (int j = i + 1; j < words.length; j++)  //@pairs
                                        if ((pattern.charAt(i) == pattern.charAt(j)) != words[i].equals(words[j])) return false;  //@pairs
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool followsRhythm(string& pattern, string& sentence) {
                                vector<string> words;  //@split
                                stringstream in(sentence);  //@split
                                for (string w; in >> w;) words.push_back(w);  //@split
                                if (words.size() != pattern.size()) return false;  //@split
                                for (size_t i = 0; i < words.size(); i++)  //@pairs
                                    for (size_t j = i + 1; j < words.size(); j++)  //@pairs
                                        if ((pattern[i] == pattern[j]) != (words[i] == words[j])) return false;  //@pairs
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool followsRhythm(char* pattern, char* sentence) {
                            int n = strlen(pattern), count = 0;  //@split
                            char* copy = malloc(strlen(sentence) + 1);  //@split
                            strcpy(copy, sentence);  //@split
                            char** words = malloc((strlen(sentence) / 2 + 2) * sizeof(char*));  //@split
                            for (char* w = strtok(copy, " "); w; w = strtok(NULL, " ")) words[count++] = w;  //@split
                            bool ok = count == n;  //@split
                            for (int i = 0; i < n && ok; i++)  //@pairs
                                for (int j = i + 1; j < n && ok; j++)  //@pairs
                                    if ((pattern[i] == pattern[j]) != (strcmp(words[i], words[j]) == 0)) ok = false;  //@pairs
                            free(words); free(copy);  //@ret
                            return ok;  //@ret
                        }
                    """,
                },
                lines=[("split", "One word per pattern letter, or it fails immediately.", {"c": "`strtok` cuts a copy of the sentence at spaces."}), ("pairs", "Equal letters must mean equal words and vice versa."), ("ret", "Every pair agreed.")],
                complexity=["**Time O(n² · L)** for n words of length L. **Space O(n).**"],
                limits=["Compares every pair (45,000 pairs for 300 words). Two maps check each position once."],
            ),
            approach(
                "Two maps",
                "best",
                "O(n · L)",
                "O(n · L)",
                idea=["Walk letters and words together. `to_word[letter]` and `to_letter[word]` must each be unset or equal to the current partner."],
                walk=w2,
                build=["Split; compare counts.", "Check and record both directions.", "True if no conflict."],
                code={
                    "python": """
                        class Solution:
                            def followsRhythm(self, pattern: str, sentence: str) -> bool:
                                words = sentence.split(" ")  #@split
                                if len(words) != len(pattern):  #@split
                                    return False  #@split
                                to_word, to_letter = {}, {}  #@maps
                                for p, w in zip(pattern, words):  #@check
                                    if to_word.setdefault(p, w) != w or to_letter.setdefault(w, p) != p:  #@check
                                        return False  #@check
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean followsRhythm(String pattern, String sentence) {
                                String[] words = sentence.split(" ");  //@split
                                if (words.length != pattern.length()) return false;  //@split
                                Map<Character, String> toWord = new HashMap<>();  //@maps
                                Map<String, Character> toLetter = new HashMap<>();  //@maps
                                for (int i = 0; i < words.length; i++) {  //@check
                                    char p = pattern.charAt(i);  //@check
                                    String w = words[i];  //@check
                                    if (!toWord.computeIfAbsent(p, k -> w).equals(w)) return false;  //@check
                                    if (toLetter.computeIfAbsent(w, k -> p) != p) return false;  //@check
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool followsRhythm(string& pattern, string& sentence) {
                                vector<string> words;  //@split
                                stringstream in(sentence);  //@split
                                for (string w; in >> w;) words.push_back(w);  //@split
                                if (words.size() != pattern.size()) return false;  //@split
                                unordered_map<char, string> toWord;  //@maps
                                unordered_map<string, char> toLetter;  //@maps
                                for (size_t i = 0; i < words.size(); i++) {  //@check
                                    auto a = toWord.emplace(pattern[i], words[i]).first;  //@check
                                    auto b = toLetter.emplace(words[i], pattern[i]).first;  //@check
                                    if (a->second != words[i] || b->second != pattern[i]) return false;  //@check
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool followsRhythm(char* pattern, char* sentence) {
                            int n = strlen(pattern), count = 0;  //@split
                            char* copy = malloc(strlen(sentence) + 1);  //@split
                            strcpy(copy, sentence);  //@split
                            char** words = malloc((strlen(sentence) / 2 + 2) * sizeof(char*));  //@split
                            for (char* w = strtok(copy, " "); w; w = strtok(NULL, " ")) words[count++] = w;  //@split
                            bool ok = count == n;  //@split
                            int first[26];  //@maps
                            for (int c = 0; c < 26; c++) first[c] = -1;  //@maps
                            for (int i = 0; i < n && ok; i++) {  //@check
                                int c = pattern[i] - 'a';  //@check
                                if (first[c] == -1) first[c] = i;  //@check
                                else if (strcmp(words[first[c]], words[i]) != 0) ok = false;  //@check
                            }
                            for (int a = 0; a < 26 && ok; a++)  //@unique
                                for (int b = a + 1; b < 26 && ok; b++)  //@unique
                                    if (first[a] >= 0 && first[b] >= 0 && strcmp(words[first[a]], words[first[b]]) == 0) ok = false;  //@unique
                            free(words); free(copy);  //@ret
                            return ok;  //@ret
                        }
                    """,
                },
                lines=[
                    ("split", "One word per letter, or it fails.", {"c": "`strtok` cuts a copy of the sentence at spaces."}),
                    ("maps", "Letter → word and word → letter.", {"c": "No string map in C: `first[c]` remembers the position of letter c's first word."}),
                    ("check", "Each pair must match what each map already says (or set it).", {"c": "Same letter ⇒ same word: compare with the letter's first word."}),
                    ("unique", "Different letters ⇒ different words: compare the first words of every pair of used letters (at most 26 × 25 / 2 comparisons)."),
                    ("ret", "A one-to-one match."),
                ],
                complexity=["**Time O(n · L)** (C adds O(26² · L)). **Space O(n · L)** for the maps."],
            ),
        ],
        takeaways=[
            """
            - **Bijection check = two maps** (or one map plus a "used" set for the other side).
            - A single map misses "two keys, same value".
            - Compare lengths first.
            """
        ],
    )
