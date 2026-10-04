"""In-depth text for the histogram-and-area problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

REACH = """
**How far can a bar reach?** For bar `i` with height `h`, the widest stretch where every bar is at least `h` runs from
just after the **nearest shorter bar on the left** to just before the **nearest shorter bar on the right**. Both
"nearest shorter" positions come from a monotonic stack in one pass each: pop bars that are not shorter than the
current one; what's left on top is the nearest shorter bar.

**Why this finds the best rectangle.** Any rectangle under a histogram is limited by its lowest bar. Taking each bar as
the lowest and stretching as far as possible covers the best rectangle for that height, so the best of these is the
best overall.
"""


def nearest_shorter(a):
    n = len(a)
    left, right, st = [-1] * n, [n] * n, []
    for i in range(n):
        while st and a[st[-1]] >= a[i]:
            st.pop()
        left[i] = st[-1] if st else -1
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and a[st[-1]] >= a[i]:
            st.pop()
        right[i] = st[-1] if st else n
        st.append(i)
    return left, right


# ---------------------------------------------------------------- poster-reach
panels = [3, 5, 4, 1, 4, 6, 2]
pl, pr = nearest_shorter(panels)
pw = [pr[i] - pl[i] - 1 for i in range(len(panels))]
EXTRA["poster-reach"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Equal neighbours: a poster can spread over panels of the **same** height.
        - The shortest panel reaches the whole fence.
        - "No shorter panel on a side" means the poster reaches that end (index −1 or n as the boundary).
        """
    ],
    "think": [
        REACH,
        f"**For `{panels}`:**",
        table(["panel", "height", "nearest shorter on the left", "nearest shorter on the right", "width = right − left − 1"],
              *[(i, panels[i], pl[i], pr[i], pw[i]) for i in range(len(panels))]),
        f"Widths: **{pw}**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each panel, walk left and right while neighbours are at least as tall."],
            "build": ["For each panel, extend left.", "Extend right.", "Width = right − left + 1."],
            "complexity": ["**Time O(n²)** (e.g. all panels equal). **Space O(1)** besides the output."],
            "limits": ["Walks overlap heavily. The nearest shorter panel on each side, found with stacks, gives every width directly."],
        },
        1: {
            "idea": [
                """
                Left pass: a stack of panel indices; pop while the top is at least as tall as the current panel; the
                remaining top is the nearest shorter panel on the left (−1 if none). Right pass: the same from the right
                (n if none). Width = `right − left − 1`.
                """
            ],
            "build": ["Left nearest-shorter pass.", "Right nearest-shorter pass.", "Widths from the two boundaries."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Reach of each bar = nearest shorter on both sides**, via two monotonic-stack passes.
        - Boundaries −1 and n stand for "no shorter bar".
        - **Pitfall:** popping only strictly taller bars (stops at equal ones, undercounting the width).
        """
    ],
}


# ---------------------------------------------------------------- biggest-billboard
hb = [2, 4, 5, 3, 1, 3]
bl, br = nearest_shorter(hb)
areas = [hb[i] * (br[i] - bl[i] - 1) for i in range(len(hb))]
best_b = max(areas)
st, orow = [], []
ext = hb + [0]
for i, h in enumerate(ext):
    popped = []
    while st and ext[st[-1]] >= h:
        height = ext[st.pop()]
        left = st[-1] if st else -1
        popped.append(f"{height}×{i - left - 1}={height * (i - left - 1)}")
    st.append(i)
    orow.append((i, h if i < len(hb) else "0 (sentinel)", ", ".join(popped) or "—", [ext[x] for x in st]))
EXTRA["biggest-billboard"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Buildings of height 0 split the row.
        - All equal heights: the whole row.
        - Areas reach `10⁹ × 10⁵ = 10¹⁴`: use 64 bits.
        """
    ],
    "think": [
        REACH,
        f"**Each building as the lowest point of the billboard, for `{hb}`:**",
        table(["building", "height", "stretch", "area"], *[(i, hb[i], f"{bl[i] + 1} … {br[i] - 1}", areas[i]) for i in range(len(hb))]),
        f"""
        Largest **{best_b}**.

        **One pass instead of two.** Keep a stack of buildings with increasing heights. When a building arrives that is
        not taller than the top, the top's right boundary has just been found (this building), and its left boundary is
        the building below it on the stack. So measure it as it's popped. A height-0 sentinel at the end flushes
        everything:
        """,
        table(["i", "height", "measured when popped (height × width)", "stack heights after"], *orow),
    ],
    "approaches": {
        0: {
            "idea": ["Try every run of neighbouring buildings with a running minimum height; area = min × width."],
            "build": ["Every start.", "Extend with a running minimum.", "Track the best area."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Quadratic. Each building's best rectangle is determined by its two nearest shorter neighbours."],
        },
        1: {
            "idea": ["Two monotonic-stack passes give each building's nearest shorter neighbours; area = height × (right − left − 1)."],
            "build": ["Left boundaries.", "Right boundaries and areas.", "Maximum."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
            "limits": ["Two passes and a boundary array; one pass can measure each building at the moment it's popped."],
        },
        2: {
            "idea": [
                """
                One left-to-right pass with an increasing stack and a 0 sentinel at the end. When a building is popped, the
                current index is its right boundary and the new stack top is its left boundary; measure it then.

                **Equal heights.** Popping on `≥` measures an earlier equal building too narrowly, but the last one of the
                equal group is measured with the full width, so the maximum is still right.
                """
            ],
            "build": ["Stack of indices, sentinel 0 appended.", "Pop and measure while the top isn't shorter.", "Push the current index."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Largest rectangle in a histogram:** increasing stack; measure each bar when it's popped.
        - The sentinel 0 forces every remaining bar to be measured.
        - **Pitfall:** computing the width as `i − popped_index` instead of `i − new_top − 1`.
        """
    ],
}


# ---------------------------------------------------------------- largest-clear-plot
land = ["01101", "11110", "11111", "01101"]
C = len(land[0])
h = [0] * C
lrows, best_l = [], 0
for r, row in enumerate(land):
    for c in range(C):
        h[c] = h[c] + 1 if row[c] == "1" else 0
    hl, hr = nearest_shorter(h)
    row_best = max(h[i] * (hr[i] - hl[i] - 1) for i in range(C))
    best_l = max(best_l, row_best)
    lrows.append((r, row, list(h), row_best, best_l))
EXTRA["largest-clear-plot"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No clear cell: 0.
        - One row or one column: the longest run of clear cells.
        - Cells are characters `'0'`/`'1'`, not numbers.
        """
    ],
    "think": [
        REACH,
        """
        **Turn the grid into histograms.** For each row, let `h[c]` be the number of consecutive clear cells ending at
        that row in column `c` (0 if the cell is rocky). Any clear rectangle has a bottom row; seen from that row, it's a
        rectangle under the histogram `h`. So run the largest-rectangle-in-a-histogram method once per row.
        """,
        f"**The field {' / '.join(land)}, row by row:**",
        table(["row", "cells", "histogram h", "best rectangle with this bottom row", "best so far"], *lrows),
        f"Largest clear plot: **{best_l}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Try every pair of corners and check whether the whole rectangle is clear."],
            "build": ["Every top-left and bottom-right corner.", "Check all cells inside.", "Track the best area."],
            "complexity": ["**Time O(R³ · C³)** in the worst case. **Space O(1).**"],
            "limits": ["Hopeless beyond tiny grids. Fixing the rows reduces the problem to runs of usable columns."],
        },
        1: {
            "idea": ["Fix the top row; extend the bottom row downwards while tracking which columns are clear in every row so far; the longest run of such columns times the height is a candidate."],
            "build": ["For each top row, a 'usable' flag per column.", "Extend the bottom row, updating the flags.", "Longest run of usable columns × height."],
            "complexity": ["**Time O(R² · C).** **Space O(C).**"],
            "limits": ["Quadratic in the number of rows. Keeping a histogram per row and using a stack gives O(R · C)."],
        },
        2: {
            "idea": [
                """
                Update the column heights row by row (`+1` for clear, reset to 0 for rocks), then run the one-pass
                histogram stack on them, with a 0 sentinel at the end.
                """
            ],
            "build": ["Heights array with one extra 0.", "Update heights for each row.", "Largest rectangle in that histogram."],
            "complexity": ["**Time O(R · C).** **Space O(C).**"],
        },
    },
    "takeaways": [
        """
        - **Largest all-ones rectangle in a grid:** a histogram per row + the histogram stack.
        - Heights reset to 0 on a blocked cell.
        - **Pitfall:** treating `'1'` as truthy without comparing the character.
        """
    ],
}


# ---------------------------------------------------------------- largest-pool
walls = [2, 0, 3, 1, 1, 4, 0, 2, 2, 0, 1]
nw = len(walls)
lm = [max(walls[:i + 1]) for i in range(nw)]
rm = [max(walls[i:]) for i in range(nw)]
water = [min(lm[i], rm[i]) - walls[i] for i in range(nw)]
pools, cur = [], 0
for w in water:
    if w > 0:
        cur += w
    elif cur:
        pools.append(cur)
        cur = 0
if cur:
    pools.append(cur)
peak = walls.index(max(walls))
EXTRA["largest-pool"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A column that holds no water ends a pool, even if water sits on both sides of it.
        - No water anywhere: 0.
        - Volumes reach about `10¹⁰`: use 64 bits.
        """
    ],
    "think": [
        """
        **Water per column, then pools.** Column `i` holds `min(tallest wall on its left, tallest on its right) −
        walls[i]` (both including itself). Consecutive columns holding water form one pool; a dry column ends it.
        """,
        f"**For `{walls}`:**",
        table(["column", "height", "max left", "max right", "water"], *[(i, walls[i], lm[i], rm[i], water[i]) for i in range(nw)]),
        f"""
        Pools: {pools}, so the answer is **{max(pools) if pools else 0}** (total water would be {sum(water)}).

        **Splitting at the tallest wall.** The tallest wall (index {peak}) is at least as tall as anything, so for every
        column to its left, the right bound is that peak, and the water level is just the running maximum from the left.
        Symmetrically on the right side. Two simple scans, no arrays.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For each column, scan both sides for the tallest walls; accumulate water into the current pool, resetting it at dry columns."],
            "build": ["For each column, both maxima by scanning.", "Water amount.", "Extend or reset the current pool."],
            "complexity": ["**Time O(n²).** **Space O(1)** (Python slices aside)."],
            "limits": ["Rescans both sides for every column; running maxima give them in O(1)."],
        },
        1: {
            "idea": ["Precompute `max_left` and `max_right` arrays, then one pass computes each column's water and grows or resets the current pool."],
            "build": ["Running maxima from both ends.", "Water per column.", "Pools split by dry columns."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
            "limits": ["Two arrays of maxima; splitting at the tallest wall needs only a running maximum per side."],
        },
        2: {
            "idea": [
                """
                Find the tallest wall. Scan from the left end up to it, keeping the running maximum as the water level, and
                from the right end down to it the same way. Within each scan, add water to the current pool and reset at
                dry columns; track the largest pool.

                **Why the running maximum is the level.** On the left side, the tallest wall lies to the right and is at
                least the running maximum, so the lower bound is the running maximum.
                """
            ],
            "build": ["Index of the tallest wall.", "Left scan up to it.", "Right scan down to it.", "Largest pool."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Trapped water with pool boundaries:** water per column, then group consecutive wet columns.
        - Splitting at the global maximum makes each side's level a running maximum.
        - **Pitfall:** summing all water instead of the largest pool.
        """
    ],
}
