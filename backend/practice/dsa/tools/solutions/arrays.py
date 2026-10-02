"""Written-out solutions for Arrays & Hashing. Run: python3 tools/solutions/arrays.py [id ...]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sol import Grid, Row, Steps, Vars, approach, fig, sol, table, WRITTEN  # noqa: E402

ONLY = set(sys.argv[1:])
REGISTRY = []


def problem(fn):
    REGISTRY.append(fn)
    return fn


def cells_st(n, **groups):
    """{index: state} from state=[indices] keyword lists."""
    out = {}
    for state, idx in groups.items():
        for i in idx:
            out[i] = state
    return out


# ============================================================================ complement-lookup


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


# ============================================================================ run

if __name__ == "__main__":
    for fn in REGISTRY:
        pid = fn.__name__.replace("_", "-")
        if not ONLY or pid in ONLY:
            fn()
    print(f"wrote {len(WRITTEN)} solutions: {', '.join(WRITTEN)}")
