"""In-depth text for the read/write-pointer problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

READ_WRITE = """
**The read/write idea.** One pointer, `read`, visits every element once. A second pointer, `write`, marks the end of
the part we're keeping, which always sits at the **front** of the array. Each kept element is copied to `a[write]`
and `write` moves on; a dropped element is simply not copied.

**Why it's safe to overwrite in place.** `write` never gets ahead of `read` (it moves at most once per element read),
so every write lands on a slot that has already been read. Nothing unread is ever lost.

**Invariant.** After reading the first `r` elements, `a[0 .. write)` holds exactly the elements that should be kept
among those `r`, in their original order.
"""

SHIFT = """
**Why deleting by shifting is slow.** Removing one element from the middle of an array means moving everything after
it one step left: O(n) per deletion. With many deletions that's O(n²), even though each kept element only needs to
move once, straight to its final slot.
"""


def rw_trace(values, keep, label):
    """Rows of a read/write run: read index, value, decision, write after, kept prefix."""
    a, w, rows = list(values), 0, []
    for r, x in enumerate(values):
        if keep(a, w, x):
            a[w] = x
            w += 1
            rows.append((r, x, "keep → a[" + str(w - 1) + "]", w, a[:w]))
        else:
            rows.append((r, x, label, w, a[:w]))
    return rows


# ---------------------------------------------------------------- remove-the-blanks
cells, blank = [4, 0, 7, 0, 0, 3, 8], 0
rows = rw_trace(cells, lambda a, w, x: x != blank, "blank: skip")
EXTRA["remove-the-blanks"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No blanks: the list is unchanged.
        - All blanks: the result is empty.
        - The kept cells must stay in their original order.
        """
    ],
    "think": [
        SHIFT,
        READ_WRITE,
        f"**Trace on `{cells}` with blank {blank}:**",
        table(["read", "value", "decision", "write after", "kept part"], *rows),
        f"Result **`{rows[-1][4]}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["Scan the list; whenever a blank is found, shift everything after it one place left and shrink the length. Don't advance the index after a deletion, because a new element has moved into it."],
            "build": ["Scan with an index.", "On a blank, shift the tail left and shrink.", "Otherwise move on."],
            "complexity": ["**Time O(n²)** when many cells are blank. **Space O(1)** besides the copy."],
            "limits": ["Each deletion moves the whole tail. The read/write pass moves each kept cell once, straight to its final slot."],
            "lines": {
                "init": "A working copy, its current length and the scan position.",
                "scan": "Look at each cell of the shrinking list.",
                "shift": "A blank: slide the rest of the list left over it and shrink the length. The index stays, because the next cell now sits here.",
                "ret": "The first `n` cells.",
            },
        },
        1: {
            "idea": [
                """
                Read every cell; copy each non-blank cell to `a[write]` and advance `write`. The answer is `a[0 .. write)`.
                """
            ],
            "build": ["`write = 0`.", "For each cell: if it isn't blank, `a[write] = cell`, `write += 1`.", "Return the first `write` cells."],
            "complexity": ["**Time O(n):** one read per cell, at most one write. **Space O(1)** besides the output."],
            "lines": {
                "init": "The write position starts at 0: nothing kept yet.",
                "read": "Visit every cell once, in order.",
                "keep": "A non-blank cell goes to the next free slot of the kept prefix. Blank cells are skipped by not writing them.",
                "ret": "The kept prefix. C reports its length through `returnSize`.",
            },
        },
    },
    "takeaways": [
        """
        - **Filter in place:** a reader visits everything, a writer collects what stays.
        - The writer never passes the reader, so overwriting is safe.
        - **Pitfall:** deleting with shifts (O(n²)).
        """
    ],
}


# ---------------------------------------------------------------- unique-stock-codes
codes = [3, 3, 5, 8, 8, 8, 11]
urows, a, w = [], list(codes), 1
urows.append((0, codes[0], "first code: always kept", 1, a[:1]))
for i in range(1, len(codes)):
    if a[i] != a[w - 1]:
        a[w] = a[i]
        w += 1
        urows.append((i, codes[i], f"differs from last kept {a[w - 2]}: keep", w, a[:w]))
    else:
        urows.append((i, codes[i], f"equals last kept {a[w - 1]}: repeat", w, a[:w]))
EXTRA["unique-stock-codes"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One code: unchanged.
        - All codes equal: one code remains.
        - The input is sorted, so equal codes are always next to each other.
        """
    ],
    "think": [
        SHIFT,
        READ_WRITE,
        """
        **What counts as a repeat?** Because the list is sorted, equal codes form one consecutive run. A code is a repeat
        exactly when it equals the **last code we kept**. (Comparing with the previous code in the input works too; the
        last kept code is the same value.)
        """,
        f"**Trace on `{codes}`:**",
        table(["read", "code", "decision", "write after", "kept part"], *urows),
    ],
    "approaches": {
        0: {
            "idea": ["Scan from the second code; when a code equals the one before it, shift the tail left over it and shrink the list."],
            "build": ["Scan from index 1.", "On a repeat, shift and shrink.", "Otherwise advance."],
            "complexity": ["**Time O(n²)** for long runs of repeats. **Space O(1)** besides the copy."],
            "limits": ["Every removed repeat shifts the whole tail. The write pointer places each kept code once."],
            "lines": {
                "init": "A working copy, its length, and the scan position (starting at the second code).",
                "scan": "Compare each code with its left neighbour in the shrinking list.",
                "shift": "A repeat: slide the tail left over it and shrink. The index stays to check the code that moved in.",
                "ret": "The first `n` codes.",
            },
        },
        1: {
            "idea": [
                """
                Keep `a[0]`. For each later code, copy it to `a[write]` if it differs from `a[write − 1]`, the last kept
                code. The answer is `a[0 .. write)`.

                **Why one comparison is enough.** The kept part is strictly increasing and the input is sorted, so a new
                code is either equal to the last kept code (a repeat) or larger than every kept code (new).
                """
            ],
            "build": ["`write = 1` (the first code is always kept).", "For each later code, keep it if it differs from the last kept one.", "Return the first `write` codes."],
            "complexity": ["**Time O(n).** **Space O(1)** besides the output."],
            "lines": {
                "init": "The first code is always kept, so the kept prefix starts with length 1.",
                "read": "Every later code, in order.",
                "keep": "A code different from the last kept one is new: write it to the next free slot.",
                "ret": "The kept prefix, one copy of each code in increasing order.",
            },
        },
    },
    "takeaways": [
        """
        - **De-duplicate a sorted array in place:** compare with the last kept value.
        - Sortedness turns "seen anywhere before" into "equal to the last kept".
        - **Pitfall:** comparing with `a[i − 1]` after it may have been overwritten; compare with the kept prefix instead.
        """
    ],
}


# ---------------------------------------------------------------- at-most-twice
vals = [1, 1, 1, 2, 2, 3, 3, 3, 3]
trows, a, w = [], list(vals), 0
for r, x in enumerate(vals):
    if w < 2 or a[w - 2] != x:
        why = "fewer than 2 kept" if w < 2 else f"a[write−2] = {a[w - 2]} ≠ {x}"
        a[w] = x
        w += 1
        trows.append((r, x, why + ": keep", w, a[:w]))
    else:
        trows.append((r, x, f"a[write−2] = {a[w - 2]} = {x}: third copy, skip", w, a[:w]))
EXTRA["at-most-twice"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Lists of length 1 or 2 are always fine.
        - Values appearing once or twice are kept in full.
        - Negative values are allowed; only equality matters.
        """
    ],
    "think": [
        READ_WRITE,
        """
        **When is a value one copy too many?** When the kept part already ends with two copies of it. Because the input
        is sorted and the kept part is too, checking just **the element two back**, `a[write − 2]`, is enough: if it
        equals `x`, then `a[write − 1]` (which lies between it and `x` in sorted order) equals `x` as well, so two copies
        are already kept.

        The same check generalises: to keep at most `k` copies, compare with `a[write − k]`.
        """,
        f"**Trace on `{vals}`:**",
        table(["read", "value", "decision", "write after", "kept part"], *trows),
    ],
    "approaches": {
        0: {
            "idea": ["Walk the runs of equal values; for each run, append `min(2, run length)` copies to a new list. Simple, but it builds a separate output."],
            "build": ["Find each run's end.", "Append up to two copies.", "Jump to the next run."],
            "complexity": ["**Time O(n).** **Space O(n)** for the new list."],
            "limits": ["The task asks for O(1) extra space. The look-back-two check does it in place."],
            "lines": {
                "init": "The output list and the start of the current run.",
                "run": "Advance `j` to the end of the run of equal values.",
                "take": "Append at most two copies of the run's value, then continue after the run.",
                "ret": "The trimmed list.",
            },
        },
        1: {
            "idea": [
                """
                Read every value; keep it if fewer than two values have been kept so far, or if `a[write − 2] ≠ x`.

                **Why it's correct.** If `a[write − 2] = x`, the last two kept values are both `x` (sorted order), so `x`
                would be a third copy. Otherwise at most one `x` is kept so far, and keeping this one is fine.
                """
            ],
            "build": ["`write = 0`.", "Keep `x` if `write < 2` or `a[write − 2] ≠ x`.", "Return the first `write` values."],
            "complexity": ["**Time O(n).** **Space O(1)** besides the output copy."],
            "lines": {
                "init": "A working copy and the write position.",
                "read": "Every value, in order.",
                "keep": "The first two values are always kept. After that, a value equal to the one two places back would be a third copy, so it's skipped.",
                "ret": "The kept prefix.",
            },
        },
    },
    "takeaways": [
        """
        - **At most k copies in a sorted array:** compare with `a[write − k]`.
        - The comparison is against the kept prefix, never the original positions.
        - **Pitfall:** comparing with `a[read − 2]`, which may already have been overwritten.
        """
    ],
}


# ---------------------------------------------------------------- compact-the-shelf
slots = [0, 5, 0, 0, 3, 9, 0, 2]
crows = rw_trace(slots, lambda a, w, x: x != 0, "empty: skip")
moved = crows[-1][4]
passes, b, changed = 0, list(slots), True
while changed:
    changed = False
    for i in range(len(b) - 1):
        if b[i] == 0 and b[i + 1] != 0:
            b[i], b[i + 1] = b[i + 1], b[i]
            changed = True
    passes += 1
EXTRA["compact-the-shelf"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No empty slots, or all empty: unchanged.
        - Negative values are items, not empties; only `0` is empty.
        - The items' order must be preserved (so sorting is not allowed).
        """
    ],
    "think": [
        READ_WRITE,
        f"""
        **Two phases.** First move every item to the front with the read/write pass; then everything from `write` to the
        end must be empty, so fill those slots with 0. For `{slots}`:
        """,
        table(["read", "value", "decision", "write after", "items placed"], *crows),
        f"""
        After the pass, `{len(moved)}` items sit at the front; filling slots `{len(moved)} … {len(slots) - 1}` with 0 gives
        **`{moved + [0] * (len(slots) - len(moved))}`**.

        **Why bubbling is slow.** Swapping each empty slot rightward one step at a time needs many passes: {passes}
        passes for this small shelf, and up to `n` passes of `n` steps in general.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Repeatedly sweep the shelf, swapping an empty slot with the item to its right, until a full sweep makes no swap. Each item drifts left one step per sweep."],
            "build": ["Repeat sweeps while something changed.", "Swap empty-then-item neighbours.", "Stop after a sweep with no swaps."],
            "complexity": ["**Time O(n²):** up to `n` sweeps of `n` steps. **Space O(1)** besides the copy."],
            "limits": ["Items move one step per sweep. The write pointer moves each item straight to its final slot in one pass."],
            "lines": {
                "init": "A working copy and a flag to keep sweeping.",
                "pass": "One left-to-right sweep over neighbouring pairs.",
                "swap": "An empty slot followed by an item: swap them so the item moves left.",
                "ret": "The compacted shelf.",
            },
        },
        1: {
            "idea": [
                """
                Copy each item to `a[write]` and advance `write`; then set every slot from `write` to the end to 0.

                **Why the order is kept.** Items are written in the order they're read, to positions `0, 1, 2, …`.
                """
            ],
            "build": ["Read/write pass over the items.", "Fill the rest with zeros."],
            "complexity": ["**Time O(n).** **Space O(1)** besides the output copy."],
            "lines": {
                "init": "A working copy and the next free slot at the front.",
                "move": "Each item goes to the next free slot; empty slots are skipped.",
                "fill": "Everything after the last item must be empty.",
                "ret": "The compacted shelf.",
            },
        },
    },
    "takeaways": [
        """
        - **Move items to one side, keeping order:** read/write pass, then fill the rest.
        - Each element moves at most once.
        - **Pitfall:** swapping in a way that reorders the items (e.g. with a pointer from the right).
        """
    ],
}


# ---------------------------------------------------------------- run-length-code
text = "aaabccddddx"
lrows, i = [], 0
while i < len(text):
    j = i
    while j < len(text) and text[j] == text[i]:
        j += 1
    lrows.append((i, j, text[i:j], j - i, text[i] + (str(j - i) if j - i > 1 else "")))
    i = j
EXTRA["run-length-code"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Runs of length 1 are written without a number.
        - Long runs need multi-digit counts (`a12`).
        - The whole text can be one run, or every character can be its own run.
        """
    ],
    "think": [
        """
        **Runs with two pointers.** `i` marks the start of a run. Move `j` right while `text[j]` equals `text[i]`; when
        it stops, the run is `text[i .. j)` with length `j − i`. Emit the character (and the length if it's more than 1),
        then start the next run at `j`.
        """,
        f"**Runs of `\"{text}\"`:**",
        table(["i", "j", "run", "length", "code"], *lrows),
        f"""
        Result **`{''.join(r[4] for r in lrows)}`**.

        **Building the output efficiently.** Appending to a string with `+` in a loop can copy the whole result every
        time, which is O(n²) overall in some languages. Collect pieces in a list (Python), a `StringBuilder` (Java), a
        `string` with `+=` (C++, which appends in place), or write into a preallocated buffer (C).
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Walk the runs with `i` and `j` as above, appending each run's code to an output builder.

                **Why each character is read once.** `j` moves forward through every character exactly once over the whole
                loop, and `i` jumps straight to `j`.
                """
            ],
            "build": ["Run start `i = 0`.", "Extend `j` to the end of the run.", "Emit the character, and the length if above 1.", "Continue from `j`."],
            "complexity": ["**Time O(n).** **Space O(n)** for the output (at most `n` characters)."],
            "lines": {
                "init": "An output builder and the start of the first run.",
                "run": "Move `j` until the character changes; `j − i` is the run's length.",
                "emit": "Write the character, plus its count only when the run is longer than 1.",
                "next": "The next run starts where this one ended.",
                "ret": "The compressed text.",
            },
        },
    },
    "takeaways": [
        """
        - **Runs of equal items:** a run-start pointer and a scanning pointer.
        - Build strings with a builder, not repeated concatenation.
        - **Pitfall:** writing single-digit counts only (`a12` needs two digits).
        """
    ],
}
