"""Lesson: Counting while merging (Sorting, pattern 5)."""
from lesson import Bars, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

INV = {
    "python": """
        def sort_count(a, buf, lo, hi):
            if hi - lo < 2:                                 #@base
                return 0                                    #@base
            mid = (lo + hi) // 2                            #@split
            count = sort_count(a, buf, lo, mid) + sort_count(a, buf, mid, hi)   #@halves
            i, j, k = lo, mid, lo                           #@merge
            while i < mid and j < hi:                       #@merge
                if a[i] <= a[j]:                            #@left
                    buf[k] = a[i]                           #@left
                    i += 1                                  #@left
                else:                                       #@right
                    buf[k] = a[j]                           #@right
                    j += 1                                  #@right
                    count += mid - i                        #@count
                k += 1                                      #@merge
            rest = a[i:mid] + a[j:hi]                       #@rest
            buf[k:hi] = rest                                #@rest
            a[lo:hi] = buf[lo:hi]                           #@rest
            return count                                    #@ret


        def count_inversions(nums):
            a = list(nums)                                  #@start
            return sort_count(a, [0] * len(a), 0, len(a))   #@start
    """,
    "java": """
        static long sortCount(int[] a, int[] buf, int lo, int hi) {
            if (hi - lo < 2) return 0;                      //@base
            int mid = (lo + hi) >>> 1;                      //@split
            long count = sortCount(a, buf, lo, mid) + sortCount(a, buf, mid, hi);   //@halves
            int i = lo, j = mid, k = lo;                    //@merge
            while (i < mid && j < hi) {                     //@merge
                if (a[i] <= a[j]) buf[k++] = a[i++];        //@left
                else {                                      //@right
                    buf[k++] = a[j++];                      //@right
                    count += mid - i;                       //@count
                }
            }
            while (i < mid) buf[k++] = a[i++];              //@rest
            while (j < hi) buf[k++] = a[j++];               //@rest
            System.arraycopy(buf, lo, a, lo, hi - lo);      //@rest
            return count;                                   //@ret
        }

        static long countInversions(int[] nums) {
            int[] a = nums.clone();                         //@start
            return sortCount(a, new int[a.length], 0, a.length);    //@start
        }
    """,
    "cpp": """
        long long sortCount(vector<int>& a, vector<int>& buf, int lo, int hi) {
            if (hi - lo < 2) return 0;                      //@base
            int mid = lo + (hi - lo) / 2;                   //@split
            long long count = sortCount(a, buf, lo, mid) + sortCount(a, buf, mid, hi);  //@halves
            int i = lo, j = mid, k = lo;                    //@merge
            while (i < mid && j < hi) {                     //@merge
                if (a[i] <= a[j]) buf[k++] = a[i++];        //@left
                else {                                      //@right
                    buf[k++] = a[j++];                      //@right
                    count += mid - i;                       //@count
                }
            }
            while (i < mid) buf[k++] = a[i++];              //@rest
            while (j < hi) buf[k++] = a[j++];               //@rest
            copy(buf.begin() + lo, buf.begin() + hi, a.begin() + lo);  //@rest
            return count;                                   //@ret
        }

        long long countInversions(vector<int> a) {
            vector<int> buf(a.size());                      //@start
            return sortCount(a, buf, 0, a.size());          //@start
        }
    """,
    "c": """
        static long long sortCount(int* a, int* buf, int lo, int hi) {
            if (hi - lo < 2) return 0;                      //@base
            int mid = lo + (hi - lo) / 2;                   //@split
            long long count = sortCount(a, buf, lo, mid) + sortCount(a, buf, mid, hi);  //@halves
            int i = lo, j = mid, k = lo;                    //@merge
            while (i < mid && j < hi) {                     //@merge
                if (a[i] <= a[j]) buf[k++] = a[i++];        //@left
                else {                                      //@right
                    buf[k++] = a[j++];                      //@right
                    count += mid - i;                       //@count
                }
            }
            while (i < mid) buf[k++] = a[i++];              //@rest
            while (j < hi) buf[k++] = a[j++];               //@rest
            memcpy(a + lo, buf + lo, (hi - lo) * sizeof(int));  //@rest
            return count;                                   //@ret
        }

        long long countInversions(const int* nums, int n) {
            int* a = malloc((n > 0 ? n : 1) * sizeof(int));     //@start
            int* buf = malloc((n > 0 ? n : 1) * sizeof(int));   //@start
            memcpy(a, nums, n * sizeof(int));               //@start
            long long count = sortCount(a, buf, 0, n);      //@start
            free(a);                                        //@start
            free(buf);                                      //@start
            return count;                                   //@start
        }
    """,
}
INV_RUN = {
    "python": """
        print(count_inversions([5, 2, 6, 1, 3]))
        print(count_inversions([1, 2, 3]))
        print(count_inversions([4, 3, 2, 1]))
        print(count_inversions([2, 2, 1]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(countInversions(new int[] {5, 2, 6, 1, 3}));
            System.out.println(countInversions(new int[] {1, 2, 3}));
            System.out.println(countInversions(new int[] {4, 3, 2, 1}));
            System.out.println(countInversions(new int[] {2, 2, 1}));
        }
    """,
    "cpp": """
        int main() {
            cout << countInversions({5, 2, 6, 1, 3}) << "\\n" << countInversions({1, 2, 3}) << "\\n";
            cout << countInversions({4, 3, 2, 1}) << "\\n" << countInversions({2, 2, 1}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {5, 2, 6, 1, 3}, b[] = {1, 2, 3}, c[] = {4, 3, 2, 1}, d[] = {2, 2, 1};
            printf("%lld\\n%lld\\n", countInversions(a, 5), countInversions(b, 3));
            printf("%lld\\n%lld\\n", countInversions(c, 4), countInversions(d, 3));
            return 0;
        }
    """,
}

DROPS = {
    "python": """
        def sort_drops(a, buf, lo, hi, d):
            if hi - lo < 2:                                 #@base
                return 0                                    #@base
            mid = (lo + hi) // 2                            #@base
            count = sort_drops(a, buf, lo, mid, d) + sort_drops(a, buf, mid, hi, d)    #@base
            i = lo                                          #@pair
            for j in range(mid, hi):                        #@pair
                while i < mid and a[i] <= a[j] + d:         #@skip
                    i += 1                                  #@skip
                count += mid - i                            #@add
            buf[lo:hi] = sorted(a[lo:mid] + a[mid:hi])      #@merge
            a[lo:hi] = buf[lo:hi]                           #@merge
            return count                                    #@ret


        def count_drops(nums, d):
            a = list(nums)                                  #@start
            return sort_drops(a, [0] * len(a), 0, len(a), d)    #@start
    """,
    "java": """
        static long sortDrops(int[] a, int[] buf, int lo, int hi, long d) {
            if (hi - lo < 2) return 0;                      //@base
            int mid = (lo + hi) >>> 1;                      //@base
            long count = sortDrops(a, buf, lo, mid, d) + sortDrops(a, buf, mid, hi, d);    //@base
            int i = lo;                                     //@pair
            for (int j = mid; j < hi; j++) {                //@pair
                while (i < mid && a[i] <= a[j] + d) i++;    //@skip
                count += mid - i;                           //@add
            }
            int l = lo, r = mid, k = lo;                    //@merge
            while (l < mid && r < hi) buf[k++] = a[l] <= a[r] ? a[l++] : a[r++];   //@merge
            while (l < mid) buf[k++] = a[l++];              //@merge
            while (r < hi) buf[k++] = a[r++];               //@merge
            System.arraycopy(buf, lo, a, lo, hi - lo);      //@merge
            return count;                                   //@ret
        }

        static long countDrops(int[] nums, int d) {
            int[] a = nums.clone();                         //@start
            return sortDrops(a, new int[a.length], 0, a.length, d);    //@start
        }
    """,
    "cpp": """
        long long sortDrops(vector<int>& a, vector<int>& buf, int lo, int hi, long long d) {
            if (hi - lo < 2) return 0;                      //@base
            int mid = lo + (hi - lo) / 2;                   //@base
            long long count = sortDrops(a, buf, lo, mid, d) + sortDrops(a, buf, mid, hi, d);   //@base
            int i = lo;                                     //@pair
            for (int j = mid; j < hi; j++) {                //@pair
                while (i < mid && a[i] <= a[j] + d) i++;    //@skip
                count += mid - i;                           //@add
            }
            merge(a.begin() + lo, a.begin() + mid, a.begin() + mid, a.begin() + hi, buf.begin() + lo);  //@merge
            copy(buf.begin() + lo, buf.begin() + hi, a.begin() + lo);  //@merge
            return count;                                   //@ret
        }

        long long countDrops(vector<int> a, int d) {
            vector<int> buf(a.size());                      //@start
            return sortDrops(a, buf, 0, a.size(), d);       //@start
        }
    """,
    "c": """
        static long long sortDrops(int* a, int* buf, int lo, int hi, long long d) {
            if (hi - lo < 2) return 0;                      //@base
            int mid = lo + (hi - lo) / 2;                   //@base
            long long count = sortDrops(a, buf, lo, mid, d) + sortDrops(a, buf, mid, hi, d);   //@base
            int i = lo;                                     //@pair
            for (int j = mid; j < hi; j++) {                //@pair
                while (i < mid && a[i] <= a[j] + d) i++;    //@skip
                count += mid - i;                           //@add
            }
            int l = lo, r = mid, k = lo;                    //@merge
            while (l < mid && r < hi) buf[k++] = a[l] <= a[r] ? a[l++] : a[r++];   //@merge
            while (l < mid) buf[k++] = a[l++];              //@merge
            while (r < hi) buf[k++] = a[r++];               //@merge
            memcpy(a + lo, buf + lo, (hi - lo) * sizeof(int));  //@merge
            return count;                                   //@ret
        }

        long long countDrops(const int* nums, int n, int d) {
            int* a = malloc((n > 0 ? n : 1) * sizeof(int));     //@start
            int* buf = malloc((n > 0 ? n : 1) * sizeof(int));   //@start
            memcpy(a, nums, n * sizeof(int));               //@start
            long long count = sortDrops(a, buf, 0, n, d);   //@start
            free(a);                                        //@start
            free(buf);                                      //@start
            return count;                                   //@start
        }
    """,
}
DROPS_RUN = {
    "python": """
        print(count_drops([9, 2, 7, 1, 8, 3], 4))
        print(count_drops([9, 2, 7, 1, 8, 3], 0))
        print(count_drops([1, 2, 3], 0))
    """,
    "java": """
        public static void main(String[] args) {
            int[] a = {9, 2, 7, 1, 8, 3};
            System.out.println(countDrops(a, 4));
            System.out.println(countDrops(a, 0));
            System.out.println(countDrops(new int[] {1, 2, 3}, 0));
        }
    """,
    "cpp": """
        int main() {
            vector<int> a = {9, 2, 7, 1, 8, 3};
            cout << countDrops(a, 4) << "\\n" << countDrops(a, 0) << "\\n" << countDrops({1, 2, 3}, 0) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {9, 2, 7, 1, 8, 3}, b[] = {1, 2, 3};
            printf("%lld\\n%lld\\n%lld\\n", countDrops(a, 6, 4), countDrops(a, 6, 0), countDrops(b, 3, 0));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

count_inversions = py(INV["python"], "count_inversions")
count_drops = py(DROPS["python"], "count_drops")

DEMO = [5, 2, 6, 1, 3]
PAIRS = [(i, j) for i in range(len(DEMO)) for j in range(i + 1, len(DEMO)) if DEMO[i] > DEMO[j]]
assert count_inversions(DEMO) == len(PAIRS) == 6
pair_rows = [(f"index {i} ({DEMO[i]})", f"index {j} ({DEMO[j]})") for i, j in PAIRS]
BRUTE_CHECKS = len(DEMO) * (len(DEMO) - 1) // 2


# Every merge, with the pairs it counts.
MERGES = []


def trace(a, lo, hi):
    if hi - lo < 2:
        return a[lo:hi]
    mid = (lo + hi) // 2
    l_, r_ = trace(a, lo, mid), trace(a, mid, hi)
    cross = sum(1 for x in l_ for y in r_ if x > y)
    MERGES.append((l_, r_, cross))
    return sorted(l_ + r_)


trace(DEMO, 0, len(DEMO))
merge_rows = [(" ".join(map(str, l_)), " ".join(map(str, r_)), str(c)) for l_, r_, c in MERGES]
assert sum(c for *_, c in MERGES) == len(PAIRS)

# Counting during one merge.
L, R = [2, 5, 8], [1, 3, 9]
mw = Steps(f"Merging {L} and {R}, counting pairs where a left value is bigger than a right value. Every left value came earlier in the array than every right value.")
i = j = cnt = 0
out = []


def mw_panels(counted=()):
    return (Row(L, st={**{k: "dim" for k in range(i)}, **{k: "mark" for k in counted}}, ptr={"i": i if i < len(L) else None}, label="left"),
            Row(R, st={k: "dim" for k in range(j)}, ptr={"j": j if j < len(R) else None}, label="right"),
            Row(out + [None] * (len(L) + len(R) - len(out)), st={len(out) - 1: "new"} if out else None, label="merged"),
            M({"crossing pairs": cnt}))


mw.step("Two sorted halves. A crossing pair is any left value bigger than any right value.", *mw_panels())
while i < len(L) and j < len(R):
    if L[i] <= R[j]:
        out.append(L[i])
        msg = f"{L[i]} ≤ {R[j]}: take {L[i]} from the left. Every right value still waiting is at least {R[j]}, so {L[i]} isn't bigger than any of them. Nothing to count."
        i += 1
        counted = ()
    else:
        add = len(L) - i
        cnt += add
        out.append(R[j])
        counted = range(i, len(L))
        msg = (f"{R[j]} < {L[i]}: take {R[j]} from the right. The left half is sorted, so {L[i]} and everything after it "
               f"({', '.join(map(str, L[i:]))}) are bigger than {R[j]}: {add} crossing pair{'s' if add > 1 else ''} at once.")
        j += 1
    mw.step(msg, *mw_panels(counted))
rest = L[i:] + R[j:]
i, j = len(L), len(R)
out += rest
assert cnt == sum(1 for x in L for y in R if x > y)
mw.step(f"The left half is used up, so copy the rest of the right ({', '.join(map(str, rest))}). Leftover right values are bigger than every left value, so they add nothing. Total: {cnt}.",
        *mw_panels(), result=cnt)
MW_LEGEND = {"dim": "already taken", "mark": "each forms a pair with the value just taken", "new": "just placed"}

# The whole count: every merge of the recursion, in order.
ftw = Steps(f"`count_inversions({DEMO})`, one merge per step. Each merge counts only the pairs that cross between its two halves.")
arr, total = list(DEMO), 0
ftw.step("Nothing merged yet. Single values have no pairs inside them.", Row(arr, slots=True), M({"merging": "–", "pairs crossing": "–", "total": 0}))


def ft(lo, hi):
    global total
    if hi - lo < 2:
        return
    mid = (lo + hi) // 2
    ft(lo, mid)
    ft(mid, hi)
    left, right = arr[lo:mid], arr[mid:hi]
    here = sum(1 for x in left for y in right if x > y)
    total += here
    arr[lo:hi] = sorted(arr[lo:hi])
    pairs = ", ".join(f"({x}, {y})" for x in left for y in right if x > y)
    ftw.step(f"Merge {left} with {right}: " + (f"{here} crossing pair{'s' if here != 1 else ''}: {pairs}." if here else "no left value is bigger than a right one, so nothing to count.")
             + (" That was the last merge." if (lo, hi) == (0, len(arr)) else ""),
             Row(list(arr), st={k: "found" for k in range(lo, hi)}, slots=True),
             M({"merging": f"{left} + {right}", "pairs crossing": here, "total": total}))


ft(0, len(arr))
assert total == len(PAIRS)

# The drops variation: the two-pointer pass on one pair of halves.
DL, DR_, DD = [2, 7, 9], [1, 3, 8], 4
dw = Steps(f"Counting pairs where a left value is more than {DD} bigger than a right value, *before* merging {DL} and {DR_}.")
i, cnt = 0, 0
dw.step(f"For each right value `r`, count the left values greater than `r + {DD}`. As `r` grows, so does the threshold, so `i` only ever moves right.",
        Row(DL, ptr={"i": 0}, label="left"), Row(DR_, label="right"), M({"pairs": 0}))
for j, r in enumerate(DR_):
    skipped = []
    while i < len(DL) and DL[i] <= r + DD:
        skipped.append(DL[i])
        i += 1
    add = len(DL) - i
    cnt += add
    msg = (f"r = {r}, threshold {r + DD}. " + (f"Skip {', '.join(map(str, skipped))} (not more than {DD} bigger). " if skipped else "")
           + (f"Everything from `i` on ({', '.join(map(str, DL[i:]))}) qualifies: {add} pair{'s' if add != 1 else ''}." if add else "Nothing left in the left half qualifies."))
    dw.step(msg, Row(DL, st={**{k: "dim" for k in range(i)}, **{k: "found" for k in range(i, len(DL))}}, ptr={"i": i if i < len(DL) else None}, label="left"),
            Row(DR_, st={j: "active"}, label="right"), M({"pairs": cnt}))
assert cnt == sum(1 for x in DL for y in DR_ if x - y > DD)
dw.steps[-1]["text"] += " Then merge the halves as usual; the counting and the merging are separate."
DROPS_IN = [9, 2, 7, 1, 8, 3]
DROPS_OUT = count_drops(DROPS_IN, 4)
assert DROPS_OUT == sum(1 for a in range(6) for b in range(a + 1, 6) if DROPS_IN[a] - DROPS_IN[b] > 4)

# Work: n^2/2 pair checks vs n log n.
WORK_ROWS = [(f"{n:,}", f"{n * (n - 1) // 2:,}", f"{n * max(1, n.bit_length() - 1):,}") for n in (1000, 100_000, 1_000_000)]

# Adjacent swaps: bubble sort on DEMO swaps exactly the inversion count.
a, swaps = list(DEMO), 0
for _ in range(len(a)):
    for k in range(len(a) - 1):
        if a[k] > a[k + 1]:
            a[k], a[k + 1] = a[k + 1], a[k]
            swaps += 1
assert swaps == len(PAIRS)

# Per-element counts: for each value, how many later values are smaller (carried by index).
PER = [sum(1 for j in range(i + 1, len(DEMO)) if DEMO[j] < DEMO[i]) for i in range(len(DEMO))]

lesson(
    "sorting",
    "merge-count",
    """
    Some questions count pairs (i, j) with i < j that satisfy a condition, like "the earlier value is bigger". Checking
    every pair is O(n²). Merge sort does it in O(n log n): when it merges two sorted halves, every left value came
    before every right value, and sortedness lets you count whole groups of pairs in one step.
    """,
    [
        ("idea", "The idea", [
            f"""
            A judge lists contestants in the order they performed, with the rank each one got: `{DEMO}`. How "out of
            order" is this list? A natural measure is the number of **inversions**: pairs where the earlier contestant
            got a bigger rank number than a later one. Here there are {len(PAIRS)}:
            """,
            table(["earlier", "later"], *pair_rows),
            f"""
            Checking every pair takes `n(n - 1) / 2` comparisons ({BRUTE_CHECKS} here, but half a trillion for a million
            values). Merge sort can count them while it sorts. Split the list in half. Every pair is either inside the
            left half, inside the right half, or **crossing**: one value from each. The first two kinds are counted when
            sorting the halves. The crossing ones are counted during the merge, and that's cheap, because both halves
            are sorted by then: the moment a right value is taken before some left values, it's smaller than *all* of
            the left values still waiting.
            """,
            key("""
            Merge sort, plus one line: when the merge takes `a[j]` from the right half while left values `a[i..mid-1]` are
            still waiting, add `mid - i`. Each half counts its own pairs recursively. O(n log n) instead of O(n²).
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The question counts pairs `i < j` (an earlier item and a later item) under a condition that compares their
            values: "how many pairs are out of order", "how many pairs where the earlier one is more than twice the later
            one", "for each item, how many later items are smaller", "the fewest swaps of neighbours to sort". With `n`
            up to 10⁵ or more, O(n²) is too slow, and that's the hint.

            It works when, once both halves are sorted, you can count the condition for a whole range of left values at
            once with a pointer that only moves forward. Conditions like `a[i] > a[j]`, `a[i] > 2·a[j]`
            and `a[i] - a[j] > d` all have that shape.

            Not a fit:

            - The condition depends on positions as well as values ("pairs at most k apart"). Sorting scrambles positions.
            - Values are small integers: a counting array or a Fenwick tree (Binary Indexed Tree, a later topic) may be
              simpler.
            """,
            table(["n", "check every pair", "merge and count (≈ n log₂ n)"], *WORK_ROWS),
        ]),
        ("theory", "Why it works", [
            """
            ### Every pair is counted exactly once

            Pick any pair of positions `i < j`. At the top level they're either on the same side (then they're counted
            inside that side's recursion) or on opposite sides, with `i` on the left (then they're a crossing pair at this
            level). Following the recursion down, every pair is split apart at exactly one level, and that's the only
            merge that counts it. Here are the merges for `{DEMO}` and the crossing pairs each one finds:
            """.replace("{DEMO}", str(DEMO)),
            table(["left (sorted)", "right (sorted)", "crossing pairs counted"], *merge_rows),
            """
            ### Sorting the halves doesn't change the crossing pairs

            Sorting the left half reorders values *within* it, but each of them still came before every right value in
            the original array. So "left value bigger than right value" counts exactly the crossing inversions, whatever
            order the halves are in. Having them sorted only makes the counting fast.

            ### Counting a group at once

            During the merge, suppose the next smallest value is `a[j]` from the right half, while `a[i..mid-1]` are still
            waiting on the left. All of those are bigger than `a[j]` (otherwise one of them would have been taken first),
            and all of them came earlier. So `a[j]` forms `mid - i` inversions, counted in one addition.
            """,
            walk(mw, legend=MW_LEGEND),
            """
            Equal values aren't inversions, which is why ties take from the left: the left value goes out first and isn't
            counted against an equal right value.

            ### When the condition isn't plain "bigger than"

            For a condition like `a[i] > a[j] + d` (or `a[i] > 2·a[j]`), the merge's comparisons don't line up with the
            condition any more. So count in a separate pass *before* merging: walk the right half in sorted order with a
            pointer into the sorted left half. As right values grow, the threshold grows, and the pointer only moves
            forward. That pass is O(length), so the whole thing stays O(n log n).

            ### Inversions and neighbour swaps

            Swapping two neighbours that are out of order removes exactly one inversion and creates none (no other pair
            changes its relative order). Bubble sort and insertion sort sort by such swaps, so the number of swaps they
            make equals the number of inversions, so the inversion count is a fair measure of how far a list is from
            sorted.
            """,
        ]),
        ("template", "The template", [
            "Count inversions, pairs `i < j` with `a[i] > a[j]`, while merge sorting a copy.",
            code(
                "Count inversions with merge sort",
                INV,
                [
                    ("base", "Fewer than two values: no pairs."),
                    ("split", "The middle of `[lo, hi)`."),
                    ("halves", "Pairs inside each half, counted (and sorted) recursively.",
                     {"java": "Counts can reach about n²/2, so they're `long`.",
                      "cpp": "`long long`: up to about n²/2 pairs.",
                      "c": "`long long`: up to about n²/2 pairs."}),
                    ("merge", "The usual merge: `i` in the left half, `j` in the right, `k` in the buffer."),
                    ("left", "A left value goes first (ties too). It's not bigger than anything still waiting on the right."),
                    ("right", "A right value goes first: it's smaller than every left value still waiting."),
                    ("count", "Those `mid - i` waiting left values each form an inversion with it."),
                    ("rest", "Copy the leftovers and write the merged range back."),
                    ("ret", "Inversions inside this range."),
                    ("start", "Sort a copy (the caller's order is the whole point) with one shared buffer.",
                     {"c": "Copy the input, sort-and-count, then free both arrays."}),
                ],
                INV_RUN,
                "count_inversions([5, 2, 6, 1, 3]); ([1, 2, 3]); ([4, 3, 2, 1]); ([2, 2, 1])",
            ),
            """
            `[4, 3, 2, 1]` is fully reversed, so every one of its 6 pairs is an inversion. `[2, 2, 1]` has 2: the equal 2s
            don't count.
            """,
        ]),
        ("trace", "Trace it by hand", [
            f"""
            For a small list, write out the recursion: split down to single values, then merge back up, writing the count
            next to each merge. For `{DEMO}` the merges count {', '.join(c for *_, c in merge_rows)}, which adds up to
            {len(PAIRS)}, the same as the table of pairs in *The idea*. If your hand trace and a brute-force count disagree,
            the mistake is almost always in which side ties go to, or in counting `mid - i` versus `mid - i + 1`.

            As a check, bubble sort on `{DEMO}` makes exactly {swaps} neighbour swaps.

            Here's the whole recursion, one merge per step:
            """,
            walk(ftw, legend={"found": "the range just merged (now sorted)"}),
        ]),
        ("examples", "More examples", [
            f"""
            ### Drops of more than d

            Count pairs of days `i < j` where the price fell by more than `d`: `a[i] - a[j] > d`. That's not the merge's
            own comparison, so count with a separate two-pointer pass on the sorted halves before merging them:
            """,
            walk(dw, legend={"dim": "skipped: not more than d bigger", "found": "more than d bigger: counted", "active": "the right value being matched"}),
            f"""
            On the whole of `{DROPS_IN}` with `d = 4` that finds {DROPS_OUT} drops.

            ### A count for every item

            Sometimes you want, for each item, how many later items are smaller than it: here `{PER}` for `{DEMO}`. The
            merge works the same way, but the counts must be credited to the right item, and items move around while
            sorting. So sort *indices* (or `(value, index)` pairs) instead of bare values, and keep a result array indexed
            by original position. When a left item is placed, it's bigger than every right item that has already been
            placed before it, so credit it with that number.

            ### How far from sorted?

            Comparing two rankings of the same items (two judges, or a list before and after a change) comes down to
            inversions: rewrite one ranking in terms of the other's order, and count. Zero means they agree completely;
            `n(n - 1) / 2` means one is the reverse of the other.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Counting with a separate pass

            The general form: recurse, then count crossing pairs with a forward-only pointer, then merge. Counting and
            merging are kept apart, so any condition that's monotonic in the right value works.
            """,
            code(
                "Count pairs where the earlier value is more than d bigger",
                DROPS,
                [
                    ("base", "Split, and count each half's own pairs (sorting it) recursively.",
                     {"java": "`d` is a `long`, so `a[j] + d` can't overflow.",
                      "cpp": "`d` is `long long`, so `a[j] + d` can't overflow.",
                      "c": "`d` is `long long`, so `a[j] + d` can't overflow."}),
                    ("pair", "Both halves are sorted. Walk the right half, with `i` pointing into the left half."),
                    ("skip", "Move past left values that aren't more than `d` bigger than this right value. The threshold "
                             "only rises, so `i` never moves back."),
                    ("add", "Every left value from `i` on is more than `d` bigger."),
                    ("merge", "Now merge the halves, exactly as in merge sort.",
                     {"python": "`sorted` on two sorted runs is a merge in practice (Timsort spots the runs); it keeps the code short.",
                      "cpp": "`std::merge` merges two sorted ranges into the buffer."}),
                    ("ret", "Pairs in this range."),
                    ("start", "Work on a copy, with one shared buffer.", {"c": "Copy, count, then free both arrays."}),
                ],
                DROPS_RUN,
                "count_drops([9, 2, 7, 1, 8, 3], 4); (same, 0); ([1, 2, 3], 0)",
            ),
            """
            With `d = 0` it counts ordinary inversions, which is a good way to test it against the template.

            ### Fenwick trees

            Another way to count inversions: walk the array from the right, and for each value ask "how many values
            already seen are smaller?" using a Fenwick tree over the values (compressed to ranks first). Also O(n log n),
            and it handles values arriving one at a time. You'll meet it later; merge sort needs nothing new.

            ### Counting ranges of sums

            Count the subarrays whose sum lies in `[low, high]`: build prefix sums (*Prefix sums*), and count pairs
            `i < j` with `low ≤ P[j] - P[i] ≤ high`. That's this pattern again, with two forward-only pointers in the
            counting pass.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            The same as merge sort: O(n log n) time, because each level does O(n) merging plus O(n) counting, and there
            are `log n` levels. O(n) extra space for the buffer (and the copy of the input). The count itself can be as
            large as `n(n - 1) / 2`, about 5 × 10⁹ for n = 10⁵, which doesn't fit in a 32-bit `int`.
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Check every pair", "O(n²)", "O(1)"],
                ["Merge sort, count during the merge", "O(n log n)", "O(n)"],
                ["Merge sort, separate counting pass", "O(n log n)", "O(n)"],
                ["Fenwick tree over ranks", "O(n log n)", "O(n)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            Integers don't overflow, so counts are safe. Recursion depth is only `log₂ n`. For speed on big inputs, avoid
            slicing inside the merge loop; index into one shared buffer as the template does.

            ### Java

            Return counts as `long`. Use `>>> 1` for the midpoint and `System.arraycopy` to write merged ranges back.
            Clone the input so the caller's array keeps its order.

            ### C++

            `long long` for counts and for `a[j] + d` style thresholds. `std::merge` can do the merging, but the counting
            in the template has to be inside your own merge loop.

            ### C

            `long long` counts, printed with `%lld`. `malloc` the copy and the buffer once, pass them down, and `free`
            them at the end.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Counting in a 32-bit `int`: the count overflows long before `n` is large.
            - Taking from the right on ties, which counts equal values as inversions.
            - Adding `mid - i + 1` or `hi - j`: draw a three-element example and check.
            - Doing the counting pass *after* merging, when the halves are no longer separate.
            - Thresholds like `a[j] + d` or `2 * a[j]` overflowing.
            - Counting on the caller's array and sorting it as a side effect.
            - Credit going to the wrong item in per-item counts because values moved; carry original indices.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why is every inversion counted exactly once?",
                 "Each pair of positions is split onto opposite sides at exactly one level of the recursion, and only that level's merge counts crossing pairs."),
                ("When a right value is taken during the merge, why add mid - i?",
                 "The left values a[i..mid-1] are all still waiting, so they're all bigger than it, and every left value came earlier in the array."),
                ("How many inversions does [3, 1, 2] have, and how many neighbour swaps sort it?",
                 "Two: (3, 1) and (3, 2). And two neighbour swaps: 3↔1, then 3↔2."),
                ("Why count 'more than twice' pairs in a separate pass instead of during the merge?",
                 "The merge compares a[i] with a[j], but the condition compares a[i] with 2·a[j]. A separate pass with its own forward-only pointer counts the condition correctly."),
                ("What's the largest possible inversion count for n values?",
                 "n(n - 1) / 2, when the values are strictly decreasing."),
            ),
        ]),
    ],
)
