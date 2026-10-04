"""In-depth text for stack-simulation, structure-emulation and contribution-counting problems (merged via sol.EXTRA)."""
from collections import deque
from fractions import Fraction

from sol import EXTRA, table

COLLIDE = """
**Let new items collide with the top.** In these processes a new item only ever interacts with the **most recent
survivors**: the comet just to its left, the truck just ahead, the plate on top. A stack holds the survivors so far,
and each new item fights the top until it either wins (pop and continue) or stops. Every item is pushed and popped at
most once: O(n).
"""

AMORTISED = """
**Amortised cost.** Some operations occasionally do a lot of work (pouring a whole stack, rotating a whole queue). What
matters is the total over many operations: if each item can only be moved a constant number of times overall, the
average per operation is O(1), even if one particular call is slow.
"""

CONTRIB = """
**The contribution technique.** Instead of looping over all `n(n + 1)/2` stretches, ask for each element: **in how
many stretches is it the minimum (or maximum)?** If element `i` is the minimum of every stretch that starts in the
`L` positions from just after its previous smaller element up to `i`, and ends in the `R` positions from `i` up to
just before its next smaller element, then it is the minimum of exactly `L · R` stretches and contributes
`value · L · R`.

**Ties.** With equal values, a stretch could be credited to two elements. Make one side strict and the other not
(previous strictly smaller on the left, next smaller-**or-equal** on the right), so every stretch is credited to exactly
one of its minimums (here, the rightmost one).
"""

# ---------------------------------------------------------------- comet-collisions
comets = [5, 10, -5, 8, -12, 3, -3, -1]
st, crows = [], []
for c in comets:
    alive, events = True, []
    while alive and c < 0 and st and st[-1] > 0:
        if st[-1] < -c:
            events.append(f"{st.pop()} breaks")
        elif st[-1] == -c:
            events.append(f"{st.pop()} and {c} both break")
            alive = False
        else:
            events.append(f"{c} breaks against {st[-1]}")
            alive = False
    if alive:
        st.append(c)
    crows.append((c, "; ".join(events) or ("moves right: no collision yet" if c > 0 else "nothing to its left flies right"), list(st)))
EXTRA["comet-collisions"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Only a right-mover followed by a left-mover can collide.
        - Equal sizes destroy each other.
        - A big left-mover can destroy several right-movers in a row.
        """
    ],
    "think": [
        COLLIDE,
        f"""
        **Who meets whom.** A comet moving left meets the comets to its left that move right, starting with the nearest.
        Comets moving the same way, or a left-mover with only left-movers before it, never meet. So scan left to right
        with a stack of survivors; a left-mover fights the stack's top while the top moves right. For `{comets}`:
        """,
        table(["comet", "collisions", "survivors after"], *crows),
        f"Survivors: **{st}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Find the first adjacent pair moving toward each other (right-mover then left-mover), resolve it, and restart the scan; stop when no such pair remains."],
            "build": ["Copy.", "Find the first colliding pair.", "Remove the loser(s).", "Restart."],
            "complexity": ["**Time O(n²)** (each collision restarts the scan and deletes from the middle). **Space O(n).**"],
            "limits": ["Restarts after every collision. A stack resolves each new comet against the survivors directly."],
        },
        1: {
            "idea": [
                """
                Stack of survivors. For each comet: while it moves left, is still alive, and the top moves right, compare
                sizes: a smaller top breaks (pop and continue), an equal top breaks with it, a bigger top destroys it. If
                it survives, push it.

                **Invariant.** The stack never contains a right-mover followed by a left-mover, so it's always a stable
                set of survivors.
                """
            ],
            "build": ["Empty stack.", "Fight the top while a collision is possible.", "Push the comet if it survives."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Collisions:** stack of survivors; only right-then-left pairs fight.
        - Handle the three outcomes: smaller, equal, bigger.
        - **Pitfall:** letting right-movers fight left-movers that are to their left (they fly apart).
        """
    ],
}


# ---------------------------------------------------------------- convoys-to-the-depot
depot, pos, spd = 12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]
trucks = sorted(zip(pos, spd), reverse=True)
vrows, count, lead = [], 0, None
for p, s in trucks:
    t = Fraction(depot - p, s)
    if lead is None or t > lead:
        count += 1
        lead = t
        vrows.append((p, s, str(t), "slower than the convoy ahead: leads a new convoy", count))
    else:
        vrows.append((p, s, str(t), f"would arrive by {lead}: catches up and joins the convoy ahead", count))
EXTRA["convoys-to-the-depot"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Catching up exactly at the depot still joins the convoy.
        - A truck already ahead and slower slows everyone behind it.
        - Arrival times are fractions; compare `dist₁ · speed₂` with `dist₂ · speed₁` to stay exact.
        """
    ],
    "think": [
        COLLIDE,
        f"""
        **Process trucks from the one nearest the depot.** A truck can only be held up by trucks ahead of it. Going from
        the front of the road backwards, keep the arrival time of the convoy just ahead. A truck that would arrive **no
        later** (on its own) catches up and joins that convoy; a truck that would arrive later is slower than everything
        ahead, so it leads a new convoy. Depot at {depot}:
        """,
        table(["position", "speed", "arrival alone (hours)", "decision", "convoys"], *vrows),
        f"Convoys: **{count}**.",
    ],
    "approaches": {
        0: {
            "idea": ["A truck leads its own convoy exactly when no truck ahead of it would arrive at the same time or later. Check that for every truck against every truck ahead."],
            "build": ["For each truck, compare with every truck ahead.", "Count trucks that no truck ahead holds up."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Compares every pair. After sorting by position, only the convoy just ahead matters."],
        },
        1: {
            "idea": [
                """
                Sort trucks by position, nearest to the depot first. Keep the lead convoy's `(distance, speed)`. A truck
                starts a new convoy when its arrival time is strictly later, compared exactly as
                `dist · lead_speed > lead_dist · speed`.
                """
            ],
            "build": ["Sort by position, descending.", "Carry the latest convoy arrival time.", "Count trucks that arrive strictly later."],
            "complexity": ["**Time O(n log n)** for the sort. **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Car fleets:** sort by position from the front; a slower-arriving truck starts a new fleet.
        - Compare fractions by cross-multiplication.
        - **Pitfall:** floating-point arrival times with exact ties.
        """
    ],
}


# ---------------------------------------------------------------- plate-stack-check
washed, served = [3, 1, 4, 2, 5], [1, 4, 2, 5, 3]
bad = [4, 3, 5, 1, 2]


def replay(w, s):
    st, j, rows = [], 0, []
    for plate in w:
        st.append(plate)
        out = []
        while st and st[-1] == s[j]:
            out.append(st.pop())
            j += 1
        rows.append((plate, out or "—", list(st)))
    return rows, j == len(s)


r1, ok1 = replay(washed, served)
r2, ok2 = replay(washed, bad)
EXTRA["plate-stack-check"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Plates can be served immediately after washing, or wait at any depth.
        - Numbers are distinct, so each serve matches exactly one plate.
        - Served order equal to washed order is always possible.
        """
    ],
    "think": [
        COLLIDE,
        f"""
        **Replay greedily.** Wash plates in order; after each wash, serve from the top as long as the top is the next
        plate to be served. Serving as early as possible never hurts: a plate that's on top and due now can only block
        others if it stays. If all plates get served, the order was possible. Washed `{washed}`, served `{served}`:
        """,
        table(["washed", "served now", "stack after"], *r1),
        f"All served: **{str(ok1).lower()}**. With served `{bad}`:",
        table(["washed", "served now", "stack after"], *r2),
        f"Stuck with plates left on the stack: **{str(ok2).lower()}**.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Use the rule that characterises stack orders: after serving plate `p`, any plates washed **before** `p`
                and served later must come out in reverse washing order. Check it for every plate with a scan of the rest.
                """
            ],
            "build": ["Washing position of every served plate.", "For each plate, scan later serves.", "Plates washed earlier must appear in decreasing washing order."],
            "complexity": ["**Time O(n²)** (plus O(n²) for the `index` lookups). **Space O(n).**"],
            "limits": ["Quadratic. Simply replaying with a stack checks the same rule in one pass."],
        },
        1: {
            "idea": ["Push each washed plate, then pop while the top is the next plate to serve. Possible exactly when every plate was served."],
            "build": ["Empty stack and a pointer into `served`.", "Push, then pop matching tops.", "Check the pointer reached the end."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Validate a stack sequence:** replay it, popping greedily whenever the top matches.
        - Greedy is safe because waiting can only block later plates.
        - **Pitfall:** checking only that each served plate was washed before it's served.
        """
    ],
}


# ---------------------------------------------------------------- queue-from-two-stacks
ops = [("push", 1), ("push", 2), ("push", 3), ("pop", None), ("push", 4), ("peek", None), ("pop", None), ("pop", None), ("pop", None)]
inbox, outbox, qrows = [], [], []
for op, x in ops:
    note = ""
    if op == "push":
        inbox.append(x)
        res = "—"
    else:
        if not outbox:
            moved = len(inbox)
            while inbox:
                outbox.append(inbox.pop())
            note = f"outbox empty: pour {moved} item(s) over (order reverses)"
        res = outbox.pop() if op == "pop" else outbox[-1]
    qrows.append((f"{op}({x})" if x is not None else f"{op}()", res, note or "—", list(inbox), list(outbox)))
EXTRA["queue-from-two-stacks"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Pushes and pops interleave: new pushes must not jump ahead of older items.
        - `peek` must not remove anything.
        - `pop`/`peek` are only called on a non-empty queue.
        """
    ],
    "think": [
        AMORTISED,
        """
        **Reversing a stack makes it a queue.** Pushing 1, 2, 3 onto a stack leaves 3 on top, but the queue's front is 1.
        Popping everything onto a second stack reverses the order, putting 1 on top.

        **Inbox and outbox.** New items go into the inbox. Reads come from the outbox. Pour the inbox into the outbox
        **only when the outbox is empty**: then the outbox holds the oldest items in the right order, and everything in
        the inbox is newer, so it can wait.
        """,
        table(["operation", "returns", "pour?", "inbox (bottom→top)", "outbox (bottom→top)"], *qrows),
    ],
    "approaches": {
        0: {
            "idea": ["Keep everything in one stack. For every pop or peek, pour all items into the spare stack to reach the oldest, read it, then pour everything back."],
            "build": ["Main stack for all items.", "Pour over, read the front, pour back."],
            "complexity": ["**Time O(n)** for every pop or peek. **Space O(n).**"],
            "limits": ["Pours everything back after every read. Leaving items in the reversed stack until it's empty makes reads O(1) amortised."],
        },
        1: {
            "idea": [
                """
                `push` → inbox. `pop`/`peek` → if the outbox is empty, pour the whole inbox into it; then use the outbox's
                top. `empty` checks both stacks.

                **Why amortised O(1).** Each item is pushed onto the inbox once, moved to the outbox once, and popped once:
                three stack operations per item over its lifetime.
                """
            ],
            "build": ["Two stacks.", "Push to the inbox.", "Pour only when the outbox is empty.", "Read from the outbox."],
            "complexity": ["**Time O(1)** amortised per operation (one pour can be O(n)). **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Queue from two stacks:** inbox + outbox, pour only when the outbox is empty.
        - Amortised analysis: count how many times each item can move.
        - **Pitfall:** pouring while the outbox still has items (breaks the order).
        """
    ],
}


# ---------------------------------------------------------------- stack-from-a-queue
q, srows = deque(), []
for op, x in [("push", 1), ("push", 2), ("push", 3), ("top", None), ("pop", None), ("push", 4), ("pop", None)]:
    if op == "push":
        q.append(x)
        for _ in range(len(q) - 1):
            q.append(q.popleft())
        srows.append((f"push({x})", "—", f"add to back, rotate {len(q) - 1} time(s)", list(q)))
    elif op == "pop":
        v = q.popleft()
        srows.append(("pop()", v, "front is the top", list(q)))
    else:
        srows.append(("top()", q[0], "front is the top", list(q)))
EXTRA["stack-from-a-queue"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Only queue operations are allowed: add to the back, read/remove the front.
        - Interleaved pushes and pops.
        - `pop`/`top` only on a non-empty stack.
        """
    ],
    "think": [
        AMORTISED,
        """
        **Rotation.** Removing the front and adding it to the back keeps the cyclic order of a queue. So after adding a
        new item at the back, rotating `size − 1` times brings it to the front, while everything else keeps its order
        behind it. If every push does that, the front is always the newest item: the stack's top.
        """,
        table(["operation", "returns", "what happens", "queue (front→back)"], *srows),
    ],
    "approaches": {
        0: {
            "idea": ["Push to the back. For `pop`/`top`, rotate `size − 1` times so the newest item reaches the front, read it (and for `top`, put it back at the end)."],
            "build": ["Push to the back.", "Rotate the newest to the front on reads.", "Read it."],
            "complexity": ["**Time O(1)** push, **O(n)** pop and top. **Space O(n).**"],
            "limits": ["Every read rotates the whole queue. Rotating once per push keeps the queue in stack order, so reads are O(1)."],
        },
        1: {
            "idea": [
                """
                On `push`, add the item to the back and rotate `size − 1` times so it's at the front. Then `pop` and `top`
                read the front.

                **Invariant.** The queue, front to back, lists the items from newest to oldest.
                """
            ],
            "build": ["One queue.", "Push: add, then rotate the rest behind it.", "Pop/top: the front."],
            "complexity": ["**Time O(n)** push, **O(1)** pop and top. **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Stack from a queue:** rotate after each push so the newest item is at the front.
        - Choose which operation pays: here pushes are O(n), reads O(1).
        - **Pitfall:** rotating `size` times (the new item ends up at the back again).
        """
    ],
}


# ---------------------------------------------------------------- ring-buffer
k = 3
buf, head, size, rrows = [None] * k, 0, 0, []
for op, x in [("enqueue", 1), ("enqueue", 2), ("enqueue", 3), ("enqueue", 9), ("dequeue", None), ("enqueue", 4), ("front", None), ("rear", None)]:
    if op == "enqueue":
        if size == k:
            res = "false (full)"
        else:
            buf[(head + size) % k] = x
            size += 1
            res = "true"
    elif op == "dequeue":
        if size == 0:
            res = "false"
        else:
            head = (head + 1) % k
            size -= 1
            res = "true"
    elif op == "front":
        res = buf[head] if size else -1
    else:
        res = buf[(head + size - 1) % k] if size else -1
    rrows.append((f"{op}({x})" if x is not None else f"{op}()", res, list(buf), head, size))
EXTRA["ring-buffer"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Enqueue on a full buffer fails and changes nothing; dequeue on an empty one fails.
        - `front`/`rear` return −1 when empty.
        - Capacity 1: front and rear are the same slot.
        """
    ],
    "think": [
        """
        **Wrap around instead of shifting.** A plain list that removes from the front shifts every item: O(n) per
        dequeue. A fixed array of size `k` with a `head` index and a `size` avoids that: the front is `buf[head]`, the
        next free slot is `(head + size) mod k`, and dequeuing just moves `head` forward. When an index passes the end,
        `mod k` wraps it to the start, so the array behaves like a ring.

        **Why store `size` rather than a tail index.** With only `head` and `tail`, an empty buffer and a full one look
        the same (`head == tail`); the size tells them apart.
        """,
        table(["operation", "returns", "array", "head", "size"], *rrows),
    ],
    "approaches": {
        0: {
            "idea": ["Use a list: append to enqueue, remove index 0 to dequeue, and check the length against `k`."],
            "build": ["List and capacity.", "Append / pop(0).", "Length checks for full and empty."],
            "complexity": ["**Time O(n)** per dequeue (shifting). **Space O(k).**"],
            "limits": ["Removing from the front shifts every item. A ring buffer moves an index instead."],
        },
        1: {
            "idea": ["Fixed array of size `k`, `head` and `size`. Enqueue writes at `(head + size) mod k`; dequeue advances `head`; rear is at `(head + size − 1) mod k`."],
            "build": ["Array, head, size.", "Index arithmetic with `mod k`.", "Full/empty from `size`."],
            "complexity": ["**Time O(1)** per operation. **Space O(k).**"],
        },
    },
    "takeaways": [
        """
        - **Circular queue:** fixed array, `head` and `size`, indices taken `mod k`.
        - Track the size to tell full from empty.
        - **Pitfall:** computing the rear as `head + size` (one past the last item).
        """
    ],
}


# ---------------------------------------------------------------- sum-of-stretch-lows
pr = [3, 1, 2, 4, 2]
n = len(pr)
L = [i - next((j for j in range(i - 1, -1, -1) if pr[j] < pr[i]), -1) for i in range(n)]
R = [next((j for j in range(i + 1, n) if pr[j] <= pr[i]), n) - i for i in range(n)]
lows = sum(pr[i] * L[i] * R[i] for i in range(n))
brute_lows = sum(min(pr[i:j + 1]) for i in range(n) for j in range(i, n))
EXTRA["sum-of-stretch-lows"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Equal prices: each stretch must be counted for exactly one of its minimums.
        - One day: the answer is that price.
        - Return the sum modulo 10⁹ + 7.
        """
    ],
    "think": [
        CONTRIB,
        f"**For `{pr}`** (L = choices of start, R = choices of end, for stretches where this day is the low):",
        table(["day", "price", "L", "R", "stretches", "contribution"], *[(i, pr[i], L[i], R[i], L[i] * R[i], pr[i] * L[i] * R[i]) for i in range(n)]),
        f"Sum of contributions **{lows}** (adding up the low of every stretch directly gives {brute_lows}).",
    ],
    "approaches": {
        0: {
            "idea": ["For every start, extend with a running minimum and add it for every end."],
            "build": ["Every start.", "Running low while extending.", "Add each low."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Quadratic. Each day's total contribution can be computed from its two boundaries."],
        },
        1: {
            "idea": ["For each day, walk left over prices `≥` it and right over prices `>` it to find `L` and `R`, then add `price · L · R`."],
            "build": ["For each day, walk to both boundaries.", "Add `price · L · R`."],
            "complexity": ["**Time O(n²)** in the worst case (long walks). **Space O(1).**"],
            "limits": ["The walks overlap; monotonic stacks find every boundary in one pass per side."],
        },
        2: {
            "idea": [
                """
                Left pass: stack popping prices `≥` the current one; `L = i − (previous strictly smaller index)`. Right pass:
                stack popping prices `>` the current one; `R = (next smaller-or-equal index) − i`. Sum `price · L · R`
                modulo 10⁹ + 7.
                """
            ],
            "build": ["Left boundaries with a stack.", "Right boundaries with a stack.", "Sum contributions."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Sum of subarray minimums:** contribution `value · L · R` from previous/next smaller elements.
        - One strict side and one non-strict side for ties.
        - **Pitfall:** both sides strict (stretches with equal minimums counted twice).
        """
    ],
}


# ---------------------------------------------------------------- total-swing
rd = [4, 1, 4, 2]
m = len(rd)
Lh = [i - next((j for j in range(i - 1, -1, -1) if rd[j] > rd[i]), -1) for i in range(m)]
Rh = [next((j for j in range(i + 1, m) if rd[j] >= rd[i]), m) - i for i in range(m)]
Ll = [i - next((j for j in range(i - 1, -1, -1) if rd[j] < rd[i]), -1) for i in range(m)]
Rl = [next((j for j in range(i + 1, m) if rd[j] <= rd[i]), m) - i for i in range(m)]
highs = sum(rd[i] * Lh[i] * Rh[i] for i in range(m))
lows2 = sum(rd[i] * Ll[i] * Rl[i] for i in range(m))
brute_swing = sum(max(rd[i:j + 1]) - min(rd[i:j + 1]) for i in range(m) for j in range(i, m))
EXTRA["total-swing"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Single readings have swing 0.
        - Negative readings are fine; only differences matter.
        - The total can reach about `n²/2 · 2 × 10⁶ ≈ 10¹⁶`: use 64 bits.
        """
    ],
    "think": [
        CONTRIB,
        f"""
        **Split the swing.** `Σ (high − low) = Σ high − Σ low` over all stretches. Each sum is a contribution count: the
        sum of maxima uses previous/next **larger** elements, the sum of minima uses previous/next **smaller** ones. For
        `{rd}`:
        """,
        table(["i", "reading", "times it's the high", "times it's the low"], *[(i, rd[i], Lh[i] * Rh[i], Ll[i] * Rl[i]) for i in range(m)]),
        f"Sum of highs {highs} − sum of lows {lows2} = **{highs - lows2}** (direct check: {brute_swing}).",
    ],
    "approaches": {
        0: {
            "idea": ["For every start, extend with a running maximum and minimum, adding their difference for every end."],
            "build": ["Every start.", "Running high and low.", "Add each swing."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Quadratic. Splitting into highs and lows lets each element's contribution be counted directly."],
        },
        1: {
            "idea": [
                """
                `sum_of_highs(a)` computes Σ max over all stretches with two monotonic-stack passes (one side strict).
                The sum of lows is `−sum_of_highs(−a)`, so the answer is `sum_of_highs(a) + sum_of_highs(−a)`.
                """
            ],
            "build": ["Contribution sum of maxima.", "Reuse it on the negated readings for the minima.", "Add (64-bit)."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Sum of (max − min) over subarrays = Σ max − Σ min**, each by contribution.
        - Negating the array turns maxima into minima, so one routine serves both.
        - **Pitfall:** 32-bit totals.
        """
    ],
}
