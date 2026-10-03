"""In-depth text for the opposite-ends two-pointer problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

ELIMINATE = """
**Why moving inward is safe: every step rules out a whole row of pairs.** Picture all pairs `(i, j)` with `i < j`
as a triangle. With the pointers at the two ends we look at one pair, and the comparison proves that one of its two
elements **can't be part of a better answer with any partner still between the pointers**. So we drop that element:
a whole row (or column) of the triangle disappears in O(1). After at most `n − 1` steps every pair has been either
checked or ruled out, which is why one pass is enough.
"""


# ---------------------------------------------------------------- biggest-water-tank
posts = [3, 7, 2, 6, 4, 8, 1]
trow, i, j, best = [], 0, len(posts) - 1, 0
while i < j:
    area = (j - i) * min(posts[i], posts[j])
    best = max(best, area)
    short = "left" if posts[i] < posts[j] else "right"
    gone = i if posts[i] < posts[j] else j
    trow.append((i, j, posts[i], posts[j], f"{j - i} × {min(posts[i], posts[j])} = {area}", best, f"post {gone} ({short}, shorter) is finished"))
    if posts[i] < posts[j]:
        i += 1
    else:
        j -= 1
EXTRA["biggest-water-tank"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Posts of height 0 hold no water.
        - Equal heights at both ends: moving either pointer is fine.
        - The area can reach `10⁵ × 10⁹ = 10¹⁴`, so it needs 64 bits.
        """
    ],
    "think": [
        """
        **Restating it.** Choose `i < j` to maximise `(j − i) · min(posts[i], posts[j])`: width times the shorter post.
        """,
        ELIMINATE,
        """
        **Which post is finished?** Look at the current pair and suppose `posts[i]` is the shorter one. Any other tank
        using post `i` with a partner between the pointers is **narrower** (its partner is closer), and its height is at
        most `posts[i]` (the shorter post caps the water). So none of them can beat the current tank, and post `i` can be
        dropped. Moving the taller post instead could never help: the height stays capped by the same short post while
        the width shrinks.
        """,
        f"**Trace on `{posts}`:**",
        table(["i", "j", "posts[i]", "posts[j]", "area", "best", "decision"], *trow),
        f"Best tank **{best}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Try every pair of posts and compute its area; keep the largest. It checks all `n(n − 1)/2` pairs, so it's a reliable reference."],
            "build": ["Two nested loops over `i < j`.", "Area = width × shorter height.", "Keep the maximum."],
            "complexity": ["**Time O(n²):** 5 × 10⁹ pairs for `n = 10⁵`. **Space O(1).**"],
            "limits": ["Most pairs can be ruled out without being checked: once a post is the shorter end of a pair, no narrower tank with it can win."],
            "lines": {
                "init": "The best area so far (0 is safe: an area is never negative).",
                "pairs": "Every pair of posts with `i < j`.",
                "area": "Width `j − i` times the shorter of the two heights, computed in 64 bits.",
                "ret": "The largest area.",
            },
        },
        1: {
            "idea": [
                """
                Start with the widest tank (posts `0` and `n − 1`). Record its area, then move the pointer at the
                **shorter** post inward. Repeat until the pointers meet.

                **Invariant.** The best tank overall is either already recorded or uses two posts between `i` and `j`
                (inclusive). Dropping the shorter post keeps this true, by the argument above.
                """
            ],
            "build": ["Pointers at both ends.", "Record the current area.", "Move the shorter side inward.", "Stop when they meet."],
            "complexity": ["**Time O(n):** each step moves one pointer, at most `n − 1` steps. **Space O(1).**"],
            "lines": {
                "init": "The widest possible tank, and the best area so far.",
                "loop": "While at least two posts remain between the pointers.",
                "area": "Record the current tank: width `j − i` times the shorter post, in 64 bits.",
                "move": "The shorter post can't do better with any narrower partner, so it's finished. On a tie either may move: both are finished.",
                "ret": "The largest area seen.",
            },
        },
    },
    "takeaways": [
        """
        - **Recognise it:** choose two positions to maximise something that depends on their distance and the smaller value.
        - **Template:** start widest, move the side that limits the answer.
        - **Pitfall:** moving the taller side, which can't improve the area.
        """
    ],
}


# ---------------------------------------------------------------- boats-for-hikers
weights, limit = [70, 50, 80, 50, 30, 90], 100
a = sorted(weights)
brow, i, j, boats = [], 0, len(a) - 1, 0
while i <= j:
    if i == j:
        brow.append((a[j], "—", "alone (last hiker)"))
    elif a[i] + a[j] <= limit:
        brow.append((a[j], a[i], f"{a[j]} + {a[i]} = {a[i] + a[j]} ≤ {limit}: together"))
        i += 1
    else:
        brow.append((a[j], "—", f"{a[j]} + {a[i]} = {a[i] + a[j]} > {limit}: alone"))
    j -= 1
    boats += 1
EXTRA["boats-for-hikers"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One hiker: one boat.
        - Everyone can pair: `n / 2` boats (rounded up).
        - Nobody can pair: `n` boats.
        - A boat holds at most **two** hikers, even if three would fit by weight.
        """
    ],
    "think": [
        f"""
        **Restating it.** Split the hikers into groups of one or two, with every pair's total at most `limit`, using as
        few groups as possible. Fewest boats = most pairs.

        **Start with the heaviest hiker.** They need a boat anyway. Their best partner is the **lightest** hiker:

        - If even the lightest doesn't fit with them, nobody does, so the heaviest goes alone.
        - If the lightest fits, pairing them is never worse. Take any optimal plan: if the heaviest is paired with
          someone else (or alone), swap partners with the lightest. Every boat still fits, because the lightest is no
          heavier than whoever they swapped with, and the number of boats doesn't increase.

        After that decision, the same reasoning applies to the remaining hikers. Sorted weights `{a}`:
        """,
        table(["heaviest left", "lightest left", "decision"], *brow),
        f"Boats: **{boats}**.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Sort heaviest first. For each hiker not yet seated, start a boat and look for the **heaviest** remaining
                hiker who still fits as a partner. This greedy also gives the optimum (it's the same exchange argument in
                another form), but searching for the partner is a linear scan.
                """
            ],
            "build": ["Sort descending.", "For each unseated hiker, open a boat.", "Scan for the heaviest partner who fits.", "Count boats."],
            "complexity": ["**Time O(n²)** for the partner searches. **Space O(n)** for the seated flags."],
            "limits": ["The partner search rescans the list. Since the lightest hiker is always the best partner to test, two pointers on the sorted list answer it in O(1)."],
            "lines": {
                "sort": "Heaviest first, so the hardest hikers are placed first.",
                "heavy": "This hiker isn't seated yet: they get a new boat.",
                "partner": "Seat the heaviest unseated hiker who still fits with them, if any.",
                "ret": "The number of boats.",
            },
        },
        1: {
            "idea": [
                """
                Sort ascending. `i` points at the lightest unseated hiker and `j` at the heaviest. Each step fills one
                boat: the heaviest always goes; the lightest joins if the two fit together.

                **Invariant.** Hikers outside `[i, j]` are seated optimally, and an optimal plan for the rest exists that
                doesn't touch them (exchange argument above).
                """
            ],
            "build": ["Sort ascending.", "Pointers at the lightest and heaviest.", "Heaviest goes every step; the lightest joins if they fit.", "One boat per step."],
            "complexity": ["**Time O(n log n)** for the sort; the pairing pass is O(n). **Space O(1)** besides the sort (O(n) for the copy in Python)."],
            "lines": {
                "sort": "Light to heavy, so both extremes are at the ends.",
                "init": "Lightest and heaviest unseated hikers, and the boat count.",
                "loop": "While someone is still on shore. `i == j` is the last hiker, who goes alone.",
                "pair": "If the lightest fits with the heaviest, they share this boat.",
                "heavy": "The heaviest leaves on this boat either way.",
                "ret": "One boat per step.",
            },
        },
    },
    "takeaways": [
        """
        - **Pairing to minimise groups:** sort, then try heaviest with lightest.
        - Justify greedy choices with an **exchange argument**: swap into any optimal plan without making it worse.
        - **Pitfall:** pairing heaviest with the heaviest that fits is fine but slow; with the lightest it's O(1).
        """
    ],
}


# ---------------------------------------------------------------- budget-pair
prices, budget = [2, 5, 9, 14, 20, 27], 34
prow, i, j = [], 0, len(prices) - 1
while i < j:
    s = prices[i] + prices[j]
    if s == budget:
        prow.append((i, j, f"{prices[i]} + {prices[j]} = {s}", "found"))
        break
    if s < budget:
        prow.append((i, j, f"{prices[i]} + {prices[j]} = {s}", f"too small: {prices[i]} + anything left ≤ {s}, drop index {i}"))
        i += 1
    else:
        prow.append((i, j, f"{prices[i]} + {prices[j]} = {s}", f"too big: anything + {prices[j]} ≥ {s}, drop index {j}"))
        j -= 1
EXTRA["budget-pair"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Negative prices are allowed; the reasoning only needs the list to be sorted.
        - Sums can reach `2 × 10⁹`, past 32-bit range, so add in 64 bits.
        - The pair uses two **different** positions, even if their values are equal.
        """
    ],
    "think": [
        ELIMINATE,
        """
        **The two moves.** With `s = prices[i] + prices[j]`:

        - `s < budget`: `prices[i]` plus any remaining partner is at most `s` (the largest partner is `prices[j]`), so
          `i` can't be in the pair. Move `i` right.
        - `s > budget`: `prices[j]` plus any remaining partner is at least `s`, so `j` can't be in the pair. Move `j` left.
        """,
        f"**Trace for budget {budget} on `{prices}`:**",
        table(["i", "j", "sum", "decision"], *prow),
        f"Answer `[{i}, {j}]`.",
    ],
    "approaches": {
        0: {
            "idea": ["Check every pair `i < j` and return the one that sums to the budget."],
            "build": ["Two nested loops.", "Return the first matching pair."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Ignores that the prices are sorted. A hash map gives O(n) without using the order; two pointers use the order to get O(n) with no extra memory."],
            "lines": {
                "pairs": "Every pair of positions with `i < j`.",
                "hit": "The pair that costs exactly the budget (sum in 64 bits).",
                "ret": "Unreachable when a pair is guaranteed; kept as a safe default.",
            },
        },
        1: {
            "idea": [
                """
                Walk the prices once, remembering each price's position. For price `p` at `j`, the partner must cost
                `budget − p`; if it was seen earlier, return its position and `j`.

                This works on unsorted lists too, but uses O(n) memory.
                """
            ],
            "build": ["Empty map price → position.", "Look up the complement.", "Store the current price."],
            "complexity": ["**Time O(n)** expected. **Space O(n).**"],
            "limits": ["It needs a hash map. Sorted input allows the same answer in O(1) memory."],
            "lines": {
                "init": "Prices seen so far and their positions.",
                "loop": "Each price in order.",
                "hit": "The needed partner was seen earlier: that's the pair, with the earlier position first.",
                "store": "Remember this price for later positions (after the lookup, so it never pairs with itself).",
                "ret": "Unreachable when a pair is guaranteed.",
            },
        },
        2: {
            "idea": [
                """
                Pointers at both ends. If the sum is the budget, done; if it's too small, move `i` right; if too big, move
                `j` left.

                **Invariant.** If the answer pair is `(p, q)`, then `i ≤ p` and `q ≤ j` at all times. A pointer only moves
                past an index that was proven not to be in the pair.
                """
            ],
            "build": ["Pointers at both ends.", "Compare the sum with the budget.", "Move the side that can't be in the pair."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "lines": {
                "init": "The cheapest and the most expensive item.",
                "loop": "While two different items remain.",
                "hit": "Exactly the budget: return the positions.",
                "move": "Too small: the cheap item fails with every remaining partner, drop it. Too big: the expensive item fails with every remaining partner, drop it.",
                "ret": "Unreachable when a pair is guaranteed.",
            },
        },
    },
    "takeaways": [
        """
        - **Pair sum on a sorted array:** two pointers, O(n) time, O(1) memory.
        - **Unsorted:** a hash map of complements, O(n) memory.
        - **Pitfall:** 32-bit overflow when adding two large values.
        """
    ],
}


# ---------------------------------------------------------------- closest-pair-sum
nums, target = [8, -4, 15, 3, -9, 6], 5
c = sorted(nums)
crow, i, j, best = [], 0, len(c) - 1, None
while i < j:
    s = c[i] + c[j]
    if best is None or (abs(s - target), s) < (abs(best - target), best):
        best = s
    if s < target:
        crow.append((i, j, f"{c[i]} + {c[j]} = {s}", abs(s - target), best, f"below target: drop {c[i]}"))
        i += 1
    elif s > target:
        crow.append((i, j, f"{c[i]} + {c[j]} = {s}", abs(s - target), best, f"above target: drop {c[j]}"))
        j -= 1
    else:
        crow.append((i, j, f"{c[i]} + {c[j]} = {s}", 0, best, "exact: stop"))
        break
EXTRA["closest-pair-sum"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Ties: if two sums are equally close, return the **smaller** sum.
        - An exact match can stop the search immediately.
        - Values and target are large: sums and distances need 64 bits.
        """
    ],
    "think": [
        """
        **Restating it.** Among all pairs, the sum with the smallest distance to `target`, preferring the smaller sum on
        ties.
        """,
        ELIMINATE,
        """
        **Which side is finished?** After sorting, with `s = a[i] + a[j]`:

        - `s < target`: every other partner of `a[i]` between the pointers is at most `a[j]`, so those sums are at most
          `s`: even further below the target (or equal to `s`). `a[i]` has nothing better left; drop it.
        - `s > target`: symmetric, drop `a[j]`.
        - `s = target`: distance 0 can't be beaten.
        """,
        f"**Trace for target {target}** on sorted `{c}`:",
        table(["i", "j", "sum", "distance", "best so far", "decision"], *crow),
        f"Answer **{best}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Check every pair and keep the sum that's closest, using `(distance, sum)` as the comparison key so ties prefer the smaller sum."],
            "build": ["Two nested loops.", "Compare by `(distance, sum)`.", "Keep the best."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Quadratic. After sorting, each comparison with the target rules out one element entirely."],
            "lines": {
                "init": "No pair seen yet.",
                "pairs": "Every pair of different positions.",
                "better": "Closer to the target wins; on equal distance, the smaller sum wins. Java and C compute in 64 bits.",
                "ret": "The best sum.",
            },
        },
        1: {
            "idea": [
                """
                Sort, then squeeze from both ends: record each pair's sum if it's better, then move `i` right when the sum
                is below the target, `j` left when above, and stop on an exact hit.

                **Invariant.** The best pair is either already recorded or lies between the pointers, because every
                dropped element had no better partner left (argument above).
                """
            ],
            "build": ["Sort a copy.", "Pointers at both ends.", "Record if better, then move toward the target.", "Stop on exact."],
            "complexity": ["**Time O(n log n)** for the sort, O(n) for the squeeze. **Space O(n)** for the sorted copy."],
            "lines": {
                "sort": "Sorting puts the smallest and largest values at the ends.",
                "init": "Pointers at both ends; no best yet.",
                "loop": "While two different elements remain.",
                "better": "Keep this sum if it's closer, or equally close and smaller.",
                "move": "Below the target, the small end can't do better: move it right. Above, move the large end left. An exact hit can't be beaten.",
                "ret": "The best sum.",
            },
        },
    },
    "takeaways": [
        """
        - **Closest pair sum:** sort, squeeze toward the target, record on every step.
        - Express tie rules as a tuple key `(distance, value)`.
        - **Pitfall:** stopping as soon as the distance grows; it can shrink again later.
        """
    ],
}


# ---------------------------------------------------------------- fewest-swaps-to-palindrome
word = "letelt"
srow, s, moves = [], list(word), 0
while len(s) > 1:
    j = len(s) - 1
    while s[j] != s[0]:
        j -= 1
    before = "".join(s)
    if j == 0:
        cost = len(s) // 2
        moves += cost
        s.pop(0)
        srow.append((before, f"'{before[0]}' has no partner: it belongs in the middle", cost, moves, "".join(s) or "—"))
    else:
        cost = len(s) - 1 - j
        moves += cost
        s.pop(j)
        s.pop(0)
        srow.append((before, f"partner of '{before[0]}' at {j}: drag it to the end", cost, moves, "".join(s) or "—"))
EXTRA["fewest-swaps-to-palindrome"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Already a palindrome: 0 moves.
        - Odd length: exactly one letter has an odd count and ends up in the middle.
        - The answer can reach about `n²/4 ≈ 10⁶` for `n = 2000`.
        """
    ],
    "think": [
        """
        **Fix the outside first.** In the final palindrome, the first and last letters match. Keep the current first
        letter where it is and bring a copy of it to the end. The cheapest copy to bring is the **last** one (closest to
        the end): dragging it costs one swap per letter it passes. After that, the outer pair is done and never needs to
        move again, so remove both and repeat on the inside.

        **Why keeping the first letter is fine.** Choosing to fix the outer pair with the first letter's value, or with
        the last letter's value, costs the same by symmetry, and swaps that cross the fixed pair would only waste moves.
        Committing greedily to the nearest copies never forces extra swaps later, because the relative order of the
        remaining letters is unchanged.

        **The middle letter.** If the first letter has no other copy, it's the odd one that belongs in the middle. Moving
        it there costs `len // 2` swaps; doing that now or later costs the same, so count it and remove it.
        """,
        f"**Trace on `\"{word}\"`:**",
        table(["current", "action", "swaps", "total", "left to fix"], *srow),
        f"Total **{moves}** moves.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Repeat on a shrinking list: find the last copy of the first letter. If it's not the first letter itself,
                add the distance from it to the end, then remove it and the first letter. If it is, the first letter is the
                middle one: add `len // 2` and remove it.

                Searching all arrangements (a BFS over swaps) is hopeless for 2000 letters; the greedy argument above is
                what makes this tractable.
                """
            ],
            "build": ["Copy the word into a list.", "Find the last copy of the first letter.", "Add its distance to the end, or `len // 2` for the middle letter.", "Remove the fixed letters and repeat."],
            "complexity": ["**Time O(n²):** up to `n/2` rounds, each with an O(n) search and O(n) removals; fine for `n ≤ 2000`. **Space O(n).**"],
            "lines": {
                "init": "A mutable copy of the word and the move count.",
                "loop": "While at least two letters are left to place.",
                "find": "Search from the end for the copy of the first letter that's closest to the end: it needs the fewest swaps.",
                "middle": "The first letter has no other copy: it's the odd letter, which needs `len // 2` swaps to reach the middle. Remove it and keep going.",
                "pair": "Dragging the partner to the end passes `len − 1 − j` letters, one swap each. Then both ends are fixed and removed.",
                "ret": "The total number of swaps.",
            },
        },
    },
    "takeaways": [
        """
        - **Adjacent swaps to reach a target shape:** fix the outermost positions greedily with the nearest matching item.
        - The cost of dragging an item is the number of items it passes.
        - **Pitfall:** handling the odd middle letter too early or forgetting its cost.
        """
    ],
}


# ---------------------------------------------------------------- reverse-letters-only
text = "ab-cd3e!f"
arr, rrow, i, j = list(text), [], 0, len(text) - 1
while i < j:
    if not arr[i].isalpha():
        rrow.append((i, j, arr[i], arr[j], "left isn't a letter: skip it", "".join(arr)))
        i += 1
    elif not arr[j].isalpha():
        rrow.append((i, j, arr[i], arr[j], "right isn't a letter: skip it", "".join(arr)))
        j -= 1
    else:
        arr[i], arr[j] = arr[j], arr[i]
        rrow.append((i, j, arr[j], arr[i], "swap", "".join(arr)))
        i, j = i + 1, j - 1
EXTRA["reverse-letters-only"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No letters at all: the text is unchanged.
        - One letter: unchanged.
        - Upper- and lowercase letters both move; digits, spaces and punctuation stay put.
        """
    ],
    "think": [
        """
        **What reversing the letters means.** Number the letters from the left: 1st, 2nd, …, kth. After reversal the 1st
        letter's slot holds the kth letter, the 2nd holds the (k−1)th, and so on. So the letters swap in pairs from the
        outside in, exactly like reversing an array, except that non-letters are invisible.

        **Two pointers that skip.** `i` finds the next letter from the left and `j` the next from the right; swap them and
        move both. A non-letter is skipped on whichever side it appears.
        """,
        f"**Trace on `\"{text}\"`:**",
        table(["i", "j", "s[i]", "s[j]", "action", "text now"], *rrow),
        f"Result **`{''.join(arr)}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["Collect the letters in order, then walk the text again: each letter slot takes the last collected letter (popping from the end reverses the order), and other characters are copied unchanged."],
            "build": ["Collect the letters.", "Rebuild: letters from the back of the list, other characters as they are."],
            "complexity": ["**Time O(n).** **Space O(n)** for the letter list (plus the output)."],
            "limits": ["Needs a separate list of letters. Swapping in place from both ends needs no extra list."],
            "lines": {
                "gather": "The letters in their original order.",
                "write": "Each letter position takes the last remaining collected letter; non-letters are copied unchanged.",
                "ret": "The rebuilt text.",
            },
        },
        1: {
            "idea": [
                """
                Pointers at both ends of a mutable copy. Skip a non-letter on the left or on the right (one at a time);
                when both are letters, swap them and move both inward.

                **Why it's the reversal.** The kth swap exchanges the kth letter from the left with the kth letter from the
                right, which is exactly where the reversal sends them.
                """
            ],
            "build": ["Mutable copy, pointers at both ends.", "Skip non-letters one side at a time.", "Swap letters and move both inward."],
            "complexity": ["**Time O(n).** **Space O(1)** besides the output copy."],
            "lines": {
                "init": "A mutable copy of the text and pointers at both ends.",
                "loop": "While the pointers haven't met.",
                "skip": "A non-letter stays where it is; step past it on that side only.",
                "swap": "Both are letters: exchange them, then move both pointers inward.",
                "ret": "The text with its letters reversed.",
            },
        },
    },
    "takeaways": [
        """
        - **Reverse a filtered subsequence in place:** two pointers that skip.
        - Same skeleton as the filtered palindrome check, with a swap instead of a compare.
        - **Pitfall:** skipping on both sides in one step.
        """
    ],
}


# ---------------------------------------------------------------- squares-in-order
vals = [-7, -3, -1, 2, 4, 6]
n = len(vals)
out, qrow, i, j = [0] * n, [], 0, n - 1
for k in range(n - 1, -1, -1):
    if abs(vals[i]) > abs(vals[j]):
        out[k] = vals[i] * vals[i]
        qrow.append((k, i, j, f"{vals[i]}² = {vals[i] ** 2}", f"{vals[j]}² = {vals[j] ** 2}", f"left wins: out[{k}] = {out[k]}"))
        i += 1
    else:
        out[k] = vals[j] * vals[j]
        qrow.append((k, i, j, f"{vals[i]}² = {vals[i] ** 2}", f"{vals[j]}² = {vals[j] ** 2}", f"right wins: out[{k}] = {out[k]}"))
        j -= 1
EXTRA["squares-in-order"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - All non-negative: the squares are already in order.
        - All negative: the squares come out in reverse order.
        - Zero and equal absolute values (`−3` and `3`) give equal squares; either can go first.
        """
    ],
    "think": [
        """
        **Where are the big squares?** Squaring folds the number line at 0: the square grows with the distance from 0.
        In a sorted array, the values farthest from 0 are at the two ends (very negative on the left, very positive on the
        right). So the **largest remaining square is always at one of the two ends**.

        **Fill from the back.** Compare the two ends, write the larger square into the last free slot of the output, and
        move that end inward.
        """,
        f"**Trace on `{vals}`:**",
        table(["slot", "i", "j", "left", "right", "decision"], *qrow),
        f"Result **`{out}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["Square every value and sort the squares. Correct, but it ignores that the input is already sorted."],
            "build": ["Square each value.", "Sort."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["The question asks for O(n). The sorted input already tells us where the largest squares are."],
            "lines": {"sort": "Square everything, then sort the squares."},
        },
        1: {
            "idea": [
                """
                Pointers at both ends and a write position at the end of the output. Each step writes the larger of the
                two end squares and moves that end inward.

                **Invariant.** The output slots after `k` hold the largest squares in increasing order, and every value
                between `i` and `j` has a square no larger than any of them.
                """
            ],
            "build": ["Output array of size `n`.", "Pointers at both ends.", "From the last slot down, take the larger end square."],
            "complexity": ["**Time O(n).** **Space O(1)** besides the output."],
            "lines": {
                "init": "The output and pointers at both ends.",
                "fill": "Fill slots from the last one down, because we always know the largest remaining square.",
                "pick": "The end with the larger absolute value has the larger square; write it and move that end inward.",
                "ret": "The squares in increasing order.",
            },
        },
    },
    "takeaways": [
        """
        - **Sorted input, transformed values:** find where the extremes of the new values are (here, both ends).
        - Fill the output from the side whose extreme you know.
        - **Pitfall:** filling from the front, where the smallest square could be anywhere in the middle.
        """
    ],
}
