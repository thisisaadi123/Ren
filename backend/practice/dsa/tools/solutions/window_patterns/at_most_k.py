"""Sliding Window: counting windows; "exactly k" as atMost(k) − atMost(k − 1)."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def count_walk(w, shown, n, ok, title_k="", info=None):
    """For each right end, the window is the longest valid one ending there; it contributes its length."""
    l = total = 0
    for r in range(n):
        while not ok(l, r):
            l += 1
        total += r - l + 1
        w.step(f"{title_k}End {r}: valid starts {l}..{r}, adding {r - l + 1}.", Row(shown, st={x: "active" for x in range(l, r + 1)}), Vars(total=total, **(info(l, r) if info else {})))
    return total


@problem
def exactly_k_breeds():
    pens, k = [1, 2, 1, 3, 2, 2, 3], 2
    n = len(pens)
    want = sum(1 for l in range(n) for r in range(l, n) if len(set(pens[l:r + 1])) == k)
    at_k = sum(1 for l in range(n) for r in range(l, n) if len(set(pens[l:r + 1])) <= k)
    at_k1 = sum(1 for l in range(n) for r in range(l, n) if len(set(pens[l:r + 1])) <= k - 1)

    w1 = Steps("From each start, extend and keep a running count of distinct breeds; count the stretches where it equals k.")
    for l in range(n):
        seen, got = set(), []
        for r in range(l, n):
            seen.add(pens[r])
            if len(seen) == k:
                got.append(r)
            if len(seen) > k:
                break
        w1.step(f"From {l}: exactly {k} breeds for ends {got if got else 'none'}.", Row(pens, st={x: "found" for x in got}))
    w1.step(f"Total: {want}.", result=want)

    w2 = Steps(f"Counting 'at most k' is easy with a window: for each end, every start from the window's left edge works. Exactly {k} = atMost({k}) − atMost({k - 1}).")
    count_walk(w2, pens, n, lambda l, r: len(set(pens[l:r + 1])) <= k, f"At most {k}. ")
    w2.step(f"atMost({k}) = {at_k}. The same pass with {k - 1} gives atMost({k - 1}) = {at_k1}. Difference: {at_k - at_k1}.", result=want)

    sol(
        "exactly-k-breeds",
        summary="""
            "Exactly k distinct" isn't monotone (shrinking can drop below k), but "at most k distinct" is: for each right
            end, a window finds the leftmost valid start, and every start from there works, adding `r − left + 1` stretches.
            So count `atMost(k) − atMost(k − 1)`, two linear passes. O(n), 64-bit count.
        """,
        question=[
            """
            Count the contiguous stretches of `pens` with exactly `k` different values.

            - **n up to 10⁵**: up to 5 × 10⁹ stretches, so the count needs 64 bits.
            - Values are in `1..n`.
            """
        ],
        think=[
            f"""
            `pens = {pens}`, `k = {k}` → **{want}** stretches.

            For a fixed right end, as the start moves left the number of breeds only grows. The starts with exactly `k`
            breeds form a contiguous range, but tracking both of its ends is fiddly. "At most `k`" is a single range
            ending at `r`, which the usual window gives directly. And stretches with exactly `k` breeds are those with at
            most `k` minus those with at most `k − 1`.
            """,
            fig(Row(pens, label="pens")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["For each start, extend while the distinct count is at most `k`, counting the ends where it is exactly `k`."],
                walk=w1,
                build=["Loop over starts.", "Running distinct count.", "Stop once it passes `k`."],
                code={
                    "python": """
                        class Solution:
                            def countBreedStretches(self, pens: List[int], k: int) -> int:
                                n, total = len(pens), 0  #@init
                                for i in range(n):  #@starts
                                    seen = set()  #@extend
                                    for j in range(i, n):  #@extend
                                        seen.add(pens[j])  #@extend
                                        if len(seen) > k:  #@extend
                                            break  #@extend
                                        if len(seen) == k:  #@count
                                            total += 1  #@count
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countBreedStretches(int[] pens, int k) {
                                int n = pens.length;  //@init
                                int[] mark = new int[n + 1];  //@init
                                long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int distinct = 0;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        if (mark[pens[j]] != i + 1) { mark[pens[j]] = i + 1; distinct++; }  //@extend
                                        if (distinct > k) break;  //@extend
                                        if (distinct == k) total++;  //@count
                                    }
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countBreedStretches(vector<int>& pens, int k) {
                                int n = pens.size();  //@init
                                vector<int> mark(n + 1, 0);  //@init
                                long long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int distinct = 0;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        if (mark[pens[j]] != i + 1) { mark[pens[j]] = i + 1; distinct++; }  //@extend
                                        if (distinct > k) break;  //@extend
                                        if (distinct == k) total++;  //@count
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countBreedStretches(int* pens, int pensSize, int k) {
                            int n = pensSize;  //@init
                            int* mark = calloc(n + 1, sizeof(int));  //@init
                            long long total = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                int distinct = 0;  //@extend
                                for (int j = i; j < n; j++) {  //@extend
                                    if (mark[pens[j]] != i + 1) { mark[pens[j]] = i + 1; distinct++; }  //@extend
                                    if (distinct > k) break;  //@extend
                                    if (distinct == k) total++;  //@count
                                }
                            }
                            free(mark);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "The count.", {"java": "`mark[v] = i + 1` means 'seen since start `i`'; no clearing needed.", "cpp": "`mark[v] = i + 1` means 'seen since start `i`'; no clearing needed.", "c": "`mark[v] = i + 1` means 'seen since start `i`'; no clearing needed."}),
                    ("starts", "Each start."),
                    ("extend", "Add pens; past `k` breeds, longer stretches only get worse."),
                    ("count", "Exactly `k` breeds."),
                    ("ret", "Total."),
                ],
                complexity=["**Time O(n²)** in the worst case. **Space O(n).**"],
                limits=["Quadratic; the at-most trick counts all stretches ending at each position in O(1) amortised."],
                slow=True,
            ),
            approach(
                "atMost(k) − atMost(k − 1)",
                "best",
                "O(n)",
                "O(n)",
                idea=["`atMost(t)`: window with counts and a distinct counter; shrink while distinct > `t`; add `r − left + 1` per end. Answer `atMost(k) − atMost(k − 1)`."],
                walk=w2,
                build=["Counting window for 'at most t'.", "Run it twice.", "Subtract."],
                code={
                    "python": """
                        class Solution:
                            def countBreedStretches(self, pens: List[int], k: int) -> int:
                                def at_most(limit):  #@atmost
                                    count = [0] * (len(pens) + 1)  #@atmost
                                    left = distinct = total = 0  #@atmost
                                    for i, v in enumerate(pens):  #@grow
                                        count[v] += 1  #@grow
                                        if count[v] == 1:  #@grow
                                            distinct += 1  #@grow
                                        while distinct > limit:  #@shrink
                                            count[pens[left]] -= 1  #@shrink
                                            if count[pens[left]] == 0:  #@shrink
                                                distinct -= 1  #@shrink
                                            left += 1  #@shrink
                                        total += i - left + 1  #@add
                                    return total  #@add
                                return at_most(k) - at_most(k - 1)  #@ret
                    """,
                    "java": """
                        class Solution {
                            private long atMost(int[] pens, int limit) {  //@atmost
                                int[] count = new int[pens.length + 1];  //@atmost
                                int left = 0, distinct = 0;  //@atmost
                                long total = 0;  //@atmost
                                for (int i = 0; i < pens.length; i++) {  //@grow
                                    if (count[pens[i]]++ == 0) distinct++;  //@grow
                                    while (distinct > limit) if (--count[pens[left++]] == 0) distinct--;  //@shrink
                                    total += i - left + 1;  //@add
                                }
                                return total;  //@add
                            }  //@atmost

                            public long countBreedStretches(int[] pens, int k) {
                                return atMost(pens, k) - atMost(pens, k - 1);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static long long atMost(const vector<int>& pens, int limit) {  //@atmost
                                vector<int> count(pens.size() + 1, 0);  //@atmost
                                int left = 0, distinct = 0;  //@atmost
                                long long total = 0;  //@atmost
                                for (int i = 0; i < (int) pens.size(); i++) {  //@grow
                                    if (count[pens[i]]++ == 0) distinct++;  //@grow
                                    while (distinct > limit) if (--count[pens[left++]] == 0) distinct--;  //@shrink
                                    total += i - left + 1;  //@add
                                }
                                return total;  //@add
                            }  //@atmost

                        public:
                            long long countBreedStretches(vector<int>& pens, int k) {
                                return atMost(pens, k) - atMost(pens, k - 1);  //@ret
                            }
                        };
                    """,
                    "c": """
                        static long long at_most(const int* pens, int n, int limit) {  //@atmost
                            int* count = calloc(n + 1, sizeof(int));  //@atmost
                            int left = 0, distinct = 0;  //@atmost
                            long long total = 0;  //@atmost
                            for (int i = 0; i < n; i++) {  //@grow
                                if (count[pens[i]]++ == 0) distinct++;  //@grow
                                while (distinct > limit) if (--count[pens[left++]] == 0) distinct--;  //@shrink
                                total += i - left + 1;  //@add
                            }
                            free(count);  //@add
                            return total;  //@add
                        }  //@atmost

                        long long countBreedStretches(int* pens, int pensSize, int k) {
                            return at_most(pens, pensSize, k) - at_most(pens, pensSize, k - 1);  //@ret
                        }
                    """,
                },
                lines=[
                    ("atmost", "Counts stretches with at most `limit` breeds (values are at most `n`, so an array works)."),
                    ("grow", "Add pen `i`; a breed entering from zero raises `distinct`."),
                    ("shrink", "Too many breeds: drop pens from the left until one breed disappears."),
                    ("add", "Every start from `left` to `i` gives a valid stretch ending at `i`: `i − left + 1` of them."),
                    ("ret", "At most `k` minus at most `k − 1` leaves exactly `k`. (`atMost(0)` is 0: the window is always empty.)"),
                ],
                complexity=["**Time O(n):** two passes, each moving both pointers at most `n` times. **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - **Exactly k = atMost(k) − atMost(k − 1)** whenever "at most" is window-friendly.
            - A counting window adds `r − left + 1` per right end: all valid starts at once.
            - Use 64-bit counts: there are about n²/2 windows.
            """
        ],
    )


@problem
def exactly_k_odd_tickets():
    tickets, k = [2, 5, 4, 7, 3, 6, 8, 1, 2], 2
    n = len(tickets)
    odd = [t & 1 for t in tickets]
    want = sum(1 for l in range(n) for r in range(l, n) if sum(odd[l:r + 1]) == k)
    at_k = sum(1 for l in range(n) for r in range(l, n) if sum(odd[l:r + 1]) <= k)
    at_k1 = sum(1 for l in range(n) for r in range(l, n) if sum(odd[l:r + 1]) <= k - 1)

    w1 = Steps("From each start, count odd numbers as you extend; count the ends where there are exactly k.")
    for l in range(n):
        c, got = 0, []
        for r in range(l, n):
            c += odd[r]
            if c == k:
                got.append(r)
            if c > k:
                break
        w1.step(f"From {l}: exactly {k} odd for ends {got if got else 'none'}.", Row(tickets, st={x: "found" for x in got}))
    w1.step(f"Total: {want}.", result=want)

    w2 = Steps("Let p be the number of odd tickets seen so far. A stretch ending here has exactly k odds when it starts right after a point where the count was p − k. Keep how often each count has occurred.")
    seen = {0: 1}
    p = total = 0
    for i, v in enumerate(tickets):
        p += v & 1
        add = seen.get(p - k, 0)
        total += add
        seen[p] = seen.get(p, 0) + 1
        w2.step(f"Ticket {v}: {p} odd so far; {add} earlier point(s) had {p - k}.", Row(tickets, st={i: "active"}), Vars(total=total, odd_so_far=p))
    w2.step(f"Total: {total}.", result=total)

    w3 = Steps(f"Exactly {k} = atMost({k}) − atMost({k - 1}), each counted with a window that holds at most that many odd tickets.")
    count_walk(w3, tickets, n, lambda l, r: sum(odd[l:r + 1]) <= k, f"At most {k}. ", lambda l, r: {"odd": sum(odd[l:r + 1])})
    w3.step(f"atMost({k}) = {at_k}, atMost({k - 1}) = {at_k1}. Difference: {at_k - at_k1}.", result=want)

    sol(
        "exactly-k-odd-tickets",
        summary="""
            Only parity matters, so this is "count subarrays of 0/1 values summing to k". Either count prefix sums (how
            many earlier prefixes had `p − k` odds) or use two windows: `atMost(k) − atMost(k − 1)`, where each counts
            stretches with at most that many odds by adding `r − left + 1` per end. O(n).
        """,
        question=[
            """
            Count contiguous stretches of `tickets` containing exactly `k` odd numbers.

            - **n up to 10⁵**; the count needs 64 bits.
            """
        ],
        think=[
            f"""
            `tickets = {tickets}`, `k = {k}` → **{want}**.

            Replace each ticket by 1 if odd, else 0: `{odd}`. Now we count stretches summing to exactly `k`. Even tickets
            around a valid stretch can be included or not, which is why the count isn't simply the number of ways to pick
            `k` consecutive odds. Both techniques below handle that automatically.
            """,
            fig(Row(tickets, label="tickets"), Row(odd, label="odd?")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start, extend while the odd count is at most `k`, counting ends where it equals `k`."],
                walk=w1,
                build=["Loop over starts.", "Running odd count.", "Stop past `k`."],
                code={
                    "python": """
                        class Solution:
                            def countOddStretches(self, tickets: List[int], k: int) -> int:
                                n, total = len(tickets), 0  #@init
                                for i in range(n):  #@starts
                                    odd = 0  #@extend
                                    for j in range(i, n):  #@extend
                                        odd += tickets[j] & 1  #@extend
                                        if odd > k:  #@extend
                                            break  #@extend
                                        if odd == k:  #@count
                                            total += 1  #@count
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countOddStretches(int[] tickets, int k) {
                                int n = tickets.length;  //@init
                                long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int odd = 0;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        odd += tickets[j] & 1;  //@extend
                                        if (odd > k) break;  //@extend
                                        if (odd == k) total++;  //@count
                                    }
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countOddStretches(vector<int>& tickets, int k) {
                                int n = tickets.size();  //@init
                                long long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int odd = 0;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        odd += tickets[j] & 1;  //@extend
                                        if (odd > k) break;  //@extend
                                        if (odd == k) total++;  //@count
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countOddStretches(int* tickets, int ticketsSize, int k) {
                            long long total = 0;  //@init
                            for (int i = 0; i < ticketsSize; i++) {  //@starts
                                int odd = 0;  //@extend
                                for (int j = i; j < ticketsSize; j++) {  //@extend
                                    odd += tickets[j] & 1;  //@extend
                                    if (odd > k) break;  //@extend
                                    if (odd == k) total++;  //@count
                                }
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("init", "The count."), ("starts", "Each start."), ("extend", "`& 1` is 1 for odd numbers; past `k` odds, stop."), ("count", "Exactly `k` odds."), ("ret", "Total.")],
                complexity=["**Time O(n²)** when odd numbers are rare. **Space O(1).**"],
                limits=["Quadratic. Prefix counts or the at-most trick count all stretches ending at a position at once."],
                slow=True,
            ),
            approach(
                "Prefix counts",
                "better",
                "O(n)",
                "O(n)",
                idea=["`p` = odd tickets so far; `seen[c]` = how many prefixes had `c` odds (starting with `seen[0] = 1`). At each ticket add `seen[p − k]`, then record `p`."],
                walk=w2,
                build=["Frequency of prefix odd counts.", "Look up `p − k`.", "Record `p`."],
                code={
                    "python": """
                        class Solution:
                            def countOddStretches(self, tickets: List[int], k: int) -> int:
                                seen = [0] * (len(tickets) + 1)  #@init
                                seen[0] = 1  #@init
                                p = total = 0  #@init
                                for v in tickets:  #@scan
                                    p += v & 1  #@scan
                                    if p >= k:  #@look
                                        total += seen[p - k]  #@look
                                    seen[p] += 1  #@record
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countOddStretches(int[] tickets, int k) {
                                int[] seen = new int[tickets.length + 1];  //@init
                                seen[0] = 1;  //@init
                                int p = 0;  //@init
                                long total = 0;  //@init
                                for (int v : tickets) {  //@scan
                                    p += v & 1;  //@scan
                                    if (p >= k) total += seen[p - k];  //@look
                                    seen[p]++;  //@record
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countOddStretches(vector<int>& tickets, int k) {
                                vector<int> seen(tickets.size() + 1, 0);  //@init
                                seen[0] = 1;  //@init
                                int p = 0;  //@init
                                long long total = 0;  //@init
                                for (int v : tickets) {  //@scan
                                    p += v & 1;  //@scan
                                    if (p >= k) total += seen[p - k];  //@look
                                    seen[p]++;  //@record
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countOddStretches(int* tickets, int ticketsSize, int k) {
                            int* seen = calloc(ticketsSize + 1, sizeof(int));  //@init
                            seen[0] = 1;  //@init
                            int p = 0;  //@init
                            long long total = 0;  //@init
                            for (int i = 0; i < ticketsSize; i++) {  //@scan
                                p += tickets[i] & 1;  //@scan
                                if (p >= k) total += seen[p - k];  //@look
                                seen[p]++;  //@record
                            }
                            free(seen);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Odd counts range over `0..n`, so an array replaces a map. The empty prefix has 0 odds."),
                    ("scan", "`p` = odd tickets among those read so far."),
                    ("look", "Each earlier prefix with `p − k` odds starts a stretch ending here with exactly `k`."),
                    ("record", "This prefix becomes available for later positions."),
                    ("ret", "Total."),
                ],
                complexity=["**Time O(n).** **Space O(n)** for the prefix-count table."],
                limits=["Needs an O(n) table. The two-window method uses O(1) memory."],
            ),
            approach(
                "atMost(k) − atMost(k − 1)",
                "best",
                "O(n)",
                "O(1)",
                idea=["`atMost(t)`: window holding at most `t` odd tickets, adding `r − left + 1` per end. Answer `atMost(k) − atMost(k − 1)`."],
                walk=w3,
                build=["Counting window.", "Two passes.", "Subtract."],
                code={
                    "python": """
                        class Solution:
                            def countOddStretches(self, tickets: List[int], k: int) -> int:
                                def at_most(limit):  #@atmost
                                    left = odd = total = 0  #@atmost
                                    for i, v in enumerate(tickets):  #@grow
                                        odd += v & 1  #@grow
                                        while odd > limit:  #@shrink
                                            odd -= tickets[left] & 1  #@shrink
                                            left += 1  #@shrink
                                        total += i - left + 1  #@add
                                    return total  #@add
                                return at_most(k) - at_most(k - 1)  #@ret
                    """,
                    "java": """
                        class Solution {
                            private long atMost(int[] tickets, int limit) {  //@atmost
                                int left = 0, odd = 0;  //@atmost
                                long total = 0;  //@atmost
                                for (int i = 0; i < tickets.length; i++) {  //@grow
                                    odd += tickets[i] & 1;  //@grow
                                    while (odd > limit) odd -= tickets[left++] & 1;  //@shrink
                                    total += i - left + 1;  //@add
                                }
                                return total;  //@add
                            }  //@atmost

                            public long countOddStretches(int[] tickets, int k) {
                                return atMost(tickets, k) - atMost(tickets, k - 1);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static long long atMost(const vector<int>& tickets, int limit) {  //@atmost
                                int left = 0, odd = 0;  //@atmost
                                long long total = 0;  //@atmost
                                for (int i = 0; i < (int) tickets.size(); i++) {  //@grow
                                    odd += tickets[i] & 1;  //@grow
                                    while (odd > limit) odd -= tickets[left++] & 1;  //@shrink
                                    total += i - left + 1;  //@add
                                }
                                return total;  //@add
                            }  //@atmost

                        public:
                            long long countOddStretches(vector<int>& tickets, int k) {
                                return atMost(tickets, k) - atMost(tickets, k - 1);  //@ret
                            }
                        };
                    """,
                    "c": """
                        static long long at_most(const int* tickets, int n, int limit) {  //@atmost
                            int left = 0, odd = 0;  //@atmost
                            long long total = 0;  //@atmost
                            for (int i = 0; i < n; i++) {  //@grow
                                odd += tickets[i] & 1;  //@grow
                                while (odd > limit) odd -= tickets[left++] & 1;  //@shrink
                                total += i - left + 1;  //@add
                            }
                            return total;  //@add
                        }  //@atmost

                        long long countOddStretches(int* tickets, int ticketsSize, int k) {
                            return at_most(tickets, ticketsSize, k) - at_most(tickets, ticketsSize, k - 1);  //@ret
                        }
                    """,
                },
                lines=[
                    ("atmost", "Counts stretches with at most `limit` odd tickets."),
                    ("grow", "Add ticket `i`."),
                    ("shrink", "Too many odds: drop from the left until one odd ticket leaves."),
                    ("add", "All starts from `left` to `i` are valid for this end."),
                    ("ret", "Exactly `k` = at most `k` − at most `k − 1`."),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Count subarrays with sum exactly k (non-negative values):** prefix-count map, or atMost difference.
            - Reduce to 0/1 values when only a property (odd, vowel, …) matters.
            - atMost counting adds `r − left + 1` per end.
            """
        ],
    )


@problem
def full_set_of_stamps():
    s = "abcabbcab"
    n = len(s)
    full = lambda l, r: set("abc") <= set(s[l:r + 1])
    want = sum(1 for l in range(n) for r in range(l, n) if full(l, r))

    w1 = Steps("From each start, find the first end where all three stamps appear; every longer run from that start is full too.")
    total = 0
    for l in range(n):
        r = l
        while r < n and not full(l, r):
            r += 1
        add = n - r if r < n else 0
        total += add
        w1.step(f"From {l}: first full at {r if r < n else '—'}, so {add} full set(s) start here.", Row(list(s), st={**{x: "active" for x in range(l, min(r, n))}, **({x: "found" for x in range(r, n)} if r < n else {})}), Vars(total=total))
    w1.step(f"Total: {want}.", result=want)

    w2 = Steps("For each end, remember the last position of a, b and c. A run ending here is full exactly when it starts at or before the earliest of the three: min(last) + 1 choices.")
    last = {"a": -1, "b": -1, "c": -1}
    total = 0
    for i, c in enumerate(s):
        last[c] = i
        add = min(last.values()) + 1
        total += add
        w2.step(f"'{c}' at {i}: last a, b, c at " + ", ".join(str(last[x]) for x in "abc") + f"; {add} full set(s) end here.", Row(list(s), st={**{x: "found" for x in range(0, add)}, i: "active"}), Vars(total=total))
    w2.step(f"Total: {total}.", result=total)

    sol(
        "full-set-of-stamps",
        summary="""
            For each end `i`, track the last position of `a`, `b` and `c`. A substring ending at `i` is a full set exactly
            when its start is at or before the earliest of those three positions, which gives `min(last) + 1` starts
            (zero while some letter hasn't appeared). Sum over all ends. O(n).
        """,
        question=[
            """
            Count the substrings of `s` (letters `a`, `b`, `c` only) that contain at least one of each letter.

            - **n up to 10⁵**; the count needs 64 bits.
            """
        ],
        think=[
            f"""
            `"{s}"` → **{want}**.

            "Contains all three" survives extending, so for a fixed end the good starts are a prefix range `0..x`. The
            boundary `x` is the latest start that still includes one of each letter, which is the smallest of the three
            letters' last positions. This is the counting-window idea with the left edge computed directly.
            """,
            fig(Row(list(s), label="s")),
        ],
        approaches=[
            approach(
                "First full end from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start, extend until all three letters have appeared at `r`; then the `n − r` runs ending at `r` or later are full."],
                walk=w1,
                build=["Loop over starts.", "Extend until all three appear.", "Add the runs that extend further."],
                code={
                    "python": """
                        class Solution:
                            def countFullSets(self, s: str) -> int:
                                n, total = len(s), 0  #@init
                                for i in range(n):  #@starts
                                    seen = set()  #@extend
                                    for j in range(i, n):  #@extend
                                        seen.add(s[j])  #@extend
                                        if len(seen) == 3:  #@add
                                            total += n - j  #@add
                                            break  #@add
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countFullSets(String s) {
                                int n = s.length();  //@init
                                long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int mask = 0;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        mask |= 1 << (s.charAt(j) - 'a');  //@extend
                                        if (mask == 7) { total += n - j; break; }  //@add
                                    }
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countFullSets(string& s) {
                                int n = s.size();  //@init
                                long long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int mask = 0;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        mask |= 1 << (s[j] - 'a');  //@extend
                                        if (mask == 7) { total += n - j; break; }  //@add
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countFullSets(char* s) {
                            int n = strlen(s);  //@init
                            long long total = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                int mask = 0;  //@extend
                                for (int j = i; j < n; j++) {  //@extend
                                    mask |= 1 << (s[j] - 'a');  //@extend
                                    if (mask == 7) { total += n - j; break; }  //@add
                                }
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "The count."),
                    ("starts", "Each start."),
                    ("extend", "Collect letters until all three are present.", {"java": "A 3-bit mask; 7 means all three.", "cpp": "A 3-bit mask; 7 means all three.", "c": "A 3-bit mask; 7 means all three."}),
                    ("add", "The first full end `j` and every later end work: `n − j` runs."),
                    ("ret", "Total."),
                ],
                complexity=["**Time O(n²)** when a letter is missing for long stretches. **Space O(1).**"],
                limits=["Re-scans from every start. Last positions give each end's count directly."],
                slow=True,
            ),
            approach(
                "Last positions per end",
                "best",
                "O(n)",
                "O(1)",
                idea=["`last[a|b|c]` start at −1. For each `i`: update `last[s[i]] = i`; add `min(last) + 1`."],
                walk=w2,
                build=["Last positions.", "Count per end.", "Sum."],
                code={
                    "python": """
                        class Solution:
                            def countFullSets(self, s: str) -> int:
                                last = {"a": -1, "b": -1, "c": -1}  #@init
                                total = 0  #@init
                                for i, c in enumerate(s):  #@scan
                                    last[c] = i  #@scan
                                    total += min(last.values()) + 1  #@add
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countFullSets(String s) {
                                int[] last = {-1, -1, -1};  //@init
                                long total = 0;  //@init
                                for (int i = 0; i < s.length(); i++) {  //@scan
                                    last[s.charAt(i) - 'a'] = i;  //@scan
                                    total += Math.min(last[0], Math.min(last[1], last[2])) + 1;  //@add
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countFullSets(string& s) {
                                int last[3] = {-1, -1, -1};  //@init
                                long long total = 0;  //@init
                                for (int i = 0; i < (int) s.size(); i++) {  //@scan
                                    last[s[i] - 'a'] = i;  //@scan
                                    total += min({last[0], last[1], last[2]}) + 1;  //@add
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countFullSets(char* s) {
                            int last[3] = {-1, -1, -1}, n = strlen(s);  //@init
                            long long total = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@scan
                                last[s[i] - 'a'] = i;  //@scan
                                int m = last[0] < last[1] ? last[0] : last[1];  //@add
                                if (last[2] < m) m = last[2];  //@add
                                total += m + 1;  //@add
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "−1 means 'not seen yet'."),
                    ("scan", "Position `i` is now the last of its letter."),
                    ("add", "Starts `0..min(last)` include all three letters; `min + 1` of them (0 if a letter is still missing)."),
                    ("ret", "Total."),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Count windows with "at least one of each":** for each end, the valid starts are `0..min(last positions)`.
            - Counting per right end is the core of every window-counting problem.
            - Equivalent to a window whose left edge is computed instead of moved.
            """
        ],
    )


@problem
def products_under_a_cap():
    factors, cap = [3, 2, 5, 1, 4, 6, 1], 25
    n = len(factors)

    def prod(l, r):
        p = 1
        for x in factors[l:r + 1]:
            p *= x
        return p
    want = sum(1 for l in range(n) for r in range(l, n) if prod(l, r) < cap)

    w1 = Steps("From each start, multiply as you extend; stop once the product reaches the cap.")
    total = 0
    for l in range(n):
        p, r, got = 1, l, 0
        while r < n and p * factors[r] < cap:
            p *= factors[r]
            r += 1
            got += 1
        total += got
        w1.step(f"From {l}: {got} run(s) stay under {cap}.", Row(factors, st={x: "found" for x in range(l, r)}), Vars(total=total))
    w1.step(f"Total: {want}.", result=want)

    w2 = Steps("Keep the product of the window. Multiply in each new factor; while the product is at least the cap, divide out factors from the left. Every start in the window gives a run ending here.")
    count_walk(w2, factors, n, lambda l, r: l > r or prod(l, r) < cap, "", lambda l, r: {"product": prod(l, r) if l <= r else 1})
    w2.step(f"Total: {want}.", result=want)

    sol(
        "products-under-a-cap",
        summary="""
            Factors are at least 1, so extending a run never lowers its product: a counting window works. Multiply in each
            factor; while the product is at least `cap`, divide out the leftmost factor. Then all `r − left + 1` runs ending
            at `r` are under the cap. A cap of 0 or 1 admits nothing. O(n).
        """,
        question=[
            """
            Count the contiguous runs of `factors` whose product is strictly less than `cap`.

            - **n up to 10⁵**, factors 1..1000, cap up to 10⁶.
            """
        ],
        think=[
            f"""
            `factors = {factors}`, `cap = {cap}` → **{want}**.

            Products of positive integers grow (or stay the same, with 1s) as a run is extended, so the runs ending at `r`
            that are under the cap are exactly those starting at or after some `left`. The window keeps the product below
            `cap` (at most 10⁶), so multiplying in one more factor stays below 10⁹: no overflow, and division by the
            leaving factor is exact.
            """,
            fig(Row(factors, label="factors")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start, multiply while the product stays under the cap, counting each run."],
                walk=w1,
                build=["Loop over starts.", "Multiply while under the cap.", "Count."],
                code={
                    "python": """
                        class Solution:
                            def countUnderCap(self, factors: List[int], cap: int) -> int:
                                n, total = len(factors), 0  #@init
                                for i in range(n):  #@starts
                                    product = 1  #@extend
                                    for j in range(i, n):  #@extend
                                        product *= factors[j]  #@extend
                                        if product >= cap:  #@extend
                                            break  #@extend
                                        total += 1  #@extend
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countUnderCap(int[] factors, int cap) {
                                int n = factors.length;  //@init
                                long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    long product = 1;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        product *= factors[j];  //@extend
                                        if (product >= cap) break;  //@extend
                                        total++;  //@extend
                                    }
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countUnderCap(vector<int>& factors, int cap) {
                                int n = factors.size();  //@init
                                long long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    long long product = 1;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        product *= factors[j];  //@extend
                                        if (product >= cap) break;  //@extend
                                        total++;  //@extend
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countUnderCap(int* factors, int factorsSize, int cap) {
                            long long total = 0;  //@init
                            for (int i = 0; i < factorsSize; i++) {  //@starts
                                long long product = 1;  //@extend
                                for (int j = i; j < factorsSize; j++) {  //@extend
                                    product *= factors[j];  //@extend
                                    if (product >= cap) break;  //@extend
                                    total++;  //@extend
                                }
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("init", "The count."), ("starts", "Each start."), ("extend", "Multiply in the next factor; once at or above the cap, longer runs are too (64-bit: one factor past 10⁶ stays below 10⁹)."), ("ret", "Total.")],
                complexity=["**Time O(n²)** when many factors are 1. **Space O(1).**"],
                limits=["Long runs of 1s make every start extend far. The window keeps one product for all starts."],
                slow=True,
            ),
            approach(
                "Counting window with a running product",
                "best",
                "O(n)",
                "O(1)",
                idea=["If `cap ≤ 1`, return 0. Otherwise multiply in `factors[r]`; while `product ≥ cap`, divide by `factors[left]` and advance. Add `r − left + 1`."],
                walk=w2,
                build=["Small caps admit nothing.", "Multiply in, divide out.", "Count runs per end."],
                code={
                    "python": """
                        class Solution:
                            def countUnderCap(self, factors: List[int], cap: int) -> int:
                                if cap <= 1:  #@edge
                                    return 0  #@edge
                                product, left, total = 1, 0, 0  #@init
                                for i, f in enumerate(factors):  #@grow
                                    product *= f  #@grow
                                    while product >= cap:  #@shrink
                                        product //= factors[left]  #@shrink
                                        left += 1  #@shrink
                                    total += i - left + 1  #@add
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countUnderCap(int[] factors, int cap) {
                                if (cap <= 1) return 0;  //@edge
                                long product = 1, total = 0;  //@init
                                int left = 0;  //@init
                                for (int i = 0; i < factors.length; i++) {  //@grow
                                    product *= factors[i];  //@grow
                                    while (product >= cap) product /= factors[left++];  //@shrink
                                    total += i - left + 1;  //@add
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countUnderCap(vector<int>& factors, int cap) {
                                if (cap <= 1) return 0;  //@edge
                                long long product = 1, total = 0;  //@init
                                int left = 0;  //@init
                                for (int i = 0; i < (int) factors.size(); i++) {  //@grow
                                    product *= factors[i];  //@grow
                                    while (product >= cap) product /= factors[left++];  //@shrink
                                    total += i - left + 1;  //@add
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countUnderCap(int* factors, int factorsSize, int cap) {
                            if (cap <= 1) return 0;  //@edge
                            long long product = 1, total = 0;  //@init
                            int left = 0;  //@init
                            for (int i = 0; i < factorsSize; i++) {  //@grow
                                product *= factors[i];  //@grow
                                while (product >= cap) product /= factors[left++];  //@shrink
                                total += i - left + 1;  //@add
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("edge", "Every product is at least 1, so a cap of 0 or 1 admits no run (this also keeps the shrink loop from running past `i`)."),
                    ("init", "Empty window, product 1."),
                    ("grow", "Multiply in factor `i`."),
                    ("shrink", "Divide out factors from the left until the product is under the cap; division is exact since they were multiplied in."),
                    ("add", "Every start from `left` to `i` gives a run under the cap."),
                    ("ret", "Total."),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Products of factors ≥ 1** behave like sums of non-negatives: windows work.
            - Handle `cap ≤ 1` first, or the window would try to shrink past empty.
            - Counting windows add `r − left + 1` per end.
            """
        ],
    )
