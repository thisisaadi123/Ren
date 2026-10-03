"""Arrays & Hashing: consecutive runs."""
import textwrap

from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

# A small hash set of 64-bit keys for the C versions: open addressing, linear probing.
C_SET = """
    // C has no built-in hash set, so here is a small one: open addressing with
    // linear probing over a power-of-two table. Keys are 64-bit.
    typedef struct { long long key; bool used; } Slot;  //@set

    static unsigned slotOf(long long key, unsigned mask) {  //@set
        unsigned long long h = (unsigned long long) key * 0x9E3779B97F4A7C15ULL;  //@set
        return (unsigned) (h >> 32) & mask;  //@set
    }  //@set

    static bool has(const Slot* t, unsigned mask, long long key) {  //@set
        for (unsigned s = slotOf(key, mask); t[s].used; s = (s + 1) & mask)  //@set
            if (t[s].key == key) return true;  //@set
        return false;  //@set
    }  //@set

    static void add(Slot* t, unsigned mask, long long key) {  //@set
        unsigned s = slotOf(key, mask);  //@set
        while (t[s].used && t[s].key != key) s = (s + 1) & mask;  //@set
        t[s].key = key;  //@set
        t[s].used = true;  //@set
    }  //@set
"""
C_SET = textwrap.indent(C_SET, " " * 20)  # match the code strings it is joined to
C_SET_ROW = ("set", "C has no hash set, so these few lines build one. `slotOf` scrambles a key into a starting slot (multiply by a large odd constant, keep the well-mixed high bits). `has` walks forward from there until it finds the key or an empty slot; `add` walks the same way and claims the slot. With the table at most half full, each call is O(1) on average.")


@problem
def is_it_a_straight():
    good, bad = [9, 6, 8, 5, 7], [4, 7, 5, 4]

    w1 = Steps("Find the smallest card, then look for each card the run needs.")
    lo = min(good)
    w1.step(f"The smallest card is {lo}. A straight of {len(good)} cards must be exactly {lo} … {lo + len(good) - 1}.", Row(good, st={good.index(lo): "active"}, slots=True), Vars(smallest=lo))
    for t in range(1, len(good)):
        v = lo + t
        j = good.index(v)
        st = {good.index(lo + s): "found" for s in range(t)}
        st[j] = "answer"
        w1.step(f"Need {v}: scan the hand… found at index {j}.", Row(good, st=st, slots=True), Vars(looking_for=v))
    w1.step("Every value from 5 to 9 is there, and there are exactly 5 cards: a straight.", Row(good, st={i: "found" for i in range(len(good))}, slots=True), result=True)

    w2 = Steps("Sort, then every neighbour must be exactly one more.")
    s = sorted(good)
    w2.step(f"Sorted: {s}.", Row(good, label="hand"), Row(s, label="sorted", slots=True))
    for i in range(len(s) - 1):
        w2.step(f"{s[i]} → {s[i + 1]}: a step of exactly 1.", Row(s, st={i: "active", i + 1: "active", **{q: "found" for q in range(i)}}, slots=True))
    w2.step("All four steps are +1: a straight.", Row(s, st={i: "found" for i in range(len(s))}, slots=True), result=True)
    sb = sorted(bad)
    w2.step(f"A failing hand, {bad}, sorted is {sb}: 4 → 4 repeats, so it fails at once.", Row(sb, st={0: "mark", 1: "mark"}, slots=True), result=False)

    w3 = Steps("The span must be exactly n − 1, and no card may repeat.")
    lo, hi = min(good), max(good)
    w3.step(f"Smallest {lo}, largest {hi}: span {hi} − {lo} = {hi - lo}, and n − 1 = {len(good) - 1}. The span fits.", Row(good, st={good.index(lo): "mark", good.index(hi): "mark"}, slots=True), Vars(min=lo, max=hi, span=hi - lo))
    seen = [False] * len(good)
    for c in good:
        seen[c - lo] = True
        w3.step(f"Card {c} goes to slot {c} − {lo} = {c - lo}. The slot was empty.", Row(good, st={good.index(c): "active"}, slots=True), Row(["✓" if x else None for x in seen], st={c - lo: "new"}, label="seen[card − min]", slots=True))
    w3.step("Five cards, five different slots: no repeats, so it's a straight.", Row(["✓"] * 5, label="seen[card − min]", slots=True), result=True)
    lo2, hi2 = min(bad), max(bad)
    seen2 = [None] * (hi2 - lo2 + 1)
    w3.step(f"For {bad}: span {hi2} − {lo2} = {hi2 - lo2} = n − 1, so check repeats. 4 → slot 0, 7 → slot 3, 5 → slot 1, then 4 → slot 0 again: taken. Not a straight.", Row(bad, st={0: "mark", 3: "mark"}, slots=True), Row(["✓", "✓", None, "✓"], st={0: "mark"}, label="seen[card − min]", slots=True), result=False)

    sol(
        "is-it-a-straight",
        summary="""
            A straight of n cards is exactly the values `min, min + 1, …, min + n − 1`. So the hand is a
            straight when the largest card is `min + n − 1` **and** no card repeats. Checking both takes one
            pass and a small table, no sorting.
        """,
        question=[
            """
            You get a hand of numbers. Decide whether you could lay them out as a run where each card is
            exactly one more than the card before it.

            - **Order doesn't matter.** `[7, 5, 6]` is a straight: rearranged it's 5, 6, 7.
            - **Every card must be used**, so a gap anywhere breaks it: `[2, 4, 3, 6]` is missing a 5.
            - **Repeats break it** too: a straight goes up by exactly one at each step, so no two cards can
              be equal. `[1, 2, 2]` is not a straight.
            - **One card** is always a straight (there's nothing to compare).
            - **Negative cards** are allowed: `[−1, 0, 1]` is a straight.
            - **Size and range:** up to 10⁵ cards between −10⁹ and 10⁹. The gap between the largest and
              smallest card can be 2 × 10⁹, past the 32-bit `int` limit, so compute it with 64-bit integers in
              Java, C++ and C.
            """
        ],
        think=[
            """
            Take the hand `[9, 6, 8, 5, 7]`. If you lay it out by hand you'd pick the smallest card, 5, and
            then look for 6, then 7, 8, 9. Once you know the smallest card and how many cards there are, the
            whole straight is **forced**: it must be 5, 6, 7, 8, 9.
            """,
            fig(Row([9, 6, 8, 5, 7], label="hand"), Row([5, 6, 7, 8, 9], label="the only possible straight"),
                caption="With 5 cards and a smallest card of 5, the only straight is 5 … 9."),
            """
            That gives two simple conditions, and together they're exactly right:

            1. **The span fits:** `max − min == n − 1`. Five cards from 5 to 9 have span 4.
            2. **No repeats.** If the span is n − 1, there are exactly n possible values, and n cards with
               no repeats must use each of them once. With a repeat, something is missing: `[4, 7, 5, 4]` has
               span 3 = n − 1, but the 4 is doubled, so the 6 is missing.

            Condition 1 alone isn't enough (`[4, 7, 5, 4]` passes it), and condition 2 alone isn't either
            (`[1, 5]` has no repeats). Both are needed. The approaches below check them with less and less
            work.
            """,
        ],
        approaches=[
            approach(
                "Look for every card the straight needs",
                "brute",
                "O(n²)",
                "O(1)",
                idea=[
                    """
                    Find the smallest card `lo`. The straight must contain `lo + 1, lo + 2, …, lo + n − 1`.
                    For each of those values, scan the hand; if any is missing, it's not a straight.

                    Why does this catch repeats? If all n values `lo … lo + n − 1` are found among n cards,
                    each card is one of those values and each value is used, so no value can be used twice
                    (a repeat would leave too few cards to cover all n values).
                    """
                ],
                walk=w1,
                build=[
                    "Find the minimum card `lo`.",
                    "For `t` from 1 to n − 1, scan the hand for `lo + t`.",
                    "If some value is never found, return false.",
                    "If every value was found, return true.",
                ],
                code={
                    "python": """
                        class Solution:
                            def isStraight(self, cards: List[int]) -> bool:
                                lo = min(cards)  #@min
                                for t in range(1, len(cards)):  #@each
                                    if lo + t not in cards:  #@scan
                                        return False  #@scan
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean isStraight(int[] cards) {
                                int lo = Integer.MAX_VALUE;  //@min
                                for (int c : cards) lo = Math.min(lo, c);  //@min
                                for (int t = 1; t < cards.length; t++) {  //@each
                                    boolean found = false;  //@scan
                                    for (int c : cards) if (c == lo + t) { found = true; break; }  //@scan
                                    if (!found) return false;  //@scan
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool isStraight(vector<int>& cards) {
                                int lo = *min_element(cards.begin(), cards.end());  //@min
                                for (int t = 1; t < (int) cards.size(); t++) {  //@each
                                    if (find(cards.begin(), cards.end(), lo + t) == cards.end()) {  //@scan
                                        return false;  //@scan
                                    }
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool isStraight(int* cards, int cardsSize) {
                            int lo = cards[0];  //@min
                            for (int i = 1; i < cardsSize; i++) if (cards[i] < lo) lo = cards[i];  //@min
                            for (int t = 1; t < cardsSize; t++) {  //@each
                                bool found = false;  //@scan
                                for (int i = 0; i < cardsSize && !found; i++) found = cards[i] == lo + t;  //@scan
                                if (!found) return false;  //@scan
                            }
                            return true;  //@ret
                        }
                    """,
                },
                lines=[
                    ("min", "The smallest card fixes where the straight starts."),
                    ("each", "Each value the straight needs after the first: `lo + 1` up to `lo + n − 1`. `lo + t` stays within `int` because `t` is under 10⁵."),
                    ("scan", "Scan the whole hand for that value. Missing means there's a gap (or a repeat that pushed a value out).",
                     {"python": "`in` on a list is a linear scan.", "cpp": "`find` is a linear scan; it returns `end()` when the value isn't there."}),
                    ("ret", "All n values are present among n cards, so each appears exactly once: a straight."),
                ],
                complexity=["**Time O(n²):** up to n − 1 scans of n cards. **Space O(1).**"],
                limits=[
                    """
                    Every "is this value in the hand?" question is answered by a full scan, about 10¹⁰ steps
                    for 10⁵ cards. Sorting answers all of them at once.
                    """
                ],
                slow=True,
            ),
            approach(
                "Sort, then check each neighbour",
                "better",
                "O(n log n)",
                "O(n)",
                idea=[
                    """
                    Sort a copy of the hand. A straight sorted is `lo, lo + 1, lo + 2, …`, so every adjacent
                    pair must differ by exactly 1. A difference of 0 is a repeat; a difference of 2 or more is
                    a gap. Either fails.
                    """
                ],
                walk=w2,
                build=[
                    "Sort a copy of the cards.",
                    "For each adjacent pair, if `s[i + 1] − s[i]` isn't 1, return false.",
                    "Otherwise return true.",
                ],
                code={
                    "python": """
                        class Solution:
                            def isStraight(self, cards: List[int]) -> bool:
                                s = sorted(cards)  #@sort
                                for i in range(len(s) - 1):  #@pairs
                                    if s[i + 1] - s[i] != 1:  #@pairs
                                        return False  #@pairs
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean isStraight(int[] cards) {
                                int[] s = cards.clone();  //@sort
                                Arrays.sort(s);  //@sort
                                for (int i = 0; i + 1 < s.length; i++) {  //@pairs
                                    if ((long) s[i + 1] - s[i] != 1) return false;  //@pairs
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool isStraight(vector<int>& cards) {
                                vector<int> s = cards;  //@sort
                                sort(s.begin(), s.end());  //@sort
                                for (size_t i = 0; i + 1 < s.size(); i++) {  //@pairs
                                    if ((long long) s[i + 1] - s[i] != 1) return false;  //@pairs
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* x, const void* y) {  //@cmp
                            int p = *(const int*) x, q = *(const int*) y;  //@cmp
                            return (p > q) - (p < q);  //@cmp
                        }  //@cmp

                        bool isStraight(int* cards, int cardsSize) {
                            int* s = malloc(cardsSize * sizeof(int));  //@sort
                            memcpy(s, cards, cardsSize * sizeof(int));  //@sort
                            qsort(s, cardsSize, sizeof(int), cmpInt);  //@sort
                            bool ok = true;  //@pairs
                            for (int i = 0; i + 1 < cardsSize && ok; i++) {  //@pairs
                                ok = (long long) s[i + 1] - s[i] == 1;  //@pairs
                            }
                            free(s);  //@ret
                            return ok;  //@ret
                        }
                    """,
                },
                lines=[
                    ("cmp", "`qsort` needs a comparator. `(p > q) − (p < q)` gives −1, 0 or 1 and can't overflow like `p − q` could with values near ±10⁹."),
                    ("sort", "Sort a copy so the caller's hand isn't rearranged."),
                    ("pairs", "Each neighbour must be exactly one more. 0 means a repeat, more than 1 means a gap.",
                     {"java": "The difference is taken as `long`: two cards at ±10⁹ differ by 2 × 10⁹, which overflows `int` and could wrap around to a wrong value.",
                      "cpp": "The difference is taken as `long long` so it can't overflow.",
                      "c": "The difference is taken as `long long` so it can't overflow; `ok` lets the loop stop early and still free the copy."}),
                    ("ret", "No bad step: the sorted hand climbs by one each time.", {"c": "Free the copy, then return."}),
                ],
                complexity=["**Time O(n log n)** for the sort; the scan is O(n). **Space O(n)** for the sorted copy."],
                limits=[
                    """
                    Sorting puts every card in order, but the question only needs two facts: the span, and
                    whether anything repeats. Both can be found without ordering anything.
                    """
                ],
            ),
            approach(
                "Check the span, then mark each card's slot",
                "best",
                "O(n)",
                "O(n)",
                idea=[
                    """
                    1. One pass finds `min` and `max`. If `max − min != n − 1`, the hand can't be a straight
                       (too wide means a gap; too narrow means repeats).
                    2. Now every card lies in `min … min + n − 1`, so card `c` has a natural slot
                       `c − min` between 0 and n − 1. Mark slots in a boolean array; a slot marked twice is a
                       repeat.

                    The span check is what makes the array small: without it, slots could reach 2 × 10⁹. And
                    no hash set is needed, because the slots are plain array indices.
                    """
                ],
                walk=w3,
                build=[
                    "Find `lo = min(cards)` and `hi = max(cards)`.",
                    "If `hi − lo != n − 1` (in 64 bits), return false.",
                    "Make a boolean array `seen` of size n.",
                    "For each card: if `seen[c − lo]` is already true, return false; otherwise set it.",
                    "Return true.",
                ],
                code={
                    "python": """
                        class Solution:
                            def isStraight(self, cards: List[int]) -> bool:
                                n = len(cards)
                                lo, hi = min(cards), max(cards)  #@span
                                if hi - lo != n - 1:  #@span
                                    return False  #@span
                                seen = [False] * n  #@seen
                                for c in cards:  #@mark
                                    if seen[c - lo]:  #@mark
                                        return False  #@mark
                                    seen[c - lo] = True  #@mark
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean isStraight(int[] cards) {
                                int n = cards.length;
                                int lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;  //@span
                                for (int c : cards) { lo = Math.min(lo, c); hi = Math.max(hi, c); }  //@span
                                if ((long) hi - lo != n - 1) return false;  //@span
                                boolean[] seen = new boolean[n];  //@seen
                                for (int c : cards) {  //@mark
                                    if (seen[c - lo]) return false;  //@mark
                                    seen[c - lo] = true;  //@mark
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool isStraight(vector<int>& cards) {
                                int n = cards.size();
                                auto [mn, mx] = minmax_element(cards.begin(), cards.end());  //@span
                                int lo = *mn, hi = *mx;  //@span
                                if ((long long) hi - lo != n - 1) return false;  //@span
                                vector<bool> seen(n, false);  //@seen
                                for (int c : cards) {  //@mark
                                    if (seen[c - lo]) return false;  //@mark
                                    seen[c - lo] = true;  //@mark
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool isStraight(int* cards, int cardsSize) {
                            int lo = cards[0], hi = cards[0];  //@span
                            for (int i = 1; i < cardsSize; i++) {  //@span
                                if (cards[i] < lo) lo = cards[i];  //@span
                                if (cards[i] > hi) hi = cards[i];  //@span
                            }  //@span
                            if ((long long) hi - lo != cardsSize - 1) return false;  //@span
                            bool* seen = calloc(cardsSize, sizeof(bool));  //@seen
                            bool ok = true;  //@mark
                            for (int i = 0; i < cardsSize && ok; i++) {  //@mark
                                if (seen[cards[i] - lo]) ok = false;  //@mark
                                seen[cards[i] - lo] = true;  //@mark
                            }
                            free(seen);  //@ret
                            return ok;  //@ret
                        }
                    """,
                },
                lines=[
                    ("span", "One pass for the smallest and largest card. A straight of n cards spans exactly n − 1. Anything else fails immediately.",
                     {"java": "`(long) hi − lo`: the span can be 2 × 10⁹, which doesn't fit in `int`.",
                      "cpp": "`minmax_element` finds both in one pass. The span is computed as `long long` because it can be 2 × 10⁹.",
                      "c": "The span is computed as `long long` because it can be 2 × 10⁹."}),
                    ("seen", "One flag per possible value. After the span check there are exactly n possible values, `lo … lo + n − 1`, so n flags are enough.",
                     {"c": "`calloc` gives n flags, all false."}),
                    ("mark", "Card `c` belongs in slot `c − lo`, which is between 0 and n − 1 (and fits in `int`, because the span check passed). A slot already taken means this value repeats.",
                     {"c": "`ok` stops the loop early but still lets us free the array afterwards."}),
                    ("ret", "n cards in n different slots: every value from `lo` to `hi` appears exactly once."),
                ],
                complexity=[
                    """
                    **Time O(n):** two passes over the cards, O(1) work each.

                    **Space O(n)** for the flags. (A hash set would also work, but array slots are simpler and
                    have no hashing cost.)
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - A run of consecutive values is pinned down by its **minimum and its length**. Check the span
              (`max − min == n − 1`) plus "no repeats", rather than sorting.
            - When values are known to lie in a small range `[lo, lo + n)`, a plain array indexed by
              `value − lo` replaces a hash set.
            - Spans and differences of 32-bit values can overflow: compute them in 64 bits.
            """
        ],
    )


@problem
def longest_chain_with_step():
    values, step = [10, 4, 1, 7, 5, 13, 8, 2, 20, 23], 3
    have = set(values)

    def chain_from(v):
        n = 1
        while v + n * step in have:
            n += 1
        return n

    best = max(chain_from(v) for v in have)
    assert best == 5

    w1 = Steps("Start a chain at every value and extend it as far as it goes.")
    w1.step("Step 3. Try every value as the first link.", Row(values, slots=True), Vars(best=0))
    bestsofar = 0
    for v in values:
        n = chain_from(v)
        bestsofar = max(bestsofar, n)
        links = [v + t * step for t in range(n)]
        st = {values.index(x): ("answer" if t == 0 else "found") for t, x in enumerate(links)}
        w1.step(f"From {v}: {' → '.join(map(str, links))} (then {v + n * step} is missing). Length {n}.", Row(values, st=st, slots=True), Vars(best=bestsofar))
    w1.step(f"The longest chain has {bestsofar} links. Note how 4, 7, 10 and 13 each re-walked part of the chain that 1 already walked.", Row(values, slots=True), result=bestsofar)

    w2 = Steps("Sort; each value's chain is one longer than the chain ending at value − step.")
    s = sorted(set(values))
    ln = {}
    w2.step(f"Sorted, without repeats: {s}. Process from left to right.", Row(s, slots=True))
    for i, v in enumerate(s):
        prev = ln.get(v - step)
        ln[v] = (prev or 0) + 1
        st = {i: "active"}
        if prev:
            st[s.index(v - step)] = "found"
        w2.step(f"{v}: is {v - step} to the left? " + (f"Yes, ending a chain of {prev}, so {v} ends a chain of {ln[v]}." if prev else f"No, so {v} starts a chain of 1."),
                Row(s, st=st, slots=True), Row([ln.get(x) for x in s], st={i: "new"}, label="chain length ending here", slots=True))
    w2.step(f"The largest length is {max(ln.values())}.", Row([ln[x] for x in s], st={s.index(13): "answer"}, label="chain length ending here", slots=True), result=max(ln.values()))

    w3 = Steps("Put every value in a set. Only walk from values that start a chain (value − step is missing).")
    order = list(dict.fromkeys(values))
    w3.step("All values go in a hash set.", Row(values, slots=True), Vars(best=0))
    bestsofar = 0
    for v in order:
        i = values.index(v)
        if v - step in have:
            w3.step(f"{v}: {v - step} is in the set, so {v} is in the middle of a chain. Skip it; the chain's head will count it.", Row(values, st={i: "dim", values.index(v - step): "mark"}, slots=True), Vars(best=bestsofar))
            continue
        n = chain_from(v)
        bestsofar = max(bestsofar, n)
        links = [v + t * step for t in range(n)]
        st = {values.index(x): ("answer" if t == 0 else "found") for t, x in enumerate(links)}
        w3.step(f"{v}: {v - step} isn't in the set, so a chain starts here: {' → '.join(map(str, links))}, length {n}.", Row(values, st=st, slots=True), Vars(best=bestsofar))
    w3.step(f"Each value was walked over at most once as part of a chain: best {bestsofar}.", Row(values, slots=True), result=bestsofar)

    sol(
        "longest-chain-with-step",
        summary="""
            Put the values in a hash set, and only start counting at a value whose predecessor
            `value − step` is **not** in the set: that value is the head of a chain. Walking forward from
            heads only means every value is visited about twice in total, so the whole thing is O(n).
        """,
        question=[
            """
            A chain is `v, v + step, v + 2·step, …`. From the numbers you're given (each used at most once,
            in any order), build the longest chain and return its length.

            - **Order in the input doesn't matter.** You pick the numbers; you don't need them to be next to
              each other in the list.
            - **Each number is used at most once**, and repeats don't help: `[2, 2, 2]` with step 5 gives
              chains of length 1, because 2 + 5 = 7 isn't there. Only *distinct* values matter.
            - **Steps can be large and values negative.** `step` goes up to 10⁹ and values to ±10⁹, so
              `value + step` can reach 2 × 10⁹, beyond the 32-bit `int`. Use 64-bit arithmetic for it in
              Java, C++ and C.
            - **Any single number is a chain of length 1**, so the answer is at least 1.
            - **Size:** up to 10⁵ values.
            """
        ],
        think=[
            """
            Take `values = [10, 4, 1, 7, 5, 13, 8, 2, 20, 23]` with `step = 3`.

            By hand, you'd notice runs like 1, 4, 7, 10, 13. Every value belongs to exactly one maximal
            chain (its next link is forced: `v + 3`; its previous link is forced: `v − 3`). Here the values
            split into these chains:
            """,
            fig(Row([1, 4, 7, 10, 13], st={0: "answer"}, label="length 5"), Row([2, 5, 8], st={0: "answer"}, label="length 3"), Row([20, 23], st={0: "answer"}, label="length 2"),
                caption="Shaded: each chain's head, the one value whose predecessor (value − 3) is missing."),
            """
            The key question is **where to start counting**. If you start at 7 you get 7, 10, 13 (length
            3), which undercounts and wastes time. If you start only at values whose predecessor is
            missing (1, 2 and 20 here), every chain is measured once and from its true start.

            And "is the predecessor missing?" and "is the next link present?" are both membership
            questions, which a hash set answers in O(1).
            """,
        ],
        approaches=[
            approach(
                "Extend a chain from every value",
                "brute",
                "O(n³)",
                "O(1)",
                idea=[
                    """
                    Treat every value as a possible first link. From `v`, look for `v + step` by scanning the
                    list; if it's there, look for `v + 2·step`, and so on. Keep the longest length found.

                    It's correct because the longest chain has some first value, and when the loop reaches
                    that value it walks the whole chain.
                    """
                ],
                walk=w1,
                build=[
                    "For each value `v`, set `length = 1` and `next = v + step`.",
                    "While `next` appears in the list (found by scanning), add 1 to `length` and move `next` up by `step`.",
                    "Keep the maximum `length` over all starting values.",
                ],
                code={
                    "python": """
                        class Solution:
                            def longestChain(self, values: List[int], step: int) -> int:
                                best = 0
                                for v in values:  #@start
                                    length, nxt = 1, v + step  #@start
                                    while nxt in values:  #@walk
                                        length += 1  #@walk
                                        nxt += step  #@walk
                                    best = max(best, length)  #@best
                                return best  #@best
                    """,
                    "java": """
                        class Solution {
                            public int longestChain(int[] values, int step) {
                                int best = 0;
                                for (int v : values) {  //@start
                                    int length = 1;  //@start
                                    long next = (long) v + step;  //@start
                                    while (contains(values, next)) {  //@walk
                                        length++;  //@walk
                                        next += step;  //@walk
                                    }
                                    best = Math.max(best, length);  //@best
                                }
                                return best;  //@best
                            }

                            private boolean contains(int[] values, long x) {  //@scan
                                for (int v : values) if (v == x) return true;  //@scan
                                return false;  //@scan
                            }  //@scan
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestChain(vector<int>& values, int step) {
                                auto contains = [&](long long x) {  //@scan
                                    for (int v : values) if (v == x) return true;  //@scan
                                    return false;  //@scan
                                };  //@scan
                                int best = 0;
                                for (int v : values) {  //@start
                                    int length = 1;  //@start
                                    long long next = (long long) v + step;  //@start
                                    while (contains(next)) {  //@walk
                                        length++;  //@walk
                                        next += step;  //@walk
                                    }
                                    best = max(best, length);  //@best
                                }
                                return best;  //@best
                            }
                        };
                    """,
                    "c": """
                        static bool contains(const int* values, int n, long long x) {  //@scan
                            for (int i = 0; i < n; i++) if (values[i] == x) return true;  //@scan
                            return false;  //@scan
                        }  //@scan

                        int longestChain(int* values, int valuesSize, int step) {
                            int best = 0;
                            for (int i = 0; i < valuesSize; i++) {  //@start
                                int length = 1;  //@start
                                long long next = (long long) values[i] + step;  //@start
                                while (contains(values, valuesSize, next)) {  //@walk
                                    length++;  //@walk
                                    next += step;  //@walk
                                }
                                best = length > best ? length : best;  //@best
                            }
                            return best;  //@best
                        }
                    """,
                },
                lines=[
                    ("scan", "A plain linear search: is `x` anywhere in the list? It takes a 64-bit `x` because chain links can go past `int` range (a value of 10⁹ plus a step of 10⁹)."),
                    ("start", "Every value gets a turn as the first link. The chain so far has length 1, and the link we want next is `v + step`.",
                     {"java": "`(long) v + step` so the sum can't overflow.", "cpp": "`(long long) v + step` so the sum can't overflow.", "c": "`(long long)` so the sum can't overflow."}),
                    ("walk", "While the next link exists, the chain grows by one and we look for the link after it.",
                     {"python": "`in` on a list scans it from the start each time."}),
                    ("best", "Keep the longest chain seen from any start."),
                ],
                complexity=[
                    """
                    **Time O(n³) in the worst case:** a chain of length n can be re-walked from each of its n
                    values, and each step of the walk scans n numbers.

                    **Space O(1).**
                    """
                ],
                limits=[
                    """
                    Two kinds of waste. Each membership check scans the list (fixable with sorting or a set),
                    and each chain is walked again from every value inside it (fixable by starting only at
                    chain heads). The next approach removes the first waste, the best approach removes both.
                    """
                ],
                slow=900,
            ),
            approach(
                "Sort, then build chain lengths left to right",
                "better",
                "O(n log n)",
                "O(n)",
                idea=[
                    """
                    Sort the distinct values in increasing order. A chain that ends at `v` is a chain that ends
                    at `v − step`, plus `v`. Since `v − step < v`, that chain was already measured when we got
                    here. So:

                    `len(v) = len(v − step) + 1` if `v − step` is among the values, else `1`.

                    Finding `v − step` in the sorted list is a binary search, and the answer is the largest
                    `len` seen. No hashing is needed.
                    """
                ],
                walk=w2,
                build=[
                    "Sort the values and drop repeats.",
                    "Keep `len[i]`, the length of the chain ending at sorted position `i`.",
                    "For each `i`, binary-search `s[i] − step` among positions `0 … i − 1`. Found at `j`: `len[i] = len[j] + 1`. Not found: `len[i] = 1`.",
                    "Return the largest `len[i]`.",
                ],
                code={
                    "python": """
                        from bisect import bisect_left

                        class Solution:
                            def longestChain(self, values: List[int], step: int) -> int:
                                s = sorted(set(values))  #@sort
                                length = [1] * len(s)  #@len
                                for i, v in enumerate(s):  #@loop
                                    j = bisect_left(s, v - step, 0, i)  #@search
                                    if j < i and s[j] == v - step:  #@extend
                                        length[i] = length[j] + 1  #@extend
                                return max(length)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestChain(int[] values, int step) {
                                long[] s = Arrays.stream(values).asLongStream().sorted().distinct().toArray();  //@sort
                                int[] length = new int[s.length];  //@len
                                int best = 0;
                                for (int i = 0; i < s.length; i++) {  //@loop
                                    int j = Arrays.binarySearch(s, 0, i, s[i] - step);  //@search
                                    length[i] = j >= 0 ? length[j] + 1 : 1;  //@extend
                                    best = Math.max(best, length[i]);  //@ret
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestChain(vector<int>& values, int step) {
                                vector<long long> s(values.begin(), values.end());  //@sort
                                sort(s.begin(), s.end());  //@sort
                                s.erase(unique(s.begin(), s.end()), s.end());  //@sort
                                vector<int> length(s.size(), 1);  //@len
                                int best = 0;
                                for (int i = 0; i < (int) s.size(); i++) {  //@loop
                                    auto it = lower_bound(s.begin(), s.begin() + i, s[i] - step);  //@search
                                    if (it != s.begin() + i && *it == s[i] - step) {  //@extend
                                        length[i] = length[it - s.begin()] + 1;  //@extend
                                    }
                                    best = max(best, length[i]);  //@ret
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpLong(const void* x, const void* y) {  //@cmp
                            long long p = *(const long long*) x, q = *(const long long*) y;  //@cmp
                            return (p > q) - (p < q);  //@cmp
                        }  //@cmp

                        int longestChain(int* values, int valuesSize, int step) {
                            long long* s = malloc(valuesSize * sizeof(long long));  //@sort
                            for (int i = 0; i < valuesSize; i++) s[i] = values[i];  //@sort
                            qsort(s, valuesSize, sizeof(long long), cmpLong);  //@sort
                            int m = 0;  //@sort
                            for (int i = 0; i < valuesSize; i++) if (m == 0 || s[i] != s[m - 1]) s[m++] = s[i];  //@sort
                            int* length = malloc(m * sizeof(int));  //@len
                            int best = 0;
                            for (int i = 0; i < m; i++) {  //@loop
                                long long want = s[i] - step;  //@search
                                int lo = 0, hi = i;  //@search
                                while (lo < hi) {  //@search
                                    int mid = (lo + hi) / 2;  //@search
                                    if (s[mid] < want) lo = mid + 1; else hi = mid;  //@search
                                }  //@search
                                length[i] = (lo < i && s[lo] == want) ? length[lo] + 1 : 1;  //@extend
                                if (length[i] > best) best = length[i];  //@ret
                            }
                            free(s);  //@ret
                            free(length);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("cmp", "Comparator for `qsort` over 64-bit values, returning −1, 0 or 1."),
                    ("sort", "Sorted distinct values, stored as 64-bit so `value − step` can be computed without overflow (it can go down to −2 × 10⁹).",
                     {"python": "`set` drops repeats, `sorted` orders them. Python integers never overflow.",
                      "java": "The stream widens to `long`, sorts and removes repeats in one line.",
                      "cpp": "Copy into `long long`, sort, then `unique` + `erase` removes adjacent repeats.",
                      "c": "Copy into `long long`, sort, then compact the array in place keeping only the first of each run of equal values; `m` is the new length."}),
                    ("len", "`length[i]` will be the longest chain ending at `s[i]`. Every value alone is a chain of 1."),
                    ("loop", "Left to right, so every smaller value is finished before it's needed."),
                    ("search", "Binary-search the predecessor link `s[i] − step` among the values to the left.",
                     {"java": "`Arrays.binarySearch(s, 0, i, key)` returns the index when found and a negative number when not.",
                      "cpp": "`lower_bound` finds the first position not less than the key in `[0, i)`.",
                      "c": "A hand-written lower bound over `[0, i)`."}),
                    ("extend", "If the predecessor exists, this value extends its chain by one; otherwise it starts a new chain (length stays 1)."),
                    ("ret", "The answer is the longest chain ending anywhere.", {"c": "Free both arrays before returning."}),
                ],
                complexity=[
                    """
                    **Time O(n log n):** the sort, plus one O(log n) binary search per value.

                    **Space O(n):** the sorted copy and the lengths.
                    """
                ],
                limits=[
                    """
                    Fast and dependable, but the sort does more than needed: we only ever ask "is `v − step`
                    present?" and "is `v + step` present?", which a hash set answers in O(1) without ordering
                    anything.
                    """
                ],
            ),
            approach(
                "Hash set, walking only from chain heads",
                "best",
                "O(n)",
                "O(n)",
                idea=[
                    """
                    Put all values in a hash set. For each distinct value `v`:

                    - If `v − step` is in the set, `v` is not a head: some chain reaches it from below. Skip it.
                    - Otherwise `v` is a head. Walk `v + step`, `v + 2·step`, … while they're in the set, and
                      count the links.

                    Each value is the head of exactly one chain and is walked over only by that chain's walk,
                    so all the walks together take O(n) steps, even though there's a loop inside a loop.
                    """
                ],
                walk=w3,
                build=[
                    "Build a hash set of the values (64-bit keys in Java and C).",
                    "For each distinct value `v`: if `v − step` is in the set, skip it.",
                    "Otherwise walk forward from `v` while `x + step` is in the set, counting the links.",
                    "Keep the longest walk.",
                ],
                code={
                    "python": """
                        class Solution:
                            def longestChain(self, values: List[int], step: int) -> int:
                                have = set(values)  #@build
                                best = 0
                                for v in have:  #@each
                                    if v - step in have:  #@head
                                        continue  #@head
                                    length, x = 1, v  #@walk
                                    while x + step in have:  #@walk
                                        x += step  #@walk
                                        length += 1  #@walk
                                    best = max(best, length)  #@best
                                return best  #@best
                    """,
                    "java": """
                        class Solution {
                            public int longestChain(int[] values, int step) {
                                Set<Long> have = new HashSet<>();  //@build
                                for (int v : values) have.add((long) v);  //@build
                                int best = 0;
                                for (long v : have) {  //@each
                                    if (have.contains(v - step)) continue;  //@head
                                    int length = 1;  //@walk
                                    long x = v;  //@walk
                                    while (have.contains(x + step)) {  //@walk
                                        x += step;  //@walk
                                        length++;  //@walk
                                    }
                                    best = Math.max(best, length);  //@best
                                }
                                return best;  //@best
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestChain(vector<int>& values, int step) {
                                unordered_set<long long> have(values.begin(), values.end());  //@build
                                int best = 0;
                                for (long long v : have) {  //@each
                                    if (have.count(v - step)) continue;  //@head
                                    int length = 1;  //@walk
                                    long long x = v;  //@walk
                                    while (have.count(x + step)) {  //@walk
                                        x += step;  //@walk
                                        length++;  //@walk
                                    }
                                    best = max(best, length);  //@best
                                }
                                return best;  //@best
                            }
                        };
                    """,
                    "c": C_SET + """
                        int longestChain(int* values, int valuesSize, int step) {
                            unsigned cap = 1;  //@build
                            while (cap < 2u * valuesSize) cap <<= 1;  //@build
                            Slot* have = calloc(cap, sizeof(Slot));  //@build
                            for (int i = 0; i < valuesSize; i++) add(have, cap - 1, values[i]);  //@build
                            int best = 0;
                            for (unsigned s = 0; s < cap; s++) {  //@each
                                if (!have[s].used) continue;  //@each
                                long long v = have[s].key;  //@each
                                if (has(have, cap - 1, v - step)) continue;  //@head
                                int length = 1;  //@walk
                                long long x = v;  //@walk
                                while (has(have, cap - 1, x + step)) {  //@walk
                                    x += step;  //@walk
                                    length++;  //@walk
                                }
                                if (length > best) best = length;  //@best
                            }
                            free(have);  //@best
                            return best;  //@best
                        }
                    """,
                },
                lines=[
                    C_SET_ROW,
                    ("build", "Every value goes into a hash set, so membership checks are O(1). Repeats collapse into one entry.",
                     {"java": "`Long` keys, because we'll look up `v ± step`, which can leave `int` range.",
                      "cpp": "`long long` keys, because we'll look up `v ± step`, which can leave `int` range.",
                      "c": "A table at least twice the number of values, zeroed by `calloc`, then every value added."}),
                    ("each", "Consider each **distinct** value as a possible chain head. Looping over the set (not the input) matters: with many copies of a head, looping over the input would walk its chain once per copy.",
                     {"c": "Walk the table's slots and skip the empty ones: the used slots are exactly the distinct values."}),
                    ("head", "If the value one step below is present, this value sits inside a longer chain. Its chain will be measured from the head, so skip it."),
                    ("walk", "A head: count links upward until one is missing."),
                    ("best", "Keep the longest chain.", {"c": "Free the table before returning."}),
                ],
                complexity=[
                    """
                    **Time O(n) on average.** The skip test costs O(1) per value. A walk only starts at a
                    head and only steps through that head's own chain, and the chains don't overlap, so all
                    walks together take at most n steps.

                    **Space O(n)** for the set.
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - For "longest run of linked values" problems, **only start at the beginning of a run**: a value
              whose predecessor is missing. It turns a quadratic re-walk into a linear one.
            - A loop inside a loop can still be O(n) when the inner loop's total work across all iterations is
              bounded. Count total work, not nesting depth.
            - Sorting + binary search is a solid hash-free fallback: it costs a log factor.
            """
        ],
    )
