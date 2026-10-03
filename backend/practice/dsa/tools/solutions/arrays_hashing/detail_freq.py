"""In-depth text for the frequency-counting problems (merged into their sol() calls via sol.EXTRA)."""
from collections import Counter

from sol import EXTRA, table

COUNTING = """
**Counting is a lookup table.** Most "how many times" questions reduce to: walk the input once and keep a count per
value. The only design choice is the table:

- **A plain array** when the values are small and known in advance (26 letters, 128 characters, ids in a fixed range):
  index directly by the value.
- **A hash map (or hash set)** when values are large or unpredictable (up to 10⁹): expected O(1) per lookup.

Either way, one pass builds the counts in O(n), which is what replaces repeated scanning.
"""


# ---------------------------------------------------------------- duplicate-badges
badges = [12, 5, 9, 2, 5, 8]
seen, drows = [], []
for b in badges:
    if b in seen:
        drows.append((b, "{" + ", ".join(map(str, seen)) + "}", "already seen → true"))
        break
    drows.append((b, "{" + ", ".join(map(str, seen)) + "}", "new: add it"))
    seen.append(b)
EXTRA["duplicate-badges"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One badge: no duplicate.
        - The duplicate may be the very last element; the scan must reach it.
        - Negative numbers and huge values are fine for hashing and sorting, but rule out indexing an array directly.
        """
    ],
    "think": [
        """
        **Restating it.** Is there a pair of positions with equal values?

        **Three ways to answer "have I seen this before?"**

        1. Compare with everything earlier: O(n) per element, O(n²) total.
        2. Sort, so equal values become neighbours, and compare each element with the next: O(n log n).
        3. Keep a hash set of values seen: O(1) expected per element, O(n) total, and you can stop at the first repeat.
        """,
        f"**Hash-set trace on `{badges}`:**",
        table(["badge", "seen before it", "result"], *drows),
    ],
    "approaches": {
        0: {
            "idea": ["Compare every pair of positions `i < j`; any equal pair means a duplicate."],
            "build": ["Two nested loops over `i < j`.", "Return true on an equal pair."],
            "complexity": ["**Time O(n²):** 5 × 10⁹ comparisons for `n = 10⁵`. **Space O(1).**"],
            "limits": ["Each badge is compared with all others. Sorting brings equal values together; a hash set remembers what's been seen."],
            "lines": {
                "loops": "Every pair of different positions, each once.",
                "test": "Two equal badges: a duplicate exists.",
                "ret": "No pair was equal.",
            },
        },
        1: {
            "idea": [
                """
                Sort a copy. Equal values are then adjacent, so it's enough to compare each element with the next one.

                **Why neighbours are enough.** If `x` appears twice, all its copies form one consecutive block after
                sorting, and any block of size ≥ 2 contains an adjacent equal pair.
                """
            ],
            "build": ["Sort a copy.", "Compare each element with the next."],
            "complexity": ["**Time O(n log n).** **Space O(n)** for the copy (O(1) if sorting in place is allowed)."],
            "limits": ["Sorting does more work than needed: we only ask whether a value repeats, not where it goes. A hash set answers that in O(n)."],
            "lines": {
                "sort": "Equal badges become neighbours.",
                "scan": "Compare each badge with the next one.",
                "ret": "No neighbours were equal, so no value repeats.",
            },
        },
        2: {
            "idea": [
                """
                Walk the badges, keeping a set of numbers seen so far. If the current number is already in the set, return
                true; otherwise add it. If the walk ends, there's no duplicate.

                **Invariant.** Before processing badge `i`, the set holds exactly the distinct values among the first `i`
                badges. So "in the set" means "appeared earlier".
                """
            ],
            "build": ["Empty set.", "For each badge: check, then add.", "False if the loop finishes."],
            "complexity": ["**Time O(n)** expected. **Space O(n)** for the set."],
            "lines": {
                "init": "The set of numbers seen so far.",
                "loop": "Each badge once.",
                "check": "Seen before: this is the second copy, stop immediately.",
                "add": "Remember it for later badges.",
                "ret": "Every badge was new.",
            },
        },
    },
    "takeaways": [
        """
        - **"Any repeats?"** → hash set, O(n); stop at the first hit.
        - Sorting is the O(1)-extra-space alternative (in place) at O(n log n).
        - **Pitfall:** adding before checking, which makes every value look like a repeat.
        """
    ],
}


# ---------------------------------------------------------------- letter-tiles
sign, tiles = "spoon", "nopxos"
have = Counter(tiles)
trows = []
h = dict(have)
for ch in sign:
    h[ch] = h.get(ch, 0) - 1
    trows.append((ch, h[ch] + 1, h[ch], "ok" if h[ch] >= 0 else "missing → false"))
EXTRA["letter-tiles"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Repeated letters in the sign need that many tiles (`"spoon"` needs two `o`s).
        - Extra tiles are fine; only missing ones matter.
        - A letter that isn't among the tiles at all fails immediately.
        """
    ],
    "think": [
        COUNTING,
        f"""
        **Tiles as counts.** Order doesn't matter, only how many of each letter. Count the tiles once, then spend one
        tile per letter of the sign; if any count goes below zero, a tile is missing. For sign `"{sign}"` and tiles
        `"{tiles}"` (counts {dict(sorted(have.items()))}):
        """,
        table(["sign letter", "tiles before", "tiles after", "result"], *trows),
    ],
    "approaches": {
        0: {
            "idea": ["Put the tiles in a list. For each sign letter, find a matching tile and remove it; if none is left, the sign can't be spelled."],
            "build": ["Copy the tiles into a pool.", "For each letter, find and remove a tile.", "Fail if a letter has no tile."],
            "complexity": ["**Time O(|sign| · |tiles|):** each find and remove scans the pool. **Space O(|tiles|).**"],
            "limits": ["Searching the pool is linear each time. Since only the number of each letter matters, 26 counters replace the pool."],
            "lines": {
                "pool": "All tiles, available to be taken.",
                "loop": "Each letter of the sign.",
                "find": "Is there still a tile with this letter?",
                "take": "Use it up: remove it from the pool.",
                "ret": "Every letter found a tile.",
            },
        },
        1: {
            "idea": [
                """
                Sort the sign and the tiles. Walk the sorted sign; for each letter, move a tile pointer past smaller tiles
                and check that the next tile is that letter. Each tile is used at most once because the pointer only moves
                forward.
                """
            ],
            "build": ["Sort both.", "For each sign letter, skip smaller tiles.", "The next tile must match; use it."],
            "complexity": ["**Time O(n log n)** for the sorts. **Space O(n)** for the sorted copies."],
            "limits": ["Sorting letters costs O(n log n) to learn what counting tells us in O(n)."],
            "lines": {
                "sort": "Sorted letters let both lists be walked in step.",
                "walk": "Take the sign's letters in sorted order.",
                "skip": "Tiles smaller than the needed letter are extras; pass over them.",
                "match": "The next tile must be this letter; if not (or none is left), the sign can't be made. Using it moves the pointer on.",
                "ret": "Every letter matched a tile.",
            },
        },
        2: {
            "idea": [
                """
                Count the tiles into 26 counters. For each sign letter, decrease its counter; if it drops below zero, the
                sign needs more of that letter than there are tiles.

                **Why it's exact.** After processing the whole sign, counter `x` equals (tiles with `x`) − (sign letters
                `x`). The sign can be spelled exactly when no counter is negative, and checking during the loop catches
                the first shortage early.
                """
            ],
            "build": ["Count the tiles.", "Spend one per sign letter.", "Fail on a negative counter."],
            "complexity": ["**Time O(|sign| + |tiles|).** **Space O(1):** 26 counters."],
            "lines": {
                "count": "How many tiles of each letter there are.",
                "spend": "Use one tile for each letter of the sign.",
                "check": "A negative counter means the sign needs more of this letter than the tiles provide.",
                "ret": "No letter ran out.",
            },
        },
    },
    "takeaways": [
        """
        - **"Can A be built from B?"** → count B, spend for A, watch for negatives.
        - Small alphabets: a fixed array beats a hash map.
        - **Pitfall:** checking only that each letter exists, ignoring how many are needed.
        """
    ],
}


# ---------------------------------------------------------------- loudest-letters-first
s = "banana12b"
cnt = Counter(s)
order = sorted(cnt, key=lambda c: (-cnt[c], c))
buckets = {}
for c in sorted(cnt):
    buckets.setdefault(cnt[c], []).append(c)
EXTRA["loudest-letters-first"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Ties are broken by character code: digits before uppercase before lowercase.
        - All copies of a character stay together.
        - One distinct character: the string is unchanged.
        """
    ],
    "think": [
        COUNTING,
        f"""
        **Count, then order the distinct characters.** The output is just "each character repeated its count times", in
        order of (count descending, code ascending). For `"{s}"`:
        """,
        table(["char", "count", "position in the order"], *[(c, cnt[c], order.index(c) + 1) for c in order]),
        f"""
        Result **`{''.join(c * cnt[c] for c in order)}`**.

        **Sorting without comparisons.** Counts are between 1 and `n`, so instead of sorting the characters, drop each
        into **bucket number = its count**. Reading buckets from `n` down to 1 gives counts in descending order; filling
        each bucket in increasing character code gives the tie order for free:
        """,
        table(["count", "bucket"], *[(k, ", ".join(buckets[k])) for k in sorted(buckets, reverse=True)]),
    ],
    "approaches": {
        0: {
            "idea": ["Repeatedly pick the remaining character with the highest count (ties to the smaller code), output all its copies and remove it. Counting with `s.count` rescans the string each time."],
            "build": ["Distinct characters in code order.", "Each round, find the most frequent remaining one.", "Output its copies and remove it."],
            "complexity": ["**Time O(d² · n)** for `d` distinct characters (up to 62), because every count rescans the string. **Space O(d).**"],
            "limits": ["Counts are recomputed again and again. Counting once, then ordering the distinct characters, is enough."],
            "lines": {
                "left": "The distinct characters still to place, in code order (so ties resolve to the smaller code).",
                "round": "One character is placed per round.",
                "pick": "Find the remaining character with the largest count; strictly larger is needed to replace, so ties keep the smaller code.",
                "emit": "Write all its copies and remove it from the remaining set.",
                "ret": "The arranged string.",
            },
        },
        1: {
            "idea": [
                """
                Count each character once (an array of 128 for ASCII). Collect the characters that occur and sort them by
                `(−count, code)`. Output each one `count` times.
                """
            ],
            "build": ["Count into 128 slots.", "Collect the present characters.", "Sort by count descending, then code.", "Output."],
            "complexity": ["**Time O(n + d log d):** at most 62 distinct characters to sort. **Space O(n)** for the output."],
            "limits": ["Already fast, but it still sorts; buckets indexed by count avoid comparisons entirely."],
            "lines": {
                "count": "One pass: how often each character appears.",
                "collect": "Only characters that actually occur.",
                "sort": "Most frequent first; on equal counts, smaller code first.",
                "emit": "Each character repeated its count times, in that order.",
            },
        },
        2: {
            "idea": [
                """
                Count once. Put each present character into `bucket[count]`, scanning codes in increasing order so each
                bucket is already in tie order. Read buckets from the largest count down and output each character that
                many times.

                **Why it's ordered correctly.** Higher buckets come first (count descending), and within a bucket
                characters were appended in increasing code.
                """
            ],
            "build": ["Count into 128 slots.", "Bucket by count, codes ascending.", "Read buckets from high to low."],
            "complexity": ["**Time O(n):** counting, 128 bucket insertions, and `n` output characters. **Space O(n)** for the buckets and output."],
            "lines": {
                "count": "How often each character appears.",
                "fill": "Drop each present character into the bucket for its count, in increasing code order.",
                "read": "Highest count first; within a bucket the order is already by code.",
                "ret": "The arranged string.",
            },
        },
    },
    "takeaways": [
        """
        - **Sort by frequency:** count, then bucket by count (O(n)) or sort the distinct items.
        - Fill buckets in the tie-break order to get ties for free.
        - **Pitfall:** sorting all `n` characters instead of the few distinct ones.
        """
    ],
}


# ---------------------------------------------------------------- majority-reading
rd = [2, 8, 8, 1, 8, 8, 3, 8, 2]
vrows, cand, c = [], None, 0
for r in rd:
    note = ""
    if c == 0:
        cand = r
        note = "count was 0: new candidate. "
    c += 1 if r == cand else -1
    vrows.append((r, cand, c, note + ("same as candidate: +1" if r == cand else "different: −1 (cancels one)")))
EXTRA["majority-reading"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One reading: it's the majority.
        - "More than half" is strict: in `[1, 2]` there is none, but the problem guarantees one exists.
        - Values up to 10⁹ in size, so counting needs a hash map (or no table at all, with voting).
        """
    ],
    "think": [
        """
        **Three observations, three methods.**

        1. **Counting:** a hash map of counts finds the value whose count exceeds `n/2`.
        2. **Sorting:** a value filling more than half of a sorted array must cover the middle position `n/2`, whatever
           its range, so the middle element is the answer.
        3. **Cancelling:** pair up two **different** readings and throw both away. Each majority reading can be cancelled
           by at most one other reading, and there are fewer others than majority readings, so the majority always
           survives. Boyer–Moore voting does this cancellation in one pass with a candidate and a counter.
        """,
        f"**Voting on `{rd}`:**",
        table(["reading", "candidate", "count", "what happens"], *vrows),
        f"The surviving candidate is **{cand}**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each reading, count its occurrences by scanning the whole list; return the first with count above `n/2`."],
            "build": ["For each reading, count it.", "Return it if it's a majority."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Counts the same values over and over. One pass with a table, or voting, is enough."],
            "lines": {
                "each": "Try each reading as the candidate.",
                "count": "Count it by scanning the list; more than half means it's the answer.",
                "none": "Unreachable when a majority is guaranteed.",
            },
        },
        1: {
            "idea": [
                """
                Sort and return the middle element `s[n // 2]`.

                **Why the middle.** The majority occupies more than `n/2` consecutive positions after sorting. Any block
                that long, wherever it starts, must contain index `n // 2`.
                """
            ],
            "build": ["Sort a copy.", "Return the middle element."],
            "complexity": ["**Time O(n log n).** **Space O(n)** for the copy."],
            "limits": ["Sorting costs O(n log n) to find one value."],
            "lines": {
                "sort": "Group equal readings together.",
                "mid": "The majority's block always covers the middle position.",
            },
        },
        2: {
            "idea": ["Count readings in a hash map; as soon as a count passes `n/2`, return that value."],
            "build": ["Empty map.", "Increment the count of each reading.", "Return when a count exceeds half."],
            "complexity": ["**Time O(n)** expected. **Space O(n)** for the map."],
            "limits": ["The map can hold up to `n/2` distinct values. Voting needs only two variables."],
            "lines": {
                "map": "Value → how many times seen so far.",
                "loop": "Each reading once.",
                "check": "More than half of all readings: this is the majority.",
                "none": "Unreachable when a majority is guaranteed.",
            },
        },
        3: {
            "idea": [
                """
                Keep a `candidate` and a `count`. For each reading: if `count` is 0, take the reading as the new candidate.
                Then add 1 if the reading equals the candidate, else subtract 1.

                **Why the majority survives.** Every decrement pairs one reading with one reading of a different value and
                discards both. The majority has more readings than all others combined, so it can't be fully cancelled; the
                candidate left at the end must be it.
                """
            ],
            "build": ["`candidate`, `count = 0`.", "On `count = 0`, adopt the current reading.", "+1 for a match, −1 otherwise.", "Return the candidate."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "lines": {
                "init": "No candidate yet; count 0.",
                "loop": "Each reading once.",
                "new": "Everything so far has cancelled out: start fresh with this reading.",
                "vote": "A matching reading supports the candidate; a different one cancels one supporting reading.",
                "ret": "The survivor is the majority (guaranteed to exist).",
            },
        },
    },
    "takeaways": [
        """
        - **Majority (> n/2):** Boyer–Moore voting, O(n) time and O(1) space.
        - If a majority isn't guaranteed, verify the candidate with a second counting pass.
        - **Pitfall:** using voting for "most frequent" (plurality); it only works for a strict majority.
        """
    ],
}


# ---------------------------------------------------------------- top-genres
plays, k = [3, 1, 3, 2, 1, 3, 4, 2, 1, 5], 3
gc = Counter(plays)
gb = {}
for g in sorted(gc):
    gb.setdefault(gc[g], []).append(g)
top = sorted(gc, key=lambda g: (-gc[g], g))[:k]
EXTRA["top-genres"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Ties in play count: smaller genre id first.
        - `k` equals the number of genres: return all of them in order.
        - Genre ids can be negative (down to −10⁴), so an array index needs an offset of 10⁴.
        """
    ],
    "think": [
        COUNTING,
        f"""
        **Count, then take the best `k`.** For `{plays}` with `k = {k}`:
        """,
        table(["genre", "plays"], *sorted(gc.items(), key=lambda t: (-t[1], t[0]))),
        f"""
        The top {k} are **`{top}`**.

        **Ways to take the best `k`:** sort all genres (O(g log g)), keep a size-`k` min-heap of the best seen so far
        (O(g log k)), or, since counts are at most `n`, put genres in **buckets by count** and read from the highest
        bucket down (O(n)):
        """,
        table(["play count", "genres (id order)"], *[(c, ", ".join(map(str, gb[c]))) for c in sorted(gb, reverse=True)]),
    ],
    "approaches": {
        0: {
            "idea": ["`k` times, scan all remaining genres for the most played (counting with `plays.count`), take it and remove it."],
            "build": ["Distinct genres in id order.", "Each round, find the most played.", "Take it and remove it."],
            "complexity": ["**Time O(k · g · n)** because every count rescans the log. **Space O(g).**"],
            "limits": ["Counts are recomputed constantly. Count once, then select."],
            "lines": {
                "distinct": "The genres still available, in id order (so ties go to the smaller id).",
                "round": "One genre is chosen per round.",
                "pick": "The genre with the most plays; strictly more is needed to replace, so ties keep the smaller id.",
                "take": "Add it to the answer and remove it from the candidates.",
                "ret": "The `k` chosen genres.",
            },
        },
        1: {
            "idea": ["Count plays into an array indexed by `genre + 10⁴`. Collect the genres that were played and sort them by `(−count, id)`; take the first `k`."],
            "build": ["Count with an offset.", "Collect played genres.", "Sort by count descending, then id.", "Take `k`."],
            "complexity": ["**Time O(n + g log g)** for `g` distinct genres. **Space O(R)** for the count array (R = 20001)."],
            "limits": ["Sorts every genre although only `k` are needed."],
            "lines": {
                "count": "One pass over the log; the offset maps ids −10⁴…10⁴ to indices 0…20000.",
                "collect": "The genres that were played at least once.",
                "sort": "Most plays first; ties by smaller id.",
                "ret": "The first `k`.",
            },
        },
        2: {
            "idea": [
                """
                Count, then scan the genres keeping a **min-heap of size `k`** holding the best `k` so far, ordered by
                `(count, −id)` so the weakest is on top. A new genre replaces the top only if it's better. At the end, sort
                the heap's `k` items from best to worst.
                """
            ],
            "build": ["Count with an offset.", "Min-heap of the best `k`.", "Replace the weakest when a better genre appears.", "Sort the `k` winners."],
            "complexity": ["**Time O(n + g log k).** **Space O(k)** for the heap."],
            "limits": ["Still O(log k) per genre. Counts are bounded by `n`, so buckets avoid comparisons entirely."],
            "lines": {
                "count": "One pass over the log.",
                "heap": "The best `k` genres seen so far, weakest on top.",
                "scan": "Every genre that was played.",
                "out": "Sort the `k` winners from most to fewest plays (ties by id) and return their ids.",
            },
        },
        3: {
            "idea": [
                """
                Count, then drop each played genre into `bucket[count]` in increasing id order. Read buckets from the
                highest count down, collecting genres until `k` are taken.

                **Why the order is right.** Higher buckets come first; within a bucket, ids were appended in increasing
                order, which is the tie rule.
                """
            ],
            "build": ["Count with an offset.", "Bucket genres by count (ids ascending).", "Read from the highest bucket until `k` are taken."],
            "complexity": ["**Time O(n + R):** counting, a pass over the id range, and the buckets. **Space O(n + R).**"],
            "lines": {
                "count": "One pass over the log.",
                "fill": "Each played genre goes into the bucket for its play count, in increasing id order.",
                "read": "Highest count first; stop as soon as `k` genres are collected.",
                "ret": "The top `k` genres.",
            },
        },
    },
    "takeaways": [
        """
        - **Top k by frequency:** count, then buckets (O(n)), a size-k heap (O(g log k)), or a full sort.
        - Encode tie rules in the order buckets are filled or in the heap key.
        - **Pitfall:** a max-heap of all genres when a size-k min-heap is enough.
        """
    ],
}
