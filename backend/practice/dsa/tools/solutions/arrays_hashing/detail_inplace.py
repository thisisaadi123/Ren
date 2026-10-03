"""In-depth text for in-place grid-marker problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table


def grid_table(g):
    return table(["r \\ c"] + list(range(len(g[0]))), *[[r] + list(row) for r, row in enumerate(g)])


SIMULTANEOUS = """
**Simultaneous updates.** Every cell's new value must be computed from the **old** values of its neighbours. Writing
new values straight into the grid breaks that: a neighbour processed later would read an already-updated cell. The
easy fix is a copy of the grid. The in-place fix is to store **both** the old and the new value in the same cell, using
spare bits:

- old value in the low bits (read with a mask, `x & 1` or `x & 255`);
- new value in the higher bits (written with `|=` and a shift);
- one final pass shifts every cell right, keeping only the new value.
"""

# ---------------------------------------------------------------- colony-next-generation
board = [[0, 1, 0, 0], [0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0]]
m, n = len(board), len(board[0])


def live_n(b, r, c):
    return sum(b[rr][cc] for rr in range(max(0, r - 1), min(m, r + 2)) for cc in range(max(0, c - 1), min(n, c + 2))) - b[r][c]


counts = [[live_n(board, r, c) for c in range(n)] for r in range(m)]
nxt = [[1 if counts[r][c] == 3 or (counts[r][c] == 2 and board[r][c]) else 0 for c in range(n)] for r in range(m)]
marked = [[board[r][c] | (2 if nxt[r][c] else 0) for c in range(n)] for r in range(m)]
EXTRA["colony-next-generation"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Border and corner cells have fewer than eight neighbours.
        - A 1 × 1 board: the single cell has no neighbours, so a living cell dies.
        - All updates are simultaneous: births and deaths must not affect each other's counts.
        """
    ],
    "think": [
        SIMULTANEOUS,
        "**The board:**",
        grid_table(board),
        "**Living neighbours of each cell (old values):**",
        grid_table(counts),
        """
        **Rules:** alive with 2 or 3 neighbours → stays alive; empty with exactly 3 → born; otherwise empty.

        **Two states in one cell.** Bit 0 holds the current state; bit 1 holds the next state. Counting reads `x & 1`, so
        it only ever sees the old state, even for cells already processed. After marking:
        """,
        grid_table(marked),
        "Shifting every cell right by one keeps the next state:",
        grid_table(nxt),
    ],
    "approaches": {
        0: {
            "idea": ["Copy the board; count each cell's living neighbours in the copy and write the new state into the board."],
            "build": ["Copy.", "Count neighbours from the copy.", "Apply the rules."],
            "complexity": ["**Time O(m · n)** (up to 8 neighbours each). **Space O(m · n)** for the copy."],
            "limits": ["A full copy of the board just to remember old values; each cell has spare bits that can hold the new value instead."],
        },
        1: {
            "idea": [
                """
                Pass 1: for each cell, count neighbours with `& 1` (old state only) and, if the cell will be alive, set bit
                1 (`|= 2`). Pass 2: shift every cell right by one.

                **Why counts stay correct.** Setting bit 1 never changes bit 0, and counting reads only bit 0.
                """
            ],
            "build": ["Count with `& 1`.", "Mark future-alive cells with `|= 2`.", "Shift everything right by one."],
            "complexity": ["**Time O(m · n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Simultaneous in-place updates:** keep old and new states in different bits of the same cell.
        - Always read through a mask that sees only the old state.
        - **Pitfall:** writing the new state directly (later cells read updated neighbours).
        """
    ],
}


# ---------------------------------------------------------------- soften-the-photo
img = [[10, 20, 30], [40, 250, 60], [70, 80, 90]]
im, inn = len(img), len(img[0])


def block(r, c):
    cells = [img[rr][cc] for rr in range(max(0, r - 1), min(im, r + 2)) for cc in range(max(0, c - 1), min(inn, c + 2))]
    return sum(cells), len(cells)


avg = [[block(r, c)[0] // block(r, c)[1] for c in range(inn)] for r in range(im)]
EXTRA["soften-the-photo"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Edge pixels average fewer than 9 values (6 on an edge, 4 in a corner).
        - The average is rounded down.
        - A single pixel stays the same.
        """
    ],
    "think": [
        SIMULTANEOUS,
        "**The photo:**",
        grid_table(img),
        "**Each pixel's block (sum / count):**",
        table(["r \\ c"] + list(range(inn)), *[[r] + [f"{block(r, c)[0]} / {block(r, c)[1]}" for c in range(inn)] for r in range(im)]),
        "**Softened (rounded down):**",
        grid_table(avg),
        """
        **Why 8 bits are enough.** Values are 0 … 255, so they fit in the low 8 bits; the average does too, so it can be
        stored in bits 8 … 15 (`|= avg << 8`) while the old value stays readable as `x & 255`.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Compute every pixel's average from the original image into a new grid."],
            "build": ["New grid.", "Average each 3 × 3 block (clipped at the edges)."],
            "complexity": ["**Time O(m · n)** (at most 9 values each). **Space O(m · n)** for the output."],
            "limits": ["Allocates a second grid. The unused high bits of each pixel can hold the new value."],
        },
        1: {
            "idea": [
                """
                Pass 1: for each pixel, average the old values (`& 255`) of its block and store the result in bits 8 … 15.
                Pass 2: shift every pixel right by 8.

                **Why the averages use old values.** Writing to bits 8 … 15 never changes bits 0 … 7, and every read masks
                with 255.
                """
            ],
            "build": ["Average old values (`& 255`).", "Store in the high byte.", "Shift right by 8."],
            "complexity": ["**Time O(m · n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Image filters in place:** pack the new value into unused high bits, then shift.
        - Clip the 3 × 3 block at the borders and divide by the real count.
        - **Pitfall:** reading neighbours without the mask after some cells already hold packed values.
        """
    ],
}
