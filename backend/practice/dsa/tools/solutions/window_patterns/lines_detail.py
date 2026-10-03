"""Fuller line-by-line breakdowns and shortfall notes for every Sliding Window solution (merged via sol.EXTRA).
Loaded after the detail_* modules (module names are imported in sorted order), so it adds to their entries."""
from sol import EXTRA


def more(pid, i, lines=None, limits=None):
    slot = EXTRA.setdefault(pid, {}).setdefault("approaches", {}).setdefault(i, {})
    if lines:
        slot["lines"] = lines
    if limits:
        slot["limits"] = limits


# Shared wording for the brute-force "extend from every start" loops.
STARTS = "Every index is tried as the left end of the window. Nothing learned from one start is reused for the next, which is exactly the waste the better approaches remove."

# ======================================================================== fixed-size windows
more("best-sales-week", 0, {
    "init": "The best total seen so far. It starts at the smallest possible value (or `None`), not 0: if every day lost money, the right answer is negative, and starting at 0 would report a total no window has.",
    "starts": f"The window can start at `0 … n − k`; starting later would run past the end. That's `n − k + 1` windows. {STARTS}",
    "sum": "Add the `k` values of this window from scratch. This inner loop is the costly part: `k` additions per window, most of them repeated from the previous window.",
    "best": "Keep the larger of the stored best and this window's total.",
    "ret": "After all windows are checked, `best` holds the largest total.",
}, ["**Repeated work.** Windows `i` and `i + 1` share `k − 1` days, yet both are summed in full. With `n = 10⁵` and `k = 5 × 10⁴`, that's about 2.5 × 10⁹ additions, far beyond a one-second limit. Since only one value enters and one leaves per step, the total can be updated in O(1) instead."])
more("best-sales-week", 1, {
    "first": "Sum the first `k` days once. This is window `0 … k − 1`, and it's also the best so far. Every later window will be derived from it.",
    "slide": "Move the window one day to the right: day `i` enters and day `i − k` leaves. After this line, `total` is the sum of days `i − k + 1 … i`. It's one addition and one subtraction, regardless of `k`.",
    "best": "Compare the new window with the best. Every window is compared exactly once, right after its total is formed.",
    "ret": "The largest window total. It's accumulated in 64 bits because the return type is `long`.",
})

more("calm-shift", 0, {
    "init": "The best number of happy customers over all placements.",
    "starts": f"Each possible first minute of the calm stretch: `0 … n − minutes`. {STARTS}",
    "count": "Recount the whole day for this placement: a minute's customers are happy if the owner isn't moody **or** the minute lies inside the stretch. The \"happy anyway\" part is recomputed every time even though it never changes.",
    "ret": "The best placement's count.",
}, ["**Two kinds of repetition.** The customers in non-moody minutes are recounted for every placement, and neighbouring placements differ by just two minutes. At `n = 10⁵` this is 10¹⁰ steps. Splitting the answer into a fixed part plus a sliding window removes both."])
more("calm-shift", 1, {
    "base": "Customers served while the owner isn't moody. They're happy no matter where the calm stretch goes, so they're counted once, up front.",
    "first": "Customers the stretch would rescue if it covered minutes `0 … minutes − 1`. Multiplying by `moody[i]` gives 0 for non-moody minutes, so they aren't counted twice. This is the first window and the best so far.",
    "slide": "Shift the stretch one minute right: minute `i` is added (if it's moody) and minute `i − minutes` is removed (if it was moody). `best` keeps the largest rescue seen.",
    "ret": "Happy anyway plus the best possible rescue. The two parts count disjoint minutes, so adding them is exact.",
})

more("calm-stretches", 0, {
    "init": "The number of calm stretches found.",
    "starts": f"Every stretch of `k` minutes. {STARTS}",
    "test": "Add the window from scratch and compare with `limit · k`. Comparing sums avoids dividing: `sum / k ≤ limit` is the same as `sum ≤ limit · k` because `k` is positive.",
    "ret": "How many stretches passed.",
}, ["Each window is summed in O(k), re-adding `k − 1` minutes it shares with its neighbour: up to 2.5 × 10⁹ additions."])
more("calm-stretches", 1, {
    "cap": "Turn the average condition into a sum condition once. The product is computed in 64 bits so it can't overflow.",
    "first": "Sum the first window and count it if it's calm.",
    "slide": "Update the sum with the minute entering and the minute leaving, then test the new window. Each of the `n − k + 1` windows is tested exactly once.",
    "ret": "The number of calm stretches.",
})

more("seat-the-team", 0, {
    "init": "`t` is the team size, which is also the length of the arc the team must occupy. `best` is the most members already sitting in one arc.",
    "arcs": f"Each seat is tried as the start of the arc, including starts near the end whose arc wraps around to seat 0. {STARTS}",
    "count": "Count the members inside this arc, using `% n` to wrap around. Recounting `t` seats per arc is the slow part.",
    "ret": "The guests in the best arc. Each needs one swap with a member outside, so this is the number of swaps.",
}, ["Neighbouring arcs share `t − 1` seats but each is recounted: O(n · t), which is O(n²) when about half the seats are team members."])
more("seat-the-team", 1, {
    "init": "Count the team. With nobody to seat, no swaps are needed. Returning early also avoids sliding a window of length 0.",
    "first": "Members already in seats `0 … t − 1`: the first arc, and the best so far.",
    "slide": "Rotate the arc one seat clockwise. Seat `i % n` enters and seat `(i − t) % n` leaves; the modulo makes the arc wrap past the last seat. The loop runs `n − 1` times, so every starting seat is visited once.",
    "ret": "Members missing from the fullest arc = guests inside it = swaps needed.",
})

more("vowel-rich-window", 0, {
    "init": "The most vowels found in a window so far.",
    "starts": f"Every substring of length `k`. {STARTS}",
    "count": "Count vowels letter by letter in this window. `k − 1` of these letters were counted for the previous window as well.",
    "ret": "The best count.",
}, ["O(k) per window for a quantity that changes by at most 2 per slide."])
more("vowel-rich-window", 1, {
    "test": "Turn a letter into 1 (vowel) or 0 (anything else). Once letters are numbers, \"vowels in a window\" is just a window sum.",
    "first": "Vowels in the first `k` letters.",
    "slide": "The entering letter can add 1 and the leaving letter can remove 1. Everything in between is unchanged, so this is the whole update.",
    "ret": "The most vowels in any window (at most `k`).",
})

# ======================================================================== longest valid window
LONG_GROW = "Bring the next element into the window on the right. The window may now break the rule; the next lines repair it."
LONG_BEST = "After the repair, `L … R` is the longest valid window that ends at `R` (no earlier start works). Comparing its length with the best covers every possible right end."

more("longest-fresh-run", 0, {
    "init": "The longest fresh run found so far.",
    "starts": f"Each position as the start of a run. {STARTS}",
    "extend": "Grow the run while the next character hasn't appeared in it yet. The \"seen\" set (or array) is rebuilt for every start.",
    "best": "The run from this start is `j − i` long; keep the longest.",
    "ret": "The longest fresh run.",
}, ["With a small alphabet each start stops within 37 characters, but with a large one (or unrestricted text) this is O(n²), and characters are rescanned from every start. Remembering where each character was last seen lets the window jump past a repeat directly."])
more("longest-fresh-run", 1, {
    "init": "`last[c]` is the latest index of character `c` (−1 = never seen). `L` is where the current fresh window starts.",
    "grow": "Take the character at `R` into the window and record that it was seen here.",
    "jump": "If this character's previous copy lies **inside** the window (`last[c] ≥ L`), the window must start just after it. If the previous copy is already left of `L`, it's irrelevant, and moving `L` would wrongly move it backwards.",
    "best": LONG_BEST,
    "ret": "The longest fresh run.",
})

more("one-colour-banner", 0, {
    "init": "The longest run that can be made one colour.",
    "starts": f"Each tile as the start of a run. {STARTS}",
    "extend": "Add tiles while tracking colour counts and the most common colour (`top`). The run needs `length − top` repaints; once that exceeds `k`, longer runs from this start need even more, so stop.",
    "best": "Every run that stays within `k` repaints is a candidate.",
    "ret": "The longest run.",
}, ["Each start rebuilds its counts and may scan most of the banner: O(n²) for a large `k`. A single window that grows on the right and shrinks on the left reuses the counts."])
more("one-colour-banner", 1, {
    "init": "Colour counts for the window `L … R`.",
    "grow": LONG_GROW,
    "shrink": "While the window would need more than `k` repaints (`length − top > k`), drop tiles from the left. `top` is recomputed from the 26 counts on every check, which is correct but costs 26 steps each time.",
    "best": LONG_BEST,
    "ret": "The longest valid run.",
}, ["Recomputing the top count over 26 colours at every check makes it O(26 · n). Since we only care about beating the best length, a never-decreasing maximum count is enough."])
more("one-colour-banner", 2, {
    "init": "Colour counts, the left edge, and `maxf`, the highest count any colour has reached in a window so far.",
    "grow": "Add the tile at `R`.",
    "maxf": "Only the colour just added can set a new maximum, so this is a single comparison.",
    "slide": "If the window is one tile too long for `maxf`, drop exactly one tile from the left. The window length stays the same: it slides. It never shrinks, and `maxf` is never lowered, because a lower value can't produce a longer window.",
    "best": "The length grows only when a colour reaches a new `maxf`, so the best length only improves in those steps.",
    "ret": "The longest achievable run.",
})

more("patch-the-outage", 0, {
    "init": "The longest patchable run.",
    "starts": f"Each minute as the start of a run. {STARTS}",
    "extend": "Take the next minute if patching it (when it's down) keeps the patches within `k`.",
    "best": "The run from this start has `j − i` minutes.",
    "ret": "The longest run.",
}, ["Restarts the zero count at every start. When `k` is large, each start scans almost the whole log: O(n²)."])
more("patch-the-outage", 1, {
    "init": "An empty window with no zeros.",
    "grow": LONG_GROW + " A down minute adds one patch.",
    "shrink": "With more than `k` zeros the window can't be fixed. Drop minutes from the left until one zero has left. Ones dropped along the way are simply lost from this window.",
    "best": LONG_BEST,
    "ret": "The longest run that can be fully online.",
})

more("ride-on-a-budget", 0, {
    "init": "The longest affordable ride.",
    "starts": f"Each stop as the boarding point. {STARTS}",
    "extend": "Keep riding while the next fare still fits in the budget. Fares are positive, so once a hop doesn't fit, no longer ride from here fits either.",
    "best": "The number of hops from this stop.",
    "ret": "The longest ride.",
}, ["Up to `n` hops from each of `n` stops: O(n²) for a big budget. Prefix sums let us binary-search the end; a window removes even the search."])
more("ride-on-a-budget", 1, {
    "prefix": "`pre[j]` is the cost of the first `j` hops, so hops `i … j − 1` cost `pre[j] − pre[i]`. Fares are positive, so `pre` strictly increases, which is what makes binary search valid.",
    "search": "For start `i`, find the last `j` with `pre[j] ≤ pre[i] + budget`. Then `j − i` hops is the longest ride from `i`. Searching in `[i, n]` guarantees at least 0 hops.",
    "ret": "The longest ride over all starts.",
}, ["One binary search per start: O(n log n). It ignores that the best end only moves right as the start moves right, which the two-pointer window exploits."])
more("ride-on-a-budget", 2, {
    "init": "An empty ride with zero cost.",
    "grow": LONG_GROW + " The cost rises by this hop's fare.",
    "shrink": "Over budget: give up hops from the front until the ride fits. If this single hop costs more than the budget, the window empties completely (`L = R + 1`).",
    "best": LONG_BEST + " An empty window contributes 0, which is the right answer when nothing is affordable.",
    "ret": "The longest affordable ride.",
})

more("steady-readings", 0, {
    "init": "The longest steady run.",
    "starts": f"Each reading as the start of a run. {STARTS}",
    "extend": "Extend while the running max and min stay within `limit` of each other. They're updated incrementally, but the work restarts at every start.",
    "best": "The run from this start.",
    "ret": "The longest steady run.",
}, ["O(n²) for a generous limit. A window needs the max and min after removing from the left, which plain variables can't provide; monotonic deques can."])
more("steady-readings", 1, {
    "init": "Two deques of indices (`hi` for the maximum, `lo` for the minimum) and the window's left edge.",
    "push": "Before adding `R`, remove from the back of `hi` every index whose reading is `≤` the new one: they can never be the maximum while `R` is in the window. Likewise for `lo` with `≥`. Then add `R` to both. The fronts are now the window's maximum and minimum.",
    "shrink": "While the spread `max − min` exceeds `limit`, move `L` right. A deque front whose index fell below `L` has left the window and is popped, so the fronts stay correct.",
    "best": LONG_BEST,
    "ret": "The longest steady run.",
})

more("two-flavour-basket", 0, {
    "init": "The most scoops found.",
    "starts": f"Each tub as the starting point. {STARTS}",
    "extend": "Walk right while the tub's flavour is one of the (at most two) flavours already chosen, or while the second slot is still free.",
    "best": "Scoops taken from this start.",
    "ret": "The most scoops.",
}, ["With two alternating flavours, every start walks to the end: O(n²)."])
more("two-flavour-basket", 1, {
    "init": "A count per flavour for the window and `distinct`, the number of flavours with a positive count.",
    "grow": LONG_GROW + " A flavour whose count goes from 0 to 1 is new to the window.",
    "shrink": "Three flavours: drop tubs from the left until some flavour's count reaches 0. That can take several steps, because the leftmost flavour may appear again later in the window.",
    "best": LONG_BEST,
    "ret": "The most scoops.",
})

# ======================================================================== shortest valid window
SHORT_SHRINK = "While the window is valid, it's a candidate: record its length, then drop the leftmost element to try a shorter one. The loop stops at the first invalid window, so the last recorded one is the tightest valid window ending at `R`."

more("shortest-push", 0, {
    "init": "0 means \"not found yet\".",
    "starts": f"Each hour as the start of a push. {STARTS}",
    "extend": "Add hours one by one.",
    "record": "The first time the total reaches the target is the shortest push from this start; longer ones from here can't be shorter, so stop.",
    "ret": "The fewest hours, or 0.",
}, ["Each start sums afresh: O(n²) when the target is large."])
more("shortest-push", 1, {
    "init": "`n + 1` stands for \"no valid window\" because no real answer can be that long.",
    "grow": "Add hour `R` to the window total.",
    "shrink": SHORT_SHRINK,
    "ret": "Convert the sentinel to 0 if the target was never reached.",
})

more("every-flavour-sampler", 0, {
    "init": "`d` is the number of different flavours on the whole shelf; the whole shelf always works, so `best = n` to start.",
    "starts": f"Each jar as the start of the stretch. {STARTS}",
    "extend": "Extend until all `d` flavours are present, but only while the stretch is shorter than the best: a longer one can't help.",
    "compress": "C has no hash map, so flavours are replaced by their rank among the distinct values: sort a copy, remove duplicates, binary-search each jar.",
    "ret": "The shortest stretch.",
}, ["Each start rebuilds its flavour set: O(n²) in the worst case."])
more("every-flavour-sampler", 1, {
    "init": "Count the distinct flavours first, so we know what \"complete\" means. Then an empty window.",
    "compress": "C maps each flavour to a small id once, so the counts can live in a plain array.",
    "grow": "Add jar `R`. A flavour going from 0 to 1 is now present.",
    "shrink": SHORT_SHRINK + " The window becomes incomplete exactly when a flavour's count drops to 0.",
    "ret": "The shortest complete stretch.",
})

more("balance-the-quartet", 0, {
    "init": "Count each voice. If three of them already sit at `n/4`, the fourth must too, and nothing needs changing.",
    "starts": f"Each position as the start of the piece. {STARTS}",
    "extend": "Move singers from \"outside\" into the piece until no voice has more than `n/4` singers outside. That's the shortest usable piece from this start.",
    "ret": "The shortest piece.",
}, ["Copies the counts and rescans for every start: O(n²)."])
more("balance-the-quartet", 1, {
    "init": "`out` starts as the counts of the whole string (the piece is empty). Return 0 if it's already balanced.",
    "grow": "Singer `R` joins the piece, so they're no longer outside.",
    "shrink": SHORT_SHRINK + " The window is valid when every voice has at most `n/4` singers outside it.",
    "ret": "The shortest usable piece.",
})

more("shortest-trail-window", 0, {
    "init": "`n + 1` means \"not found\".",
    "starts": "A shortest window must begin with `t[0]` (otherwise trim its first letter), so only those positions are tried as starts.",
    "match": "Match `t` greedily: take each next letter of `t` at its first occurrence. That finishes the route as early as possible, giving the shortest window from this start.",
    "best": "Strictly shorter only, so the leftmost window wins ties.",
    "ret": "The window, or an empty string.",
}, ["Each start may scan to the end of `s`: O(n²). The \"latest start\" table processes all starts in one pass."])
more("shortest-trail-window", 1, {
    "init": "`start[j]` (for `j = 1 … m`) will be the latest position from which the first `j` letters of `t` can be matched in order, ending at or before the current position. −1 means not possible yet.",
    "scan": "Each position of `s` is considered as the right end of a window.",
    "update": "If `s[i]` equals `t[j − 1]`, then the first `j` letters can finish at `i`, starting where the first `j − 1` letters started. Going from `j = m` down to 1 makes sure `start[j − 1]` still refers to positions before `i`, so one character never matches two letters of `t`.",
    "best": "`start[m]` is the latest start of a full match ending at `i`: the shortest window ending here. Strictly shorter only, so the leftmost wins ties.",
    "ret": "The window, or an empty string.",
})

more("smallest-covering-window", 0, {
    "init": "How many of each character `t` requires.",
    "starts": f"Each position as the start. {STARTS}",
    "extend": "Extend with a fresh copy of the requirements until nothing is missing, stopping early if the window can't beat the best.",
    "ret": "The window, or an empty string.",
}, ["Each start rebuilds its requirement counts and may scan far: O(n²)."])
more("smallest-covering-window", 1, {
    "init": "`need[c]` = copies of `c` still required (negative = extras in the window); `missing` = total copies still required.",
    "grow": "Add `s[R]`. Only a copy that was still needed (`need > 0`) reduces `missing`; extras just push `need` below zero.",
    "shrink": SHORT_SHRINK + " Removing a character whose `need` turns positive makes the window lack it again, so `missing` rises and the loop ends.",
    "ret": "The best window, cut out once at the end.",
})

# ======================================================================== "at most k" counting
ADD = "All windows ending at `R` that start at `L`, `L + 1`, …, `R` satisfy the rule (shrinking keeps it), so this adds `R − L + 1` windows in one step. Each window is counted exactly once: at its own right end."

more("exactly-k-breeds", 0, {
    "init": "The running count of stretches. In Java, C++ and C, `mark` records the start at which a breed was last seen, so the array never needs clearing.",
    "starts": f"Each pen as the left end. {STARTS}",
    "extend": "Add pens and keep the number of breeds seen. Past `k` breeds, every longer stretch from this start has more than `k` too, so stop.",
    "count": "Count the stretches that have exactly `k` breeds.",
    "ret": "The total, in 64 bits.",
}, ["Quadratic: about 5 × 10⁹ steps when breeds are few and `k` is large. Counting \"at most\" with a window handles all stretches ending at `R` at once."])
more("exactly-k-breeds", 1, {
    "atmost": "One routine counts stretches with **at most** `limit` breeds; the answer comes from calling it twice. Counts live in an array because breed values are at most `n`.",
    "grow": "Add pen `R`. If its breed's count goes from 0 to 1, the window has one more breed.",
    "shrink": "Too many breeds: drop pens from the left until a breed's count reaches 0. After this, `L` is the earliest start with at most `limit` breeds.",
    "add": ADD,
    "ret": "Stretches with at most `k` breeds, minus those with at most `k − 1`, leaves exactly `k`. `atMost(0)` is 0 because the window is emptied for every `R`.",
})

more("exactly-k-odd-tickets", 0, {
    "init": "The running count.",
    "starts": f"Each draw as the left end. {STARTS}",
    "extend": "`& 1` is 1 for odd numbers. Past `k` odd tickets, stop: longer stretches only add more.",
    "count": "A stretch with exactly `k` odd tickets.",
    "ret": "The total.",
}, ["Quadratic when odd tickets are rare: each start scans a long run of even tickets."])
more("exactly-k-odd-tickets", 1, {
    "init": "`seen[c]` = how many prefixes so far contain exactly `c` odd tickets. The empty prefix has 0, so `seen[0] = 1`. An array works because `c` is at most `n`.",
    "scan": "`p` = odd tickets among the tickets read so far.",
    "look": "A stretch ending here has exactly `k` odd tickets when the prefix before it had `p − k`. There are `seen[p − k]` such prefixes, so that many stretches.",
    "record": "Only now add the current prefix, so it can't pair with itself (that would be an empty stretch).",
    "ret": "The total.",
}, ["It needs a table of size `n + 1`. The two-window method computes the same count with O(1) memory."])
more("exactly-k-odd-tickets", 2, {
    "atmost": "Counts stretches with at most `limit` odd tickets.",
    "grow": "Add ticket `R` to the window's odd count.",
    "shrink": "Too many odd tickets: drop from the left until one odd ticket leaves (even tickets in front of it go too).",
    "add": ADD,
    "ret": "At most `k` minus at most `k − 1` = exactly `k`.",
})

more("full-set-of-stamps", 0, {
    "init": "The running count.",
    "starts": f"Each stamp as the left end. {STARTS}",
    "extend": "Collect letters until all three are present. Java, C++ and C use a 3-bit mask, where 7 means a, b and c have all been seen.",
    "add": "Once full at `j`, every substring from this start ending at `j` or later is full too: `n − j` of them.",
    "ret": "The total.",
}, ["A start may scan far when a letter is missing for a long stretch: O(n²)."])
more("full-set-of-stamps", 1, {
    "init": "The last position of `a`, `b` and `c`; −1 means not seen yet.",
    "scan": "Position `i` is now the latest of its letter.",
    "add": "A substring ending at `i` contains all three letters exactly when it starts at or before the earliest of the three last positions. That's `min(last) + 1` substrings, or 0 while a letter is still unseen.",
    "ret": "The total.",
})

more("products-under-a-cap", 0, {
    "init": "The running count.",
    "starts": f"Each factor as the left end. {STARTS}",
    "extend": "Multiply in the next factor; once the product reaches the cap, longer runs can't drop below it, so stop. The product is kept in 64 bits: it's below 10⁶ before the multiply and at most 1000 times larger after.",
    "ret": "The total.",
}, ["Runs of 1s don't increase the product, so each start may extend across the whole array: O(n²)."])
more("products-under-a-cap", 1, {
    "edge": "Every product is at least 1, so with `cap ≤ 1` nothing qualifies. Returning here also stops the shrink loop from running past an empty window.",
    "init": "Empty window: product 1.",
    "grow": "Multiply in factor `R`.",
    "shrink": "While the product is too big, divide out the leftmost factor. The division is exact because that factor was multiplied in earlier.",
    "add": ADD,
    "ret": "The total.",
})

# ======================================================================== frequency maps
more("best-unique-bundle", 0, {
    "init": "The best total, or 0 if no bundle exists. In C, `mark[v] = i + 1` means \"seen in window `i`\".",
    "windows": "Every window of `k` neighbouring prices.",
    "check": "Build the set and the sum for this window from scratch. If the set has `k` values, all prices differ.",
    "ret": "The best total.",
}, ["O(k) work per window: up to 2.5 × 10⁹ steps."])
more("best-unique-bundle", 1, {
    "init": "A count per price, `dup` (prices appearing twice or more in the window) and the window total.",
    "add": "Price `i` enters. If its count just became 2, there's one more duplicated price.",
    "remove": "Price `i − k` leaves. If its count just dropped to 1, it's no longer duplicated.",
    "best": "A full window with no duplicated price is a valid bundle.",
    "ret": "The best bundle total, or 0.",
})

more("every-word-once", 0, {
    "init": "Word length, word count, and how often each word is required. C first converts words and chunks to ids (see the next row).",
    "ids": "C has no string map: sort the words, merge duplicates into counts, then binary-search the chunk at every position of `s` to get its word id (−1 if it isn't a word).",
    "starts": "Every position where a full chain would fit.",
    "check": "Cut the chunks one by one and count them; a chunk that isn't a word, or one used more often than required, rules this start out.",
    "ret": "The starts, already in increasing order.",
}, ["Each start re-cuts and re-hashes `w` chunks of length `L`: O(n · w · L). Starts `L` apart share all but one chunk."])
more("every-word-once", 1, {
    "init": "How often each word is required.",
    "ids": "C turns words and chunks into small ids once, so the counts can be arrays.",
    "offsets": "Starts with the same remainder mod `L` walk through the same chunks; each offset gets its own window. C also undoes the counts left by one offset before the next.",
    "grow": "Take the next whole word into the window.",
    "reset": "A chunk that isn't a word can't be in any chain. Empty the window and restart right after it.",
    "shrink": "If this word is now used more often than required, drop words from the left until it isn't. Any chain containing the current chunk must start after the dropped part.",
    "hit": "The window uses every word exactly as required: a chain starts at `left`. Drop its first word to keep searching.",
    "ret": "Starts from different offsets interleave, so sort them.",
})

more("repeat-within-reach", 0, {
    "init": "The number of codes.",
    "each": "Each position as the earlier copy.",
    "ahead": "Look at the next `k` codes only; anything further is out of reach.",
    "ret": "No close repeat.",
}, ["Up to `n · k` = 10¹⁰ comparisons at the limits."])
more("repeat-within-reach", 1, {
    "sort": "Order positions by code, then by position, so equal codes sit together in increasing position order.",
    "pairs": "For a given code, the closest two positions are neighbours in this order, so checking adjacent pairs is enough.",
    "ret": "No close repeat.",
}, ["The sort costs O(n log n). A hash map of last positions answers each check in O(1) expected time."])
more("repeat-within-reach", 2, {
    "init": "A map from code to its most recent position. C builds a small open-addressing hash table.",
    "scan": "Each code in order.",
    "check": "Only the most recent earlier copy matters, since it's the closest. If it's at most `k` back, we're done.",
    "update": "This position becomes the most recent one. For any later position, it's at least as close as any older copy.",
    "ret": "No close repeat.",
})

more("scrambled-copies", 0, {
    "init": "Letter counts of the word.",
    "windows": "Every window of the word's length.",
    "count": "Count this window's letters from scratch and compare all 26 counts.",
    "ret": "The matching starts in order.",
}, ["O(m) per window, although sliding changes only two letters."])
more("scrambled-copies", 1, {
    "init": "`delta[c]` = window count − word count, starting at minus the word's counts. `diff` = how many letters have a non-zero `delta`.",
    "bump": "Change one letter's `delta` and keep `diff` correct: leaving 0 adds a mismatch, reaching 0 removes one.",
    "slide": "The entering letter is added; once the window is longer than the word, the leaving letter is removed.",
    "hit": "No mismatched letter in a full window: it's a rearrangement of the word.",
    "ret": "The matching starts in order.",
})

more("variety-per-window", 0, {
    "windows": "Every window's distinct count, computed from scratch. In C, values are first compressed to ids and `mark[id] = i + 1` means \"seen in window `i`\".",
    "compress": "C replaces each value by its rank among the distinct values (sort, de-duplicate, binary-search), so arrays can be used instead of a hash map.",
}, ["O(k) per window: up to 2.5 × 10⁹ steps."])
more("variety-per-window", 1, {
    "init": "Counts of the window's values and `distinct`, the number of values with a positive count.",
    "compress": "C maps values to small ids once.",
    "add": "Item `i` enters. A value going from 0 to 1 is a new type.",
    "remove": "Item `i − k` leaves. A value dropping to 0 is gone.",
    "record": "Each full window's number of types, in order.",
    "ret": "One number per window.",
})
