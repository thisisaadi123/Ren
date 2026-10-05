"""Lesson: Palindrome checks (Strings, pattern 7)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

DEL = {
    "python": """
        def deletions(s, c):
            lo, hi, d = 0, len(s) - 1, 0                    #@ends
            while lo < hi:                                  #@loop
                if s[lo] == s[hi]:                          #@match
                    lo, hi = lo + 1, hi - 1                 #@match
                elif s[lo] == c:                            #@left
                    lo, d = lo + 1, d + 1                   #@left
                elif s[hi] == c:                            #@right
                    hi, d = hi - 1, d + 1                   #@right
                else:                                       #@stuck
                    return -1                               #@stuck
            return d                                        #@count


        def fewest_deletions(s):
            lo, hi = 0, len(s) - 1                          #@scan
            while lo < hi and s[lo] == s[hi]:               #@scan
                lo, hi = lo + 1, hi - 1                     #@scan
            if lo >= hi:                                    #@already
                return 0                                    #@already
            a, b = deletions(s, s[lo]), deletions(s, s[hi]) #@try
            if a < 0 or b < 0:                              #@pick
                return max(a, b)                            #@pick
            return min(a, b)                                #@pick
    """,
    "java": """
        static int deletions(String s, char c) {
            int lo = 0, hi = s.length() - 1, d = 0;         //@ends
            while (lo < hi) {                               //@loop
                if (s.charAt(lo) == s.charAt(hi)) {         //@match
                    lo++;                                   //@match
                    hi--;                                   //@match
                } else if (s.charAt(lo) == c) {             //@left
                    lo++;                                   //@left
                    d++;                                    //@left
                } else if (s.charAt(hi) == c) {             //@right
                    hi--;                                   //@right
                    d++;                                    //@right
                } else {                                    //@stuck
                    return -1;                              //@stuck
                }
            }
            return d;                                       //@count
        }

        static int fewestDeletions(String s) {
            int lo = 0, hi = s.length() - 1;                //@scan
            while (lo < hi && s.charAt(lo) == s.charAt(hi)) {   //@scan
                lo++;                                       //@scan
                hi--;                                       //@scan
            }
            if (lo >= hi) return 0;                         //@already
            int a = deletions(s, s.charAt(lo)), b = deletions(s, s.charAt(hi));    //@try
            if (a < 0 || b < 0) return Math.max(a, b);      //@pick
            return Math.min(a, b);                          //@pick
        }
    """,
    "cpp": """
        int deletions(const string& s, char c) {
            int lo = 0, hi = (int)s.size() - 1, d = 0;      //@ends
            while (lo < hi) {                               //@loop
                if (s[lo] == s[hi]) {                       //@match
                    lo++;                                   //@match
                    hi--;                                   //@match
                } else if (s[lo] == c) {                    //@left
                    lo++;                                   //@left
                    d++;                                    //@left
                } else if (s[hi] == c) {                    //@right
                    hi--;                                   //@right
                    d++;                                    //@right
                } else {                                    //@stuck
                    return -1;                              //@stuck
                }
            }
            return d;                                       //@count
        }

        int fewestDeletions(const string& s) {
            int lo = 0, hi = (int)s.size() - 1;             //@scan
            while (lo < hi && s[lo] == s[hi]) {             //@scan
                lo++;                                       //@scan
                hi--;                                       //@scan
            }
            if (lo >= hi) return 0;                         //@already
            int a = deletions(s, s[lo]), b = deletions(s, s[hi]);  //@try
            if (a < 0 || b < 0) return max(a, b);           //@pick
            return min(a, b);                               //@pick
        }
    """,
    "c": """
        int deletions(const char* s, int n, char c) {
            int lo = 0, hi = n - 1, d = 0;                  //@ends
            while (lo < hi) {                               //@loop
                if (s[lo] == s[hi]) {                       //@match
                    lo++;                                   //@match
                    hi--;                                   //@match
                } else if (s[lo] == c) {                    //@left
                    lo++;                                   //@left
                    d++;                                    //@left
                } else if (s[hi] == c) {                    //@right
                    hi--;                                   //@right
                    d++;                                    //@right
                } else {                                    //@stuck
                    return -1;                              //@stuck
                }
            }
            return d;                                       //@count
        }

        int fewestDeletions(const char* s) {
            int n = strlen(s), lo = 0, hi = n - 1;          //@scan
            while (lo < hi && s[lo] == s[hi]) {             //@scan
                lo++;                                       //@scan
                hi--;                                       //@scan
            }
            if (lo >= hi) return 0;                         //@already
            int a = deletions(s, n, s[lo]), b = deletions(s, n, s[hi]);    //@try
            if (a < 0 || b < 0) return a > b ? a : b;       //@pick
            return a < b ? a : b;                           //@pick
        }
    """,
}
DEL_RUN = {
    "python": """
        for s in ["abcaacab", "abccbda", "racecar", "xyzxyz"]:
            print(fewest_deletions(s))
    """,
    "java": """
        public static void main(String[] args) {
            for (String s : new String[] {"abcaacab", "abccbda", "racecar", "xyzxyz"}) System.out.println(fewestDeletions(s));
        }
    """,
    "cpp": """
        int main() {
            for (string s : {"abcaacab", "abccbda", "racecar", "xyzxyz"}) cout << fewestDeletions(s) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* tests[] = {"abcaacab", "abccbda", "racecar", "xyzxyz"};
            for (int i = 0; i < 4; i++) printf("%d\\n", fewestDeletions(tests[i]));
            return 0;
        }
    """,
}

CHG = {
    "python": """
        def changes_needed(s):
            lo, hi, changes = 0, len(s) - 1, 0              #@ends
            while lo < hi:                                  #@loop
                if s[lo] != s[hi]:                          #@pair
                    changes += 1                            #@pair
                lo, hi = lo + 1, hi - 1                     #@move
            return changes                                  #@ret
    """,
    "java": """
        static int changesNeeded(String s) {
            int lo = 0, hi = s.length() - 1, changes = 0;   //@ends
            while (lo < hi) {                               //@loop
                if (s.charAt(lo) != s.charAt(hi)) changes++;    //@pair
                lo++;                                       //@move
                hi--;                                       //@move
            }
            return changes;                                 //@ret
        }
    """,
    "cpp": """
        int changesNeeded(const string& s) {
            int lo = 0, hi = (int)s.size() - 1, changes = 0;    //@ends
            while (lo < hi) {                               //@loop
                if (s[lo] != s[hi]) changes++;              //@pair
                lo++;                                       //@move
                hi--;                                       //@move
            }
            return changes;                                 //@ret
        }
    """,
    "c": """
        int changesNeeded(const char* s) {
            int lo = 0, hi = (int)strlen(s) - 1, changes = 0;   //@ends
            while (lo < hi) {                               //@loop
                if (s[lo] != s[hi]) changes++;              //@pair
                lo++;                                       //@move
                hi--;                                       //@move
            }
            return changes;                                 //@ret
        }
    """,
}
CHG_RUN = {
    "python": """
        for s in ["abcd", "abca", "racecar", "ab"]:
            print(changes_needed(s))
    """,
    "java": """
        public static void main(String[] args) {
            for (String s : new String[] {"abcd", "abca", "racecar", "ab"}) System.out.println(changesNeeded(s));
        }
    """,
    "cpp": """
        int main() {
            for (string s : {"abcd", "abca", "racecar", "ab"}) cout << changesNeeded(s) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* tests[] = {"abcd", "abca", "racecar", "ab"};
            for (int i = 0; i < 4; i++) printf("%d\\n", changesNeeded(tests[i]));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

import itertools  # noqa: E402
import random  # noqa: E402

deletions = py(DEL["python"], "deletions")
fewest_deletions = py(DEL["python"], "fewest_deletions")
changes_needed = py(CHG["python"], "changes_needed")


def brute(s):
    if s == s[::-1]:
        return 0
    best = -1
    for c in set(s):
        idx = [i for i, ch in enumerate(s) if ch == c]
        for k in range(1, len(idx) + 1):
            if any((t := "".join(ch for i, ch in enumerate(s) if i not in rem)) == t[::-1] for rem in itertools.combinations(idx, k)):
                best = k if best < 0 else min(best, k)
                break
    return best


rng = random.Random(4)
for _ in range(1500):
    s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 8)))
    assert fewest_deletions(s) == brute(s), s
    assert changes_needed(s) == sum(s[i] != s[-1 - i] for i in range(len(s) // 2))


def del_walk(s, c, w, show_scan_note=True):
    """Add the steps of deletions(s, c) to walk w."""
    lo, hi, d = 0, len(s) - 1, 0
    st = {}
    art = "an" if c in "aefhilmnorsx" else "a"

    def panels():
        return (Row(list(s), st=dict(st), ptr={"lo": lo if lo <= hi else None, "hi": hi if hi >= lo else None}, slots=True, label="s"),
                M({"deleting only": f"'{c}'", "deleted": d}))

    while lo < hi:
        if s[lo] == s[hi]:
            st[lo] = st[hi] = "found"
            msg = f"'{s[lo]}' and '{s[hi]}' match. Keep both and move inward."
            lo, hi = lo + 1, hi - 1
        elif s[lo] == c:
            st[lo] = "dim"
            d += 1
            msg = f"'{s[lo]}' and '{s[hi]}' differ. The left one is {art} '{c}', so delete it: {d} so far."
            lo += 1
        elif s[hi] == c:
            st[hi] = "dim"
            d += 1
            msg = f"'{s[lo]}' and '{s[hi]}' differ. The right one is {art} '{c}', so delete it: {d} so far."
            hi -= 1
        else:
            st[lo] = st[hi] = "mark"
            w.step(f"'{s[lo]}' and '{s[hi]}' differ, and neither is {art} '{c}'. Deleting '{c}'s can't fix this pair: this letter doesn't work.", *panels())
            return -1
        w.step(msg, *panels())
    w.steps[-1]["text"] += f" The pointers have met: deleting {d} '{c}'{'s' if d != 1 else ''} leaves a palindrome."
    return d


# Theory walk: deletions with one fixed letter.
TS, TC = "abcaacab", "a"
tw = Steps(f"`deletions(\"{TS}\", '{TC}')`: may we delete only '{TC}'s? Compare the two ends; when they differ, delete whichever end is a '{TC}'.")
tw.step(f"Both ends in play, nothing deleted.", Row(list(TS), ptr={"lo": 0, "hi": len(TS) - 1}, slots=True, label="s"), M({"deleting only": f"'{TC}'", "deleted": 0}))
TD = del_walk(TS, TC, tw)
assert TD == deletions(TS, TC)
T_LEGEND = {"found": "kept: matches its mirror", "dim": f"deleted (a '{TC}')"}

# Trace walk: the full template, both candidates.
FS = "abccbda"
fw = Steps(f"`fewest_deletions(\"{FS}\")`. Find the first pair that differs; only those two letters are worth trying.")
lo, hi = 0, len(FS) - 1
pre = {}
while lo < hi and FS[lo] == FS[hi]:
    pre[lo] = pre[hi] = "found"
    lo, hi = lo + 1, hi - 1
CA, CB = FS[lo], FS[hi]
fw.step(f"The outer '{FS[0]}'s match, then '{CA}' and '{CB}' don't. Any fix must delete one of these two, so the letter to delete is '{CA}' or '{CB}'.",
        Row(list(FS), st={**pre, lo: "mark", hi: "mark"}, ptr={"lo": lo, "hi": hi}, slots=True, label="s"), M({"deleting only": "?", "deleted": 0}))
fw.step(f"Try '{CA}' first, starting again from the ends.", Row(list(FS), ptr={"lo": 0, "hi": len(FS) - 1}, slots=True, label="s"), M({"deleting only": f"'{CA}'", "deleted": 0}))
RA = del_walk(FS, CA, fw)
fw.step(f"Now try '{CB}'.", Row(list(FS), ptr={"lo": 0, "hi": len(FS) - 1}, slots=True, label="s"), M({"deleting only": f"'{CB}'", "deleted": 0}))
RB = del_walk(FS, CB, fw)
ANS = fewest_deletions(FS)
fw.steps[-1]["text"] += (f" Only '{CB if RA < 0 else CA}' worked, so the answer is {ANS}." if min(RA, RB) < 0 else f" Both worked; the answer is the smaller: {ANS}.")
assert (RA, RB) == (deletions(FS, CA), deletions(FS, CB))
F_LEGEND = {"found": "kept: matches its mirror", "dim": "deleted", "mark": "a pair that differs"}

# Example: a number, reversed half way.
NUM = 12321
half, x = 0, NUM
while x > half:
    half = half * 10 + x % 10
    x //= 10
NUM_OK = x == half or x == half // 10

VARIANTS = [
    ("the whole string, as is", "compare ends, move both inward"),
    ("only some characters count", "skip characters that don't count, on each side, before comparing"),
    ("one deletion allowed (anywhere)", "at the first mismatch, try skipping the left one or the right one"),
    ("delete copies of one letter", "the letter must be one of the first mismatched pair (template)"),
    ("change letters", "count the mismatched pairs (variation)"),
]

lesson(
    "strings",
    "palindrome-checks",
    """
    A palindrome check compares the first character with the last, the second with the second last, and so on.
    The variations come from what happens at a mismatch: skip a character that doesn't count, allow one deletion, or
    count what would need changing. Each one is still a single pass with two pointers moving inward.
    """,
    [
        ("idea", "The idea", [
            f"""
            Hold a word up to a mirror down its middle. The first letter faces the last, the second faces the second
            last. If every facing pair matches, it's a palindrome. You never need more than one look at each pair, so
            that's half the word's length in comparisons.

            Most palindrome questions are that check plus a rule for mismatches. "Ignore punctuation" says to skip
            some characters before comparing. "Allow one typo" says a mismatch can be forgiven once. "Delete some copies
            of one letter" says a mismatch can be fixed only by removing that letter. The pointers still only move
            inward, so it's still O(n).
            """,
            fig(Row(list("racecar"), st={0: "found", 6: "found", 1: "active", 5: "active", 3: "mark"}, slots=True, label="pairs, from the outside in"),
                caption="Facing pairs are compared; the middle letter of an odd-length word faces itself."),
            key("""
            `lo = 0`, `hi = n - 1`. While `lo < hi`: if the characters match, move both inward; otherwise apply the
            question's rule for a mismatch (skip, forgive once, delete, count). The rule is the only part that changes.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The question asks whether a string is (or can become) a palindrome, under some rule: ignoring certain
            characters, with a limited number of deletions or changes, or after removing some letter.
            """,
            table(["the rule", "what happens at a mismatch"], *VARIANTS),
            """
            Not a fit:

            - The *longest* palindromic substring, or counting them. That's *Expand around center*.
            - Can the letters be rearranged into a palindrome? Order doesn't matter there: count letters (*Anagrams and
              signatures*).
            - Many deletions allowed anywhere ("fewest deletions to make a palindrome"). That's the longest palindromic
              subsequence, a dynamic programming problem.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Matching pairs can be kept

            When `s[lo] == s[hi]`, keeping both as a mirrored pair is never worse than removing either. If some solution
            removed one of them, the remaining copy would need a partner somewhere else, and pairing the two outermost
            equal characters leaves the most room inside. So a match always means "move both inward".

            ### The first mismatch narrows the choices

            Scan from the ends until the first pair that differs, `s[lo]` and `s[hi]`. Everything outside it already
            matches. To fix this pair, at least one of the two characters must go. So if the rule is "delete copies of one
            chosen letter", that letter must be `s[lo]` or `s[hi]`. Instead of trying all 26 letters, try two.

            ### Deleting one letter, greedily

            With the letter `c` fixed, walk from the ends again. A match is kept. A mismatch where one end is `c` deletes
            that end; it has to go, since it can't pair with the other. A mismatch where neither end is `c` can't be
            fixed, so `c` doesn't work. Every deletion is forced, so the count is the fewest for that letter.
            """,
            walk(tw, legend=T_LEGEND),
            """
            ### Changing letters instead of deleting

            If you may change any letter, each mismatched pair needs exactly one change (make one side equal the other),
            and matched pairs need none. So the fewest changes is the number of mismatched facing pairs. No search is
            needed at all.
            """,
        ]),
        ("template", "The template", [
            """
            Choose one letter and delete some of its copies (possibly none) so that `s` becomes a palindrome. What's the
            fewest deletions? Return -1 if no letter works.
            """,
            code(
                "Fewest deletions of one chosen letter",
                DEL,
                [
                    ("ends", "Both ends, and nothing deleted yet."),
                    ("loop", "Until the pointers meet."),
                    ("match", "Equal ends stay as a mirrored pair."),
                    ("left", "They differ and the left one is the chosen letter: it has to go."),
                    ("right", "They differ and the right one is the chosen letter: it has to go."),
                    ("stuck", "They differ and neither is the chosen letter. No amount of deleting it helps."),
                    ("count", "The deletions this letter needs."),
                    ("scan", "Skip the matching outer pairs to find the first mismatch."),
                    ("already", "No mismatch: it's already a palindrome."),
                    ("try", "The letter to delete must be one of the two that differ. Try both."),
                    ("pick", "If one failed, take the other (or -1 if both did). Otherwise the smaller."),
                ],
                DEL_RUN,
                'fewest_deletions("abcaacab"); ("abccbda"); ("racecar"); ("xyzxyz")',
            ),
            """
            `"xyzxyz"` fails with either candidate, so no letter works. `"racecar"` needs nothing.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "The second example, with both candidate letters:",
            walk(fw, legend=F_LEGEND),
            """
            On paper, connect each kept pair with an arc and cross out each deleted letter. Arcs never cross, and every
            letter is either inside an arc pair, crossed out, or the single middle letter.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Skipping what doesn't count

            "A man, a plan, a canal: Panama" is a palindrome if you ignore everything but letters and compare letters
            without case. Before comparing, move `lo` right past characters that don't count, and `hi` left past them
            too (both moves guarded by `lo < hi`). Then compare in lowercase. Nothing is copied, so it stays O(1) space.

            ### Numbers without strings

            Is {NUM} a palindrome? Reverse its *second half* arithmetically: peel digits off the end into a new number
            until the new number is at least the remaining one. For {NUM} that leaves 12 and 123; dropping the middle digit
            (`123 // 10 = 12`) gives a match, so it {"is" if NUM_OK else "isn't"}. Reversing only half avoids overflow,
            and negative numbers are never palindromes because of the sign.

            ### One deletion anywhere

            If any single character may be deleted, the first mismatch still decides: delete the left one or the right
            one, and check whether the rest between them is a palindrome. Two plain checks, so O(n). Allowing more
            deletions makes the choices branch, and it becomes dynamic programming.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Changes instead of deletions

            Each mismatched facing pair costs exactly one change, so count them.
            """,
            code(
                "Fewest letter changes to make a palindrome",
                CHG,
                [
                    ("ends", "Both ends, and no changes yet."),
                    ("loop", "Each facing pair once."),
                    ("pair", "A mismatched pair needs one change: set either letter to the other."),
                    ("move", "Both pointers move inward every time; nothing is skipped."),
                    ("ret", "The number of mismatched pairs."),
                ],
                CHG_RUN,
                'changes_needed("abcd"); ("abca"); ("racecar"); ("ab")',
            ),
            """
            "Can it become a palindrome with at most `k` changes?" is then `changes_needed(s) <= k`. To get the *smallest*
            such palindrome in dictionary order, change each mismatched pair to the smaller of its two letters.

            ### Palindromes across two strings

            Some questions glue a prefix of one string to a suffix of another. Compare from the outside in, one pointer in
            each string, until the first mismatch; whatever's left in the middle must be a palindrome on its own, in one
            string or the other. Still two pointers, still O(n).

            ### Linked lists

            A singly linked list can't walk backwards, so find the middle (fast and slow pointers), reverse the second
            half, and compare the two halves front to front. Reverse it back afterwards if the caller needs the list.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            A plain check is at most `n / 2` comparisons: O(n) time, O(1) space. The template runs one scan plus at most
            two full checks: still O(n). Counting changes is one pass. Building a reversed copy and comparing would also
            be O(n) time, but O(n) extra space.
            """,
            table(
                ["Task", "Time", "Extra space"],
                ["Is it a palindrome?", "O(n)", "O(1)"],
                ["Ignoring some characters", "O(n)", "O(1)"],
                ["One deletion anywhere", "O(n)", "O(1)"],
                ["Delete copies of one letter (template)", "O(n)", "O(1)"],
                ["Fewest changes", "O(n)", "O(1)"],
                ["Fewest deletions, any letters", "O(n²) (dynamic programming)", "O(n) to O(n²)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `s == s[::-1]` checks a whole string in one line, with an O(n) copy. For the two-pointer versions, index
            directly. `ch.isalnum()` and `ch.lower()` handle skipping and case.

            ### Java

            `charAt` and `Character.isLetterOrDigit` / `Character.toLowerCase`. `new StringBuilder(s).reverse()` makes a
            reversed copy if you want the one-line version.

            ### C++

            `std::equal(s.begin(), s.begin() + s.size() / 2, s.rbegin())` compares the first half with the reversed second
            half. `isalnum` and `tolower` take `unsigned char` values.

            ### C

            Two indices into the `char` array, `strlen` once. `isalnum` and `tolower` from `<ctype.h>`, with a cast to
            `unsigned char`.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Moving only one pointer on a match.
            - Skipping characters without checking `lo < hi`, which can run a pointer past the other or off the string.
            - Trying all 26 letters when the first mismatch already names the two candidates (correct, but wasteful).
            - Treating -1 ("impossible") as a small number when taking the minimum of two answers.
            - Empty strings and single characters: both are palindromes.
            - Comparing characters of different case or type without normalising them first.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why is it safe to keep a matching pair instead of considering deleting one of them?",
                 "The two outermost equal characters can always serve as a mirrored pair. Any solution that deletes one of them can keep it instead, pairing it with the other, without needing more deletions inside."),
                ("Why only two candidate letters in `fewest_deletions`?",
                 "Everything outside the first mismatched pair already matches. At least one of the two mismatched characters must be deleted, so the chosen letter has to be one of them."),
                ("deletions(\"abca\", 'b'): what happens?",
                 "a and a match. Then b and c differ; the left is a b, so it's deleted (1). The pointers meet on c: one deletion gives \"aca\"."),
                ("changes_needed(\"abcde\")?",
                 "2: the pairs (a, e) and (b, d) differ; c is the middle."),
                ("How do you check that 1221 is a palindrome without converting it to a string?",
                 "Peel digits off the end into a reversed number until it's at least what's left: 12 and 12. They're equal, so yes. (For odd lengths, drop the middle digit from the reversed half first.)"),
            ),
        ]),
    ],
)
