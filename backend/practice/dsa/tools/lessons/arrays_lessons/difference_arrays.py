"""Lesson: Difference arrays (Arrays & Hashing, pattern 5)."""
from lesson import Bars, Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

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
TOPV = max(FINAL)

# Final diff, for scaling.
DF = [0] * (N8 + 1)
for l, r, v in JOBS:
    DF[l] += v
    DF[r + 1] -= v
DTOP = max(max(DF), max(abs(sum(DF[:k + 1])) for k in range(N8)))
DBOT = min(DF)

steps = Steps(f"`apply_ranges({N8}, {JOBS})`. Mark where each update starts and stops, then sweep once.")
diff = [0] * (N8 + 1)
steps.step(f"`diff` has {N8 + 1} slots, all 0. The last one is a spare for updates that run right to the end.",
           Bars(diff, label="diff", top=max(DF), bottom=DBOT))
for l, r, v in JOBS:
    diff[l] += v
    diff[r + 1] -= v
    steps.step(f"Add {v} to boards {l} to {r}: diff[{l}] goes up by {v} (that's where it starts) and diff[{r + 1}] goes down by {v} (that's where it stops). "
               f"Two changes, no matter how long the range is.",
               Bars(list(diff), st={l: "new", r + 1: "mark"}, label="diff", top=max(DF), bottom=DBOT))
run, out = 0, [None] * N8
for i in range(N8):
    run += diff[i]
    out[i] = run
    steps.step(f"Sweep: add diff[{i}] = {diff[i]} to the running total, which is now {run}. That's the final value of board {i}.",
               Bars(list(diff), st={**{j: "dim" for j in range(i)}, i: "active"}, label="diff", top=max(DF), bottom=DBOT),
               Bars(list(out), st={i: "new"}, label="result", top=TOPV))
steps.step(f"Done: {FINAL}. Four updates cost eight changes, and the sweep took {N8} steps.",
           Bars(FINAL, st={i: "answer" for i in range(N8)}, label="result", top=TOPV), result=FINAL)

d_rows = []
d = [0] * (N8 + 1)
for l, r, v in JOBS:
    d[l] += v
    d[r + 1] -= v
    d_rows.append((f"+{v} on [{l}, {r}]", " ".join(f"{x:+d}" if x else "0" for x in d)))

# Differences of an array and getting it back.
A = [4, 4, 7, 7, 7, 2]
DA = [A[0]] + [A[i] - A[i - 1] for i in range(1, len(A))]
rec, s = [], 0
for x in DA:
    s += x
    rec.append(s)
assert rec == A

# The bus.
STOPS = 7
TRIPS = [(3, 1, 4), (2, 0, 2), (4, 2, 6), (1, 3, 5)]  # (people, on at, off at)
ons = [0] * STOPS
offs = [0] * STOPS
for p, a, b in TRIPS:
    ons[a] += p
    offs[b] += p
board, cur = [], 0
for s_ in range(STOPS):
    cur += ons[s_] - offs[s_]
    board.append(cur)
BUS_MAX = max(board)
check = [sum(p for p, a, b in TRIPS if a <= s_ < b) for s_ in range(STOPS)]
assert board == check
CAP = 6
OVER = next((s_ for s_ in range(STOPS) if board[s_] > CAP), None)

MEET = [(900, 1030), (1000, 1100), (1030, 1200), (1015, 1045), (1100, 1130)]
MANS = max_overlap(MEET)
ev = sorted([(a, +1) for a, b in MEET] + [(b, -1) for a, b in MEET])
ev_rows, live, best = [], 0, 0
sweep = Steps("Five meetings, as ten sorted events. `live` is how many meetings are running right now.")
lives = []
sweep.step("Sort all starts (+1) and ends (-1) by time. At the same time, ends come first.", M({"events": ", ".join(f"{t}{'+' if d_ > 0 else '−'}" for t, d_ in ev)}))
for k, (at, dlt) in enumerate(ev):
    live += dlt
    best = max(best, live)
    lives.append(live)
    ev_rows.append((str(at), "start" if dlt > 0 else "end", f"{dlt:+d}", str(live), str(best)))
    times = [str(t) for t, _ in ev]
    sweep.step(f"{at}: a meeting {'starts' if dlt > 0 else 'ends'}. {live} running now" + (f", the most so far." if live == best and dlt > 0 else "."),
               Bars(lives + [None] * (len(ev) - len(lives)), labels=times, st={k: "answer" if live == best and dlt > 0 else "active"}, label="meetings running after each event", top=MANS))
assert best == MANS and max_overlap([(1, 2), (2, 3), (3, 4)]) == 1

RECTS = [[0, 0, 1, 2, 1], [1, 1, 3, 3, 2], [2, 4, 3, 4, 5]]
PAINT = paint_rects(4, 5, RECTS)
chk = [[0] * 5 for _ in range(4)]
for r1_, c1_, r2_, c2_, v_ in RECTS:
    for r in range(r1_, r2_ + 1):
        for c in range(c1_, c2_ + 1):
            chk[r][c] += v_
assert PAINT == chk

# 2D walk for one rectangle: corners, then rows, then columns.
r1, c1, r2, c2, v = RECTS[1]
CORNERS = [[0] * 6 for _ in range(5)]
CORNERS[r1][c1] += v
CORNERS[r1][c2 + 1] -= v
CORNERS[r2 + 1][c1] -= v
CORNERS[r2 + 1][c2 + 1] += v
ROWS = [row[:] for row in CORNERS]
for r in range(5):
    for c in range(1, 6):
        ROWS[r][c] += ROWS[r][c - 1]
COLS = [row[:] for row in ROWS]
for r in range(1, 5):
    for c in range(6):
        COLS[r][c] += COLS[r - 1][c]
assert all(COLS[r][c] == (v if r1 <= r <= r2 and c1 <= c <= c2 else 0) for r in range(5) for c in range(6))
w2 = Steps(f"Adding {v} to the rectangle from ({r1}, {c1}) to ({r2}, {c2}) in a 2D difference grid.")
w2.step("Four corner changes: +v at the top-left, -v just right of the top-right, -v just below the bottom-left, +v diagonally past the bottom-right.",
        Grid(CORNERS, st={(r1, c1): "new", (r1, c2 + 1): "mark", (r2 + 1, c1): "mark", (r2 + 1, c2 + 1): "new"}))
w2.step("Running totals along each row: every +v spreads right until its -v cancels it. Now each row band is right, but it carries on below the rectangle.",
        Grid(ROWS, st={(r, c): "found" for r in range(5) for c in range(6) if ROWS[r][c]}))
w2.step(f"Running totals down each column: the bottom row of corners cancels what was spreading downwards. What's left is exactly the rectangle, all {v}s.",
        Grid(COLS, st={(r, c): "answer" for r in range(5) for c in range(6) if COLS[r][c]}))

# Lamps with negative reach: offset positions.
LAMPS = [(2, 3), (6, 1), (-1, 2)]  # (position, reach)
lo = min(p - rch for p, rch in LAMPS)
hi = max(p + rch for p, rch in LAMPS)
ld = [0] * (hi - lo + 2)
for p, rch in LAMPS:
    ld[p - rch - lo] += 1
    ld[p + rch - lo + 1] -= 1
light, cur = [], 0
for i in range(hi - lo + 1):
    cur += ld[i]
    light.append(cur)
assert light == [sum(1 for p, rch in LAMPS if p - rch <= x <= p + rch) for x in range(lo, hi + 1)]
BRIGHT = max(light)
BRIGHT_AT = [x for x, b in zip(range(lo, hi + 1), light) if b == BRIGHT]

N = 10**5
lesson(
    "arrays-hashing",
    "difference-arrays",
    """
    When lots of updates each add something to a whole range, don't touch every element. Just write down where each
    change starts and where it stops, then rebuild the whole array with one running total at the end.
    """,
    [
        ("idea", "The idea", [
            f"""
            Picture a bus driver who wants to know how many people were on board between each pair of stops. They
            don't count heads at every stop. They just note who got on and who got off. The number on board at any
            point is then a running total: everyone who's got on so far, minus everyone who's got off.

            Here are four groups riding a bus with {STOPS} stops. A group of 3 gets on at stop 1 and off at stop 4, a
            group of 2 rides from 0 to 2, and so on:
            """,
            fig(Bars(ons, label="getting on at each stop"), Bars([-x for x in offs], label="getting off"),
                Bars(board, st={board.index(BUS_MAX): "answer"}, label="on board after each stop"),
                caption=f"Only the ons and offs are written down. The running total gives the load everywhere, and it peaks at {BUS_MAX}."),
            """
            A **difference array** does exactly that for "add `v` to every element from `l` to `r`". Instead of
            looping over the range, you make two changes:

            1. `diff[l] += v`, which means "from here on, everything is `v` higher";
            2. `diff[r + 1] -= v`, which means "and from here on, it isn't any more".

            After all the updates, one running total over `diff` gives you the final array.
            """,
            key("""
            A range update becomes two point updates: `+v` where it starts, `-v` just after it ends. Do every update
            in O(1), then rebuild everything with one O(n) running total.
            """),
            """
            If you've done *Prefix sums*, this is its mirror image. Prefix sums make range *questions* cheap on an array
            that doesn't change. Difference arrays make range *updates* cheap, as long as you only need to read the
            result at the end.
            """,
        ]),
        ("signals", "When to reach for it", [
            table(
                ["The problem says…", "each event becomes"],
                ["add to every element from `l` to `r`, many times", "`diff[l] += v`, `diff[r + 1] -= v`"],
                ["bookings, reservations, passengers between stops", "`+count` at the start, `-count` at the end"],
                ["how many ranges cover each point, or the busiest point", "`+1` at the start, `-1` just after the end"],
                ["lamps, ranges of influence, coverage", "`+1` over `[p - reach, p + reach]`"],
                ["lots of rectangles painted on a grid", "four corners in a 2D difference grid"],
            ),
            """
            The shape to spot is *all the updates first, all the reading afterwards*, with every update covering a
            contiguous range.

            If the problem mixes them, asking "what's `a[i]` now?" after each update, you'd have to redo the running
            total every time. That's where a Fenwick tree on the difference array comes in (O(log n) for both), or a
            segment tree with lazy updates.

            If positions are huge, like times up to a billion, you can't make an array that big. Keep just the events,
            sort them, and sweep through them in order (shown below). And if an update isn't an addition, like "set
            everything in `[l, r]` to `v`" or "take the max with `v`", you can't describe it with a start and a stop,
            so this doesn't apply.
            """,
        ]),
        ("theory", "Why it works", [
            f"""
            ### Differences, and getting the array back

            For an array `A`, the **difference array** is `D[0] = A[0]` and `D[i] = A[i] - A[i - 1]`: how much each
            element changes from the one before. If you take running totals of `D`, you get `A` back, because the
            in-between terms cancel out:

            `D[0] + D[1] + … + D[i] = A[0] + (A[1] - A[0]) + … + (A[i] - A[i - 1]) = A[i]`

            For `A = {A}`:
            """,
            fig(Bars(A, label="A"), Bars(DA, label="D: change from the previous element"),
                caption="D is zero wherever A stays flat, and non-zero only where A steps up or down."),
            table(["i", "A[i]", "D[i]", "running total of D"],
                  *[(str(i), str(A[i]), f"{DA[i]:+d}" if i else str(DA[i]), str(rec[i])) for i in range(len(A))]),
            """
            Long flat stretches in `A` turn into runs of zeros in `D`. That's the reason range updates are cheap there.

            ### Why a range update only touches two entries

            Add `v` to `A[l..r]`. Which of the differences change?

            Inside the range, both neighbours went up by `v`, so their difference stays the same. At `l`, only `A[l]`
            went up (its left neighbour didn't), so `D[l]` grows by `v`. At `r + 1`, only the left neighbour `A[r]` went
            up, so `D[r + 1]` shrinks by `v`. Nothing else changed.

            So the whole update is `D[l] += v; D[r + 1] -= v`. If `r` is the last index, `D[r + 1]` is a spare slot past
            the end, which is why the array has `n + 1` slots. The rebuild never reads it.

            ### Lots of updates

            Each update is just a few additions to `D`, and additions can happen in any order, so all of them simply
            pile up in `D`. One running total at the end applies every update at once. If you're starting from an
            existing array instead of zeros, either start from its differences, or build the changes separately and
            add them on at the end.

            ### The same idea, without an array

            You can read `D[l] += v` as an event: "`+v` happens at position `l`". And `D[r + 1] -= v` is "`-v` happens at
            `r + 1`". The value at any position is the sum of all events up to there. If positions are huge or not
            whole numbers (times, coordinates), keep just the `2m` events, sort them by position, and walk through
            them. Between two events nothing changes, so you only need to look at the events themselves. That's
            O(m log m), no matter how far apart they are.

            ### Including the end, or not?

            If the range includes `r`, the change stops *after* `r`, so the `-v` goes at `r + 1`. If it's half-open,
            like a meeting from 10:00 to 11:00 that's over at 11:00, the `-v` goes at the end itself.

            With sorted events, the same choice shows up as a tie-break. For half-open ranges, handle ends before
            starts at the same time (a meeting ending at 11:00 and one starting at 11:00 don't overlap). For inclusive
            ranges, handle starts first.

            ### Two dimensions

            In 2D, adding `v` to the rectangle from `(r1, c1)` to `(r2, c2)` takes four corner changes. Then running
            totals along the rows and down the columns spread them into exactly the rectangle:
            """,
            walk(w2),
            table(["corner", "change", "why"],
                  ["`(r1, c1)`", "`+v`", "the rectangle starts here"],
                  ["`(r1, c2 + 1)`", "`-v`", "stop to the right of it"],
                  ["`(r2 + 1, c1)`", "`-v`", "stop below it"],
                  ["`(r2 + 1, c2 + 1)`", "`+v`", "the area down and to the right got taken away twice"]),
        ]),
        ("template", "The template", [
            """
            Apply `m` updates `[l, r, v]` (add `v` to every index from `l` to `r`, including both) to an array of `n`
            zeros, and return the result. The example is a fence of 8 boards, where each painting job adds some coats to
            a run of boards.
            """,
            code(
                "Apply many range additions",
                APPLY,
                [
                    ("make", "`n + 1` zeros. The extra slot catches the `-v` from updates that end at the last index.",
                     {"c": "`calloc` gives us zeros."}),
                    ("mark", "Two changes per update, however long the range: up at `l`, down at `r + 1`."),
                    ("build", "One running total over `diff`. At index `i`, it's every `+v` that started at or before `i`, "
                              "minus every `-v` from ranges that already finished. In other words, exactly the updates "
                              "that cover `i`."),
                    ("ret", "The final values. Slot `n` of `diff` is never read; whatever ended up there would only "
                            "affect positions past the end.",
                     {"c": "Free the difference array. The caller owns `result`."}),
                ],
                APPLY_RUN,
                "apply_ranges(8, [[1, 4, 2], [3, 6, 1], [0, 2, 3], [5, 7, 4]])",
            ),
        ]),
        ("trace", "Trace it by hand", [
            """
            Watch `diff` go up and down as each job is marked (bars below the line are negative), then watch the sweep
            turn it into the final array:
            """,
            walk(steps),
            "Here's `diff` (indices 0 to 8) after each update:",
            table(["update", "diff"], *d_rows),
            f"""
            The running total of the last row is `{FINAL}`. Painting every board directly would have taken
            {sum(r - l + 1 for l, r, _ in JOBS)} changes here. With `m` updates over long ranges that grows to `n × m`,
            while the difference array always takes `2m` changes plus one sweep.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Can the bus carry everyone?

            Back to the bus from the start. Say it has {CAP} seats. Mark `+people` where each group gets on and
            `-people` where it gets off, sweep, and check whether the running total ever goes above {CAP}:
            """,
            fig(Bars(board, st={i: ("answer" if b > CAP else "found") for i, b in enumerate(board)}, label="on board after each stop"),
                caption=(f"At stop {OVER} there are {board[OVER]} people on a {CAP}-seat bus, so the answer is no. You can stop the sweep right there."
                         if OVER is not None else f"The load never goes above {CAP}, so yes.")),
            """
            One detail: at a stop where some people get off and others get on, the running total applies both at
            once, so the people leaving free their seats before the new ones sit down. If a problem said the opposite
            (everyone boards first), you'd check the load between the ons and the offs instead.

            ### Lamps along a street, with negative positions
            """,
            f"""
            Lamps at `(position, reach)` = `{LAMPS}` light every point from `position - reach` to `position + reach`.
            How bright is each point? The leftmost lit point is {lo}, which is negative, so we can't use positions as
            indices directly. Shift everything by {-lo}, so point {lo} becomes index 0:
            """,
            fig(Bars(light, labels=range(lo, hi + 1), st={i: "answer" for i, b in enumerate(light) if b == BRIGHT}, label="how many lamps light each point"),
                caption=f"The brightest points ({', '.join(map(str, BRIGHT_AT))}) are lit by {BRIGHT} lamps."),
            """
            The shift is just `index = position - lowest`. Forgetting it is one of the most common bugs with
            difference arrays, because negative indices either crash or (in Python) silently wrap around to the end of
            the list.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Sweeping sorted events

            Meetings `[start, end)` at times up to a billion: what's the most that are ever running at once? An array
            covering every possible time is out of the question, but there are only `2m` events. Sort them and keep a
            running total. Sorting `(time, change)` pairs puts `-1` before `+1` at the same time, which is exactly what
            half-open meetings need: one that ends at 11:00 frees its room before one starting at 11:00 takes it.
            """,
            walk(sweep),
            code(
                "Most meetings at once (sorted events)",
                SWEEP,
                [
                    ("events", "Two events per meeting: `+1` when it starts, `-1` when it ends."),
                    ("sort", "Sort by time. At equal times, `-1` (an end) comes before `+1` (a start).",
                     {"c": "The comparator orders by time with `(a > b) - (a < b)`. Writing `a - b` can overflow for big values.",
                      "java": "`Long.compare` avoids the overflow that `a[0] - b[0]` could cause."}),
                    ("scan", "Go through the events in order. `live` is how many meetings are running just after this event."),
                    ("best", "The busiest moment is the biggest `live` we see. Nothing changes between events, so "
                             "checking at the events is enough."),
                    ("ret", "The most meetings at once.",
                     {"c": "Free the events first."}),
                ],
                SWEEP_RUN,
                "max_overlap([(900, 1030), (1000, 1100), (1030, 1200), (1015, 1045), (1100, 1130)]); [(1, 2), (2, 3), (3, 4)]; huge times",
            ),
            table(["time", "event", "change", "running", "most so far"], *ev_rows),
            f"""
            At 10:30 one meeting ends and another starts. The end goes first, so the count dips before it rises, and
            the answer is {MANS}. Back-to-back meetings `(1, 2), (2, 3), (3, 4)` never overlap, so that one's 1.

            ### Rectangles on a grid

            Four corner changes per rectangle, then running totals along each row and down each column.
            """,
            code(
                "Add values to many rectangles",
                GRID2,
                [
                    ("make", "An `(rows + 1) × (cols + 1)` grid of zeros. The extra row and column catch the corners "
                             "that land just past the edge."),
                    ("mark", "The four corners of every rectangle: `+v`, `-v`, `-v`, `+v`."),
                    ("rows", "Running totals along each row spread every `+v` to the right until its `-v`."),
                    ("cols", "Then running totals down each column spread them downwards. Together that's a 2D prefix sum."),
                    ("ret", "Drop the spare row and column.",
                     {"c": "Copy out the `rows × cols` part and free the working grid."}),
                ],
                GRID2_RUN,
                "paint_rects(4, 5, [[0, 0, 1, 2, 1], [1, 1, 3, 3, 2], [2, 4, 3, 4, 5]])",
            ),
            fig(Grid(PAINT, label="result"), caption="Three rectangles take twelve corner changes and one 2D sweep."),
            """
            ### Updates and questions mixed together

            If you need to read values between updates, keep the difference array inside a Fenwick tree. A range
            update is still two point changes, and reading `A[i]` is a running-total query. Both take O(log n).
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            Updating every element directly costs up to O(n) per update, so O(n × m) for `m` updates. With `n` and `m`
            both 100,000, that's up to {N * N:,} additions.

            A difference array costs O(1) per update plus one O(n) rebuild, so O(n + m) time and O(n) memory.
            Sweeping sorted events costs O(m log m) to sort `2m` events and O(m) memory, however large the positions
            are. In 2D, it's O(1) per rectangle and O(rows × cols) to rebuild.
            """,
            table(
                ["Approach", "Time", "Extra space", "Use it when"],
                ["Update every element", "O(n · m)", "O(1)", "the input is tiny"],
                ["Difference array", "O(n + m)", "O(n)", "positions fit in an array"],
                ["Sorted events (sweep)", "O(m log m)", "O(m)", "positions are huge or not whole numbers"],
                ["Fenwick tree on the differences", "O((m + q) log n)", "O(n)", "you read values between updates"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `diff = [0] * (n + 1)`, and `itertools.accumulate(diff[:n])` rebuilds it in one line. For events, sorting
            `(time, change)` tuples puts ends before starts automatically, since `-1 < 1`. Be careful with negative
            indices: `diff[-1]` doesn't crash, it quietly changes the last element.

            ### Java

            `long[] diff = new long[n + 1]`, because lots of updates on one index can overflow an `int`. Sort events
            with a comparator that uses `Integer.compare` or `Long.compare`, never `a - b`.

            ### C++

            `vector<long long> diff(n + 1)`, and `partial_sum` can do the rebuild. A `vector<pair<int, int>>` of events
            sorts by time and then by change with the default `<`. When positions are sparse, a `std::map<int, long
            long>` of changes, walked in order, is a sweep without an explicit sort.

            ### C

            `calloc(n + 1, sizeof(long long))`. For events, an array of structs and `qsort` with a comparator that
            can't overflow.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            Common mistakes:

            - No spare slot. With `r = n - 1`, `diff[r + 1]` writes past the end unless `diff` has `n + 1` entries.
            - Mixing up inclusive and half-open ranges. Inclusive ranges stop at `r + 1`, half-open ones at `end`. Get
              it wrong and every boundary moves by one.
            - The tie-break in sweeps. At the same position, decide from the problem's wording whether ends or starts
              go first. Does a range ending at 5 overlap one starting at 5?
            - Reading `diff` before the rebuild. It holds changes, not values. Only the running total gives you values.
            - Overflow. Lots of big updates on the same spot need 64 bits.
            - Negative or shifted positions. A lamp at 2 with reach 5 covers -3 to 7. Shift positions so the smallest
              becomes 0, or switch to events.
            - Comparators written as `a - b`. They overflow for values near ±2³¹. Compare instead.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why does `diff` need `n + 1` slots?",
                 "An update ending at the last index, `r = n - 1`, puts its `-v` at index `n`. The rebuild never reads that slot, but it has to exist."),
                ("Show that adding `v` to `A[l..r]` only changes `D[l]` and `D[r + 1]`.",
                 "`D[i] = A[i] - A[i - 1]`. Inside the range both terms went up by `v`, so the difference didn't change. At `l`, only `A[l]` went up, so `D[l]` grows by `v`. At `r + 1`, only `A[r]` went up, so `D[r + 1]` shrinks by `v`. Nothing else changed."),
                ("Meetings `[10, 11)` and `[11, 12)`. With events sorted by `(time, change)`, what's the most running at once, and why?",
                 "1. At 11, the end (`-1`) sorts before the start (`+1`), so the count goes 1, then 0, then 1, and never hits 2. That's right for half-open meetings."),
                ("There are 100,000 updates and 100,000 \"what's `a[i]` now?\" questions, mixed together. Is a plain difference array enough?",
                 "No. Each question would need an O(n) rebuild. Put the difference array in a Fenwick tree instead: two O(log n) changes per update, and `a[i]` is an O(log n) running-total query."),
                ("How are difference arrays and prefix sums related?",
                 "They undo each other. The running total of the difference array gives you back the array, and the differences of the prefix array give you back the original values. Differences make range updates cheap; prefix sums make range questions cheap."),
            ),
        ]),
    ],
)
