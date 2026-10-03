"""In-depth text for the complement-lookup problems (merged into their sol() calls via sol.EXTRA)."""
from collections import Counter
from itertools import product

from sol import EXTRA, table

COMPLEMENT = """
**The complement idea.** When a pair has to satisfy an equation like `x + y = target`, choosing `x` *forces* `y`: it
must be exactly `target − x`. So instead of trying every partner, **store what you've seen** in a hash map and **look
up the one value you need**. One pass, O(1) expected per lookup, O(n) total. Looking up *before* storing the current
element guarantees an element never pairs with itself.
"""


# ---------------------------------------------------------------- two-gifts
prices, budget = [3, 8, 11, 2, 15, 7], 9
where, grows, ans = {}, [], None
for j, p in enumerate(prices):
    need = budget - p
    hit = need in where
    grows.append((j, p, need, f"yes, at {where[need]}" if hit else "no", "{" + ", ".join(f"{k}: {v}" for k, v in where.items()) + "}"))
    if hit:
        ans = [where[need], j]
        break
    where[p] = j
EXTRA["two-gifts"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Negative prices (coupons) are allowed, so sums can be anything, and sorting tricks must keep track of indices.
        - Two gifts with the same price can be the pair (`[4, 4]` with budget 8).
        - The answer must be two **different** gifts and in index order `i < j`.
        """
    ],
    "think": [
        COMPLEMENT,
        f"**Hash-map trace** for budget {budget} on `{prices}` (the map stores price → index of the gifts seen so far):",
        table(["j", "price", "partner needed", "partner seen?", "map before storing"], *grows),
        f"Answer **{ans}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Try every pair `i < j` and return the one that sums to the budget."],
            "build": ["Two nested loops.", "Return the first exact pair."],
            "complexity": ["**Time O(n²):** about 5 × 10⁹ pairs for `n = 10⁵`. **Space O(1).**"],
            "limits": ["For each gift, the partner's price is known exactly (`budget − price`), yet the loop searches for it by trying everything."],
        },
        1: {
            "idea": [
                """
                Sort the **indices** by price (so original positions are kept), then squeeze two pointers from the cheapest
                and the most expensive: too big drops the expensive end, too small drops the cheap end.

                **Why it's correct.** If the total is too big, the most expensive gift overshoots even with the cheapest
                remaining partner, so it can't be in the pair; symmetrically for too small.
                """
            ],
            "build": ["Sort indices by price.", "Pointers at both ends.", "Move the side that can't be in the pair.", "Return the two original indices in order."],
            "complexity": ["**Time O(n log n)** for the sort. **Space O(n)** for the index order."],
            "limits": ["Sorting costs O(n log n) and extra memory for the order. A hash map finds the pair in one O(n) pass."],
        },
        2: {
            "idea": [
                """
                Walk the gifts once with a map from price to index. For gift `j`, compute `need = budget − price[j]`. If
                `need` is in the map, the pair is `[map[need], j]`; otherwise store `price[j] → j`.

                **Why the pair is found.** When the second gift of the pair is reached, the first one is already stored,
                so the lookup succeeds at exactly that moment, and the earlier index comes first automatically.
                """
            ],
            "build": ["Empty map price → index.", "For each gift, look up its partner.", "Return on a hit, else store the gift."],
            "complexity": ["**Time O(n)** expected. **Space O(n)** for the map."],
        },
    },
    "takeaways": [
        """
        - **Pair with a fixed sum:** one pass with a hash map of complements.
        - **Look up before storing** so an element never pairs with itself.
        - **Pitfall:** sorting the values and losing the original indices.
        """
    ],
}


# ---------------------------------------------------------------- divisible-pairs
nums, k = [4, 7, 2, 5, 9, 1], 3
rem = [x % k for x in nums]
rc = Counter(rem)
seen, drows, tot = [0] * k, [], 0
for x in nums:
    r = x % k
    need = (k - r) % k
    tot += seen[need]
    drows.append((x, r, need, seen[need], tot))
    seen[r] += 1
EXTRA["divisible-pairs"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Remainder 0 pairs with remainder 0.
        - When `k` is even, remainder `k/2` pairs with itself.
        - `k = 1`: every pair works, `n(n − 1)/2` of them; the count needs 64 bits.
        """
    ],
    "think": [
        COMPLEMENT,
        f"""
        **Work with remainders.** Whether `x + y` is divisible by `k` depends only on `x mod k` and `y mod k`: their
        remainders must add up to 0 or `k`. So remainder `r` needs a partner with remainder `(k − r) mod k`. For
        `{nums}` and `k = {k}` the remainders are `{rem}`.

        **Counting without pairs.** Walk the numbers once, keeping how many earlier numbers had each remainder. Each
        number pairs with all earlier numbers whose remainder complements its own:
        """,
        table(["number", "remainder", "partner remainder", "earlier partners", "total"], *drows),
        f"Total **{tot}** pairs.",
    ],
    "approaches": {
        0: {
            "idea": ["Test every pair `i < j` for `(nums[i] + nums[j]) % k == 0`."],
            "build": ["Two nested loops.", "Count divisible sums."],
            "complexity": ["**Time O(n²):** 5 × 10⁹ pairs at the limit. **Space O(1).**"],
            "limits": ["Divisibility only depends on remainders, so numbers with the same remainder are interchangeable; counting them by remainder avoids looking at pairs."],
        },
        1: {
            "idea": [
                f"""
                Count how many numbers have each remainder. Then pair up groups:

                - remainder 0 with itself: `c₀ (c₀ − 1) / 2` pairs;
                - remainder `r` with `k − r` for `0 < r < k − r`: `c_r · c_(k−r)` pairs;
                - if `k` is even, remainder `k/2` with itself: `c (c − 1) / 2` pairs.

                Here the counts are {dict(sorted(rc.items()))}.
                """
            ],
            "build": ["Count remainders.", "Pairs within remainder 0.", "Pairs across `r` and `k − r`.", "Pairs within `k/2` when `k` is even."],
            "complexity": ["**Time O(n + k).** **Space O(k)** for the counts."],
            "limits": ["Correct, but it has three separate cases to get right. Counting partners as you go handles all of them with one rule."],
        },
        2: {
            "idea": [
                """
                One pass. For each number with remainder `r`, add how many **earlier** numbers have remainder
                `(k − r) mod k`, then record `r`.

                **Why each pair is counted once.** A pair `i < j` is counted exactly when `j` is processed, because `i` was
                recorded earlier. The `(k − r) mod k` form makes remainder 0 look up remainder 0, and remainder `k/2` look
                up itself, without special cases.
                """
            ],
            "build": ["Remainder counts, all 0.", "For each number: add the partner count, then record its remainder."],
            "complexity": ["**Time O(n + k).** **Space O(k).**"],
        },
    },
    "takeaways": [
        """
        - **Divisibility of sums → remainders:** `r` pairs with `(k − r) mod k`.
        - Counting partners seen so far counts each pair once, with no special cases.
        - **Pitfall:** forgetting the self-paired remainders (0, and `k/2` for even `k`).
        """
    ],
}


# ---------------------------------------------------------------- four-lists-zero
A, B, C, D = [2, -1, 0], [1, -2, 3], [-3, 0, 1], [1, 2, -1]
sums = Counter(w + x for w in A for x in B)
frows, tot4 = [], 0
for y in C:
    for z in D:
        need = -(y + z)
        tot4 += sums[need]
        if sums[need]:
            frows.append((y, z, y + z, need, sums[need]))
brute4 = sum(1 for t in product(A, B, C, D) if sum(t) == 0)
EXTRA["four-lists-zero"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Tuples are counted by positions, so equal values at different positions count separately.
        - The count can reach `n⁴ = 6.25 × 10¹⁰`: use 64 bits.
        - Values are at most 2²⁸ in size, so any sum of four fits in 32-bit `int`.
        """
    ],
    "think": [
        COMPLEMENT,
        f"""
        **Split the tuple in half (meet in the middle).** `a + b + c + d = 0` means `a + b = −(c + d)`. So count every
        sum `a[i] + b[j]` in a map (n² entries), then for every pair `(c[k], d[l])` look up how many first-half pairs have
        the needed sum. Two O(n²) phases instead of O(n⁴).

        **First half** for `a = {A}`, `b = {B}`: {dict(sorted(sums.items()))}.

        **Second half** (only the pairs that find partners):
        """,
        table(["c", "d", "c + d", "needed a + b", "matching first-half pairs"], *frows),
        f"Total **{tot4}** (checking all {len(A) ** 4} tuples directly gives {brute4}).",
    ],
    "approaches": {
        0: {
            "idea": ["Four nested loops over every tuple; count the zero sums."],
            "build": ["One loop per list.", "Count tuples summing to 0."],
            "complexity": ["**Time O(n⁴):** 6.25 × 10¹⁰ tuples for `n = 500`. **Space O(1).**"],
            "limits": ["The last element is forced by the first three, so the fourth loop is a search that a count table can answer."],
        },
        1: {
            "idea": ["Count the values of `d` once. Loop over `a`, `b`, `c`; the fourth value must be `−(a + b + c)`, so add its count."],
            "build": ["Count `d`.", "Three nested loops.", "Add the count of the forced fourth value."],
            "complexity": ["**Time O(n³):** 1.25 × 10⁸ lookups for `n = 500`. **Space O(n).**"],
            "limits": ["Still cubic. Splitting into two pairs makes both halves quadratic."],
        },
        2: {
            "idea": [
                """
                Count all `a[i] + b[j]` sums in a map. Then for every `c[k] + d[l]`, add the count of `−(c[k] + d[l])`.

                **Why each tuple is counted once.** A zero tuple `(i, j, k, l)` is counted exactly when its `(k, l)` is
                processed, as one of the `sums[−(c + d)]` first-half pairs, which include its `(i, j)`.
                """
            ],
            "build": ["Map of all `a + b` sums with counts.", "For each `c + d`, add the count of its negation."],
            "complexity": ["**Time O(n²)** expected: 2.5 × 10⁵ insertions and lookups. **Space O(n²)** for the map."],
        },
    },
    "takeaways": [
        """
        - **Meet in the middle:** split a k-part condition into two halves, count one half, look up the other.
        - Trades O(n⁴) time for O(n²) time and O(n²) memory.
        - **Pitfall:** storing sums in a set instead of counting them, which loses multiplicities.
        """
    ],
}


# ---------------------------------------------------------------- pairs-a-gap-apart
gn, gk = [6, 2, 9, 4, 2, 11, 7], 2
gc = Counter(gn)
prow = [(x, x + gk, "yes" if x + gk in gc else "no") for x in sorted(gc)]
gans = sum(1 for x in gc if x + gk in gc)
EXTRA["pairs-a-gap-apart"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Pairs are counted by **values**, so duplicates don't create extra pairs.
        - `k = 0`: the pair is `(x, x)`, which needs `x` at two different positions.
        - `k > 0`: `x` and `x + k` are different values, so they're automatically at different positions.
        """
    ],
    "think": [
        COMPLEMENT,
        f"""
        **Think in values, not positions.** A pair is `(x, x + k)`, so choosing `x` decides the pair. Count each distinct
        value once and ask whether its partner exists. For `{gn}` and `k = {gk}`:
        """,
        table(["x (distinct)", "partner x + k", "present?"], *prow),
        f"""
        **{gans}** distinct pairs.

        **The `k = 0` case.** Then the "partner" is `x` itself, and every value trivially finds itself. What's actually
        needed is a second copy, so count the values that appear at least twice.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For each position whose value hasn't appeared earlier, scan the whole list for `x + k` at another position."],
            "build": ["Skip values seen to the left.", "Search for the partner elsewhere.", "Count each distinct value once."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Both the duplicate check and the partner search are linear scans. Sorting or a hash map makes them fast."],
        },
        1: {
            "idea": [
                """
                Sort a copy. For each first copy of a value `x`, binary-search for `x + k` strictly to its right. Searching
                to the right handles `k = 0` correctly: a second copy of `x` must sit just after the first.
                """
            ],
            "build": ["Sort.", "Skip repeated values.", "Binary-search the partner to the right."],
            "complexity": ["**Time O(n log n).** **Space O(n)** for the sorted copy."],
            "limits": ["A binary search per value. A hash map of counts answers each lookup in O(1) expected time."],
        },
        2: {
            "idea": [
                """
                Count every value in a hash map. If `k = 0`, count values with at least two copies. Otherwise count the
                distinct values `x` whose `x + k` is also a key.

                **Why pairs aren't double-counted.** Each pair `(x, x + k)` is counted only from its smaller value `x`.
                """
            ],
            "build": ["Count values.", "`k = 0`: values with count ≥ 2.", "`k > 0`: distinct `x` with `x + k` present."],
            "complexity": ["**Time O(n)** expected. **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Distinct pairs with a fixed difference:** iterate distinct values, look up `x + k`.
        - Handle `k = 0` separately: it needs a second copy, not a different value.
        - **Pitfall:** counting from both ends of a pair (looking up `x − k` as well).
        """
    ],
}
