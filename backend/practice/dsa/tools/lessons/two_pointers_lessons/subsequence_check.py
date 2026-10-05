"""Lesson: Subsequence matching (Two Pointers, pattern 6)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

APPEND = {
    "python": """
        def letters_to_append(text, word):
            j = 0                                       #@start
            for ch in text:                             #@scan
                if j < len(word) and ch == word[j]:     #@match
                    j += 1                              #@match
            return len(word) - j                        #@ret
    """,
    "java": """
        static int lettersToAppend(String text, String word) {
            int j = 0;                                  //@start
            for (int i = 0; i < text.length(); i++) {   //@scan
                if (j < word.length() && text.charAt(i) == word.charAt(j))  //@match
                    j++;                                //@match
            }
            return word.length() - j;                   //@ret
        }
    """,
    "cpp": """
        int lettersToAppend(const string& text, const string& word) {
            size_t j = 0;                               //@start
            for (char ch : text) {                      //@scan
                if (j < word.size() && ch == word[j])   //@match
                    j++;                                //@match
            }
            return word.size() - j;                     //@ret
        }
    """,
    "c": """
        int lettersToAppend(const char* text, const char* word) {
            int j = 0, n = strlen(word);                //@start
            for (const char* p = text; *p != '\\0'; p++) {  //@scan
                if (j < n && *p == word[j])             //@match
                    j++;                                //@match
            }
            return n - j;                               //@ret
        }
    """,
}
APPEND_RUN = {
    "python": """
        for text, word in [("travelling", "tile"), ("pineapple", "pale"), ("z", "abc"), ("abc", "")]:
            print(letters_to_append(text, word))
    """,
    "java": """
        public static void main(String[] args) {
            String[][] tests = {{"travelling", "tile"}, {"pineapple", "pale"}, {"z", "abc"}, {"abc", ""}};
            for (String[] t : tests) System.out.println(lettersToAppend(t[0], t[1]));
        }
    """,
    "cpp": """
        int main() {
            vector<pair<string, string>> tests = {{"travelling", "tile"}, {"pineapple", "pale"}, {"z", "abc"}, {"abc", ""}};
            for (auto& [text, word] : tests) cout << lettersToAppend(text, word) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* tests[][2] = {{"travelling", "tile"}, {"pineapple", "pale"}, {"z", "abc"}, {"abc", ""}};
            for (int i = 0; i < 4; i++) printf("%d\\n", lettersToAppend(tests[i][0], tests[i][1]));
            return 0;
        }
    """,
}

COPIES = {
    "python": """
        def copies_needed(source, target):
            copies, j = 0, 0                            #@start
            while j < len(target):                      #@loop
                start = j                               #@pass
                for ch in source:                       #@pass
                    if j < len(target) and ch == target[j]:     #@pass
                        j += 1                          #@pass
                if j == start:                          #@stuck
                    return -1                           #@stuck
                copies += 1                             #@count
            return copies                               #@ret
    """,
    "java": """
        static int copiesNeeded(String source, String target) {
            int copies = 0, j = 0;                      //@start
            while (j < target.length()) {               //@loop
                int start = j;                          //@pass
                for (int i = 0; i < source.length(); i++)   //@pass
                    if (j < target.length() && source.charAt(i) == target.charAt(j)) j++;    //@pass
                if (j == start) return -1;              //@stuck
                copies++;                               //@count
            }
            return copies;                              //@ret
        }
    """,
    "cpp": """
        int copiesNeeded(const string& source, const string& target) {
            int copies = 0;                             //@start
            size_t j = 0;                               //@start
            while (j < target.size()) {                 //@loop
                size_t start = j;                       //@pass
                for (char ch : source)                  //@pass
                    if (j < target.size() && ch == target[j]) j++;  //@pass
                if (j == start) return -1;              //@stuck
                copies++;                               //@count
            }
            return copies;                              //@ret
        }
    """,
    "c": """
        int copiesNeeded(const char* source, const char* target) {
            int copies = 0, j = 0, n = strlen(target);  //@start
            while (j < n) {                             //@loop
                int start = j;                          //@pass
                for (const char* p = source; *p != '\\0'; p++)  //@pass
                    if (j < n && *p == target[j]) j++;  //@pass
                if (j == start) return -1;              //@stuck
                copies++;                               //@count
            }
            return copies;                              //@ret
        }
    """,
}
COPIES_RUN = {
    "python": """
        for source, target in [("abc", "abcbc"), ("abc", "acdbc"), ("xyz", "xzyxz"), ("ab", "")]:
            print(copies_needed(source, target))
    """,
    "java": """
        public static void main(String[] args) {
            String[][] tests = {{"abc", "abcbc"}, {"abc", "acdbc"}, {"xyz", "xzyxz"}, {"ab", ""}};
            for (String[] t : tests) System.out.println(copiesNeeded(t[0], t[1]));
        }
    """,
    "cpp": """
        int main() {
            vector<pair<string, string>> tests = {{"abc", "abcbc"}, {"abc", "acdbc"}, {"xyz", "xzyxz"}, {"ab", ""}};
            for (auto& [source, target] : tests) cout << copiesNeeded(source, target) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* tests[][2] = {{"abc", "abcbc"}, {"abc", "acdbc"}, {"xyz", "xzyxz"}, {"ab", ""}};
            for (int i = 0; i < 4; i++) printf("%d\\n", copiesNeeded(tests[i][0], tests[i][1]));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

from itertools import combinations  # noqa: E402

letters_to_append = py(APPEND["python"], "letters_to_append")
copies_needed = py(COPIES["python"], "copies_needed")


def hidden(word, text):
    return any("".join(c) == word for c in combinations(text, len(word)))


for text, word in [("travelling", "tile"), ("pineapple", "pale"), ("z", "abc"), ("abc", ""), ("banana", "bnn"), ("banana", "nab")]:
    k = len(word) - letters_to_append(text, word)
    assert hidden(word[:k], text) and (k == len(word) or not hidden(word[:k + 1], text))


def walk_match(text, word, title, legend_done):
    w = Steps(title)
    j = 0

    def panels(i=None, hit=None):
        st_t, st_w = {}, {}
        for k in range(len(text)):
            if k in matched:
                st_t[k] = "found"
            elif i is not None and k < i:
                st_t[k] = "dim"
        for k in range(j):
            st_w[k] = "found"
        if i is not None and i < len(text):
            if hit:
                st_t[i] = "found"
                st_w[j - 1] = "found"
            else:
                st_t[i] = "active"
                if j < len(word):
                    st_w[j] = "active"
        return (Row(list(text), st=st_t, ptr={"i": i} if i is not None and i < len(text) else None, slots=True, label="text"),
                Row(list(word), st=st_w, ptr={"j": j if j < len(word) else None}, slots=True, label="word"))

    matched = []
    w.step(f"`j` points at the first letter of \"{word}\" still to find. `i` will read \"{text}\" once, left to right.", *panels())
    for i, ch in enumerate(text):
        if j < len(word) and ch == word[j]:
            j += 1
            matched.append(i)
            msg = f"'{ch}' is the letter we're waiting for. " + (f"Match it and wait for the next one, '{word[j]}'." if j < len(word) else "Match it: that was the last letter of the word.")
            w.step(msg, *panels(i, hit=True))
        elif j < len(word):
            w.step(f"'{ch}' isn't '{word[j]}'. Skip it; the text moves on and the word waits.", *panels(i))
        else:
            break
    w.steps[-1]["text"] += " " + legend_done(j)
    return w, j


TW, WW = "pineapple", "pale"
gw, GJ = walk_match(TW, WW, f"Is \"{WW}\" hidden in \"{TW}\"? Take each letter of the word the first time it can appear.",
                    lambda j: f"All {len(WW)} letters were found, in order: it's hidden." if j == len(WW) else f"The text ran out with {len(WW) - j} letters still to find.")
assert GJ == len(WW)
G_LEGEND = {"found": "matched", "active": "compared now", "dim": "skipped"}

T2, W2 = "travelling", "tile"
tw, TJ = walk_match(T2, W2, f"`letters_to_append(\"{T2}\", \"{W2}\")`. Match as much of the word as possible, then count what's left.",
                    lambda j: f"The text is used up. {j} of {len(W2)} letters matched, so {len(W2) - j} must be added at the end: \"{W2[j:]}\".")
assert len(W2) - TJ == letters_to_append(T2, W2)

# Why taking the earliest match is safe: compare greedy positions with another valid choice.
GT, GWD = "abracadabra", "aba"
greedy_pos, j = [], 0
for i, ch in enumerate(GT):
    if j < len(GWD) and ch == GWD[j]:
        greedy_pos.append(i)
        j += 1
assert j == len(GWD)
OTHER = list(max((c for c in combinations(range(len(GT)), len(GWD)) if "".join(GT[k] for k in c) == GWD), key=sum))
assert OTHER and all(g <= o for g, o in zip(greedy_pos, OTHER))
ex_rows = [(f"'{GWD[k]}'", str(greedy_pos[k]), str(OTHER[k])) for k in range(len(GWD))]

# Typed with stuck keys.
NAME, TYPED = "alex", "aaleexx"
COMPARE = [
    ("subsequence", "letters in order, gaps allowed", '"ace" in "abcde": yes', "two pointers"),
    ("substring", "letters in order, no gaps", '"bcd" in "abcde": yes; "ace": no', "string search (KMP, Z)"),
    ("anagram", "same letters, any order", '"dcbae" of "abcde": yes', "counting"),
]

lesson(
    "two-pointers",
    "subsequence-check",
    """
    A word is a subsequence of a text if its letters appear in the text in the same order, not necessarily next to
    each other. One pointer reads the text, one waits on the next letter of the word, and the word's pointer moves
    only on a match. If it reaches the end of the word, the word is in there.
    """,
    [
        ("idea", "The idea", [
            f"""
            You're reading a long sign, "{TW}", and wondering whether the word "{WW}" is hidden in it if you're allowed
            to skip letters. Put a finger on the "p" of "{WW}". Read the sign from the left. The first letter is a "p":
            that's the one you wanted, so move your finger to "a". Keep reading, skipping everything that isn't "a",
            until an "a" turns up. Then wait for "l", then "e". If your finger reaches the end of the word before the
            sign ends, the word is hidden.

            Two pointers, one per string. The text's pointer moves every step. The word's pointer moves only on a
            match. Nothing ever goes backwards, so it's one pass over the text.
            """,
            fig(Row(list(TW), st={k: "found" for k in [0, 4, 7, 8]}, slots=True, label="text"),
                Row(list(WW), st={k: "found" for k in range(len(WW))}, slots=True, label="word"),
                caption="Each letter of the word is matched the first time it can be, left to right."),
            key("""
            `j = 0`. For each character of the text, if it equals `word[j]`, move `j` on. At the end, `j` is how much of
            the word was found in order: all of it means the word is a subsequence. O(length of the text), O(1) space.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The question talks about deleting characters, skipping letters, "in the same order but not necessarily
            next to each other", or "can you get this from that by removing some". Also: typing with repeated keys,
            matching patterns where some letters are optional, and checking a list of words against one text.
            """,
            table(["word is a …", "means", "example", "tool"], *COMPARE),
            """
            Not a fit:

            - The longest *common* subsequence of two strings, or the fewest edits between them. Choosing which letters
              to keep from *both* sides needs dynamic programming, not one greedy pass.
            - Letters must be next to each other (substring). Use string search.
            - Order doesn't matter (anagram, "made from these letters"). Count letters instead.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Taking the earliest match is never a mistake

            The loop matches each letter of the word at the *first* place it can. Why is that safe? Because matching
            earlier only leaves more text for the rest of the word.

            Suppose the word can be found at some positions `p₀ < p₁ < p₂ < …`. The greedy scan matches the first letter
            at some position `g₀ ≤ p₀`, since it takes the earliest one. Then it matches the second letter at the first
            spot after `g₀`, and `p₁` is after `p₀ ≥ g₀`, so that spot is at most `p₁`. Carrying on, every greedy position
            is at or before the corresponding position of *any* valid match. So if a match exists, greedy finds one,
            and if greedy runs out of text, no match exists.
            """,
            walk(gw, legend=G_LEGEND),
            f"""
            Here is that comparison for "{GWD}" in "{GT}": the greedy positions against the latest valid way of picking
            the letters. Greedy is never later, letter by letter.
            """,
            table(["letter", "greedy position", "another valid choice"], *ex_rows),
            """
            ### What `j` tells you at the end

            The loop doesn't just answer yes or no. When the text runs out, `j` is the length of the longest *prefix* of
            the word that's a subsequence of the text, by the same argument: no other way of matching could get further.
            That's what the template uses: `len(word) - j` letters are missing at the end.

            ### Stopping early

            Once `j` reaches the end of the word, nothing else in the text matters, so you can stop reading. And if the
            word is longer than the text, the answer is no before you start.
            """,
        ]),
        ("template", "The template", [
            """
            How many letters must be added to the end of `text` so that `word` becomes a subsequence of it? Match as
            much of `word` as the text allows; whatever is left over has to be appended.
            """,
            code(
                "Letters to append so the word is hidden",
                APPEND,
                [
                    ("start", "`j` is the next letter of the word to find.",
                     {"c": "`n` is the word's length, found once with `strlen`."}),
                    ("scan", "Read every character of the text once.",
                     {"c": "Walk the text with a pointer until the terminating `'\\0'`."}),
                    ("match", "If it's the letter the word is waiting for, take it. Otherwise skip it: the word waits. The "
                              "`j <` check stops once the whole word has been found."),
                    ("ret", "`j` letters were found in order; the other `len(word) - j` have to be appended.",
                     {"cpp": "Both sizes are unsigned and `j` never exceeds `word.size()`, so the difference is safe."}),
                ],
                APPEND_RUN,
                'letters_to_append("travelling", "tile"); ("pineapple", "pale"); ("z", "abc"); ("abc", "")',
            ),
            """
            0 means the word is already hidden. An empty word is always hidden, and a text with none of the word's
            letters needs the whole word appended.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "The first example, character by character:",
            walk(tw, legend={"found": "matched", "active": "compared now", "dim": "skipped"}),
            """
            On paper, write the word under the text and draw a line from each word letter to the text letter it
            matched. The lines never cross, and each one goes to the first possible letter after the previous line.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### A name typed with sticky keys

            Someone typed their name, "{NAME}", and some keys repeated: "{TYPED}". Is that a possible result? This is a
            subsequence check with an extra rule: a text letter that doesn't match the name's next letter is only
            allowed if it repeats the letter typed just before it. Walk both strings: on a match, move both; on a
            repeat of the previous typed letter, move only the typed pointer; anything else means no. At the end, the
            whole name must have been matched.

            ### Many words against one text

            Checking `w` words against a text of length `t` one at a time costs O(w · t). When there are thousands of
            words, it helps to precompute, for every position in the text and every letter, where that letter next
            appears. Each word is then checked by jumping straight from match to match, in time proportional to the
            word's length. The matching rule is the same; only the "scan until the letter appears" part got faster.

            ### Words you can make by deleting

            "Which dictionary words can be made by deleting letters from the text?" is a subsequence check for each
            word. If the question wants the longest such word, sort or compare candidates by length (and then
            alphabetically) and check them, skipping any that are longer than the text.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Reading the text more than once

            How many copies of `source`, written one after another, does it take for `target` to be a subsequence? Each
            pass over `source` matches as much of `target` as it can (greedy, as before). If a whole pass matches
            nothing, the next letter of `target` doesn't appear in `source` at all, and the answer is -1.
            """,
            code(
                "Copies of the source needed to hide the target",
                COPIES,
                [
                    ("start", "No copies used yet, and `j` waits at the start of `target`.",
                     {"c": "`n` is the target's length."}),
                    ("loop", "Until all of `target` has been matched."),
                    ("pass", "One pass over a fresh copy of `source`, matching greedily from where `j` left off."),
                    ("stuck", "A full pass matched nothing: the letter `target[j]` isn't in `source`, so it can never be matched."),
                    ("count", "That pass used one copy."),
                    ("ret", "The number of copies. An empty target needs none."),
                ],
                COPIES_RUN,
                'copies_needed("abc", "abcbc"); ("abc", "acdbc"); ("xyz", "xzyxz"); ("ab", "")',
            ),
            """
            "abcbc" takes 2 copies ("abc" then "bc"). "acdbc" can't be made: there's no "d" in "abc". "xzyxz" takes 3:
            "x z", then "y", then "x z". Each pass is greedy, and by the same argument as before, greedy wastes no copy.

            ### Matching with optional letters

            Some checks allow the text to contain extra letters only of a certain kind. In camel-case matching, the
            pattern "FB" matches "FooBar" (every extra letter is lowercase) but not "FooBarTest" (the extra "T" is a
            capital). The skeleton doesn't change:
            decide, for a text letter that doesn't match `word[j]`, whether skipping it is allowed. If not, the answer
            is no.

            ### Deleting from the other side

            "What's the smallest number of letters to delete from the text so that the word is *no longer* hidden?" or
            "the longest word hidden in both of two texts" sound similar but need more than one greedy pass. When both
            strings are free to lose letters, it's dynamic programming.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            The text pointer moves every step and the word pointer never moves back, so a check takes at most `t`
            steps, where `t` is the text's length: O(t) time and O(1) extra space.

            Reading the source again and again costs O(s) per copy, and at most one copy per target letter, so
            O(s · m) for a target of length `m`. With a next-occurrence table it drops to O(m log s) or O(m), plus the
            table.
            """,
            table(
                ["Task", "Time", "Extra space"],
                ["Is one word hidden in the text?", "O(t)", "O(1)"],
                ["w words, one at a time", "O(w · t)", "O(1)"],
                ["w words with a next-occurrence table", "O(26 · t + total word length)", "O(26 · t)"],
                ["Copies of the source needed", "O(s · m)", "O(1)"],
                ["Longest common subsequence (not this pattern)", "O(t · m)", "O(t · m) or O(m)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            A neat one-liner uses an iterator: `it = iter(text); all(ch in it for ch in word)`. Each `in` consumes the
            iterator up to and including the match, which is exactly the two-pointer walk. Write the loop out when you
            need `j` afterwards.

            ### Java

            `charAt(i)` reads a character. For very long texts, `toCharArray()` once and index the array; it avoids a
            bounds check per call.

            ### C++

            `string::find(ch, from)` jumps to the next occurrence of a character, which is a convenient way to write
            the "skip until the letter appears" step. Mixing `size_t` and `int` in comparisons gives warnings; pick one.

            ### C

            Walk the text with a `const char*` until `'\\0'`. Call `strlen` on the word once, not in the loop condition,
            or each check costs O(length) again.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Moving the word pointer on a mismatch. Only a match moves it.
            - Reading `word[j]` after the whole word is matched. Check `j < len(word)` first, or stop early.
            - Confusing subsequence with substring. Gaps are allowed here.
            - An empty word: it's always hidden, even in an empty text.
            - Restarting the text from the beginning after a match. The text pointer never goes back.
            - Calling `strlen` in a C loop condition, which makes the loop quadratic.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why is matching each letter at its earliest possible position never a mistake?",
                 "Any other valid matching uses positions at or after greedy's, letter by letter. Matching earlier leaves at least as much text for the rest of the word, so greedy never falls behind."),
                ("What does `j` mean when the text runs out?",
                 "It's the length of the longest prefix of the word that is hidden in the text."),
                ("Is \"ace\" hidden in \"abcde\"? Is \"aec\"?",
                 "\"ace\" is: a, then c, then e appear in that order. \"aec\" isn't: after the e at index 4 there's no c."),
                ("letters_to_append(\"banana\", \"bnx\"): what's the answer?",
                 "1. b and n are found in order; x isn't in the text, so it has to be appended."),
                ("Why can't this greedy pass find the longest common subsequence of two strings?",
                 "Here only the text may skip letters; the word must be matched in full. When both strings may drop letters, choosing which to keep needs dynamic programming."),
            ),
        ]),
    ],
)
