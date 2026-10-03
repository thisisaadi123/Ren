"""In-depth text for the in-place index-marking problems (merged into their sol() calls via sol.EXTRA)."""
from functools import reduce

from sol import EXTRA, table

MARKING = """
**The array as its own checklist.** When the values are numbers `1 … n` and the array has `n` slots, slot `v − 1` can
serve as the checkbox for value `v`. To tick it, change slot `v − 1` in a way that is **reversible** and that doesn't
destroy the value stored there:

- **Flip its sign** (values are positive, so the original is `|x|`);
- **Add `n`** (the original is `(x − 1) mod n + 1`, and the number of additions counts how often `v` appeared).

Reading a slot's value always uses the decoding (`abs`, or the `mod`), so earlier ticks never confuse later reads.
That's O(n) time with O(1) extra space, and a final pass can restore the input.
"""


def show(a):
    return " ".join(map(str, a))


# ---------------------------------------------------------------- unclaimed-numbers
tk = [3, 1, 3, 6, 1, 2]
a, urows = tk[:], []
for x in tk:
    v = abs(x)
    a[v - 1] = -abs(a[v - 1])
    urows.append((v, v - 1, show(a)))
unclaimed = [i + 1 for i, x in enumerate(a) if x > 0]
EXTRA["unclaimed-numbers"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Every number present: return an empty list.
        - The same number many times: its slot is negative after the first tick and stays negative.
        - The answer must be in increasing order, which a left-to-right read gives for free.
        """
    ],
    "think": [
        MARKING,
        f"**Ticking for `{tk}`** (each value `v` makes slot `v − 1` negative):",
        table(["value read (|x|)", "slot ticked", "array after"], *urows),
        f"Slots still positive: indices {[i for i, x in enumerate(a) if x > 0]}, so the unclaimed numbers are **{unclaimed}**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each number `1 … n`, scan the tickets for it; collect the ones not found."],
            "build": ["For each candidate number, linear search.", "Collect the missing ones."],
            "complexity": ["**Time O(n²).** **Space O(1)** besides the answer."],
            "limits": ["Each search rescans all tickets. One pass that records presence answers every number at once."],
            "lines": {"scan": "Every number from 1 to n that no ticket shows, found by searching the whole list.", "ret": "The unclaimed numbers in order."},
        },
        1: {
            "idea": ["Use a boolean array `seen[1 … n]`: one pass marks the numbers present, a second collects the unmarked ones."],
            "build": ["Flag array of size `n + 1`.", "Mark each ticket.", "Collect unmarked numbers."],
            "complexity": ["**Time O(n).** **Space O(n)** for the flags."],
            "limits": ["The flag array is extra memory, but the input already has exactly one slot per number."],
            "lines": {"flags": "Mark every number that appears on some ticket.", "read": "Numbers never marked, in increasing order."},
        },
        2: {
            "idea": [
                """
                For each ticket value `v = |x|`, make slot `v − 1` negative. Afterwards, every slot that is still positive
                belongs to a number nobody claimed. Restore the signs at the end.

                **Why reading `|x|` matters.** Slot `i` may already have been negated by an earlier ticket, but its
                original value is still `|x|`.
                """
            ],
            "build": ["Negate slot `|x| − 1` for each value.", "Collect `i + 1` for each positive slot.", "Restore the signs."],
            "complexity": ["**Time O(n):** three passes. **Space O(1)** besides the answer."],
            "lines": {
                "mark": "Tick number `|x|` by making its slot negative; `-abs(...)` keeps an already-ticked slot negative.",
                "read": "A slot that is still positive was never ticked: its number `i + 1` is unclaimed.",
                "restore": "Undo the marks so the caller's list is unchanged.",
                "ret": "The unclaimed numbers in increasing order.",
            },
        },
    },
    "takeaways": [
        """
        - **Values `1 … n` in an array of size `n`:** use slot `v − 1` as `v`'s marker.
        - Mark reversibly (sign) and always decode with `abs` when reading.
        - **Pitfall:** `tickets[v − 1] *= −1`, which un-ticks a slot ticked twice.
        """
    ],
}


# ---------------------------------------------------------------- double-booked
bk = [5, 1, 4, 5, 2, 1, 7]
n = len(bk)
b, drows = bk[:], []
for i in range(n):
    v = (b[i] - 1) % n + 1
    b[v - 1] += n
    drows.append((i, v, v - 1, show(b)))
twice = [i + 1 for i in range(n) if b[i] > 2 * n]
EXTRA["double-booked"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No room booked twice: return an empty list.
        - Each room appears at most twice, so counts are 0, 1 or 2.
        - The answer must be in increasing order.
        """
    ],
    "think": [
        MARKING,
        f"""
        **Counting in place by adding `n`.** For each booking, decode the room `v = (x − 1) mod n + 1` (the original
        value, even if `n` has been added to this slot), then add `n` to slot `v − 1`. Each slot ends at
        `original + n · (times its room was booked)`. A room booked twice has gained `2n`, so its slot exceeds `2n`.
        For `{bk}` (n = {n}):
        """,
        table(["i", "room decoded", "slot gets +n", "array after"], *drows),
        f"Slots above {2 * n}: rooms **{twice}**. Decoding each slot with `(x − 1) mod n + 1` restores the input.",
    ],
    "approaches": {
        0: {
            "idea": ["For each room `1 … n`, count its bookings by scanning; keep rooms with count 2."],
            "build": ["For each room, count by scanning.", "Keep count-2 rooms."],
            "complexity": ["**Time O(n²).** **Space O(1)** besides the answer."],
            "limits": ["Each count rescans the list. One pass can count every room at once."],
            "lines": {"scan": "Rooms whose count, found by scanning the whole list, is exactly 2.", "ret": "Those rooms in order."},
        },
        1: {
            "idea": ["Count bookings per room in an array of size `n + 1`, then list rooms with count 2."],
            "build": ["Count array.", "Tally.", "Read count-2 rooms."],
            "complexity": ["**Time O(n).** **Space O(n)** for the counts."],
            "limits": ["Extra O(n) memory, while the input itself has one slot per room."],
            "lines": {"tally": "One pass counts every room's bookings.", "read": "Rooms booked exactly twice, in increasing order."},
        },
        2: {
            "idea": [
                """
                Read rooms with `|x|`. If slot `v − 1` is already negative, room `v` was seen before: it's double-booked.
                Otherwise negate it. Restore the signs and sort the answer (rooms are found in input order).
                """
            ],
            "build": ["For each booking, check the sign of its room's slot.", "Negative → second booking; positive → negate.", "Restore and sort."],
            "complexity": ["**Time O(n log n)** because the answer is sorted (the marking itself is O(n)). **Space O(1)** besides the answer."],
            "limits": ["Rooms are discovered in input order, so the answer needs a sort. Counting by adding `n` lets a final left-to-right read produce them already sorted."],
            "lines": {
                "loop": "Each booking once.",
                "read": "The room number, ignoring any sign added by a mark.",
                "seen": "Its slot is already negative: this is the room's second booking.",
                "mark": "First booking of this room: tick its slot by negating it.",
                "restore": "Undo all marks.",
                "ret": "The double-booked rooms, sorted.",
            },
        },
        3: {
            "idea": [
                """
                Add `n` to slot `v − 1` for each booking (decoding `v` with `(x − 1) mod n + 1`). Then a left-to-right pass
                reports every slot above `2n` and restores each value with the same decoding.

                **Why `> 2n` means twice.** A slot starts between 1 and `n`; after `k` additions it lies in
                `(k·n, (k + 1)·n]`. Only `k = 2` puts it above `2n`.
                """
            ],
            "build": ["Add `n` per booking.", "Read slots above `2n` in index order.", "Restore every slot."],
            "complexity": ["**Time O(n).** **Space O(1)** besides the answer. Values reach at most `3n`, so there's no overflow."],
            "lines": {
                "add": "Decode the room even if this slot has already been increased, then count the booking in its room's slot.",
                "read": "A slot that gained `2n` belongs to a room booked twice; reading by index gives increasing order.",
                "restore": "Decoding with `(x − 1) mod n + 1` removes the added multiples of `n`.",
                "ret": "The double-booked rooms, already sorted.",
            },
        },
    },
    "takeaways": [
        """
        - **Count in place:** add `n` per occurrence; decode with `(x − 1) mod n + 1`.
        - Sign marks record "seen"; additions record "how many".
        - **Pitfall:** reading a slot without decoding it after it has been marked.
        """
    ],
}


# ---------------------------------------------------------------- first-missing-ticket
fm = [5, 3, -2, 1, 9, 2]
m = len(fm)
c = [x if 1 <= x <= m else m + 1 for x in fm]
cleaned = c[:]
frows = []
for i in range(m):
    v = abs(c[i])
    if v <= m:
        c[v - 1] = -abs(c[v - 1])
        frows.append((i, v, f"tick slot {v - 1}", show(c)))
    else:
        frows.append((i, v, "out of range: ignore", show(c)))
first = next((i + 1 for i, x in enumerate(c) if x > 0), m + 1)
EXTRA["first-missing-ticket"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - All of `1 … n` present: the answer is `n + 1`.
        - Only junk (zeros, negatives, huge values): the answer is 1.
        - Values span the full 32-bit range, so negating an arbitrary value could overflow; clean them first.
        """
    ],
    "think": [
        f"""
        **The answer is at most `n + 1`.** With `n` numbers, the best case is that they're exactly `1 … n`, making the
        answer `n + 1`. Anything missing from `1 … n` makes the answer smaller. So only values in `1 … n` matter, and
        everything else is junk.
        """,
        MARKING,
        f"""
        **Clean, then mark.** First replace every junk value (≤ 0 or > n) with `n + 1`, a positive value that will be
        ignored. Now all values are positive, so signs are free to use as marks. For `{fm}` (n = {m}) the cleaned array
        is `{cleaned}`:
        """,
        table(["i", "|value|", "action", "array after"], *frows),
        f"The first slot still positive is index {first - 1}, so the answer is **{first}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Try 1, 2, 3, … and scan the whole array for each, stopping at the first number not found."],
            "build": ["`k = 1`.", "While `k` is in the array, `k += 1`."],
            "complexity": ["**Time O(n²):** up to `n + 1` scans of `n`. **Space O(1).**"],
            "limits": ["Every candidate rescans the array. One pass can record which of `1 … n + 1` are present."],
            "lines": {"init": "The first candidate.", "scan": "Each candidate is searched for in the whole array.", "ret": "The first candidate not present."},
        },
        1: {
            "idea": ["Flags for `1 … n + 1`: mark each value in range, then find the first unmarked number."],
            "build": ["Flags of size `n + 2`.", "Mark values in range.", "First unmarked."],
            "complexity": ["**Time O(n).** **Space O(n)**, which the problem forbids."],
            "limits": ["Uses O(n) extra space. The input array's own slots can hold the marks."],
            "lines": {"flags": "Room for 1 … n + 1.", "mark": "Only values in range can affect the answer.", "find": "The first unmarked number (at most n + 1)."},
        },
        2: {
            "idea": [
                """
                Cyclic sort: swap each value `v` in `1 … n` into slot `v − 1` until every slot holds its own number or
                junk. Then the first slot `i` without `i + 1` gives the answer.

                **Why it's O(n).** Every swap puts at least one value into its final slot, and a value in its final slot
                is never moved again, so there are at most `n` swaps in total.
                """
            ],
            "build": ["For each slot, swap its value into place while possible.", "Find the first slot without its own number."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Correct and O(1) space, but it rearranges the input heavily. Sign marks record the same information with simple writes."],
            "lines": {
                "place": "Visit every slot.",
                "swap": "While this slot holds a value in range that isn't already in its home slot, swap it home. The duplicate check stops endless swapping between equal values.",
                "find": "The first slot that doesn't hold its own number.",
                "full": "Every slot holds its number: the answer is `n + 1`.",
            },
        },
        3: {
            "idea": [
                """
                Replace junk with `n + 1`. For each value `v = |x| ≤ n`, make slot `v − 1` negative. The first slot that
                stays positive is the answer's index; if none, the answer is `n + 1`.

                **Why cleaning first matters.** It makes every value positive, so a negative sign can only mean "ticked",
                and it removes values like −2³¹ whose negation would overflow.
                """
            ],
            "build": ["Replace junk with `n + 1`.", "Negate slot `|x| − 1` for in-range values.", "First positive slot → answer."],
            "complexity": ["**Time O(n):** three passes. **Space O(1).**"],
            "lines": {
                "clean": "Junk can't affect the answer; `n + 1` is positive and out of range, so it will simply be ignored.",
                "mark": "Tick each present number's slot; `abs` decodes values whose slots were already ticked.",
                "find": "The first unticked slot `i` means `i + 1` never appeared.",
                "full": "Every number `1 … n` is present.",
            },
        },
    },
    "takeaways": [
        """
        - **Smallest missing positive:** the answer is in `1 … n + 1`, so index marking applies.
        - Clean out-of-range values first so signs can be used as marks.
        - **Pitfall:** negating raw input values (overflow at −2³¹, and existing negatives look "ticked").
        """
    ],
}


# ---------------------------------------------------------------- missing-seat
st = [3, 0, 1, 5, 2]
ns = len(st)
full = ns * (ns + 1) // 2
xrows, x = [], ns
for i, s in enumerate(st):
    x ^= i ^ s
    xrows.append((i, s, f"{x:03b} ({x})"))
EXTRA["missing-seat"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The free seat may be 0 or `n`.
        - Exactly one seat is free; all taken seats are distinct.
        - The sum `n(n + 1)/2` reaches 5 × 10⁹ for `n = 10⁵`, past 32 bits.
        """
    ],
    "think": [
        f"""
        **Two cancellation tricks.** The full set of seats `0 … n` is known; the input is that set minus one seat.

        - **Sum:** `0 + 1 + … + n = n(n + 1)/2`. Subtract the taken seats and the free one is left: for `{st}`,
          `{full} − {sum(st)} = {full - sum(st)}`.
        - **XOR:** `x ^ x = 0` and order doesn't matter. XOR all of `0 … n` with all taken seats: every taken seat
          appears twice and cancels, leaving the free seat. No overflow risk at all.
        """,
        f"**XOR trace** (start with `n = {ns}`, then XOR each index `i` and seat):",
        table(["i", "seat", "running XOR"], *xrows),
        f"Result: **{x}**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each seat `0 … n`, scan the list for it; return the first one not found."],
            "build": ["For each seat number, search the list."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Each search rescans the list. A flag array, a sum or an XOR finds the gap in one pass."],
            "lines": {"each": "Every seat number from 0 to n.", "scan": "The first seat not in the list is free.", "none": "Unreachable: exactly one seat is free."},
        },
        1: {
            "idea": ["Flag taken seats in a boolean array of size `n + 1`; the unflagged index is the answer."],
            "build": ["Flag array.", "Mark taken seats.", "Find the unflagged one."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
            "limits": ["Extra O(n) memory; arithmetic finds the answer with none."],
            "lines": {"flags": "Mark every taken seat.", "find": "The one seat never marked."},
        },
        2: {
            "idea": ["The full total `n(n + 1)/2` minus the sum of the taken seats is the free seat."],
            "build": ["Total of `0 … n`.", "Subtract the input's sum."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["The total needs 64 bits for large `n`; XOR avoids any overflow."],
            "lines": {"full": "Sum of all seats `0 … n` (64-bit).", "diff": "Removing every taken seat leaves the free one."},
        },
        3: {
            "idea": [
                """
                Start with `x = n`, then XOR in every index `i` and every seat. Indices `0 … n − 1` plus the starting `n`
                cover all of `0 … n`; every taken seat appears once among them and once among the seats, so it cancels.
                The free seat appears only once and survives.
                """
            ],
            "build": ["`x = n`.", "XOR each index and each seat.", "Return `x`."],
            "complexity": ["**Time O(n).** **Space O(1)**, and no overflow."],
            "lines": {
                "init": "Include `n`, the one seat number that isn't also an index.",
                "loop": "XOR in index `i` (one of `0 … n − 1`) and seat `s`; equal numbers cancel.",
                "ret": "Only the free seat appears an odd number of times.",
            },
        },
    },
    "takeaways": [
        """
        - **One missing number from a known range:** sum difference or XOR.
        - XOR cancels pairs with no overflow risk.
        - **Pitfall:** 32-bit overflow in `n(n + 1)/2`.
        """
    ],
}
