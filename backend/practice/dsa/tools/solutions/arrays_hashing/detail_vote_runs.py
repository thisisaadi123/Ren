"""In-depth text for majority-vote and consecutive-run problems (merged into their sol() calls via sol.EXTRA)."""
from collections import Counter

from sol import EXTRA, table

CANCEL = """
**Cancelling different votes.** Remove a group of votes that are all for **different** options, and any option that
had more than its share before still has more than its share after:

- With groups of **2** (one vote each for two different options), an option with more than `n/2` votes can't be wiped
  out: each of its votes needs a different partner, and there aren't enough.
- With groups of **3**, the same argument works for options with more than `n/3` votes, and at most **two** options can
  have that many.

Boyer–Moore voting performs this cancellation in one pass with a few counters. The survivors are only *candidates*:
when a winner isn't guaranteed, a second pass must count their real votes.
"""


def vote_rows(v):
    rows, cand, c = [], None, 0
    for x in v:
        note = ""
        if c == 0:
            cand, note = x, "count 0: new candidate. "
        c += 1 if x == cand else -1
        rows.append((x, cand, c, note + ("+1" if x == cand else "−1")))
    return rows, cand


# ---------------------------------------------------------------- half-or-more
win, lose = [4, 9, 4, 4, 2, 4, 9], [6, 1, 6, 2, 6, 3]
wr, wc = vote_rows(win)
lr, lc = vote_rows(lose)
EXTRA["half-or-more"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Exactly half is **not** a win: `[6, 1, 6, 2, 6, 3]` has no winner.
        - One vote: it wins.
        - Voting always produces a candidate, even when nobody wins, so the verification pass is essential.
        """
    ],
    "think": [
        CANCEL,
        f"**Voting on `{win}`:**",
        table(["vote", "candidate", "count", "change"], *wr),
        f"Candidate {wc}, which really has {win.count(wc)} of {len(win)} votes: a winner.",
        f"**Voting on `{lose}`:**",
        table(["vote", "candidate", "count", "change"], *lr),
        f"Candidate {lc}, but it has only {lose.count(lc)} of {len(lose)} votes, so the answer is **−1**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each vote, count its option by scanning all votes; return the first option with more than half."],
            "build": ["For each vote, count by scanning.", "Return the first majority, else −1."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Recounts the same options repeatedly. A hash map counts all options in one pass."],
        },
        1: {
            "idea": ["Count options in a hash map; return as soon as one passes `n/2`, or −1 at the end."],
            "build": ["Map option → votes.", "Return when a count exceeds half."],
            "complexity": ["**Time O(n)** expected. **Space O(n)** for the map."],
            "limits": ["Uses O(n) memory. Voting plus a verification pass needs O(1)."],
        },
        2: {
            "idea": [
                """
                Pass 1: Boyer–Moore voting gives a candidate (the only option that *could* have a majority). Pass 2:
                count the candidate's votes and return it only if it has more than half.

                **Why the candidate is the only possibility.** If a majority option exists, cancellation can't remove all
                of its votes, so it's the survivor.
                """
            ],
            "build": ["Vote to get a candidate.", "Count the candidate's real votes.", "Return it if it's a strict majority, else −1."],
            "complexity": ["**Time O(n):** two passes. **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Majority not guaranteed:** vote, then verify with a second pass.
        - Voting never proves a winner exists; it only narrows it to one candidate.
        - **Pitfall:** `≥ n/2` instead of `> n/2`.
        """
    ],
}


# ---------------------------------------------------------------- strong-candidates
sv = [3, 8, 3, 5, 8, 3, 8, 1, 3, 8]
a = b = None
ca = cb = 0
srows = []
for x in sv:
    if x == a:
        ca += 1
        act = f"matches A: A count {ca}"
    elif x == b:
        cb += 1
        act = f"matches B: B count {cb}"
    elif ca == 0:
        a, ca = x, 1
        act = "A slot free: A = this vote"
    elif cb == 0:
        b, cb = x, 1
        act = "B slot free: B = this vote"
    else:
        ca -= 1
        cb -= 1
        act = "third different option: cancel one of each"
    srows.append((x, f"{a} ({ca})", f"{b} ({cb})", act))
counts = Counter(sv)
strong = sorted(c for c in {a, b} if c is not None and counts[c] > len(sv) // 3)
EXTRA["strong-candidates"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - At most two options can be strong (three would need more than all the votes).
        - The answer may be empty, one option, or two.
        - Strict inequality: more than `⌊n/3⌋` votes.
        """
    ],
    "think": [
        CANCEL,
        f"**Two-candidate voting on `{sv}`** (n = {len(sv)}, threshold > {len(sv) // 3}):",
        table(["vote", "candidate A (count)", "candidate B (count)", "what happens"], *srows),
        f"""
        Candidates {a} and {b}; their real counts are {counts[a]} and {counts[b]}, so the strong options are **{strong}**.

        **Why a strong option always survives.** Each cancellation removes three votes for three different options, so an
        option loses at most one vote per cancellation, and since every cancellation uses up three votes there are at most
        `n/3` of them. An option with more than `n/3` votes therefore keeps at least one uncancelled vote, which means it
        sits in one of the two slots at the end.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For each distinct option, count its votes by scanning; keep those above `⌊n/3⌋`, then sort."],
            "build": ["Skip options already handled.", "Count by scanning.", "Keep strong ones; sort."],
            "complexity": ["**Time O(n²).** **Space O(1)** besides the answer."],
            "limits": ["Each option is counted with a full scan. A hash map counts everything in one pass."],
        },
        1: {
            "idea": ["Count all options in a hash map and keep those with more than `⌊n/3⌋` votes, sorted."],
            "build": ["Count with a map.", "Filter by the threshold.", "Sort."],
            "complexity": ["**Time O(n)** expected. **Space O(n).**"],
            "limits": ["O(n) memory for the map, although at most two options can qualify."],
        },
        2: {
            "idea": [
                """
                Keep two candidate slots with counts. A vote for a candidate increases its count; a vote that fits an empty
                slot fills it; any other vote cancels one vote from each candidate. Finally count the two candidates'
                real votes and keep those above `⌊n/3⌋`.

                **Why verification is needed.** The slots hold whatever survived cancellation, which might not be strong
                (e.g. when no option is).
                """
            ],
            "build": ["Two empty slots.", "Match, fill, or cancel for each vote.", "Count the two candidates and keep the strong ones, sorted."],
            "complexity": ["**Time O(n):** two passes. **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **More than n/k votes:** at most `k − 1` options qualify; keep `k − 1` candidate slots and cancel groups of `k`.
        - Always verify candidates when existence isn't guaranteed.
        - **Pitfall:** checking a vote against an empty slot's stale value before the "matches" checks.
        """
    ],
}


# ---------------------------------------------------------------- is-it-a-straight
hand = [9, 6, 8, 5, 7]
bad_dup, bad_gap = [5, 6, 6, 8], [5, 6, 8, 9]


def straight(c):
    lo, hi = min(c), max(c)
    return hi - lo == len(c) - 1 and len(set(c)) == len(c)


EXTRA["is-it-a-straight"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One card is always a straight.
        - Duplicates break a straight even when the span is right (`5, 6, 6, 8`).
        - Values span ±10⁹, so `max − min` can reach 2 × 10⁹.
        """
    ],
    "think": [
        f"""
        **The straight is forced.** Once the smallest card `lo` and the number of cards `n` are known, the straight must
        be exactly `lo, lo + 1, …, lo + n − 1`. So two conditions are equivalent to being a straight:

        1. the span is right: `max − min = n − 1`;
        2. no card repeats.

        If both hold, the `n` distinct cards fit into `n` slots of the span, so every slot is filled exactly once.
        """,
        table(["hand", "min", "max", "max − min", "n − 1", "duplicates?", "straight?"],
              *[(h, min(h), max(h), max(h) - min(h), len(h) - 1, "yes" if len(set(h)) < len(h) else "no", "yes" if straight(h) else "no") for h in (hand, bad_dup, bad_gap)]),
        """
        **Checking duplicates without a hash set.** Once the span is exactly `n − 1`, every card `c` maps to slot
        `c − min` in `0 … n − 1`, so a boolean array of size `n` detects repeats.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Find the smallest card, then search the hand for each of `min + 1, …, min + n − 1`."],
            "build": ["Minimum.", "Search for each required card.", "True if all are found."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Each required card is a linear search. Sorting, or checking the span with slot marks, avoids that."],
        },
        1: {
            "idea": ["Sort the hand; it's a straight exactly when every neighbour difference is 1."],
            "build": ["Sort.", "Check each neighbour difference."],
            "complexity": ["**Time O(n log n).** **Space O(n)** for the copy."],
            "limits": ["Sorting is more than needed: the straight is fully determined by its minimum and length."],
        },
        2: {
            "idea": [
                """
                Compute `min` and `max`. If `max − min ≠ n − 1`, return false. Otherwise mark slot `c − min` for each card;
                a slot marked twice means a duplicate. If no duplicate appears, it's a straight.
                """
            ],
            "build": ["Min and max.", "Check the span.", "Mark slots; reject a repeat."],
            "complexity": ["**Time O(n).** **Space O(n)** for the slot marks."],
        },
    },
    "takeaways": [
        """
        - **"Can it be rearranged into consecutive values?"** ⇔ span `= n − 1` and no duplicates.
        - A known span turns values into slots for O(1) duplicate checks.
        - **Pitfall:** checking only the span (misses duplicates).
        """
    ],
}


# ---------------------------------------------------------------- longest-chain-with-step
vals, step = [10, 4, 1, 7, 5, 13, 8, 2, 20, 23], 3
have = set(vals)
crows = []
for v in sorted(have):
    if v - step in have:
        crows.append((v, f"{v - step} is present: not a head", "—"))
        continue
    chain, x = [v], v
    while x + step in have:
        x += step
        chain.append(x)
    crows.append((v, "head: walk " + " → ".join(map(str, chain)), len(chain)))
best = max(r[2] for r in crows if r[2] != "—")
EXTRA["longest-chain-with-step"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Duplicates can't be used twice in a chain.
        - Negative values are fine.
        - Every value alone is a chain of length 1, so the answer is at least 1.
        """
    ],
    "think": [
        f"""
        **Each value belongs to one maximal chain.** A value's next link must be `v + step` and its previous link
        `v − step`, so the values split into disjoint maximal chains. The **head** of a chain is a value whose
        `v − step` is absent. Walking forward only from heads visits every value exactly once. For `{vals}`,
        `step = {step}`:
        """,
        table(["value (distinct)", "decision", "chain length"], *crows),
        f"Longest chain **{best}**.",
    ],
    "approaches": {
        0: {
            "idea": ["From every value, walk `v + step, v + 2·step, …` while present, searching the list each time."],
            "build": ["For each value, extend while the next link is in the list.", "Track the longest."],
            "complexity": ["**Time O(n³)** worst case: walks of length O(n), each step a linear search. **Space O(1).**"],
            "limits": ["Linear searches, and every member of a chain walks it again."],
        },
        1: {
            "idea": [
                """
                Sort the distinct values. For each value `v` (in increasing order), binary-search `v − step` among the
                smaller values; if found, `v`'s chain length is that value's length plus one. The longest length wins.
                """
            ],
            "build": ["Sorted distinct values.", "Binary-search each value's predecessor.", "Extend its chain length."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["O(n log n) for the sort and searches; a hash set gives O(1) membership."],
        },
        2: {
            "idea": [
                """
                Put the values in a set. For each value that is a chain head (`v − step` absent), walk forward while
                `x + step` is present, counting the length.

                **Why it's O(n).** Chains are disjoint and each is walked only from its head.
                """
            ],
            "build": ["Hash set.", "Skip non-heads.", "Walk forward from each head."],
            "complexity": ["**Time O(n)** expected. **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Longest arithmetic chain with a fixed step:** hash set, walk only from heads.
        - Same idea as the longest consecutive run (step 1).
        - **Pitfall:** walking from every value (quadratic on one long chain).
        """
    ],
}
