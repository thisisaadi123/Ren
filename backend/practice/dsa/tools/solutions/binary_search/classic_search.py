"""Binary Search: classic search over values."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def find_the_locker():
    lockers, target = [-4, 1, 3, 8, 12, 17, 23, 30], 17
    want = lockers.index(target)

    w1 = Steps("Check lockers from the left until the target is found (or passed).")
    for i, v in enumerate(lockers):
        w1.step(f"Locker {v}" + (": found." if v == target else "."), Row(lockers, st={**{k: "dim" for k in range(i)}, i: ("answer" if v == target else "active")}, slots=True))
        if v == target:
            w1.steps[-1]["result"] = str(i)
            break

    w2 = Steps("Compare the target with the middle locker and throw away the half that can't contain it.")
    lo, hi = 0, len(lockers) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        st = {k: "dim" for k in range(len(lockers)) if k < lo or k > hi}
        st[mid] = "answer" if lockers[mid] == target else "active"
        if lockers[mid] == target:
            w2.step(f"lo={lo}, hi={hi}, mid={mid}: locker {lockers[mid]} is the target.", Row(lockers, st=st, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True), result=mid)
            break
        go = "right" if lockers[mid] < target else "left"
        w2.step(f"lo={lo}, hi={hi}, mid={mid}: {lockers[mid]} {'<' if go == 'right' else '>'} {target}, so the target can only be to the {go}.", Row(lockers, st=st, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True))
        if go == "right":
            lo = mid + 1
        else:
            hi = mid - 1

    sol(
        "find-the-locker",
        summary="""
            In a sorted list, one comparison with the middle element tells you which half the target must be in. Halving
            the range each time finds the target (or proves it's absent) in O(log n): about 17 comparisons for 10⁵
            lockers.
        """,
        question=[
            """
            Lockers are listed in strictly increasing order. Return the index of `target`, or −1.

            - **Strictly increasing**, so there is at most one match.
            - **Required: O(log n)**, which rules out checking lockers one by one.
            - **Negative numbers** are fine; only the order matters.
            """
        ],
        think=[
            f"""
            Take `lockers = {lockers}` and target {target}. Compare with the middle locker, {lockers[(len(lockers) - 1) // 2]}:
            it's smaller than {target}, and since the list is sorted, **everything to its left is smaller too**. Half
            the list is gone after one comparison. Repeat on the right half.
            """,
            fig(Row(lockers, st={k: "dim" for k in range((len(lockers) - 1) // 2 + 1)} | {(len(lockers) - 1) // 2: "active"}, slots=True), caption="One comparison with the middle rules out a whole half."),
            """
            Keep a closed range `[lo, hi]` of positions where the target could still be. Each step either finds it at
            `mid`, or moves `lo` to `mid + 1` or `hi` to `mid − 1`. When the range is empty (`lo > hi`), the target isn't
            there.
            """,
        ],
        approaches=[
            approach(
                "Check every locker",
                "brute",
                "O(n)",
                "O(1)",
                idea=["Scan from the left; return the index where the value equals the target. (You can stop once you pass a bigger value, but the worst case is still linear.)"],
                walk=w1,
                build=["For each i, return i if `lockers[i] == target`.", "Return −1."],
                code={
                    "python": """
                        class Solution:
                            def findLocker(self, lockers: List[int], target: int) -> int:
                                for i, v in enumerate(lockers):  #@scan
                                    if v == target:  #@scan
                                        return i  #@scan
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int findLocker(int[] lockers, int target) {
                                for (int i = 0; i < lockers.length; i++) if (lockers[i] == target) return i;  //@scan
                                return -1;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int findLocker(vector<int>& lockers, int target) {
                                for (int i = 0; i < (int) lockers.size(); i++) if (lockers[i] == target) return i;  //@scan
                                return -1;  //@none
                            }
                        };
                    """,
                    "c": """
                        int findLocker(int* lockers, int lockersSize, int target) {
                            for (int i = 0; i < lockersSize; i++) if (lockers[i] == target) return i;  //@scan
                            return -1;  //@none
                        }
                    """,
                },
                lines=[("scan", "Compare every locker with the target."), ("none", "Not present.")],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Doesn't use the ordering; the requirement is O(log n)."],
            ),
            approach(
                "Binary search",
                "best",
                "O(log n)",
                "O(1)",
                idea=["Closed range `[lo, hi] = [0, n − 1]`. While non-empty: look at `mid`; equal → return; smaller → `lo = mid + 1`; larger → `hi = mid − 1`. Empty range → −1."],
                walk=w2,
                build=["`lo = 0`, `hi = n − 1`.", "While `lo ≤ hi`: compute `mid`, compare, and shrink.", "Return −1 when the range empties."],
                code={
                    "python": """
                        class Solution:
                            def findLocker(self, lockers: List[int], target: int) -> int:
                                lo, hi = 0, len(lockers) - 1  #@range
                                while lo <= hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if lockers[mid] == target:  #@hit
                                        return mid  #@hit
                                    if lockers[mid] < target:  #@move
                                        lo = mid + 1  #@move
                                    else:  #@move
                                        hi = mid - 1  #@move
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int findLocker(int[] lockers, int target) {
                                int lo = 0, hi = lockers.length - 1;  //@range
                                while (lo <= hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (lockers[mid] == target) return mid;  //@hit
                                    if (lockers[mid] < target) lo = mid + 1;  //@move
                                    else hi = mid - 1;  //@move
                                }
                                return -1;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int findLocker(vector<int>& lockers, int target) {
                                int lo = 0, hi = (int) lockers.size() - 1;  //@range
                                while (lo <= hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (lockers[mid] == target) return mid;  //@hit
                                    if (lockers[mid] < target) lo = mid + 1;  //@move
                                    else hi = mid - 1;  //@move
                                }
                                return -1;  //@none
                            }
                        };
                    """,
                    "c": """
                        int findLocker(int* lockers, int lockersSize, int target) {
                            int lo = 0, hi = lockersSize - 1;  //@range
                            while (lo <= hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (lockers[mid] == target) return mid;  //@hit
                                if (lockers[mid] < target) lo = mid + 1;  //@move
                                else hi = mid - 1;  //@move
                            }
                            return -1;  //@none
                        }
                    """,
                },
                lines=[("range", "Closed range of positions that could still hold the target."), ("loop", "While anything is left; `lo + (hi − lo) / 2` is the overflow-safe middle."), ("hit", "Found."), ("move", "Smaller: the target is right of mid. Larger: left of mid. Either way mid itself is excluded."), ("none", "The range is empty: absent.")],
                complexity=["**Time O(log n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Classic binary search: closed range `[lo, hi]`, loop while `lo ≤ hi`, exclude mid when moving.
            - Every comparison halves the candidates: log₂(10⁵) ≈ 17 steps.
            """
        ],
    )


def isqrt_walk(W, x):
    lo, hi = 0, min(x, 100_000_000)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        ok = mid * mid <= x
        W.step(f"lo={lo}, hi={hi}, mid={mid}: {mid}² = {mid * mid} " + ("≤" if ok else ">") + f" {x}, so " + (f"the answer is at least {mid}: lo = {mid}." if ok else f"the answer is below {mid}: hi = {mid - 1}."), Vars(lo=lo, mid=mid, hi=hi))
        if ok:
            lo = mid
        else:
            hi = mid - 1
    return lo


@problem
def square_floor():
    x = 2024
    want = int(x ** 0.5)
    while (want + 1) ** 2 <= x:
        want += 1
    while want * want > x:
        want -= 1
    assert want == 44

    w1 = Steps("Count upward: the answer is the last k whose square doesn't exceed x.")
    for k in [0, 1, 2, 3, 43, 44, 45]:
        w1.step(f"k = {k}: {k}² = {k * k} " + ("≤" if k * k <= x else ">") + f" {x}." + (" (…counting on…)" if k == 3 else ""), Vars(k=k, square=k * k))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps(f"Binary-search the largest k with k² ≤ {x}.")
    r = isqrt_walk(w2, x)
    w2.step(f"lo = hi = {r}: {r}² = {r * r} ≤ {x} < {(r + 1) ** 2} = {r + 1}².", Vars(answer=r), result=r)

    sol(
        "square-floor",
        summary="""
            ⌊√x⌋ is the **largest k with k² ≤ x**. "k² ≤ x" is true for small k and false for large k, so binary search on
            k finds the boundary in O(log x) steps. Keep k ≤ 10⁸ so k² can't overflow 64 bits.
        """,
        question=[
            """
            Return √x rounded down, without a built-in square root or power function.

            - **Rounded down:** √8 ≈ 2.83 → 2. Perfect squares give their exact root: √49 = 7.
            - **x up to 9 × 10¹⁵:** the answer is at most about 9.5 × 10⁷, but squaring a candidate as large as x itself
              would overflow 64 bits. Bound the search range.
            - **x = 0** gives 0.
            """
        ],
        think=[
            f"""
            Take x = {x}. 44² = 1936 ≤ {x} and 45² = 2025 > {x}, so the answer is 44.

            Think of the yes/no question "is k² ≤ x?" for k = 0, 1, 2, …: it's **yes** up to the answer and **no** after
            it. Finding where a monotonic yes/no flips is exactly what binary search does, so search on k instead of
            counting up.

            Range: k is at least 0 and at most `min(x, 10⁸)` (since (10⁸)² = 10¹⁶ > 9 × 10¹⁵). The cap keeps `mid * mid`
            within 64 bits.
            """,
            fig(Row(["0", "…", "43", "44", "45", "…"], st={3: "answer", 4: "mark"}, label="k"), Row(["yes", "…", "yes", "yes", "no", "…"], st={3: "answer", 4: "mark"}, label="k² ≤ x?"),
                caption="The answer is the last 'yes'."),
            """
            Searching for the **last** yes needs the upper middle `mid = (lo + hi + 1) / 2`: with `lo = mid` on a yes, a
            lower middle could pick `mid = lo` forever when `hi = lo + 1`.
            """,
        ],
        approaches=[
            approach(
                "Count up",
                "brute",
                "O(√x)",
                "O(1)",
                idea=["Start at k = 0 and keep increasing while (k + 1)² ≤ x."],
                walk=w1,
                build=["`k = 0`.", "While `(k + 1)² ≤ x`, `k += 1`.", "Return k."],
                code={
                    "python": """
                        class Solution:
                            def squareFloor(self, x: int) -> int:
                                k = 0  #@init
                                while (k + 1) * (k + 1) <= x:  #@count
                                    k += 1  #@count
                                return k  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long squareFloor(long x) {
                                long k = 0;  //@init
                                while ((k + 1) * (k + 1) <= x) k++;  //@count
                                return k;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long squareFloor(long long x) {
                                long long k = 0;  //@init
                                while ((k + 1) * (k + 1) <= x) k++;  //@count
                                return k;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long squareFloor(long long x) {
                            long long k = 0;  //@init
                            while ((k + 1) * (k + 1) <= x) k++;  //@count
                            return k;  //@ret
                        }
                    """,
                },
                lines=[("init", "0² ≤ x always."), ("count", "Step up while the next square still fits. k never passes ~10⁸, so the square stays within 64 bits."), ("ret", "The largest k with k² ≤ x.")],
                complexity=["**Time O(√x):** up to ~9.5 × 10⁷ steps. **Space O(1).**"],
                limits=["Tries every k one by one, although \"k² ≤ x\" is monotonic in k and could be bisected."],
                slow=True,
            ),
            approach(
                "Binary search on the answer",
                "best",
                "O(log x)",
                "O(1)",
                idea=["Search k in `[0, min(x, 10⁸)]`. With `mid = (lo + hi + 1) / 2`: if `mid² ≤ x`, the answer is ≥ mid (`lo = mid`); else it's < mid (`hi = mid − 1`). When `lo == hi`, that's ⌊√x⌋."],
                walk=w2,
                build=["`lo = 0`, `hi = min(x, 10⁸)`.", "Upper middle; move `lo` up on a yes, `hi` down on a no.", "Return `lo`."],
                code={
                    "python": """
                        class Solution:
                            def squareFloor(self, x: int) -> int:
                                lo, hi = 0, min(x, 10**8)  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi + 1) // 2  #@mid
                                    if mid * mid <= x:  #@move
                                        lo = mid  #@move
                                    else:  #@move
                                        hi = mid - 1  #@move
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long squareFloor(long x) {
                                long lo = 0, hi = Math.min(x, 100_000_000L);  //@range
                                while (lo < hi) {  //@loop
                                    long mid = lo + (hi - lo + 1) / 2;  //@mid
                                    if (mid * mid <= x) lo = mid;  //@move
                                    else hi = mid - 1;  //@move
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long squareFloor(long long x) {
                                long long lo = 0, hi = min(x, 100000000LL);  //@range
                                while (lo < hi) {  //@loop
                                    long long mid = lo + (hi - lo + 1) / 2;  //@mid
                                    if (mid * mid <= x) lo = mid;  //@move
                                    else hi = mid - 1;  //@move
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long squareFloor(long long x) {
                            long long lo = 0, hi = x < 100000000LL ? x : 100000000LL;  //@range
                            while (lo < hi) {  //@loop
                                long long mid = lo + (hi - lo + 1) / 2;  //@mid
                                if (mid * mid <= x) lo = mid;  //@move
                                else hi = mid - 1;  //@move
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[
                    ("range", "The answer is between 0 and 10⁸ (√(9 × 10¹⁵) < 10⁸), and also at most x. Capping hi keeps `mid * mid` ≤ 10¹⁶, safely inside 64 bits."),
                    ("loop", "Until one candidate is left."),
                    ("mid", "Upper middle: when `hi = lo + 1` it picks `hi`, so `lo = mid` always makes progress."),
                    ("move", "A yes means the answer is mid or above; a no means it's below mid."),
                    ("ret", "The last k with k² ≤ x."),
                ],
                complexity=["**Time O(log x):** about 27 steps for the largest inputs. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - "Largest k with f(k) ≤ x" for an increasing f is a binary search on k.
            - For the **last true**, use the upper middle `(lo + hi + 1) / 2` with `lo = mid`; for the first true, the
              lower middle with `hi = mid`.
            - Bound the search range so intermediate values (like k²) can't overflow.
            """
        ],
    )


@problem
def perfect_square_tiles():
    tiles = 7056
    r = 84
    assert r * r == tiles

    w1 = Steps("Try k = 1, 2, 3, … until k² reaches or passes the number of tiles.")
    for k in [1, 2, 3, 83, 84]:
        w1.step(f"k = {k}: {k}² = {k * k}" + (f" = {tiles}: a perfect square." if k * k == tiles else f" < {tiles}." + (" (…continuing…)" if k == 3 else "")), Vars(k=k, square=k * k))
    w1.steps[-1]["result"] = "true"

    w2 = Steps(f"Binary-search k in [1, min(tiles, 10⁸)] for k² = {tiles}.")
    lo, hi = 1, min(tiles, 100_000_000)
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == tiles:
            w2.step(f"lo={lo}, hi={hi}, mid={mid}: {mid}² = {sq} = {tiles}. Perfect square.", Vars(lo=lo, mid=mid, hi=hi), result="true")
            break
        w2.step(f"lo={lo}, hi={hi}, mid={mid}: {mid}² = {sq} " + ("<" if sq < tiles else ">") + f" {tiles}.", Vars(lo=lo, mid=mid, hi=hi))
        if sq < tiles:
            lo = mid + 1
        else:
            hi = mid - 1

    sol(
        "perfect-square-tiles",
        summary="""
            `tiles` is a perfect square exactly when some whole number k has k² = tiles. Squares grow with k, so binary
            search for that k in O(log tiles); if the search range empties without an exact hit, it's not a square.
        """,
        question=[
            """
            Return true if `tiles` is a perfect square (k × k for some whole k), without built-in square roots.

            - **1 is a perfect square** (1 × 1).
            - **Up to 9 × 10¹⁵:** a root, if any, is below 10⁸. Searching k up to `tiles` itself would square numbers
              up to 9 × 10¹⁵, overflowing 64 bits, so cap the range at 10⁸.
            - **Floating-point roots are unreliable** at this size (doubles have only 53 bits of precision), which is one
              reason built-ins are excluded.
            """
        ],
        think=[
            f"""
            Take {tiles} tiles. 84 × 84 = {tiles}, so they form an 84 × 84 square. 7055 tiles would not: 83² = 6889 and
            84² = 7056 skip right over it.

            The question "is k² = tiles for some k?" is a search for a value in the increasing sequence 1², 2², 3², …,
            which is binary search over k: compare `mid²` with tiles, and go left or right.
            """,
            fig(Row(["1", "4", "9", "…", "6889", "7056", "7225"], st={5: "answer"}, label="k² for k = 1, 2, 3, …, 83, 84, 85"), caption="A sorted sequence of squares: binary-search it for the tile count."),
        ],
        approaches=[
            approach(
                "Try every k",
                "brute",
                "O(√n)",
                "O(1)",
                idea=["Increase k from 1 while k² < tiles. At the end, check whether k² equals tiles."],
                walk=w1,
                build=["`k = 1`.", "While `k² < tiles`, `k += 1`.", "Return `k² == tiles`."],
                code={
                    "python": """
                        class Solution:
                            def isPerfectSquare(self, tiles: int) -> bool:
                                k = 1  #@init
                                while k * k < tiles:  #@count
                                    k += 1  #@count
                                return k * k == tiles  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean isPerfectSquare(long tiles) {
                                long k = 1;  //@init
                                while (k * k < tiles) k++;  //@count
                                return k * k == tiles;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool isPerfectSquare(long long tiles) {
                                long long k = 1;  //@init
                                while (k * k < tiles) k++;  //@count
                                return k * k == tiles;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool isPerfectSquare(long long tiles) {
                            long long k = 1;  //@init
                            while (k * k < tiles) k++;  //@count
                            return k * k == tiles;  //@ret
                        }
                    """,
                },
                lines=[("init", "The smallest possible side."), ("count", "Grow the side until its square reaches the tile count (k stays below ~10⁸, so k² fits in 64 bits)."), ("ret", "Exactly equal means a perfect square; overshooting means not.")],
                complexity=["**Time O(√n):** up to ~9.5 × 10⁷ steps. **Space O(1).**"],
                limits=["Visits every candidate side; the squares are sorted, so binary search needs only ~27 checks."],
                slow=True,
            ),
            approach(
                "Binary search for the side",
                "best",
                "O(log n)",
                "O(1)",
                idea=["Closed range `[1, min(tiles, 10⁸)]`. Compare `mid²` with tiles: equal → true; smaller → `lo = mid + 1`; larger → `hi = mid − 1`. Empty range → false."],
                walk=w2,
                build=["`lo = 1`, `hi = min(tiles, 10⁸)`.", "Classic search on `mid * mid`.", "Return false if the range empties."],
                code={
                    "python": """
                        class Solution:
                            def isPerfectSquare(self, tiles: int) -> bool:
                                lo, hi = 1, min(tiles, 10**8)  #@range
                                while lo <= hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    sq = mid * mid  #@loop
                                    if sq == tiles:  #@hit
                                        return True  #@hit
                                    if sq < tiles:  #@move
                                        lo = mid + 1  #@move
                                    else:  #@move
                                        hi = mid - 1  #@move
                                return False  #@none
                    """,
                    "java": """
                        class Solution {
                            public boolean isPerfectSquare(long tiles) {
                                long lo = 1, hi = Math.min(tiles, 100_000_000L);  //@range
                                while (lo <= hi) {  //@loop
                                    long mid = lo + (hi - lo) / 2;  //@loop
                                    long sq = mid * mid;  //@loop
                                    if (sq == tiles) return true;  //@hit
                                    if (sq < tiles) lo = mid + 1;  //@move
                                    else hi = mid - 1;  //@move
                                }
                                return false;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool isPerfectSquare(long long tiles) {
                                long long lo = 1, hi = min(tiles, 100000000LL);  //@range
                                while (lo <= hi) {  //@loop
                                    long long mid = lo + (hi - lo) / 2;  //@loop
                                    long long sq = mid * mid;  //@loop
                                    if (sq == tiles) return true;  //@hit
                                    if (sq < tiles) lo = mid + 1;  //@move
                                    else hi = mid - 1;  //@move
                                }
                                return false;  //@none
                            }
                        };
                    """,
                    "c": """
                        bool isPerfectSquare(long long tiles) {
                            long long lo = 1, hi = tiles < 100000000LL ? tiles : 100000000LL;  //@range
                            while (lo <= hi) {  //@loop
                                long long mid = lo + (hi - lo) / 2;  //@loop
                                long long sq = mid * mid;  //@loop
                                if (sq == tiles) return true;  //@hit
                                if (sq < tiles) lo = mid + 1;  //@move
                                else hi = mid - 1;  //@move
                            }
                            return false;  //@none
                        }
                    """,
                },
                lines=[("range", "Any root is between 1 and 10⁸; capping hi keeps `mid * mid` from overflowing."), ("loop", "Middle candidate and its square."), ("hit", "Exact square."), ("move", "Too small → bigger sides; too big → smaller sides."), ("none", "No whole side squares to the tile count.")],
                complexity=["**Time O(log n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - "Does an integer k with f(k) = target exist?" for increasing f → binary search on k.
            - Prefer exact integer arithmetic over floating-point roots for large values.
            - Cap the search range to keep products inside 64 bits.
            """
        ],
    )
