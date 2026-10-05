"""Lesson: Partition (Two Pointers, pattern 4)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

EVENS = {
    "python": """
        def evens_first(nums):
            lo, hi = 0, len(nums) - 1                       #@ends
            while True:                                     #@loop
                while lo <= hi and nums[lo] % 2 == 0:       #@left
                    lo += 1                                 #@left
                while lo <= hi and nums[hi] % 2 != 0:       #@right
                    hi -= 1                                 #@right
                if lo > hi:                                 #@done
                    return lo                               #@done
                nums[lo], nums[hi] = nums[hi], nums[lo]     #@swap
                lo, hi = lo + 1, hi - 1                     #@swap
    """,
    "java": """
        static int evensFirst(int[] nums) {
            int lo = 0, hi = nums.length - 1;               //@ends
            while (true) {                                  //@loop
                while (lo <= hi && nums[lo] % 2 == 0) lo++; //@left
                while (lo <= hi && nums[hi] % 2 != 0) hi--; //@right
                if (lo > hi) return lo;                     //@done
                int t = nums[lo];                           //@swap
                nums[lo++] = nums[hi];                      //@swap
                nums[hi--] = t;                             //@swap
            }
        }
    """,
    "cpp": """
        int evensFirst(vector<int>& nums) {
            int lo = 0, hi = (int)nums.size() - 1;          //@ends
            while (true) {                                  //@loop
                while (lo <= hi && nums[lo] % 2 == 0) lo++; //@left
                while (lo <= hi && nums[hi] % 2 != 0) hi--; //@right
                if (lo > hi) return lo;                     //@done
                swap(nums[lo++], nums[hi--]);               //@swap
            }
        }
    """,
    "c": """
        int evensFirst(int* nums, int n) {
            int lo = 0, hi = n - 1;                         //@ends
            while (true) {                                  //@loop
                while (lo <= hi && nums[lo] % 2 == 0) lo++; //@left
                while (lo <= hi && nums[hi] % 2 != 0) hi--; //@right
                if (lo > hi) return lo;                     //@done
                int t = nums[lo];                           //@swap
                nums[lo++] = nums[hi];                      //@swap
                nums[hi--] = t;                             //@swap
            }
        }
    """,
}
EVENS_RUN = {
    "python": """
        for nums in [[3, 8, 5, 2, 7, 6, 4, 1], [2, 4, 6], [1, 3], [-3, -2, 0, 5]]:
            k = evens_first(nums)
            print(*nums, "|", k)
    """,
    "java": """
        static void run(int[] a) {
            int k = evensFirst(a);
            StringBuilder sb = new StringBuilder();
            for (int x : a) sb.append(x).append(" ");
            System.out.println(sb + "| " + k);
        }

        public static void main(String[] args) {
            run(new int[] {3, 8, 5, 2, 7, 6, 4, 1});
            run(new int[] {2, 4, 6});
            run(new int[] {1, 3});
            run(new int[] {-3, -2, 0, 5});
        }
    """,
    "cpp": """
        void run(vector<int> a) {
            int k = evensFirst(a);
            for (int x : a) cout << x << " ";
            cout << "| " << k << "\\n";
        }

        int main() {
            run({3, 8, 5, 2, 7, 6, 4, 1});
            run({2, 4, 6});
            run({1, 3});
            run({-3, -2, 0, 5});
        }
    """,
    "c": """
        static void run(int* a, int n) {
            int k = evensFirst(a, n);
            for (int i = 0; i < n; i++) printf("%d ", a[i]);
            printf("| %d\\n", k);
        }

        int main(void) {
            int a[] = {3, 8, 5, 2, 7, 6, 4, 1}, b[] = {2, 4, 6}, c[] = {1, 3}, d[] = {-3, -2, 0, 5};
            run(a, 8);
            run(b, 3);
            run(c, 2);
            run(d, 4);
            return 0;
        }
    """,
}

THREE = {
    "python": """
        def three_way(nums, pivot):
            lt, i, gt = 0, 0, len(nums) - 1                 #@marks
            while i <= gt:                                  #@scan
                if nums[i] < pivot:                         #@less
                    nums[lt], nums[i] = nums[i], nums[lt]   #@less
                    lt, i = lt + 1, i + 1                   #@less
                elif nums[i] > pivot:                       #@more
                    nums[i], nums[gt] = nums[gt], nums[i]   #@more
                    gt -= 1                                 #@more
                else:                                       #@same
                    i += 1                                  #@same
            return lt, gt                                   #@ret
    """,
    "java": """
        static int[] threeWay(int[] nums, int pivot) {
            int lt = 0, i = 0, gt = nums.length - 1;        //@marks
            while (i <= gt) {                               //@scan
                if (nums[i] < pivot) {                      //@less
                    int t = nums[lt]; nums[lt] = nums[i]; nums[i] = t;  //@less
                    lt++;                                   //@less
                    i++;                                    //@less
                } else if (nums[i] > pivot) {               //@more
                    int t = nums[gt]; nums[gt] = nums[i]; nums[i] = t;  //@more
                    gt--;                                   //@more
                } else {                                    //@same
                    i++;                                    //@same
                }
            }
            return new int[] {lt, gt};                      //@ret
        }
    """,
    "cpp": """
        pair<int, int> threeWay(vector<int>& nums, int pivot) {
            int lt = 0, i = 0, gt = (int)nums.size() - 1;   //@marks
            while (i <= gt) {                               //@scan
                if (nums[i] < pivot) {                      //@less
                    swap(nums[lt], nums[i]);                //@less
                    lt++;                                   //@less
                    i++;                                    //@less
                } else if (nums[i] > pivot) {               //@more
                    swap(nums[i], nums[gt]);                //@more
                    gt--;                                   //@more
                } else {                                    //@same
                    i++;                                    //@same
                }
            }
            return {lt, gt};                                //@ret
        }
    """,
    "c": """
        void threeWay(int* nums, int n, int pivot, int* ltOut, int* gtOut) {
            int lt = 0, i = 0, gt = n - 1;                  //@marks
            while (i <= gt) {                               //@scan
                if (nums[i] < pivot) {                      //@less
                    int t = nums[lt]; nums[lt] = nums[i]; nums[i] = t;  //@less
                    lt++;                                   //@less
                    i++;                                    //@less
                } else if (nums[i] > pivot) {               //@more
                    int t = nums[gt]; nums[gt] = nums[i]; nums[i] = t;  //@more
                    gt--;                                   //@more
                } else {                                    //@same
                    i++;                                    //@same
                }
            }
            *ltOut = lt;                                    //@ret
            *gtOut = gt;                                    //@ret
        }
    """,
}
THREE_RUN = {
    "python": """
        for nums, p in [([4, 9, 4, 1, 7, 4, 2, 8], 4), ([5, 5, 5], 5), ([1, 2, 3], 0)]:
            lt, gt = three_way(nums, p)
            print(*nums, "|", lt, gt)
    """,
    "java": """
        static void run(int[] a, int p) {
            int[] b = threeWay(a, p);
            StringBuilder sb = new StringBuilder();
            for (int x : a) sb.append(x).append(" ");
            System.out.println(sb + "| " + b[0] + " " + b[1]);
        }

        public static void main(String[] args) {
            run(new int[] {4, 9, 4, 1, 7, 4, 2, 8}, 4);
            run(new int[] {5, 5, 5}, 5);
            run(new int[] {1, 2, 3}, 0);
        }
    """,
    "cpp": """
        void run(vector<int> a, int p) {
            auto [lt, gt] = threeWay(a, p);
            for (int x : a) cout << x << " ";
            cout << "| " << lt << " " << gt << "\\n";
        }

        int main() {
            run({4, 9, 4, 1, 7, 4, 2, 8}, 4);
            run({5, 5, 5}, 5);
            run({1, 2, 3}, 0);
        }
    """,
    "c": """
        static void run(int* a, int n, int p) {
            int lt, gt;
            threeWay(a, n, p, &lt, &gt);
            for (int i = 0; i < n; i++) printf("%d ", a[i]);
            printf("| %d %d\\n", lt, gt);
        }

        int main(void) {
            int a[] = {4, 9, 4, 1, 7, 4, 2, 8}, b[] = {5, 5, 5}, c[] = {1, 2, 3};
            run(a, 8, 4);
            run(b, 3, 5);
            run(c, 3, 0);
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

import random  # noqa: E402

evens_first = py(EVENS["python"], "evens_first")
three_way = py(THREE["python"], "three_way")

rng = random.Random(5)
for _ in range(300):
    xs = [rng.randint(-9, 9) for _ in range(rng.randint(0, 9))]
    ys = list(xs)
    k = evens_first(ys)
    assert sorted(ys) == sorted(xs) and k == sum(1 for x in xs if x % 2 == 0)
    assert all(y % 2 == 0 for y in ys[:k]) and all(y % 2 for y in ys[k:])
    p = rng.randint(-9, 9)
    zs = list(xs)
    lt, gt = three_way(zs, p)
    assert sorted(zs) == sorted(xs) and all(z < p for z in zs[:lt]) and all(z == p for z in zs[lt:gt + 1]) and all(z > p for z in zs[gt + 1:])

DEMO = [3, 8, 5, 2, 7, 6, 4, 1]
N_EVEN = sum(1 for x in DEMO if x % 2 == 0)
AFTER = list(DEMO)
evens_first(AFTER)


def lomuto_swaps(xs):
    a, store, sw = list(xs), 0, 0
    for i in range(len(a)):
        if a[i] % 2 == 0:
            if i != store:
                a[i], a[store] = a[store], a[i]
                sw += 1
            store += 1
    return sw


def ends_swaps(xs):
    a, lo, hi, sw = list(xs), 0, len(xs) - 1, 0
    while True:
        while lo <= hi and a[lo] % 2 == 0:
            lo += 1
        while lo <= hi and a[hi] % 2 != 0:
            hi -= 1
        if lo > hi:
            return sw
        a[lo], a[hi] = a[hi], a[lo]
        sw += 1
        lo, hi = lo + 1, hi - 1


SWAP_ROWS = [(str(xs), str(lomuto_swaps(xs)), str(ends_swaps(xs))) for xs in (DEMO, [1, 2, 4, 6, 8, 10], [1, 3, 5, 2], [2, 4, 1, 3])]

# Theory walk: the one-direction (Lomuto) version on the same array.
lw = Steps(f"Evens first in `{DEMO}`, with both pointers starting on the left. `store` marks where the next even value goes.")
a, store, sw = list(DEMO), 0, 0
lw.step("Nothing scanned yet. Everything left of `store` will be even.", Row(list(a), ptr={"i": 0, "store": 0}, slots=True, label="nums"), M({"swaps": 0}))
for i in range(len(a)):
    x = a[i]
    if x % 2 == 0:
        if i != store:
            a[i], a[store] = a[store], a[i]
            sw += 1
            msg = f"`i` = {i}: {x} is even. Swap it with the odd value at `store` (index {store}), and `store` moves on."
        else:
            msg = f"`i` = {i}: {x} is even and already at `store`. No swap needed; `store` moves on."
        store += 1
    else:
        msg = f"`i` = {i}: {x} is odd. Leave it; it's in the odd part for now."
    lw.step(msg, Row(list(a), st={**{k: "found" for k in range(store)}, **{k: "mark" for k in range(store, i + 1)}}, ptr={"i": i, "store": store if store < len(a) else None}, slots=True, label="nums"),
            M({"swaps": sw}))
LOMUTO = sw
_a, _st, _pos, THREE_MOVES = list(DEMO), 0, 0, 0
for _i in range(len(_a)):
    if _a[_i] % 2 == 0:
        if _i != _st:
            if _a[_st] == 3:
                THREE_MOVES += 1
            _a[_i], _a[_st] = _a[_st], _a[_i]
        _st += 1
assert THREE_MOVES == 3
lw.steps[-1]["text"] += f" Done: {store} evens in front, after {sw} swaps, where the two-ended version needs {ends_swaps(DEMO)}. The 3 that started at the front was moved {THREE_MOVES} times before it settled."
L_LEGEND = {"found": "even: the front part", "mark": "odd: scanned, behind the front part"}

# Trace walk: the two-ended template.
tw = Steps(f"`evens_first({DEMO})`. `lo` stops at an odd value, `hi` stops at an even one, and then they swap.")
a, lo, hi, sw = list(DEMO), 0, len(DEMO) - 1, 0


def t_state(active=()):
    st = {**{k: "found" for k in range(lo)}, **{k: "mark" for k in range(hi + 1, len(a))}}
    for k in active:
        st[k] = "active"
    return st


tw.step("Nothing is settled yet: the even part (left of `lo`) and the odd part (right of `hi`) are both empty.",
        Row(list(a), st=t_state(), ptr={"lo": lo, "hi": hi}, slots=True, label="nums"), M({"swaps": 0}))
while True:
    start_lo, start_hi = lo, hi
    while lo <= hi and a[lo] % 2 == 0:
        lo += 1
    while lo <= hi and a[hi] % 2 != 0:
        hi -= 1
    moved = []
    if lo != start_lo:
        moved.append(f"`lo` walks past {', '.join(map(str, a[start_lo:lo]))} (even, already in place)")
    if hi != start_hi:
        moved.append(f"`hi` walks past {', '.join(map(str, a[hi + 1:start_hi + 1][::-1]))} (odd, already in place)")
    if lo > hi:
        tw.step((" and ".join(moved).capitalize() + ". " if moved else "") + f"Now `lo` has passed `hi`: everything is settled. {lo} evens in front.",
                Row(list(a), st=t_state(), ptr={"lo": lo if lo < len(a) else None, "hi": hi if hi >= 0 else None}, slots=True, label="nums"), M({"swaps": sw}), result=lo)
        break
    tw.step((" and ".join(moved).capitalize() + ". " if moved else "") + f"`lo` stops at {a[lo]} (odd, on the wrong side) and `hi` at {a[hi]} (even, on the wrong side).",
            Row(list(a), st=t_state((lo, hi)), ptr={"lo": lo, "hi": hi}, slots=True, label="nums"), M({"swaps": sw}))
    a[lo], a[hi] = a[hi], a[lo]
    sw += 1
    tw.step(f"Swap them. Both are now on the right side, so both pointers move in.",
            Row(list(a), st={**t_state(), lo: "found", hi: "mark"}, ptr={"lo": lo + 1, "hi": hi - 1}, slots=True, label="nums"), M({"swaps": sw}))
    lo, hi = lo + 1, hi - 1
assert a == AFTER and sw == ends_swaps(DEMO)
T_LEGEND = {"found": "settled: even", "mark": "settled: odd", "active": "both on the wrong side: swap them"}

# Variation walk: three-way partition.
TD, TP = [4, 9, 4, 1, 7, 4, 2, 8], 4
vw = Steps(f"`three_way({TD}, {TP})`: smaller than {TP} to the left, equal in the middle, bigger to the right.")
a, lt, i, gt = list(TD), 0, 0, len(TD) - 1


def v_state():
    st = {**{k: "found" for k in range(lt)}, **{k: "answer" for k in range(lt, i)}, **{k: "mark" for k in range(gt + 1, len(a))}}
    if i <= gt:
        st[i] = "active"
    return st


vw.step(f"Before `lt` is smaller than {TP}, from `lt` to `i` is equal, after `gt` is bigger. Between `i` and `gt` hasn't been looked at.",
        Row(list(a), st=v_state(), ptr={"lt": lt, "i": i, "gt": gt}, slots=True, label="nums"), M({"unexamined": gt - i + 1}))
while i <= gt:
    x = a[i]
    if x < TP:
        a[lt], a[i] = a[i], a[lt]
        lt, i = lt + 1, i + 1
        msg = f"{x} < {TP}: swap it to the end of the smaller part. The value swapped back is equal to {TP} (or is {x} itself), so `i` moves on too."
    elif x > TP:
        a[i], a[gt] = a[gt], a[i]
        gt -= 1
        msg = f"{x} > {TP}: swap it into the bigger part at `gt`, and `gt` moves left. `i` stays: the {a[i]} that came back hasn't been looked at."
    else:
        i += 1
        msg = f"{x} = {TP}: it's already in the middle part. `i` moves on."
    vw.step(msg, Row(list(a), st=v_state(), ptr={"lt": lt, "i": i if i < len(a) else None, "gt": gt if gt >= 0 else None}, slots=True, label="nums"), M({"unexamined": max(0, gt - i + 1)}))
vw.steps[-1]["text"] += f" Nothing is left unexamined. Indices {lt} to {gt} hold every {TP}."
assert (lt, gt) == three_way(list(TD), TP)
V_LEGEND = {"found": f"smaller than {TP}", "answer": f"equal to {TP}", "mark": f"bigger than {TP}", "active": "being looked at"}

# Example: stability, shown on labelled values.
REC = [("a", 5), ("b", 2), ("c", 7), ("d", 4), ("e", 9), ("f", 6)]
rec = list(REC)
lo_, hi_ = 0, len(rec) - 1
while True:
    while lo_ <= hi_ and rec[lo_][1] % 2 == 0:
        lo_ += 1
    while lo_ <= hi_ and rec[hi_][1] % 2 != 0:
        hi_ -= 1
    if lo_ > hi_:
        break
    rec[lo_], rec[hi_] = rec[hi_], rec[lo_]
    lo_, hi_ = lo_ + 1, hi_ - 1
STABLE = [r for r in REC if r[1] % 2 == 0] + [r for r in REC if r[1] % 2]


def rstr(rs):
    return ", ".join(f"{n}{v}" for n, v in rs)


lesson(
    "two-pointers",
    "partition",
    """
    Split an array into groups in place (evens before odds, small before big, or three colours in order) by keeping
    each group's boundary in a pointer. Values on the wrong side get swapped across, and every element is looked at
    about once.
    """,
    [
        ("idea", "The idea", [
            f"""
            A coach lines the team up and wants everyone with an even shirt number on the left and odd on the right.
            The order inside each group doesn't matter. The coach walks in from the left end and an assistant from the
            right. The coach walks past even numbers until reaching someone odd: that person is on the wrong side. The
            assistant walks past odd numbers until reaching someone even: also on the wrong side. Those two swap places,
            and both carry on. When the coach and the assistant meet, everyone is on the right side.

            Nobody is moved twice, and anyone already on the correct side is walked past without being touched. On
            `{DEMO}` that's {ends_swaps(DEMO)} swaps.
            """,
            fig(Row(DEMO, st={k: ("found" if x % 2 == 0 else "mark") for k, x in enumerate(DEMO)}, slots=True, label="before"),
                Row(AFTER, st={k: ("found" if x % 2 == 0 else "mark") for k, x in enumerate(AFTER)}, slots=True, label="after"),
                caption=f"Evens and odds, each group in one block. The boundary sits at index {N_EVEN}, which is how many evens there are."),
            key("""
            Keep the settled part of each group behind its own pointer. Move a pointer past values that already belong
            on its side; when both pointers are stuck on values that belong on the other side, swap them. O(n) time,
            O(1) space, but the order inside each group isn't kept.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The array has to be split into two or three groups by a yes/no test or by comparing with a value, "in
            place", "in one pass", "with O(1) extra space". The order inside a group usually doesn't matter.
            """,
            table(
                ["The problem says…", "the groups"],
                ["evens before odds, negatives before positives", "two groups by a test"],
                ["sort an array of 0s, 1s and 2s", "three groups, one per value"],
                ["smaller than `p`, equal, bigger", "three groups around a pivot value"],
                ["move every `x` to the end, order doesn't matter", "two groups: not `x`, then `x`"],
                ["the k-th smallest value, quickly", "partition, then keep one side (*Quickselect*)"],
            ),
            """
            Not a fit:

            - The order inside each group must be kept (a *stable* partition). The swaps here jump values over each
              other. A stable split needs an extra array (or the read/write pass, if one group can simply be dropped or
              filled in afterwards).
            - More than three groups. Run the partition more than once, or count values and rebuild (*Counting and
              bucket sort*) when the values are small.
            - You only need the count of each group. Counting is simpler than moving anything.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Regions, and what each pointer guarantees

            A partition keeps the array split into regions, each with a meaning that never stops being true. For the
            two-ended version:

            > Everything before `lo` is even. Everything after `hi` is odd. Between them is unexamined.

            The inner loops grow the two settled regions for free. When both stop, `a[lo]` is odd and `a[hi]` is even,
            each sitting on the other's side, so one swap fixes both and both regions grow by one. The unexamined middle
            shrinks every step, and when it's empty (`lo > hi`) the array is split, with `lo` equal to the number of
            evens.

            ### One pointer from the left

            The other common version walks both pointers from the left. `store` marks the end of the even region, and
            `i` scans. Each even value found is swapped back to `store`.
            """,
            walk(lw, legend=L_LEGEND),
            f"""
            It's simpler to get right, and it's what quick sort usually uses, but it does more swaps: every even value
            after the first odd one gets swapped, even if lots of them are already near the front. The two-ended version
            only swaps values that are on the wrong side:
            """,
            table(["input", "one pointer from the left", "two from the ends"], *SWAP_ROWS),
            """
            ### Three groups

            The three-way version (often called the Dutch national flag partition, after the flag's three stripes)
            keeps four regions with three pointers: smaller before `lt`, equal from `lt` to `i`, unexamined from `i`
            to `gt`, bigger after `gt`. Each step looks at `a[i]` and either grows the smaller region (swap with `lt`),
            grows the bigger region (swap with `gt`), or grows the equal region (just move `i`). The only subtle rule:
            after swapping with `gt`, `i` stays put, because the value that came back is unexamined.

            ### Why it isn't stable

            A swap moves a value from one end to the other, jumping over everything between. Two even values can swap
            their relative order because one of them got carried across. If the original order inside a group matters,
            a swap-based partition can't promise it.
            """,
        ]),
        ("template", "The template", [
            """
            Move every even value in front of every odd value, in place. Return how many evens there are, which is
            also the index where the odd part starts.
            """,
            code(
                "Evens before odds, from both ends",
                EVENS,
                [
                    ("ends", "One pointer at each end. Everything before `lo` will be even, everything after `hi` odd."),
                    ("loop", "Each round settles at least one value."),
                    ("left", "Walk `lo` past values that are already even. They're in the right place."),
                    ("right", "Walk `hi` past values that are already odd. `!= 0` rather than `== 1`, because a negative odd "
                              "number gives `-1` in Java, C and C++.",
                     {"python": "Python's `%` is never negative here, but `!= 0` reads the same in every language."}),
                    ("done", "If the pointers have crossed, every value is settled. `lo` is the first odd position, which "
                             "is also the number of evens."),
                    ("swap", "`lo` is on an odd value and `hi` on an even one, each on the wrong side. Swap, and both "
                             "pointers move in.",
                     {"cpp": "`swap(nums[lo++], nums[hi--])` swaps first, then moves both."}),
                ],
                EVENS_RUN,
                "evens_first([3, 8, 5, 2, 7, 6, 4, 1]); ([2, 4, 6]); ([1, 3]); ([-3, -2, 0, 5])",
            ),
            """
            Each output line is the array after the call, then the boundary. `[2, 4, 6]` is all even, so the boundary
            is 3, the length, and nothing was swapped.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "The same array as the one-pointer walkthrough, so you can compare the swaps:",
            walk(tw, legend=T_LEGEND),
            """
            On paper, shade the settled part of each end as it grows. If you ever swap a value that was already on the
            correct side, one of the inner loops is missing.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Seeing the order change

            Label each value with a letter so you can follow it: `{rstr(REC)}`. Evens first, from both ends, gives
            `{rstr(rec)}`. A stable split would give `{rstr(STABLE)}`. The groups are right in both, but the swaps
            reordered values inside the groups. If a question asks for the original order inside each group, this
            pattern is the wrong tool; use the read/write pass, or a second array.

            ### Partition as a building block

            Quick sort partitions around a pivot and then sorts each side. Quickselect partitions and keeps only the
            side that holds the answer. Both need the pivot's final index, which is exactly the boundary a partition
            returns. A three-way partition helps them both when values repeat a lot.

            ### Any yes/no test

            Replace "is even" with any test: negative, below a threshold, a vowel, a bad record. The two-ended loop
            doesn't change, as long as each value can be judged on its own.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Three groups around a value

            Smaller than the pivot to the left, equal in the middle, bigger to the right, in one pass. The function
            returns the equal block's first and last index; if the pivot doesn't appear, the block is empty and `lt`
            is one more than `gt`.
            """,
            walk(vw, legend=V_LEGEND),
            code(
                "Three-way partition around a pivot value",
                THREE,
                [
                    ("marks", "`[0, lt)` smaller, `[lt, i)` equal, `[i, gt]` unexamined, `(gt, end]` bigger. At the start "
                              "everything is unexamined."),
                    ("scan", "Until the unexamined part is empty."),
                    ("less", "A smaller value swaps to the end of the smaller part. What comes back from `lt` is an equal "
                             "value (or the same element), so `i` can move on too."),
                    ("more", "A bigger value swaps into the bigger part. What comes back from `gt` is unexamined, so `i` "
                             "stays."),
                    ("same", "An equal value is already in the middle."),
                    ("ret", "The first and last index of the equal block.",
                     {"java": "Two values come back in a small array.",
                      "cpp": "Two values come back as a `pair`.",
                      "c": "C writes the two indices through pointers."}),
                ],
                THREE_RUN,
                "three_way([4, 9, 4, 1, 7, 4, 2, 8], 4); ([5, 5, 5], 5); ([1, 2, 3], 0)",
            ),
            """
            With pivot 0 on `[1, 2, 3]`, everything is bigger: the equal block is "from 0 to -1", which is empty.

            ### More groups

            For four or more groups, partition once to split off the smallest group, then partition the rest, and so on.
            Or, when there are `k` group labels, split by the middle label and recurse on each half: about `log k`
            levels of O(n) work.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Every step either moves a pointer inward or swaps and moves two, so the two-ended version is O(n) with at
            most `n / 2` swaps. The one-pointer version is O(n) with up to `n` swaps. The three-way version is O(n)
            with at most `n` swaps. All of them use O(1) extra space.
            """,
            table(
                ["Approach", "Time", "Extra space", "Keeps order"],
                ["Sort the whole array", "O(n log n)", "O(1) to O(n)", "depends on the sort"],
                ["Two passes into a new array", "O(n)", "O(n)", "yes"],
                ["One pointer from the left", "O(n), up to n swaps", "O(1)", "no"],
                ["Two from the ends", "O(n), at most n / 2 swaps", "O(1)", "no"],
                ["Three-way", "O(n)", "O(1)", "no"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            Tuple assignment swaps in one line. `x % 2` is 0 or 1 even for negatives. A one-line, non-in-place
            version is `[x for x in a if x % 2 == 0] + [x for x in a if x % 2]`, which is stable and O(n) extra.

            ### Java

            No built-in swap for arrays; use a temporary. `-3 % 2` is `-1`, so test for odd with `!= 0`.

            ### C++

            `std::partition(first, last, pred)` does this and returns the boundary iterator; `std::stable_partition`
            keeps order (with extra memory). `std::nth_element` partitions around the k-th value.

            ### C

            A temporary for swaps. `%` follows the sign of the left side, so negative odd values give `-1`.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Testing odd with `% 2 == 1`, which misses negative odd numbers in Java, C and C++.
            - Forgetting `lo <= hi` in the inner loops, so a pointer runs off the end on an all-even or all-odd array.
            - In the three-way version, moving `i` after swapping with `gt`. The value that came back hasn't been checked.
            - Expecting the order inside each group to be kept.
            - Returning the wrong boundary: after the loop, `lo` is the count of the first group.
            - Empty arrays: `hi` starts at -1 and nothing should happen.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("What does the two-ended loop guarantee about the parts before `lo` and after `hi`?",
                 "Everything before `lo` belongs to the first group (even), everything after `hi` to the second (odd). Only the middle is unexamined."),
                ("Why does the two-ended version need fewer swaps than the one-pointer version?",
                 "It only swaps pairs that are both on the wrong side. The one-pointer version swaps every first-group value it finds after the first second-group value, even ones that end up close to where they started."),
                ("In the three-way partition, why does `i` move after swapping with `lt` but not after swapping with `gt`?",
                 "Everything between `lt` and `i` is equal to the pivot, so the value that comes back from `lt` is known. The value that comes back from `gt` comes from the unexamined part."),
                ("Partition [b2, a4, c1] (letters only to track them) evens first from both ends. Are a4 and b2 still in their original order?",
                 "Yes here: `lo` walks past b2 and a4 (both even), `hi` walks past c1, and the pointers cross with no swap. On other inputs a swap can carry an even value across another and change their order."),
                ("Three-way partition of [5, 5, 5] around 5: what are lt and gt?",
                 "0 and 2: everything is equal, so the equal block is the whole array."),
            ),
        ]),
    ],
)
