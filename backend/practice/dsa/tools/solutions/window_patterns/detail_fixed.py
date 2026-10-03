"""Fuller explanations for the fixed-size window problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, Row, fig, table


def windows(values, k):
    return [(i, values[i:i + k]) for i in range(len(values) - k + 1)]


# ---------------------------------------------------------------- best-sales-week
sales, k = [3, -2, 5, -1, 4, -6, 2, 3], 3
tot = [sum(w) for _, w in windows(sales, k)]
best_i = max(range(len(tot)), key=lambda i: tot[i])
EXTRA["best-sales-week"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `k = n`: there is exactly one window, the whole array.
        - Every value negative: the answer is negative too. Starting the best at 0 would wrongly report 0.
        - `k = 1`: the answer is simply the largest single value.
        """
    ],
    "think": [
        f"""
        **Restating it.** Slide a frame of width `k` over the array. It sits at `n − k + 1` positions; for each one, add up
        what is inside, and report the largest of those sums.

        **Doing it by hand.** With `sales = {sales}` and `k = {k}` there are {len(tot)} frames:
        """,
        table(["start", "days", "total"], *[(i, w, t) for (i, w), t in zip(windows(sales, k), tot)]),
        f"""
        The best frame starts at day {best_i} with total **{tot[best_i]}**.

        **Spotting the waste.** Look at two neighbouring rows of the table. Frame 0 is `{sales[0:3]}` and frame 1 is
        `{sales[1:4]}`: they share `{sales[1:3]}`. Adding the shared part again is pure repetition. Going from one frame
        to the next, exactly one value leaves on the left and one value enters on the right:

        `total(next) = total(current) − value leaving + value entering`

        For example {tot[0]} − ({sales[0]}) + ({sales[3]}) = {tot[1]}. That is O(1) work per frame instead of O(k).

        **Why negatives don't break anything here.** In "variable size" window problems, negative numbers are dangerous
        because growing a window might lower its sum, so you can't tell when to stop growing. Here the size is fixed, so
        nothing is decided by growing or shrinking: we visit every frame and simply compare. The running total is exact
        whatever the signs.
        """,
        fig(Row(sales, st={x: "active" for x in range(best_i, best_i + k)}, ptr={"L": best_i, "R": best_i + k - 1}, label="best frame")),
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Treat every start `i` from `0` to `n − k` separately: add the `k` values `sales[i..i+k−1]` with a small
                inner loop and keep the largest total.

                This is the direct translation of the question, which makes it a good correctness reference: anything
                faster must produce the same numbers. It's also how you'd confirm the hand-made table above.
                """
            ],
            "complexity": [
                """
                **Time O(n · k).** There are `n − k + 1` starts and each costs `k` additions, so the work is
                `(n − k + 1) · k`. That product is largest when `k ≈ n/2`: about `n²/4`, which is 2.5 × 10⁹ for `n = 10⁵`.

                **Space O(1).** Only the running total and the best.
                """
            ],
        },
        1: {
            "idea": [
                """
                Compute the first frame's total once. Then move the frame one step at a time, and update the total with
                the value entering on the right and the value leaving on the left.

                **The invariant.** After processing index `i` (for `i ≥ k − 1`), `total` equals the sum of
                `sales[i − k + 1 .. i]`, the frame ending at `i`. It holds for the first frame by construction, and each
                update keeps it true because exactly one element enters and one leaves.

                **Why the answer is right.** Every frame ends at some `i` in `k − 1 .. n − 1`, and at that moment `total`
                is exactly its sum and gets compared with `best`. So the largest frame sum is seen.
                """
            ],
            "build": [
                "Add up `sales[0..k−1]`; this is the first frame, and also the best so far (not 0: totals may be negative).",
                "For `i` from `k` to `n − 1`: `total += sales[i] − sales[i − k]`. Now `total` is the frame ending at `i`.",
                "After each update, `best = max(best, total)`.",
                "Return `best` as a 64-bit value.",
            ],
            "complexity": [
                """
                **Time O(n).** `k` additions for the first frame plus one O(1) update for each of the other `n − k`
                frames: `n` operations in total, regardless of `k`.

                **Space O(1).**

                **Range check.** A frame sum is at most `10⁵ · 10⁴ = 10⁹` in size, which fits in 32 bits, but the return
                type is `long`, so the code accumulates in 64 bits anyway.
                """
            ],
        },
    },
    "takeaways": [
        """
        - **Recognise it:** "every block of exactly `k` consecutive items", with an aggregate (sum, count, number of
          matches) that you can update when one item enters and one leaves.
        - **Template:** build the first window, then loop `i = k..n−1` doing `+ a[i] − a[i−k]`, and evaluate after each
          update.
        - **Pitfalls:** starting `best` at 0 when values can be negative; an off-by-one that skips the first window or
          the last one (there are `n − k + 1` windows).
        - **Related:** the same running-sum idea answers averages (divide by `k`), counts of a property (add 0/1 flags)
          and "is any window good enough" checks.
        """
    ],
}


# ---------------------------------------------------------------- calm-shift
cus, moody, mins = [2, 0, 4, 1, 3, 5, 1, 2], [0, 1, 1, 0, 1, 1, 0, 1], 2
base = sum(c for c, m in zip(cus, moody) if not m)
lost = [c * m for c, m in zip(cus, moody)]
gains = [sum(lost[i:i + mins]) for i in range(len(cus) - mins + 1)]
gi = max(range(len(gains)), key=lambda i: gains[i])
EXTRA["calm-shift"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `minutes = n`: the owner is calm all day, so every customer is happy.
        - The owner is never moody: the calm stretch changes nothing; the answer is the total of all customers.
        - Several placements tie: any of them gives the same count, so ties don't matter.
        """
    ],
    "think": [
        f"""
        **Restating it.** Each minute is either "happy anyway" (owner not moody) or "lost unless covered" (owner moody).
        We place one block of `minutes` consecutive minutes; inside it, lost customers are rescued. Maximise happy
        customers.

        **Separate what you control from what you don't.** Customers in non-moody minutes are happy whatever we do:
        that's `{base}` here. The only thing our choice changes is how many moody-minute customers fall inside the block.
        So:

        `answer = (customers in non-moody minutes) + (most rescued customers by one block)`

        **Turn the condition into a number.** A customer at minute `i` can be rescued only if `moody[i] = 1`, so the
        number rescued at that minute is `customers[i] · moody[i]`:
        """,
        table(["minute", "customers", "moody", "rescuable"], *[(i, c, m, l) for i, (c, m, l) in enumerate(zip(cus, moody, lost))]),
        f"""
        Now the second part is an ordinary fixed-size window: the block of `{mins}` minutes with the largest sum of
        `rescuable`. The block sums are `{gains}`; the best starts at minute {gi} and rescues {gains[gi]}. Answer
        {base} + {gains[gi]} = **{base + gains[gi]}**.

        **Why the split is valid.** The two parts don't interact: a non-moody minute counts the same inside or outside
        the block, so including it in the window sum would double-count it. Multiplying by `moody[i]` makes such minutes
        contribute 0 to the window.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Try every placement of the calm block, `start = 0 .. n − minutes`. For each placement, walk the whole day
                and count a minute's customers as happy if the owner isn't moody **or** the minute falls in
                `[start, start + minutes)`. Keep the best count.

                It's correct by definition, but each placement recounts the entire day, including the "happy anyway" part
                that never changes.
                """
            ],
            "complexity": [
                "**Time O(n²):** `n − minutes + 1` placements × `n` minutes each, up to 10¹⁰. **Space O(1).**"
            ],
        },
        1: {
            "idea": [
                """
                Compute `base` (customers in non-moody minutes) once. Then slide a window of length `minutes` over the
                rescuable counts `customers[i] · moody[i]`, keeping the window total `gain` and the best `gain` seen.

                **Invariant.** After processing minute `i ≥ minutes − 1`, `gain` is the number rescued by the block that
                ends at `i`.

                **Why it's right.** Every placement of the block ends at some `i` and is evaluated exactly once, and
                `base + gain` is exactly the number of happy customers for that placement, because `base` and `gain`
                count disjoint sets of minutes.
                """
            ],
            "build": [
                "`base` = total customers over minutes with `moody[i] = 0`.",
                "`gain` = rescuable customers in minutes `0 .. minutes − 1`; `best = gain`.",
                "For each later minute `i`: add `customers[i] · moody[i]`, subtract `customers[i − minutes] · moody[i − minutes]`, update `best`.",
                "Return `base + best`.",
            ],
            "complexity": [
                """
                **Time O(n):** one pass for `base`, one for the window. **Space O(1).**

                The largest possible answer is `10⁵ · 1000 = 10⁸`, which fits in a 32-bit int.
                """
            ],
        },
    },
    "takeaways": [
        """
        - **Split the objective** into a fixed part and a part your choice controls; optimise only the second.
        - **Weights instead of conditions:** `value · flag` turns "count only when …" into a plain sum.
        - Then it's the fixed-window maximum: first window, then `+ entering − leaving`.
        - **Pitfall:** adding non-moody customers into the window as well, which double-counts them.
        """
    ],
}


# ---------------------------------------------------------------- calm-stretches
noise, kk, limit = [4, 6, 2, 3, 8, 1, 2, 5], 3, 4
cap = limit * kk
rows = [(i, w, sum(w), f"{sum(w) / kk:.2f}", "calm" if sum(w) <= cap else "loud") for i, w in windows(noise, kk)]
EXTRA["calm-stretches"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Averages are fractions: `7/3` is not `2`. Integer division would round and give wrong answers.
        - "At most" includes equality: an average exactly equal to `limit` counts as calm.
        - `limit · k` can reach 10⁹; still fits in 32 bits, but 64-bit arithmetic is the safe habit.
        """
    ],
    "think": [
        f"""
        **Restating it.** Count the windows of exactly `k` readings whose average is at most `limit`.

        **Remove the division.** All windows have the same length `k`, so

        `sum / k ≤ limit  ⇔  sum ≤ limit · k`

        (multiplying both sides by the positive `k` keeps the direction). Here `limit · k = {limit} · {kk} = {cap}`. This
        avoids floating point and rounding entirely.

        **By hand** with `noise = {noise}`:
        """,
        table(["start", "window", "sum", "average", "verdict"], *rows),
        f"""
        **{sum(1 for r in rows if r[4] == 'calm')}** windows are calm.

        Each row's sum differs from the previous one by one value entering and one leaving, so the running-sum window
        applies directly: instead of a maximum, we keep a counter.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                For each start, add the `k` readings and test the sum against `limit · k`. This is a direct check of the
                definition, useful as a reference, but it repeats `k − 1` additions per window.
                """
            ],
            "complexity": ["**Time O(n · k).** **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Precompute `cap = limit · k`. Sum the first window; it's calm if `sum ≤ cap`. Then, for each next window,
                update the sum with `+ entering − leaving` and test it again.

                **Invariant.** Right after the update at index `i`, `total` is the sum of the window ending at `i`. So each
                of the `n − k + 1` windows is tested exactly once, with its exact sum.
                """
            ],
            "build": [
                "`cap = limit · k` (64-bit).",
                "Sum the first `k` readings; count 1 if the sum is at most `cap`.",
                "For `i = k..n−1`: `total += noise[i] − noise[i − k]`; count it if `total ≤ cap`.",
                "Return the count.",
            ],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Average over a fixed length → compare sums with `limit · k`**; it's exact and avoids floats.
        - Running windows can count, not just maximise.
        - **Pitfalls:** integer division of the average; `<` instead of `≤`.
        """
    ],
}


# ---------------------------------------------------------------- seat-the-team
seats = [1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
n, t = len(seats), sum(seats)
arcs = [(i, [(i + j) % n for j in range(t)]) for i in range(n)]
arc_rows = [(i, [seats[x] for x in a], sum(seats[x] for x in a), t - sum(seats[x] for x in a)) for i, a in arcs]
bi = max(range(n), key=lambda i: arc_rows[i][2])
EXTRA["seat-the-team"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No team members, or everyone is a team member: 0 swaps.
        - The best group may wrap around the end of the list (the table is round).
        - A swap can move any two people, not just neighbours.
        """
    ],
    "think": [
        f"""
        **What does the final seating look like?** There are `t = {t}` team members. When they sit together, they fill
        some arc of exactly `{t}` consecutive seats, going around the table. So the question becomes: which arc should
        they end up in, and how many swaps does that arc cost?

        **Cost of one arc.** Inside the chosen arc, every guest has to leave, and outside it, every member has to come
        in. The two numbers are equal (the arc has `t` seats and there are `t` members). One swap of a guest inside with a
        member outside fixes one guest and one member, so the cost is exactly **the number of guests in the arc**; it
        can't be done with fewer, because each swap moves at most one member into the arc.

        **All arcs, by hand** (`seats = {seats}`):
        """,
        table(["start", "arc", "members", "guests = swaps"], *arc_rows),
        f"""
        The arc starting at seat {bi} already has {arc_rows[bi][2]} members, so **{arc_rows[bi][3]}** swap(s) are enough.

        **Why a window works.** Arcs are windows of fixed length `t` over a circular array. Moving the arc one seat
        clockwise adds one seat and removes one, so the member count updates in O(1). The circle is handled by letting the
        index run past `n − 1` and taking `i % n`.
        """,
        fig(Row(seats, st={x: ("found" if seats[x] else "mark") for x in arcs[bi][1]}, label="best arc (guests in red)")),
    ],
    "approaches": {
        0: {
            "idea": [
                """
                For every starting seat `i`, count the members in seats `i, i+1, …, i+t−1` (mod `n`). The best arc has the
                most members, and the answer is `t − most`.

                The reasoning about swaps is the important part; this approach then just evaluates every arc separately.
                """
            ],
            "complexity": ["**Time O(n · t)**, up to O(n²) when about half the seats are members. **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Count members in seats `0..t−1`. Then rotate the arc one seat at a time: seat `i % n` enters and seat
                `(i − t) % n` leaves, for `i = t .. n + t − 2`. Track the largest member count.

                **Coverage.** Starting seats `0, 1, …, n − 1` are each visited exactly once (the loop produces `n − 1`
                further arcs after the first), including arcs that wrap past the end.

                **Answer.** `t − (most members in an arc)` = fewest guests to swap out.
                """
            ],
            "build": [
                "Count `t`; if it's 0, return 0.",
                "Members in seats `0..t−1` → `inside`, `best`.",
                "For `i = t .. n + t − 2`: `inside += seats[i % n] − seats[(i − t) % n]`; update `best`.",
                "Return `t − best`.",
            ],
            "complexity": ["**Time O(n):** `t` for the first arc plus `n − 1` O(1) rotations. **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **"Group k items together" → pick the window they end up in**; its cost is what doesn't belong there.
        - **Arbitrary swaps:** each swap fixes one misplaced pair, so cost = number of outsiders inside the window.
        - **Circular arrays:** run the index to `n + k − 1` and use `% n` (or concatenate the array with itself).
        - **Pitfall:** forgetting arcs that wrap around the end.
        """
    ],
}


# ---------------------------------------------------------------- vowel-rich-window
s5, k5 = "rhythmaeiouxqueue", 5
flags = [1 if c in "aeiou" else 0 for c in s5]
counts = [sum(flags[i:i + k5]) for i in range(len(s5) - k5 + 1)]
bv = max(range(len(counts)), key=lambda i: counts[i])
EXTRA["vowel-rich-window"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No vowels at all: the answer is 0.
        - `k = n`: count the vowels of the whole string.
        - The maximum possible answer is `k`; once reached you could stop early.
        """
    ],
    "think": [
        f"""
        **Turn letters into numbers.** Write 1 under every vowel and 0 under every other letter. "Vowels in a substring"
        becomes "sum of the flags in a window":
        """,
        fig(Row(list(s5), label="s"), Row(flags, label="vowel?")),
        f"""
        **Window sums** for `k = {k5}`: `{counts}`. The best window is `"{s5[bv:bv + k5]}"` at index {bv} with
        **{counts[bv]}** vowels.

        **The update.** Sliding right changes two letters: the one leaving can lower the count by 1 (if it was a vowel)
        and the one entering can raise it by 1 (if it is a vowel). So the next count is
        `count + isVowel(entering) − isVowel(leaving)`.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                "For each start, count the vowels in the next `k` letters. Correct, but every window recounts `k − 1` letters it shares with its neighbour."
            ],
            "complexity": ["**Time O(n · k).** **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Count vowels in the first `k` letters. Then for each `i ≥ k`, add 1 if `s[i]` is a vowel and subtract 1 if
                `s[i − k]` was one. Keep the maximum.

                **Invariant.** After the update at `i`, `count` is the number of vowels in `s[i − k + 1 .. i]`.
                """
            ],
            "build": [
                "A helper `isVowel(c)` returning 1 or 0.",
                "Count over `s[0..k−1]`; that's `best`.",
                "Slide: `count += isVowel(s[i]) − isVowel(s[i − k])`; update `best`.",
                "Return `best`.",
            ],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Count a property in fixed windows** = sliding sum of 0/1 flags.
        - Only the two edge letters change per step.
        - Early exit when the count reaches `k` is a free bonus.
        """
    ],
}
