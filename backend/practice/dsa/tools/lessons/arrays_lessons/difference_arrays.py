"""Lesson: Difference arrays (Arrays & Hashing, pattern 5)."""
from lesson import Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

APPLY = {
    "python": """
        def apply_ranges(n, updates):
            diff = [0] * (n + 1)                    #@make
            for l, r, v in updates:                 #@mark
                diff[l] += v                        #@mark
                diff[r + 1] -= v                    #@mark
            result = [0] * n                        #@build
            running = 0                             #@build
            for i in range(n):                      #@build
                running += diff[i]                  #@build
                result[i] = running                 #@build
            return result                           #@ret
    """,
    "java": """
        static long[] applyRanges(int n, int[][] updates) {
            long[] diff = new long[n + 1];                  //@make
            for (int[] u : updates) {                       //@mark
                diff[u[0]] += u[2];                         //@mark
                diff[u[1] + 1] -= u[2];                     //@mark
            }
            long[] result = new long[n];                    //@build
            long running = 0;                               //@build
            for (int i = 0; i < n; i++) {                   //@build
                running += diff[i];                         //@build
                result[i] = running;                        //@build
            }
            return result;                                  //@ret
        }
    """,
    "cpp": """
        vector<long long> applyRanges(int n, const vector<array<int, 3>>& updates) {
            vector<long long> diff(n + 1, 0);               //@make
            for (auto [l, r, v] : updates) {                //@mark
                diff[l] += v;                               //@mark
                diff[r + 1] -= v;                           //@mark
            }
            vector<long long> result(n);                    //@build
            long long running = 0;                          //@build
            for (int i = 0; i < n; i++) {                   //@build
                running += diff[i];                         //@build
                result[i] = running;                        //@build
            }
            return result;                                  //@ret
        }
    """,
    "c": """
        // updates[k] = {l, r, v}; the caller frees the result.
        long long* applyRanges(int n, const int (*updates)[3], int m) {
            long long* diff = calloc(n + 1, sizeof(long long));     //@make
            for (int k = 0; k < m; k++) {                   //@mark
                diff[updates[k][0]] += updates[k][2];       //@mark
                diff[updates[k][1] + 1] -= updates[k][2];   //@mark
            }
            long long* result = malloc(n * sizeof(long long));      //@build
            long long running = 0;                          //@build
            for (int i = 0; i < n; i++) {                   //@build
                running += diff[i];                         //@build
                result[i] = running;                        //@build
            }
            free(diff);                                     //@ret
            return result;                                  //@ret
        }
    """,
}
APPLY_RUN = {
    "python": """
        print(*apply_ranges(8, [[1, 4, 2], [3, 6, 1], [0, 2, 3], [5, 7, 4]]))
    """,
    "java": """
        public static void main(String[] args) {
            long[] a = applyRanges(8, new int[][] {{1, 4, 2}, {3, 6, 1}, {0, 2, 3}, {5, 7, 4}});
            StringBuilder sb = new StringBuilder();
            for (long v : a) sb.append(sb.length() > 0 ? " " : "").append(v);
            System.out.println(sb);
        }
    """,
    "cpp": """
        int main() {
            auto a = applyRanges(8, {{1, 4, 2}, {3, 6, 1}, {0, 2, 3}, {5, 7, 4}});
            for (size_t i = 0; i < a.size(); i++) cout << (i ? " " : "") << a[i];
            cout << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int ups[][3] = {{1, 4, 2}, {3, 6, 1}, {0, 2, 3}, {5, 7, 4}};
            long long* a = applyRanges(8, ups, 4);
            for (int i = 0; i < 8; i++) printf(i ? " %lld" : "%lld", a[i]);
            printf("\\n");
            free(a);
            return 0;
        }
    """,
}

SWEEP = {
    "python": """
        def max_overlap(intervals):
            events = []                                 #@events
            for start, end in intervals:                #@events
                events.append((start, +1))              #@events
                events.append((end, -1))                #@events
            events.sort()                               #@sort
            live = best = 0                             #@scan
            for _, delta in events:                     #@scan
                live += delta                           #@scan
                best = max(best, live)                  #@best
            return best                                 #@ret
    """,
    "java": """
        static int maxOverlap(int[][] intervals) {
            int m = intervals.length;
            long[][] events = new long[2 * m][];                        //@events
            for (int k = 0; k < m; k++) {                               //@events
                events[2 * k] = new long[] {intervals[k][0], +1};       //@events
                events[2 * k + 1] = new long[] {intervals[k][1], -1};   //@events
            }
            Arrays.sort(events, (a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));  //@sort
            int live = 0, best = 0;                                     //@scan
            for (long[] e : events) {                                   //@scan
                live += (int) e[1];                                     //@scan
                best = Math.max(best, live);                            //@best
            }
            return best;                                                //@ret
        }
    """,
    "cpp": """
        int maxOverlap(const vector<pair<int, int>>& intervals) {
            vector<pair<int, int>> events;                  //@events
            for (auto [start, end] : intervals) {           //@events
                events.push_back({start, +1});              //@events
                events.push_back({end, -1});                //@events
            }
            sort(events.begin(), events.end());             //@sort
            int live = 0, best = 0;                         //@scan
            for (auto [at, delta] : events) {               //@scan
                live += delta;                              //@scan
                best = max(best, live);                     //@best
            }
            return best;                                    //@ret
        }
    """,
    "c": """
        typedef struct { int at, delta; } Event;

        static int byTimeThenDelta(const void* a, const void* b) {
            const Event *x = a, *y = b;                                 //@sort
            if (x->at != y->at) return (x->at > y->at) - (x->at < y->at);  //@sort
            return x->delta - y->delta;                                 //@sort
        }

        int maxOverlap(const int (*intervals)[2], int m) {
            Event* events = malloc(2 * m * sizeof(Event));              //@events
            for (int k = 0; k < m; k++) {                               //@events
                events[2 * k] = (Event){intervals[k][0], +1};           //@events
                events[2 * k + 1] = (Event){intervals[k][1], -1};       //@events
            }
            qsort(events, 2 * m, sizeof(Event), byTimeThenDelta);       //@sort
            int live = 0, best = 0;                                     //@scan
            for (int k = 0; k < 2 * m; k++) {                           //@scan
                live += events[k].delta;                                //@scan
                if (live > best) best = live;                           //@best
            }
            free(events);                                               //@ret
            return best;                                                //@ret
        }
    """,
}
SWEEP_RUN = {
    "python": """
        print(max_overlap([(900, 1030), (1000, 1100), (1030, 1200), (1015, 1045), (1100, 1130)]))
        print(max_overlap([(1, 2), (2, 3), (3, 4)]))
        print(max_overlap([(0, 1000000000), (5, 6), (999999990, 1000000000)]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(maxOverlap(new int[][] {{900, 1030}, {1000, 1100}, {1030, 1200}, {1015, 1045}, {1100, 1130}}));
            System.out.println(maxOverlap(new int[][] {{1, 2}, {2, 3}, {3, 4}}));
            System.out.println(maxOverlap(new int[][] {{0, 1000000000}, {5, 6}, {999999990, 1000000000}}));
        }
    """,
    "cpp": """
        int main() {
            cout << maxOverlap({{900, 1030}, {1000, 1100}, {1030, 1200}, {1015, 1045}, {1100, 1130}}) << "\\n";
            cout << maxOverlap({{1, 2}, {2, 3}, {3, 4}}) << "\\n";
            cout << maxOverlap({{0, 1000000000}, {5, 6}, {999999990, 1000000000}}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[][2] = {{900, 1030}, {1000, 1100}, {1030, 1200}, {1015, 1045}, {1100, 1130}};
            int b[][2] = {{1, 2}, {2, 3}, {3, 4}};
            int c[][2] = {{0, 1000000000}, {5, 6}, {999999990, 1000000000}};
            printf("%d\\n%d\\n%d\\n", maxOverlap(a, 5), maxOverlap(b, 3), maxOverlap(c, 3));
            return 0;
        }
    """,
}

GRID2 = {
    "python": """
        def paint_rects(rows, cols, rects):
            D = [[0] * (cols + 1) for _ in range(rows + 1)]     #@make
            for r1, c1, r2, c2, v in rects:                     #@mark
                D[r1][c1] += v                                  #@mark
                D[r1][c2 + 1] -= v                              #@mark
                D[r2 + 1][c1] -= v                              #@mark
                D[r2 + 1][c2 + 1] += v                          #@mark
            for r in range(rows):                               #@rows
                for c in range(1, cols):                        #@rows
                    D[r][c] += D[r][c - 1]                      #@rows
            for r in range(1, rows):                            #@cols
                for c in range(cols):                           #@cols
                    D[r][c] += D[r - 1][c]                      #@cols
            return [row[:cols] for row in D[:rows]]             #@ret
    """,
    "java": """
        static long[][] paintRects(int rows, int cols, int[][] rects) {
            long[][] D = new long[rows + 1][cols + 1];          //@make
            for (int[] q : rects) {                             //@mark
                D[q[0]][q[1]] += q[4];                          //@mark
                D[q[0]][q[3] + 1] -= q[4];                      //@mark
                D[q[2] + 1][q[1]] -= q[4];                      //@mark
                D[q[2] + 1][q[3] + 1] += q[4];                  //@mark
            }
            for (int r = 0; r < rows; r++)                      //@rows
                for (int c = 1; c < cols; c++) D[r][c] += D[r][c - 1];  //@rows
            for (int r = 1; r < rows; r++)                      //@cols
                for (int c = 0; c < cols; c++) D[r][c] += D[r - 1][c];  //@cols
            long[][] out = new long[rows][];                    //@ret
            for (int r = 0; r < rows; r++) out[r] = Arrays.copyOf(D[r], cols);  //@ret
            return out;                                         //@ret
        }
    """,
    "cpp": """
        vector<vector<long long>> paintRects(int rows, int cols, const vector<array<int, 5>>& rects) {
            vector<vector<long long>> D(rows + 1, vector<long long>(cols + 1, 0));  //@make
            for (auto [r1, c1, r2, c2, v] : rects) {            //@mark
                D[r1][c1] += v;                                 //@mark
                D[r1][c2 + 1] -= v;                             //@mark
                D[r2 + 1][c1] -= v;                             //@mark
                D[r2 + 1][c2 + 1] += v;                         //@mark
            }
            for (int r = 0; r < rows; r++)                      //@rows
                for (int c = 1; c < cols; c++) D[r][c] += D[r][c - 1];  //@rows
            for (int r = 1; r < rows; r++)                      //@cols
                for (int c = 0; c < cols; c++) D[r][c] += D[r - 1][c];  //@cols
            D.pop_back();                                       //@ret
            for (auto& row : D) row.pop_back();                 //@ret
            return D;                                           //@ret
        }
    """,
    "c": """
        // Returns a rows x cols grid in one block (cell (r, c) at r * cols + c); the caller frees it.
        long long* paintRects(int rows, int cols, const int (*rects)[5], int m) {
            int w = cols + 1;                                   //@make
            long long* D = calloc((size_t)(rows + 1) * w, sizeof(long long));  //@make
            for (int k = 0; k < m; k++) {                       //@mark
                int r1 = rects[k][0], c1 = rects[k][1], r2 = rects[k][2], c2 = rects[k][3], v = rects[k][4];  //@mark
                D[r1 * w + c1] += v;                            //@mark
                D[r1 * w + c2 + 1] -= v;                        //@mark
                D[(r2 + 1) * w + c1] -= v;                      //@mark
                D[(r2 + 1) * w + c2 + 1] += v;                  //@mark
            }
            for (int r = 0; r < rows; r++)                      //@rows
                for (int c = 1; c < cols; c++) D[r * w + c] += D[r * w + c - 1];  //@rows
            for (int r = 1; r < rows; r++)                      //@cols
                for (int c = 0; c < cols; c++) D[r * w + c] += D[(r - 1) * w + c];  //@cols
            long long* out = malloc((size_t)rows * cols * sizeof(long long));  //@ret
            for (int r = 0; r < rows; r++)                      //@ret
                for (int c = 0; c < cols; c++) out[r * cols + c] = D[r * w + c];  //@ret
            free(D);                                            //@ret
            return out;                                         //@ret
        }
    """,
}
GRID2_RUN = {
    "python": """
        for row in paint_rects(4, 5, [[0, 0, 1, 2, 1], [1, 1, 3, 3, 2], [2, 4, 3, 4, 5]]):
            print(*row)
    """,
    "java": """
        public static void main(String[] args) {
            for (long[] row : paintRects(4, 5, new int[][] {{0, 0, 1, 2, 1}, {1, 1, 3, 3, 2}, {2, 4, 3, 4, 5}})) {
                StringBuilder sb = new StringBuilder();
                for (long v : row) sb.append(sb.length() > 0 ? " " : "").append(v);
                System.out.println(sb);
            }
        }
    """,
    "cpp": """
        int main() {
            for (auto& row : paintRects(4, 5, {{0, 0, 1, 2, 1}, {1, 1, 3, 3, 2}, {2, 4, 3, 4, 5}})) {
                for (size_t i = 0; i < row.size(); i++) cout << (i ? " " : "") << row[i];
                cout << "\\n";
            }
        }
    """,
    "c": """
        int main(void) {
            int rects[][5] = {{0, 0, 1, 2, 1}, {1, 1, 3, 3, 2}, {2, 4, 3, 4, 5}};
            long long* g = paintRects(4, 5, rects, 3);
            for (int r = 0; r < 4; r++) {
                for (int c = 0; c < 5; c++) printf(c ? " %lld" : "%lld", g[r * 5 + c]);
                printf("\\n");
            }
            free(g);
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

apply_ranges = py(APPLY["python"], "apply_ranges")
max_overlap = py(SWEEP["python"], "max_overlap")
paint_rects = py(GRID2["python"], "paint_rects")

N8 = 8
JOBS = [[1, 4, 2], [3, 6, 1], [0, 2, 3], [5, 7, 4]]
FINAL = apply_ranges(N8, JOBS)
naive = [0] * N8
for l, r, v in JOBS:
    for i in range(l, r + 1):
        naive[i] += v
assert FINAL == naive

steps = Steps(f"`apply_ranges({N8}, {JOBS})`: mark both ends of every update, then sweep once.")
diff = [0] * (N8 + 1)
steps.step(f"diff has n + 1 = {N8 + 1} slots, all 0. Slot {N8} is a spare: it absorbs updates that run to the last index.", Row(diff, slots=True, label="diff"))
for l, r, v in JOBS:
    diff[l] += v
    diff[r + 1] -= v
    steps.step(f"Add {v} to [{l}, {r}]: diff[{l}] += {v} (the rise starts at {l}), diff[{r + 1}] -= {v} (it stops after {r}). Two writes, whatever the length.",
               Row(list(diff), st={l: "new", r + 1: "new"}, slots=True, label="diff"))
run, out = 0, [None] * N8
for i in range(N8):
    run += diff[i]
    out[i] = run
    if i in (0, 3, N8 - 1) or i == 5:
        steps.step(f"Sweep: running total after diff[{i}] = {run}. That's the final value at index {i}.",
                   Row(list(diff), st={**{j: "dim" for j in range(i)}, i: "active"}, ptr={"i": i}, slots=True, label="diff"),
                   Row(list(out), st={i: "new"}, slots=True, label="result"))
steps.step(f"Done: {FINAL}. {len(JOBS)} updates cost {2 * len(JOBS)} writes; the sweep cost {N8} steps.", Row(FINAL, st={i: "answer" for i in range(N8)}, slots=True, label="result"), result=FINAL)

d_rows = []
d = [0] * (N8 + 1)
for l, r, v in JOBS:
    d[l] += v
    d[r + 1] -= v
    d_rows.append((f"+{v} on [{l}, {r}]", " ".join(f"{x:+d}" if x else "0" for x in d)))

# Differences of an array and its recovery.
A = [4, 4, 7, 7, 7, 2]
DA = [A[0]] + [A[i] - A[i - 1] for i in range(1, len(A))]
rec, s = [], 0
for x in DA:
    s += x
    rec.append(s)
assert rec == A

MEET = [(900, 1030), (1000, 1100), (1030, 1200), (1015, 1045), (1100, 1130)]
MANS = max_overlap(MEET)
ev = sorted([(a, +1) for a, b in MEET] + [(b, -1) for a, b in MEET])
ev_rows, live, best = [], 0, 0
for at, dlt in ev:
    live += dlt
    best = max(best, live)
    ev_rows.append((str(at), "start" if dlt > 0 else "end", f"{dlt:+d}", str(live), str(best)))
assert best == MANS
assert max_overlap([(1, 2), (2, 3), (3, 4)]) == 1

RECTS = [[0, 0, 1, 2, 1], [1, 1, 3, 3, 2], [2, 4, 3, 4, 5]]
PAINT = paint_rects(4, 5, RECTS)
chk = [[0] * 5 for _ in range(4)]
for r1, c1, r2, c2, v in RECTS:
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            chk[r][c] += v
assert PAINT == chk
CORNERS = [[0] * 6 for _ in range(5)]
r1, c1, r2, c2, v = RECTS[1]
CORNERS[r1][c1] += v
CORNERS[r1][c2 + 1] -= v
CORNERS[r2 + 1][c1] -= v
CORNERS[r2 + 1][c2 + 1] += v

N = 10**5
lesson(
    "arrays-hashing",
    "difference-arrays",
    """
    When many updates each add a value to a whole range, don't touch every element. Record only where each change
    **starts** and where it **stops**, then rebuild the array with one running total at the end.
    """,
    [
        ("idea", "The idea", [
            """
            A bus driver doesn't count every passenger at every stop. They note two events: "3 got on at stop 2",
            "3 got off at stop 6". The number of people on board at any stop is just the running total of those
            events up to that stop.

            A difference array applies that to range updates. To "add `v` to every element from `l` to `r`":

            1. `diff[l] += v` (from here on, everything is `v` higher),
            2. `diff[r + 1] -= v` (and from here on, it isn't any more).

            After all the updates, a single running total over `diff` (a prefix sum) gives the final array.
            """,
            fig(Row([0, 2, 0, 0, 0, -2, 0], slots=True, label="diff after +2 on [1, 4]"),
                Row([0, 2, 2, 2, 2, 0, 0], st={i: "new" for i in range(1, 5)}, slots=True, label="running total"),
                caption="Two writes describe the whole update. The running total spreads it across `[1, 4]` and cancels it at 5."),
            key("""
            A range update is two point updates on the difference array: `+v` where it starts, `-v` just after it ends.
            Apply all updates in O(1) each, then rebuild everything with one O(n) prefix sum.
            """),
            """
            This is the **mirror image of prefix sums**. Prefix sums make range *queries* cheap on an array that doesn't
            change. Difference arrays make range *updates* cheap, as long as you only need to read the result at the end.
            """,
        ]),
        ("signals", "When to reach for it", [
            table(
                ["The problem says…", "Each event becomes"],
                ["add / increase every element from `l` to `r`, many times", "`diff[l] += v`, `diff[r + 1] -= v`"],
                ["bookings, reservations, passengers between stops", "`+count` at start, `-count` at end"],
                ["how many intervals cover each point / the busiest point", "`+1` at start, `-1` after end"],
                ["lamps, ranges of influence, coverage", "`+1` on `[p - reach, p + reach]`"],
                ["many rectangles painted on a grid", "four corners in a 2D difference array"],
            ),
            """
            **The shape to recognise:** *many updates first, all reads afterwards*, and each update touches a contiguous
            range.

            **When it is the wrong tool**

            - **Reads between updates.** If the problem asks "what is `a[i]` now?" after each update, the running total
              would have to be recomputed every time. Use a Fenwick tree over the difference array (range update, point
              query in O(log n)), or a segment tree with lazy propagation.
            - **Coordinates are huge.** An array indexed up to 10⁹ won't fit. Keep only the events, **sort** them, and
              sweep (the *sweep line* variation below).
            - **Updates that aren't additions.** "Set every element in `[l, r]` to `v`" or "take the max with `v`" can't be
              expressed as start/stop differences.
            """,
        ]),
        ("theory", "Why it works", [
            f"""
            ### Differences and their running total

            For an array `A`, define the **difference array** `D[0] = A[0]` and `D[i] = A[i] - A[i - 1]`. Then the prefix
            sums of `D` give back `A`, by telescoping:

            `D[0] + D[1] + … + D[i] = A[0] + (A[1] - A[0]) + … + (A[i] - A[i - 1]) = A[i]`

            For `A = {A}`:
            """,
            table(["i", "A[i]", "D[i] = A[i] - A[i-1]", "running total of D"],
                  *[(str(i), str(A[i]), f"{DA[i]:+d}" if i else str(DA[i]), str(rec[i])) for i in range(len(A))]),
            """
            `D` is non-zero only where `A` **changes**. A long flat stretch in `A` is a run of zeros in `D`. That's why a
            range update is cheap in `D`.

            ### A range update touches two differences

            Add `v` to `A[l..r]`. Which neighbour differences change?

            - Inside the range, both neighbours went up by `v`: `A[i] - A[i - 1]` is unchanged for `l < i ≤ r`.
            - At `i = l`, only `A[l]` went up: `D[l]` grows by `v`.
            - At `i = r + 1`, only `A[r]` went up: `D[r + 1]` shrinks by `v`.
            - Everywhere else nothing changed.

            So the update is exactly `D[l] += v; D[r + 1] -= v`. If `r` is the last index, `D[r + 1]` is a spare slot
            past the end (size `n + 1`) that the rebuild never reads.

            ### Many updates

            Each update is a change to `D`, and additions can be done in any order, so all `m` updates simply add up in
            `D`. One prefix sum at the end applies all of them at once. Starting from an all-zero array, `D` starts at all
            zeros too; starting from an existing array, start with its differences (or add the result to it).

            ### Events: the same idea without an array

            Read `D[l] += v` as an **event** "`+v` happens at position `l`" and `D[r + 1] -= v` as "`-v` happens at
            `r + 1`". The running total at a position is the sum of all events at or before it. If positions are huge
            or not integers (times, coordinates), keep only the `2m` events, sort them by position, and sweep. Between
            two consecutive events nothing changes, so you only need to look at event positions: O(m log m) regardless of
            how far apart they are.

            ### Inclusive or half-open?

            - Inclusive `[l, r]`: the change ends **after** `r`, so the `-v` goes at `r + 1`.
            - Half-open `[start, end)` (a meeting from 10:00 to 11:00 is over at 11:00): the `-v` goes at `end` itself.

            With events, the tie-break at equal positions encodes the same choice: for half-open intervals process ends
            before starts (a meeting ending at 11:00 and one starting at 11:00 don't overlap); for inclusive ones, starts
            first.

            ### Two dimensions

            In 2D, adding `v` to the rectangle `(r1, c1)–(r2, c2)` is four corner updates, by the same reasoning applied
            along rows and then columns:
            """,
            table(["corner", "update", "why"],
                  ["`(r1, c1)`", "`+v`", "the rectangle starts here"],
                  ["`(r1, c2 + 1)`", "`-v`", "stop to the right of the rectangle"],
                  ["`(r2 + 1, c1)`", "`-v`", "stop below the rectangle"],
                  ["`(r2 + 1, c2 + 1)`", "`+v`", "the region right and below was subtracted twice"]),
            fig(Grid(CORNERS, st={(r1, c1): "new", (r1, c2 + 1): "mark", (r2 + 1, c1): "mark", (r2 + 1, c2 + 1): "new"}, label=f"+{v} on ({r1},{c1})–({r2},{c2})"),
                caption="Four writes. A 2D prefix sum (rows, then columns) spreads them over exactly the rectangle."),
        ]),
        ("template", "The template", [
            """
            Apply `m` updates `[l, r, v]` (add `v` to every index from `l` to `r`, inclusive) to an array of `n` zeros,
            and return the final array. The example: a fence of 8 boards, and painting jobs that each add coats to a
            run of boards.
            """,
            code(
                "Apply many range additions",
                APPLY,
                [
                    ("make", "`n + 1` zeros. The extra slot takes the `-v` of updates that end at the last index.",
                     {"c": "`calloc` gives zeros."}),
                    ("mark", "Two writes per update, however long the range: the rise at `l`, the fall at `r + 1`."),
                    ("build", "One running total over `diff`. The total at index `i` is the sum of every `+v` that started "
                              "at or before `i`, minus every `-v` of ranges that already ended: exactly the updates that "
                              "cover `i`."),
                    ("ret", "The final values. Slot `n` of `diff` is never read: whatever it holds affects only positions "
                            "past the end.",
                     {"c": "Free the difference array; the caller owns `result`."}),
                ],
                APPLY_RUN,
                "apply_ranges(8, [[1, 4, 2], [3, 6, 1], [0, 2, 3], [5, 7, 4]])",
            ),
        ]),
        ("trace", "Trace it by hand", [
            walk(steps),
            "The difference array after each update (index 0 to 8):",
            table(["update", "diff"], *d_rows),
            f"""
            The running total of the last row is `{FINAL}`. Updating every element directly would have cost
            {sum(r - l + 1 for l, r, _ in JOBS)} writes here; with ranges of length n and m updates that's up to `n · m`.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Sweep line: huge coordinates

            Meetings `[start, end)` with times up to 10⁹: what's the most that overlap at any moment? An array over all
            times is impossible, but there are only `2m` events. Sort them and keep the running total. Sorting `(time,
            delta)` pairs puts `-1` before `+1` at the same time, which is exactly the half-open rule: a meeting that
            ends at 11:00 frees its room before one that starts at 11:00 takes it.
            """,
            code(
                "Most meetings at once (sorted events)",
                SWEEP,
                [
                    ("events", "Two events per meeting: `+1` when it starts, `-1` when it ends."),
                    ("sort", "Sort by time; at equal times, `-1` (an end) sorts before `+1` (a start).",
                     {"c": "The comparator orders by time with `(a > b) - (a < b)`, which can't overflow the way `a - b` can for large values, then by delta.",
                      "java": "Comparing with `Long.compare` avoids the overflow that `a[0] - b[0]` would risk."}),
                    ("scan", "Walk the events in order; `live` is how many meetings are running right after this event."),
                    ("best", "The busiest moment is the largest `live` seen. Between events nothing changes, so checking "
                             "only at events is enough."),
                    ("ret", "The maximum overlap.",
                     {"c": "Free the events first."}),
                ],
                SWEEP_RUN,
                "max_overlap([(900, 1030), (1000, 1100), (1030, 1200), (1015, 1045), (1100, 1130)]); [(1, 2), (2, 3), (3, 4)]; huge times",
            ),
            table(["time", "event", "delta", "live", "best"], *ev_rows),
            f"""
            At 10:30 one meeting ends and another starts: the end goes first, so `live` dips before it rises, and the
            answer is {MANS}. Back-to-back meetings `(1, 2), (2, 3), (3, 4)` never overlap: 1.

            ### Rectangles on a grid

            Four corner updates per rectangle, then a prefix sum along each row and one along each column.
            """,
            code(
                "Add values to many rectangles",
                GRID2,
                [
                    ("make", "An `(rows + 1) × (cols + 1)` difference grid of zeros; the extra row and column catch the "
                             "corners just past the edge."),
                    ("mark", "The four corners of every rectangle: `+v`, `-v`, `-v`, `+v`."),
                    ("rows", "Running totals along each row spread every `+v` rightwards until its `-v`."),
                    ("cols", "Then running totals down each column spread them downwards. Together this is a 2D prefix sum."),
                    ("ret", "Drop the spare row and column.",
                     {"c": "Copy the `rows × cols` part out and free the work grid."}),
                ],
                GRID2_RUN,
                "paint_rects(4, 5, [[0, 0, 1, 2, 1], [1, 1, 3, 3, 2], [2, 4, 3, 4, 5]])",
            ),
            fig(Grid(PAINT, label="result"), caption="Three rectangles, twelve corner writes, one 2D sweep."),
            """
            ### Checking a limit

            "Can a shuttle with `c` seats carry every booking?" Build the occupancy with a difference array (or events),
            then check that the running total never exceeds `c`. You can stop at the first position where it does.

            ### Interleaved updates and queries

            If you must read values between updates, keep the difference array in a **Fenwick tree**: a range update is
            still two point updates, and reading `A[i]` is a prefix-sum query, both O(log n).
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            - **Direct updates:** each update loops over its range, O(n) worst case, so O(n · m) in total. For
              n = m = 10⁵ that's up to {N * N:,} additions.
            - **Difference array:** O(1) per update, plus one O(n) rebuild: **O(n + m)** time, O(n) space.
            - **Sweep line:** O(m log m) for sorting `2m` events, O(m) space, independent of how large the coordinates are.
            - **2D:** O(1) per rectangle, O(rows · cols) to rebuild.
            """,
            table(
                ["Approach", "Time", "Extra space", "Use when"],
                ["Update every element", "O(n · m)", "O(1)", "tiny inputs"],
                ["Difference array", "O(n + m)", "O(n)", "positions fit in an array"],
                ["Sorted events (sweep)", "O(m log m)", "O(m)", "huge or real-valued positions"],
                ["Fenwick tree on differences", "O((m + q) log n)", "O(n)", "reads between updates"],
            ),
        ]),
        ("languages", "In your language", [
            """
            **Python:** `diff = [0] * (n + 1)`; `itertools.accumulate(diff[:n])` rebuilds in one line. For events, sorting
            tuples `(time, delta)` gives the "ends before starts" order for free, since `-1 < 1`.

            **Java:** `long[] diff = new long[n + 1]` (sums of many updates overflow `int`). Sort events with a comparator
            that uses `Integer.compare` / `Long.compare`, never `a - b`.

            **C++:** `vector<long long> diff(n + 1)`; `partial_sum` can rebuild. A `vector<pair<int, int>>` of events
            sorts by time then delta with the default `<`. With sparse coordinates, a `std::map<int, long long>` of
            deltas iterated in order is a sweep with no explicit sort.

            **C:** `calloc(n + 1, sizeof(long long))`; for events, a `struct` array and `qsort` with a comparator that
            doesn't overflow.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - **No spare slot.** `diff[r + 1]` with `r = n - 1` writes out of bounds unless `diff` has `n + 1` entries.
            - **Inclusive vs half-open.** Inclusive ranges stop at `r + 1`; half-open ones at `end`. Mixing them up
              shifts every boundary by one.
            - **Tie order in sweeps.** At equal positions, decide whether ends or starts go first, from the problem's
              wording (does a range ending at 5 overlap one starting at 5?).
            - **Reading before rebuilding.** `diff` holds changes, not values. Only the running total gives values.
            - **Overflow.** Many large updates on the same index overflow 32 bits.
            - **Negative or shifted positions.** A lamp at position 2 with reach 5 covers -3..7. Offset positions so the
              smallest maps to 0, or use events.
            - **Counter-comparators.** `return a.at - b.at` overflows for values near ±2³¹; compare instead.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why does `diff` need `n + 1` slots?",
                 "An update ending at the last index `r = n - 1` writes its `-v` at `n`. The rebuild never reads slot `n`, but it must exist."),
                ("Prove that adding `v` to `A[l..r]` changes only `D[l]` and `D[r + 1]`.",
                 "`D[i] = A[i] - A[i - 1]`. For `l < i ≤ r` both terms rose by `v`, so the difference is unchanged. At `i = l` only `A[l]` rose (`D[l] += v`); at `i = r + 1` only `A[r]` rose (`D[r + 1] -= v`). Elsewhere nothing changed."),
                ("Meetings `[10, 11)` and `[11, 12)`. With events sorted by `(time, delta)`, what's the maximum overlap, and why?",
                 "1. At time 11 the end (`-1`) sorts before the start (`+1`), so the count goes 1 → 0 → 1 and never reaches 2. That matches half-open intervals."),
                ("Updates and \"what is `a[i]` now?\" questions are interleaved, 10⁵ of each. Is a plain difference array enough?",
                 "No: each question would need an O(n) rebuild. Put the difference array in a Fenwick tree: two O(log n) point updates per range update, and `a[i]` is an O(log n) prefix sum."),
                ("How is a difference array related to prefix sums?",
                 "They're inverses. The prefix sum of the difference array gives back the array, and the difference array of the prefix array gives back the original values. Differences make range updates cheap; prefix sums make range queries cheap."),
            ),
        ]),
    ],
)
