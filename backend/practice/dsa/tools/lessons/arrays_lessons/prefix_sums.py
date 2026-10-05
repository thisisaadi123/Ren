"""Lesson: Prefix sums (Arrays & Hashing, pattern 4)."""
from lesson import Bars, Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

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
TOP = P[-1]

build = Steps(f"Building `P` for `{RAIN}`, then using it to answer \"how much rain from day {QL} to day {QR}?\".")
build.step("P has one more slot than the input. P[0] = 0, because before day 0 no rain has fallen.",
           Row(RAIN, slots=True, label="rain"), Bars([0] + [None] * len(RAIN), st={0: "new"}, label="P", top=TOP))
for i, x in enumerate(RAIN):
    cells = P[:i + 2] + [None] * (len(RAIN) - i - 1)
    build.step(f"P[{i + 1}] = P[{i}] + rain[{i}] = {P[i]} + {x} = {P[i + 1]}. That's all the rain up to the end of day {i}.",
               Row(RAIN, st={j: ("active" if j == i else "dim") for j in range(i + 1)}, ptr={"i": i}, slots=True, label="rain"),
               Bars(cells, st={i + 1: "new"}, label="P", top=TOP))
build.step(f"Days {QL} to {QR}: all the rain up to the end of day {QR} is P[{QR + 1}] = {P[QR + 1]}, and the rain before day {QL} is P[{QL}] = {P[QL]}. "
           f"Subtract and you get {P[QR + 1]} - {P[QL]} = {QS}.",
           Row(RAIN, st={j: "answer" for j in range(QL, QR + 1)}, ptr={"l": QL, "r": QR}, slots=True, label="rain"),
           Bars(P, st={QR + 1: "answer", QL: "mark"}, label="P", top=TOP), result=QS)

# Longest stretch with sum k, as a walkthrough.
LD, LK = [2, -1, 3, 1, -2, 4], 4
LANS = longest_with_sum(LD, LK)
assert LANS == max((j - i + 1 for i in range(len(LD)) for j in range(i, len(LD)) if sum(LD[i:j + 1]) == LK), default=0)
lwalk = Steps(f"`longest_with_sum({LD}, {LK})`. The map remembers the first index where each running total showed up.")
first, pre, best = {0: -1}, 0, 0
lwalk.step("Before we start, the running total is 0, and we pretend it was reached at index -1 (just before the array).",
           Row(LD, slots=True), M({f"{k}": f"index {v}" for k, v in first.items()}, "first time each total appeared"), M({"best": 0}))
l_rows = []
for j, x in enumerate(LD):
    pre += x
    hit = first.get(pre - LK)
    st = {j: "active"}
    if hit is not None:
        cand = j - hit
        best = max(best, cand)
        for t in range(hit + 1, j + 1):
            st[t] = "answer"
        msg = f"Running total {pre}. We want an earlier total of {pre} - {LK} = {pre - LK}, and it first appeared at index {hit}. So indices {hit + 1}..{j} add up to {LK}: length {cand}."
        note = f"{hit + 1}..{j}, length {cand}"
    else:
        msg = f"Running total {pre}. We'd need an earlier total of {pre - LK}; there isn't one."
        note = "none"
    if pre not in first:
        first[pre] = j
        msg += f" {pre} is new, so remember index {j}."
        kept = "keep"
    else:
        msg += f" {pre} was already seen at index {first[pre]}; keep the older index."
        kept = "already there"
    lwalk.step(msg, Row(LD, st=st, ptr={"j": j}, slots=True), M({f"{k}": f"index {v}" for k, v in first.items()}, "first time each total appeared"), M({"best": best}))
    l_rows.append((str(j), str(x), str(pre), str(pre - LK), note, str(best), kept))
assert best == LANS

G = [[2, 0, 1, 3], [4, 1, 0, 2], [1, 5, 2, 1]]
GP = build_2d(G)
R1, C1, R2, C2 = 1, 1, 2, 2
GS = rect_sum(GP, R1, C1, R2, C2)
assert GS == sum(G[r][c] for r in range(R1, R2 + 1) for c in range(C1, C2 + 1))


def region(r_hi, c_hi, state):
    return {(r, c): state for r in range(r_hi + 1) for c in range(c_hi + 1)}


q2 = Steps(f"Sum of rows {R1} to {R2}, columns {C1} to {C2}, using four values from P.")
big, top, left, corner = GP[R2 + 1][C2 + 1], GP[R1][C2 + 1], GP[R2 + 1][C1], GP[R1][C1]
q2.step(f"Start with everything from the top-left corner down to ({R2}, {C2}): P[{R2 + 1}][{C2 + 1}] = {big}.",
        Grid(G, st=region(R2, C2, "found")))
q2.step(f"Take away the rows above row {R1}: P[{R1}][{C2 + 1}] = {top}. That leaves {big - top}.",
        Grid(G, st={**region(R2, C2, "found"), **region(R1 - 1, C2, "dim")}))
q2.step(f"Take away the columns left of column {C1}: P[{R2 + 1}][{C1}] = {left}. But the top-left corner has now been taken away twice.",
        Grid(G, st={**region(R2, C2, "found"), **region(R1 - 1, C2, "dim"), **region(R2, C1 - 1, "dim"), **region(R1 - 1, C1 - 1, "mark")}))
q2.step(f"So add the corner back once: P[{R1}][{C1}] = {corner}. {big} - {top} - {left} + {corner} = {GS}.",
        Grid(G, st={**{(r, c): "answer" for r in range(R1, R2 + 1) for c in range(C1, C2 + 1)}}), result=GS)

# Counting stretches with sum k: the {0: 1} seed, as a table and a walkthrough.
CD, CK = [1, 2, 1, 3, -3, 3], 3
c_rows, cnt, pre, tot = [], {0: 1}, 0, 0
cwalk = Steps(f"Counting stretches of `{CD}` that add up to {CK}. The map counts how often each running total has appeared.")
cwalk.step("The empty prefix (total 0) has appeared once, before we start.", Row(CD, slots=True), M({k: v for k, v in cnt.items()}, "running total → times seen"), M({"stretches": 0}))
for j, x in enumerate(CD):
    pre += x
    add = cnt.get(pre - CK, 0)
    tot += add
    c_rows.append((str(j), str(x), str(pre), str(pre - CK), str(add), str(tot)))
    cnt[pre] = cnt.get(pre, 0) + 1
    cwalk.step(f"Running total {pre}. Earlier totals equal to {pre} - {CK} = {pre - CK}: {add}. " + (f"Each one starts a stretch ending here, so add {add}." if add else "Nothing ends here."),
               Row(CD, st={j: "active"}, ptr={"j": j}, slots=True), M({k: v for k, v in cnt.items()}, "running total → times seen"), M({"stretches": tot}))
assert tot == sum(1 for i in range(len(CD)) for j in range(i, len(CD)) if sum(CD[i:j + 1]) == CK)

# Example: balance point.
W = [2, 7, 1, 4, 5]
WT = sum(W)
w_rows, left_sum, BAL = [], 0, -1
for i, x in enumerate(W):
    right = WT - left_sum - x
    w_rows.append((str(i), str(x), str(left_sum), str(right), "balanced" if left_sum == right else ""))
    if left_sum == right and BAL < 0:
        BAL = i
    left_sum += x
assert BAL == 2

# Example: equal 0s and 1s through ±1.
BITS = [1, 1, 0, 1, 0, 0, 1, 1]
PM = [1 if b else -1 for b in BITS]
PP = [0]
for v in PM:
    PP.append(PP[-1] + v)
seen_at, BEST01, B01 = {}, 0, None
for i, v in enumerate(PP):
    if v in seen_at:
        if i - seen_at[v] > BEST01:
            BEST01, B01 = i - seen_at[v], (seen_at[v], i)
    else:
        seen_at[v] = i
assert BEST01 == max(j - i for i in range(len(PP)) for j in range(i, len(PP)) if PP[i] == PP[j])

N = 10**5
lesson(
    "arrays-hashing",
    "prefix-sums",
    """
    Work out the running totals once, and the sum of any stretch of the array becomes a single subtraction. Add a
    hash map, and the same idea finds or counts stretches with a given sum in one pass, even when some numbers are
    negative.
    """,
    [
        ("idea", "The idea", [
            """
            A car's odometer shows how far the car has gone since it was new. Nobody resets it in every town. But if
            you want to know how far it is from one town to the next, you just subtract: the reading when you arrive,
            minus the reading when you set off.

            A **prefix sum** array is an odometer for an array. `P[i]` is the total of the first `i` elements. `P[0]`
            is 0 (nothing added yet), and each next entry adds one more element: `P[i + 1] = P[i] + nums[i]`.

            Once you have that, the sum of any stretch `nums[l..r]` is just two readings subtracted:

            `sum of nums[l..r] = P[r + 1] - P[l]`
            """,
            fig(Bars(RAIN, label="daily rain"), Bars(P, st={QR + 1: "answer", QL: "mark"}, label="P: rain so far, like an odometer"),
                caption=f"The rain on days {QL} to {QR} is the reading after day {QR} ({P[QR + 1]}) minus the reading before day {QL} ({P[QL]}): {QS}. It doesn't matter how long the stretch is."),
            key("""
            Spend O(n) once building `P`, and every range sum after that costs O(1): `P[r + 1] - P[l]`. And "some
            stretch adds up to `k`" turns into "two running totals differ by `k`", which is a complement lookup.
            """),
        ]),
        ("signals", "When to reach for it", [
            table(
                ["The problem says…", "what prefix sums give you"],
                ["lots of questions like \"sum from `l` to `r`\" on an array that doesn't change", "each answer in O(1) after O(n) setup"],
                ["count (or find the longest / shortest) subarrays that add up to `k`", "`P[j] - P[i] = k`, so look up `P[j] - k` in a map"],
                ["a balance point where the left side equals the right side", "left = `P[i]`, right = `total - P[i + 1]`"],
                ["as many 0s as 1s, as many A's as B's", "turn one into `-1` and the other into `+1`, then look for a sum of 0"],
                ["subarray sum divisible by `k`", "two running totals with the same remainder"],
                ["running balance, cumulative totals", "`P` itself is the answer"],
                ["sums over rectangles in a grid, many times", "2D prefix sums, O(1) per rectangle"],
            ),
            """
            The word to look for is "contiguous" (or "subarray", "consecutive days", "a range of indices"). Prefix
            sums are about stretches, never about picking arbitrary elements.

            They're the wrong tool when the array keeps changing between questions, because one update can change
            every running total after it. A Fenwick tree or segment tree handles that in O(log n) per update. They also
            can't do max, min or gcd over a range, because you can't "subtract" a maximum. Knowing the biggest value in
            `[0..r]` and in `[0..l-1]` doesn't tell you the biggest in `[l..r]`.

            And if every value is positive and you need a window, a sliding window with two pointers is often simpler.
            Prefix sums plus a hash map are what you want when values can be negative, which is exactly when the
            sliding window's "make it bigger and the sum goes up" logic stops working.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Things cancel out

            `P[i]` is `nums[0] + nums[1] + … + nums[i - 1]`. Write out `P[r + 1] - P[l]` in full:

            `(nums[0] + … + nums[l - 1] + nums[l] + … + nums[r]) - (nums[0] + … + nums[l - 1])`

            The first `l` terms appear once with a plus and once with a minus, so they cancel, and you're left with
            exactly `nums[l] + … + nums[r]`. (This kind of cancelling is called **telescoping**, like a telescope
            folding up.)

            ### Why `P` has one extra slot

            `P[i]` is the sum of the first `i` elements, so `i` goes from 0 to `n`. That's `n + 1` values. The extra
            `P[0] = 0` means a stretch starting at index 0 doesn't need a special case: its sum is `P[r + 1] - P[0]`.
            It helps to picture `P[i]` sitting on the *gap* just before index `i`. A stretch `[l, r]` runs from gap `l`
            to gap `r + 1`.

            ### Finding stretches with a given sum

            A stretch `nums[i..j-1]` adds up to `k` exactly when `P[j] - P[i] = k`, which is the same as

            `P[i] = P[j] - k`

            So walk `j` from left to right, keep a running total, and ask a hash map whether an earlier running total
            equals `P[j] - k`. That's complement lookup again, just on running totals instead of on the values
            themselves. And the same reasoning applies: the map only holds totals from before `j`, so each stretch is
            found once, when you reach its end.

            What you keep in the map depends on the question. To count stretches, store how many times each total has
            appeared, and start the map with `{0: 1}` for the empty prefix, so stretches starting at index 0 get
            counted. For the longest stretch, store the *first* index where each total appeared (starting with
            `{0: -1}`). For the shortest, store the *latest* index.

            Here's the counting version, step by step:
            """,
            walk(cwalk),
            table(["j", "x", "running total", "looking for", "earlier matches", "stretches so far"], *c_rows),
            f"""
            Each step adds the number of earlier gaps that start a stretch summing to {CK} and ending at `j`. That gives
            {tot}, the same as checking all {len(CD) * (len(CD) + 1) // 2} stretches one by one.

            ### Why negative numbers are fine

            A sliding window grows on the right and shrinks on the left, and it relies on "adding an element makes the
            sum bigger". With negative numbers that's just not true, and the window gets stuck. Prefix sums don't
            assume anything like that. `P[r + 1] - P[l]` is true for any integers, and the hash map finds matching
            totals wherever they are.

            ### Divisible by `k`

            A stretch's sum is divisible by `k` exactly when the two running totals at its ends leave the same
            remainder when divided by `k` (their difference is then a multiple of `k`). So count remainders instead
            of totals. The map has at most `k` keys. Watch out for negative remainders and fix them with
            `((p % k) + k) % k`.

            ### Not just sums

            This works for anything you can undo. XOR undoes itself, so `X[r + 1] ^ X[l]` gives the XOR of a range.
            Prefix counts of a category ("how many vowels so far?") work the same way. Products work too, as long as
            there are no zeros. Max, min and gcd don't, because they can't be undone.

            ### Two dimensions

            For a grid, let `P[r][c]` be the sum of the rectangle from the top-left corner down to `(r - 1, c - 1)`.
            Building it: `P[r+1][c+1] = grid[r][c] + P[r][c+1] + P[r+1][c] - P[r][c]`. The bit above and the bit to the
            left both include the top-left block, so it gets added twice and you take it away once. Querying works the
            other way round. Here's a query, one step at a time:
            """,
            walk(q2),
        ]),
        ("template", "The template", [
            """
            Build the prefix array once, then answer each "how much from `l` to `r`?" with one subtraction. The
            example uses daily rainfall.
            """,
            code(
                "Prefix array and range sums",
                RANGE,
                [
                    ("make", "One more slot than the input, and `P[0] = 0`, the sum of nothing. The totals are 64-bit, "
                             "because 100,000 values of a billion each add up to 10¹⁴.",
                     {"c": "`malloc` doesn't zero memory, so we set `P[0]` ourselves."}),
                    ("fill", "Each entry is the one before plus one element. O(1) each, O(n) in total."),
                    ("ret", "The prefix array, with `n + 1` entries."),
                    ("query", "Everything up to and including `r`, minus everything before `l`. The `+ 1` is because "
                              "`r` is included, so we want the gap just after it."),
                ],
                RANGE_RUN,
                "build_prefix([3, 0, 5, 2, 7, 1, 4]); range_sum for [1, 3], [0, 6], [4, 4], [2, 5]",
            ),
            table(["question [l, r]", "worked out as", "answer"], *q_rows),
        ]),
        ("trace", "Trace it by hand", [
            "Watch `P` grow, one bar per day, and then answer a question with two of its bars:",
            walk(build),
            """
            ### Running totals plus a hash map

            Now something harder: the longest stretch that adds up to exactly `k`. Some values are negative, so a
            sliding window won't work. For each `j`, the longest stretch ending at `j` starts just after the
            *earliest* gap where the running total was `P[j] - k`. So the map remembers the first index of every
            running total.
            """,
            walk(lwalk),
            code(
                "Longest stretch with a given sum",
                LONGEST,
                [
                    ("seed", "The empty prefix (total 0) sits at index -1, just before the array, so a stretch starting "
                             "at index 0 can be found too. `best = 0` means we haven't found one yet."),
                    ("loop", "`j` is the end of the stretches we're looking for."),
                    ("run", "`prefix` is the sum of `nums[0..j]`. Keep it 64-bit."),
                    ("look", "If an earlier gap had a running total of `prefix - k`, then everything after it up to `j` "
                             "adds up to `k`. Using its first appearance gives the longest such stretch ending at `j`.",
                     {"cpp": "`find` doesn't insert anything."}),
                    ("keep", "Only store a running total the first time it appears. A later gap with the same total "
                             "could only give shorter stretches."),
                    ("ret", "The longest length found, or 0 if there wasn't one."),
                    ("table", "An open-addressing table on 64-bit totals, storing the first index for each."),
                    ("free", "Free the table."),
                ],
                LONGEST_RUN,
                "longest_with_sum([2, -1, 3, 1, -2, 4], 4); longest_with_sum([5, -5, 5, -5], 0); longest_with_sum([1, 2], 7)",
            ),
            table(["j", "x", "running total", "looking for", "stretch found", "best", "map"], *l_rows),
            f"""
            The answer is {LANS}. Look at the row where a running total shows up a second time: the map keeps the
            older index, and that's what makes the stretches as long as possible.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Finding a balance point

            Weights `{W}` sit in a row. Is there a position where everything to its left weighs the same as everything
            to its right? You don't even need the whole `P` array. Work out the total once ({WT}), keep a running left
            sum, and the right side is just `total - left - weight`:
            """,
            table(["i", "weight", "left of it", "right of it", ""], *w_rows),
            fig(Bars(W, st={BAL: "answer", **{i: "found" for i in range(BAL)}, **{i: "mark" for i in range(BAL + 1, len(W))}}, label="weights"),
                caption=f"At index {BAL}, the left side ({sum(W[:BAL])}) and the right side ({sum(W[BAL + 1:])}) balance."),
            f"""
            ### As many 0s as 1s

            What's the longest stretch of `{BITS}` with the same number of 0s and 1s? Counting 0s and 1s for every
            stretch would be slow. Instead, turn every 0 into -1. A stretch with equal numbers then adds up to 0, and
            a stretch adds up to 0 exactly when the running total is the same at both ends:
            """,
            fig(Row(BITS, label="bits"), Row(PM, label="0 → -1"),
                Bars(PP, st={B01[0]: "answer", B01[1]: "answer"}, label="running total (gap 0 to gap 8)"),
                caption=f"The running total is {PP[B01[0]]} at gap {B01[0]} and again at gap {B01[1]}, so the {BEST01} elements in between are balanced."),
            f"""
            That's {BEST01}. Rewriting the input so that the condition becomes a sum is a trick worth remembering.
            Whenever a problem says "as many X as Y", try +1 and -1.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Two dimensions

            For sums over rectangles in a grid, asked many times. Build `P` with an extra row and column of zeros,
            then each query uses four values.
            """,
            code(
                "2D prefix sums",
                GRID,
                [
                    ("make", "A `(rows + 1) × (cols + 1)` table of zeros. Row 0 and column 0 stay 0, just like `P[0]` in 1D.",
                     {"c": "One flat block of memory, where `(r, c)` lives at `r * (cols + 1) + c`. `calloc` zeroes it."}),
                    ("fill", "Fill it row by row, so the three neighbours each cell needs are already done."),
                    ("cell", "This cell, plus the rectangle above, plus the rectangle to the left, minus the top-left "
                             "block, which got added twice."),
                    ("ret", "The table."),
                    ("query", "The big rectangle down to `(r2, c2)`, minus the strip above row `r1`, minus the strip left "
                              "of column `c1`, plus the corner that both strips took away."),
                ],
                GRID_RUN,
                "rect_sum on [[2, 0, 1, 3], [4, 1, 0, 2], [1, 5, 2, 1]] for (0,0)-(2,3), (1,1)-(2,2), (0,2)-(1,3), (2,0)-(2,0)",
            ),
            fig(Grid(G, st={(r, c): "answer" for r in range(R1, R2 + 1) for c in range(C1, C2 + 1)}, label="grid"),
                Grid(GP, st={(R2 + 1, C2 + 1): "found", (R1, C2 + 1): "mark", (R2 + 1, C1): "mark", (R1, C1): "found"}, label="P"),
                caption=f"The four values from P: {GP[R2 + 1][C2 + 1]} - {GP[R1][C2 + 1]} - {GP[R2 + 1][C1]} + {GP[R1][C1]} = {GS}."),
            """
            ### Counting stretches with sum `k`

            Same loop as *longest*, but the map stores how many times each total has appeared, starting with `{0: 1}`.
            At each step, add `count[prefix - k]` to the answer, then bump `count[prefix]`. The walkthrough in *Why it
            works* shows it running.

            ### Prefix of anything you can undo

            XOR: `X[r + 1] ^ X[l]` is the XOR of a range, and "stretches with XOR `k`" looks up `X[j] ^ k`. Counts per
            category: 26 prefix arrays, one per letter, answer "how many `e`s are in `s[l..r]`?" in O(1). A running
            maximum is still useful, but only for prefixes ("the best so far"); it can't answer ranges.

            ### Going the other way

            Prefix sums turn an array into running totals. The reverse, taking differences between neighbours, turns
            "add `v` to a whole range" into two small changes. That's the next pattern, *Difference arrays*.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            Building `P` takes O(n) time and O(n) memory (O(rows × cols) in 2D). Each range question after that is
            O(1). Finding stretches with a hash map is O(n) on average, with O(n) memory for the map.

            Without prefix sums, `q` questions over ranges of length up to `n` cost O(q × n). With `n` and `q` both
            100,000, that's up to {N * N:,} additions, against about {2 * N:,} with prefix sums. For "count the
            stretches that add up to `k`", brute force looks at all n(n + 1)/2 stretches, while the prefix-and-map
            version does one lookup per element.
            """,
            table(
                ["Task", "Without", "With prefix sums"],
                ["q range sums", "O(q · n)", "O(n + q)"],
                ["count stretches with sum k", "O(n²)", "O(n) on average"],
                ["longest stretch with sum k", "O(n²)", "O(n) on average"],
                ["q rectangle sums in an R × C grid", "O(q · R · C)", "O(R · C + q)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `itertools.accumulate(nums, initial=0)` builds `P` in one go (Python 3.8 and later). Integers never
            overflow. For the stretch search, `dict.get(prefix - k, 0)` and `setdefault(prefix, j)` (which keeps the
            first index).

            ### Java

            Use `long[]` for `P`, since an `int` total overflows past about 2.1 billion. A `Map<Long, Integer>` needs
            `Long` keys, so write `first.put(0L, -1)` with the `L`. A plain `0` would turn into an `Integer`, which is a
            different key, and your lookups would quietly miss it.

            ### C++

            `std::partial_sum` exists, but writing the loop yourself with an explicit `P[0] = 0` is clearer. Use
            `long long`. For the map, `unordered_map<long long, int>` with `emplace` (keeps the first) and `find` (doesn't
            insert).

            ### C

            `long long` totals. For 2D, one flat `calloc` block indexed `r * (cols + 1) + c`. The hash map for the
            stretch problems is the same open-addressing table as before, on 64-bit keys.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            Where prefix-sum code usually goes wrong:

            - Off by one. The sum of `l..r` including both ends is `P[r + 1] - P[l]`, not `P[r] - P[l]`. If you're
              unsure, draw the gaps.
            - Forgetting to seed the map. Without `{0: 1}` (counting) or `{0: -1}` (longest), stretches that start at
              index 0 get missed.
            - Keeping the wrong index. For the longest stretch keep the first one; overwriting gives you shorter ones.
            - Overflow. Adding up lots of big values needs 64 bits, both in `P` and in the running total.
            - Negative remainders. In Java, C and C++, `-1 % 5` is `-1`. Fix it before using a remainder as a key.
            - Using a sliding window when there are negatives. Shrinking the window doesn't reliably lower the sum any
              more. Use prefix sums with a map.
            - Trying to subtract maximums. Range max and min need different tools.
            - Signs in 2D. Building: plus above, plus left, minus corner. Querying: minus above, minus left, plus
              corner.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("With `P` built from `nums`, what's the sum of `nums[2..5]`?",
                 "`P[6] - P[2]`. That's everything before gap 6 (indices 0 to 5) minus everything before gap 2 (indices 0 and 1)."),
                ("Why does counting stretches with sum `k` start the map at `{0: 1}`?",
                 "`P[0] = 0` is the gap before the first element. A stretch from index 0 to `j` adds up to `k` exactly when `P[j + 1] - 0 = k`. Without the seed, the lookup for 0 would miss it."),
                ("Some values are negative. Why does a sliding window fail for \"longest stretch with sum k\", when prefix sums work?",
                 "The window shrinks when the sum gets too big, assuming that dropping elements makes the sum smaller. Negative values break that. Prefix sums only rely on `P[r + 1] - P[l]`, which is true for any integers."),
                ("Can you answer \"what's the biggest value in `nums[l..r]`?\" with running maximums?",
                 "No. The maximum of `[0..r]` might be before `l`, and there's no way to subtract it back out. You'd use a sparse table or a segment tree."),
                ("Longest stretch with as many 0s as 1s: how do you turn it into a prefix-sum problem?",
                 "Turn every 0 into -1. A stretch has equal counts exactly when it adds up to 0, which means the running total is the same at both ends. Keep the first index where each total appeared."),
            ),
        ]),
    ],
)
