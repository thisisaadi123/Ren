"""Lesson: Anagrams and signatures (Strings, pattern 5)."""
from lesson import Bars, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

STEPS = {
    "python": """
        def steps_to_anagram(s, t):
            count = [0] * 26                                #@count
            for ch in s:                                    #@up
                count[ord(ch) - ord("a")] += 1              #@up
            for ch in t:                                    #@down
                count[ord(ch) - ord("a")] -= 1              #@down
            return sum(c for c in count if c > 0)           #@sum
    """,
    "java": """
        static int stepsToAnagram(String s, String t) {
            int[] count = new int[26];                      //@count
            for (char ch : s.toCharArray()) count[ch - 'a']++;  //@up
            for (char ch : t.toCharArray()) count[ch - 'a']--;  //@down
            int steps = 0;                                  //@sum
            for (int c : count) if (c > 0) steps += c;      //@sum
            return steps;                                   //@sum
        }
    """,
    "cpp": """
        int stepsToAnagram(const string& s, const string& t) {
            int count[26] = {0};                            //@count
            for (char ch : s) count[ch - 'a']++;            //@up
            for (char ch : t) count[ch - 'a']--;            //@down
            int steps = 0;                                  //@sum
            for (int c : count) if (c > 0) steps += c;      //@sum
            return steps;                                   //@sum
        }
    """,
    "c": """
        int stepsToAnagram(const char* s, const char* t) {
            int count[26] = {0};                            //@count
            for (const char* p = s; *p; p++) count[*p - 'a']++;     //@up
            for (const char* p = t; *p; p++) count[*p - 'a']--;     //@down
            int steps = 0;                                  //@sum
            for (int i = 0; i < 26; i++) if (count[i] > 0) steps += count[i];   //@sum
            return steps;                                   //@sum
        }
    """,
}
STEPS_RUN = {
    "python": """
        for s, t in [("bab", "aba"), ("leetcode", "practice"), ("anagram", "mangaar"), ("abc", "xyz")]:
            print(steps_to_anagram(s, t))
    """,
    "java": """
        public static void main(String[] args) {
            String[][] tests = {{"bab", "aba"}, {"leetcode", "practice"}, {"anagram", "mangaar"}, {"abc", "xyz"}};
            for (String[] t : tests) System.out.println(stepsToAnagram(t[0], t[1]));
        }
    """,
    "cpp": """
        int main() {
            vector<pair<string, string>> tests = {{"bab", "aba"}, {"leetcode", "practice"}, {"anagram", "mangaar"}, {"abc", "xyz"}};
            for (auto& [s, t] : tests) cout << stepsToAnagram(s, t) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* tests[][2] = {{"bab", "aba"}, {"leetcode", "practice"}, {"anagram", "mangaar"}, {"abc", "xyz"}};
            for (int i = 0; i < 4; i++) printf("%d\\n", stepsToAnagram(tests[i][0], tests[i][1]));
            return 0;
        }
    """,
}

PAL = {
    "python": """
        def can_be_palindrome(s):
            odd = 0                                         #@mask
            for ch in s:                                    #@flip
                odd ^= 1 << (ord(ch) - ord("a"))            #@flip
            return odd & (odd - 1) == 0                     #@test
    """,
    "java": """
        static boolean canBePalindrome(String s) {
            int odd = 0;                                    //@mask
            for (char ch : s.toCharArray()) odd ^= 1 << (ch - 'a');     //@flip
            return (odd & (odd - 1)) == 0;                  //@test
        }
    """,
    "cpp": """
        bool canBePalindrome(const string& s) {
            unsigned odd = 0;                               //@mask
            for (char ch : s) odd ^= 1u << (ch - 'a');      //@flip
            return (odd & (odd - 1)) == 0;                  //@test
        }
    """,
    "c": """
        bool canBePalindrome(const char* s) {
            unsigned odd = 0;                               //@mask
            for (const char* p = s; *p; p++) odd ^= 1u << (*p - 'a');  //@flip
            return (odd & (odd - 1)) == 0;                  //@test
        }
    """,
}
PAL_RUN = {
    "python": """
        for s in ["carerac", "code", "aab", ""]:
            print(str(can_be_palindrome(s)).lower())
    """,
    "java": """
        public static void main(String[] args) {
            for (String s : new String[] {"carerac", "code", "aab", ""}) System.out.println(canBePalindrome(s));
        }
    """,
    "cpp": """
        int main() {
            for (string s : {"carerac", "code", "aab", ""}) cout << (canBePalindrome(s) ? "true" : "false") << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* tests[] = {"carerac", "code", "aab", ""};
            for (int i = 0; i < 4; i++) printf("%s\\n", canBePalindrome(tests[i]) ? "true" : "false");
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

from collections import Counter  # noqa: E402
from itertools import permutations  # noqa: E402

steps_to_anagram = py(STEPS["python"], "steps_to_anagram")
can_be_palindrome = py(PAL["python"], "can_be_palindrome")
for s, t in [("bab", "aba"), ("leetcode", "practice"), ("anagram", "mangaar"), ("abc", "xyz"), ("bacon", "cobra")]:
    assert steps_to_anagram(s, t) == sum((Counter(s) - Counter(t)).values())
for s in ["carerac", "code", "aab", "", "aabbccd", "abcd"]:
    assert can_be_palindrome(s) == any("".join(p) == "".join(p)[::-1] for p in permutations(s))

# Theory walk: one counter table for two words.
WA, WB = "bacon", "cobra"
LET = sorted(set(WA + WB))
cw = Steps(f"`steps_to_anagram(\"{WA}\", \"{WB}\")`: count up for the first word, down for the second.")
cnt = {c: 0 for c in LET}


def c_panels(i_a=None, i_b=None, changed=None, final=False):
    if i_a is not None:
        sa, sb = {**{k: "dim" for k in range(i_a)}, i_a: "active"}, {}
    elif i_b is not None:
        sa, sb = {k: "dim" for k in range(len(WA))}, {**{k: "dim" for k in range(i_b)}, i_b: "active"}
    elif final:
        sa, sb = {k: "dim" for k in range(len(WA))}, {k: "dim" for k in range(len(WB))}
    else:
        sa, sb = {}, {}
    bst = {}
    if changed is not None:
        bst[LET.index(changed)] = "active"
    if final:
        bst = {k: "answer" for k, c in enumerate(LET) if cnt[c] > 0}
    return (Row(list(WA), st=sa, slots=True, label="s"), Row(list(WB), st=sb, slots=True, label="t"),
            Bars([cnt[c] for c in LET], labels=LET, st=bst, label="count (s minus t)", top=1, bottom=-1))


cw.step(f"One counter per letter, all 0. Only the letters that appear ({', '.join(LET)}) are drawn.", *c_panels())
for i, ch in enumerate(WA):
    cnt[ch] += 1
    cw.step(f"'{ch}' from s: its counter goes up to {cnt[ch]}.", *c_panels(i_a=i, changed=ch))
for i, ch in enumerate(WB):
    cnt[ch] -= 1
    note = " Back to 0: the two words agree on it so far." if cnt[ch] == 0 else (f" Below 0: t has {'an' if ch in 'aefhilmnorsx' else 'a'} '{ch}' that s doesn't." if cnt[ch] < 0 else "")
    cw.step(f"'{ch}' from t: its counter goes down to {cnt[ch]}.{note}", *c_panels(i_b=i, changed=ch))
POS = sum(c for c in cnt.values() if c > 0)
cw.step(f"Positive counters are letters s has that t is missing; negative ones are the letters t has instead. Each change in t fixes one of each: {POS} step{'s' if POS != 1 else ''}.",
        *c_panels(final=True), result=POS)
assert POS == steps_to_anagram(WA, WB)
C_LEGEND = {"active": "the letter being counted", "dim": "already counted", "answer": "letters t is short of"}

# Trace walk: the odd-count mask.
PS = "tacocat"
PL = sorted(set(PS))
pw = Steps(f"`can_be_palindrome(\"{PS}\")`. One bit per letter: 1 means the letter has been seen an odd number of times.")
bits = {c: 0 for c in PL}


def p_panels(i=None):
    st = {k: "dim" for k in range(i if i is not None else len(PS))}
    bst = {}
    if i is not None:
        st[i] = "active"
        bst[PL.index(PS[i])] = "active"
    mask = sum(bits[c] << (ord(c) - 97) for c in PL)
    return (Row(list(PS), st=st, slots=True, label="s"), Row([bits[c] for c in PL], st=bst, slots=True, label="odd so far? (" + " ".join(PL) + ")"),
            M({"odd letters": " ".join(c for c in PL if bits[c]) or "none", "mask": mask}))


pw.step("Nothing read yet. Every count is 0, which is even.", Row(list(PS), slots=True, label="s"),
        Row([0] * len(PL), slots=True, label="odd so far? (" + " ".join(PL) + ")"), M({"odd letters": "none", "mask": 0}))
for i, ch in enumerate(PS):
    bits[ch] ^= 1
    pw.step(f"'{ch}': flip its bit to {bits[ch]} ({'odd' if bits[ch] else 'even'} so far).", *p_panels(i))
ODD = [c for c in PL if bits[c]]
pw.step(f"At most one letter has an odd count ({', '.join(ODD) or 'none'}), so a palindrome can be made: the odd one goes in the middle. "
        "In the mask, \"at most one bit set\" is `mask & (mask - 1) == 0`.", *p_panels(), result="true")
P_LEGEND = {"active": "the letter just read, and its bit", "dim": "already read"}

# Example: substring queries with prefix masks.
QS_S = "abcbaab"
pref = [0]
for ch in QS_S:
    pref.append(pref[-1] ^ (1 << (ord(ch) - 97)))
QUERIES = [(0, 4), (1, 3), (0, 6), (2, 5)]
q_rows = []
for l, r in QUERIES:
    m = pref[r + 1] ^ pref[l]
    ok = m & (m - 1) == 0
    q_rows.append((f"[{l}, {r}] \"{QS_S[l:r + 1]}\"", f"{bin(m)[2:].zfill(3)}", "yes" if ok else "no"))
    assert ok == can_be_palindrome(QS_S[l:r + 1])

KINDS = [
    ("same letters, same counts (anagram)", "sorted letters, or 26 counts", '"listen" → "eilnst"'),
    ("same counts, compared to a target", "count difference", "s minus t, as in the template"),
    ("could be rearranged into a palindrome", "which counts are odd (a bitmask)", '"aab" → only b odd'),
    ("same set of letters, any counts", "which letters appear (a bitmask)", '"abba" and "ab" → {a, b}'),
    ("one can be built from the other's letters", "counts, compared letter by letter", "every count in t ≤ the count in s"),
]

N = 10**5

lesson(
    "strings",
    "string-signature",
    """
    When a question only cares about which letters a string has and how many of each, not their order, replace the
    string by a short signature: sorted letters, a table of 26 counts, or a bitmask. Comparing, grouping and
    measuring strings then becomes comparing signatures, in time proportional to the length.
    """,
    [
        ("idea", "The idea", [
            f"""
            Scrabble players know this instinctively. With the tiles `{WA.upper()}` on your rack, it doesn't matter what
            order they're in: the question is what you have. "Can I make `{WB.upper()}`?" is answered by counting: one
            C, one O, one B, one R, one A. You have all of them except an R, and you have an N you won't use.

            A signature is that tile count, written down. Two strings with the same signature are anagrams. Two strings
            with different signatures can be compared letter by letter to see exactly what's missing or extra. Order is
            gone, which is the point: whatever the question asks about order is irrelevant here, so the signature keeps
            only what matters.
            """,
            fig(Row(list(WA), slots=True, label="s"), Row(list(WB), slots=True, label="t"),
                Bars([Counter(WA)[c] - Counter(WB)[c] for c in LET], labels=LET, label="count in s minus count in t", top=1, bottom=-1),
                caption="Every letter balances except n (s has one t doesn't) and r (the other way round)."),
            key("""
            Pick the smallest signature that captures the question: 26 counts for "same letters", their difference for
            "how far apart", a parity bitmask for "can it become a palindrome", a presence bitmask for "same set of
            letters". Build it in one pass, O(n).
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            Words like anagram, rearrange, permutation, scramble, "using the letters of", "any order", or "could be made
            into a palindrome". If you can shuffle the input and the answer doesn't change, a signature is probably the
            right representation.
            """,
            table(["what the question cares about", "signature", "example"], *KINDS),
            """
            Not a fit:

            - Order matters (subsequence, substring, the next arrangement). Signatures throw order away.
            - You need it for every window of a long string. Keep the counts and update them as the window slides
              (Sliding Window topic) instead of rebuilding.
            - The alphabet is huge or unknown (any Unicode, words instead of letters). Use a hash map of counts rather
              than a fixed array.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Counts decide anagrams

            Two strings are anagrams exactly when every letter appears the same number of times in both. One direction:
            rearranging doesn't change counts. The other: with equal counts you can build one from the other by putting
            the letters in the other's order. So the count table is a complete signature: equal tables, anagrams;
            different tables, not.

            ### Counting up and down

            Instead of two tables, use one: add 1 for each letter of `s`, subtract 1 for each letter of `t`. A zero means
            the letter balances. A positive count is a letter `s` has more of; a negative count, one `t` has more of.
            """,
            walk(cw, legend=C_LEGEND),
            """
            ### Measuring the gap

            If the strings have the same length, the positive counts add up to the same total as the negative ones (each
            side has the same number of letters). To turn `t` into an anagram of `s` by changing letters of `t`, each
            change can replace one surplus letter of `t` with one letter it's short of. So the number of changes needed is
            the sum of the positive counts, and it can't be done in fewer.

            ### Parity and palindromes

            A palindrome pairs each letter with its mirror, so every letter appears an even number of times, except
            possibly one in the middle. So a string can be rearranged into a palindrome exactly when at most one letter
            has an odd count. Only parity matters, which fits in one bit per letter: flip the letter's bit on every
            occurrence. "At most one bit set" is the test `mask & (mask - 1) == 0`, because subtracting 1 clears the lowest
            set bit.

            ### Sorting versus counting

            Sorting the letters also gives a signature, in O(L log L) for a word of length `L`. Counting is O(L + 26),
            and the counts can be compared or subtracted directly. For short words either is fine; for long strings, or
            when you need the differences, count.
            """,
        ]),
        ("template", "The template", [
            """
            `s` and `t` have the same length and use lowercase letters. In one step you may change any letter of `t` to
            any other letter. How many steps make `t` an anagram of `s`?
            """,
            code(
                "Steps to make one word an anagram of another",
                STEPS,
                [
                    ("count", "One counter per letter, all 0."),
                    ("up", "Count every letter of `s` up."),
                    ("down", "Count every letter of `t` down. Now each counter is (count in `s`) minus (count in `t`)."),
                    ("sum", "Positive counters are letters `t` is short of. Each change supplies one of them, so their total "
                            "is the answer."),
                ],
                STEPS_RUN,
                'steps_to_anagram("bab", "aba"); ("leetcode", "practice"); ("anagram", "mangaar"); ("abc", "xyz")',
            ),
            """
            `"anagram"` and `"mangaar"` are already anagrams: 0 steps. `"abc"` and `"xyz"` share nothing: all 3 letters
            change.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "The parity bitmask from the variation below, on a palindrome-shaped word:",
            walk(pw, legend=P_LEGEND),
            """
            On paper, list the alphabet's letters that appear, and tick or untick each one as you read. Whatever's still
            ticked at the end has an odd count.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Many questions about substrings

            "Can `s[l..r]` be rearranged into a palindrome?" for lots of `(l, r)` pairs. Keep a prefix of masks:
            `pref[i]` is the parity mask of the first `i` letters. The parity of a substring is `pref[r + 1] ^ pref[l]`,
            because XOR cancels the shared prefix (like subtraction in *Prefix sums*). Each question is then O(1). For
            `{QS_S}`:
            """,
            table(["substring", "odd-count mask (c b a)", "palindrome possible?"], *q_rows),
            """
            ### Building one word from another's letters

            "Can `note` be written using the letters of `magazine`?" Count the magazine up and the note down; if any
            counter goes below zero, a letter ran out. You can stop at the first negative.

            ### Normalise before counting

            Real inputs have capitals, spaces and punctuation. Decide what counts as "the same letter" first (lowercase
            everything, drop spaces), then build the signature from the cleaned characters. Otherwise `'D'` and `'d'`
            land in different counters, or out of range of a 26-slot array.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### A palindrome in some order

            Can the letters of `s` be rearranged into a palindrome? Flip one bit per letter; at most one bit may be left
            set.
            """,
            code(
                "Can it be rearranged into a palindrome?",
                PAL,
                [
                    ("mask", "One bit per letter, all 0: every count starts even.",
                     {"cpp": "Unsigned, so shifting a 1 into bit 25 is well defined.",
                      "c": "Unsigned, so shifting a 1 into bit 25 is well defined."}),
                    ("flip", "Each occurrence flips its letter's bit: odd becomes even and back."),
                    ("test", "`odd - 1` turns the lowest set bit off and the bits below it on. ANDing with `odd` leaves 0 exactly "
                             "when at most one bit was set."),
                ],
                PAL_RUN,
                'can_be_palindrome("carerac"); ("code"); ("aab"); ("")',
            ),
            """
            ### Signatures as dictionary keys

            To group words by their letters, use the signature as a hash map key: sorted letters as a string, or the
            26 counts as a tuple or a string with separators. *Group by key* covers this in detail.

            ### Comparing signatures, not strings

            Some questions compare signatures in a looser way: "the same letters, and the same *multiset* of counts, in
            any assignment" or "the same set of letters". Work out what's preserved by the allowed moves, and compare
            exactly that. For instance, if swapping any two letters is allowed, the counts are preserved; if
            relabelling is also allowed, only the sorted list of counts is.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            Building a count signature is O(L) time for a string of length `L`, with O(σ) space for an alphabet of size
            σ (26 here). Comparing two count signatures is O(σ). A bitmask is O(L) to build and O(1) to test. Sorting
            letters instead is O(L log L).

            Checking anagrams by trying every rearrangement would be O(L!), and even "for each letter of `s`, find and
            remove it from `t`" is O(L²): for `L = {N:,}` that's billions of steps against {N:,} here.
            """,
            table(
                ["Signature", "Build", "Compare", "Space"],
                ["Sorted letters", "O(L log L)", "O(L)", "O(L)"],
                ["26 counts", "O(L)", "O(26)", "O(26)"],
                ["Hash map of counts (any alphabet)", "O(L) average", "O(distinct)", "O(distinct)"],
                ["Parity bitmask", "O(L)", "O(1)", "one integer"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `collections.Counter(s)` builds a count map; `Counter(s) == Counter(t)` compares; `Counter(s) - Counter(t)`
            keeps only positive differences. `sorted(s)` returns a list; `"".join(sorted(s))` for a key.

            ### Java

            `int[26]` with `ch - 'a'`. `Arrays.equals(a, b)` compares count arrays; `Arrays.toString(counts)` makes a key.
            `Integer.bitCount(mask) <= 1` is a readable parity test.

            ### C++

            `array<int, 26>` compares with `==` and works as a `map` key. `__builtin_popcount(mask) <= 1` counts set bits.

            ### C

            `int count[26] = {0};` and `memcmp` to compare two tables. Cast to `unsigned char` before indexing if the
            input might contain characters outside `a` to `z`.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Indexing `count[ch - 'a']` with a capital letter, space or digit: out of range.
            - Forgetting that different lengths can never be anagrams (check first; it's cheap).
            - Using a set of letters when counts matter (`"aab"` and `"abb"` have the same set).
            - Summing absolute differences instead of the positive ones, which double counts.
            - Shifting `1 << 31` or more in a 32-bit signed integer.
            - Rebuilding a signature for every window instead of updating it.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why are equal count tables enough to say two strings are anagrams?",
                 "With the same number of each letter, you can rebuild one string from the other's letters by putting them in its order. And rearranging never changes counts, so it works both ways."),
                ("steps_to_anagram(\"aab\", \"bbc\"): what's the answer?",
                 "Counts: a +2, b -1, c -1. The positive total is 2, so two letters of t must change."),
                ("Why does a palindrome allow at most one odd count?",
                 "Mirrored positions pair up equal letters. Only the middle position of an odd-length palindrome has no partner."),
                ("What does `mask & (mask - 1)` do?",
                 "It clears the lowest set bit. The result is 0 exactly when the mask had at most one bit set."),
                ("How do prefix masks answer \"can s[l..r] be a palindrome?\" in O(1)?",
                 "The parity of s[l..r] is pref[r + 1] XOR pref[l]: the shared prefix cancels. Then test it for at most one set bit."),
            ),
        ]),
    ],
)
