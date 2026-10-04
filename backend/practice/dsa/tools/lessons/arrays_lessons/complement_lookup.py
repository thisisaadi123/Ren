"""Lesson: Complement lookup (Arrays & Hashing, pattern 2)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

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

steps = Steps(f"`count_pairs({DEMO}, {T})`: at each value, ask the table for its partner, then add the value.")
steps.step(f"The table starts empty: no earlier values, so no partners yet. Target {T}.", Row(DEMO, slots=True), M({"seen": "{ }", "pairs": 0}))
seen, pairs = {}, 0
trace_rows = []
for j, x in enumerate(DEMO):
    need = T - x
    got = seen.get(need, 0)
    pairs += got
    before = dict(seen)
    seen[x] = seen.get(x, 0) + 1
    partners = [i for i in range(j) if DEMO[i] == need]
    if got:
        msg = f"x = {x}, so we need {T} - {x} = {need}. The table has {got} of them (index {', '.join(map(str, partners))}): {got} new pair{'s' if got > 1 else ''}. Then add {x}."
    else:
        msg = f"x = {x}, so we need {T} - {x} = {need}. Not in the table yet: no pair ends here. Add {x}."
    st = {i: "found" for i in partners}
    st[j] = "active"
    steps.step(msg, Row(DEMO, st=st, ptr={"x": j}, slots=True), M({**{f"seen[{k}]": v for k, v in seen.items()}, "pairs": pairs}))
    trace_rows.append((str(j), str(x), str(need), str(got), str(pairs), "{" + ", ".join(f"{k}: {v}" for k, v in seen.items()) + "}"))
steps.step(f"Every pair was counted exactly once, at its right end. Total: {pairs}.", Row(DEMO, slots=True), M({"pairs": pairs}), result=pairs)

FP = [([8, 3, 5, 3, 6], 6), ([1, 4, 2, 4], 8), ([5, 1], 7)]
fp_rows = [(str(n), str(t), str(first_pair(n, t))) for n, t in FP]

XD, XT = [5, 1, 4, 0, 5], 5
XOR_ANS = xor_pairs(XD, XT)
assert XOR_ANS == sum(1 for i in range(len(XD)) for j in range(i + 1, len(XD)) if XD[i] ^ XD[j] == XT)

# Remainders: pairs whose sum is divisible by k
RK, RNUMS = 5, [7, 3, 12, 8, 10, 15]
rem_rows = [(str(x), str(x % RK), str((RK - x % RK) % RK)) for x in RNUMS]

N = 10**5
lesson(
    "arrays-hashing",
    "complement-lookup",
    """
    When you need two items that fit together (sum to a target, differ by `k`, XOR to `t`), don't search for the
    partner. Work out exactly what the partner must be, and ask a table of everything seen so far whether it's there.
    """,
    [
        ("idea", "The idea", [
            """
            You're doing a jigsaw. You pick up a piece with a particular tab on its edge. You could try it against
            every loose piece on the table, one by one. Or you could look at it, say "I need a piece with *this* exact
            hole", and go straight to the spot where such pieces are kept.

            Complement lookup is the second way. In a pair problem, one side of the pair usually **determines** the
            other:

            - if `x + y = target`, then `y` must be `target - x`;
            - if `y - x = k`, then `y = x + k` (or `x = y - k`);
            - if `x XOR y = t`, then `y = x XOR t`.

            So for each `x`, you don't search for a partner; you **compute** it. The only question left is "have I seen
            that value already?", and a hash table answers that in O(1).
            """,
            key("""
            Scan once. At each element, compute the partner it needs, look it up in a table of the elements **before**
            it, and only then add the element itself to the table.
            """),
            """
            **Why "before it" is the key detail.** Every pair `(i, j)` with `i < j` gets discovered exactly once: when
            the scan reaches `j`, element `i` is already in the table. Because the current element is added *after* the
            lookup, it can never pair with itself, and no pair is counted twice. This "look up, then insert" order is
            the heart of the pattern.
            """,
            fig(Row(DEMO, st={0: "found", 1: "active"}, ptr={"x": 1}, slots=True, label=f"target {T}"),
                M({"need": f"{T} - 7 = 2", "in the table?": "yes, index 0"}),
                caption="At `7`, the partner must be `2`. One lookup finds it among the earlier values."),
        ]),
        ("signals", "When to reach for it", [
            table(
                ["The problem says…", "Partner of x", "Table stores"],
                ["two values that add up to `t`", "`t - x`", "value → index or count"],
                ["pairs with difference `k`", "`x - k` and `x + k`", "value → count, or a set"],
                ["pairs whose XOR is `t`", "`x ^ t`", "value → count"],
                ["pair sum divisible by `k`", "remainder `(k - x % k) % k`", "remainder → count"],
                ["`a[i] + b[j] = t` across two lists", "`t - b[j]`", "all of list `a`, counted"],
                ["4 lists, `a + b + c + d = 0`", "`-(c + d)`", "every `a + b` sum, counted"],
            ),
            """
            **The recognisable shape:** "find / count pairs `(i, j)` such that `f(a[i], a[j]) = something`", where
            knowing one side pins down the other exactly.

            **When it is the wrong tool**

            - **Inequalities.** "Pairs with sum *less than* `t`" has a whole range of valid partners. A hash table
              answers "is this exact value here?", not "how many values are below this?". Sort, then use two pointers or
              binary search.
            - **The input is already sorted and memory is tight.** Two pointers from both ends finds a pair with a given
              sum in O(n) time and O(1) space.
            - **You must list every pair.** If the answer has O(n²) pairs, no trick makes it faster than its own size.
              Counting them, though, is still O(n).
            - **Triples and beyond.** Three-sum fixes one element and runs a two-sum on the rest, O(n²). Hashing helps
              the inner step, but the outer loop stays.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Inverting the equation

            Complement lookup works whenever the pair condition can be **solved for one side**. Write the condition as
            `x ⊕ y = t`. If the operation `⊕` has an inverse, then `y = t ⊖ x` has exactly one solution, and you can
            compute it:
            """,
            table(
                ["Condition", "Solve for the partner", "Works because"],
                ["`x + y = t`", "`y = t - x`", "subtraction undoes addition"],
                ["`y - x = k`", "`y = x + k`", "addition undoes subtraction"],
                ["`x ^ y = t`", "`y = x ^ t`", "XOR is its own inverse: `x ^ x = 0`"],
                ["`(x + y) % k = 0`", "`y % k = (k - x % k) % k`", "remainders add like numbers, mod k"],
                ["`x · y = t`", "`y = t / x` if `x` divides `t`", "only for non-zero `x` dividing `t`"],
            ),
            """
            When the inverse isn't unique (`x · y = 0` is satisfied by any `y` when `x = 0`), handle those values
            separately.

            ### The one-pass invariant

            Here's the precise statement that makes the loop correct:

            > **Invariant:** just before the scan processes index `j`, the table holds exactly the elements at
            > indices `0 .. j-1`.

            - It holds at the start (`j = 0`, empty table).
            - Each iteration looks up first and inserts `a[j]` last, so it holds again for `j + 1`.

            So the lookup at `j` sees every possible left partner `i < j` and nothing else. Summing over all `j` counts
            every pair `i < j` exactly once. That's the whole proof, and it's why we never compare two elements
            directly.

            ### What to store

            The table's values depend on what the question asks for:

            - **"Is there a pair?"**: a set of values seen.
            - **"Which pair?"** (return positions): value → index. Decide whether you want the first or the latest
              index of a repeated value and write that on purpose.
            - **"How many pairs?"**: value → count, since every earlier copy of the partner forms its own pair.

            ### Duplicates are handled for free

            Take `target = 6` and `nums = [3, 3]`. At index 0 the table is empty: no pair. Then `3` goes in. At index 1,
            the partner is `6 - 3 = 3`, which is in the table: one pair, `(0, 1)`. A value pairing with a different copy
            of itself works naturally, while pairing with *itself* is impossible because it isn't in the table yet.

            ### Two collections: meet in the middle

            With two lists, `a[i] + b[j] = t`, put all of `a` in the table (as counts), then scan `b` and look up
            `t - b[j]`. Here there's no "before" rule to worry about: the pairs are always one from each list.

            The same idea scales. For four lists with `a + b + c + d = 0`, trying every quadruple is O(n⁴). Instead,
            count every sum `a[i] + b[j]` in a table (n² entries), then for every `c[k] + d[l]` look up its negation.
            That's O(n²): you've split one O(n⁴) search into two O(n²) halves that **meet in the middle** at the table.
            """,
        ]),
        ("template", "The template", [
            """
            Count the pairs `i < j` with `nums[i] + nums[j] == target`. Values may repeat, and every pair of positions
            counts. Assume `|values|` and `|target|` are at most 10⁹ (that bound matters; see *Pitfalls*).
            """,
            code(
                "Count pairs with a given sum",
                COUNT_PAIRS,
                [
                    ("make", "An empty table of `value → how many times seen so far`, and a 64-bit total. With many "
                             "equal values the number of pairs grows like n²/2, beyond 32 bits."),
                    ("loop", "One pass, left to right. The current position is the **right** end of every pair we count here."),
                    ("need", "Solve `x + need = target` for the partner. With values and target within ±10⁹, the "
                             "difference stays within ±2·10⁹, which still fits in a 32-bit `int`."),
                    ("look", "Every earlier copy of `need` makes one pair with this `x`. A missing key counts as 0.",
                     {"cpp": "`find` looks without inserting. `seen[need]` would insert `need` with a 0 count, growing the table with values that never occurred."}),
                    ("add", "Only now does `x` join the table, so it can pair with later elements but never with itself."),
                    ("ret", "Each pair was counted once, at its right end."),
                    ("table", "The same open-addressing table as in *Frequency counting*: a power-of-two array of slots, "
                              "a multiplicative hash, and linear probing to the key or the first empty slot."),
                    ("free", "Give the table's memory back."),
                ],
                COUNT_PAIRS_RUN,
                "count_pairs([2, 7, 4, 5, 2, 5], 9); count_pairs([3, 3, 3, 3], 6); count_pairs([1, 2, 3], 100)",
            ),
            f"""
            The second run shows duplicates working: four `3`s with target `6` make every pair of positions valid,
            4 · 3 / 2 = {count_pairs([3, 3, 3, 3], 6)} pairs, and none of them is a `3` paired with itself.
            """,
        ]),
        ("trace", "Trace it by hand", [
            walk(steps),
            table(["j", "x", "need", "partners in table", "pairs so far", "table after"], *trace_rows),
            f"""
            Checking every pair directly gives the same {BRUTE}: {', '.join(f'({i}, {j})' for i, j in PAIR_LIST)}. The
            scan found each one at its right end, with {len(DEMO)} lookups instead of {len(DEMO) * (len(DEMO) - 1) // 2}
            pair checks.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Return positions instead of counting

            Store `value → index` instead of `value → count`. The question is now *which* index to keep for a repeated
            value. Keeping the **first** index (insert only if absent) means the pair you return uses the earliest
            possible left partner. The function below returns the pair whose right end comes first, and among those,
            the earliest left end.
            """,
            code(
                "First pair with a given sum",
                FIRST_PAIR,
                [
                    ("make", "`value → index of its first occurrence`."),
                    ("loop", "Scan left to right; `j` is the candidate right end."),
                    ("need", "The partner this element needs."),
                    ("look", "If the partner appeared earlier, `[where[need], j]` is the answer, and it's the first "
                             "right end that has any partner at all, because we stop the moment one exists."),
                    ("keep", "Record `x` only if it's new, so the table keeps the earliest index of every value.",
                     {"java": "`putIfAbsent` leaves an existing entry alone.",
                      "cpp": "`emplace` does nothing if the key already exists."}),
                    ("none", "No two elements add up to the target."),
                    ("table", "The open-addressing table again, storing an index per key instead of a count."),
                    ("free", "Free the table before returning; the answer is already in `out`."),
                ],
                FIRST_PAIR_RUN,
                "first_pair([8, 3, 5, 3, 6], 6); first_pair([1, 4, 2, 4], 8); first_pair([5, 1], 7)",
            ),
            table(["nums", "target", "answer"], *fp_rows),
            """
            In the first case, `3 + 3 = 6` uses two different positions (1 and 3), found at `j = 3`. In the second,
            `4 + 4 = 8` likewise; the single `4` at index 1 could not pair with itself.

            ### XOR partners

            XOR is its own inverse (`x ^ x = 0`, so `x ^ y = t` means `y = x ^ t`). With values below 1024 the table
            can be a plain array.
            """,
            code(
                "Count pairs with a given XOR (values below 1024)",
                XOR_PAIRS,
                [
                    ("make", "Values are below 1024, so `x ^ t` is too (both fit in 10 bits): 1024 counters cover every partner."),
                    ("loop", "One pass."),
                    ("look", "The partner of `x` is `x ^ t`; every earlier copy is one pair."),
                    ("add", "Then count `x` itself."),
                    ("ret", "Pairs `i < j` with `nums[i] ^ nums[j] == t`."),
                ],
                XOR_PAIRS_RUN,
                "xor_pairs([5, 1, 4, 0, 5], 5); xor_pairs([9, 9, 9], 0)",
            ),
            f"""
            For `{XD}` and `t = {XT}`: the pairs are `5 ^ 0` (twice, once per `5`) and `1 ^ 4`, so {XOR_ANS}. With
            `t = 0` the partner of `x` is `x` itself: three `9`s make 3 pairs.

            ### Difference `k`

            For ordered pairs (`y - x = k` with the `x` anywhere earlier or later), look up both `x - k` and `x + k` in
            the table of earlier values. If the problem asks for **distinct value pairs** rather than index pairs, build a
            set or count map first and check each distinct value once: `k > 0` needs `x + k` present, and `k = 0` needs
            `x` to appear at least twice.

            ### Remainders: sums divisible by `k`

            `x + y` is divisible by `k` exactly when their remainders add up to 0 or `k`. Count remainders seen so far,
            and look up the complementary remainder:
            """,
            table([f"x (k = {RK})", "x % k", "partner remainder (k - x % k) % k"], *rem_rows),
            """
            The outer `% k` turns a partner of `k` into `0`, so a remainder of `0` pairs with another `0`. The table has
            only `k` possible keys, so it can be an array of size `k`.

            ### Sorted input: two pointers instead

            If the array is sorted, start pointers at both ends. If the sum is too small, move the left one right; too
            big, move the right one left. That finds a pair in O(n) with O(1) memory. It's the right choice when the
            input is already sorted or you can't afford the table, and it also handles *less than* questions.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            **Brute force** checks every pair: `n(n - 1)/2` checks, so O(n²). For n = 10⁵ that's
            {N * (N - 1) // 2:,} checks.

            **Complement lookup** does one lookup and one insert per element: O(n) expected time (each hash operation is
            O(1) expected) and O(n) extra space for the table. With an array table (XOR below 1024, remainders mod `k`)
            it's O(n) worst case and O(R) space.

            **Meet in the middle** for four lists of length n: O(n²) time and O(n²) space instead of O(n⁴) time.
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Check every pair", "O(n²)", "O(1)"],
                ["Sort + two pointers", "O(n log n)", "O(1) to O(n)"],
                ["Complement lookup (hash table)", "O(n) expected", "O(n)"],
                ["Complement lookup (array, range R)", "O(n + R)", "O(R)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            **Python:** `seen.get(need, 0)` for counts; `need in where` for existence. Integers never overflow, so `t - x`
            is always exact.

            **Java:** `getOrDefault(need, 0)`, `merge(x, 1, Integer::sum)`, `putIfAbsent`. `map.get` returns `null` for
            a missing key; unboxing that `null` into an `int` throws `NullPointerException`, so read into an `Integer`
            first (as `firstPair` does). If values span the full `int` range, compute `long need = (long) t - x` and
            skip the lookup when it falls outside `int`.

            **C++:** use `find` (or `count`) to look up; `seen[need]` would insert. `emplace` keeps the first index.
            For untrusted inputs, `unordered_map<int, int>` can be slowed by keys chosen to collide; `reserve` helps
            with rehashing, and a salted hash helps against adversarial keys.

            **C:** a small open-addressing table (shown in the template) or, when values are bounded, a plain array.
            Another route is to sort a copy of the values with their indices and use two pointers.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - **Inserting before looking up.** The element pairs with itself: `[3]` with target `6` would report a pair.
            - **Filling the whole table first, then scanning.** Every pair is found twice (once from each end) and every
              `x` with `2x = t` pairs with itself. If you must build first, correct for both, or switch to the one-pass
              form.
            - **Overflow in `t - x`.** With values near ±2³¹, `t - x` overflows a 32-bit `int` and wraps to a wrong but
              valid-looking key. Use 64-bit arithmetic for the partner when the bounds allow it.
            - **Negative remainders.** In Java, C and C++, `-7 % 5` is `-2`, not `3`. Normalise with `((x % k) + k) % k`.
            - **A set when duplicates matter.** A set says "there's a 5"; it can't say "there are three 5s". Counting
              pairs needs counts.
            - **First vs latest index.** Overwriting `where[x] = j` on every occurrence keeps the latest index. That's
              right for some questions ("closest pair") and wrong for others ("earliest pair"). Choose deliberately.
            - **`k = 0` in difference problems.** The partner is the value itself; it only counts if it appears at least
              twice.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why must the lookup come before inserting the current element?",
                 "So the table holds only earlier elements. Then each pair `i < j` is found exactly once, at `j`, and no element can pair with itself."),
                ("`nums = [4, 4, 4]`, `target = 8`. What does `count_pairs` return, and how does it get there?",
                 "3. At index 0 nothing is in the table; at index 1 one `4` is (1 pair); at index 2 two `4`s are (2 more pairs). That's every pair of positions: 3 · 2 / 2 = 3."),
                ("You need the number of pairs with `nums[i] + nums[j] < target`. Does complement lookup work?",
                 "Not directly: a hash table answers exact-match questions, and here a whole range of partners qualifies. Sort and use two pointers (or binary search for each element)."),
                ("How do you count tuples with `a[i] + b[j] + c[k] + d[l] = 0` faster than O(n⁴)?",
                 "Count every `a[i] + b[j]` in a table (O(n²) sums). Then for every `c[k] + d[l]`, add the count of `-(c[k] + d[l])`. That's O(n²) time and space."),
                ("In Java, why might `target - x` give a wrong partner, and how do you avoid it?",
                 "If values are near the limits of `int`, the subtraction overflows and wraps around. Compute it as a `long` and skip the lookup when it's out of `int` range."),
            ),
        ]),
    ],
)
