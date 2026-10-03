"""In-depth text for the cyclic-sort problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

HOME = """
**Every value has a home.** When the values are `1 … n` (or should be), value `v` belongs at index `v − 1`. That turns
the array into a map from positions to positions: position `i` "points to" the home of the value it holds. Following
those pointers reveals the structure: duplicates, missing values, and **cycles** of values that must move among
themselves.
"""

# ---------------------------------------------------------------- fewest-swaps-to-sort
order = [2, 3, 1, 5, 4, 7, 6]
n = len(order)
seen, cycles, crow = [False] * n, [], []
for i in range(n):
    if seen[i]:
        continue
    cyc, j = [], i
    while not seen[j]:
        seen[j] = True
        cyc.append(j)
        j = order[j] - 1
    cycles.append(cyc)
    crow.append((" → ".join(str(p) for p in cyc + [cyc[0]]), [order[p] for p in cyc], len(cyc), len(cyc) - 1))
EXTRA["fewest-swaps-to-sort"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Already sorted: 0 swaps (every bib is its own cycle of length 1).
        - Reversed order: pairs swap with each other, `n // 2` swaps.
        - Any two runners may swap, not just neighbours.
        """
    ],
    "think": [
        HOME,
        f"""
        **Cycles.** From position `i`, the bib there belongs at `order[i] − 1`; from there, that position's bib belongs
        somewhere else, and so on until we return to `i`. The positions on one such loop only exchange bibs among
        themselves. For `{order}`:
        """,
        table(["cycle (positions)", "bibs on it", "length", "swaps needed"], *crow),
        f"""
        Total **{sum(r[3] for r in crow)}** = n − (number of cycles) = {n} − {len(cycles)}.

        **Why a cycle of length `L` needs exactly `L − 1` swaps.** Each swap that puts one bib home splits its cycle,
        and the last swap puts two bibs home at once, so `L − 1` swaps suffice. And no swap can do better: swapping two
        positions changes the number of cycles by exactly one (it either splits one cycle or merges two), while the
        sorted order has `n` cycles. Going from `c` cycles to `n` therefore needs at least `n − c` swaps.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For each position from the left, if it doesn't hold its own bib, find that bib further right and swap it in. Each swap fixes at least one position, and only necessary swaps happen."],
            "build": ["Copy the order.", "For each position, check its bib.", "Search for the right bib and swap it in.", "Count swaps."],
            "complexity": ["**Time O(n²)** because of the searches. **Space O(n)** for the copy."],
            "limits": ["The swap count is already optimal; only the searching is slow. Counting cycles gives the same number without performing any swaps."],
        },
        1: {
            "idea": [
                """
                Walk each cycle once with a `seen` array, counting cycles. The answer is `n − cycles`.

                **Why every position is visited once.** A cycle is walked from its first unseen position, marking every
                position on it; later starts skip seen positions.
                """
            ],
            "build": ["`seen` array.", "For each unseen position, walk its cycle and count it.", "Return `n − cycles`."],
            "complexity": ["**Time O(n).** **Space O(n)** for `seen`."],
        },
    },
    "takeaways": [
        """
        - **Minimum swaps to sort a permutation = n − number of cycles.**
        - Follow `i → order[i] − 1` to find cycles.
        - **Pitfall:** counting misplaced elements (that's the number of moves, not swaps).
        """
    ],
}


# ---------------------------------------------------------------- first-k-missing
nums, k = [4, 3, 2, 7, 8, 2, 3, 1], 3
limit = len(nums) + k
present = [False] * (limit + 1)
for v in nums:
    if 1 <= v <= limit:
        present[v] = True
missing, x = [], 1
while len(missing) < k:
    if not present[x]:
        missing.append(x)
    x += 1
EXTRA["first-k-missing"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Repeats, zeros and negatives don't help cover anything.
        - If `nums` is empty of positives, the answer is `1 … k`.
        - Huge values beyond `n + k` are irrelevant.
        """
    ],
    "think": [
        HOME,
        f"""
        **How far do we need to look?** Among `1 … n + k` there are `n + k` numbers, and `nums` can cover at most `n` of
        them, so at least `k` are missing. The first `k` missing numbers therefore all lie in `1 … n + k`. Values outside
        that range can be ignored, and a flag array of size `n + k` suffices.

        For `{nums}`, `k = {k}`, the range is `1 … {limit}`:
        """,
        table(["number"] + list(range(1, limit + 1)), ["present?"] + ["✓" if present[v] else "·" for v in range(1, limit + 1)]),
        f"The first {k} gaps: **{missing}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Count up from 1, checking each number with a linear search; collect the first `k` not found."],
            "build": ["`x = 1`.", "Search the list for `x`; collect it if absent.", "Stop after `k`."],
            "complexity": ["**Time O((n + k) · n)** in the worst case. **Space O(1)** besides the answer."],
            "limits": ["Every candidate rescans the list. A set or flag array answers membership in O(1)."],
        },
        1: {
            "idea": ["Put the numbers in a hash set, then count up from 1, collecting numbers not in the set until `k` are found."],
            "build": ["Hash set.", "Count up and collect missing numbers."],
            "complexity": ["**Time O(n + k)** expected. **Space O(n).**"],
            "limits": ["A hash set works but stores large irrelevant values too. Only `1 … n + k` matters, which a plain flag array covers."],
        },
        2: {
            "idea": [
                """
                Flags for `1 … n + k`: mark every value in that range, then scan upwards collecting unmarked numbers until
                `k` are found.

                **Why the scan never runs past `n + k`.** At least `k` numbers in the range are unmarked (argument above).
                """
            ],
            "build": ["`limit = n + k`, flags of that size.", "Mark values in range.", "Collect the first `k` unmarked numbers."],
            "complexity": ["**Time O(n + k).** **Space O(n + k).**"],
        },
    },
    "takeaways": [
        """
        - **First k missing positives:** the answers lie in `1 … n + k`; flags over that range.
        - Bound the search range by counting how many values can be covered.
        - **Pitfall:** sizing the flag array by the largest value (up to 10⁹).
        """
    ],
}


# ---------------------------------------------------------------- swapped-label
lab = [3, 1, 2, 5, 3]
nl = len(lab)
tot, sq = sum(lab), sum(v * v for v in lab)
d1 = tot - nl * (nl + 1) // 2
d2 = sq - nl * (nl + 1) * (2 * nl + 1) // 6
both = d2 // d1
dup = (d1 + both) // 2
EXTRA["swapped-label"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The duplicate may be smaller or larger than the missing number.
        - `n = 2`: one number twice, the other missing.
        - Sums of squares reach about `n³/3 ≈ 3.3 × 10¹⁴`: use 64 bits.
        """
    ],
    "think": [
        HOME,
        f"""
        **Two unknowns, two equations.** Call the duplicate `d` and the missing number `m`. Compared with `1 … n`:

        - the sum is off by `d − m`: `sum(labels) − n(n+1)/2 = d − m`;
        - the sum of squares is off by `d² − m²`: `Σ labels² − n(n+1)(2n+1)/6 = d² − m² = (d − m)(d + m)`.

        Dividing the second by the first gives `d + m`; together with `d − m` that pins down both. For `{lab}`:
        """,
        table(["quantity", "value"],
              ("sum of labels", tot), ("1 + … + n", nl * (nl + 1) // 2), ("d − m", d1),
              ("sum of squares", sq), ("1² + … + n²", nl * (nl + 1) * (2 * nl + 1) // 6), ("d² − m²", d2),
              ("d + m = (d² − m²) / (d − m)", both), ("d = ((d − m) + (d + m)) / 2", dup), ("m = (d + m) − d", both - dup)),
        f"Answer **[{dup}, {both - dup}]**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each number `1 … n`, count its occurrences by scanning; count 2 is the duplicate, count 0 the missing one."],
            "build": ["Count each number by scanning.", "Identify the duplicate and the missing number."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Each count rescans the list."],
        },
        1: {
            "idea": ["Count occurrences in an array of size `n + 1`; read off the value with count 2 and the one with count 0."],
            "build": ["Count array.", "Find counts 2 and 0."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
            "limits": ["O(n) extra memory; the array itself or arithmetic can replace it."],
        },
        2: {
            "idea": [
                """
                Cyclic sort: swap each label into its home slot (`v − 1`) until it's either home or blocked by an equal
                label already there. Afterwards, the one slot `p` not holding `p + 1` holds the duplicate, and `p + 1` is the
                missing number.
                """
            ],
            "build": ["Swap labels home until blocked.", "Find the slot without its own label."],
            "complexity": ["**Time O(n):** each swap sends a label home for good. **Space O(1)** (it reorders the input)."],
            "limits": ["Modifies the input. Arithmetic gets both numbers without touching it."],
        },
        3: {
            "idea": [
                """
                Compute `d − m` from the sum and `d² − m²` from the sum of squares, divide to get `d + m`, and solve.

                **Why the division is exact.** `d ≠ m`, so `d − m ≠ 0`, and `d² − m²` is a multiple of it.
                """
            ],
            "build": ["Sum and sum of squares (64-bit).", "Subtract the expected values.", "Solve the two equations."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **One duplicate + one missing:** two equations (sum and sum of squares), or cyclic sort, or XOR tricks.
        - Each equation compares the input with the ideal `1 … n`.
        - **Pitfall:** 32-bit overflow in the sum of squares.
        """
    ],
}
