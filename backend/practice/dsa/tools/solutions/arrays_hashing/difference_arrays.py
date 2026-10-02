"""Arrays & Hashing: difference arrays."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def brightest_spot():
    lamps = [[2, 3], [6, 1], [4, 1], [10, 2], [5, 2]]
    spans = [(p - r, p + r) for p, r in lamps]
    lo, hi = min(a for a, _ in spans), max(b for _, b in spans)
    pts = list(range(lo, hi + 1))
    bright = [sum(a <= x <= b for a, b in spans) for x in pts]
    best = max(bright)
    at = pts[bright.index(best)]
    assert (best, at) == (4, 5)

    w1 = Steps("Only a lamp's left edge can be the answer. Count the lamps over each left edge.")
    w1.step("Each lamp lights [position − reach, position + reach].", Row([f"{a}…{b}" for a, b in spans], label="lit range per lamp"))
    cands = sorted(set(a for a, _ in spans))
    bsf, bat = -1, None
    for x in cands:
        cnt = sum(a <= x <= b for a, b in spans)
        if cnt > bsf:
            bsf, bat = cnt, x
        w1.step(f"Point {x}: lit by {cnt} lamp{'s' if cnt != 1 else ''}" + (" — a new best." if bat == x else "."),
                Row([f"{a}…{b}" for a, b in spans], st={i: "answer" for i, (a, b) in enumerate(spans) if a <= x <= b}, label="lamps covering it"), Vars(point=x, best=bsf, at=bat))
    w1.step(f"The best is {bsf} lamps, first reached at {bat}.", Row(bright, st={pts.index(bat): "answer"}, label=f"brightness at {lo} … {hi}"), result=bat)

    w2 = Steps("Sort where light starts and where it stops. Walk the starts; brightness = starts passed − stops passed.")
    starts = sorted(a for a, _ in spans)
    stops = sorted(b + 1 for _, b in spans)
    w2.step("A lamp adds 1 from its start and takes it back at end + 1 (the first dark point).", Row(starts, label="starts (sorted)", slots=True), Row(stops, label="stops = end + 1 (sorted)", slots=True))
    j, bsf, bat = 0, -1, None
    i = 0
    n = len(starts)
    while i < n:
        x = starts[i]
        while i + 1 < n and starts[i + 1] == x:
            i += 1
        while j < n and stops[j] <= x:
            j += 1
        b = (i + 1) - j
        if b > bsf:
            bsf, bat = b, x
        w2.step(f"At {x}: {i + 1} lamps have started and {j} have stopped, so {b} are lit" + (" — new best." if bat == x else "."),
                Row(starts, st={q: "found" for q in range(i + 1)}, ptr={"i": i}, label="starts", slots=True), Row(stops, st={q: "dim" for q in range(j)}, ptr={"j": j} if j < n else None, label="stops", slots=True), Vars(lit=b, best=bsf, at=bat))
        i += 1
    w2.step(f"Brightest: {bsf} lamps, first at point {bat}.", Row(bright, st={pts.index(bat): "answer"}, label=f"brightness at {lo} … {hi}"), result=bat)

    sol(
        "brightest-spot",
        summary="""
            Brightness only goes **up** at a lamp's left edge and only goes **down** just past a right edge,
            so the answer is always some lamp's left edge. Sort the start points and the stop points; walking
            the starts in order, the brightness is "starts passed minus stops passed". That's O(n log n), and it
            never touches the (infinitely long) street itself.
        """,
        question=[
            """
            Each lamp `[position, reach]` lights the whole interval `[position − reach, position + reach]`
            (integer points, both ends included). A point's brightness is how many intervals contain it. Find
            the brightest point; if several tie, return the **smallest**.

            - **Endpoints count.** A lamp at 5 with reach 0 lights exactly the point 5.
            - **The street is endless** and positions go from −10⁸ to 10⁸ with reach up to 10⁸, so lit points
              range over about 4 × 10⁸ values. An array with one cell per point would be far too big.
            - **Ties go to the smallest point.** `[[−3, 2], [1, 2], [3, 3]]` lights −1, 0 and 1 with two lamps
              each; the answer is −1.
            - **Size:** up to 10⁵ lamps. All coordinates (including `end + 1`) stay within ±2 × 10⁸ + 1, so
              `int` is enough.
            """
        ],
        think=[
            """
            Take `lamps = [[2, 3], [6, 1], [4, 1], [10, 2], [5, 2]]`. Their lit ranges are −1…5, 5…7, 3…5,
            8…12 and 3…7. Count the brightness at every point from −1 to 12:
            """,
            fig(Row(pts, label="point"), Row(bright, st={pts.index(5): "answer"}, label="brightness"),
                caption="Point 5 is under four lamps. Nothing else reaches 4."),
            """
            Walking left to right, the brightness changes only at two kinds of places: it goes **up by one** at
            a lamp's left edge, and **down by one** just after a lamp's right edge. Between those places it's
            flat.

            So the brightest stretch must **begin** at some left edge (that's where the brightness last went up
            before the peak). The smallest brightest point is therefore one of the n left edges, not one of
            hundreds of millions of points. That cuts the search down to n candidates.

            This is the **difference array** idea (+1 where something starts, −1 just after it ends, then a
            running sum), except the street is too long for an array, so we keep only the places where
            something changes and visit them in sorted order.
            """,
        ],
        approaches=[
            approach(
                "Count the lamps over every left edge",
                "brute",
                "O(n²)",
                "O(1)",
                idea=[
                    """
                    Only left edges can be the answer. For each lamp's left edge `x`, count how many lamps
                    satisfy `start ≤ x ≤ end`. Keep the largest count; on a tie keep the smaller `x`.
                    """
                ],
                walk=w1,
                build=[
                    "For each lamp, take its left edge `x = position − reach`.",
                    "Count lamps whose range contains `x` (a scan over all lamps).",
                    "If the count beats the best, or ties it with a smaller `x`, remember `x`.",
                    "Return the remembered point.",
                ],
                code={
                    "python": """
                        class Solution:
                            def brightestSpot(self, lamps: List[List[int]]) -> int:
                                best, best_at = -1, 0  #@init
                                for p, r in lamps:  #@cand
                                    x = p - r  #@cand
                                    lit = sum(1 for q, s in lamps if q - s <= x <= q + s)  #@count
                                    if lit > best or (lit == best and x < best_at):  #@keep
                                        best, best_at = lit, x  #@keep
                                return best_at  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int brightestSpot(int[][] lamps) {
                                int best = -1, bestAt = 0;  //@init
                                for (int[] a : lamps) {  //@cand
                                    int x = a[0] - a[1];  //@cand
                                    int lit = 0;  //@count
                                    for (int[] b : lamps) if (b[0] - b[1] <= x && x <= b[0] + b[1]) lit++;  //@count
                                    if (lit > best || (lit == best && x < bestAt)) {  //@keep
                                        best = lit;  //@keep
                                        bestAt = x;  //@keep
                                    }
                                }
                                return bestAt;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int brightestSpot(vector<vector<int>>& lamps) {
                                int best = -1, bestAt = 0;  //@init
                                for (auto& a : lamps) {  //@cand
                                    int x = a[0] - a[1];  //@cand
                                    int lit = 0;  //@count
                                    for (auto& b : lamps) if (b[0] - b[1] <= x && x <= b[0] + b[1]) lit++;  //@count
                                    if (lit > best || (lit == best && x < bestAt)) {  //@keep
                                        best = lit;  //@keep
                                        bestAt = x;  //@keep
                                    }
                                }
                                return bestAt;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int brightestSpot(int** lamps, int lampsSize, int* lampsColSize) {
                            int best = -1, bestAt = 0;  //@init
                            for (int i = 0; i < lampsSize; i++) {  //@cand
                                int x = lamps[i][0] - lamps[i][1];  //@cand
                                int lit = 0;  //@count
                                for (int j = 0; j < lampsSize; j++) {  //@count
                                    if (lamps[j][0] - lamps[j][1] <= x && x <= lamps[j][0] + lamps[j][1]) lit++;  //@count
                                }
                                if (lit > best || (lit == best && x < bestAt)) {  //@keep
                                    best = lit;  //@keep
                                    bestAt = x;  //@keep
                                }
                            }
                            return bestAt;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "The best brightness so far (−1 so the first candidate always wins) and where it happens."),
                    ("cand", "Each lamp's left edge is a candidate answer.", {"c": "A 2-D input arrives as an array of row pointers; each row is `[position, reach]`."}),
                    ("count", "How many lamps light this point: those with `start ≤ x ≤ end`."),
                    ("keep", "A brighter point wins; an equally bright but smaller point also wins, which handles the tie rule."),
                    ("ret", "The smallest of the brightest points."),
                ],
                complexity=["**Time O(n²):** n candidates, each checked against n lamps (10¹⁰ at the limit). **Space O(1).**"],
                limits=[
                    """
                    Neighbouring candidates share almost all of their lamps, yet each count starts from scratch.
                    If the candidates are visited in increasing order, the count can be **updated** as lamps
                    switch on and off, instead of recounted.
                    """
                ],
                slow=True,
            ),
            approach(
                "Sweep sorted starts and stops",
                "best",
                "O(n log n)",
                "O(n)",
                idea=[
                    """
                    Make two sorted lists: every lamp's **start** (`position − reach`) and every lamp's **stop**,
                    the first dark point after it (`position + reach + 1`). For any point `x`:

                    `brightness(x) = (starts ≤ x) − (stops ≤ x)`

                    because a lamp lights `x` exactly when it has started and hasn't yet stopped. Walk the starts
                    in increasing order with one pointer `i`, and move a second pointer `j` through the stops
                    while `stops[j] ≤ x`. Both pointers only move forward, so the walk is linear after sorting.

                    Equal starts are handled together (we evaluate after the last of them), and the first `x`
                    that **strictly** beats the best is kept, which makes ties resolve to the smaller point.
                    """
                ],
                walk=w2,
                build=[
                    "Build `starts[k] = p − r` and `stops[k] = p + r + 1`, and sort both.",
                    "Set `j = 0`, `best = −1`. Walk `i` over `starts`.",
                    "Skip ahead while the next start equals this one, so every lamp starting at `x` is counted.",
                    "Advance `j` while `stops[j] ≤ x` (those lamps are already dark at `x`).",
                    "`lit = (i + 1) − j`. If `lit > best`, record `best = lit` and the point `x`.",
                    "Return the recorded point.",
                ],
                code={
                    "python": """
                        class Solution:
                            def brightestSpot(self, lamps: List[List[int]]) -> int:
                                starts = sorted(p - r for p, r in lamps)  #@lists
                                stops = sorted(p + r + 1 for p, r in lamps)  #@lists
                                n = len(starts)
                                best, best_at, j, i = -1, 0, 0, 0  #@init
                                while i < n:  #@walk
                                    x = starts[i]  #@walk
                                    while i + 1 < n and starts[i + 1] == x:  #@same
                                        i += 1  #@same
                                    while j < n and stops[j] <= x:  #@stop
                                        j += 1  #@stop
                                    lit = (i + 1) - j  #@lit
                                    if lit > best:  #@keep
                                        best, best_at = lit, x  #@keep
                                    i += 1  #@walk
                                return best_at  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int brightestSpot(int[][] lamps) {
                                int n = lamps.length;
                                int[] starts = new int[n], stops = new int[n];  //@lists
                                for (int k = 0; k < n; k++) {  //@lists
                                    starts[k] = lamps[k][0] - lamps[k][1];  //@lists
                                    stops[k] = lamps[k][0] + lamps[k][1] + 1;  //@lists
                                }  //@lists
                                Arrays.sort(starts);  //@lists
                                Arrays.sort(stops);  //@lists
                                int best = -1, bestAt = 0, j = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@walk
                                    int x = starts[i];  //@walk
                                    while (i + 1 < n && starts[i + 1] == x) i++;  //@same
                                    while (j < n && stops[j] <= x) j++;  //@stop
                                    int lit = (i + 1) - j;  //@lit
                                    if (lit > best) {  //@keep
                                        best = lit;  //@keep
                                        bestAt = x;  //@keep
                                    }
                                }
                                return bestAt;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int brightestSpot(vector<vector<int>>& lamps) {
                                int n = lamps.size();
                                vector<int> starts(n), stops(n);  //@lists
                                for (int k = 0; k < n; k++) {  //@lists
                                    starts[k] = lamps[k][0] - lamps[k][1];  //@lists
                                    stops[k] = lamps[k][0] + lamps[k][1] + 1;  //@lists
                                }  //@lists
                                sort(starts.begin(), starts.end());  //@lists
                                sort(stops.begin(), stops.end());  //@lists
                                int best = -1, bestAt = 0, j = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@walk
                                    int x = starts[i];  //@walk
                                    while (i + 1 < n && starts[i + 1] == x) i++;  //@same
                                    while (j < n && stops[j] <= x) j++;  //@stop
                                    int lit = (i + 1) - j;  //@lit
                                    if (lit > best) {  //@keep
                                        best = lit;  //@keep
                                        bestAt = x;  //@keep
                                    }
                                }
                                return bestAt;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@cmp
                            int p = *(const int*) a, q = *(const int*) b;  //@cmp
                            return (p > q) - (p < q);  //@cmp
                        }  //@cmp

                        int brightestSpot(int** lamps, int lampsSize, int* lampsColSize) {
                            int n = lampsSize;
                            int* starts = malloc(n * sizeof(int));  //@lists
                            int* stops = malloc(n * sizeof(int));  //@lists
                            for (int k = 0; k < n; k++) {  //@lists
                                starts[k] = lamps[k][0] - lamps[k][1];  //@lists
                                stops[k] = lamps[k][0] + lamps[k][1] + 1;  //@lists
                            }  //@lists
                            qsort(starts, n, sizeof(int), cmpInt);  //@lists
                            qsort(stops, n, sizeof(int), cmpInt);  //@lists
                            int best = -1, bestAt = 0, j = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@walk
                                int x = starts[i];  //@walk
                                while (i + 1 < n && starts[i + 1] == x) i++;  //@same
                                while (j < n && stops[j] <= x) j++;  //@stop
                                int lit = (i + 1) - j;  //@lit
                                if (lit > best) {  //@keep
                                    best = lit;  //@keep
                                    bestAt = x;  //@keep
                                }
                            }
                            free(starts);  //@ret
                            free(stops);  //@ret
                            return bestAt;  //@ret
                        }
                    """,
                },
                lines=[
                    ("cmp", "Comparator for `qsort`: −1, 0 or 1, without the overflow risk of subtracting."),
                    ("lists", "Where each lamp's light begins, and the first point after it ends. Using `end + 1` means \"lit at x\" is exactly `start ≤ x < stop`, so both lists can be compared with `≤ x`. Values stay within ±2 × 10⁸ + 1."),
                    ("init", "`j` counts stops at or before the current point; `best` starts below any real brightness."),
                    ("walk", "Candidate points are the starts, in increasing order."),
                    ("same", "Several lamps can start at the same point. Jump `i` to the last of them so all of them are counted as started."),
                    ("stop", "Every lamp whose stop is at or before `x` is dark at `x`. `j` only moves forward because `x` only increases."),
                    ("lit", "`i + 1` lamps have started by `x`, and `j` of them have stopped: the rest are on."),
                    ("keep", "Only a strictly brighter point replaces the answer. Points are visited smallest first, so a tie keeps the earlier, smaller point."),
                    ("ret", "The smallest brightest point.", {"c": "Free both lists first."}),
                ],
                complexity=[
                    """
                    **Time O(n log n):** two sorts; the walk is O(n) because `i` and `j` each move at most n
                    times.

                    **Space O(n)** for the two lists.

                    With the street this long, sorting the change points is the right tool: a true
                    difference array would need hundreds of millions of cells.
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - Coverage counts change only at interval **edges**. Think "+1 at start, −1 just after the end,
              running sum": the difference-array idea.
            - When the coordinate range is too large for an array, keep only the edge points, **sort** them, and
              sweep (this is coordinate compression in disguise).
            - "Lit at x" = `starts ≤ x` minus `stops ≤ x` with `stop = end + 1`. The +1 turns an inclusive end
              into an exclusive one and avoids off-by-one errors.
            - For "smallest point with the max", visit points in increasing order and replace only on a
              strict improvement.
            """
        ],
    )


@problem
def shuttle_seats():
    capacity, trips = 6, [[2, 1, 5], [3, 3, 7], [4, 5, 8]]
    last = max(t[2] for t in trips)
    onboard = [sum(p for p, a, b in trips if a <= m < b) for m in range(last + 1)]
    assert max(onboard) == 7

    w1 = Steps("At every mark, add up everyone on board.")
    w1.step(f"Capacity {capacity}. Trips: 2 people 1→5, 3 people 3→7, 4 people 5→8.", Row(list(range(last + 1)), label="mark"), Vars(capacity=capacity))
    for m in range(last + 1):
        on = [(p, a, b) for p, a, b in trips if a <= m < b]
        total = sum(p for p, _, _ in on)
        st = {q: "found" for q in range(m)}
        st[m] = "mark" if total > capacity else "active"
        w1.step(f"Mark {m}: " + (" + ".join(f"{p} ({a}→{b})" for p, a, b in on) or "nobody") + f" = {total}" + (" > 6. Over capacity." if total > capacity else "."),
                Row(onboard[:m + 1] + [None] * (last - m), st=st, label="people on board", slots=True), Vars(on_board=total))
        if total > capacity:
            w1.step("So the answer is false.", Row(onboard[:m + 1] + [None] * (last - m), st={m: "mark"}, label="people on board", slots=True), result=False)
            break

    w2 = Steps("Turn trips into get-on and get-off events, sort them, and keep a running count.")
    ev = sorted([(a, p) for p, a, b in trips] + [(b, -p) for p, a, b in trips])
    w2.step("Each trip is two events: +people at 'from', −people at 'to'. At the same mark, −'s sort first: off before on.", Row([f"{m}:{'+' if d > 0 else ''}{d}" for m, d in ev], label="events (mark: change)"))
    on = 0
    for k, (m, d) in enumerate(ev):
        on += d
        st = {q: "found" for q in range(k)}
        st[k] = "mark" if on > capacity else "active"
        w2.step(f"Mark {m}: {'+' if d > 0 else ''}{d} → {on} on board" + (" > 6. Over capacity." if on > capacity else "."), Row([f"{mm}:{'+' if dd > 0 else ''}{dd}" for mm, dd in ev], st=st, label="events"), Vars(on_board=on))
        if on > capacity:
            break
    w2.step("False.", Row([f"{mm}:{'+' if dd > 0 else ''}{dd}" for mm, dd in ev], st={k: "mark"}, label="events"), result=False)

    w3 = Steps("One array slot per mark: +people where a party boards, −people where it leaves. A running sum gives the load.")
    change = [0] * (last + 1)
    w3.step("change[m] starts at 0 for every mark.", Row(change, label="change", slots=True))
    for p, a, b in trips:
        change[a] += p
        change[b] -= p
        w3.step(f"Trip of {p} from {a} to {b}: change[{a}] += {p}, change[{b}] −= {p}.", Row(list(change), st={a: "new", b: "new"}, label="change", slots=True))
    run = 0
    sums = []
    for m in range(last + 1):
        run += change[m]
        sums.append(run)
        st = {m: "mark" if run > capacity else "active"}
        w3.step(f"Running sum at mark {m}: {run}" + (" > 6. Over capacity." if run > capacity else "."), Row(change, st={m: "active"}, label="change", slots=True), Row(sums + [None] * (last - m), st=st, label="on board", slots=True))
        if run > capacity:
            break
    w3.step("False: at mark 5 there would be 7 people.", Row(sums + [None] * (last - m), st={m: "mark"}, label="on board", slots=True), result=False)

    sol(
        "shuttle-seats",
        summary="""
            The shuttle only moves forward, so all that matters is the number of people on board at each mark.
            Record "+p at boarding, −p at leaving" in an array indexed by mark, then a running sum gives the load
            at every mark in one pass: O(trips + marks).
        """,
        question=[
            """
            A shuttle drives forward past marks 0, 1, 2, … A trip `[p, from, to]` puts `p` people on board from
            mark `from` until mark `to`. Return whether the number on board ever exceeds `capacity`.

            - **People get off before others get on** at the same mark. So a party riding 0 → 2 and another
              riding 2 → 4 never share the shuttle: at mark 2 the first leaves, then the second boards. A party
              is on board for marks `from … to − 1`.
            - **Only the peak matters.** You return true/false, not the schedule.
            - **Size:** up to 10⁵ trips, marks up to 10⁵, at most 100 people per trip. The load can reach
              10⁷, which fits in an `int`.
            """
        ],
        think=[
            """
            Take capacity 6 and trips `[[2, 1, 5], [3, 3, 7], [4, 5, 8]]`. Track the load mark by mark:
            """,
            fig(Row(list(range(last + 1)), label="mark"), Row(onboard, st={5: "mark", 6: "mark"}, label="people on board"),
                caption="At mark 5 the party of 2 leaves and the party of 4 boards: 3 + 4 = 7 > 6."),
            """
            Notice what changes the load: only boarding (`+p` at `from`) and leaving (`−p` at `to`). Between
            those marks it stays flat. So instead of recounting every party at every mark, write down the
            **changes** and add them up as you drive:

            - change[1] = +2, change[3] = +3, change[5] = −2 + 4 = +2, change[7] = −3, change[8] = −4.
            - Running sum: 0, 2, 2, 5, 5, **7**, 7, 4, 0.

            That's the difference-array trick: a range update becomes two point updates, and one prefix-sum
            pass rebuilds every value.
            """,
        ],
        approaches=[
            approach(
                "Recount the riders at every mark",
                "brute",
                "O(M · T)",
                "O(1)",
                idea=["For each mark `m` up to the last drop-off, add up the parties with `from ≤ m < to`. If any total exceeds the capacity, return false."],
                walk=w1,
                build=[
                    "Find the last mark, `max(to)`.",
                    "For each mark `m` from 0 to it: sum `p` over trips with `from ≤ m < to`.",
                    "If the sum exceeds `capacity`, return false. After all marks, return true.",
                ],
                code={
                    "python": """
                        class Solution:
                            def canCarryAll(self, capacity: int, trips: List[List[int]]) -> bool:
                                last = max(t[2] for t in trips)  #@last
                                for m in range(last + 1):  #@marks
                                    load = sum(p for p, a, b in trips if a <= m < b)  #@load
                                    if load > capacity:  #@check
                                        return False  #@check
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean canCarryAll(int capacity, int[][] trips) {
                                int last = 0;  //@last
                                for (int[] t : trips) last = Math.max(last, t[2]);  //@last
                                for (int m = 0; m <= last; m++) {  //@marks
                                    int load = 0;  //@load
                                    for (int[] t : trips) if (t[1] <= m && m < t[2]) load += t[0];  //@load
                                    if (load > capacity) return false;  //@check
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool canCarryAll(int capacity, vector<vector<int>>& trips) {
                                int last = 0;  //@last
                                for (auto& t : trips) last = max(last, t[2]);  //@last
                                for (int m = 0; m <= last; m++) {  //@marks
                                    int load = 0;  //@load
                                    for (auto& t : trips) if (t[1] <= m && m < t[2]) load += t[0];  //@load
                                    if (load > capacity) return false;  //@check
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool canCarryAll(int capacity, int** trips, int tripsSize, int* tripsColSize) {
                            int last = 0;  //@last
                            for (int i = 0; i < tripsSize; i++) if (trips[i][2] > last) last = trips[i][2];  //@last
                            for (int m = 0; m <= last; m++) {  //@marks
                                int load = 0;  //@load
                                for (int i = 0; i < tripsSize; i++) {  //@load
                                    if (trips[i][1] <= m && m < trips[i][2]) load += trips[i][0];  //@load
                                }
                                if (load > capacity) return false;  //@check
                            }
                            return true;  //@ret
                        }
                    """,
                },
                lines=[
                    ("last", "No one rides past the last drop-off, so marks beyond it don't matter."),
                    ("marks", "Check every mark the shuttle passes."),
                    ("load", "A party is aboard at `m` when it boarded at or before `m` and leaves after `m`. `m < to` (not `≤`) is the \"off before on\" rule."),
                    ("check", "One overloaded mark is enough to fail."),
                    ("ret", "No mark was over capacity."),
                ],
                complexity=["**Time O(M · T)** for M marks and T trips: 10⁵ × 10⁵ = 10¹⁰ in the worst case. **Space O(1).**"],
                limits=["Each mark recounts every trip, although from one mark to the next only the parties boarding or leaving there change the load."],
                slow=True,
            ),
            approach(
                "Sort boarding and leaving events",
                "better",
                "O(T log T)",
                "O(T)",
                idea=[
                    """
                    Each trip becomes two events: `(from, +p)` and `(to, −p)`. Sort by mark, and at equal marks put
                    the negative changes first (people get off before others get on). Then walk the events with a
                    running load; if it ever exceeds the capacity, return false.

                    This never looks at marks where nothing happens, so it works even if marks were huge.
                    """
                ],
                walk=w2,
                build=[
                    "Make a list of `(mark, change)` pairs: `(from, +p)` and `(to, −p)` per trip.",
                    "Sort by mark, then by change (so −p comes before +p at the same mark).",
                    "Add the changes in order; if the running load exceeds `capacity`, return false.",
                    "Return true.",
                ],
                code={
                    "python": """
                        class Solution:
                            def canCarryAll(self, capacity: int, trips: List[List[int]]) -> bool:
                                events = []  #@events
                                for p, a, b in trips:  #@events
                                    events.append((a, p))  #@events
                                    events.append((b, -p))  #@events
                                events.sort()  #@sort
                                load = 0  #@sweep
                                for _, change in events:  #@sweep
                                    load += change  #@sweep
                                    if load > capacity:  #@check
                                        return False  #@check
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean canCarryAll(int capacity, int[][] trips) {
                                int[][] events = new int[2 * trips.length][];  //@events
                                for (int i = 0; i < trips.length; i++) {  //@events
                                    events[2 * i] = new int[] {trips[i][1], trips[i][0]};  //@events
                                    events[2 * i + 1] = new int[] {trips[i][2], -trips[i][0]};  //@events
                                }
                                Arrays.sort(events, (x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0]) : Integer.compare(x[1], y[1]));  //@sort
                                int load = 0;  //@sweep
                                for (int[] e : events) {  //@sweep
                                    load += e[1];  //@sweep
                                    if (load > capacity) return false;  //@check
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool canCarryAll(int capacity, vector<vector<int>>& trips) {
                                vector<pair<int, int>> events;  //@events
                                for (auto& t : trips) {  //@events
                                    events.push_back({t[1], t[0]});  //@events
                                    events.push_back({t[2], -t[0]});  //@events
                                }
                                sort(events.begin(), events.end());  //@sort
                                int load = 0;  //@sweep
                                for (auto& [mark, change] : events) {  //@sweep
                                    load += change;  //@sweep
                                    if (load > capacity) return false;  //@check
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int mark, change; } Event;  //@type

                        static int byMarkThenChange(const void* a, const void* b) {  //@type
                            const Event* x = a;  //@type
                            const Event* y = b;  //@type
                            if (x->mark != y->mark) return (x->mark > y->mark) - (x->mark < y->mark);  //@type
                            return (x->change > y->change) - (x->change < y->change);  //@type
                        }  //@type

                        bool canCarryAll(int capacity, int** trips, int tripsSize, int* tripsColSize) {
                            Event* events = malloc(2 * tripsSize * sizeof(Event));  //@events
                            for (int i = 0; i < tripsSize; i++) {  //@events
                                events[2 * i] = (Event) {trips[i][1], trips[i][0]};  //@events
                                events[2 * i + 1] = (Event) {trips[i][2], -trips[i][0]};  //@events
                            }
                            qsort(events, 2 * tripsSize, sizeof(Event), byMarkThenChange);  //@sort
                            int load = 0;  //@sweep
                            bool ok = true;  //@sweep
                            for (int i = 0; i < 2 * tripsSize && ok; i++) {  //@sweep
                                load += events[i].change;  //@sweep
                                if (load > capacity) ok = false;  //@check
                            }
                            free(events);  //@ret
                            return ok;  //@ret
                        }
                    """,
                },
                lines=[
                    ("type", "An event is a mark and a change in load. The comparator orders by mark, then by change, so at the same mark negative changes (drop-offs) come first."),
                    ("events", "Two events per trip: boarding adds `p`, leaving removes `p`."),
                    ("sort", "Order the events along the road. Ties at one mark: smaller change first, so `−p` before `+p`: off before on.",
                     {"python": "Tuples compare by mark first, then by change, which is exactly the order we need.",
                      "cpp": "Pairs compare by `first`, then `second`: mark, then change."}),
                    ("sweep", "Apply the changes in road order; `load` is the number on board right after each event."),
                    ("check", "Any moment over capacity fails.", {"c": "`ok` lets the loop stop early and still free the array."}),
                    ("ret", "The load never went over capacity."),
                ],
                complexity=["**Time O(T log T)** for sorting 2T events. **Space O(T)** for the events."],
                limits=[
                    """
                    Sorting is needed only because the events arrive in random order. Here the marks are small
                    integers (≤ 10⁵), so they can index an array directly, which puts every event in place
                    without sorting.
                    """
                ],
            ),
            approach(
                "Difference array over the marks",
                "best",
                "O(T + M)",
                "O(M)",
                idea=[
                    """
                    Make an array `change` with one slot per mark. For each trip, `change[from] += p` and
                    `change[to] −= p`. Walking the marks in order with a running sum gives the load at each
                    mark: at mark `m` it equals all boardings at marks ≤ m minus all drop-offs at marks ≤ m.

                    "Off before on" is automatic: at one mark the `+` and `−` are already combined into a single
                    number, so a party leaving and a party boarding at the same mark never overlap.
                    """
                ],
                walk=w3,
                build=[
                    "Find the last mark and make `change` with that many slots + 1, all zero.",
                    "For each trip: `change[from] += p`, `change[to] −= p`.",
                    "Walk `m` from 0 up, adding `change[m]` to `load`; return false as soon as `load > capacity`.",
                    "Return true.",
                ],
                code={
                    "python": """
                        class Solution:
                            def canCarryAll(self, capacity: int, trips: List[List[int]]) -> bool:
                                last = max(t[2] for t in trips)  #@size
                                change = [0] * (last + 1)  #@size
                                for p, a, b in trips:  #@mark
                                    change[a] += p  #@mark
                                    change[b] -= p  #@mark
                                load = 0  #@sum
                                for c in change:  #@sum
                                    load += c  #@sum
                                    if load > capacity:  #@check
                                        return False  #@check
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean canCarryAll(int capacity, int[][] trips) {
                                int last = 0;  //@size
                                for (int[] t : trips) last = Math.max(last, t[2]);  //@size
                                int[] change = new int[last + 1];  //@size
                                for (int[] t : trips) {  //@mark
                                    change[t[1]] += t[0];  //@mark
                                    change[t[2]] -= t[0];  //@mark
                                }
                                int load = 0;  //@sum
                                for (int c : change) {  //@sum
                                    load += c;  //@sum
                                    if (load > capacity) return false;  //@check
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool canCarryAll(int capacity, vector<vector<int>>& trips) {
                                int last = 0;  //@size
                                for (auto& t : trips) last = max(last, t[2]);  //@size
                                vector<int> change(last + 1, 0);  //@size
                                for (auto& t : trips) {  //@mark
                                    change[t[1]] += t[0];  //@mark
                                    change[t[2]] -= t[0];  //@mark
                                }
                                int load = 0;  //@sum
                                for (int c : change) {  //@sum
                                    load += c;  //@sum
                                    if (load > capacity) return false;  //@check
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool canCarryAll(int capacity, int** trips, int tripsSize, int* tripsColSize) {
                            int last = 0;  //@size
                            for (int i = 0; i < tripsSize; i++) if (trips[i][2] > last) last = trips[i][2];  //@size
                            int* change = calloc(last + 1, sizeof(int));  //@size
                            for (int i = 0; i < tripsSize; i++) {  //@mark
                                change[trips[i][1]] += trips[i][0];  //@mark
                                change[trips[i][2]] -= trips[i][0];  //@mark
                            }
                            int load = 0;  //@sum
                            bool ok = true;  //@sum
                            for (int m = 0; m <= last && ok; m++) {  //@sum
                                load += change[m];  //@sum
                                if (load > capacity) ok = false;  //@check
                            }
                            free(change);  //@ret
                            return ok;  //@ret
                        }
                    """,
                },
                lines=[
                    ("size", "One slot per mark up to the last drop-off, all starting at 0.", {"c": "`calloc` zeroes the slots."}),
                    ("mark", "A trip changes the load in exactly two places: up by `p` where it boards, down by `p` where it leaves. The marks in between need no update: that's the whole trick."),
                    ("sum", "The running sum of changes up to mark `m` is the number of people on board just after the shuttle leaves mark `m`."),
                    ("check", "Over capacity anywhere means it can't carry everyone.", {"c": "`ok` stops the loop and still lets us free the array."}),
                    ("ret", "Every mark was within capacity."),
                ],
                complexity=[
                    """
                    **Time O(T + M):** two writes per trip, then one pass over at most 10⁵ + 1 marks.

                    **Space O(M)** for the `change` array.
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - **Range add, then read everything once?** Use a difference array: `+v` at the start, `−v` just
              past the end, then a running sum.
            - Exclusive ends (`to` is the first mark the party is *not* on board) make "off before on" fall out
              naturally.
            - If the coordinates are too large or sparse for an array, sort the events instead (the
              **Brightest Spot** approach).
            """
        ],
    )


@problem
def stadium_sections():
    n, groups = 6, [[0, 2, 10], [1, 4, 5], [3, 5, 2]]
    expect = [0] * n
    for l, r, p in groups:
        for i in range(l, r + 1):
            expect[i] += p
    assert expect == [10, 15, 15, 7, 7, 2]

    w1 = Steps("Add each group to every section it covers, one section at a time.")
    out = [0] * n
    w1.step("Six sections, all empty.", Row(out, slots=True))
    for l, r, p in groups:
        for i in range(l, r + 1):
            out[i] += p
        w1.step(f"Group {l}…{r} with {p} fans: {r - l + 1} sections each get +{p}.", Row(list(out), st={i: "new" for i in range(l, r + 1)}, slots=True))
    w1.step("Done. Each group cost as many updates as it has sections.", Row(out, slots=True), result=out)

    w2 = Steps("Mark only where each group starts (+fans) and where it stops (−fans), then take a running sum.")
    diff = [0] * (n + 1)
    w2.step("A difference array with one extra slot at the end.", Row(diff, slots=True, label="diff"))
    for l, r, p in groups:
        diff[l] += p
        diff[r + 1] -= p
        w2.step(f"Group {l}…{r}, {p} fans: diff[{l}] += {p}, diff[{r + 1}] −= {p}.", Row(list(diff), st={l: "new", r + 1: "new"}, slots=True, label="diff"))
    run, res = 0, []
    for i in range(n):
        run += diff[i]
        res.append(run)
        w2.step(f"Section {i}: running sum {run}.", Row(diff, st={i: "active"}, slots=True, label="diff"), Row(res + [None] * (n - i - 1), st={i: "new"}, slots=True, label="fans"))
    w2.step(f"Answer {res}.", Row(res, slots=True, label="fans"), result=res)

    sol(
        "stadium-sections",
        summary="""
            Adding a group to every section in its range costs up to n per group. Instead, write `+people` at
            the range's first section and `−people` just past its last; a single running sum afterwards gives
            every section's total. O(n + groups) instead of O(n · groups).
        """,
        question=[
            """
            There are `n` sections (0 to n − 1). Each group `[l, r, people]` adds `people` fans to **every**
            section from `l` to `r`, both included. Return the final count for every section.

            - **Every section in the range gets the full amount**: `[1, 4, 5]` adds 5 to sections 1, 2, 3
              and 4 (it doesn't split 5 fans among them).
            - **Ranges overlap** and simply add up.
            - **Size:** up to 10⁵ sections and 10⁵ groups, each possibly covering the whole stadium, so doing
              each group section by section can be 10¹⁰ updates. The largest total is 10⁵ × 10⁴ = 10⁹, which
              still fits in an `int`.
            """
        ],
        think=[
            """
            Take `n = 6` and groups `[0, 2, 10]`, `[1, 4, 5]`, `[3, 5, 2]`. The answer is
            `[10, 15, 15, 7, 7, 2]`.

            Read the answer left to right and ask: **where does it change, and by how much?** It starts at 10
            (group 1 starts), goes up 5 at section 1 (group 2 starts), down 10 at section 3 (group 1 ended at 2)
            and up 2 there (group 3 starts), then down 5 at section 5 (group 2 ended at 4).
            """,
            fig(Row(expect, label="fans", slots=True), Row([10, 5, 0, -8, 0, -5, -2], label="change from the previous section", slots=True),
                caption="Each group causes exactly two changes: +people at l and −people at r + 1."),
            """
            So instead of touching every section of a group, record just its **two changes**. After all groups
            are recorded, a running sum over the changes rebuilds the counts. The slot at index `n` collects the
            "−people" of groups ending at the last section; it's never read.
            """,
        ],
        approaches=[
            approach(
                "Add each group section by section",
                "brute",
                "O(n · g)",
                "O(1)",
                idea=["Start with zeros. For each group, loop over its sections and add its fans to each. It's the statement turned into code."],
                walk=w1,
                build=["Make `out` with n zeros.", "For each group `[l, r, p]`, add `p` to `out[l] … out[r]`.", "Return `out`."],
                code={
                    "python": """
                        class Solution:
                            def sectionCounts(self, n: int, groups: List[List[int]]) -> List[int]:
                                out = [0] * n  #@init
                                for l, r, people in groups:  #@groups
                                    for i in range(l, r + 1):  #@add
                                        out[i] += people  #@add
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] sectionCounts(int n, int[][] groups) {
                                int[] out = new int[n];  //@init
                                for (int[] g : groups) {  //@groups
                                    for (int i = g[0]; i <= g[1]; i++) out[i] += g[2];  //@add
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sectionCounts(int n, vector<vector<int>>& groups) {
                                vector<int> out(n, 0);  //@init
                                for (auto& g : groups) {  //@groups
                                    for (int i = g[0]; i <= g[1]; i++) out[i] += g[2];  //@add
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* sectionCounts(int n, int** groups, int groupsSize, int* groupsColSize, int* returnSize) {
                            int* out = calloc(n, sizeof(int));  //@init
                            for (int k = 0; k < groupsSize; k++) {  //@groups
                                for (int i = groups[k][0]; i <= groups[k][1]; i++) out[i] += groups[k][2];  //@add
                            }
                            *returnSize = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Every section starts empty.", {"c": "`calloc` gives n zeroed counters; the caller frees them."}),
                    ("groups", "One group at a time."),
                    ("add", "Every section from `l` to `r` inclusive gets the group's fans."),
                    ("ret", "The totals.", {"c": "Report the length in `returnSize`."}),
                ],
                complexity=["**Time O(n · g):** a group can cover all n sections, so up to 10¹⁰ additions. **Space O(1)** beyond the output."],
                limits=["The work per group is the length of its range, even though the group only *changes* the running total in two places."],
                slow=True,
            ),
            approach(
                "Difference array",
                "best",
                "O(n + g)",
                "O(n)",
                idea=[
                    """
                    Keep `diff` of size `n + 1`. A group `[l, r, p]` does `diff[l] += p` and `diff[r + 1] −= p`.
                    Then section `i`'s total is `diff[0] + diff[1] + … + diff[i]`: each group whose range covers
                    `i` added its `+p` at or before `i` and hasn't yet subtracted it (its `−p` sits after `i`),
                    while groups that ended before `i` have contributed `+p − p = 0`.
                    """
                ],
                walk=w2,
                build=[
                    "Make `diff` with n + 1 zeros (the extra slot takes `r + 1 = n`).",
                    "For each group: `diff[l] += p`, `diff[r + 1] −= p`.",
                    "Walk i from 0 to n − 1 with a running sum of `diff[i]`; that sum is section i's total.",
                ],
                code={
                    "python": """
                        class Solution:
                            def sectionCounts(self, n: int, groups: List[List[int]]) -> List[int]:
                                diff = [0] * (n + 1)  #@diff
                                for l, r, people in groups:  #@mark
                                    diff[l] += people  #@mark
                                    diff[r + 1] -= people  #@mark
                                out, running = [], 0  #@sum
                                for i in range(n):  #@sum
                                    running += diff[i]  #@sum
                                    out.append(running)  #@sum
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] sectionCounts(int n, int[][] groups) {
                                int[] diff = new int[n + 1];  //@diff
                                for (int[] g : groups) {  //@mark
                                    diff[g[0]] += g[2];  //@mark
                                    diff[g[1] + 1] -= g[2];  //@mark
                                }
                                int[] out = new int[n];  //@sum
                                int running = 0;  //@sum
                                for (int i = 0; i < n; i++) {  //@sum
                                    running += diff[i];  //@sum
                                    out[i] = running;  //@sum
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sectionCounts(int n, vector<vector<int>>& groups) {
                                vector<int> diff(n + 1, 0);  //@diff
                                for (auto& g : groups) {  //@mark
                                    diff[g[0]] += g[2];  //@mark
                                    diff[g[1] + 1] -= g[2];  //@mark
                                }
                                vector<int> out(n);  //@sum
                                int running = 0;  //@sum
                                for (int i = 0; i < n; i++) {  //@sum
                                    running += diff[i];  //@sum
                                    out[i] = running;  //@sum
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* sectionCounts(int n, int** groups, int groupsSize, int* groupsColSize, int* returnSize) {
                            int* diff = calloc(n + 1, sizeof(int));  //@diff
                            for (int k = 0; k < groupsSize; k++) {  //@mark
                                diff[groups[k][0]] += groups[k][2];  //@mark
                                diff[groups[k][1] + 1] -= groups[k][2];  //@mark
                            }
                            int* out = malloc(n * sizeof(int));  //@sum
                            int running = 0;  //@sum
                            for (int i = 0; i < n; i++) {  //@sum
                                running += diff[i];  //@sum
                                out[i] = running;  //@sum
                            }
                            free(diff);  //@ret
                            *returnSize = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("diff", "One slot per section plus one: a group ending at the last section writes its `−people` into index n."),
                    ("mark", "Two writes per group no matter how wide it is: start counting its fans at `l`, stop counting them after `r`."),
                    ("sum", "The running sum of `diff` up to `i` is exactly the fans of every group covering `i`. Partial sums never exceed the final maximum of 10⁹, so `int` is safe."),
                    ("ret", "Every section's total.", {"c": "Free `diff`, report the length; the caller frees `out`."}),
                ],
                complexity=["**Time O(n + g):** two writes per group, one pass over the sections. **Space O(n)** for `diff`."],
            ),
        ],
        takeaways=[
            """
            - Many "add v to a range" updates followed by reading all values: **difference array**, O(1) per
              update plus one prefix-sum pass.
            - Size it `n + 1` so `r + 1` never falls off the end.
            - The reverse also holds: a prefix sum undoes a difference array, and a difference array undoes a
              prefix sum. Recognising which one you need is half the problem.
            """
        ],
    )
