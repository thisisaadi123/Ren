"""Lesson: Complement lookup (Arrays & Hashing, pattern 2)."""
from lesson import Bars, Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

COUNT_PAIRS = {
    "python": """
        def count_pairs(nums, target):
            seen = {}                               #@make
            pairs = 0                               #@make
            for x in nums:                          #@loop
                need = target - x                   #@need
                pairs += seen.get(need, 0)          #@look
                seen[x] = seen.get(x, 0) + 1        #@add
            return pairs                            #@ret
    """,
    "java": """
        static long countPairs(int[] nums, int target) {
            Map<Integer, Integer> seen = new HashMap<>();   //@make
            long pairs = 0;                                 //@make
            for (int x : nums) {                            //@loop
                int need = target - x;                      //@need
                pairs += seen.getOrDefault(need, 0);        //@look
                seen.merge(x, 1, Integer::sum);             //@add
            }
            return pairs;                                   //@ret
        }
    """,
    "cpp": """
        long long countPairs(const vector<int>& nums, int target) {
            unordered_map<int, int> seen;                   //@make
            seen.reserve(nums.size() * 2);                  //@make
            long long pairs = 0;                            //@make
            for (int x : nums) {                            //@loop
                int need = target - x;                      //@need
                auto it = seen.find(need);                  //@look
                if (it != seen.end()) pairs += it->second;  //@look
                seen[x]++;                                  //@add
            }
            return pairs;                                   //@ret
        }
    """,
    "c": """
        typedef struct {
            int *keys, *counts;
            bool *used;
            size_t mask;
        } CountMap;                                                         //@table

        static size_t cm_slot(const CountMap* m, int key) {
            size_t i = ((uint32_t)key * 2654435761u) & m->mask;             //@table
            while (m->used[i] && m->keys[i] != key) i = (i + 1) & m->mask;  //@table
            return i;
        }

        long long countPairs(const int* nums, int n, int target) {
            size_t cap = 16;                                                //@make
            while (cap < 2 * (size_t)n) cap <<= 1;                          //@make
            CountMap seen = {malloc(cap * sizeof(int)), calloc(cap, sizeof(int)), calloc(cap, sizeof(bool)), cap - 1};  //@make
            long long pairs = 0;                                            //@make
            for (int j = 0; j < n; j++) {                                   //@loop
                int need = target - nums[j];                                //@need
                size_t i = cm_slot(&seen, need);                            //@look
                if (seen.used[i]) pairs += seen.counts[i];                  //@look
                i = cm_slot(&seen, nums[j]);                                //@add
                seen.used[i] = true;                                        //@add
                seen.keys[i] = nums[j];                                     //@add
                seen.counts[i]++;                                           //@add
            }
            free(seen.keys); free(seen.counts); free(seen.used);            //@free
            return pairs;                                                   //@ret
        }
    """,
}
COUNT_PAIRS_RUN = {
    "python": """
        print(count_pairs([2, 7, 4, 5, 2, 5], 9))
        print(count_pairs([3, 3, 3, 3], 6))
        print(count_pairs([1, 2, 3], 100))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(countPairs(new int[] {2, 7, 4, 5, 2, 5}, 9));
            System.out.println(countPairs(new int[] {3, 3, 3, 3}, 6));
            System.out.println(countPairs(new int[] {1, 2, 3}, 100));
        }
    """,
    "cpp": """
        int main() {
            cout << countPairs({2, 7, 4, 5, 2, 5}, 9) << "\\n" << countPairs({3, 3, 3, 3}, 6) << "\\n" << countPairs({1, 2, 3}, 100) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {2, 7, 4, 5, 2, 5}, b[] = {3, 3, 3, 3}, c[] = {1, 2, 3};
            printf("%lld\\n%lld\\n%lld\\n", countPairs(a, 6, 9), countPairs(b, 4, 6), countPairs(c, 3, 100));
            return 0;
        }
    """,
}

FIRST_PAIR = {
    "python": """
        def first_pair(nums, target):
            where = {}                              #@make
            for j, x in enumerate(nums):            #@loop
                need = target - x                   #@need
                if need in where:                   #@look
                    return [where[need], j]         #@look
                if x not in where:                  #@keep
                    where[x] = j                    #@keep
            return [-1, -1]                         #@none
    """,
    "java": """
        static int[] firstPair(int[] nums, int target) {
            Map<Integer, Integer> where = new HashMap<>();          //@make
            for (int j = 0; j < nums.length; j++) {                 //@loop
                int need = target - nums[j];                        //@need
                Integer i = where.get(need);                        //@look
                if (i != null) return new int[] {i, j};             //@look
                where.putIfAbsent(nums[j], j);                      //@keep
            }
            return new int[] {-1, -1};                              //@none
        }
    """,
    "cpp": """
        pair<int, int> firstPair(const vector<int>& nums, int target) {
            unordered_map<int, int> where;                          //@make
            for (int j = 0; j < (int)nums.size(); j++) {            //@loop
                int need = target - nums[j];                        //@need
                auto it = where.find(need);                         //@look
                if (it != where.end()) return {it->second, j};      //@look
                where.emplace(nums[j], j);                          //@keep
            }
            return {-1, -1};                                        //@none
        }
    """,
    "c": """
        typedef struct {
            int *keys, *idx;
            bool *used;
            size_t mask;
        } IndexMap;                                                         //@table

        static size_t im_slot(const IndexMap* m, int key) {
            size_t i = ((uint32_t)key * 2654435761u) & m->mask;             //@table
            while (m->used[i] && m->keys[i] != key) i = (i + 1) & m->mask;  //@table
            return i;
        }

        void firstPair(const int* nums, int n, int target, int out[2]) {
            size_t cap = 16;                                                //@make
            while (cap < 2 * (size_t)n) cap <<= 1;                          //@make
            IndexMap where = {malloc(cap * sizeof(int)), malloc(cap * sizeof(int)), calloc(cap, sizeof(bool)), cap - 1};  //@make
            out[0] = out[1] = -1;                                           //@none
            for (int j = 0; j < n; j++) {                                   //@loop
                int need = target - nums[j];                                //@need
                size_t i = im_slot(&where, need);                           //@look
                if (where.used[i]) {                                        //@look
                    out[0] = where.idx[i];                                  //@look
                    out[1] = j;                                             //@look
                    break;                                                  //@look
                }
                i = im_slot(&where, nums[j]);                               //@keep
                if (!where.used[i]) {                                       //@keep
                    where.used[i] = true;                                   //@keep
                    where.keys[i] = nums[j];                                //@keep
                    where.idx[i] = j;                                       //@keep
                }
            }
            free(where.keys); free(where.idx); free(where.used);            //@free
        }
    """,
}
FIRST_PAIR_RUN = {
    "python": """
        for nums, t in [([8, 3, 5, 3, 6], 6), ([1, 4, 2, 4], 8), ([5, 1], 7)]:
            print(*first_pair(nums, t))
    """,
    "java": """
        public static void main(String[] args) {
            int[][] arrays = {{8, 3, 5, 3, 6}, {1, 4, 2, 4}, {5, 1}};
            int[] targets = {6, 8, 7};
            for (int k = 0; k < 3; k++) {
                int[] p = firstPair(arrays[k], targets[k]);
                System.out.println(p[0] + " " + p[1]);
            }
        }
    """,
    "cpp": """
        int main() {
            vector<pair<vector<int>, int>> cases = {{{8, 3, 5, 3, 6}, 6}, {{1, 4, 2, 4}, 8}, {{5, 1}, 7}};
            for (auto& [nums, t] : cases) {
                auto [i, j] = firstPair(nums, t);
                cout << i << " " << j << "\\n";
            }
        }
    """,
    "c": """
        int main(void) {
            int a[] = {8, 3, 5, 3, 6}, b[] = {1, 4, 2, 4}, c[] = {5, 1}, out[2];
            firstPair(a, 5, 6, out); printf("%d %d\\n", out[0], out[1]);
            firstPair(b, 4, 8, out); printf("%d %d\\n", out[0], out[1]);
            firstPair(c, 2, 7, out); printf("%d %d\\n", out[0], out[1]);
            return 0;
        }
    """,
}

XOR_PAIRS = {
    "python": """
        def xor_pairs(nums, t):
            seen = [0] * 1024                       #@make
            pairs = 0                               #@make
            for x in nums:                          #@loop
                pairs += seen[x ^ t]                #@look
                seen[x] += 1                        #@add
            return pairs                            #@ret
    """,
    "java": """
        static long xorPairs(int[] nums, int t) {
            int[] seen = new int[1024];             //@make
            long pairs = 0;                         //@make
            for (int x : nums) {                    //@loop
                pairs += seen[x ^ t];               //@look
                seen[x]++;                          //@add
            }
            return pairs;                           //@ret
        }
    """,
    "cpp": """
        long long xorPairs(const vector<int>& nums, int t) {
            vector<int> seen(1024, 0);              //@make
            long long pairs = 0;                    //@make
            for (int x : nums) {                    //@loop
                pairs += seen[x ^ t];               //@look
                seen[x]++;                          //@add
            }
            return pairs;                           //@ret
        }
    """,
    "c": """
        long long xorPairs(const int* nums, int n, int t) {
            int seen[1024] = {0};                   //@make
            long long pairs = 0;                    //@make
            for (int i = 0; i < n; i++) {           //@loop
                pairs += seen[nums[i] ^ t];         //@look
                seen[nums[i]]++;                    //@add
            }
            return pairs;                           //@ret
        }
    """,
}
XOR_PAIRS_RUN = {
    "python": """
        print(xor_pairs([5, 1, 4, 0, 5], 5))
        print(xor_pairs([9, 9, 9], 0))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(xorPairs(new int[] {5, 1, 4, 0, 5}, 5));
            System.out.println(xorPairs(new int[] {9, 9, 9}, 0));
        }
    """,
    "cpp": """
        int main() {
            cout << xorPairs({5, 1, 4, 0, 5}, 5) << "\\n" << xorPairs({9, 9, 9}, 0) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {5, 1, 4, 0, 5}, b[] = {9, 9, 9};
            printf("%lld\\n%lld\\n", xorPairs(a, 5, 5), xorPairs(b, 3, 0));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

count_pairs = py(COUNT_PAIRS["python"], "count_pairs")
first_pair = py(FIRST_PAIR["python"], "first_pair")
xor_pairs = py(XOR_PAIRS["python"], "xor_pairs")

DEMO, T = [2, 7, 4, 5, 2, 5], 9
ANSWER = count_pairs(DEMO, T)
BRUTE = sum(1 for i in range(len(DEMO)) for j in range(i + 1, len(DEMO)) if DEMO[i] + DEMO[j] == T)
assert ANSWER == BRUTE
PAIR_LIST = [(i, j) for i in range(len(DEMO)) for j in range(i + 1, len(DEMO)) if DEMO[i] + DEMO[j] == T]
NPAIRS = len(DEMO) * (len(DEMO) - 1) // 2

# Every pair brute force checks: the upper triangle of sums.
SUMS = [["" if j <= i else DEMO[i] + DEMO[j] for j in range(len(DEMO))] for i in range(len(DEMO))]
SUM_ST = {(i, j): ("answer" if DEMO[i] + DEMO[j] == T else None) for i in range(len(DEMO)) for j in range(i + 1, len(DEMO))}

VALS = sorted(set(DEMO))
steps = Steps(f"`count_pairs({DEMO}, {T})`. At each value: work out its partner, ask the table, then add the value.")
steps.step(f"The table starts empty. Nothing came before the first element, so it can't pair with anything yet.",
           Row(DEMO, slots=True), Bars([0] * len(VALS), labels=VALS, label="seen so far", top=2), M({"pairs": 0}))
seen, pairs = {}, 0
trace_rows = []
for j, x in enumerate(DEMO):
    need = T - x
    got = seen.get(need, 0)
    pairs += got
    partners = [i for i in range(j) if DEMO[i] == need]
    if got:
        msg = f"{x} needs {T} - {x} = {need}. The table has {got} of those (index {', '.join(map(str, partners))}), so that's {got} new pair{'s' if got > 1 else ''}. Then {x} goes in."
    else:
        msg = f"{x} needs {T} - {x} = {need}. No {need} so far, so no pair ends here. {x} goes in."
    seen[x] = seen.get(x, 0) + 1
    st = {i: "found" for i in partners}
    st[j] = "active"
    bst = {VALS.index(need): "found"} if need in VALS and got else {}
    bst[VALS.index(x)] = "new"
    steps.step(msg, Row(DEMO, st=st, ptr={"x": j}, slots=True), Bars([seen.get(v, 0) for v in VALS], labels=VALS, st=bst, label="seen so far", top=2), M({"pairs": pairs}))
    trace_rows.append((str(j), str(x), str(need), str(got), str(pairs)))
steps.step(f"Done. Each pair was found once, when we reached its second element: {pairs} pairs.", Row(DEMO, slots=True), M({"pairs": pairs}), result=pairs)

FP = [([8, 3, 5, 3, 6], 6), ([1, 4, 2, 4], 8), ([5, 1], 7)]
fp_rows = [(str(n), str(t), str(first_pair(n, t))) for n, t in FP]

FPD, FPT = [8, 3, 5, 3, 6], 6
fwalk = Steps(f"`first_pair({FPD}, {FPT})`. This time the table remembers *where* it first saw each value.")
where = {}
fwalk.step("Empty table.", Row(FPD, slots=True), M({"where": "{ }"}))
for j, x in enumerate(FPD):
    need = FPT - x
    if need in where:
        fwalk.step(f"{x} needs {need}, and the table says we saw {need} at index {where[need]}. Answer: [{where[need]}, {j}].",
                   Row(FPD, st={where[need]: "answer", j: "answer"}, ptr={"j": j}, slots=True), M({f"{k}": f"index {v}" for k, v in where.items()}, "where"), result=[where[need], j])
        break
    fresh = x not in where
    where.setdefault(x, j)
    fwalk.step(f"{x} needs {need}. Not seen yet. " + (f"Remember that {x} is at index {j}." if fresh else f"{x} is already in the table at index {where[x]}, and we keep that earlier one."),
               Row(FPD, st={j: "active"}, ptr={"j": j}, slots=True), M({f"{k}": f"index {v}" for k, v in where.items()}, "where"))

XD, XT = [5, 1, 4, 0, 5], 5
XOR_ANS = xor_pairs(XD, XT)
assert XOR_ANS == sum(1 for i in range(len(XD)) for j in range(i + 1, len(XD)) if XD[i] ^ XD[j] == XT)
xor_rows = [(str(x), f"{x:03b}", f"{x ^ XT:03b}", str(x ^ XT)) for x in sorted(set(XD))]

# Remainders: pairs whose sum is divisible by k
RK, RNUMS = 5, [7, 3, 12, 8, 10, 15]
rem_rows = [(str(x), str(x % RK), str((RK - x % RK) % RK)) for x in RNUMS]
RCOUNT = [sum(1 for x in RNUMS if x % RK == r) for r in range(RK)]
RPAIRS = sum(1 for i in range(len(RNUMS)) for j in range(i + 1, len(RNUMS)) if (RNUMS[i] + RNUMS[j]) % RK == 0)

# Two pointers on sorted input.
SORTED, ST = [1, 3, 4, 6, 8, 11], 10
tp = Steps(f"Sorted `{SORTED}`, target {ST}. One pointer at each end.")
l, r = 0, len(SORTED) - 1
while l < r:
    s = SORTED[l] + SORTED[r]
    if s == ST:
        tp.step(f"{SORTED[l]} + {SORTED[r]} = {s}. Found it.", Row(SORTED, st={l: "answer", r: "answer"}, ptr={"L": l, "R": r}, slots=True), result=[l, r])
        break
    if s < ST:
        tp.step(f"{SORTED[l]} + {SORTED[r]} = {s}, too small. The only way to grow the sum is to move L right (R already points at the biggest value still in play).",
                Row(SORTED, st={l: "active", r: "active", **{i: "dim" for i in range(l)}}, ptr={"L": l, "R": r}, slots=True))
        l += 1
    else:
        tp.step(f"{SORTED[l]} + {SORTED[r]} = {s}, too big. {SORTED[r]} is too large to pair with anything still in range, so move R left.",
                Row(SORTED, st={l: "active", r: "active", **{i: "dim" for i in range(r + 1, len(SORTED))}}, ptr={"L": l, "R": r}, slots=True))
        r -= 1

# Meet in the middle, tiny: a + b + c + d = 0.
MA, MB, MC, MD = [1, -2], [-1, 2], [0, 3], [-3, 0]
ab = {}
for a in MA:
    for b in MB:
        ab[a + b] = ab.get(a + b, 0) + 1
mm_rows, MM = [], 0
for c in MC:
    for d in MD:
        got = ab.get(-(c + d), 0)
        MM += got
        mm_rows.append((f"{c} + {d} = {c + d}", str(-(c + d)), str(got)))
assert MM == sum(1 for a in MA for b in MB for c in MC for d in MD if a + b + c + d == 0)

# Worked example: index pairs with a fixed difference.
GD, GK = [4, 1, 6, 3, 8, 6], 2
g_rows, gseen, gtot = [], {}, 0
for j, y in enumerate(GD):
    add = gseen.get(y - GK, 0)
    gtot += add
    g_rows.append((str(j), str(y), str(y - GK), str(add), str(gtot)))
    gseen[y] = gseen.get(y, 0) + 1
assert gtot == sum(1 for i in range(len(GD)) for j in range(i + 1, len(GD)) if GD[j] - GD[i] == GK)

N = 10**5
lesson(
    "arrays-hashing",
    "complement-lookup",
    """
    When you're looking for two things that fit together (two numbers that add up to a target, two that differ by
    `k`), you don't have to go searching. Work out exactly what the partner has to be, and check whether you've
    already seen it.
    """,
    [
        ("idea", "The idea", [
            """
            Say you're at a shop with exactly $9 of gift card and you want to spend all of it on two items. You pick up
            something that costs $7. You don't need to compare it against every other price on the shelf. You already
            know the only thing that works with it is something costing exactly $2. So the question becomes "have I
            seen a $2 item?".

            In a lot of pair problems, knowing one half tells you exactly what the other half
            must be:

            - if `x + y = target`, then `y = target - x`
            - if `y - x = k`, then `y = x + k`
            - if `x XOR y = t`, then `y = x XOR t`

            So for each element, you compute the partner it needs and ask a hash table whether you've met it. That's
            one O(1) question per element, instead of comparing against everyone.
            """,
            f"""
            Here's what the slow way looks like. To find pairs in `{DEMO}` adding up to {T}, brute force fills in this
            whole triangle of sums, {NPAIRS} of them, just to find the {BRUTE} that hit the target:
            """,
            fig(Grid(SUMS, st=SUM_ST, label="nums[i] + nums[j] for every i < j"),
                caption=f"Brute force checks every cell. Complement lookup visits each of the {len(DEMO)} elements once and asks one question."),
            key("""
            Walk through the array once. At each element, work out the partner it needs, look it up among the elements
            you've already passed, and only then add the current element to the table.
            """),
            """
            Because the element goes into the table *after* the lookup, each element only ever pairs with elements
            that came before it. So every pair gets found exactly once (when you reach
            its second element), nothing pairs with itself, and nothing is counted twice.
            """,
        ]),
        ("signals", "When to reach for it", [
            """
            You're looking for the shape "find or count pairs where some condition holds", where knowing one side pins
            down the other exactly. Some common versions:
            """,
            table(
                ["The problem says…", "partner of x", "the table holds"],
                ["two values that add up to `t`", "`t - x`", "value → index, or value → count"],
                ["pairs with difference `k`", "`x - k` (and maybe `x + k`)", "value → count, or a set"],
                ["pairs whose XOR is `t`", "`x ^ t`", "value → count"],
                ["pair sum divisible by `k`", "remainder `(k - x % k) % k`", "remainder → count"],
                ["`a[i] + b[j] = t` across two lists", "`t - b[j]`", "all of list `a`, counted"],
                ["4 lists, `a + b + c + d = 0`", "`-(c + d)`", "every `a + b`, counted"],
            ),
            """
            It doesn't work well for inequalities. "Pairs with a sum *less than* `t`" has a whole range of valid
            partners, and a hash table can only answer "is this exact value here?". For that, sort and use two
            pointers or binary search.

            If the array is already sorted and you're short on memory, two pointers from both ends (shown in
            *Variations*) finds a pair with no table at all. And if the problem wants you to *list* every pair, there
            might be about n² of them, so no trick makes that fast. Counting them is still quick though.

            Triples and bigger are a step up: three-sum usually fixes one element and runs a two-sum on the rest,
            which is O(n²). The table helps with the inner part, but the outer loop is still there.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Solving for the partner

            The pattern only works when you can turn the condition around and solve for the other side. Write the
            condition as `x ⊕ y = t`, where `⊕` is some operation. If you can undo `⊕`, then there's exactly one `y`
            that works, and you can compute it directly:
            """,
            table(
                ["condition", "partner", "why you can do that"],
                ["`x + y = t`", "`y = t - x`", "subtraction undoes addition"],
                ["`y - x = k`", "`y = x + k`", "addition undoes subtraction"],
                ["`x ^ y = t`", "`y = x ^ t`", "XOR undoes itself: `x ^ x = 0`"],
                ["`(x + y) % k = 0`", "`y % k = (k - x % k) % k`", "remainders add up like numbers do, mod k"],
                ["`x * y = t`", "`y = t / x`, if `x` divides `t`", "only when `x` isn't 0 and divides `t`"],
            ),
            """
            When the answer isn't unique, like `x * y = 0` when `x` is 0 (any `y` works), you handle those values on
            their own.

            ### Why one pass is enough

            The loop keeps one thing true:

            > Just before the loop looks at index `j`, the table holds exactly the elements at indices `0` to `j - 1`.

            It's true at the start (the table is empty when `j = 0`). Each step looks things up first and adds `a[j]`
            last, so it's still true when we move on to `j + 1`. That means the lookup at `j` sees every possible
            partner to its left and nothing else. Add that up over all `j`, and every pair `i < j` gets counted
            exactly once. No two elements are ever compared directly.

            ### What to put in the table

            It depends on what the question wants back. If it's just "is there a pair?", a set of the values you've
            seen is enough. If it wants the positions, store value → index (and decide on purpose whether you keep the
            first or the latest index of a repeated value). If it wants the number of pairs, store value → count,
            because every earlier copy of the partner makes its own pair.

            ### Duplicates take care of themselves

            Take target 6 and `[3, 3]`. At index 0 the table is empty, so no pair, and then 3 goes in. At index 1 the
            partner is 6 - 3 = 3, which is in the table, so we've got one pair, (0, 1). A value can pair with a
            *different* copy of itself, but it can never pair with *itself*, because it isn't in the table yet when we
            look.

            ### Two lists, and meeting in the middle

            With two separate lists and `a[i] + b[j] = t`, put all of `a` into the table first (with counts), then go
            through `b` and look up `t - b[j]`. There's no "before" rule to worry about here, since every pair takes
            one element from each list.

            This scales up nicely. For four lists and `a + b + c + d = 0`, trying every combination is O(n⁴). Instead,
            put every `a[i] + b[j]` into a table (that's n² sums), then for every `c[k] + d[l]` look up its negative.
            That's O(n²). You've split one huge search into two halves that meet at the table. Here it is with lists
            of length 2:
            """,
            fig(Row(MA, label="a"), Row(MB, label="b"), M({str(k): v for k, v in ab.items()}, "a + b → how many ways"),
                caption="Every a + b sum, counted. There are only four, but with lists of 1,000 there'd be a million instead of a trillion combinations."),
            table(["c + d", "need a + b =", "ways"], *mm_rows),
            f"So there are {MM} ways for the four to add up to zero, found with 4 + 4 steps instead of 16.",
        ]),
        ("template", "The template", [
            """
            Count the pairs `i < j` where `nums[i] + nums[j] == target`. Values can repeat, and every pair of positions
            counts. We'll assume values and the target are between -10⁹ and 10⁹ (that turns out to matter, see
            *Pitfalls*).
            """,
            code(
                "Count pairs with a given sum",
                COUNT_PAIRS,
                [
                    ("make", "An empty table of how many times each value has appeared so far, and a 64-bit total. "
                             "With lots of equal values the number of pairs grows like n²/2, which gets big."),
                    ("loop", "One pass, left to right. The current element is always the *second* element of the pairs "
                             "we count here."),
                    ("need", "Solve `x + need = target` for `need`. With everything within ±10⁹, the difference stays "
                             "within ±2·10⁹, which still just about fits in a 32-bit `int`."),
                    ("look", "Every earlier copy of `need` makes one pair with this `x`. If there aren't any, that's 0.",
                     {"cpp": "Use `find` to look without changing anything. `seen[need]` would add `need` to the map with a count of 0, filling it up with values that never appeared."}),
                    ("add", "Only now does `x` go into the table. Later elements can pair with it, but it can't pair "
                            "with itself."),
                    ("ret", "Each pair was counted once, when we got to its second element."),
                    ("table", "The same little open-addressing table from *Frequency counting*: a power-of-two array of "
                              "slots, a multiply-and-mask hash, and a walk forward to the key or the first empty slot."),
                    ("free", "Hand the memory back."),
                ],
                COUNT_PAIRS_RUN,
                "count_pairs([2, 7, 4, 5, 2, 5], 9); count_pairs([3, 3, 3, 3], 6); count_pairs([1, 2, 3], 100)",
            ),
            f"""
            The second run is worth a look: four 3s with target 6. Every pair of positions works, so the answer is
            4 × 3 / 2 = {count_pairs([3, 3, 3, 3], 6)}, and none of them is a 3 paired with itself.
            """,
        ]),
        ("trace", "Trace it by hand", [
            """
            Step through it. The bars show how many of each value the table holds at that moment. When a partner is
            found, its bar lights up along with the earlier positions it came from.
            """,
            walk(steps),
            table(["j", "x", "partner", "partners already seen", "pairs so far"], *trace_rows),
            f"""
            If you check every pair by hand you get the same {BRUTE}: {', '.join(f'({i}, {j})' for i, j in PAIR_LIST)}.
            The scan found each one with {len(DEMO)} lookups, where brute force checked {NPAIRS} pairs.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Pairs a fixed distance apart

            How many pairs `i < j` have `nums[j] - nums[i] = {GK}` in `{GD}`? The partner of `y` (as the later element)
            is `y - {GK}`. Same loop, different partner:
            """,
            table(["j", "y", "partner y - 2", "seen before", "pairs so far"], *g_rows),
            f"""
            That's {gtot}. Notice the two 6s: each finds the 4 that came before it. If the question were about
            *distinct values* instead of positions, you'd count that as one pair, so read the wording carefully.

            ### XOR, bit by bit

            Why does `x ^ t` give the partner? XOR flips the bits of `x` wherever `t` has a 1. Doing it twice flips
            them back. With `t = {XT}` (binary `101`):
            """,
            table(["x", "x in binary", "x ^ 5 in binary", "partner"], *xor_rows),
            f"""
            So in `{XD}`, 5 pairs with 0 and 1 pairs with 4. With two 5s and one 0 that's two pairs, plus 1 and 4:
            {XOR_ANS} in total.

            ### Sums divisible by {RK}

            For `{RNUMS}`, only the remainder mod {RK} matters. A remainder of 2 needs a 3, a 1 needs a 4, and a 0
            needs another 0:
            """,
            fig(Bars(RCOUNT, labels=[f"r={r}" for r in range(RK)], label=f"how many numbers leave each remainder mod {RK}"),
                caption=f"Pairs: the {RCOUNT[2]} with remainder 2 against the {RCOUNT[3]} with remainder 3, plus pairs within remainder 0. That's {RPAIRS}."),
            table([f"x", f"x % {RK}", "partner remainder"], *rem_rows),
        ]),
        ("variations", "Variations", [
            """
            ### Return the positions instead

            Store value → index instead of value → count. The question then is which index to keep when a value
            repeats. If you only store a value the first time you see it, you'll always pair with the earliest
            possible left partner. This version returns the pair whose second element comes first, and among those,
            the one with the earliest first element.
            """,
            walk(fwalk),
            code(
                "First pair with a given sum",
                FIRST_PAIR,
                [
                    ("make", "value → the index where we first saw it."),
                    ("loop", "Scan left to right. `j` is the candidate second element."),
                    ("need", "The partner this element needs."),
                    ("look", "If we've seen the partner, we're done: `[where[need], j]`. Since we stop at the first `j` "
                             "that has any partner, no pair can end earlier."),
                    ("keep", "Only store `x` if it's new, so the table always holds the earliest index of each value.",
                     {"java": "`putIfAbsent` leaves an existing entry alone.",
                      "cpp": "`emplace` does nothing if the key is already there."}),
                    ("none", "No two elements add up to the target."),
                    ("table", "The open-addressing table again, storing an index for each key instead of a count."),
                    ("free", "Free the table before returning. The answer is already in `out`."),
                ],
                FIRST_PAIR_RUN,
                "first_pair([8, 3, 5, 3, 6], 6); first_pair([1, 4, 2, 4], 8); first_pair([5, 1], 7)",
            ),
            table(["nums", "target", "answer"], *fp_rows),
            """
            ### XOR, with an array for a table

            Since XOR undoes itself, the partner of `x` is `x ^ t`. When values are below 1024, so is their XOR, and a
            plain array of 1024 counters does the job.
            """,
            code(
                "Count pairs with a given XOR (values below 1024)",
                XOR_PAIRS,
                [
                    ("make", "Values are below 1024 (10 bits), so `x ^ t` is too. 1024 counters cover every possible partner."),
                    ("loop", "One pass."),
                    ("look", "The partner is `x ^ t`. Each earlier copy of it is one pair."),
                    ("add", "Then count `x` itself."),
                    ("ret", "The number of pairs `i < j` with `nums[i] ^ nums[j] == t`."),
                ],
                XOR_PAIRS_RUN,
                "xor_pairs([5, 1, 4, 0, 5], 5); xor_pairs([9, 9, 9], 0)",
            ),
            """
            With `t = 0`, the partner of `x` is `x` itself, so three 9s make three pairs.

            ### Difference `k`, both directions

            If the earlier element could be either the bigger or the smaller one, look up both `x - k` and `x + k`. If
            the problem counts *distinct value pairs* rather than positions, build a set or count map first and check
            each distinct value once: for `k > 0` you need `x + k` to be present, and for `k = 0` you need `x` to appear
            at least twice.

            ### Already sorted? Use two pointers

            On a sorted array you can find a pair with no table at all. Put one pointer at each end. If the sum is too
            small, move the left one right; if it's too big, move the right one left. Each step throws away an element
            that can't be part of any answer.
            """,
            walk(tp),
            """
            That's O(n) time and O(1) memory, and unlike hashing it also handles "less than" questions. The catch is
            that the array has to be sorted, and sorting costs O(n log n) and loses the original positions.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            Brute force checks all `n(n - 1)/2` pairs, which is O(n²). For `n = 100,000` that's {N * (N - 1) // 2:,}
            checks.

            Complement lookup does one lookup and one insert per element. Each is O(1) on average with a hash table,
            so the whole thing is O(n) on average, with O(n) extra memory for the table. If the table is a plain array
            (XOR below 1024, remainders mod `k`), it's O(n) guaranteed plus the array's size.

            Meeting in the middle for four lists of length `n` costs O(n²) time and O(n²) memory, instead of O(n⁴) time.
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Check every pair", "O(n²)", "O(1)"],
                ["Sort, then two pointers", "O(n log n)", "O(1) to O(n)"],
                ["Complement lookup, hash table", "O(n) on average", "O(n)"],
                ["Complement lookup, array of size R", "O(n + R)", "O(R)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `seen.get(need, 0)` for counts and `need in where` to check existence. Python integers never overflow, so
            `t - x` is always exact.

            ### Java

            `getOrDefault(need, 0)`, `merge(x, 1, Integer::sum)` and `putIfAbsent`. Be careful with `map.get`: it
            returns `null` for a missing key, and if you assign that straight into an `int`, Java throws a
            `NullPointerException`. Read it into an `Integer` first, like `firstPair` does. If values can be anywhere in
            the `int` range, compute `long need = (long) t - x` and skip the lookup when it doesn't fit in an `int`.

            ### C++

            Look things up with `find` (or `count`). `seen[need]` would insert a 0. `emplace` keeps the first index if
            the key's already there. On inputs designed to cause collisions, `unordered_map<int, int>` can slow right
            down; `reserve` helps with resizing, and a randomised hash helps against deliberate collisions.

            ### C

            The small open-addressing table from the template works, or a plain array when values are bounded.
            Another route is to sort a copy of the values along with their indices and use two pointers.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            The mistakes that come up most:

            - Adding the element *before* looking it up. Then it pairs with itself, and `[3]` with target 6 reports a
              pair that doesn't exist.
            - Filling the whole table first and then scanning. Every pair gets found twice (once from each end), and
              any `x` with `2x = t` pairs with itself. If you really must build first, correct for both, or just switch
              to the one-pass version.
            - Overflow in `t - x`. Near the edges of a 32-bit `int`, the subtraction wraps around and gives you a wrong
              partner that still looks like a normal number. Use 64-bit arithmetic when the bounds call for it.
            - Negative remainders. In Java, C and C++, `-7 % 5` is `-2`, not `3`. Fix it with `((x % k) + k) % k`.
            - Using a set when duplicates matter. A set knows there's a 5; it can't tell you there are three of them.
            - Keeping the first index versus the latest. Writing `where[x] = j` every time keeps the latest one. That's
              right for some questions (the closest pair) and wrong for others (the earliest pair).
            - `k = 0` in difference problems. The partner is the value itself, so it only counts if it shows up twice.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why does the lookup have to happen before the current element is added?",
                 "So the table only holds earlier elements. That way each pair `i < j` is found exactly once, when we reach `j`, and no element can pair with itself."),
                ("`nums = [4, 4, 4]` and `target = 8`. What does `count_pairs` return, and how does it get there?",
                 "3. At index 0 the table is empty. At index 1 it has one 4, so one pair. At index 2 it has two 4s, so two more. That's every pair of positions: 3 × 2 / 2 = 3."),
                ("You need the number of pairs with `nums[i] + nums[j] < target`. Does complement lookup work?",
                 "Not really. A hash table answers \"is this exact value here?\", and here a whole range of partners would work. Sort the array and use two pointers, or binary search for each element."),
                ("How can you count `(i, j, k, l)` with `a[i] + b[j] + c[k] + d[l] = 0` faster than O(n⁴)?",
                 "Put every `a[i] + b[j]` into a table with counts (n² sums). Then for every `c[k] + d[l]`, add the count of its negative. That's O(n²) time and space."),
                ("In Java, why might `target - x` give the wrong partner, and how do you avoid it?",
                 "If the values are near the limits of `int`, the subtraction overflows and wraps around. Do it in `long`, and skip the lookup when the result doesn't fit in an `int`."),
            ),
        ]),
    ],
)
