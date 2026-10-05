"""Lesson: Sort then scan (Arrays & Hashing, pattern 8)."""
from lesson import Bars, Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

DISTINCT = {
    "python": """
        def count_distinct(nums):
            nums = sorted(nums)                                 #@sort
            count = 0                                           #@count
            for i in range(len(nums)):                          #@scan
                if i == 0 or nums[i] != nums[i - 1]:            #@new
                    count += 1                                  #@new
            return count                                        #@ret
    """,
    "java": """
        static int countDistinct(int[] nums) {
            int[] a = nums.clone();                             //@sort
            Arrays.sort(a);                                     //@sort
            int count = 0;                                      //@count
            for (int i = 0; i < a.length; i++) {                //@scan
                if (i == 0 || a[i] != a[i - 1]) count++;        //@new
            }
            return count;                                       //@ret
        }
    """,
    "cpp": """
        int countDistinct(vector<int> nums) {
            sort(nums.begin(), nums.end());                     //@sort
            int count = 0;                                      //@count
            for (size_t i = 0; i < nums.size(); i++) {          //@scan
                if (i == 0 || nums[i] != nums[i - 1]) count++;  //@new
            }
            return count;                                       //@ret
        }
    """,
    "c": """
        static int cmpInt(const void* a, const void* b) {
            int x = *(const int*)a, y = *(const int*)b;         //@cmp
            return (x > y) - (x < y);                           //@cmp
        }

        int countDistinct(const int* nums, int n) {
            int* a = malloc(n * sizeof(int));                   //@sort
            memcpy(a, nums, n * sizeof(int));                   //@sort
            qsort(a, n, sizeof(int), cmpInt);                   //@sort
            int count = 0;                                      //@count
            for (int i = 0; i < n; i++) {                       //@scan
                if (i == 0 || a[i] != a[i - 1]) count++;        //@new
            }
            free(a);                                            //@ret
            return count;                                       //@ret
        }
    """,
}
DISTINCT_RUN = {
    "python": """
        print(count_distinct([4, 9, 4, 1, 9, 9, 7]))
        print(count_distinct([-3, -3, -3]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(countDistinct(new int[] {4, 9, 4, 1, 9, 9, 7}));
            System.out.println(countDistinct(new int[] {-3, -3, -3}));
        }
    """,
    "cpp": """
        int main() {
            cout << countDistinct({4, 9, 4, 1, 9, 9, 7}) << "\\n" << countDistinct({-3, -3, -3}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {4, 9, 4, 1, 9, 9, 7}, b[] = {-3, -3, -3};
            printf("%d\\n%d\\n", countDistinct(a, 7), countDistinct(b, 3));
            return 0;
        }
    """,
}

COMMON = {
    "python": """
        def common_count(a, b):
            a, b = sorted(a), sorted(b)                         #@sort
            i = j = common = 0                                  #@start
            while i < len(a) and j < len(b):                    #@loop
                if a[i] == b[j]:                                #@match
                    common += 1                                 #@match
                    i += 1                                      #@match
                    j += 1                                      #@match
                elif a[i] < b[j]:                               #@small
                    i += 1                                      #@small
                else:                                           #@big
                    j += 1                                      #@big
            return common                                       #@ret
    """,
    "java": """
        static int commonCount(int[] a0, int[] b0) {
            int[] a = a0.clone(), b = b0.clone();               //@sort
            Arrays.sort(a);                                     //@sort
            Arrays.sort(b);                                     //@sort
            int i = 0, j = 0, common = 0;                       //@start
            while (i < a.length && j < b.length) {              //@loop
                if (a[i] == b[j]) {                             //@match
                    common++;                                   //@match
                    i++;                                        //@match
                    j++;                                        //@match
                } else if (a[i] < b[j]) {                       //@small
                    i++;                                        //@small
                } else {                                        //@big
                    j++;                                        //@big
                }
            }
            return common;                                      //@ret
        }
    """,
    "cpp": """
        int commonCount(vector<int> a, vector<int> b) {
            sort(a.begin(), a.end());                           //@sort
            sort(b.begin(), b.end());                           //@sort
            size_t i = 0, j = 0;                                //@start
            int common = 0;                                     //@start
            while (i < a.size() && j < b.size()) {              //@loop
                if (a[i] == b[j]) {                             //@match
                    common++;                                   //@match
                    i++;                                        //@match
                    j++;                                        //@match
                } else if (a[i] < b[j]) {                       //@small
                    i++;                                        //@small
                } else {                                        //@big
                    j++;                                        //@big
                }
            }
            return common;                                      //@ret
        }
    """,
    "c": """
        static int cmpInt(const void* a, const void* b) {
            int x = *(const int*)a, y = *(const int*)b;         //@cmp
            return (x > y) - (x < y);                           //@cmp
        }

        int commonCount(const int* a0, int na, const int* b0, int nb) {
            int* a = malloc(na * sizeof(int));                  //@sort
            int* b = malloc(nb * sizeof(int));                  //@sort
            memcpy(a, a0, na * sizeof(int));                    //@sort
            memcpy(b, b0, nb * sizeof(int));                    //@sort
            qsort(a, na, sizeof(int), cmpInt);                  //@sort
            qsort(b, nb, sizeof(int), cmpInt);                  //@sort
            int i = 0, j = 0, common = 0;                       //@start
            while (i < na && j < nb) {                          //@loop
                if (a[i] == b[j]) {                             //@match
                    common++;                                   //@match
                    i++;                                        //@match
                    j++;                                        //@match
                } else if (a[i] < b[j]) {                       //@small
                    i++;                                        //@small
                } else {                                        //@big
                    j++;                                        //@big
                }
            }
            free(a); free(b);                                   //@ret
            return common;                                      //@ret
        }
    """,
}
COMMON_RUN = {
    "python": """
        print(common_count([5, 1, 3, 3, 8], [3, 9, 1, 3, 3]))
        print(common_count([2, 4], [6, 8]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(commonCount(new int[] {5, 1, 3, 3, 8}, new int[] {3, 9, 1, 3, 3}));
            System.out.println(commonCount(new int[] {2, 4}, new int[] {6, 8}));
        }
    """,
    "cpp": """
        int main() {
            cout << commonCount({5, 1, 3, 3, 8}, {3, 9, 1, 3, 3}) << "\\n" << commonCount({2, 4}, {6, 8}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {5, 1, 3, 3, 8}, b[] = {3, 9, 1, 3, 3}, c[] = {2, 4}, d[] = {6, 8};
            printf("%d\\n%d\\n", commonCount(a, 5, b, 5), commonCount(c, 2, d, 2));
            return 0;
        }
    """,
}

UNREACH = {
    "python": """
        def smallest_unpayable(coins):
            coins = sorted(coins)                               #@sort
            reach = 0                                           #@reach
            for c in coins:                                     #@loop
                if c > reach + 1:                               #@gap
                    break                                       #@gap
                reach += c                                      #@grow
            return reach + 1                                    #@ret
    """,
    "java": """
        static long smallestUnpayable(int[] coins0) {
            int[] coins = coins0.clone();                       //@sort
            Arrays.sort(coins);                                 //@sort
            long reach = 0;                                     //@reach
            for (int c : coins) {                               //@loop
                if (c > reach + 1) break;                       //@gap
                reach += c;                                     //@grow
            }
            return reach + 1;                                   //@ret
        }
    """,
    "cpp": """
        long long smallestUnpayable(vector<int> coins) {
            sort(coins.begin(), coins.end());                   //@sort
            long long reach = 0;                                //@reach
            for (int c : coins) {                               //@loop
                if (c > reach + 1) break;                       //@gap
                reach += c;                                     //@grow
            }
            return reach + 1;                                   //@ret
        }
    """,
    "c": """
        static int cmpInt(const void* a, const void* b) {
            int x = *(const int*)a, y = *(const int*)b;         //@cmp
            return (x > y) - (x < y);                           //@cmp
        }

        long long smallestUnpayable(const int* coins0, int n) {
            int* coins = malloc(n * sizeof(int));               //@sort
            memcpy(coins, coins0, n * sizeof(int));             //@sort
            qsort(coins, n, sizeof(int), cmpInt);               //@sort
            long long reach = 0;                                //@reach
            for (int i = 0; i < n; i++) {                       //@loop
                if (coins[i] > reach + 1) break;                //@gap
                reach += coins[i];                              //@grow
            }
            free(coins);                                        //@ret
            return reach + 1;                                   //@ret
        }
    """,
}
UNREACH_RUN = {
    "python": """
        print(smallest_unpayable([1, 5, 1, 2, 12]))
        print(smallest_unpayable([1, 1, 1, 1]))
        print(smallest_unpayable([2, 3]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(smallestUnpayable(new int[] {1, 5, 1, 2, 12}));
            System.out.println(smallestUnpayable(new int[] {1, 1, 1, 1}));
            System.out.println(smallestUnpayable(new int[] {2, 3}));
        }
    """,
    "cpp": """
        int main() {
            cout << smallestUnpayable({1, 5, 1, 2, 12}) << "\\n" << smallestUnpayable({1, 1, 1, 1}) << "\\n" << smallestUnpayable({2, 3}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {1, 5, 1, 2, 12}, b[] = {1, 1, 1, 1}, c[] = {2, 3};
            printf("%lld\\n%lld\\n%lld\\n", smallestUnpayable(a, 5), smallestUnpayable(b, 4), smallestUnpayable(c, 2));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

count_distinct = py(DISTINCT["python"], "count_distinct")
common_count = py(COMMON["python"], "common_count")
smallest_unpayable = py(UNREACH["python"], "smallest_unpayable")

DEMO = [4, 9, 4, 1, 9, 9, 7]
SD = sorted(DEMO)
DIST = count_distinct(DEMO)
assert DIST == len(set(DEMO))
starts = [i for i in range(len(SD)) if i == 0 or SD[i] != SD[i - 1]]

dw = Steps(f"`count_distinct({DEMO})`: sort, then count where a new value begins.")
dw.step(f"Sorted: {SD}. Equal values are now next to each other.", Row(SD, slots=True), M({"distinct": 0}))
cnt = 0
for i in range(len(SD)):
    new = i == 0 or SD[i] != SD[i - 1]
    if new:
        cnt += 1
    why = "the first element always starts a run" if i == 0 else (f"{SD[i]} differs from the {SD[i - 1]} before it: a new value" if new else f"{SD[i]} is the same as the one before it: same run")
    dw.step(f"Index {i}: {why}.", Row(SD, st={**{s: "found" for s in starts if s < i}, i: "answer" if new else "active"}, ptr={"i": i}, slots=True), M({"distinct": cnt}))

CA, CB = [5, 1, 3, 3, 8], [3, 9, 1, 3, 3]
SA, SB = sorted(CA), sorted(CB)
COM = common_count(CA, CB)
cw = Steps(f"Counting values the two lists share (with repeats): sort both, then walk them together.")
i = j = c = 0
cw.step(f"a = {SA}, b = {SB}. Both pointers start at the front.", Row(SA, ptr={"i": 0}, label="a"), Row(SB, ptr={"j": 0}, label="b"), M({"common": 0}))
used_a, used_b = set(), set()
while i < len(SA) and j < len(SB):
    if SA[i] == SB[j]:
        c += 1
        used_a.add(i)
        used_b.add(j)
        msg = f"a[{i}] = b[{j}] = {SA[i]}: a match. Count it and move both."
        st_a, st_b = {i: "answer"}, {j: "answer"}
        i += 1
        j += 1
    elif SA[i] < SB[j]:
        msg = f"a[{i}] = {SA[i]} is smaller than b[{j}] = {SB[j]}. Nothing later in b can be that small, so {SA[i]} has no partner. Move i."
        st_a, st_b = {i: "dim"}, {j: "active"}
        i += 1
    else:
        msg = f"b[{j}] = {SB[j]} is smaller than a[{i}] = {SA[i]}, so it has no partner in a. Move j."
        st_a, st_b = {i: "active"}, {j: "dim"}
        j += 1
    cw.step(msg, Row(SA, st={**{k: "found" for k in used_a}, **st_a}, ptr={"i": min(i, len(SA) - 1)}, label="a"),
            Row(SB, st={**{k: "found" for k in used_b}, **st_b}, ptr={"j": min(j, len(SB) - 1)}, label="b"), M({"common": c}))
cw.step(f"One list ran out. Shared values (counting repeats): {c}.", Row(SA, st={k: "found" for k in used_a}, label="a"), Row(SB, st={k: "found" for k in used_b}, label="b"), result=c)
assert c == COM

COINS = [1, 5, 1, 2, 12]
SC = sorted(COINS)
UN = smallest_unpayable(COINS)
assert UN == 10


def brute_unpayable(coins):
    sums = {0}
    for x in coins:
        sums |= {s + x for s in sums}
    k = 1
    while k in sums:
        k += 1
    return k


assert brute_unpayable(COINS) == UN and brute_unpayable([2, 3]) == 1 and brute_unpayable([1, 1, 1, 1]) == 5
uw = Steps(f"`smallest_unpayable({COINS})`. `reach` means every amount from 0 to reach can be paid exactly.")
reach = 0
uw.step(f"Sorted coins: {SC}. With no coins, only 0 can be paid: reach = 0.", Row(SC, slots=True), M({"payable": "0 to 0"}))
for k, x in enumerate(SC):
    if x > reach + 1:
        uw.step(f"The next coin is {x}, but we can't pay {reach + 1} yet, and every coin from here on is at least {x}, so nothing can ever make {reach + 1}. Answer: {reach + 1}.",
                Row(SC, st={**{t: "found" for t in range(k)}, k: "dim", **{t: "dim" for t in range(k + 1, len(SC))}}, ptr={"coin": k}, slots=True), M({"payable": f"0 to {reach}"}), result=reach + 1)
        break
    old = reach
    reach += x
    uw.step(f"Coin {x} is at most {old} + 1. Adding it to each amount 0..{old} gives {x}..{old + x}, which joins up with 0..{old}. Now 0 to {reach} are all payable.",
            Row(SC, st={**{t: "found" for t in range(k)}, k: "new"}, ptr={"coin": k}, slots=True), M({"payable": f"0 to {reach}"}))

# Example: ranks (coordinate compression).
RK = [40, 10, 70, 10, 25]
order = sorted(set(RK))
RANKS = [order.index(x) for x in RK]

# Example: pairing to keep the biggest pair sum small.
PEOPLE = [8, 3, 6, 1, 5, 9]
PS = sorted(PEOPLE)
PAIRS = [(PS[k], PS[-1 - k]) for k in range(len(PS) // 2)]
WORST = max(a + b for a, b in PAIRS)


def best_pairing(xs):
    best = None
    xs = list(xs)
    if not xs:
        return 0
    a = xs[0]
    for t in range(1, len(xs)):
        rest = xs[1:t] + xs[t + 1:]
        cand = max(a + xs[t], best_pairing(rest))
        best = cand if best is None else min(best, cand)
    return best


assert best_pairing(PEOPLE) == WORST
NAIVE_PAIRS = [(PEOPLE[k], PEOPLE[k + 1]) for k in range(0, len(PEOPLE), 2)]

N = 10**5
lesson(
    "arrays-hashing",
    "sort-then-scan",
    """
    A lot of questions get easy once the data is in order. Equal values end up side by side, close values become
    neighbours, and "the smallest that works" can be found by walking forward. Sort first, then one linear pass usually
    finishes the job.
    """,
    [
        ("idea", "The idea", [
            """
            Tip a jar of coins onto a table and someone asks: how many different kinds of coin are there? Are there two
            the same? What's the closest pair in value? With a messy pile, each question means hunting around. Now line
            the coins up from smallest to largest. Suddenly every question is answered by looking along the line once:
            same coins sit together, and the coins closest in value are always next to each other.

            That's sort then scan. Sorting costs O(n log n), and it buys you an order that turns many "compare everything
            with everything" questions into "compare each element with the one next to it".
            """,
            fig(Bars(DEMO, label="as given"), Bars(SD, st={s: "found" for s in starts}, label="sorted: each new value starts a run"),
                caption=f"After sorting, the {DIST} different values are easy to see: each one starts where the bar height changes."),
            key("""
            Sort first, so that what you're looking for ends up next to each other: equal values in runs, close values as
            neighbours, small values first. Then a single pass, often comparing `a[i]` with `a[i - 1]`, gives the answer.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            Good signs:

            - The answer doesn't depend on the original order (you could shuffle the input and the answer stays the same).
            - The question is about duplicates, closest values, gaps, runs of consecutive values, or the "k-th smallest".
            - You need to match things up between two lists, or pair elements so that some total is as good as possible.
            - A greedy choice ("always use the smallest coin first") only works if you go through items in a fixed order.
            - O(1) extra space is wanted and you're allowed to reorder the input. Sorting in place uses little memory,
              while a hash set needs O(n).

            When to think twice:

            - Original positions matter (return indices, or "first occurrence"). Sorting loses them. Sort `(value,
              index)` pairs instead, or use a hash map.
            - O(n) is required. Sorting is O(n log n). A hash map or counting may be the intended solution. (Counting
              sort is O(n + range) if values are small.)
            - The data keeps changing. Re-sorting after every update is slow. A heap or a balanced tree keeps things
              in order as you go.
            """,
        ]),
        ("theory", "Why sorting helps", [
            """
            ### Equal values become runs

            After sorting, all copies of a value are next to each other. So "is this a new value?" is just
            `a[i] != a[i - 1]`, and duplicates are `a[i] == a[i - 1]`. Counting runs gives the number of distinct values;
            the length of a run gives a count.

            ### The closest pair is always neighbouring

            In a sorted array, any two elements `a[i] ≤ a[j]` with something in between, `a[i] ≤ a[k] ≤ a[j]`, are at least
            as far apart as `a[i]` and `a[k]`. So the smallest difference between any two elements is always between two
            neighbours. You only need to check `n - 1` pairs instead of all `n(n - 1)/2`.

            ### Walking two sorted lists together

            With two sorted lists, two pointers can move forward together, like merging in merge sort. If `a[i] < b[j]`,
            then `a[i]` is smaller than everything left in `b`, so it can't match anything there, and you can safely skip
            it. Each step moves at least one pointer, so the walk is O(n + m).

            ### Greedy choices need an order

            Many "pick the best" problems have a greedy solution that only works in a specific order: smallest first,
            earliest deadline first, biggest first. Sorting is what puts the items in that order. The proof that the
            greedy choice is right usually goes like this: suppose a better answer did something different at the first
            point where it disagrees with greedy; show you can swap it to the greedy choice without making it worse. This
            is called an **exchange argument**. You'll see one in *More examples*.

            ### What sorting costs

            Comparison sorts (merge sort, quicksort, the built-in sorts) take O(n log n) time. That's a hard limit: no
            comparison sort can do better in general. The built-in sorts are well tuned, so `sort` is almost always the
            right call.

            - Python's `sorted` and `list.sort` are stable (equal elements keep their order) and use O(n) extra memory.
            - Java's `Arrays.sort` on `int[]` is a quicksort variant (not stable, but for plain numbers that doesn't
              matter); on objects it's a stable merge sort.
            - C++'s `std::sort` isn't stable; `std::stable_sort` is.
            - C's `qsort` takes a comparison function.

            If values are small integers (say 0 to 1000), counting sort is O(n + range) and beats the general sort.
            """,
        ]),
        ("template", "The template", [
            """
            Count how many different values an array has, using sorting rather than a hash set. It shows the most common
            shape of this pattern: sort, then compare each element with the one before it.
            """,
            code(
                "Count distinct values",
                DISTINCT,
                [
                    ("sort", "Sort a copy, so the caller's array keeps its order.",
                     {"python": "`sorted` returns a new list; `nums.sort()` would sort in place.",
                      "java": "`clone()` makes a copy; `Arrays.sort` sorts it in place.",
                      "cpp": "`nums` was passed by value, so it's already a copy.",
                      "c": "Copy with `memcpy`, then sort the copy with `qsort`."}),
                    ("cmp", "The comparison `qsort` uses: negative, zero or positive. `(x > y) - (x < y)` can't overflow, "
                            "unlike `x - y`."),
                    ("count", "No values counted yet."),
                    ("scan", "One pass over the sorted values."),
                    ("new", "A value starts a new run if it's the first element or differs from the one before it. Each "
                            "run is one distinct value."),
                    ("ret", "The number of runs.", {"c": "Free the copy first."}),
                ],
                DISTINCT_RUN,
                "count_distinct([4, 9, 4, 1, 9, 9, 7]); count_distinct([-3, -3, -3])",
            ),
        ]),
        ("trace", "Trace it by hand", [
            walk(dw),
            f"""
            Runs start at indices {', '.join(map(str, starts))}, so there are {DIST} distinct values. A hash set would give
            the same answer in O(n) on average. Sorting takes O(n log n) but needs no hashing and, if you sort in place,
            hardly any memory.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Ranking values (coordinate compression)

            Replace every value with its rank among the distinct values: the smallest becomes 0, the next 1, and so on.
            For `{RK}`, the distinct values sorted are `{order}`, so the ranks are `{RANKS}`. This shrinks huge numbers
            down to 0..d-1 while keeping their order, which lets you use them as array indices later (you'll need this
            for Fenwick trees and segment trees).

            ### Pairing people to keep the biggest pair small

            Six people with weights `{PEOPLE}` ride a two-seat ride in pairs, and you want the heaviest pair to be as
            light as possible. Pairing them in the order given would make pairs `{NAIVE_PAIRS}`, the heaviest weighing
            {max(a + b for a, b in NAIVE_PAIRS)}. Sort them, then pair the lightest with the heaviest, the second lightest
            with the second heaviest, and so on:
            """,
            table(["pair", "total"], *[(f"{a} + {b}", str(a + b)) for a, b in PAIRS]),
            f"""
            The heaviest pair is now {WORST}, and checking every possible pairing confirms nothing does better.

            Why does it work? Take the heaviest person. Whoever they ride with, that pair is at least heaviest + partner,
            so the best possible partner is the lightest person. Any pairing that does something else can swap the
            heaviest person's partner for the lightest without making the worst pair heavier. That's the exchange argument
            from *Why sorting helps*.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Walking two sorted lists together

            How many values do two lists share, counting repeats? (A value that appears twice in both counts twice.) Sort
            both, then move two pointers forward, always advancing the one pointing at the smaller value.
            """,
            walk(cw),
            code(
                "Count common values (with repeats)",
                COMMON,
                [
                    ("sort", "Sort copies of both lists."),
                    ("cmp", "The same overflow-safe comparison for `qsort`."),
                    ("start", "Both pointers at the front, no matches yet."),
                    ("loop", "Stop when either list runs out: nothing left can match."),
                    ("match", "Equal values: one shared value. Use up one copy from each list by moving both pointers."),
                    ("small", "`a[i]` is smaller than `b[j]`, and everything after `b[j]` is even bigger, so `a[i]` can't be "
                              "matched. Skip it."),
                    ("big", "The mirror case: `b[j]` is too small to match anything left in `a`."),
                    ("ret", "The number of matched pairs.", {"c": "Free both copies first."}),
                ],
                COMMON_RUN,
                "common_count([5, 1, 3, 3, 8], [3, 9, 1, 3, 3]); common_count([2, 4], [6, 8])",
            ),
            """
            ### The smallest amount you can't pay

            You have some coins (positive values, repeats allowed). What's the smallest amount you *can't* pay exactly
            using some of them? Trying every subset is 2ⁿ. Sorting gives a neat O(n log n) answer with a real proof
            behind it.

            Keep `reach`: every amount from 0 to `reach` can be paid with the coins used so far. Take coins smallest
            first. If the next coin `c` is at most `reach + 1`, then adding it to each amount 0..reach covers `c` to
            `reach + c`, which joins up with 0..reach with no gap. So now 0..reach + c are all payable. If `c` is bigger
            than `reach + 1`, then `reach + 1` can't be paid: the coins used so far can't make it, and every remaining
            coin is already too big.
            """,
            walk(uw),
            code(
                "Smallest amount the coins can't pay",
                UNREACH,
                [
                    ("sort", "Smallest coins first. The argument only works in this order."),
                    ("cmp", "Overflow-safe comparison for `qsort`."),
                    ("reach", "With no coins, the only payable amount is 0. The total can grow past 2³¹, so it's 64-bit."),
                    ("loop", "Take the coins in increasing order."),
                    ("gap", "If this coin is bigger than `reach + 1`, nothing can ever make `reach + 1`. Stop."),
                    ("grow", "Otherwise the payable range grows to `0..reach + c` with no gaps."),
                    ("ret", "The first amount that isn't payable.", {"c": "Free the copy first."}),
                ],
                UNREACH_RUN,
                "smallest_unpayable([1, 5, 1, 2, 12]); smallest_unpayable([1, 1, 1, 1]); smallest_unpayable([2, 3])",
            ),
            """
            With `[2, 3]` the answer is 1 straight away: the smallest coin is already too big to make 1.

            ### Sorting with the original positions

            When you need to sort but also answer in terms of original indices, sort pairs `(value, index)`. Python sorts
            tuples by value then index; in Java sort an `Integer[]` of indices with a comparator on the values; in C++
            sort `pair<int, int>`; in C sort an array of structs.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            The sort dominates: O(n log n) time. The scan afterwards is O(n). Walking two lists is O(n log n + m log m)
            for the sorts plus O(n + m) for the walk.

            Memory depends on the sort and whether you copy the input. Sorting a copy is O(n) extra; sorting in place can
            be O(log n) (quicksort's recursion) or O(n) (merge sort).

            For `n = 100,000`, n log n is about {int(N * 17):,} comparisons, against {N * (N - 1) // 2:,} for comparing
            every pair. A hash-based approach can get to O(n) on average, which is why "sort then scan" is often the
            simple, solid answer, and hashing the faster one when the interviewer asks for O(n).
            """,
            table(
                ["Approach", "Time", "Extra space", "Keeps original order?"],
                ["Compare every pair", "O(n²)", "O(1)", "yes"],
                ["Sort then scan", "O(n log n)", "O(1) to O(n)", "no (unless you sort a copy)"],
                ["Hash set / hash map", "O(n) on average", "O(n)", "yes"],
                ["Counting sort (values 0..R)", "O(n + R)", "O(R)", "no"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `sorted(xs)` returns a new list; `xs.sort()` sorts in place and returns `None` (a classic bug is
            `xs = xs.sort()`). Sort by a key with `key=lambda p: (p[1], -p[0])`. Sorting is stable.

            ### Java

            `Arrays.sort(int[])` for primitives, `Collections.sort(list)` or `list.sort(cmp)` for objects. A comparator
            written as `(a, b) -> a - b` can overflow on large values; use `Integer.compare(a, b)`. Sorting an `int[]` by
            a custom rule needs boxing to `Integer[]`.

            ### C++

            `sort(v.begin(), v.end())`, with a lambda for custom order: `sort(v.begin(), v.end(), [](auto& a, auto& b)
            { return a.second < b.second; })`. The comparator must be a strict "less than" (never `<=`), or the sort can
            misbehave. `unique` plus `erase` removes adjacent duplicates after sorting.

            ### C

            `qsort(arr, n, sizeof(arr[0]), cmp)`. The comparator returns negative, zero or positive. Write it as
            `(x > y) - (x < y)`, not `x - y`, which overflows for values far apart.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Losing original positions. If the answer needs indices, sort `(value, index)` pairs.
            - Sorting the caller's array when you shouldn't. Sort a copy if the input must stay as it was.
            - Comparators that overflow (`a - b`) or aren't strict (`<=` in C++).
            - Off-by-one at the start of the scan: `a[i - 1]` doesn't exist at `i = 0`.
            - Forgetting that the last run never gets "closed" by a different value. If you do something at the end of
              each run, handle the final run after the loop.
            - Using a greedy order without a reason. Smallest first is right for the coin problem; for other problems it
              might be largest first, or by deadline. Check with an exchange argument or small examples.
            - Sorting when O(n) is required.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why is it enough to compare neighbours to find the two closest values in a sorted array?",
                 "If a[i] ≤ a[k] ≤ a[j], then a[j] - a[i] ≥ a[k] - a[i]. Any pair with something between them is at least as far apart as a neighbouring pair, so the closest pair is always neighbours."),
                ("In `common_count`, why is it safe to skip `a[i]` when `a[i] < b[j]`?",
                 "Both lists are sorted, so everything from `b[j]` onwards is at least `b[j]`, which is bigger than `a[i]`. Nothing left in `b` can equal `a[i]`."),
                ("Coins [1, 2, 4, 9]. What's the smallest amount you can't pay?",
                 "Reach goes 0 → 1 → 3 → 7. The next coin is 9, which is bigger than 8, so the answer is 8."),
                ("Why does `smallest_unpayable` need the coins sorted?",
                 "The argument relies on every remaining coin being at least as big as the current one. In a different order, a big coin could appear before a small one that would have filled the gap, and you'd stop too early."),
                ("When would you choose a hash set over sorting to count distinct values?",
                 "When O(n) time is required or the original order must be kept. Sorting is O(n log n) but needs no hashing and can work in place."),
            ),
        ]),
    ],
)
