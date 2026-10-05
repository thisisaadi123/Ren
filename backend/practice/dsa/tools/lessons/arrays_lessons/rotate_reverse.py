"""Lesson: Rotate and reverse in place (Arrays & Hashing, pattern 13)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

ROT = {
    "python": """
        def reverse(a, lo, hi):
            while lo < hi:                          #@rev
                a[lo], a[hi] = a[hi], a[lo]         #@rev
                lo, hi = lo + 1, hi - 1             #@rev


        def rotate_left(a, k):
            n = len(a)                              #@n
            if n == 0:                              #@n
                return a                            #@n
            k %= n                                  #@mod
            reverse(a, 0, k - 1)                    #@first
            reverse(a, k, n - 1)                    #@second
            reverse(a, 0, n - 1)                    #@all
            return a                                #@ret
    """,
    "java": """
        static void reverse(int[] a, int lo, int hi) {
            while (lo < hi) {                       //@rev
                int t = a[lo];                      //@rev
                a[lo++] = a[hi];                    //@rev
                a[hi--] = t;                        //@rev
            }
        }

        static int[] rotateLeft(int[] a, int k) {
            int n = a.length;                       //@n
            if (n == 0) return a;                   //@n
            k %= n;                                 //@mod
            reverse(a, 0, k - 1);                   //@first
            reverse(a, k, n - 1);                   //@second
            reverse(a, 0, n - 1);                   //@all
            return a;                               //@ret
        }
    """,
    "cpp": """
        vector<int>& rotateLeft(vector<int>& a, int k) {
            int n = a.size();                       //@n
            if (n == 0) return a;                   //@n
            k %= n;                                 //@mod
            reverse(a.begin(), a.begin() + k);      //@first
            reverse(a.begin() + k, a.end());        //@second
            reverse(a.begin(), a.end());            //@all
            return a;                               //@ret
        }
    """,
    "c": """
        static void reverse(int* a, int lo, int hi) {
            while (lo < hi) {                       //@rev
                int t = a[lo];                      //@rev
                a[lo++] = a[hi];                    //@rev
                a[hi--] = t;                        //@rev
            }
        }

        void rotateLeft(int* a, int n, int k) {
            if (n == 0) return;                     //@n
            k %= n;                                 //@mod
            reverse(a, 0, k - 1);                   //@first
            reverse(a, k, n - 1);                   //@second
            reverse(a, 0, n - 1);                   //@all
        }
    """,
}
ROT_RUN = {
    "python": """
        print(*rotate_left([1, 2, 3, 4, 5, 6, 7], 3))
        print(*rotate_left([1, 2, 3, 4, 5], 7))
        print(*rotate_left([9], 4))
    """,
    "java": """
        static void show(int[] a) {
            StringBuilder sb = new StringBuilder();
            for (int x : a) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
        }

        public static void main(String[] args) {
            show(rotateLeft(new int[] {1, 2, 3, 4, 5, 6, 7}, 3));
            show(rotateLeft(new int[] {1, 2, 3, 4, 5}, 7));
            show(rotateLeft(new int[] {9}, 4));
        }
    """,
    "cpp": """
        void show(const vector<int>& a) {
            for (size_t i = 0; i < a.size(); i++) cout << (i ? " " : "") << a[i];
            cout << "\\n";
        }

        int main() {
            vector<int> a = {1, 2, 3, 4, 5, 6, 7}, b = {1, 2, 3, 4, 5}, c = {9};
            show(rotateLeft(a, 3));
            show(rotateLeft(b, 7));
            show(rotateLeft(c, 4));
        }
    """,
    "c": """
        static void show(const int* a, int n) {
            for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
        }

        int main(void) {
            int a[] = {1, 2, 3, 4, 5, 6, 7}, b[] = {1, 2, 3, 4, 5}, c[] = {9};
            rotateLeft(a, 7, 3);
            rotateLeft(b, 5, 7);
            rotateLeft(c, 1, 4);
            show(a, 7);
            show(b, 5);
            show(c, 1);
            return 0;
        }
    """,
}

WORDS = {
    "python": """
        def reverse(a, lo, hi):
            while lo < hi:                          #@rev
                a[lo], a[hi] = a[hi], a[lo]         #@rev
                lo, hi = lo + 1, hi - 1             #@rev


        def reverse_words(s):
            chars = list(s)                         #@chars
            reverse(chars, 0, len(chars) - 1)       #@all
            start = 0                               #@scan
            for i in range(len(chars) + 1):         #@scan
                if i == len(chars) or chars[i] == " ":  #@end
                    reverse(chars, start, i - 1)    #@word
                    start = i + 1                   #@next
            return "".join(chars)                   #@ret
    """,
    "java": """
        static void reverse(char[] a, int lo, int hi) {
            while (lo < hi) {                       //@rev
                char t = a[lo];                     //@rev
                a[lo++] = a[hi];                    //@rev
                a[hi--] = t;                        //@rev
            }
        }

        static String reverseWords(String s) {
            char[] chars = s.toCharArray();         //@chars
            int n = chars.length;                   //@chars
            reverse(chars, 0, n - 1);               //@all
            int start = 0;                          //@scan
            for (int i = 0; i <= n; i++) {          //@scan
                if (i == n || chars[i] == ' ') {    //@end
                    reverse(chars, start, i - 1);   //@word
                    start = i + 1;                  //@next
                }
            }
            return new String(chars);               //@ret
        }
    """,
    "cpp": """
        string& reverseWords(string& s) {
            reverse(s.begin(), s.end());            //@all
            size_t start = 0;                       //@scan
            for (size_t i = 0; i <= s.size(); i++) {    //@scan
                if (i == s.size() || s[i] == ' ') { //@end
                    reverse(s.begin() + start, s.begin() + i);  //@word
                    start = i + 1;                  //@next
                }
            }
            return s;                               //@ret
        }
    """,
    "c": """
        static void reverse(char* a, int lo, int hi) {
            while (lo < hi) {                       //@rev
                char t = a[lo];                     //@rev
                a[lo++] = a[hi];                    //@rev
                a[hi--] = t;                        //@rev
            }
        }

        void reverseWords(char* s) {
            int n = strlen(s);                      //@chars
            reverse(s, 0, n - 1);                   //@all
            int start = 0;                          //@scan
            for (int i = 0; i <= n; i++) {          //@scan
                if (i == n || s[i] == ' ') {        //@end
                    reverse(s, start, i - 1);       //@word
                    start = i + 1;                  //@next
                }
            }
        }
    """,
}
WORDS_RUN = {
    "python": """
        print(reverse_words("the sky is blue"))
        print(reverse_words("hello"))
        print(reverse_words("a b"))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(reverseWords("the sky is blue"));
            System.out.println(reverseWords("hello"));
            System.out.println(reverseWords("a b"));
        }
    """,
    "cpp": """
        int main() {
            for (string s : {"the sky is blue", "hello", "a b"}) cout << reverseWords(s) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            char a[] = "the sky is blue", b[] = "hello", c[] = "a b";
            reverseWords(a);
            reverseWords(b);
            reverseWords(c);
            printf("%s\\n%s\\n%s\\n", a, b, c);
            return 0;
        }
    """,
}

CYC = {
    "python": """
        def gcd(a, b):
            while b:                                #@gcd
                a, b = b, a % b                     #@gcd
            return a                                #@gcd


        def rotate_left_cycles(a, k):
            n = len(a)                              #@n
            if n == 0:                              #@n
                return a                            #@n
            k %= n                                  #@mod
            for start in range(gcd(n, k)):          #@cycles
                carry = a[start]                    #@carry
                i = start                           #@carry
                while True:                         #@walk
                    j = (i + k) % n                 #@from
                    if j == start:                  #@close
                        break                       #@close
                    a[i] = a[j]                     #@pull
                    i = j                           #@pull
                a[i] = carry                        #@drop
            return a                                #@ret
    """,
    "java": """
        static int gcd(int a, int b) {
            while (b != 0) {                        //@gcd
                int t = a % b;                      //@gcd
                a = b;                              //@gcd
                b = t;                              //@gcd
            }
            return a;                               //@gcd
        }

        static int[] rotateLeftCycles(int[] a, int k) {
            int n = a.length;                       //@n
            if (n == 0) return a;                   //@n
            k %= n;                                 //@mod
            for (int start = 0; start < gcd(n, k); start++) {   //@cycles
                int carry = a[start], i = start;    //@carry
                while (true) {                      //@walk
                    int j = (i + k) % n;            //@from
                    if (j == start) break;          //@close
                    a[i] = a[j];                    //@pull
                    i = j;                          //@pull
                }
                a[i] = carry;                       //@drop
            }
            return a;                               //@ret
        }
    """,
    "cpp": """
        vector<int>& rotateLeftCycles(vector<int>& a, int k) {
            int n = a.size();                       //@n
            if (n == 0) return a;                   //@n
            k %= n;                                 //@mod
            for (int start = 0; start < gcd(n, k); start++) {   //@cycles
                int carry = a[start], i = start;    //@carry
                while (true) {                      //@walk
                    int j = (i + k) % n;            //@from
                    if (j == start) break;          //@close
                    a[i] = a[j];                    //@pull
                    i = j;                          //@pull
                }
                a[i] = carry;                       //@drop
            }
            return a;                               //@ret
        }
    """,
    "c": """
        static int gcd(int a, int b) {
            while (b != 0) {                        //@gcd
                int t = a % b;                      //@gcd
                a = b;                              //@gcd
                b = t;                              //@gcd
            }
            return a;                               //@gcd
        }

        void rotateLeftCycles(int* a, int n, int k) {
            if (n == 0) return;                     //@n
            k %= n;                                 //@mod
            for (int start = 0; start < gcd(n, k); start++) {   //@cycles
                int carry = a[start], i = start;    //@carry
                while (true) {                      //@walk
                    int j = (i + k) % n;            //@from
                    if (j == start) break;          //@close
                    a[i] = a[j];                    //@pull
                    i = j;                          //@pull
                }
                a[i] = carry;                       //@drop
            }
        }
    """,
}
CYC_RUN = {
    "python": """
        print(*rotate_left_cycles([1, 2, 3, 4, 5, 6], 2))
        print(*rotate_left_cycles([1, 2, 3, 4, 5, 6, 7], 3))
    """,
    "java": """
        static void show(int[] a) {
            StringBuilder sb = new StringBuilder();
            for (int x : a) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
        }

        public static void main(String[] args) {
            show(rotateLeftCycles(new int[] {1, 2, 3, 4, 5, 6}, 2));
            show(rotateLeftCycles(new int[] {1, 2, 3, 4, 5, 6, 7}, 3));
        }
    """,
    "cpp": """
        void show(const vector<int>& a) {
            for (size_t i = 0; i < a.size(); i++) cout << (i ? " " : "") << a[i];
            cout << "\\n";
        }

        int main() {
            vector<int> a = {1, 2, 3, 4, 5, 6}, b = {1, 2, 3, 4, 5, 6, 7};
            show(rotateLeftCycles(a, 2));
            show(rotateLeftCycles(b, 3));
        }
    """,
    "c": """
        static void show(const int* a, int n) {
            for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
        }

        int main(void) {
            int a[] = {1, 2, 3, 4, 5, 6}, b[] = {1, 2, 3, 4, 5, 6, 7};
            rotateLeftCycles(a, 6, 2);
            rotateLeftCycles(b, 7, 3);
            show(a, 6);
            show(b, 7);
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

rotate_left = py(ROT["python"], "rotate_left")
reverse_words = py(WORDS["python"], "reverse_words")
rotate_left_cycles = py(CYC["python"], "rotate_left_cycles")

DEMO, K = [1, 2, 3, 4, 5, 6, 7], 3
N = len(DEMO)
OUT = rotate_left(list(DEMO), K)
assert OUT == DEMO[K:] + DEMO[:K]
A_ST = {i: "found" for i in range(K)}
B_ST = {i: "mark" for i in range(K, N)}

# Block picture: where each block ends up after each reversal.
blk = {v: ("found" if v <= K else "mark") for v in DEMO}


def by_value(arr):
    return {i: blk[v] for i, v in enumerate(arr)}


S1 = DEMO[:K][::-1] + DEMO[K:]
S2 = DEMO[:K][::-1] + DEMO[K:][::-1]
S3 = S2[::-1]
assert S3 == OUT

# Swap-by-swap walkthrough.
rw = Steps(f"`rotate_left({DEMO}, {K})`: the first {K} values move to the back. Three reversals, all swaps.")
arr = list(DEMO)
rw.step(f"Call the first {K} values A and the other {N - K} B. We want B then A.", Row(arr, st=by_value(arr), slots=True), M({"A": "1 2 3", "B": "4 5 6 7"}))
swaps = 0
for name, lo0, hi0 in [("A (indices 0 to 2)", 0, K - 1), ("B (indices 3 to 6)", K, N - 1), ("the whole array", 0, N - 1)]:
    lo, hi = lo0, hi0
    first = True
    while lo < hi:
        arr[lo], arr[hi] = arr[hi], arr[lo]
        swaps += 1
        msg = (f"Reverse {name}. " if first else "") + f"Swap indices {lo} and {hi}" + (", then move both ends inwards." if lo + 1 < hi - 1 else ". The ends have met: this reversal is done.")
        rw.step(msg, Row(list(arr), st={**by_value(arr), lo: "active", hi: "active"}, ptr={"lo": lo, "hi": hi}, slots=True), M({"swaps": swaps}))
        first = False
        lo, hi = lo + 1, hi - 1
rw.steps[-1]["text"] += f" B is at the front and A at the back, each in its original order: {' '.join(map(str, arr))}."
assert arr == OUT

# Where index i goes.
WHERE = [(str(i), str(DEMO[i]), str((i - K) % N)) for i in range(N)]

# Words.
SENT = "the sky is blue"
SENT_OUT = reverse_words(SENT)
assert SENT_OUT == "blue is sky the"


def chars(s):
    return [("␣" if ch == " " else ch) for ch in s]


ww = Steps(f"`reverse_words(\"{SENT}\")`. Reverse everything, then put each word back the right way round.")
cs = list(SENT)
ww.step("The sentence as an array of characters (␣ is a space).", Row(chars(cs), slots=True))
cs.reverse()
ww.step("Reverse the whole thing. The words are now in the right order, but each one is spelled backwards.", Row(chars(cs), slots=True))
start = 0
for i in range(len(cs) + 1):
    if i == len(cs) or cs[i] == " ":
        word_before = "".join(cs[start:i])
        cs[start:i] = cs[start:i][::-1]
        ww.step(f"Indices {start} to {i - 1} hold \"{word_before}\". Reverse just that word: \"{''.join(cs[start:i])}\".",
                Row(chars(cs), st={k: "found" for k in range(start, i)}, slots=True))
        start = i + 1
assert "".join(cs) == SENT_OUT
ww.steps[-1]["text"] += f" Done: \"{SENT_OUT}\"."

# Cycles: n = 6, k = 2 gives gcd 2, so two cycles of three.
CN, CK = 6, 2
CA = list(range(1, CN + 1))
COUT = rotate_left_cycles(list(CA), CK)
assert COUT == CA[CK:] + CA[:CK]
cw = Steps(f"`rotate_left_cycles({CA}, {CK})`. Each slot pulls its value from {CK} places to its right, round the end.")
a = list(CA)
cw.step(f"After a left rotation by {CK}, slot i holds what was at (i + {CK}) mod {CN}. Following that rule from slot 0 visits 0 → 2 → 4 → 0: a cycle. gcd({CN}, {CK}) = 2, so there are 2 cycles.",
        Row(a, st={0: "found", 2: "found", 4: "found", 1: "mark", 3: "mark", 5: "mark"}, slots=True))


def g(x, y):
    while y:
        x, y = y, x % y
    return x


for s in range(g(CN, CK)):
    carry, i = a[s], s
    cw.step(f"Cycle starting at slot {s}: pick up {carry} so slot {s} is free.", Row(list(a), st={s: "dim"}, ptr={"i": s}, slots=True), M({"carrying": carry}))
    while True:
        j = (i + CK) % CN
        if j == s:
            break
        a[i] = a[j]
        cw.step(f"Slot {i} pulls {a[j]} from slot {j}. Now slot {j} is the free one.", Row(list(a), st={i: "new", j: "dim"}, ptr={"i": i, "j": j}, slots=True), M({"carrying": carry}))
        i = j
    a[i] = carry
    cw.step(f"The next slot to pull from would be slot {s}, where we started. Drop the carried {carry} into slot {i}. This cycle is done.",
            Row(list(a), st={i: "new"}, slots=True), M({"carrying": "nothing"}))
assert a == COUT

# Swap counts for both methods.
COUNT_ROWS = []
for n_, k_ in [(7, 3), (6, 2), (10, 4), (12, 5)]:
    rev_swaps = k_ // 2 + (n_ - k_) // 2 + n_ // 2
    COUNT_ROWS.append((f"n = {n_}, k = {k_}", f"{rev_swaps} swaps ({3 * rev_swaps} writes)", f"{n_ + g(n_, k_)} writes ({g(n_, k_)} cycle{'s' if g(n_, k_) > 1 else ''})"))

lesson(
    "arrays-hashing",
    "rotate-reverse",
    """
    Reversing a stretch of an array in place is easy: swap the two ends and walk inwards. Three of those reversals
    rotate an array by any amount with O(1) extra space, and the same trick reorders words, swaps two blocks of
    different lengths, and shows up inside harder algorithms.
    """,
    [
        ("idea", "The idea", [
            """
            Write the word ROTATION on a strip of paper and suppose you want to move the first three letters to the
            end: ATIONROT. The obvious way is to cut ROT off, slide the rest along, and tape ROT back on, which needs a
            spare place to hold ROT. With an array, that spare place is extra memory.

            Here's a way with no spare place at all. Flip the first three letters around (TOR), flip the rest around
            (NOITA), and then flip the whole strip. The two pieces swap ends, and the final flip also puts each piece
            back the right way round. Every flip is just swapping letters from the outside in.
            """,
            fig(Row(DEMO, st=by_value(DEMO), slots=True, label="A = 1 2 3, B = 4 5 6 7"),
                Row(S1, st=by_value(S1), slots=True, label="reverse A"),
                Row(S2, st=by_value(S2), slots=True, label="reverse B"),
                Row(S3, st=by_value(S3), slots=True, label="reverse everything"),
                caption="Three reversals turn A B into B A. Nothing is copied anywhere else."),
            key("""
            To rotate left by `k`: reverse the first `k`, reverse the rest, reverse the whole array. Each reversal swaps
            the ends and moves inwards. Take `k % n` first. It's O(n) time and O(1) extra space.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            "Rotate the array by k", "shift every element k places, wrapping round", "move the last k to the front",
            "reverse the order of the words", "swap these two blocks", usually with "in place" or "O(1) extra space".

            More generally: whenever two adjacent blocks need to trade places, that's a rotation, and a rotation is three
            reversals. You'll also see a single reversal of a *suffix* as the last step of other algorithms (the next
            lesson, *Next permutation*, ends with one).

            Not a fit:

            - Extra memory is allowed and you want the simplest code. Building `a[k:] + a[:k]` into a new array is
              clearer and just as fast.
            - The rotation happens again and again, and you only need to *read* the rotated array. Don't move anything;
              keep an offset and read `a[(i + k) % n]`.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Reversing a joined-up array

            Write `X'` for "X reversed". If you reverse two blocks stuck together, `(X Y)'`, the last element comes
            first, so `Y`'s elements come out first, backwards, then `X`'s, backwards: `(X Y)' = Y' X'`. The blocks
            swap order *and* each one is flipped.

            Rotation wants the blocks swapped but *not* flipped. So flip each one in advance, and the big reversal
            flips them back:

            > `(A' B')' = (B')' (A')' = B A`

            ### Where every element ends up

            After rotating left by `k`, the value that was at index `i` is at index `(i - k) mod n`. Equivalently, index
            `i` now holds what used to be at `(i + k) mod n`. For `{DEMO}` with `k = {K}`:
            """.replace("{DEMO}", str(DEMO)).replace("{K}", str(K)),
            table(["was at index", "value", "now at index"], *WHERE),
            """
            A right rotation by `k` moves everything the other way, which is the same as a left rotation by `n - k`.

            ### k can be bigger than n

            Rotating by `n` puts every element back where it was. So rotating by `k` is the same as rotating by
            `k % n`. Without that line, `k > n` sends the first reversal off the end of the array. With `k % n == 0`,
            the first reversal covers nothing and the other two undo each other: the array is unchanged, as it should
            be.

            ### Reversing a stretch

            `lo` and `hi` start at the two ends. Swap them, step both inwards, and stop when they meet or cross. A stretch
            of length `L` takes `L / 2` swaps (rounded down; the middle of an odd stretch stays put). The loop condition
            `lo < hi` also handles empty stretches: reversing `0..-1` does nothing.
            """,
        ]),
        ("template", "The template", [
            "Rotate left by `k`, in place.",
            code(
                "Rotate with three reversals",
                ROT,
                [
                    ("rev", "Reverse `a[lo..hi]`: swap the ends and walk inwards until they meet."),
                    ("n", "An empty array has nothing to rotate (and `k % 0` would fail).",
                     {"c": "C gets the length from the caller."}),
                    ("mod", "Rotating by `n` changes nothing, so only `k % n` matters."),
                    ("first", "Flip block A, the first `k` values.",
                     {"cpp": "`std::reverse` takes a half-open range `[first, last)`, so the end is `begin() + k`, not `k - 1`."}),
                    ("second", "Flip block B, the remaining `n - k`."),
                    ("all", "Flip everything. The blocks trade places and each is the right way round again."),
                    ("ret", "The rotated array (the same array, changed in place)."),
                ],
                ROT_RUN,
                "rotate_left([1, 2, 3, 4, 5, 6, 7], 3); ([1, 2, 3, 4, 5], 7); ([9], 4)",
            ),
            """
            `k = 7` on five values behaves like `k = 2`. A single value rotates to itself however big `k` is.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "Every swap, with A in one colour and B in another:",
            walk(rw),
        ]),
        ("examples", "More examples", [
            f"""
            ### Reversing the words of a sentence

            "`{SENT}`" should become "`{SENT_OUT}`". The words are blocks, and you want the blocks in reverse order but
            each block still readable. That's the rotation trick, the other way round: reverse the whole sentence
            first (the words land in the right order, each spelled backwards), then reverse each word.
            """,
            walk(ww),
            """
            ### Moving one element

            Taking the element at index `i` and inserting it at index `j > i` shifts everything in between one place
            left. That's a left rotation by 1 of the stretch `a[i..j]`, so three reversals of that stretch do it. (For a
            single move, a plain loop shifting values one place is simpler. The rotation view pays off for big blocks.)

            ### Swapping two blocks that aren't next to each other

            To swap blocks `X` and `Z` in `X Y Z` (with `Y` in between), reverse each of the three, then reverse the
            whole thing: `(X' Y' Z')' = Z Y X`. The middle block ends up the right way round too.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Reverse the words

            The example above as code. Here words are separated by single spaces. If there can be extra spaces, squeeze
            them out first (a write pointer copying characters forward), then do the same thing.
            """,
            code(
                "Reverse the order of words in place",
                WORDS,
                [
                    ("rev", "The same in-place reversal as before, on characters."),
                    ("chars", "Python and Java strings can't be changed, so work on an array of characters.",
                     {"c": "C strings are already arrays of characters ending in `'\\0'`, so this works on the caller's buffer directly."}),
                    ("all", "Reverse the whole sentence. Words are now in the right order, spelled backwards."),
                    ("scan", "Walk through, remembering where the current word started. Going one past the end lets the "
                             "last word be handled like the others."),
                    ("end", "A space, or the end of the string, closes the current word."),
                    ("word", "Turn this one word back the right way round.",
                     {"cpp": "Half-open again: `begin() + i` is one past the word's last character."}),
                    ("next", "The next word starts after the space."),
                    ("ret", "The sentence with its words reversed."),
                ],
                WORDS_RUN,
                "reverse_words(\"the sky is blue\"); (\"hello\"); (\"a b\")",
            ),
            """
            ### Rotation by cycles

            There's a second O(1)-space way to rotate, using the cycle idea from *Cyclic sort*. After rotating left by
            `k`, slot `i` should hold the value from slot `(i + k) % n`. Pick up the value in slot 0, then let slot 0
            pull from slot `k`, slot `k` pull from slot `2k`, and so on round the end, until the next pull would be from
            slot 0 again; drop the carried value there. That's one cycle. There are exactly `gcd(n, k)` cycles, each of
            length `n / gcd(n, k)`, starting at slots `0, 1, …, gcd - 1`.
            """,
            walk(cw),
            code(
                "Rotate by following cycles",
                CYC,
                [
                    ("gcd", "Euclid's algorithm: the number of separate cycles."),
                    ("n", "Nothing to rotate in an empty array."),
                    ("mod", "Only `k % n` matters."),
                    ("cycles", "One cycle starts at each of the first `gcd(n, k)` slots.",
                     {"cpp": "`std::gcd` (from `<numeric>`, C++17) does Euclid's algorithm for us."}),
                    ("carry", "Pick up the value at the start, freeing that slot."),
                    ("walk", "Go round the cycle."),
                    ("from", "The slot that the free slot `i` should pull from."),
                    ("close", "If that's the start, the cycle is complete."),
                    ("pull", "Move the value into the free slot; the slot it came from is now free."),
                    ("drop", "The last free slot gets the value picked up at the start."),
                    ("ret", "The rotated array."),
                ],
                CYC_RUN,
                "rotate_left_cycles([1, 2, 3, 4, 5, 6], 2); ([1, 2, 3, 4, 5, 6, 7], 3)",
            ),
            """
            The cycle version writes each slot once (plus one extra write per cycle), while the reversal version does
            about `n` swaps, which is about `3n` writes. In practice the reversals are usually just as fast, because they
            walk memory in order, and they're much harder to get wrong. The cycle version is worth knowing, but the
            reversals are the one to write.
            """,
            table(["", "three reversals", "cycles"], *COUNT_ROWS),
        ]),
        ("complexity", "What it costs", [
            """
            The three reversals do `⌊k / 2⌋ + ⌊(n - k) / 2⌋ + ⌊n / 2⌋` swaps, which is about `n`. So O(n) time, O(1) extra
            space: two indices and a temporary. The cycle method is also O(n) time and O(1) space. Copying into a new
            array is O(n) time but O(n) space.
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Shift by one, k times", "O(n·k)", "O(1)"],
                ["Copy into a new array", "O(n)", "O(n)"],
                ["Three reversals", "O(n)", "O(1)"],
                ["Follow the gcd(n, k) cycles", "O(n)", "O(1)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            Slicing makes a rotated copy in one line: `a[k:] + a[:k]`. To change the list in place with that, assign to
            the full slice: `a[:] = a[k:] + a[:k]` (O(n) extra space, but often fine). `a[lo:hi + 1] = a[lo:hi + 1][::-1]`
            reverses a stretch. `collections.deque.rotate(-k)` rotates a deque left by `k`.

            ### Java

            No built-in reverse for `int[]`; write the two-index loop. For a `List`, `Collections.reverse` and
            `Collections.rotate(list, distance)` exist (positive distance rotates right).

            ### C++

            `std::reverse(first, last)` on half-open ranges, and `std::rotate(first, middle, last)` does a whole left
            rotation, making `middle` the new first element. Mind the half-open ends: reversing indices `lo..hi` is
            `reverse(a.begin() + lo, a.begin() + hi + 1)`.

            ### C

            Write the reversal with two indices and a temporary. `%` with a negative left side gives a negative result
            in C, so if `k` can be negative, use `((k % n) + n) % n`.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Forgetting `k %= n`. With `k > n` the first reversal runs off the end.
            - An empty array and `k % 0`. Check `n == 0` first.
            - Reversing in the wrong order for the direction you want. Draw A and B, and check which block should end up
              in front.
            - Off-by-one at the block boundary: block A is indices `0..k-1`, block B is `k..n-1`.
            - Inclusive versus half-open ends when switching between your own `reverse(a, lo, hi)` and `std::reverse`.
            - Negative `k` (a rotation the other way) with `%` in Java, C++ and C.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why do you reverse each block before (or after) reversing the whole array?",
                 "Reversing the whole array swaps the two blocks but also flips each one. Reversing each block separately flips them back, so they end up swapped and the right way round."),
                ("What does rotate_left([1, 2, 3, 4, 5], 7) give, and why?",
                 "3 4 5 1 2. Rotating by 5 changes nothing, so 7 behaves like 7 % 5 = 2."),
                ("After rotating left by k, which original index does slot i hold?",
                 "(i + k) mod n."),
                ("How many cycles does rotating 12 values by 8 have, and how long is each?",
                 "gcd(12, 8) = 4 cycles, each of length 12 / 4 = 3."),
                ("How would you swap blocks X and Z in X Y Z using only reversals?",
                 "Reverse X, reverse Y, reverse Z, then reverse the whole thing: (X' Y' Z')' = Z Y X."),
            ),
        ]),
    ],
)
