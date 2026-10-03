"""Two Pointers: pointers moving in from both ends."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def biggest_water_tank():
    posts = [3, 7, 2, 6, 4, 8, 1]
    n = len(posts)
    want = max((j - i) * min(posts[i], posts[j]) for i in range(n) for j in range(i + 1, n))

    w1 = Steps("Try every pair of posts.")
    for i in range(n):
        best_j = max(range(i + 1, n), key=lambda j: (j - i) * min(posts[i], posts[j]), default=None)
        if best_j is not None:
            w1.step(f"Left post {i} (height {posts[i]}): its best partner is post {best_j}, holding {(best_j - i) * min(posts[i], posts[best_j])}.", Row(posts, st={i: "active", best_j: "found"}))
    w1.step(f"Largest: {want}.", result=want)

    w2 = Steps("Start with the widest tank. The shorter post limits the water, and any narrower tank using it would be worse, so drop the shorter post and move inward.")
    i, j, best = 0, n - 1, 0
    while i < j:
        area = (j - i) * min(posts[i], posts[j])
        best = max(best, area)
        move = "left" if posts[i] < posts[j] else "right"
        w2.step(f"Posts {i} and {j}: width {j - i} × height {min(posts[i], posts[j])} = {area}. The {move} post is shorter (or equal): move it inward.", Row(posts, st={i: "active", j: "active"}, ptr={"i": i, "j": j}), Vars(best=best))
        if posts[i] < posts[j]:
            i += 1
        else:
            j -= 1
    w2.step(f"The pointers met. Largest: {best}.", result=best)

    sol(
        "biggest-water-tank",
        summary="""
            Start with the two outermost posts. The water level is set by the shorter one, and any other tank using that
            shorter post would be narrower and no taller, so it can never do better: discard it and move that pointer
            inward. One pass, O(n), keeping the best area (in 64 bits).
        """,
        question=[
            """
            Choose two posts; the tank holds `(distance between them) × (height of the shorter post)`. Return the most water
            any pair can hold.

            - **Posts in between don't matter** (the sheet goes over them).
            - **Up to 10⁵ posts, heights up to 10⁹**: the answer can reach 10¹⁴, so it needs 64 bits.
            """
        ],
        think=[
            f"""
            Posts `{posts}`. The best tank uses posts 1 (height 7) and 5 (height 8): width 4 × height 7 = **{want}**.

            Start as wide as possible: posts 0 and {n - 1}. To find something better we must give up width, so we need
            more height. Which post to give up? The shorter one: keeping it, every narrower tank is still capped by its
            height, so all of those tanks are worse than the one we just measured. Dropping it loses nothing.
            """,
            fig(Row(posts, label="posts")),
        ],
        approaches=[
            approach(
                "Every pair",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For every pair `i < j`, compute `(j − i) × min(posts[i], posts[j])` and keep the maximum."],
                walk=w1,
                build=["Double loop.", "64-bit area.", "Track the maximum."],
                code={
                    "python": """
                        class Solution:
                            def biggestTank(self, posts: List[int]) -> int:
                                best = 0  #@init
                                for i in range(len(posts)):  #@pairs
                                    for j in range(i + 1, len(posts)):  #@pairs
                                        best = max(best, (j - i) * min(posts[i], posts[j]))  #@area
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long biggestTank(int[] posts) {
                                long best = 0;  //@init
                                for (int i = 0; i < posts.length; i++)  //@pairs
                                    for (int j = i + 1; j < posts.length; j++)  //@pairs
                                        best = Math.max(best, (long) (j - i) * Math.min(posts[i], posts[j]));  //@area
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long biggestTank(vector<int>& posts) {
                                long long best = 0;  //@init
                                for (size_t i = 0; i < posts.size(); i++)  //@pairs
                                    for (size_t j = i + 1; j < posts.size(); j++)  //@pairs
                                        best = max(best, (long long) (j - i) * min(posts[i], posts[j]));  //@area
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long biggestTank(int* posts, int postsSize) {
                            long long best = 0;  //@init
                            for (int i = 0; i < postsSize; i++)  //@pairs
                                for (int j = i + 1; j < postsSize; j++) {  //@pairs
                                    int h = posts[i] < posts[j] ? posts[i] : posts[j];  //@area
                                    if ((long long) (j - i) * h > best) best = (long long) (j - i) * h;  //@area
                                }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Best area so far."), ("pairs", "Every pair of posts."), ("area", "Width times the shorter height, in 64 bits."), ("ret", "The largest.")],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["5 × 10⁹ pairs for 10⁵ posts. Most pairs can be ruled out: once a short post has been paired with the farthest post it can reach, no other pair with it can do better."],
                slow=True,
            ),
            approach(
                "Two pointers from the ends",
                "best",
                "O(n)",
                "O(1)",
                idea=["`i = 0`, `j = n − 1`. Measure the tank, then move whichever pointer has the shorter post inward (either one on a tie). Stop when they meet."],
                walk=w2,
                build=["Pointers at both ends.", "Measure; update the best.", "Move the shorter side inward."],
                code={
                    "python": """
                        class Solution:
                            def biggestTank(self, posts: List[int]) -> int:
                                i, j, best = 0, len(posts) - 1, 0  #@init
                                while i < j:  #@loop
                                    best = max(best, (j - i) * min(posts[i], posts[j]))  #@area
                                    if posts[i] < posts[j]:  #@move
                                        i += 1  #@move
                                    else:  #@move
                                        j -= 1  #@move
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long biggestTank(int[] posts) {
                                int i = 0, j = posts.length - 1;  //@init
                                long best = 0;  //@init
                                while (i < j) {  //@loop
                                    best = Math.max(best, (long) (j - i) * Math.min(posts[i], posts[j]));  //@area
                                    if (posts[i] < posts[j]) i++;  //@move
                                    else j--;  //@move
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long biggestTank(vector<int>& posts) {
                                int i = 0, j = (int) posts.size() - 1;  //@init
                                long long best = 0;  //@init
                                while (i < j) {  //@loop
                                    best = max(best, (long long) (j - i) * min(posts[i], posts[j]));  //@area
                                    if (posts[i] < posts[j]) i++;  //@move
                                    else j--;  //@move
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long biggestTank(int* posts, int postsSize) {
                            int i = 0, j = postsSize - 1;  //@init
                            long long best = 0;  //@init
                            while (i < j) {  //@loop
                                int h = posts[i] < posts[j] ? posts[i] : posts[j];  //@area
                                if ((long long) (j - i) * h > best) best = (long long) (j - i) * h;  //@area
                                if (posts[i] < posts[j]) i++;  //@move
                                else j--;  //@move
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "The widest possible tank, and the best so far."), ("loop", "Until the pointers meet."), ("area", "Measure the current tank (64-bit)."), ("move", "The shorter post can't do better with any narrower partner, so drop it. On a tie, dropping either is safe."), ("ret", "The largest tank seen.")],
                complexity=["**Time O(n):** each step moves one pointer. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Two pointers from both ends**: start with the widest choice and discard the side that can't improve.
            - The proof is an exchange argument: every pair the move skips is no better than one already measured.
            - Use 64-bit products when width × height can exceed 2³¹.
            """
        ],
    )


@problem
def boats_for_hikers():
    weights, limit = [70, 50, 80, 50, 30, 90], 100
    a = sorted(weights)
    i, j, boats, trips = 0, len(a) - 1, 0, []
    while i <= j:
        if i < j and a[i] + a[j] <= limit:
            trips.append(f"{a[j]}+{a[i]}"); i += 1
        else:
            trips.append(f"{a[j]}")
        j -= 1
        boats += 1
    want = boats

    w1 = Steps("Heaviest first: each heaviest hiker takes the heaviest remaining partner that still fits (scanning everyone left).")
    left = sorted(weights, reverse=True)
    count = 0
    while left:
        h = left.pop(0)
        partner = next((x for x in left if x + h <= limit), None)
        if partner is not None:
            left.remove(partner)
        count += 1
        w1.step(f"{h} takes a boat" + (f" with {partner}." if partner is not None else " alone: nobody left fits with them."), Row(left or ["·"], label="still waiting"), Vars(boats=count))
    w1.step(f"{count} boats.", result=count)

    w2 = Steps("Sort. The heaviest hiker must go now; pair them with the lightest if the two fit, since the lightest is the best partner anyone could have.")
    a2 = sorted(weights)
    i, j, b = 0, len(a2) - 1, 0
    while i <= j:
        pair = i < j and a2[i] + a2[j] <= limit
        b += 1
        w2.step(f"Heaviest {a2[j]}" + (f" and lightest {a2[i]} share a boat ({a2[i] + a2[j]} ≤ {limit})." if pair else (" goes alone." if i < j else " is the last hiker.")), Row(a2, st={j: "active", **({i: "active"} if pair else {})}, ptr={"i": i, "j": j}), Vars(boats=b))
        if pair:
            i += 1
        j -= 1
    w2.step(f"{b} boats.", result=b)

    sol(
        "boats-for-hikers",
        summary="""
            Sort the weights. The heaviest hiker needs a boat now; give them the lightest hiker as a partner if the pair fits
            (if even the lightest doesn't fit, nobody does). Either way the heaviest leaves. Two pointers do this in one pass
            after sorting: O(n log n).
        """,
        question=[
            """
            Each boat carries at most **two** hikers with total weight at most `limit`. Everyone weighs at most `limit`.
            Return the fewest boats.

            - **Two per boat at most**, even if three light hikers would fit by weight.
            - **Up to 10⁵ hikers.**
            """
        ],
        think=[
            f"""
            Weights `{weights}`, limit {limit}. Sorted: `{a}`. Trips: {', '.join(trips)}: **{want}** boats.

            The heaviest hiker is the hardest to pair. If the lightest hiker can join them, pairing those two is never
            worse than any other plan (swap partners in any optimal plan and it stays valid). If the lightest can't join,
            nobody can, so the heaviest rides alone. Either way, decide the heaviest and repeat.
            """,
            fig(Row(a, label="sorted weights")),
        ],
        approaches=[
            approach(
                "Heaviest takes the heaviest partner who fits",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Sort descending. Repeatedly take the heaviest remaining hiker and scan the rest for the heaviest partner who still fits; remove both (or just the one)."],
                walk=w1,
                build=["Sort descending; mark taken hikers.", "For each untaken hiker, scan forward for the first untaken partner that fits.", "Count boats."],
                code={
                    "python": """
                        class Solution:
                            def fewestBoats(self, weights: List[int], limit: int) -> int:
                                a = sorted(weights, reverse=True)  #@sort
                                taken = [False] * len(a)  #@sort
                                boats = 0  #@sort
                                for i in range(len(a)):  #@heavy
                                    if taken[i]:  #@heavy
                                        continue  #@heavy
                                    taken[i] = True  #@heavy
                                    boats += 1  #@heavy
                                    for j in range(i + 1, len(a)):  #@partner
                                        if not taken[j] and a[i] + a[j] <= limit:  #@partner
                                            taken[j] = True  #@partner
                                            break  #@partner
                                return boats  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int fewestBoats(int[] weights, int limit) {
                                int n = weights.length, boats = 0;  //@sort
                                int[] a = weights.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                boolean[] taken = new boolean[n];  //@sort
                                for (int i = n - 1; i >= 0; i--) {  //@heavy
                                    if (taken[i]) continue;  //@heavy
                                    taken[i] = true;  //@heavy
                                    boats++;  //@heavy
                                    for (int j = i - 1; j >= 0; j--)  //@partner
                                        if (!taken[j] && a[i] + a[j] <= limit) { taken[j] = true; break; }  //@partner
                                }
                                return boats;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int fewestBoats(vector<int>& weights, int limit) {
                                vector<int> a = weights;  //@sort
                                sort(a.rbegin(), a.rend());  //@sort
                                vector<char> taken(a.size(), 0);  //@sort
                                int boats = 0;  //@sort
                                for (size_t i = 0; i < a.size(); i++) {  //@heavy
                                    if (taken[i]) continue;  //@heavy
                                    taken[i] = 1;  //@heavy
                                    boats++;  //@heavy
                                    for (size_t j = i + 1; j < a.size(); j++)  //@partner
                                        if (!taken[j] && a[i] + a[j] <= limit) { taken[j] = 1; break; }  //@partner
                                }
                                return boats;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmp_int(const void* x, const void* y) {  //@sort
                            int a = *(const int*) x, b = *(const int*) y;  //@sort
                            return (a > b) - (a < b);  //@sort
                        }  //@sort

                        int fewestBoats(int* weights, int weightsSize, int limit) {
                            int n = weightsSize, boats = 0;  //@sort
                            int* a = malloc(n * sizeof(int));  //@sort
                            memcpy(a, weights, n * sizeof(int));  //@sort
                            qsort(a, n, sizeof(int), cmp_int);  //@sort
                            char* taken = calloc(n, 1);  //@sort
                            for (int i = n - 1; i >= 0; i--) {  //@heavy
                                if (taken[i]) continue;  //@heavy
                                taken[i] = 1;  //@heavy
                                boats++;  //@heavy
                                for (int j = i - 1; j >= 0; j--)  //@partner
                                    if (!taken[j] && a[i] + a[j] <= limit) { taken[j] = 1; break; }  //@partner
                            }
                            free(a); free(taken);  //@ret
                            return boats;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Heaviest first, with a mark for hikers already on a boat.", {"java": "Sorted ascending and walked from the end, which is the same as heaviest first.", "c": "Sorted ascending and walked from the end, which is the same as heaviest first."}), ("heavy", "The heaviest hiker still waiting gets a new boat."), ("partner", "The heaviest waiting hiker who still fits joins them."), ("ret", "Boats used.")],
                complexity=["**Time O(n²)** for the partner scans. **Space O(n).**"],
                limits=["The partner scan is wasted effort: if any partner fits the heaviest hiker, the lightest one does, and pairing with the lightest is just as good. That makes it two pointers."],
                slow=True,
            ),
            approach(
                "Sort, then pair heaviest with lightest",
                "best",
                "O(n log n)",
                "O(n)",
                idea=["Sort ascending; `i` at the lightest, `j` at the heaviest. Each boat takes hiker `j`, plus hiker `i` if `a[i] + a[j] ≤ limit`. Move the pointers and count."],
                walk=w2,
                build=["Sort.", "While `i ≤ j`: if the pair fits, `i += 1`; always `j −= 1`; count a boat.", "Return the count."],
                code={
                    "python": """
                        class Solution:
                            def fewestBoats(self, weights: List[int], limit: int) -> int:
                                a = sorted(weights)  #@sort
                                i, j, boats = 0, len(a) - 1, 0  #@init
                                while i <= j:  #@loop
                                    if a[i] + a[j] <= limit:  #@pair
                                        i += 1  #@pair
                                    j -= 1  #@heavy
                                    boats += 1  #@heavy
                                return boats  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int fewestBoats(int[] weights, int limit) {
                                int[] a = weights.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                int i = 0, j = a.length - 1, boats = 0;  //@init
                                while (i <= j) {  //@loop
                                    if (a[i] + a[j] <= limit) i++;  //@pair
                                    j--;  //@heavy
                                    boats++;  //@heavy
                                }
                                return boats;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int fewestBoats(vector<int>& weights, int limit) {
                                vector<int> a = weights;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                int i = 0, j = (int) a.size() - 1, boats = 0;  //@init
                                while (i <= j) {  //@loop
                                    if (a[i] + a[j] <= limit) i++;  //@pair
                                    j--;  //@heavy
                                    boats++;  //@heavy
                                }
                                return boats;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmp_int(const void* x, const void* y) {  //@sort
                            int a = *(const int*) x, b = *(const int*) y;  //@sort
                            return (a > b) - (a < b);  //@sort
                        }  //@sort

                        int fewestBoats(int* weights, int weightsSize, int limit) {
                            int* a = malloc(weightsSize * sizeof(int));  //@sort
                            memcpy(a, weights, weightsSize * sizeof(int));  //@sort
                            qsort(a, weightsSize, sizeof(int), cmp_int);  //@sort
                            int i = 0, j = weightsSize - 1, boats = 0;  //@init
                            while (i <= j) {  //@loop
                                if (a[i] + a[j] <= limit) i++;  //@pair
                                j--;  //@heavy
                                boats++;  //@heavy
                            }
                            free(a);  //@ret
                            return boats;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Lightest to heaviest."), ("init", "`i` at the lightest waiting hiker, `j` at the heaviest."), ("loop", "While anyone is waiting (`i == j` is a single last hiker)."), ("pair", "If the lightest fits with the heaviest, they share. (When `i == j`, this just moves `i` past the same hiker, which is harmless.)"), ("heavy", "The heaviest leaves on this boat either way."), ("ret", "Boats used.")],
                complexity=["**Time O(n log n)** for the sort; the pairing pass is O(n). **Space O(n)** for the sorted copy."],
            ),
        ],
        takeaways=[
            """
            - **Pairing greedy:** the hardest item (heaviest) takes the most accommodating partner (lightest), or goes alone.
            - Sorting turns "find the best partner" into moving two pointers.
            - Exchange arguments justify greedy pairings: swapping partners in any optimal plan never makes it worse.
            """
        ],
    )


@problem
def budget_pair():
    prices, budget = [2, 5, 9, 14, 20, 27], 34
    i, j = 0, len(prices) - 1
    while prices[i] + prices[j] != budget:
        if prices[i] + prices[j] < budget:
            i += 1
        else:
            j -= 1
    want = [i, j]

    w1 = Steps("Check every pair.")
    for a in range(len(prices)):
        for b in range(a + 1, len(prices)):
            if prices[a] + prices[b] == budget:
                w1.step(f"Pair {a}, {b}: {prices[a]} + {prices[b]} = {budget}. Found after checking all pairs before it.", Row(prices, st={a: "found", b: "found"}), result=str([a, b]))
                break
        else:
            w1.step(f"Position {a} ({prices[a]}): no partner adds to {budget}.", Row(prices, st={a: "mark"}))
            continue
        break

    w2 = Steps("Remember each price's position in a hash map; for each price, look up budget − price among the earlier ones.")
    seen = {}
    for k, p in enumerate(prices):
        need = budget - p
        if need in seen:
            w2.step(f"{p}: need {need}, seen at position {seen[need]}.", Row(prices, st={k: "found", seen[need]: "found"}), result=str([seen[need], k]))
            break
        seen[p] = k
        w2.step(f"{p}: need {need}, not seen yet. Remember {p} → {k}.", Row(prices, st={k: "active"}))

    w3 = Steps("The prices are sorted: start with the cheapest and the dearest. Too little → move the left pointer up; too much → move the right pointer down.")
    i, j = 0, len(prices) - 1
    while True:
        s = prices[i] + prices[j]
        if s == budget:
            w3.step(f"{prices[i]} + {prices[j]} = {budget}.", Row(prices, st={i: "found", j: "found"}, ptr={"i": i, "j": j}), result=str([i, j]))
            break
        w3.step(f"{prices[i]} + {prices[j]} = {s} is too {'small: move i right' if s < budget else 'big: move j left'}.", Row(prices, st={i: "active", j: "active"}, ptr={"i": i, "j": j}))
        if s < budget:
            i += 1
        else:
            j -= 1

    sol(
        "budget-pair",
        summary="""
            The prices are sorted, so start with the cheapest (`i`) and the most expensive (`j`). If their sum is too small,
            only a pricier left item can help, so move `i` right; if too big, move `j` left. Each step rules out one item
            for good: O(n) time and O(1) space.
        """,
        question=[
            """
            Prices are in increasing order; exactly one pair of different items sums to `budget`. Return their positions
            `[i, j]` with `i < j`.

            - **Sorted input** is the hint.
            - **Prices can be negative**, and sums reach 2 × 10⁹ (use 64-bit sums in C-like languages).
            """
        ],
        think=[
            f"""
            Prices `{prices}`, budget {budget}: {prices[want[0]]} + {prices[want[1]]} = {budget}, so the answer is
            `{want}`.

            With sorted prices, compare the smallest and largest. If `2 + 27 = 29`, done; if the sum were too small, the
            smallest price can't be in the pair with **anything** (even the largest isn't enough), so drop it. If too big,
            the largest can't be in the pair with anything, so drop it. Each comparison removes one candidate.
            """,
            fig(Row(prices, label="prices")),
        ],
        approaches=[
            approach(
                "Every pair",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["Check every `i < j` until the sum matches."],
                walk=w1,
                build=["Double loop.", "Return the first match."],
                code={
                    "python": """
                        class Solution:
                            def budgetPair(self, prices: List[int], budget: int) -> List[int]:
                                for i in range(len(prices)):  #@pairs
                                    for j in range(i + 1, len(prices)):  #@pairs
                                        if prices[i] + prices[j] == budget:  #@hit
                                            return [i, j]  #@hit
                                return [-1, -1]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] budgetPair(int[] prices, int budget) {
                                for (int i = 0; i < prices.length; i++)  //@pairs
                                    for (int j = i + 1; j < prices.length; j++)  //@pairs
                                        if ((long) prices[i] + prices[j] == budget) return new int[] {i, j};  //@hit
                                return new int[] {-1, -1};  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> budgetPair(vector<int>& prices, int budget) {
                                for (int i = 0; i < (int) prices.size(); i++)  //@pairs
                                    for (int j = i + 1; j < (int) prices.size(); j++)  //@pairs
                                        if ((long long) prices[i] + prices[j] == budget) return {i, j};  //@hit
                                return {-1, -1};  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* budgetPair(int* prices, int pricesSize, int budget, int* returnSize) {
                            int* out = malloc(2 * sizeof(int));  //@ret
                            out[0] = out[1] = -1;  //@ret
                            *returnSize = 2;  //@ret
                            for (int i = 0; i < pricesSize; i++)  //@pairs
                                for (int j = i + 1; j < pricesSize; j++)  //@pairs
                                    if ((long long) prices[i] + prices[j] == budget) { out[0] = i; out[1] = j; return out; }  //@hit
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("pairs", "Every pair of positions."), ("hit", "The pair that adds up (64-bit sum).", {"python": "Python integers don't overflow."}), ("ret", "Not reached: the input always has a pair.")],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["Ignores that the prices are sorted. A hash map gets O(n) but needs O(n) memory; sortedness allows O(n) with no memory."],
                slow=True,
            ),
            approach(
                "Hash map of seen prices",
                "better",
                "O(n)",
                "O(n)",
                idea=["Walk the prices; for each, check if `budget − price` was seen (store price → position)."],
                walk=w2,
                build=["Empty map.", "For each position: look up the complement, else store the price."],
                code={
                    "python": """
                        class Solution:
                            def budgetPair(self, prices: List[int], budget: int) -> List[int]:
                                seen = {}  #@init
                                for j, p in enumerate(prices):  #@loop
                                    if budget - p in seen:  #@hit
                                        return [seen[budget - p], j]  #@hit
                                    seen[p] = j  #@store
                                return [-1, -1]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] budgetPair(int[] prices, int budget) {
                                Map<Long, Integer> seen = new HashMap<>();  //@init
                                for (int j = 0; j < prices.length; j++) {  //@loop
                                    Integer i = seen.get((long) budget - prices[j]);  //@hit
                                    if (i != null) return new int[] {i, j};  //@hit
                                    seen.put((long) prices[j], j);  //@store
                                }
                                return new int[] {-1, -1};  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> budgetPair(vector<int>& prices, int budget) {
                                unordered_map<long long, int> seen;  //@init
                                for (int j = 0; j < (int) prices.size(); j++) {  //@loop
                                    auto it = seen.find((long long) budget - prices[j]);  //@hit
                                    if (it != seen.end()) return {it->second, j};  //@hit
                                    seen[prices[j]] = j;  //@store
                                }
                                return {-1, -1};  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* budgetPair(int* prices, int pricesSize, int budget, int* returnSize) {
                            int cap = 1;  //@init
                            while (cap < 2 * pricesSize) cap <<= 1;  //@init
                            long long* keys = malloc(cap * sizeof(long long));  //@init
                            int* pos = malloc(cap * sizeof(int));  //@init
                            for (int h = 0; h < cap; h++) pos[h] = -1;  //@init
                            int* out = malloc(2 * sizeof(int));  //@ret
                            out[0] = out[1] = -1;  //@ret
                            *returnSize = 2;  //@ret
                            for (int j = 0; j < pricesSize; j++) {  //@loop
                                long long need = (long long) budget - prices[j];  //@hit
                                unsigned h = (unsigned) (need * 2654435761u) & (cap - 1);  //@hit
                                while (pos[h] >= 0 && keys[h] != need) h = (h + 1) & (cap - 1);  //@hit
                                if (pos[h] >= 0) { out[0] = pos[h]; out[1] = j; break; }  //@hit
                                h = (unsigned) ((long long) prices[j] * 2654435761u) & (cap - 1);  //@store
                                while (pos[h] >= 0 && keys[h] != prices[j]) h = (h + 1) & (cap - 1);  //@store
                                if (pos[h] < 0) { keys[h] = prices[j]; pos[h] = j; }  //@store
                            }
                            free(keys); free(pos);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "Price → position for the prices seen so far.", {"c": "An open-addressing hash table; `pos = −1` marks an empty slot."}), ("loop", "Each price as the right half of the pair."), ("hit", "Its complement among earlier prices finishes the pair."), ("store", "Remember this price for later ones."), ("ret", "The pair.")],
                complexity=["**Time O(n).** **Space O(n).**"],
                limits=["Works for unsorted input too, but here it spends O(n) memory to learn what the order already tells us."],
            ),
            approach(
                "Two pointers on the sorted prices",
                "best",
                "O(n)",
                "O(1)",
                idea=["`i = 0`, `j = n − 1`. If the sum is too small, `i += 1`; too big, `j −= 1`; equal, return `[i, j]`."],
                walk=w3,
                build=["Pointers at both ends.", "Compare the sum with the budget.", "Move one pointer or return."],
                code={
                    "python": """
                        class Solution:
                            def budgetPair(self, prices: List[int], budget: int) -> List[int]:
                                i, j = 0, len(prices) - 1  #@init
                                while i < j:  #@loop
                                    s = prices[i] + prices[j]  #@loop
                                    if s == budget:  #@hit
                                        return [i, j]  #@hit
                                    if s < budget:  #@move
                                        i += 1  #@move
                                    else:  #@move
                                        j -= 1  #@move
                                return [-1, -1]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] budgetPair(int[] prices, int budget) {
                                int i = 0, j = prices.length - 1;  //@init
                                while (i < j) {  //@loop
                                    long s = (long) prices[i] + prices[j];  //@loop
                                    if (s == budget) return new int[] {i, j};  //@hit
                                    if (s < budget) i++;  //@move
                                    else j--;  //@move
                                }
                                return new int[] {-1, -1};  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> budgetPair(vector<int>& prices, int budget) {
                                int i = 0, j = (int) prices.size() - 1;  //@init
                                while (i < j) {  //@loop
                                    long long s = (long long) prices[i] + prices[j];  //@loop
                                    if (s == budget) return {i, j};  //@hit
                                    if (s < budget) i++;  //@move
                                    else j--;  //@move
                                }
                                return {-1, -1};  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* budgetPair(int* prices, int pricesSize, int budget, int* returnSize) {
                            int* out = malloc(2 * sizeof(int));  //@ret
                            out[0] = out[1] = -1;  //@ret
                            *returnSize = 2;  //@ret
                            int i = 0, j = pricesSize - 1;  //@init
                            while (i < j) {  //@loop
                                long long s = (long long) prices[i] + prices[j];  //@loop
                                if (s == budget) { out[0] = i; out[1] = j; break; }  //@hit
                                if (s < budget) i++;  //@move
                                else j--;  //@move
                            }
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "Cheapest and dearest."), ("loop", "The current pair's sum (64-bit)."), ("hit", "Found it."), ("move", "Too small: `prices[i]` is too cheap even with the dearest item left, so it's out. Too big: `prices[j]` is too dear even with the cheapest, so it's out."), ("ret", "The pair.")],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Sorted array + target sum = two pointers from the ends**, O(n) and O(1) memory.
            - Each comparison eliminates one end: the excluded item can't pair with anything left.
            - Unsorted input → hash map (or sort first, but then track original positions).
            """
        ],
    )


@problem
def closest_pair_sum():
    nums, target = [8, -4, 15, 3, -9, 6], 5
    a = sorted(nums)
    n = len(a)
    pairs = sorted({a[i] + a[j] for i in range(n) for j in range(i + 1, n)}, key=lambda s: (abs(s - target), s))
    want = pairs[0]

    w1 = Steps("Try every pair, keeping the sum closest to the target (smaller sum on a tie).")
    best = None
    for i in range(n):
        for j in range(i + 1, n):
            s = nums[i] + nums[j]
            if best is None or (abs(s - target), s) < (abs(best - target), best):
                best = s
        w1.step(f"After pairs starting at position {i}: best sum {best}.", Row(nums, st={i: "active"}), Vars(best=best))
    w1.step(f"Closest: {best}.", result=best)

    w2 = Steps("Sort, then squeeze from both ends: below the target, raise the sum; above it, lower it.")
    i, j, best = 0, n - 1, None
    w2.step(f"Sorted: {a}.", Row(a))
    while i < j:
        s = a[i] + a[j]
        if best is None or (abs(s - target), s) < (abs(best - target), best):
            best = s
        w2.step(f"{a[i]} + {a[j]} = {s} (distance {abs(s - target)}). {'Below the target: move i right.' if s < target else ('Above: move j left.' if s > target else 'Exact!')}", Row(a, st={i: "active", j: "active"}, ptr={"i": i, "j": j}), Vars(best=best))
        if s == target:
            break
        if s < target:
            i += 1
        else:
            j -= 1
    w2.step(f"Closest: {best}.", result=best)

    sol(
        "closest-pair-sum",
        summary="""
            Sort, then move two pointers inward: when the pair sum is below the target, only a bigger left value can get
            closer, and when it's above, only a smaller right value can. Track the best sum (closer, or equally close and
            smaller). O(n log n).
        """,
        question=[
            """
            Return the sum of two different elements that is closest to `target`; on a tie, the smaller sum.

            - **Values up to ±10⁹ and target up to ±2 × 10⁹**: distances need 64-bit arithmetic.
            - **Up to 10⁵ elements.**
            """
        ],
        think=[
            f"""
            `{nums}`, target {target}. The closest sums are {pairs[:3]}…, so the answer is **{want}**.

            After sorting, look at the smallest and largest values. If their sum is below the target, the smallest value
            paired with anything else would be even smaller, so it has no better pairing left: move past it. Symmetrically
            for a sum above the target. Every pair that could be the closest is still visited.
            """,
            fig(Row(nums, label="nums"), Row(a, label="sorted")),
        ],
        approaches=[
            approach(
                "Every pair",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["Check every pair, keeping the best by (distance, sum)."],
                walk=w1,
                build=["Double loop.", "Compare (|s − target|, s) with the best."],
                code={
                    "python": """
                        class Solution:
                            def closestPairSum(self, nums: List[int], target: int) -> int:
                                best = None  #@init
                                for i in range(len(nums)):  #@pairs
                                    for j in range(i + 1, len(nums)):  #@pairs
                                        s = nums[i] + nums[j]  #@better
                                        if best is None or (abs(s - target), s) < (abs(best - target), best):  #@better
                                            best = s  #@better
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int closestPairSum(int[] nums, int target) {
                                long best = Long.MAX_VALUE / 4;  //@init
                                for (int i = 0; i < nums.length; i++)  //@pairs
                                    for (int j = i + 1; j < nums.length; j++) {  //@pairs
                                        long s = (long) nums[i] + nums[j];  //@better
                                        long d = Math.abs(s - target), bd = Math.abs(best - target);  //@better
                                        if (d < bd || (d == bd && s < best)) best = s;  //@better
                                    }
                                return (int) best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int closestPairSum(vector<int>& nums, int target) {
                                long long best = LLONG_MAX / 4;  //@init
                                for (size_t i = 0; i < nums.size(); i++)  //@pairs
                                    for (size_t j = i + 1; j < nums.size(); j++) {  //@pairs
                                        long long s = (long long) nums[i] + nums[j];  //@better
                                        long long d = llabs(s - target), bd = llabs(best - target);  //@better
                                        if (d < bd || (d == bd && s < best)) best = s;  //@better
                                    }
                                return (int) best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int closestPairSum(int* nums, int numsSize, int target) {
                            long long best = LLONG_MAX / 4;  //@init
                            for (int i = 0; i < numsSize; i++)  //@pairs
                                for (int j = i + 1; j < numsSize; j++) {  //@pairs
                                    long long s = (long long) nums[i] + nums[j];  //@better
                                    long long d = llabs(s - target), bd = llabs(best - target);  //@better
                                    if (d < bd || (d == bd && s < best)) best = s;  //@better
                                }
                            return (int) best;  //@ret
                        }
                    """,
                },
                lines=[("init", "No pair yet.", {"java": "A huge sentinel, far from any target.", "cpp": "A huge sentinel, far from any target.", "c": "A huge sentinel, far from any target."}), ("pairs", "Every pair."), ("better", "Closer wins; on equal distance, the smaller sum. 64-bit so `s − target` can't overflow."), ("ret", "A sum of two values within ±10⁹ fits in an `int`, so the answer can be returned as one.")],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["5 × 10⁹ pairs for 10⁵ values. After sorting, two pointers visit only O(n) candidate pairs, and the skipped ones are provably no closer."],
                slow=True,
            ),
            approach(
                "Sort and squeeze",
                "best",
                "O(n log n)",
                "O(n)",
                idea=["Sort. `i = 0`, `j = n − 1`. Compute `s`, update the best; if `s < target` move `i` right, if `s > target` move `j` left, if equal return `s`."],
                walk=w2,
                build=["Sort a copy.", "Two pointers; update best by (distance, sum).", "Move toward the target."],
                code={
                    "python": """
                        class Solution:
                            def closestPairSum(self, nums: List[int], target: int) -> int:
                                a = sorted(nums)  #@sort
                                i, j, best = 0, len(a) - 1, None  #@init
                                while i < j:  #@loop
                                    s = a[i] + a[j]  #@loop
                                    if best is None or (abs(s - target), s) < (abs(best - target), best):  #@better
                                        best = s  #@better
                                    if s < target:  #@move
                                        i += 1  #@move
                                    elif s > target:  #@move
                                        j -= 1  #@move
                                    else:  #@move
                                        return s  #@move
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int closestPairSum(int[] nums, int target) {
                                int[] a = nums.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                int i = 0, j = a.length - 1;  //@init
                                long best = Long.MAX_VALUE / 4;  //@init
                                while (i < j) {  //@loop
                                    long s = (long) a[i] + a[j];  //@loop
                                    long d = Math.abs(s - target), bd = Math.abs(best - target);  //@better
                                    if (d < bd || (d == bd && s < best)) best = s;  //@better
                                    if (s < target) i++;  //@move
                                    else if (s > target) j--;  //@move
                                    else return (int) s;  //@move
                                }
                                return (int) best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int closestPairSum(vector<int>& nums, int target) {
                                vector<int> a = nums;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                int i = 0, j = (int) a.size() - 1;  //@init
                                long long best = LLONG_MAX / 4;  //@init
                                while (i < j) {  //@loop
                                    long long s = (long long) a[i] + a[j];  //@loop
                                    long long d = llabs(s - target), bd = llabs(best - target);  //@better
                                    if (d < bd || (d == bd && s < best)) best = s;  //@better
                                    if (s < target) i++;  //@move
                                    else if (s > target) j--;  //@move
                                    else return (int) s;  //@move
                                }
                                return (int) best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmp_int(const void* x, const void* y) {  //@sort
                            int a = *(const int*) x, b = *(const int*) y;  //@sort
                            return (a > b) - (a < b);  //@sort
                        }  //@sort

                        int closestPairSum(int* nums, int numsSize, int target) {
                            int* a = malloc(numsSize * sizeof(int));  //@sort
                            memcpy(a, nums, numsSize * sizeof(int));  //@sort
                            qsort(a, numsSize, sizeof(int), cmp_int);  //@sort
                            int i = 0, j = numsSize - 1;  //@init
                            long long best = LLONG_MAX / 4;  //@init
                            while (i < j) {  //@loop
                                long long s = (long long) a[i] + a[j];  //@loop
                                long long d = llabs(s - target), bd = llabs(best - target);  //@better
                                if (d < bd || (d == bd && s < best)) best = s;  //@better
                                if (s < target) i++;  //@move
                                else if (s > target) j--;  //@move
                                else break;  //@move
                            }
                            free(a);  //@ret
                            return (int) best;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Sort a copy."), ("init", "Pointers at both ends; no best yet."), ("loop", "The current pair's sum, in 64 bits."), ("better", "Keep it if closer, or equally close and smaller."), ("move", "Below the target, `a[i]` has no closer partner left (all are ≤ `a[j]`): drop it. Above, drop `a[j]`. Exact hits can't be beaten."), ("ret", "The best sum.")],
                complexity=["**Time O(n log n)** for the sort; the squeeze is O(n). **Space O(n)** for the copy."],
            ),
        ],
        takeaways=[
            """
            - **Closest pair sum = sort + squeeze**; the moving rule is the same as for an exact target.
            - Track ties explicitly (here: smaller sum wins).
            - Compute differences in 64 bits when values and targets are near the 32-bit limit.
            """
        ],
    )


@problem
def fewest_swaps_to_palindrome():
    word = "letelt"
    s, moves = list(word), 0
    w = Steps("Fix the outermost pair first: keep the first letter, bring its last matching copy to the end, and count the neighbour swaps. Then work inward.")
    w.step(f"Start: {word}.", Row(list(word)))
    while len(s) > 1:
        j = len(s) - 1
        while s[j] != s[0]:
            j -= 1
        if j == 0:
            moves += len(s) // 2
            w.step(f"'{s[0]}' has no partner: it's the middle letter. It will move to the centre, costing {len(s) // 2} swaps; set it aside.", Row(s, st={0: "mark"}), Vars(moves=moves))
            s.pop(0)
        else:
            cost = len(s) - 1 - j
            moves += cost
            w.step(f"Outer letter '{s[0]}': its last copy is at position {j}; {cost} swap(s) move it to the end. Both ends match; remove them.", Row(s, st={0: "found", j: "found"}), Vars(moves=moves))
            s.pop(j)
            s.pop(0)
    w.step(f"Fewest moves: {moves}.", result=moves)
    want = moves

    sol(
        "fewest-swaps-to-palindrome",
        summary="""
            Fix the string from the outside in. Keep the first letter where it is and bring the **nearest-to-the-end** copy
            of it to the last position with neighbour swaps; then both ends are settled and the problem shrinks. If the first
            letter has no other copy, it's the middle letter: it costs half the remaining length to reach the centre. O(n²)
            for n ≤ 2000.
        """,
        question=[
            """
            Using swaps of neighbouring letters only, turn `word` into a palindrome with the fewest moves. It can always be
            done.

            - **At most one letter** appears an odd number of times (it ends up in the middle).
            - **Length up to 2000.**
            """
        ],
        think=[
            f"""
            `{word}` needs **{want}** moves.

            Look at the outermost pair. The first letter has to match the last letter. Moving the first letter or moving a
            copy to the end are equivalent in cost by symmetry, so keep the first letter and drag its **last** copy (the
            one closest to the end, which needs the fewest swaps) to the end. Those swaps never disturb the relative order
            of the other letters, so the inner part is a smaller version of the same problem.

            The middle letter is the exception: if the first letter has no other copy, moving it now would be wasteful.
            It must end in the centre, which is half the current length away, and moving it later costs the same, so
            count that and remove it.
            """,
            fig(Row(list(word), label="word")),
        ],
        approaches=[
            approach(
                "Greedy from the outside in",
                "best",
                "O(n²)",
                "O(n)",
                idea=["Loop while more than one letter remains: find the last copy `j` of `s[0]`. If `j == 0`, add `len/2` and drop `s[0]`. Otherwise add `len − 1 − j` (swaps to bring it to the end) and drop both ends."],
                walk=w,
                build=["Work on a mutable copy.", "Find the last copy of the first letter.", "Middle letter or outer pair: count and shrink."],
                code={
                    "python": """
                        class Solution:
                            def minSwapsToPalindrome(self, word: str) -> int:
                                s, moves = list(word), 0  #@init
                                while len(s) > 1:  #@loop
                                    j = len(s) - 1  #@find
                                    while s[j] != s[0]:  #@find
                                        j -= 1  #@find
                                    if j == 0:  #@middle
                                        moves += len(s) // 2  #@middle
                                        s.pop(0)  #@middle
                                    else:  #@pair
                                        moves += len(s) - 1 - j  #@pair
                                        s.pop(j)  #@pair
                                        s.pop(0)  #@pair
                                return moves  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int minSwapsToPalindrome(String word) {
                                StringBuilder s = new StringBuilder(word);  //@init
                                int moves = 0;  //@init
                                while (s.length() > 1) {  //@loop
                                    int j = s.length() - 1;  //@find
                                    while (s.charAt(j) != s.charAt(0)) j--;  //@find
                                    if (j == 0) {  //@middle
                                        moves += s.length() / 2;  //@middle
                                        s.deleteCharAt(0);  //@middle
                                    } else {  //@pair
                                        moves += s.length() - 1 - j;  //@pair
                                        s.deleteCharAt(j);  //@pair
                                        s.deleteCharAt(0);  //@pair
                                    }
                                }
                                return moves;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int minSwapsToPalindrome(string& word) {
                                string s = word;  //@init
                                int moves = 0;  //@init
                                while (s.size() > 1) {  //@loop
                                    int j = s.size() - 1;  //@find
                                    while (s[j] != s[0]) j--;  //@find
                                    if (j == 0) {  //@middle
                                        moves += s.size() / 2;  //@middle
                                        s.erase(0, 1);  //@middle
                                    } else {  //@pair
                                        moves += s.size() - 1 - j;  //@pair
                                        s.erase(j, 1);  //@pair
                                        s.erase(0, 1);  //@pair
                                    }
                                }
                                return moves;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int minSwapsToPalindrome(char* word) {
                            int n = strlen(word), lo = 0, moves = 0;  //@init
                            char* s = malloc(n + 1);  //@init
                            memcpy(s, word, n + 1);  //@init
                            while (n - lo > 1) {  //@loop
                                int j = n - 1;  //@find
                                while (s[j] != s[lo]) j--;  //@find
                                if (j == lo) {  //@middle
                                    moves += (n - lo) / 2;  //@middle
                                    lo++;  //@middle
                                } else {  //@pair
                                    moves += n - 1 - j;  //@pair
                                    memmove(s + j, s + j + 1, n - 1 - j);  //@pair
                                    n--;  //@pair
                                    lo++;  //@pair
                                }
                            }
                            free(s);  //@ret
                            return moves;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "A copy we can shrink, and the move count.", {"c": "The live part of the string is `s[lo..n−1]`: dropping the first letter just advances `lo`."}),
                    ("loop", "Until at most one letter is left."),
                    ("find", "The last copy of the first letter: the one that needs the fewest swaps to reach the end."),
                    ("middle", "No other copy: this is the odd letter that belongs in the centre, half the current length away. Counting it now and removing it is the same as moving it at the end."),
                    ("pair", "Swap that copy step by step to the end (`len − 1 − j` swaps), then the outer pair matches: remove both.", {"c": "`memmove` closes the gap where the copy was (it has conceptually moved to the end and leaves the live part), and `lo++` drops the first letter."}),
                    ("ret", "Total moves."),
                ],
                complexity=["**Time O(n²):** each round scans and shifts up to n letters, n/2 rounds. **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - Work **from the outside in**: settle the outer pair, and the rest is a smaller instance.
            - Always move the copy that needs the fewest swaps; adjacent swaps don't change the others' order.
            - The odd letter is handled once, by its distance to the centre.
            """
        ],
    )


@problem
def reverse_letters_only():
    text = "ab-cd3e!f"
    letters = [c for c in text if c.isalpha()]
    out, k = [], len(letters) - 1
    for c in text:
        if c.isalpha():
            out.append(letters[k]); k -= 1
        else:
            out.append(c)
    want = "".join(out)

    w1 = Steps("Collect the letters, then write them back in reverse order into the letter positions.")
    w1.step(f"Letters in order: {''.join(letters)}.", Row(list(text), st={i: "active" for i, c in enumerate(text) if c.isalpha()}))
    w1.step(f"Write them back reversed: {want}.", Row(list(want)), result=want)

    w2 = Steps("Two pointers from the ends: skip non-letters on each side, then swap the two letters.")
    a, i, j = list(text), 0, len(text) - 1
    while i < j:
        if not a[i].isalpha():
            i += 1
        elif not a[j].isalpha():
            j -= 1
        else:
            w2.step(f"Swap '{a[i]}' and '{a[j]}'.", Row(a, st={i: "active", j: "active"}, ptr={"i": i, "j": j}))
            a[i], a[j] = a[j], a[i]
            i += 1
            j -= 1
    w2.step(f"Result: {''.join(a)}.", Row(a), result=want)

    sol(
        "reverse-letters-only",
        summary="""
            Two pointers from both ends: move each pointer past non-letters, then swap the two letters they point at and
            step both inward. Non-letters never move, and the letters end up reversed. O(n) time, in place.
        """,
        question=[
            """
            Reverse only the letters of `text`; every other character keeps its exact position.

            - **Letters** are A–Z and a–z; digits, punctuation and spaces stay put.
            - **Up to 10⁵ characters.**
            """
        ],
        think=[
            f"""
            `{text}` becomes `{want}`: the letters a, b, c, d, e, f come out as f, e, d, c, b, a, while `-`, `3` and `!`
            stay where they were.

            Reversing means the first letter swaps with the last letter, the second with the second-to-last, and so on.
            Two pointers find those pairs directly, skipping the characters that don't take part.
            """,
            fig(Row(list(text), label="text"), Row(list(want), label="result")),
        ],
        approaches=[
            approach(
                "Collect and write back",
                "better",
                "O(n)",
                "O(n)",
                idea=["Copy the letters out in order. Walk the text again; at each letter position, write the next letter from the end of the copy."],
                walk=w1,
                build=["Gather letters.", "Rebuild the text, taking letters from the back of the gathered list."],
                code={
                    "python": """
                        class Solution:
                            def reverseLetters(self, text: str) -> str:
                                letters = [c for c in text if c.isalpha()]  #@gather
                                out = []  #@write
                                for c in text:  #@write
                                    out.append(letters.pop() if c.isalpha() else c)  #@write
                                return "".join(out)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String reverseLetters(String text) {
                                StringBuilder letters = new StringBuilder();  //@gather
                                for (char c : text.toCharArray()) if (Character.isLetter(c)) letters.append(c);  //@gather
                                StringBuilder out = new StringBuilder();  //@write
                                int k = letters.length() - 1;  //@write
                                for (char c : text.toCharArray()) out.append(Character.isLetter(c) ? letters.charAt(k--) : c);  //@write
                                return out.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string reverseLetters(string& text) {
                                string letters;  //@gather
                                for (char c : text) if (isalpha((unsigned char) c)) letters += c;  //@gather
                                string out = text;  //@write
                                int k = (int) letters.size() - 1;  //@write
                                for (char& c : out) if (isalpha((unsigned char) c)) c = letters[k--];  //@write
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        #include <ctype.h>

                        char* reverseLetters(char* text) {
                            int n = strlen(text), m = 0;  //@gather
                            char* letters = malloc(n + 1);  //@gather
                            for (int i = 0; i < n; i++) if (isalpha((unsigned char) text[i])) letters[m++] = text[i];  //@gather
                            char* out = malloc(n + 1);  //@write
                            for (int i = 0; i < n; i++) out[i] = isalpha((unsigned char) text[i]) ? letters[--m] : text[i];  //@write
                            out[n] = '\\0';  //@write
                            free(letters);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("gather", "The letters, in their original order."), ("write", "Letter positions get letters from the back of the list; other characters are copied as they are."), ("ret", "The new text.")],
                complexity=["**Time O(n).** **Space O(n)** for the gathered letters."],
                limits=["Uses an extra copy of the letters. Swapping from both ends does the same reversal in place."],
            ),
            approach(
                "Swap from both ends",
                "best",
                "O(n)",
                "O(1) extra",
                idea=["`i` at the start, `j` at the end. Advance `i` past non-letters, pull `j` back past non-letters; when both sit on letters, swap them and move both inward."],
                walk=w2,
                build=["Mutable copy of the text.", "Two pointers with skipping.", "Swap letters."],
                code={
                    "python": """
                        class Solution:
                            def reverseLetters(self, text: str) -> str:
                                a = list(text)  #@init
                                i, j = 0, len(a) - 1  #@init
                                while i < j:  #@loop
                                    if not a[i].isalpha():  #@skip
                                        i += 1  #@skip
                                    elif not a[j].isalpha():  #@skip
                                        j -= 1  #@skip
                                    else:  #@swap
                                        a[i], a[j] = a[j], a[i]  #@swap
                                        i += 1  #@swap
                                        j -= 1  #@swap
                                return "".join(a)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String reverseLetters(String text) {
                                char[] a = text.toCharArray();  //@init
                                int i = 0, j = a.length - 1;  //@init
                                while (i < j) {  //@loop
                                    if (!Character.isLetter(a[i])) i++;  //@skip
                                    else if (!Character.isLetter(a[j])) j--;  //@skip
                                    else { char t = a[i]; a[i++] = a[j]; a[j--] = t; }  //@swap
                                }
                                return new String(a);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string reverseLetters(string& text) {
                                string a = text;  //@init
                                int i = 0, j = (int) a.size() - 1;  //@init
                                while (i < j) {  //@loop
                                    if (!isalpha((unsigned char) a[i])) i++;  //@skip
                                    else if (!isalpha((unsigned char) a[j])) j--;  //@skip
                                    else swap(a[i++], a[j--]);  //@swap
                                }
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        #include <ctype.h>

                        char* reverseLetters(char* text) {
                            int n = strlen(text);  //@init
                            char* a = malloc(n + 1);  //@init
                            memcpy(a, text, n + 1);  //@init
                            int i = 0, j = n - 1;  //@init
                            while (i < j) {  //@loop
                                if (!isalpha((unsigned char) a[i])) i++;  //@skip
                                else if (!isalpha((unsigned char) a[j])) j--;  //@skip
                                else { char t = a[i]; a[i++] = a[j]; a[j--] = t; }  //@swap
                            }
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("init", "A mutable copy (strings are immutable in Python and Java), with pointers at both ends."), ("loop", "Until the pointers meet."), ("skip", "Non-letters stay where they are: step over them."), ("swap", "Both pointers are on letters: swap and move inward."), ("ret", "The result.")],
                complexity=["**Time O(n):** every step moves a pointer. **Space O(1)** beyond the copy of the text."],
            ),
        ],
        takeaways=[
            """
            - **Reversal = swapping from both ends.** Filtering (only letters) just adds skip steps.
            - Characters that don't participate never move, so skipping them keeps them in place.
            - In C/C++, cast to `unsigned char` before calling `isalpha`.
            """
        ],
    )


@problem
def squares_in_order():
    values = [-7, -3, -1, 2, 4, 6]
    want = sorted(v * v for v in values)

    w1 = Steps("Square everything, then sort.")
    sq = [v * v for v in values]
    w1.step(f"Squares: {sq}. The negatives' squares are out of order.", Row(sq))
    w1.step(f"Sorted: {want}.", Row(want), result=str(want))

    w2 = Steps("The largest square is at one of the two ends. Fill the output from the back, taking the end with the bigger absolute value.")
    n = len(values)
    out = ["·"] * n
    i, j = 0, n - 1
    for k in range(n - 1, -1, -1):
        if abs(values[i]) > abs(values[j]):
            out[k] = values[i] ** 2
            w2.step(f"|{values[i]}| > |{values[j]}|: write {values[i] ** 2} at position {k}, move i right.", Row(values, st={i: "active"}, ptr={"i": i, "j": j}), Row(out, st={k: "new"}, label="output"))
            i += 1
        else:
            out[k] = values[j] ** 2
            w2.step(f"|{values[j]}| ≥ |{values[i]}|: write {values[j] ** 2} at position {k}, move j left.", Row(values, st={j: "active"}, ptr={"i": i, "j": j}), Row(out, st={k: "new"}, label="output"))
            j -= 1
    w2.step(f"Output: {out}.", result=str(want))

    sol(
        "squares-in-order",
        summary="""
            The input is sorted, so the biggest square comes from one of the two ends (the most negative or the most
            positive value). Compare the ends' absolute values, write the larger square into the last free slot of the
            output, and move that pointer inward. O(n).
        """,
        question=[
            """
            `values` is sorted (with negatives); return all squares in increasing order, in **O(n)**.

            - **Negatives flip order** when squared: −7 squares to 49, bigger than 6².
            - **Up to 10⁵ values**, |value| ≤ 10⁴ (squares fit in 32 bits).
            """
        ],
        think=[
            f"""
            `{values}` squares to `{[v * v for v in values]}`; sorted: `{want}`.

            The squares are smallest near zero and grow toward **both** ends. So the largest remaining square is always at
            the left end or the right end. Taking the larger of the two each time produces the squares from largest to
            smallest: fill the output from the back.
            """,
            fig(Row(values, label="values"), Row(want, label="squares sorted")),
        ],
        approaches=[
            approach(
                "Square and sort",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Square every value and sort the result."],
                walk=w1,
                build=["Square.", "Sort."],
                code={
                    "python": """
                        class Solution:
                            def sortedSquares(self, values: List[int]) -> List[int]:
                                return sorted(v * v for v in values)  #@sort
                    """,
                    "java": """
                        class Solution {
                            public int[] sortedSquares(int[] values) {
                                int[] out = new int[values.length];  //@sort
                                for (int i = 0; i < values.length; i++) out[i] = values[i] * values[i];  //@sort
                                Arrays.sort(out);  //@sort
                                return out;  //@sort
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortedSquares(vector<int>& values) {
                                vector<int> out;  //@sort
                                for (int v : values) out.push_back(v * v);  //@sort
                                sort(out.begin(), out.end());  //@sort
                                return out;  //@sort
                            }
                        };
                    """,
                    "c": """
                        static int cmp_int(const void* x, const void* y) {  //@sort
                            int a = *(const int*) x, b = *(const int*) y;  //@sort
                            return (a > b) - (a < b);  //@sort
                        }  //@sort

                        int* sortedSquares(int* values, int valuesSize, int* returnSize) {
                            int* out = malloc(valuesSize * sizeof(int));  //@sort
                            for (int i = 0; i < valuesSize; i++) out[i] = values[i] * values[i];  //@sort
                            qsort(out, valuesSize, sizeof(int), cmp_int);  //@sort
                            *returnSize = valuesSize;  //@sort
                            return out;  //@sort
                        }
                    """,
                },
                lines=[("sort", "Square everything and sort.")],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Misses the O(n) requirement and ignores that the input is sorted: the squares are two sorted runs (negatives reversed, then non-negatives) that only need merging."],
            ),
            approach(
                "Two pointers, fill from the back",
                "best",
                "O(n)",
                "O(n)",
                idea=["`i = 0`, `j = n − 1`. For `k` from `n − 1` down to 0: put the larger of `values[i]²` and `values[j]²` at `out[k]` and move that pointer inward."],
                walk=w2,
                build=["Output of size n.", "Pointers at both ends.", "Fill from the back with the larger square."],
                code={
                    "python": """
                        class Solution:
                            def sortedSquares(self, values: List[int]) -> List[int]:
                                n = len(values)  #@init
                                out = [0] * n  #@init
                                i, j = 0, n - 1  #@init
                                for k in range(n - 1, -1, -1):  #@fill
                                    if abs(values[i]) > abs(values[j]):  #@pick
                                        out[k] = values[i] * values[i]  #@pick
                                        i += 1  #@pick
                                    else:  #@pick
                                        out[k] = values[j] * values[j]  #@pick
                                        j -= 1  #@pick
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] sortedSquares(int[] values) {
                                int n = values.length, i = 0, j = n - 1;  //@init
                                int[] out = new int[n];  //@init
                                for (int k = n - 1; k >= 0; k--) {  //@fill
                                    if (Math.abs(values[i]) > Math.abs(values[j])) { out[k] = values[i] * values[i]; i++; }  //@pick
                                    else { out[k] = values[j] * values[j]; j--; }  //@pick
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortedSquares(vector<int>& values) {
                                int n = values.size(), i = 0, j = n - 1;  //@init
                                vector<int> out(n);  //@init
                                for (int k = n - 1; k >= 0; k--) {  //@fill
                                    if (abs(values[i]) > abs(values[j])) { out[k] = values[i] * values[i]; i++; }  //@pick
                                    else { out[k] = values[j] * values[j]; j--; }  //@pick
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* sortedSquares(int* values, int valuesSize, int* returnSize) {
                            int n = valuesSize, i = 0, j = n - 1;  //@init
                            int* out = malloc(n * sizeof(int));  //@init
                            for (int k = n - 1; k >= 0; k--) {  //@fill
                                if (abs(values[i]) > abs(values[j])) { out[k] = values[i] * values[i]; i++; }  //@pick
                                else { out[k] = values[j] * values[j]; j--; }  //@pick
                            }
                            *returnSize = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "The output and pointers at both ends."), ("fill", "Fill from the largest slot down."), ("pick", "The larger absolute value at either end gives the largest remaining square."), ("ret", "Squares in increasing order.")],
                complexity=["**Time O(n).** **Space O(n)** for the output."],
            ),
        ],
        takeaways=[
            """
            - **Sorted input with negatives:** the extremes are at both ends; two pointers merge them.
            - Filling the output from the back avoids having to find the smallest square first.
            - It's a merge of two sorted runs in disguise.
            """
        ],
    )
