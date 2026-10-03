"""Binary Search: bounds (first position at least / greater than a value)."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

from binary_search._walk import lower_bound_walk

LOWER_BOUND_NOTE = """
    The pattern behind every problem here is the **lower bound**: in a sorted array, the first index whose value
    is ≥ x (or > x for an "upper bound"). Keep a half-open range `[lo, hi)` that always contains the answer. If
    `a[mid] < x`, the answer is to the right of mid (`lo = mid + 1`); otherwise mid itself could be the answer
    (`hi = mid`). When `lo == hi`, that's the answer, possibly `n` meaning "past the end".
"""


@problem
def insert_position():
    scores, target = [2, 5, 9, 14, 20, 27, 31], 15
    pos = next((i for i, s in enumerate(scores) if s >= target), len(scores))
    assert pos == 4

    w1 = Steps("Walk from the left until reaching a score that is at least the target.")
    for i, s in enumerate(scores):
        if s >= target:
            w1.step(f"{s} ≥ {target}: the target belongs at position {i}.", Row(scores, st={**{k: "dim" for k in range(i)}, i: "answer"}, slots=True), result=i)
            break
        w1.step(f"{s} < {target}: keep going.", Row(scores, st={**{k: "dim" for k in range(i)}, i: "active"}, slots=True))

    w2 = Steps("Binary search for the first score ≥ target, keeping the answer inside [lo, hi).")
    r = lower_bound_walk(w2, scores, target)
    w2.step(f"lo = hi = {r}: the first score ≥ {target} is at {r}.", Row(scores, st={r: "answer"}, slots=True), result=r)

    sol(
        "insert-position",
        summary="""
            "Where is the target, or where would it go?" is the same question: the **first position whose score is at
            least the target**. That's a lower bound, found by binary search in O(log n).
        """,
        question=[
            """
            Scores are sorted and distinct. Return the target's index if present, otherwise the index where it would be
            inserted to keep the order.

            - **Both cases have one answer:** the first index whose score is ≥ target. If the target is present, that's
              its own index; if not, it's where it would slot in.
            - **It can be past the end:** a target larger than everything goes at index n.
            - **Required: O(log n).**
            """
        ],
        think=[
            f"""
            Take `scores = {scores}` and target {target}. Nothing equals {target}; the first score that is at least
            {target} is {scores[pos]} at index {pos}, so {target} would be inserted at {pos}.
            """,
            fig(Row(scores, st={k: ("dim" if k < pos else "found") for k in range(len(scores))} | {pos: "answer"}, slots=True), caption=f"Scores split into '< {target}' (left) and '≥ {target}' (right). The answer is where the right part starts."),
            LOWER_BOUND_NOTE,
        ],
        approaches=[
            approach(
                "Scan from the left",
                "brute",
                "O(n)",
                "O(1)",
                idea=["Return the first index whose score is at least the target; if none, return n."],
                walk=w1,
                build=["For each i, if `scores[i] ≥ target`, return i.", "Return n."],
                code={
                    "python": """
                        class Solution:
                            def insertPosition(self, scores: List[int], target: int) -> int:
                                for i, s in enumerate(scores):  #@scan
                                    if s >= target:  #@scan
                                        return i  #@scan
                                return len(scores)  #@end
                    """,
                    "java": """
                        class Solution {
                            public int insertPosition(int[] scores, int target) {
                                for (int i = 0; i < scores.length; i++) if (scores[i] >= target) return i;  //@scan
                                return scores.length;  //@end
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int insertPosition(vector<int>& scores, int target) {
                                for (int i = 0; i < (int) scores.size(); i++) if (scores[i] >= target) return i;  //@scan
                                return scores.size();  //@end
                            }
                        };
                    """,
                    "c": """
                        int insertPosition(int* scores, int scoresSize, int target) {
                            for (int i = 0; i < scoresSize; i++) if (scores[i] >= target) return i;  //@scan
                            return scoresSize;  //@end
                        }
                    """,
                },
                lines=[("scan", "The first score that is not smaller than the target marks the spot (equal means found, larger means insert here)."), ("end", "Everything is smaller: insert at the end.")],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Correct, but it ignores the sorting: the problem requires O(log n), and each comparison could rule out half of the remaining scores instead of one."],
            ),
            approach(
                "Lower-bound binary search",
                "best",
                "O(log n)",
                "O(1)",
                idea=["Keep `[lo, hi)` = `[0, n)`. While `lo < hi`: `mid = lo + (hi − lo) / 2`; if `scores[mid] < target`, the answer is after mid (`lo = mid + 1`); else mid may be it (`hi = mid`). Return `lo`."],
                walk=w2,
                build=["`lo = 0`, `hi = n` (n itself is a valid answer).", "Loop while `lo < hi`, halving the range.", "Return `lo`."],
                code={
                    "python": """
                        class Solution:
                            def insertPosition(self, scores: List[int], target: int) -> int:
                                lo, hi = 0, len(scores)  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@mid
                                    if scores[mid] < target:  #@right
                                        lo = mid + 1  #@right
                                    else:  #@left
                                        hi = mid  #@left
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int insertPosition(int[] scores, int target) {
                                int lo = 0, hi = scores.length;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@mid
                                    if (scores[mid] < target) lo = mid + 1;  //@right
                                    else hi = mid;  //@left
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int insertPosition(vector<int>& scores, int target) {
                                int lo = 0, hi = scores.size();  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@mid
                                    if (scores[mid] < target) lo = mid + 1;  //@right
                                    else hi = mid;  //@left
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int insertPosition(int* scores, int scoresSize, int target) {
                            int lo = 0, hi = scoresSize;  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@mid
                                if (scores[mid] < target) lo = mid + 1;  //@right
                                else hi = mid;  //@left
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[
                    ("range", "The answer lies in `[0, n]`; `hi = n` allows \"insert at the end\"."),
                    ("loop", "Stop when the range is a single position."),
                    ("mid", "The middle of the range; `lo + (hi − lo) / 2` avoids overflowing `lo + hi` in fixed-width languages.", {"python": "Python integers can't overflow, so `(lo + hi) // 2` is fine."}),
                    ("right", "Too small: neither mid nor anything left of it can be the first position ≥ target."),
                    ("left", "Big enough: mid could be the answer, and nothing to its right can be earlier. Keep mid in range."),
                    ("ret", "`lo == hi`: the first position whose score is ≥ target."),
                ],
                complexity=["**Time O(log n):** the range halves every step (about 17 steps for 10⁵ scores). **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Lower bound** = first index with `a[i] ≥ x`. Use the half-open `[lo, hi)` template:
              `a[mid] < x ? lo = mid + 1 : hi = mid`, return `lo`.
            - "Found or insertion point" problems are lower-bound problems in disguise.
            - `mid = lo + (hi − lo) / 2` is the overflow-safe midpoint.
            """
        ],
    )


@problem
def first_and_last_delivery():
    times, target = [2, 4, 4, 7, 7, 7, 7, 9, 12], 7
    first = times.index(target)
    last = len(times) - 1 - times[::-1].index(target)

    w1 = Steps("Scan the whole list, noting the first and last positions of the target.")
    f = l = -1
    for i, t in enumerate(times):
        if t == target:
            if f < 0:
                f = i
            l = i
        w1.step(f"Index {i}: {t}" + (f" = {target} → first {f}, last {l}." if t == target else "."), Row(times, st={i: "answer" if t == target else "active"}, slots=True), Vars(first=f, last=l))
    w1.steps[-1]["result"] = str([f, l])

    w2 = Steps("Binary-search any copy of the target, then walk outward to the ends of the block.")
    lo, hi, hit = 0, len(times) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        w2.step(f"lo={lo}, hi={hi}, mid={mid}: {times[mid]}" + (" = target." if times[mid] == target else (" < target → right." if times[mid] < target else " > target → left.")), Row(times, st={mid: "active"}, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
        if times[mid] == target:
            hit = mid
            break
        if times[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    a = b = hit
    while a > 0 and times[a - 1] == target:
        a -= 1
    while b < len(times) - 1 and times[b + 1] == target:
        b += 1
    w2.step(f"Walk left and right from {hit} while the value is still {target}: block {a}…{b}. With m copies, this walk costs O(m).", Row(times, st={k: "answer" for k in range(a, b + 1)}, slots=True), result=[a, b])

    w3 = Steps("Two lower bounds: the first index ≥ target, and the first index ≥ target + 1. The block lies between them.")
    a = lower_bound_walk(w3, times, target)
    w3.step(f"First index ≥ {target}: {a}. times[{a}] = {times[a]} = target, so it's present.", Row(times, st={a: "answer"}, slots=True))
    b = lower_bound_walk(w3, times, target + 1)
    w3.step(f"First index ≥ {target + 1}: {b}. So the last {target} is at {b} − 1 = {b - 1}.", Row(times, st={k: "answer" for k in range(a, b)}, slots=True), result=[a, b - 1])

    sol(
        "first-and-last-delivery",
        summary="""
            In a sorted list, all copies of the target form one contiguous block. Its first index is the lower bound of
            `target`, and its last index is one before the lower bound of `target + 1`. Two binary searches give both
            in O(log n), however many copies there are.
        """,
        question=[
            """
            Timestamps are sorted (with repeats). Return `[first, last]`, the first and last index of `target`, or
            `[−1, −1]` if it's absent.

            - **Many copies** can share a timestamp, possibly the whole list. The solution must stay O(log n) even
              then.
            - **Empty list** → `[−1, −1]`.
            - **target + 1** can reach 10⁹ + 1, still inside a 32-bit `int`.
            """
        ],
        think=[
            f"""
            Take `times = {times}` and target {target}. The copies of {target} occupy indices {first} … {last}.
            """,
            fig(Row(times, st={k: "answer" for k in range(first, last + 1)}, slots=True), caption=f"One contiguous block of {target}s."),
            f"""
            The block's **start** is the first index with value ≥ {target}. Its **end** is just before the first index
            with value ≥ {target + 1} (equivalently, > {target}). Both are lower bounds, so two binary searches find
            the whole block, and a final check confirms the start actually holds {target} (otherwise it's absent).
            """,
        ],
        approaches=[
            approach(
                "Scan the whole list",
                "brute",
                "O(n)",
                "O(1)",
                idea=["Walk through the list; remember the first index that equals the target and keep updating the last."],
                walk=w1,
                build=["`first = last = −1`.", "For each index with `times[i] == target`: set `first` if unset, and set `last = i`.", "Return `[first, last]`."],
                code={
                    "python": """
                        class Solution:
                            def deliveryRange(self, times: List[int], target: int) -> List[int]:
                                first = last = -1  #@init
                                for i, t in enumerate(times):  #@scan
                                    if t == target:  #@scan
                                        if first < 0:  #@scan
                                            first = i  #@scan
                                        last = i  #@scan
                                return [first, last]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] deliveryRange(int[] times, int target) {
                                int first = -1, last = -1;  //@init
                                for (int i = 0; i < times.length; i++) {  //@scan
                                    if (times[i] == target) {  //@scan
                                        if (first < 0) first = i;  //@scan
                                        last = i;  //@scan
                                    }
                                }
                                return new int[] {first, last};  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> deliveryRange(vector<int>& times, int target) {
                                int first = -1, last = -1;  //@init
                                for (int i = 0; i < (int) times.size(); i++) {  //@scan
                                    if (times[i] == target) {  //@scan
                                        if (first < 0) first = i;  //@scan
                                        last = i;  //@scan
                                    }
                                }
                                return {first, last};  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* deliveryRange(int* times, int timesSize, int target, int* returnSize) {
                            int first = -1, last = -1;  //@init
                            for (int i = 0; i < timesSize; i++) {  //@scan
                                if (times[i] == target) {  //@scan
                                    if (first < 0) first = i;  //@scan
                                    last = i;  //@scan
                                }
                            }
                            int* out = malloc(2 * sizeof(int));  //@ret
                            out[0] = first;  //@ret
                            out[1] = last;  //@ret
                            *returnSize = 2;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "Not found yet."), ("scan", "The first match sets `first`; every match moves `last`."), ("ret", "Both stay −1 if the target never appears.")],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Ignores the sort order; the problem demands O(log n)."],
            ),
            approach(
                "Find one copy, then walk outward",
                "better",
                "O(log n + m)",
                "O(1)",
                idea=["Classic binary search finds *some* index holding the target. Then step left and right while neighbours are still equal, to reach the block's ends."],
                walk=w2,
                build=["Binary-search for any index with `times[mid] == target`; return `[−1, −1]` if none.", "Move `a` left and `b` right while the neighbours equal the target.", "Return `[a, b]`."],
                code={
                    "python": """
                        class Solution:
                            def deliveryRange(self, times: List[int], target: int) -> List[int]:
                                lo, hi = 0, len(times) - 1  #@search
                                while lo <= hi:  #@search
                                    mid = (lo + hi) // 2  #@search
                                    if times[mid] == target:  #@expand
                                        a = b = mid  #@expand
                                        while a > 0 and times[a - 1] == target:  #@expand
                                            a -= 1  #@expand
                                        while b < len(times) - 1 and times[b + 1] == target:  #@expand
                                            b += 1  #@expand
                                        return [a, b]  #@expand
                                    if times[mid] < target:  #@search
                                        lo = mid + 1  #@search
                                    else:  #@search
                                        hi = mid - 1  #@search
                                return [-1, -1]  #@none
                    """,
                    "java": """
                        class Solution {
                            public int[] deliveryRange(int[] times, int target) {
                                int lo = 0, hi = times.length - 1;  //@search
                                while (lo <= hi) {  //@search
                                    int mid = lo + (hi - lo) / 2;  //@search
                                    if (times[mid] == target) {  //@expand
                                        int a = mid, b = mid;  //@expand
                                        while (a > 0 && times[a - 1] == target) a--;  //@expand
                                        while (b < times.length - 1 && times[b + 1] == target) b++;  //@expand
                                        return new int[] {a, b};  //@expand
                                    }
                                    if (times[mid] < target) lo = mid + 1;  //@search
                                    else hi = mid - 1;  //@search
                                }
                                return new int[] {-1, -1};  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> deliveryRange(vector<int>& times, int target) {
                                int lo = 0, hi = (int) times.size() - 1;  //@search
                                while (lo <= hi) {  //@search
                                    int mid = lo + (hi - lo) / 2;  //@search
                                    if (times[mid] == target) {  //@expand
                                        int a = mid, b = mid;  //@expand
                                        while (a > 0 && times[a - 1] == target) a--;  //@expand
                                        while (b < (int) times.size() - 1 && times[b + 1] == target) b++;  //@expand
                                        return {a, b};  //@expand
                                    }
                                    if (times[mid] < target) lo = mid + 1;  //@search
                                    else hi = mid - 1;  //@search
                                }
                                return {-1, -1};  //@none
                            }
                        };
                    """,
                    "c": """
                        int* deliveryRange(int* times, int timesSize, int target, int* returnSize) {
                            int* out = malloc(2 * sizeof(int));  //@none
                            out[0] = out[1] = -1;  //@none
                            *returnSize = 2;  //@none
                            int lo = 0, hi = timesSize - 1;  //@search
                            while (lo <= hi) {  //@search
                                int mid = lo + (hi - lo) / 2;  //@search
                                if (times[mid] == target) {  //@expand
                                    int a = mid, b = mid;  //@expand
                                    while (a > 0 && times[a - 1] == target) a--;  //@expand
                                    while (b < timesSize - 1 && times[b + 1] == target) b++;  //@expand
                                    out[0] = a;  //@expand
                                    out[1] = b;  //@expand
                                    break;  //@expand
                                }
                                if (times[mid] < target) lo = mid + 1;  //@search
                                else hi = mid - 1;  //@search
                            }
                            return out;  //@none
                        }
                    """,
                },
                lines=[("search", "Standard binary search over the closed range `[lo, hi]` for any copy of the target."), ("expand", "Found one: the block's ends are found by stepping outward while values stay equal."), ("none", "Not present: `[−1, −1]`.", {"c": "The answer array starts as `[−1, −1]` and is overwritten only when the target is found."})],
                complexity=["**Time O(log n + m)** for m copies, which is **O(n)** when most of the list is the target. **Space O(1).**"],
                limits=["The outward walk is linear in the number of copies, breaking the O(log n) requirement on inputs like a list of 10⁵ identical timestamps. Search for each end directly instead."],
            ),
            approach(
                "Two lower bounds",
                "best",
                "O(log n)",
                "O(1)",
                idea=["`a` = first index with value ≥ target. If `a == n` or `times[a] != target`, the target is absent. Otherwise `b` = first index with value ≥ target + 1, and the answer is `[a, b − 1]`."],
                walk=w3,
                build=["Write `firstAtLeast(x)` (lower bound).", "`a = firstAtLeast(target)`; return `[−1, −1]` if absent.", "Return `[a, firstAtLeast(target + 1) − 1]`."],
                code={
                    "python": """
                        class Solution:
                            def deliveryRange(self, times: List[int], target: int) -> List[int]:
                                def first_at_least(x):  #@lb
                                    lo, hi = 0, len(times)  #@lb
                                    while lo < hi:  #@lb
                                        mid = (lo + hi) // 2  #@lb
                                        if times[mid] < x:  #@lb
                                            lo = mid + 1  #@lb
                                        else:  #@lb
                                            hi = mid  #@lb
                                    return lo  #@lb
                                a = first_at_least(target)  #@start
                                if a == len(times) or times[a] != target:  #@absent
                                    return [-1, -1]  #@absent
                                return [a, first_at_least(target + 1) - 1]  #@end
                    """,
                    "java": """
                        class Solution {
                            public int[] deliveryRange(int[] times, int target) {
                                int a = firstAtLeast(times, target);  //@start
                                if (a == times.length || times[a] != target) return new int[] {-1, -1};  //@absent
                                return new int[] {a, firstAtLeast(times, target + 1) - 1};  //@end
                            }

                            private int firstAtLeast(int[] a, int x) {  //@lb
                                int lo = 0, hi = a.length;  //@lb
                                while (lo < hi) {  //@lb
                                    int mid = lo + (hi - lo) / 2;  //@lb
                                    if (a[mid] < x) lo = mid + 1; else hi = mid;  //@lb
                                }  //@lb
                                return lo;  //@lb
                            }  //@lb
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> deliveryRange(vector<int>& times, int target) {
                                int a = lower_bound(times.begin(), times.end(), target) - times.begin();  //@start
                                if (a == (int) times.size() || times[a] != target) return {-1, -1};  //@absent
                                int b = lower_bound(times.begin(), times.end(), target + 1) - times.begin();  //@end
                                return {a, b - 1};  //@end
                            }
                        };
                    """,
                    "c": """
                        static int firstAtLeast(const int* a, int n, int x) {  //@lb
                            int lo = 0, hi = n;  //@lb
                            while (lo < hi) {  //@lb
                                int mid = lo + (hi - lo) / 2;  //@lb
                                if (a[mid] < x) lo = mid + 1; else hi = mid;  //@lb
                            }  //@lb
                            return lo;  //@lb
                        }  //@lb

                        int* deliveryRange(int* times, int timesSize, int target, int* returnSize) {
                            int* out = malloc(2 * sizeof(int));  //@start
                            *returnSize = 2;  //@start
                            int a = firstAtLeast(times, timesSize, target);  //@start
                            if (a == timesSize || times[a] != target) {  //@absent
                                out[0] = out[1] = -1;  //@absent
                                return out;  //@absent
                            }
                            out[0] = a;  //@end
                            out[1] = firstAtLeast(times, timesSize, target + 1) - 1;  //@end
                            return out;  //@end
                        }
                    """,
                },
                lines=[
                    ("lb", "The lower-bound search: first index whose value is ≥ x, or n if none."),
                    ("start", "The block, if any, starts at the first value ≥ target.", {"cpp": "`std::lower_bound` is exactly this search."}),
                    ("absent", "If that position is past the end or holds a bigger value, the target never appears."),
                    ("end", "The first value ≥ target + 1 is just past the block, so the last copy is one before it. (target + 1 ≤ 10⁹ + 1 fits in `int`.)"),
                ],
                complexity=["**Time O(log n):** two binary searches, regardless of how many copies. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - The range of a value in a sorted array is `[lowerBound(x), lowerBound(x + 1) − 1]` (or use an upper bound
              for the end).
            - "Find one, then expand" degrades to O(n) with many duplicates; search for both boundaries instead.
            """
        ],
    )


@problem
def next_gate_letter():
    gates, cur = "bdfffkm", "f"
    idx = next((i for i, g in enumerate(gates) if g > cur), len(gates))
    want = gates[idx % len(gates)]
    assert want == "k"

    w1 = Steps("Scan from the left for the first letter strictly after the current one; wrap to the start if none.")
    for i, g in enumerate(gates):
        if g > cur:
            w1.step(f"'{g}' > '{cur}': answer.", Row(list(gates), st={**{k: "dim" for k in range(i)}, i: "answer"}, slots=True), result=g)
            break
        w1.step(f"'{g}' is not after '{cur}'.", Row(list(gates), st={**{k: "dim" for k in range(i)}, i: "active"}, slots=True))

    w2 = Steps("Upper bound: binary-search the first letter > current. If it's past the end, wrap to index 0.")
    r = lower_bound_walk(w2, list(gates), cur, strict=True)
    w2.step(f"First letter after '{cur}' is at {r}: '{gates[r % len(gates)]}'. (Had it been {len(gates)}, the answer would wrap to gates[0].)", Row(list(gates), st={r % len(gates): "answer"}, slots=True), result=gates[r % len(gates)])

    sol(
        "next-gate-letter",
        summary="""
            The answer is the first letter **strictly greater** than the current one: an upper bound in the sorted
            letters. If there is none, wrap around to the first letter. Binary search makes it O(log n); `index mod n`
            handles the wrap.
        """,
        question=[
            """
            Gate letters are sorted (with repeats). Return the first gate letter that comes strictly **after** `current`,
            or wrap around to the first letter if none does.

            - **Strictly after:** being at gate `c` with gates `cfj` gives `f`, not `c`.
            - **Repeats** don't matter: with `fff`, being at `f` skips all of them.
            - **Wrap-around:** if `current` is at or past the last letter, the answer is `gates[0]`.
            - **`current` need not be a gate letter** itself.
            """
        ],
        think=[
            f"""
            Take `gates = "{gates}"` and current `{cur}`. Letters ≤ `{cur}` (b, d and the three f's) can't be the answer;
            the first letter beyond them is `{want}`.
            """,
            fig(Row(list(gates), st={k: ("dim" if gates[k] <= cur else "found") for k in range(len(gates))} | {idx: "answer"}, slots=True), caption=f"Letters ≤ '{cur}' on the left, letters > '{cur}' on the right; the answer starts the right part."),
            """
            So this is the **upper bound**: the first index whose letter is > current. It's the lower-bound template
            with `≤` in place of `<`. If it equals n (no such letter), wrapping means index 0, and `index % n` gives both
            cases in one expression.
            """,
        ],
        approaches=[
            approach(
                "Scan from the left",
                "brute",
                "O(n)",
                "O(1)",
                idea=["Return the first letter greater than `current`; if none, return the first letter."],
                walk=w1,
                build=["For each letter, if it's > current, return it.", "Return `gates[0]`."],
                code={
                    "python": """
                        class Solution:
                            def nextGate(self, gates: str, current: str) -> str:
                                for g in gates:  #@scan
                                    if g > current:  #@scan
                                        return g  #@scan
                                return gates[0]  #@wrap
                    """,
                    "java": """
                        class Solution {
                            public String nextGate(String gates, String current) {
                                char c = current.charAt(0);  //@scan
                                for (char g : gates.toCharArray()) if (g > c) return String.valueOf(g);  //@scan
                                return String.valueOf(gates.charAt(0));  //@wrap
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string nextGate(string& gates, string& current) {
                                for (char g : gates) if (g > current[0]) return string(1, g);  //@scan
                                return string(1, gates[0]);  //@wrap
                            }
                        };
                    """,
                    "c": """
                        char* nextGate(char* gates, char* current) {
                            char* out = calloc(2, 1);  //@scan
                            out[0] = gates[0];  //@wrap
                            for (char* p = gates; *p; p++) {  //@scan
                                if (*p > current[0]) { out[0] = *p; break; }  //@scan
                            }
                            return out;  //@wrap
                        }
                    """,
                },
                lines=[("scan", "The first strictly larger letter wins.", {"java": "`current` is a one-letter string; compare its character.", "c": "The answer is a new one-letter string (plus terminator)."}), ("wrap", "Nothing larger: wrap to the first gate.", {"c": "The output starts as the wrap-around answer and is overwritten if a larger letter is found."})],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Linear in the number of gates, although the letters are sorted and half of them could be ruled out per comparison."],
            ),
            approach(
                "Upper-bound binary search with wrap",
                "best",
                "O(log n)",
                "O(1)",
                idea=["Find the first index whose letter is > current with the half-open template (`gates[mid] <= current` → `lo = mid + 1`, else `hi = mid`). Return `gates[lo % n]`."],
                walk=w2,
                build=["`lo = 0`, `hi = n`.", "While `lo < hi`: move right if `gates[mid] ≤ current`, else `hi = mid`.", "Return `gates[lo % n]`."],
                code={
                    "python": """
                        class Solution:
                            def nextGate(self, gates: str, current: str) -> str:
                                lo, hi = 0, len(gates)  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if gates[mid] <= current:  #@step
                                        lo = mid + 1  #@step
                                    else:  #@step
                                        hi = mid  #@step
                                return gates[lo % len(gates)]  #@wrap
                    """,
                    "java": """
                        class Solution {
                            public String nextGate(String gates, String current) {
                                char c = current.charAt(0);
                                int lo = 0, hi = gates.length();  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (gates.charAt(mid) <= c) lo = mid + 1;  //@step
                                    else hi = mid;  //@step
                                }
                                return String.valueOf(gates.charAt(lo % gates.length()));  //@wrap
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string nextGate(string& gates, string& current) {
                                int i = upper_bound(gates.begin(), gates.end(), current[0]) - gates.begin();  //@step
                                return string(1, gates[i % gates.size()]);  //@wrap
                            }
                        };
                    """,
                    "c": """
                        char* nextGate(char* gates, char* current) {
                            int n = strlen(gates);
                            int lo = 0, hi = n;  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (gates[mid] <= current[0]) lo = mid + 1;  //@step
                                else hi = mid;  //@step
                            }
                            char* out = calloc(2, 1);  //@wrap
                            out[0] = gates[lo % n];  //@wrap
                            return out;  //@wrap
                        }
                    """,
                },
                lines=[("range", "Half-open range over all positions plus \"past the end\"."), ("loop", "Halve until one position remains."), ("step", "Letters ≤ current are never the answer: skip past them. A larger letter might be the first one: keep it.", {"cpp": "`std::upper_bound` returns the first position with a value greater than the given one: exactly this search."}), ("wrap", "`lo == n` means no letter is after `current`; `% n` turns that into index 0.")],
                complexity=["**Time O(log n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Upper bound** = first index with `a[i] > x`; the lower-bound template with `≤` instead of `<`.
            - Circular "next" answers: compute the position, then take it `mod n`.
            """
        ],
    )


@problem
def scores_in_range():
    scores = [70, 85, 90, 60, 85, 72, 99, 55]
    qs = [[70, 86], [0, 59], [85, 85]]
    s = sorted(scores)
    import bisect
    want = [bisect.bisect_right(s, hi) - bisect.bisect_left(s, lo) for lo, hi in qs]

    w1 = Steps("For every query, scan all scores and count those inside the range.")
    for lo, hi in qs:
        c = sum(lo <= x <= hi for x in scores)
        w1.step(f"Query [{lo}, {hi}]: {c} score{'s' if c != 1 else ''} inside (checked all {len(scores)}).", Row(scores, st={i: ("answer" if lo <= x <= hi else "dim") for i, x in enumerate(scores)}, slots=True))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Sort once. For each query, the matching scores form one block: [first ≥ lo, first > hi).")
    w2.step(f"Sorted: {s}.", Row(scores, label="scores"), Row(s, label="sorted", slots=True))
    for lo, hi in qs:
        a, b = bisect.bisect_left(s, lo), bisect.bisect_right(s, hi)
        w2.step(f"Query [{lo}, {hi}]: first ≥ {lo} is index {a}; first > {hi} is index {b}; count {b} − {a} = {b - a}.", Row(s, st={k: "answer" for k in range(a, b)}, slots=True))
    w2.steps[-1]["result"] = str(want)

    sol(
        "scores-in-range",
        summary="""
            Sort the scores once. In sorted order, the scores within `[lo, hi]` are one contiguous block, from the first
            score ≥ lo to just before the first score > hi. Two binary searches per query give its size: O((n + q) log n).
        """,
        question=[
            """
            For each query `[lo, hi]`, count the scores with `lo ≤ score ≤ hi`, answering in order.

            - **The scores are unsorted**, but we may sort a copy: queries only ask how many, not which ones.
            - **Inclusive bounds**, and repeated scores each count.
            - **Many queries:** up to 10⁵ queries over 10⁵ scores, so scanning all scores per query (10¹⁰) is too slow.
            """
        ],
        think=[
            f"""
            Take `scores = {scores}`. Sorted: `{s}`. For the query [70, 86], the qualifying scores 70, 72, 85, 85 sit
            next to each other in sorted order.
            """,
            fig(Row(s, st={k: "answer" for k in range(len(s)) if 70 <= s[k] <= 86}, slots=True), caption="Scores within a range are always one block of the sorted list."),
            """
            The block starts at the **lower bound** of lo (first score ≥ lo) and ends just before the **upper bound** of
            hi (first score > hi). Their difference is the count. Sorting costs O(n log n) once; each query then costs
            two O(log n) searches.
            """,
        ],
        approaches=[
            approach(
                "Scan all scores per query",
                "brute",
                "O(n · q)",
                "O(1)",
                idea=["For each query, count the scores between lo and hi with a full pass."],
                walk=w1,
                build=["For each query, loop over all scores and count those with `lo ≤ s ≤ hi`."],
                code={
                    "python": """
                        class Solution:
                            def countInRange(self, scores: List[int], queries: List[List[int]]) -> List[int]:
                                return [sum(1 for s in scores if lo <= s <= hi) for lo, hi in queries]  #@scan
                    """,
                    "java": """
                        class Solution {
                            public int[] countInRange(int[] scores, int[][] queries) {
                                int[] out = new int[queries.length];
                                for (int q = 0; q < queries.length; q++)  //@scan
                                    for (int s : scores)  //@scan
                                        if (s >= queries[q][0] && s <= queries[q][1]) out[q]++;  //@scan
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> countInRange(vector<int>& scores, vector<vector<int>>& queries) {
                                vector<int> out;
                                for (auto& q : queries) {  //@scan
                                    int c = 0;  //@scan
                                    for (int s : scores) if (s >= q[0] && s <= q[1]) c++;  //@scan
                                    out.push_back(c);  //@scan
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* countInRange(int* scores, int scoresSize, int** queries, int queriesSize, int* queriesColSize, int* returnSize) {
                            int* out = calloc(queriesSize, sizeof(int));
                            for (int q = 0; q < queriesSize; q++)  //@scan
                                for (int i = 0; i < scoresSize; i++)  //@scan
                                    if (scores[i] >= queries[q][0] && scores[i] <= queries[q][1]) out[q]++;  //@scan
                            *returnSize = queriesSize;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("scan", "Each query checks every score."), ("ret", "Counts in query order.")],
                complexity=["**Time O(n · q).** **Space O(1)** besides the output."],
                limits=["Every query re-reads every score. Sorting once makes each query's matches a block whose ends can be binary-searched."],
                slow=True,
            ),
            approach(
                "Sort once, two binary searches per query",
                "best",
                "O((n + q) log n)",
                "O(n)",
                idea=["Sort a copy. For each query: `a` = first index with score ≥ lo, `b` = first index with score > hi. Answer `b − a`."],
                walk=w2,
                build=["Sort a copy of the scores.", "For each query, compute the lower bound of lo and the upper bound of hi.", "Append `b − a`."],
                code={
                    "python": """
                        from bisect import bisect_left, bisect_right

                        class Solution:
                            def countInRange(self, scores: List[int], queries: List[List[int]]) -> List[int]:
                                s = sorted(scores)  #@sort
                                return [bisect_right(s, hi) - bisect_left(s, lo) for lo, hi in queries]  #@query
                    """,
                    "java": """
                        class Solution {
                            public int[] countInRange(int[] scores, int[][] queries) {
                                int[] s = scores.clone();  //@sort
                                Arrays.sort(s);  //@sort
                                int[] out = new int[queries.length];  //@query
                                for (int q = 0; q < queries.length; q++) {  //@query
                                    out[q] = firstAbove(s, queries[q][1]) - firstAbove(s, queries[q][0] - 1L);  //@query
                                }
                                return out;  //@query
                            }

                            // First index whose value is greater than x.
                            private int firstAbove(int[] a, long x) {  //@bound
                                int lo = 0, hi = a.length;  //@bound
                                while (lo < hi) {  //@bound
                                    int mid = lo + (hi - lo) / 2;  //@bound
                                    if (a[mid] <= x) lo = mid + 1; else hi = mid;  //@bound
                                }  //@bound
                                return lo;  //@bound
                            }  //@bound
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> countInRange(vector<int>& scores, vector<vector<int>>& queries) {
                                vector<int> s = scores;  //@sort
                                sort(s.begin(), s.end());  //@sort
                                vector<int> out;  //@query
                                for (auto& q : queries) {  //@query
                                    auto a = lower_bound(s.begin(), s.end(), q[0]);  //@query
                                    auto b = upper_bound(s.begin(), s.end(), q[1]);  //@query
                                    out.push_back(b - a);  //@query
                                }
                                return out;  //@query
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@sort
                            int p = *(const int*) a, q = *(const int*) b;  //@sort
                            return (p > q) - (p < q);  //@sort
                        }  //@sort

                        // First index whose value is greater than x.
                        static int firstAbove(const int* a, int n, long long x) {  //@bound
                            int lo = 0, hi = n;  //@bound
                            while (lo < hi) {  //@bound
                                int mid = lo + (hi - lo) / 2;  //@bound
                                if (a[mid] <= x) lo = mid + 1; else hi = mid;  //@bound
                            }  //@bound
                            return lo;  //@bound
                        }  //@bound

                        int* countInRange(int* scores, int scoresSize, int** queries, int queriesSize, int* queriesColSize, int* returnSize) {
                            int* s = malloc(scoresSize * sizeof(int));  //@sort
                            memcpy(s, scores, scoresSize * sizeof(int));  //@sort
                            qsort(s, scoresSize, sizeof(int), cmpInt);  //@sort
                            int* out = malloc(queriesSize * sizeof(int));  //@query
                            for (int q = 0; q < queriesSize; q++) {  //@query
                                out[q] = firstAbove(s, scoresSize, queries[q][1]) - firstAbove(s, scoresSize, (long long) queries[q][0] - 1);  //@query
                            }
                            free(s);  //@query
                            *returnSize = queriesSize;  //@query
                            return out;  //@query
                        }
                    """,
                },
                lines=[
                    ("bound", "`firstAbove(x)` is the upper bound: the first index whose value exceeds x. \"First ≥ lo\" equals \"first > lo − 1\" for integers, so one helper serves both ends; `lo − 1` is computed in 64 bits because lo can be −10⁹."),
                    ("sort", "Sort a copy once."),
                    ("query", "Scores in `[lo, hi]` are the block from the first value ≥ lo up to (not including) the first value > hi.", {"python": "`bisect_left` is the lower bound, `bisect_right` the upper bound.", "cpp": "`lower_bound(lo)` and `upper_bound(hi)` bracket exactly the scores in range."}),
                ],
                complexity=["**Time O(n log n + q log n).** **Space O(n)** for the sorted copy."],
            ),
        ],
        takeaways=[
            """
            - **Count in [lo, hi] on sorted data** = `upperBound(hi) − lowerBound(lo)`.
            - Sorting once pays off when many queries follow.
            - For integers, "≥ lo" equals "> lo − 1", so one bound function can serve both ends.
            """
        ],
    )


@problem
def closest_prices():
    prices, k, x = [1, 3, 4, 7, 8, 10, 13, 15], 3, 9
    want = sorted(sorted(prices, key=lambda p: (abs(p - x), p))[:k])
    assert want == [7, 8, 10]

    w1 = Steps("Sort every price by (distance to x, price) and keep the first k, then put them back in order.")
    ranked = sorted(prices, key=lambda p: (abs(p - x), p))
    w1.step(f"Distances to {x}: " + ", ".join(f"{p}→{abs(p - x)}" for p in prices) + ".", Row(prices, slots=True), Row([abs(p - x) for p in prices], label=f"|price − {x}|", slots=True))
    w1.step(f"Ranked closest first: {ranked}. Take {k}: {ranked[:k]}; sorted: {want}.", Row(ranked, st={i: "answer" for i in range(k)}, label="ranked"), result=want)

    w2 = Steps("Start with the whole list; repeatedly drop whichever end is farther from x until k remain.")
    lo, hi = 0, len(prices) - 1
    while hi - lo + 1 > k:
        far_left = x - prices[lo] > prices[hi] - x
        w2.step(f"Ends {prices[lo]} (distance {abs(x - prices[lo])}) and {prices[hi]} (distance {abs(prices[hi] - x)}): drop the " + ("left" if far_left else "right") + " one" + (" (ties keep the smaller price)" if x - prices[lo] == prices[hi] - x else "") + ".", Row(prices, st={k2: ("dim" if k2 < lo or k2 > hi else "found") for k2 in range(len(prices))} | {lo if far_left else hi: "mark"}, ptr={"lo": lo, "hi": hi}, slots=True))
        if far_left:
            lo += 1
        else:
            hi -= 1
    w2.step(f"{k} prices remain: {prices[lo:hi + 1]}.", Row(prices, st={k2: "answer" for k2 in range(lo, hi + 1)}, slots=True), result=prices[lo:hi + 1])

    w3 = Steps("Binary-search the window's start s in [0, n − k]: compare x − prices[s] with prices[s + k] − x.")
    lo, hi = 0, len(prices) - k
    while lo < hi:
        mid = (lo + hi) // 2
        left_d, right_d = x - prices[mid], prices[mid + k] - x
        move = left_d > right_d
        w3.step(f"Window starting at {mid} is {prices[mid:mid + k]}; the next price outside it is {prices[mid + k]}. x − {prices[mid]} = {left_d} vs {prices[mid + k]} − x = {right_d}: " + ("the left end is worse, so start later: lo = " + str(mid + 1) if move else "the left end is at least as good, so start here or earlier: hi = " + str(mid)) + ".", Row(prices, st={k2: "found" for k2 in range(mid, mid + k)} | {mid + k: "mark"}, ptr={"start": mid}, slots=True))
        if move:
            lo = mid + 1
        else:
            hi = mid
    w3.step(f"Best start {lo}: {prices[lo:lo + k]}.", Row(prices, st={k2: "answer" for k2 in range(lo, lo + k)}, slots=True), result=prices[lo:lo + k])

    sol(
        "closest-prices",
        summary="""
            The k closest prices in a sorted list are always **one contiguous window**. So the task is choosing the
            window's start `s` in `0 … n − k`. Comparing the window's left end with the first price just past its right
            end tells you which way to slide, and that comparison is monotonic, so the start can be binary-searched:
            O(log(n − k) + k).
        """,
        question=[
            """
            Prices are sorted. Return the k prices closest to `x`, in increasing order. Closer means smaller `|price − x|`;
            on a tie, the **smaller price** counts as closer.

            - **Tie rule:** with x = 3 and prices 2 and 4 equally far, 2 wins.
            - **x may be outside the range** of prices; then the answer is the first or last k prices.
            - **Duplicates** each count as separate prices.
            - **Overflow:** `x − price` can be about 2 × 10⁹ in magnitude, beyond 32 bits; compare distances in 64 bits.
            """
        ],
        think=[
            f"""
            Take `prices = {prices}`, k = {k}, x = {x}. Distances: {', '.join(f'{p}→{abs(p - x)}' for p in prices)}.
            The three smallest belong to 8, 10 and 7, and they sit **next to each other** in the list.
            """,
            fig(Row(prices, st={i: "answer" for i, p in enumerate(prices) if p in want}, slots=True), caption=f"The k closest form a window around x = {x}."),
            """
            That always happens: if a price is in the answer, every price between it and x is at least as close, so it
            must be in the answer too. So the answer is a window `prices[s … s + k − 1]` and we only need s.

            To compare windows starting at s and s + 1: they share everything except `prices[s]` (only in the first) and
            `prices[s + k]` (only in the second). If `x − prices[s] > prices[s + k] − x`, the left end is worse, so the
            best start is after s; otherwise s (or something earlier) is at least as good. That test flips only once as
            s grows, which is exactly what binary search needs.
            """,
        ],
        approaches=[
            approach(
                "Rank everything by distance",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Sort all prices by (distance to x, price), take the first k, and sort those k back into increasing order."],
                walk=w1,
                build=["Sort a copy with key `(|p − x|, p)`.", "Take the first k.", "Sort them ascending and return."],
                code={
                    "python": """
                        class Solution:
                            def closestPrices(self, prices: List[int], k: int, x: int) -> List[int]:
                                ranked = sorted(prices, key=lambda p: (abs(p - x), p))  #@rank
                                return sorted(ranked[:k])  #@take
                    """,
                    "java": """
                        class Solution {
                            public int[] closestPrices(int[] prices, int k, int x) {
                                Integer[] ranked = Arrays.stream(prices).boxed().toArray(Integer[]::new);  //@rank
                                Arrays.sort(ranked, (a, b) -> {  //@rank
                                    long da = Math.abs((long) a - x), db = Math.abs((long) b - x);  //@rank
                                    return da != db ? Long.compare(da, db) : Integer.compare(a, b);  //@rank
                                });  //@rank
                                int[] out = new int[k];  //@take
                                for (int i = 0; i < k; i++) out[i] = ranked[i];  //@take
                                Arrays.sort(out);  //@take
                                return out;  //@take
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> closestPrices(vector<int>& prices, int k, int x) {
                                vector<int> ranked = prices;  //@rank
                                sort(ranked.begin(), ranked.end(), [x](int a, int b) {  //@rank
                                    long long da = llabs((long long) a - x), db = llabs((long long) b - x);  //@rank
                                    return da != db ? da < db : a < b;  //@rank
                                });  //@rank
                                vector<int> out(ranked.begin(), ranked.begin() + k);  //@take
                                sort(out.begin(), out.end());  //@take
                                return out;  //@take
                            }
                        };
                    """,
                    "c": """
                        static int gX;  //@rank

                        static int byCloseness(const void* pa, const void* pb) {  //@rank
                            int a = *(const int*) pa, b = *(const int*) pb;  //@rank
                            long long da = llabs((long long) a - gX), db = llabs((long long) b - gX);  //@rank
                            if (da != db) return da < db ? -1 : 1;  //@rank
                            return (a > b) - (a < b);  //@rank
                        }  //@rank

                        static int cmpInt(const void* pa, const void* pb) {  //@take
                            int a = *(const int*) pa, b = *(const int*) pb;  //@take
                            return (a > b) - (a < b);  //@take
                        }  //@take

                        int* closestPrices(int* prices, int pricesSize, int k, int x, int* returnSize) {
                            int* ranked = malloc(pricesSize * sizeof(int));  //@rank
                            memcpy(ranked, prices, pricesSize * sizeof(int));  //@rank
                            gX = x;  //@rank
                            qsort(ranked, pricesSize, sizeof(int), byCloseness);  //@rank
                            qsort(ranked, k, sizeof(int), cmpInt);  //@take
                            *returnSize = k;  //@take
                            return ranked;  //@take
                        }
                    """,
                },
                lines=[
                    ("rank", "Order every price by closeness, ties going to the smaller price. Distances are taken in 64 bits since `a − x` can reach about 2 × 10⁹.", {"c": "`qsort` can't capture x, so it's stored in a file-level variable for the comparator."}),
                    ("take", "The first k are the answer; return them in increasing order.", {"c": "Sort just the first k in place and return the array (its first k entries)."}),
                ],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["It ignores that the prices are already sorted, which is what makes the answer a contiguous window."],
            ),
            approach(
                "Shrink the window from both ends",
                "better",
                "O(n)",
                "O(1)",
                idea=["Start with the whole list as the window. While it holds more than k prices, remove the end that is farther from x (on a tie, remove the right end, since the smaller price wins). What's left is the answer."],
                walk=w2,
                build=["`lo = 0`, `hi = n − 1`.", "While `hi − lo + 1 > k`: if `x − prices[lo] > prices[hi] − x`, `lo += 1`, else `hi −= 1`.", "Return `prices[lo … hi]`."],
                code={
                    "python": """
                        class Solution:
                            def closestPrices(self, prices: List[int], k: int, x: int) -> List[int]:
                                lo, hi = 0, len(prices) - 1  #@ends
                                while hi - lo + 1 > k:  #@shrink
                                    if x - prices[lo] > prices[hi] - x:  #@shrink
                                        lo += 1  #@shrink
                                    else:  #@shrink
                                        hi -= 1  #@shrink
                                return prices[lo:hi + 1]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] closestPrices(int[] prices, int k, int x) {
                                int lo = 0, hi = prices.length - 1;  //@ends
                                while (hi - lo + 1 > k) {  //@shrink
                                    if ((long) x - prices[lo] > (long) prices[hi] - x) lo++;  //@shrink
                                    else hi--;  //@shrink
                                }
                                return Arrays.copyOfRange(prices, lo, hi + 1);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> closestPrices(vector<int>& prices, int k, int x) {
                                int lo = 0, hi = (int) prices.size() - 1;  //@ends
                                while (hi - lo + 1 > k) {  //@shrink
                                    if ((long long) x - prices[lo] > (long long) prices[hi] - x) lo++;  //@shrink
                                    else hi--;  //@shrink
                                }
                                return vector<int>(prices.begin() + lo, prices.begin() + hi + 1);  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* closestPrices(int* prices, int pricesSize, int k, int x, int* returnSize) {
                            int lo = 0, hi = pricesSize - 1;  //@ends
                            while (hi - lo + 1 > k) {  //@shrink
                                if ((long long) x - prices[lo] > (long long) prices[hi] - x) lo++;  //@shrink
                                else hi--;  //@shrink
                            }
                            int* out = malloc(k * sizeof(int));  //@ret
                            memcpy(out, prices + lo, k * sizeof(int));  //@ret
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("ends", "The window starts as the whole list."),
                    ("shrink", "The farthest price in the window is always one of its two ends (the list is sorted). Drop it; on a tie, the larger price (right end) goes. Distances in 64 bits."),
                    ("ret", "The remaining k prices, already in increasing order."),
                ],
                complexity=["**Time O(n − k).** **Space O(1)** besides the output."],
                limits=["Removes one price per step. Since the answer is decided by a single monotonic comparison per start position, binary search can find the start in O(log n)."],
            ),
            approach(
                "Binary-search the window start",
                "best",
                "O(log(n − k) + k)",
                "O(1)",
                idea=["Search `s` in `[0, n − k]`. For a candidate `mid`, if `x − prices[mid] > prices[mid + k] − x`, the window starting at mid loses to the one starting at mid + 1 (its left end is strictly farther), so `lo = mid + 1`; otherwise `hi = mid`. Return `prices[lo … lo + k − 1]`."],
                walk=w3,
                build=["`lo = 0`, `hi = n − k`.", "While `lo < hi`: compare `x − prices[mid]` with `prices[mid + k] − x` (64-bit).", "Return the window at `lo`."],
                code={
                    "python": """
                        class Solution:
                            def closestPrices(self, prices: List[int], k: int, x: int) -> List[int]:
                                lo, hi = 0, len(prices) - k  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if x - prices[mid] > prices[mid + k] - x:  #@cmp
                                        lo = mid + 1  #@cmp
                                    else:  #@cmp
                                        hi = mid  #@cmp
                                return prices[lo:lo + k]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] closestPrices(int[] prices, int k, int x) {
                                int lo = 0, hi = prices.length - k;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if ((long) x - prices[mid] > (long) prices[mid + k] - x) lo = mid + 1;  //@cmp
                                    else hi = mid;  //@cmp
                                }
                                return Arrays.copyOfRange(prices, lo, lo + k);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> closestPrices(vector<int>& prices, int k, int x) {
                                int lo = 0, hi = (int) prices.size() - k;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if ((long long) x - prices[mid] > (long long) prices[mid + k] - x) lo = mid + 1;  //@cmp
                                    else hi = mid;  //@cmp
                                }
                                return vector<int>(prices.begin() + lo, prices.begin() + lo + k);  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* closestPrices(int* prices, int pricesSize, int k, int x, int* returnSize) {
                            int lo = 0, hi = pricesSize - k;  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if ((long long) x - prices[mid] > (long long) prices[mid + k] - x) lo = mid + 1;  //@cmp
                                else hi = mid;  //@cmp
                            }
                            int* out = malloc(k * sizeof(int));  //@ret
                            memcpy(out, prices + lo, k * sizeof(int));  //@ret
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("range", "Possible window starts: 0 … n − k."),
                    ("loop", "Halve the candidate starts."),
                    ("cmp", "Windows at mid and mid + 1 differ only in `prices[mid]` vs `prices[mid + k]`. If the left one is strictly farther from x, starting later is better. Otherwise (closer, or tied, where the smaller price wins) a start at mid or earlier is best. Signed differences in 64 bits work even when x is outside the window: a price to the right of x gives a negative `x − price`."),
                    ("ret", "The k prices of the best window, already sorted."),
                ],
                complexity=["**Time O(log(n − k) + k):** the search plus copying k prices. **Space O(1)** besides the output."],
            ),
        ],
        takeaways=[
            """
            - In sorted data, "the k closest to x" is a **contiguous window**; search for its start, not its members.
            - Binary search works on any yes/no question that flips once, not only on values: here, "is the window at s
              worse than the one at s + 1?".
            - Use signed differences (not absolute values) in the window comparison so the tie rule falls out
              naturally.
            """
        ],
    )
