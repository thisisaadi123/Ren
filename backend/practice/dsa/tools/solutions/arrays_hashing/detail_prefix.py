"""In-depth text for the prefix-sum problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

PREFIX = """
**Prefix sums.** Let `P[k]` be the sum of the first `k` elements (`P[0] = 0`). Then the sum of any stretch
`a[i .. j−1]` is `P[j] − P[i]`: everything up to `j`, minus everything before `i`. One O(n) pass builds `P`; after
that, every range sum costs O(1). Many "subarray sum" questions become questions about **pairs of prefix sums**.
"""


def prefix_of(a):
    p = [0]
    for x in a:
        p.append(p[-1] + x)
    return p


# ---------------------------------------------------------------- running-balance
ch = [5, -2, 10, -7, 3]
rb = prefix_of(ch)[1:]
EXTRA["running-balance"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The balance can go negative; nothing special happens.
        - One day: the answer is just that day's change.
        - Balances stay within ±10⁹, which fits in a 32-bit int.
        """
    ],
    "think": [
        PREFIX,
        f"""
        **Each day builds on yesterday.** Day `i`'s balance is day `i − 1`'s balance plus today's change. Recomputing from
        day 0 each time repeats all the earlier additions.
        """,
        table(["day", "change", "yesterday's balance", "balance"], *[(i, ch[i], rb[i - 1] if i else 0, rb[i]) for i in range(len(ch))]),
    ],
    "approaches": {
        0: {
            "idea": ["For each day, add up all changes from day 0 to that day."],
            "build": ["For each day, sum the changes so far.", "Store the sum."],
            "complexity": ["**Time O(n²):** about `n²/2` additions. **Space O(n)** for the output."],
            "limits": ["Day `i`'s sum contains day `i − 1`'s sum, which was just computed. Keeping a running total makes each day O(1)."],
        },
        1: {
            "idea": ["Keep a running `balance`. For each change, add it and record the new balance. This is exactly the prefix-sum array without its leading 0."],
            "build": ["`balance = 0`.", "Add each change and record."],
            "complexity": ["**Time O(n).** **Space O(n)** for the output."],
        },
    },
    "takeaways": [
        """
        - **Running totals are prefix sums.** Build them with one addition per element.
        - Reuse the previous answer instead of recomputing.
        - The same running-total idea underlies every other prefix-sum problem.
        """
    ],
}


# ---------------------------------------------------------------- range-totals
sales = [3, -1, 4, 1, 5, 9, -2]
P = prefix_of(sales)
qs = [[1, 4], [0, 6], [3, 3], [5, 6]]
EXTRA["range-totals"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A query with `l = r` is a single day.
        - Totals can reach `10⁵ × 10⁹ = 10¹⁴` in size: use 64-bit sums.
        - Up to 10⁵ queries, so each must be answered quickly.
        """
    ],
    "think": [
        PREFIX,
        f"**Prefix sums of `{sales}`:**",
        table(["k"] + list(range(len(P))), ["P[k]"] + P),
        "**Answering queries with `P[r + 1] − P[l]`:**",
        table(["query [l, r]", "P[r + 1]", "P[l]", "total"], *[([l, r], P[r + 1], P[l], P[r + 1] - P[l]) for l, r in qs]),
    ],
    "approaches": {
        0: {
            "idea": ["Answer each query by adding up its range directly."],
            "build": ["For each query, sum `sales[l .. r]`."],
            "complexity": ["**Time O(n · q)** in the worst case: 10¹⁰ additions for 10⁵ long queries. **Space O(q)** for the answers."],
            "limits": ["Overlapping queries re-add the same days. Precomputing prefix sums once answers every query in O(1)."],
        },
        1: {
            "idea": [
                """
                Build `P` once. Answer each query `[l, r]` with `P[r + 1] − P[l]`.

                **Why it's right.** `P[r + 1]` covers days `0 … r`; subtracting `P[l]` removes days `0 … l − 1`, leaving
                exactly `l … r`.
                """
            ],
            "build": ["Prefix sums with a leading 0.", "One subtraction per query."],
            "complexity": ["**Time O(n + q).** **Space O(n)** for the prefix sums."],
        },
    },
    "takeaways": [
        """
        - **Many range-sum queries on a fixed array:** prefix sums, O(1) per query.
        - The leading `P[0] = 0` removes the special case for `l = 0`.
        - **Pitfall:** off-by-one (`P[r] − P[l]` misses day `r`); 32-bit overflow.
        """
    ],
}


# ---------------------------------------------------------------- balance-point
wts = [2, 5, -3, 7, 1, 2, 1]
total = sum(wts)
brows, left, found = [], 0, None
for i, w in enumerate(wts):
    right = total - left - w
    brows.append((i, w, left, right, "balance point" if left == right else ""))
    if left == right and found is None:
        found = i
        break
    left += w
EXTRA["balance-point"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Index 0 has an empty left side (sum 0); the last index has an empty right side.
        - Negative weights mean sums don't grow steadily, so no early stopping on size.
        - Several balance points: return the leftmost.
        """
    ],
    "think": [
        PREFIX,
        f"""
        **Left and right from one running sum.** With `total` the sum of all weights and `left` the sum before index
        `i`, the right side is `total − left − weights[i]`. So one pass with a running `left` checks every index in O(1).
        For `{wts}` (total {total}):
        """,
        table(["i", "weight", "left", "right = total − left − weight", ""], *brows),
        f"Leftmost balance point: **{found}**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each index, add up the left side and the right side separately and compare."],
            "build": ["For each index, sum both sides.", "Return the first equal one."],
            "complexity": ["**Time O(n²).** **Space O(1)** (O(n) in Python for the slices)."],
            "limits": ["Every index re-adds almost the whole array. Prefix sums give both sides in O(1)."],
        },
        1: {
            "idea": ["Build prefix sums. Index `i` balances when `P[i] = P[n] − P[i + 1]` (left side vs right side)."],
            "build": ["Prefix sums.", "Check each index with two lookups."],
            "complexity": ["**Time O(n).** **Space O(n)** for the prefix array."],
            "limits": ["Stores the whole prefix array, but each check only needs the sum to the left, which a single running variable provides."],
        },
        2: {
            "idea": [
                """
                Compute `total`. Walk with `left = 0`: at index `i`, if `left == total − left − weights[i]`, return `i`;
                otherwise add `weights[i]` to `left`.

                **Why it's leftmost.** Indices are checked from left to right and the first success returns immediately.
                """
            ],
            "build": ["Total of all weights.", "Running left sum.", "Compare left with `total − left − weight`."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Left vs right sums:** `right = total − left − current`, with one running `left`.
        - Prefix sums with a running variable need no array at all.
        - **Pitfall:** including the current element in one of the sides.
        """
    ],
}


# ---------------------------------------------------------------- subarrays-hitting-target
nums, target = [1, 2, 1, 2, 1, 3], 3
seen, srows, cnt, pre = {0: 1}, [], 0, 0
for i, x in enumerate(nums):
    pre += x
    hits = seen.get(pre - target, 0)
    cnt += hits
    srows.append((i, x, pre, pre - target, hits, cnt))
    seen[pre] = seen.get(pre, 0) + 1
brute = sum(1 for i in range(len(nums)) for j in range(i, len(nums)) if sum(nums[i:j + 1]) == target)
EXTRA["subarrays-hitting-target"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Negative numbers are allowed, so a sliding window doesn't work (sums aren't monotone).
        - `target = 0`: stretches summing to zero, including repeated prefix values.
        - The count can reach about `n²/2 = 5 × 10⁹`: use 64 bits.
        """
    ],
    "think": [
        PREFIX,
        """
        **From stretches to pairs of prefixes.** A stretch ending at `j` sums to `target` exactly when some earlier prefix
        equals `P[j] − target`. So walk once, and at each position add **how many earlier prefixes** had that value. A
        hash map counts prefix values seen so far, starting with `{0: 1}` for the empty prefix.
        """,
        f"**Trace for target {target} on `{nums}`:**",
        table(["i", "value", "prefix", "looking for", "earlier prefixes with it", "count"], *srows),
        f"Total **{cnt}** (direct check of every stretch: {brute}).",
    ],
    "approaches": {
        0: {
            "idea": ["For every start, extend to the right with a running sum and count the ends where it equals the target."],
            "build": ["Every start.", "Running sum while extending.", "Count exact hits."],
            "complexity": ["**Time O(n²):** 5 × 10⁹ steps at the limit. **Space O(1).**"],
            "limits": ["It can't stop early (negative numbers can bring the sum back), so it always scans everything. Counting prefix values answers all stretches ending at a position at once."],
        },
        1: {
            "idea": [
                """
                Walk once with a running prefix. Before recording the current prefix, add the number of earlier prefixes
                equal to `prefix − target`. Start the map with the empty prefix (`0` seen once) so stretches starting at
                index 0 are counted.

                **Why each stretch is counted once.** A stretch `i … j` corresponds to the pair (prefix before `i`,
                prefix through `j`), counted exactly when `j` is processed.
                """
            ],
            "build": ["Map with `{0: 1}`.", "Running prefix.", "Add `seen[prefix − target]`.", "Record the prefix."],
            "complexity": ["**Time O(n)** expected. **Space O(n)** for the map."],
        },
    },
    "takeaways": [
        """
        - **Count subarrays with sum k (any signs):** prefix sums + hash map of counts.
        - Seed the map with the empty prefix.
        - **Pitfall:** using a sliding window, which needs non-negative values.
        """
    ],
}


# ---------------------------------------------------------------- longest-even-stretch
bits = [1, 0, 0, 1, 1, 1, 0, 1, 0]
first, bal, best, lrows = {0: -1}, 0, 0, []
for i, b in enumerate(bits):
    bal += 1 if b else -1
    if bal in first:
        cand = i - first[bal]
        best = max(best, cand)
        lrows.append((i, b, bal, f"seen first at {first[bal]}", f"stretch {first[bal] + 1}..{i}, length {cand}", best))
    else:
        first[bal] = i
        lrows.append((i, b, bal, "new: remember position", "—", best))
EXTRA["longest-even-stretch"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - All 0s or all 1s: no balanced stretch, answer 0.
        - The whole array may be balanced.
        - A balanced stretch always has even length.
        """
    ],
    "think": [
        PREFIX,
        """
        **Turn "equal counts" into "sum zero".** Replace each 0 by −1. A stretch has as many 0s as 1s exactly when its
        sum is 0, i.e. when the running balance is the same before and after it.

        **Longest means earliest.** For the balance value at position `i`, the longest stretch ending at `i` starts right
        after the **first** position where that balance occurred. So remember only the first position of each balance
        (with balance 0 at position −1 for the empty prefix).
        """,
        f"**Trace on `{bits}`:**",
        table(["i", "bit", "balance", "first time?", "stretch", "best"], *lrows),
        f"Longest balanced stretch: **{best}**.",
    ],
    "approaches": {
        0: {
            "idea": ["For every start, extend with a running balance (+1 for 1, −1 for 0); whenever it returns to 0, the stretch is balanced."],
            "build": ["Every start.", "Running balance.", "Record lengths where it's 0."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Quadratic. Equal balances at two positions mark a balanced stretch between them, so remembering first occurrences finds the longest in one pass."],
        },
        1: {
            "idea": [
                """
                Map each balance value to the first index where it occurred, seeded with `0 → −1`. Walk once; if the
                current balance was seen before, the stretch after its first occurrence is balanced, so compare its length;
                otherwise record the current index.

                **Why only the first occurrence matters.** For a fixed end, an earlier start gives a longer stretch;
                later occurrences of the same balance can only give shorter ones.
                """
            ],
            "build": ["Map `{0: −1}`.", "Running balance.", "Seen → measure; new → record."],
            "complexity": ["**Time O(n).** **Space O(n)** (balances range over `−n … n`, so an array of size `2n + 1` also works)."],
        },
    },
    "takeaways": [
        """
        - **Equal counts of two kinds:** map them to +1/−1 and look for equal prefix sums.
        - **Longest stretch with a given sum:** remember the **first** index of each prefix value.
        - **Pitfall:** overwriting the first index with later ones.
        """
    ],
}


# ---------------------------------------------------------------- sums-in-bounds
sn, lo, hi = [3, -2, 4, -5, 1], -1, 2
SP = prefix_of(sn)
pairs = [(i, j, SP[j] - SP[i]) for i in range(len(SP)) for j in range(i + 1, len(SP)) if lo <= SP[j] - SP[i] <= hi]
EXTRA["sums-in-bounds"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Values up to ±2³¹ and up to 3 × 10⁴ of them: prefix sums need 64 bits.
        - Negative numbers rule out a sliding window.
        - Both bounds are inclusive.
        """
    ],
    "think": [
        PREFIX,
        f"""
        **Pairs of prefix sums.** A run `i … j − 1` has sum `P[j] − P[i]`, so we count pairs `i < j` with
        `{lo} ≤ P[j] − P[i] ≤ {hi}`. For `{sn}`: `P = {SP}`. The qualifying pairs are:
        """,
        table(["i", "j", "run", "sum P[j] − P[i]"], *[(i, j, sn[i:j], s) for i, j, s in pairs]),
        f"""
        **{len(pairs)}** runs.

        **Counting pairs fast with merge sort.** Split the prefix array into a left half and a right half. Every pair
        `i < j` is either inside the left half, inside the right half, or **crosses** (i on the left, j on the right).
        The first two kinds are counted recursively. For crossing pairs only the *values* matter, not their order inside
        each half, so both halves may be sorted. With both sorted, for each left value `p`, the right values in
        `[p + lower, p + upper]` form one contiguous window, and as `p` increases that window only moves right: two
        pointers count all crossing pairs in linear time. Merging the halves keeps them sorted for the level above.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For every start, extend with a running sum and count sums inside the bounds."],
            "build": ["Every start.", "Running sum.", "Count sums within the bounds."],
            "complexity": ["**Time O(n²):** 4.5 × 10⁸ steps for `n = 3 × 10⁴`, too slow by the problem's own statement. **Space O(1).**"],
            "limits": ["Every run is examined individually. Counting pairs of prefix sums with merge sort handles many runs at once."],
        },
        1: {
            "idea": [
                """
                Build the prefix sums. `sort_count(a)` returns `a` sorted plus the number of pairs `i < j` inside `a` with
                `lower ≤ a[j] − a[i] ≤ upper`:

                1. Split in half and recurse on both.
                2. For each value `p` of the sorted left half, advance `lo` to the first right value `≥ p + lower` and
                   `hi` to the first right value `> p + upper`; add `hi − lo`.
                3. Merge the halves.

                **Why the pointers never move back.** Left values are increasing, so both window edges `p + lower` and
                `p + upper` increase too.
                """
            ],
            "build": ["Prefix sums (64-bit).", "Recursive split.", "Count crossing pairs with two pointers.", "Merge."],
            "complexity": ["**Time O(n log n):** each level does O(n) counting and merging, over `log n` levels. **Space O(n)** for the merge buffers."],
        },
    },
    "takeaways": [
        """
        - **Count subarray sums in a range:** prefix sums, then count pairs `P[j] − P[i]` in range.
        - **Merge sort counts cross pairs** in linear time once both halves are sorted.
        - **Pitfall:** 32-bit prefix sums; forgetting the empty prefix `P[0] = 0`.
        """
    ],
}
