"""In-depth text for next-permutation and rotate/reverse problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

NEXT = """
**The next arrangement, step by step.** To get the next larger arrangement, change as little as possible, as far to
the right as possible.

1. **Find the pivot.** Scan from the right while values don't increase (`a[i] ≥ a[i+1]`). That tail is already the
   *largest* arrangement of its values, so nothing inside it can grow. The pivot is the first index `i` from the right
   with `a[i] < a[i+1]`; if there is none, the whole sequence is the last arrangement.
2. **Swap.** Replace `a[i]` with the smallest tail value that's larger than it. Because the tail is non-increasing,
   that's the **rightmost** tail value greater than `a[i]`.
3. **Reverse the tail.** After the swap the tail is still non-increasing; reversing it makes it non-decreasing, its
   *smallest* arrangement, so the result is the very next one.

All three steps are linear, so the whole thing is O(n) with O(1) extra space. Duplicates are handled by the `≥`/`≤`
comparisons, which skip equal values.
"""


def next_perm(a):
    a = list(a)
    i = len(a) - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i < 0:
        return None, None, None, a[::-1]
    j = len(a) - 1
    while a[j] <= a[i]:
        j -= 1
    a[i], a[j] = a[j], a[i]
    swapped = a[:]
    a[i + 1:] = reversed(a[i + 1:])
    return i, j, swapped, a


def steps_table(src, label="values"):
    i, j, swapped, res = next_perm(src)
    if i is None:
        return table(["step", label], ("input", src), ("no pivot: last arrangement", "—"), ("wrap to ascending", res)), res
    return table(["step", label],
                 ("input", " ".join(map(str, src))),
                 (f"pivot at index {i} (value {src[i]}); tail {src[i + 1:]} is non-increasing", "—"),
                 (f"swap with index {j} (value {src[j]}), the rightmost tail value > {src[i]}", " ".join(map(str, swapped))),
                 (f"reverse the tail after index {i}", " ".join(map(str, res)))), res


# ---------------------------------------------------------------- next-arrangement
na = [1, 5, 8, 4, 7, 6, 5, 3, 1]
na_tab, na_res = steps_table(na)
EXTRA["next-arrangement"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Fully descending (the last arrangement): wrap to fully ascending.
        - Repeated values: equal values must not be swapped with each other.
        - One element: unchanged.
        """
    ],
    "think": [
        NEXT,
        f"**On `{na}`:**",
        na_tab,
        f"Next arrangement: **{na_res}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Generate arrangements of the values in dictionary order (smallest value first at each position) and return the first one larger than the input; if none, return the sorted values."],
            "build": ["Count the values.", "Depth-first generation in increasing order.", "Stop at the first arrangement larger than the input."],
            "complexity": ["**Time O(n! · n)** in the worst case. **Space O(n)** for the recursion."],
            "limits": ["Only usable for a handful of values (the checker runs it on tiny inputs). The pivot-swap-reverse rule jumps straight to the answer."],
        },
        1: {
            "idea": [
                """
                Pivot, swap, reverse, as above. If there's no pivot, reversing the whole array gives the ascending order,
                which is exactly the wrap-around.
                """
            ],
            "build": ["Find the pivot from the right.", "If found, swap with the rightmost larger tail value.", "Reverse everything after the pivot (the whole array if none)."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Next permutation:** rightmost ascent, swap with the rightmost larger value, reverse the tail.
        - The tail after the pivot is non-increasing, which is why "rightmost larger" is the smallest larger.
        - **Pitfall:** `>` instead of `≥` when finding the pivot (breaks with duplicates).
        """
    ],
}


# ---------------------------------------------------------------- next-badge-number
nb = list("158476531")
nb_tab, nb_res = steps_table(nb, "digits")
EXTRA["next-badge-number"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Digits in non-increasing order (like `"9531"`): no larger number exists, return `""`.
        - Repeated digits: `"115"` → `"151"`.
        - Up to 10⁵ digits, far beyond any integer type, so work on the string.
        """
    ],
    "think": [
        NEXT,
        f"**On `\"{''.join(nb)}\"`:**",
        nb_tab,
        f"Next badge: **`{''.join(nb_res)}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["Generate digit arrangements in increasing order and return the first one larger than `code`."],
            "build": ["Count digits.", "Generate arrangements smallest first.", "Return the first larger one, or `\"\"`."],
            "complexity": ["**Time O(n! · n)** in the worst case. **Space O(n).**"],
            "limits": ["Factorial; only for tiny inputs."],
        },
        1: {
            "idea": ["Find the pivot, swap it with the smallest larger digit in the tail, then **sort** the tail ascending."],
            "build": ["Pivot.", "Smallest larger tail digit.", "Swap and sort the tail."],
            "complexity": ["**Time O(n log n)** for the sort. **Space O(n).**"],
            "limits": ["The tail is already non-increasing after the swap, so sorting it is just a reversal: O(n) instead of O(n log n)."],
        },
        2: {
            "idea": ["Pivot, swap with the rightmost larger tail digit, reverse the tail. If there's no pivot, return `\"\"`."],
            "build": ["Pivot from the right; none → `\"\"`.", "Swap with the rightmost larger digit.", "Reverse the tail."],
            "complexity": ["**Time O(n).** **Space O(n)** for the digit list."],
        },
    },
    "takeaways": [
        """
        - **Next larger number with the same digits = next permutation of the digit string.**
        - Sorting the tail works but reversing it is enough.
        - **Pitfall:** converting to an integer (overflow) instead of working on digits.
        """
    ],
}


# ---------------------------------------------------------------- next-mirror-number
nm = "1323231"
half = list(nm[:len(nm) // 2])
hm_tab, hm_res = steps_table(half, "left half")
mirror = "".join(hm_res) + nm[len(nm) // 2:(len(nm) + 1) // 2] + "".join(hm_res)[::-1]
EXTRA["next-mirror-number"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Odd length: the middle digit (the one with an odd count) is fixed.
        - A left half in non-increasing order: no larger mirror number, return `""`.
        - One or two digits: the left half is too short to change, so `""`.
        """
    ],
    "think": [
        f"""
        **A mirror number is decided by its left half.** The right half is the left half reversed, and with an odd
        length the middle digit is forced (it's the digit with an odd count). Comparing two mirror numbers of the same
        digits compares their left halves first, so the next larger mirror number has the **next larger left half**. That
        is the next permutation of the left half.

        `"{nm}"`: left half `{''.join(half)}`, middle `{nm[len(nm) // 2:(len(nm) + 1) // 2] or '(none)'}`.
        """,
        NEXT,
        "**Next permutation of the left half:**",
        hm_tab,
        f"Mirror it back: **`{mirror}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["Generate arrangements of the left half's digits in increasing order; take the first one larger than the current left half and mirror it."],
            "build": ["Left half's digit counts.", "Generate arrangements in order.", "Mirror the first larger one."],
            "complexity": ["**Time O(h! · h)** for a half of length `h`. **Space O(h).**"],
            "limits": ["Factorial; only for tiny inputs. Next permutation of the half is linear."],
        },
        1: {
            "idea": [
                """
                Take the left half, apply next permutation (no pivot → `""`), and build left + middle + reversed left.

                **Why it's the smallest larger mirror.** Any larger mirror number made of these digits has a left half
                larger than the current one, and the next permutation is the smallest such half.
                """
            ],
            "build": ["Left half.", "Next permutation (or `\"\"`).", "Mirror with the middle digit."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Palindromes are determined by their first half**; operate on the half, then mirror.
        - The middle digit of an odd-length palindrome never moves.
        - **Pitfall:** permuting the whole string, which breaks the mirror property.
        """
    ],
}


# ---------------------------------------------------------------- one-step-back
sb = [1, 5, 8, 4, 1, 3, 5, 6, 7]


def prev_perm(a):
    a = list(a)
    i = len(a) - 2
    while i >= 0 and a[i] <= a[i + 1]:
        i -= 1
    if i < 0:
        return None, None, None, a[::-1]
    j = len(a) - 1
    while a[j] >= a[i]:
        j -= 1
    a[i], a[j] = a[j], a[i]
    swapped = a[:]
    a[i + 1:] = a[i + 1:][::-1]
    return i, j, swapped, a


pi_, pj, psw, pres = prev_perm(sb)
EXTRA["one-step-back"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Fully ascending (the first ordering): wrap to fully descending.
        - Repeated ratings: equal values must not count as a change.
        - One rating: unchanged.
        """
    ],
    "think": [
        """
        **The mirror image of "next".** To step back by the smallest amount, change as far right as possible:

        1. **Pivot:** from the right, the tail with `a[i] ≤ a[i+1]` (non-decreasing) is already the *smallest*
           arrangement of its values. The pivot is the first index from the right with `a[i] > a[i+1]`.
        2. **Swap** `a[i]` with the **largest tail value smaller than it**, which is the rightmost tail value `< a[i]`
           (the tail is non-decreasing).
        3. **Reverse the tail** so it becomes non-increasing: its *largest* arrangement, giving the ordering immediately
           before.
        """,
        f"**On `{sb}`:**",
        table(["step", "ratings"],
              ("input", " ".join(map(str, sb))),
              (f"pivot at index {pi_} (value {sb[pi_]}); tail {sb[pi_ + 1:]} is non-decreasing", "—"),
              (f"swap with index {pj} (value {sb[pj]}), the rightmost tail value < {sb[pi_]}", " ".join(map(str, psw))),
              (f"reverse the tail after index {pi_}", " ".join(map(str, pres)))),
        f"Previous ordering: **{pres}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Generate orderings from largest to smallest and return the first one smaller than the input; if none, return the descending order."],
            "build": ["Count ratings.", "Generate orderings largest first.", "Return the first smaller one (or wrap)."],
            "complexity": ["**Time O(n! · n)** in the worst case. **Space O(n).**"],
            "limits": ["Factorial; only for tiny inputs."],
        },
        1: {
            "idea": ["Pivot (rightmost descent), swap with the rightmost smaller tail value, reverse the tail; with no pivot, return the reversed (descending) ratings."],
            "build": ["Copy.", "Pivot from the right; none → reverse everything.", "Swap and reverse the tail."],
            "complexity": ["**Time O(n).** **Space O(n)** for the copy."],
        },
    },
    "takeaways": [
        """
        - **Previous permutation = next permutation with every comparison flipped.**
        - Rightmost descent, swap with the largest smaller value, reverse the tail.
        - **Pitfall:** swapping with the first smaller value from the left (not the largest smaller).
        """
    ],
}


# ---------------------------------------------------------------- rotate-the-carousel
rc, rk = [1, 2, 3, 4, 5, 6, 7], 3
r1 = rc[::-1]
r2 = r1[:rk][::-1] + r1[rk:]
r3 = r2[:rk] + r2[rk:][::-1]
EXTRA["rotate-the-carousel"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `k` larger than `n`: only `k mod n` matters (a full turn changes nothing).
        - `k mod n = 0`: unchanged.
        - One seat: unchanged.
        """
    ],
    "think": [
        f"""
        **Rotation = swapping two blocks.** Rotating right by `k` moves the last `k` seats to the front: the array is
        `A B` with `B` the last `k` seats, and the answer is `B A`.

        **Three reversals.** Reversing the whole array gives `reverse(B) reverse(A)`: the blocks are in the right order,
        but each is backwards. Reversing each block separately fixes that. For `{rc}`, `k = {rk}`:
        """,
        table(["step", "seats"], ("input (A = first n − k, B = last k)", rc), ("reverse everything", r1), (f"reverse the first {rk}", r2), (f"reverse the remaining {len(rc) - rk}", r3)),
    ],
    "approaches": {
        0: {
            "idea": ["Rotate by one step `k mod n` times: save the last seat, shift everything right by one, put it in front."],
            "build": ["Repeat `k mod n` times.", "Shift by one."],
            "complexity": ["**Time O(n · k):** up to 10¹⁰ moves. **Space O(1).**"],
            "limits": ["Every seat moves `k` times instead of once."],
        },
        1: {
            "idea": ["Copy each seat `i` to `out[(i + k) mod n]` in a new array."],
            "build": ["New array.", "Place each seat at its rotated position."],
            "complexity": ["**Time O(n).** **Space O(n)** for the copy."],
            "limits": ["Uses a second array; three reversals do it in place."],
        },
        2: {
            "idea": [
                """
                Reduce `k` modulo `n`, then reverse the whole array, reverse the first `k` seats, and reverse the rest.

                **Why it works.** Whole reversal: `A B → B' A'` (primes mean reversed). Reversing each block:
                `B' → B`, `A' → A`. Result `B A`.
                """
            ],
            "build": ["`k %= n`.", "Reverse all.", "Reverse `[0, k)` and `[k, n)`."],
            "complexity": ["**Time O(n):** each seat is swapped about twice. **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Rotate in place = three reversals.** Left rotation reverses the blocks in the other order.
        - Always reduce `k` modulo `n` first.
        - **Pitfall:** forgetting `k %= n` (out-of-range reversal for `k ≥ n`).
        """
    ],
}
