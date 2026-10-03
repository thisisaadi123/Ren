"""Stacks & Queues: monotonic deque."""
from collections import deque

from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def window_peaks():
    temps, k = [3, 1, -2, 5, 4, 2, 0, 6], 3
    n = len(temps)
    want = [max(temps[i:i + k]) for i in range(n - k + 1)]

    w1 = Steps("Look at every window and scan all k readings for the highest.")
    for i in range(n - k + 1):
        w1.step(f"Window {i}..{i + k - 1}: {temps[i:i + k]}, highest {want[i]}.", Row(temps, st={j: ("found" if temps[j] == want[i] else "mark") for j in range(i, i + k)}), Row(want[:i + 1], label="peaks"))
    w1.step(f"Peaks: {want}.", result=str(want))

    pre = [0] * n
    suf = [0] * n
    for i in range(n):
        pre[i] = temps[i] if i % k == 0 else max(pre[i - 1], temps[i])
    for i in range(n - 1, -1, -1):
        suf[i] = temps[i] if i == n - 1 or (i + 1) % k == 0 else max(suf[i + 1], temps[i])
    blocks = [f"block {b}" for b in range(0, n, k)]
    w2 = Steps(f"Cut the readings into blocks of k = {k}. Any window covers the end of one block and the start of the next, so its peak = max(best from i to its block's end, best from the next block's start to the window's end).")
    w2.step(f"Blocks start at {list(range(0, n, k))}. Running max from each block's start:", Row(temps, label="temps"), Row(pre, label="max from block start"))
    w2.step("Running max back from each block's end:", Row(temps, label="temps"), Row(pre, label="max from block start"), Row(suf, label="max to block end"))
    for i in range(n - k + 1):
        j = i + k - 1
        w2.step(f"Window {i}..{j}: max(to-block-end at {i} = {suf[i]}, from-block-start at {j} = {pre[j]}) = {max(suf[i], pre[j])}.", Row(temps, st={i: "active", j: "active", **{x: "mark" for x in range(i + 1, j)}}, label="temps"), Row(suf, st={i: "found"}, label="max to block end"), Row(pre, st={j: "found"}, label="max from block start"))
    w2.step(f"Peaks: {want}.", result=str(want))
    del blocks

    w3 = Steps("A deque of indices whose readings decrease from front to back. The front is the current window's peak.")
    dq, out = deque(), []
    for i, v in enumerate(temps):
        popped = []
        while dq and temps[dq[-1]] <= v:
            popped.append(temps[dq.pop()])
        dq.append(i)
        expired = None
        if dq[0] <= i - k:
            expired = temps[dq.popleft()]
        if i >= k - 1:
            out.append(temps[dq[0]])
        msg = f"Hour {i} ({v}): "
        msg += f"drop {popped} from the back (never a peak again while {v} is in view); " if popped else ""
        msg += "push it."
        if expired is not None:
            msg += f" The front ({expired}) left the window: drop it."
        if i >= k - 1:
            msg += f" Peak of {i - k + 1}..{i}: {out[-1]}."
        w3.step(msg, Row(temps, st={**{x: "mark" for x in range(max(0, i - k + 1), i + 1)}, i: "active"}), Row([f"{x}:{temps[x]}" for x in dq], label="deque (hour:reading)"), Row(out or ["·"], label="peaks"))
    w3.step(f"Peaks: {out}.", result=str(out))

    sol(
        "window-peaks",
        summary="""
            Keep a deque of hours whose readings strictly decrease from front to back. A new reading first removes every
            reading at the back that's no higher (those can never be a peak while it's on screen), then joins at the back;
            the front leaves when it scrolls out of the window. The front is always the current peak. O(n).
        """,
        question=[
            f"""
            Slide a window of `k` consecutive readings from the start to the end, one hour at a time. For each of the
            `n − k + 1` positions, report the highest reading in view.

            - **Readings can repeat and be negative.**
            - **`k` can be 1** (every reading is its own peak) or `n` (a single window).
            - **Up to 10⁵ readings and `k` up to `n`**, so `n × k` can reach 10¹⁰.
            """
        ],
        think=[
            f"""
            Readings `{temps}` with `k = {k}`. The windows' peaks are `{want}`.

            When the 5 arrives at hour 3, the readings 1 and −2 before it are still in view for a while, but they'll never
            be the peak again: the 5 is higher and will stay on screen longer than they will. So they can be forgotten.
            What's left is always a **decreasing** list of candidates: each one is the peak of the future windows until
            something higher arrives or it scrolls off.
            """,
            fig(Row(temps, st={j: "mark" for j in range(1, 4)} | {3: "found"}), caption="Once 5 is in view, 1 and −2 can never be a peak again."),
            """
            New candidates join at the back (after removing the weaker ones there), and expired ones leave from the front:
            a double-ended queue. The front is the oldest surviving candidate and the highest, so it's the peak.
            """,
        ],
        approaches=[
            approach(
                "Scan every window",
                "brute",
                "O(n·k)",
                "O(1)",
                idea=["For each window start `i`, scan `temps[i..i+k−1]` for the maximum."],
                walk=w1,
                build=["For `i` from 0 to `n − k`: compute the max of the window.", "Append it to the answer."],
                code={
                    "python": """
                        class Solution:
                            def windowPeaks(self, temps: List[int], k: int) -> List[int]:
                                out = []  #@init
                                for i in range(len(temps) - k + 1):  #@each
                                    peak = temps[i]  #@scan
                                    for j in range(i, i + k):  #@scan
                                        peak = max(peak, temps[j])  #@scan
                                    out.append(peak)  #@add
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] windowPeaks(int[] temps, int k) {
                                int[] out = new int[temps.length - k + 1];  //@init
                                for (int i = 0; i + k <= temps.length; i++) {  //@each
                                    int peak = temps[i];  //@scan
                                    for (int j = i; j < i + k; j++) peak = Math.max(peak, temps[j]);  //@scan
                                    out[i] = peak;  //@add
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> windowPeaks(vector<int>& temps, int k) {
                                vector<int> out;  //@init
                                for (size_t i = 0; i + k <= temps.size(); i++) {  //@each
                                    int peak = temps[i];  //@scan
                                    for (size_t j = i; j < i + k; j++) peak = max(peak, temps[j]);  //@scan
                                    out.push_back(peak);  //@add
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* windowPeaks(int* temps, int tempsSize, int k, int* returnSize) {
                            int m = tempsSize - k + 1;  //@init
                            int* out = malloc(m * sizeof(int));  //@init
                            for (int i = 0; i < m; i++) {  //@each
                                int peak = temps[i];  //@scan
                                for (int j = i; j < i + k; j++) if (temps[j] > peak) peak = temps[j];  //@scan
                                out[i] = peak;  //@add
                            }
                            *returnSize = m;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "One peak per window: `n − k + 1` of them."), ("each", "Every window start."), ("scan", "Highest of the `k` readings in view."), ("add", "Record this window's peak."), ("ret", "All peaks.")],
                complexity=["**Time O(n·k):** up to 10¹⁰ for large windows. **Space O(1)** beyond the answer."],
                limits=["Neighbouring windows share `k − 1` readings, and the scan redoes all of them. Either precompute block maxima, or keep only the readings that can still be a peak."],
                slow=True,
            ),
            approach(
                "Block running maxima",
                "better",
                "O(n)",
                "O(n)",
                idea=["Split the array into blocks of `k`. Compute `fromStart[i]` (max from `i`'s block start to `i`) and `toEnd[i]` (max from `i` to its block's end). A window `i..i+k−1` is the tail of one block plus the head of the next (or exactly one block), so its peak is `max(toEnd[i], fromStart[i+k−1])`."],
                walk=w2,
                build=["Forward pass: `fromStart[i]` restarts at each block boundary (`i % k == 0`).", "Backward pass: `toEnd[i]` restarts at each block's last index (or the array end).", "Each window's peak is the max of the two lookups."],
                code={
                    "python": """
                        class Solution:
                            def windowPeaks(self, temps: List[int], k: int) -> List[int]:
                                n = len(temps)  #@init
                                from_start, to_end = temps[:], temps[:]  #@init
                                for i in range(1, n):  #@fwd
                                    if i % k:  #@fwd
                                        from_start[i] = max(from_start[i - 1], temps[i])  #@fwd
                                for i in range(n - 2, -1, -1):  #@back
                                    if (i + 1) % k:  #@back
                                        to_end[i] = max(to_end[i + 1], temps[i])  #@back
                                return [max(to_end[i], from_start[i + k - 1]) for i in range(n - k + 1)]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] windowPeaks(int[] temps, int k) {
                                int n = temps.length;  //@init
                                int[] fromStart = temps.clone(), toEnd = temps.clone();  //@init
                                for (int i = 1; i < n; i++) if (i % k != 0) fromStart[i] = Math.max(fromStart[i - 1], temps[i]);  //@fwd
                                for (int i = n - 2; i >= 0; i--) if ((i + 1) % k != 0) toEnd[i] = Math.max(toEnd[i + 1], temps[i]);  //@back
                                int[] out = new int[n - k + 1];  //@ret
                                for (int i = 0; i + k <= n; i++) out[i] = Math.max(toEnd[i], fromStart[i + k - 1]);  //@ret
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> windowPeaks(vector<int>& temps, int k) {
                                int n = temps.size();  //@init
                                vector<int> fromStart = temps, toEnd = temps;  //@init
                                for (int i = 1; i < n; i++) if (i % k != 0) fromStart[i] = max(fromStart[i - 1], temps[i]);  //@fwd
                                for (int i = n - 2; i >= 0; i--) if ((i + 1) % k != 0) toEnd[i] = max(toEnd[i + 1], temps[i]);  //@back
                                vector<int> out;  //@ret
                                for (int i = 0; i + k <= n; i++) out.push_back(max(toEnd[i], fromStart[i + k - 1]));  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* windowPeaks(int* temps, int tempsSize, int k, int* returnSize) {
                            int n = tempsSize;  //@init
                            int* fromStart = malloc(n * sizeof(int));  //@init
                            int* toEnd = malloc(n * sizeof(int));  //@init
                            for (int i = 0; i < n; i++) fromStart[i] = i % k != 0 && fromStart[i - 1] > temps[i] ? fromStart[i - 1] : temps[i];  //@fwd
                            for (int i = n - 1; i >= 0; i--) toEnd[i] = i < n - 1 && (i + 1) % k != 0 && toEnd[i + 1] > temps[i] ? toEnd[i + 1] : temps[i];  //@back
                            int m = n - k + 1;  //@ret
                            int* out = malloc(m * sizeof(int));  //@ret
                            for (int i = 0; i < m; i++) out[i] = toEnd[i] > fromStart[i + k - 1] ? toEnd[i] : fromStart[i + k - 1];  //@ret
                            free(fromStart);  //@ret
                            free(toEnd);  //@ret
                            *returnSize = m;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "Two copies of the readings to turn into running maxima."), ("fwd", "Running max from the start of each block; it restarts when `i` is a multiple of `k`."), ("back", "Running max back from the end of each block; it restarts at each block's last index."), ("ret", "Window `i..i+k−1` = (tail of `i`'s block) + (head of the next block up to `i+k−1`). If `i` starts a block, both lookups cover the same whole block. Either way, the peak is the larger lookup.")],
                complexity=["**Time O(n):** two passes plus one lookup per window. **Space O(n)** for the two arrays."],
                limits=["Linear, but it needs the whole array up front and two extra arrays of size n. The deque handles readings as they stream in, using only O(k) memory."],
            ),
            approach(
                "Monotonic deque",
                "best",
                "O(n)",
                "O(k)",
                idea=["Keep a deque of indices whose readings strictly decrease front to back. For each hour `i`: pop from the back while the back's reading ≤ `temps[i]`; push `i`; if the front index is `≤ i − k`, it has scrolled off, so pop it from the front. Once `i ≥ k − 1`, the front is the peak."],
                walk=w3,
                build=["An empty deque of indices.", "For each hour: clear weaker readings from the back, push the hour.", "Drop the front if it's outside the window.", "From the first full window on, record the front's reading."],
                code={
                    "python": """
                        from collections import deque

                        class Solution:
                            def windowPeaks(self, temps: List[int], k: int) -> List[int]:
                                dq, out = deque(), []  #@init
                                for i, v in enumerate(temps):  #@loop
                                    while dq and temps[dq[-1]] <= v:  #@back
                                        dq.pop()  #@back
                                    dq.append(i)  #@back
                                    if dq[0] <= i - k:  #@front
                                        dq.popleft()  #@front
                                    if i >= k - 1:  #@peak
                                        out.append(temps[dq[0]])  #@peak
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] windowPeaks(int[] temps, int k) {
                                int n = temps.length;  //@init
                                int[] dq = new int[n], out = new int[n - k + 1];  //@init
                                int head = 0, tail = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@loop
                                    while (tail > head && temps[dq[tail - 1]] <= temps[i]) tail--;  //@back
                                    dq[tail++] = i;  //@back
                                    if (dq[head] <= i - k) head++;  //@front
                                    if (i >= k - 1) out[i - k + 1] = temps[dq[head]];  //@peak
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> windowPeaks(vector<int>& temps, int k) {
                                deque<int> dq;  //@init
                                vector<int> out;  //@init
                                for (int i = 0; i < (int) temps.size(); i++) {  //@loop
                                    while (!dq.empty() && temps[dq.back()] <= temps[i]) dq.pop_back();  //@back
                                    dq.push_back(i);  //@back
                                    if (dq.front() <= i - k) dq.pop_front();  //@front
                                    if (i >= k - 1) out.push_back(temps[dq.front()]);  //@peak
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* windowPeaks(int* temps, int tempsSize, int k, int* returnSize) {
                            int n = tempsSize;  //@init
                            int* dq = malloc(n * sizeof(int));  //@init
                            int* out = malloc((n - k + 1) * sizeof(int));  //@init
                            int head = 0, tail = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@loop
                                while (tail > head && temps[dq[tail - 1]] <= temps[i]) tail--;  //@back
                                dq[tail++] = i;  //@back
                                if (dq[head] <= i - k) head++;  //@front
                                if (i >= k - 1) out[i - k + 1] = temps[dq[head]];  //@peak
                            }
                            free(dq);  //@ret
                            *returnSize = n - k + 1;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "The deque of candidate hours and the answer.", {"java": "An array with `head` and `tail` works as a deque: each index enters once, so `n` slots are enough.", "c": "An array with `head` and `tail` works as a deque: each index enters once, so `n` slots are enough."}),
                    ("loop", "One pass over the hours."),
                    ("back", "A reading that's no higher than the new one, and older, can never be a peak again: remove it from the back. Then the new hour joins. The deque stays strictly decreasing."),
                    ("front", "The front is the oldest candidate; if it's now outside `i−k+1..i`, drop it. At most one index expires per step."),
                    ("peak", "From the first full window on, the front is the highest reading in view."),
                    ("ret", "All peaks."),
                ],
                complexity=["**Time O(n):** every index enters and leaves the deque at most once. **Space O(k)** in the deque (it only holds indices inside the window); the C and Java versions allocate `n` slots for simplicity."],
            ),
        ],
        takeaways=[
            """
            - **Sliding-window maximum = monotonic deque:** pop weaker items from the back, expired items from the front;
              the front is the answer.
            - An item can be discarded as soon as a **newer, at-least-as-good** item arrives.
            - Store indices, not values, so you can tell when the front has left the window.
            """
        ],
    )


@problem
def stepping_stones_score():
    stones, k = [2, -5, -3, 4, -6, -1, 3], 2
    n = len(stones)
    best = [0] * n
    best[0] = stones[0]
    for i in range(1, n):
        best[i] = stones[i] + max(best[max(0, i - k):i])
    want = best[-1]

    w1 = Steps(f"best[i] = the top score on arriving at stone i = stones[i] + the best of the {k} stones before it. Check all k every time.")
    w1.step(f"best[0] = stones[0] = {stones[0]}.", Row(stones, st={0: "active"}, label="stones"), Row([best[0]] + ["·"] * (n - 1), label="best"))
    for i in range(1, n):
        lo = max(0, i - k)
        src = max(range(lo, i), key=lambda j: best[j])
        w1.step(f"Stone {i}: look back at best[{lo}..{i - 1}] = {best[lo:i]}; the top is {best[src]} (stone {src}). best[{i}] = {stones[i]} + {best[src]} = {best[i]}.", Row(stones, st={i: "active"}, label="stones"), Row(best[:i + 1] + ["·"] * (n - i - 1), st={**{j: "mark" for j in range(lo, i)}, src: "found"}, label="best"))
    w1.step(f"best[{n - 1}] = {want}.", result=want)

    w2 = Steps("Same recurrence, but the 'best of the last k' is a sliding-window maximum: keep a deque of stones whose best values decrease front to back.")
    dq = deque([0])
    w2.step(f"best[0] = {stones[0]}; the deque holds stone 0.", Row(stones, st={0: "active"}, label="stones"), Row([best[0]] + ["·"] * (n - 1), label="best"), Row([f"{j}:{best[j]}" for j in dq], label="deque (stone:best)"))
    for i in range(1, n):
        msg = f"Stone {i}: "
        while dq[0] < i - k:
            msg += f"stone {dq.popleft()} is out of reach, drop it. "
        msg += f"The front (stone {dq[0]}, best {best[dq[0]]}) is the best take-off: best[{i}] = {stones[i]} + {best[dq[0]]} = {best[i]}."
        popped = []
        while dq and best[dq[-1]] <= best[i]:
            popped.append(dq.pop())
        dq.append(i)
        if popped:
            msg += f" Stones {popped} at the back are no better and older: drop them."
        w2.step(msg, Row(stones, st={i: "active"}, label="stones"), Row(best[:i + 1] + ["·"] * (n - i - 1), label="best"), Row([f"{j}:{best[j]}" for j in dq], label="deque (stone:best)"))
    w2.step(f"best[{n - 1}] = {want}.", result=want)

    path, i = [n - 1], n - 1
    while i > 0:
        i = max(range(max(0, i - k), i), key=lambda j: (best[j], j))
        path.append(i)
    path.reverse()

    sol(
        "stepping-stones-score",
        summary="""
            Let `best[i]` be the highest score on landing on stone `i`. You arrive from one of the `k` stones before it, so
            `best[i] = stones[i] + max(best[i−k..i−1])`. That max is a sliding-window maximum over the `best` values
            already computed, so a monotonic deque gives it in O(1) amortised: O(n) overall.
        """,
        question=[
            """
            You start on stone 0, must end on the last stone, and each step jumps forward 1 to `k` stones. Your score is
            the sum of the stones you land on, including the first and last. Return the maximum score.

            - **Negative stones can't always be avoided**: if a run of more than `k − 1` negatives lies in the way, you
              must land on some of them.
            - **One stone** means the score is just `stones[0]`.
            - **Up to 10⁵ stones and `k` up to 10⁵**, so `n × k` can reach 10¹⁰. The score fits in 64 bits.
            """
        ],
        think=[
            f"""
            Stones `{stones}` with `k = {k}`. The best route lands on stones `{path}` for a score of **{want}**. Every jump
            is at most {k}, so of the two negatives −5, −3 one must be stepped on (the smaller loss, −3), and of −6, −1
            the −1.

            Greedy choices fail: jumping to the best nearby stone can leave you facing a long negative run. Instead, think
            backwards: whatever route reaches stone `i`, its previous stone is one of the `k` before `i`, and the route up
            to that stone should itself be the best one. So `best[i] = stones[i] + max(best[i−k..i−1])`.
            """,
            table(["stone", "value", "best"], *[(i, stones[i], best[i]) for i in range(n)]),
            """
            Computing that max by scanning `k` values per stone is O(nk). But as `i` moves right, the range
            `i−k..i−1` slides by one: it's exactly the sliding-window maximum, over the `best` array as it's being built.
            """,
        ],
        approaches=[
            approach(
                "Dynamic programming, scanning back k stones",
                "brute",
                "O(n·k)",
                "O(n)",
                idea=["Fill `best` left to right. `best[0] = stones[0]`; for each later stone, scan the up-to-`k` previous `best` values for the maximum and add `stones[i]`."],
                walk=w1,
                build=["`best[0] = stones[0]`.", "For `i ≥ 1`, `best[i] = stones[i] + max(best[max(0, i−k) .. i−1])`.", "Return `best[n−1]`."],
                code={
                    "python": """
                        class Solution:
                            def bestScore(self, stones: List[int], k: int) -> int:
                                n = len(stones)  #@init
                                best = [0] * n  #@init
                                best[0] = stones[0]  #@init
                                for i in range(1, n):  #@each
                                    top = best[i - 1]  #@scan
                                    for j in range(max(0, i - k), i):  #@scan
                                        top = max(top, best[j])  #@scan
                                    best[i] = stones[i] + top  #@set
                                return best[-1]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long bestScore(int[] stones, int k) {
                                int n = stones.length;  //@init
                                long[] best = new long[n];  //@init
                                best[0] = stones[0];  //@init
                                for (int i = 1; i < n; i++) {  //@each
                                    long top = best[i - 1];  //@scan
                                    for (int j = Math.max(0, i - k); j < i; j++) top = Math.max(top, best[j]);  //@scan
                                    best[i] = stones[i] + top;  //@set
                                }
                                return best[n - 1];  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long bestScore(vector<int>& stones, int k) {
                                int n = stones.size();  //@init
                                vector<long long> best(n);  //@init
                                best[0] = stones[0];  //@init
                                for (int i = 1; i < n; i++) {  //@each
                                    long long top = best[i - 1];  //@scan
                                    for (int j = max(0, i - k); j < i; j++) top = max(top, best[j]);  //@scan
                                    best[i] = stones[i] + top;  //@set
                                }
                                return best[n - 1];  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long bestScore(int* stones, int stonesSize, int k) {
                            int n = stonesSize;  //@init
                            long long* best = malloc(n * sizeof(long long));  //@init
                            best[0] = stones[0];  //@init
                            for (int i = 1; i < n; i++) {  //@each
                                long long top = best[i - 1];  //@scan
                                for (int j = i - k > 0 ? i - k : 0; j < i; j++) if (best[j] > top) top = best[j];  //@scan
                                best[i] = stones[i] + top;  //@set
                            }
                            long long answer = best[n - 1];  //@ret
                            free(best);  //@ret
                            return answer;  //@ret
                        }
                    """,
                },
                lines=[("init", "`best[0]`: you start on stone 0, so its value is always counted.", {"java": "`long` values, matching the return type.", "cpp": "64-bit values, matching the return type.", "c": "64-bit values, matching the return type."}), ("each", "Stones in order: every take-off stone is computed before it's needed."), ("scan", "The best landing score among the stones you could have jumped from."), ("set", "Land on stone `i` from that best take-off point."), ("ret", "The score on the last stone.")],
                complexity=["**Time O(n·k):** up to 10¹⁰ when `k` is large. **Space O(n).**"],
                limits=["Consecutive stones look at windows that overlap in `k − 1` places, so most of each scan is repeated. The window maximum can be maintained incrementally with a deque."],
                slow=True,
            ),
            approach(
                "Dynamic programming with a monotonic deque",
                "best",
                "O(n)",
                "O(n)",
                idea=["Keep a deque of stone indices whose `best` values decrease from front to back. For stone `i`: drop the front if it's more than `k` stones back; `best[i] = stones[i] + best[front]`; then pop from the back every stone with `best ≤ best[i]` (older and no better) and push `i`."],
                walk=w2,
                build=["`best[0] = stones[0]`, deque = [0].", "For each `i ≥ 1`: expire the front (index `< i − k`).", "`best[i] = stones[i] + best[front]`.", "Pop weaker stones from the back; push `i`.", "Return `best[n−1]`."],
                code={
                    "python": """
                        from collections import deque

                        class Solution:
                            def bestScore(self, stones: List[int], k: int) -> int:
                                n = len(stones)  #@init
                                best = [0] * n  #@init
                                best[0] = stones[0]  #@init
                                dq = deque([0])  #@init
                                for i in range(1, n):  #@each
                                    if dq[0] < i - k:  #@expire
                                        dq.popleft()  #@expire
                                    best[i] = stones[i] + best[dq[0]]  #@set
                                    while dq and best[dq[-1]] <= best[i]:  #@back
                                        dq.pop()  #@back
                                    dq.append(i)  #@back
                                return best[-1]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long bestScore(int[] stones, int k) {
                                int n = stones.length;  //@init
                                long[] best = new long[n];  //@init
                                int[] dq = new int[n];  //@init
                                int head = 0, tail = 0;  //@init
                                best[0] = stones[0];  //@init
                                dq[tail++] = 0;  //@init
                                for (int i = 1; i < n; i++) {  //@each
                                    if (dq[head] < i - k) head++;  //@expire
                                    best[i] = stones[i] + best[dq[head]];  //@set
                                    while (tail > head && best[dq[tail - 1]] <= best[i]) tail--;  //@back
                                    dq[tail++] = i;  //@back
                                }
                                return best[n - 1];  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long bestScore(vector<int>& stones, int k) {
                                int n = stones.size();  //@init
                                vector<long long> best(n);  //@init
                                deque<int> dq;  //@init
                                best[0] = stones[0];  //@init
                                dq.push_back(0);  //@init
                                for (int i = 1; i < n; i++) {  //@each
                                    if (dq.front() < i - k) dq.pop_front();  //@expire
                                    best[i] = stones[i] + best[dq.front()];  //@set
                                    while (!dq.empty() && best[dq.back()] <= best[i]) dq.pop_back();  //@back
                                    dq.push_back(i);  //@back
                                }
                                return best[n - 1];  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long bestScore(int* stones, int stonesSize, int k) {
                            int n = stonesSize;  //@init
                            long long* best = malloc(n * sizeof(long long));  //@init
                            int* dq = malloc(n * sizeof(int));  //@init
                            int head = 0, tail = 0;  //@init
                            best[0] = stones[0];  //@init
                            dq[tail++] = 0;  //@init
                            for (int i = 1; i < n; i++) {  //@each
                                if (dq[head] < i - k) head++;  //@expire
                                best[i] = stones[i] + best[dq[head]];  //@set
                                while (tail > head && best[dq[tail - 1]] <= best[i]) tail--;  //@back
                                dq[tail++] = i;  //@back
                            }
                            long long answer = best[n - 1];  //@ret
                            free(best);  //@ret
                            free(dq);  //@ret
                            return answer;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "`best[0]` and a deque holding stone 0, the only take-off point so far.", {"java": "The deque is an array with `head`/`tail`; each index enters once.", "c": "The deque is an array with `head`/`tail`; each index enters once."}),
                    ("each", "Stones in order."),
                    ("expire", "A stone more than `k` back can't be jumped from any more. Only one stone falls out of range per step, so one check suffices."),
                    ("set", "The front has the highest `best` among stones in range: take off from it."),
                    ("back", "Stones at the back with `best ≤ best[i]` are older (they'll go out of range sooner) and no better, so they'll never be the front again. Remove them, then add `i`. The deque is never empty when the front is read, since `i − 1` is always in range."),
                    ("ret", "The highest score landing on the last stone."),
                ],
                complexity=["**Time O(n):** each stone enters and leaves the deque at most once. **Space O(n)** for `best` (the deque holds at most `k + 1` indices)."],
            ),
        ],
        takeaways=[
            """
            - **DP whose transition is 'max over the last k states'** = DP + sliding-window maximum with a monotonic deque.
            - The deque is filled with DP values as they're computed, so it works even though the window's contents are
              not known in advance.
            - Test greedy ideas against a run of negatives longer than `k`: they usually fail there.
            """
        ],
    )


@problem
def shortest_net_gain():
    changes, target = [4, -6, 3, 2, -1, 4, 1], 6
    n = len(changes)
    P = [0]
    for v in changes:
        P.append(P[-1] + v)
    want = min((j - i for i in range(n + 1) for j in range(i + 1, n + 1) if P[j] - P[i] >= target), default=-1)

    w1 = Steps("Try every start day; extend day by day with a running sum, stopping at the first end that reaches the target.")
    best = -1
    for i in range(n):
        s, hit = 0, None
        for j in range(i, n):
            s += changes[j]
            if s >= target:
                hit = j
                break
        if hit is not None and (best < 0 or hit - i + 1 < best):
            best = hit - i + 1
        w1.step(f"Start day {i}: " + (f"the sum first reaches {target} at day {hit} (sum {s}), length {hit - i + 1}." if hit is not None else f"never reaches {target}."), Row(changes, st={**({x: "mark" for x in range(i, hit + 1)} if hit is not None else {}), i: "active"}), Vars(shortest=best))
    w1.step(f"Shortest: {best}.", result=best)

    w2 = Steps("With prefix sums P, a run i..j−1 sums to P[j] − P[i]. For each end j we want the latest start i with P[i] ≤ P[j] − target. Keep candidate starts on a stack with increasing P and binary-search it.")
    st, best = [], -1
    for j in range(n + 1):
        need = P[j] - target
        lo, hi = 0, len(st) - 1
        pos = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if P[st[mid]] <= need:
                pos, lo = mid, mid + 1
            else:
                hi = mid - 1
        found = ""
        if pos >= 0:
            i = st[pos]
            if best < 0 or j - i < best:
                best = j - i
            found = f" Latest start with P ≤ {need}: index {i}, length {j - i}."
        else:
            found = f" No start has P ≤ {need}."
        popped = []
        while st and P[st[-1]] >= P[j]:
            popped.append(st.pop())
        st.append(j)
        w2.step(f"End j = {j} (P = {P[j]}).{found}" + (f" Then {popped} leave the stack (P no smaller and earlier than j)." if popped else "") + f" Push {j}.", Row(P, st={j: "active"}, label="prefix P"), Row([f"{x}:{P[x]}" for x in st], label="stack (index:P)"), Vars(shortest=best))
    w2.step(f"Shortest: {best}.", result=best)

    w3 = Steps("Same candidates, kept in a deque with increasing P. When the front already works for end j, record it and drop it: a later end could only give a longer run from that start.")
    dq, best = deque(), n + 1
    for j in range(n + 1):
        used = []
        while dq and P[j] - P[dq[0]] >= target:
            i = dq.popleft()
            used.append(i)
            best = min(best, j - i)
        popped = []
        while dq and P[dq[-1]] >= P[j]:
            popped.append(dq.pop())
        dq.append(j)
        msg = f"End j = {j} (P = {P[j]})."
        if used:
            msg += f" Front start(s) {used} reach the target: lengths {[j - i for i in used]}; drop them."
        if popped:
            msg += f" Back {popped} have P ≥ {P[j]}: drop them."
        w3.step(msg + f" Push {j}.", Row(P, st={j: "active"}, label="prefix P"), Row([f"{x}:{P[x]}" for x in dq], label="deque (index:P)"), Vars(shortest=best if best <= n else "none"))
    w3.step(f"Shortest: {best if best <= n else -1}.", result=best if best <= n else -1)

    sol(
        "shortest-net-gain",
        summary="""
            With prefix sums `P`, the run `i..j−1` gains `P[j] − P[i]`. For each end `j`, keep candidate starts in a deque
            with increasing `P`: a start with a larger `P` than a later one is never useful. While the front start reaches
            the target, record the length and drop it (a later end would only be longer). O(n).
        """,
        question=[
            """
            Find the shortest run of consecutive days whose changes sum to at least `target`, or −1 if none exists.

            - **Changes can be negative**, so a longer run isn't always better and the usual two-pointer window doesn't
              work: shrinking the window can increase its sum.
            - **`target ≥ 1`**, so an empty run never counts.
            - **Up to 10⁵ days; sums reach 10¹⁰**, beyond 32-bit integers.
            """
        ],
        think=[
            f"""
            Changes `{changes}`, target {target}. Prefix sums `P = {P}`. A run from day `i` to day `j − 1` gains
            `P[j] − P[i]`. The shortest qualifying run has length **{want}**.

            Why not a sliding window? With only positive changes, growing the window raises the sum and shrinking lowers it,
            so two pointers work. Here the −6 breaks that: dropping it from the left *raises* the sum.
            """,
            fig(Row(changes, label="changes"), Row(P, label="prefix P")),
            """
            For an end `j`, we want the **latest** start `i < j` with `P[i] ≤ P[j] − target`. Two observations prune the
            candidate starts:

            1. If `i₁ < i₂` and `P[i₁] ≥ P[i₂]`, then `i₂` is better for every future end: it's later (shorter run) and has
               a smaller `P` (bigger gain). So `i₁` can go. The survivors have strictly increasing `P`.
            2. If start `i` works for end `j`, no later end can do better with `i`: the run would only get longer. So once
               used, `i` can go too, from the front.
            """,
        ],
        approaches=[
            approach(
                "Every start, extended until it works",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start day, add days one at a time; the first time the sum reaches the target, that's the shortest run from this start. Keep the minimum over all starts."],
                walk=w1,
                build=["For each start `i`, `s = 0`.", "For `j` from `i`: add `changes[j]`; if `s ≥ target`, record `j − i + 1` and stop.", "Return the minimum, or −1."],
                code={
                    "python": """
                        class Solution:
                            def shortestNetGain(self, changes: List[int], target: int) -> int:
                                n = len(changes)  #@init
                                best = -1  #@init
                                for i in range(n):  #@start
                                    s = 0  #@start
                                    for j in range(i, n):  #@extend
                                        s += changes[j]  #@extend
                                        if s >= target:  #@hit
                                            if best < 0 or j - i + 1 < best:  #@hit
                                                best = j - i + 1  #@hit
                                            break  #@hit
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestNetGain(int[] changes, int target) {
                                int n = changes.length, best = -1;  //@init
                                for (int i = 0; i < n; i++) {  //@start
                                    long s = 0;  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        s += changes[j];  //@extend
                                        if (s >= target) {  //@hit
                                            if (best < 0 || j - i + 1 < best) best = j - i + 1;  //@hit
                                            break;  //@hit
                                        }
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestNetGain(vector<int>& changes, int target) {
                                int n = changes.size(), best = -1;  //@init
                                for (int i = 0; i < n; i++) {  //@start
                                    long long s = 0;  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        s += changes[j];  //@extend
                                        if (s >= target) {  //@hit
                                            if (best < 0 || j - i + 1 < best) best = j - i + 1;  //@hit
                                            break;  //@hit
                                        }
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int shortestNetGain(int* changes, int changesSize, int target) {
                            int n = changesSize, best = -1;  //@init
                            for (int i = 0; i < n; i++) {  //@start
                                long long s = 0;  //@start
                                for (int j = i; j < n; j++) {  //@extend
                                    s += changes[j];  //@extend
                                    if (s >= target) {  //@hit
                                        if (best < 0 || j - i + 1 < best) best = j - i + 1;  //@hit
                                        break;  //@hit
                                    }
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "No run found yet (−1)."), ("start", "Runs starting on day `i`; the sum is 64-bit in the typed languages."), ("extend", "Add the next day."), ("hit", "The first end that reaches the target is the shortest from this start; longer ones can't beat it."), ("ret", "The shortest run, or −1.")],
                complexity=["**Time O(n²)** in the worst case. **Space O(1).**"],
                limits=["Each start rescans forward from scratch. With prefix sums, the question becomes 'which earlier prefix is small enough', and most earlier prefixes can be ruled out for good."],
                slow=True,
            ),
            approach(
                "Prefix sums, increasing stack, binary search",
                "better",
                "O(n log n)",
                "O(n)",
                idea=["Compute prefix sums. Walk the ends `j = 0..n`, keeping a stack of candidate starts with strictly increasing `P` (pop starts with `P ≥ P[j]` before pushing `j`). Before pushing, binary-search the stack for the last start with `P ≤ P[j] − target`; it's the latest valid start, so `j − i` is the best run ending at `j`."],
                walk=w2,
                build=["`P[0] = 0`, `P[j+1] = P[j] + changes[j]` (64-bit).", "For each `j`: binary-search the stack for the rightmost `P[i] ≤ P[j] − target`; update the answer.", "Pop starts with `P ≥ P[j]`, push `j`.", "Return the best, or −1."],
                code={
                    "python": """
                        class Solution:
                            def shortestNetGain(self, changes: List[int], target: int) -> int:
                                n = len(changes)  #@prefix
                                P = [0] * (n + 1)  #@prefix
                                for i, v in enumerate(changes):  #@prefix
                                    P[i + 1] = P[i] + v  #@prefix
                                best, stack = n + 1, []  #@init
                                for j in range(n + 1):  #@loop
                                    lo, hi = 0, len(stack) - 1  #@search
                                    while lo <= hi:  #@search
                                        mid = (lo + hi) // 2  #@search
                                        if P[stack[mid]] <= P[j] - target:  #@search
                                            best = min(best, j - stack[mid])  #@search
                                            lo = mid + 1  #@search
                                        else:  #@search
                                            hi = mid - 1  #@search
                                    while stack and P[stack[-1]] >= P[j]:  #@push
                                        stack.pop()  #@push
                                    stack.append(j)  #@push
                                return best if best <= n else -1  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestNetGain(int[] changes, int target) {
                                int n = changes.length;  //@prefix
                                long[] P = new long[n + 1];  //@prefix
                                for (int i = 0; i < n; i++) P[i + 1] = P[i] + changes[i];  //@prefix
                                int[] stack = new int[n + 1];  //@init
                                int top = 0, best = n + 1;  //@init
                                for (int j = 0; j <= n; j++) {  //@loop
                                    int lo = 0, hi = top - 1;  //@search
                                    while (lo <= hi) {  //@search
                                        int mid = (lo + hi) >>> 1;  //@search
                                        if (P[stack[mid]] <= P[j] - target) { best = Math.min(best, j - stack[mid]); lo = mid + 1; }  //@search
                                        else hi = mid - 1;  //@search
                                    }
                                    while (top > 0 && P[stack[top - 1]] >= P[j]) top--;  //@push
                                    stack[top++] = j;  //@push
                                }
                                return best <= n ? best : -1;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestNetGain(vector<int>& changes, int target) {
                                int n = changes.size();  //@prefix
                                vector<long long> P(n + 1, 0);  //@prefix
                                for (int i = 0; i < n; i++) P[i + 1] = P[i] + changes[i];  //@prefix
                                vector<int> stack;  //@init
                                int best = n + 1;  //@init
                                for (int j = 0; j <= n; j++) {  //@loop
                                    int lo = 0, hi = (int) stack.size() - 1;  //@search
                                    while (lo <= hi) {  //@search
                                        int mid = (lo + hi) / 2;  //@search
                                        if (P[stack[mid]] <= P[j] - target) { best = min(best, j - stack[mid]); lo = mid + 1; }  //@search
                                        else hi = mid - 1;  //@search
                                    }
                                    while (!stack.empty() && P[stack.back()] >= P[j]) stack.pop_back();  //@push
                                    stack.push_back(j);  //@push
                                }
                                return best <= n ? best : -1;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int shortestNetGain(int* changes, int changesSize, int target) {
                            int n = changesSize;  //@prefix
                            long long* P = malloc((n + 1) * sizeof(long long));  //@prefix
                            P[0] = 0;  //@prefix
                            for (int i = 0; i < n; i++) P[i + 1] = P[i] + changes[i];  //@prefix
                            int* stack = malloc((n + 1) * sizeof(int));  //@init
                            int top = 0, best = n + 1;  //@init
                            for (int j = 0; j <= n; j++) {  //@loop
                                int lo = 0, hi = top - 1;  //@search
                                while (lo <= hi) {  //@search
                                    int mid = (lo + hi) / 2;  //@search
                                    if (P[stack[mid]] <= P[j] - target) { if (j - stack[mid] < best) best = j - stack[mid]; lo = mid + 1; }  //@search
                                    else hi = mid - 1;  //@search
                                }
                                while (top > 0 && P[stack[top - 1]] >= P[j]) top--;  //@push
                                stack[top++] = j;  //@push
                            }
                            free(P);  //@ret
                            free(stack);  //@ret
                            return best <= n ? best : -1;  //@ret
                        }
                    """,
                },
                lines=[("prefix", "`P[j]` = total change of the first `j` days; run `i..j−1` gains `P[j] − P[i]`.", {"java": "64-bit: sums reach 10¹⁰.", "cpp": "64-bit: sums reach 10¹⁰.", "c": "64-bit: sums reach 10¹⁰."}), ("init", "Candidate starts and the best length (`n + 1` = none yet)."), ("loop", "Each prefix index is an end, and afterwards a candidate start."), ("search", "`P` increases along the stack, so the valid starts (`P ≤ P[j] − target`) form a prefix of it. Binary-search for its last element: the latest valid start, giving the shortest run ending at `j`."), ("push", "Earlier starts with `P ≥ P[j]` are dominated by `j` (later and no larger), so remove them; then `j` becomes a candidate."), ("ret", "The best length, or −1.")],
                complexity=["**Time O(n log n):** a binary search per end; pushes and pops are O(n) in total. **Space O(n).**"],
                limits=["The binary search is unnecessary: once a start works for some end, it never needs to be considered again (later ends make longer runs). Removing used starts from the front makes every check O(1) amortised."],
            ),
            approach(
                "Prefix sums with a monotonic deque",
                "best",
                "O(n)",
                "O(n)",
                idea=["Keep candidate starts in a deque with strictly increasing `P`. For each end `j`: while the front start satisfies `P[j] − P[front] ≥ target`, record `j − front` and pop it from the front. Then pop from the back every start with `P ≥ P[j]` and push `j`."],
                walk=w3,
                build=["Prefix sums in 64 bits.", "For each `j`: pop qualifying starts from the front, recording lengths.", "Pop dominated starts from the back; push `j`.", "Return the best, or −1."],
                code={
                    "python": """
                        from collections import deque

                        class Solution:
                            def shortestNetGain(self, changes: List[int], target: int) -> int:
                                n = len(changes)  #@prefix
                                P = [0] * (n + 1)  #@prefix
                                for i, v in enumerate(changes):  #@prefix
                                    P[i + 1] = P[i] + v  #@prefix
                                best, dq = n + 1, deque()  #@init
                                for j in range(n + 1):  #@loop
                                    while dq and P[j] - P[dq[0]] >= target:  #@front
                                        best = min(best, j - dq.popleft())  #@front
                                    while dq and P[dq[-1]] >= P[j]:  #@back
                                        dq.pop()  #@back
                                    dq.append(j)  #@back
                                return best if best <= n else -1  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestNetGain(int[] changes, int target) {
                                int n = changes.length;  //@prefix
                                long[] P = new long[n + 1];  //@prefix
                                for (int i = 0; i < n; i++) P[i + 1] = P[i] + changes[i];  //@prefix
                                int[] dq = new int[n + 1];  //@init
                                int head = 0, tail = 0, best = n + 1;  //@init
                                for (int j = 0; j <= n; j++) {  //@loop
                                    while (tail > head && P[j] - P[dq[head]] >= target) best = Math.min(best, j - dq[head++]);  //@front
                                    while (tail > head && P[dq[tail - 1]] >= P[j]) tail--;  //@back
                                    dq[tail++] = j;  //@back
                                }
                                return best <= n ? best : -1;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestNetGain(vector<int>& changes, int target) {
                                int n = changes.size();  //@prefix
                                vector<long long> P(n + 1, 0);  //@prefix
                                for (int i = 0; i < n; i++) P[i + 1] = P[i] + changes[i];  //@prefix
                                deque<int> dq;  //@init
                                int best = n + 1;  //@init
                                for (int j = 0; j <= n; j++) {  //@loop
                                    while (!dq.empty() && P[j] - P[dq.front()] >= target) {  //@front
                                        best = min(best, j - dq.front());  //@front
                                        dq.pop_front();  //@front
                                    }
                                    while (!dq.empty() && P[dq.back()] >= P[j]) dq.pop_back();  //@back
                                    dq.push_back(j);  //@back
                                }
                                return best <= n ? best : -1;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int shortestNetGain(int* changes, int changesSize, int target) {
                            int n = changesSize;  //@prefix
                            long long* P = malloc((n + 1) * sizeof(long long));  //@prefix
                            P[0] = 0;  //@prefix
                            for (int i = 0; i < n; i++) P[i + 1] = P[i] + changes[i];  //@prefix
                            int* dq = malloc((n + 1) * sizeof(int));  //@init
                            int head = 0, tail = 0, best = n + 1;  //@init
                            for (int j = 0; j <= n; j++) {  //@loop
                                while (tail > head && P[j] - P[dq[head]] >= target) {  //@front
                                    if (j - dq[head] < best) best = j - dq[head];  //@front
                                    head++;  //@front
                                }
                                while (tail > head && P[dq[tail - 1]] >= P[j]) tail--;  //@back
                                dq[tail++] = j;  //@back
                            }
                            free(P);  //@ret
                            free(dq);  //@ret
                            return best <= n ? best : -1;  //@ret
                        }
                    """,
                },
                lines=[
                    ("prefix", "Prefix sums: run `i..j−1` gains `P[j] − P[i]`."),
                    ("init", "Candidate starts in increasing `P` order, and the best length.", {"java": "Array deque with `head`/`tail`.", "c": "Array deque with `head`/`tail`."}),
                    ("loop", "Each prefix index as an end."),
                    ("front", "The front has the smallest `P`, so if any start works for `j`, the front does. Record the length and drop it: any later end would make a longer run from it. Keep going, since the next start is later and may still work."),
                    ("back", "Starts with `P ≥ P[j]` are dominated by `j`: it's later and gains at least as much for any future end. Remove them, then add `j`."),
                    ("ret", "The best length, or −1 if no run reached the target."),
                ],
                complexity=["**Time O(n):** each index enters and leaves the deque at most once. **Space O(n)** for prefix sums and the deque."],
            ),
        ],
        takeaways=[
            """
            - **Negative numbers break the two-pointer window**; switch to prefix sums and ask about pairs `P[j] − P[i]`.
            - Prune candidates that are **dominated** (earlier and no better) from the back, and candidates that are
              **used up** (can only get worse) from the front: a monotonic deque.
            - A binary search over a monotonic stack is a good intermediate step when the front-popping argument isn't
              obvious.
            """
        ],
    )


@problem
def best_pair_of_posts():
    posts, k = [[0, 3], [2, 1], [3, 5], [7, 2], [8, 6], [12, 0]], 4
    n = len(posts)
    pairs = [(posts[i][1] + posts[j][1] + posts[j][0] - posts[i][0], i, j) for j in range(n) for i in range(j) if posts[j][0] - posts[i][0] <= k]
    want, bi, bj = max(pairs)
    score = [y - x for x, y in posts]

    w1 = Steps(f"Try every pair i < j that is at most k = {k} apart and compute y_i + y_j + (x_j − x_i).")
    best = None
    for j in range(n):
        vals = [(posts[i][1] + posts[j][1] + posts[j][0] - posts[i][0], i) for i in range(j) if posts[j][0] - posts[i][0] <= k]
        if vals:
            v, i = max(vals)
            best = v if best is None else max(best, v)
            w1.step(f"Right post {j} (x={posts[j][0]}, y={posts[j][1]}): partners in range {[i for _, i in vals]}, values {[v for v, _ in vals]}.", Row([f"{x},{y}" for x, y in posts], st={**{i: "mark" for _, i in vals}, j: "active"}, label="posts (x,y)"), Vars(best=best))
        else:
            w1.step(f"Right post {j}: no earlier post within {k}.", Row([f"{x},{y}" for x, y in posts], st={j: "active"}, label="posts (x,y)"), Vars(best=best if best is not None else "none"))
    w1.step(f"Best banner: {best}.", result=best)

    w2 = Steps("Rewrite the value as (y_i − x_i) + (y_j + x_j). For each right post j, we need the largest y_i − x_i among posts within k to its left: a sliding-window maximum, kept in a deque.")
    dq, best = deque(), None
    for j, (x, y) in enumerate(posts):
        msg = f"Post {j} (x={x}): "
        gone = []
        while dq and x - posts[dq[0]][0] > k:
            gone.append(dq.popleft())
        if gone:
            msg += f"posts {gone} are more than {k} away: drop them from the front. "
        if dq:
            i = dq[0]
            v = y + x + score[i]
            best = v if best is None else max(best, v)
            msg += f"Best partner is the front, post {i} (y−x = {score[i]}): value {y + x} + {score[i]} = {v}. "
        else:
            msg += "No partner in range. "
        popped = []
        while dq and score[dq[-1]] <= y - x:
            popped.append(dq.pop())
        dq.append(j)
        if popped:
            msg += f"Its y−x = {y - x} beats posts {popped} at the back: drop them. "
        msg += "Push it."
        w2.step(msg, Row([f"{x},{y}" for x, y in posts], st={j: "active"}, label="posts (x,y)"), Row(score, label="y − x"), Row([f"{q}:{score[q]}" for q in dq], label="deque (post:y−x)"), Vars(best=best if best is not None else "none"))
    w2.step(f"Best banner: {best}.", result=best)

    sol(
        "best-pair-of-posts",
        summary="""
            Split the value into a part for each post: `(y_i − x_i) + (y_j + x_j)`. For each right post `j`, the best
            partner is the post within distance `k` to its left with the largest `y_i − x_i`. As `j` moves right, that range
            slides, so a monotonic deque of `y − x` values gives the best partner in O(1) amortised. O(n).
        """,
        question=[
            """
            Posts are sorted by position `x`. A pair `i < j` with `x_j − x_i ≤ k` can hold a banner worth
            `y_i + y_j + (x_j − x_i)`. Return the best value. At least one valid pair exists.

            - **Heights can be negative**, so the best value can be negative too.
            - **Distance helps:** a farther partner adds more `x_j − x_i`, but it must stay within `k`.
            - **Up to 10⁵ posts.** Values reach about 6 × 10⁸ in size; use 64-bit to be safe (the return type is `long`).
            """
        ],
        think=[
            f"""
            Posts `{posts}`, `k = {k}`. The best banner joins posts {bi} and {bj}: {posts[bi][1]} + {posts[bj][1]} +
            ({posts[bj][0]} − {posts[bi][0]}) = **{want}**.

            The value mixes both posts, but it separates: `y_i + y_j + x_j − x_i = (y_i − x_i) + (y_j + x_j)`. With `j`
            fixed, `y_j + x_j` is a constant, so we just need the largest `y_i − x_i` among the posts in range.
            """,
            table(["post", "x", "y", "y − x", "y + x"], *[(i, posts[i][0], posts[i][1], posts[i][1] - posts[i][0], posts[i][1] + posts[i][0]) for i in range(n)]),
            """
            The range for `j` is the posts with `x_j − k ≤ x_i` and `i < j`. As `j` moves right, posts leave from the left
            and `j` itself joins on the right: a sliding window (sized by distance, not count). The maximum of a sliding
            window is a monotonic deque.
            """,
        ],
        approaches=[
            approach(
                "Every close-enough pair",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For every pair `i < j` with `x_j − x_i ≤ k`, compute the value and keep the best."],
                walk=w1,
                build=["Double loop over `j` and `i < j`.", "Skip pairs farther than `k`.", "Track the maximum (start below any possible value)."],
                code={
                    "python": """
                        class Solution:
                            def bestPair(self, posts: List[List[int]], k: int) -> int:
                                best = None  #@init
                                for j in range(len(posts)):  #@pairs
                                    for i in range(j):  #@pairs
                                        if posts[j][0] - posts[i][0] <= k:  #@range
                                            value = posts[i][1] + posts[j][1] + posts[j][0] - posts[i][0]  #@value
                                            if best is None or value > best:  #@value
                                                best = value  #@value
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long bestPair(int[][] posts, int k) {
                                long best = Long.MIN_VALUE;  //@init
                                for (int j = 0; j < posts.length; j++) {  //@pairs
                                    for (int i = 0; i < j; i++) {  //@pairs
                                        if (posts[j][0] - posts[i][0] <= k) {  //@range
                                            long value = (long) posts[i][1] + posts[j][1] + posts[j][0] - posts[i][0];  //@value
                                            best = Math.max(best, value);  //@value
                                        }
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long bestPair(vector<vector<int>>& posts, int k) {
                                long long best = LLONG_MIN;  //@init
                                for (size_t j = 0; j < posts.size(); j++) {  //@pairs
                                    for (size_t i = 0; i < j; i++) {  //@pairs
                                        if (posts[j][0] - posts[i][0] <= k) {  //@range
                                            long long value = (long long) posts[i][1] + posts[j][1] + posts[j][0] - posts[i][0];  //@value
                                            best = max(best, value);  //@value
                                        }
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long bestPair(int** posts, int postsSize, int* postsColSize, int k) {
                            long long best = LLONG_MIN;  //@init
                            for (int j = 0; j < postsSize; j++) {  //@pairs
                                for (int i = 0; i < j; i++) {  //@pairs
                                    if (posts[j][0] - posts[i][0] <= k) {  //@range
                                        long long value = (long long) posts[i][1] + posts[j][1] + posts[j][0] - posts[i][0];  //@value
                                        if (value > best) best = value;  //@value
                                    }
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "No pair yet: start below every possible value (values can be negative)."), ("pairs", "Every pair with `i` left of `j`."), ("range", "Only posts at most `k` apart can hold a banner. (Differences stay within 32 bits: at most 2 × 10⁸.)"), ("value", "The banner's value, in 64 bits."), ("ret", "The best value; the input guarantees a valid pair.")],
                complexity=["**Time O(n²):** about 5 × 10⁹ pairs for 10⁵ posts. **Space O(1).**"],
                limits=["The distance check rejects most pairs when `k` is small, and when `k` is large most pairs are valid but only the best partner matters. Separating the value into per-post parts makes 'best partner' a sliding-window maximum."],
                slow=True,
            ),
            approach(
                "Split the value, then a monotonic deque",
                "best",
                "O(n)",
                "O(n)",
                idea=["Process posts left to right with a deque of earlier posts whose `y − x` strictly decreases from front to back. For post `j`: drop front posts farther than `k`; if the deque isn't empty, `(y_j + x_j) + (y − x of the front)` is the best banner ending at `j`; then pop back posts with `y − x ≤ y_j − x_j` and push `j`."],
                walk=w2,
                build=["An empty deque, best = −∞.", "For each `j`: expire front posts with `x_j − x_front > k`.", "Use the front as the partner, if any.", "Pop dominated posts from the back; push `j`.", "Return the best."],
                code={
                    "python": """
                        from collections import deque

                        class Solution:
                            def bestPair(self, posts: List[List[int]], k: int) -> int:
                                dq, best = deque(), None  #@init
                                for j, (x, y) in enumerate(posts):  #@loop
                                    while dq and x - posts[dq[0]][0] > k:  #@expire
                                        dq.popleft()  #@expire
                                    if dq:  #@use
                                        xi, yi = posts[dq[0]]  #@use
                                        value = (y + x) + (yi - xi)  #@use
                                        if best is None or value > best:  #@use
                                            best = value  #@use
                                    while dq and posts[dq[-1]][1] - posts[dq[-1]][0] <= y - x:  #@back
                                        dq.pop()  #@back
                                    dq.append(j)  #@back
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long bestPair(int[][] posts, int k) {
                                int n = posts.length;  //@init
                                int[] dq = new int[n];  //@init
                                int head = 0, tail = 0;  //@init
                                long best = Long.MIN_VALUE;  //@init
                                for (int j = 0; j < n; j++) {  //@loop
                                    int x = posts[j][0], y = posts[j][1];  //@loop
                                    while (tail > head && x - posts[dq[head]][0] > k) head++;  //@expire
                                    if (tail > head) {  //@use
                                        int i = dq[head];  //@use
                                        best = Math.max(best, (long) y + x + posts[i][1] - posts[i][0]);  //@use
                                    }
                                    while (tail > head && posts[dq[tail - 1]][1] - posts[dq[tail - 1]][0] <= y - x) tail--;  //@back
                                    dq[tail++] = j;  //@back
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long bestPair(vector<vector<int>>& posts, int k) {
                                deque<int> dq;  //@init
                                long long best = LLONG_MIN;  //@init
                                for (int j = 0; j < (int) posts.size(); j++) {  //@loop
                                    int x = posts[j][0], y = posts[j][1];  //@loop
                                    while (!dq.empty() && x - posts[dq.front()][0] > k) dq.pop_front();  //@expire
                                    if (!dq.empty()) {  //@use
                                        int i = dq.front();  //@use
                                        best = max(best, (long long) y + x + posts[i][1] - posts[i][0]);  //@use
                                    }
                                    while (!dq.empty() && posts[dq.back()][1] - posts[dq.back()][0] <= y - x) dq.pop_back();  //@back
                                    dq.push_back(j);  //@back
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long bestPair(int** posts, int postsSize, int* postsColSize, int k) {
                            int* dq = malloc(postsSize * sizeof(int));  //@init
                            int head = 0, tail = 0;  //@init
                            long long best = LLONG_MIN;  //@init
                            for (int j = 0; j < postsSize; j++) {  //@loop
                                int x = posts[j][0], y = posts[j][1];  //@loop
                                while (tail > head && x - posts[dq[head]][0] > k) head++;  //@expire
                                if (tail > head) {  //@use
                                    int i = dq[head];  //@use
                                    long long value = (long long) y + x + posts[i][1] - posts[i][0];  //@use
                                    if (value > best) best = value;  //@use
                                }
                                while (tail > head && posts[dq[tail - 1]][1] - posts[dq[tail - 1]][0] <= y - x) tail--;  //@back
                                dq[tail++] = j;  //@back
                            }
                            free(dq);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Candidate left posts, in decreasing order of `y − x`, and the best value.", {"java": "Array deque with `head`/`tail`.", "c": "Array deque with `head`/`tail`."}),
                    ("loop", "Each post as the right end of a banner."),
                    ("expire", "Posts farther than `k` to the left can't pair with `j`, nor with any later post (positions only grow). Drop them from the front."),
                    ("use", "The front has the largest `y − x` in range, so it's `j`'s best partner: value `(y_j + x_j) + (y_i − x_i)`."),
                    ("back", "Earlier posts whose `y − x` is no bigger than `j`'s are dominated: `j` is closer (stays in range longer) and at least as good. Remove them, then `j` becomes a candidate partner for later posts."),
                    ("ret", "The best banner."),
                ],
                complexity=["**Time O(n):** each post enters and leaves the deque at most once. **Space O(n)** for the deque."],
            ),
        ],
        takeaways=[
            """
            - **Separate the objective** into a part for each element of the pair; then 'best partner' becomes a max over
              a range.
            - A window defined by **distance** (not count) still slides, as long as positions are sorted: expire from the
              front with a while loop.
            - Dominated candidates (older and no better) leave from the back.
            """
        ],
    )
