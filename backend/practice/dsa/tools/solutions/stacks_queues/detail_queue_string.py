"""In-depth text for queue-simulation and string-building-with-a-stack problems (merged via sol.EXTRA)."""
from collections import deque

from sol import EXTRA, table

SIMULATE = """
**Simulate, then look for a shortcut.** Queue problems describe a process step by step. A direct simulation with a
queue is always a correct first answer. Then ask what the process *really* depends on: often the exact order doesn't
matter (only counts do), or each element's fate can be computed directly, which removes the step-by-step loop.
"""

BUILD = """
**Building text with a stack.** When later characters can undo or combine with the most recent ones (a backspace, a
run of equal tiles, a `..` in a path, a closing bracket), the most recent output is exactly what's affected next. A
stack of output pieces handles that: push to append, pop to undo, and modify the top to combine.
"""

# ---------------------------------------------------------------- ticket-line
wants, k = [2, 5, 3, 1, 4], 2
need = wants[k]
trows = [(i, w, "at or before k" if i <= k else "after k", need if i <= k else need - 1, min(w, need if i <= k else need - 1)) for i, w in enumerate(wants)]
EXTRA["ticket-line"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Person `k` may be first in line, or last.
        - People wanting fewer tickets than person `k` leave early and stop taking seconds.
        - The answer can reach `10⁵ × 10⁵ = 10¹⁰`: use 64 bits.
        """
    ],
    "think": [
        SIMULATE,
        f"""
        **Count purchases instead of seconds.** Every second exactly one ticket is bought, so the answer is the total
        number of tickets bought by everyone until person `k` finishes. Person `k` needs `{need}` rounds. In those rounds:

        - a person **at or before** `k` buys at most `{need}` tickets (one per round, including the last round);
        - a person **after** `k` buys at most `{need} − 1` (in the final round, person `k` finishes before they're served).

        Each person buys the smaller of what they want and that cap. For `{wants}`, `k = {k}`:
        """,
        table(["person", "wants", "position", "cap", "tickets bought"], *trows),
        f"Total: **{sum(r[4] for r in trows)}** seconds.",
    ],
    "approaches": {
        0: {
            "idea": ["Simulate the line with a queue of `(tickets left, person)`: serve the front, re-queue them if they still want more, and stop when person `k` buys their last ticket."],
            "build": ["Queue of (wants, index).", "Serve one ticket per second.", "Re-queue or stop."],
            "complexity": ["**Time O(total tickets)**, up to 10¹⁰ seconds. **Space O(n).**"],
            "limits": ["Steps through every second. Each person's purchases can be computed directly from their position and wants."],
        },
        1: {
            "idea": ["For each person, add `min(wants[i], need)` if `i ≤ k`, else `min(wants[i], need − 1)`."],
            "build": ["`need = wants[k]`.", "Cap each person by their position.", "Sum (64-bit)."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Round-robin queues:** count per person instead of simulating each step.
        - People after the target get one fewer round.
        - **Pitfall:** giving people after `k` the same cap as those before.
        """
    ],
}


# ---------------------------------------------------------------- lunch-line
prefers, trays = [1, 1, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1]
want = [prefers.count(0), prefers.count(1)]
lrows = []
for t in trays:
    if want[t] == 0:
        lrows.append((t, f"{want[0]} want 0, {want[1]} want 1", "nobody left wants it: lunch stops"))
        break
    want[t] -= 1
    lrows.append((t, f"{want[0]} want 0, {want[1]} want 1", "someone who wants it will reach the front"))
EXTRA["lunch-line"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Everyone may eat (answer 0).
        - The process stops as soon as nobody in line wants the top tray, even if later trays would suit them.
        - Students who don't want the top tray just rotate; the line order never matters in the end.
        """
    ],
    "think": [
        SIMULATE,
        f"""
        **Order doesn't matter, counts do.** Students keep rotating, so if anyone in the line wants the top tray, that
        student eventually reaches the front and takes it. The top tray gets stuck only when **nobody** remaining wants
        that type. So walk the trays from the top, using up one student who wants each tray, until a tray type has no
        takers. For students `{prefers}` and trays `{trays}`:
        """,
        table(["top tray", "remaining preferences", "what happens"], *lrows),
        f"Hungry students: **{want[0] + want[1]}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Simulate: serve or rotate the front student; stop after a full pass with no one taking the top tray."],
            "build": ["Queue of students.", "Take or rotate.", "Stop after a full unproductive pass."],
            "complexity": ["**Time O(n²)** in the worst case (many rotations per tray). **Space O(n).**"],
            "limits": ["Rotations don't change who eventually gets each tray; only the counts of each preference matter."],
        },
        1: {
            "idea": ["Count students wanting 0 and 1. For each tray from the top, if nobody wants that type, stop; otherwise one such student eats. The answer is the number of students left."],
            "build": ["Count preferences.", "Walk the trays, using up counts.", "Stop at the first unwanted tray."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **When a queue rotates freely, only counts matter.**
        - Stop at the first item nobody wants.
        - **Pitfall:** skipping an unwanted tray and continuing (the stack blocks everything behind it).
        """
    ],
}


# ---------------------------------------------------------------- council-vote
council = "LOOLLO"
n = len(council)
larks = deque(i for i, c in enumerate(council) if c == "L")
owls = deque(i for i, c in enumerate(council) if c == "O")
crows = []
while larks and owls:
    a, b = larks.popleft(), owls.popleft()
    if a < b:
        larks.append(a + n)
        crows.append((f"L{a % n} (turn {a})", f"O{b % n} (turn {b})", f"Lark {a % n} speaks first and silences Owl {b % n}; the Lark is due again at turn {a + n}"))
    else:
        owls.append(b + n)
        crows.append((f"L{a % n} (turn {a})", f"O{b % n} (turn {b})", f"Owl {b % n} speaks first and silences Lark {a % n}; the Owl is due again at turn {b + n}"))
EXTRA["council-vote"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - All members from one party: they win immediately.
        - Silencing lasts for all later rounds.
        - Each member acts at most once per round, in speaking order.
        """
    ],
    "think": [
        SIMULATE,
        f"""
        **The best move: silence the next opponent due to speak.** An opponent who would speak soonest is the most
        immediate threat (they'd silence one of yours first). Silencing anyone further away only helps that soonest
        opponent. So every member silences the **next** member of the other party in speaking order.

        **Two queues of turns.** Put each party's members in a queue by turn number. Compare the two fronts: the earlier
        one speaks and silences the other front; the speaker rejoins its queue with turn number `+ n` (next round).
        The party whose queue is left non-empty wins. For `{council}`:
        """,
        table(["Lark front", "Owl front", "result"], *crows),
        f"Winner: **{'Larks' if larks else 'Owls'}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Replay rounds: each active member checks whether the other party is gone (victory), else scans forward around the circle for the next active opponent and silences them."],
            "build": ["Silenced flags and active counts.", "Each active member: check victory or silence the next opponent.", "Repeat rounds."],
            "complexity": ["**Time O(n²)** in the worst case (long scans for the next opponent). **Space O(n).**"],
            "limits": ["Scanning for the next opponent is linear. Queues of turn numbers make the next opponent the front of a queue."],
        },
        1: {
            "idea": [
                """
                Two queues of turn numbers. While both are non-empty, pop both fronts; the smaller turn speaks, silences
                the other (who is simply dropped), and rejoins its queue with turn `+ n`. The non-empty queue's party wins.

                **Why `+ n`.** A member who spoke in this round speaks again next round, after everyone still due in this
                round, which is exactly turn `+ n` in a continuing count.
                """
            ],
            "build": ["Queues of indices for each party.", "Compare fronts; the earlier speaks.", "Re-queue the speaker at `+ n`."],
            "complexity": ["**Time O(n):** each comparison removes one member for good. **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Turn-based elimination:** queues of turn numbers; re-queue with `+ n` for the next round.
        - Greedy: eliminate the opponent who would act soonest.
        - **Pitfall:** silencing the first opponent in the whole list instead of the next one in turn order.
        """
    ],
}


# ---------------------------------------------------------------- magic-card-reveal
cards = [5, 2, 9, 7, 1, 4]
nc = len(cards)
spots = deque(range(nc))
deck = [None] * nc
mrows = []
for card in sorted(cards):
    p = spots.popleft()
    deck[p] = card
    moved = None
    if spots:
        moved = spots.popleft()
        spots.append(moved)
    mrows.append((card, p, moved if moved is not None else "—", list(spots), " ".join("·" if x is None else str(x) for x in deck)))
EXTRA["magic-card-reveal"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One card: it's the whole deck.
        - The numbers are distinct, so "increasing order" is unambiguous.
        - The trick moves positions in a fixed pattern regardless of the numbers.
        """
    ],
    "think": [
        SIMULATE,
        """
        **Simulate positions, not cards.** The trick doesn't look at the numbers: which deck **position** is revealed
        1st, 2nd, 3rd, … is fixed. So run the trick on positions `0 … n − 1` with a queue: the front position is revealed
        (it receives the next smallest card), then the following position moves to the back.
        """,
        f"**Dealing the sorted cards {sorted(cards)} into positions:**",
        table(["card", "revealed position", "position moved to the bottom", "queue of positions after", "deck so far"], *mrows),
        f"Stack the deck as **{deck}**; the trick then reveals the cards in increasing order.",
    ],
    "approaches": {
        0: {
            "idea": ["Undo the trick backwards: take cards from largest to smallest; before placing each card on top, move the bottom card to the top (the reverse of 'move top to bottom')."],
            "build": ["Cards in decreasing order.", "Reverse step: bottom card to the top.", "Put the card on top."],
            "complexity": ["**Time O(n²)** with list inserts at the front. **Space O(n).**"],
            "limits": ["Inserting at the front of an array is O(n). Simulating positions forward with a queue is O(n)."],
        },
        1: {
            "idea": ["Queue of positions `0 … n − 1`. For each card in increasing order, assign it to the front position, then move the next position to the back."],
            "build": ["Sort the cards.", "Queue of positions.", "Reveal (assign) and move (rotate)."],
            "complexity": ["**Time O(n log n)** for the sort; the dealing is O(n). **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Fixed shuffling processes:** simulate on positions, then place values into the positions.
        - A queue models "take the front, move the next to the back".
        - **Pitfall:** simulating with the card values, which the process never looks at.
        """
    ],
}


# ---------------------------------------------------------------- typing-with-backspace
a, b = "xy#z##w", "q#xw"


def screen(keys):
    out, rows = [], []
    for c in keys:
        if c == "#":
            if out:
                out.pop()
        else:
            out.append(c)
        rows.append("".join(out) or "(empty)")
    return out, rows


sa, ra = screen(a)
sb, rb = screen(b)
EXTRA["typing-with-backspace"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A backspace on an empty box does nothing.
        - Several backspaces in a row delete several characters.
        - Both boxes may end empty (equal).
        """
    ],
    "think": [
        BUILD,
        f"**Typing `{a}`:**",
        table(["key"] + list(a), ["box shows"] + ra),
        f"**Typing `{b}`:**",
        table(["key"] + list(b), ["box shows"] + rb),
        f"""
        `"{''.join(sa)}"` vs `"{''.join(sb)}"`: **{str(sa == sb).lower()}**.

        **Reading from the end.** A character survives exactly when the backspaces after it don't reach it. Scanning
        backwards with a counter of pending backspaces finds the surviving characters one by one, without building the
        texts: compare them pairwise.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Build both final texts with a stack (push letters, pop on `#`) and compare."],
            "build": ["Stack-based typing for each string.", "Compare the results."],
            "complexity": ["**Time O(n + m).** **Space O(n + m)** for the two texts."],
            "limits": ["Builds both texts in full; walking from the end compares surviving characters with O(1) memory."],
        },
        1: {
            "idea": [
                """
                From the end of each string, find the next surviving character: count `#` as pending deletions and skip
                that many letters. Compare the two survivors; move both pointers on. Equal exactly when the survivors match
                all the way and both run out together.
                """
            ],
            "build": ["Helper: next surviving index going backwards.", "Compare survivors pairwise.", "Both must end together."],
            "complexity": ["**Time O(n + m).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Backspace strings:** stack to build, or scan from the end with a skip counter.
        - Reading backwards turns "deletes the previous character" into "skip the next character".
        - **Pitfall:** popping from an empty stack on a leading backspace.
        """
    ],
}


# ---------------------------------------------------------------- crush-the-runs
cs, ck = "abbbacca", 3
stack, crows2 = [], []
for c in cs:
    if stack and stack[-1][0] == c:
        stack[-1][1] += 1
        if stack[-1][1] == ck:
            stack.pop()
            act = f"run of {ck} '{c}': crush"
        else:
            act = f"extend the run of '{c}'"
    else:
        stack.append([c, 1])
        act = f"new run of '{c}'"
    crows2.append((c, act, " ".join(f"{x}×{m}" for x, m in stack) or "(empty)"))
final = "".join(x * m for x, m in stack)
cs2 = "deeedbbcccbdaa"
EXTRA["crush-the-runs"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A crush can join two runs into a new crushable run (chain reactions).
        - A run longer than `k` crushes `k` and leaves the rest.
        - Everything may be crushed (empty result).
        """
    ],
    "think": [
        BUILD,
        f"""
        **Runs on a stack.** Keep the output as a stack of `(tile, run length)`. A new tile either extends the top run
        (same tile) or starts a new run. When the top run reaches `k`, pop it: the runs on either side are now neighbours
        on the stack, so if they're the same tile the next arrival extends the joined run automatically. For `{cs}`,
        `k = {ck}`:
        """,
        table(["tile", "action", "stack (tile×run)"], *crows2),
        f"""
        Result **`{final}`**. Chain reactions happen naturally: in `{cs2}` with `k = 3`, crushing `ccc` makes the two `b`
        runs meet, and the next `b` completes a run of 3.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Find the first run of `k` equal tiles, cut it out, and repeat from the start until no run remains."],
            "build": ["Scan for a run of `k`.", "Cut it out.", "Repeat until nothing changes."],
            "complexity": ["**Time O(n² / k)** or worse: each crush rescans and rebuilds the string. **Space O(n).**"],
            "limits": ["Rescans everything after every crush. A stack of runs reacts to each tile in O(1)."],
        },
        1: {
            "idea": ["Stack of `[tile, count]`: extend the top run or push a new one; pop when the count reaches `k`. Expand the stack at the end."],
            "build": ["Stack of runs.", "Extend or push.", "Pop at `k`.", "Rebuild the string."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Repeated removal of adjacent groups:** stack of (value, run length).
        - Popping a run lets its neighbours merge on the stack automatically.
        - **Pitfall:** storing single characters and recounting runs each time.
        """
    ],
}


# ---------------------------------------------------------------- expand-the-pattern
pat = "2[ab3[c]]d"
stack, cur, num, erows = [], [], 0, []
for c in pat:
    if c.isdigit():
        num = num * 10 + int(c)
        act = f"number so far {num}"
    elif c == "[":
        stack.append((cur, num))
        act = f"save ('{''.join(cur)}', ×{num}) and start fresh"
        cur, num = [], 0
    elif c == "]":
        prev, kk = stack.pop()
        prev.append("".join(cur) * kk)
        act = f"close: repeat '{''.join(cur)}' ×{kk} and append to '{''.join(prev[:-1])}'"
        cur = prev
    else:
        cur.append(c)
        act = "letter"
    erows.append((c, act, "".join(cur) or "(empty)", len(stack)))
EXTRA["expand-the-pattern"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Multi-digit repeat counts (`12[a]`).
        - Nested groups (`2[a3[b]]`).
        - Letters outside any group.
        """
    ],
    "think": [
        BUILD,
        """
        **A stack of unfinished levels.** On `k[`, the text built so far at this level and the count `k` are saved, and a
        new level starts. On `]`, the inner text is repeated `k` times and appended to the saved outer text, which becomes
        the current level again. Letters append to the current level.
        """,
        f"**Trace on `{pat}`:**",
        table(["char", "action", "current level", "saved levels"], *erows),
        f"Result **`{''.join(cur)}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["Repeatedly find an innermost group `k[letters]` (no brackets inside) and replace it by its expansion, until no brackets remain."],
            "build": ["Find an innermost group.", "Replace it by its expansion.", "Repeat."],
            "complexity": ["**Time O(groups × output length).** **Space O(output).**"],
            "limits": ["Each replacement rebuilds the whole string. A stack expands every group once, when its `]` arrives."],
        },
        1: {
            "idea": ["Recursive descent: `parse()` reads letters and groups until a `]`; a group reads its number, recurses for the inside, and repeats the result."],
            "build": ["A position pointer.", "`parse` handles letters and `k[`…`]` groups.", "Recurse for nested groups."],
            "complexity": ["**Time O(output length).** **Space O(depth)** for recursion."],
            "limits": ["Recursion depth equals nesting depth; an explicit stack avoids that limit."],
        },
        2: {
            "idea": ["Explicit stack of `(text so far, count)`: digits build the count, `[` saves and resets, `]` repeats the inner text and appends it to the saved text, letters append."],
            "build": ["Stack, current pieces, current number.", "Handle digit, `[`, `]`, letter.", "Join the final pieces."],
            "complexity": ["**Time O(output length).** **Space O(output length).**"],
        },
    },
    "takeaways": [
        """
        - **Nested repetition grammars:** stack of (outer text, repeat count).
        - Build the count across multiple digits before the `[`.
        - **Pitfall:** treating each digit as a separate count.
        """
    ],
}


# ---------------------------------------------------------------- tidy-the-path
path = "/usr//local/./bin/../lib/.../"
stack, prows = [], []
for part in path.split("/"):
    if part == "..":
        if stack:
            stack.pop()
        act = "go up one folder"
    elif part and part != ".":
        stack.append(part)
        act = "enter folder"
    else:
        act = "empty or '.': ignore"
    prows.append((f"'{part}'", act, "/" + "/".join(stack)))
EXTRA["tidy-the-path"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `..` at the root stays at the root.
        - `...` (or any other dotted name) is an ordinary folder.
        - Repeated slashes and a trailing slash disappear.
        """
    ],
    "think": [
        BUILD,
        """
        **Folders on a stack.** Split the path at `/`. Empty parts (from repeated or trailing slashes) and `.` change
        nothing; `..` pops the last folder (if any); any other name is pushed. The stack, joined with `/` and prefixed by
        one `/`, is the tidy path.
        """,
        f"**Trace on `{path}`:**",
        table(["part", "action", "path so far"], *prows),
        f"Tidy path: **`{'/' + '/'.join(stack)}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["Apply text rewriting rules (collapse slashes, remove `/./`, remove `name/../`, handle `/../` at the root) until nothing changes."],
            "build": ["Add a trailing slash.", "Apply the rules repeatedly.", "Strip the trailing slash."],
            "complexity": ["**Time O(n²)** in the worst case. **Space O(n).**"],
            "limits": ["Each rewrite rescans the whole path, and the rules are easy to get subtly wrong. A stack of folders processes each part once."],
        },
        1: {
            "idea": ["Split at `/`, push names, pop on `..`, ignore empty parts and `.`; join with `/`."],
            "build": ["Split.", "Push, pop or ignore each part.", "Join with a leading `/`."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Path normalisation:** split and use a stack of folder names.
        - `..` pops (but never below the root); `.` and empty parts are ignored.
        - **Pitfall:** treating `...` as special.
        """
    ],
}
