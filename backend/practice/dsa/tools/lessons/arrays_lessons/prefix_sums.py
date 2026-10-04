"""Lesson: Prefix sums (Arrays & Hashing, pattern 4)."""
from lesson import Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

RANGE = {
    "python": """
        def build_prefix(nums):
            prefix = [0] * (len(nums) + 1)              #@make
            for i, x in enumerate(nums):                #@fill
                prefix[i + 1] = prefix[i] + x           #@fill
            return prefix                               #@ret

        def range_sum(prefix, l, r):
            return prefix[r + 1] - prefix[l]            #@query
    """,
    "java": """
        static long[] buildPrefix(int[] nums) {
            long[] prefix = new long[nums.length + 1];          //@make
            for (int i = 0; i < nums.length; i++) {             //@fill
                prefix[i + 1] = prefix[i] + nums[i];            //@fill
            }
            return prefix;                                      //@ret
        }

        static long rangeSum(long[] prefix, int l, int r) {
            return prefix[r + 1] - prefix[l];                   //@query
        }
    """,
    "cpp": """
        vector<long long> buildPrefix(const vector<int>& nums) {
            vector<long long> prefix(nums.size() + 1, 0);       //@make
            for (size_t i = 0; i < nums.size(); i++) {          //@fill
                prefix[i + 1] = prefix[i] + nums[i];            //@fill
            }
            return prefix;                                      //@ret
        }

        long long rangeSum(const vector<long long>& prefix, int l, int r) {
            return prefix[r + 1] - prefix[l];                   //@query
        }
    """,
    "c": """
        long long* buildPrefix(const int* nums, int n) {
            long long* prefix = malloc((n + 1) * sizeof(long long));  //@make
            prefix[0] = 0;                                      //@make
            for (int i = 0; i < n; i++) {                       //@fill
                prefix[i + 1] = prefix[i] + nums[i];            //@fill
            }
            return prefix;                                      //@ret
        }

        long long rangeSum(const long long* prefix, int l, int r) {
            return prefix[r + 1] - prefix[l];                   //@query
        }
    """,
}
RANGE_RUN = {
    "python": """
        rain = [3, 0, 5, 2, 7, 1, 4]
        p = build_prefix(rain)
        print(*p)
        for l, r in [(1, 3), (0, 6), (4, 4), (2, 5)]:
            print(range_sum(p, l, r))
    """,
    "java": """
        public static void main(String[] args) {
            long[] p = buildPrefix(new int[] {3, 0, 5, 2, 7, 1, 4});
            StringBuilder sb = new StringBuilder();
            for (long v : p) sb.append(sb.length() > 0 ? " " : "").append(v);
            System.out.println(sb);
            int[][] qs = {{1, 3}, {0, 6}, {4, 4}, {2, 5}};
            for (int[] q : qs) System.out.println(rangeSum(p, q[0], q[1]));
        }
    """,
    "cpp": """
        int main() {
            auto p = buildPrefix({3, 0, 5, 2, 7, 1, 4});
            for (size_t i = 0; i < p.size(); i++) cout << (i ? " " : "") << p[i];
            cout << "\\n";
            for (auto [l, r] : vector<pair<int, int>>{{1, 3}, {0, 6}, {4, 4}, {2, 5}}) cout << rangeSum(p, l, r) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int rain[] = {3, 0, 5, 2, 7, 1, 4}, qs[][2] = {{1, 3}, {0, 6}, {4, 4}, {2, 5}};
            long long* p = buildPrefix(rain, 7);
            for (int i = 0; i <= 7; i++) printf(i ? " %lld" : "%lld", p[i]);
            printf("\\n");
            for (int k = 0; k < 4; k++) printf("%lld\\n", rangeSum(p, qs[k][0], qs[k][1]));
            free(p);
            return 0;
        }
    """,
}

LONGEST = {
    "python": """
        def longest_with_sum(nums, k):
            first = {0: -1}                         #@seed
            prefix = 0                              #@seed
            best = 0                                #@seed
            for j, x in enumerate(nums):            #@loop
                prefix += x                         #@run
                if prefix - k in first:             #@look
                    best = max(best, j - first[prefix - k])     #@look
                if prefix not in first:             #@keep
                    first[prefix] = j               #@keep
            return best                             #@ret
    """,
    "java": """
        static int longestWithSum(int[] nums, long k) {
            Map<Long, Integer> first = new HashMap<>();         //@seed
            first.put(0L, -1);                                  //@seed
            long prefix = 0;                                    //@seed
            int best = 0;                                       //@seed
            for (int j = 0; j < nums.length; j++) {             //@loop
                prefix += nums[j];                              //@run
                Integer i = first.get(prefix - k);              //@look
                if (i != null) best = Math.max(best, j - i);    //@look
                first.putIfAbsent(prefix, j);                   //@keep
            }
            return best;                                        //@ret
        }
    """,
    "cpp": """
        int longestWithSum(const vector<int>& nums, long long k) {
            unordered_map<long long, int> first{{0, -1}};       //@seed
            long long prefix = 0;                               //@seed
            int best = 0;                                       //@seed
            for (int j = 0; j < (int)nums.size(); j++) {        //@loop
                prefix += nums[j];                              //@run
                auto it = first.find(prefix - k);               //@look
                if (it != first.end()) best = max(best, j - it->second);  //@look
                first.emplace(prefix, j);                       //@keep
            }
            return best;                                        //@ret
        }
    """,
    "c": """
        typedef struct {
            long long* keys;
            int* idx;
            bool* used;
            size_t mask;
        } FirstMap;                                                         //@table

        static size_t fm_slot(const FirstMap* m, long long key) {
            size_t i = (size_t)(((uint64_t)key * 0x9E3779B97F4A7C15ull) >> 32) & m->mask;  //@table
            while (m->used[i] && m->keys[i] != key) i = (i + 1) & m->mask;  //@table
            return i;
        }

        static void fm_keep(FirstMap* m, long long key, int j) {
            size_t i = fm_slot(m, key);                                     //@keep
            if (!m->used[i]) {                                              //@keep
                m->used[i] = true;                                          //@keep
                m->keys[i] = key;                                           //@keep
                m->idx[i] = j;                                              //@keep
            }
        }

        int longestWithSum(const int* nums, int n, long long k) {
            size_t cap = 16;                                                //@seed
            while (cap < 2 * ((size_t)n + 1)) cap <<= 1;                    //@seed
            FirstMap first = {malloc(cap * sizeof(long long)), malloc(cap * sizeof(int)), calloc(cap, sizeof(bool)), cap - 1};  //@seed
            fm_keep(&first, 0, -1);                                         //@seed
            long long prefix = 0;                                           //@seed
            int best = 0;                                                   //@seed
            for (int j = 0; j < n; j++) {                                   //@loop
                prefix += nums[j];                                          //@run
                size_t i = fm_slot(&first, prefix - k);                     //@look
                if (first.used[i] && j - first.idx[i] > best) best = j - first.idx[i];  //@look
                fm_keep(&first, prefix, j);                                 //@keep
            }
            free(first.keys); free(first.idx); free(first.used);            //@free
            return best;                                                    //@ret
        }
    """,
}
LONGEST_RUN = {
    "python": """
        print(longest_with_sum([2, -1, 3, 1, -2, 4], 4))
        print(longest_with_sum([5, -5, 5, -5], 0))
        print(longest_with_sum([1, 2], 7))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(longestWithSum(new int[] {2, -1, 3, 1, -2, 4}, 4));
            System.out.println(longestWithSum(new int[] {5, -5, 5, -5}, 0));
            System.out.println(longestWithSum(new int[] {1, 2}, 7));
        }
    """,
    "cpp": """
        int main() {
            cout << longestWithSum({2, -1, 3, 1, -2, 4}, 4) << "\\n" << longestWithSum({5, -5, 5, -5}, 0) << "\\n" << longestWithSum({1, 2}, 7) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {2, -1, 3, 1, -2, 4}, b[] = {5, -5, 5, -5}, c[] = {1, 2};
            printf("%d\\n%d\\n%d\\n", longestWithSum(a, 6, 4), longestWithSum(b, 4, 0), longestWithSum(c, 2, 7));
            return 0;
        }
    """,
}

GRID = {
    "python": """
        def build_2d(grid):
            rows, cols = len(grid), len(grid[0])                #@make
            P = [[0] * (cols + 1) for _ in range(rows + 1)]     #@make
            for r in range(rows):                               #@fill
                for c in range(cols):                           #@fill
                    P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]  #@cell
            return P                                            #@ret

        def rect_sum(P, r1, c1, r2, c2):
            return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]  #@query
    """,
    "java": """
        static long[][] build2d(int[][] grid) {
            int rows = grid.length, cols = grid[0].length;              //@make
            long[][] P = new long[rows + 1][cols + 1];                  //@make
            for (int r = 0; r < rows; r++) {                            //@fill
                for (int c = 0; c < cols; c++) {                        //@fill
                    P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c];  //@cell
                }
            }
            return P;                                                   //@ret
        }

        static long rectSum(long[][] P, int r1, int c1, int r2, int c2) {
            return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1];  //@query
        }
    """,
    "cpp": """
        vector<vector<long long>> build2d(const vector<vector<int>>& grid) {
            size_t rows = grid.size(), cols = grid[0].size();           //@make
            vector<vector<long long>> P(rows + 1, vector<long long>(cols + 1, 0));  //@make
            for (size_t r = 0; r < rows; r++) {                         //@fill
                for (size_t c = 0; c < cols; c++) {                     //@fill
                    P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c];  //@cell
                }
            }
            return P;                                                   //@ret
        }

        long long rectSum(const vector<vector<long long>>& P, int r1, int c1, int r2, int c2) {
            return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1];  //@query
        }
    """,
    "c": """
        // P is (rows + 1) x (cols + 1), stored row by row: P[r][c] lives at P[r * (cols + 1) + c].
        long long* build2d(const int* grid, int rows, int cols) {
            int w = cols + 1;                                           //@make
            long long* P = calloc((size_t)(rows + 1) * w, sizeof(long long));  //@make
            for (int r = 0; r < rows; r++) {                            //@fill
                for (int c = 0; c < cols; c++) {                        //@fill
                    P[(r + 1) * w + c + 1] = grid[r * cols + c] + P[r * w + c + 1] + P[(r + 1) * w + c] - P[r * w + c];  //@cell
                }
            }
            return P;                                                   //@ret
        }

        long long rectSum(const long long* P, int cols, int r1, int c1, int r2, int c2) {
            int w = cols + 1;                                           //@query
            return P[(r2 + 1) * w + c2 + 1] - P[r1 * w + c2 + 1] - P[(r2 + 1) * w + c1] + P[r1 * w + c1];  //@query
        }
    """,
}
GRID_RUN = {
    "python": """
        g = [[2, 0, 1, 3], [4, 1, 0, 2], [1, 5, 2, 1]]
        P = build_2d(g)
        for q in [(0, 0, 2, 3), (1, 1, 2, 2), (0, 2, 1, 3), (2, 0, 2, 0)]:
            print(rect_sum(P, *q))
    """,
    "java": """
        public static void main(String[] args) {
            long[][] P = build2d(new int[][] {{2, 0, 1, 3}, {4, 1, 0, 2}, {1, 5, 2, 1}});
            int[][] qs = {{0, 0, 2, 3}, {1, 1, 2, 2}, {0, 2, 1, 3}, {2, 0, 2, 0}};
            for (int[] q : qs) System.out.println(rectSum(P, q[0], q[1], q[2], q[3]));
        }
    """,
    "cpp": """
        int main() {
            auto P = build2d({{2, 0, 1, 3}, {4, 1, 0, 2}, {1, 5, 2, 1}});
            int qs[4][4] = {{0, 0, 2, 3}, {1, 1, 2, 2}, {0, 2, 1, 3}, {2, 0, 2, 0}};
            for (auto& q : qs) cout << rectSum(P, q[0], q[1], q[2], q[3]) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int g[] = {2, 0, 1, 3, 4, 1, 0, 2, 1, 5, 2, 1};
            int qs[4][4] = {{0, 0, 2, 3}, {1, 1, 2, 2}, {0, 2, 1, 3}, {2, 0, 2, 0}};
            long long* P = build2d(g, 3, 4);
            for (int k = 0; k < 4; k++) printf("%lld\\n", rectSum(P, 4, qs[k][0], qs[k][1], qs[k][2], qs[k][3]));
            free(P);
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

build_prefix = py(RANGE["python"], "build_prefix")
range_sum = py(RANGE["python"], "range_sum")
longest_with_sum = py(LONGEST["python"], "longest_with_sum")
build_2d = py(GRID["python"], "build_2d")
rect_sum = py(GRID["python"], "rect_sum")

RAIN = [3, 0, 5, 2, 7, 1, 4]
P = build_prefix(RAIN)
QL, QR = 1, 3
QS = range_sum(P, QL, QR)
assert QS == sum(RAIN[QL:QR + 1])
QUERIES = [(1, 3), (0, 6), (4, 4), (2, 5)]
q_rows = [(f"[{l}, {r}]", f"P[{r + 1}] - P[{l}] = {P[r + 1]} - {P[l]}", str(range_sum(P, l, r))) for l, r in QUERIES]
for l, r in QUERIES:
    assert range_sum(P, l, r) == sum(RAIN[l:r + 1])

build = Steps(f"Building `P` for `{RAIN}`, then answering the question \"total from day {QL} to day {QR}\".")
build.step("P has one more slot than the input. P[0] = 0: the sum of no elements.", Row(RAIN, slots=True, label="nums"),
           Row([0] + [None] * len(RAIN), st={0: "new"}, slots=True, label="P"))
for i, x in enumerate(RAIN):
    cells = P[:i + 2] + [None] * (len(RAIN) - i - 1)
    build.step(f"P[{i + 1}] = P[{i}] + nums[{i}] = {P[i]} + {x} = {P[i + 1]}: the total of the first {i + 1} element{'s' if i else ''}.",
               Row(RAIN, st={j: ("active" if j == i else "dim") for j in range(i + 1)}, ptr={"i": i}, slots=True, label="nums"),
               Row(cells, st={i + 1: "new", i: "found"}, slots=True, label="P"))
build.step(f"Sum of nums[{QL}..{QR}]: everything up to day {QR} is P[{QR + 1}] = {P[QR + 1]}; the part before day {QL} is P[{QL}] = {P[QL]}. "
           f"Subtract: {P[QR + 1]} - {P[QL]} = {QS}.",
           Row(RAIN, st={j: "answer" for j in range(QL, QR + 1)}, ptr={"l": QL, "r": QR}, slots=True, label="nums"),
           Row(P, st={QR + 1: "found", QL: "mark"}, slots=True, label="P"), result=QS)

LD, LK = [2, -1, 3, 1, -2, 4], 4
LANS = longest_with_sum(LD, LK)
assert LANS == max((j - i + 1 for i in range(len(LD)) for j in range(i, len(LD)) if sum(LD[i:j + 1]) == LK), default=0)
l_rows = []
first, pre, best = {0: -1}, 0, 0
for j, x in enumerate(LD):
    pre += x
    hit = first.get(pre - LK)
    note = "—"
    if hit is not None:
        cand = j - hit
        note = f"stretch {hit + 1}..{j}, length {cand}"
        best = max(best, cand)
    kept = "keep" if pre not in first else "already there"
    first.setdefault(pre, j)
    l_rows.append((str(j), str(x), str(pre), str(pre - LK), note, str(best), kept))
assert best == LANS

G = [[2, 0, 1, 3], [4, 1, 0, 2], [1, 5, 2, 1]]
GP = build_2d(G)
R1, C1, R2, C2 = 1, 1, 2, 2
GS = rect_sum(GP, R1, C1, R2, C2)
assert GS == sum(G[r][c] for r in range(R1, R2 + 1) for c in range(C1, C2 + 1))

# Counting stretches with a given sum: the {0: 1} seed, shown on a small case.
CD, CK = [1, 2, 1, 3, -3, 3], 3
c_rows, cnt, pre, tot = [], {0: 1}, 0, 0
for j, x in enumerate(CD):
    pre += x
    add = cnt.get(pre - CK, 0)
    tot += add
    c_rows.append((str(j), str(x), str(pre), str(pre - CK), str(add), str(tot)))
    cnt[pre] = cnt.get(pre, 0) + 1
assert tot == sum(1 for i in range(len(CD)) for j in range(i, len(CD)) if sum(CD[i:j + 1]) == CK)

N = 10**5
lesson(
    "arrays-hashing",
    "prefix-sums",
    """
    Precompute running totals once, and the sum of any stretch of the array becomes one subtraction. Combined with a
    hash map, the same idea counts or finds stretches with a given sum, negatives included, in a single pass.
    """,
    [
        ("idea", "The idea", [
            """
            A car's odometer shows the total distance driven since the car was new. Nobody resets it at every town.
            Still, to know how far it is from town A to town B, you just subtract: reading at B minus reading at A.

            A **prefix sum** array is an odometer for an array. `P[i]` is the total of the first `i` elements:

            - `P[0] = 0` (nothing added yet),
            - `P[i + 1] = P[i] + nums[i]`.

            Then the sum of any stretch `nums[l..r]` (inclusive) is a difference of two readings:

            `sum(nums[l..r]) = P[r + 1] - P[l]`
            """,
            fig(Row(RAIN, st={j: "answer" for j in range(QL, QR + 1)}, ptr={"l": QL, "r": QR}, slots=True, label="nums"),
                Row(P, st={QR + 1: "found", QL: "mark"}, slots=True, label="P"),
                caption=f"Total of `nums[{QL}..{QR}]` = `P[{QR + 1}] - P[{QL}]` = {P[QR + 1]} - {P[QL]} = {QS}. "
                        f"One subtraction, however long the stretch."),
            key("""
            Pay O(n) once to build `P`; afterwards every range sum is O(1): `P[r + 1] - P[l]`. And "some stretch sums to
            `k`" becomes "two prefix values differ by `k`", which is a complement lookup.
            """),
        ]),
        ("signals", "When to reach for it", [
            table(
                ["The problem says…", "What prefix sums give you"],
                ["many questions \"sum / count from `l` to `r`\" on a fixed array", "each answer in O(1) after O(n) setup"],
                ["count (or find longest / shortest) **subarrays** with sum `k`", "`P[j] - P[i] = k`: look up `P[j] - k` in a map"],
                ["balance point, left total equals right total", "left = `P[i]`, right = `total - P[i + 1]`"],
                ["equal number of 0s and 1s, of A and B", "map one to `-1`, the other to `+1`; look for sum 0"],
                ["subarray sum divisible by `k`", "equal remainders `P[j] % k == P[i] % k`"],
                ["running balance, cumulative totals", "`P` itself is the answer"],
                ["sum over a rectangle of a grid, many times", "2D prefix sums, O(1) per rectangle"],
            ),
            """
            **The key phrase is "contiguous".** Prefix sums answer questions about *stretches* (subarrays,
            consecutive days, ranges of indices), never about arbitrary subsets.

            **When it is the wrong tool**

            - **The array changes between questions.** One update can change `n` prefix values. Use a Fenwick tree or
              segment tree (O(log n) per update and query).
            - **Max, min or gcd of a range.** These can't be "subtracted": knowing the max of `[0..r]` and of `[0..l-1]`
              doesn't give the max of `[l..r]`. Use a sparse table or segment tree.
            - **All values are positive and you need a window.** A sliding window with two pointers is often simpler
              and uses O(1) memory. Prefix sums with a hash map are the tool when values can be **negative**, which
              breaks the window's "growing it only increases the sum" logic.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Telescoping

            By definition `P[i] = nums[0] + nums[1] + … + nums[i - 1]`. Write out `P[r + 1] - P[l]`:

            `(nums[0] + … + nums[l - 1] + nums[l] + … + nums[r]) - (nums[0] + … + nums[l - 1])`

            The first `l` terms cancel, leaving exactly `nums[l] + … + nums[r]`. That cancellation (each term appears once
            with `+` and once with `-`) is called **telescoping**, and it's the whole proof.

            ### Why `P` has `n + 1` entries

            `P[i]` is the sum of the first `i` elements, so `i` runs from 0 to `n`. The extra `P[0] = 0` means a stretch
            that starts at index 0 needs no special case: `sum(nums[0..r]) = P[r + 1] - P[0]`. Think of `P[i]` as sitting
            on the **boundary** before index `i`; a stretch `[l, r]` runs from boundary `l` to boundary `r + 1`.

            ### Stretches with a given sum

            A stretch `nums[i..j-1]` sums to `k` exactly when `P[j] - P[i] = k`, that is when

            `P[i] = P[j] - k`

            So: walk `j` from left to right, keep a running prefix, and ask a hash map about **earlier** prefix values.
            That's complement lookup, applied to prefix values instead of array values. The same invariant applies: the
            map holds only boundaries before `j`, so each stretch is found once, at its right end.

            What the map stores depends on the question:

            - **count** the stretches: prefix value → how many times seen; seed it with `{0: 1}` (the empty prefix
              `P[0]`), so stretches that start at index 0 are counted;
            - **longest** stretch: prefix value → **first** index where it occurred; seed with `{0: -1}`, keep only the
              first occurrence, length `j - first[P[j] - k]`;
            - **shortest** stretch: prefix value → **latest** index (overwrite on every occurrence).

            Here is the counting version on `{CD}`, `k = {CK}`. The table is seeded with `0 → 1`:
            """.replace("{CD}", str(CD)).replace("{CK}", str(CK)),
            table(["j", "x", "prefix", "need prefix - k", "earlier prefixes equal to it", "stretches so far"], *c_rows),
            f"""
            Every row adds the number of earlier boundaries that close a stretch summing to {CK} at `j`. Total:
            **{tot}**, which matches checking all {len(CD) * (len(CD) + 1) // 2} stretches one by one.

            ### Why negatives are fine here (and not for sliding windows)

            A sliding window grows on the right and shrinks on the left, relying on "adding an element increases the sum".
            With negative numbers that's false, and the window gets stuck. Prefix sums make no such assumption: the
            identity `P[r + 1] - P[l]` holds for any integers, and the hash map finds matching boundaries wherever they
            are.

            ### Remainders: divisible by `k`

            `sum(nums[i..j-1])` is divisible by `k` exactly when `P[j]` and `P[i]` leave the **same remainder** mod `k`
            (their difference is a multiple of `k`). Count remainders instead of prefix values; the map has at most `k`
            keys. Normalise negative remainders with `((p % k) + k) % k`.

            ### Beyond sums

            The trick works for any operation you can **undo**: XOR (`X[r + 1] ^ X[l]`, since XOR undoes itself),
            counts of a category (a prefix count of vowels), products when no element is 0. It does **not** work for
            max, min or gcd, which can't be undone.

            ### Two dimensions

            For a grid, let `P[r][c]` be the sum of the rectangle from `(0, 0)` to `(r - 1, c - 1)`. By
            **inclusion–exclusion**:

            - building: `P[r+1][c+1] = grid[r][c] + P[r][c+1] + P[r+1][c] - P[r][c]` (the top-left part was added twice);
            - querying rows `r1..r2`, columns `c1..c2`:
              `P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]` (the top-left part was subtracted twice).
            """,
        ]),
        ("template", "The template", [
            """
            Build the prefix array once, then answer each range question with one subtraction. The example: daily
            rainfall, and questions "how much rain fell from day `l` to day `r`?".
            """,
            code(
                "Prefix array and range sums",
                RANGE,
                [
                    ("make", "One more slot than the input; `P[0] = 0` is the sum of nothing. Totals are 64-bit: "
                             "10⁵ values of 10⁹ add up to 10¹⁴.",
                     {"c": "`malloc` doesn't zero memory, so `P[0]` is set explicitly."}),
                    ("fill", "Each prefix is the previous one plus one element: O(1) per entry, O(n) in total."),
                    ("ret", "The prefix array, `n + 1` entries."),
                    ("query", "Everything up to and including `r`, minus everything before `l`. The `+ 1` turns the "
                              "inclusive `r` into the boundary after it."),
                ],
                RANGE_RUN,
                "build_prefix([3, 0, 5, 2, 7, 1, 4]); range_sum for [1, 3], [0, 6], [4, 4], [2, 5]",
            ),
            table(["query [l, r]", "computed as", "answer"], *q_rows),
        ]),
        ("trace", "Trace it by hand", [
            walk(build),
            """
            ### A prefix walk with a hash map

            Find the length of the longest stretch with sum exactly `k`. Values can be negative, so a sliding window
            won't work. For each `j`, the best stretch ending at `j` starts right after the **earliest** boundary `i`
            with `P[i] = P[j] - k`: so remember the first index of every prefix value.
            """,
            code(
                "Longest stretch with a given sum",
                LONGEST,
                [
                    ("seed", "The empty prefix (sum 0) sits at boundary `-1`, before the first element, so a stretch "
                             "starting at index 0 is found too. `best = 0` means \"none found yet\"."),
                    ("loop", "`j` is the right end of the stretches we look for."),
                    ("run", "`prefix` is the sum of `nums[0..j]`. Keep it 64-bit."),
                    ("look", "If some earlier boundary has prefix `prefix - k`, the stretch after it up to `j` sums to "
                             "`k`. Its first occurrence gives the longest such stretch ending at `j`.",
                     {"cpp": "`find` doesn't insert."}),
                    ("keep", "Record the prefix only the first time it appears. A later boundary with the same value "
                             "would only give shorter stretches."),
                    ("ret", "The longest length over all right ends, or 0."),
                    ("table", "An open-addressing table on 64-bit prefix values, storing the first index of each."),
                    ("free", "Release the table."),
                ],
                LONGEST_RUN,
                "longest_with_sum([2, -1, 3, 1, -2, 4], 4); longest_with_sum([5, -5, 5, -5], 0); longest_with_sum([1, 2], 7)",
            ),
            f"For `{LD}` with `k = {LK}` (the map starts as `0 → -1`):",
            table(["j", "x", "prefix", "need", "stretch found", "best", "map"], *l_rows),
            f"""
            The answer is {LANS}. Notice the row where the prefix value repeats: the map keeps the **older** index, which
            is exactly what makes stretches long.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Two dimensions

            Sums of rectangles in a grid, many times over. Build `P` with one extra row and column of zeros, then use
            inclusion–exclusion.
            """,
            code(
                "2D prefix sums",
                GRID,
                [
                    ("make", "An `(rows + 1) × (cols + 1)` table of zeros. Row 0 and column 0 stay 0, like `P[0]` in 1D.",
                     {"c": "One flat block of memory, indexed `r * (cols + 1) + c`; `calloc` zeroes it."}),
                    ("fill", "Fill row by row, so the three neighbours a cell needs are already done."),
                    ("cell", "This cell, plus the rectangle above, plus the rectangle to the left, minus their overlap "
                             "(the top-left rectangle, added twice)."),
                    ("ret", "The table."),
                    ("query", "The big rectangle down to `(r2, c2)`, minus the strip above row `r1`, minus the strip left "
                              "of column `c1`, plus the corner that both strips removed."),
                ],
                GRID_RUN,
                "rect_sum on [[2, 0, 1, 3], [4, 1, 0, 2], [1, 5, 2, 1]] for (0,0)-(2,3), (1,1)-(2,2), (0,2)-(1,3), (2,0)-(2,0)",
            ),
            fig(Grid(G, st={(r, c): "answer" for r in range(R1, R2 + 1) for c in range(C1, C2 + 1)}, label="grid"),
                Grid(GP, st={(R2 + 1, C2 + 1): "found", (R1, C2 + 1): "mark", (R2 + 1, C1): "mark", (R1, C1): "found"}, label="P"),
                caption=f"Rows {R1}–{R2}, columns {C1}–{C2}: "
                        f"{GP[R2 + 1][C2 + 1]} - {GP[R1][C2 + 1]} - {GP[R2 + 1][C1]} + {GP[R1][C1]} = {GS}."),
            """
            ### Counting stretches with sum `k`

            Same loop as *longest*, but the map holds **counts** of each prefix value, seeded with `{0: 1}`, and each
            step adds `count[prefix - k]` before incrementing `count[prefix]` (the table in *Why it works* traces it).

            ### Equal numbers of two kinds

            "Longest stretch with as many A's as B's": replace A with `+1` and B with `-1`. Equal counts means sum 0, so
            it's *longest with sum 0*. Rewriting the input so a condition becomes a sum is a very common move.

            ### Balance points

            With the total `T` known, the sum left of `i` is `P[i]` and the sum right of `i` is `T - P[i + 1]`. You don't
            even need the array: keep a running left sum while scanning.

            ### Prefix of anything you can undo

            - **XOR:** `X[r + 1] ^ X[l]` is the XOR of a range; "stretches with XOR `k`" looks up `X[j] ^ k`.
            - **Counts per category:** 26 prefix arrays (one per letter) answer "how many `e`s in `s[l..r]`?" in O(1).
            - **Prefix maximum** is still useful, but only for prefixes: "the best so far" (it can't answer ranges).

            ### The inverse: difference arrays

            Prefix sums turn an array into running totals. The opposite operation, differences of neighbours, turns
            "add `v` to a whole range" into two point changes. That's the next pattern, *Difference arrays*.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            - **Building:** O(n) time, O(n) space for `P` (O(rows · cols) in 2D).
            - **Each range query:** O(1).
            - **Stretch search with a hash map:** O(n) expected time, O(n) space for the map.

            **Compared with summing each range directly:** `q` queries over ranges of length up to `n` cost O(q · n).
            With `n = q = 10⁵` that's up to {N * N:,} additions, versus {2 * N:,} with prefix sums. For "count the
            stretches with sum `k`", the brute force checks all n(n + 1)/2 stretches; the prefix + map version does one
            lookup per element.
            """,
            table(
                ["Task", "Direct", "With prefix sums"],
                ["q range sums", "O(q · n)", "O(n + q)"],
                ["count stretches with sum k", "O(n²) (running sums)", "O(n) expected"],
                ["longest stretch with sum k", "O(n²)", "O(n) expected"],
                ["q rectangle sums in an R × C grid", "O(q · R · C)", "O(R · C + q)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            **Python:** `itertools.accumulate(nums, initial=0)` builds `P` in one call (Python 3.8+). Integers never
            overflow. For the stretch search, `dict.get(prefix - k, 0)` and `setdefault(prefix, j)` (keeps the first).

            **Java:** use `long[]` for `P`: an `int` prefix overflows past about 2.1 · 10⁹. A `Map<Long, Integer>` key must
            be a `Long`: `first.put(0L, -1)` with the `L`, since `0` alone would box to an `Integer`, a different key.

            **C++:** `std::partial_sum` exists, but writing the loop with an explicit `P[0] = 0` is clearer. Use
            `long long`. `unordered_map<long long, int>` with `emplace` (keeps the first) and `find` (no insertion).

            **C:** `long long` prefixes; for 2D, one flat `calloc` block indexed `r * (cols + 1) + c`. The hash map for
            stretch problems is the same open-addressing table as before, on 64-bit keys.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - **Off by one.** `sum(l..r)` inclusive is `P[r + 1] - P[l]`, not `P[r] - P[l]`. Draw the boundaries if in
              doubt.
            - **Forgetting the seed.** Without `{0: 1}` (count) or `{0: -1}` (longest), stretches that start at index 0
              are missed.
            - **First vs last index.** For the longest stretch keep the first occurrence; overwriting gives shorter ones.
            - **Overflow.** Sums of many large values need 64 bits, in `P` and in the running prefix.
            - **Negative remainders.** In Java, C and C++, `-1 % 5 == -1`. Normalise before using a remainder as a key.
            - **Using a sliding window with negatives.** Shrinking the window no longer reduces the sum; use prefix sums
              with a map instead.
            - **Trying to "subtract" maxima.** Range max/min need other structures.
            - **2D inclusion–exclusion signs.** Build: `+ above + left - corner`. Query: `- above - left + corner`.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("With `P` built from `nums`, what is the sum of `nums[2..5]`?",
                 "`P[6] - P[2]`: everything before boundary 6 (indices 0–5) minus everything before boundary 2 (indices 0–1)."),
                ("Why does counting stretches with sum `k` seed the map with `{0: 1}`?",
                 "`P[0] = 0` is the boundary before the first element. A stretch starting at index 0 ending at `j` sums to `k` exactly when `P[j + 1] - 0 = k`; without the seed, the lookup for `0` would miss it."),
                ("Values can be negative. Why does a sliding window fail for \"longest stretch with sum k\", while prefix sums work?",
                 "The window shrinks when the sum is too big, assuming that removing elements lowers the sum. Negative values break that. Prefix sums rely only on `P[r + 1] - P[l]`, which holds for any integers."),
                ("Can you answer \"maximum of `nums[l..r]`\" with prefix maxima?",
                 "No. The max of `[0..r]` might sit before `l`, and there's no way to subtract it out. Max isn't invertible; use a sparse table or segment tree."),
                ("Longest stretch with equally many 0s and 1s: how do you turn it into a prefix-sum problem?",
                 "Replace each 0 with -1. A stretch has equal counts exactly when its sum is 0, i.e. two boundaries with the same prefix value. Keep the first index of each prefix value."),
            ),
        ]),
    ],
)
