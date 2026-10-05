"""Lesson: Opposite ends (Two Pointers, pattern 1)."""
from lesson import Bars, Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

COUNT = {
    "python": """
        def count_pairs(nums, target):
            lo, hi = 0, len(nums) - 1                   #@ends
            count = 0                                   #@ends
            while lo < hi:                              #@loop
                s = nums[lo] + nums[hi]                 #@sum
                if s < target:                          #@small
                    lo += 1                             #@small
                elif s > target:                        #@big
                    hi -= 1                             #@big
                elif nums[lo] == nums[hi]:              #@same
                    k = hi - lo + 1                     #@same
                    count += k * (k - 1) // 2           #@same
                    break                               #@same
                else:
                    a = 1                               #@runs
                    while nums[lo + a] == nums[lo]:     #@runs
                        a += 1                          #@runs
                    b = 1                               #@runs
                    while nums[hi - b] == nums[hi]:     #@runs
                        b += 1                          #@runs
                    count += a * b                      #@take
                    lo, hi = lo + a, hi - b             #@take
            return count                                #@ret
    """,
    "java": """
        static long countPairs(int[] nums, long target) {
            int lo = 0, hi = nums.length - 1;           //@ends
            long count = 0;                             //@ends
            while (lo < hi) {                           //@loop
                long s = (long) nums[lo] + nums[hi];    //@sum
                if (s < target) lo++;                   //@small
                else if (s > target) hi--;              //@big
                else if (nums[lo] == nums[hi]) {        //@same
                    long k = hi - lo + 1;               //@same
                    count += k * (k - 1) / 2;           //@same
                    break;                              //@same
                } else {
                    int a = 1, b = 1;                   //@runs
                    while (nums[lo + a] == nums[lo]) a++;   //@runs
                    while (nums[hi - b] == nums[hi]) b++;   //@runs
                    count += (long) a * b;              //@take
                    lo += a;                            //@take
                    hi -= b;                            //@take
                }
            }
            return count;                               //@ret
        }
    """,
    "cpp": """
        long long countPairs(const vector<int>& nums, long long target) {
            int lo = 0, hi = (int)nums.size() - 1;      //@ends
            long long count = 0;                        //@ends
            while (lo < hi) {                           //@loop
                long long s = (long long)nums[lo] + nums[hi];   //@sum
                if (s < target) lo++;                   //@small
                else if (s > target) hi--;              //@big
                else if (nums[lo] == nums[hi]) {        //@same
                    long long k = hi - lo + 1;          //@same
                    count += k * (k - 1) / 2;           //@same
                    break;                              //@same
                } else {
                    int a = 1, b = 1;                   //@runs
                    while (nums[lo + a] == nums[lo]) a++;   //@runs
                    while (nums[hi - b] == nums[hi]) b++;   //@runs
                    count += (long long)a * b;          //@take
                    lo += a;                            //@take
                    hi -= b;                            //@take
                }
            }
            return count;                               //@ret
        }
    """,
    "c": """
        long long countPairs(const int* nums, int n, long long target) {
            int lo = 0, hi = n - 1;                     //@ends
            long long count = 0;                        //@ends
            while (lo < hi) {                           //@loop
                long long s = (long long)nums[lo] + nums[hi];   //@sum
                if (s < target) lo++;                   //@small
                else if (s > target) hi--;              //@big
                else if (nums[lo] == nums[hi]) {        //@same
                    long long k = hi - lo + 1;          //@same
                    count += k * (k - 1) / 2;           //@same
                    break;                              //@same
                } else {
                    int a = 1, b = 1;                   //@runs
                    while (nums[lo + a] == nums[lo]) a++;   //@runs
                    while (nums[hi - b] == nums[hi]) b++;   //@runs
                    count += (long long)a * b;          //@take
                    lo += a;                            //@take
                    hi -= b;                            //@take
                }
            }
            return count;                               //@ret
        }
    """,
}
COUNT_RUN = {
    "python": """
        print(count_pairs([1, 2, 3, 4, 5, 6, 7], 8))
        print(count_pairs([1, 1, 2, 3, 3, 3, 4], 5))
        print(count_pairs([2, 2, 2, 2], 4))
        print(count_pairs([1, 3], 10))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(countPairs(new int[] {1, 2, 3, 4, 5, 6, 7}, 8));
            System.out.println(countPairs(new int[] {1, 1, 2, 3, 3, 3, 4}, 5));
            System.out.println(countPairs(new int[] {2, 2, 2, 2}, 4));
            System.out.println(countPairs(new int[] {1, 3}, 10));
        }
    """,
    "cpp": """
        int main() {
            cout << countPairs({1, 2, 3, 4, 5, 6, 7}, 8) << "\\n";
            cout << countPairs({1, 1, 2, 3, 3, 3, 4}, 5) << "\\n";
            cout << countPairs({2, 2, 2, 2}, 4) << "\\n";
            cout << countPairs({1, 3}, 10) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {1, 2, 3, 4, 5, 6, 7}, b[] = {1, 1, 2, 3, 3, 3, 4}, c[] = {2, 2, 2, 2}, d[] = {1, 3};
            printf("%lld\\n", countPairs(a, 7, 8));
            printf("%lld\\n", countPairs(b, 7, 5));
            printf("%lld\\n", countPairs(c, 4, 4));
            printf("%lld\\n", countPairs(d, 2, 10));
            return 0;
        }
    """,
}

BEST = {
    "python": """
        def best_under(prices, cap):
            lo, hi = 0, len(prices) - 1                 #@ends
            best = -1                                   #@ends
            while lo < hi:                              #@loop
                s = prices[lo] + prices[hi]             #@sum
                if s <= cap:                            #@fits
                    best = max(best, s)                 #@fits
                    lo += 1                             #@fits
                else:                                   #@over
                    hi -= 1                             #@over
            return best                                 #@ret
    """,
    "java": """
        static long bestUnder(int[] prices, long cap) {
            int lo = 0, hi = prices.length - 1;         //@ends
            long best = -1;                             //@ends
            while (lo < hi) {                           //@loop
                long s = (long) prices[lo] + prices[hi];    //@sum
                if (s <= cap) {                         //@fits
                    best = Math.max(best, s);           //@fits
                    lo++;                               //@fits
                } else {                                //@over
                    hi--;                               //@over
                }
            }
            return best;                                //@ret
        }
    """,
    "cpp": """
        long long bestUnder(const vector<int>& prices, long long cap) {
            int lo = 0, hi = (int)prices.size() - 1;    //@ends
            long long best = -1;                        //@ends
            while (lo < hi) {                           //@loop
                long long s = (long long)prices[lo] + prices[hi];   //@sum
                if (s <= cap) {                         //@fits
                    best = max(best, s);                //@fits
                    lo++;                               //@fits
                } else {                                //@over
                    hi--;                               //@over
                }
            }
            return best;                                //@ret
        }
    """,
    "c": """
        long long bestUnder(const int* prices, int n, long long cap) {
            int lo = 0, hi = n - 1;                     //@ends
            long long best = -1;                        //@ends
            while (lo < hi) {                           //@loop
                long long s = (long long)prices[lo] + prices[hi];   //@sum
                if (s <= cap) {                         //@fits
                    if (s > best) best = s;             //@fits
                    lo++;                               //@fits
                } else {                                //@over
                    hi--;                               //@over
                }
            }
            return best;                                //@ret
        }
    """,
}
BEST_RUN = {
    "python": """
        print(best_under([3, 5, 8, 10, 14], 16))
        print(best_under([2, 5, 7, 11, 15], 20))
        print(best_under([10, 20], 5))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(bestUnder(new int[] {3, 5, 8, 10, 14}, 16));
            System.out.println(bestUnder(new int[] {2, 5, 7, 11, 15}, 20));
            System.out.println(bestUnder(new int[] {10, 20}, 5));
        }
    """,
    "cpp": """
        int main() {
            cout << bestUnder({3, 5, 8, 10, 14}, 16) << "\\n";
            cout << bestUnder({2, 5, 7, 11, 15}, 20) << "\\n";
            cout << bestUnder({10, 20}, 5) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {3, 5, 8, 10, 14}, b[] = {2, 5, 7, 11, 15}, c[] = {10, 20};
            printf("%lld\\n", bestUnder(a, 5, 16));
            printf("%lld\\n", bestUnder(b, 5, 20));
            printf("%lld\\n", bestUnder(c, 2, 5));
            return 0;
        }
    """,
}

PAL = {
    "python": """
        def is_palindrome(word):
            lo, hi = 0, len(word) - 1                   #@ends
            while lo < hi:                              #@loop
                if word[lo] != word[hi]:                #@diff
                    return False                        #@diff
                lo, hi = lo + 1, hi - 1                 #@step
            return True                                 #@ret
    """,
    "java": """
        static boolean isPalindrome(String word) {
            int lo = 0, hi = word.length() - 1;         //@ends
            while (lo < hi) {                           //@loop
                if (word.charAt(lo) != word.charAt(hi)) //@diff
                    return false;                       //@diff
                lo++;                                   //@step
                hi--;                                   //@step
            }
            return true;                                //@ret
        }
    """,
    "cpp": """
        bool isPalindrome(const string& word) {
            int lo = 0, hi = (int)word.size() - 1;      //@ends
            while (lo < hi) {                           //@loop
                if (word[lo] != word[hi])               //@diff
                    return false;                       //@diff
                lo++;                                   //@step
                hi--;                                   //@step
            }
            return true;                                //@ret
        }
    """,
    "c": """
        bool isPalindrome(const char* word) {
            int lo = 0, hi = (int)strlen(word) - 1;     //@ends
            while (lo < hi) {                           //@loop
                if (word[lo] != word[hi])               //@diff
                    return false;                       //@diff
                lo++;                                   //@step
                hi--;                                   //@step
            }
            return true;                                //@ret
        }
    """,
}
PAL_RUN = {
    "python": """
        for w in ["racecar", "level", "ab", "x", ""]:
            print(str(is_palindrome(w)).lower())
    """,
    "java": """
        public static void main(String[] args) {
            for (String w : new String[] {"racecar", "level", "ab", "x", ""}) System.out.println(isPalindrome(w));
        }
    """,
    "cpp": """
        int main() {
            for (string w : {"racecar", "level", "ab", "x", ""}) cout << (isPalindrome(w) ? "true" : "false") << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* ws[] = {"racecar", "level", "ab", "x", ""};
            for (int i = 0; i < 5; i++) printf("%s\\n", isPalindrome(ws[i]) ? "true" : "false");
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

count_pairs = py(COUNT["python"], "count_pairs")
best_under = py(BEST["python"], "best_under")


def brute_pairs(a, t):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] + a[j] == t)


for arr, t in [([1, 2, 3, 4, 5, 6, 7], 8), ([1, 1, 2, 3, 3, 3, 4], 5), ([2, 2, 2, 2], 4), ([1, 3], 10), ([0, 0, 1, 2, 2, 2, 3, 4, 4], 4)]:
    assert count_pairs(arr, t) == brute_pairs(arr, t)

# The search space: every pair as a cell, crossed out a row or a column at a time.
A, AT = [1, 2, 4, 5, 7, 9], 12
AN = len(A)
SUMS = [[A[i] + A[j] if j > i else "" for j in range(AN)] for i in range(AN)]
gw = Steps(f"Pairs from `{A}` that add up to {AT}. Each cell is one pair: row `i`, column `j`, holding `a[i] + a[j]`.")
gone = set()


def g_state(cur=None, hits=()):
    st = {c: "dim" for c in gone}
    for h in hits:
        st[h] = "answer"
    if cur:
        st[cur] = "active"
    return st


hits = []
gw.step(f"There are {AN * (AN - 1) // 2} pairs. Checking them all is the slow way. Start with the pointers at the two ends.",
        Grid(SUMS, label="a[i] + a[j]"), Row(A, ptr={"lo": 0, "hi": AN - 1}, slots=True, label="a"))
lo, hi = 0, AN - 1
while lo < hi:
    s = A[lo] + A[hi]
    if s < AT:
        row = {(lo, j) for j in range(lo + 1, hi + 1)}
        msg = (f"{A[lo]} + {A[hi]} = {s}, less than {AT}. {A[hi]} is the biggest value still in play, so {A[lo]} is too small to reach {AT} "
               f"with anything. Its whole row goes: {len(row)} pair{'s' if len(row) > 1 else ''} ruled out with one comparison. Move `lo` right.")
        gone |= row
        cur = (lo, hi)
        lo += 1
    elif s > AT:
        col = {(i, hi) for i in range(lo, hi)}
        msg = (f"{A[lo]} + {A[hi]} = {s}, more than {AT}. {A[lo]} is the smallest value still in play, so {A[hi]} overshoots with everything. "
               f"Its whole column goes: {len(col)} pair{'s' if len(col) > 1 else ''} ruled out. Move `hi` left.")
        gone |= col
        cur = (lo, hi)
        hi -= 1
    else:
        hits.append((lo, hi))
        msg = (f"{A[lo]} + {A[hi]} = {AT}. A pair. All values are different, so {A[lo]} can't pair with anything else and neither can {A[hi]}: "
               f"cross out both the row and the column, and move both pointers.")
        gone |= {(lo, j) for j in range(lo + 1, hi + 1)} | {(i, hi) for i in range(lo, hi)}
        cur = None
        lo, hi = lo + 1, hi - 1
    gw.step(msg, Grid(SUMS, st=g_state(cur, hits), label="a[i] + a[j]"),
            Row(A, ptr={"lo": lo if lo < AN else None, "hi": hi if hi >= 0 else None}, slots=True, label="a"))
GW_STEPS = len(gw.steps) - 1
gw.steps[-1]["text"] += f" The pointers have met. {GW_STEPS} comparisons covered all {AN * (AN - 1) // 2} pairs, and found {len(hits)}."
G_LEGEND = {"dim": "ruled out without being checked", "active": "the pair being checked", "answer": f"adds up to {AT}"}

# Trace of the template on a sorted array with repeats.
TD, TT = [0, 1, 1, 2, 3, 3, 3, 4, 5, 5, 9], 6
tw = Steps(f"`count_pairs({TD}, {TT})`. Repeated values mean one match can stand for several pairs of positions.")
lo, hi, cnt = 0, len(TD) - 1, 0


def t_state(extra=None):
    st = {k: "dim" for k in range(len(TD)) if k < lo or k > hi}
    if lo <= hi:
        st[lo] = "active"
        st[hi] = "active"
    st.update(extra or {})
    return st


tw.step("Both ends in play, nothing counted.", Row(TD, st=t_state(), ptr={"lo": lo, "hi": hi}, slots=True, label="nums"), M({"sum": "–", "pairs": 0}))
while lo < hi:
    s = TD[lo] + TD[hi]
    if s < TT:
        msg = f"{TD[lo]} + {TD[hi]} = {s}, too small. Move `lo` right."
        lo += 1
        extra = None
    elif s > TT:
        msg = f"{TD[lo]} + {TD[hi]} = {s}, too big. Move `hi` left."
        hi -= 1
        extra = None
    elif TD[lo] == TD[hi]:
        k = hi - lo + 1
        cnt += k * (k - 1) // 2
        msg = f"{TD[lo]} + {TD[hi]} = {s}, and both ends hold the same value, so everything between is that value too: any 2 of these {k} make a pair, {k * (k - 1) // 2} in all."
        extra = {x: "answer" for x in range(lo, hi + 1)}
        lo, hi = lo, lo - 1
    else:
        a = 1
        while TD[lo + a] == TD[lo]:
            a += 1
        b = 1
        while TD[hi - b] == TD[hi]:
            b += 1
        cnt += a * b
        extra = {x: "answer" for x in list(range(lo, lo + a)) + list(range(hi - b + 1, hi + 1))}
        msg = (f"{TD[lo]} + {TD[hi]} = {s}, a match. There {'are' if a > 1 else 'is'} {a} cop{'ies' if a > 1 else 'y'} of {TD[lo]} on the left and {b} of {TD[hi]} on the right, "
               f"and every one on the left pairs with every one on the right: {a} × {b} = {a * b} pair{'s' if a * b != 1 else ''}. Jump both pointers past their runs.")
        lo, hi = lo + a, hi - b
    tw.step(msg, Row(TD, st=t_state(extra), ptr={"lo": lo if lo < len(TD) else None, "hi": hi if hi >= 0 else None}, slots=True, label="nums"),
            M({"sum": s, "pairs": cnt}))
tw.steps[-1]["text"] += f" `lo` has passed `hi`, so we're done: {cnt} pairs."
assert cnt == count_pairs(TD, TT)
T_LEGEND = {"active": "the two ends being added", "answer": "counted in this step", "dim": "out of play"}

# Example: count pairs with sum below a target, many at once.
LD, LT = [1, 3, 4, 6, 8, 11], 10
l_rows, lo, hi, lc = [], 0, len(LD) - 1, 0
while lo < hi:
    s = LD[lo] + LD[hi]
    if s < LT:
        lc += hi - lo
        l_rows.append((f"{LD[lo]} + {LD[hi]} = {s}", f"below {LT}: {LD[lo]} pairs with all {hi - lo} values from index {lo + 1} to {hi}", str(lc)))
        lo += 1
    else:
        l_rows.append((f"{LD[lo]} + {LD[hi]} = {s}", f"not below {LT}: drop {LD[hi]}", str(lc)))
        hi -= 1
assert lc == sum(1 for i in range(len(LD)) for j in range(i + 1, len(LD)) if LD[i] + LD[j] < LT)

# Difference k doesn't work from opposite ends: a counter-example table.
DF = [1, 3, 6, 10]

N = 10**5

lesson(
    "two-pointers",
    "opposite-ends",
    """
    Put one pointer at each end of a sorted array (or of any sequence you're comparing with itself back to front)
    and walk them towards each other. Every comparison tells you which end can't be part of an answer, so one of them
    moves in, and the whole search takes a single pass.
    """,
    [
        ("idea", "The idea", [
            f"""
            You're at a market with a voucher worth exactly 11 and a row of stalls sorted by price: `{A}`. You want two
            items that use the voucher exactly.

            Stand at both ends. Take the cheapest item (1) and the dearest (9): 10, not enough. Could the 1 work with
            anything else? No: 9 was the dearest thing on offer, and even that wasn't enough. So the 1 is out, and you
            step in from the left. Now 2 and 9 make 11. Found one. Step in from both sides and keep going: 4 and 7 make
            11 too.

            Every comparison either finds a pair or proves that one of the two items can't be in any pair. That
            item is dropped, so the row shrinks by one each time. After at most `n - 1` comparisons the two pointers
            meet and you've checked every pair, most of them without looking at them.
            """,
            fig(Bars(A, ptr={"lo": 0, "hi": AN - 1}, label="sorted prices"),
                caption="Too small? The left value is out, because it already had the biggest partner available. Too big? The right value is out, for the mirror reason."),
            key("""
            Start with `lo` at the left end and `hi` at the right end of a sorted array. If `a[lo] + a[hi]` is too
            small, move `lo` right. If it's too big, move `hi` left. If it's right, record it and move. Stop when they
            meet. O(n) time, O(1) space.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The input is sorted (or you're allowed to sort it), and the question is about pairs whose *sum* has to hit,
            stay under or get close to a target. Or the question compares a sequence with its own mirror image:
            palindromes, reversing in place, matching the first item with the last.
            """,
            table(
                ["The problem says…", "what the two ends do"],
                ["sorted array, two values adding up to `t`", "too small: `lo++`; too big: `hi--`"],
                ["the pair with the biggest (or closest) sum under a cap", "record every pair that fits, then move as above"],
                ["count pairs with sum below `t`", "when `a[lo] + a[hi] < t`, all `hi - lo` partners of `a[lo]` count at once"],
                ["palindrome, reverse in place", "compare or swap `a[lo]` and `a[hi]`, then move both"],
                ["pair people up so no pair is too heavy", "try the lightest with the heaviest"],
                ["the widest container, the biggest area between two walls", "move the shorter wall, which can't do better"],
            ),
            f"""
            Not a fit:

            - The array isn't sorted and you can't sort it (you need the original positions, say). Use a hash map
              (*Complement lookup*).
            - The condition is a *difference*, like `a[j] - a[i] = k`. From the two ends a gap that's too big doesn't
              tell you which pointer to move: moving either one could shrink it. Put both pointers at the left and move
              them in the same direction instead.
            - You need every pair in a range of sums printed out. There can be about `n² / 2` of them, and no pointer
              trick prints them faster than that.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### The search space is a triangle

            Draw every pair `i < j` as a cell in a grid: row `i`, column `j`. Because the array is sorted, sums grow as
            you go right along a row and as you go down a column. The pointers always sit at the top-right corner of
            the part that's still in play.

            That corner is special. It's the biggest sum in its row and the smallest in its column. So:

            - if it's too small, every cell to its left in the same row is smaller still, and the whole row can go;
            - if it's too big, every cell below it in the same column is bigger still, and the whole column can go.

            Either way a full row or column disappears with one comparison. There are only `n - 1` rows and columns
            to remove, so that's at most `n - 1` comparisons.
            """,
            walk(gw, legend=G_LEGEND),
            """
            ### What the loop keeps true

            > Every pair that could still be an answer has both its positions between `lo` and `hi`.

            It's true at the start. When `a[lo] + a[hi]` is too small, the pairs that use `lo` have partners at most
            `a[hi]`, so they're all too small, and dropping `lo` loses nothing. The same argument, mirrored, covers
            dropping `hi`. When the loop ends with `lo ≥ hi`, no pair is left, so none was missed.

            ### When the sum matches

            If every value is different, a match uses up both ends: the left value's only possible partner is the right
            value, and the other way round. Move both.

            With repeats, a match can stand for many pairs. If the left end's value appears `a` times in a row and the
            right end's value `b` times, every left copy pairs with every right copy: `a × b` pairs. If the two ends hold
            the *same* value, everything between them is that value too, and any 2 of those `k` positions make a pair:
            `k(k - 1) / 2`. The template handles both.

            ### Sorting first

            If the input isn't sorted, sorting it costs O(n log n), which then dominates. That's still much better
            than O(n²), and it uses no extra memory if you can sort in place. The price is that the original positions
            are gone. If the answer needs them, sort `(value, index)` pairs or use a hash map instead.
            """,
        ]),
        ("template", "The template", [
            """
            Count the pairs of positions `i < j` in a sorted array with `nums[i] + nums[j] == target`. Values can repeat,
            and each pair of positions counts once.
            """,
            code(
                "Count pairs with a given sum (sorted input)",
                COUNT,
                [
                    ("ends", "One pointer at each end, and nothing counted yet. The count can reach about n²/2, so it's 64-bit."),
                    ("loop", "While there are at least two positions in play."),
                    ("sum", "The sum of the two ends.",
                     {"java": "Widen to `long` before adding: two values near 10⁹ overflow an `int`.",
                      "cpp": "Widen before adding, so two large `int`s can't overflow.",
                      "c": "Widen before adding, so two large `int`s can't overflow."}),
                    ("small", "Too small. `nums[lo]` was paired with the biggest value left and still fell short, so it can't be "
                              "in any pair. Drop it."),
                    ("big", "Too big. `nums[hi]` overshoots even with the smallest value left. Drop it."),
                    ("same", "A match where both ends hold the same value. Everything between them is equal too, so any two "
                             "of those `k` positions make a pair. Nothing else is left to check."),
                    ("runs", "A match with different values. Count the run of equal values at each end. Each run stops before "
                             "reaching the other end, because the values there differ."),
                    ("take", "Every copy on the left pairs with every copy on the right. Then step past both runs."),
                    ("ret", "The number of pairs."),
                ],
                COUNT_RUN,
                "count_pairs([1, 2, 3, 4, 5, 6, 7], 8); ([1, 1, 2, 3, 3, 3, 4], 5); ([2, 2, 2, 2], 4); ([1, 3], 10)",
            ),
            """
            `[2, 2, 2, 2]` with target 4 is the "same value" branch: any 2 of the 4 positions, which is 6 pairs.
            """,
        ]),
        ("trace", "Trace it by hand", [
            f"`count_pairs` on `{TD}` with target {TT}, one comparison per step:",
            walk(tw, legend=T_LEGEND),
            """
            On paper, write the array once and draw `lo` and `hi` under it. For each step write the sum, then cross out
            whichever end the rule drops. If you ever feel the urge to move both pointers on a mismatch, stop: only a
            match lets both move.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Counting pairs with a sum below a target

            In `{LD}`, how many pairs add up to less than {LT}? When `a[lo] + a[hi]` is below {LT}, the left value is
            below {LT} with `a[hi]`, and so with every value between `lo` and `hi` as well, because those are smaller.
            That's `hi - lo` pairs counted in one step. Then `lo` can move on.
            """,
            table(["ends", "what it means", "pairs so far"], *l_rows),
            f"""
            {lc} pairs, found in {len(l_rows)} comparisons. The same counting step is the inner loop of several
            *k-Sum* problems.

            ### Pairing heavy with light

            People with weights go two at a time on a ride with a weight limit. Sort them. The heaviest person has to go
            with *someone* or alone. If even the lightest person is too heavy to join them, nobody can, so they ride
            alone and `hi` moves. Otherwise pairing them with the lightest is safe: the lightest person fits with
            anyone the heaviest fits with. This is the same "drop the end that can't do better" argument, used to make
            a greedy choice instead of to search.

            ### Why differences need a different walk

            Look for two values in `{DF}` that differ by exactly 5. From the ends, 10 - 1 = 9 is too big. Moving `hi`
            left gives 6 - 1 = 5, but moving `lo` right would give 10 - 3 = 7, also smaller. Both moves shrink the gap,
            so the comparison doesn't say which end is useless, and the argument that made opposite ends safe falls
            apart. For differences, start both pointers on the left and move whichever one makes the gap move in the
            direction you need.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### The best pair under a cap

            Instead of an exact target, find the largest sum that doesn't go over `cap`. Every pair that fits is a
            candidate, so record it before moving. The moves are the same as before: a pair that fits means `lo` can't
            do better with any smaller partner, so `lo` moves; a pair that's over means `hi` is too big for everyone left.
            """,
            code(
                "Largest pair sum not above a cap",
                BEST,
                [
                    ("ends", "Both ends, and no pair found yet. Prices are positive, so -1 can stand for \"no pair fits\"."),
                    ("loop", "Two positions still in play."),
                    ("sum", "The sum of the two ends, widened so it can't overflow."),
                    ("fits", "It fits. It's the best pair for `prices[lo]`, since `prices[hi]` is its biggest possible partner, "
                             "so record it and move `lo` on."),
                    ("over", "Over the cap. `prices[hi]` is too expensive with every remaining partner."),
                    ("ret", "The best sum found, or -1."),
                ],
                BEST_RUN,
                "best_under([3, 5, 8, 10, 14], 16); ([2, 5, 7, 11, 15], 20); ([10, 20], 5)",
            ),
            """
            ### Comparing a sequence with its mirror

            The two ends don't need a sorted array at all when the question is about symmetry. A palindrome check
            compares the first character with the last, the second with the second last, and so on, until the pointers
            meet. Reversing in place swaps the same pairs.
            """,
            code(
                "Palindrome check",
                PAL,
                [
                    ("ends", "The first and last positions."),
                    ("loop", "Until the pointers meet. A middle character in an odd-length word is compared with nothing."),
                    ("diff", "One mismatched pair is enough to say no."),
                    ("step", "This pair matched. Move both pointers inward."),
                    ("ret", "Every mirrored pair matched. An empty word and a single letter both get here straight away."),
                ],
                PAL_RUN,
                'is_palindrome("racecar"); ("level"); ("ab"); ("x"); ("")',
            ),
            """
            Real questions add a twist, like skipping characters that aren't letters or allowing one mismatch. The
            skeleton stays: two pointers, compare, move inward.

            ### Moving the weaker side

            Some problems don't have a target at all. "Pick two walls and maximise the water between them" has a value
            that depends on the width (which shrinks every step) and the shorter wall. Moving the taller wall can't help,
            because the shorter one still caps the height and the width got smaller. So the shorter wall is the one
            that moves. The general habit: work out which end can't possibly improve, and drop that one.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            Each step moves at least one pointer inward, and they start `n - 1` apart, so there are at most `n - 1`
            steps. The template's run-counting loops also only move the pointers forward, so they don't add to that.
            O(n) time and O(1) extra space. If you have to sort first, the sort's O(n log n) dominates.

            Checking every pair is `n(n - 1) / 2` comparisons: for `n = 100,000` that's {N * (N - 1) // 2:,}, against
            fewer than {N:,} here.
            """,
            table(
                ["Approach", "Time", "Extra space", "Needs"],
                ["Check every pair", "O(n²)", "O(1)", "nothing"],
                ["Hash map of values seen", "O(n) on average", "O(n)", "exact targets only"],
                ["Opposite ends on sorted input", "O(n)", "O(1)", "sorted input"],
                ["Sort, then opposite ends", "O(n log n)", "O(1) to O(n)", "positions aren't needed"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `lo, hi = 0, len(a) - 1` and tuple assignment to move both at once. Integers don't overflow. If you sort a
            copy, `sorted(a)` leaves the caller's list alone; `a.sort()` doesn't.

            ### Java

            Add in `long`: `(long) a[lo] + a[hi]`. `Arrays.sort(int[])` sorts primitives in place. For strings,
            `charAt` reads a character; there's no in-place reverse, so work on a `char[]` from `toCharArray()`.

            ### C++

            Cast before adding: `(long long)a[lo] + a[hi]`. `std::reverse` does the "swap the ends, move inward" loop for
            you. Be careful with `size() - 1` on an empty vector: it's unsigned and wraps to a huge number. Cast to
            `int` first, as the template does.

            ### C

            Pass the length with the array. Cast to `long long` before adding. `strlen` gives a string's length, and an
            empty string gives `hi = -1`, which the loop condition handles.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Using it on unsorted input. The "drop this end" argument depends on sorted order.
            - Moving both pointers on a mismatch. Only a match uses up both ends (and with repeats, only past the runs).
            - `lo <= hi` instead of `lo < hi`, which pairs an element with itself.
            - Overflow when adding two large values in Java, C or C++.
            - With repeats, counting a match as one pair when it stands for `a × b` (or `k(k - 1) / 2`).
            - Trying it on differences from opposite ends. Both moves can shrink the gap, so neither is safe to drop.
            - `size() - 1` on an empty container in C++.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("`a[lo] + a[hi]` is less than the target. Why is it safe to drop `a[lo]`?",
                 "`a[hi]` is the biggest value still in play, so it's the best partner `a[lo]` could have. If even that falls short, every other partner does too."),
                ("Why does the loop run at most n - 1 times?",
                 "Every step moves at least one pointer one place inward, and they start n - 1 places apart."),
                ("Sorted [2, 2, 3, 3, 3, 4], target 6. How many pairs of positions add up to 6?",
                 "2 + 4: two 2s and one 4 make 2 pairs. 3 + 3: any two of the three 3s, which is 3 pairs. 5 in total."),
                ("Count pairs with sum below t: why can you add `hi - lo` in one go?",
                 "If `a[lo] + a[hi] < t`, then `a[lo]` plus any value between `lo + 1` and `hi` is smaller still, because those values are at most `a[hi]`. That's `hi - lo` pairs."),
                ("Why doesn't the opposite-ends walk work for \"two values that differ by exactly k\"?",
                 "When the gap is too big, moving either pointer inward makes it smaller, so the comparison doesn't tell you which end is useless. Put both pointers on the left and move them in the same direction instead."),
            ),
        ]),
    ],
)
