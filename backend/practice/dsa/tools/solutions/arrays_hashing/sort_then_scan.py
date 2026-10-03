"""Arrays & Hashing: sort, then scan."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

from arrays_hashing.consecutive_runs import C_SET, C_SET_ROW


@problem
def closest_heights():
    h = [170, 182, 165, 180, 176, 190]
    s = sorted(h)
    gaps = [b - a for a, b in zip(s, s[1:])]
    want = min(gaps)

    w1 = Steps("Compare every pair of players.")
    best = None
    for i in range(len(h)):
        for j in range(i + 1, len(h)):
            d = abs(h[i] - h[j])
            if best is None or d < best:
                best = d
                w1.step(f"{h[i]} vs {h[j]}: difference {d}, the closest so far.", Row(h, st={i: "answer", j: "answer"}, slots=True), Vars(best=best))
    w1.step(f"All {len(h) * (len(h) - 1) // 2} pairs checked: {best}.", Row(h, slots=True), result=best)

    w2 = Steps("Sort; the closest pair must be neighbours in sorted order.")
    w2.step(f"Sorted: {s}.", Row(h, label="heights"), Row(s, label="sorted", slots=True))
    for i, g in enumerate(gaps):
        w2.step(f"{s[i]} → {s[i + 1]}: gap {g}" + (" (smallest so far)" if g == min(gaps[:i + 1]) else "") + ".", Row(s, st={i: "active", i + 1: "active"}, slots=True), Vars(best=min(gaps[:i + 1])))
    w2.steps[-1]["result"] = str(want)

    sol(
        "closest-heights",
        summary="""
            After sorting, the two closest values are always **next to each other**: anything between them would be
            even closer to one of them. So sort and take the smallest gap between neighbours: O(n log n) instead of
            comparing all pairs.
        """,
        question=[
            """
            Return the smallest absolute difference between the heights of any two different players.

            - **Two different players**, possibly with equal heights: `[150, 150]` gives 0.
            - **Only the difference** is returned, not which players.
            - **Size:** up to 10⁵ heights up to 10⁹; differences fit in an `int`.
            """
        ],
        think=[
            f"""
            Take `{h}`. Sorted: `{s}`. The gaps between neighbours are `{gaps}`, and the smallest is {want}.
            """,
            fig(Row(s, slots=True, st={gaps.index(want): "answer", gaps.index(want) + 1: "answer"}), caption=f"The closest pair are neighbours in sorted order (gap {want})."),
            """
            Why only neighbours? Take any two values a < c that are **not** adjacent after sorting. Some b sits between
            them, and then `b − a < c − a`. So a non-adjacent pair can never be the closest one, and n − 1 neighbour
            gaps cover every candidate.
            """,
        ],
        approaches=[
            approach(
                "Compare every pair",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["Check `|h[i] − h[j]|` for every pair and keep the minimum."],
                walk=w1,
                build=["`best = ∞`.", "For every i < j, `best = min(best, |h[i] − h[j]|)`.", "Return `best`."],
                code={
                    "python": """
                        class Solution:
                            def closestGap(self, heights: List[int]) -> int:
                                n = len(heights)
                                best = float("inf")  #@init
                                for i in range(n):  #@pairs
                                    for j in range(i + 1, n):  #@pairs
                                        best = min(best, abs(heights[i] - heights[j]))  #@pairs
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int closestGap(int[] heights) {
                                int n = heights.length, best = Integer.MAX_VALUE;  //@init
                                for (int i = 0; i < n; i++)  //@pairs
                                    for (int j = i + 1; j < n; j++)  //@pairs
                                        best = Math.min(best, Math.abs(heights[i] - heights[j]));  //@pairs
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int closestGap(vector<int>& heights) {
                                int n = heights.size(), best = INT_MAX;  //@init
                                for (int i = 0; i < n; i++)  //@pairs
                                    for (int j = i + 1; j < n; j++)  //@pairs
                                        best = min(best, abs(heights[i] - heights[j]));  //@pairs
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int closestGap(int* heights, int heightsSize) {
                            int best = INT_MAX;  //@init
                            for (int i = 0; i < heightsSize; i++)  //@pairs
                                for (int j = i + 1; j < heightsSize; j++) {  //@pairs
                                    int d = abs(heights[i] - heights[j]);  //@pairs
                                    if (d < best) best = d;  //@pairs
                                }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Larger than any real difference."), ("pairs", "Every pair once; heights are 0 … 10⁹, so differences fit in `int`."), ("ret", "The smallest difference.")],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["Most pairs are far apart and can't be the answer. In sorted order only neighbours can be."],
                slow=True,
            ),
            approach(
                "Sort, then check neighbours",
                "best",
                "O(n log n)",
                "O(n)",
                idea=["Sort a copy; return the minimum of `s[i + 1] − s[i]`."],
                walk=w2,
                build=["Sort a copy.", "Scan neighbours, keeping the smallest gap."],
                code={
                    "python": """
                        class Solution:
                            def closestGap(self, heights: List[int]) -> int:
                                s = sorted(heights)  #@sort
                                return min(s[i + 1] - s[i] for i in range(len(s) - 1))  #@scan
                    """,
                    "java": """
                        class Solution {
                            public int closestGap(int[] heights) {
                                int[] s = heights.clone();  //@sort
                                Arrays.sort(s);  //@sort
                                int best = Integer.MAX_VALUE;  //@scan
                                for (int i = 0; i + 1 < s.length; i++) best = Math.min(best, s[i + 1] - s[i]);  //@scan
                                return best;  //@scan
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int closestGap(vector<int>& heights) {
                                vector<int> s = heights;  //@sort
                                sort(s.begin(), s.end());  //@sort
                                int best = INT_MAX;  //@scan
                                for (size_t i = 0; i + 1 < s.size(); i++) best = min(best, s[i + 1] - s[i]);  //@scan
                                return best;  //@scan
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@sort
                            int p = *(const int*) a, q = *(const int*) b;  //@sort
                            return (p > q) - (p < q);  //@sort
                        }  //@sort

                        int closestGap(int* heights, int heightsSize) {
                            int* s = malloc(heightsSize * sizeof(int));  //@sort
                            memcpy(s, heights, heightsSize * sizeof(int));  //@sort
                            qsort(s, heightsSize, sizeof(int), cmpInt);  //@sort
                            int best = INT_MAX;  //@scan
                            for (int i = 0; i + 1 < heightsSize; i++) if (s[i + 1] - s[i] < best) best = s[i + 1] - s[i];  //@scan
                            free(s);  //@scan
                            return best;  //@scan
                        }
                    """,
                },
                lines=[("sort", "Sort a copy so close values become neighbours.", {"c": "Overflow-safe comparator for `qsort`."}), ("scan", "The answer is the smallest gap between neighbours; no other pair can beat it.", {"c": "Free the copy."})],
                complexity=["**Time O(n log n)** for the sort; the scan is O(n). **Space O(n)** for the copy."],
            ),
        ],
        takeaways=[
            """
            - After sorting, "closest pair" questions only need **adjacent** comparisons.
            - Sort-then-scan turns many O(n²) pairwise questions into O(n log n).
            """
        ],
    )


@problem
def influence_score():
    cit = [3, 0, 6, 1, 5, 4, 8]
    n = len(cit)
    want = max(h for h in range(n + 1) if sum(c >= h for c in cit) >= h)
    assert want == 4

    w1 = Steps("Try h from n down to 0; count papers with at least h citations; the first h that works is the answer.")
    for h in range(n, -1, -1):
        c = sum(x >= h for x in cit)
        w1.step(f"h = {h}: {c} paper{'s' if c != 1 else ''} with ≥ {h} citations" + (" → enough." if c >= h else f" (need {h})."), Row(cit, st={i: ("answer" if x >= h else "dim") for i, x in enumerate(cit)}, slots=True))
        if c >= h:
            w1.steps[-1]["result"] = str(h)
            break

    w2 = Steps("Sort descending. The i-th paper (1-based) has at least i citations as long as citations[i − 1] ≥ i.")
    s = sorted(cit, reverse=True)
    w2.step(f"Sorted, most cited first: {s}.", Row(s, slots=True))
    h = 0
    for i, c in enumerate(s):
        if c >= i + 1:
            h = i + 1
            w2.step(f"Paper #{i + 1} has {c} ≥ {i + 1} citations, so {i + 1} papers have at least {i + 1} each.", Row(s, st={k: "answer" for k in range(i + 1)}, slots=True), Vars(h=h))
        else:
            w2.step(f"Paper #{i + 1} has only {c} < {i + 1}: stop. The score is {h}.", Row(s, st={k: "answer" for k in range(i)} | {i: "mark"}, slots=True), Vars(h=h))
            break
    w2.steps[-1]["result"] = str(h)

    b = [0] * (n + 1)
    for c in cit:
        b[min(c, n)] += 1
    w3 = Steps(f"The score is at most n = {n}. Count papers per citation level (capping at n), then walk down accumulating.")
    w3.step(f"bucket[c] = papers with exactly c citations; anything above {n} goes into bucket {n}.", Row(cit, slots=True), Row(b, label="bucket 0 … n", slots=True))
    acc = 0
    for hh in range(n, -1, -1):
        acc += b[hh]
        w3.step(f"h = {hh}: papers with ≥ {hh} citations = {acc}" + (" ≥ h → answer." if acc >= hh else "."), Row(b, st={k: "found" for k in range(hh, n + 1)}, label="bucket 0 … n", slots=True), Vars(at_least=acc))
        if acc >= hh:
            w3.steps[-1]["result"] = str(hh)
            break

    sol(
        "influence-score",
        summary="""
            The score h is the largest number such that h papers each have at least h citations. Sorting the papers by
            citations (most first) makes it a simple scan: the score is the last position i where the i-th paper has at
            least i citations. Since h can never exceed n, counting papers per citation level (capped at n) avoids the
            sort and gives O(n).
        """,
        question=[
            """
            Return the largest h such that **at least h** papers have **at least h** citations each.

            - **Both conditions use the same h.** With `[3, 0, 6, 1, 5]`, three papers have ≥ 3 citations, so h ≥ 3;
              only two have ≥ 4, so h = 3.
            - **h ≤ n:** you can't have more than n papers. A huge citation count doesn't raise h past the number of
              papers.
            - **h can be 0** (no paper has any citation, or `[0]`).
            - **Size:** up to 10⁵ papers; citations up to 10⁹.
            """
        ],
        think=[
            f"""
            Take `{cit}`. Sort them, most cited first: `{sorted(cit, reverse=True)}`. Read along: the 1st paper has 8 ≥ 1,
            the 2nd has 6 ≥ 2, the 3rd has 5 ≥ 3, the 4th has 4 ≥ 4, the 5th has 3 < 5. So 4 papers have at least 4
            citations, and 5 papers don't have 5 each: h = {want}.
            """,
            fig(Row(sorted(cit, reverse=True), st={k: "answer" for k in range(want)}, slots=True), caption=f"The first {want} papers (most cited) each have at least {want} citations."),
            """
            Counting view: "how many papers have ≥ h citations?" only goes **down** as h goes up, while the requirement
            h goes up. The answer is where they cross. Since h ≤ n, any citation count above n can be treated as n,
            which lets us count papers per level in an array of size n + 1 instead of sorting.
            """,
        ],
        approaches=[
            approach(
                "Try every h",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For h = n, n − 1, …, 0: count the papers with at least h citations. The first h whose count is ≥ h is the answer."],
                walk=w1,
                build=["For h from n down to 0: count papers with `citations ≥ h`.", "Return the first h with `count ≥ h`."],
                code={
                    "python": """
                        class Solution:
                            def influenceScore(self, citations: List[int]) -> int:
                                for h in range(len(citations), -1, -1):  #@try
                                    if sum(1 for c in citations if c >= h) >= h:  #@count
                                        return h  #@count
                                return 0  #@none
                    """,
                    "java": """
                        class Solution {
                            public int influenceScore(int[] citations) {
                                for (int h = citations.length; h >= 0; h--) {  //@try
                                    int count = 0;  //@count
                                    for (int c : citations) if (c >= h) count++;  //@count
                                    if (count >= h) return h;  //@count
                                }
                                return 0;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int influenceScore(vector<int>& citations) {
                                for (int h = citations.size(); h >= 0; h--) {  //@try
                                    int count = 0;  //@count
                                    for (int c : citations) if (c >= h) count++;  //@count
                                    if (count >= h) return h;  //@count
                                }
                                return 0;  //@none
                            }
                        };
                    """,
                    "c": """
                        int influenceScore(int* citations, int citationsSize) {
                            for (int h = citationsSize; h >= 0; h--) {  //@try
                                int count = 0;  //@count
                                for (int i = 0; i < citationsSize; i++) if (citations[i] >= h) count++;  //@count
                                if (count >= h) return h;  //@count
                            }
                            return 0;  //@none
                        }
                    """,
                },
                lines=[("try", "From the largest possible score downwards, so the first success is the maximum."), ("count", "How many papers reach h citations? Enough of them means h works."), ("none", "Unreachable: h = 0 always works.")],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["Each h recounts all papers. Sorting once answers every \"how many have ≥ h?\" by position."],
                slow=True,
            ),
            approach(
                "Sort descending and scan",
                "better",
                "O(n log n)",
                "O(n)",
                idea=["Sort citations from most to least. The i-th paper (1-based) is the weakest of the top i. While it has at least i citations, the top i papers all have ≥ i, so h is at least i. The first failure ends the scan."],
                walk=w2,
                build=["Sort descending.", "For i = 1, 2, …: if `s[i − 1] ≥ i`, set `h = i`; otherwise stop.", "Return h."],
                code={
                    "python": """
                        class Solution:
                            def influenceScore(self, citations: List[int]) -> int:
                                s = sorted(citations, reverse=True)  #@sort
                                h = 0  #@scan
                                while h < len(s) and s[h] >= h + 1:  #@scan
                                    h += 1  #@scan
                                return h  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int influenceScore(int[] citations) {
                                int[] s = citations.clone();  //@sort
                                Arrays.sort(s);  //@sort
                                int n = s.length, h = 0;  //@scan
                                while (h < n && s[n - 1 - h] >= h + 1) h++;  //@scan
                                return h;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int influenceScore(vector<int>& citations) {
                                vector<int> s = citations;  //@sort
                                sort(s.rbegin(), s.rend());  //@sort
                                int h = 0;  //@scan
                                while (h < (int) s.size() && s[h] >= h + 1) h++;  //@scan
                                return h;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int descending(const void* a, const void* b) {  //@sort
                            int p = *(const int*) a, q = *(const int*) b;  //@sort
                            return (q > p) - (q < p);  //@sort
                        }  //@sort

                        int influenceScore(int* citations, int citationsSize) {
                            int* s = malloc(citationsSize * sizeof(int));  //@sort
                            memcpy(s, citations, citationsSize * sizeof(int));  //@sort
                            qsort(s, citationsSize, sizeof(int), descending);  //@sort
                            int h = 0;  //@scan
                            while (h < citationsSize && s[h] >= h + 1) h++;  //@scan
                            free(s);  //@ret
                            return h;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Most cited first.", {"java": "Java sorts `int[]` ascending, so the scan reads it from the end.", "cpp": "Sorting with reverse iterators gives descending order.", "c": "A comparator with the arguments swapped sorts descending."}), ("scan", "`h` papers are confirmed; the next one (the (h + 1)-th most cited) must have at least h + 1 citations to raise the score."), ("ret", "The score.")],
                complexity=["**Time O(n log n).** **Space O(n)** for the copy."],
                limits=["We sort values up to 10⁹, but only whether each count is ≥ some h ≤ n matters. Capping at n and counting replaces the sort."],
            ),
            approach(
                "Count papers per citation level",
                "best",
                "O(n)",
                "O(n)",
                idea=["`bucket[c]` = number of papers with exactly c citations, where any count above n is put in `bucket[n]`. Walk h from n down, accumulating `bucket[h]` into \"papers with ≥ h\". The first h where that total reaches h is the answer."],
                walk=w3,
                build=["`bucket` of size n + 1; add each paper to `bucket[min(c, n)]`.", "`atLeast = 0`; for h from n down to 0: `atLeast += bucket[h]`; if `atLeast ≥ h`, return h."],
                code={
                    "python": """
                        class Solution:
                            def influenceScore(self, citations: List[int]) -> int:
                                n = len(citations)
                                bucket = [0] * (n + 1)  #@bucket
                                for c in citations:  #@bucket
                                    bucket[min(c, n)] += 1  #@bucket
                                at_least = 0  #@walk
                                for h in range(n, -1, -1):  #@walk
                                    at_least += bucket[h]  #@walk
                                    if at_least >= h:  #@walk
                                        return h  #@walk
                                return 0  #@none
                    """,
                    "java": """
                        class Solution {
                            public int influenceScore(int[] citations) {
                                int n = citations.length;
                                int[] bucket = new int[n + 1];  //@bucket
                                for (int c : citations) bucket[Math.min(c, n)]++;  //@bucket
                                int atLeast = 0;  //@walk
                                for (int h = n; h >= 0; h--) {  //@walk
                                    atLeast += bucket[h];  //@walk
                                    if (atLeast >= h) return h;  //@walk
                                }
                                return 0;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int influenceScore(vector<int>& citations) {
                                int n = citations.size();
                                vector<int> bucket(n + 1, 0);  //@bucket
                                for (int c : citations) bucket[min(c, n)]++;  //@bucket
                                int atLeast = 0;  //@walk
                                for (int h = n; h >= 0; h--) {  //@walk
                                    atLeast += bucket[h];  //@walk
                                    if (atLeast >= h) return h;  //@walk
                                }
                                return 0;  //@none
                            }
                        };
                    """,
                    "c": """
                        int influenceScore(int* citations, int citationsSize) {
                            int n = citationsSize;
                            int* bucket = calloc(n + 1, sizeof(int));  //@bucket
                            for (int i = 0; i < n; i++) bucket[citations[i] < n ? citations[i] : n]++;  //@bucket
                            int atLeast = 0, h = n;  //@walk
                            for (; h >= 0; h--) {  //@walk
                                atLeast += bucket[h];  //@walk
                                if (atLeast >= h) break;  //@walk
                            }
                            free(bucket);  //@none
                            return h;  //@none
                        }
                    """,
                },
                lines=[("bucket", "Papers per citation level. Levels above n can't make h larger than n, so they're merged into level n; this keeps the array at n + 1 slots."), ("walk", "From high to low, `atLeast` = papers with at least h citations. It only grows as h shrinks; the first h it reaches is the largest that works."), ("none", "h = 0 always works, so the loop always returns.", {"c": "Free the buckets and return the h where the loop stopped."})],
                complexity=["**Time O(n).** **Space O(n)** for the buckets."],
            ),
        ],
        takeaways=[
            """
            - "Largest h such that at least h items are ≥ h" is answered by sorting descending and scanning, or by
              **counting sort with values capped at n**.
            - When the answer is bounded by n, values larger than n can be clamped, which makes counting feasible.
            """
        ],
    )


@problem
def longest_streak():
    days = [100, 4, 200, 1, 3, 2, 101, 102, 50]
    have = set(days)
    want = 0
    for d in have:
        if d - 1 not in have:
            e = d
            while e + 1 in have:
                e += 1
            want = max(want, e - d + 1)
    assert want == 4

    w1 = Steps("From every day, extend the streak forward by scanning the list for the next day.")
    best = 0
    for d in days:
        n = 1
        while d + n in days:
            n += 1
        best = max(best, n)
        w1.step(f"From {d}: {' → '.join(str(d + t) for t in range(n))} (then {d + n} is missing): length {n}.", Row(days, st={days.index(d + t): ("answer" if t == 0 else "found") for t in range(n)}, slots=True), Vars(best=best))
    w1.steps[-1]["result"] = str(best)

    w2 = Steps("Sort; walk through, extending the current streak on +1, ignoring repeats, restarting otherwise.")
    s = sorted(days)
    w2.step(f"Sorted: {s}.", Row(s, slots=True))
    cur = best = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            note = "a repeat: skip"
        elif s[i] == s[i - 1] + 1:
            cur += 1
            note = f"continues the streak → {cur}"
        else:
            cur = 1
            note = "a gap: new streak of 1"
        best = max(best, cur)
        w2.step(f"{s[i]}: {note}.", Row(s, st={i: "active"}, slots=True), Vars(current=cur, best=best))
    w2.steps[-1]["result"] = str(best)

    w3 = Steps("Put the days in a hash set; only start counting at days whose previous day is missing.")
    order = list(dict.fromkeys(days))
    best = 0
    for d in order:
        i = days.index(d)
        if d - 1 in have:
            w3.step(f"{d}: {d - 1} is in the set, so {d} is not the start of a streak. Skip.", Row(days, st={i: "dim"}, slots=True), Vars(best=best))
            continue
        e = d
        while e + 1 in have:
            e += 1
        best = max(best, e - d + 1)
        w3.step(f"{d} starts a streak: {d} … {e}, length {e - d + 1}.", Row(days, st={days.index(x): ("answer" if x == d else "found") for x in range(d, e + 1)}, slots=True), Vars(best=best))
    w3.steps[-1]["result"] = str(best)

    sol(
        "longest-streak",
        summary="""
            A streak is a run of consecutive day numbers, in any order in the input. Put the days in a hash set and only
            count from days whose previous day is absent (streak starts); walk forward from each start. Every day is
            visited a constant number of times: O(n).
        """,
        question=[
            """
            Return the length of the longest run of **consecutive day numbers** that all appear in `days`.

            - **Order in the input doesn't matter:** `[100, 4, 200, 1, 3, 2]` contains 1, 2, 3, 4: length 4.
            - **Repeats don't extend a streak:** practising twice on day 5 is still one day.
            - **Empty input** gives 0.
            - **Day numbers are ±10⁹**, so they can't index an array.
            - The same idea as **Longest Chain With a Step** with step 1.
            """
        ],
        think=[
            f"""
            Take `{days}`. The streaks are 1-2-3-4 (length 4), 100-101-102 (length 3), and single days 200 and 50.
            """,
            fig(Row([1, 2, 3, 4], st={0: "answer"}, label="length 4"), Row([100, 101, 102], st={0: "answer"}, label="length 3"), Row([50], st={0: "answer"}, label="1"), Row([200], st={0: "answer"}, label="1"),
                caption="Shaded: each streak's first day, the only day whose previous day is missing."),
            """
            Two natural tools: **sorting** puts each streak's days side by side; a **hash set** answers "is day d + 1
            present?" in O(1). With the set, the trick is to start counting only at a streak's first day (where d − 1 is
            absent). Starting anywhere else would re-walk part of a streak already counted.
            """,
        ],
        approaches=[
            approach(
                "Extend from every day by scanning",
                "brute",
                "O(n³)",
                "O(1)",
                idea=["For each day d, look for d + 1 in the list, then d + 2, and so on, each time with a full scan. Keep the longest streak found."],
                walk=w1,
                build=["For each day d: `length = 1`.", "While `d + length` appears in the list (scan), `length += 1`.", "Keep the maximum (0 for an empty list)."],
                code={
                    "python": """
                        class Solution:
                            def longestStreak(self, days: List[int]) -> int:
                                best = 0
                                for d in days:  #@each
                                    length = 1  #@each
                                    while d + length in days:  #@extend
                                        length += 1  #@extend
                                    best = max(best, length)  #@best
                                return best  #@best
                    """,
                    "java": """
                        class Solution {
                            public int longestStreak(int[] days) {
                                int best = 0;
                                for (int d : days) {  //@each
                                    int length = 1;  //@each
                                    while (contains(days, (long) d + length)) length++;  //@extend
                                    best = Math.max(best, length);  //@best
                                }
                                return best;  //@best
                            }

                            private boolean contains(int[] days, long x) {  //@scan
                                for (int d : days) if (d == x) return true;  //@scan
                                return false;  //@scan
                            }  //@scan
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestStreak(vector<int>& days) {
                                auto contains = [&](long long x) {  //@scan
                                    for (int d : days) if (d == x) return true;  //@scan
                                    return false;  //@scan
                                };  //@scan
                                int best = 0;
                                for (int d : days) {  //@each
                                    int length = 1;  //@each
                                    while (contains((long long) d + length)) length++;  //@extend
                                    best = max(best, length);  //@best
                                }
                                return best;  //@best
                            }
                        };
                    """,
                    "c": """
                        static bool contains(const int* days, int n, long long x) {  //@scan
                            for (int i = 0; i < n; i++) if (days[i] == x) return true;  //@scan
                            return false;  //@scan
                        }  //@scan

                        int longestStreak(int* days, int daysSize) {
                            int best = 0;
                            for (int i = 0; i < daysSize; i++) {  //@each
                                int length = 1;  //@each
                                while (contains(days, daysSize, (long long) days[i] + length)) length++;  //@extend
                                if (length > best) best = length;  //@best
                            }
                            return best;  //@best
                        }
                    """,
                },
                lines=[("scan", "Linear search for a day number (64-bit, since `d + length` can pass 2³¹ − 1 near 10⁹)."), ("each", "Every day gets a turn as a streak start."), ("extend", "Keep finding the next day."), ("best", "Longest streak; 0 when there are no days.")],
                complexity=["**Time O(n³)** in the worst case (a streak of n days, re-walked from each day, each step scanning n). **Space O(1).**"],
                limits=["Scanning answers membership slowly, and every day re-walks its streak. Sorting fixes both at once."],
                slow=900,
            ),
            approach(
                "Sort, then scan",
                "better",
                "O(n log n)",
                "O(n)",
                idea=["Sort a copy. Walk it: an equal neighbour is a repeat (ignore); a neighbour exactly one larger extends the current streak; anything else starts a new streak of 1."],
                walk=w2,
                build=["If there are no days, return 0.", "Sort a copy; `current = best = 1`.", "For each i ≥ 1: equal → skip; +1 → `current += 1`; otherwise `current = 1`. Update `best`."],
                code={
                    "python": """
                        class Solution:
                            def longestStreak(self, days: List[int]) -> int:
                                if not days:  #@empty
                                    return 0  #@empty
                                s = sorted(days)  #@sort
                                current = best = 1  #@scan
                                for i in range(1, len(s)):  #@scan
                                    if s[i] == s[i - 1]:  #@repeat
                                        continue  #@repeat
                                    current = current + 1 if s[i] == s[i - 1] + 1 else 1  #@step
                                    best = max(best, current)  #@step
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestStreak(int[] days) {
                                if (days.length == 0) return 0;  //@empty
                                int[] s = days.clone();  //@sort
                                Arrays.sort(s);  //@sort
                                int current = 1, best = 1;  //@scan
                                for (int i = 1; i < s.length; i++) {  //@scan
                                    if (s[i] == s[i - 1]) continue;  //@repeat
                                    current = (s[i] == s[i - 1] + 1) ? current + 1 : 1;  //@step
                                    best = Math.max(best, current);  //@step
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestStreak(vector<int>& days) {
                                if (days.empty()) return 0;  //@empty
                                vector<int> s = days;  //@sort
                                sort(s.begin(), s.end());  //@sort
                                int current = 1, best = 1;  //@scan
                                for (size_t i = 1; i < s.size(); i++) {  //@scan
                                    if (s[i] == s[i - 1]) continue;  //@repeat
                                    current = (s[i] == s[i - 1] + 1) ? current + 1 : 1;  //@step
                                    best = max(best, current);  //@step
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@sort
                            int p = *(const int*) a, q = *(const int*) b;  //@sort
                            return (p > q) - (p < q);  //@sort
                        }  //@sort

                        int longestStreak(int* days, int daysSize) {
                            if (daysSize == 0) return 0;  //@empty
                            int* s = malloc(daysSize * sizeof(int));  //@sort
                            memcpy(s, days, daysSize * sizeof(int));  //@sort
                            qsort(s, daysSize, sizeof(int), cmpInt);  //@sort
                            int current = 1, best = 1;  //@scan
                            for (int i = 1; i < daysSize; i++) {  //@scan
                                if (s[i] == s[i - 1]) continue;  //@repeat
                                current = (s[i] == s[i - 1] + 1) ? current + 1 : 1;  //@step
                                if (current > best) best = current;  //@step
                            }
                            free(s);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("empty", "No days, no streak."), ("sort", "Sorted copy: each streak's days become neighbours."), ("scan", "The first day alone is a streak of 1."), ("repeat", "Same day again: doesn't extend or break the streak."), ("step", "Exactly one more than the previous day extends the streak; any bigger jump starts over. `s[i − 1] + 1` stays within `int` because days are ≤ 10⁹."), ("ret", "Longest streak.", {"c": "Free the copy."})],
                complexity=["**Time O(n log n).** **Space O(n)** for the copy."],
                limits=["The sort orders all days, but each streak only needs \"is d + 1 present?\", which a hash set answers in O(1)."],
            ),
            approach(
                "Hash set, counting from streak starts",
                "best",
                "O(n)",
                "O(n)",
                idea=["Put all days in a hash set. For each distinct day d whose previous day d − 1 is **not** present, walk forward d + 1, d + 2, … while present, and record the length. Each streak is walked once, from its start."],
                walk=w3,
                build=["Build a hash set of the days.", "For each distinct d: skip if d − 1 is in the set.", "Otherwise walk forward while the next day is present; keep the longest length.", "Return it (0 when empty)."],
                code={
                    "python": """
                        class Solution:
                            def longestStreak(self, days: List[int]) -> int:
                                have = set(days)  #@build
                                best = 0
                                for d in have:  #@each
                                    if d - 1 in have:  #@head
                                        continue  #@head
                                    end = d  #@walk
                                    while end + 1 in have:  #@walk
                                        end += 1  #@walk
                                    best = max(best, end - d + 1)  #@best
                                return best  #@best
                    """,
                    "java": """
                        class Solution {
                            public int longestStreak(int[] days) {
                                Set<Long> have = new HashSet<>();  //@build
                                for (int d : days) have.add((long) d);  //@build
                                int best = 0;
                                for (long d : have) {  //@each
                                    if (have.contains(d - 1)) continue;  //@head
                                    long end = d;  //@walk
                                    while (have.contains(end + 1)) end++;  //@walk
                                    best = Math.max(best, (int) (end - d + 1));  //@best
                                }
                                return best;  //@best
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestStreak(vector<int>& days) {
                                unordered_set<long long> have(days.begin(), days.end());  //@build
                                int best = 0;
                                for (long long d : have) {  //@each
                                    if (have.count(d - 1)) continue;  //@head
                                    long long end = d;  //@walk
                                    while (have.count(end + 1)) end++;  //@walk
                                    best = max(best, (int) (end - d + 1));  //@best
                                }
                                return best;  //@best
                            }
                        };
                    """,
                    "c": C_SET + """
                        int longestStreak(int* days, int daysSize) {
                            unsigned cap = 1;  //@build
                            while (cap < 2u * daysSize) cap <<= 1;  //@build
                            Slot* have = calloc(cap, sizeof(Slot));  //@build
                            for (int i = 0; i < daysSize; i++) add(have, cap - 1, days[i]);  //@build
                            int best = 0;
                            for (unsigned s = 0; s < cap; s++) {  //@each
                                if (!have[s].used) continue;  //@each
                                long long d = have[s].key;  //@each
                                if (has(have, cap - 1, d - 1)) continue;  //@head
                                long long end = d;  //@walk
                                while (has(have, cap - 1, end + 1)) end++;  //@walk
                                if (end - d + 1 > best) best = (int) (end - d + 1);  //@best
                            }
                            free(have);  //@best
                            return best;  //@best
                        }
                    """,
                },
                lines=[
                    C_SET_ROW,
                    ("build", "All distinct days in a hash set.", {"java": "`Long` keys, so `d ± 1` near ±10⁹ can't overflow.", "cpp": "`long long` keys, so `d ± 1` near ±10⁹ can't overflow.", "c": "A table at least twice the number of days; repeats collapse into one entry."}),
                    ("each", "Each distinct day once.", {"c": "Walk the table's used slots: exactly the distinct days."}),
                    ("head", "If the previous day is present, this day is in the middle of a streak that its first day will measure."),
                    ("walk", "A streak start: count forward while the next day exists."),
                    ("best", "Longest streak; 0 for an empty list.", {"c": "Free the table."}),
                ],
                complexity=["**Time O(n)** on average: each day is checked as a possible start once and walked over at most once. **Space O(n)** for the set."],
            ),
        ],
        takeaways=[
            """
            - Longest run of consecutive values: hash set + **start only where the previous value is missing**.
            - Sorting and scanning is the hash-free alternative (O(n log n)); remember to skip repeats.
            - Same pattern as **Longest Chain With a Step**: replace +1 with +step.
            """
        ],
    )
