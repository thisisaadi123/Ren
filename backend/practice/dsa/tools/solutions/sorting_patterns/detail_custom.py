"""In-depth text for the custom-order sorting problems (merged into their sol() calls via sol.EXTRA)."""
import bisect
import functools

from sol import EXTRA, table

KEYS = """
**Every custom order is a sort with the right key.** Decide what makes one item come before another, and express it
either as a **key** (a tuple compared element by element: first key, then the next to break ties) or as a
**comparator** (a rule for two items). The sort then does the rest in O(n log n). The thinking is all in choosing a key
or rule that really produces the required order.
"""

# ---------------------------------------------------------------- follow-the-guide
items, guide = [5, 9, 2, 7, 9, 4, 5, 1], [9, 5, 3]
rank = {v: i for i, v in enumerate(guide)}
keyed = sorted(items, key=lambda x: (rank.get(x, len(guide)), x))
EXTRA["follow-the-guide"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Guide values that don't occur among the items contribute nothing.
        - Repeated items stay together (same key).
        - Items not in the guide go last, in increasing order.
        """
    ],
    "think": [
        KEYS,
        f"""
        **The key here.** Give each guide value its position in the guide; anything not in the guide gets
        `len(guide)` (after every guide value). Then break ties by the value itself, which orders the leftovers
        increasingly. For items `{items}` and guide `{guide}`:
        """,
        table(["item", "key (guide position, value)"], *[(x, (rank.get(x, len(guide)), x)) for x in items]),
        f"Sorted by key: **{keyed}**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each guide value, scan the items and pull out its copies; finally sort the unused items and append them."],
            "build": ["For each guide value, collect matching items.", "Sort the leftovers.", "Concatenate."],
            "complexity": ["**Time O(n · g + n log n)** for `n` items and `g` guide values. **Space O(n).**"],
            "limits": ["Scans all items once per guide value. A rank map and one sort handle everything together."],
        },
        1: {
            "idea": [
                """
                Map each guide value to its index. Sort the items by `(rank or len(guide), value)`.

                **Why the tie-breaker is safe for guide items.** Items with the same rank have the same value, so the
                second key changes nothing for them; it only orders the leftovers.
                """
            ],
            "build": ["Rank map from the guide.", "Sort by (rank, value)."],
            "complexity": ["**Time O(g + n log n).** **Space O(g + n).**"],
        },
    },
    "takeaways": [
        """
        - **Order by a reference list:** rank map + tuple key.
        - Use a sentinel rank for "not listed" to push those items last.
        - **Pitfall:** a comparator that looks up ranks with a linear search (O(n · g) per comparison).
        """
    ],
}


# ---------------------------------------------------------------- largest-number-from-pieces
pieces = [30, 3, 34, 5, 9]
strs = [str(p) for p in pieces]
cmp = lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)
ordered = sorted(strs, key=functools.cmp_to_key(cmp))
pairs = [("3", "30"), ("34", "3"), ("9", "5"), ("30", "34")]
EXTRA["largest-number-from-pieces"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - All pieces are 0: return `"0"`, not `"000"`.
        - Plain numeric or plain string order is wrong: `3` must come before `30` (`330 > 303`), although `"30" > "3"`.
        - Pieces up to 10⁹ and up to 10⁴ of them: the result has up to 10⁵ digits, so build a string.
        """
    ],
    "think": [
        KEYS,
        """
        **The glue rule.** Look at two neighbouring pieces `a` then `b`. Swapping them only changes that stretch of the
        number, `a + b` vs `b + a` (string concatenation), and both have the same length. So `a` should come first exactly
        when `a + b > b + a`.
        """,
        table(["a", "b", "a + b", "b + a", "first"], *[(a, b, a + b, b + a, a if a + b > b + a else b) for a, b in pairs]),
        f"""
        **Why sorting by this rule is valid.** The rule is consistent (transitive): `a` before `b` and `b` before `c`
        implies `a` before `c`, so it defines a proper order that a sort can use. And in the best arrangement no
        neighbouring pair can be improved by swapping, which is exactly what the sorted order guarantees (an exchange
        argument).

        For `{pieces}`: `{ordered}` → **`{''.join(ordered)}`**.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Bubble sort with the glue rule: repeatedly swap neighbouring pieces whenever `b + a > a + b`, until no swap happens."],
            "build": ["Pieces as strings.", "Bubble passes with the glue rule.", "Join; fix all-zero output."],
            "complexity": ["**Time O(n² · L)** for pieces of length up to `L` (10 digits). **Space O(n · L).**"],
            "limits": ["Bubble sort is quadratic. The same rule plugged into an O(n log n) sort does the job."],
        },
        1: {
            "idea": ["Convert to strings, sort with the comparator \"`a` first if `a + b > b + a`\", join, and return `\"0\"` if the result starts with 0."],
            "build": ["Strings.", "Sort with the glue comparator.", "Join and handle the all-zero case."],
            "complexity": ["**Time O(n log n · L).** **Space O(n · L).**"],
        },
    },
    "takeaways": [
        """
        - **Arrange pieces to make the largest concatenation:** compare `a + b` with `b + a`.
        - Pairwise "which goes first" rules work when they're transitive (exchange argument).
        - **Pitfall:** returning `"00…0"` instead of `"0"`.
        """
    ],
}


# ---------------------------------------------------------------- nesting-boxes
boxes = [[5, 4], [6, 4], [6, 7], [2, 3], [5, 6]]
order = sorted(boxes, key=lambda b: (b[0], -b[1]))
tails, nrows = [], []
for w, h in order:
    i = bisect.bisect_left(tails, h)
    if i == len(tails):
        tails.append(h)
        act = f"extends the longest chain (now {len(tails)})"
    else:
        tails[i] = h
        act = f"replaces tails[{i}] (a chain of length {i + 1} can end lower)"
    nrows.append((f"{w}×{h}", h, act, list(tails)))
EXTRA["nesting-boxes"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Equal widths (or equal heights) can't nest: "strictly smaller in both".
        - One box: the answer is 1.
        - Boxes can't be rotated.
        """
    ],
    "think": [
        KEYS,
        """
        **Reduce two dimensions to one.** Sort by width. Then a nesting chain uses strictly increasing widths, and it must
        also use strictly increasing heights: a chain is a **strictly increasing subsequence of heights**.

        **The tie trick.** Boxes with equal widths can't nest, but if they were sorted by increasing height, their heights
        would look like a valid increasing run. Sorting equal widths by **decreasing** height makes their heights
        non-increasing, so at most one of them can be in any strictly increasing subsequence.

        **Longest increasing subsequence in O(n log n).** Keep `tails[i]` = the smallest possible last height of an
        increasing chain of length `i + 1`. For each height, binary-search the first tail `≥` it and replace it (or append
        if it's larger than all tails). `tails` stays sorted, and its length is the answer.
        """,
        f"**Sorted by (width ↑, height ↓):** `{order}`",
        table(["box", "height", "what happens", "tails"], *nrows),
        f"Longest chain: **{len(tails)}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Sort by width; `chain[i]` = longest nesting ending at box `i`, computed from every earlier box that fits strictly inside."],
            "build": ["Sort.", "For each box, check all earlier boxes.", "Take the best chain."],
            "complexity": ["**Time O(n²):** 10¹⁰ checks at the limit. **Space O(n).**"],
            "limits": ["Quadratic. After the tie-aware sort, the question is a longest increasing subsequence, which binary search solves in O(n log n)."],
        },
        1: {
            "idea": [
                """
                Sort by `(width, −height)`, then compute the longest strictly increasing subsequence of the heights with
                the `tails` array and `bisect_left` (first tail `≥ h`), which enforces strict increase.
                """
            ],
            "build": ["Sort by width ascending, height descending.", "LIS on heights with binary search.", "Return the length."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **2-D nesting (envelopes):** sort by one dimension, LIS on the other; break ties so equal first coordinates can't chain.
        - `bisect_left` gives strictly increasing; `bisect_right` would allow equal heights.
        - **Pitfall:** sorting ties by increasing height.
        """
    ],
}


# ---------------------------------------------------------------- reconstruct-the-line
people = [[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]
line, rrows = [], []
for h, k in sorted(people, key=lambda p: (-p[0], p[1])):
    line.insert(k, [h, k])
    rrows.append((f"[{h}, {k}]", k, [list(x) for x in line]))
EXTRA["reconstruct-the-line"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - People of equal height count each other ("at least as tall").
        - A person with `ahead = 0` has nobody taller or equal in front.
        - The input always describes some valid line.
        """
    ],
    "think": [
        KEYS,
        """
        **Tallest first.** A shorter person is invisible to a taller person's count. So if we place people from tallest
        to shortest, each new person is at most as tall as everyone already placed, and everyone placed so far counts
        toward their `ahead`. Inserting them at index `ahead` gives them exactly `ahead` taller-or-equal people in front.
        People placed later are shorter, so they never change earlier people's counts. For equal heights, processing
        them in increasing `ahead` order means a later equal-height person is inserted behind the earlier ones, so their
        counts stay right too.

        **Trace** for `[[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]`, sorted by height ↓ then `ahead` ↑:
        """,
        table(["person", "insert at", "line after"], *rrows),
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Shortest first: sort by height ascending (ties: `ahead` descending) and put each person into the
                `(ahead + 1)`-th **empty** slot from the front. Empty slots will later be filled by taller (or equal) people,
                so exactly `ahead` of them end up in front.
                """
            ],
            "build": ["Empty line of `n` slots.", "Sort shortest first.", "Place each person in the right empty slot."],
            "complexity": ["**Time O(n²):** each placement scans for empty slots. **Space O(n).**"],
            "limits": ["Each placement scans the line. Inserting tallest first is shorter to write (still O(n²) with list inserts, fine for n ≤ 2000)."],
        },
        1: {
            "idea": [
                """
                Sort by height descending, ties by `ahead` ascending, and insert each person at index `ahead` of the growing
                line.

                **Why it's correct.** When a person is inserted, everyone already in the line is at least as tall, so
                index `ahead` gives exactly `ahead` of them in front. Later insertions are of shorter people (who don't
                count) or equal-height people with larger `ahead` (inserted behind them).
                """
            ],
            "build": ["Sort by (−height, ahead).", "Insert each at index `ahead`."],
            "complexity": ["**Time O(n²)** for list insertions (n ≤ 2000). **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Queue reconstruction:** tallest first, insert at index `ahead`.
        - Process items in an order where later items don't disturb earlier ones.
        - **Pitfall:** sorting equal heights by `ahead` descending in the tallest-first approach.
        """
    ],
}
