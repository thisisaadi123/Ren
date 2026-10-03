"""In-depth text for the merge-two-sorted-sequences problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

MERGE = """
**The merge idea.** Two sorted inputs, one pointer into each. The smallest element not yet output must be at one of the
two pointers (everything after a pointer is at least as large as the element under it). So compare the two fronts,
output the smaller, and advance that pointer. When one input runs out, the rest of the other is already in order.
Every element is handled once: **O(n + m)**.
"""


def merge_rows(x, y):
    out, i, j, rows = [], 0, 0, []
    while i < len(x) and j < len(y):
        if x[i] <= y[j]:
            out.append(x[i])
            rows.append((x[i], y[j], f"take {x[i]} from the first", list(out)))
            i += 1
        else:
            out.append(y[j])
            rows.append((x[i], y[j], f"take {y[j]} from the second", list(out)))
            j += 1
    rest = x[i:] + y[j:]
    out += rest
    rows.append(("—" if i == len(x) else x[i], "—" if j == len(y) else y[j], f"one side is empty: append {rest}", list(out)))
    return rows


# ---------------------------------------------------------------- merge-two-shelves
L, R = [2, 5, 9, 12], [1, 5, 7, 15, 20]
EXTRA["merge-two-shelves"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One shelf empty: the answer is the other shelf.
        - Equal heights on both shelves: either may go first; taking the left one first keeps the merge stable.
        - Very different lengths: the leftover tail is copied in one go.
        """
    ],
    "think": [
        MERGE,
        f"**Trace on `{L}` and `{R}`:**",
        table(["front of first", "front of second", "action", "merged so far"], *merge_rows(L, R)),
    ],
    "approaches": {
        0: {
            "idea": ["Concatenate the two shelves and sort the result. Correct, but it throws away the fact that each shelf is already sorted."],
            "build": ["Concatenate.", "Sort."],
            "complexity": ["**Time O((n + m) log(n + m)).** **Space O(n + m).**"],
            "limits": ["Re-sorts data that's already in order. A merge needs only one comparison per output element."],
            "lines": {"sort": "Put both shelves together and sort everything."},
        },
        1: {
            "idea": [
                """
                Pointers `i` and `j` at the fronts. While both shelves have books, append the smaller front book (the left
                one on ties) and advance its pointer. Then append whatever remains.

                **Invariant.** The output holds the smallest `i + j` books of both shelves, in order, and both fronts are
                at least as large as the last output book.
                """
            ],
            "build": ["Two pointers at the fronts.", "Take the smaller front each step.", "Append the leftover tail."],
            "complexity": ["**Time O(n + m).** **Space O(n + m)** for the output."],
            "lines": {
                "init": "An empty output and a pointer at the front of each shelf.",
                "merge": "Compare the two front books and move the smaller one to the output; `≤` takes the left book first on ties.",
                "rest": "One shelf is used up; the other's remaining books are all larger and already sorted.",
                "ret": "The merged shelf.",
            },
        },
    },
    "takeaways": [
        """
        - **Merge = repeatedly take the smaller front.**
        - The leftover tail needs no comparisons.
        - **Pitfall:** forgetting to append the leftovers.
        - **Related:** merge sort's combine step; merging k lists uses a heap of fronts.
        """
    ],
}


# ---------------------------------------------------------------- merge-two-train-lines
A, B = [1, 4, 6], [2, 3, 6, 9]
EXTRA["merge-two-train-lines"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Either train (or both) can be empty.
        - Cars must be **reused**: change `next` links instead of creating new nodes.
        - Equal car numbers can come from either train.
        """
    ],
    "think": [
        MERGE,
        """
        **Merging linked lists by relinking.** Instead of copying values, keep a `tail` pointer to the last car of the
        merged train and set `tail.next` to the smaller front car, then advance. No new cars are created.

        **The dummy head.** The first car of the result isn't known until the first comparison. Start with a throw-away
        `dummy` car and let `tail = dummy`; then the first real car is attached exactly like every other one, and the
        answer is `dummy.next`.
        """,
        f"**Trace on `{A}` and `{B}`:**",
        table(["front of first", "front of second", "action", "merged so far"], *merge_rows(A, B)),
        """
        At the end, attaching the leftover part is a single link: `tail.next = whichever train still has cars`.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Read all car numbers into an array, sort it, and build a brand-new train. It works but doesn't reuse the cars, which the task asks for."],
            "build": ["Collect the values.", "Sort.", "Build a new list."],
            "complexity": ["**Time O((n + m) log(n + m)).** **Space O(n + m)** for the values and the new nodes."],
            "limits": ["Allocates a whole new train and re-sorts sorted data. Relinking the existing cars costs O(1) extra space."],
            "lines": {
                "read": "Every car number from both trains.",
                "sort": "Sort the numbers.",
                "build": "Create a new car for each number, linked after a dummy head.",
                "ret": "The first new car.",
            },
        },
        1: {
            "idea": [
                """
                `dummy` and `tail` start at a placeholder car. While both trains have cars, attach the smaller front car
                to `tail`, advance that train, and move `tail` forward. Finally attach the rest of the non-empty train.

                **Invariant.** The cars after `dummy` form the merged train of everything already detached, in order, and
                `tail` is its last car.
                """
            ],
            "build": ["Dummy head and tail.", "Attach the smaller front car each step.", "Attach the leftover train.", "Return `dummy.next`."],
            "complexity": ["**Time O(n + m).** **Space O(1):** only pointers change."],
            "lines": {
                "init": "A placeholder car so the first real car is attached like every other; `tail` is the end of the merged train.",
                "merge": "Link the smaller front car after `tail`, advance that train, then move `tail` to the new last car.",
                "rest": "One train is empty; the other is already sorted, so link all of it at once.",
                "ret": "The merged train starts right after the placeholder.",
            },
        },
    },
    "takeaways": [
        """
        - **Merging linked lists:** relink with a `tail` pointer; no copying.
        - **Dummy head** removes the special case for the first node.
        - **Pitfall:** forgetting to move `tail` after linking.
        """
    ],
}


# ---------------------------------------------------------------- closest-across-lists
ca, cb = [1, 7, 15, 30], [4, 12, 19, 28, 40]
crows, i, j, best = [], 0, 0, abs(ca[0] - cb[0])
while i < len(ca) and j < len(cb):
    d = abs(ca[i] - cb[j])
    best = min(best, d)
    if ca[i] < cb[j]:
        crows.append((ca[i], cb[j], d, best, f"{ca[i]} is smaller: its other partners are even farther, advance a"))
        i += 1
    else:
        crows.append((ca[i], cb[j], d, best, f"{cb[j]} is smaller (or equal): advance b"))
        j += 1
EXTRA["closest-across-lists"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One element in a list: compare it with the nearest values of the other.
        - Equal values across lists: the answer is 0.
        - Differences up to `2 × 10⁹` fit in a signed 32-bit int, but only just.
        """
    ],
    "think": [
        """
        **Which pointer to advance?** Look at `a[i]` and `b[j]` and suppose `a[i] < b[j]`. Every later value of `b` is
        at least `b[j]`, so it's even farther from `a[i]`: `a[i]` has already met its best partner among the remaining
        `b` values. The only way to get closer is a larger `a`, so advance `i`. Symmetrically, if `b[j] ≤ a[i]`, advance
        `j`.

        Every pair skipped this way is no closer than one already measured, so the minimum is never missed.
        """,
        f"**Trace on `a = {ca}`, `b = {cb}`:**",
        table(["a[i]", "b[j]", "difference", "best", "decision"], *crows),
        f"Smallest difference **{best}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Compare every value of `a` with every value of `b` and take the smallest difference."],
            "build": ["All pairs.", "Minimum absolute difference."],
            "complexity": ["**Time O(n · m):** 10¹⁰ pairs at the limits. **Space O(1).**"],
            "limits": ["Ignores the sorting. For each value only its nearest neighbours in the other list matter."],
            "lines": {"pairs": "Every (a, b) pair's absolute difference; keep the smallest."},
        },
        1: {
            "idea": [
                """
                For each `x` in `a`, binary-search `b` for the first value `≥ x`. The closest value to `x` is either that
                one or the one just before it.
                """
            ],
            "build": ["Start with any pair as the best.", "Binary-search each `x` in `b`.", "Check the two neighbours."],
            "complexity": ["**Time O(n log m).** **Space O(1).**"],
            "limits": ["Each search starts from scratch, although consecutive values of `a` land at non-decreasing positions in `b`. One walk over both lists uses that."],
            "lines": {
                "init": "Any pair gives a valid starting answer.",
                "search": "Where `x` would be inserted into `b`: the first value `≥ x`.",
                "near": "The nearest values to `x` are at that position and just before it.",
                "ret": "The smallest difference.",
            },
        },
        2: {
            "idea": [
                """
                Pointers at the start of both lists. Record `|a[i] − b[j]|`, then advance the pointer at the smaller value.
                Stop when either list ends.

                **Why stopping early is fine.** When `a` runs out, the last `a` value was smaller than the current `b[j]`,
                and all remaining `b` values are larger still: no closer pair remains (and symmetrically).
                """
            ],
            "build": ["Two pointers at the starts.", "Record the difference.", "Advance the smaller side."],
            "complexity": ["**Time O(n + m).** **Space O(1).**"],
            "lines": {
                "init": "Both pointers at the start; the first pair is the best so far.",
                "walk": "Record the current pair's difference.",
                "move": "The smaller value has met its closest remaining partner, so advance past it.",
                "ret": "The smallest difference.",
            },
        },
    },
    "takeaways": [
        """
        - **Closest pair across two sorted lists:** walk both, advance the smaller.
        - Binary search per element is the O(n log m) alternative.
        - **Pitfall:** advancing the larger value, which moves away from the answer.
        """
    ],
}


# ---------------------------------------------------------------- pairs-within-budget
mains, sides, budget = [5, 8, 12, 20], [2, 4, 9, 11], 16
prows, j, total = [], len(sides) - 1, 0
for x in mains:
    dropped = []
    while j >= 0 and x + sides[j] > budget:
        dropped.append(sides[j])
        j -= 1
    total += j + 1
    prows.append((x, budget - x, ", ".join(map(str, dropped)) or "—", sides[:j + 1], j + 1, total))
EXTRA["pairs-within-budget"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A main that costs more than the budget minus the cheapest side contributes 0.
        - "At most" includes equality.
        - Up to `10¹⁰` combinations and totals up to `2 × 10⁹`: use 64 bits.
        """
    ],
    "think": [
        """
        **For one main, the fitting sides are a prefix.** Sides are sorted, so the sides that fit with main `x` are
        exactly those priced at most `budget − x`: the first few sides. Count = length of that prefix.

        **The prefix only shrinks.** Mains are sorted too. A more expensive main leaves less money, so its prefix is no
        longer than the previous one. So one pointer `j` (the last side that fits) only moves left over the whole run:
        start it at the most expensive side and move it down as needed for each main.
        """,
        f"**Trace with budget {budget}:**",
        table(["main", "money left for a side", "sides dropped now", "sides that fit", "count", "total"], *prows),
        f"Total **{total}** combinations.",
    ],
    "approaches": {
        0: {
            "idea": ["Check every (main, side) combination."],
            "build": ["All pairs.", "Count those within budget."],
            "complexity": ["**Time O(n · m).** **Space O(1).**"],
            "limits": ["10¹⁰ combinations at the limits. The fitting sides for a main form a prefix that can be measured instead of enumerated."],
            "lines": {"pairs": "Every (main, side) combination; count it if it fits the budget."},
        },
        1: {
            "idea": ["For each main, binary-search the sides for the last price `≤ budget − main`; its position + 1 is the count."],
            "build": ["For each main, upper-bound search.", "Add the prefix length."],
            "complexity": ["**Time O(n log m).** **Space O(1).**"],
            "limits": ["Each search restarts, although the boundary only moves one way as mains get pricier."],
            "lines": {
                "init": "The running total (64-bit).",
                "search": "The number of sides priced at most `budget − main`: an upper-bound binary search.",
                "ret": "The total.",
            },
        },
        2: {
            "idea": [
                """
                `j` starts at the last side. For each main in increasing order, move `j` left while the pair is over budget;
                then sides `0 … j` all fit, so add `j + 1`.

                **Why `j` never needs to move right.** A side that's too expensive for this main is too expensive for every
                later (pricier) main.
                """
            ],
            "build": ["`j` at the most expensive side.", "For each main: move `j` left while over budget.", "Add `j + 1`."],
            "complexity": ["**Time O(n + m):** `j` moves left at most `m` times in total. **Space O(1).**"],
            "lines": {
                "init": "The total and the boundary `j`, starting at the most expensive side.",
                "loop": "Mains from cheapest to most expensive.",
                "shrink": "Drop sides that no longer fit; they won't fit any later main either.",
                "add": "Sides `0 … j` all fit with this main.",
                "ret": "The total number of combinations.",
            },
        },
    },
    "takeaways": [
        """
        - **Counting pairs across two sorted lists under a bound:** one pointer per list, moving in opposite directions.
        - Count a whole prefix at once instead of enumerating it.
        - **Pitfall:** resetting `j` for every main (back to O(n · m)).
        """
    ],
}
