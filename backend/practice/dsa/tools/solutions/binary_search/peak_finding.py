"""Binary Search: peaks and mountains."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def slope_walk(W, h):
    lo, hi = 0, len(h) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        up = h[mid] < h[mid + 1]
        W.step(f"lo={lo}, hi={hi}, mid={mid}: {h[mid]} " + ("<" if up else ">") + f" {h[mid + 1]}, so the trail " + ("rises after mid: a summit lies to the right, lo = " + str(mid + 1) if up else "falls after mid: a summit lies at mid or to its left, hi = " + str(mid)) + ".", Row(h, st={k: "dim" for k in range(len(h)) if k < lo or k > hi} | {mid: "active", mid + 1: "mark"}, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
        if up:
            lo = mid + 1
        else:
            hi = mid
    return lo


@problem
def mountain_top():
    e = [1, 4, 6, 9, 13, 11, 7, 2]
    top = e.index(max(e))

    w1 = Steps("Walk up the trail until the next point is lower.")
    for i in range(len(e) - 1):
        if e[i] > e[i + 1]:
            w1.step(f"{e[i]} > {e[i + 1]}: the trail starts falling, so index {i} is the top.", Row(e, st={i: "answer"}, slots=True), result=i)
            break
        w1.step(f"{e[i]} < {e[i + 1]}: still rising.", Row(e, st={i: "active"}, slots=True))

    w2 = Steps("Look at the slope at mid: rising means the top is to the right, falling means it's at mid or to the left.")
    r = slope_walk(w2, e)
    w2.step(f"lo = hi = {r}: the top.", Row(e, st={r: "answer"}, slots=True), result=r)

    sol(
        "mountain-top",
        summary="""
            On a mountain, every point before the top is followed by a higher point and every point from the top onward
            by a lower one. Comparing `e[mid]` with `e[mid + 1]` tells you which side of the top mid is on, so binary
            search finds the top in O(log n).
        """,
        question=[
            """
            Elevations rise strictly to one top and then fall strictly; the top is never at either end. Return its index
            in O(log n).

            - **Strictly** rising and falling: no flat stretches, so "next is higher" is a clean yes/no.
            - **Exactly one top**, never at index 0 or n − 1.
            """
        ],
        think=[
            f"""
            Take `{e}`. Ask, for each point, "is the next point higher?": yes, yes, yes, yes, then no from the top
            onwards.
            """,
            fig(Row(e, st={top: "answer"}, slots=True), Row(["yes" if e[i] < e[i + 1] else "no" for i in range(len(e) - 1)] + ["–"], label="next is higher?"), caption="The answers flip from yes to no exactly at the top."),
            """
            A yes/no question that flips once is exactly what binary search finds. At `mid`: if `e[mid] < e[mid + 1]`
            we're on the way up, so the top is to the right (`lo = mid + 1`); otherwise we're at the top or past it
            (`hi = mid`). Using `mid + 1` is always safe because `mid < hi ≤ n − 1`.
            """,
        ],
        approaches=[
            approach(
                "Walk up until it falls",
                "brute",
                "O(n)",
                "O(1)",
                idea=["Return the first index whose next point is lower."],
                walk=w1,
                build=["For i from 0: if `e[i] > e[i + 1]`, return i."],
                code={
                    "python": """
                        class Solution:
                            def mountainTop(self, elevations: List[int]) -> int:
                                i = 0  #@walk
                                while elevations[i] < elevations[i + 1]:  #@walk
                                    i += 1  #@walk
                                return i  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int mountainTop(int[] elevations) {
                                int i = 0;  //@walk
                                while (elevations[i] < elevations[i + 1]) i++;  //@walk
                                return i;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int mountainTop(vector<int>& elevations) {
                                int i = 0;  //@walk
                                while (elevations[i] < elevations[i + 1]) i++;  //@walk
                                return i;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int mountainTop(int* elevations, int elevationsSize) {
                            int i = 0;  //@walk
                            while (elevations[i] < elevations[i + 1]) i++;  //@walk
                            return i;  //@ret
                        }
                    """,
                },
                lines=[("walk", "Climb while the next point is higher. The top is never the last point, so `i + 1` stays in range."), ("ret", "The first point followed by a lower one.")],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Climbs one step at a time; the required O(log n) needs halving."],
            ),
            approach(
                "Binary search on the slope",
                "best",
                "O(log n)",
                "O(1)",
                idea=["`lo = 0`, `hi = n − 1`. While `lo < hi`: if `e[mid] < e[mid + 1]`, `lo = mid + 1`; else `hi = mid`. Return `lo`."],
                walk=w2,
                build=["`lo = 0`, `hi = n − 1`.", "Compare mid with its right neighbour and keep the half containing the top.", "Return `lo`."],
                code={
                    "python": """
                        class Solution:
                            def mountainTop(self, elevations: List[int]) -> int:
                                lo, hi = 0, len(elevations) - 1  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if elevations[mid] < elevations[mid + 1]:  #@slope
                                        lo = mid + 1  #@slope
                                    else:  #@slope
                                        hi = mid  #@slope
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int mountainTop(int[] elevations) {
                                int lo = 0, hi = elevations.length - 1;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (elevations[mid] < elevations[mid + 1]) lo = mid + 1;  //@slope
                                    else hi = mid;  //@slope
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int mountainTop(vector<int>& elevations) {
                                int lo = 0, hi = (int) elevations.size() - 1;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (elevations[mid] < elevations[mid + 1]) lo = mid + 1;  //@slope
                                    else hi = mid;  //@slope
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int mountainTop(int* elevations, int elevationsSize) {
                            int lo = 0, hi = elevationsSize - 1;  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (elevations[mid] < elevations[mid + 1]) lo = mid + 1;  //@slope
                                else hi = mid;  //@slope
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("range", "The top is somewhere in [0, n − 1]."), ("loop", "`mid < hi`, so `mid + 1` is a valid index."), ("slope", "Rising after mid: the top is further right. Falling: mid is the top or past it, so keep mid."), ("ret", "The single remaining index is the top.")],
                complexity=["**Time O(log n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Binary search doesn't need sorted data, only a yes/no question that flips once: "is the next point
              higher?"
            - Compare `a[mid]` with `a[mid + 1]` and keep the side that contains the peak.
            """
        ],
    )


@problem
def any_summit():
    h = [2, 5, 3, 1, 4, 8, 6, 7, 0]
    peaks = [i for i in range(len(h)) if (i == 0 or h[i] > h[i - 1]) and (i == len(h) - 1 or h[i] > h[i + 1])]

    w1 = Steps("Scan for the first point that is higher than the point after it (or the last point).")
    for i in range(len(h)):
        if i == len(h) - 1 or h[i] > h[i + 1]:
            w1.step(f"{h[i]} > {h[i + 1]}: since we got here by climbing, it's higher than both neighbours. Summit at {i}." if i < len(h) - 1 else f"Last point, reached by climbing: summit at {i}.", Row(h, st={i: "answer"}, slots=True), result=i)
            break
        w1.step(f"{h[i]} < {h[i + 1]}: keep climbing.", Row(h, st={i: "active"}, slots=True))

    w2 = Steps("Compare mid with its right neighbour and walk uphill: there is always a summit in the uphill direction.")
    r = slope_walk(w2, h)
    w2.step(f"lo = hi = {r}: {h[r]} is higher than its neighbours.", Row(h, st={r: "answer"}, slots=True), result=r)

    sol(
        "any-summit",
        summary="""
            Walking uphill must eventually reach a summit, because the trail ends in a drop on both sides. So at `mid`,
            if the next point is higher, a summit exists to the right; otherwise one exists at mid or to its left.
            Binary search keeps the half that's guaranteed to contain a summit: O(log n). Any summit is accepted.
        """,
        question=[
            """
            Heights have no equal neighbours; the trail drops to −∞ before the first and after the last point. Return the
            index of **any** point higher than both neighbours, in O(log n).

            - **Any summit** is accepted; there may be several.
            - **The ends can be summits** thanks to the imaginary drops: `[7]` → 0; `[1, 2]` → 1.
            - **Heights span the full 32-bit range**, but only comparisons are needed, so no overflow risk.
            - **The input isn't sorted**, yet binary search still works.
            """
        ],
        think=[
            f"""
            Take `{h}`. Summits are at indices {peaks}. We only need one.

            Stand at any point and look right. If the next point is **higher**, keep walking right while it keeps rising.
            You can't climb forever: either the trail turns down (that's a summit) or it ends (the last point, with a
            drop after it, is a summit). So **"the next point is higher" guarantees a summit to the right**. Likewise, if
            the next point is lower, a summit exists at the current point or to its left.
            """,
            fig(Row(h, st={p: "answer" for p in peaks}, slots=True), caption="Any of the shaded points is a valid answer."),
            """
            That's enough for binary search. At mid: rising to the right → `lo = mid + 1`; falling → `hi = mid`. The kept
            half always contains a summit, and when one index is left, it is one.
            """,
        ],
        approaches=[
            approach(
                "Scan for the first downturn",
                "brute",
                "O(n)",
                "O(1)",
                idea=["Return the first index i whose next point is lower, or the last index if the trail never turns down. Every point before i was rising, so i is higher than its left neighbour too."],
                walk=w1,
                build=["For i from 0 to n − 2: if `h[i] > h[i + 1]`, return i.", "Return n − 1."],
                code={
                    "python": """
                        class Solution:
                            def findSummit(self, heights: List[int]) -> int:
                                for i in range(len(heights) - 1):  #@scan
                                    if heights[i] > heights[i + 1]:  #@scan
                                        return i  #@scan
                                return len(heights) - 1  #@last
                    """,
                    "java": """
                        class Solution {
                            public int findSummit(int[] heights) {
                                for (int i = 0; i + 1 < heights.length; i++) if (heights[i] > heights[i + 1]) return i;  //@scan
                                return heights.length - 1;  //@last
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int findSummit(vector<int>& heights) {
                                for (size_t i = 0; i + 1 < heights.size(); i++) if (heights[i] > heights[i + 1]) return i;  //@scan
                                return heights.size() - 1;  //@last
                            }
                        };
                    """,
                    "c": """
                        int findSummit(int* heights, int heightsSize) {
                            for (int i = 0; i + 1 < heightsSize; i++) if (heights[i] > heights[i + 1]) return i;  //@scan
                            return heightsSize - 1;  //@last
                        }
                    """,
                },
                lines=[("scan", "The first point higher than the next. It was reached by climbing (or is index 0, with a drop before it), so it beats its left neighbour as well."), ("last", "Climbing all the way: the last point is a summit thanks to the drop after it.")],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Linear; the requirement is O(log n). The \"walk uphill\" argument works from any midpoint, not just from the start."],
            ),
            approach(
                "Binary search uphill",
                "best",
                "O(log n)",
                "O(1)",
                idea=["`lo = 0`, `hi = n − 1`. If `h[mid] < h[mid + 1]`, a summit lies right: `lo = mid + 1`. Else one lies at mid or left: `hi = mid`. Return `lo`."],
                walk=w2,
                build=["`lo = 0`, `hi = n − 1`.", "Compare mid with mid + 1; keep the uphill half.", "Return `lo`."],
                code={
                    "python": """
                        class Solution:
                            def findSummit(self, heights: List[int]) -> int:
                                lo, hi = 0, len(heights) - 1  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if heights[mid] < heights[mid + 1]:  #@uphill
                                        lo = mid + 1  #@uphill
                                    else:  #@uphill
                                        hi = mid  #@uphill
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int findSummit(int[] heights) {
                                int lo = 0, hi = heights.length - 1;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (heights[mid] < heights[mid + 1]) lo = mid + 1;  //@uphill
                                    else hi = mid;  //@uphill
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int findSummit(vector<int>& heights) {
                                int lo = 0, hi = (int) heights.size() - 1;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (heights[mid] < heights[mid + 1]) lo = mid + 1;  //@uphill
                                    else hi = mid;  //@uphill
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int findSummit(int* heights, int heightsSize) {
                            int lo = 0, hi = heightsSize - 1;  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (heights[mid] < heights[mid + 1]) lo = mid + 1;  //@uphill
                                else hi = mid;  //@uphill
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("range", "A summit exists somewhere in the whole trail."), ("loop", "`mid < hi`, so `mid + 1` is valid."), ("uphill", "Go towards the higher neighbour: a summit is guaranteed that way. Invariant: `[lo, hi]` always contains a summit."), ("ret", "One index left: it's a summit.")],
                complexity=["**Time O(log n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Peak finding:** move towards the higher neighbour; the boundary drops guarantee a peak in that
              direction, so binary search works on unsorted data.
            - The invariant "the range contains a valid answer" is what makes it correct, not sortedness.
            """
        ],
    )


@problem
def mountain_lookups():
    e = [1, 3, 6, 9, 12, 10, 6, 4, 3, 0]
    targets = [6, 3, 11, 0]
    want = [e.index(t) if t in e else -1 for t in targets]
    top = e.index(max(e))

    w1 = Steps("For each target, scan the mountain from the left.")
    for t, a in zip(targets, want):
        w1.step(f"Target {t}: " + (f"first found at index {a}." if a >= 0 else f"not found after checking all {len(e)} points."), Row(e, st={a: "answer"} if a >= 0 else {k: "dim" for k in range(len(e))}, slots=True))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("One pass records each elevation's first index in a hash map; then every lookup is O(1).")
    first = {}
    for i, v in enumerate(e):
        first.setdefault(v, i)
    w2.step("Map elevation → first index (the left slope wins for values on both slopes).", Row(e, slots=True), Row([f"{v}→{i}" for v, i in first.items()], label="first index"))
    w2.step(f"Lookups: {', '.join(f'{t}→{first.get(t, -1)}' for t in targets)}.", Row([f"{v}→{i}" for v, i in first.items()], st={list(first).index(t): "answer" for t in targets if t in first}, label="first index"), result=want)

    w3 = Steps("Find the top once. Then each target is a binary search on the rising slope, and if that fails, on the falling slope.")
    w3.step(f"Binary search for the top (as in Mountain Top): index {top}. Left of it the slope rises; right of it, it falls.", Row(e, st={top: "answer"} | {k: "found" for k in range(top)} | {k: "mark" for k in range(top + 1, len(e))}, slots=True))
    import bisect
    for t in targets:
        i = bisect.bisect_left(e, t, 0, top + 1)
        if i <= top and e[i] == t:
            w3.step(f"Target {t}: rising slope [0, {top}] → found at {i} (the smallest index, since the rising slope comes first).", Row(e, st={i: "answer"}, slots=True))
            continue
        lo, hi = top, len(e)
        while lo < hi:
            mid = (lo + hi) // 2
            if e[mid] > t:
                lo = mid + 1
            else:
                hi = mid
        found = lo < len(e) and e[lo] == t
        w3.step(f"Target {t}: not on the rising slope; falling slope [{top}, {len(e) - 1}] (search reversed) → " + (f"found at {lo}." if found else "not there either: −1."), Row(e, st={lo: "answer"} if found else {k: "dim" for k in range(len(e))}, slots=True))
    w3.steps[-1]["result"] = str(want)

    sol(
        "mountain-lookups",
        summary="""
            A mountain is two sorted runs: increasing up to the top, decreasing after it. Find the top once with a slope
            binary search, then answer each target with a binary search on the rising side and, only if it's not there,
            on the falling side. Searching the rising side first guarantees the **smallest** index. O((q + 1) log n)
            time, O(1) extra space.
        """,
        question=[
            """
            `elevations` rises strictly to one top, then falls strictly. For each target, return the **smallest** index
            holding it, or −1.

            - **A value can appear twice**, once on each slope (e.g. 6 and 3 in the example). The smallest index is the
              one on the rising slope.
            - **Up to 10⁵ targets** on 10⁵ points: scanning per target is 10¹⁰ steps.
            - **Answer in the order of `targets`.**
            """
        ],
        think=[
            f"""
            Take `{e}` with targets `{targets}`. The top is {max(e)} at index {top}. Left of it the values increase;
            right of it they decrease.
            """,
            fig(Row(e, st={top: "answer"} | {k: "found" for k in range(top)} | {k: "mark" for k in range(top + 1, len(e))}, slots=True), caption="Rising slope (light), top, falling slope (marked): two sorted halves."),
            """
            Each slope is sorted, one ascending and one descending, so each can be binary-searched. The order of the two
            searches matters: every index on the rising slope is smaller than every index on the falling slope, so look
            there first and only fall back to the falling slope if the target isn't on the rising one.

            A hash map from value to first index also answers every lookup in O(1), at the cost of reading the whole
            mountain and storing it.
            """,
        ],
        approaches=[
            approach(
                "Scan for every target",
                "brute",
                "O(n · q)",
                "O(1)",
                idea=["For each target, return the first index whose elevation equals it."],
                walk=w1,
                build=["For each target, scan from index 0; record the first match or −1."],
                code={
                    "python": """
                        class Solution:
                            def findAltitudes(self, elevations: List[int], targets: List[int]) -> List[int]:
                                out = []
                                for t in targets:  #@each
                                    idx = -1  #@scan
                                    for i, v in enumerate(elevations):  #@scan
                                        if v == t:  #@scan
                                            idx = i  #@scan
                                            break  #@scan
                                    out.append(idx)  #@scan
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] findAltitudes(int[] elevations, int[] targets) {
                                int[] out = new int[targets.length];
                                for (int q = 0; q < targets.length; q++) {  //@each
                                    out[q] = -1;  //@scan
                                    for (int i = 0; i < elevations.length; i++) if (elevations[i] == targets[q]) { out[q] = i; break; }  //@scan
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findAltitudes(vector<int>& elevations, vector<int>& targets) {
                                vector<int> out;
                                for (int t : targets) {  //@each
                                    auto it = find(elevations.begin(), elevations.end(), t);  //@scan
                                    out.push_back(it == elevations.end() ? -1 : (int) (it - elevations.begin()));  //@scan
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* findAltitudes(int* elevations, int elevationsSize, int* targets, int targetsSize, int* returnSize) {
                            int* out = malloc(targetsSize * sizeof(int));
                            for (int q = 0; q < targetsSize; q++) {  //@each
                                out[q] = -1;  //@scan
                                for (int i = 0; i < elevationsSize; i++) if (elevations[i] == targets[q]) { out[q] = i; break; }  //@scan
                            }
                            *returnSize = targetsSize;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("each", "One lookup per target."), ("scan", "First match from the left, so the smallest index; −1 if none."), ("ret", "Answers in target order.")],
                complexity=["**Time O(n · q).** **Space O(1)** besides the output."],
                limits=["Every lookup re-reads the whole mountain."],
                slow=True,
            ),
            approach(
                "Hash map of first indices",
                "better",
                "O(n + q)",
                "O(n)",
                idea=["One pass from the left stores each elevation's first index (later duplicates don't overwrite). Each target is then a map lookup."],
                walk=w2,
                build=["For each index, store `first[e[i]] = i` if absent.", "Answer each target with `first.get(t, −1)`."],
                code={
                    "python": """
                        class Solution:
                            def findAltitudes(self, elevations: List[int], targets: List[int]) -> List[int]:
                                first = {}  #@map
                                for i, v in enumerate(elevations):  #@map
                                    first.setdefault(v, i)  #@map
                                return [first.get(t, -1) for t in targets]  #@look
                    """,
                    "java": """
                        class Solution {
                            public int[] findAltitudes(int[] elevations, int[] targets) {
                                Map<Integer, Integer> first = new HashMap<>();  //@map
                                for (int i = 0; i < elevations.length; i++) first.putIfAbsent(elevations[i], i);  //@map
                                int[] out = new int[targets.length];  //@look
                                for (int q = 0; q < targets.length; q++) out[q] = first.getOrDefault(targets[q], -1);  //@look
                                return out;  //@look
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findAltitudes(vector<int>& elevations, vector<int>& targets) {
                                unordered_map<int, int> first;  //@map
                                for (int i = 0; i < (int) elevations.size(); i++) first.emplace(elevations[i], i);  //@map
                                vector<int> out;  //@look
                                for (int t : targets) {  //@look
                                    auto it = first.find(t);  //@look
                                    out.push_back(it == first.end() ? -1 : it->second);  //@look
                                }
                                return out;  //@look
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int key; int idx; bool used; } Slot;  //@table

                        static Slot* slotFor(Slot* t, unsigned mask, int key) {  //@table
                            unsigned long long h = (unsigned long long) (long long) key * 0x9E3779B97F4A7C15ULL;  //@table
                            unsigned s = (unsigned) (h >> 32) & mask;  //@table
                            while (t[s].used && t[s].key != key) s = (s + 1) & mask;  //@table
                            return &t[s];  //@table
                        }  //@table

                        int* findAltitudes(int* elevations, int elevationsSize, int* targets, int targetsSize, int* returnSize) {
                            unsigned cap = 1;  //@map
                            while (cap < 2u * elevationsSize) cap <<= 1;  //@map
                            Slot* first = calloc(cap, sizeof(Slot));  //@map
                            for (int i = 0; i < elevationsSize; i++) {  //@map
                                Slot* s = slotFor(first, cap - 1, elevations[i]);  //@map
                                if (!s->used) *s = (Slot) {elevations[i], i, true};  //@map
                            }  //@map
                            int* out = malloc(targetsSize * sizeof(int));  //@look
                            for (int q = 0; q < targetsSize; q++) {  //@look
                                Slot* s = slotFor(first, cap - 1, targets[q]);  //@look
                                out[q] = s->used ? s->idx : -1;  //@look
                            }  //@look
                            free(first);  //@look
                            *returnSize = targetsSize;  //@look
                            return out;  //@look
                        }
                    """,
                },
                lines=[
                    ("table", "C has no hash map: `slotFor` probes from a value's hashed slot to its entry or the empty slot where it would go."),
                    ("map", "Left to right, keep only the first index of each value, so a value on both slopes maps to its rising-slope index.", {"java": "`putIfAbsent` never overwrites an earlier index.", "cpp": "`emplace` doesn't overwrite an existing key."}),
                    ("look", "Each target is one lookup; missing values give −1."),
                ],
                complexity=["**Time O(n + q).** **Space O(n)** for the map."],
                limits=["It reads and stores the entire mountain even though the mountain shape already allows searching it in place. With the slopes binary-searched, each lookup touches only O(log n) points and no extra memory is needed."],
            ),
            approach(
                "Find the top, then search each slope",
                "best",
                "O((q + 1) log n)",
                "O(1)",
                idea=["Binary-search the top. For each target: lower-bound search on the rising slope `[0, top]`; if not found, search the falling slope `[top, n)` for the first index whose value is ≤ target and check it equals the target."],
                walk=w3,
                build=["Find `top` with the slope test.", "Rising slope: first index in `[0, top]` with value ≥ t; equal → answer.", "Falling slope: first index in `[top, n)` with value ≤ t; equal → answer; else −1."],
                code={
                    "python": """
                        class Solution:
                            def findAltitudes(self, elevations: List[int], targets: List[int]) -> List[int]:
                                e, n = elevations, len(elevations)
                                lo, hi = 0, n - 1  #@top
                                while lo < hi:  #@top
                                    mid = (lo + hi) // 2  #@top
                                    if e[mid] < e[mid + 1]:  #@top
                                        lo = mid + 1  #@top
                                    else:  #@top
                                        hi = mid  #@top
                                top = lo  #@top
                                out = []
                                for t in targets:  #@each
                                    lo, hi = 0, top + 1  #@rise
                                    while lo < hi:  #@rise
                                        mid = (lo + hi) // 2  #@rise
                                        if e[mid] < t:  #@rise
                                            lo = mid + 1  #@rise
                                        else:  #@rise
                                            hi = mid  #@rise
                                    if lo <= top and e[lo] == t:  #@rise
                                        out.append(lo)  #@rise
                                        continue  #@rise
                                    lo, hi = top, n  #@fall
                                    while lo < hi:  #@fall
                                        mid = (lo + hi) // 2  #@fall
                                        if e[mid] > t:  #@fall
                                            lo = mid + 1  #@fall
                                        else:  #@fall
                                            hi = mid  #@fall
                                    out.append(lo if lo < n and e[lo] == t else -1)  #@fall
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] findAltitudes(int[] e, int[] targets) {
                                int n = e.length, lo = 0, hi = n - 1;  //@top
                                while (lo < hi) {  //@top
                                    int mid = lo + (hi - lo) / 2;  //@top
                                    if (e[mid] < e[mid + 1]) lo = mid + 1; else hi = mid;  //@top
                                }  //@top
                                int top = lo;  //@top
                                int[] out = new int[targets.length];
                                for (int q = 0; q < targets.length; q++) {  //@each
                                    int t = targets[q];  //@each
                                    lo = 0; hi = top + 1;  //@rise
                                    while (lo < hi) {  //@rise
                                        int mid = lo + (hi - lo) / 2;  //@rise
                                        if (e[mid] < t) lo = mid + 1; else hi = mid;  //@rise
                                    }  //@rise
                                    if (lo <= top && e[lo] == t) { out[q] = lo; continue; }  //@rise
                                    lo = top; hi = n;  //@fall
                                    while (lo < hi) {  //@fall
                                        int mid = lo + (hi - lo) / 2;  //@fall
                                        if (e[mid] > t) lo = mid + 1; else hi = mid;  //@fall
                                    }  //@fall
                                    out[q] = (lo < n && e[lo] == t) ? lo : -1;  //@fall
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findAltitudes(vector<int>& e, vector<int>& targets) {
                                int n = e.size(), lo = 0, hi = n - 1;  //@top
                                while (lo < hi) {  //@top
                                    int mid = lo + (hi - lo) / 2;  //@top
                                    if (e[mid] < e[mid + 1]) lo = mid + 1; else hi = mid;  //@top
                                }  //@top
                                int top = lo;  //@top
                                vector<int> out;
                                for (int t : targets) {  //@each
                                    int i = lower_bound(e.begin(), e.begin() + top + 1, t) - e.begin();  //@rise
                                    if (i <= top && e[i] == t) { out.push_back(i); continue; }  //@rise
                                    int j = lower_bound(e.begin() + top, e.end(), t, greater<int>()) - e.begin();  //@fall
                                    out.push_back(j < n && e[j] == t ? j : -1);  //@fall
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* findAltitudes(int* e, int n, int* targets, int targetsSize, int* returnSize) {
                            int lo = 0, hi = n - 1;  //@top
                            while (lo < hi) {  //@top
                                int mid = lo + (hi - lo) / 2;  //@top
                                if (e[mid] < e[mid + 1]) lo = mid + 1; else hi = mid;  //@top
                            }  //@top
                            int top = lo;  //@top
                            int* out = malloc(targetsSize * sizeof(int));
                            for (int q = 0; q < targetsSize; q++) {  //@each
                                int t = targets[q];  //@each
                                lo = 0; hi = top + 1;  //@rise
                                while (lo < hi) {  //@rise
                                    int mid = lo + (hi - lo) / 2;  //@rise
                                    if (e[mid] < t) lo = mid + 1; else hi = mid;  //@rise
                                }  //@rise
                                if (lo <= top && e[lo] == t) { out[q] = lo; continue; }  //@rise
                                lo = top; hi = n;  //@fall
                                while (lo < hi) {  //@fall
                                    int mid = lo + (hi - lo) / 2;  //@fall
                                    if (e[mid] > t) lo = mid + 1; else hi = mid;  //@fall
                                }  //@fall
                                out[q] = (lo < n && e[lo] == t) ? lo : -1;  //@fall
                            }
                            *returnSize = targetsSize;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("top", "Slope binary search for the top, done once."),
                    ("each", "Each target separately."),
                    ("rise", "Lower bound on the ascending part `[0, top]`. A hit here is automatically the smallest index, because every rising index comes before every falling one.", {"cpp": "`std::lower_bound` on the rising part."}),
                    ("fall", "On the descending part `[top, n)`, the condition flips: skip values **greater** than the target and stop at the first value ≤ target; it must equal the target to count.", {"cpp": "`lower_bound` with `greater<int>()` searches a descending range."}),
                    ("ret", "Answers in target order."),
                ],
                complexity=["**Time O(log n + q log n).** **Space O(1)** besides the output."],
            ),
        ],
        takeaways=[
            """
            - A mountain (bitonic) array = **two sorted halves**: find the peak once, then binary-search each side.
            - On a descending range, flip the comparison (or use a `greater` comparator).
            - "Smallest index" with duplicates across halves: search the left half first.
            """
        ],
    )
