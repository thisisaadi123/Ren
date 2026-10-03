"""Binary Search: rotated sorted arrays."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def min_walk(W, a, repeats=False):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        st = {k: "dim" for k in range(len(a)) if k < lo or k > hi}
        st[mid] = "active"
        st[hi] = "mark"
        if a[mid] > a[hi]:
            W.step(f"lo={lo}, hi={hi}, mid={mid}: {a[mid]} > {a[hi]}, so the drop (and the minimum) is right of mid: lo = {mid + 1}.", Row(a, st=st, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
            lo = mid + 1
        elif a[mid] < a[hi] or not repeats:
            W.step(f"lo={lo}, hi={hi}, mid={mid}: {a[mid]} < {a[hi]}, so mid … hi is sorted and the minimum is at mid or left of it: hi = {mid}.", Row(a, st=st, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
            hi = mid
        else:
            W.step(f"lo={lo}, hi={hi}, mid={mid}: {a[mid]} = {a[hi]}: can't tell which side holds the minimum. But a[hi] has a copy at mid, so dropping hi loses nothing: hi = {hi - 1}.", Row(a, st=st, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
            hi -= 1
    return lo


@problem
def rotation_low_point():
    r = [18, 22, 27, 31, 3, 6, 9, 14]
    i = r.index(min(r))

    w1 = Steps("Check every reading and keep the smallest.")
    best = r[0]
    for k, v in enumerate(r):
        best = min(best, v)
        w1.step(f"{v}: smallest so far {best}.", Row(r, st={k: "active", r.index(best): "found"}, slots=True))
    w1.steps[-1]["result"] = str(best)

    w2 = Steps("Compare mid with the last element: bigger means mid is in the upper (rotated-off) part, so the minimum is to its right.")
    lo = min_walk(w2, r)
    w2.step(f"lo = hi = {lo}: the minimum is {r[lo]}.", Row(r, st={lo: "answer"}, slots=True), result=r[lo])

    sol(
        "rotation-low-point",
        summary="""
            A rotated sorted list is two ascending runs: a high one followed by a low one, and the minimum starts the low
            run. Every element of the high run is bigger than the last element, every element of the low run is not. So
            comparing `a[mid]` with `a[hi]` tells which run mid is in, and binary search finds the start of the low run in
            O(log n).
        """,
        question=[
            """
            The readings were increasing (all different), then rotated. Return the smallest reading in O(log n).

            - **Rotation can be zero:** an unrotated list's minimum is its first element.
            - **Distinct values** make every comparison strict, which keeps the search simple. (Repeats need extra care:
              see **Low Point With Repeats**.)
            """
        ],
        think=[
            f"""
            Take `{r}`. It's two increasing runs: `{r[:i]}` (the part rotated to the front) and `{r[i:]}`. The minimum,
            {min(r)}, is where the second run begins.
            """,
            fig(Row(r, st={k: "mark" for k in range(i)} | {k: "found" for k in range(i, len(r))} | {i: "answer"}, slots=True), caption=f"High run (marked) then low run; every high value is > the last value, {r[-1]}."),
            """
            How do you tell the runs apart at a glance? Compare with the **last** element: everything in the high run is
            bigger than it, everything in the low run is at most it. That's a yes/no question ("is a[mid] > a[hi]?") that
            is yes on a prefix and no afterwards: binary search territory.

            Why compare with the last element and not the first? Because if the list wasn't rotated, comparing with the
            first element can't tell which side to go; comparing with `a[hi]` works in every case.
            """,
        ],
        approaches=[
            approach(
                "Linear minimum",
                "brute",
                "O(n)",
                "O(1)",
                idea=["Look at every reading and keep the smallest."],
                walk=w1,
                build=["Track the minimum over all readings."],
                code={
                    "python": """
                        class Solution:
                            def lowestReading(self, readings: List[int]) -> int:
                                return min(readings)  #@min
                    """,
                    "java": """
                        class Solution {
                            public int lowestReading(int[] readings) {
                                int best = readings[0];  //@min
                                for (int v : readings) best = Math.min(best, v);  //@min
                                return best;  //@min
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int lowestReading(vector<int>& readings) {
                                return *min_element(readings.begin(), readings.end());  //@min
                            }
                        };
                    """,
                    "c": """
                        int lowestReading(int* readings, int readingsSize) {
                            int best = readings[0];  //@min
                            for (int i = 1; i < readingsSize; i++) if (readings[i] < best) best = readings[i];  //@min
                            return best;  //@min
                        }
                    """,
                },
                lines=[("min", "A plain scan for the smallest value.")],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Ignores the structure; the requirement is O(log n)."],
            ),
            approach(
                "Binary search against the last element",
                "best",
                "O(log n)",
                "O(1)",
                idea=["`lo = 0`, `hi = n − 1`. If `a[mid] > a[hi]`, mid is in the high run: `lo = mid + 1`. Otherwise mid is in the low run, at or after the minimum: `hi = mid`. Return `a[lo]`."],
                walk=w2,
                build=["`lo = 0`, `hi = n − 1`.", "Compare `a[mid]` with `a[hi]` and keep the half with the drop.", "Return `a[lo]`."],
                code={
                    "python": """
                        class Solution:
                            def lowestReading(self, readings: List[int]) -> int:
                                lo, hi = 0, len(readings) - 1  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if readings[mid] > readings[hi]:  #@cmp
                                        lo = mid + 1  #@cmp
                                    else:  #@cmp
                                        hi = mid  #@cmp
                                return readings[lo]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int lowestReading(int[] readings) {
                                int lo = 0, hi = readings.length - 1;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (readings[mid] > readings[hi]) lo = mid + 1;  //@cmp
                                    else hi = mid;  //@cmp
                                }
                                return readings[lo];  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int lowestReading(vector<int>& readings) {
                                int lo = 0, hi = (int) readings.size() - 1;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (readings[mid] > readings[hi]) lo = mid + 1;  //@cmp
                                    else hi = mid;  //@cmp
                                }
                                return readings[lo];  //@ret
                            }
                        };
                    """,
                    "c": """
                        int lowestReading(int* readings, int readingsSize) {
                            int lo = 0, hi = readingsSize - 1;  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (readings[mid] > readings[hi]) lo = mid + 1;  //@cmp
                                else hi = mid;  //@cmp
                            }
                            return readings[lo];  //@ret
                        }
                    """,
                },
                lines=[("range", "The minimum is somewhere in the whole list."), ("loop", "Until one index remains."), ("cmp", "Bigger than the range's last element → mid is before the drop, so skip past it. Otherwise everything from mid to hi is ascending, so the minimum is mid or to its left."), ("ret", "The start of the low run.")],
                complexity=["**Time O(log n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - A rotated sorted array = two sorted runs. Compare `a[mid]` with `a[hi]` to know which run mid is in.
            - Comparing with `a[hi]` also handles the unrotated case without special code.
            """
        ],
    )


@problem
def low_point_with_repeats():
    r = [4, 4, 5, 6, 1, 2, 2, 4, 4, 4]

    w1 = Steps("Scan for the first drop (a reading smaller than the one before it); with no drop, the first reading is the minimum.")
    for k in range(1, len(r)):
        if r[k] < r[k - 1]:
            w1.step(f"{r[k]} < {r[k - 1]}: the drop. Minimum {r[k]}.", Row(r, st={k: "answer"}, slots=True), result=r[k])
            break
        w1.step(f"{r[k]} ≥ {r[k - 1]}: no drop yet.", Row(r, st={k: "active"}, slots=True))

    w2 = Steps("As before, but when a[mid] equals a[hi], step hi down by one.")
    lo = min_walk(w2, r, repeats=True)
    w2.step(f"lo = hi = {lo}: minimum {r[lo]}.", Row(r, st={lo: "answer"}, slots=True), result=r[lo])

    sol(
        "low-point-with-repeats",
        summary="""
            Same idea as the distinct case, comparing `a[mid]` with `a[hi]`, plus one new case: when they're **equal**,
            you can't tell which side the drop is on, but you can safely discard `hi` (mid holds the same value). That keeps
            O(log n) on typical inputs; with many equal values it degrades to O(n), which no algorithm can avoid.
        """,
        question=[
            """
            The readings were non-decreasing (repeats allowed), then rotated. Return the smallest reading.

            - **Repeats break the simple rule:** with `[3, 1, 3, 3, 3]`, mid and hi both hold 3, and the drop could be on
              either side.
            - **Worst case O(n) is expected:** `[1, 1, …, 1, 0, 1, …, 1]` hides the 0 anywhere; any algorithm must look at
              almost every element.
            """
        ],
        think=[
            f"""
            Take `{r}`. When `a[mid] > a[hi]` or `a[mid] < a[hi]`, the old reasoning still holds. The trouble is
            `a[mid] == a[hi]`: in `[3, 1, 3, 3, 3]` the minimum is left of mid, while in `[3, 3, 3, 1, 3]` it's right of mid,
            yet both look identical at mid and hi.
            """,
            fig(Row([3, 1, 3, 3, 3], st={1: "answer", 2: "active", 4: "mark"}, slots=True), Row([3, 3, 3, 1, 3], st={3: "answer", 2: "active", 4: "mark"}, slots=True), caption="Same values at mid and hi, opposite answers."),
            """
            The fix: when they're equal, drop just `hi`. That's safe because if `a[hi]` were the minimum, an equal copy
            still exists at mid, which stays in range. Each such step only shrinks the range by one, which is where the
            O(n) worst case comes from.
            """,
        ],
        approaches=[
            approach(
                "Scan for the drop",
                "brute",
                "O(n)",
                "O(1)",
                idea=["The minimum is right after the first drop; if there's no drop, it's the first element."],
                walk=w1,
                build=["For k from 1: if `a[k] < a[k − 1]`, return `a[k]`.", "Return `a[0]`."],
                code={
                    "python": """
                        class Solution:
                            def lowestWithRepeats(self, readings: List[int]) -> int:
                                for k in range(1, len(readings)):  #@scan
                                    if readings[k] < readings[k - 1]:  #@scan
                                        return readings[k]  #@scan
                                return readings[0]  #@none
                    """,
                    "java": """
                        class Solution {
                            public int lowestWithRepeats(int[] readings) {
                                for (int k = 1; k < readings.length; k++) if (readings[k] < readings[k - 1]) return readings[k];  //@scan
                                return readings[0];  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int lowestWithRepeats(vector<int>& readings) {
                                for (size_t k = 1; k < readings.size(); k++) if (readings[k] < readings[k - 1]) return readings[k];  //@scan
                                return readings[0];  //@none
                            }
                        };
                    """,
                    "c": """
                        int lowestWithRepeats(int* readings, int readingsSize) {
                            for (int k = 1; k < readingsSize; k++) if (readings[k] < readings[k - 1]) return readings[k];  //@scan
                            return readings[0];  //@none
                        }
                    """,
                },
                lines=[("scan", "The only place the sequence decreases is where the rotation cut it."), ("none", "No drop: not rotated (or all equal), so the first element is smallest.")],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Always linear, even when the values are distinct enough for binary search to work."],
            ),
            approach(
                "Binary search, shrinking on ties",
                "best",
                "O(log n) average, O(n) worst",
                "O(1)",
                idea=["`a[mid] > a[hi]` → `lo = mid + 1`; `a[mid] < a[hi]` → `hi = mid`; equal → `hi −= 1`. Return `a[lo]`."],
                walk=w2,
                build=["Same loop as the distinct case.", "Add the tie case: `hi −= 1`.", "Return `a[lo]`."],
                code={
                    "python": """
                        class Solution:
                            def lowestWithRepeats(self, readings: List[int]) -> int:
                                lo, hi = 0, len(readings) - 1  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if readings[mid] > readings[hi]:  #@right
                                        lo = mid + 1  #@right
                                    elif readings[mid] < readings[hi]:  #@left
                                        hi = mid  #@left
                                    else:  #@tie
                                        hi -= 1  #@tie
                                return readings[lo]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int lowestWithRepeats(int[] readings) {
                                int lo = 0, hi = readings.length - 1;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (readings[mid] > readings[hi]) lo = mid + 1;  //@right
                                    else if (readings[mid] < readings[hi]) hi = mid;  //@left
                                    else hi--;  //@tie
                                }
                                return readings[lo];  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int lowestWithRepeats(vector<int>& readings) {
                                int lo = 0, hi = (int) readings.size() - 1;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (readings[mid] > readings[hi]) lo = mid + 1;  //@right
                                    else if (readings[mid] < readings[hi]) hi = mid;  //@left
                                    else hi--;  //@tie
                                }
                                return readings[lo];  //@ret
                            }
                        };
                    """,
                    "c": """
                        int lowestWithRepeats(int* readings, int readingsSize) {
                            int lo = 0, hi = readingsSize - 1;  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (readings[mid] > readings[hi]) lo = mid + 1;  //@right
                                else if (readings[mid] < readings[hi]) hi = mid;  //@left
                                else hi--;  //@tie
                            }
                            return readings[lo];  //@ret
                        }
                    """,
                },
                lines=[("range", "Search the whole list."), ("loop", "Until one index remains."), ("right", "mid is in the high run: the minimum is to its right."), ("left", "mid … hi ascends: the minimum is at mid or left."), ("tie", "Ambiguous. Dropping `hi` is safe because mid holds the same value, so the minimum value is never lost."), ("ret", "The minimum value (we return the value, not its position, so losing a duplicate position doesn't matter).")],
                complexity=["**Time O(log n)** when ties are rare; **O(n)** worst case (e.g. almost all values equal). **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - With duplicates, `a[mid] == a[hi]` gives no direction; shrink by one (`hi −= 1`), which is safe because an
              equal value stays in range.
            - Some worst cases are unavoidable: when the input can hide the answer anywhere, O(n) is a lower bound.
            """
        ],
    )


@problem
def rotated_playlist():
    p, target = [21, 25, 30, 34, 2, 7, 11, 16], 7
    want = p.index(target)

    w1 = Steps("Check every position.")
    for k, v in enumerate(p):
        w1.step(f"{v}" + (": found." if v == target else "."), Row(p, st={k: "answer" if v == target else "active"}, slots=True))
        if v == target:
            w1.steps[-1]["result"] = str(k)
            break

    w2 = Steps("First find the rotation point (the minimum). Then the target lies in one of the two sorted runs: binary-search that run.")
    piv = min_walk(w2, p)
    run = (piv, len(p) - 1) if p[piv] <= target <= p[-1] else (0, piv - 1)
    w2.step(f"The low run starts at {piv}. {target} is between {p[piv]} and {p[-1]}, so search indices {run[0]}…{run[1]}." if run[0] == piv else f"The low run starts at {piv}; {target} isn't within it, so search the high run {run[0]}…{run[1]}.", Row(p, st={k: "found" for k in range(run[0], run[1] + 1)}, slots=True))
    lo, hi = run
    while lo <= hi:
        mid = (lo + hi) // 2
        if p[mid] == target:
            w2.step(f"mid={mid}: found.", Row(p, st={mid: "answer"}, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True), result=mid)
            break
        w2.step(f"mid={mid}: {p[mid]} {'<' if p[mid] < target else '>'} {target}.", Row(p, st={mid: "active"}, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
        if p[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    w3 = Steps("One pass: at least one half around mid is sorted. If the target fits inside the sorted half's range, go there; otherwise go to the other half.")
    lo, hi = 0, len(p) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        st = {k: "dim" for k in range(len(p)) if k < lo or k > hi}
        if p[mid] == target:
            st[mid] = "answer"
            w3.step(f"lo={lo}, hi={hi}, mid={mid}: found {target}.", Row(p, st=st, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True), result=mid)
            break
        st[mid] = "active"
        if p[lo] <= p[mid]:
            inside = p[lo] <= target < p[mid]
            w3.step(f"lo={lo}, hi={hi}, mid={mid}: left half {p[lo]}…{p[mid]} is sorted; {target} is " + ("inside it: go left." if inside else "not inside it: go right."), Row(p, st=st | {k: "found" for k in range(lo, mid)}, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
            if inside:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            inside = p[mid] < target <= p[hi]
            w3.step(f"lo={lo}, hi={hi}, mid={mid}: right half {p[mid]}…{p[hi]} is sorted; {target} is " + ("inside it: go right." if inside else "not inside it: go left."), Row(p, st=st | {k: "found" for k in range(mid + 1, hi + 1)}, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
            if inside:
                lo = mid + 1
            else:
                hi = mid - 1

    sol(
        "rotated-playlist",
        summary="""
            Split a rotated sorted list anywhere and **at least one side is sorted**. A sorted side has a known range
            (its two ends), so you can tell instantly whether the target could be in it. Go there if so, otherwise to the
            other side. One binary search, O(log n).
        """,
        question=[
            """
            Distinct ids were sorted, then rotated. Return the target's index, or −1, in O(log n).

            - **Unknown rotation point.** It could even be zero (fully sorted).
            - **Distinct values,** so comparisons between ends are reliable. (With repeats see **Rotated Shelf With
              Repeats**.)
            """
        ],
        think=[
            f"""
            Take `{p}` and target {target}. Split at the middle (index {(len(p) - 1) // 2}, value {p[(len(p) - 1) // 2]}).
            The left half `{p[:(len(p) - 1) // 2 + 1]}` happens to be sorted; the right half contains the drop.
            """,
            fig(Row(p, st={k: "found" for k in range((len(p) - 1) // 2 + 1)}, slots=True), caption="The sorted half (shaded) covers exactly the values between its two ends."),
            f"""
            A sorted half covers exactly the values between its first and last element. {target} is not between
            {p[0]} and {p[(len(p) - 1) // 2]}, so it can't be in the left half: go right. Repeat on the new range: again one side
            of its middle is sorted. Which side is sorted? If `a[lo] ≤ a[mid]`, the left side is (no drop inside it);
            otherwise the right side is.

            Alternatively, first find the rotation point (the minimum) with one binary search, then run an ordinary binary
            search on whichever run could contain the target. Same complexity, two searches.
            """,
        ],
        approaches=[
            approach(
                "Linear search",
                "brute",
                "O(n)",
                "O(1)",
                idea=["Check every position."],
                walk=w1,
                build=["Return the index where the value equals the target, or −1."],
                code={
                    "python": """
                        class Solution:
                            def findTrack(self, playlist: List[int], target: int) -> int:
                                for i, v in enumerate(playlist):  #@scan
                                    if v == target:  #@scan
                                        return i  #@scan
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int findTrack(int[] playlist, int target) {
                                for (int i = 0; i < playlist.length; i++) if (playlist[i] == target) return i;  //@scan
                                return -1;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int findTrack(vector<int>& playlist, int target) {
                                for (int i = 0; i < (int) playlist.size(); i++) if (playlist[i] == target) return i;  //@scan
                                return -1;  //@none
                            }
                        };
                    """,
                    "c": """
                        int findTrack(int* playlist, int playlistSize, int target) {
                            for (int i = 0; i < playlistSize; i++) if (playlist[i] == target) return i;  //@scan
                            return -1;  //@none
                        }
                    """,
                },
                lines=[("scan", "Compare every id."), ("none", "Not present.")],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Ignores that the list is two sorted runs; the requirement is O(log n)."],
            ),
            approach(
                "Find the rotation point, then search one run",
                "better",
                "O(log n)",
                "O(1)",
                idea=["Binary-search the minimum's index `p` (compare with the last element). The list is then `[p … n − 1]` and `[0 … p − 1]`, both sorted. If `a[p] ≤ target ≤ a[n − 1]`, binary-search the first run; otherwise the second."],
                walk=w2,
                build=["Find `p`, the index of the minimum.", "Pick the run whose value range could contain the target.", "Classic binary search in that run."],
                code={
                    "python": """
                        class Solution:
                            def findTrack(self, playlist: List[int], target: int) -> int:
                                a, n = playlist, len(playlist)
                                lo, hi = 0, n - 1  #@pivot
                                while lo < hi:  #@pivot
                                    mid = (lo + hi) // 2  #@pivot
                                    if a[mid] > a[hi]:  #@pivot
                                        lo = mid + 1  #@pivot
                                    else:  #@pivot
                                        hi = mid  #@pivot
                                p = lo  #@pivot
                                lo, hi = (p, n - 1) if a[p] <= target <= a[n - 1] else (0, p - 1)  #@run
                                while lo <= hi:  #@search
                                    mid = (lo + hi) // 2  #@search
                                    if a[mid] == target:  #@search
                                        return mid  #@search
                                    if a[mid] < target:  #@search
                                        lo = mid + 1  #@search
                                    else:  #@search
                                        hi = mid - 1  #@search
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int findTrack(int[] a, int target) {
                                int n = a.length, lo = 0, hi = n - 1;  //@pivot
                                while (lo < hi) {  //@pivot
                                    int mid = lo + (hi - lo) / 2;  //@pivot
                                    if (a[mid] > a[hi]) lo = mid + 1; else hi = mid;  //@pivot
                                }  //@pivot
                                int p = lo;  //@pivot
                                if (a[p] <= target && target <= a[n - 1]) { lo = p; hi = n - 1; }  //@run
                                else { lo = 0; hi = p - 1; }  //@run
                                while (lo <= hi) {  //@search
                                    int mid = lo + (hi - lo) / 2;  //@search
                                    if (a[mid] == target) return mid;  //@search
                                    if (a[mid] < target) lo = mid + 1; else hi = mid - 1;  //@search
                                }  //@search
                                return -1;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int findTrack(vector<int>& a, int target) {
                                int n = a.size(), lo = 0, hi = n - 1;  //@pivot
                                while (lo < hi) {  //@pivot
                                    int mid = lo + (hi - lo) / 2;  //@pivot
                                    if (a[mid] > a[hi]) lo = mid + 1; else hi = mid;  //@pivot
                                }  //@pivot
                                int p = lo;  //@pivot
                                auto first = (a[p] <= target && target <= a[n - 1]) ? a.begin() + p : a.begin();  //@run
                                auto last = (a[p] <= target && target <= a[n - 1]) ? a.end() : a.begin() + p;  //@run
                                auto it = lower_bound(first, last, target);  //@search
                                return (it != last && *it == target) ? (int) (it - a.begin()) : -1;  //@search
                            }
                        };
                    """,
                    "c": """
                        int findTrack(int* a, int n, int target) {
                            int lo = 0, hi = n - 1;  //@pivot
                            while (lo < hi) {  //@pivot
                                int mid = lo + (hi - lo) / 2;  //@pivot
                                if (a[mid] > a[hi]) lo = mid + 1; else hi = mid;  //@pivot
                            }  //@pivot
                            int p = lo;  //@pivot
                            if (a[p] <= target && target <= a[n - 1]) { lo = p; hi = n - 1; }  //@run
                            else { lo = 0; hi = p - 1; }  //@run
                            while (lo <= hi) {  //@search
                                int mid = lo + (hi - lo) / 2;  //@search
                                if (a[mid] == target) return mid;  //@search
                                if (a[mid] < target) lo = mid + 1; else hi = mid - 1;  //@search
                            }  //@search
                            return -1;  //@none
                        }
                    """,
                },
                lines=[("pivot", "Index of the minimum, found by comparing with the last element (as in **Rotation Low Point**)."), ("run", "The low run `[p, n − 1]` holds values from `a[p]` to `a[n − 1]`; if the target is in that range, search there, else in the high run `[0, p − 1]`."), ("search", "An ordinary binary search inside one sorted run.", {"cpp": "`lower_bound` over the chosen run, then check equality."}), ("none", "Not found.")],
                complexity=["**Time O(log n):** two binary searches. **Space O(1).**"],
                limits=["Already optimal, but it needs two separate searches and an extra decision. The one-pass version folds both into a single loop."],
            ),
            approach(
                "One-pass search on the sorted half",
                "best",
                "O(log n)",
                "O(1)",
                idea=["At each step: if `a[mid]` is the target, done. If `a[lo] ≤ a[mid]`, the left half is sorted: go left if `a[lo] ≤ target < a[mid]`, else right. Otherwise the right half is sorted: go right if `a[mid] < target ≤ a[hi]`, else left."],
                walk=w3,
                build=["Closed range `[0, n − 1]`.", "Decide which half is sorted with `a[lo] ≤ a[mid]`.", "Check whether the target lies within that half's end values; move accordingly.", "Return −1 if the range empties."],
                code={
                    "python": """
                        class Solution:
                            def findTrack(self, playlist: List[int], target: int) -> int:
                                a = playlist
                                lo, hi = 0, len(a) - 1  #@range
                                while lo <= hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if a[mid] == target:  #@hit
                                        return mid  #@hit
                                    if a[lo] <= a[mid]:  #@leftsorted
                                        if a[lo] <= target < a[mid]:  #@leftsorted
                                            hi = mid - 1  #@leftsorted
                                        else:  #@leftsorted
                                            lo = mid + 1  #@leftsorted
                                    else:  #@rightsorted
                                        if a[mid] < target <= a[hi]:  #@rightsorted
                                            lo = mid + 1  #@rightsorted
                                        else:  #@rightsorted
                                            hi = mid - 1  #@rightsorted
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int findTrack(int[] a, int target) {
                                int lo = 0, hi = a.length - 1;  //@range
                                while (lo <= hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (a[mid] == target) return mid;  //@hit
                                    if (a[lo] <= a[mid]) {  //@leftsorted
                                        if (a[lo] <= target && target < a[mid]) hi = mid - 1;  //@leftsorted
                                        else lo = mid + 1;  //@leftsorted
                                    } else {  //@rightsorted
                                        if (a[mid] < target && target <= a[hi]) lo = mid + 1;  //@rightsorted
                                        else hi = mid - 1;  //@rightsorted
                                    }
                                }
                                return -1;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int findTrack(vector<int>& a, int target) {
                                int lo = 0, hi = (int) a.size() - 1;  //@range
                                while (lo <= hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (a[mid] == target) return mid;  //@hit
                                    if (a[lo] <= a[mid]) {  //@leftsorted
                                        if (a[lo] <= target && target < a[mid]) hi = mid - 1;  //@leftsorted
                                        else lo = mid + 1;  //@leftsorted
                                    } else {  //@rightsorted
                                        if (a[mid] < target && target <= a[hi]) lo = mid + 1;  //@rightsorted
                                        else hi = mid - 1;  //@rightsorted
                                    }
                                }
                                return -1;  //@none
                            }
                        };
                    """,
                    "c": """
                        int findTrack(int* a, int n, int target) {
                            int lo = 0, hi = n - 1;  //@range
                            while (lo <= hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (a[mid] == target) return mid;  //@hit
                                if (a[lo] <= a[mid]) {  //@leftsorted
                                    if (a[lo] <= target && target < a[mid]) hi = mid - 1;  //@leftsorted
                                    else lo = mid + 1;  //@leftsorted
                                } else {  //@rightsorted
                                    if (a[mid] < target && target <= a[hi]) lo = mid + 1;  //@rightsorted
                                    else hi = mid - 1;  //@rightsorted
                                }
                            }
                            return -1;  //@none
                        }
                    """,
                },
                lines=[("range", "Search the whole list."), ("loop", "Closed-range binary search."), ("hit", "Found."), ("leftsorted", "`a[lo] ≤ a[mid]` means no drop between lo and mid: that half is sorted and holds exactly the values `a[lo] … a[mid]`. Go there only if the target is in that range."), ("rightsorted", "Otherwise the drop is in the left half, so the right half `a[mid] … a[hi]` is sorted; same test on it."), ("none", "Range exhausted.")],
                complexity=["**Time O(log n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - In a rotated sorted array, **one half around mid is always sorted**; test whether the target lies in that
              half's value range.
            - `a[lo] ≤ a[mid]` identifies a sorted left half (with distinct values).
            - Equivalent two-step method: find the rotation point, then search one run.
            """
        ],
    )


@problem
def rotated_with_repeats():
    s, target = [6, 6, 6, 6, 6, 1, 3, 6, 6], 3

    w1 = Steps("Check every book.")
    for k, v in enumerate(s):
        w1.step(f"{v}" + (": found." if v == target else "."), Row(s, st={k: "answer" if v == target else "active"}, slots=True))
        if v == target:
            w1.steps[-1]["result"] = "true"
            break

    w2 = Steps("Sorted-half search, plus one rule: if a[lo], a[mid] and a[hi] are all equal, shrink both ends by one.")
    lo, hi = 0, len(s) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        st = {k: "dim" for k in range(len(s)) if k < lo or k > hi}
        if s[mid] == target:
            w2.step(f"lo={lo}, hi={hi}, mid={mid}: found.", Row(s, st=st | {mid: "answer"}, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True), result="true")
            break
        st[mid] = "active"
        if s[lo] == s[mid] == s[hi]:
            w2.step(f"lo={lo}, hi={hi}, mid={mid}: a[lo] = a[mid] = a[hi] = {s[mid]}; neither half can be proven sorted. Neither end is the target, so drop both: lo={lo + 1}, hi={hi - 1}.", Row(s, st=st, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
            lo += 1
            hi -= 1
        elif s[lo] <= s[mid]:
            inside = s[lo] <= target < s[mid]
            w2.step(f"lo={lo}, hi={hi}, mid={mid}: left half sorted ({s[lo]}…{s[mid]}); target " + ("inside → left." if inside else "outside → right."), Row(s, st=st, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
            if inside:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            inside = s[mid] < target <= s[hi]
            w2.step(f"lo={lo}, hi={hi}, mid={mid}: right half sorted ({s[mid]}…{s[hi]}); target " + ("inside → right." if inside else "outside → left."), Row(s, st=st, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
            if inside:
                lo = mid + 1
            else:
                hi = mid - 1

    sol(
        "rotated-with-repeats",
        summary="""
            Use the rotated-search idea (one half around mid is sorted, check whether the target fits its range). Repeats
            add one ambiguous case: when `a[lo] == a[mid] == a[hi]` you can't tell which half is sorted, so shrink both ends
            by one. Average O(log n), worst O(n), which is unavoidable here.
        """,
        question=[
            """
            Ids were sorted non-decreasingly (repeats allowed), then rotated. Return true if `target` is on the shelf.

            - **Repeats can hide the structure:** `[1, 0, 1, 1, 1]` and `[1, 1, 1, 0, 1]` look identical at lo, mid and hi.
            - **Worst case O(n) is unavoidable:** an all-equal shelf with one different id could hide it anywhere.
            - **Only true/false** is needed, which makes discarding duplicate positions harmless.
            """
        ],
        think=[
            f"""
            Take `{s}` and target {target}. At the start, a[lo], a[mid] and a[hi] are all 6. Here the drop is in the right
            half, but the shelf `[6, 1, 3, 6, 6, 6, 6, 6, 6]` shows exactly the same three values with the drop on the left.
            `a[lo] ≤ a[mid]` (6 ≤ 6) can't distinguish the two.
            """,
            fig(Row(s, st={0: "mark", 4: "active", 8: "mark"}, slots=True), caption="Equal values at lo, mid and hi: no way to tell where the drop is."),
            """
            In that situation, neither end can be the target (they equal a[mid], which we already checked), so **drop both
            ends** and look again. When the three values aren't all equal, `a[lo] ≤ a[mid]` once again reliably means the
            left half is sorted, and the distinct-values logic applies.
            """,
        ],
        approaches=[
            approach(
                "Linear search",
                "brute",
                "O(n)",
                "O(1)",
                idea=["Check every id."],
                walk=w1,
                build=["Return true if any id equals the target."],
                code={
                    "python": """
                        class Solution:
                            def onShelf(self, shelf: List[int], target: int) -> bool:
                                return target in shelf  #@scan
                    """,
                    "java": """
                        class Solution {
                            public boolean onShelf(int[] shelf, int target) {
                                for (int v : shelf) if (v == target) return true;  //@scan
                                return false;  //@scan
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool onShelf(vector<int>& shelf, int target) {
                                return find(shelf.begin(), shelf.end(), target) != shelf.end();  //@scan
                            }
                        };
                    """,
                    "c": """
                        bool onShelf(int* shelf, int shelfSize, int target) {
                            for (int i = 0; i < shelfSize; i++) if (shelf[i] == target) return true;  //@scan
                            return false;  //@scan
                        }
                    """,
                },
                lines=[("scan", "Every position is compared with the target.")],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Always linear, even on shelves with few repeats where O(log n) is possible."],
            ),
            approach(
                "Rotated search with duplicate shrinking",
                "best",
                "O(log n) average, O(n) worst",
                "O(1)",
                idea=["Same as the distinct case, but first check `a[lo] == a[mid] == a[hi]`: if so, `lo += 1`, `hi −= 1` and continue."],
                walk=w2,
                build=["Closed range binary search.", "Hit → true.", "All three equal → shrink both ends.", "Else decide the sorted half with `a[lo] ≤ a[mid]` and test the target's range."],
                code={
                    "python": """
                        class Solution:
                            def onShelf(self, shelf: List[int], target: int) -> bool:
                                a = shelf
                                lo, hi = 0, len(a) - 1  #@range
                                while lo <= hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if a[mid] == target:  #@hit
                                        return True  #@hit
                                    if a[lo] == a[mid] == a[hi]:  #@shrink
                                        lo += 1  #@shrink
                                        hi -= 1  #@shrink
                                    elif a[lo] <= a[mid]:  #@leftsorted
                                        if a[lo] <= target < a[mid]:  #@leftsorted
                                            hi = mid - 1  #@leftsorted
                                        else:  #@leftsorted
                                            lo = mid + 1  #@leftsorted
                                    else:  #@rightsorted
                                        if a[mid] < target <= a[hi]:  #@rightsorted
                                            lo = mid + 1  #@rightsorted
                                        else:  #@rightsorted
                                            hi = mid - 1  #@rightsorted
                                return False  #@none
                    """,
                    "java": """
                        class Solution {
                            public boolean onShelf(int[] a, int target) {
                                int lo = 0, hi = a.length - 1;  //@range
                                while (lo <= hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (a[mid] == target) return true;  //@hit
                                    if (a[lo] == a[mid] && a[mid] == a[hi]) { lo++; hi--; }  //@shrink
                                    else if (a[lo] <= a[mid]) {  //@leftsorted
                                        if (a[lo] <= target && target < a[mid]) hi = mid - 1;  //@leftsorted
                                        else lo = mid + 1;  //@leftsorted
                                    } else {  //@rightsorted
                                        if (a[mid] < target && target <= a[hi]) lo = mid + 1;  //@rightsorted
                                        else hi = mid - 1;  //@rightsorted
                                    }
                                }
                                return false;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool onShelf(vector<int>& a, int target) {
                                int lo = 0, hi = (int) a.size() - 1;  //@range
                                while (lo <= hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (a[mid] == target) return true;  //@hit
                                    if (a[lo] == a[mid] && a[mid] == a[hi]) { lo++; hi--; }  //@shrink
                                    else if (a[lo] <= a[mid]) {  //@leftsorted
                                        if (a[lo] <= target && target < a[mid]) hi = mid - 1;  //@leftsorted
                                        else lo = mid + 1;  //@leftsorted
                                    } else {  //@rightsorted
                                        if (a[mid] < target && target <= a[hi]) lo = mid + 1;  //@rightsorted
                                        else hi = mid - 1;  //@rightsorted
                                    }
                                }
                                return false;  //@none
                            }
                        };
                    """,
                    "c": """
                        bool onShelf(int* a, int n, int target) {
                            int lo = 0, hi = n - 1;  //@range
                            while (lo <= hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (a[mid] == target) return true;  //@hit
                                if (a[lo] == a[mid] && a[mid] == a[hi]) { lo++; hi--; }  //@shrink
                                else if (a[lo] <= a[mid]) {  //@leftsorted
                                    if (a[lo] <= target && target < a[mid]) hi = mid - 1;  //@leftsorted
                                    else lo = mid + 1;  //@leftsorted
                                } else {  //@rightsorted
                                    if (a[mid] < target && target <= a[hi]) lo = mid + 1;  //@rightsorted
                                    else hi = mid - 1;  //@rightsorted
                                }
                            }
                            return false;  //@none
                        }
                    """,
                },
                lines=[("range", "Search the whole shelf."), ("loop", "Closed-range loop."), ("hit", "Found."), ("shrink", "Ambiguous: the sorted half can't be identified. The ends equal a[mid], which isn't the target, so they can't be the target either; drop both."), ("leftsorted", "Now `a[lo] ≤ a[mid]` reliably means the left half is sorted (the all-equal case is gone). Go left only if the target is in its range."), ("rightsorted", "Otherwise the right half is sorted; same test."), ("none", "Not on the shelf.")],
                complexity=["**Time O(log n)** typically, **O(n)** when the shrink case repeats (many equal ids). **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Duplicates add one case to rotated search: `a[lo] == a[mid] == a[hi]` → shrink both ends.
            - Expect a linear worst case whenever equal values can mask the structure.
            """
        ],
    )
