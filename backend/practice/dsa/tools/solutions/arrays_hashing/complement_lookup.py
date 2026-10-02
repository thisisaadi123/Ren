"""Arrays & Hashing: complement lookup."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def two_gifts():
    prices, budget = [3, 8, 11, 2, 15, 7], 9

    # Brute force: every pair, one row per first gift.
    w1 = Steps("Fix the first gift, then try every gift after it as the second.")
    w1.step("Six gifts, budget 9. Each gift i is paired with every j after it.", Row(prices, slots=True))
    found = None
    for i in range(len(prices)):
        partners = list(range(i + 1, len(prices)))
        hit = next((j for j in partners if prices[i] + prices[j] == budget), None)
        st = {k: "dim" for k in range(i)}
        st[i] = "active"
        if hit is None:
            for j in partners:
                st[j] = "mark"
            sums = ", ".join(f"{prices[i]}+{prices[j]}={prices[i] + prices[j]}" for j in partners)
            w1.step(f"i = {i} (price {prices[i]}): {sums}. None is 9.", Row(prices, st=st, ptr={"i": i}, slots=True))
        else:
            for j in partners:
                if j < hit:
                    st[j] = "mark"
            st[i], st[hit] = "answer", "answer"
            w1.step(f"i = {i} (price {prices[i]}): {prices[i]} + {prices[hit]} = 9. Found it.", Row(prices, st=st, ptr={"i": i, "j": hit}, slots=True), result=[i, hit])
            found = [i, hit]
            break
    assert found == [3, 5]

    # Sort + two pointers.
    w2 = Steps("Sort (price, index) pairs, then squeeze from both ends.")
    order = sorted(range(len(prices)), key=lambda k: prices[k])
    sp = [prices[k] for k in order]
    idx = [f"#{k}" for k in order]
    w2.step("Pair every price with its original index, then sort by price. The indices ride along.", Row(sp, label="sorted prices"), Row(idx, label="original index"))
    lo, hi = 0, len(sp) - 1
    while lo < hi:
        s = sp[lo] + sp[hi]
        st = {k: "dim" for k in range(len(sp)) if k < lo or k > hi}
        st[lo] = st[hi] = "active"
        if s == budget:
            st[lo] = st[hi] = "answer"
            a, b = sorted([order[lo], order[hi]])
            w2.step(f"{sp[lo]} + {sp[hi]} = 9. Their original indices are {order[lo]} and {order[hi]}.", Row(sp, st=st, ptr={"lo": lo, "hi": hi}, label="sorted prices"), Row(idx, st={lo: "answer", hi: "answer"}, label="original index"), result=[a, b])
            break
        if s > budget:
            w2.step(f"{sp[lo]} + {sp[hi]} = {s}, too much. {sp[hi]} is too big even with the cheapest gift, so drop it: hi moves left.", Row(sp, st=st, ptr={"lo": lo, "hi": hi}, label="sorted prices"), Vars(sum=s))
            hi -= 1
        else:
            w2.step(f"{sp[lo]} + {sp[hi]} = {s}, too little. {sp[lo]} is too small even with the priciest gift left, so drop it: lo moves right.", Row(sp, st=st, ptr={"lo": lo, "hi": hi}, label="sorted prices"), Vars(sum=s))
            lo += 1

    # Hash map.
    w3 = Steps("Walk once. For each price, ask the map whether its partner (9 − price) has already gone by.")
    seen = {}
    for j, p in enumerate(prices):
        need = budget - p
        st = {k: "dim" for k in range(j)}
        st[j] = "active"
        mp = Row([f"{k}→{v}" for k, v in seen.items()], label="price → index") if seen else Row([], label="price → index")
        if need in seen:
            st[seen[need]] = "answer"
            st[j] = "answer"
            w3.step(f"j = {j}, price {p}: partner 9 − {p} = {need} is in the map at index {seen[need]}. Done.", Row(prices, st=st, ptr={"j": j}, slots=True), Row([f"{k}→{v}" for k, v in seen.items()], st={list(seen).index(need): "answer"}, label="price → index"), result=[seen[need], j])
            break
        w3.step(f"j = {j}, price {p}: partner {need} isn't in the map. Store {p}→{j}.", Row(prices, st=st, ptr={"j": j}, slots=True), mp)
        seen[p] = j

    sol(
        "two-gifts",
        summary="""
            For each gift, the second gift is already decided: it must cost `budget − price`. The whole problem
            is about how fast you can answer "have I seen that price, and where?" A hash map answers it in
            O(1), which takes the solution from O(n²) to O(n).
        """,
        question=[
            """
            You get a list of gift prices and a budget. Exactly two **different** gifts add up to the budget
            exactly, and you return their positions (indices), smaller one first.

            The details that matter:

            - **Indices, not prices.** You return where the gifts sit in the list, so any trick that
              rearranges the list has to remember the original positions.
            - **Two different gifts.** One gift can't be bought twice. With `prices = [3, 2, 4]` and budget 6,
              the gift at index 0 costs 3, and 3 + 3 = 6, but that would be the same gift twice. The answer is
              `[1, 2]` (2 + 4).
            - **Equal prices are fine.** Two *different* gifts may cost the same: `[5, 5]` with budget 10 is
              `[0, 1]`.
            - **Prices can be negative** (coupons), so you can't throw a price away just because it's bigger
              than the budget: 15 + (−6) = 9.
            - **Exactly one answer exists**, so you can stop the moment you find a pair.
            - **Size:** up to 10⁵ prices. Checking every pair is about 5 × 10⁹ checks, far too slow.
              You need something close to one pass.
            - **Big numbers:** prices go to ±10⁹ and the budget to ±2 × 10⁹. In Java, C++ and C,
              `budget − price` can reach 3 × 10⁹, past the 32-bit `int` limit (about 2.1 × 10⁹), so that
              arithmetic needs 64-bit integers.
            """
        ],
        think=[
            """
            Take `prices = [3, 8, 11, 2, 15, 7]` and `budget = 9`, and solve it by hand.

            You'd probably pick a gift and ask "what would go with this?" For the 3, the partner must cost
            9 − 3 = **6**. Is there a 6? You scan the list: no. For the 8 you need a **1**: no. For the 11 you
            need **−2**: no. For the 2 you need a **7**: yes, at index 5.
            """,
            fig(Row(prices, st={3: "answer", 5: "answer"}, slots=True), Row([6, 1, -2, 7, -6, 2], st={3: "answer", 5: "answer"}, label="partner needed (9 − price)"),
                caption="Every price has exactly one partner value. The answer is the pair where a price's partner is also in the list."),
            """
            Two things stand out:

            1. **The partner is fixed.** You never search for "some gift that works". You search for one exact
               value, `budget − price`. That turns the problem into a lookup problem.
            2. **The slow part is the scan.** Each "is there a 6?" scans the whole list, and n scans of n items
               is O(n²). The rest of this solution is about making that question cheap: first by sorting,
               then with a hash map.

            Also notice the order: if you only ever look *backwards* (at gifts you've already passed), the 7
            at index 5 finds the 2 at index 3. You never need to look ahead, because the second gift of the
            pair will find the first.
            """,
        ],
        approaches=[
            approach(
                "Check every pair",
                "brute",
                "O(n²)",
                "O(1)",
                idea=[
                    """
                    Try every pair of different gifts `(i, j)` with `i < j` and return the first pair whose
                    prices add up to the budget. Starting `j` at `i + 1` does two things at once: it never pairs
                    a gift with itself, and it never checks a pair twice (`(2, 5)` and `(5, 2)` are the same
                    pair).
                    """
                ],
                walk=w1,
                build=[
                    "Loop `i` over every index: the first gift.",
                    "Inside it, loop `j` from `i + 1` to the end: the second gift, always after the first.",
                    "If `prices[i] + prices[j] == budget`, return `[i, j]`. It's already in order because `i < j`.",
                    "After the loops, return an empty list. The problem promises an answer, so this line never runs, but the compiler or reader still wants every path to return.",
                ],
                code={
                    "python": """
                        class Solution:
                            def pickTwo(self, prices: List[int], budget: int) -> List[int]:  #@sig
                                n = len(prices)  #@n
                                for i in range(n):  #@i
                                    for j in range(i + 1, n):  #@j
                                        if prices[i] + prices[j] == budget:  #@test
                                            return [i, j]  #@ret
                                return []  #@none
                    """,
                    "java": """
                        class Solution {
                            public int[] pickTwo(int[] prices, int budget) {  //@sig
                                int n = prices.length;  //@n
                                for (int i = 0; i < n; i++) {  //@i
                                    for (int j = i + 1; j < n; j++) {  //@j
                                        if ((long) prices[i] + prices[j] == budget) {  //@test
                                            return new int[] {i, j};  //@ret
                                        }
                                    }
                                }
                                return new int[0];  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> pickTwo(vector<int>& prices, int budget) {  //@sig
                                int n = prices.size();  //@n
                                for (int i = 0; i < n; i++) {  //@i
                                    for (int j = i + 1; j < n; j++) {  //@j
                                        if ((long long) prices[i] + prices[j] == budget) {  //@test
                                            return {i, j};  //@ret
                                        }
                                    }
                                }
                                return {};  //@none
                            }
                        };
                    """,
                    "c": """
                        int* pickTwo(int* prices, int pricesSize, int budget, int* returnSize) {  //@sig
                            int* answer = malloc(2 * sizeof(int));  //@alloc
                            *returnSize = 2;  //@alloc
                            for (int i = 0; i < pricesSize; i++) {  //@i
                                for (int j = i + 1; j < pricesSize; j++) {  //@j
                                    if ((long long) prices[i] + prices[j] == budget) {  //@test
                                        answer[0] = i;  //@ret
                                        answer[1] = j;  //@ret
                                        return answer;  //@ret
                                    }
                                }
                            }
                            *returnSize = 0;  //@none
                            return answer;  //@none
                        }
                    """,
                },
                lines=[
                    ("sig", "The function takes the prices and the budget and returns two indices.",
                     {"c": "In C an array arrives as a pointer plus its length (`pricesSize`). The answer is an array too, so the function also gets `returnSize`, where it writes how long the answer is."}),
                    ("n", "Keep the length in `n` so the loops read clearly."),
                    ("alloc", "C has no list to return, so make room for two ints with `malloc` and say the answer has length 2. The caller frees it."),
                    ("i", "`i` is the first gift. It goes over every index."),
                    ("j", "`j` is the second gift and always starts right after `i`. That rules out using one gift twice, and it visits each pair exactly once."),
                    ("test", "Do the two prices hit the budget exactly?",
                     {"java": "`(long)` widens the sum to 64 bits before adding. Two prices near 10⁹ add up to 2 × 10⁹, close to `int`'s limit; widening is the safe habit.",
                      "cpp": "`(long long)` widens the sum to 64 bits before adding, so it can't overflow.",
                      "c": "`(long long)` widens the sum to 64 bits before adding, so it can't overflow."}),
                    ("ret", "The first match is the answer. `i < j` already, so the order is right."),
                    ("none", "Unreachable with valid input (exactly one pair exists), but every path must return something."),
                ],
                complexity=[
                    """
                    **Time O(n²).** For `i = 0` the inner loop runs n − 1 times, for `i = 1` it runs n − 2
                    times, and so on: (n − 1) + (n − 2) + … + 1 = n(n − 1)/2 pair checks in the worst case.
                    With n = 10⁵ that's about 5 × 10⁹ checks.

                    **Space O(1).** Just two loop counters (and the two-number answer).
                    """
                ],
                limits=[
                    """
                    It's correct, but it re-asks the same question over and over: "is there a 6 somewhere after
                    me?" is answered by scanning, every time. At 10⁵ prices that's billions of additions, many
                    seconds even in C. Interviewers expect you to say this version out loud as a baseline and
                    then improve it.
                    """
                ],
                slow=True,
            ),
            approach(
                "Sort, then walk inward from both ends",
                "better",
                "O(n log n)",
                "O(n)",
                idea=[
                    """
                    In a **sorted** list, a pair sum tells you which way to move. Put one finger on the cheapest
                    price (`lo`) and one on the most expensive (`hi`):

                    - If the sum is **too big**, the price at `hi` can't be in the answer: even paired with the
                      cheapest gift left it overshoots, and every other partner is pricier. Drop it: `hi − 1`.
                    - If the sum is **too small**, the price at `lo` can't be in the answer: even paired with the
                      priciest gift left it falls short. Drop it: `lo + 1`.
                    - If it's **equal**, you found the pair.

                    Each step throws away one gift for good, so the walk takes at most n − 1 steps.

                    The catch: sorting moves the prices, and we must return **original** indices. So sort the
                    *indices* by price (or sort (price, index) pairs), and read the positions off at the end.
                    """
                ],
                walk=w2,
                build=[
                    "Make a list of indices `0 … n−1` and sort it by `prices[index]`. Now `order[0]` is the index of the cheapest gift.",
                    "Set `lo = 0` and `hi = n − 1`, pointing into `order`.",
                    "While `lo < hi`: add the two prices. Equal: you're done. Too big: `hi -= 1`. Too small: `lo += 1`.",
                    "When they match, the answer is the two original indices `order[lo]` and `order[hi]`, smaller first. Sorting by price may have put the later index first.",
                ],
                code={
                    "python": """
                        class Solution:
                            def pickTwo(self, prices: List[int], budget: int) -> List[int]:
                                order = sorted(range(len(prices)), key=lambda k: prices[k])  #@sort
                                lo, hi = 0, len(prices) - 1  #@ptr
                                while lo < hi:  #@loop
                                    total = prices[order[lo]] + prices[order[hi]]  #@sum
                                    if total == budget:  #@hit
                                        a, b = order[lo], order[hi]  #@hit
                                        return [min(a, b), max(a, b)]  #@hit
                                    if total > budget:  #@big
                                        hi -= 1  #@big
                                    else:  #@small
                                        lo += 1  #@small
                                return []  #@none
                    """,
                    "java": """
                        class Solution {
                            public int[] pickTwo(int[] prices, int budget) {
                                int n = prices.length;
                                Integer[] order = new Integer[n];  //@sort
                                for (int k = 0; k < n; k++) order[k] = k;  //@sort
                                Arrays.sort(order, (a, b) -> Integer.compare(prices[a], prices[b]));  //@sort
                                int lo = 0, hi = n - 1;  //@ptr
                                while (lo < hi) {  //@loop
                                    long total = (long) prices[order[lo]] + prices[order[hi]];  //@sum
                                    if (total == budget) {  //@hit
                                        int a = order[lo], b = order[hi];  //@hit
                                        return new int[] {Math.min(a, b), Math.max(a, b)};  //@hit
                                    }
                                    if (total > budget) hi--;  //@big
                                    else lo++;  //@small
                                }
                                return new int[0];  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> pickTwo(vector<int>& prices, int budget) {
                                int n = prices.size();
                                vector<int> order(n);  //@sort
                                iota(order.begin(), order.end(), 0);  //@sort
                                sort(order.begin(), order.end(), [&](int a, int b) { return prices[a] < prices[b]; });  //@sort
                                int lo = 0, hi = n - 1;  //@ptr
                                while (lo < hi) {  //@loop
                                    long long total = (long long) prices[order[lo]] + prices[order[hi]];  //@sum
                                    if (total == budget) {  //@hit
                                        int a = order[lo], b = order[hi];  //@hit
                                        return {min(a, b), max(a, b)};  //@hit
                                    }
                                    if (total > budget) hi--;  //@big
                                    else lo++;  //@small
                                }
                                return {};  //@none
                            }
                        };
                    """,
                    "c": """
                        static int* gPrices;  //@cmp

                        static int byPrice(const void* x, const void* y) {  //@cmp
                            int a = gPrices[*(const int*) x], b = gPrices[*(const int*) y];  //@cmp
                            return (a > b) - (a < b);  //@cmp
                        }  //@cmp

                        int* pickTwo(int* prices, int pricesSize, int budget, int* returnSize) {
                            int* order = malloc(pricesSize * sizeof(int));  //@sort
                            for (int k = 0; k < pricesSize; k++) order[k] = k;  //@sort
                            gPrices = prices;  //@sort
                            qsort(order, pricesSize, sizeof(int), byPrice);  //@sort
                            int* answer = malloc(2 * sizeof(int));
                            *returnSize = 0;
                            int lo = 0, hi = pricesSize - 1;  //@ptr
                            while (lo < hi) {  //@loop
                                long long total = (long long) prices[order[lo]] + prices[order[hi]];  //@sum
                                if (total == budget) {  //@hit
                                    int a = order[lo], b = order[hi];  //@hit
                                    answer[0] = a < b ? a : b;  //@hit
                                    answer[1] = a < b ? b : a;  //@hit
                                    *returnSize = 2;  //@hit
                                    break;  //@hit
                                }
                                if (total > budget) hi--;  //@big
                                else lo++;  //@small
                            }
                            free(order);  //@free
                            return answer;  //@free
                        }
                    """,
                },
                lines=[
                    ("cmp", "C's `qsort` compares two elements without any extra context, so the prices go in a file-level pointer, `gPrices`, and `byPrice` compares two indices by their prices. `(a > b) - (a < b)` gives −1, 0 or 1 without the overflow that `a − b` could cause."),
                    ("sort", "Build the indices `0 … n−1` and sort them by price. The prices themselves don't move, so each entry of `order` still knows its gift's original position.",
                     {"java": "`Arrays.sort` with a comparator needs objects, hence `Integer[]` instead of `int[]`.",
                      "cpp": "`iota` fills `0, 1, 2, …`; the lambda compares two indices by their prices."}),
                    ("ptr", "`lo` starts at the cheapest gift, `hi` at the most expensive (positions in `order`)."),
                    ("loop", "Keep going while the fingers point at two different gifts."),
                    ("sum", "The current pair's total.",
                     {"java": "Computed as `long`, so two big prices can't overflow.", "cpp": "Computed as `long long`, so two big prices can't overflow.", "c": "Computed as `long long`, so two big prices can't overflow."}),
                    ("hit", "A match. The two original indices can come out in either order (the cheaper gift might sit later in the list), so return the smaller one first."),
                    ("big", "Too big: the gift at `hi` overshoots even with the cheapest partner left, so it can't be in the answer. Drop it."),
                    ("small", "Too small: the gift at `lo` falls short even with the priciest partner left. Drop it."),
                    ("free", "Free the scratch array; return the answer (the caller frees that)."),
                    ("none", "Unreachable with valid input."),
                ],
                complexity=[
                    """
                    **Time O(n log n).** Sorting costs O(n log n). The two-pointer walk is O(n): every step
                    moves `lo` or `hi` one place inward, and they meet after at most n − 1 steps. The sort
                    dominates.

                    **Space O(n)** for the `order` array of indices (plus whatever the sort uses internally).
                    """
                ],
                limits=[
                    """
                    Much faster than checking every pair (about 1.7 million steps for n = 10⁵ instead of 5
                    billion), but the sort is work the problem never asked for, and it forces the extra index
                    bookkeeping. This is the right tool when the input is **already sorted** (then it's O(n)
                    time and O(1) space). Here the input is unsorted, and a hash map skips the sort entirely.
                    """
                ],
            ),
            approach(
                "One pass with a hash map",
                "best",
                "O(n)",
                "O(n)",
                idea=[
                    """
                    Go through the gifts once, left to right, and keep a **hash map from price to index** of the
                    gifts you've already passed. At gift `j` with price `p`, the partner must cost
                    `budget − p`. Ask the map: is that price there?

                    - **Yes:** the partner sits at `map[budget − p]`, which is earlier than `j`. Return
                      `[map[budget − p], j]`, already in order.
                    - **No:** store `p → j` and move on. If `p`'s partner comes later, that gift will find `p`
                      here.

                    The order inside the loop matters: **look up first, store second.** If you stored first,
                    a price of 3 with budget 6 would find itself and you'd return one gift twice.
                    """
                ],
                walk=w3,
                build=[
                    "Create an empty map from price to index.",
                    "Loop `j` over the indices, with `p = prices[j]`.",
                    "Compute `need = budget − p` (in 64 bits in Java, C++ and C).",
                    "If `need` is in the map, return `[map[need], j]`.",
                    "Otherwise store `map[p] = j` and continue.",
                    "Equal prices: if a price appears twice, the second copy overwrites nothing important. When the pair *is* the two copies (`[5, 5]`, budget 10), the second 5 looks up 5 and finds the first one before storing itself.",
                ],
                code={
                    "python": """
                        class Solution:
                            def pickTwo(self, prices: List[int], budget: int) -> List[int]:
                                where = {}  #@map
                                for j, p in enumerate(prices):  #@loop
                                    need = budget - p  #@need
                                    if need in where:  #@look
                                        return [where[need], j]  #@look
                                    where[p] = j  #@store
                                return []  #@none
                    """,
                    "java": """
                        class Solution {
                            public int[] pickTwo(int[] prices, int budget) {
                                Map<Long, Integer> where = new HashMap<>();  //@map
                                for (int j = 0; j < prices.length; j++) {  //@loop
                                    long need = (long) budget - prices[j];  //@need
                                    Integer i = where.get(need);  //@look
                                    if (i != null) return new int[] {i, j};  //@look
                                    where.put((long) prices[j], j);  //@store
                                }
                                return new int[0];  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> pickTwo(vector<int>& prices, int budget) {
                                unordered_map<long long, int> where;  //@map
                                where.reserve(prices.size() * 2);  //@map
                                for (int j = 0; j < (int) prices.size(); j++) {  //@loop
                                    long long need = (long long) budget - prices[j];  //@need
                                    auto it = where.find(need);  //@look
                                    if (it != where.end()) return {it->second, j};  //@look
                                    where[prices[j]] = j;  //@store
                                }
                                return {};  //@none
                            }
                        };
                    """,
                    "c": """
                        // C has no built-in hash map, so here is a small one: open addressing
                        // with linear probing. Keys are prices, values are indices.
                        typedef struct { long long key; int val; bool used; } Slot;  //@table

                        static unsigned slotOf(long long key, unsigned mask) {  //@hash
                            unsigned long long h = (unsigned long long) key * 0x9E3779B97F4A7C15ULL;  //@hash
                            return (unsigned) (h >> 32) & mask;  //@hash
                        }  //@hash

                        int* pickTwo(int* prices, int pricesSize, int budget, int* returnSize) {
                            unsigned cap = 1;  //@cap
                            while (cap < 2u * pricesSize) cap <<= 1;  //@cap
                            Slot* where = calloc(cap, sizeof(Slot));  //@map
                            int* answer = malloc(2 * sizeof(int));
                            *returnSize = 0;
                            for (int j = 0; j < pricesSize; j++) {  //@loop
                                long long need = (long long) budget - prices[j];  //@need
                                unsigned s = slotOf(need, cap - 1);  //@look
                                while (where[s].used && where[s].key != need) s = (s + 1) & (cap - 1);  //@look
                                if (where[s].used) {  //@look
                                    answer[0] = where[s].val;  //@look
                                    answer[1] = j;  //@look
                                    *returnSize = 2;  //@look
                                    break;  //@look
                                }
                                s = slotOf(prices[j], cap - 1);  //@store
                                while (where[s].used && where[s].key != prices[j]) s = (s + 1) & (cap - 1);  //@store
                                where[s] = (Slot) {prices[j], j, true};  //@store
                            }
                            free(where);  //@free
                            return answer;  //@free
                        }
                    """,
                },
                lines=[
                    ("table", "A slot in the table: a key (a price), a value (its index) and whether it's taken."),
                    ("hash", "Turns a price into a slot number. Multiplying by a large odd constant scrambles the bits so nearby prices land far apart. The high bits are the most mixed, so we take those and keep the ones that fit the table (`& mask`)."),
                    ("cap", "The table gets a power-of-two size at least twice the number of prices. Half-empty tables keep the probe runs short, and a power of two lets `& (cap − 1)` stand in for `% cap`."),
                    ("map", "The map from a price to the index where we saw it. It starts empty.",
                     {"java": "Keys are `Long` because we look up `budget − price`, which can be past `int` range.",
                      "cpp": "Keys are `long long` because we look up `budget − price`, which can be past `int` range. `reserve` sizes the table up front so it doesn't rehash as it grows.",
                      "c": "`calloc` zeroes the table, so every slot starts unused."}),
                    ("loop", "One pass, left to right. `j` is the current gift, which is always the second gift of any pair it completes."),
                    ("need", "The only price that pairs with this one.",
                     {"java": "`(long) budget − prices[j]` is computed in 64 bits: 2 × 10⁹ − (−10⁹) = 3 × 10⁹ doesn't fit in `int`.",
                      "cpp": "Computed in 64 bits: 2 × 10⁹ − (−10⁹) = 3 × 10⁹ doesn't fit in `int`.",
                      "c": "Computed in 64 bits: 2 × 10⁹ − (−10⁹) = 3 × 10⁹ doesn't fit in `int`."}),
                    ("look", "Look the partner up **before** storing the current price, so a gift can never pair with itself. If the partner is there, its index is smaller than `j`, so `[partner, j]` is already in order.",
                     {"c": "Start at the partner's slot and step forward past slots holding other keys. Landing on a used slot with our key means found; landing on an empty slot means it isn't in the table."}),
                    ("store", "Not found yet: remember this price and its index for the gifts still to come.",
                     {"c": "Same probing as the lookup to find this price's slot (or an empty one), then write the entry."}),
                    ("free", "Free the table and return the answer."),
                    ("none", "Unreachable with valid input."),
                ],
                complexity=[
                    """
                    **Time O(n).** One pass over the prices, and each step does one lookup and at most one
                    insert, each O(1) on average for a hash map.

                    **Space O(n).** In the worst case the pair is the last two gifts, so nearly every price
                    goes into the map first.

                    "On average" matters: a hash map can degrade when many keys collide, but with a decent hash
                    function (every standard library has one) that doesn't happen on real inputs.
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - When the partner of an item is **fully determined** (here `budget − price`), stop searching
              for pairs and start **looking up** the partner. A hash map makes each lookup O(1).
            - **Look up before you insert** when an item must not pair with itself.
            - Store whatever the answer needs as the map's value. We needed indices, so the map goes
              price → index.
            - Sort + two pointers is the go-to when the input is already sorted (O(1) extra space), but
              sorting first costs O(n log n) and loses the original positions unless you carry them along.
            - In fixed-width languages, check whether a subtraction like `budget − price` can overflow, and
              use 64-bit integers when it can.
            """
        ],
    )


# ---------------------------------------------------------------------------- divisible-pairs


@problem
def divisible_pairs():
    nums, k = [4, 7, 2, 5, 9, 1], 3
    rem = [x % k for x in nums]
    brute_total = sum((nums[i] + nums[j]) % k == 0 for i in range(len(nums)) for j in range(i + 1, len(nums)))
    assert brute_total == 6

    # Brute force, one row per i.
    w1 = Steps("Try every pair i < j and test the sum.")
    w1.step("Six numbers, k = 3. Each i is paired with every j after it.", Row(nums, slots=True))
    total = 0
    for i in range(len(nums) - 1):
        good = [j for j in range(i + 1, len(nums)) if (nums[i] + nums[j]) % k == 0]
        total += len(good)
        st = {x: "dim" for x in range(i)}
        st[i] = "active"
        for j in range(i + 1, len(nums)):
            st[j] = "answer" if j in good else "mark"
        sums = ", ".join(f"{nums[i]}+{nums[j]}={nums[i] + nums[j]}{' ✓' if j in good else ''}" for j in range(i + 1, len(nums)))
        w1.step(f"i = {i}: {sums}. Pairs so far: {total}.", Row(nums, st=st, ptr={"i": i}, slots=True), Vars(pairs=total))
    w1.step(f"Every pair checked: {total}.", Row(nums, slots=True), result=total)

    # Buckets.
    count = [rem.count(r) for r in range(k)]
    w2 = Steps("Sort the numbers into remainder groups, then multiply group sizes.")
    w2.step("Replace each number by its remainder mod 3. Only remainders decide divisibility.", Row(nums, label="nums"), Row(rem, label="remainder"))
    w2.step(f"Count each remainder: {count[0]} with 0, {count[1]} with 1, {count[2]} with 2.", Row(count, label="count[r]", slots=True))
    w2.step("Remainder 0 pairs with remainder 0: choose 2 of the 1 number there, 1·0/2 = 0 pairs.", Row(count, st={0: "active"}, label="count[r]", slots=True), Vars(pairs=0))
    w2.step(f"Remainder 1 pairs with remainder 2 (1 + 2 = 3): {count[1]} × {count[2]} = {count[1] * count[2]} pairs.", Row(count, st={1: "active", 2: "active"}, label="count[r]", slots=True), Vars(pairs=count[1] * count[2]))
    w2.step("k = 3 is odd, so there is no 'half' group pairing with itself. Total 6.", Row(count, label="count[r]", slots=True), result=6)

    # One pass.
    w3 = Steps("For each number, add how many earlier numbers have the matching remainder, then record its own remainder.")
    seen = [0] * k
    total = 0
    w3.step("seen[r] counts earlier numbers with remainder r. All zero to start.", Row(nums, slots=True), Row(seen, label="seen[r]", slots=True), Vars(pairs=0))
    for j, x in enumerate(nums):
        r = x % k
        need = (k - r) % k
        add = seen[need]
        total += add
        st = {i: "dim" for i in range(j)}
        st[j] = "active"
        w3.step(f"{x} has remainder {r}, so it needs remainder {need}. seen[{need}] = {add}: +{add} → {total}. Then seen[{r}] += 1.",
                Row(nums, st=st, slots=True), Row(seen, st={need: "active"}, label="seen[r] (before)", slots=True), Vars(pairs=total))
        seen[r] += 1
    w3.step(f"Done: {total} pairs.", Row(seen, label="seen[r]", slots=True), result=total)

    sol(
        "divisible-pairs",
        summary="""
            Whether `a + b` is divisible by `k` depends only on the **remainders** `a % k` and `b % k`. So
            you never need the numbers themselves: count how many numbers have each remainder, and each new
            number pairs with every earlier number whose remainder completes it to a multiple of `k`.
        """,
        question=[
            """
            Count the pairs of positions `i < j` where `nums[i] + nums[j]` is a multiple of `k`.

            - **Pairs of positions.** Two equal numbers at different positions are two different
              elements, and `(i, j)` with `i < j` means each pair is counted once (not also as `(j, i)`),
              and no number pairs with itself.
            - **"Divisible by k"** means the remainder is 0: `(nums[i] + nums[j]) % k == 0`.
            - **k = 1** makes every sum divisible, so the answer is just n(n − 1)/2.
            - **Size:** up to 10⁵ numbers, so checking all ~5 × 10⁹ pairs is too slow.
            - **The answer can be huge:** with 10⁵ numbers that all work, it's about 5 × 10⁹, more than a
              32-bit `int` holds. That's why the return type is `long`. Also, two numbers near 10⁹ add up to
              2 × 10⁹, right at the `int` limit, so in Java, C++ and C, add them as 64-bit values.
            """
        ],
        think=[
            """
            Take `nums = [4, 7, 2, 5, 9, 1]` and `k = 3`.

            Checking pairs by hand: 4 + 2 = 6 ✓, 4 + 5 = 9 ✓, 7 + 2 = 9 ✓, 7 + 5 = 12 ✓, 2 + 1 = 3 ✓,
            5 + 1 = 6 ✓. Six pairs. But look at *why* each one works. Write every number as its remainder
            when divided by 3:
            """,
            fig(Row(nums, label="nums"), Row(rem, label="nums[i] % 3"),
                caption="4 → 1, 7 → 1, 2 → 2, 5 → 2, 9 → 0, 1 → 1."),
            """
            Every working pair is a **1 with a 2** (1 + 2 = 3, a multiple of 3). And that's the whole rule:
            adding two numbers adds their remainders, so `a + b` is a multiple of `k` exactly when
            `a % k + b % k` is 0 or `k`.

            So for a number with remainder `r`, the partners it needs have remainder:

            - `k − r`, if `r` isn't 0 (here 1 needs 2, and 2 needs 1);
            - `0`, if `r` is 0 (a multiple of `k` only pairs with another multiple of `k`).

            Both cases are `(k − r) % k`. The 9 (remainder 0) would need another remainder-0 number, and
            there isn't one, so it's in no pair.

            Once you see that, the actual numbers stop mattering. Three numbers have remainder 1 and two
            have remainder 2, so there are 3 × 2 = 6 pairs, without looking at a single sum.
            """,
        ],
        approaches=[
            approach(
                "Check every pair",
                "brute",
                "O(n²)",
                "O(1)",
                idea=[
                    """
                    Loop over every pair `i < j`, add the two numbers, and count the sums whose remainder is 0.
                    It's the definition of the problem turned straight into code.
                    """
                ],
                walk=w1,
                build=[
                    "Start a counter `total = 0` (64-bit, since the answer can exceed 2³¹).",
                    "Loop `i` over every index, and `j` from `i + 1` to the end.",
                    "If `(nums[i] + nums[j]) % k == 0`, add 1 to `total`. Add as 64-bit in Java, C++ and C.",
                    "Return `total`.",
                ],
                code={
                    "python": """
                        class Solution:
                            def countDivisiblePairs(self, nums: List[int], k: int) -> int:
                                n = len(nums)
                                total = 0  #@total
                                for i in range(n):  #@loops
                                    for j in range(i + 1, n):  #@loops
                                        if (nums[i] + nums[j]) % k == 0:  #@test
                                            total += 1  #@test
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countDivisiblePairs(int[] nums, int k) {
                                int n = nums.length;
                                long total = 0;  //@total
                                for (int i = 0; i < n; i++) {  //@loops
                                    for (int j = i + 1; j < n; j++) {  //@loops
                                        if (((long) nums[i] + nums[j]) % k == 0) {  //@test
                                            total++;  //@test
                                        }
                                    }
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countDivisiblePairs(vector<int>& nums, int k) {
                                int n = nums.size();
                                long long total = 0;  //@total
                                for (int i = 0; i < n; i++) {  //@loops
                                    for (int j = i + 1; j < n; j++) {  //@loops
                                        if (((long long) nums[i] + nums[j]) % k == 0) {  //@test
                                            total++;  //@test
                                        }
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countDivisiblePairs(int* nums, int numsSize, int k) {
                            long long total = 0;  //@total
                            for (int i = 0; i < numsSize; i++) {  //@loops
                                for (int j = i + 1; j < numsSize; j++) {  //@loops
                                    if (((long long) nums[i] + nums[j]) % k == 0) {  //@test
                                        total++;  //@test
                                    }
                                }
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("total", "The running count of good pairs. It must be 64-bit: up to ~5 × 10⁹ pairs can qualify."),
                    ("loops", "Every pair of positions with `i < j`: each pair once, never a number with itself."),
                    ("test", "A sum divisible by `k` leaves remainder 0. Count it.",
                     {"java": "`(long)` makes the addition 64-bit: 10⁹ + 10⁹ is right at the edge of `int`.",
                      "cpp": "`(long long)` makes the addition 64-bit: 10⁹ + 10⁹ is right at the edge of `int`.",
                      "c": "`(long long)` makes the addition 64-bit: 10⁹ + 10⁹ is right at the edge of `int`."}),
                    ("ret", "Every pair has been checked."),
                ],
                complexity=[
                    """
                    **Time O(n²):** n(n − 1)/2 pairs, about 5 × 10⁹ for n = 10⁵.

                    **Space O(1):** a counter and two loop variables.
                    """
                ],
                limits=[
                    """
                    Each number gets compared with every other number one by one, even though all it cares
                    about is *how many* earlier numbers have one particular remainder. That count can be kept
                    up to date instead of rediscovered, which is what the next two approaches do.
                    """
                ],
                slow=True,
            ),
            approach(
                "Count remainders, then pair up the groups",
                "better",
                "O(n + k)",
                "O(k)",
                idea=[
                    """
                    Put every number into a group by its remainder: `count[r]` = how many numbers have
                    remainder `r`. Then count pairs **between groups** with multiplication:

                    - Remainder `r` with remainder `k − r` (for `0 < r < k − r`): every number in one group
                      pairs with every number in the other, `count[r] × count[k − r]` pairs.
                    - Remainder 0 with itself: choose any 2 of the `count[0]` numbers,
                      `count[0] × (count[0] − 1) / 2` pairs.
                    - If `k` is even, remainder `k/2` also pairs with itself (k/2 + k/2 = k): another
                      "choose 2".

                    The loop over `r` stops before the middle, so each pair of groups is counted once.
                    """
                ],
                walk=w2,
                build=[
                    "Make an array `count` of size `k`, all zeros, and add 1 to `count[x % k]` for every `x`.",
                    "Start `total` with the remainder-0 pairs: `c0 × (c0 − 1) / 2`.",
                    "For `r = 1, 2, …` while `r < k − r`, add `count[r] × count[k − r]`.",
                    "If `k` is even, add the pairs inside the middle group: `c × (c − 1) / 2` with `c = count[k/2]`.",
                    "Return `total`. Do the multiplications in 64 bits: 5 × 10⁴ × 5 × 10⁴ is already past `int`.",
                ],
                code={
                    "python": """
                        class Solution:
                            def countDivisiblePairs(self, nums: List[int], k: int) -> int:
                                count = [0] * k  #@count
                                for x in nums:  #@count
                                    count[x % k] += 1  #@count
                                total = count[0] * (count[0] - 1) // 2  #@zero
                                r = 1  #@pairs
                                while r < k - r:  #@pairs
                                    total += count[r] * count[k - r]  #@pairs
                                    r += 1  #@pairs
                                if k % 2 == 0:  #@half
                                    c = count[k // 2]  #@half
                                    total += c * (c - 1) // 2  #@half
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countDivisiblePairs(int[] nums, int k) {
                                long[] count = new long[k];  //@count
                                for (int x : nums) count[x % k]++;  //@count
                                long total = count[0] * (count[0] - 1) / 2;  //@zero
                                for (int r = 1; r < k - r; r++) {  //@pairs
                                    total += count[r] * count[k - r];  //@pairs
                                }
                                if (k % 2 == 0) {  //@half
                                    long c = count[k / 2];  //@half
                                    total += c * (c - 1) / 2;  //@half
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countDivisiblePairs(vector<int>& nums, int k) {
                                vector<long long> count(k, 0);  //@count
                                for (int x : nums) count[x % k]++;  //@count
                                long long total = count[0] * (count[0] - 1) / 2;  //@zero
                                for (int r = 1; r < k - r; r++) {  //@pairs
                                    total += count[r] * count[k - r];  //@pairs
                                }
                                if (k % 2 == 0) {  //@half
                                    long long c = count[k / 2];  //@half
                                    total += c * (c - 1) / 2;  //@half
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countDivisiblePairs(int* nums, int numsSize, int k) {
                            long long* count = calloc(k, sizeof(long long));  //@count
                            for (int i = 0; i < numsSize; i++) count[nums[i] % k]++;  //@count
                            long long total = count[0] * (count[0] - 1) / 2;  //@zero
                            for (int r = 1; r < k - r; r++) {  //@pairs
                                total += count[r] * count[k - r];  //@pairs
                            }
                            if (k % 2 == 0) {  //@half
                                long long c = count[k / 2];  //@half
                                total += c * (c - 1) / 2;  //@half
                            }
                            free(count);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("count", "Group the numbers by remainder. `count[r]` is the size of group `r`. The values are 0 or more, so `x % k` is never negative.",
                     {"java": "`long[]` so the products below are already 64-bit.", "cpp": "`long long` so the products below are already 64-bit.", "c": "`calloc` gives `k` zeroed counters, 64-bit so the products below can't overflow."}),
                    ("zero", "Multiples of `k` pair only with each other. Any 2 of the `count[0]` of them work: c·(c − 1)/2 ways to choose 2."),
                    ("pairs", "Group `r` pairs with group `k − r`. Stopping at `r < k − r` visits each pair of groups once: (1, k−1), (2, k−2), … up to the middle."),
                    ("half", "When `k` is even, the middle group `k/2` pairs with itself (k/2 + k/2 = k), the same choose-2 count as group 0. For odd `k` there is no middle group."),
                    ("ret", "All the groups are accounted for.", {"c": "Free the counters before returning."}),
                ],
                complexity=[
                    """
                    **Time O(n + k):** one pass to fill the groups, then a sweep over about k/2 remainders.

                    **Space O(k):** the `count` array, up to 10⁵ entries.
                    """
                ],
                limits=[
                    """
                    This is already as fast as the problem allows. Its weakness is **correctness risk**: it
                    needs two special cases (remainder 0 and remainder k/2) and an exact loop bound, and
                    forgetting either one gives wrong answers only on some inputs. The next approach gets the
                    same speed with no special cases at all, because it never has to reason about pairs of
                    groups.
                    """
                ],
            ),
            approach(
                "One pass, counting remainders seen so far",
                "best",
                "O(n + k)",
                "O(k)",
                idea=[
                    """
                    This is the complement idea from pair-sum problems, applied to remainders. Walk left to
                    right, keeping `seen[r]`: how many **earlier** numbers have remainder `r`.

                    At each number with remainder `r`, its partners are the earlier numbers with remainder
                    `(k − r) % k`, and there are exactly `seen[(k − r) % k]` of them. Add that, then record the
                    current number: `seen[r] += 1`.

                    Every pair `i < j` is counted exactly once, at `j`, when `i` is already in `seen`. The
                    special cases disappear: a remainder-0 number looks up `seen[0]` (other multiples of k),
                    and with even k a remainder-k/2 number looks up `seen[k/2]`. Because the current number is
                    recorded **after** the lookup, it never pairs with itself.
                    """
                ],
                walk=w3,
                build=[
                    "Make `seen`, an array of `k` zeros, and `total = 0` (64-bit).",
                    "For each number `x`: compute `r = x % k` and the needed remainder `need = (k − r) % k`.",
                    "Add `seen[need]` to `total`: one pair for each earlier partner.",
                    "Then do `seen[r] += 1`, so later numbers can pair with this one.",
                    "Return `total`.",
                ],
                code={
                    "python": """
                        class Solution:
                            def countDivisiblePairs(self, nums: List[int], k: int) -> int:
                                seen = [0] * k  #@seen
                                total = 0  #@seen
                                for x in nums:  #@loop
                                    r = x % k  #@r
                                    total += seen[(k - r) % k]  #@add
                                    seen[r] += 1  #@record
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countDivisiblePairs(int[] nums, int k) {
                                int[] seen = new int[k];  //@seen
                                long total = 0;  //@seen
                                for (int x : nums) {  //@loop
                                    int r = x % k;  //@r
                                    total += seen[(k - r) % k];  //@add
                                    seen[r]++;  //@record
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countDivisiblePairs(vector<int>& nums, int k) {
                                vector<int> seen(k, 0);  //@seen
                                long long total = 0;  //@seen
                                for (int x : nums) {  //@loop
                                    int r = x % k;  //@r
                                    total += seen[(k - r) % k];  //@add
                                    seen[r]++;  //@record
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countDivisiblePairs(int* nums, int numsSize, int k) {
                            int* seen = calloc(k, sizeof(int));  //@seen
                            long long total = 0;  //@seen
                            for (int i = 0; i < numsSize; i++) {  //@loop
                                int r = nums[i] % k;  //@r
                                total += seen[(k - r) % k];  //@add
                                seen[r]++;  //@record
                            }
                            free(seen);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("seen", "`seen[r]` counts the numbers already passed with remainder `r`; `total` is the answer so far (64-bit). A single group never exceeds 10⁵, so the counts themselves fit in `int`."),
                    ("loop", "One pass over the numbers. The current number is always the **second** element of the pairs it completes."),
                    ("r", "Its remainder, from 0 to k − 1 (the numbers are never negative, so `%` gives no negative results)."),
                    ("add", "The partners it needs have remainder `(k − r) % k`: `k − r` normally, and 0 when `r` is 0 (that's what the outer `% k` handles). Every one of them seen so far makes a pair."),
                    ("record", "Only now add the current number to `seen`, so it can't pair with itself."),
                    ("ret", "Every pair was counted once, at its right-hand element.", {"c": "Free the counters first."}),
                ],
                complexity=[
                    """
                    **Time O(n + k):** O(k) to create `seen`, then O(1) work per number.

                    **Space O(k)** for `seen`. If `k` were huge compared with n (say 10¹⁸), you'd use a hash map
                    from remainder to count instead, which only stores remainders that actually occur:
                    O(n) time and O(min(n, k)) space.
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - For "is the sum divisible by k?", work with **remainders**. `(a + b) % k` depends only on
              `a % k` and `b % k`.
            - The partner remainder of `r` is `(k − r) % k`, which handles `r = 0` without a special case.
            - "Count earlier partners, then record yourself" counts each pair exactly once and never pairs an
              element with itself. It's the counting version of the two-sum lookup.
            - When the answer counts pairs among up to 10⁵ items, it can exceed 2³¹. Use 64-bit totals.
            """
        ],
    )


# ---------------------------------------------------------------------------- four-lists-zero


@problem
def four_lists_zero():
    from collections import Counter
    a, b, c, d = [2, -1, 0], [1, -2, 3], [-3, 0, 1], [1, 2, -1]
    brute = sum(1 for w in a for x in b for y in c for z in d if w + x + y + z == 0)
    ab = Counter(x + y for x in a for y in b)
    best = sum(ab[-(x + y)] for x in c for y in d)
    assert brute == best

    grid_ab = [[x + y for y in b] for x in a]
    grid_cd = [[x + y for y in d] for x in c]

    w2 = Steps("Fix a, b and c; the last number is decided, so look it up in a count of d.")
    dcount = Counter(d)
    w2.step(f"Count the values of d: {dict(sorted(dcount.items()))}. For every (a, b, c), the needed d is −(a + b + c).", Row(d, label="d"), Row([f"{v}×{n}" for v, n in sorted(dcount.items())], label="d value × count"))
    total = 0
    shown = 0
    for x in a:
        for y in b:
            for z in c:
                need = -(x + y + z)
                got = dcount.get(need, 0)
                total += got
                if got and shown < 6:
                    shown += 1
                    w2.step(f"a = {x}, b = {y}, c = {z}: need d = {need}, which appears {got} time{'s' if got > 1 else ''}. Total {total}.",
                            Row(a, st={a.index(x): "active"}, label="a"), Row(b, st={b.index(y): "active"}, label="b"), Row(c, st={c.index(z): "active"}, label="c"), Row(d, st={i: "answer" for i, v in enumerate(d) if v == need}, label="d"))
    w2.step(f"All {len(a) ** 3} triples done (most found no partner): {total} tuples.", Row(d, label="d"), result=total)
    assert total == brute

    w3 = Steps("Count every a + b sum. Then each c + d needs the a + b sum that cancels it.")
    w3.step("All a + b sums: n² of them. Rows are a, columns are b.", Grid(grid_ab), Vars(a=str(a), b=str(b)))
    w3.step(f"Count them: {dict(sorted(ab.items()))}.", Row([f"{s}×{n}" for s, n in sorted(ab.items())], label="a + b sum × count"))
    total = 0
    for i, x in enumerate(c):
        for j, y in enumerate(d):
            s = x + y
            got = ab.get(-s, 0)
            total += got
            keys = sorted(ab)
            st = {keys.index(-s): "answer"} if got else {}
            w3.step(f"c = {x}, d = {y}: c + d = {s}, needs a + b = {-s}" + (f", which occurs {got} time{'s' if got > 1 else ''}. Total {total}." if got else ", which never occurs."),
                    Grid(grid_cd, st={(i, j): "answer" if got else "active"}, label="c + d sums"), Row([f"{k}×{ab[k]}" for k in keys], st=st, label="a + b sum × count"))
    w3.step(f"Answer: {total}.", Grid(grid_cd, label="c + d sums"), result=total)
    assert total == brute

    w1 = Steps("Four nested loops: every choice of one number from each list.")
    total = 0
    hits = []
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            for k, z in enumerate(c):
                for l, v in enumerate(d):
                    if x + y + z + v == 0:
                        hits.append((i, j, k, l))
    w1.step(f"With n = {len(a)} there are {len(a)}⁴ = {len(a) ** 4} tuples to try.", Row(a, label="a"), Row(b, label="b"), Row(c, label="c"), Row(d, label="d"))
    for t, (i, j, k, l) in enumerate(hits[:5]):
        w1.step(f"({i}, {j}, {k}, {l}): {a[i]} + {b[j]} + {c[k]} + {d[l]} = 0. Count {t + 1}.",
                Row(a, st={i: "answer"}, label="a"), Row(b, st={j: "answer"}, label="b"), Row(c, st={k: "answer"}, label="c"), Row(d, st={l: "answer"}, label="d"))
    w1.step(f"After all {len(a) ** 4} tuples: {len(hits)} add up to zero.", Row(a, label="a"), Row(b, label="b"), Row(c, label="c"), Row(d, label="d"), result=len(hits))

    sol(
        "four-lists-zero",
        summary="""
            Split the four lists into two halves. Count every sum `a[i] + b[j]` in a hash map (n² sums), then
            for every `c[k] + d[l]` add how many first-half sums cancel it. Four nested loops become two
            separate double loops: O(n⁴) becomes O(n²).
        """,
        question=[
            """
            Pick one number from each of four lists, `a`, `b`, `c` and `d` (all of length `n`). Count the
            choices whose four numbers add up to exactly 0.

            - **Choices are positions, not values.** If `d` contains 2 twice, a tuple using the first 2
              and a tuple using the second 2 are different tuples and both count.
            - **The order is fixed:** the first number always comes from `a`, the second from `b`, and so
              on. You never mix lists.
            - **Size:** n ≤ 500, so there are up to 500⁴ = 6.25 × 10¹⁰ tuples. Even at a billion checks a
              second that takes over a minute.
            - **The count can be huge:** if every tuple works it's 6.25 × 10¹⁰, which needs a 64-bit
              integer. The values themselves are at most 2²⁸, so any sum of two or four of them stays
              within ±2³⁰ and fits in an `int`.
            """
        ],
        think=[
            """
            Take `a = [2, −1, 0]`, `b = [1, −2, 3]`, `c = [−3, 0, 1]`, `d = [1, 2, −1]`.

            Brute force means 3⁴ = 81 tuples. Instead, think about what each part of a tuple **needs**.
            Once you've chosen from `a`, `b` and `c`, the number from `d` is forced: it must be
            `−(a + b + c)`. That's the complement idea: a lookup can replace the fourth loop.

            Push the idea further. Group the tuple as **(a + b) + (c + d) = 0**. Once you know `c + d`, the
            first half must sum to exactly `−(c + d)`. And there are only n² possible first halves:
            """,
            fig(Grid([[x + y for y in b] for x in a]), Grid([[x + y for y in d] for x in c]),
                caption="Left: every a + b (rows a, columns b). Right: every c + d (rows c, columns d)."),
            """
            So the question becomes: for each sum on the right, how many sums on the left are its
            negative? For example, c = 1 and d = −1 give `c + d = 0`, which needs `a + b = 0`. The left grid
            has two 0s (a = 2 with b = −2, and a = −1 with b = 1), so that single right-hand pair completes
            **two** tuples. To answer that instantly for every right-hand sum, first build a table of **how
            many times each left sum occurs**; then each right sum is one lookup.

            That is "meet in the middle": instead of one search over n⁴ tuples, do two searches over n²
            halves and join them with a hash map.
            """,
        ],
        approaches=[
            approach(
                "Try every tuple",
                "brute",
                "O(n⁴)",
                "O(1)",
                idea=["Four nested loops pick one index from each list; count the tuples that sum to zero."],
                walk=w1,
                build=[
                    "Set `total = 0` (64-bit).",
                    "Nest four loops: `i` over `a`, `j` over `b`, `k` over `c`, `l` over `d`.",
                    "If `a[i] + b[j] + c[k] + d[l] == 0`, add 1.",
                    "Return `total`.",
                ],
                code={
                    "python": """
                        class Solution:
                            def countZeroQuads(self, a: List[int], b: List[int], c: List[int], d: List[int]) -> int:
                                total = 0  #@total
                                for w in a:  #@loops
                                    for x in b:  #@loops
                                        for y in c:  #@loops
                                            for z in d:  #@loops
                                                if w + x + y + z == 0:  #@test
                                                    total += 1  #@test
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countZeroQuads(int[] a, int[] b, int[] c, int[] d) {
                                long total = 0;  //@total
                                for (int w : a)  //@loops
                                    for (int x : b)  //@loops
                                        for (int y : c)  //@loops
                                            for (int z : d)  //@loops
                                                if (w + x + y + z == 0) total++;  //@test
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countZeroQuads(vector<int>& a, vector<int>& b, vector<int>& c, vector<int>& d) {
                                long long total = 0;  //@total
                                for (int w : a)  //@loops
                                    for (int x : b)  //@loops
                                        for (int y : c)  //@loops
                                            for (int z : d)  //@loops
                                                if (w + x + y + z == 0) total++;  //@test
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countZeroQuads(int* a, int aSize, int* b, int bSize, int* c, int cSize, int* d, int dSize) {
                            long long total = 0;  //@total
                            for (int i = 0; i < aSize; i++)  //@loops
                                for (int j = 0; j < bSize; j++)  //@loops
                                    for (int k = 0; k < cSize; k++)  //@loops
                                        for (int l = 0; l < dSize; l++)  //@loops
                                            if (a[i] + b[j] + c[k] + d[l] == 0) total++;  //@test
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("total", "The number of zero tuples, 64-bit because it can reach n⁴."),
                    ("loops", "One loop per list: every combination of one element from each."),
                    ("test", "Four values of at most 2²⁸ in size sum to at most 2³⁰, so plain `int` addition is safe here."),
                    ("ret", "All n⁴ tuples were checked."),
                ],
                complexity=["**Time O(n⁴):** 6.25 × 10¹⁰ checks at n = 500. **Space O(1).**"],
                limits=[
                    """
                    The innermost loop searches `d` for one specific value, `−(a + b + c)`, by checking every
                    element. That search is exactly what a hash map does in O(1), which removes a whole loop.
                    """
                ],
                slow=700,
            ),
            approach(
                "Three loops and a count of d",
                "better",
                "O(n³)",
                "O(n)",
                idea=[
                    """
                    The fourth number is forced: `d` must be `−(a + b + c)`. So count how often each value
                    appears in `d` (a hash map from value to count), loop over `a`, `b` and `c`, and add the
                    count of the needed value. Duplicates in `d` are handled by the count: two copies of the
                    needed value give two tuples.
                    """
                ],
                walk=w2,
                build=[
                    "Build `countD`: value → how many times it appears in `d`.",
                    "Loop over `a`, `b` and `c` (three nested loops).",
                    "For each triple, add `countD[−(a + b + c)]` (0 if missing) to `total`.",
                    "Return `total`.",
                ],
                code={
                    "python": """
                        from collections import Counter

                        class Solution:
                            def countZeroQuads(self, a: List[int], b: List[int], c: List[int], d: List[int]) -> int:
                                count_d = Counter(d)  #@count
                                total = 0
                                for w in a:  #@loops
                                    for x in b:  #@loops
                                        for y in c:  #@loops
                                            total += count_d[-(w + x + y)]  #@look
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countZeroQuads(int[] a, int[] b, int[] c, int[] d) {
                                Map<Integer, Integer> countD = new HashMap<>();  //@count
                                for (int z : d) countD.merge(z, 1, Integer::sum);  //@count
                                long total = 0;
                                for (int w : a)  //@loops
                                    for (int x : b)  //@loops
                                        for (int y : c)  //@loops
                                            total += countD.getOrDefault(-(w + x + y), 0);  //@look
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countZeroQuads(vector<int>& a, vector<int>& b, vector<int>& c, vector<int>& d) {
                                unordered_map<int, int> countD;  //@count
                                for (int z : d) countD[z]++;  //@count
                                long long total = 0;
                                for (int w : a)  //@loops
                                    for (int x : b)  //@loops
                                        for (int y : c) {  //@loops
                                            auto it = countD.find(-(w + x + y));  //@look
                                            if (it != countD.end()) total += it->second;  //@look
                                        }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* x, const void* y) {  //@cmp
                            int p = *(const int*) x, q = *(const int*) y;  //@cmp
                            return (p > q) - (p < q);  //@cmp
                        }  //@cmp

                        // How many times v appears in the sorted array s of length n.
                        static int occurrences(const int* s, int n, int v) {  //@occ
                            int lo = 0, hi = n;  //@occ
                            while (lo < hi) {  //@occ
                                int mid = (lo + hi) / 2;  //@occ
                                if (s[mid] < v) lo = mid + 1; else hi = mid;  //@occ
                            }  //@occ
                            int first = lo;  //@occ
                            hi = n;  //@occ
                            while (lo < hi) {  //@occ
                                int mid = (lo + hi) / 2;  //@occ
                                if (s[mid] <= v) lo = mid + 1; else hi = mid;  //@occ
                            }  //@occ
                            return lo - first;  //@occ
                        }  //@occ

                        long long countZeroQuads(int* a, int aSize, int* b, int bSize, int* c, int cSize, int* d, int dSize) {
                            int* sortedD = malloc(dSize * sizeof(int));  //@count
                            memcpy(sortedD, d, dSize * sizeof(int));  //@count
                            qsort(sortedD, dSize, sizeof(int), cmpInt);  //@count
                            long long total = 0;
                            for (int i = 0; i < aSize; i++)  //@loops
                                for (int j = 0; j < bSize; j++)  //@loops
                                    for (int k = 0; k < cSize; k++)  //@loops
                                        total += occurrences(sortedD, dSize, -(a[i] + b[j] + c[k]));  //@look
                            free(sortedD);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("cmp", "A comparator for `qsort`. `(p > q) − (p < q)` is −1, 0 or 1 and can't overflow the way `p − q` can."),
                    ("occ", "C has no hash map, and `d` is tiny (n ≤ 500), so a sorted copy plus binary search does the counting: find where `v` starts and where it ends; the difference is how many copies there are. Each call is O(log n)."),
                    ("count", "Count each value of `d` once, up front.",
                     {"python": "`Counter` maps each value to its number of copies and returns 0 for values it hasn't seen.",
                      "java": "`merge(z, 1, Integer::sum)` adds 1 to `z`'s count, starting it at 1 when it's new.",
                      "cpp": "`countD[z]++` creates the entry at 0 when it's new, then adds 1.",
                      "c": "Sort a copy of `d` (we don't change the input) so copies of a value sit next to each other."}),
                    ("loops", "Three loops choose the first three numbers, n³ triples."),
                    ("look", "The fourth number must be `−(a + b + c)`. Every copy of it in `d` completes a tuple, so add its count (0 if it isn't there).",
                     {"c": "Here the count comes from two binary searches: O(log n) instead of O(1), still far better than scanning `d`."}),
                    ("ret", "Return the total.", {"c": "Free the sorted copy first."}),
                ],
                complexity=[
                    """
                    **Time O(n³):** n³ = 1.25 × 10⁸ lookups for n = 500, each O(1) on average (O(log n) in the
                    C version). That's borderline: often a few seconds, too slow for a 1-second limit in most
                    languages.

                    **Space O(n)** for the counts of `d`.
                    """
                ],
                limits=[
                    """
                    We used the "forced last number" trick once, on one list. The same trick works on **pairs**
                    of lists: once `c + d` is known, `a + b` is forced. That balances the work as n² + n²
                    instead of n³ + n.
                    """
                ],
                slow=1500,
            ),
            approach(
                "Meet in the middle: count a + b, look up −(c + d)",
                "best",
                "O(n²)",
                "O(n²)",
                idea=[
                    """
                    Write the condition as `(a[i] + b[j]) = −(c[k] + d[l])`.

                    1. Loop over all n² pairs from `a` and `b`, and count each sum in a hash map:
                       `sums[s]` = how many `(i, j)` give `a[i] + b[j] = s`.
                    2. Loop over all n² pairs from `c` and `d`. For `t = c[k] + d[l]`, every first-half pair
                       with sum `−t` completes a zero tuple, so add `sums[−t]`.

                    Two double loops replace four nested ones. Storing **counts** (not just "seen") matters:
                    several `(i, j)` can share a sum, and each is a different tuple.
                    """
                ],
                walk=w3,
                build=[
                    "Create a hash map `sums` from a sum to how many (i, j) pairs produce it.",
                    "Double loop over `a` and `b`: `sums[a[i] + b[j]] += 1`.",
                    "Double loop over `c` and `d`: add `sums[−(c[k] + d[l])]` (0 if absent) to `total`.",
                    "Return `total` (64-bit).",
                ],
                code={
                    "python": """
                        from collections import Counter

                        class Solution:
                            def countZeroQuads(self, a: List[int], b: List[int], c: List[int], d: List[int]) -> int:
                                sums = Counter(w + x for w in a for x in b)  #@first
                                total = 0  #@second
                                for y in c:  #@second
                                    for z in d:  #@second
                                        total += sums[-(y + z)]  #@look
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countZeroQuads(int[] a, int[] b, int[] c, int[] d) {
                                Map<Integer, Integer> sums = new HashMap<>();  //@first
                                for (int w : a)  //@first
                                    for (int x : b)  //@first
                                        sums.merge(w + x, 1, Integer::sum);  //@first
                                long total = 0;  //@second
                                for (int y : c)  //@second
                                    for (int z : d)  //@second
                                        total += sums.getOrDefault(-(y + z), 0);  //@look
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countZeroQuads(vector<int>& a, vector<int>& b, vector<int>& c, vector<int>& d) {
                                unordered_map<int, int> sums;  //@first
                                sums.reserve(a.size() * b.size() * 2);  //@first
                                for (int w : a)  //@first
                                    for (int x : b)  //@first
                                        sums[w + x]++;  //@first
                                long long total = 0;  //@second
                                for (int y : c)  //@second
                                    for (int z : d) {  //@second
                                        auto it = sums.find(-(y + z));  //@look
                                        if (it != sums.end()) total += it->second;  //@look
                                    }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        // A small hash map from a sum to its count: open addressing, linear probing.
                        typedef struct { int key; int count; bool used; } Slot;  //@table

                        static unsigned slotOf(int key, unsigned mask) {  //@hash
                            unsigned long long h = (unsigned long long) (long long) key * 0x9E3779B97F4A7C15ULL;  //@hash
                            return (unsigned) (h >> 32) & mask;  //@hash
                        }  //@hash

                        static Slot* find(Slot* t, unsigned mask, int key) {  //@find
                            unsigned s = slotOf(key, mask);  //@find
                            while (t[s].used && t[s].key != key) s = (s + 1) & mask;  //@find
                            return &t[s];  //@find
                        }  //@find

                        long long countZeroQuads(int* a, int aSize, int* b, int bSize, int* c, int cSize, int* d, int dSize) {
                            unsigned cap = 1;  //@cap
                            while (cap < 2u * aSize * bSize) cap <<= 1;  //@cap
                            Slot* sums = calloc(cap, sizeof(Slot));  //@first
                            for (int i = 0; i < aSize; i++)  //@first
                                for (int j = 0; j < bSize; j++) {  //@first
                                    Slot* e = find(sums, cap - 1, a[i] + b[j]);  //@first
                                    e->key = a[i] + b[j];  //@first
                                    e->used = true;  //@first
                                    e->count++;  //@first
                                }  //@first
                            long long total = 0;  //@second
                            for (int k = 0; k < cSize; k++)  //@second
                                for (int l = 0; l < dSize; l++) {  //@second
                                    Slot* e = find(sums, cap - 1, -(c[k] + d[l]));  //@look
                                    if (e->used) total += e->count;  //@look
                                }  //@second
                            free(sums);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("table", "One slot of the table: a sum, how many pairs produced it, and whether the slot is taken."),
                    ("hash", "Scrambles a sum into a slot number: multiply by a large odd constant, keep the well-mixed high bits, and mask down to the table size. Negative sums work too, since the cast reinterprets them as unsigned."),
                    ("find", "Returns the slot holding `key`, or the empty slot where it would go. It steps forward past slots that hold other keys (linear probing)."),
                    ("cap", "A power of two at least twice the n² entries, so the table stays at most half full and probe runs stay short."),
                    ("first", "First half: every `a[i] + b[j]`, counted. n² pairs, so at most n² different sums.",
                     {"python": "`Counter` over a generator of all n² sums builds the whole table in one line.",
                      "java": "`merge(sum, 1, Integer::sum)` increments the count (starting new sums at 1).",
                      "cpp": "`reserve` sizes the table for n² entries up front so it never rehashes; `sums[w + x]++` creates missing keys at 0 and increments.",
                      "c": "Find the sum's slot (existing or empty), claim it for this key, and add one to its count."}),
                    ("second", "Second half: every `c[k] + d[l]`."),
                    ("look", "To total zero, the first half must sum to `−(c + d)`. Each of the `sums[−(c + d)]` first-half pairs makes one tuple with this second-half pair.",
                     {"c": "If `find` lands on an empty slot, no first-half pair has that sum and nothing is added."}),
                    ("ret", "Every zero tuple was counted exactly once: at its (k, l), through the count of its (i, j).", {"c": "Free the table first."}),
                ],
                complexity=[
                    """
                    **Time O(n²):** n² inserts plus n² lookups, about 500,000 hash operations for n = 500.

                    **Space O(n²):** up to n² = 250,000 distinct first-half sums in the map.

                    Why not split 1 + 3 or 3 + 1? Then one side has n³ combinations. Splitting **evenly**, 2 + 2,
                    makes both sides as small as possible: that balance is the whole point of meeting in the
                    middle.
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - **Meet in the middle:** when a condition joins several independent choices, split the choices
              into two equal halves, enumerate each half, and join them with a hash map. Here n⁴ became
              2 · n².
            - The join stores **counts**, not just presence, because many first halves can share one sum
              and each one is a different answer.
            - The "forced last element" trick (look up what's missing instead of looping over it) is the
              same idea as Two Gifts, applied to sums of pairs.
            - Check value ranges before reaching for 64-bit: here the sums fit in `int`, but the **count**
              doesn't.
            """
        ],
    )


# ---------------------------------------------------------------------------- pairs-a-gap-apart


@problem
def pairs_a_gap_apart():
    from collections import Counter
    nums, k = [6, 2, 9, 4, 2, 11, 7], 2
    distinct = sorted(set(nums))
    want = sum(1 for x in set(nums) if x + k in set(nums))
    assert want == 4

    w1 = Steps("For each position, skip values already handled, then search the whole list for value + k.")
    total = 0
    w1.step("k = 2. Each distinct value x counts once if x + 2 is somewhere else in the list.", Row(nums, slots=True), Vars(pairs=0))
    for i, x in enumerate(nums):
        st = {i: "active"}
        if x in nums[:i]:
            first = nums.index(x)
            st[first] = "dim"
            w1.step(f"i = {i}: {x} already appeared at index {first}, so its pair (if any) was counted. Skip.", Row(nums, st=st, ptr={"i": i}, slots=True), Vars(pairs=total))
            continue
        hits = [j for j, y in enumerate(nums) if j != i and y == x + k]
        if hits:
            total += 1
            for j in hits:
                st[j] = "answer"
            st[i] = "answer"
            w1.step(f"i = {i}: is {x + k} anywhere else? Yes, at index {hits[0]}. Pair ({x}, {x + k}). Count {total}.", Row(nums, st=st, ptr={"i": i}, slots=True), Vars(pairs=total))
        else:
            w1.step(f"i = {i}: is {x + k} anywhere else? No.", Row(nums, st=st, ptr={"i": i}, slots=True), Vars(pairs=total))
    w1.step(f"Answer: {total}.", Row(nums, slots=True), result=total)

    w2 = Steps("Sort, then for each new value binary-search for value + k to its right.")
    s = sorted(nums)
    w2.step(f"Sorted: {s}. Copies of a value now sit together.", Row(s, slots=True), Vars(pairs=0))
    total = 0
    import bisect
    for i, x in enumerate(s):
        if i > 0 and s[i - 1] == x:
            w2.step(f"Index {i} is another {x}: same value as before, skip.", Row(s, st={i: "dim", i - 1: "dim"}, ptr={"i": i}, slots=True), Vars(pairs=total))
            continue
        j = bisect.bisect_left(s, x + k, i + 1)
        ok = j < len(s) and s[j] == x + k
        total += ok
        st = {t: "dim" for t in range(i + 1)}
        st[i] = "active"
        for t in range(i + 1, len(s)):
            st[t] = "mark"
        if ok:
            st[j] = "answer"
            st[i] = "answer"
        w2.step(f"x = {x}: binary-search {x + k} in indices {i + 1}…{len(s) - 1}: " + (f"found at {j}. Count {total}." if ok else "not there."), Row(s, st=st, ptr={"i": i, "j": j} if ok else {"i": i}, slots=True), Vars(pairs=total))
    w2.step(f"Answer: {total}.", Row(s, slots=True), result=total)

    w3 = Steps("Count every value once. Then each distinct value just asks: is value + k in the table?")
    cnt = Counter(nums)
    keys = list(cnt)
    w3.step("Count the values (a hash map from value to copies).", Row(nums, slots=True), Row([f"{v}×{cnt[v]}" for v in keys], label="value × copies"))
    total = 0
    for t, x in enumerate(keys):
        ok = (x + k) in cnt
        total += ok
        st = {t: "answer" if ok else "active"}
        if ok:
            st[keys.index(x + k)] = "answer"
        w3.step(f"{x}: is {x + k} in the table? " + (f"Yes. Pair ({x}, {x + k}). Count {total}." if ok else "No."), Row([f"{v}×{cnt[v]}" for v in keys], st=st, label="value × copies"), Vars(pairs=total))
    w3.step(f"Answer: {total}. With k = 0 we'd instead count values with 2 or more copies: just 2 here, so 1.", Row([f"{v}×{cnt[v]}" for v in keys], st={keys.index(2): "found"}, label="value × copies"), result=total)

    sol(
        "pairs-a-gap-apart",
        summary="""
            Because `y − x = k` fixes `y` once you know `x`, a distinct pair is really just a distinct value `x`
            whose partner `x + k` exists. Count the values once in a hash map; then each distinct value is a
            single lookup. The one twist is `k = 0`, where the partner is the value itself and you need a
            second copy.
        """,
        question=[
            """
            Count the **distinct** pairs of values `(x, y)` in the list with `y − x = k`.

            - **Distinct value pairs, not position pairs.** In `[3, 1, 4, 1, 5]` with k = 2, both 1s pair
              with the 3, but `(1, 3)` counts once. The answer is 2: `(1, 3)` and `(3, 5)`.
            - **The pair is ordered by the gap:** `y = x + k`, so `(1, 3)` and `(3, 1)` aren't two different
              pairs; only `(1, 3)` has `y − x = 2`.
            - **Different positions.** `x` and `y` must be two different elements. That only matters when
              **k = 0**: then `y = x`, so the value must appear **at least twice**. `[1, 3, 1, 5, 4]` with
              k = 0 has one pair, `(1, 1)`.
            - **k is never negative**, so `y ≥ x`.
            - **Size:** up to 10⁵ numbers, so comparing all pairs (10¹⁰) is too slow.
            """
        ],
        think=[
            """
            Take `nums = [6, 2, 9, 4, 2, 11, 7]` and `k = 2`.

            A pair is `(x, x + 2)`. Once you pick `x`, there's only one possible `y`. So instead of
            thinking about pairs, think about **values**: which values `x` have their partner `x + 2` in the
            list?
            """,
            fig(Row(distinct, label="distinct values"), Row([x + k for x in distinct], st={i: "answer" for i, x in enumerate(distinct) if x + k in set(nums)}, label="partner x + 2 (shaded = present)"),
                caption="2 → 4 ✓, 4 → 6 ✓, 6 → 8, 7 → 9 ✓, 9 → 11 ✓, 11 → 13. Four pairs."),
            """
            Two observations:

            1. **Duplicates don't matter** (when k > 0): the second 2 adds nothing new, because `(2, 4)` is
               already counted. So work with the **set** of distinct values.
            2. **For k = 0**, the partner of `x` is `x` itself, which is always "in the set". The real
               question becomes "does `x` appear at least twice?" Here only 2 does, so with k = 0 the answer
               would be 1. Keeping **counts** instead of just a set answers both questions with one table.
            """,
        ],
        approaches=[
            approach(
                "Search the list for each new value",
                "brute",
                "O(n²)",
                "O(1)",
                idea=[
                    """
                    Go through the positions. For position `i` with value `x`:

                    - If `x` already appeared at an earlier position, skip it: that value's pair was already
                      decided, and counting it again would break "distinct".
                    - Otherwise scan every other position `j ≠ i` for the value `x + k`. If you find one,
                      count the pair.

                    Requiring `j ≠ i` is what makes k = 0 work: the value needs a *second* copy.
                    """
                ],
                walk=w1,
                build=[
                    "Loop `i` over every position, with `x = nums[i]`.",
                    "Scan positions `0 … i − 1`; if any equals `x`, skip this `i` (already handled).",
                    "Scan all positions `j ≠ i`; if any equals `x + k`, add 1 and stop scanning.",
                    "Return the count.",
                ],
                code={
                    "python": """
                        class Solution:
                            def countGapPairs(self, nums: List[int], k: int) -> int:
                                n = len(nums)
                                total = 0
                                for i in range(n):  #@outer
                                    x = nums[i]  #@outer
                                    if any(nums[p] == x for p in range(i)):  #@dup
                                        continue  #@dup
                                    if any(j != i and nums[j] == x + k for j in range(n)):  #@search
                                        total += 1  #@search
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countGapPairs(int[] nums, int k) {
                                int n = nums.length, total = 0;
                                for (int i = 0; i < n; i++) {  //@outer
                                    int x = nums[i];  //@outer
                                    boolean seenBefore = false;  //@dup
                                    for (int p = 0; p < i && !seenBefore; p++) seenBefore = nums[p] == x;  //@dup
                                    if (seenBefore) continue;  //@dup
                                    for (int j = 0; j < n; j++) {  //@search
                                        if (j != i && nums[j] == x + k) {  //@search
                                            total++;  //@search
                                            break;  //@search
                                        }
                                    }
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countGapPairs(vector<int>& nums, int k) {
                                int n = nums.size(), total = 0;
                                for (int i = 0; i < n; i++) {  //@outer
                                    int x = nums[i];  //@outer
                                    bool seenBefore = false;  //@dup
                                    for (int p = 0; p < i && !seenBefore; p++) seenBefore = nums[p] == x;  //@dup
                                    if (seenBefore) continue;  //@dup
                                    for (int j = 0; j < n; j++) {  //@search
                                        if (j != i && nums[j] == x + k) {  //@search
                                            total++;  //@search
                                            break;  //@search
                                        }
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countGapPairs(int* nums, int numsSize, int k) {
                            int total = 0;
                            for (int i = 0; i < numsSize; i++) {  //@outer
                                int x = nums[i];  //@outer
                                bool seenBefore = false;  //@dup
                                for (int p = 0; p < i && !seenBefore; p++) seenBefore = nums[p] == x;  //@dup
                                if (seenBefore) continue;  //@dup
                                for (int j = 0; j < numsSize; j++) {  //@search
                                    if (j != i && nums[j] == x + k) {  //@search
                                        total++;  //@search
                                        break;  //@search
                                    }
                                }
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("outer", "Consider each position's value as the smaller member `x` of a pair."),
                    ("dup", "Has this value already shown up to the left? Then it was already handled, at its first position. Skipping it keeps each value pair counted once."),
                    ("search", "Look for the partner `x + k` at any **other** position. `j != i` matters only for k = 0, where the partner must be a second copy. One hit is enough, so stop there. `x + k` is at most 2 × 10⁷, so it fits in an `int`."),
                    ("ret", "Each distinct value contributed at most once."),
                ],
                complexity=[
                    """
                    **Time O(n²):** each position may scan the whole list (twice). That's ~10¹⁰ steps for
                    n = 10⁵.

                    **Space O(1):** no extra structures.
                    """
                ],
                limits=[
                    """
                    Two linear scans per position: "have I seen x?" and "does x + k exist?". Both are
                    membership questions, and scanning is the slowest way to answer them. Sorting makes the
                    first trivial and the second a binary search.
                    """
                ],
                slow=True,
            ),
            approach(
                "Sort, then binary-search each partner",
                "better",
                "O(n log n)",
                "O(n)",
                idea=[
                    """
                    Sort a copy of the list. Now:

                    - Copies of a value sit next to each other, so "is this value new?" is just
                      `i == 0 or s[i] != s[i − 1]`.
                    - The partner `x + k` is at least `x`, so if it exists at another position it lies **to
                      the right** of `i`. Binary-search for it in `s[i + 1 …]`.

                    Searching from `i + 1` handles k = 0 for free: the search looks for `x` itself among the
                    later positions, which only succeeds if a second copy exists.
                    """
                ],
                walk=w2,
                build=[
                    "Sort a copy `s` of `nums`.",
                    "Loop `i` over `s`; skip `i` when `s[i] == s[i − 1]` (not the first copy).",
                    "Binary-search `x + k` in `s[i + 1 … n − 1]`; if found, add 1.",
                    "Return the count.",
                ],
                code={
                    "python": """
                        from bisect import bisect_left

                        class Solution:
                            def countGapPairs(self, nums: List[int], k: int) -> int:
                                s = sorted(nums)  #@sort
                                n = len(s)
                                total = 0
                                for i in range(n):  #@loop
                                    if i > 0 and s[i] == s[i - 1]:  #@dup
                                        continue  #@dup
                                    j = bisect_left(s, s[i] + k, i + 1)  #@bs
                                    if j < n and s[j] == s[i] + k:  #@bs
                                        total += 1  #@bs
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countGapPairs(int[] nums, int k) {
                                int[] s = nums.clone();  //@sort
                                Arrays.sort(s);  //@sort
                                int n = s.length, total = 0;
                                for (int i = 0; i < n; i++) {  //@loop
                                    if (i > 0 && s[i] == s[i - 1]) continue;  //@dup
                                    if (Arrays.binarySearch(s, i + 1, n, s[i] + k) >= 0) total++;  //@bs
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countGapPairs(vector<int>& nums, int k) {
                                vector<int> s = nums;  //@sort
                                sort(s.begin(), s.end());  //@sort
                                int n = s.size(), total = 0;
                                for (int i = 0; i < n; i++) {  //@loop
                                    if (i > 0 && s[i] == s[i - 1]) continue;  //@dup
                                    if (binary_search(s.begin() + i + 1, s.end(), s[i] + k)) total++;  //@bs
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* x, const void* y) {  //@cmp
                            int p = *(const int*) x, q = *(const int*) y;  //@cmp
                            return (p > q) - (p < q);  //@cmp
                        }  //@cmp

                        int countGapPairs(int* nums, int numsSize, int k) {
                            int* s = malloc(numsSize * sizeof(int));  //@sort
                            memcpy(s, nums, numsSize * sizeof(int));  //@sort
                            qsort(s, numsSize, sizeof(int), cmpInt);  //@sort
                            int total = 0;
                            for (int i = 0; i < numsSize; i++) {  //@loop
                                if (i > 0 && s[i] == s[i - 1]) continue;  //@dup
                                int want = s[i] + k, lo = i + 1, hi = numsSize;  //@bs
                                while (lo < hi) {  //@bs
                                    int mid = lo + (hi - lo) / 2;  //@bs
                                    if (s[mid] < want) lo = mid + 1; else hi = mid;  //@bs
                                }  //@bs
                                if (lo < numsSize && s[lo] == want) total++;  //@bs
                            }
                            free(s);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("cmp", "A comparator for `qsort` that returns −1, 0 or 1 without risking overflow."),
                    ("sort", "Sort a copy, leaving the caller's list alone.",
                     {"python": "`sorted` returns a new list.", "java": "`clone()` copies the array before sorting it.", "cpp": "Copy the vector, then sort the copy.", "c": "Copy into new memory with `memcpy`, then `qsort` it."}),
                    ("loop", "Each position of the sorted copy."),
                    ("dup", "Only the first copy of each value is considered. Equal values are adjacent after sorting, so comparing with the previous element is enough."),
                    ("bs", "Binary-search `x + k` strictly to the right of `i`. Found means some other position holds the partner.",
                     {"python": "`bisect_left(s, v, i + 1)` returns the first index ≥ `i + 1` whose value is not less than `v`; check that it's in range and equal to `v`.",
                      "java": "`Arrays.binarySearch(s, from, to, key)` searches `s[from … to − 1]` and returns a non-negative index only when the key is present.",
                      "cpp": "`binary_search` on the range after `i` returns whether the value is there.",
                      "c": "A hand-written lower bound: `lo` ends at the first position in `[i + 1, n)` whose value is ≥ `want`; check that it's in range and equal."}),
                    ("ret", "One count per distinct value with a partner.", {"c": "Free the copy first."}),
                ],
                complexity=[
                    """
                    **Time O(n log n):** the sort, plus one O(log n) search per position.

                    **Space O(n)** for the sorted copy.
                    """
                ],
                limits=[
                    """
                    The sort exists only to make lookups fast, but a hash table gives O(1) lookups without
                    sorting. With up to 10⁵ numbers either is fast enough; the hash version is simpler and
                    asymptotically better.
                    """
                ],
            ),
            approach(
                "Count values in a hash map",
                "best",
                "O(n)",
                "O(n)",
                idea=[
                    """
                    Count every value: `count[v]` = how many times `v` appears. Then loop over the **distinct**
                    values (the map's keys), which automatically ignores duplicates:

                    - **k > 0:** count `x` when `x + k` is a key.
                    - **k = 0:** count `x` when `count[x] ≥ 2` (a second copy at another position).
                    """
                ],
                walk=w3,
                build=[
                    "Build `count`: value → number of copies.",
                    "If `k == 0`, return how many values have a count of at least 2.",
                    "Otherwise return how many keys `x` have `x + k` also as a key.",
                ],
                code={
                    "python": """
                        from collections import Counter

                        class Solution:
                            def countGapPairs(self, nums: List[int], k: int) -> int:
                                count = Counter(nums)  #@count
                                if k == 0:  #@zero
                                    return sum(1 for c in count.values() if c >= 2)  #@zero
                                return sum(1 for x in count if x + k in count)  #@gap
                    """,
                    "java": """
                        class Solution {
                            public int countGapPairs(int[] nums, int k) {
                                Map<Integer, Integer> count = new HashMap<>();  //@count
                                for (int x : nums) count.merge(x, 1, Integer::sum);  //@count
                                int total = 0;
                                for (Map.Entry<Integer, Integer> e : count.entrySet()) {  //@each
                                    if (k == 0) {  //@zero
                                        if (e.getValue() >= 2) total++;  //@zero
                                    } else if (count.containsKey(e.getKey() + k)) {  //@gap
                                        total++;  //@gap
                                    }
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countGapPairs(vector<int>& nums, int k) {
                                unordered_map<int, int> count;  //@count
                                for (int x : nums) count[x]++;  //@count
                                int total = 0;
                                for (auto& [x, c] : count) {  //@each
                                    if (k == 0) {  //@zero
                                        if (c >= 2) total++;  //@zero
                                    } else if (count.count(x + k)) {  //@gap
                                        total++;  //@gap
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        // A small hash map from a value to its count: open addressing, linear probing.
                        typedef struct { int key; int count; bool used; } Slot;  //@table

                        static unsigned slotOf(int key, unsigned mask) {  //@hash
                            unsigned long long h = (unsigned long long) (long long) key * 0x9E3779B97F4A7C15ULL;  //@hash
                            return (unsigned) (h >> 32) & mask;  //@hash
                        }  //@hash

                        static Slot* find(Slot* t, unsigned mask, int key) {  //@hash
                            unsigned s = slotOf(key, mask);  //@hash
                            while (t[s].used && t[s].key != key) s = (s + 1) & mask;  //@hash
                            return &t[s];  //@hash
                        }  //@hash

                        int countGapPairs(int* nums, int numsSize, int k) {
                            unsigned cap = 1;  //@count
                            while (cap < 2u * numsSize) cap <<= 1;  //@count
                            Slot* count = calloc(cap, sizeof(Slot));  //@count
                            for (int i = 0; i < numsSize; i++) {  //@count
                                Slot* e = find(count, cap - 1, nums[i]);  //@count
                                e->key = nums[i];  //@count
                                e->used = true;  //@count
                                e->count++;  //@count
                            }  //@count
                            int total = 0;
                            for (unsigned s = 0; s < cap; s++) {  //@each
                                if (!count[s].used) continue;  //@each
                                if (k == 0) {  //@zero
                                    if (count[s].count >= 2) total++;  //@zero
                                } else if (find(count, cap - 1, count[s].key + k)->used) {  //@gap
                                    total++;  //@gap
                                }
                            }
                            free(count);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("table", "A slot: a value, how many times it appears, and whether the slot is in use."),
                    ("hash", "`slotOf` scrambles a value into a starting slot; `find` steps forward from there until it reaches the value's slot or an empty one."),
                    ("count", "Count every value once. The keys of this table are exactly the distinct values.",
                     {"python": "`Counter(nums)` does the whole count in one call.",
                      "java": "`merge(x, 1, Integer::sum)` adds one to `x`'s count, starting new values at 1.",
                      "cpp": "`count[x]++` creates missing keys at 0 and adds one.",
                      "c": "Size the table to a power of two at least 2n, then claim each value's slot and bump its count."}),
                    ("each", "Visit each **distinct** value once, which is what makes the pairs distinct.",
                     {"c": "Walk the table's slots and skip the unused ones."}),
                    ("zero", "k = 0: the pair is `(x, x)`, which needs two copies of `x` at different positions."),
                    ("gap", "k > 0: the pair `(x, x + k)` exists exactly when `x + k` is a key. It's at most 2 × 10⁷, well inside `int`."),
                    ("ret", "The number of distinct pairs.", {"c": "Free the table first."}),
                ],
                complexity=[
                    """
                    **Time O(n):** one pass to count, then one O(1) lookup per distinct value.

                    **Space O(n):** the table holds up to n distinct values.
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - When a pair condition **fixes** the partner (`y = x + k`), count pairs by checking each `x`'s
              partner instead of comparing everything with everything.
            - "Distinct pairs" usually means "work over distinct values": the keys of a count table.
            - Watch the degenerate case where the partner equals the element itself (k = 0 here): a
              presence check isn't enough, you need a **count ≥ 2**.
            - Sorting turns "seen before?" into a neighbour check and "exists?" into a binary search, a
              useful fallback when you can't use a hash map.
            """
        ],
    )
