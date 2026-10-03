"""Binary Search: searching over real numbers."""
import heapq
import math

from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def f6(x):
    return f"{x:.6f}".rstrip("0").rstrip(".")


@problem
def cube_root():
    v = 50.0
    want = v ** (1 / 3)

    w1 = Steps("Newton's method: improve a guess r with r − (r³ − v) / (3r²) until it stops changing.")
    r = v
    for i in range(8):
        nr = r - (r * r * r - v) / (3 * r * r)
        w1.step(f"Step {i + 1}: r = {f6(r)} → {f6(nr)} (r³ = {f6(nr ** 3)}).", Vars(r=f6(nr), r_cubed=f6(nr ** 3)))
        if abs(nr - r) < 1e-9:
            break
        r = nr
    w1.steps[-1]["result"] = f6(want)

    w2 = Steps("Bisection: keep an interval [lo, hi] whose cube brackets v; halve it ~100 times.")
    lo, hi = -max(1.0, abs(v)), max(1.0, abs(v))
    for i in range(12):
        mid = (lo + hi) / 2
        below = mid ** 3 < v
        w2.step(f"[{f6(lo)}, {f6(hi)}], mid = {f6(mid)}: mid³ = {f6(mid ** 3)} " + ("<" if below else "≥") + f" {f6(v)}, so the root is in the " + ("upper" if below else "lower") + " half.", Vars(lo=f6(lo), hi=f6(hi), mid=f6(mid)))
        if below:
            lo = mid
        else:
            hi = mid
    w2.step(f"After 100 halvings the interval is narrower than 10⁻¹⁵ of its start: r ≈ {f6(want)}.", Vars(root=f6(want)), result=f6(want))

    sol(
        "cube-root",
        summary="""
            x³ grows steadily with x (it's strictly increasing, even for negatives), so the cube root of v is the single
            point where x³ crosses v. Bisection keeps an interval around that point and halves it a fixed number of times;
            100 halvings shrink any starting interval far below the 10⁻⁶ tolerance.
        """,
        question=[
            """
            Return r with r³ = volume, within 10⁻⁶ (relative for large values), without built-in power or root
            functions.

            - **Negative inputs are fine:** the cube root of −8 is −2 (unlike square roots).
            - **|volume| < 1** has a root larger in size than the volume (∛0.125 = 0.5), so the search interval must be
              at least [−1, 1], not [−|v|, |v|].
            - **The answer is a decimal**; exact equality is not expected.
            """
        ],
        think=[
            """
            Take v = 50. 3³ = 27 is too small and 4³ = 64 too big, so the root is between 3 and 4. Try 3.5: 42.875, too
            small, so it's between 3.5 and 4. Each test halves the interval: this is binary search on real numbers.
            """,
            fig(Row(["3", "3.5", "3.75", "3.6875", "…", "3.684"], st={5: "answer"}, label="midpoints tried"), caption="Each midpoint's cube tells which half keeps the root."),
            """
            Two details make it robust:

            - **Starting interval:** `[−max(1, |v|), max(1, |v|)]` always contains the root: for |v| ≥ 1 the root's size is
              at most |v|, and for |v| < 1 it's at most 1.
            - **Stopping:** instead of comparing with a tolerance (tricky with relative error), just halve a fixed 100 or
              more times. The interval shrinks by 2¹⁰⁰, far beyond double precision.
            """,
        ],
        approaches=[
            approach(
                "Newton's method",
                "better",
                "O(log log(1/ε)) steps once close",
                "O(1)",
                idea=["Treat it as solving f(r) = r³ − v = 0. Newton's update `r ← r − f(r) / f′(r) = r − (r³ − v) / (3r²)` roughly doubles the number of correct digits per step once r is close. Start from r = v (or 1 when v is 0 or tiny), iterate a fixed number of times."],
                walk=w1,
                build=["If v is 0, return 0.", "Start with `r = v`.", "Repeat ~100 times: `r = r − (r³ − v) / (3r²)`.", "Return r."],
                code={
                    "python": """
                        class Solution:
                            def cubeRoot(self, volume: float) -> float:
                                if volume == 0:  #@zero
                                    return 0.0  #@zero
                                r = volume  #@start
                                for _ in range(100):  #@iterate
                                    r -= (r * r * r - volume) / (3 * r * r)  #@iterate
                                return r  #@ret
                    """,
                    "java": """
                        class Solution {
                            public double cubeRoot(double volume) {
                                if (volume == 0) return 0;  //@zero
                                double r = volume;  //@start
                                for (int i = 0; i < 100; i++) r -= (r * r * r - volume) / (3 * r * r);  //@iterate
                                return r;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            double cubeRoot(double volume) {
                                if (volume == 0) return 0;  //@zero
                                double r = volume;  //@start
                                for (int i = 0; i < 100; i++) r -= (r * r * r - volume) / (3 * r * r);  //@iterate
                                return r;  //@ret
                            }
                        };
                    """,
                    "c": """
                        double cubeRoot(double volume) {
                            if (volume == 0) return 0;  //@zero
                            double r = volume;  //@start
                            for (int i = 0; i < 100; i++) r -= (r * r * r - volume) / (3 * r * r);  //@iterate
                            return r;  //@ret
                        }
                    """,
                },
                lines=[("zero", "Newton divides by 3r², so the root 0 is handled up front."), ("start", "Start at v itself: it has the right sign, and the iteration moves towards the root from there."), ("iterate", "Slide along the tangent of r³ − v to where it hits zero. Far from the root each step shrinks r by about a third; close to it, the correct digits double each step. 100 steps is plenty for |v| ≤ 10⁹."), ("ret", "The converged root.")],
                complexity=["**Time:** a handful of steps once close; up to ~60 to get close from v = 10⁹ (each step shrinks r by ~2/3 there). **Space O(1).**"],
                limits=["Fast, but its behaviour depends on the starting point and on dividing by r², which is fragile near 0 (for tiny |v|, intermediate values blow up before settling). Bisection is slower per digit but always safe and needs no derivative."],
            ),
            approach(
                "Bisection on the real line",
                "best",
                "O(log(range / ε))",
                "O(1)",
                idea=["Keep `[lo, hi] = [−max(1, |v|), max(1, |v|)]`. Repeat 200 times: `mid = (lo + hi) / 2`; if `mid³ < v`, `lo = mid`, else `hi = mid`. Return the midpoint."],
                walk=w2,
                build=["Bracket the root with `±max(1, |v|)`.", "Halve the bracket a fixed number of times by comparing `mid³` with v.", "Return `(lo + hi) / 2`."],
                code={
                    "python": """
                        class Solution:
                            def cubeRoot(self, volume: float) -> float:
                                bound = max(1.0, abs(volume))  #@bracket
                                lo, hi = -bound, bound  #@bracket
                                for _ in range(200):  #@halve
                                    mid = (lo + hi) / 2  #@halve
                                    if mid * mid * mid < volume:  #@halve
                                        lo = mid  #@halve
                                    else:  #@halve
                                        hi = mid  #@halve
                                return (lo + hi) / 2  #@ret
                    """,
                    "java": """
                        class Solution {
                            public double cubeRoot(double volume) {
                                double bound = Math.max(1.0, Math.abs(volume));  //@bracket
                                double lo = -bound, hi = bound;  //@bracket
                                for (int i = 0; i < 200; i++) {  //@halve
                                    double mid = (lo + hi) / 2;  //@halve
                                    if (mid * mid * mid < volume) lo = mid; else hi = mid;  //@halve
                                }
                                return (lo + hi) / 2;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            double cubeRoot(double volume) {
                                double bound = max(1.0, fabs(volume));  //@bracket
                                double lo = -bound, hi = bound;  //@bracket
                                for (int i = 0; i < 200; i++) {  //@halve
                                    double mid = (lo + hi) / 2;  //@halve
                                    if (mid * mid * mid < volume) lo = mid; else hi = mid;  //@halve
                                }
                                return (lo + hi) / 2;  //@ret
                            }
                        };
                    """,
                    "c": """
                        double cubeRoot(double volume) {
                            double bound = fabs(volume) > 1.0 ? fabs(volume) : 1.0;  //@bracket
                            double lo = -bound, hi = bound;  //@bracket
                            for (int i = 0; i < 200; i++) {  //@halve
                                double mid = (lo + hi) / 2;  //@halve
                                if (mid * mid * mid < volume) lo = mid; else hi = mid;  //@halve
                            }
                            return (lo + hi) / 2;  //@ret
                        }
                    """,
                },
                lines=[("bracket", "An interval guaranteed to contain the root, for any sign and size of v (`fabs` is plain absolute value, not a root function)."), ("halve", "x³ is increasing, so comparing `mid³` with v tells which half holds the root. A fixed number of rounds avoids fiddly tolerance tests; 200 halvings is far more than double precision needs."), ("ret", "The midpoint of a vanishingly small interval.")],
                complexity=["**Time O(log(range / ε))**: here a fixed 200 iterations. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Binary search on reals:** keep a bracket `[lo, hi]` around the answer of a monotonic condition, halve it a
              fixed number of times (60–100+) instead of testing a tolerance.
            - Choose the starting bracket carefully: for |v| < 1 the root lies outside [−|v|, |v|].
            - Newton's method converges faster near the root but needs a derivative and care near zero.
            """
        ],
    )


@problem
def rope_pieces():
    ropes, pieces = [8, 5, 13], 7
    best = max(r / m for r in ropes for m in range(1, pieces + 1) if sum(math.floor(x * m / r) for x in ropes) >= pieces)
    want = best

    w1 = Steps("The best length is always some rope cut evenly into m pieces: rope / m. Try every such candidate and keep the largest that works.")
    shown = 0
    for r in ropes:
        for m in range(1, 4):
            L = r / m
            cnt = sum(math.floor(x * m / r) for x in ropes)
            if shown < 9:
                w1.step(f"{r} / {m} = {f6(L)}: pieces = " + " + ".join(str(math.floor(x * m / r)) for x in ropes) + f" = {cnt}" + (f" ≥ {pieces} ✓" if cnt >= pieces else f" < {pieces}") + ".", Row(ropes, slots=True), Vars(length=f6(L), pieces=cnt))
                shown += 1
    w1.step(f"The largest candidate that yields at least {pieces} pieces is {f6(want)}.", Row(ropes, slots=True), result=f6(want))

    w2 = Steps("Binary-search the length: a length L works if Σ floor(rope / L) ≥ pieces. Longer lengths give fewer pieces.")
    lo, hi = 0.0, float(max(ropes))
    for i in range(12):
        mid = (lo + hi) / 2
        cnt = sum(int(r / mid) for r in ropes)
        ok = cnt >= pieces
        w2.step(f"[{f6(lo)}, {f6(hi)}], L = {f6(mid)}: " + " + ".join(str(int(r / mid)) for r in ropes) + f" = {cnt} pieces → " + ("enough: try longer." if ok else "too few: shorter."), Row(ropes, slots=True), Vars(lo=f6(lo), hi=f6(hi), L=f6(mid)))
        if ok:
            lo = mid
        else:
            hi = mid
    w2.step(f"After ~100 halvings, L ≈ {f6(want)}.", Row(ropes, slots=True), result=f6(want))

    sol(
        "rope-pieces",
        summary="""
            "Can every piece be L long?" is easy to check: Σ ⌊rope / L⌋ ≥ pieces. Longer pieces only make the count go
            down, so the feasible lengths form an interval [0, L*], and binary search on the real number L finds its end.
            O(n · log(range / ε)).
        """,
        question=[
            """
            Cut the ropes (no joining) into at least `pieces` pieces of equal length L; leftovers are discarded. Return the
            largest possible L, within 10⁻⁶.

            - **Pieces can't be glued:** a 5 m and a 3 m rope can't make one 8 m piece.
            - **L can be a fraction:** one 5 m rope and 2 pieces → 2.5.
            - **"At least" `pieces`:** extra pieces are fine.
            - **Sizes:** up to 10⁴ ropes of up to 10⁷, and up to 10⁶ pieces.
            """
        ],
        think=[
            f"""
            Take ropes `{ropes}` and {pieces} pieces. For a candidate length L, each rope gives ⌊rope / L⌋ pieces. At L = 3:
            2 + 1 + 4 = 7 pieces, enough. At L = 4: 2 + 1 + 3 = 6, not enough. The answer is between 3 and 4.
            """,
            fig(Row(ropes, label="ropes", slots=True), Row(["L=3 → 7", "L=4 → 6"], label="pieces at L"), caption="Longer pieces → fewer pieces. The answer is where the count drops below the target."),
            f"""
            The count never increases as L grows, so "L works" is true up to some L* and false after: binary search on L.
            Searching real numbers, we stop after a fixed number of halvings rather than at an exact value. (The exact
            optimum here is {f6(want)}: the largest L of the form rope/m that still gives {pieces} pieces.)
            """,
        ],
        approaches=[
            approach(
                "Try every rope ÷ m candidate",
                "brute",
                "O(n² · pieces)",
                "O(1)",
                idea=[
                    """
                    At the optimum, some rope is cut with no leftover (otherwise every piece could be made a little longer).
                    So the answer is `ropes[i] / m` for some rope i and some m ≤ pieces. Check each candidate exactly with
                    integers: rope j gives `⌊ropes[j] · m / ropes[i]⌋` pieces. Keep the largest candidate that works.
                    """
                ],
                walk=w1,
                build=["For each rope i and each m in 1 … pieces: count Σⱼ `ropes[j] · m // ropes[i]` (64-bit).", "If the count ≥ pieces, the candidate `ropes[i] / m` is feasible; keep the largest.", "Return it."],
                code={
                    "python": """
                        class Solution:
                            def longestPiece(self, ropes: List[int], pieces: int) -> float:
                                best = 0.0  #@init
                                for r in ropes:  #@cand
                                    for m in range(1, pieces + 1):  #@cand
                                        count = sum(x * m // r for x in ropes)  #@count
                                        if count >= pieces:  #@keep
                                            best = max(best, r / m)  #@keep
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public double longestPiece(int[] ropes, int pieces) {
                                double best = 0;  //@init
                                for (int r : ropes) {  //@cand
                                    for (int m = 1; m <= pieces; m++) {  //@cand
                                        long count = 0;  //@count
                                        for (int x : ropes) count += (long) x * m / r;  //@count
                                        if (count >= pieces) best = Math.max(best, (double) r / m);  //@keep
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            double longestPiece(vector<int>& ropes, int pieces) {
                                double best = 0;  //@init
                                for (int r : ropes) {  //@cand
                                    for (int m = 1; m <= pieces; m++) {  //@cand
                                        long long count = 0;  //@count
                                        for (int x : ropes) count += (long long) x * m / r;  //@count
                                        if (count >= pieces) best = max(best, (double) r / m);  //@keep
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        double longestPiece(int* ropes, int ropesSize, int pieces) {
                            double best = 0;  //@init
                            for (int i = 0; i < ropesSize; i++) {  //@cand
                                for (int m = 1; m <= pieces; m++) {  //@cand
                                    long long count = 0;  //@count
                                    for (int j = 0; j < ropesSize; j++) count += (long long) ropes[j] * m / ropes[i];  //@count
                                    if (count >= pieces && (double) ropes[i] / m > best) best = (double) ropes[i] / m;  //@keep
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Nothing feasible yet."), ("cand", "Every candidate length: some rope split into exactly m equal parts."), ("count", "Pieces at length r / m, computed exactly: x ÷ (r / m) = x · m / r, floored with integer division. 64-bit because x · m reaches 10¹³."), ("keep", "Feasible candidates compete for the largest length."), ("ret", "The best feasible length.")],
                complexity=["**Time O(n² · pieces):** astronomically large at full size (10⁴ · 10⁶ · 10⁴). **Space O(1).**"],
                limits=["It enumerates up to 10¹⁰ candidates, each checked in O(n). Feasibility is monotonic in L, so only ~100 well-chosen candidates are needed: binary search."],
                slow=40,
            ),
            approach(
                "Binary search on the length",
                "best",
                "O(n log(range / ε))",
                "O(1)",
                idea=["`lo = 0`, `hi = max(ropes)` (no piece can be longer than the longest rope). Repeat 100 times: `mid = (lo + hi) / 2`; if Σ ⌊rope / mid⌋ ≥ pieces, `lo = mid` (feasible, try longer), else `hi = mid`. Return `lo`."],
                walk=w2,
                build=["Bracket `[0, max(ropes)]`.", "Count pieces at the midpoint (64-bit).", "Feasible → raise lo; else lower hi. 100 rounds.", "Return lo (always feasible)."],
                code={
                    "python": """
                        class Solution:
                            def longestPiece(self, ropes: List[int], pieces: int) -> float:
                                lo, hi = 0.0, float(max(ropes))  #@bracket
                                for _ in range(100):  #@halve
                                    mid = (lo + hi) / 2  #@halve
                                    if sum(int(r / mid) for r in ropes) >= pieces:  #@test
                                        lo = mid  #@test
                                    else:  #@test
                                        hi = mid  #@test
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public double longestPiece(int[] ropes, int pieces) {
                                double lo = 0, hi = 0;  //@bracket
                                for (int r : ropes) hi = Math.max(hi, r);  //@bracket
                                for (int it = 0; it < 100; it++) {  //@halve
                                    double mid = (lo + hi) / 2;  //@halve
                                    long count = 0;  //@test
                                    for (int r : ropes) count += (long) (r / mid);  //@test
                                    if (count >= pieces) lo = mid; else hi = mid;  //@test
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            double longestPiece(vector<int>& ropes, int pieces) {
                                double lo = 0, hi = *max_element(ropes.begin(), ropes.end());  //@bracket
                                for (int it = 0; it < 100; it++) {  //@halve
                                    double mid = (lo + hi) / 2;  //@halve
                                    long long count = 0;  //@test
                                    for (int r : ropes) count += (long long) (r / mid);  //@test
                                    if (count >= pieces) lo = mid; else hi = mid;  //@test
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        double longestPiece(int* ropes, int ropesSize, int pieces) {
                            double lo = 0, hi = 0;  //@bracket
                            for (int i = 0; i < ropesSize; i++) if (ropes[i] > hi) hi = ropes[i];  //@bracket
                            for (int it = 0; it < 100; it++) {  //@halve
                                double mid = (lo + hi) / 2;  //@halve
                                long long count = 0;  //@test
                                for (int i = 0; i < ropesSize; i++) count += (long long) (ropes[i] / mid);  //@test
                                if (count >= pieces) lo = mid; else hi = mid;  //@test
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("bracket", "The answer is between 0 and the longest rope."), ("halve", "100 halvings of [0, 10⁷] leave an interval far below 10⁻⁶."), ("test", "Pieces available at length mid; truncating each rope's quotient is the floor. A count can be huge for tiny mid (10⁴ ropes × 10⁷ / tiny), so use 64 bits. mid is never 0 here because lo starts at 0 and hi > 0."), ("ret", "`lo` only ever moves to feasible lengths, so it's always a valid answer.")],
                complexity=["**Time O(n · 100).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Maximise a value subject to a monotonic feasibility check** → binary search on the value. With real
              numbers, iterate a fixed number of times.
            - Return the side of the bracket that's always feasible (`lo` here).
            - The exact optimum is always a "tight" configuration (some rope cut with no waste), which is what makes the
              brute-force candidate list finite.
            """
        ],
    )


@problem
def charging_stations():
    st, extra = [0, 4, 15, 21], 4
    gaps = [b - a for a, b in zip(st, st[1:])]

    def need(d):
        return sum(math.ceil(g / d) - 1 for g in gaps)

    lo, hi = 0.0, float(max(gaps))
    for _ in range(100):
        mid = (lo + hi) / 2
        if mid > 0 and need(mid) <= extra:
            hi = mid
        else:
            lo = mid
    want = hi

    w1 = Steps("Greedy: always place the next station in the gap whose current pieces are longest; recompute that by scanning all gaps.")
    add = [0] * len(gaps)
    w1.step(f"Gaps: {gaps}. Every new station goes into the gap with the longest current piece.", Row(gaps, label="gap", slots=True), Row([f6(g) for g in gaps], label="current piece"))
    for t in range(extra):
        i = max(range(len(gaps)), key=lambda q: gaps[q] / (add[q] + 1))
        add[i] += 1
        w1.step(f"Station {t + 1} → gap {i} ({gaps[i]}), now split into {add[i] + 1} pieces of {f6(gaps[i] / (add[i] + 1))}.", Row(gaps, st={i: "active"}, label="gap", slots=True), Row([f6(g / (a + 1)) for g, a in zip(gaps, add)], label="current piece"))
    w1.step(f"Largest piece now: {f6(max(g / (a + 1) for g, a in zip(gaps, add)))}.", Row([f6(g / (a + 1)) for g, a in zip(gaps, add)], label="current piece"), result=f6(want))

    w3 = Steps("Binary-search the answer D: stations needed = Σ (ceil(gap / D) − 1). D is achievable if that's ≤ extra.")
    lo, hi = 0.0, float(max(gaps))
    for i in range(12):
        mid = (lo + hi) / 2
        nd = need(mid)
        ok = nd <= extra
        w3.step(f"[{f6(lo)}, {f6(hi)}], D = {f6(mid)}: needs " + " + ".join(str(math.ceil(g / mid) - 1) for g in gaps) + f" = {nd} station{'s' if nd != 1 else ''} → " + ("affordable: try smaller." if ok else "too many: larger."), Row(gaps, label="gap", slots=True), Vars(lo=f6(lo), hi=f6(hi), D=f6(mid)))
        if ok:
            hi = mid
        else:
            lo = mid
    w3.step(f"Converges to {f6(want)}.", Row(gaps, label="gap", slots=True), result=f6(want))

    sol(
        "charging-stations",
        summary="""
            Fix a target maximum gap D. Splitting a gap g so no piece exceeds D takes `⌈g / D⌉ − 1` new stations, and the
            total needed only goes down as D grows. So binary-search the real number D: the answer is the smallest D whose
            total need is at most `extra`. O(n · log(range / ε)), independent of how many stations you may add.
        """,
        question=[
            """
            Stations are at sorted integer positions. Add `extra` stations anywhere (fractional positions allowed) to make
            the **largest gap between neighbours** as small as possible; return that gap within 10⁻⁶.

            - **Only gaps matter**, not absolute positions.
            - **New stations within a gap are best spread evenly:** k stations split a gap g into k + 1 pieces of g/(k+1).
            - **extra can be 10⁶**, so placing stations one at a time can be slow.
            """
        ],
        think=[
            f"""
            Take stations `{st}` (gaps `{gaps}`) and {extra} extra stations. The longest gap is {max(gaps)}. Putting one
            station in its middle halves it to {max(gaps) / 2}; now the gap of {sorted(gaps)[-2]} might be the longest, and
            so on.
            """,
            fig(Row(gaps, label="gaps", slots=True), caption="k stations inside a gap g leave pieces of g / (k + 1)."),
            """
            Flip the question: **for a given maximum D, how many stations are needed?** Gap g needs pieces of length ≤ D,
            i.e. at least ⌈g / D⌉ pieces, which takes ⌈g / D⌉ − 1 stations. Summing over gaps gives the total, and a
            larger D never needs more stations. So "D is achievable with `extra` stations" is monotonic: false for tiny D,
            true from the answer upward. Binary search on D finds the boundary.
            """,
        ],
        approaches=[
            approach(
                "Place stations one by one (scan for the worst gap)",
                "brute",
                "O(extra · n)",
                "O(n)",
                idea=["Track how many stations each gap has received. Each time, scan all gaps for the one with the longest current piece `gap / (added + 1)`, and add a station there. After all stations, return the longest piece. (Adding to the worst gap is always optimal: no other choice can reduce the maximum.)"],
                walk=w1,
                build=["`added[i] = 0` for each gap.", "Repeat `extra` times: find the gap with the largest `gap / (added + 1)` and increment its count.", "Return the largest `gap / (added + 1)`."],
                code={
                    "python": """
                        class Solution:
                            def smallestMaxGap(self, stations: List[int], extra: int) -> float:
                                gaps = [b - a for a, b in zip(stations, stations[1:])]  #@gaps
                                added = [0] * len(gaps)  #@gaps
                                for _ in range(extra):  #@place
                                    i = max(range(len(gaps)), key=lambda q: gaps[q] / (added[q] + 1))  #@place
                                    added[i] += 1  #@place
                                return max(g / (a + 1) for g, a in zip(gaps, added))  #@ret
                    """,
                    "java": """
                        class Solution {
                            public double smallestMaxGap(int[] stations, int extra) {
                                int m = stations.length - 1;
                                int[] added = new int[m];  //@gaps
                                for (int t = 0; t < extra; t++) {  //@place
                                    int best = 0;  //@place
                                    for (int i = 1; i < m; i++) {  //@place
                                        double cur = (double) (stations[i + 1] - stations[i]) / (added[i] + 1);  //@place
                                        if (cur > (double) (stations[best + 1] - stations[best]) / (added[best] + 1)) best = i;  //@place
                                    }  //@place
                                    added[best]++;  //@place
                                }
                                double worst = 0;  //@ret
                                for (int i = 0; i < m; i++) worst = Math.max(worst, (double) (stations[i + 1] - stations[i]) / (added[i] + 1));  //@ret
                                return worst;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            double smallestMaxGap(vector<int>& stations, int extra) {
                                int m = stations.size() - 1;
                                vector<int> added(m, 0);  //@gaps
                                auto piece = [&](int i) { return (double) (stations[i + 1] - stations[i]) / (added[i] + 1); };  //@gaps
                                for (int t = 0; t < extra; t++) {  //@place
                                    int best = 0;  //@place
                                    for (int i = 1; i < m; i++) if (piece(i) > piece(best)) best = i;  //@place
                                    added[best]++;  //@place
                                }
                                double worst = 0;  //@ret
                                for (int i = 0; i < m; i++) worst = max(worst, piece(i));  //@ret
                                return worst;  //@ret
                            }
                        };
                    """,
                    "c": """
                        double smallestMaxGap(int* stations, int stationsSize, int extra) {
                            int m = stationsSize - 1;
                            int* added = calloc(m, sizeof(int));  //@gaps
                            for (int t = 0; t < extra; t++) {  //@place
                                int best = 0;  //@place
                                for (int i = 1; i < m; i++) {  //@place
                                    double cur = (double) (stations[i + 1] - stations[i]) / (added[i] + 1);  //@place
                                    if (cur > (double) (stations[best + 1] - stations[best]) / (added[best] + 1)) best = i;  //@place
                                }  //@place
                                added[best]++;  //@place
                            }
                            double worst = 0;  //@ret
                            for (int i = 0; i < m; i++) {  //@ret
                                double cur = (double) (stations[i + 1] - stations[i]) / (added[i] + 1);  //@ret
                                if (cur > worst) worst = cur;  //@ret
                            }  //@ret
                            free(added);  //@ret
                            return worst;  //@ret
                        }
                    """,
                },
                lines=[("gaps", "Each gap and the number of stations added inside it so far (spread evenly, so pieces are gap / (added + 1))."), ("place", "Find the gap whose pieces are currently longest and give it one more station. That's the only move that can lower the overall maximum."), ("ret", "The longest piece after all stations are placed.")],
                complexity=["**Time O(extra · n):** up to 10⁶ × 2000 = 2 × 10⁹. **Space O(n).**"],
                limits=["One full scan per station. A max-heap of gaps would make each placement O(log n), but the work still grows with `extra` (10⁶). Binary search on the answer doesn't depend on `extra` at all."],
                slow=True,
            ),
            approach(
                "Binary search on the maximum gap",
                "best",
                "O(n log(range / ε))",
                "O(n)",
                idea=["`lo = 0`, `hi = largest gap`. Repeat 100 times: `mid = (lo + hi) / 2`; `need = Σ (⌈gap / mid⌉ − 1)`; if `need ≤ extra`, mid is achievable (`hi = mid`), else `lo = mid`. Return `hi`."],
                walk=w3,
                build=["Bracket `[0, max gap]` (with no extra stations the max gap is achievable).", "For mid: stations needed = Σ ⌈gap / mid⌉ − 1.", "Achievable → `hi = mid`; else `lo = mid`. 100 rounds.", "Return `hi` (always achievable)."],
                code={
                    "python": """
                        import math

                        class Solution:
                            def smallestMaxGap(self, stations: List[int], extra: int) -> float:
                                gaps = [b - a for a, b in zip(stations, stations[1:])]  #@bracket
                                lo, hi = 0.0, float(max(gaps))  #@bracket
                                for _ in range(100):  #@halve
                                    mid = (lo + hi) / 2  #@halve
                                    need = sum(math.ceil(g / mid) - 1 for g in gaps)  #@need
                                    if need <= extra:  #@move
                                        hi = mid  #@move
                                    else:  #@move
                                        lo = mid  #@move
                                return hi  #@ret
                    """,
                    "java": """
                        class Solution {
                            public double smallestMaxGap(int[] stations, int extra) {
                                double lo = 0, hi = 0;  //@bracket
                                for (int i = 0; i + 1 < stations.length; i++) hi = Math.max(hi, stations[i + 1] - stations[i]);  //@bracket
                                for (int it = 0; it < 100; it++) {  //@halve
                                    double mid = (lo + hi) / 2;  //@halve
                                    long need = 0;  //@need
                                    for (int i = 0; i + 1 < stations.length; i++) need += (long) Math.ceil((stations[i + 1] - stations[i]) / mid) - 1;  //@need
                                    if (need <= extra) hi = mid; else lo = mid;  //@move
                                }
                                return hi;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            double smallestMaxGap(vector<int>& stations, int extra) {
                                double lo = 0, hi = 0;  //@bracket
                                for (size_t i = 0; i + 1 < stations.size(); i++) hi = max(hi, (double) (stations[i + 1] - stations[i]));  //@bracket
                                for (int it = 0; it < 100; it++) {  //@halve
                                    double mid = (lo + hi) / 2;  //@halve
                                    long long need = 0;  //@need
                                    for (size_t i = 0; i + 1 < stations.size(); i++) need += (long long) ceil((stations[i + 1] - stations[i]) / mid) - 1;  //@need
                                    if (need <= extra) hi = mid; else lo = mid;  //@move
                                }
                                return hi;  //@ret
                            }
                        };
                    """,
                    "c": """
                        double smallestMaxGap(int* stations, int stationsSize, int extra) {
                            double lo = 0, hi = 0;  //@bracket
                            for (int i = 0; i + 1 < stationsSize; i++) if (stations[i + 1] - stations[i] > hi) hi = stations[i + 1] - stations[i];  //@bracket
                            for (int it = 0; it < 100; it++) {  //@halve
                                double mid = (lo + hi) / 2;  //@halve
                                long long need = 0;  //@need
                                for (int i = 0; i + 1 < stationsSize; i++) need += (long long) ceil((stations[i + 1] - stations[i]) / mid) - 1;  //@need
                                if (need <= extra) hi = mid; else lo = mid;  //@move
                            }
                            return hi;  //@ret
                        }
                    """,
                },
                lines=[("bracket", "The answer is between 0 and the current largest gap (adding nothing already achieves that)."), ("halve", "100 halvings of [0, 10⁸] reach far below 10⁻⁶."), ("need", "Stations needed so no piece exceeds mid: gap g needs ⌈g / mid⌉ pieces. Totals can be huge for tiny mid, hence 64-bit. mid is never 0, since hi starts positive and the midpoint of a positive interval is positive."), ("move", "Affordable → the true answer is ≤ mid. Too many → it's > mid."), ("ret", "`hi` is always achievable.")],
                complexity=["**Time O(n · 100).** **Space O(1)** (the Python version builds the gap list: O(n))."],
            ),
        ],
        takeaways=[
            """
            - **Minimise the maximum** problems often invert well: fix the maximum D, compute the cost to achieve it, and
              binary-search D.
            - Cost for a gap: `⌈g / D⌉ − 1` cuts. Monotonic in D, which is all binary search needs.
            - Greedy placement is correct but scales with the number of items placed; searching on the answer doesn't.
            """
        ],
    )
