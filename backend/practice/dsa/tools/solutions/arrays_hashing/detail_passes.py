"""In-depth text for the prefix/suffix-pass problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

PASSES = """
**Two passes, one from each side.** Many "everything except me" or "everything to my left/right" questions split
into a part that depends only on what comes **before** an index and a part that depends only on what comes **after**
it. A left-to-right pass accumulates the first part, a right-to-left pass accumulates the second, and each index
combines them in O(1). Two linear passes replace an O(n) scan per index.
"""

# ---------------------------------------------------------------- taller-ahead
hts = [4, 9, 2, 7, 3, 3, 1]
out, best, trows = [-1] * len(hts), -1, []
for i in range(len(hts) - 1, -1, -1):
    out[i] = best
    trows.append((i, hts[i], best, max(best, hts[i])))
    best = max(best, hts[i])
EXTRA["taller-ahead"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The last building has nothing after it: `−1`.
        - "Strictly after": a building's own height never counts for itself.
        - All equal heights: every answer except the last is that height.
        """
    ],
    "think": [
        PASSES,
        f"""
        **Only the right-hand pass is needed.** "Tallest building after `i`" is a running maximum taken from the right.
        Walk from the end, carrying `best` = tallest building seen so far (to the right of the current one): write `best`
        as the answer **before** folding in the current building. For `{hts}`:
        """,
        table(["i", "height", "answer (best so far)", "best after including it"], *trows),
        f"Answers **{out}**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each building, scan everything after it for the maximum."],
            "build": ["For each building, scan to the end.", "Store the maximum (or −1)."],
            "complexity": ["**Time O(n²).** **Space O(1)** besides the output."],
            "limits": ["Building `i`'s scan repeats building `i + 1`'s scan plus one more element. Carrying the maximum from the right reuses it."],
        },
        1: {
            "idea": [
                """
                Walk from right to left with `best = −1`. At each building, record `best`, then update
                `best = max(best, height)`.

                **Invariant.** Just before processing index `i`, `best` is the maximum of `heights[i+1 …]` (or −1 if
                empty), exactly the required answer.
                """
            ],
            "build": ["Output filled with −1, `best = −1`.", "Right to left: write `best`, then fold in the height."],
            "complexity": ["**Time O(n).** **Space O(1)** besides the output."],
        },
    },
    "takeaways": [
        """
        - **"Maximum to my right":** a running maximum from the right; write before you fold.
        - Same pattern for minimum, sum, product to the left or right.
        - **Pitfall:** updating `best` before writing it (includes the building itself).
        """
    ],
}


# ---------------------------------------------------------------- everyone-elses-product
nums = [3, -1, 2, 2, -2]
n = len(nums)
pre, suf = [1] * n, [1] * n
for i in range(1, n):
    pre[i] = pre[i - 1] * nums[i - 1]
for i in range(n - 2, -1, -1):
    suf[i] = suf[i + 1] * nums[i + 1]
ans = [pre[i] * suf[i] for i in range(n)]
EXTRA["everyone-elses-product"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Zeros: one zero makes every other answer 0; two zeros make every answer 0. Division would fail here, which is
          why it's banned.
        - Negative values flip signs; nothing special is needed.
        - Products fit in 64 bits by the constraints (at most 60 factors of ±2).
        """
    ],
    "think": [
        PASSES,
        f"""
        **Split each answer into left and right.** The product of everything except `nums[i]` is
        `(product of nums[0 … i−1]) × (product of nums[i+1 … n−1])`. Both parts are running products. For `{nums}`:
        """,
        table(["i", "nums[i]", "product to the left", "product to the right", "answer"], *[(i, nums[i], pre[i], suf[i], ans[i]) for i in range(n)]),
    ],
    "approaches": {
        0: {
            "idea": ["For each index, multiply all the other elements together."],
            "build": ["For each index, loop over the others.", "Store the product."],
            "complexity": ["**Time O(n²).** **Space O(1)** besides the output."],
            "limits": ["Neighbouring answers share almost all their factors. Running products from both ends compute every answer from two shared passes."],
        },
        1: {
            "idea": ["Build `prefix[i]` = product before `i` and `suffix[i]` = product after `i`; each answer is `prefix[i] × suffix[i]`."],
            "build": ["Prefix products.", "Suffix products.", "Multiply them index by index."],
            "complexity": ["**Time O(n).** **Space O(n)** for the two extra arrays."],
            "limits": ["The two arrays aren't needed: the output can hold the prefix products, and the suffix product can be a single running variable."],
        },
        2: {
            "idea": [
                """
                First pass (left to right): `out[i] = left`, then `left *= nums[i]`. Second pass (right to left):
                `out[i] *= right`, then `right *= nums[i]`.

                **Invariant.** In the first pass, `left` is the product of everything before `i`; in the second, `right` is
                the product of everything after `i`. So each `out[i]` ends as left × right.
                """
            ],
            "build": ["Output of ones.", "Left pass writes products before each index.", "Right pass multiplies in products after each index."],
            "complexity": ["**Time O(n).** **Space O(1)** besides the output."],
        },
    },
    "takeaways": [
        """
        - **"All except me" without division:** prefix × suffix.
        - Store one side in the output and carry the other in a variable.
        - **Pitfall:** dividing the total product by `nums[i]` (fails on zeros).
        """
    ],
}


# ---------------------------------------------------------------- rain-on-the-skyline
w = [3, 0, 2, 0, 4, 1, 0, 2]
nw = len(w)
lm = [max(w[:i + 1]) for i in range(nw)]
rm = [max(w[i:]) for i in range(nw)]
water = [min(lm[i], rm[i]) - w[i] for i in range(nw)]
lo, hi, lmax, rmax, tot, prows = 0, nw - 1, 0, 0, 0, []
while lo < hi:
    if w[lo] < w[hi]:
        lmax = max(lmax, w[lo])
        tot += lmax - w[lo]
        prows.append((lo, hi, f"left ({w[lo]} < {w[hi]})", f"left max {lmax}", lmax - w[lo], tot))
        lo += 1
    else:
        rmax = max(rmax, w[hi])
        tot += rmax - w[hi]
        prows.append((lo, hi, f"right ({w[hi]} ≤ {w[lo]})", f"right max {rmax}", rmax - w[hi], tot))
        hi -= 1
EXTRA["rain-on-the-skyline"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The first and last columns never hold water (it flows off the ends).
        - Strictly increasing or decreasing skylines hold nothing.
        - The total can reach about `10⁵ × 10⁵ = 10¹⁰`: use 64 bits.
        """
    ],
    "think": [
        PASSES,
        f"""
        **Water above one column.** Water above column `i` rises until it would spill over the lower of the two tallest
        walls around it: level `min(tallest on the left, tallest on the right)`, including the column itself. The water is
        that level minus the column's height. For `{w}`:
        """,
        table(["i", "height", "tallest left (incl.)", "tallest right (incl.)", "water"], *[(i, w[i], lm[i], rm[i], water[i]) for i in range(nw)]),
        f"""
        Total **{sum(water)}**.

        **Settling the lower side with two pointers.** Move inward from both ends, always on the side with the **lower**
        current wall. Invariant: the wall under the pointer that stays put is at least as tall as every wall already
        passed on the moving side. So when the left wall is lower, the right side certainly has a wall at least as tall
        as the left maximum, and the left column's level is just the left maximum: its water is settled without knowing
        the true right maximum.
        """,
        table(["lo", "hi", "move", "running max", "water added", "total"], *prows),
    ],
    "approaches": {
        0: {
            "idea": ["For each column, scan left and right for the tallest walls and add `min(left, right) − height`."],
            "build": ["For each column, find both maxima by scanning.", "Add the water."],
            "complexity": ["**Time O(n²).** **Space O(1)** (Python's slices cost O(n))."],
            "limits": ["Each column rescans both sides; the maxima are running maxima that two passes compute for all columns."],
        },
        1: {
            "idea": ["Precompute `left_max[i]` (left to right) and `right_max[i]` (right to left), then sum `min(left_max, right_max) − height`."],
            "build": ["Running maximum from the left.", "Running maximum from the right.", "Sum the water."],
            "complexity": ["**Time O(n).** **Space O(n)** for the two arrays."],
            "limits": ["Two extra arrays. Two pointers settle each column using only the maximum on its own side."],
        },
        2: {
            "idea": [
                """
                `lo` and `hi` at the ends, with running maxima on each side. If `walls[lo] < walls[hi]`, update the left
                maximum, add `left_max − walls[lo]`, and move `lo`; otherwise do the same on the right.

                **Why it's correct.** By the invariant above, the moving side's own running maximum is the lower of the two
                bounding walls for that column, so it's exactly the column's water level.
                """
            ],
            "build": ["Pointers at both ends, maxima at 0.", "Work on the lower side.", "Update its maximum and add its water."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Trapped water per column = min(max left, max right) − height.**
        - Two passes of running maxima, or two pointers that settle the lower side.
        - **Pitfall:** using the nearest taller wall instead of the tallest one.
        """
    ],
}
