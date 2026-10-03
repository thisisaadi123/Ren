"""Two Pointers: k-sum (fix one value, two pointers for the rest)."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

C_CMP = """
                        static int cmp_int(const void* x, const void* y) {  //@sort
                            int a = *(const int*) x, b = *(const int*) y;  //@sort
                            return (a > b) - (a < b);  //@sort
                        }  //@sort
""".strip("\n")


@problem
def three_weights():
    weights, target = [12, 3, 7, 1, 9, 20], 28
    a = sorted(weights)
    trip = None
    for i in range(len(a) - 2):
        j, k = i + 1, len(a) - 1
        while j < k:
            s = a[i] + a[j] + a[k]
            if s == target:
                trip = (a[i], a[j], a[k]); break
            j, k = (j + 1, k) if s < target else (j, k - 1)
        if trip:
            break
    want = trip is not None

    w1 = Steps("Try every triple of different positions.")
    count = 0
    n = len(weights)
    found = None
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                count += 1
                if weights[i] + weights[j] + weights[k] == target and not found:
                    found = (i, j, k)
    w1.step(f"{count} triples to check for {n} weights.", Row(weights))
    w1.step(f"Weights {[weights[t] for t in found]} at positions {list(found)} add up to {target}.", Row(weights, st={t: "found" for t in found}), result="true")

    w2 = Steps("Sort. Fix the smallest weight of the triple, then find the other two with pointers from both ends of the rest.")
    w2.step(f"Sorted: {a}.", Row(a))
    for i in range(len(a) - 2):
        j, k = i + 1, len(a) - 1
        while j < k:
            s = a[i] + a[j] + a[k]
            w2.step(f"Fix {a[i]}: {a[i]} + {a[j]} + {a[k]} = {s}" + (" = target!" if s == target else (", too small: move j right." if s < target else ", too big: move k left.")), Row(a, st={i: "active", j: "mark", k: "mark"}, ptr={"j": j, "k": k}))
            if s == target:
                break
            j, k = (j + 1, k) if s < target else (j, k - 1)
        else:
            continue
        break
    w2.step("Found a triple.", result="true")

    sol(
        "three-weights",
        summary="""
            Sort the weights. For each choice of the smallest weight `a[i]`, the other two must add up to `target − a[i]`
            among the weights after it, which two pointers from both ends find in linear time. O(n²) overall, O(1) extra
            space.
        """,
        question=[
            """
            Decide whether three weights at different positions add up to exactly `target`.

            - **Different positions**, but equal weights are allowed (two 5-gram weights can both be used).
            - **Up to 500 weights**: O(n³) is about 2 × 10⁷ triples, O(n²) is 2.5 × 10⁵ steps.
            """
        ],
        think=[
            f"""
            Weights `{weights}`, target {target}: {trip[0]} + {trip[1]} + {trip[2]} = {target}, so **true**.

            Three unknowns are hard; two are easy. Fix the first weight, and the problem becomes "find two weights with sum
            `target − first`", which in a sorted list is the two-pointer squeeze. To avoid counting the same weight twice,
            only search to the right of the fixed one.
            """,
            fig(Row(weights, label="weights"), Row(a, label="sorted")),
        ],
        approaches=[
            approach(
                "Every triple",
                "brute",
                "O(n³)",
                "O(1)",
                idea=["Three nested loops over `i < j < k`."],
                walk=w1,
                build=["Triple loop.", "Return true on a match."],
                code={
                    "python": """
                        class Solution:
                            def hasTriple(self, weights: List[int], target: int) -> bool:
                                n = len(weights)  #@loops
                                for i in range(n):  #@loops
                                    for j in range(i + 1, n):  #@loops
                                        for k in range(j + 1, n):  #@loops
                                            if weights[i] + weights[j] + weights[k] == target:  #@hit
                                                return True  #@hit
                                return False  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean hasTriple(int[] weights, int target) {
                                int n = weights.length;  //@loops
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++)  //@loops
                                            if (weights[i] + weights[j] + weights[k] == target) return true;  //@hit
                                return false;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool hasTriple(vector<int>& weights, int target) {
                                int n = weights.size();  //@loops
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++)  //@loops
                                            if (weights[i] + weights[j] + weights[k] == target) return true;  //@hit
                                return false;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool hasTriple(int* weights, int weightsSize, int target) {
                            int n = weightsSize;  //@loops
                            for (int i = 0; i < n; i++)  //@loops
                                for (int j = i + 1; j < n; j++)  //@loops
                                    for (int k = j + 1; k < n; k++)  //@loops
                                        if (weights[i] + weights[j] + weights[k] == target) return true;  //@hit
                            return false;  //@ret
                        }
                    """,
                },
                lines=[("loops", "Every triple of positions."), ("hit", "Sums reach 3 × 10⁵, well within 32 bits."), ("ret", "No triple works.")],
                complexity=["**Time O(n³).** **Space O(1).**"],
                limits=["The innermost loop just searches for one value, `target − w[i] − w[j]`. Sorting lets two pointers find the last two weights together in linear time."],
                slow=True,
            ),
            approach(
                "Sort, fix one, squeeze two",
                "best",
                "O(n²)",
                "O(1)",
                idea=["Sort. For each `i`, set `j = i + 1`, `k = n − 1` and squeeze: sum too small → `j++`, too big → `k−−`, equal → true."],
                walk=w2,
                build=["Sort a copy.", "Outer loop fixes `a[i]`.", "Two-pointer search on `a[i+1..]`."],
                code={
                    "python": """
                        class Solution:
                            def hasTriple(self, weights: List[int], target: int) -> bool:
                                a = sorted(weights)  #@sort
                                for i in range(len(a) - 2):  #@fix
                                    j, k = i + 1, len(a) - 1  #@fix
                                    while j < k:  #@squeeze
                                        s = a[i] + a[j] + a[k]  #@squeeze
                                        if s == target:  #@squeeze
                                            return True  #@squeeze
                                        if s < target:  #@squeeze
                                            j += 1  #@squeeze
                                        else:  #@squeeze
                                            k -= 1  #@squeeze
                                return False  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean hasTriple(int[] weights, int target) {
                                int[] a = weights.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                for (int i = 0; i + 2 < a.length; i++) {  //@fix
                                    int j = i + 1, k = a.length - 1;  //@fix
                                    while (j < k) {  //@squeeze
                                        int s = a[i] + a[j] + a[k];  //@squeeze
                                        if (s == target) return true;  //@squeeze
                                        if (s < target) j++; else k--;  //@squeeze
                                    }
                                }
                                return false;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool hasTriple(vector<int>& weights, int target) {
                                vector<int> a = weights;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                for (int i = 0; i + 2 < (int) a.size(); i++) {  //@fix
                                    int j = i + 1, k = (int) a.size() - 1;  //@fix
                                    while (j < k) {  //@squeeze
                                        int s = a[i] + a[j] + a[k];  //@squeeze
                                        if (s == target) return true;  //@squeeze
                                        if (s < target) j++; else k--;  //@squeeze
                                    }
                                }
                                return false;  //@ret
                            }
                        };
                    """,
                    "c": C_CMP + """

                        bool hasTriple(int* weights, int weightsSize, int target) {
                            int n = weightsSize;  //@sort
                            int* a = malloc(n * sizeof(int));  //@sort
                            memcpy(a, weights, n * sizeof(int));  //@sort
                            qsort(a, n, sizeof(int), cmp_int);  //@sort
                            bool found = false;  //@fix
                            for (int i = 0; i + 2 < n && !found; i++) {  //@fix
                                int j = i + 1, k = n - 1;  //@fix
                                while (j < k) {  //@squeeze
                                    int s = a[i] + a[j] + a[k];  //@squeeze
                                    if (s == target) { found = true; break; }  //@squeeze
                                    if (s < target) j++; else k--;  //@squeeze
                                }
                            }
                            free(a);  //@ret
                            return found;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Sort a copy."), ("fix", "The smallest weight of the triple is `a[i]`; the other two come from positions after `i`."), ("squeeze", "Two-pointer search for the remaining pair: too small → raise the low end, too big → lower the high end."), ("ret", "No triple works.")],
                complexity=["**Time O(n²)** (plus the sort). **Space O(n)** for the sorted copy, O(1) besides."],
            ),
        ],
        takeaways=[
            """
            - **3-sum = fix one + 2-sum.** Sorting makes the inner 2-sum a linear squeeze.
            - Only search to the right of the fixed element so each triple is considered once.
            - 4-sum: fix two, squeeze two (O(n³)).
            """
        ],
    )


@problem
def closest_triple_sum():
    values, target = [4, -2, 9, 1, -6, 7], 6
    a = sorted(values)
    n = len(a)
    import itertools
    sums = sorted({x + y + z for x, y, z in itertools.combinations(values, 3)}, key=lambda s: (abs(s - target), s))
    want = sums[0]

    w = Steps("Sort, fix the smallest value, squeeze the other two toward the target, and remember the closest sum seen.")
    w.step(f"Sorted: {a}.", Row(a))
    best = a[0] + a[1] + a[2]
    for i in range(n - 2):
        j, k = i + 1, n - 1
        while j < k:
            s = a[i] + a[j] + a[k]
            if (abs(s - target), s) < (abs(best - target), best):
                best = s
            w.step(f"{a[i]} + {a[j]} + {a[k]} = {s}. Best so far {best}.", Row(a, st={i: "active", j: "mark", k: "mark"}), Vars(best=best))
            if s == target:
                break
            j, k = (j + 1, k) if s < target else (j, k - 1)
        if best == target:
            break
    w.step(f"Closest: {best}.", result=best)

    sol(
        "closest-triple-sum",
        summary="""
            Sort; for each fixed first value, squeeze the other two from both ends of the rest: below the target, move the
            low pointer up; above, move the high pointer down. Track the sum with the smallest distance (smaller sum on
            ties). O(n²).
        """,
        question=[
            """
            Return the sum of three values (different positions) closest to `target`; on a tie, the smaller sum.

            - **Up to 1000 values**: O(n³) is about 1.7 × 10⁸ triples, O(n²) is 5 × 10⁵.
            - Small values (|v| ≤ 1000), so no overflow worries.
            """
        ],
        think=[
            f"""
            Values `{values}`, target {target}: the closest sums are {sums[:3]}…, so **{want}**.

            Same skeleton as 3-sum: fix the smallest value and squeeze the other two. The squeeze doesn't stop early; it
            moves toward the target and records the best sum along the way. The skipped pairs are always farther from the
            target than one already seen.
            """,
            fig(Row(values, label="values"), Row(a, label="sorted")),
        ],
        approaches=[
            approach(
                "Every triple",
                "brute",
                "O(n³)",
                "O(1)",
                idea=["Check every triple, keeping the best by (distance, sum)."],
                build=["Triple loop.", "Compare by distance, then sum."],
                code={
                    "python": """
                        class Solution:
                            def closestTriple(self, values: List[int], target: int) -> int:
                                n, best = len(values), None  #@init
                                for i in range(n):  #@loops
                                    for j in range(i + 1, n):  #@loops
                                        for k in range(j + 1, n):  #@loops
                                            s = values[i] + values[j] + values[k]  #@better
                                            if best is None or (abs(s - target), s) < (abs(best - target), best):  #@better
                                                best = s  #@better
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int closestTriple(int[] values, int target) {
                                int n = values.length, best = values[0] + values[1] + values[2];  //@init
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++) {  //@loops
                                            int s = values[i] + values[j] + values[k];  //@better
                                            int d = Math.abs(s - target), bd = Math.abs(best - target);  //@better
                                            if (d < bd || (d == bd && s < best)) best = s;  //@better
                                        }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int closestTriple(vector<int>& values, int target) {
                                int n = values.size(), best = values[0] + values[1] + values[2];  //@init
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++) {  //@loops
                                            int s = values[i] + values[j] + values[k];  //@better
                                            int d = abs(s - target), bd = abs(best - target);  //@better
                                            if (d < bd || (d == bd && s < best)) best = s;  //@better
                                        }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int closestTriple(int* values, int valuesSize, int target) {
                            int n = valuesSize, best = values[0] + values[1] + values[2];  //@init
                            for (int i = 0; i < n; i++)  //@loops
                                for (int j = i + 1; j < n; j++)  //@loops
                                    for (int k = j + 1; k < n; k++) {  //@loops
                                        int s = values[i] + values[j] + values[k];  //@better
                                        int d = abs(s - target), bd = abs(best - target);  //@better
                                        if (d < bd || (d == bd && s < best)) best = s;  //@better
                                    }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Start from any triple."), ("loops", "Every triple."), ("better", "Closer wins; equally close, the smaller sum."), ("ret", "The closest sum.")],
                complexity=["**Time O(n³).** **Space O(1).**"],
                limits=["~1.7 × 10⁸ triples at n = 1000. Fixing one value and squeezing the other two visits only O(n²) triples without missing the best one."],
                slow=True,
            ),
            approach(
                "Sort, fix one, squeeze toward the target",
                "best",
                "O(n²)",
                "O(1)",
                idea=["Sort. For each `i`, squeeze `j`, `k` over the rest; update the best each time; move `j` up if the sum is below the target, `k` down if above, return immediately on an exact hit."],
                walk=w,
                build=["Sort a copy.", "Fix `a[i]`.", "Squeeze and update the best."],
                code={
                    "python": """
                        class Solution:
                            def closestTriple(self, values: List[int], target: int) -> int:
                                a = sorted(values)  #@sort
                                best = a[0] + a[1] + a[2]  #@sort
                                for i in range(len(a) - 2):  #@fix
                                    j, k = i + 1, len(a) - 1  #@fix
                                    while j < k:  #@squeeze
                                        s = a[i] + a[j] + a[k]  #@squeeze
                                        if (abs(s - target), s) < (abs(best - target), best):  #@better
                                            best = s  #@better
                                        if s < target:  #@move
                                            j += 1  #@move
                                        elif s > target:  #@move
                                            k -= 1  #@move
                                        else:  #@move
                                            return s  #@move
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int closestTriple(int[] values, int target) {
                                int[] a = values.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                int best = a[0] + a[1] + a[2];  //@sort
                                for (int i = 0; i + 2 < a.length; i++) {  //@fix
                                    int j = i + 1, k = a.length - 1;  //@fix
                                    while (j < k) {  //@squeeze
                                        int s = a[i] + a[j] + a[k];  //@squeeze
                                        int d = Math.abs(s - target), bd = Math.abs(best - target);  //@better
                                        if (d < bd || (d == bd && s < best)) best = s;  //@better
                                        if (s < target) j++;  //@move
                                        else if (s > target) k--;  //@move
                                        else return s;  //@move
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int closestTriple(vector<int>& values, int target) {
                                vector<int> a = values;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                int best = a[0] + a[1] + a[2];  //@sort
                                for (int i = 0; i + 2 < (int) a.size(); i++) {  //@fix
                                    int j = i + 1, k = (int) a.size() - 1;  //@fix
                                    while (j < k) {  //@squeeze
                                        int s = a[i] + a[j] + a[k];  //@squeeze
                                        int d = abs(s - target), bd = abs(best - target);  //@better
                                        if (d < bd || (d == bd && s < best)) best = s;  //@better
                                        if (s < target) j++;  //@move
                                        else if (s > target) k--;  //@move
                                        else return s;  //@move
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": C_CMP + """

                        int closestTriple(int* values, int valuesSize, int target) {
                            int n = valuesSize;  //@sort
                            int* a = malloc(n * sizeof(int));  //@sort
                            memcpy(a, values, n * sizeof(int));  //@sort
                            qsort(a, n, sizeof(int), cmp_int);  //@sort
                            int best = a[0] + a[1] + a[2];  //@sort
                            for (int i = 0; i + 2 < n && best != target; i++) {  //@fix
                                int j = i + 1, k = n - 1;  //@fix
                                while (j < k) {  //@squeeze
                                    int s = a[i] + a[j] + a[k];  //@squeeze
                                    int d = abs(s - target), bd = abs(best - target);  //@better
                                    if (d < bd || (d == bd && s < best)) best = s;  //@better
                                    if (s < target) j++;  //@move
                                    else if (s > target) k--;  //@move
                                    else break;  //@move
                                }
                            }
                            free(a);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Sort a copy; any triple is a starting answer."), ("fix", "Fix the smallest of the three."), ("squeeze", "The current triple's sum."), ("better", "Closer wins; equally close, the smaller sum."), ("move", "Move toward the target; an exact hit can't be beaten."), ("ret", "The closest sum.")],
                complexity=["**Time O(n²).** **Space O(n)** for the sorted copy."],
            ),
        ],
        takeaways=[
            """
            - **Closest 3-sum:** the 3-sum skeleton, recording the best instead of stopping at a match.
            - Moving toward the target never skips a closer sum (same argument as 2-sum).
            - Spell out the tie rule in code: `(distance, sum)` comparisons do it neatly.
            """
        ],
    )


@problem
def triples_under_a_cap():
    values, cap = [3, -1, 5, 0, 2, -4], 2
    a = sorted(values)
    n = len(a)
    import itertools
    want = sum(1 for t in itertools.combinations(values, 3) if sum(t) < cap)

    w = Steps("Sort. Fix a[i]. If a[i] + a[j] + a[k] < cap, then every k' between j and k also works with this j: count k − j at once and move j up. Otherwise move k down.")
    w.step(f"Sorted: {a}.", Row(a))
    total = 0
    for i in range(n - 2):
        j, k = i + 1, n - 1
        while j < k:
            s = a[i] + a[j] + a[k]
            if s < cap:
                total += k - j
                w.step(f"{a[i]} + {a[j]} + {a[k]} = {s} < {cap}: all {k - j} choices of the third value between j and k work. +{k - j}.", Row(a, st={i: "active", j: "found", **{t: "found" for t in range(j + 1, k + 1)}}), Vars(count=total))
                j += 1
            else:
                w.step(f"{a[i]} + {a[j]} + {a[k]} = {s} ≥ {cap}: lower k.", Row(a, st={i: "active", j: "mark", k: "mark"}), Vars(count=total))
                k -= 1
    w.step(f"Total: {total}.", result=total)

    sol(
        "triples-under-a-cap",
        summary="""
            Sort; fix the smallest value `a[i]` and squeeze `j`, `k` over the rest. When `a[i] + a[j] + a[k] < cap`, every
            third value between `j` and `k` also works (they're smaller than `a[k]`), so add `k − j` in one go and move `j`.
            Otherwise move `k` down. O(n²), counting in 64 bits.
        """,
        question=[
            """
            Count triples of positions `i < j < k` whose values sum to **less than** `cap`.

            - Positions, not values, are counted: equal values at different positions count separately.
            - **Up to 2000 values**: about 1.3 × 10⁹ triples, so the count needs 64 bits and the method must beat O(n³).
            """
        ],
        think=[
            f"""
            `{values}`, cap {cap}: **{want}** triples have a smaller sum.

            Sorting doesn't change which sets of positions qualify, just their order, so sort freely. Then, with `a[i]` and
            `a[j]` fixed, the valid third values form a prefix (everything up to some `k`): count it in one step.
            """,
            fig(Row(values, label="values"), Row(a, label="sorted")),
        ],
        approaches=[
            approach(
                "Every triple",
                "brute",
                "O(n³)",
                "O(1)",
                idea=["Count every `i < j < k` with sum below the cap."],
                build=["Triple loop.", "64-bit count."],
                code={
                    "python": """
                        class Solution:
                            def countTriplesBelow(self, values: List[int], cap: int) -> int:
                                n, count = len(values), 0  #@init
                                for i in range(n):  #@loops
                                    for j in range(i + 1, n):  #@loops
                                        for k in range(j + 1, n):  #@loops
                                            if values[i] + values[j] + values[k] < cap:  #@loops
                                                count += 1  #@loops
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countTriplesBelow(int[] values, int cap) {
                                int n = values.length;  //@init
                                long count = 0;  //@init
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++)  //@loops
                                            if (values[i] + values[j] + values[k] < cap) count++;  //@loops
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countTriplesBelow(vector<int>& values, int cap) {
                                int n = values.size();  //@init
                                long long count = 0;  //@init
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++)  //@loops
                                            if (values[i] + values[j] + values[k] < cap) count++;  //@loops
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countTriplesBelow(int* values, int valuesSize, int cap) {
                            int n = valuesSize;  //@init
                            long long count = 0;  //@init
                            for (int i = 0; i < n; i++)  //@loops
                                for (int j = i + 1; j < n; j++)  //@loops
                                    for (int k = j + 1; k < n; k++)  //@loops
                                        if (values[i] + values[j] + values[k] < cap) count++;  //@loops
                            return count;  //@ret
                        }
                    """,
                },
                lines=[("init", "A 64-bit count."), ("loops", "Every triple of positions."), ("ret", "Total.")],
                complexity=["**Time O(n³).** **Space O(1).**"],
                limits=["Visits each valid triple one at a time. After sorting, the valid third values form a contiguous range that can be counted in O(1)."],
                slow=True,
            ),
            approach(
                "Sort, fix one, count ranges",
                "best",
                "O(n²)",
                "O(1)",
                idea=["Sort. For each `i`: `j = i + 1`, `k = n − 1`; if the sum is below the cap, add `k − j` and `j++`; else `k−−`."],
                walk=w,
                build=["Sort.", "Fix `a[i]`.", "Count whole ranges with the squeeze."],
                code={
                    "python": """
                        class Solution:
                            def countTriplesBelow(self, values: List[int], cap: int) -> int:
                                a, total = sorted(values), 0  #@sort
                                for i in range(len(a) - 2):  #@fix
                                    j, k = i + 1, len(a) - 1  #@fix
                                    while j < k:  #@squeeze
                                        if a[i] + a[j] + a[k] < cap:  #@count
                                            total += k - j  #@count
                                            j += 1  #@count
                                        else:  #@squeeze
                                            k -= 1  #@squeeze
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countTriplesBelow(int[] values, int cap) {
                                int[] a = values.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                long total = 0;  //@sort
                                for (int i = 0; i + 2 < a.length; i++) {  //@fix
                                    int j = i + 1, k = a.length - 1;  //@fix
                                    while (j < k) {  //@squeeze
                                        if (a[i] + a[j] + a[k] < cap) { total += k - j; j++; }  //@count
                                        else k--;  //@squeeze
                                    }
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countTriplesBelow(vector<int>& values, int cap) {
                                vector<int> a = values;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                long long total = 0;  //@sort
                                for (int i = 0; i + 2 < (int) a.size(); i++) {  //@fix
                                    int j = i + 1, k = (int) a.size() - 1;  //@fix
                                    while (j < k) {  //@squeeze
                                        if (a[i] + a[j] + a[k] < cap) { total += k - j; j++; }  //@count
                                        else k--;  //@squeeze
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": C_CMP + """

                        long long countTriplesBelow(int* values, int valuesSize, int cap) {
                            int n = valuesSize;  //@sort
                            int* a = malloc(n * sizeof(int));  //@sort
                            memcpy(a, values, n * sizeof(int));  //@sort
                            qsort(a, n, sizeof(int), cmp_int);  //@sort
                            long long total = 0;  //@sort
                            for (int i = 0; i + 2 < n; i++) {  //@fix
                                int j = i + 1, k = n - 1;  //@fix
                                while (j < k) {  //@squeeze
                                    if (a[i] + a[j] + a[k] < cap) { total += k - j; j++; }  //@count
                                    else k--;  //@squeeze
                                }
                            }
                            free(a);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Sort a copy (the set of qualifying position-triples doesn't change); a 64-bit total."), ("fix", "Fix the smallest of the three."), ("squeeze", "Sum too big: the largest candidate `a[k]` can't work with this `j` or any bigger one: drop it."), ("count", "Sum small enough: `a[j]` works with every third value in `j+1..k`, `k − j` of them. Then try the next `j`."), ("ret", "Total.")],
                complexity=["**Time O(n²).** **Space O(n)** for the sorted copy."],
            ),
        ],
        takeaways=[
            """
            - **Counting k-sum under a bound:** when the squeeze condition holds, a whole range qualifies: add `k − j`.
            - Sorting is safe when the question is about sets of positions, not their order.
            - Counts of triples can exceed 32 bits.
            """
        ],
    )


@problem
def triples_in_a_band():
    values, low, high = [4, -3, 1, 6, -1, 2], 0, 5
    a = sorted(values)
    import itertools
    want = sum(1 for t in itertools.combinations(values, 3) if low <= sum(t) <= high)

    def at_most(x):
        total = 0
        for i in range(len(a) - 2):
            j, k = i + 1, len(a) - 1
            while j < k:
                if a[i] + a[j] + a[k] <= x:
                    total += k - j; j += 1
                else:
                    k -= 1
        return total

    hi_c, lo_c = at_most(high), at_most(low - 1)
    w = Steps("Count triples with sum ≤ high, count those with sum ≤ low − 1, and subtract: what's left lies in the band.")
    w.step(f"Sorted: {a}.", Row(a))
    w.step(f"Triples with sum ≤ {high}: {hi_c} (counted with the fix-one squeeze).", Row(a), Vars(at_most_high=hi_c))
    w.step(f"Triples with sum ≤ {low - 1}: {lo_c}.", Row(a), Vars(at_most_high=hi_c, at_most_low_minus_1=lo_c))
    w.step(f"In the band [{low}, {high}]: {hi_c} − {lo_c} = {hi_c - lo_c}.", result=hi_c - lo_c)

    sol(
        "triples-in-a-band",
        summary="""
            Counting sums inside `[low, high]` directly is awkward, but counting sums `≤ x` is easy with the sorted
            fix-one squeeze. So compute `count(≤ high) − count(≤ low − 1)`. O(n²), with 64-bit counts.
        """,
        question=[
            """
            Count triples of positions `i < j < k` whose sum lies between `low` and `high`, inclusive.

            - **Up to 1500 values** in ±10⁶; sums fit in 32 bits, counts need 64.
            - Equal values at different positions count separately.
            """
        ],
        think=[
            f"""
            `{values}`, band [{low}, {high}]: **{want}** triples.

            A two-sided condition is two one-sided conditions: "sum ≤ high" minus "sum < low". The one-sided count is the
            triples-under-a-cap technique (with `≤`), run twice.
            """,
            fig(Row(values, label="values"), Row(a, label="sorted")),
        ],
        approaches=[
            approach(
                "Every triple",
                "brute",
                "O(n³)",
                "O(1)",
                idea=["Count triples whose sum is in the band."],
                build=["Triple loop.", "Check both bounds."],
                code={
                    "python": """
                        class Solution:
                            def countTriplesInBand(self, values: List[int], low: int, high: int) -> int:
                                n, count = len(values), 0  #@init
                                for i in range(n):  #@loops
                                    for j in range(i + 1, n):  #@loops
                                        for k in range(j + 1, n):  #@loops
                                            if low <= values[i] + values[j] + values[k] <= high:  #@loops
                                                count += 1  #@loops
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countTriplesInBand(int[] values, int low, int high) {
                                int n = values.length;  //@init
                                long count = 0;  //@init
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++) {  //@loops
                                            int s = values[i] + values[j] + values[k];  //@loops
                                            if (low <= s && s <= high) count++;  //@loops
                                        }
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countTriplesInBand(vector<int>& values, int low, int high) {
                                int n = values.size();  //@init
                                long long count = 0;  //@init
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++) {  //@loops
                                            int s = values[i] + values[j] + values[k];  //@loops
                                            if (low <= s && s <= high) count++;  //@loops
                                        }
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countTriplesInBand(int* values, int valuesSize, int low, int high) {
                            int n = valuesSize;  //@init
                            long long count = 0;  //@init
                            for (int i = 0; i < n; i++)  //@loops
                                for (int j = i + 1; j < n; j++)  //@loops
                                    for (int k = j + 1; k < n; k++) {  //@loops
                                        int s = values[i] + values[j] + values[k];  //@loops
                                        if (low <= s && s <= high) count++;  //@loops
                                    }
                            return count;  //@ret
                        }
                    """,
                },
                lines=[("init", "A 64-bit count."), ("loops", "Every triple, checked against both bounds."), ("ret", "Total.")],
                complexity=["**Time O(n³).** **Space O(1).**"],
                limits=["About 5.6 × 10⁸ triples at n = 1500. Turning the band into a difference of two one-sided counts allows the O(n²) range-counting squeeze."],
                slow=True,
            ),
            approach(
                "Two one-sided counts",
                "best",
                "O(n²)",
                "O(n)",
                idea=["`atMost(x)` counts triples with sum `≤ x` by the fix-one squeeze (add `k − j` when the sum fits). The answer is `atMost(high) − atMost(low − 1)`."],
                walk=w,
                build=["Sort.", "`atMost(x)` with the squeeze.", "Subtract."],
                code={
                    "python": """
                        class Solution:
                            def countTriplesInBand(self, values: List[int], low: int, high: int) -> int:
                                a = sorted(values)  #@sort
                                def at_most(x):  #@count
                                    total = 0  #@count
                                    for i in range(len(a) - 2):  #@count
                                        j, k = i + 1, len(a) - 1  #@count
                                        while j < k:  #@count
                                            if a[i] + a[j] + a[k] <= x:  #@count
                                                total += k - j  #@count
                                                j += 1  #@count
                                            else:  #@count
                                                k -= 1  #@count
                                    return total  #@count
                                return at_most(high) - at_most(low - 1)  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int[] a;

                            private long atMost(int x) {  //@count
                                long total = 0;  //@count
                                for (int i = 0; i + 2 < a.length; i++) {  //@count
                                    int j = i + 1, k = a.length - 1;  //@count
                                    while (j < k) {  //@count
                                        if (a[i] + a[j] + a[k] <= x) { total += k - j; j++; }  //@count
                                        else k--;  //@count
                                    }
                                }
                                return total;  //@count
                            }  //@count

                            public long countTriplesInBand(int[] values, int low, int high) {
                                a = values.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                return atMost(high) - atMost(low - 1);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            vector<int> a;

                            long long atMost(int x) {  //@count
                                long long total = 0;  //@count
                                for (int i = 0; i + 2 < (int) a.size(); i++) {  //@count
                                    int j = i + 1, k = (int) a.size() - 1;  //@count
                                    while (j < k) {  //@count
                                        if (a[i] + a[j] + a[k] <= x) { total += k - j; j++; }  //@count
                                        else k--;  //@count
                                    }
                                }
                                return total;  //@count
                            }  //@count

                        public:
                            long long countTriplesInBand(vector<int>& values, int low, int high) {
                                a = values;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                return atMost(high) - atMost(low - 1);  //@ret
                            }
                        };
                    """,
                    "c": C_CMP + """

                        static long long at_most(const int* a, int n, int x) {  //@count
                            long long total = 0;  //@count
                            for (int i = 0; i + 2 < n; i++) {  //@count
                                int j = i + 1, k = n - 1;  //@count
                                while (j < k) {  //@count
                                    if (a[i] + a[j] + a[k] <= x) { total += k - j; j++; }  //@count
                                    else k--;  //@count
                                }
                            }
                            return total;  //@count
                        }  //@count

                        long long countTriplesInBand(int* values, int valuesSize, int low, int high) {
                            int* a = malloc(valuesSize * sizeof(int));  //@sort
                            memcpy(a, values, valuesSize * sizeof(int));  //@sort
                            qsort(a, valuesSize, sizeof(int), cmp_int);  //@sort
                            long long answer = at_most(a, valuesSize, high) - at_most(a, valuesSize, low - 1);  //@ret
                            free(a);  //@ret
                            return answer;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Sort a copy."), ("count", "Triples with sum `≤ x`: fix `a[i]`, squeeze; when the sum fits, all `k − j` third values do (64-bit total)."), ("ret", "Sums in `[low, high]` = (sums ≤ high) − (sums ≤ low − 1).")],
                complexity=["**Time O(n²):** two counting passes. **Space O(n)** for the sorted copy."],
            ),
        ],
        takeaways=[
            """
            - **Two-sided range = difference of two one-sided counts:** `count(≤ high) − count(≤ low − 1)`.
            - The one-sided count uses the k-sum squeeze with range counting.
            - Watch the boundaries: `≤` versus `<` decides whether to subtract `low` or `low − 1`.
            """
        ],
    )


@problem
def zero_sum_triples():
    values = [-1, 0, 1, 2, -1, -4, 2, -2]
    a = sorted(values)
    out = []
    n = len(a)
    for i in range(n - 2):
        if i and a[i] == a[i - 1]:
            continue
        j, k = i + 1, n - 1
        while j < k:
            s = a[i] + a[j] + a[k]
            if s < 0:
                j += 1
            elif s > 0:
                k -= 1
            else:
                out.append([a[i], a[j], a[k]]); j += 1
                while j < k and a[j] == a[j - 1]:
                    j += 1
                k -= 1
    want = out

    w = Steps("Sort. Fix each different first value, squeeze for pairs summing to its negative, and skip repeated values so no triple is reported twice.")
    w.step(f"Sorted: {a}.", Row(a))
    found = []
    for i in range(n - 2):
        if i and a[i] == a[i - 1]:
            w.step(f"{a[i]} is the same first value as before: skip it (it would find the same triples).", Row(a, st={i: "mark"}))
            continue
        j, k = i + 1, n - 1
        hits = []
        while j < k:
            s = a[i] + a[j] + a[k]
            if s < 0:
                j += 1
            elif s > 0:
                k -= 1
            else:
                hits.append([a[i], a[j], a[k]]); j += 1
                while j < k and a[j] == a[j - 1]:
                    j += 1
                k -= 1
        found += hits
        w.step(f"First value {a[i]}: found {hits or 'nothing'}.", Row(a, st={i: "active"}), Vars(triples=len(found)))
    w.step(f"Triples: {found}.", result=str(found))

    sol(
        "zero-sum-triples",
        summary="""
            Sort, then for each **different** first value `a[i]`, squeeze `j`, `k` over the rest looking for
            `a[j] + a[k] = −a[i]`. After a hit, move `j` past copies of `a[j]` so the same triple isn't found again; skip
            repeated first values too. Triples come out already sorted. O(n²).
        """,
        question=[
            """
            Find every **different** triple of values (from three different positions) summing to 0. Each triple is written
            in increasing order, and the list is sorted.

            - **Duplicates in the input** must not create duplicate triples: `[-1, 0, 1]` is reported once.
            - **Up to 2000 values.**
            """
        ],
        think=[
            f"""
            `{values}` gives `{want}`.

            The 3-sum squeeze finds every triple, but with repeated values it would find some more than once. Two skips fix
            that, both easy because equal values sit together after sorting: skip a first value equal to the previous
            first value, and after recording a triple, step `j` past every copy of the value just used.
            """,
            fig(Row(values, label="values"), Row(a, label="sorted")),
        ],
        approaches=[
            approach(
                "Every triple, deduplicated with a set",
                "brute",
                "O(n³)",
                "O(t)",
                idea=["Check every triple; store each zero-sum triple, sorted, in a set; return the set sorted."],
                build=["Triple loop.", "Sorted tuple into a set.", "Sort the results."],
                code={
                    "python": """
                        class Solution:
                            def zeroTriples(self, values: List[int]) -> List[List[int]]:
                                n, found = len(values), set()  #@init
                                for i in range(n):  #@loops
                                    for j in range(i + 1, n):  #@loops
                                        for k in range(j + 1, n):  #@loops
                                            if values[i] + values[j] + values[k] == 0:  #@keep
                                                found.add(tuple(sorted((values[i], values[j], values[k]))))  #@keep
                                return [list(t) for t in sorted(found)]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] zeroTriples(int[] values) {
                                int n = values.length;  //@init
                                TreeSet<List<Integer>> found = new TreeSet<>((x, y) -> {  //@init
                                    for (int t = 0; t < 3; t++) if (!x.get(t).equals(y.get(t))) return Integer.compare(x.get(t), y.get(t));  //@init
                                    return 0;  //@init
                                });  //@init
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++)  //@loops
                                            if (values[i] + values[j] + values[k] == 0) {  //@keep
                                                Integer[] t = {values[i], values[j], values[k]};  //@keep
                                                Arrays.sort(t);  //@keep
                                                found.add(Arrays.asList(t));  //@keep
                                            }
                                int[][] out = new int[found.size()][];  //@ret
                                int r = 0;  //@ret
                                for (List<Integer> t : found) out[r++] = new int[] {t.get(0), t.get(1), t.get(2)};  //@ret
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> zeroTriples(vector<int>& values) {
                                int n = values.size();  //@init
                                set<vector<int>> found;  //@init
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        for (int k = j + 1; k < n; k++)  //@loops
                                            if (values[i] + values[j] + values[k] == 0) {  //@keep
                                                vector<int> t = {values[i], values[j], values[k]};  //@keep
                                                sort(t.begin(), t.end());  //@keep
                                                found.insert(t);  //@keep
                                            }
                                return vector<vector<int>>(found.begin(), found.end());  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmp3(const void* x, const void* y) {  //@keep
                            const int *a = *(int* const*) x, *b = *(int* const*) y;  //@keep
                            for (int t = 0; t < 3; t++) if (a[t] != b[t]) return (a[t] > b[t]) - (a[t] < b[t]);  //@keep
                            return 0;  //@keep
                        }  //@keep

                        int** zeroTriples(int* values, int valuesSize, int* returnSize, int** returnColumnSizes) {
                            int n = valuesSize, cap = 16, m = 0;  //@init
                            int** found = malloc(cap * sizeof(int*));  //@init
                            for (int i = 0; i < n; i++)  //@loops
                                for (int j = i + 1; j < n; j++)  //@loops
                                    for (int k = j + 1; k < n; k++)  //@loops
                                        if (values[i] + values[j] + values[k] == 0) {  //@keep
                                            int t[3] = {values[i], values[j], values[k]};  //@keep
                                            if (t[0] > t[1]) { int s = t[0]; t[0] = t[1]; t[1] = s; }  //@keep
                                            if (t[1] > t[2]) { int s = t[1]; t[1] = t[2]; t[2] = s; }  //@keep
                                            if (t[0] > t[1]) { int s = t[0]; t[0] = t[1]; t[1] = s; }  //@keep
                                            if (m == cap) found = realloc(found, (cap *= 2) * sizeof(int*));  //@keep
                                            found[m] = malloc(3 * sizeof(int));  //@keep
                                            memcpy(found[m++], t, sizeof t);  //@keep
                                        }
                            qsort(found, m, sizeof(int*), cmp3);  //@ret
                            int w = 0;  //@ret
                            for (int r = 0; r < m; r++) {  //@ret
                                if (w && cmp3(&found[w - 1], &found[r]) == 0) { free(found[r]); continue; }  //@ret
                                found[w++] = found[r];  //@ret
                            }
                            *returnSize = w;  //@ret
                            *returnColumnSizes = malloc((w + 1) * sizeof(int));  //@ret
                            for (int r = 0; r < w; r++) (*returnColumnSizes)[r] = 3;  //@ret
                            return found;  //@ret
                        }
                    """,
                },
                lines=[("init", "A set of distinct triples.", {"c": "No set in C: collect all triples, then sort and drop repeats."}), ("loops", "Every triple of positions."), ("keep", "Store the triple in increasing order, so equal triples look identical."), ("ret", "Sorted, distinct triples.", {"c": "Sort, then keep only the first copy of each triple; each row has 3 columns."})],
                complexity=["**Time O(n³).** **Space O(t)** for the t triples found."],
                limits=["About 1.3 × 10⁹ triples at n = 2000, plus a set to remove repeats. Sorting first lets the squeeze find each distinct triple once and skip duplicates by comparing neighbours."],
                slow=True,
            ),
            approach(
                "Sort, fix one, squeeze, skip duplicates",
                "best",
                "O(n²)",
                "O(1)",
                idea=["Sort. For each `i` (skipping `a[i] == a[i−1]`; stopping once `a[i] > 0`), squeeze `j`, `k`: sum < 0 → `j++`, > 0 → `k−−`, = 0 → record, then advance `j` past equal values and decrease `k`."],
                walk=w,
                build=["Sort a copy.", "Skip repeated first values.", "Squeeze; on a hit, skip repeated second values."],
                code={
                    "python": """
                        class Solution:
                            def zeroTriples(self, values: List[int]) -> List[List[int]]:
                                a, out = sorted(values), []  #@sort
                                for i in range(len(a) - 2):  #@fix
                                    if i and a[i] == a[i - 1]:  #@fix
                                        continue  #@fix
                                    if a[i] > 0:  #@stop
                                        break  #@stop
                                    j, k = i + 1, len(a) - 1  #@squeeze
                                    while j < k:  #@squeeze
                                        s = a[i] + a[j] + a[k]  #@squeeze
                                        if s < 0:  #@squeeze
                                            j += 1  #@squeeze
                                        elif s > 0:  #@squeeze
                                            k -= 1  #@squeeze
                                        else:  #@hit
                                            out.append([a[i], a[j], a[k]])  #@hit
                                            j += 1  #@hit
                                            while j < k and a[j] == a[j - 1]:  #@hit
                                                j += 1  #@hit
                                            k -= 1  #@hit
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] zeroTriples(int[] values) {
                                int[] a = values.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                List<int[]> out = new ArrayList<>();  //@sort
                                for (int i = 0; i + 2 < a.length; i++) {  //@fix
                                    if (i > 0 && a[i] == a[i - 1]) continue;  //@fix
                                    if (a[i] > 0) break;  //@stop
                                    int j = i + 1, k = a.length - 1;  //@squeeze
                                    while (j < k) {  //@squeeze
                                        int s = a[i] + a[j] + a[k];  //@squeeze
                                        if (s < 0) j++;  //@squeeze
                                        else if (s > 0) k--;  //@squeeze
                                        else {  //@hit
                                            out.add(new int[] {a[i], a[j], a[k]});  //@hit
                                            j++;  //@hit
                                            while (j < k && a[j] == a[j - 1]) j++;  //@hit
                                            k--;  //@hit
                                        }
                                    }
                                }
                                return out.toArray(new int[0][]);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> zeroTriples(vector<int>& values) {
                                vector<int> a = values;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                vector<vector<int>> out;  //@sort
                                int n = a.size();  //@sort
                                for (int i = 0; i + 2 < n; i++) {  //@fix
                                    if (i > 0 && a[i] == a[i - 1]) continue;  //@fix
                                    if (a[i] > 0) break;  //@stop
                                    int j = i + 1, k = n - 1;  //@squeeze
                                    while (j < k) {  //@squeeze
                                        int s = a[i] + a[j] + a[k];  //@squeeze
                                        if (s < 0) j++;  //@squeeze
                                        else if (s > 0) k--;  //@squeeze
                                        else {  //@hit
                                            out.push_back({a[i], a[j], a[k]});  //@hit
                                            j++;  //@hit
                                            while (j < k && a[j] == a[j - 1]) j++;  //@hit
                                            k--;  //@hit
                                        }
                                    }
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": C_CMP + """

                        int** zeroTriples(int* values, int valuesSize, int* returnSize, int** returnColumnSizes) {
                            int n = valuesSize, cap = 16, m = 0;  //@sort
                            int* a = malloc(n * sizeof(int));  //@sort
                            memcpy(a, values, n * sizeof(int));  //@sort
                            qsort(a, n, sizeof(int), cmp_int);  //@sort
                            int** out = malloc(cap * sizeof(int*));  //@sort
                            for (int i = 0; i + 2 < n; i++) {  //@fix
                                if (i > 0 && a[i] == a[i - 1]) continue;  //@fix
                                if (a[i] > 0) break;  //@stop
                                int j = i + 1, k = n - 1;  //@squeeze
                                while (j < k) {  //@squeeze
                                    int s = a[i] + a[j] + a[k];  //@squeeze
                                    if (s < 0) j++;  //@squeeze
                                    else if (s > 0) k--;  //@squeeze
                                    else {  //@hit
                                        if (m == cap) out = realloc(out, (cap *= 2) * sizeof(int*));  //@hit
                                        out[m] = malloc(3 * sizeof(int));  //@hit
                                        out[m][0] = a[i]; out[m][1] = a[j]; out[m][2] = a[k];  //@hit
                                        m++;  //@hit
                                        j++;  //@hit
                                        while (j < k && a[j] == a[j - 1]) j++;  //@hit
                                        k--;  //@hit
                                    }
                                }
                            }
                            free(a);  //@ret
                            *returnSize = m;  //@ret
                            *returnColumnSizes = malloc((m + 1) * sizeof(int));  //@ret
                            for (int r = 0; r < m; r++) (*returnColumnSizes)[r] = 3;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("sort", "Sort a copy; triples will come out in increasing order automatically."),
                    ("fix", "A first value equal to the previous one would find exactly the same triples: skip it."),
                    ("stop", "If the smallest of the three is positive, no sum can be 0 from here on."),
                    ("squeeze", "Look for `a[j] + a[k] = −a[i]`."),
                    ("hit", "Record the triple, then move `j` past every copy of this second value (the third value is then forced, so `k` moves too).", {"c": "The output array grows by doubling; each row has 3 columns."}),
                    ("ret", "Distinct triples, already sorted."),
                ],
                complexity=["**Time O(n²).** **Space O(1)** besides the sorted copy and the output."],
            ),
        ],
        takeaways=[
            """
            - **Distinct 3-sum:** sort, skip equal first values, and after each hit skip equal second values.
            - Sorting makes duplicates adjacent, so a neighbour comparison replaces a hash set.
            - Early exit: once the fixed value is positive, a zero sum is impossible.
            """
        ],
    )
