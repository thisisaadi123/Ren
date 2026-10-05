"""Lesson: k-Sum (Two Pointers, pattern 3)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

FOUR = {
    "python": """
        def four_sum(nums, target):
            a = sorted(nums)                                    #@sort
            n, out = len(a), []                                 #@sort
            for i in range(n - 3):                              #@first
                if i > 0 and a[i] == a[i - 1]:                  #@skip1
                    continue                                    #@skip1
                for j in range(i + 1, n - 2):                   #@second
                    if j > i + 1 and a[j] == a[j - 1]:          #@skip2
                        continue                                #@skip2
                    need = target - a[i] - a[j]                 #@need
                    lo, hi = j + 1, n - 1                       #@pair
                    while lo < hi:                              #@pair
                        s = a[lo] + a[hi]                       #@pair
                        if s < need:                            #@move
                            lo += 1                             #@move
                        elif s > need:                          #@move
                            hi -= 1                             #@move
                        else:                                   #@hit
                            out.append([a[i], a[j], a[lo], a[hi]])  #@hit
                            lo, hi = lo + 1, hi - 1             #@hit
                            while lo < hi and a[lo] == a[lo - 1]:   #@dedupe
                                lo += 1                         #@dedupe
            return out                                          #@ret
    """,
    "java": """
        static List<int[]> fourSum(int[] nums, long target) {
            int[] a = nums.clone();                             //@sort
            Arrays.sort(a);                                     //@sort
            int n = a.length;                                   //@sort
            List<int[]> out = new ArrayList<>();                //@sort
            for (int i = 0; i < n - 3; i++) {                   //@first
                if (i > 0 && a[i] == a[i - 1]) continue;        //@skip1
                for (int j = i + 1; j < n - 2; j++) {           //@second
                    if (j > i + 1 && a[j] == a[j - 1]) continue;    //@skip2
                    long need = target - a[i] - a[j];           //@need
                    int lo = j + 1, hi = n - 1;                 //@pair
                    while (lo < hi) {                           //@pair
                        long s = (long) a[lo] + a[hi];          //@pair
                        if (s < need) lo++;                     //@move
                        else if (s > need) hi--;                //@move
                        else {                                  //@hit
                            out.add(new int[] {a[i], a[j], a[lo], a[hi]});  //@hit
                            lo++;                               //@hit
                            hi--;                               //@hit
                            while (lo < hi && a[lo] == a[lo - 1]) lo++;     //@dedupe
                        }
                    }
                }
            }
            return out;                                         //@ret
        }
    """,
    "cpp": """
        vector<array<int, 4>> fourSum(vector<int> a, long long target) {
            sort(a.begin(), a.end());                           //@sort
            int n = a.size();                                   //@sort
            vector<array<int, 4>> out;                          //@sort
            for (int i = 0; i < n - 3; i++) {                   //@first
                if (i > 0 && a[i] == a[i - 1]) continue;        //@skip1
                for (int j = i + 1; j < n - 2; j++) {           //@second
                    if (j > i + 1 && a[j] == a[j - 1]) continue;    //@skip2
                    long long need = target - a[i] - a[j];      //@need
                    int lo = j + 1, hi = n - 1;                 //@pair
                    while (lo < hi) {                           //@pair
                        long long s = (long long)a[lo] + a[hi]; //@pair
                        if (s < need) lo++;                     //@move
                        else if (s > need) hi--;                //@move
                        else {                                  //@hit
                            out.push_back({a[i], a[j], a[lo], a[hi]});  //@hit
                            lo++;                               //@hit
                            hi--;                               //@hit
                            while (lo < hi && a[lo] == a[lo - 1]) lo++;     //@dedupe
                        }
                    }
                }
            }
            return out;                                         //@ret
        }
    """,
    "c": """
        static int cmpInt(const void* x, const void* y) {
            int a = *(const int*)x, b = *(const int*)y;         //@cmp
            return (a > b) - (a < b);                           //@cmp
        }

        int fourSum(const int* nums, int n, long long target, int (*out)[4]) {
            int* a = malloc((n > 0 ? n : 1) * sizeof(int));     //@sort
            memcpy(a, nums, n * sizeof(int));                   //@sort
            qsort(a, n, sizeof(int), cmpInt);                   //@sort
            int found = 0;                                      //@sort
            for (int i = 0; i < n - 3; i++) {                   //@first
                if (i > 0 && a[i] == a[i - 1]) continue;        //@skip1
                for (int j = i + 1; j < n - 2; j++) {           //@second
                    if (j > i + 1 && a[j] == a[j - 1]) continue;    //@skip2
                    long long need = target - a[i] - a[j];      //@need
                    int lo = j + 1, hi = n - 1;                 //@pair
                    while (lo < hi) {                           //@pair
                        long long s = (long long)a[lo] + a[hi]; //@pair
                        if (s < need) lo++;                     //@move
                        else if (s > need) hi--;                //@move
                        else {                                  //@hit
                            int* q = out[found++];              //@hit
                            q[0] = a[i]; q[1] = a[j]; q[2] = a[lo]; q[3] = a[hi];  //@hit
                            lo++;                               //@hit
                            hi--;                               //@hit
                            while (lo < hi && a[lo] == a[lo - 1]) lo++;     //@dedupe
                        }
                    }
                }
            }
            free(a);                                            //@ret
            return found;                                       //@ret
        }
    """,
}
FOUR_RUN = {
    "python": """
        tests = [([1, 0, -1, 0, -2, 2], 0), ([2, 2, 2, 2, 2], 8), ([1, 2, 3], 6), ([10**9] * 4, -294967296)]
        for nums, t in tests:
            qs = four_sum(nums, t)
            print(" | ".join(" ".join(map(str, q)) for q in qs) if qs else "none")
    """,
    "java": """
        static void show(List<int[]> qs) {
            if (qs.isEmpty()) { System.out.println("none"); return; }
            StringBuilder sb = new StringBuilder();
            for (int[] q : qs) {
                if (sb.length() > 0) sb.append(" | ");
                sb.append(q[0]).append(" ").append(q[1]).append(" ").append(q[2]).append(" ").append(q[3]);
            }
            System.out.println(sb);
        }

        public static void main(String[] args) {
            show(fourSum(new int[] {1, 0, -1, 0, -2, 2}, 0));
            show(fourSum(new int[] {2, 2, 2, 2, 2}, 8));
            show(fourSum(new int[] {1, 2, 3}, 6));
            show(fourSum(new int[] {1000000000, 1000000000, 1000000000, 1000000000}, -294967296));
        }
    """,
    "cpp": """
        void show(const vector<array<int, 4>>& qs) {
            if (qs.empty()) { cout << "none\\n"; return; }
            for (size_t k = 0; k < qs.size(); k++)
                cout << (k ? " | " : "") << qs[k][0] << " " << qs[k][1] << " " << qs[k][2] << " " << qs[k][3];
            cout << "\\n";
        }

        int main() {
            show(fourSum({1, 0, -1, 0, -2, 2}, 0));
            show(fourSum({2, 2, 2, 2, 2}, 8));
            show(fourSum({1, 2, 3}, 6));
            show(fourSum({1000000000, 1000000000, 1000000000, 1000000000}, -294967296));
        }
    """,
    "c": """
        static void show(int (*qs)[4], int m) {
            if (m == 0) { printf("none\\n"); return; }
            for (int k = 0; k < m; k++)
                printf("%s%d %d %d %d", k ? " | " : "", qs[k][0], qs[k][1], qs[k][2], qs[k][3]);
            printf("\\n");
        }

        int main(void) {
            int out[16][4];
            int a[] = {1, 0, -1, 0, -2, 2}, b[] = {2, 2, 2, 2, 2}, c[] = {1, 2, 3};
            int d[] = {1000000000, 1000000000, 1000000000, 1000000000};
            show(out, fourSum(a, 6, 0, out));
            show(out, fourSum(b, 5, 8, out));
            show(out, fourSum(c, 3, 6, out));
            show(out, fourSum(d, 4, -294967296, out));
            return 0;
        }
    """,
}

TRI = {
    "python": """
        def count_triangles(sides):
            a = sorted(sides)                                   #@sort
            count = 0                                           #@count
            for k in range(len(a) - 1, 1, -1):                  #@big
                lo, hi = 0, k - 1                               #@pair
                while lo < hi:                                  #@pair
                    if a[lo] + a[hi] > a[k]:                    #@ok
                        count += hi - lo                        #@ok
                        hi -= 1                                 #@ok
                    else:                                       #@short
                        lo += 1                                 #@short
            return count                                        #@ret
    """,
    "java": """
        static long countTriangles(int[] sides) {
            int[] a = sides.clone();                            //@sort
            Arrays.sort(a);                                     //@sort
            long count = 0;                                     //@count
            for (int k = a.length - 1; k >= 2; k--) {           //@big
                int lo = 0, hi = k - 1;                         //@pair
                while (lo < hi) {                               //@pair
                    if (a[lo] + a[hi] > a[k]) {                 //@ok
                        count += hi - lo;                       //@ok
                        hi--;                                   //@ok
                    } else {                                    //@short
                        lo++;                                   //@short
                    }
                }
            }
            return count;                                       //@ret
        }
    """,
    "cpp": """
        long long countTriangles(vector<int> a) {
            sort(a.begin(), a.end());                           //@sort
            long long count = 0;                                //@count
            for (int k = (int)a.size() - 1; k >= 2; k--) {      //@big
                int lo = 0, hi = k - 1;                         //@pair
                while (lo < hi) {                               //@pair
                    if (a[lo] + a[hi] > a[k]) {                 //@ok
                        count += hi - lo;                       //@ok
                        hi--;                                   //@ok
                    } else {                                    //@short
                        lo++;                                   //@short
                    }
                }
            }
            return count;                                       //@ret
        }
    """,
    "c": """
        static int cmpSide(const void* x, const void* y) {
            int a = *(const int*)x, b = *(const int*)y;         //@sort
            return (a > b) - (a < b);                           //@sort
        }

        long long countTriangles(const int* sides, int n) {
            int* a = malloc((n > 0 ? n : 1) * sizeof(int));     //@sort
            memcpy(a, sides, n * sizeof(int));                  //@sort
            qsort(a, n, sizeof(int), cmpSide);                  //@sort
            long long count = 0;                                //@count
            for (int k = n - 1; k >= 2; k--) {                  //@big
                int lo = 0, hi = k - 1;                         //@pair
                while (lo < hi) {                               //@pair
                    if (a[lo] + a[hi] > a[k]) {                 //@ok
                        count += hi - lo;                       //@ok
                        hi--;                                   //@ok
                    } else {                                    //@short
                        lo++;                                   //@short
                    }
                }
            }
            free(a);                                            //@ret
            return count;                                       //@ret
        }
    """,
}
TRI_RUN = {
    "python": """
        print(count_triangles([2, 2, 3, 4]))
        print(count_triangles([4, 2, 3, 4]))
        print(count_triangles([1, 2, 3]))
        print(count_triangles([5, 5, 5, 5]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(countTriangles(new int[] {2, 2, 3, 4}));
            System.out.println(countTriangles(new int[] {4, 2, 3, 4}));
            System.out.println(countTriangles(new int[] {1, 2, 3}));
            System.out.println(countTriangles(new int[] {5, 5, 5, 5}));
        }
    """,
    "cpp": """
        int main() {
            cout << countTriangles({2, 2, 3, 4}) << "\\n";
            cout << countTriangles({4, 2, 3, 4}) << "\\n";
            cout << countTriangles({1, 2, 3}) << "\\n";
            cout << countTriangles({5, 5, 5, 5}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {2, 2, 3, 4}, b[] = {4, 2, 3, 4}, c[] = {1, 2, 3}, d[] = {5, 5, 5, 5};
            printf("%lld\\n", countTriangles(a, 4));
            printf("%lld\\n", countTriangles(b, 4));
            printf("%lld\\n", countTriangles(c, 3));
            printf("%lld\\n", countTriangles(d, 4));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

from itertools import combinations  # noqa: E402

four_sum = py(FOUR["python"], "four_sum")
count_triangles = py(TRI["python"], "count_triangles")


def brute_four(nums, t):
    return sorted({tuple(sorted(c)) for c in combinations(nums, 4) if sum(c) == t})


for nums, t in [([1, 0, -1, 0, -2, 2], 0), ([2, 2, 2, 2, 2], 8), ([1, 2, 3], 6), ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], 14), ([0, 0, 0, 0, 0, 0], 0)]:
    assert [tuple(q) for q in four_sum(nums, t)] == brute_four(nums, t), (nums, t)
for s in ([2, 2, 3, 4], [4, 2, 3, 4], [1, 2, 3], [5, 5, 5, 5], [3, 4, 5, 6, 7, 10]):
    assert count_triangles(s) == sum(1 for x, y, z in combinations(sorted(s), 3) if x + y > z)

# Theory walk: three values adding up to 9, with a repeated value to skip.
KA, KT = [1, 2, 2, 3, 4, 6], 9
kw = Steps(f"Distinct triples from `{KA}` (already sorted) adding up to {KT}. Fix the first value, then run opposite ends on the rest.")
found = []


def ks(i, lo=None, hi=None, hit=False, skip=False):
    st = {}
    if skip:
        st[i] = "dim"
    else:
        st[i] = "mark"
        for p in (lo, hi):
            if p is not None:
                st[p] = "answer" if hit else "active"
    return st


def fstr():
    return ", ".join("(" + " ".join(map(str, t)) + ")" for t in found) or "none yet"


kw.step("Sorted, so equal values sit together and opposite ends work on any suffix.",
        Row(KA, slots=True, label="sorted"), M({"first value": "–", "need from the pair": "–", "triples": fstr()}))
for i in range(len(KA) - 2):
    if i > 0 and KA[i] == KA[i - 1]:
        kw.step(f"Index {i} holds {KA[i]} again. Every triple starting with {KA[i]} was already found with the first {KA[i]}, so skip it.",
                Row(KA, st=ks(i, skip=True), ptr={"i": i}, slots=True, label="sorted"), M({"first value": KA[i], "need from the pair": "–", "triples": fstr()}))
        continue
    need = KT - KA[i]
    lo, hi = i + 1, len(KA) - 1
    first = True
    while lo < hi:
        s = KA[lo] + KA[hi]
        lead = f"Fix {KA[i]} at index {i}: the other two must add up to {KT} - {KA[i]} = {need}. " if first else ""
        first = False
        if s < need:
            kw.step(lead + f"{KA[lo]} + {KA[hi]} = {s}, too small: move `lo` right.",
                    Row(KA, st=ks(i, lo, hi), ptr={"i": i, "lo": lo, "hi": hi}, slots=True, label="sorted"), M({"first value": KA[i], "need from the pair": need, "triples": fstr()}))
            lo += 1
        elif s > need:
            kw.step(lead + f"{KA[lo]} + {KA[hi]} = {s}, too big: move `hi` left.",
                    Row(KA, st=ks(i, lo, hi), ptr={"i": i, "lo": lo, "hi": hi}, slots=True, label="sorted"), M({"first value": KA[i], "need from the pair": need, "triples": fstr()}))
            hi -= 1
        else:
            found.append((KA[i], KA[lo], KA[hi]))
            olo = lo
            lo, hi = lo + 1, hi - 1
            skipped = 0
            while lo < hi and KA[lo] == KA[lo - 1]:
                lo += 1
                skipped += 1
            extra = f" The next value on the left is another {KA[olo]}, which would only find the same triple, so `lo` skips past it." if skipped else ""
            kw.step(lead + f"{KA[olo]} + {KA[hi + 1]} = {need}. Found ({KA[i]}, {KA[olo]}, {KA[hi + 1]}). Move both pointers.{extra}",
                    Row(KA, st=ks(i, olo, hi + 1, hit=True), ptr={"i": i, "lo": olo, "hi": hi + 1}, slots=True, label="sorted"), M({"first value": KA[i], "need from the pair": need, "triples": fstr()}))
    if first:
        kw.step(f"Fix {KA[i]} at index {i}: fewer than two values after it, nothing to pair.",
                Row(KA, st=ks(i), ptr={"i": i}, slots=True, label="sorted"), M({"first value": KA[i], "need from the pair": need, "triples": fstr()}))
assert found == sorted({tuple(sorted(c)) for c in combinations(KA, 3) if sum(c) == KT})
kw.steps[-1]["text"] += f" Every first value has been tried: {len(found)} triples, each found once."
K_LEGEND = {"mark": "the fixed first value", "active": "the pair being tried", "answer": "a triple that works", "dim": "a repeated first value, skipped"}

# Trace of four_sum: one step per (i, j).
FA, FT = sorted([1, 0, -1, 0, -2, 2]), 0
tw = Steps(f"`four_sum([1, 0, -1, 0, -2, 2], 0)` after sorting to `{FA}`. One step per choice of the first two values.")
quads = []


def qstr():
    return " | ".join(" ".join(map(str, q)) for q in quads) or "none yet"


tw.step("Sorted. The two outer loops choose `a[i]` and `a[j]`; opposite ends find every pair after `j` that completes them.",
        Row(FA, slots=True, label="sorted"), M({"first two": "–", "need": "–", "found": qstr()}))
n = len(FA)
for i in range(n - 3):
    if i > 0 and FA[i] == FA[i - 1]:
        tw.step(f"`i` = {i}: another {FA[i]} as the first value. Skip it.", Row(FA, st={i: "dim"}, slots=True, label="sorted"),
                M({"first two": f"{FA[i]}, …", "need": "–", "found": qstr()}))
        continue
    for j in range(i + 1, n - 2):
        if j > i + 1 and FA[j] == FA[j - 1]:
            tw.step(f"`i` = {i}, `j` = {j}: {FA[j]} again as the second value, after {FA[i]}. Skip it.", Row(FA, st={i: "mark", j: "dim"}, slots=True, label="sorted"),
                    M({"first two": f"{FA[i]}, {FA[j]}", "need": "–", "found": qstr()}))
            continue
        need = FT - FA[i] - FA[j]
        lo, hi, hits = j + 1, n - 1, []
        while lo < hi:
            s = FA[lo] + FA[hi]
            if s < need:
                lo += 1
            elif s > need:
                hi -= 1
            else:
                hits.append((lo, hi))
                quads.append([FA[i], FA[j], FA[lo], FA[hi]])
                lo, hi = lo + 1, hi - 1
                while lo < hi and FA[lo] == FA[lo - 1]:
                    lo += 1
        st = {i: "mark", j: "mark"}
        for p in hits:
            st[p[0]] = st[p[1]] = "answer"
        got = ("; ".join(f"{FA[a]} + {FA[b]}" for a, b in hits) + f" works, giving {len(hits)} quadruple{'s' if len(hits) > 1 else ''}") if hits else "no pair works"
        tw.step(f"`i` = {i}, `j` = {j}: {FA[i]} and {FA[j]}, so the last two must add up to {need}. Opposite ends over indices {j + 1} to {n - 1}: {got}.",
                Row(FA, st=st, slots=True, label="sorted"), M({"first two": f"{FA[i]}, {FA[j]}", "need": need, "found": qstr()}))
assert quads == four_sum([1, 0, -1, 0, -2, 2], 0)
T_LEGEND = {"mark": "the two fixed values", "answer": "a pair that completes them", "dim": "a repeated value, skipped"}

# Example: one value from each of three lists.
LA, LB, LC, LT = [2, 5, 9], [1, 3, 4, 8], [2, 6, 7, 10], 15
x_rows, x_found = [], []
for x in LA:
    need = LT - x
    lo, hi, got = 0, len(LC) - 1, []
    while lo < len(LB) and hi >= 0:
        s = LB[lo] + LC[hi]
        if s < need:
            lo += 1
        elif s > need:
            hi -= 1
        else:
            got.append(f"{LB[lo]} + {LC[hi]}")
            x_found.append((x, LB[lo], LC[hi]))
            lo += 1
            hi -= 1
    x_rows.append((str(x), str(need), ", ".join(got) or "none"))
assert sorted(x_found) == sorted((x, y, z) for x in LA for y in LB for z in LC if x + y + z == LT)

# How the work grows with k.
GROW = [(str(k), f"O(n^{k - 1})" if k > 2 else "O(n)", f"O(n^{k})") for k in (2, 3, 4)]

N3 = 2000

lesson(
    "two-pointers",
    "k-sum",
    """
    To find three (or four, or k) values that add up to a target, sort once, fix the first value with a loop, and
    solve the rest as a smaller problem of the same kind. When only two values are left, opposite ends finish the job
    in one pass. Skipping repeated values at each level makes every answer come out exactly once.
    """,
    [
        ("idea", "The idea", [
            f"""
            You're packing a crate that has to weigh exactly {KT} kg, using three of the boxes on a shelf sorted by
            weight: `{KA}`. Trying every three boxes works but grows fast. Instead, pick up the first box and hold it.
            Now the question is smaller: which *two* of the boxes after it make up the rest? That's a pair-sum on a
            sorted shelf, which two pointers answer in one sweep. Put the box down, pick up the next one, and repeat.

            Four boxes works the same way: hold two, sweep for the last two. In general, `k` values means `k - 2`
            nested loops around one opposite-ends sweep.

            The shelf being sorted does a second job too. Two boxes of the same weight sit side by side, so if you've
            already held a 2 kg box and found everything that goes with it, the next 2 kg box can only find the same
            triples again. Skip it.
            """,
            fig(Row(KA, st={0: "mark", 2: "answer", 5: "answer"}, ptr={"i": 0, "lo": 2, "hi": 5}, slots=True, label="hold one, sweep the rest"),
                caption=f"With {KA[0]} held, the pair must make {KT - KA[0]}. Opposite ends over everything to its right find it."),
            key("""
            Sort. Loop over the first value (skipping repeats), then (for 4-sum) the second, then find the last two
            with opposite ends on what's left, moving past repeats after each find. 3-sum is O(n²) and 4-sum is O(n³),
            with O(1) extra space besides the output.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            Three or more values from one array whose sum must equal, approach or stay under a target, especially with
            "distinct triples", "no duplicate answers", or `n` up to a few thousand (which allows O(n²) but not O(n³)).
            """,
            table(
                ["The problem says…", "inside the two-pointer sweep"],
                ["all distinct triples (or quadruples) with sum `t`", "record a hit, move both, skip repeats"],
                ["the triple whose sum is closest to `t`", "track the closest sum seen; move towards `t`"],
                ["count triples with sum below `t`", "when the pair fits, add `hi - lo` at once"],
                ["count triples that can form a triangle", "fix the longest side, count pairs whose sum beats it"],
                ["count triples by position, values repeat", "count runs, as in *Opposite ends*"],
            ),
            """
            Not a fit:

            - Two values only. That's plain *Opposite ends*, or a hash map if the array isn't sorted and positions matter.
            - The values come from separate lists and you only need a count, as in "how many `a + b + c + d = 0` with
              one from each of four lists". Meet in the middle with a hash map is O(n²) for that (*Complement
              lookup*).
            - `k` is large or variable, and the values are small non-negative integers. That's a subset-sum dynamic
              programming problem.
            - The answer needs the original positions in order (`i < j < k` matters, not just the values). Sorting
              shuffles positions; you'd sort `(value, index)` pairs or think again.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### One level at a time

            Every triple, once sorted, has a smallest value. Fixing `a[i]` as that smallest value and searching only to
            its right means each triple is looked for exactly once, under its first value. What's left is "two values
            after `i` adding up to `t - a[i]`", which is a pair-sum on a sorted suffix. Opposite ends solves it in
            O(n), so 3-sum costs O(n) per first value, O(n²) in all.

            Four values is the same with one more loop: fix `a[i]`, then `a[j]` with `j > i`, then sweep. Each extra
            value costs one more factor of `n`.
            """,
            table(["k", "two pointers inside k - 2 loops", "trying every k-tuple"], *GROW),
            """
            ### Skipping repeats

            Sorting puts equal values next to each other, and that's what makes duplicate answers easy to stop. There
            are two places where the same answer could appear twice:

            - The same value fixed twice at one level. If `a[i] == a[i - 1]`, every combination using `a[i]` as the
              first value was already found with `a[i - 1]`, which had at least as many values after it. Skip. The same
              goes for `a[j] == a[j - 1]` at the second level, but only when `j` isn't the first index of its loop
              (`j > i + 1`): the first `j` is allowed to equal `a[i]`, since `[2, 2, …]` uses two different 2s.
            - The same pair found twice in the sweep. After a hit, move `lo` past every copy of the value it just used.
              (`hi` doesn't need its own skip: once `lo` holds a new, bigger value, the same pair of values can't
              come up again.)
            """,
            walk(kw, legend=K_LEGEND),
            """
            ### Counting instead of listing

            When the question asks "how many" rather than "which", the sweep can often count many triples in one step.
            For "sum below `t`", if `a[lo] + a[hi]` fits, so does `a[lo]` with every value between `lo` and `hi`: add
            `hi - lo` and move `lo`. For "can form a triangle", fix the *largest* side `a[k]` and count pairs whose sum
            beats it: if `a[lo] + a[hi] > a[k]`, every `lo` between them works with `hi`, so add `hi - lo` and move
            `hi`. Each sweep stays O(n), so counting is O(n²) even when the answer is O(n³) large.

            ### Overflow

            Four values near 10⁹ add up to 4 × 10⁹, more than a 32-bit `int` holds. Compute the remaining target and
            the pair sums in 64 bits. The template's last test is the classic trap: four copies of 10⁹ wrap around to
            exactly the target in 32-bit arithmetic.
            """,
        ]),
        ("template", "The template", [
            """
            Every distinct set of four values from `nums` that adds up to `target`. Each answer is listed in increasing
            order, and the answers come out sorted.
            """,
            code(
                "Four values with a given sum",
                FOUR,
                [
                    ("sort", "Sort a copy. Equal values become neighbours, and every suffix is ready for opposite ends.",
                     {"c": "Copy with `malloc` and `memcpy`, then `qsort`. At least one element is allocated so `n = 0` is fine."}),
                    ("cmp", "The `qsort` comparator: -1, 0 or 1 without subtracting, so it can't overflow."),
                    ("first", "The smallest value of the four. At least three values must be left after it."),
                    ("skip1", "A repeat of the previous first value would only find the same quadruples."),
                    ("second", "The second value, to the right of the first."),
                    ("skip2", "Repeats are skipped here too, except for the first `j`, which may equal `a[i]` (two different "
                              "copies of the same value)."),
                    ("need", "What the last two must add up to, in 64 bits.",
                     {"java": "`target` is a `long`, so the subtraction happens in `long`."}),
                    ("pair", "Opposite ends over everything after `j`."),
                    ("move", "Too small: the left value can't work with anything. Too big: the right one can't."),
                    ("hit", "A match. Record it and move both pointers inward.",
                     {"c": "The caller supplies room for the answers; `found` counts them."}),
                    ("dedupe", "Step `lo` past copies of the value just used, so the same pair isn't found again."),
                    ("ret", "Every distinct quadruple, in sorted order.", {"c": "Free the sorted copy and return how many were found."}),
                ],
                FOUR_RUN,
                "four_sum([1, 0, -1, 0, -2, 2], 0); ([2, 2, 2, 2, 2], 8); ([1, 2, 3], 6); ([10⁹] × 4, -294967296)",
            ),
            """
            The last test is four copies of 10⁹. Their real sum is 4 × 10⁹, nowhere near the target. In 32-bit
            arithmetic it wraps around to exactly -294967296, and code that adds in `int` reports a quadruple that
            doesn't exist.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "One step per choice of the first two values. The sweep inside each step is the same as in *Opposite ends*:",
            walk(tw, legend=T_LEGEND),
            """
            When you trace 3-sum or 4-sum on paper, write the sorted array once and make a small table: the fixed
            values, the target left for the pair, and the pairs found. Most mistakes show up as the same answer appearing
            in two rows, which means a skip is missing.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### One value from each of three lists

            Pick one value from `{LA}`, one from `{LB}` and one from `{LC}` so they add up to {LT}. Loop over the first
            list, and for each value run a sweep with `lo` at the *start* of the second list and `hi` at the *end* of the
            third. The two pointers are in different lists, but the logic is unchanged: too small moves `lo` forward,
            too big moves `hi` back.
            """,
            table(["from the first list", "the other two must make", "pairs found"], *x_rows),
            f"""
            {len(x_found)} combinations. Both lists in the sweep have to be sorted; the first doesn't.

            ### Closest instead of exact

            For "the triple whose sum is closest to the target", there's no hit to wait for. Every pair the sweep looks
            at is a candidate: compare its distance with the best so far, then move towards the target (too small, `lo`
            right; too big, `hi` left). If a sum equals the target exactly, nothing can be closer, so you can stop.

            ### When the order of positions matters

            "Count `i < j < k` with `a[i] < a[k] < a[j]`" mentions values *and* positions. Sorting would destroy the
            positions, so this isn't k-sum at all. Before you sort, check that the question only cares about which
            values are picked.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Counting triangles

            Three lengths `x ≤ y ≤ z` form a triangle when `x + y > z` (the other two conditions hold automatically).
            Fix the longest side `z` from the right end, and sweep the values before it. If `a[lo] + a[hi] > z`, then
            every value from `lo` up to `hi - 1` also works with `a[hi]`, because those values are at least `a[lo]`.
            That's `hi - lo` triangles in one step, and `hi` moves left. Otherwise `a[lo]` is too short for anything,
            and `lo` moves right.
            """,
            code(
                "Count the triples that can form a triangle",
                TRI,
                [
                    ("sort", "Sort a copy, so the largest side of any triple is the one furthest right.",
                     {"c": "Copy, then `qsort` with an overflow-safe comparator."}),
                    ("count", "The count can grow like n³/6, so it's 64-bit."),
                    ("big", "Fix the longest side, from the right end down to index 2."),
                    ("pair", "Opposite ends over everything before it."),
                    ("ok", "These two beat the longest side, and so does every value between `lo` and `hi` paired with "
                           "`a[hi]`: `hi - lo` triangles. Then `a[hi]` has been fully counted."),
                    ("short", "Too short together. `a[lo]` can't work with any remaining partner, which are all at most `a[hi]`."),
                    ("ret", "The number of triangles.", {"c": "Free the copy first."}),
                ],
                TRI_RUN,
                "count_triangles([2, 2, 3, 4]); ([4, 2, 3, 4]); ([1, 2, 3]); ([5, 5, 5, 5])",
            ),
            """
            `[1, 2, 3]` is no triangle: 1 + 2 is equal to 3, not bigger, so the three sides lie flat.

            ### Any k, recursively

            The loops can be written once as a recursive function: `k_sum(start, k, target)` loops `i` from `start`,
            skips repeats, and calls `k_sum(i + 1, k - 1, target - a[i])`, with `k = 2` handled by opposite ends. It's
            tidy, and it makes the cost obvious: O(n^(k-1)) for `k ≥ 2`.

            ### Pruning

            Because the array is sorted, a loop can stop early. If the smallest possible sum from here
            (`a[i]` plus the next `k - 1` values) is already above the target, no later `i` can do better, so break.
            If the largest possible sum (`a[i]` plus the last `k - 1` values) is below it, this `i` is hopeless, so
            continue. It doesn't change the worst case, but it can skip a lot of work on real data.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            Sorting costs O(n log n). For 3-sum, each of the `n` first values runs an O(n) sweep: O(n²). For 4-sum it's
            O(n³), and in general O(n^(k-1)). Extra space is O(1) besides the output, or O(n) if you sort a copy.

            For `n = {N3:,}`, 3-sum does about {N3 * N3 // 2:,} sweep steps; trying every triple would be about
            {N3 ** 3 // 6:,}.
            """,
            table(
                ["Approach (3 values)", "Time", "Extra space", "Duplicates"],
                ["Try every triple", "O(n³)", "O(1)", "needs a set to remove"],
                ["Fix one, hash set for the pair", "O(n²) on average", "O(n)", "awkward to remove"],
                ["Sort, fix one, opposite ends", "O(n²)", "O(1) to O(n)", "skipped as you go"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `sorted(nums)` for a copy. Integers never overflow, so the 32-bit trap doesn't apply. For speed on large
            inputs, keep the inner sweep simple; Python's per-step cost is high, and O(n²) at `n = 3000` is already
            millions of steps.

            ### Java

            `Arrays.sort(int[])` sorts primitives. Compute the remaining target as `long`. Return
            `List<List<Integer>>` if the problem demands it; `List<int[]>` is lighter while you work.

            ### C++

            `sort` then the same loops. `vector<array<int, 4>>` or `vector<vector<int>>` for answers. Use `long long`
            for `need`. Watch `n - 3` on an unsigned `size()`: with fewer than three elements it wraps around. Cast to
            `int` first.

            ### C

            `qsort` with a comparator that doesn't subtract. The caller usually provides the output buffer; know the
            worst-case number of answers, or grow the buffer with `realloc`.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Forgetting to sort, or sorting after you've started.
            - Skipping a repeat at the *first* index of an inner loop (`j > i + 1`, not `j > 0`), which loses answers
              like `[2, 2, 2, 2]`.
            - Not moving `lo` past repeats after a hit, which lists the same answer twice.
            - Adding in 32 bits. Four values near 10⁹ overflow.
            - Loop bounds that leave fewer than enough values for the inner levels (`i < n - 3` for 4-sum).
            - Using the k-sum loops when the question cares about the original positions' order.
            - `size() - 3` on an unsigned size in C++ when `n < 3`.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why does 3-sum cost O(n²) and not O(n³)?",
                 "Fixing the first value leaves a pair-sum on a sorted suffix, which opposite ends solves in O(n). That's O(n) per first value, so O(n²) overall."),
                ("Why is `a[i] == a[i - 1]` safe to skip at the first level?",
                 "Every combination that starts with that value was already found when the previous copy was fixed, and that copy had at least as many values after it to choose from."),
                ("In 4-sum, why is the second-level skip `j > i + 1 && a[j] == a[j - 1]` rather than `j > 0`?",
                 "The first `j` after `i` may hold the same value as `a[i]`. That's a different copy, and quadruples like [2, 2, 2, 2] need it."),
                ("Counting triangles: why does a match add `hi - lo` and move `hi`?",
                 "If `a[lo] + a[hi]` beats the longest side, so does any value between them paired with `a[hi]`, since those are at least `a[lo]`. That's `hi - lo` triangles that use `a[hi]`, all counted, so `a[hi]` is done."),
                ("[10⁹, 10⁹, 10⁹, 10⁹] with target -294967296 reports a quadruple in some code. Why?",
                 "The sum is 4 × 10⁹, which wraps around to -294967296 in 32-bit arithmetic. Doing the sums in 64 bits fixes it."),
            ),
        ]),
    ],
)
