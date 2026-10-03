"""Stacks & Queues: monotonic stack."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def warmer_day_wait():
    temps = [30, 28, 31, 27, 27, 29, 33, 26]
    n = len(temps)
    want = [next((j - i for j in range(i + 1, n) if temps[j] > temps[i]), 0) for i in range(n)]

    w1 = Steps("For each day, look forward day by day until a strictly warmer one.")
    for i in range(n):
        j = i + want[i] if want[i] else None
        w1.step(f"Day {i} ({temps[i]}°): " + (f"first warmer day is {j} ({temps[j]}°), wait {want[i]}." if j is not None else "no warmer day ahead, wait 0."), Row(temps, st={**{x: "mark" for x in range(i + 1, (j if j is not None else n))}, i: "active", **({j: "found"} if j is not None else {})}), Row(want[:i + 1] + ["·"] * (n - i - 1), label="wait"))
    w1.step(f"Waits: {want}.", result=str(want))

    w2 = Steps("Go backwards, remembering for every temperature the nearest later day that had it. A day's answer is the nearest of the remembered days that are warmer.")
    nxt = {}
    for i in range(n - 1, -1, -1):
        warmer = {t: d for t, d in nxt.items() if t > temps[i]}
        nearest = min(warmer.values()) if warmer else None
        w2.step(f"Day {i} ({temps[i]}°): remembered warmer temperatures {dict(sorted(warmer.items())) or '{}'} (temp: day). " + (f"Nearest is day {nearest}: wait {nearest - i}." if nearest is not None else "None: wait 0.") + f" Now day {i} is the nearest {temps[i]}°.", Row(temps, st={i: "active", **({nearest: "found"} if nearest is not None else {})}), Row(["·"] * i + want[i:], label="wait"))
        nxt[temps[i]] = i
    w2.step(f"Waits: {want}.", result=str(want))

    w3 = Steps("A stack of days still waiting for a warmer day; their temperatures never increase from bottom to top. Each new day settles every waiting day it's warmer than.")
    st, res = [], [0] * n
    for i, t in enumerate(temps):
        done = []
        while st and temps[st[-1]] < t:
            j = st.pop()
            res[j] = i - j
            done.append(j)
        st.append(i)
        w3.step(f"Day {i} ({t}°): " + (f"warmer than waiting days {done}: their waits are {[i - j for j in done]}. " if done else "settles nobody. ") + "It starts waiting.", Row(temps, st={i: "active", **{j: "found" for j in done}}), Row([f"{j}:{temps[j]}°" for j in st], label="waiting (day:temp)"), Row(res, label="wait"))
    w3.step(f"Days {st} never found a warmer day: their wait stays 0. Waits: {res}.", result=str(res))

    sol(
        "warmer-day-wait",
        summary="""
            Keep a stack of days still waiting for a warmer one. Their temperatures never rise from bottom to top, because
            a warmer day would have settled the cooler days below it. Each new day pops every waiting day that's cooler
            and records the gap. Every day is pushed and popped once: O(n).
        """,
        question=[
            """
            For every day, how many days until a strictly warmer one? If none comes, 0.

            - **Strictly warmer:** an equal temperature doesn't count.
            - **The last day always gets 0.**
            - **Up to 10⁵ days**; temperatures are between −100 and 100.
            """
        ],
        think=[
            f"""
            Temperatures `{temps}`. Day 0 (30°) waits 2 days for 31°. Days 3 and 4 (27°, 27°) both get settled by day 5
            (29°). Day 6 (33°) never sees anything warmer. Waits: `{want}`.
            """,
            fig(Row(temps, label="temps"), Row(want, label="wait")),
            """
            Turn it around: instead of each day searching forward, let each new day **answer the earlier days that were
            waiting for it**. Which days are still waiting when day `i` arrives? Only ones that haven't seen anything warmer
            yet, so each waiting day is at least as warm as every waiting day after it. That means the coolest waiting days
            are the most recent ones, on top of a stack. Day `i` pops them while it's warmer, and stops at the first one
            that's at least as warm: everything below is warmer still.
            """,
        ],
        approaches=[
            approach(
                "Look ahead from every day",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each day `i`, scan `j = i+1, i+2, …` until `temps[j] > temps[i]`; the wait is `j − i`, or 0 if the scan runs out."],
                walk=w1,
                build=["For each `i`, scan forward.", "Stop at the first warmer day and record the gap.", "Leave 0 if none."],
                code={
                    "python": """
                        class Solution:
                            def daysUntilWarmer(self, temps: List[int]) -> List[int]:
                                n = len(temps)  #@init
                                wait = [0] * n  #@init
                                for i in range(n):  #@each
                                    for j in range(i + 1, n):  #@scan
                                        if temps[j] > temps[i]:  #@hit
                                            wait[i] = j - i  #@hit
                                            break  #@hit
                                return wait  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] daysUntilWarmer(int[] temps) {
                                int n = temps.length;  //@init
                                int[] wait = new int[n];  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    for (int j = i + 1; j < n; j++) {  //@scan
                                        if (temps[j] > temps[i]) { wait[i] = j - i; break; }  //@hit
                                    }
                                }
                                return wait;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> daysUntilWarmer(vector<int>& temps) {
                                int n = temps.size();  //@init
                                vector<int> wait(n, 0);  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    for (int j = i + 1; j < n; j++) {  //@scan
                                        if (temps[j] > temps[i]) { wait[i] = j - i; break; }  //@hit
                                    }
                                }
                                return wait;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* daysUntilWarmer(int* temps, int tempsSize, int* returnSize) {
                            int n = tempsSize;  //@init
                            int* wait = calloc(n, sizeof(int));  //@init
                            for (int i = 0; i < n; i++) {  //@each
                                for (int j = i + 1; j < n; j++) {  //@scan
                                    if (temps[j] > temps[i]) { wait[i] = j - i; break; }  //@hit
                                }
                            }
                            *returnSize = n;  //@ret
                            return wait;  //@ret
                        }
                    """,
                },
                lines=[("init", "Waits default to 0 (no warmer day)."), ("each", "Every day."), ("scan", "Look ahead one day at a time."), ("hit", "The first strictly warmer day ends the wait."), ("ret", "All waits.")],
                complexity=["**Time O(n²)**, e.g. for steadily cooling temperatures, where every scan runs to the end. **Space O(1)** beyond the answer."],
                limits=["A long cooling stretch makes every day scan the same days again. Either use the small temperature range, or let each warm day settle the waiting days itself."],
                slow=True,
            ),
            approach(
                "Nearest later day for each temperature",
                "better",
                "O(n·W)",
                "O(W)",
                idea=["Temperatures only take W = 201 values. Walk the days backwards, keeping `next[t]` = the nearest later day with temperature `t`. For day `i`, the first warmer day is the smallest `next[t]` over all `t > temps[i]`. Then set `next[temps[i]] = i`."],
                walk=w2,
                build=["`next[t] = ∞` for all 201 temperatures (offset by 100).", "From the last day back: take the min of `next[t]` for `t > temps[i]`.", "Record the wait (or 0), then `next[temps[i]] = i`."],
                code={
                    "python": """
                        class Solution:
                            def daysUntilWarmer(self, temps: List[int]) -> List[int]:
                                n = len(temps)  #@init
                                wait = [0] * n  #@init
                                INF = n  #@init
                                nxt = [INF] * 201  #@init
                                for i in range(n - 1, -1, -1):  #@back
                                    first = INF  #@scan
                                    for t in range(temps[i] + 101, 201):  #@scan
                                        first = min(first, nxt[t])  #@scan
                                    if first < INF:  #@set
                                        wait[i] = first - i  #@set
                                    nxt[temps[i] + 100] = i  #@remember
                                return wait  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] daysUntilWarmer(int[] temps) {
                                int n = temps.length;  //@init
                                int[] wait = new int[n], next = new int[201];  //@init
                                Arrays.fill(next, n);  //@init
                                for (int i = n - 1; i >= 0; i--) {  //@back
                                    int first = n;  //@scan
                                    for (int t = temps[i] + 101; t < 201; t++) first = Math.min(first, next[t]);  //@scan
                                    if (first < n) wait[i] = first - i;  //@set
                                    next[temps[i] + 100] = i;  //@remember
                                }
                                return wait;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> daysUntilWarmer(vector<int>& temps) {
                                int n = temps.size();  //@init
                                vector<int> wait(n, 0), next(201, n);  //@init
                                for (int i = n - 1; i >= 0; i--) {  //@back
                                    int first = n;  //@scan
                                    for (int t = temps[i] + 101; t < 201; t++) first = min(first, next[t]);  //@scan
                                    if (first < n) wait[i] = first - i;  //@set
                                    next[temps[i] + 100] = i;  //@remember
                                }
                                return wait;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* daysUntilWarmer(int* temps, int tempsSize, int* returnSize) {
                            int n = tempsSize;  //@init
                            int* wait = calloc(n, sizeof(int));  //@init
                            int next[201];  //@init
                            for (int t = 0; t < 201; t++) next[t] = n;  //@init
                            for (int i = n - 1; i >= 0; i--) {  //@back
                                int first = n;  //@scan
                                for (int t = temps[i] + 101; t < 201; t++) if (next[t] < first) first = next[t];  //@scan
                                if (first < n) wait[i] = first - i;  //@set
                                next[temps[i] + 100] = i;  //@remember
                            }
                            *returnSize = n;  //@ret
                            return wait;  //@ret
                        }
                    """,
                },
                lines=[("init", "`next[t + 100]` = nearest later day with temperature `t`; `n` stands for 'never'."), ("back", "From the last day to the first, so `next` always describes the days after `i`."), ("scan", "Every strictly warmer temperature (index `temps[i] + 101` and up); the nearest such day is the first warmer day."), ("set", "Found one: the wait is the gap."), ("remember", "Day `i` is now the nearest day with its temperature for everything before it."), ("ret", "All waits.")],
                complexity=["**Time O(n·W)** with W = 201 temperatures: about 2 × 10⁷ steps, fine here. **Space O(W).**"],
                limits=["It leans on the tiny temperature range: with values up to 10⁹ it would be hopeless. The stack method doesn't care about the range at all."],
            ),
            approach(
                "Stack of waiting days",
                "best",
                "O(n)",
                "O(n)",
                idea=["Keep a stack of indices still waiting for a warmer day. For each day `i`: while the top's temperature is lower than `temps[i]`, pop it and set its wait to `i − top`. Then push `i`. Days left on the stack at the end keep wait 0."],
                walk=w3,
                build=["Waits default to 0; an empty stack.", "For each day, pop and settle every cooler waiting day.", "Push the day.", "Return the waits."],
                code={
                    "python": """
                        class Solution:
                            def daysUntilWarmer(self, temps: List[int]) -> List[int]:
                                wait = [0] * len(temps)  #@init
                                stack = []  #@init
                                for i, t in enumerate(temps):  #@loop
                                    while stack and temps[stack[-1]] < t:  #@settle
                                        j = stack.pop()  #@settle
                                        wait[j] = i - j  #@settle
                                    stack.append(i)  #@push
                                return wait  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] daysUntilWarmer(int[] temps) {
                                int n = temps.length;  //@init
                                int[] wait = new int[n], stack = new int[n];  //@init
                                int top = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@loop
                                    while (top > 0 && temps[stack[top - 1]] < temps[i]) {  //@settle
                                        int j = stack[--top];  //@settle
                                        wait[j] = i - j;  //@settle
                                    }
                                    stack[top++] = i;  //@push
                                }
                                return wait;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> daysUntilWarmer(vector<int>& temps) {
                                int n = temps.size();  //@init
                                vector<int> wait(n, 0), stack;  //@init
                                for (int i = 0; i < n; i++) {  //@loop
                                    while (!stack.empty() && temps[stack.back()] < temps[i]) {  //@settle
                                        wait[stack.back()] = i - stack.back();  //@settle
                                        stack.pop_back();  //@settle
                                    }
                                    stack.push_back(i);  //@push
                                }
                                return wait;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* daysUntilWarmer(int* temps, int tempsSize, int* returnSize) {
                            int n = tempsSize;  //@init
                            int* wait = calloc(n, sizeof(int));  //@init
                            int* stack = malloc(n * sizeof(int));  //@init
                            int top = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@loop
                                while (top > 0 && temps[stack[top - 1]] < temps[i]) {  //@settle
                                    int j = stack[--top];  //@settle
                                    wait[j] = i - j;  //@settle
                                }
                                stack[top++] = i;  //@push
                            }
                            free(stack);  //@ret
                            *returnSize = n;  //@ret
                            return wait;  //@ret
                        }
                    """,
                },
                lines=[("init", "Waits default to 0; the stack holds days still waiting."), ("loop", "Each day in order."), ("settle", "Day `i` is the first warmer day for every cooler day on top of the stack. Settle them; stop at a day at least as warm, since everything below it is warmer still."), ("push", "Day `i` now waits for its own warmer day."), ("ret", "Days never popped keep 0.")],
                complexity=["**Time O(n):** each day is pushed once and popped at most once. **Space O(n)** for the stack (a steadily cooling run keeps everything waiting)."],
            ),
        ],
        takeaways=[
            """
            - **"Next greater element" = monotonic stack:** each new element settles the waiting elements it beats.
            - The stack is never increasing from bottom to top, which is why one comparison with the top decides when to
              stop.
            - A small value range can give a simple alternative (one slot per value), but don't depend on it.
            """
        ],
    )


@problem
def next_bigger_on_the_ring():
    ring = [4, 2, 7, 3, 7, 1]
    n = len(ring)
    want = [next((ring[(i + d) % n] for d in range(1, n) if ring[(i + d) % n] > ring[i]), -1) for i in range(n)]

    w1 = Steps("From every tile, walk clockwise (wrapping) for up to n − 1 tiles until a bigger number.")
    for i in range(n):
        d = next((d for d in range(1, n) if ring[(i + d) % n] > ring[i]), None)
        seen = [(i + e) % n for e in range(1, d if d else n)]
        w1.step(f"Tile {i} ({ring[i]}): " + (f"walk {d} step(s) to tile {(i + d) % n} ({want[i]})." if d else "nothing on the ring is bigger: −1."), Row(ring, st={**{x: "mark" for x in seen}, i: "active", **({(i + d) % n: "found"} if d else {})}), Row(want[:i + 1] + ["·"] * (n - i - 1), label="answer"))
    w1.step(f"Answer: {want}.", result=str(want))

    w2 = Steps("Run the 'next bigger' stack over the ring twice in a row (indices 0..2n−1, using i mod n). The second lap lets tiles near the end find bigger tiles near the start.")
    st, res = [], [-1] * n
    for i in range(2 * n):
        v = ring[i % n]
        done = []
        while st and ring[st[-1]] < v:
            j = st.pop()
            res[j] = v
            done.append(j)
        if i < n:
            st.append(i)
        if i < n or done:
            w2.step(f"{'Lap 1' if i < n else 'Lap 2'}, tile {i % n} ({v}): " + (f"answers tiles {done}. " if done else "answers nobody. ") + ("Push it." if i < n else "(Not pushed again: every tile already waits once.)"), Row(ring, st={i % n: "active", **{j: "found" for j in done}}), Row([f"{j}:{ring[j]}" for j in st] or ["·"], label="waiting (tile:number)"), Row(res, label="answer"))
    w2.step(f"Tiles {st} are the biggest numbers on the ring: −1. Answer: {res}.", result=str(res))

    sol(
        "next-bigger-on-the-ring",
        summary="""
            The usual next-greater stack, but the ring wraps, so a tile near the end may find its answer near the start.
            Walk the indices twice (`0 .. 2n−1`, reading `ring[i mod n]`), pushing tiles only during the first lap. The
            second lap answers the tiles still waiting. O(n).
        """,
        question=[
            """
            Tiles sit in a circle. From each tile, walk clockwise and report the first strictly bigger number; −1 if no
            tile on the ring is bigger.

            - **Wrap-around:** after the last tile comes tile 0.
            - **Strictly bigger:** equal numbers don't count, so every copy of the maximum gets −1.
            - **Up to 10⁵ tiles.**
            """
        ],
        think=[
            f"""
            Ring `{ring}`. Tile 0 (4) finds 7 two steps on. Tile 5 (1) wraps around and finds 4 at tile 0. Both 7s are the
            maximum, so they get −1. Answer: `{want}`.
            """,
            fig(Row(ring, label="ring"), Row(want, label="next bigger")),
            """
            Without the wrap this is the classic next-greater problem: keep a stack of tiles waiting for an answer, and let
            each new tile answer the smaller ones on top. With the wrap, any tile still waiting at the end of the array
            needs to keep looking from the start. Simply **replay the array a second time**: during the second lap, tiles
            only answer, they don't join the stack again. Anything still waiting after two laps has nothing bigger anywhere.
            """,
        ],
        approaches=[
            approach(
                "Walk the ring from every tile",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each tile `i`, check tiles `(i + d) mod n` for `d = 1 .. n−1` and stop at the first bigger number."],
                walk=w1,
                build=["For each `i`, loop `d` from 1 to `n − 1`.", "Index `(i + d) % n` wraps around.", "First bigger number is the answer; otherwise −1."],
                code={
                    "python": """
                        class Solution:
                            def nextBiggerOnRing(self, ring: List[int]) -> List[int]:
                                n = len(ring)  #@init
                                res = [-1] * n  #@init
                                for i in range(n):  #@each
                                    for d in range(1, n):  #@walk
                                        if ring[(i + d) % n] > ring[i]:  #@hit
                                            res[i] = ring[(i + d) % n]  #@hit
                                            break  #@hit
                                return res  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] nextBiggerOnRing(int[] ring) {
                                int n = ring.length;  //@init
                                int[] res = new int[n];  //@init
                                Arrays.fill(res, -1);  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    for (int d = 1; d < n; d++) {  //@walk
                                        if (ring[(i + d) % n] > ring[i]) { res[i] = ring[(i + d) % n]; break; }  //@hit
                                    }
                                }
                                return res;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> nextBiggerOnRing(vector<int>& ring) {
                                int n = ring.size();  //@init
                                vector<int> res(n, -1);  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    for (int d = 1; d < n; d++) {  //@walk
                                        if (ring[(i + d) % n] > ring[i]) { res[i] = ring[(i + d) % n]; break; }  //@hit
                                    }
                                }
                                return res;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* nextBiggerOnRing(int* ring, int ringSize, int* returnSize) {
                            int n = ringSize;  //@init
                            int* res = malloc(n * sizeof(int));  //@init
                            for (int i = 0; i < n; i++) {  //@each
                                res[i] = -1;  //@each
                                for (int d = 1; d < n; d++) {  //@walk
                                    if (ring[(i + d) % n] > ring[i]) { res[i] = ring[(i + d) % n]; break; }  //@hit
                                }
                            }
                            *returnSize = n;  //@ret
                            return res;  //@ret
                        }
                    """,
                },
                lines=[("init", "Answers default to −1."), ("each", "Every starting tile."), ("walk", "The other `n − 1` tiles in clockwise order; `% n` wraps around."), ("hit", "First strictly bigger number."), ("ret", "All answers.")],
                complexity=["**Time O(n²)** (e.g. all equal: every walk goes all the way round). **Space O(1).**"],
                limits=["Every tile re-walks the ring. The stack method answers each tile exactly once; the only twist is the wrap, handled by a second lap."],
                slow=True,
            ),
            approach(
                "Stack over two laps",
                "best",
                "O(n)",
                "O(n)",
                idea=["Loop `i` from 0 to `2n − 1` with value `ring[i % n]`. Pop and answer every waiting tile with a smaller number. Push `i` only when `i < n`. Tiles never popped keep −1."],
                walk=w2,
                build=["Answers default to −1; empty stack.", "For `i` in `0 .. 2n−1`: `v = ring[i % n]`.", "While the top's number < `v`: answer it with `v`.", "If `i < n`, push `i`."],
                code={
                    "python": """
                        class Solution:
                            def nextBiggerOnRing(self, ring: List[int]) -> List[int]:
                                n = len(ring)  #@init
                                res, stack = [-1] * n, []  #@init
                                for i in range(2 * n):  #@laps
                                    v = ring[i % n]  #@laps
                                    while stack and ring[stack[-1]] < v:  #@answer
                                        res[stack.pop()] = v  #@answer
                                    if i < n:  #@push
                                        stack.append(i)  #@push
                                return res  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] nextBiggerOnRing(int[] ring) {
                                int n = ring.length;  //@init
                                int[] res = new int[n], stack = new int[n];  //@init
                                Arrays.fill(res, -1);  //@init
                                int top = 0;  //@init
                                for (int i = 0; i < 2 * n; i++) {  //@laps
                                    int v = ring[i % n];  //@laps
                                    while (top > 0 && ring[stack[top - 1]] < v) res[stack[--top]] = v;  //@answer
                                    if (i < n) stack[top++] = i;  //@push
                                }
                                return res;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> nextBiggerOnRing(vector<int>& ring) {
                                int n = ring.size();  //@init
                                vector<int> res(n, -1), stack;  //@init
                                for (int i = 0; i < 2 * n; i++) {  //@laps
                                    int v = ring[i % n];  //@laps
                                    while (!stack.empty() && ring[stack.back()] < v) {  //@answer
                                        res[stack.back()] = v;  //@answer
                                        stack.pop_back();  //@answer
                                    }
                                    if (i < n) stack.push_back(i);  //@push
                                }
                                return res;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* nextBiggerOnRing(int* ring, int ringSize, int* returnSize) {
                            int n = ringSize;  //@init
                            int* res = malloc(n * sizeof(int));  //@init
                            int* stack = malloc(n * sizeof(int));  //@init
                            int top = 0;  //@init
                            for (int i = 0; i < n; i++) res[i] = -1;  //@init
                            for (int i = 0; i < 2 * n; i++) {  //@laps
                                int v = ring[i % n];  //@laps
                                while (top > 0 && ring[stack[top - 1]] < v) res[stack[--top]] = v;  //@answer
                                if (i < n) stack[top++] = i;  //@push
                            }
                            free(stack);  //@ret
                            *returnSize = n;  //@ret
                            return res;  //@ret
                        }
                    """,
                },
                lines=[("init", "Answers default to −1; the stack holds tiles still waiting."), ("laps", "Two passes over the ring; `i % n` maps the second lap back onto the tiles."), ("answer", "The current number is the first bigger one for every smaller tile waiting on top."), ("push", "Each tile waits once, so it's pushed only in the first lap. In the second lap, tiles only answer."), ("ret", "Tiles still waiting are the maximum (or tied with it): −1.")],
                complexity=["**Time O(n):** 2n iterations, each tile pushed and popped at most once. **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - **Circular arrays: iterate twice** (`i mod n`) instead of copying the array.
            - Push only in the first lap so each element waits once.
            - Elements left on the stack have no answer anywhere: they're the maximum.
            """
        ],
    )


@problem
def trim_the_reading():
    num, k = "4205318", 3

    def best(num, k):
        st = []
        for d in num:
            while k and st and st[-1] > d:
                st.pop()
                k -= 1
            st.append(d)
        if k:
            st = st[:-k]
        return "".join(st).lstrip("0") or "0"

    want = best(num, k)

    w1 = Steps("Erase one digit at a time: the first digit that is bigger than the digit after it (or the last digit if they never go down). Repeat k times.")
    s = num
    w1.step(f"Start: {s}, k = {k}.", Row(list(s)))
    for r in range(k):
        i = 0
        while i + 1 < len(s) and s[i] <= s[i + 1]:
            i += 1
        w1.step(f"Round {r + 1}: the first drop is after '{s[i]}' at position {i}" + (f" ('{s[i]}' > '{s[i + 1]}')" if i + 1 < len(s) else " (the digits never go down, so the last one)") + ": erase it.", Row(list(s), st={i: "mark"}))
        s = s[:i] + s[i + 1:]
    w1.step(f"Left: {s}; drop leading zeros → {s.lstrip('0') or '0'}.", Row(list(s)), result=want)

    w2 = Steps("Keep the digits kept so far on a stack. A new digit pops bigger digits off the top while erasures remain: an earlier position matters more.")
    st, kk = [], k
    for idx, d in enumerate(num):
        popped = []
        while kk and st and st[-1] > d:
            popped.append(st.pop())
            kk -= 1
        st.append(d)
        w2.step(f"Digit '{d}': " + (f"erase {popped} (bigger, and earlier). " if popped else "nothing bigger on top to erase. ") + f"Keep it. Erasures left: {kk}.", Row(list(num), st={idx: "active"}), Row(list(st), label="kept"))
    if kk:
        w2.step(f"{kk} erasure(s) left over: drop the last {kk} kept digit(s); the kept digits never go down, so the end is the biggest.", Row(list(st), st={len(st) - 1 - x: "mark" for x in range(kk)}, label="kept"))
        st = st[:-kk]
    w2.step(f"Kept '{''.join(st)}'; drop leading zeros → {want}.", Row(list(st), label="kept"), result=want)

    sol(
        "trim-the-reading",
        summary="""
            Earlier digits matter more, so whenever a digit is bigger than the one right after it, erasing it makes the
            number smaller. Scan once with a stack of kept digits: each new digit pops bigger digits off the top while
            erasures remain. Leftover erasures come off the end. Strip leading zeros. O(n).
        """,
        question=[
            """
            Erase exactly `k` digits from the string `num`, keeping the rest in order, so the result is as small as possible.
            Drop leading zeros; return `"0"` if nothing (or only zeros) remains.

            - **Same length after erasing**, so comparing results is comparing digit by digit from the left.
            - **Erasing a digit can expose zeros** at the front, which disappear and make the number much shorter.
            - **Up to 10⁵ digits**: far too many to try subsets.
            """
        ],
        think=[
            f"""
            Take `{num}` with `k = {k}`. Erase 4 (the 2 after it is smaller), then 2 (the 0 after it is smaller), then 5 (the
            3 after it is smaller): `0318`, which is **{want}**.

            All results have the same length, so the smallest one has the smallest first digit, then the smallest second
            digit, and so on. Look at the first place where the digits go down, `d > next`. Erasing `d` puts the smaller
            `next` in its spot, and nothing earlier changes. Erasing anything else leaves `d` where it is or later digits
            change, which only affects less important positions. So: **erase the first digit that's bigger than its
            successor**, then repeat.
            """,
            fig(Row(list(num), label="reading"), Row(list(want), label="smallest")),
            """
            Doing that literally restarts the scan each time. But after erasing a digit, the only new 'drop' can appear
            just before the erased spot, between the previous kept digit and the next one. So a stack of kept digits handles
            all the rounds in a single left-to-right pass.
            """,
        ],
        approaches=[
            approach(
                "Erase the first drop, k times",
                "brute",
                "O(n·k)",
                "O(n)",
                idea=["Repeat `k` times: find the first `i` with `num[i] > num[i+1]` (or the last digit if the digits never decrease) and erase it. Finally strip leading zeros."],
                walk=w1,
                build=["Copy the digits.", "k rounds: scan for the first drop, erase that digit.", "Strip leading zeros; empty → `\"0\"`."],
                code={
                    "python": """
                        class Solution:
                            def trimReading(self, num: str, k: int) -> str:
                                s = num  #@copy
                                for _ in range(k):  #@round
                                    i = 0  #@find
                                    while i + 1 < len(s) and s[i] <= s[i + 1]:  #@find
                                        i += 1  #@find
                                    s = s[:i] + s[i + 1:]  #@erase
                                return s.lstrip("0") or "0"  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String trimReading(String num, int k) {
                                StringBuilder s = new StringBuilder(num);  //@copy
                                for (int r = 0; r < k; r++) {  //@round
                                    int i = 0;  //@find
                                    while (i + 1 < s.length() && s.charAt(i) <= s.charAt(i + 1)) i++;  //@find
                                    s.deleteCharAt(i);  //@erase
                                }
                                int z = 0;  //@ret
                                while (z < s.length() && s.charAt(z) == '0') z++;  //@ret
                                return z == s.length() ? "0" : s.substring(z);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string trimReading(string& num, int k) {
                                string s = num;  //@copy
                                for (int r = 0; r < k; r++) {  //@round
                                    size_t i = 0;  //@find
                                    while (i + 1 < s.size() && s[i] <= s[i + 1]) i++;  //@find
                                    s.erase(i, 1);  //@erase
                                }
                                size_t z = s.find_first_not_of('0');  //@ret
                                return z == string::npos ? "0" : s.substr(z);  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* trimReading(char* num, int k) {
                            int len = strlen(num);  //@copy
                            char* s = malloc(len + 2);  //@copy
                            strcpy(s, num);  //@copy
                            for (int r = 0; r < k; r++) {  //@round
                                int i = 0;  //@find
                                while (i + 1 < len && s[i] <= s[i + 1]) i++;  //@find
                                memmove(s + i, s + i + 1, len - i);  //@erase
                                len--;  //@erase
                            }
                            int z = 0;  //@ret
                            while (z < len && s[z] == '0') z++;  //@ret
                            if (z == len) { strcpy(s, "0"); return s; }  //@ret
                            memmove(s, s + z, len - z + 1);  //@ret
                            return s;  //@ret
                        }
                    """,
                },
                lines=[("copy", "A copy we can erase from."), ("round", "One erasure per round."), ("find", "The first position where the next digit is smaller; if there's none, `i` ends on the last digit."), ("erase", "Erase it: the smaller digit after it moves into its place.", {"c": "`memmove` shifts the tail (including the terminating NUL) one place left."}), ("ret", "Strip leading zeros; nothing left means `\"0\"`.")],
                complexity=["**Time O(n·k):** each round rescans from the start and shifts the string. **Space O(n).**"],
                limits=["With `k` near `n`, that's ~10¹⁰ steps. After an erasure, only the spot just before it can become a new drop, so a stack can continue where it left off instead of restarting."],
                slow=True,
            ),
            approach(
                "Greedy stack of kept digits",
                "best",
                "O(n)",
                "O(n)",
                idea=["For each digit `d`: while erasures remain and the top of the stack is bigger than `d`, pop it (erase it) and decrement `k`. Push `d`. If erasures remain at the end, the kept digits never decrease, so drop the last `k`. Strip leading zeros."],
                walk=w2,
                build=["An empty stack (a char buffer).", "For each digit: pop bigger tops while `k > 0`; push.", "Remove `k` digits from the end.", "Skip leading zeros; empty → `\"0\"`."],
                code={
                    "python": """
                        class Solution:
                            def trimReading(self, num: str, k: int) -> str:
                                stack = []  #@init
                                for d in num:  #@loop
                                    while k and stack and stack[-1] > d:  #@pop
                                        stack.pop()  #@pop
                                        k -= 1  #@pop
                                    stack.append(d)  #@push
                                if k:  #@tail
                                    stack = stack[:-k]  #@tail
                                return "".join(stack).lstrip("0") or "0"  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String trimReading(String num, int k) {
                                StringBuilder stack = new StringBuilder();  //@init
                                for (char d : num.toCharArray()) {  //@loop
                                    while (k > 0 && stack.length() > 0 && stack.charAt(stack.length() - 1) > d) {  //@pop
                                        stack.setLength(stack.length() - 1);  //@pop
                                        k--;  //@pop
                                    }
                                    stack.append(d);  //@push
                                }
                                stack.setLength(stack.length() - k);  //@tail
                                int z = 0;  //@ret
                                while (z < stack.length() && stack.charAt(z) == '0') z++;  //@ret
                                return z == stack.length() ? "0" : stack.substring(z);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string trimReading(string& num, int k) {
                                string stack;  //@init
                                for (char d : num) {  //@loop
                                    while (k > 0 && !stack.empty() && stack.back() > d) {  //@pop
                                        stack.pop_back();  //@pop
                                        k--;  //@pop
                                    }
                                    stack.push_back(d);  //@push
                                }
                                stack.resize(stack.size() - k);  //@tail
                                size_t z = stack.find_first_not_of('0');  //@ret
                                return z == string::npos ? "0" : stack.substr(z);  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* trimReading(char* num, int k) {
                            int n = strlen(num), top = 0;  //@init
                            char* stack = malloc(n + 2);  //@init
                            for (int i = 0; i < n; i++) {  //@loop
                                while (k > 0 && top > 0 && stack[top - 1] > num[i]) {  //@pop
                                    top--;  //@pop
                                    k--;  //@pop
                                }
                                stack[top++] = num[i];  //@push
                            }
                            top -= k;  //@tail
                            int z = 0;  //@ret
                            while (z < top && stack[z] == '0') z++;  //@ret
                            if (z == top) { strcpy(stack, "0"); return stack; }  //@ret
                            memmove(stack, stack + z, top - z);  //@ret
                            stack[top - z] = '\\0';  //@ret
                            return stack;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "The kept digits, as a stack."),
                    ("loop", "One pass over the digits."),
                    ("pop", "A kept digit bigger than the new one is a 'drop': erasing it brings a smaller digit into an earlier position. Keep popping while erasures remain, because the digit below may be bigger too."),
                    ("push", "Keep the new digit (for now)."),
                    ("tail", "Erasures left over: the kept digits never decrease, so the last ones are the biggest and least important. Remove `k` from the end."),
                    ("ret", "Strip leading zeros; nothing left means `\"0\"`."),
                ],
                complexity=["**Time O(n):** each digit is pushed once and popped at most once. **Space O(n)** for the kept digits."],
            ),
        ],
        takeaways=[
            """
            - **Smallest subsequence of fixed length:** greedily remove a digit when a smaller one follows, using a stack.
            - The kept digits end up non-decreasing; leftover removals come off the end.
            - Watch the edge cases: leading zeros and an empty result.
            """
        ],
    )


@problem
def low_high_between():
    values = [2, 4, 3, 6, 5, 1, 7]
    n = len(values)
    trip = next((i, j, k) for j in range(n) for i in range(j) for k in range(j + 1, n) if values[i] < values[k] < values[j])

    w1 = Steps("Fix the middle moment j. The best first moment is the lowest value before j; look for a later value strictly between that low and values[j].")
    low = values[0]
    for j in range(1, n):
        hit = next((k for k in range(j + 1, n) if low < values[k] < values[j]), None)
        w1.step(f"j = {j} ({values[j]}): lowest before it is {low}. " + (f"values[{hit}] = {values[hit]} lies strictly between {low} and {values[j]}: found." if hit is not None else f"No later value strictly between {low} and {values[j]}."), Row(values, st={j: "active", **({hit: "found"} if hit is not None else {}), **{x: "mark" for x in range(j) if values[x] == low}}), Vars(low_before_j=low))
        if hit is not None:
            break
        low = min(low, values[j])
    w1.step(f"Moments {trip[0]}, {trip[1]}, {trip[2]} work: {values[trip[0]]} < {values[trip[2]]} < {values[trip[1]]}.", result="true")

    w2 = Steps("Scan from the right. The stack holds candidates for the high, decreasing; 'mid' is the biggest value ever popped. A popped value has a bigger value to its left, so it is a valid third moment. Any later (further left) value below mid completes the pattern.")
    st, mid = [], None
    for idx in range(n - 1, -1, -1):
        v = values[idx]
        if mid is not None and v < mid:
            w2.step(f"values[{idx}] = {v} < mid {mid}: it's the low, mid is the 'in between', and the value that popped mid is the high. True.", Row(values, st={idx: "found"}), Row(st, label="stack"), Vars(mid=mid), result="true")
            break
        popped = []
        while st and st[-1] < v:
            popped.append(st.pop())
        if popped:
            mid = popped[-1] if mid is None else max(mid, popped[-1])
        st.append(v)
        w2.step(f"values[{idx}] = {v}: " + (f"pops {popped}, which now have a bigger value ({v}) to their left; mid = {mid}. " if popped else "pops nothing. ") + "Push it.", Row(values, st={idx: "active"}), Row(st, label="stack"), Vars(mid=mid if mid is not None else "−∞"))

    sol(
        "low-high-between",
        summary="""
            Scan from the right with a stack that stays decreasing. When a value pops smaller values, each popped value
            has a bigger value (the popper) to its left, so it can serve as the third moment; remember the largest such
            value as `mid`. Any later value, further left, below `mid` is the first moment. O(n).
        """,
        question=[
            """
            Find indexes `i < j < k` with `values[i] < values[k] < values[j]`: a low, then a high, then something strictly in
            between. Return whether they exist.

            - **The order is fixed:** low first, high in the middle, the in-between value last.
            - **Strict inequalities:** equal values don't count.
            - **Up to 10⁵ values**, so trying all triples (~10¹⁵) or all pairs (~10¹⁰) is out.
            """
        ],
        think=[
            f"""
            Values `{values}`. Moments {trip[0]}, {trip[1]}, {trip[2]} work: {values[trip[0]]} < {values[trip[2]]} <
            {values[trip[1]]}. A sorted list like `[1, 2, 3]` never works (the last value is never below the middle one).
            """,
            fig(Row(values, st={trip[0]: "found", trip[1]: "active", trip[2]: "mark"})),
            """
            For a fixed high `j`, the best low is simply the smallest value before `j`, which gives an O(n²) method. To do
            better, scan from the right and think about the in-between value: a value `x` is usable as the third moment
            once we've seen **something bigger to its left**. Scanning leftwards, that's exactly when a bigger value pops
            `x` from a decreasing stack. Among usable third moments, the largest is the easiest to beat, so keep only it
            (`mid`). Then any value further left that's below `mid` is a valid low.
            """,
        ],
        approaches=[
            approach(
                "Try every triple",
                "brute",
                "O(n³)",
                "O(1)",
                idea=["Check every `i < j < k` for `values[i] < values[k] < values[j]`."],
                build=["Three nested loops.", "Return true at the first match, false at the end."],
                code={
                    "python": """
                        class Solution:
                            def hasLowHighBetween(self, values: List[int]) -> bool:
                                n = len(values)  #@init
                                for i in range(n):  #@loops
                                    for j in range(i + 1, n):  #@loops
                                        for k in range(j + 1, n):  #@loops
                                            if values[i] < values[k] < values[j]:  #@check
                                                return True  #@check
                                return False  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean hasLowHighBetween(int[] values) {
                                int n = values.length;  //@init
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++)  //@loops
                                            if (values[i] < values[k] && values[k] < values[j]) return true;  //@check
                                return false;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool hasLowHighBetween(vector<int>& values) {
                                int n = values.size();  //@init
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++)  //@loops
                                            if (values[i] < values[k] && values[k] < values[j]) return true;  //@check
                                return false;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool hasLowHighBetween(int* values, int valuesSize) {
                            int n = valuesSize;  //@init
                            for (int i = 0; i < n; i++)  //@loops
                                for (int j = i + 1; j < n; j++)  //@loops
                                    for (int k = j + 1; k < n; k++)  //@loops
                                        if (values[i] < values[k] && values[k] < values[j]) return true;  //@check
                            return false;  //@ret
                        }
                    """,
                },
                lines=[("init", "Number of values."), ("loops", "Every ordered triple of moments."), ("check", "Low, high, in between."), ("ret", "No triple works.")],
                complexity=["**Time O(n³).** **Space O(1).**"],
                limits=["~10¹⁵ triples for 10⁵ values. For a fixed high, only the lowest earlier value matters as the low, which removes a loop."],
                slow=True,
            ),
            approach(
                "Fix the high, use the lowest value before it",
                "better",
                "O(n²)",
                "O(1)",
                idea=["Walk `j` left to right, keeping `low` = the smallest value before `j`. For each `j` with `low < values[j]`, scan `k > j` for a value strictly between `low` and `values[j]`."],
                walk=w1,
                build=["`low = values[0]`.", "For each `j ≥ 1`: if `values[j] > low`, scan later values for one in `(low, values[j])`.", "Update `low` with `values[j]`."],
                code={
                    "python": """
                        class Solution:
                            def hasLowHighBetween(self, values: List[int]) -> bool:
                                low = values[0]  #@init
                                for j in range(1, len(values)):  #@high
                                    if values[j] > low:  #@high
                                        for k in range(j + 1, len(values)):  #@scan
                                            if low < values[k] < values[j]:  #@scan
                                                return True  #@scan
                                    low = min(low, values[j])  #@low
                                return False  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean hasLowHighBetween(int[] values) {
                                int low = values[0];  //@init
                                for (int j = 1; j < values.length; j++) {  //@high
                                    if (values[j] > low)  //@high
                                        for (int k = j + 1; k < values.length; k++)  //@scan
                                            if (low < values[k] && values[k] < values[j]) return true;  //@scan
                                    low = Math.min(low, values[j]);  //@low
                                }
                                return false;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool hasLowHighBetween(vector<int>& values) {
                                int low = values[0];  //@init
                                for (size_t j = 1; j < values.size(); j++) {  //@high
                                    if (values[j] > low)  //@high
                                        for (size_t k = j + 1; k < values.size(); k++)  //@scan
                                            if (low < values[k] && values[k] < values[j]) return true;  //@scan
                                    low = min(low, values[j]);  //@low
                                }
                                return false;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool hasLowHighBetween(int* values, int valuesSize) {
                            int low = values[0];  //@init
                            for (int j = 1; j < valuesSize; j++) {  //@high
                                if (values[j] > low)  //@high
                                    for (int k = j + 1; k < valuesSize; k++)  //@scan
                                        if (low < values[k] && values[k] < values[j]) return true;  //@scan
                                if (values[j] < low) low = values[j];  //@low
                            }
                            return false;  //@ret
                        }
                    """,
                },
                lines=[("init", "The lowest value seen so far, the best possible first moment."), ("high", "Try `j` as the high; it must beat the low, or nothing fits in between."), ("scan", "Look for a later value strictly between the low and the high."), ("low", "`values[j]` becomes a candidate low for later highs."), ("ret", "No high had a usable in-between value.")],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["The inner scan still costs O(n) per high. Scanning from the right with a stack summarises every usable third moment in a single number, `mid`."],
                slow=True,
            ),
            approach(
                "Right-to-left stack with the best in-between value",
                "best",
                "O(n)",
                "O(n)",
                idea=["Scan from the right with `mid = −∞` and a stack. For each value `v`: if `v < mid`, return true. Otherwise pop every stack value smaller than `v`, setting `mid` to the popped value (it has the bigger `v` to its left, and pops come out in increasing order, so the last popped is the largest). Push `v`."],
                walk=w2,
                build=["`mid = −∞`, empty stack.", "From the right: `v < mid` → true.", "Pop values smaller than `v` into `mid`.", "Push `v`. False at the end."],
                code={
                    "python": """
                        class Solution:
                            def hasLowHighBetween(self, values: List[int]) -> bool:
                                mid = float("-inf")  #@init
                                stack = []  #@init
                                for v in reversed(values):  #@loop
                                    if v < mid:  #@found
                                        return True  #@found
                                    while stack and stack[-1] < v:  #@pop
                                        mid = stack.pop()  #@pop
                                    stack.append(v)  #@push
                                return False  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean hasLowHighBetween(int[] values) {
                                long mid = Long.MIN_VALUE;  //@init
                                int[] stack = new int[values.length];  //@init
                                int top = 0;  //@init
                                for (int i = values.length - 1; i >= 0; i--) {  //@loop
                                    if (values[i] < mid) return true;  //@found
                                    while (top > 0 && stack[top - 1] < values[i]) mid = stack[--top];  //@pop
                                    stack[top++] = values[i];  //@push
                                }
                                return false;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool hasLowHighBetween(vector<int>& values) {
                                long long mid = LLONG_MIN;  //@init
                                vector<int> stack;  //@init
                                for (int i = (int) values.size() - 1; i >= 0; i--) {  //@loop
                                    if (values[i] < mid) return true;  //@found
                                    while (!stack.empty() && stack.back() < values[i]) {  //@pop
                                        mid = stack.back();  //@pop
                                        stack.pop_back();  //@pop
                                    }
                                    stack.push_back(values[i]);  //@push
                                }
                                return false;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool hasLowHighBetween(int* values, int valuesSize) {
                            long long mid = LLONG_MIN;  //@init
                            int* stack = malloc(valuesSize * sizeof(int));  //@init
                            int top = 0;  //@init
                            bool found = false;  //@init
                            for (int i = valuesSize - 1; i >= 0 && !found; i--) {  //@loop
                                if (values[i] < mid) { found = true; break; }  //@found
                                while (top > 0 && stack[top - 1] < values[i]) mid = stack[--top];  //@pop
                                stack[top++] = values[i];  //@push
                            }
                            free(stack);  //@ret
                            return found;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "`mid` = the largest value known to have something bigger to its left, which is the best in-between candidate. It starts below everything.", {"java": "A `long` minimum, so no `int` value compares below it at the start.", "cpp": "A 64-bit minimum, so no `int` value compares below it at the start.", "c": "A 64-bit minimum, so no `int` value compares below it at the start."}),
                    ("loop", "Right to left: every value seen so far lies to the right of the current one."),
                    ("found", "The current value is below `mid`, so it's the low, `mid` is the in-between value, and whatever popped `mid` is the high between them."),
                    ("pop", "Smaller values on the stack now have a bigger value (`v`) on their left: each is a valid in-between candidate. The stack is decreasing, so they pop in increasing order and the last one is the largest. `mid` never shrinks: every value on the stack is at least `mid` (a smaller one would have returned true), so anything popped is too."),
                    ("push", "`v` becomes a candidate high for values further left."),
                    ("ret", "No low ever went below `mid`."),
                ],
                complexity=["**Time O(n):** each value is pushed and popped at most once. **Space O(n)** for the stack."],
            ),
        ],
        takeaways=[
            """
            - For a three-part pattern, pick the part that's hardest to choose and summarise the rest in one number.
            - Scanning right to left, **being popped** means "something bigger exists to my left", which is exactly the
              condition for the in-between value.
            - Keep the best candidate (largest `mid`), since it's the easiest for a low to beat.
            """
        ],
    )


@problem
def strongest_crew_stretch():
    strength = [3, 1, 6, 4, 5, 2]
    n = len(strength)
    pre = [0]
    for v in strength:
        pre.append(pre[-1] + v)
    L, R = [0] * n, [n - 1] * n
    st = []
    for i in range(n):
        while st and strength[st[-1]] >= strength[i]:
            st.pop()
        L[i] = st[-1] + 1 if st else 0
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and strength[st[-1]] >= strength[i]:
            st.pop()
        R[i] = st[-1] - 1 if st else n - 1
        st.append(i)
    power = [strength[i] * (pre[R[i] + 1] - pre[L[i]]) for i in range(n)]
    want = max(power)
    bi = power.index(want)
    assert want == max(min(strength[a:b + 1]) * sum(strength[a:b + 1]) for a in range(n) for b in range(a, n))

    w1 = Steps("Every crew: fix the first worker, extend to the right, keeping the weakest strength and the running sum.")
    best = 0
    for i in range(n):
        low, s, pw = strength[i], 0, []
        for j in range(i, n):
            low, s = min(low, strength[j]), s + strength[j]
            pw.append(low * s)
        best = max(best, max(pw))
        w1.step(f"Start at worker {i}: powers {pw} for crews ending at {i}..{n - 1}.", Row(strength, st={i: "active"}), Row(["·"] * i + pw, label="power"), Vars(best=best))
    w1.step(f"Strongest crew: {best}.", result=best)

    w2 = Steps("The best crew with weakest member i spreads as far as possible: until a weaker worker on each side. Stacks find those boundaries, prefix sums give the crew's total.")
    w2.step("Prefix sums: the crew l..r sums to P[r + 1] − P[l].", Row(strength, label="strength"), Row(pre, label="prefix P"))
    for i in range(n):
        w2.step(f"Worker {i} (strength {strength[i]}) as the weakest: crew {L[i]}..{R[i]}, sum {pre[R[i] + 1] - pre[L[i]]}, power {strength[i]} × {pre[R[i] + 1] - pre[L[i]]} = {power[i]}.", Row(strength, st={**{x: "mark" for x in range(L[i], R[i] + 1)}, i: "active"}, label="strength"), Row(power[:i + 1] + ["·"] * (n - i - 1), label="power"))
    w2.step(f"Strongest crew: {want}.", result=want)

    sol(
        "strongest-crew-stretch",
        summary="""
            Every crew has a weakest member. For worker `i` as the weakest, the sum only grows as the crew widens, so the
            best such crew stretches until a strictly weaker worker on each side. Monotonic stacks find those boundaries
            for every worker, prefix sums give each crew's total, and the answer is the best `strength[i] × sum`. O(n).
        """,
        question=[
            """
            A crew is a run of neighbouring workers; its power is (weakest strength) × (total strength). Return the largest
            power over all crews.

            - **Strengths are positive**, so adding a worker never lowers the sum, though it may lower the minimum.
            - **Up to 10⁵ workers with strength up to 10⁶**: a sum reaches 10¹¹ and a power 10¹⁷, which needs 64-bit
              integers (still below 9.2 × 10¹⁸).
            """
        ],
        think=[
            f"""
            Strengths `{strength}`. The crew `6, 4, 5` has weakest 4 and total 15: power 60. The whole row has weakest 1
            and total {sum(strength)}: power {sum(strength)}. The best is **{want}**, from the crew
            {L[bi]}..{R[bi]} with weakest worker {bi}.
            """,
            table(["worker", "strength", "widest crew as weakest", "sum", "power"], *[(i, strength[i], f"{L[i]}..{R[i]}", pre[R[i] + 1] - pre[L[i]], power[i]) for i in range(n)]),
            """
            Group crews by their weakest member. If worker `i` is the weakest, widening the crew (while keeping `i` the
            weakest) only adds positive strengths, so the widest such crew is best. It reaches until the nearest strictly
            weaker worker on each side. So the answer is the best of `n` candidates, and each needs the nearest weaker
            neighbours (monotonic stacks) and a range sum (prefix sums).
            """,
        ],
        approaches=[
            approach(
                "Every crew, with running minimum and sum",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each first worker, extend the crew to the right, updating the weakest strength and the total; each crew's power is their product."],
                walk=w1,
                build=["For each start `i`: `low = strength[i]`, `sum = 0`.", "For each end `j`: update both and compare `low × sum` with the best.", "Return the best (64-bit)."],
                code={
                    "python": """
                        class Solution:
                            def strongestCrew(self, strength: List[int]) -> int:
                                best = 0  #@init
                                for i in range(len(strength)):  #@start
                                    low, total = strength[i], 0  #@start
                                    for j in range(i, len(strength)):  #@extend
                                        low = min(low, strength[j])  #@extend
                                        total += strength[j]  #@extend
                                        best = max(best, low * total)  #@power
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long strongestCrew(int[] strength) {
                                long best = 0;  //@init
                                for (int i = 0; i < strength.length; i++) {  //@start
                                    int low = strength[i];  //@start
                                    long total = 0;  //@start
                                    for (int j = i; j < strength.length; j++) {  //@extend
                                        low = Math.min(low, strength[j]);  //@extend
                                        total += strength[j];  //@extend
                                        best = Math.max(best, low * total);  //@power
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long strongestCrew(vector<int>& strength) {
                                long long best = 0;  //@init
                                for (size_t i = 0; i < strength.size(); i++) {  //@start
                                    int low = strength[i];  //@start
                                    long long total = 0;  //@start
                                    for (size_t j = i; j < strength.size(); j++) {  //@extend
                                        low = min(low, strength[j]);  //@extend
                                        total += strength[j];  //@extend
                                        best = max(best, low * total);  //@power
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long strongestCrew(int* strength, int strengthSize) {
                            long long best = 0;  //@init
                            for (int i = 0; i < strengthSize; i++) {  //@start
                                int low = strength[i];  //@start
                                long long total = 0;  //@start
                                for (int j = i; j < strengthSize; j++) {  //@extend
                                    if (strength[j] < low) low = strength[j];  //@extend
                                    total += strength[j];  //@extend
                                    if (low * total > best) best = low * total;  //@power
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Best power so far."), ("start", "Crews starting at worker `i`; the total is 64-bit."), ("extend", "Add worker `j`: the weakest may drop, the total grows."), ("power", "This crew's power (64-bit because `total` is)."), ("ret", "The strongest crew.")],
                complexity=["**Time O(n²)** crews. **Space O(1).**"],
                limits=["~5 × 10⁹ crews for 10⁵ workers. Only one crew per weakest worker can be the best (the widest), so n candidates suffice."],
                slow=True,
            ),
            approach(
                "Widest crew per weakest worker",
                "best",
                "O(n)",
                "O(n)",
                idea=["Prefix sums `P`. With a stack, find for each worker the nearest strictly weaker worker on the left (`left[i]` = the index after it) and on the right (`right[i]` = the index before it). Worker `i`'s candidate power is `strength[i] × (P[right[i] + 1] − P[left[i]])`. Return the largest."],
                walk=w2,
                build=["Prefix sums in 64 bits.", "Left pass (pop while `≥`): `left[i]` = after the nearest weaker worker, or 0.", "Right pass (pop while `≥`): `right[i]` = before the nearest weaker worker, or `n − 1`.", "Best of `strength[i] × rangeSum`."],
                code={
                    "python": """
                        class Solution:
                            def strongestCrew(self, strength: List[int]) -> int:
                                n = len(strength)  #@prefix
                                P = [0] * (n + 1)  #@prefix
                                for i, v in enumerate(strength):  #@prefix
                                    P[i + 1] = P[i] + v  #@prefix
                                left, stack = [0] * n, []  #@left
                                for i in range(n):  #@left
                                    while stack and strength[stack[-1]] >= strength[i]:  #@left
                                        stack.pop()  #@left
                                    left[i] = stack[-1] + 1 if stack else 0  #@left
                                    stack.append(i)  #@left
                                best, stack = 0, []  #@right
                                for i in range(n - 1, -1, -1):  #@right
                                    while stack and strength[stack[-1]] >= strength[i]:  #@right
                                        stack.pop()  #@right
                                    right = stack[-1] - 1 if stack else n - 1  #@right
                                    best = max(best, strength[i] * (P[right + 1] - P[left[i]]))  #@power
                                    stack.append(i)  #@right
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long strongestCrew(int[] strength) {
                                int n = strength.length;  //@prefix
                                long[] P = new long[n + 1];  //@prefix
                                for (int i = 0; i < n; i++) P[i + 1] = P[i] + strength[i];  //@prefix
                                int[] left = new int[n], stack = new int[n];  //@left
                                int top = 0;  //@left
                                for (int i = 0; i < n; i++) {  //@left
                                    while (top > 0 && strength[stack[top - 1]] >= strength[i]) top--;  //@left
                                    left[i] = top > 0 ? stack[top - 1] + 1 : 0;  //@left
                                    stack[top++] = i;  //@left
                                }
                                long best = 0;  //@right
                                top = 0;  //@right
                                for (int i = n - 1; i >= 0; i--) {  //@right
                                    while (top > 0 && strength[stack[top - 1]] >= strength[i]) top--;  //@right
                                    int right = top > 0 ? stack[top - 1] - 1 : n - 1;  //@right
                                    best = Math.max(best, strength[i] * (P[right + 1] - P[left[i]]));  //@power
                                    stack[top++] = i;  //@right
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long strongestCrew(vector<int>& strength) {
                                int n = strength.size();  //@prefix
                                vector<long long> P(n + 1, 0);  //@prefix
                                for (int i = 0; i < n; i++) P[i + 1] = P[i] + strength[i];  //@prefix
                                vector<int> left(n), stack;  //@left
                                for (int i = 0; i < n; i++) {  //@left
                                    while (!stack.empty() && strength[stack.back()] >= strength[i]) stack.pop_back();  //@left
                                    left[i] = stack.empty() ? 0 : stack.back() + 1;  //@left
                                    stack.push_back(i);  //@left
                                }
                                long long best = 0;  //@right
                                stack.clear();  //@right
                                for (int i = n - 1; i >= 0; i--) {  //@right
                                    while (!stack.empty() && strength[stack.back()] >= strength[i]) stack.pop_back();  //@right
                                    int right = stack.empty() ? n - 1 : stack.back() - 1;  //@right
                                    best = max(best, strength[i] * (P[right + 1] - P[left[i]]));  //@power
                                    stack.push_back(i);  //@right
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long strongestCrew(int* strength, int strengthSize) {
                            int n = strengthSize;  //@prefix
                            long long* P = malloc((n + 1) * sizeof(long long));  //@prefix
                            P[0] = 0;  //@prefix
                            for (int i = 0; i < n; i++) P[i + 1] = P[i] + strength[i];  //@prefix
                            int* left = malloc(n * sizeof(int));  //@left
                            int* stack = malloc(n * sizeof(int));  //@left
                            int top = 0;  //@left
                            for (int i = 0; i < n; i++) {  //@left
                                while (top > 0 && strength[stack[top - 1]] >= strength[i]) top--;  //@left
                                left[i] = top > 0 ? stack[top - 1] + 1 : 0;  //@left
                                stack[top++] = i;  //@left
                            }
                            long long best = 0;  //@right
                            top = 0;  //@right
                            for (int i = n - 1; i >= 0; i--) {  //@right
                                while (top > 0 && strength[stack[top - 1]] >= strength[i]) top--;  //@right
                                int right = top > 0 ? stack[top - 1] - 1 : n - 1;  //@right
                                long long power = strength[i] * (P[right + 1] - P[left[i]]);  //@power
                                if (power > best) best = power;  //@power
                                stack[top++] = i;  //@right
                            }
                            free(P);  //@ret
                            free(left);  //@ret
                            free(stack);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("prefix", "Prefix sums, so any crew's total is one subtraction (64-bit: up to 10¹¹)."),
                    ("left", "Nearest strictly weaker worker on the left, via a stack of increasing strengths; the crew can start right after it (or at 0)."),
                    ("right", "The same from the right: the crew can end right before the nearest strictly weaker worker (or at `n − 1`). Equal strengths don't stop the crew; a tied weakest member just gives the same crew twice, which is harmless for a maximum."),
                    ("power", "Worker `i` as the weakest of its widest crew. The multiplication happens in 64 bits because the sum is 64-bit."),
                    ("ret", "The strongest of the `n` candidates."),
                ],
                complexity=["**Time O(n):** prefix sums plus two stack passes. **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - **min × sum over subarrays:** fix the minimum; with positive values, the widest subarray around it is best.
            - Nearest smaller on each side (monotonic stacks) + prefix sums = O(n).
            - For a maximum, ties can be counted twice; for a sum over subarrays (like the stretch-lows problem), they can't.
            """
        ],
    )


@problem
def who_can_you_see():
    heights = [5, 3, 4, 4, 1, 6]
    n = len(heights)

    def visible(i):
        out = []
        for j in range(i + 1, n):
            if all(heights[x] < min(heights[i], heights[j]) for x in range(i + 1, j)):
                out.append(j)
        return out

    vis = [visible(i) for i in range(n)]
    want = [len(v) for v in vis]

    w1 = Steps("For each person, walk back down the line, tracking the tallest person passed so far. Someone is visible if everyone passed is shorter than both; once someone at least as tall as you has been passed, nobody further is visible.")
    for i in range(n):
        w1.step(f"Person {i} (height {heights[i]}) sees {vis[i] or 'nobody'}: {want[i]}.", Row(heights, st={**{j: "found" for j in vis[i]}, i: "active"}), Row(want[:i + 1] + ["·"] * (n - i - 1), label="can see"))
    w1.step(f"Counts: {want}.", result=str(want))

    w2 = Steps("Go from the back of the line to the front. The stack holds the people the current person could possibly see, nearest on top, getting taller downwards.")
    st, res = [], [0] * n
    for i in range(n - 1, -1, -1):
        h, c = heights[i], 0
        popped = []
        while st and heights[st[-1]] < h:
            popped.append(st.pop())
            c += 1
        extra, same = None, False
        if st:
            c += 1
            extra = st[-1]
            if heights[st[-1]] == h:
                st.pop()
                same = True
        st.append(i)
        res[i] = c
        msg = f"Person {i} (height {heights[i]}): "
        msg += f"sees shorter {popped}, who are now hidden from everyone further forward; " if popped else ""
        msg += (f"also sees {extra} (height {heights[extra]}), the first one at least as tall, and nobody past them" + ("; equal height, so person " + str(extra) + " is hidden from now on" if same else "") + ". ") if extra is not None else "nobody taller behind. "
        msg += f"Count {c}."
        w2.step(msg, Row(heights, st={i: "active", **{j: "found" for j in popped}, **({extra: "found"} if extra is not None else {})}), Row([f"{j}:{heights[j]}" for j in reversed(st)], label="stack (top first)"), Row(["·"] * i + res[i:], label="can see"))
    w2.step(f"Counts: {res}.", result=str(res))

    sol(
        "who-can-you-see",
        summary="""
            Go from the back of the line forward with a stack of people still visible from the front, getting taller from
            top to bottom. The current person sees every shorter person on top (and hides them from everyone further
            forward, so pop them), plus the first person at least as tall, if any. An equal-height person gets hidden too.
            O(n).
        """,
        question=[
            """
            Everyone faces the back of the line. Person `i` sees person `j > i` if everyone strictly between them is shorter
            than both. Return how many people each person sees.

            - **Neighbours always see each other** (nobody is between them).
            - **Heights repeat:** someone of equal height between you and `j` blocks the view (they're not strictly
              shorter).
            - **Up to 10⁵ people.**
            """
        ],
        think=[
            f"""
            Heights `{heights}`. Person 0 (5) sees 3 and the first 4 (everyone between is shorter than both), then the 6
            (everyone between is shorter than 5 and 6), but not the second 4 (the first 4 is between them and isn't shorter
            than 4). Counts: `{want}`.
            """,
            fig(Row(heights, st={**{j: "found" for j in vis[0]}, 0: "active"}), caption="What person 0 sees."),
            """
            Two facts about person `i` looking back:

            1. They see a sequence of people that keep getting taller: each person seen must be taller than everyone
               between, including the earlier ones seen.
            2. Once they see someone at least as tall as themselves, nobody past that person is visible.

            And for the people in front of `i`: anyone shorter than `i` standing behind `i` is now hidden from them for good
            (`i` is between, and taller). So walking from the back, a stack of 'still visible' people does it: the current
            person counts and removes the shorter ones on top, counts the next one if any, and joins the stack.
            """,
        ],
        approaches=[
            approach(
                "Look back from each person",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each person `i`, walk `j = i+1, i+2, …` keeping `tallest` = the tallest person strictly between `i` and `j`. Person `j` is visible if `tallest < min(h[i], h[j])`. Stop once `tallest ≥ h[i]`: nobody further can be seen."],
                walk=w1,
                build=["For each `i`: `tallest = 0`, `count = 0`.", "For each `j > i`: check visibility, then fold `h[j]` into `tallest`.", "Stop early when `tallest ≥ h[i]`."],
                code={
                    "python": """
                        class Solution:
                            def canSee(self, heights: List[int]) -> List[int]:
                                n = len(heights)  #@init
                                res = [0] * n  #@init
                                for i in range(n):  #@each
                                    tallest = 0  #@each
                                    for j in range(i + 1, n):  #@walk
                                        if tallest < min(heights[i], heights[j]):  #@see
                                            res[i] += 1  #@see
                                        tallest = max(tallest, heights[j])  #@block
                                        if tallest >= heights[i]:  #@block
                                            break  #@block
                                return res  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] canSee(int[] heights) {
                                int n = heights.length;  //@init
                                int[] res = new int[n];  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    int tallest = 0;  //@each
                                    for (int j = i + 1; j < n; j++) {  //@walk
                                        if (tallest < Math.min(heights[i], heights[j])) res[i]++;  //@see
                                        tallest = Math.max(tallest, heights[j]);  //@block
                                        if (tallest >= heights[i]) break;  //@block
                                    }
                                }
                                return res;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> canSee(vector<int>& heights) {
                                int n = heights.size();  //@init
                                vector<int> res(n, 0);  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    int tallest = 0;  //@each
                                    for (int j = i + 1; j < n; j++) {  //@walk
                                        if (tallest < min(heights[i], heights[j])) res[i]++;  //@see
                                        tallest = max(tallest, heights[j]);  //@block
                                        if (tallest >= heights[i]) break;  //@block
                                    }
                                }
                                return res;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* canSee(int* heights, int heightsSize, int* returnSize) {
                            int n = heightsSize;  //@init
                            int* res = calloc(n, sizeof(int));  //@init
                            for (int i = 0; i < n; i++) {  //@each
                                int tallest = 0;  //@each
                                for (int j = i + 1; j < n; j++) {  //@walk
                                    int lower = heights[i] < heights[j] ? heights[i] : heights[j];  //@see
                                    if (tallest < lower) res[i]++;  //@see
                                    if (heights[j] > tallest) tallest = heights[j];  //@block
                                    if (tallest >= heights[i]) break;  //@block
                                }
                            }
                            *returnSize = n;  //@ret
                            return res;  //@ret
                        }
                    """,
                },
                lines=[("init", "One count per person."), ("each", "`tallest` = tallest person between `i` and the current `j` (nobody yet; heights are ≥ 1)."), ("walk", "People behind `i`, nearest first."), ("see", "Everyone between is shorter than both."), ("block", "Person `j` now stands between `i` and everyone further. If they're at least as tall as `i`, nobody further is visible."), ("ret", "All counts.")],
                complexity=["**Time O(n²)** in the worst case (heights rising toward the front: nobody blocks early). **Space O(1).**"],
                limits=["Each person re-walks people that a taller person in front of them already hid. Processing from the back with a stack removes hidden people once and for all."],
                slow=True,
            ),
            approach(
                "Stack of still-visible people, from the back",
                "best",
                "O(n)",
                "O(n)",
                idea=["Process people from the last to the first with a stack (nearest on top, taller below). For person `i`: pop and count everyone shorter. If the stack isn't empty, count the top too (the first one at least as tall), and pop it if its height equals `h[i]`. Push `i`."],
                walk=w2,
                build=["Empty stack; go from the back.", "Pop and count shorter people.", "Count the next one if any; pop it if equal height.", "Push the current person."],
                code={
                    "python": """
                        class Solution:
                            def canSee(self, heights: List[int]) -> List[int]:
                                n = len(heights)  #@init
                                res, stack = [0] * n, []  #@init
                                for i in range(n - 1, -1, -1):  #@loop
                                    h = heights[i]  #@loop
                                    while stack and stack[-1] < h:  #@shorter
                                        stack.pop()  #@shorter
                                        res[i] += 1  #@shorter
                                    if stack:  #@taller
                                        res[i] += 1  #@taller
                                        if stack[-1] == h:  #@equal
                                            stack.pop()  #@equal
                                    stack.append(h)  #@push
                                return res  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] canSee(int[] heights) {
                                int n = heights.length;  //@init
                                int[] res = new int[n], stack = new int[n];  //@init
                                int top = 0;  //@init
                                for (int i = n - 1; i >= 0; i--) {  //@loop
                                    int h = heights[i];  //@loop
                                    while (top > 0 && stack[top - 1] < h) { top--; res[i]++; }  //@shorter
                                    if (top > 0) {  //@taller
                                        res[i]++;  //@taller
                                        if (stack[top - 1] == h) top--;  //@equal
                                    }
                                    stack[top++] = h;  //@push
                                }
                                return res;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> canSee(vector<int>& heights) {
                                int n = heights.size();  //@init
                                vector<int> res(n, 0), stack;  //@init
                                for (int i = n - 1; i >= 0; i--) {  //@loop
                                    int h = heights[i];  //@loop
                                    while (!stack.empty() && stack.back() < h) { stack.pop_back(); res[i]++; }  //@shorter
                                    if (!stack.empty()) {  //@taller
                                        res[i]++;  //@taller
                                        if (stack.back() == h) stack.pop_back();  //@equal
                                    }
                                    stack.push_back(h);  //@push
                                }
                                return res;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* canSee(int* heights, int heightsSize, int* returnSize) {
                            int n = heightsSize;  //@init
                            int* res = calloc(n, sizeof(int));  //@init
                            int* stack = malloc(n * sizeof(int));  //@init
                            int top = 0;  //@init
                            for (int i = n - 1; i >= 0; i--) {  //@loop
                                int h = heights[i];  //@loop
                                while (top > 0 && stack[top - 1] < h) { top--; res[i]++; }  //@shorter
                                if (top > 0) {  //@taller
                                    res[i]++;  //@taller
                                    if (stack[top - 1] == h) top--;  //@equal
                                }
                                stack[top++] = h;  //@push
                            }
                            free(stack);  //@ret
                            *returnSize = n;  //@ret
                            return res;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Counts, and a stack of heights still visible from the front of the line (nearest on top)."),
                    ("loop", "From the back of the line to the front."),
                    ("shorter", "Each shorter person on top is visible to `i` (everyone between them was shorter still, or they'd have been popped). After `i`, they're hidden from everyone in front: pop them."),
                    ("taller", "The first person at least as tall as `i` is visible too; nobody beyond them is."),
                    ("equal", "An equal-height person is hidden from everyone in front of `i` (`i` stands between and isn't shorter). A strictly taller one stays visible."),
                    ("push", "`i` is visible from the person directly in front."),
                    ("ret", "All counts."),
                ],
                complexity=["**Time O(n):** each person is pushed once and popped at most once. **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - **Visibility in a line = monotonic stack:** a taller person permanently hides shorter people behind them.
            - Count what you pop: the popped elements are often exactly the answer.
            - Decide ties explicitly; here an equal height blocks the view, so equals are popped as well.
            """
        ],
    )


@problem
def price_streak_tracker():
    prices = [7, 3, 4, 4, 8, 2, 9]
    want = []
    for i, p in enumerate(prices):
        c = 0
        for q in reversed(prices[:i + 1]):
            if q > p:
                break
            c += 1
        want.append(c)

    w1 = Steps("Keep every price. On each record, count backwards from today while prices are at most today's.")
    for i, p in enumerate(prices):
        lo = i - want[i] + 1
        w1.step(f"record({p}): counting back from day {i}, days {lo}..{i} are ≤ {p}" + (f"; day {lo - 1} ({prices[lo - 1]}) is higher" if lo > 0 else "") + f". Streak {want[i]}.", Row(prices[:i + 1], st={**{x: "mark" for x in range(lo, i)}, i: "active"}, label="prices"), Row(want[:i + 1], label="streak"))
    w1.step(f"Returned {want}.", result=str(want))

    w2 = Steps("Keep a stack of (price, streak) pairs with strictly falling prices. A new price swallows every pair with a price at most its own, adding their streaks to its own.")
    st = []
    for p in prices:
        streak, eaten = 1, []
        while st and st[-1][0] <= p:
            eaten.append(st.pop())
            streak += eaten[-1][1]
        st.append((p, streak))
        w2.step(f"record({p}): " + (f"absorb {[f'{a}×{b}' for a, b in eaten]} (price×streak), so the streak is 1 + {' + '.join(str(b) for _, b in eaten)} = {streak}." if eaten else "the top's price is higher (or there is none): streak 1."), Row([f"{a}×{b}" for a, b in st], label="stack (price×streak)"), Vars(returned=streak))
    w2.step(f"Returned {want}.", result=str(want))

    sol(
        "price-streak-tracker",
        summary="""
            Once a day is followed by a day with a higher-or-equal price, any later streak that reaches the earlier day also
            covers the later one, so the earlier day never needs to be checked on its own again. Keep a stack of
            (price, streak) pairs with strictly falling prices; a new price pops every pair it's at least as high as and
            adds their streaks to 1. Amortised O(1) per call.
        """,
        question=[
            """
            Each `record(price)` adds the next day and returns its streak: the number of consecutive days ending today
            (including today) with price **at most** today's.

            - **"At most" includes equal prices**: equal days extend the streak.
            - **The first day's streak is 1**, as is any day after a higher price.
            - **Up to 10⁵ calls**, so a call can't afford to look at every past day.
            """
        ],
        think=[
            f"""
            Prices recorded in order: `{prices}`. The streaks returned are `{want}`. For example, `8` covers `7, 3, 4, 4, 8`
            (all at most 8): streak 5. `9` covers everything: 7.

            When `8` arrives, the days with 3, 4, 4 are now 'inside' its streak. Any future day that reaches back as far as
            `8` also passes them (they're lower), and a day that stops before `8` never gets there. So those days can be
            merged into `8`'s entry: remember `8` together with the size of its streak. The entries that remain have
            strictly falling prices from bottom to top: a stack.
            """,
            table(["call", "price", "streak"], *[(i + 1, p, s) for i, (p, s) in enumerate(zip(prices, want))]),
        ],
        approaches=[
            approach(
                "Store every price, count backwards",
                "brute",
                "O(n) per call",
                "O(n)",
                idea=["Append each price to a list, then walk backwards from the end while prices are at most the new one. The number of steps is the streak."],
                walk=w1,
                build=["A list of all prices.", "`record`: append, then count back from the end while `≤ price`.", "Return the count."],
                code={
                    "python": """
                        class PriceStreak:
                            def __init__(self):
                                self.days = []  #@init

                            def record(self, price: int) -> int:
                                self.days.append(price)  #@add
                                streak = 0  #@count
                                for p in reversed(self.days):  #@count
                                    if p > price:  #@stop
                                        break  #@stop
                                    streak += 1  #@count
                                return streak  #@ret
                    """,
                    "java": """
                        class PriceStreak {
                            private final List<Integer> days = new ArrayList<>();  //@init

                            public PriceStreak() {
                            }

                            public int record(int price) {
                                days.add(price);  //@add
                                int streak = 0;  //@count
                                for (int i = days.size() - 1; i >= 0; i--) {  //@count
                                    if (days.get(i) > price) break;  //@stop
                                    streak++;  //@count
                                }
                                return streak;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class PriceStreak {
                            vector<int> days;  //@init

                        public:
                            PriceStreak() {
                            }

                            int record(int price) {
                                days.push_back(price);  //@add
                                int streak = 0;  //@count
                                for (int i = (int) days.size() - 1; i >= 0; i--) {  //@count
                                    if (days[i] > price) break;  //@stop
                                    streak++;  //@count
                                }
                                return streak;  //@ret
                            }
                        };
                    """,
                },
                lines=[("init", "Every price so far."), ("add", "Today joins the history."), ("count", "Walk back from today, counting days."), ("stop", "A higher price ends the streak."), ("ret", "Today's streak.")],
                complexity=["**Time O(n) per call**, O(n²) in total for rising prices. **Space O(n).**"],
                limits=["Rising prices make every call walk the whole history: ~5 × 10⁹ steps for 10⁵ calls. Days already inside a later, higher streak never need to be walked again; merge them."],
                slow=True,
                langs=["python", "java", "cpp"],
            ),
            approach(
                "Stack of (price, streak) pairs",
                "best",
                "O(1) amortised",
                "O(n)",
                idea=["Keep pairs `(price, streak)` with strictly falling prices from bottom to top. `record(price)`: start with streak 1; while the top's price is `≤ price`, pop it and add its streak. Push `(price, streak)` and return the streak."],
                walk=w2,
                build=["An empty stack of pairs.", "`record`: streak = 1; pop and absorb every top pair with price ≤ today's.", "Push today's pair; return the streak."],
                code={
                    "python": """
                        class PriceStreak:
                            def __init__(self):
                                self.stack = []  #@init

                            def record(self, price: int) -> int:
                                streak = 1  #@today
                                while self.stack and self.stack[-1][0] <= price:  #@absorb
                                    streak += self.stack.pop()[1]  #@absorb
                                self.stack.append((price, streak))  #@push
                                return streak  #@ret
                    """,
                    "java": """
                        class PriceStreak {
                            private final Deque<int[]> stack = new ArrayDeque<>();  //@init

                            public PriceStreak() {
                            }

                            public int record(int price) {
                                int streak = 1;  //@today
                                while (!stack.isEmpty() && stack.peek()[0] <= price) streak += stack.pop()[1];  //@absorb
                                stack.push(new int[] {price, streak});  //@push
                                return streak;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class PriceStreak {
                            vector<pair<int, int>> stack;  //@init

                        public:
                            PriceStreak() {
                            }

                            int record(int price) {
                                int streak = 1;  //@today
                                while (!stack.empty() && stack.back().first <= price) {  //@absorb
                                    streak += stack.back().second;  //@absorb
                                    stack.pop_back();  //@absorb
                                }
                                stack.push_back({price, streak});  //@push
                                return streak;  //@ret
                            }
                        };
                    """,
                },
                lines=[
                    ("init", "Pairs (price, streak), prices strictly falling from bottom to top.", {"java": "`ArrayDeque` used as a stack: `push`, `peek` and `pop` work at the same end."}),
                    ("today", "Today counts itself."),
                    ("absorb", "A pair on top with price ≤ today's: its whole streak is ≤ its price ≤ today's, so it all joins today's streak. Its days are now represented by today's pair."),
                    ("push", "Today's pair goes on top; the price below it (if any) is strictly higher."),
                    ("ret", "Today's streak."),
                ],
                complexity=["**Time O(1) amortised per call:** each day's pair is pushed once and popped at most once over all calls. **Space O(n)** in the worst case (falling prices)."],
                langs=["python", "java", "cpp"],
            ),
        ],
        takeaways=[
            """
            - **Online 'previous greater' queries:** a monotonic stack where each entry carries the count it has absorbed.
            - Merging dominated entries is what makes the cost amortised O(1).
            - The same trick answers 'how far back until a bigger value' for any stream.
            """
        ],
    )
