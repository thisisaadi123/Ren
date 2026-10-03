"""Stacks & Queues: contribution counting."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def reach(a, beats_left, beats_right):
    """For each i: how many starts (left) and ends (right) keep i as the stretch's chosen extreme."""
    n = len(a)
    left, right = [0] * n, [0] * n
    for i in range(n):
        l = i
        while l > 0 and beats_left(a[i], a[l - 1]):
            l -= 1
        r = i
        while r < n - 1 and beats_right(a[i], a[r + 1]):
            r += 1
        left[i], right[i] = i - l + 1, r - i + 1
    return left, right


@problem
def sum_of_stretch_lows():
    prices = [3, 1, 2, 4, 2]
    n = len(prices)
    left, right = reach(prices, lambda x, y: y >= x, lambda x, y: y > x)
    want = sum(p * l * r for p, l, r in zip(prices, left, right))
    brute = sum(min(prices[i:j + 1]) for i in range(n) for j in range(i, n))
    assert want == brute

    w1 = Steps("Fix each start day; extend the stretch one day at a time, keeping its running low, and add that low every time.")
    total = 0
    for i in range(n):
        low, lows = prices[i], []
        for j in range(i, n):
            low = min(low, prices[j])
            lows.append(low)
        total += sum(lows)
        w1.step(f"Start at day {i}: the lows of the stretches ending at days {i}..{n - 1} are {lows}, adding {sum(lows)}.", Row(prices, st={i: "active"}, label="prices"), Row(["·"] * i + lows, label="running low"), Vars(total=total))
    w1.step(f"Total of all {n * (n + 1) // 2} lows: {total}.", result=total)

    w2 = Steps("Flip the question: for each day, in how many stretches is it the low? Walk outward while neighbours don't undercut it.")
    acc = 0
    for i in range(n):
        acc += prices[i] * left[i] * right[i]
        lo, hi = i - left[i] + 1, i + right[i] - 1
        w2.step(f"Day {i} (price {prices[i]}): it's the low of stretches starting at days {lo}..{i} ({left[i]} choices) and ending at days {i}..{hi} ({right[i]} choices): {left[i]}×{right[i]} stretches, contributing {prices[i]}×{left[i] * right[i]} = {prices[i] * left[i] * right[i]}.", Row(prices, st={**{k: "mark" for k in range(lo, hi + 1)}, i: "active"}, label="prices"), Vars(total=acc))
    w2.step(f"Same total, {acc}, with each stretch counted once by its low.", result=acc)

    w3 = Steps("Find both boundaries with monotonic stacks: the previous strictly smaller price (left) and the next smaller-or-equal price (right).")
    stack, lv = [], []
    for i in range(n):
        while stack and prices[stack[-1]] >= prices[i]:
            stack.pop()
        lv.append(i - (stack[-1] if stack else -1))
        w3.step(f"Left pass, day {i}: pop prices ≥ {prices[i]}; the stopper is {('day ' + str(stack[-1])) if stack else 'the start'}. Left count {lv[-1]}.", Row(prices, st={i: "active"}, label="prices"), Row([f"{k}:{prices[k]}" for k in stack] or ["·"], label="stack (day:price)"), Row(lv + ["·"] * (n - i - 1), label="left"))
        stack.append(i)
    stack, rv, acc = [], [0] * n, 0
    for i in range(n - 1, -1, -1):
        while stack and prices[stack[-1]] > prices[i]:
            stack.pop()
        rv[i] = (stack[-1] if stack else n) - i
        acc += prices[i] * lv[i] * rv[i]
        w3.step(f"Right pass, day {i}: pop prices > {prices[i]}; the stopper is {('day ' + str(stack[-1])) if stack else 'the end'}. Right count {rv[i]}; add {prices[i]}×{lv[i]}×{rv[i]}.", Row(prices, st={i: "active"}, label="prices"), Row([f"{k}:{prices[k]}" for k in stack] or ["·"], label="stack (day:price)"), Row(["·"] * i + rv[i:], label="right"), Vars(total=acc))
        stack.append(i)
    w3.step(f"Total {acc}, modulo 10⁹ + 7.", result=acc)

    sol(
        "sum-of-stretch-lows",
        summary="""
            Instead of finding the low of each stretch, ask how many stretches each day is the low of. Day `i` is the low of
            every stretch that starts after the previous cheaper day and ends before the next day that's no more expensive:
            `left × right` stretches. Two monotonic-stack passes find those neighbours. Total = Σ price × left × right, O(n).
        """,
        question=[
            """
            Every stretch of consecutive days (there are n(n+1)/2 of them) has a low, its smallest price. Add up all those
            lows, modulo 10⁹ + 7.

            - **Single days count:** a one-day stretch's low is that day's price.
            - **Prices can repeat**, so a stretch can contain its low twice. It must still be counted once.
            - **Up to 10⁵ days**: about 5 × 10⁹ stretches, too many to visit one by one.
            """
        ],
        think=[
            f"""
            Take `{prices}`. There are {n * (n + 1) // 2} stretches. Listing them by start day: from day 0 the lows are
            3, 1, 1, 1, 1; from day 1 they're all 1; and so on. The total is **{want}**.

            Now look at it from day 1 (price 1): it's the cheapest day, so it's the low of every stretch that contains it:
            2 possible starts × 4 possible ends = 8 stretches, contributing 8. Day 3 (price 4) is the low only of itself.
            """,
            table(["day", "price", "starts", "ends", "stretches", "contribution"], *[(i, prices[i], left[i], right[i], left[i] * right[i], prices[i] * left[i] * right[i]) for i in range(n)]),
            """
            Day `i` is the low of a stretch exactly when nothing in the stretch is cheaper. So the stretch can reach left
            until the previous cheaper day and right until the next cheaper day. Any start in that left range and any end in
            the right range work, independently: `left × right` stretches.

            **Ties:** days 2 and 4 both cost 2, and the stretch `2, 4, 2` would be counted twice. Fix this by letting a day
            reach left past equal prices but stop at equal prices on the right, so each stretch is credited to its rightmost
            low only.
            """,
        ],
        approaches=[
            approach(
                "Every start, running low",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start day, extend the stretch to the right one day at a time, keeping the running minimum. Each extension is a new stretch whose low is the running minimum: add it."],
                walk=w1,
                build=["For each start `i`, set `low = prices[i]`.", "For each end `j ≥ i`, update `low = min(low, prices[j])` and add it.", "Return the total modulo 10⁹ + 7."],
                code={
                    "python": """
                        class Solution:
                            def sumOfLows(self, prices: List[int]) -> int:
                                n = len(prices)  #@init
                                total = 0  #@init
                                for i in range(n):  #@start
                                    low = prices[i]  #@start
                                    for j in range(i, n):  #@extend
                                        low = min(low, prices[j])  #@extend
                                        total += low  #@add
                                return total % (10**9 + 7)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int sumOfLows(int[] prices) {
                                int n = prices.length;  //@init
                                long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@start
                                    int low = prices[i];  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        low = Math.min(low, prices[j]);  //@extend
                                        total += low;  //@add
                                    }
                                }
                                return (int) (total % 1_000_000_007);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int sumOfLows(vector<int>& prices) {
                                int n = prices.size();  //@init
                                long long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@start
                                    int low = prices[i];  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        low = min(low, prices[j]);  //@extend
                                        total += low;  //@add
                                    }
                                }
                                return total % 1000000007;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int sumOfLows(int* prices, int pricesSize) {
                            int n = pricesSize;  //@init
                            long long total = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@start
                                int low = prices[i];  //@start
                                for (int j = i; j < n; j++) {  //@extend
                                    if (prices[j] < low) low = prices[j];  //@extend
                                    total += low;  //@add
                                }
                            }
                            return total % 1000000007;  //@ret
                        }
                    """,
                },
                lines=[("init", "Running total.", {"java": "A `long`: the true total reaches about 1.5 × 10¹⁴ before the modulo.", "cpp": "`long long`: the true total reaches about 1.5 × 10¹⁴ before the modulo.", "c": "`long long`: the true total reaches about 1.5 × 10¹⁴ before the modulo."}), ("start", "Stretches starting at day `i`."), ("extend", "Adding day `j` can only lower the low."), ("add", "The stretch `i..j` has low `low`."), ("ret", "Reduce modulo 10⁹ + 7 at the end (the exact total fits in 64 bits).")],
                complexity=["**Time O(n²):** one step per stretch. **Space O(1).**"],
                limits=["One step per stretch is ~5 × 10⁹ steps for 10⁵ days. Counting stretches per day instead of visiting them is the way out."],
                slow=True,
            ),
            approach(
                "Count each day's stretches by walking outward",
                "better",
                "O(n²) worst",
                "O(1)",
                idea=["For each day `i`, walk left while prices are ≥ `prices[i]` and right while prices are > `prices[i]`. With `left` possible starts and `right` possible ends, day `i` is the (rightmost) low of `left × right` stretches; add `prices[i] × left × right`."],
                walk=w2,
                build=["For each day `i`: extend `l` left over prices `≥ prices[i]`.", "Extend `r` right over prices `> prices[i]`.", "Add `prices[i] × (i − l + 1) × (r − i + 1)`."],
                code={
                    "python": """
                        class Solution:
                            def sumOfLows(self, prices: List[int]) -> int:
                                n = len(prices)  #@init
                                total = 0  #@init
                                for i in range(n):  #@each
                                    l = i  #@left
                                    while l > 0 and prices[l - 1] >= prices[i]:  #@left
                                        l -= 1  #@left
                                    r = i  #@right
                                    while r < n - 1 and prices[r + 1] > prices[i]:  #@right
                                        r += 1  #@right
                                    total += prices[i] * (i - l + 1) * (r - i + 1)  #@add
                                return total % (10**9 + 7)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int sumOfLows(int[] prices) {
                                int n = prices.length;  //@init
                                long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    int l = i;  //@left
                                    while (l > 0 && prices[l - 1] >= prices[i]) l--;  //@left
                                    int r = i;  //@right
                                    while (r < n - 1 && prices[r + 1] > prices[i]) r++;  //@right
                                    total += (long) prices[i] * (i - l + 1) * (r - i + 1);  //@add
                                }
                                return (int) (total % 1_000_000_007);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int sumOfLows(vector<int>& prices) {
                                int n = prices.size();  //@init
                                long long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    int l = i;  //@left
                                    while (l > 0 && prices[l - 1] >= prices[i]) l--;  //@left
                                    int r = i;  //@right
                                    while (r < n - 1 && prices[r + 1] > prices[i]) r++;  //@right
                                    total += (long long) prices[i] * (i - l + 1) * (r - i + 1);  //@add
                                }
                                return total % 1000000007;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int sumOfLows(int* prices, int pricesSize) {
                            int n = pricesSize;  //@init
                            long long total = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@each
                                int l = i;  //@left
                                while (l > 0 && prices[l - 1] >= prices[i]) l--;  //@left
                                int r = i;  //@right
                                while (r < n - 1 && prices[r + 1] > prices[i]) r++;  //@right
                                total += (long long) prices[i] * (i - l + 1) * (r - i + 1);  //@add
                            }
                            return total % 1000000007;  //@ret
                        }
                    """,
                },
                lines=[("init", "Running total (64-bit in the typed languages)."), ("each", "Count the stretches whose low is day `i`."), ("left", "Starts can go left past prices at least as high (ties included), stopping at the previous strictly cheaper day."), ("right", "Ends can go right past strictly higher prices only, stopping at the next price ≤ this one. Together with the left rule, a stretch with a repeated low is credited only to its rightmost copy."), ("add", "Any of the `i − l + 1` starts with any of the `r − i + 1` ends.", {"java": "Cast to `long` before multiplying: price × starts × ends reaches ~7.5 × 10¹³.", "cpp": "Cast before multiplying: price × starts × ends reaches ~7.5 × 10¹³.", "c": "Cast before multiplying: price × starts × ends reaches ~7.5 × 10¹³."}), ("ret", "Reduce modulo 10⁹ + 7.")],
                complexity=["**Time O(n²) worst case:** if all prices are equal or sorted, the walks are long. Often much faster in practice. **Space O(1).**"],
                limits=["Each day walks to its boundaries from scratch, so a sorted or constant input still costs O(n²). The boundaries are 'previous smaller' and 'next smaller-or-equal', which a monotonic stack finds for all days in one pass."],
                slow=True,
            ),
            approach(
                "Boundaries from monotonic stacks",
                "best",
                "O(n)",
                "O(n)",
                idea=["Left pass: keep a stack of indices with strictly increasing prices. For day `i`, pop while the top's price ≥ `prices[i]`; the remaining top is the previous strictly cheaper day, so `left[i] = i − top` (or `i + 1` if empty). Right pass from the end: pop while the top's price > `prices[i]`; the top is the next day with price ≤ `prices[i]`, so `right[i] = top − i` (or `n − i`). Add `prices[i] × left[i] × right[i]`."],
                walk=w3,
                build=["Left pass with a stack, filling `left`.", "Right pass from the end with a fresh stack, computing `right` and adding the contribution.", "Return the total modulo 10⁹ + 7."],
                code={
                    "python": """
                        class Solution:
                            def sumOfLows(self, prices: List[int]) -> int:
                                n = len(prices)  #@init
                                left = [0] * n  #@init
                                stack = []  #@lpass
                                for i in range(n):  #@lpass
                                    while stack and prices[stack[-1]] >= prices[i]:  #@lpop
                                        stack.pop()  #@lpop
                                    left[i] = i - (stack[-1] if stack else -1)  #@lset
                                    stack.append(i)  #@lset
                                stack, total = [], 0  #@rpass
                                for i in range(n - 1, -1, -1):  #@rpass
                                    while stack and prices[stack[-1]] > prices[i]:  #@rpop
                                        stack.pop()  #@rpop
                                    right = (stack[-1] if stack else n) - i  #@rset
                                    total += prices[i] * left[i] * right  #@add
                                    stack.append(i)  #@rset
                                return total % (10**9 + 7)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int sumOfLows(int[] prices) {
                                int n = prices.length;  //@init
                                int[] left = new int[n], stack = new int[n];  //@init
                                int top = 0;  //@lpass
                                for (int i = 0; i < n; i++) {  //@lpass
                                    while (top > 0 && prices[stack[top - 1]] >= prices[i]) top--;  //@lpop
                                    left[i] = i - (top > 0 ? stack[top - 1] : -1);  //@lset
                                    stack[top++] = i;  //@lset
                                }
                                long total = 0;  //@rpass
                                top = 0;  //@rpass
                                for (int i = n - 1; i >= 0; i--) {  //@rpass
                                    while (top > 0 && prices[stack[top - 1]] > prices[i]) top--;  //@rpop
                                    int right = (top > 0 ? stack[top - 1] : n) - i;  //@rset
                                    total += (long) prices[i] * left[i] * right;  //@add
                                    stack[top++] = i;  //@rset
                                }
                                return (int) (total % 1_000_000_007);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int sumOfLows(vector<int>& prices) {
                                int n = prices.size();  //@init
                                vector<int> left(n), stack;  //@init
                                for (int i = 0; i < n; i++) {  //@lpass
                                    while (!stack.empty() && prices[stack.back()] >= prices[i]) stack.pop_back();  //@lpop
                                    left[i] = i - (stack.empty() ? -1 : stack.back());  //@lset
                                    stack.push_back(i);  //@lset
                                }
                                stack.clear();  //@rpass
                                long long total = 0;  //@rpass
                                for (int i = n - 1; i >= 0; i--) {  //@rpass
                                    while (!stack.empty() && prices[stack.back()] > prices[i]) stack.pop_back();  //@rpop
                                    int right = (stack.empty() ? n : stack.back()) - i;  //@rset
                                    total += (long long) prices[i] * left[i] * right;  //@add
                                    stack.push_back(i);  //@rset
                                }
                                return total % 1000000007;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int sumOfLows(int* prices, int pricesSize) {
                            int n = pricesSize;  //@init
                            int* left = malloc(n * sizeof(int));  //@init
                            int* stack = malloc(n * sizeof(int));  //@init
                            int top = 0;  //@lpass
                            for (int i = 0; i < n; i++) {  //@lpass
                                while (top > 0 && prices[stack[top - 1]] >= prices[i]) top--;  //@lpop
                                left[i] = i - (top > 0 ? stack[top - 1] : -1);  //@lset
                                stack[top++] = i;  //@lset
                            }
                            long long total = 0;  //@rpass
                            top = 0;  //@rpass
                            for (int i = n - 1; i >= 0; i--) {  //@rpass
                                while (top > 0 && prices[stack[top - 1]] > prices[i]) top--;  //@rpop
                                int right = (top > 0 ? stack[top - 1] : n) - i;  //@rset
                                total += (long long) prices[i] * left[i] * right;  //@add
                                stack[top++] = i;  //@rset
                            }
                            free(left);  //@ret
                            free(stack);  //@ret
                            return total % 1000000007;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "`left[i]` will hold the number of possible start days for stretches whose low is day `i`."),
                    ("lpass", "Left to right, the stack holds indices whose prices strictly increase from bottom to top."),
                    ("lpop", "Days priced ≥ today can't be anyone's 'previous cheaper day' from now on, since today is cheaper or equal and closer. Pop them."),
                    ("lset", "The top is the previous strictly cheaper day (or none, −1), so the starts run from just after it to `i`. Then push today."),
                    ("rpass", "Right to left with a fresh stack."),
                    ("rpop", "Pop days priced strictly higher; an equal price stays and acts as the stopper (the tie rule)."),
                    ("rset", "The top is the next day priced ≤ today (or none, `n`): ends run from `i` up to just before it."),
                    ("add", "Day `i` is the low of `left × right` stretches.", {"java": "64-bit product: up to ~7.5 × 10¹³.", "cpp": "64-bit product: up to ~7.5 × 10¹³.", "c": "64-bit product: up to ~7.5 × 10¹³."}),
                    ("ret", "The exact total fits in 64 bits; reduce it once at the end."),
                ],
                complexity=["**Time O(n):** each index is pushed and popped at most once per pass. **Space O(n)** for `left` and the stack."],
            ),
        ],
        takeaways=[
            """
            - **Contribution counting:** to sum a property over all subarrays, ask how many subarrays each element is
              responsible for, and multiply.
            - "Previous smaller" and "next smaller" for every element = two monotonic-stack passes.
            - With duplicates, make one side strict and the other not, so every subarray is credited exactly once.
            """
        ],
    )


@problem
def total_swing():
    readings = [4, 1, 4, 2]
    n = len(readings)
    lmax, rmax = reach(readings, lambda x, y: y <= x, lambda x, y: y < x)
    lmin, rmin = reach(readings, lambda x, y: y >= x, lambda x, y: y > x)
    smax = sum(v * l * r for v, l, r in zip(readings, lmax, rmax))
    smin = sum(v * l * r for v, l, r in zip(readings, lmin, rmin))
    want = smax - smin
    assert want == sum(max(readings[i:j + 1]) - min(readings[i:j + 1]) for i in range(n) for j in range(i, n))

    w1 = Steps("Fix each start; extend one reading at a time, keeping the running high and low, and add high − low each time.")
    total = 0
    for i in range(n):
        hi = lo = readings[i]
        sw = []
        for j in range(i, n):
            hi, lo = max(hi, readings[j]), min(lo, readings[j])
            sw.append(hi - lo)
        total += sum(sw)
        w1.step(f"Start at {i}: swings {sw}, adding {sum(sw)}.", Row(readings, st={i: "active"}, label="readings"), Row(["·"] * i + sw, label="swing"), Vars(total=total))
    w1.step(f"Total swing: {total}.", result=total)

    w2 = Steps("Total swing = (sum of every stretch's high) − (sum of every stretch's low). Count, for each reading, how many stretches it's the high of, and how many it's the low of.")
    for i in range(n):
        w2.step(f"Reading {i} ({readings[i]}): the high of {lmax[i]}×{rmax[i]} = {lmax[i] * rmax[i]} stretches, the low of {lmin[i]}×{rmin[i]} = {lmin[i] * rmin[i]}. Net contribution {readings[i]}×({lmax[i] * rmax[i]} − {lmin[i] * rmin[i]}) = {readings[i] * (lmax[i] * rmax[i] - lmin[i] * rmin[i])}.", Row(readings, st={i: "active"}, label="readings"), Row([lmax[k] * rmax[k] if k <= i else "·" for k in range(n)], label="times high"), Row([lmin[k] * rmin[k] if k <= i else "·" for k in range(n)], label="times low"))
    w2.step(f"Sum of highs {smax} − sum of lows {smin} = {want}. The counts come from monotonic stacks (previous/next greater for highs, smaller for lows).", result=want)

    sol(
        "total-swing",
        summary="""
            The sum of (high − low) over all stretches is (sum of all stretch highs) − (sum of all stretch lows), and each
            sum is a contribution count: reading `i` is the high of `left × right` stretches, where the boundaries are the
            nearest bigger readings on each side (one side strict, for ties), found by monotonic stacks. Same for lows.
            O(n), with 64-bit sums.
        """,
        question=[
            """
            For every stretch of consecutive readings, take its swing: largest minus smallest. Return the sum over all
            n(n+1)/2 stretches.

            - **Single readings have swing 0.**
            - **Readings can be negative and can repeat.**
            - **Up to 10⁵ readings with |value| ≤ 10⁶:** the answer can reach ~10¹⁶, so it needs 64-bit integers (the
              return type is `long`).
            """
        ],
        think=[
            f"""
            Take `{readings}`. The stretches from index 0 have swings 0, 3, 3, 3; from index 1: 0, 3, 3; from index 2: 0, 2;
            from index 3: 0. Total **{want}**.

            The swing mixes two things, but sums split: Σ(high − low) = Σhigh − Σlow. So the problem is two copies of "sum
            of every stretch's extreme", which is a contribution count: how many stretches is each reading the high (or
            low) of?
            """,
            table(["index", "reading", "high of", "low of", "net"], *[(i, readings[i], lmax[i] * rmax[i], lmin[i] * rmin[i], readings[i] * (lmax[i] * rmax[i] - lmin[i] * rmin[i])) for i in range(n)]),
            f"""
            Reading `i` is the high of a stretch when nothing in it is bigger: the stretch can reach left until the previous
            bigger reading and right until the next bigger one. The two 4s tie: let a reading reach left past equal values
            but stop at equal values on the right, so the stretch `4, 1, 4` is credited to one 4, not both. The highs sum to
            {smax}, the lows to {smin}, and {smax} − {smin} = {want}.

            A shortcut for the code: the low of a stretch is −(high of the negated stretch), so Σlow = −Σhigh(−readings), and
            the answer is `sumOfHighs(readings) + sumOfHighs(−readings)`.
            """,
        ],
        approaches=[
            approach(
                "Every start, running high and low",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start, extend the stretch rightwards, updating the running maximum and minimum; each extension adds `high − low`."],
                walk=w1,
                build=["For each start `i`, `hi = lo = readings[i]`.", "For each end `j`, update both and add `hi − lo`.", "Return the 64-bit total."],
                code={
                    "python": """
                        class Solution:
                            def totalSwing(self, readings: List[int]) -> int:
                                n = len(readings)  #@init
                                total = 0  #@init
                                for i in range(n):  #@start
                                    hi = lo = readings[i]  #@start
                                    for j in range(i, n):  #@extend
                                        hi = max(hi, readings[j])  #@extend
                                        lo = min(lo, readings[j])  #@extend
                                        total += hi - lo  #@add
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long totalSwing(int[] readings) {
                                int n = readings.length;  //@init
                                long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@start
                                    int hi = readings[i], lo = readings[i];  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        hi = Math.max(hi, readings[j]);  //@extend
                                        lo = Math.min(lo, readings[j]);  //@extend
                                        total += hi - lo;  //@add
                                    }
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long totalSwing(vector<int>& readings) {
                                int n = readings.size();  //@init
                                long long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@start
                                    int hi = readings[i], lo = readings[i];  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        hi = max(hi, readings[j]);  //@extend
                                        lo = min(lo, readings[j]);  //@extend
                                        total += hi - lo;  //@add
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long totalSwing(int* readings, int readingsSize) {
                            int n = readingsSize;  //@init
                            long long total = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@start
                                int hi = readings[i], lo = readings[i];  //@start
                                for (int j = i; j < n; j++) {  //@extend
                                    if (readings[j] > hi) hi = readings[j];  //@extend
                                    if (readings[j] < lo) lo = readings[j];  //@extend
                                    total += hi - lo;  //@add
                                }
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("init", "A 64-bit running total."), ("start", "Stretches starting at `i`: high and low start as the first reading."), ("extend", "The new reading may raise the high or lower the low."), ("add", "Swing of stretch `i..j` (fits in 32 bits: at most 2 × 10⁶)."), ("ret", "The total.")],
                complexity=["**Time O(n²):** one step per stretch. **Space O(1).**"],
                limits=["~5 × 10⁹ stretches for 10⁵ readings. Splitting the swing into highs minus lows turns this into two contribution counts that never visit stretches individually."],
                slow=True,
            ),
            approach(
                "Highs minus lows, by contribution",
                "best",
                "O(n)",
                "O(n)",
                idea=[
                    """
                    Write `sumOfHighs(a)`: for each `i`, `left` = distance to the previous strictly bigger value (pop the stack
                    while the top is ≤ `a[i]`), `right` = distance to the next bigger-or-equal value (pop while the top is
                    < `a[i]`); add `a[i] × left × right`.

                    Then `Σlow(a) = −sumOfHighs(−a)`, so the answer is `sumOfHighs(a) + sumOfHighs(−a)`.
                    """
                ],
                walk=w2,
                build=["Write `sumOfHighs(a)` with two monotonic-stack passes and a 64-bit total.", "Call it on the readings and on the negated readings.", "Return the sum of the two."],
                code={
                    "python": """
                        class Solution:
                            def totalSwing(self, readings: List[int]) -> int:
                                def sum_of_highs(a):  #@fn
                                    n = len(a)  #@fn
                                    left, stack = [0] * n, []  #@lpass
                                    for i in range(n):  #@lpass
                                        while stack and a[stack[-1]] <= a[i]:  #@lpass
                                            stack.pop()  #@lpass
                                        left[i] = i - (stack[-1] if stack else -1)  #@lpass
                                        stack.append(i)  #@lpass
                                    stack, total = [], 0  #@rpass
                                    for i in range(n - 1, -1, -1):  #@rpass
                                        while stack and a[stack[-1]] < a[i]:  #@rpass
                                            stack.pop()  #@rpass
                                        right = (stack[-1] if stack else n) - i  #@rpass
                                        total += a[i] * left[i] * right  #@add
                                        stack.append(i)  #@rpass
                                    return total  #@add
                                return sum_of_highs(readings) + sum_of_highs([-v for v in readings])  #@ret
                    """,
                    "java": """
                        class Solution {
                            private long sumOfHighs(int[] a, int sign) {  //@fn
                                int n = a.length;  //@fn
                                int[] left = new int[n], stack = new int[n];  //@lpass
                                int top = 0;  //@lpass
                                for (int i = 0; i < n; i++) {  //@lpass
                                    while (top > 0 && sign * a[stack[top - 1]] <= sign * a[i]) top--;  //@lpass
                                    left[i] = i - (top > 0 ? stack[top - 1] : -1);  //@lpass
                                    stack[top++] = i;  //@lpass
                                }
                                long total = 0;  //@rpass
                                top = 0;  //@rpass
                                for (int i = n - 1; i >= 0; i--) {  //@rpass
                                    while (top > 0 && sign * a[stack[top - 1]] < sign * a[i]) top--;  //@rpass
                                    int right = (top > 0 ? stack[top - 1] : n) - i;  //@rpass
                                    total += (long) sign * a[i] * left[i] * right;  //@add
                                    stack[top++] = i;  //@rpass
                                }
                                return total;  //@add
                            }  //@fn

                            public long totalSwing(int[] readings) {
                                return sumOfHighs(readings, 1) + sumOfHighs(readings, -1);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            long long sumOfHighs(vector<int>& a, int sign) {  //@fn
                                int n = a.size();  //@fn
                                vector<int> left(n), stack;  //@lpass
                                for (int i = 0; i < n; i++) {  //@lpass
                                    while (!stack.empty() && sign * a[stack.back()] <= sign * a[i]) stack.pop_back();  //@lpass
                                    left[i] = i - (stack.empty() ? -1 : stack.back());  //@lpass
                                    stack.push_back(i);  //@lpass
                                }
                                stack.clear();  //@rpass
                                long long total = 0;  //@rpass
                                for (int i = n - 1; i >= 0; i--) {  //@rpass
                                    while (!stack.empty() && sign * a[stack.back()] < sign * a[i]) stack.pop_back();  //@rpass
                                    int right = (stack.empty() ? n : stack.back()) - i;  //@rpass
                                    total += (long long) sign * a[i] * left[i] * right;  //@add
                                    stack.push_back(i);  //@rpass
                                }
                                return total;  //@add
                            }  //@fn

                        public:
                            long long totalSwing(vector<int>& readings) {
                                return sumOfHighs(readings, 1) + sumOfHighs(readings, -1);  //@ret
                            }
                        };
                    """,
                    "c": """
                        static long long sumOfHighs(int* a, int n, int sign, int* left, int* stack) {  //@fn
                            int top = 0;  //@lpass
                            for (int i = 0; i < n; i++) {  //@lpass
                                while (top > 0 && sign * a[stack[top - 1]] <= sign * a[i]) top--;  //@lpass
                                left[i] = i - (top > 0 ? stack[top - 1] : -1);  //@lpass
                                stack[top++] = i;  //@lpass
                            }
                            long long total = 0;  //@rpass
                            top = 0;  //@rpass
                            for (int i = n - 1; i >= 0; i--) {  //@rpass
                                while (top > 0 && sign * a[stack[top - 1]] < sign * a[i]) top--;  //@rpass
                                int right = (top > 0 ? stack[top - 1] : n) - i;  //@rpass
                                total += (long long) sign * a[i] * left[i] * right;  //@add
                                stack[top++] = i;  //@rpass
                            }
                            return total;  //@add
                        }  //@fn

                        long long totalSwing(int* readings, int readingsSize) {
                            int* left = malloc(readingsSize * sizeof(int));  //@ret
                            int* stack = malloc(readingsSize * sizeof(int));  //@ret
                            long long total = sumOfHighs(readings, readingsSize, 1, left, stack) + sumOfHighs(readings, readingsSize, -1, left, stack);  //@ret
                            free(left);  //@ret
                            free(stack);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("fn", "Sum of every stretch's high.", {"java": "`sign = −1` compares and adds the negated readings without copying the array: the highs of −a.", "cpp": "`sign = −1` works on the negated readings without copying: the highs of −a.", "c": "`sign = −1` works on the negated readings without copying: the highs of −a. The caller lends the scratch arrays."}),
                    ("lpass", "Left pass: pop values ≤ the current one; the remaining top is the previous strictly bigger value. `left[i]` counts the possible starts."),
                    ("rpass", "Right pass: pop values strictly smaller; the top is the next bigger-or-equal value, so a tied high is credited to its rightmost copy only. `right` counts the possible ends."),
                    ("add", "Reading `i` is the high of `left × right` stretches.", {"java": "The product reaches ~2.5 × 10¹⁵, so it's computed in `long`.", "cpp": "The product reaches ~2.5 × 10¹⁵, so it's computed in 64 bits.", "c": "The product reaches ~2.5 × 10¹⁵, so it's computed in 64 bits."}),
                    ("ret", "Σhigh(a) − Σlow(a) = Σhigh(a) + Σhigh(−a)."),
                ],
                complexity=["**Time O(n):** four stack passes, each pushing and popping every index at most once. **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - A sum of `max − min` over subarrays splits into two independent contribution counts.
            - `min(a) = −max(−a)`: one helper covers both, by negating.
            - Make one boundary strict and the other not, so a tie is credited once.
            """
        ],
    )
