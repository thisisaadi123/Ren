"""In-depth text for the counting and bucket-sort problems (merged into their sol() calls via sol.EXTRA)."""
from collections import Counter

from sol import EXTRA, table

NO_COMPARE = """
**Beating O(n log n) by not comparing.** Comparison sorts need about `n log n` comparisons in the worst case. When the
values are small integers, or we only need partial order information, we can skip comparisons entirely:

- **Counting sort:** count how many times each possible value appears, then write the values out in order. O(n + R)
  for a value range of size `R`.
- **Bucket sort / bucketing:** drop values into ranges ("buckets") whose order is known; often only a little
  information per bucket is needed.
"""

# ---------------------------------------------------------------- sort-the-grades
grades = [72, 95, 72, 40, 95, 88, 72]
gc = Counter(grades)
EXTRA["sort-the-grades"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Every possible grade (0 … 100) is known in advance: only 101 values.
        - Lots of repeats: counting handles them for free.
        - O(n) is required, so comparison sorts are out.
        """
    ],
    "think": [
        NO_COMPARE,
        f"""
        **Counting `{grades}`:** only the grades that occur are shown.
        """,
        table(["grade", "count"], *sorted(gc.items())),
        f"Reading the counts from 0 to 100: **{sorted(grades)}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Use a comparison sort. Correct, but O(n log n) where O(n) is possible."],
            "build": ["Sort."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["Compares values whose possible range is tiny and known; counting avoids comparisons."],
        },
        1: {
            "idea": [
                """
                Count each grade in an array of 101 slots, then write each grade as many times as it was counted, from 0 to
                100.

                **Why it's sorted.** The output lists grades in increasing order of value, each with its exact count.
                """
            ],
            "build": ["101 counters.", "Count.", "Write grades out in increasing order."],
            "complexity": ["**Time O(n + 101).** **Space O(101)** besides the output."],
        },
    },
    "takeaways": [
        """
        - **Small known range → counting sort**, O(n + R).
        - No comparisons, so the O(n log n) lower bound doesn't apply.
        - **Pitfall:** using it when `R` is huge (memory and time grow with the range).
        """
    ],
}


# ---------------------------------------------------------------- most-played-songs
plays, k = [7, 3, 7, 9, 3, 7, 12, 9, 3, 1], 3
pc = Counter(plays)
ranked = sorted(pc, key=lambda s: (-pc[s], s))
EXTRA["most-played-songs"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Song ids up to 10⁹: count with a hash map, not an array.
        - Ties in play count: smaller id first.
        - `k` can equal the number of different songs.
        """
    ],
    "think": [
        NO_COMPARE,
        f"""
        **Count, then rank only the distinct songs.** There may be many plays but far fewer songs; sorting the songs by
        `(−plays, id)` puts them in the required order. For `{plays}`, `k = {k}`:
        """,
        table(["song", "plays", "rank"], *[(s, pc[s], i + 1) for i, s in enumerate(ranked)]),
        f"Top {k}: **{ranked[:k]}**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each distinct song, count its plays by rescanning the log, then sort the songs by `(−count, id)`."],
            "build": ["Distinct songs.", "Count each by scanning.", "Sort and take `k`."],
            "complexity": ["**Time O(d · n + d log d)** for `d` distinct songs. **Space O(d).**"],
            "limits": ["Each song rescans the whole log. One pass with a hash map counts everything."],
        },
        1: {
            "idea": ["Count plays in a hash map, sort the distinct songs by `(−count, id)`, and return the first `k`."],
            "build": ["Hash-map counts.", "Sort distinct songs.", "Take `k`."],
            "complexity": ["**Time O(n + d log d).** **Space O(d).**"],
        },
    },
    "takeaways": [
        """
        - **Top-k by frequency:** count with a map, then sort (or bucket by count) only the distinct items.
        - Encode tie rules in the key tuple.
        - **Pitfall:** sorting all `n` plays instead of the `d` distinct songs.
        """
    ],
}


# ---------------------------------------------------------------- widest-gap-after-sorting
nums = [13, 2, 27, 8, 31, 20]
n, lo, hi = len(nums), min(nums), max(nums)
size = max(1, (hi - lo) // (n - 1))
count = (hi - lo) // size + 1
bmin, bmax = [None] * count, [None] * count
for x in nums:
    b = (x - lo) // size
    bmin[b] = x if bmin[b] is None else min(bmin[b], x)
    bmax[b] = x if bmax[b] is None else max(bmax[b], x)
brows, best, prev = [], 0, lo
for b in range(count):
    rng = f"{lo + b * size} … {lo + (b + 1) * size - 1}"
    if bmin[b] is None:
        brows.append((b, rng, "empty", "—", best))
        continue
    gap = bmin[b] - prev
    best = max(best, gap)
    brows.append((b, rng, f"min {bmin[b]}, max {bmax[b]}", f"{bmin[b]} − {prev} = {gap}", best))
    prev = bmax[b]
sgap = sorted(nums)
EXTRA["widest-gap-after-sorting"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Fewer than two numbers: 0.
        - All numbers equal: 0.
        - O(n) is required, so a full sort is out.
        """
    ],
    "think": [
        NO_COMPARE,
        f"""
        **The widest gap is at least the average gap.** In sorted order the `n − 1` neighbour gaps add up to
        `max − min`, so the widest is at least `(max − min) / (n − 1)`. For `{nums}`: `{hi} − {lo} = {hi - lo}` over
        {n - 1} gaps, average {(hi - lo) / (n - 1):.1f}.

        **Buckets narrower than that.** Make buckets of width `size = ⌊(max − min) / (n − 1)⌋` (at least 1). Two numbers
        in the same bucket differ by less than `size`, which is no more than the widest gap, so **the widest gap is never
        inside a bucket**: it's between the largest number of one non-empty bucket and the smallest of the next non-empty
        bucket. So each bucket only needs its min and max, and no sorting happens.
        """,
        f"**Buckets of width {size} starting at {lo}:**",
        table(["bucket", "range", "contents", "gap from previous bucket's max", "widest so far"], *brows),
        f"Widest gap **{best}** (sorted check: {max(sgap[i] - sgap[i - 1] for i in range(1, n))}).",
    ],
    "approaches": {
        0: {
            "idea": ["Sort and take the largest difference between neighbours."],
            "build": ["Sort.", "Largest neighbour difference."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["The problem asks for O(n). Only bucket boundaries matter, not the full order."],
        },
        1: {
            "idea": [
                """
                Compute `min`, `max` and `size`. Drop each number into bucket `(x − min) // size`, keeping only each
                bucket's min and max. Walk the buckets in order, measuring the gap from the previous non-empty bucket's
                max to the current one's min.

                **Why empty buckets are fine.** A gap that spans empty buckets is still measured: `prev` stays at the last
                non-empty bucket's max.
                """
            ],
            "build": ["Range and bucket width.", "Per-bucket min and max.", "Scan buckets, measuring gaps between neighbours."],
            "complexity": ["**Time O(n).** **Space O(n)** for at most about `n` buckets."],
        },
    },
    "takeaways": [
        """
        - **Maximum gap in O(n):** buckets narrower than the average gap; the answer is between buckets.
        - Keep only each bucket's min and max.
        - **Pitfall:** a bucket width of 0 when the range is small (clamp to 1).
        """
    ],
}
