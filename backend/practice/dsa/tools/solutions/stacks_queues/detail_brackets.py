"""In-depth text for the bracket-matching problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

STACK = """
**Why a stack.** In a well-formed bracket string, the bracket opened most recently must be closed first: brackets
nest, they never cross. "Most recent first" is exactly last-in, first-out, so keep the open brackets on a stack: push
on an opener, and on a closer check (and pop) the top. With a single kind of bracket the stack only ever holds `(`,
so a **counter** of open brackets can replace it.
"""

# ---------------------------------------------------------------- sealed-brackets
s1 = "{[()]}([)]"
pair = {")": "(", "]": "[", "}": "{"}
st, rows1, ok = [], [], True
for i, c in enumerate(s1):
    if c in pair:
        if not st or st[-1] != pair[c]:
            rows1.append((i, c, "".join(st) or "—", f"top is {st[-1] if st else 'nothing'}, needs {pair[c]}: not sealed"))
            ok = False
            break
        st.pop()
        rows1.append((i, c, "".join(st) or "—", f"closes {pair[c]}"))
    else:
        st.append(c)
        rows1.append((i, c, "".join(st), "push"))
EXTRA["sealed-brackets"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A closer when nothing is open: not sealed.
        - Openers left over at the end: not sealed.
        - Crossing pairs like `([)]`: the right counts but the wrong order, not sealed.
        """
    ],
    "think": [
        STACK,
        f"**Trace on `{s1}`:**",
        table(["i", "char", "stack after", "action"], *rows1),
        f"Answer: **{str(ok and not st).lower()}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Repeatedly delete adjacent matching pairs `()`, `[]`, `{}` until nothing changes; the string is sealed exactly when it becomes empty."],
            "build": ["Delete matching pairs.", "Repeat until stable.", "Sealed if empty."],
            "complexity": ["**Time O(n²):** up to `n/2` rounds, each rebuilding the string. **Space O(n).**"],
            "limits": ["Each round rescans everything. A stack resolves every pair the moment its closer arrives."],
        },
        1: {
            "idea": [
                """
                Push openers. On a closer, the stack top must be its partner: pop it, or fail. At the end the stack must be
                empty.

                **Invariant.** The stack holds the brackets opened but not yet closed, most recent on top. A closer can
                only legally close the top one.
                """
            ],
            "build": ["Map each closer to its opener.", "Push openers.", "On a closer, check and pop the top.", "Sealed if the stack ends empty."],
            "complexity": ["**Time O(n).** **Space O(n)** for the stack."],
        },
    },
    "takeaways": [
        """
        - **Matching nested pairs:** stack of openers; a closer must match the top.
        - Check both failure modes: a closer with an empty stack, and leftovers at the end.
        - **Pitfall:** counting each kind separately (accepts crossings like `([)]`).
        """
    ],
}


# ---------------------------------------------------------------- patch-the-brackets
s2 = "())(()(("
o, added, rows2 = 0, 0, []
for i, c in enumerate(s2):
    if c == "(":
        o += 1
        act = "open one more"
    elif o:
        o -= 1
        act = "closes an open one"
    else:
        added += 1
        act = "nothing open: needs an inserted '('"
    rows2.append((i, c, o, added, act))
EXTRA["patch-the-brackets"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Already balanced: insert nothing.
        - Only `)`: each needs a `(` inserted before it.
        - Only `(`: each needs a `)` inserted after it.
        """
    ],
    "think": [
        STACK,
        f"""
        **Which brackets can't be matched?** Scan left to right with a counter of open `(`. A `)` with nothing open is
        stray: it needs one `(` inserted before it. Any `(` still open at the end needs one `)`. Each stray bracket needs
        its own partner (one inserted bracket can't serve two of them), and the matched ones need nothing, so the answer
        is the number of stray brackets. For `{s2}`:
        """,
        table(["i", "char", "open after", "inserted so far", "action"], *rows2),
        f"Stray `)`: {added}; still open at the end: {o}. Total **{added + o}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Repeatedly delete `()` pairs; whatever remains can't be matched, and each leftover bracket needs one insertion."],
            "build": ["Delete `()` pairs until none remain.", "Return the leftover length."],
            "complexity": ["**Time O(n²).** **Space O(n).**"],
            "limits": ["Repeated deletions rescan the string; a counter finds the same leftovers in one pass."],
        },
        1: {
            "idea": [
                """
                `open` counts unmatched `(` so far; `added` counts `)` that arrived with nothing open. The answer is
                `added + open`.
                """
            ],
            "build": ["Two counters.", "`(` → open + 1; `)` → close one if possible, else count an insertion.", "Add the leftover opens."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Minimum insertions to balance:** count stray `)` plus leftover `(`.
        - One kind of bracket → a counter replaces the stack.
        - **Pitfall:** letting the counter go negative instead of counting a stray `)`.
        """
    ],
}


# ---------------------------------------------------------------- strip-stray-brackets
s3 = "a)b(c(d)e)f)(g"
stack, drop = [], set()
for i, c in enumerate(s3):
    if c == "(":
        stack.append(i)
    elif c == ")":
        if stack:
            stack.pop()
        else:
            drop.add(i)
drop.update(stack)
clean = "".join(c for i, c in enumerate(s3) if i not in drop)
EXTRA["strip-stray-brackets"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Letters are never removed.
        - Several minimal answers can exist; any one is accepted.
        - Strays can be `)` with nothing open or `(` never closed.
        """
    ],
    "think": [
        STACK,
        f"""
        **Which brackets are stray?** Scanning left to right, a `)` with nothing open can never be matched. After the
        scan, every `(` still open can never be matched either. Removing exactly those brackets leaves a balanced string,
        and no smaller removal works, because each of them is unmatched no matter what else is removed.

        For `{s3}` the stray positions are {sorted(drop)}:
        """,
        table(["position"] + list(range(len(s3))), ["char"] + list(s3), ["stray?"] + ["✗" if i in drop else "" for i in range(len(s3))]),
        f"Cleaned: **`{clean}`**.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Scan with a stack of `(` positions: pop on a matched `)`, mark an unmatched `)` for removal. At the end,
                mark every position left on the stack. Build the string without the marked positions.
                """
            ],
            "build": ["Stack of `(` positions.", "Mark unmatched `)`.", "Mark leftover `(`.", "Build the result."],
            "complexity": ["**Time O(n).** **Space O(n)** for the stack and marks."],
            "limits": ["Stores positions; two counting passes do the same with only counters (plus the output)."],
        },
        1: {
            "idea": [
                """
                Pass 1 (left to right): drop any `)` that arrives with no open `(`. Pass 2 (right to left over the result):
                drop any `(` that arrives with no `)` to its right. What's left is balanced.

                **Why two directions.** Stray `)` are detected reading forwards (nothing open yet); stray `(` are detected
                reading backwards (nothing to close them).
                """
            ],
            "build": ["Forward pass removing stray `)`.", "Backward pass removing stray `(`.", "Reverse back."],
            "complexity": ["**Time O(n).** **Space O(n)** for the output."],
        },
    },
    "takeaways": [
        """
        - **Minimum removals to balance:** remove unmatched `)` (forward) and unmatched `(` (backward or leftover stack).
        - A stack of positions tells you exactly which brackets to drop.
        - **Pitfall:** removing letters, or removing a matched bracket.
        """
    ],
}


# ---------------------------------------------------------------- longest-balanced-stretch
s4 = ")(()())(()"
stack4, best4, rows4 = [-1], 0, []
for i, c in enumerate(s4):
    if c == "(":
        stack4.append(i)
        act = "push position"
    else:
        stack4.pop()
        if not stack4:
            stack4.append(i)
            act = "unmatched: becomes the new wall"
        else:
            best4 = max(best4, i - stack4[-1])
            act = f"matched: stretch length {i} − {stack4[-1]} = {i - stack4[-1]}"
    rows4.append((i, c, stack4[:], best4, act))
EXTRA["longest-balanced-stretch"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No balanced stretch at all: 0.
        - Several balanced pieces next to each other form one longer stretch (`()()`).
        - An unmatched bracket splits the string into independent parts.
        """
    ],
    "think": [
        STACK,
        f"""
        **Walls.** An unmatched `)` or `(` can never be inside a balanced stretch, so the answer is the longest piece
        between those unmatched brackets. Keep a stack of **positions**, with a "wall" at the bottom: start with `−1`
        (before the string). Push each `(`'s position. On `)`, pop; if the stack becomes empty, this `)` is unmatched and
        becomes the new wall; otherwise the current balanced stretch runs from just after the new top to here.
        For `{s4}`:
        """,
        table(["i", "char", "stack (positions)", "best", "action"], *rows4),
        f"""
        Longest: **{best4}**.

        **The two-pass counter alternative.** Scan left to right counting `(` and `)`; equal counts mark a balanced
        stretch, and more `)` than `(` means a wall, so reset. This misses stretches where `(` stays ahead (like `(()`),
        so scan right to left too with the roles swapped. Every balanced stretch is caught by one of the two passes.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["From every start, extend with a depth counter; stop when it goes negative; record lengths where it returns to 0."],
            "build": ["Every start.", "Depth counter while extending.", "Record balanced lengths."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Restarts at every position. Walls (unmatched brackets) split the string so one pass suffices."],
        },
        1: {
            "idea": ["Stack of positions with a wall at the bottom (initially −1). Push `(`; on `)` pop, then either reset the wall (empty stack) or measure `i − top`."],
            "build": ["Stack `[-1]`.", "Push `(` positions.", "On `)`, pop; empty → new wall; else measure."],
            "complexity": ["**Time O(n).** **Space O(n)** for the stack."],
            "limits": ["O(n) stack memory; two counter passes need O(1)."],
        },
        2: {
            "idea": [
                """
                Forward pass with counters `opened`, `closed`: equal → record `2 · closed`; `closed > opened` → reset both.
                Backward pass the same way with the roles of `(` and `)` swapped (reset when `opened > closed`).

                **Why both passes.** The forward pass never resets while `(` is ahead, so a stretch inside an unfinished
                `((…` region is missed; reading backwards, those extra `(` are the ones that trigger resets, and the
                stretch is found.
                """
            ],
            "build": ["Forward counting pass.", "Backward counting pass.", "Return the best length seen."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Longest valid bracket substring:** stack of positions with a wall, or two counter passes.
        - Unmatched brackets act as walls that split the problem.
        - **Pitfall:** forgetting the initial wall `−1` (off-by-one for stretches starting at 0).
        """
    ],
}


# ---------------------------------------------------------------- nested-box-value
s5 = "(()(()))()"
depth, total, rows5 = 0, 0, []
for i, c in enumerate(s5):
    if c == "(":
        depth += 1
    else:
        depth -= 1
        if s5[i - 1] == "(":
            total += 2 ** depth
            rows5.append((i - 1, i, depth, 2 ** depth, total))
EXTRA["nested-box-value"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The answer is taken modulo 10⁹ + 7: deep nesting doubles many times.
        - Only `()` pairs contribute directly; outer boxes multiply.
        - The string is guaranteed balanced.
        """
    ],
    "think": [
        STACK,
        """
        **Expanding the rules.** `(A)` doubles `A`, and side-by-side boxes add. Expanding fully, every innermost empty box
        `()` contributes `1`, doubled once for every box around it. So the value is

        `Σ 2^(depth of each "()" pair)`,

        where depth counts the boxes enclosing that pair.
        """,
        f"**Every `()` pair in `{s5}`:**",
        table(["opens at", "closes at", "boxes around it", "contribution 2^depth", "running total"], *rows5),
        f"Value **{total}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Evaluate recursively: split the string into top-level boxes; an empty box is 1, a box around contents is 2 × the contents' value; add them up."],
            "build": ["Find top-level boxes by tracking depth.", "Recurse into each box's contents.", "Add the values."],
            "complexity": ["**Time O(n²)** in the worst case (deep nesting rescans the same characters). **Space O(n)** recursion."],
            "limits": ["Nested boxes are scanned once per level, and deep nesting risks the recursion limit. A stack evaluates in one pass."],
        },
        1: {
            "idea": [
                """
                A stack of partial sums, one per open box (plus one for the top level). `(` pushes 0. `)` pops the box's
                contents `t` and adds `1` (if the box was empty) or `2t` to the enclosing level.
                """
            ],
            "build": ["Stack `[0]`.", "`(` pushes 0.", "`)` pops `t`, adds `1` or `2t` to the new top."],
            "complexity": ["**Time O(n).** **Space O(n)** for the stack."],
            "limits": ["O(n) stack; the depth formula needs only a counter."],
        },
        2: {
            "idea": [
                """
                Track the current depth. At each `()` pair (a `)` right after a `(`), add `2^(depth after closing)`.
                Precompute powers of 2 modulo 10⁹ + 7.
                """
            ],
            "build": ["Powers of 2 mod 10⁹ + 7.", "Track depth.", "Add `2^depth` at each `()`."],
            "complexity": ["**Time O(n).** **Space O(n)** for the powers (O(1) if doubled on the fly)."],
        },
    },
    "takeaways": [
        """
        - **Nested scoring:** expand the rules into a sum over innermost pairs, each weighted by its depth.
        - A stack of partial results evaluates any nested grammar in one pass.
        - **Pitfall:** forgetting the modulus when doubling.
        """
    ],
}
