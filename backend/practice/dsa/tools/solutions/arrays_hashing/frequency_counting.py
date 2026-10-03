"""Arrays & Hashing: frequency counting."""
from collections import Counter

import textwrap

from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

C_INT_SET = """
    // C has no built-in hash set, so here is a small one: open addressing with
    // linear probing over a power-of-two table.
    typedef struct { int key; bool used; } Slot;  //@set

    static unsigned slotOf(int key, unsigned mask) {  //@set
        unsigned long long h = (unsigned long long) (long long) key * 0x9E3779B97F4A7C15ULL;  //@set
        return (unsigned) (h >> 32) & mask;  //@set
    }  //@set
"""
C_INT_SET = textwrap.indent(C_INT_SET, " " * 20)  # match the code strings it is joined to



@problem
def duplicate_badges():
    badges = [12, 5, 9, 2, 5, 8]

    w1 = Steps("Compare every badge with every badge after it.")
    found = None
    for i in range(len(badges)):
        later = list(range(i + 1, len(badges)))
        hit = next((j for j in later if badges[j] == badges[i]), None)
        st = {q: "dim" for q in range(i)}
        st[i] = "active"
        if hit is None:
            for j in later:
                st[j] = "mark"
            w1.step(f"Badge {badges[i]} (index {i}) against the {len(later)} after it: no match.", Row(badges, st=st, ptr={"i": i}, slots=True))
        else:
            for j in later:
                if j < hit:
                    st[j] = "mark"
            st[i] = st[hit] = "answer"
            w1.step(f"Badge {badges[i]} (index {i}) matches index {hit}. Duplicate.", Row(badges, st=st, ptr={"i": i, "j": hit}, slots=True), result=True)
            found = True
            break
    assert found

    w2 = Steps("Sort a copy; equal numbers end up side by side.")
    s = sorted(badges)
    w2.step(f"Sorted: {s}.", Row(badges, label="badges"), Row(s, label="sorted", slots=True))
    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            w2.step(f"{s[i]} and {s[i + 1]} are neighbours and equal. Duplicate.", Row(s, st={i: "answer", i + 1: "answer"}, slots=True), result=True)
            break
        w2.step(f"{s[i]} ≠ {s[i + 1]}.", Row(s, st={i: "active", i + 1: "active"}, slots=True))

    w3 = Steps("Remember every badge seen so far in a hash set.")
    seen = []
    for i, b in enumerate(badges):
        st = {q: "dim" for q in range(i)}
        if b in seen:
            st[i] = "answer"
            w3.step(f"{b} is already in the set. Duplicate.", Row(badges, st=st, slots=True), Row(seen, st={seen.index(b): "answer"}, label="seen"), result=True)
            break
        st[i] = "active"
        seen.append(b)
        w3.step(f"{b} is new: add it.", Row(badges, st=st, slots=True), Row(list(seen), st={len(seen) - 1: "new"}, label="seen"))

    sol(
        "duplicate-badges",
        summary="""
            Walk through the badges once while remembering every number seen in a hash set. The first number
            that's already in the set is a duplicate. That's O(n) time, against O(n²) for comparing all pairs
            and O(n log n) for sorting.
        """,
        question=[
            """
            Return `true` if any number appears **at least twice** in the list, otherwise `false`.

            - **Any repeat counts**, anywhere in the list, not just next to each other.
            - **One badge** can't repeat: `[5]` is `false`.
            - **Negative numbers** are allowed, so tricks that use the numbers as array indices don't work
              directly (values go from −10⁹ to 10⁹).
            - **Size:** up to 10⁵ badges. Comparing every pair is ~5 × 10⁹ comparisons.
            - You can **stop at the first repeat**: the answer is just yes or no.
            """
        ],
        think=[
            """
            Take `[12, 5, 9, 2, 5, 8]`. Reading it left to right as a person would, you keep a mental list of
            numbers you've passed: 12, 5, 9, 2… then another 5. "I've seen 5." Done.

            That mental list is the whole algorithm. The question is only how quickly you can check "have I
            seen this?":

            - scanning everything before it costs O(n) per check, O(n²) in total;
            - sorting first puts equal numbers next to each other, so a single neighbour check finds them;
            - a hash set answers "seen it?" in O(1) on average.
            """,
            fig(Row(badges, st={1: "answer", 4: "answer"}, slots=True), caption="The repeat is at indices 1 and 4, three places apart."),
        ],
        approaches=[
            approach(
                "Compare every pair",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["Check every pair `i < j`. If any two are equal, return true. If no pair matches, return false."],
                walk=w1,
                build=["Loop `i` over indices and `j` from `i + 1` to the end.", "If `badges[i] == badges[j]`, return true.", "After the loops, return false."],
                code={
                    "python": """
                        class Solution:
                            def hasDuplicate(self, badges: List[int]) -> bool:
                                n = len(badges)
                                for i in range(n):  #@loops
                                    for j in range(i + 1, n):  #@loops
                                        if badges[i] == badges[j]:  #@test
                                            return True  #@test
                                return False  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean hasDuplicate(int[] badges) {
                                int n = badges.length;
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        if (badges[i] == badges[j]) return true;  //@test
                                return false;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool hasDuplicate(vector<int>& badges) {
                                int n = badges.size();
                                for (int i = 0; i < n; i++)  //@loops
                                    for (int j = i + 1; j < n; j++)  //@loops
                                        if (badges[i] == badges[j]) return true;  //@test
                                return false;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool hasDuplicate(int* badges, int badgesSize) {
                            for (int i = 0; i < badgesSize; i++)  //@loops
                                for (int j = i + 1; j < badgesSize; j++)  //@loops
                                    if (badges[i] == badges[j]) return true;  //@test
                            return false;  //@ret
                        }
                    """,
                },
                lines=[
                    ("loops", "Every pair of different positions, each pair once."),
                    ("test", "Two equal badges: that's a duplicate, and nothing else needs checking."),
                    ("ret", "No pair matched, so every number is different."),
                ],
                complexity=["**Time O(n²):** n(n − 1)/2 comparisons. **Space O(1).**"],
                limits=["The \"have I seen this?\" question is answered by re-reading the list. Sorting or a hash set answers it far faster."],
                slow=True,
            ),
            approach(
                "Sort, then check neighbours",
                "better",
                "O(n log n)",
                "O(n)",
                idea=["After sorting, equal numbers are adjacent, so a duplicate exists exactly when some neighbouring pair is equal."],
                walk=w2,
                build=["Sort a copy of the badges.", "Return true if any `s[i] == s[i + 1]`, else false."],
                code={
                    "python": """
                        class Solution:
                            def hasDuplicate(self, badges: List[int]) -> bool:
                                s = sorted(badges)  #@sort
                                for i in range(len(s) - 1):  #@scan
                                    if s[i] == s[i + 1]:  #@scan
                                        return True  #@scan
                                return False  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean hasDuplicate(int[] badges) {
                                int[] s = badges.clone();  //@sort
                                Arrays.sort(s);  //@sort
                                for (int i = 0; i + 1 < s.length; i++) {  //@scan
                                    if (s[i] == s[i + 1]) return true;  //@scan
                                }
                                return false;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool hasDuplicate(vector<int>& badges) {
                                vector<int> s = badges;  //@sort
                                sort(s.begin(), s.end());  //@sort
                                for (size_t i = 0; i + 1 < s.size(); i++) {  //@scan
                                    if (s[i] == s[i + 1]) return true;  //@scan
                                }
                                return false;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@cmp
                            int p = *(const int*) a, q = *(const int*) b;  //@cmp
                            return (p > q) - (p < q);  //@cmp
                        }  //@cmp

                        bool hasDuplicate(int* badges, int badgesSize) {
                            int* s = malloc(badgesSize * sizeof(int));  //@sort
                            memcpy(s, badges, badgesSize * sizeof(int));  //@sort
                            qsort(s, badgesSize, sizeof(int), cmpInt);  //@sort
                            bool dup = false;  //@scan
                            for (int i = 0; i + 1 < badgesSize && !dup; i++) dup = s[i] == s[i + 1];  //@scan
                            free(s);  //@ret
                            return dup;  //@ret
                        }
                    """,
                },
                lines=[
                    ("cmp", "Comparator for `qsort`, safe for values near ±10⁹ (no subtraction)."),
                    ("sort", "Sort a copy so equal numbers become neighbours, leaving the input untouched."),
                    ("scan", "Only neighbours need comparing now: if a number repeats, one of its copies sits right next to another."),
                    ("ret", "No equal neighbours means no repeats.", {"c": "Free the copy, then return."}),
                ],
                complexity=["**Time O(n log n)** for the sort. **Space O(n)** for the copy (O(1) extra if sorting the input in place is allowed)."],
                limits=["Sorting orders every number, which is more than \"is anything repeated?\" needs. A hash set skips the ordering and can stop at the first repeat without reading the rest."],
            ),
            approach(
                "Hash set of numbers seen",
                "best",
                "O(n)",
                "O(n)",
                idea=["Walk left to right with a hash set. If the current badge is already in the set, return true; otherwise add it. If the walk ends, every badge was new."],
                walk=w3,
                build=["Create an empty hash set.", "For each badge: if it's in the set, return true; else add it.", "Return false."],
                code={
                    "python": """
                        class Solution:
                            def hasDuplicate(self, badges: List[int]) -> bool:
                                seen = set()  #@init
                                for b in badges:  #@loop
                                    if b in seen:  #@check
                                        return True  #@check
                                    seen.add(b)  #@add
                                return False  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean hasDuplicate(int[] badges) {
                                Set<Integer> seen = new HashSet<>();  //@init
                                for (int b : badges) {  //@loop
                                    if (!seen.add(b)) return true;  //@check
                                }
                                return false;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool hasDuplicate(vector<int>& badges) {
                                unordered_set<int> seen;  //@init
                                for (int b : badges) {  //@loop
                                    if (!seen.insert(b).second) return true;  //@check
                                }
                                return false;  //@ret
                            }
                        };
                    """,
                    "c": C_INT_SET + """
                        bool hasDuplicate(int* badges, int badgesSize) {
                            unsigned cap = 1;  //@init
                            while (cap < 2u * badgesSize) cap <<= 1;  //@init
                            Slot* seen = calloc(cap, sizeof(Slot));  //@init
                            bool dup = false;  //@init
                            for (int i = 0; i < badgesSize && !dup; i++) {  //@loop
                                unsigned s = slotOf(badges[i], cap - 1);  //@check
                                while (seen[s].used && seen[s].key != badges[i]) s = (s + 1) & (cap - 1);  //@check
                                if (seen[s].used) dup = true;  //@check
                                else seen[s] = (Slot) {badges[i], true};  //@add
                            }
                            free(seen);  //@ret
                            return dup;  //@ret
                        }
                    """,
                },
                lines=[
                    ("set", "C has no hash set, so here's a minimal one: each slot holds a key and an in-use flag. `slotOf` scrambles a key into a starting slot by multiplying by a large odd constant and keeping the well-mixed high bits."),
                    ("init", "An empty set of numbers seen so far.", {"c": "A power-of-two table at least twice the number of badges, zeroed by `calloc` (every slot unused). `dup` lets the loop stop early and still free the table."}),
                    ("loop", "One pass over the badges."),
                    ("check", "Seen before? Then it's a duplicate.",
                     {"java": "`add` returns false when the value was already present: one call both checks and inserts.",
                      "cpp": "`insert` returns a pair whose `.second` is false when the value was already present.",
                      "c": "Probe from the badge's slot, stepping forward past other keys. A used slot holding our key means seen; an empty slot means new."}),
                    ("add", "First time: remember it.", {"c": "Claim the empty slot the probe stopped at."}),
                    ("ret", "Every badge was new.", {"c": "Free the table, then return."}),
                ],
                complexity=["**Time O(n)** on average: one O(1) check and insert per badge, and it stops early at the first repeat. **Space O(n)** for the set."],
            ),
        ],
        takeaways=[
            """
            - "Have I seen this before?" is a hash-set question: O(1) per check.
            - Sorting turns "equal somewhere" into "equal neighbours", a good fallback when extra memory is
              tight.
            - Stop as soon as the answer is known; a yes/no question rarely needs the whole input.
            """
        ],
    )


@problem
def letter_tiles():
    sign, tiles = "spoon", "nopxos"

    w1 = Steps("For each letter of the sign, find a matching tile and take it out of the pool.")
    pool = list(tiles)
    w1.step("The pool starts as all the tiles.", Row(list(sign), label="sign"), Row(list(pool), label="pool"))
    for i, ch in enumerate(sign):
        j = pool.index(ch)
        w1.step(f"'{ch}': scan the pool, found at position {j}. Remove it.", Row(list(sign), st={**{q: "found" for q in range(i)}, i: "active"}, label="sign"), Row(list(pool), st={j: "answer"}, label="pool"))
        pool.pop(j)
    w1.step(f"Every letter found a tile; '{''.join(pool)}' is left over.", Row(list(sign), st={q: "found" for q in range(len(sign))}, label="sign"), Row(pool, label="pool"), result=True)

    w2 = Steps("Sort both strings, then walk them together like merging.")
    ss, st_ = sorted(sign), sorted(tiles)
    w2.step("Sorted, equal letters group together and both strings run in the same order.", Row(ss, label="sign (sorted)"), Row(st_, label="tiles (sorted)"))
    j = 0
    for i, ch in enumerate(ss):
        skipped = []
        while j < len(st_) and st_[j] < ch:
            skipped.append(j)
            j += 1
        w2.step(f"Need '{ch}'" + (f": skip unused tile{'s' if len(skipped) > 1 else ''} {', '.join(repr(st_[q]) for q in skipped)}" if skipped else "") + f"; tile {j} is '{st_[j]}'. Match.",
                Row(ss, st={**{q: "found" for q in range(i)}, i: "active"}, label="sign (sorted)"), Row(st_, st={**{q: "dim" for q in skipped}, j: "answer"}, ptr={"j": j}, label="tiles (sorted)"))
        j += 1
    w2.step("Every sign letter was matched.", Row(ss, st={q: "found" for q in range(len(ss))}, label="sign (sorted)"), result=True)

    w3 = Steps("Count the tiles by letter, then spend one count per sign letter.")
    have = Counter(tiles)
    keys = sorted(have)
    w3.step("Tile counts per letter.", Row(list(tiles), label="tiles"), Row([f"{c}:{have[c]}" for c in keys], label="count"))
    for i, ch in enumerate(sign):
        have[ch] -= 1
        w3.step(f"'{ch}': count drops to {have[ch]}" + (" — still ≥ 0." if have[ch] >= 0 else " — below 0, fail."), Row(list(sign), st={**{q: "found" for q in range(i)}, i: "active"}, label="sign"), Row([f"{c}:{have[c]}" for c in keys], st={keys.index(ch): "new"}, label="count"))
    w3.step("No count went negative: the sign can be spelled. ('boom' with tiles 'bomx' would push o to −1 at its second o.)", Row([f"{c}:{have[c]}" for c in keys], label="count"), result=True)

    sol(
        "letter-tiles",
        summary="""
            Order doesn't matter, only **how many of each letter** there are. Count the tiles per letter (26
            counters), then spend one count for every letter of the sign; if any count goes below zero, a tile
            is missing. O(sign + tiles) time, O(1) space.
        """,
        question=[
            """
            Can the sign be spelled from the tiles, each tile used at most once?

            - **Order is irrelevant.** Tiles can be rearranged freely; `sale` from `eslax` works.
            - **Multiplicity matters.** `boom` needs **two** `o` tiles; `bomx` has one, so it fails.
            - **Extra tiles are fine:** the `x` in `eslax` is simply left over.
            - **Only lowercase letters**, so there are just 26 kinds of tile, which means a fixed-size count
              array works.
            - **Size:** both strings up to 10⁵ characters.
            """
        ],
        think=[
            """
            Take sign `spoon` and tiles `nopxos`. By hand you'd lay the tiles out by letter: n×1, o×2, p×1,
            s×1, x×1. Then read the sign and take a tile per letter: s, p, o, o (the second o!), n. Every letter
            found a tile, so it works.
            """,
            fig(Row(["n:1", "o:2", "p:1", "s:1", "x:1"], label="tiles by letter"), Row(["n:1", "o:2", "p:1", "s:1"], label="sign needs"),
                caption="For each letter, tiles available ≥ letters needed. That's the whole condition."),
            """
            So the question is "for every letter, is `count in tiles ≥ count in sign`?". Counting both and
            comparing works; slightly simpler is to count the tiles and then **subtract** as you read the sign,
            failing the moment a count goes negative.
            """,
        ],
        approaches=[
            approach(
                "Take tiles out of a pool",
                "brute",
                "O(s · t)",
                "O(t)",
                idea=["Copy the tiles into a pool. For each sign letter, scan the pool for that letter; if it's missing return false, otherwise remove that tile so it can't be used twice."],
                walk=w1,
                build=["Copy the tiles into a mutable pool.", "For each letter of the sign: find it in the pool; if absent return false; else remove it.", "Return true."],
                code={
                    "python": """
                        class Solution:
                            def canSpell(self, sign: str, tiles: str) -> bool:
                                pool = list(tiles)  #@pool
                                for ch in sign:  #@loop
                                    if ch not in pool:  #@find
                                        return False  #@find
                                    pool.remove(ch)  #@take
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean canSpell(String sign, String tiles) {
                                char[] pool = tiles.toCharArray();  //@pool
                                for (char ch : sign.toCharArray()) {  //@loop
                                    int at = -1;  //@find
                                    for (int i = 0; i < pool.length && at < 0; i++) if (pool[i] == ch) at = i;  //@find
                                    if (at < 0) return false;  //@find
                                    pool[at] = '#';  //@take
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool canSpell(string& sign, string& tiles) {
                                string pool = tiles;  //@pool
                                for (char ch : sign) {  //@loop
                                    size_t at = pool.find(ch);  //@find
                                    if (at == string::npos) return false;  //@find
                                    pool[at] = '#';  //@take
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool canSpell(char* sign, char* tiles) {
                            size_t t = strlen(tiles);  //@pool
                            char* pool = malloc(t + 1);  //@pool
                            memcpy(pool, tiles, t + 1);  //@pool
                            bool ok = true;  //@loop
                            for (char* p = sign; *p && ok; p++) {  //@loop
                                char* at = strchr(pool, *p);  //@find
                                if (!at) ok = false;  //@find
                                else *at = '#';  //@take
                            }
                            free(pool);  //@ret
                            return ok;  //@ret
                        }
                    """,
                },
                lines=[
                    ("pool", "A copy of the tiles we can use up.", {"c": "Copy including the terminating `\\0` so string functions work on the pool."}),
                    ("loop", "Each letter of the sign, in order."),
                    ("find", "Look for a tile with this letter. None left means the sign can't be spelled.",
                     {"cpp": "`find` returns `npos` when the letter isn't in the pool.", "c": "`strchr` returns a pointer to the first match, or NULL."}),
                    ("take", "Use that tile up so it can't be reused.",
                     {"java": "Overwrite it with `#`, which no sign letter can match; cheaper than removing it.",
                      "cpp": "Overwrite it with `#`, which no sign letter can match.",
                      "c": "Overwrite it with `#`, which no sign letter can match."}),
                    ("ret", "Every letter got its own tile.", {"c": "Free the pool and return."}),
                ],
                complexity=["**Time O(s · t):** each sign letter scans up to t tiles (10¹⁰ at the limits). **Space O(t)** for the pool."],
                limits=["Each lookup scans the tiles one by one, but we never care *which* `o` tile we take, only how many `o`s are left. Counting replaces the search."],
                slow=True,
            ),
            approach(
                "Sort both, then walk them together",
                "better",
                "O(s log s + t log t)",
                "O(s + t)",
                idea=["Sort both strings. Walk the sorted sign; for each letter move a tile pointer forward past smaller letters (unused tiles). If the pointer runs out or lands on a bigger letter, the needed tile doesn't exist. Otherwise use it and step past it."],
                walk=w2,
                build=["Sort the sign and the tiles.", "Keep `j` = 0 in the sorted tiles.", "For each sign letter `ch`: skip tiles `< ch`; if no tile or tile `!= ch`, return false; else `j += 1`.", "Return true."],
                code={
                    "python": """
                        class Solution:
                            def canSpell(self, sign: str, tiles: str) -> bool:
                                s, t = sorted(sign), sorted(tiles)  #@sort
                                j = 0  #@walk
                                for ch in s:  #@walk
                                    while j < len(t) and t[j] < ch:  #@skip
                                        j += 1  #@skip
                                    if j == len(t) or t[j] != ch:  #@match
                                        return False  #@match
                                    j += 1  #@match
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean canSpell(String sign, String tiles) {
                                char[] s = sign.toCharArray(), t = tiles.toCharArray();  //@sort
                                Arrays.sort(s);  //@sort
                                Arrays.sort(t);  //@sort
                                int j = 0;  //@walk
                                for (char ch : s) {  //@walk
                                    while (j < t.length && t[j] < ch) j++;  //@skip
                                    if (j == t.length || t[j] != ch) return false;  //@match
                                    j++;  //@match
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool canSpell(string& sign, string& tiles) {
                                string s = sign, t = tiles;  //@sort
                                sort(s.begin(), s.end());  //@sort
                                sort(t.begin(), t.end());  //@sort
                                size_t j = 0;  //@walk
                                for (char ch : s) {  //@walk
                                    while (j < t.size() && t[j] < ch) j++;  //@skip
                                    if (j == t.size() || t[j] != ch) return false;  //@match
                                    j++;  //@match
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpChar(const void* a, const void* b) {  //@cmp
                            return *(const char*) a - *(const char*) b;  //@cmp
                        }  //@cmp

                        bool canSpell(char* sign, char* tiles) {
                            size_t n = strlen(sign), m = strlen(tiles);  //@sort
                            char* s = malloc(n + 1);  //@sort
                            char* t = malloc(m + 1);  //@sort
                            memcpy(s, sign, n + 1);  //@sort
                            memcpy(t, tiles, m + 1);  //@sort
                            qsort(s, n, 1, cmpChar);  //@sort
                            qsort(t, m, 1, cmpChar);  //@sort
                            size_t j = 0;  //@walk
                            bool ok = true;  //@walk
                            for (size_t i = 0; i < n && ok; i++) {  //@walk
                                while (j < m && t[j] < s[i]) j++;  //@skip
                                if (j == m || t[j] != s[i]) ok = false;  //@match
                                else j++;  //@match
                            }
                            free(s);  //@ret
                            free(t);  //@ret
                            return ok;  //@ret
                        }
                    """,
                },
                lines=[
                    ("cmp", "Compare two characters for `qsort`. Letters are small codes, so subtracting them can't overflow."),
                    ("sort", "Sorted copies: equal letters are grouped, and both strings run a → z."),
                    ("walk", "`j` marks the first tile not yet used or skipped."),
                    ("skip", "Tiles smaller than the needed letter can never be used later either (later sign letters are only bigger or equal), so skip them for good."),
                    ("match", "The next tile must be exactly this letter. If it's missing or bigger, no such tile is left. Otherwise use it."),
                    ("ret", "All sign letters were matched.", {"c": "Free both copies."}),
                ],
                complexity=["**Time O(s log s + t log t)** for sorting; the walk is linear. **Space O(s + t)** for the sorted copies."],
                limits=["Sorting is overkill with only 26 possible letters: 26 counters give the same information in one pass and constant space."],
            ),
            approach(
                "26 counters",
                "best",
                "O(s + t)",
                "O(1)",
                idea=["Count each letter among the tiles in an array of 26. Then for each sign letter subtract one from its counter; if a counter drops below zero, the sign needs more of that letter than there are tiles."],
                walk=w3,
                build=["Make `have` with 26 zeros; add 1 for each tile letter (`letter − 'a'` is its index).", "For each sign letter: subtract 1; if the counter is now negative, return false.", "Return true."],
                code={
                    "python": """
                        class Solution:
                            def canSpell(self, sign: str, tiles: str) -> bool:
                                have = [0] * 26  #@count
                                for ch in tiles:  #@count
                                    have[ord(ch) - ord('a')] += 1  #@count
                                for ch in sign:  #@spend
                                    k = ord(ch) - ord('a')  #@spend
                                    have[k] -= 1  #@spend
                                    if have[k] < 0:  #@check
                                        return False  #@check
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean canSpell(String sign, String tiles) {
                                int[] have = new int[26];  //@count
                                for (char ch : tiles.toCharArray()) have[ch - 'a']++;  //@count
                                for (char ch : sign.toCharArray()) {  //@spend
                                    if (--have[ch - 'a'] < 0) return false;  //@check
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool canSpell(string& sign, string& tiles) {
                                int have[26] = {0};  //@count
                                for (char ch : tiles) have[ch - 'a']++;  //@count
                                for (char ch : sign) {  //@spend
                                    if (--have[ch - 'a'] < 0) return false;  //@check
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool canSpell(char* sign, char* tiles) {
                            int have[26] = {0};  //@count
                            for (char* p = tiles; *p; p++) have[*p - 'a']++;  //@count
                            for (char* p = sign; *p; p++) {  //@spend
                                if (--have[*p - 'a'] < 0) return false;  //@check
                            }
                            return true;  //@ret
                        }
                    """,
                },
                lines=[
                    ("count", "One counter per letter. `ch − 'a'` maps 'a' → 0, …, 'z' → 25.", {"c": "Walk the string until its terminating `\\0`."}),
                    ("spend", "Use up one tile of each letter the sign needs."),
                    ("check", "Negative means this letter appears more often in the sign than among the tiles.",
                     {"java": "`--have[k]` decrements first, then the comparison sees the new value.", "cpp": "`--have[k]` decrements first, then compares.", "c": "`--have[k]` decrements first, then compares."}),
                    ("ret", "No letter ran out."),
                ],
                complexity=["**Time O(s + t):** one pass over each string. **Space O(1):** 26 counters regardless of input size."],
            ),
        ],
        takeaways=[
            """
            - "Can A be built from B?" with reusable order is a **multiset** question: compare counts, not
              positions.
            - A small fixed alphabet means a fixed-size array beats a hash map: O(1) space, no hashing.
            - Counting up one side and down the other, failing on a negative, avoids a second comparison
              pass.
            """
        ],
    )


@problem
def loudest_letters_first():
    s = "banana12b"
    cnt = Counter(s)
    order = sorted(cnt, key=lambda c: (-cnt[c], c))
    out = "".join(c * cnt[c] for c in order)
    assert out == "aaabbnn12"

    w1 = Steps("Repeatedly pick the remaining character with the most copies (counting with a full scan each time).")
    left = sorted(set(s))
    res = ""
    w1.step("Remaining characters in code order: digits, then letters.", Row(list(s), slots=True), Row(left, label="remaining"))
    while left:
        best = left[0]
        for c in left:
            if s.count(c) > s.count(best):
                best = c
        res += best * s.count(best)
        w1.step(f"Count each remaining character by scanning s: '{best}' wins with {s.count(best)}. Append it.", Row(left, st={left.index(best): "answer"}, label="remaining"), Vars(output=res))
        left.remove(best)
    w1.step(f"Result: {res}.", Row(list(res)), result=res)

    w2 = Steps("Count once, sort the distinct characters by (count high → low, code low → high), write them out.")
    keys = sorted(cnt)
    w2.step("Counts per character.", Row(list(s), slots=True), Row([f"{c}:{cnt[c]}" for c in keys], label="count"))
    w2.step(f"Sorted by count, ties by code: {' '.join(order)}.", Row([f"{c}:{cnt[c]}" for c in order], label="order"))
    res = ""
    for i, c in enumerate(order):
        res += c * cnt[c]
        w2.step(f"Write '{c}' × {cnt[c]}.", Row([f"{c}:{cnt[c]}" for c in order], st={i: "active", **{q: "found" for q in range(i)}}, label="order"), Vars(output=res))
    w2.step(f"Result: {res}.", Row(list(res)), result=res)

    w3 = Steps("Bucket characters by their count. Read buckets from the highest count down.")
    n = len(s)
    buckets = {k: [c for c in sorted(cnt) if cnt[c] == k] for k in range(1, n + 1)}
    used = [k for k in range(n, 0, -1) if buckets[k]]
    w3.step(f"Characters visited in code order land in bucket[count]: " + ", ".join(f"{k}→{''.join(buckets[k])}" for k in sorted(used)) + ".", Row([("".join(buckets[k]) or None) for k in range(1, n + 1)], label="bucket 1 … n", slots=False))
    res = ""
    for k in used:
        for c in buckets[k]:
            res += c * k
        w3.step(f"Bucket {k}: {', '.join(buckets[k])} → write each {k} time{'s' if k > 1 else ''}.", Row([("".join(buckets[q]) or None) for q in range(1, n + 1)], st={k - 1: "active"}, label="bucket 1 … n"), Vars(output=res))
    w3.step(f"Result: {res}.", Row(list(res)), result=res)

    sol(
        "loudest-letters-first",
        summary="""
            Count each character, then output characters by count from high to low, breaking ties by character
            code. Sorting the (at most 62) distinct characters is already fast; bucketing them by count makes
            the ordering linear without any comparison sort.
        """,
        question=[
            """
            Rearrange `s` so its most frequent character comes first (all its copies together), then the next
            most frequent, and so on.

            - **All copies stay together:** `tree` becomes `eert`, never `eret`.
            - **Ties are fixed by character code**, so the output is unique: digits (`0`–`9`) come before
              uppercase (`A`–`Z`), which come before lowercase (`a`–`z`). `aAbb` → `bbAa`.
            - **Only letters and digits**, so at most 62 different characters, all in ASCII. A 128-slot array
              can count them.
            - **Size:** up to 10⁵ characters. The output has the same length.
            """
        ],
        think=[
            """
            Take `s = "banana12b"`. Count: a×3, b×2, n×2, 1×1, 2×1. Now order them: a first (3). Then b and n
            tie at 2; `b` has the smaller code, so `bb` then `nn`. Then `1` and `2` tie at 1; `1` first.
            Result: `aaabbnn12`.
            """,
            fig(Row(["a:3", "b:2", "n:2", "1:1", "2:1"], label="sorted by count, then code"), caption="Write each character as many times as it appears."),
            """
            Two separate jobs: **counting** (one pass) and **ordering** the distinct characters. The ordering
            is where approaches differ. The number of distinct characters is tiny here (≤ 62), but it's worth
            seeing the linear version too: since a count is between 1 and n, characters can be dropped into
            buckets indexed by count.
            """,
        ],
        approaches=[
            approach(
                "Pick the most frequent remaining character, again and again",
                "brute",
                "O(σ² · n)",
                "O(σ)",
                idea=["Keep the distinct characters in code order. Repeatedly scan them, counting each with a pass over `s`, and take the one with the highest count (the first one found wins ties, which is the smallest code). Append it count times and remove it."],
                walk=w1,
                build=["List the distinct characters in increasing code order.", "While any remain: find the one with the largest count (strictly larger replaces, so ties keep the smaller code).", "Append it count times; remove it from the list."],
                code={
                    "python": """
                        class Solution:
                            def sortByFrequency(self, s: str) -> str:
                                left = sorted(set(s))  #@left
                                out = []
                                while left:  #@round
                                    best = left[0]  #@pick
                                    for c in left:  #@pick
                                        if s.count(c) > s.count(best):  #@pick
                                            best = c  #@pick
                                    out.append(best * s.count(best))  #@emit
                                    left.remove(best)  #@emit
                                return "".join(out)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String sortByFrequency(String s) {
                                boolean[] left = new boolean[128];  //@left
                                for (char c : s.toCharArray()) left[c] = true;  //@left
                                StringBuilder out = new StringBuilder();
                                while (true) {  //@round
                                    int best = -1, bestCount = 0;  //@pick
                                    for (int c = 0; c < 128; c++) {  //@pick
                                        if (!left[c]) continue;  //@pick
                                        int k = 0;  //@pick
                                        for (int i = 0; i < s.length(); i++) if (s.charAt(i) == c) k++;  //@pick
                                        if (k > bestCount) { best = c; bestCount = k; }  //@pick
                                    }
                                    if (best < 0) break;  //@round
                                    for (int i = 0; i < bestCount; i++) out.append((char) best);  //@emit
                                    left[best] = false;  //@emit
                                }
                                return out.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string sortByFrequency(string& s) {
                                bool left[128] = {false};  //@left
                                for (char c : s) left[(int) c] = true;  //@left
                                string out;
                                while (true) {  //@round
                                    int best = -1, bestCount = 0;  //@pick
                                    for (int c = 0; c < 128; c++) {  //@pick
                                        if (!left[c]) continue;  //@pick
                                        int k = count(s.begin(), s.end(), (char) c);  //@pick
                                        if (k > bestCount) { best = c; bestCount = k; }  //@pick
                                    }
                                    if (best < 0) break;  //@round
                                    out.append(bestCount, (char) best);  //@emit
                                    left[best] = false;  //@emit
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* sortByFrequency(char* s) {
                            size_t n = strlen(s);
                            bool left[128] = {false};  //@left
                            for (size_t i = 0; i < n; i++) left[(int) s[i]] = true;  //@left
                            char* out = malloc(n + 1);
                            size_t w = 0;
                            while (true) {  //@round
                                int best = -1, bestCount = 0;  //@pick
                                for (int c = 0; c < 128; c++) {  //@pick
                                    if (!left[c]) continue;  //@pick
                                    int k = 0;  //@pick
                                    for (size_t i = 0; i < n; i++) if (s[i] == c) k++;  //@pick
                                    if (k > bestCount) { best = c; bestCount = k; }  //@pick
                                }
                                if (best < 0) break;  //@round
                                for (int i = 0; i < bestCount; i++) out[w++] = (char) best;  //@emit
                                left[best] = false;  //@emit
                            }
                            out[w] = '\\0';  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("left", "The characters still to place.", {"java": "A flag per ASCII code; walking codes 0…127 visits them in code order.", "cpp": "A flag per ASCII code; walking codes 0…127 visits them in code order.", "c": "A flag per ASCII code; walking codes 0…127 visits them in code order."}),
                    ("round", "One round places one character.", {"java": "No character left means we're done.", "cpp": "No character left means we're done.", "c": "No character left means we're done."}),
                    ("pick", "Count every remaining character by scanning `s`, and keep the largest count. Candidates are visited in code order and only a **strictly** larger count replaces the best, so ties go to the smaller code."),
                    ("emit", "Write the winner as many times as it appears, then take it out of the running."),
                    ("ret", "The rearranged string.", {"c": "Terminate the string; the caller frees it."}),
                ],
                complexity=["**Time O(σ² · n)** for σ distinct characters: σ rounds, each counting σ characters with an O(n) scan. With σ = 62 and n = 10⁵ that's ~4 × 10⁸. **Space O(σ).**"],
                limits=["Counts never change, yet they're recomputed in every round. Count once, then order once."],
                slow=True,
            ),
            approach(
                "Count once, then sort the distinct characters",
                "better",
                "O(n + σ log σ)",
                "O(σ)",
                idea=["One pass fills `count[c]` for each ASCII code. Collect the characters with a nonzero count and sort them by `(−count, code)`. Write each one `count` times."],
                walk=w2,
                build=["Count every character into a 128-slot array.", "Collect the characters that appear.", "Sort them: higher count first, then smaller code.", "Append each `count[c]` times."],
                code={
                    "python": """
                        class Solution:
                            def sortByFrequency(self, s: str) -> str:
                                count = [0] * 128  #@count
                                for ch in s:  #@count
                                    count[ord(ch)] += 1  #@count
                                chars = [c for c in range(128) if count[c]]  #@collect
                                chars.sort(key=lambda c: (-count[c], c))  #@sort
                                return "".join(chr(c) * count[c] for c in chars)  #@emit
                    """,
                    "java": """
                        class Solution {
                            public String sortByFrequency(String s) {
                                int[] count = new int[128];  //@count
                                for (char ch : s.toCharArray()) count[ch]++;  //@count
                                List<Integer> chars = new ArrayList<>();  //@collect
                                for (int c = 0; c < 128; c++) if (count[c] > 0) chars.add(c);  //@collect
                                chars.sort((a, b) -> count[a] != count[b] ? count[b] - count[a] : a - b);  //@sort
                                StringBuilder out = new StringBuilder(s.length());  //@emit
                                for (int c : chars) for (int i = 0; i < count[c]; i++) out.append((char) c);  //@emit
                                return out.toString();  //@emit
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string sortByFrequency(string& s) {
                                int count[128] = {0};  //@count
                                for (char ch : s) count[(int) ch]++;  //@count
                                vector<int> chars;  //@collect
                                for (int c = 0; c < 128; c++) if (count[c]) chars.push_back(c);  //@collect
                                sort(chars.begin(), chars.end(), [&](int a, int b) {  //@sort
                                    return count[a] != count[b] ? count[a] > count[b] : a < b;  //@sort
                                });  //@sort
                                string out;  //@emit
                                for (int c : chars) out.append(count[c], (char) c);  //@emit
                                return out;  //@emit
                            }
                        };
                    """,
                    "c": """
                        static int gCount[128];  //@cmp

                        static int byCountThenCode(const void* a, const void* b) {  //@cmp
                            int x = *(const int*) a, y = *(const int*) b;  //@cmp
                            if (gCount[x] != gCount[y]) return gCount[y] - gCount[x];  //@cmp
                            return x - y;  //@cmp
                        }  //@cmp

                        char* sortByFrequency(char* s) {
                            size_t n = strlen(s);
                            memset(gCount, 0, sizeof gCount);  //@count
                            for (size_t i = 0; i < n; i++) gCount[(int) s[i]]++;  //@count
                            int chars[128], m = 0;  //@collect
                            for (int c = 0; c < 128; c++) if (gCount[c]) chars[m++] = c;  //@collect
                            qsort(chars, m, sizeof(int), byCountThenCode);  //@sort
                            char* out = malloc(n + 1);  //@emit
                            size_t w = 0;  //@emit
                            for (int k = 0; k < m; k++) for (int i = 0; i < gCount[chars[k]]; i++) out[w++] = (char) chars[k];  //@emit
                            out[w] = '\\0';  //@emit
                            return out;  //@emit
                        }
                    """,
                },
                lines=[
                    ("cmp", "`qsort`'s comparator can't see local variables, so the counts live in a file-level array. Higher count sorts first; equal counts fall back to the smaller code. Counts and codes are small, so subtracting is safe."),
                    ("count", "A slot per ASCII code (letters and digits are all below 128).", {"c": "Reset the shared counts first, since the function may be called more than once."}),
                    ("collect", "Only characters that actually appear: at most 62 of them."),
                    ("sort", "Order by count descending, then code ascending.", {"python": "Sorting by `(−count, code)` gives \"high count first, then small code\" with one key."}),
                    ("emit", "Write each character `count` times, keeping copies together.", {"c": "Fill a new buffer and terminate it; the caller frees it."}),
                ],
                complexity=["**Time O(n + σ log σ):** a counting pass plus a sort of σ ≤ 62 items, effectively O(n). **Space O(σ)** besides the output."],
                limits=[
                    """
                    With 62 possible characters this is as fast as anything in practice. The limit appears with a
                    large alphabet (any Unicode text): sorting σ distinct characters costs O(σ log σ). Because a
                    count is an integer from 1 to n, bucketing by count avoids the comparison sort entirely.
                    """
                ],
            ),
            approach(
                "Buckets by count",
                "best",
                "O(n + σ)",
                "O(n + σ)",
                idea=[
                    """
                    Count the characters. Make buckets `1 … n`; visit characters in increasing code order and add
                    each to `bucket[count]`, so every bucket holds its characters already sorted by code. Then read
                    the buckets from `n` down to 1 and write each character `count` times.
                    """
                ],
                walk=w3,
                build=["Count into a 128-slot array.", "For codes 0 … 127 with a nonzero count, append the code to `bucket[count]`.", "For `k` from n down to 1, write every character in `bucket[k]` k times."],
                code={
                    "python": """
                        class Solution:
                            def sortByFrequency(self, s: str) -> str:
                                count = [0] * 128  #@count
                                for ch in s:  #@count
                                    count[ord(ch)] += 1  #@count
                                bucket = [[] for _ in range(len(s) + 1)]  #@fill
                                for c in range(128):  #@fill
                                    if count[c]:  #@fill
                                        bucket[count[c]].append(c)  #@fill
                                out = []  #@read
                                for k in range(len(s), 0, -1):  #@read
                                    for c in bucket[k]:  #@read
                                        out.append(chr(c) * k)  #@read
                                return "".join(out)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String sortByFrequency(String s) {
                                int n = s.length();
                                int[] count = new int[128];  //@count
                                for (char ch : s.toCharArray()) count[ch]++;  //@count
                                List<List<Integer>> bucket = new ArrayList<>();  //@fill
                                for (int k = 0; k <= n; k++) bucket.add(new ArrayList<>());  //@fill
                                for (int c = 0; c < 128; c++) if (count[c] > 0) bucket.get(count[c]).add(c);  //@fill
                                StringBuilder out = new StringBuilder(n);  //@read
                                for (int k = n; k >= 1; k--)  //@read
                                    for (int c : bucket.get(k))  //@read
                                        for (int i = 0; i < k; i++) out.append((char) c);  //@read
                                return out.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string sortByFrequency(string& s) {
                                int n = s.size();
                                int count[128] = {0};  //@count
                                for (char ch : s) count[(int) ch]++;  //@count
                                vector<vector<int>> bucket(n + 1);  //@fill
                                for (int c = 0; c < 128; c++) if (count[c]) bucket[count[c]].push_back(c);  //@fill
                                string out;  //@read
                                for (int k = n; k >= 1; k--)  //@read
                                    for (int c : bucket[k]) out.append(k, (char) c);  //@read
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* sortByFrequency(char* s) {
                            int n = strlen(s);
                            int count[128] = {0};  //@count
                            for (int i = 0; i < n; i++) count[(int) s[i]]++;  //@count
                            int* head = malloc((n + 1) * sizeof(int));  //@fill
                            int next[128];  //@fill
                            for (int k = 0; k <= n; k++) head[k] = -1;  //@fill
                            for (int c = 127; c >= 0; c--) {  //@fill
                                if (!count[c]) continue;  //@fill
                                next[c] = head[count[c]];  //@fill
                                head[count[c]] = c;  //@fill
                            }
                            char* out = malloc(n + 1);  //@read
                            int w = 0;  //@read
                            for (int k = n; k >= 1; k--)  //@read
                                for (int c = head[k]; c != -1; c = next[c])  //@read
                                    for (int i = 0; i < k; i++) out[w++] = (char) c;  //@read
                            out[w] = '\\0';  //@ret
                            free(head);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("count", "Count each character once."),
                    ("fill", "Drop each character into the bucket for its count. Characters are visited in code order, so each bucket comes out sorted by code: the tie rule for free.",
                     {"c": "Each bucket is a linked list stored in two arrays: `head[k]` is the first character with count k, `next[c]` the one after `c`. Walking codes from 127 down and pushing to the front leaves each list in increasing code order."}),
                    ("read", "Highest count first; within a bucket, smaller code first. Each character is written `k` times."),
                    ("ret", "The rearranged string.", {"c": "Terminate it, free the bucket heads; the caller frees the result."}),
                ],
                complexity=["**Time O(n + σ):** counting, one pass over the alphabet, and n buckets to read. **Space O(n + σ)** for the buckets."],
            ),
        ],
        takeaways=[
            """
            - "Order by frequency" = **count, then order the distinct items**. Do the counting exactly once.
            - When the sort key is a small integer (a count between 1 and n), **bucket sort** beats comparison
              sorting.
            - Visiting keys in their natural order while filling buckets makes ties come out in the right
              order without extra work.
            """
        ],
    )


@problem
def majority_reading():
    v = [2, 8, 8, 1, 8, 8, 3, 8, 2]
    n = len(v)
    assert Counter(v)[8] * 2 > n

    w1 = Steps("Count each reading's copies with a full scan until one has more than half.")
    for i, x in enumerate(v):
        c = v.count(x)
        st = {j: ("answer" if c * 2 > n else "found") for j, y in enumerate(v) if y == x}
        st[i] = "active" if c * 2 <= n else "answer"
        w1.step(f"{x} appears {c} time{'s' if c != 1 else ''}" + (f" — more than {n}/2. Answer." if c * 2 > n else f", not more than {n}/2."), Row(v, st=st, ptr={"i": i}, slots=True))
        if c * 2 > n:
            break
    w1.steps[-1]["result"] = "8"

    w2 = Steps("Sort; the majority value always covers the middle position.")
    s = sorted(v)
    w2.step(f"Sorted: {s}.", Row(v, label="readings"), Row(s, slots=True, label="sorted"))
    w2.step(f"A value filling more than half the slots must cover index n // 2 = {n // 2}.", Row(s, st={i: ("answer" if i == n // 2 else "found") for i, y in enumerate(s) if y == 8}, slots=True, label="sorted"), result=s[n // 2])

    w3 = Steps("Count every value in a hash map; stop when a count passes n / 2.")
    cnt = {}
    for i, x in enumerate(v):
        cnt[x] = cnt.get(x, 0) + 1
        keys = list(cnt)
        done = cnt[x] * 2 > n
        w3.step(f"{x}: count {cnt[x]}" + (f" > {n}/2. Answer." if done else "."), Row(v, st={**{q: "dim" for q in range(i)}, i: "answer" if done else "active"}, slots=True), Row([f"{k}:{cnt[k]}" for k in keys], st={keys.index(x): "answer" if done else "new"}, label="value:count"))
        if done:
            w3.steps[-1]["result"] = str(x)
            break

    w4 = Steps("Boyer–Moore voting: different values cancel in pairs; the majority can't be cancelled out.")
    cand, count = None, 0
    for i, x in enumerate(v):
        if count == 0:
            cand, count = x, 1
            t = f"count is 0, so {x} becomes the candidate (count 1)."
        elif x == cand:
            count += 1
            t = f"{x} matches the candidate: count {count}."
        else:
            count -= 1
            t = f"{x} differs: it cancels one vote, count {count}."
        w4.step(f"Reading {x}: {t}", Row(v, st={**{q: "dim" for q in range(i)}, i: "active"}, slots=True), Vars(candidate=cand, count=count))
    w4.step(f"The survivor is {cand}.", Row(v, st={i: "answer" for i, y in enumerate(v) if y == cand}, slots=True), result=cand)

    sol(
        "majority-reading",
        summary="""
            A value that fills **more than half** the list survives any cancelling: pair each copy of it with a
            different value and there are copies left over. Boyer–Moore voting does exactly that in one pass with
            two variables, O(n) time and O(1) space.
        """,
        question=[
            """
            One value appears in more than half of the readings. Return it.

            - **More than half** means strictly more than n/2: in 7 readings it appears at least 4 times; in 8,
              at least 5. It's guaranteed to exist, so there's no "no answer" case to handle.
            - **Values can be negative** and as large as ±10⁹, so you can't index an array by value.
            - **Size:** up to 10⁵ readings.
            - The guarantee is what makes the clever O(1)-space method valid. Without it, you'd need a second
              pass to confirm the candidate.
            """
        ],
        think=[
            """
            Take `[2, 8, 8, 1, 8, 8, 3, 8, 2]`: 8 appears 5 times out of 9.

            Counting with a hash map clearly works. But here's a sharper observation: **pair up readings that
            are different and throw both away.** Each 8 can be paired with at most one non-8, and there are only
            4 non-8s. However you pair things, at least one 8 survives, and nothing else can survive more than 8
            does.
            """,
            fig(Row([2, 8], st={0: "dim", 1: "dim"}, label="cancel"), Row([8, 1], st={0: "dim", 1: "dim"}, label="cancel"), Row([8, 3], st={0: "dim", 1: "dim"}, label="cancel"), Row([8, 2], st={0: "dim", 1: "dim"}, label="cancel"), Row([8], st={0: "answer"}, label="left over"),
                caption="Four non-8s can cancel at most four 8s. The fifth 8 survives."),
            """
            Boyer–Moore turns that into a scan: keep a **candidate** and a **count**. A matching reading adds a
            vote; a different reading cancels one; when the count hits zero, the next reading becomes the new
            candidate. Whatever is left at the end is the majority.

            Another view, useful for the sorting approach: a value covering more than half the positions of a
            **sorted** list must cover the middle position.
            """,
        ],
        approaches=[
            approach(
                "Count every value by scanning",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each reading, count its copies with a full scan. The first one whose count exceeds n/2 is the answer."],
                walk=w1,
                build=["For each reading `r`, count how many readings equal `r`.", "If `count × 2 > n`, return `r`."],
                code={
                    "python": """
                        class Solution:
                            def majorityValue(self, readings: List[int]) -> int:
                                n = len(readings)
                                for r in readings:  #@each
                                    if readings.count(r) * 2 > n:  #@count
                                        return r  #@count
                                return readings[0]  #@none
                    """,
                    "java": """
                        class Solution {
                            public int majorityValue(int[] readings) {
                                int n = readings.length;
                                for (int r : readings) {  //@each
                                    int c = 0;  //@count
                                    for (int x : readings) if (x == r) c++;  //@count
                                    if (c * 2 > n) return r;  //@count
                                }
                                return readings[0];  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int majorityValue(vector<int>& readings) {
                                int n = readings.size();
                                for (int r : readings) {  //@each
                                    if (count(readings.begin(), readings.end(), r) * 2 > n) return r;  //@count
                                }
                                return readings[0];  //@none
                            }
                        };
                    """,
                    "c": """
                        int majorityValue(int* readings, int readingsSize) {
                            for (int i = 0; i < readingsSize; i++) {  //@each
                                int c = 0;  //@count
                                for (int j = 0; j < readingsSize; j++) if (readings[j] == readings[i]) c++;  //@count
                                if (c * 2 > readingsSize) return readings[i];  //@count
                            }
                            return readings[0];  //@none
                        }
                    """,
                },
                lines=[
                    ("each", "Try each reading as the answer."),
                    ("count", "Count its copies. More than half (`c × 2 > n`, which avoids rounding issues with `n / 2`) means it's the majority."),
                    ("none", "Unreachable: the majority is guaranteed."),
                ],
                complexity=["**Time O(n²):** each candidate costs a full scan. **Space O(1).**"],
                limits=["The same values get recounted over and over. Count each value once, or use the order a sort provides."],
                slow=True,
            ),
            approach(
                "Sort and take the middle",
                "better",
                "O(n log n)",
                "O(n)",
                idea=["In sorted order the majority's copies form one block longer than n/2. Any block that long must cover index `n // 2`, so the answer is simply `sorted[n // 2]`."],
                walk=w2,
                build=["Sort a copy.", "Return the element at index `n // 2`."],
                code={
                    "python": """
                        class Solution:
                            def majorityValue(self, readings: List[int]) -> int:
                                s = sorted(readings)  #@sort
                                return s[len(s) // 2]  #@mid
                    """,
                    "java": """
                        class Solution {
                            public int majorityValue(int[] readings) {
                                int[] s = readings.clone();  //@sort
                                Arrays.sort(s);  //@sort
                                return s[s.length / 2];  //@mid
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int majorityValue(vector<int>& readings) {
                                vector<int> s = readings;  //@sort
                                sort(s.begin(), s.end());  //@sort
                                return s[s.size() / 2];  //@mid
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@cmp
                            int p = *(const int*) a, q = *(const int*) b;  //@cmp
                            return (p > q) - (p < q);  //@cmp
                        }  //@cmp

                        int majorityValue(int* readings, int readingsSize) {
                            int* s = malloc(readingsSize * sizeof(int));  //@sort
                            memcpy(s, readings, readingsSize * sizeof(int));  //@sort
                            qsort(s, readingsSize, sizeof(int), cmpInt);  //@sort
                            int answer = s[readingsSize / 2];  //@mid
                            free(s);  //@mid
                            return answer;  //@mid
                        }
                    """,
                },
                lines=[
                    ("cmp", "Overflow-safe comparator for `qsort`."),
                    ("sort", "Sorted copy: each value's copies form one contiguous block."),
                    ("mid", "A block longer than half the list can't fit entirely left or right of the middle, so it covers index n / 2.", {"c": "Read the answer before freeing the copy."}),
                ],
                complexity=["**Time O(n log n).** **Space O(n)** for the copy."],
                limits=["Sorting orders all values when we only need the one that dominates. Counting avoids the log factor."],
            ),
            approach(
                "Count with a hash map",
                "better",
                "O(n)",
                "O(n)",
                idea=["Count readings in a hash map as you go. As soon as some count exceeds n/2, return that value."],
                walk=w3,
                build=["Create an empty value → count map.", "For each reading, add 1 to its count; if `count × 2 > n`, return it."],
                code={
                    "python": """
                        class Solution:
                            def majorityValue(self, readings: List[int]) -> int:
                                n = len(readings)
                                count = {}  #@map
                                for r in readings:  #@loop
                                    count[r] = count.get(r, 0) + 1  #@loop
                                    if count[r] * 2 > n:  #@check
                                        return r  #@check
                                return readings[0]  #@none
                    """,
                    "java": """
                        class Solution {
                            public int majorityValue(int[] readings) {
                                int n = readings.length;
                                Map<Integer, Integer> count = new HashMap<>();  //@map
                                for (int r : readings) {  //@loop
                                    int c = count.merge(r, 1, Integer::sum);  //@loop
                                    if (c * 2 > n) return r;  //@check
                                }
                                return readings[0];  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int majorityValue(vector<int>& readings) {
                                int n = readings.size();
                                unordered_map<int, int> count;  //@map
                                for (int r : readings) {  //@loop
                                    if (++count[r] * 2 > n) return r;  //@check
                                }
                                return readings[0];  //@none
                            }
                        };
                    """,
                    "c": """
                        // A small hash map from a value to its count: open addressing, linear probing.
                        typedef struct { int key; int count; bool used; } Slot;  //@table

                        static unsigned slotOf(int key, unsigned mask) {  //@table
                            unsigned long long h = (unsigned long long) (long long) key * 0x9E3779B97F4A7C15ULL;  //@table
                            return (unsigned) (h >> 32) & mask;  //@table
                        }  //@table

                        int majorityValue(int* readings, int readingsSize) {
                            unsigned cap = 1;  //@map
                            while (cap < 2u * readingsSize) cap <<= 1;  //@map
                            Slot* count = calloc(cap, sizeof(Slot));  //@map
                            int answer = readings[0];  //@map
                            for (int i = 0; i < readingsSize; i++) {  //@loop
                                int r = readings[i];  //@loop
                                unsigned s = slotOf(r, cap - 1);  //@loop
                                while (count[s].used && count[s].key != r) s = (s + 1) & (cap - 1);  //@loop
                                count[s].key = r;  //@loop
                                count[s].used = true;  //@loop
                                if (++count[s].count * 2 > readingsSize) { answer = r; break; }  //@check
                            }
                            free(count);  //@none
                            return answer;  //@none
                        }
                    """,
                },
                lines=[
                    ("table", "C has no hash map: a slot holds a value, its count and an in-use flag, and `slotOf` scrambles a value into a starting slot."),
                    ("map", "Counts per value, filled as we go.", {"c": "A power-of-two table at least 2n big, zeroed by `calloc`."}),
                    ("loop", "Add one to this reading's count.", {"java": "`merge(r, 1, Integer::sum)` returns the new count.", "c": "Probe from the value's slot to its entry (or an empty slot) and claim it."}),
                    ("check", "The first count to pass half is the majority; stop right there.", {"cpp": "`++count[r]` creates the entry at 0 if needed, increments it, and gives the new value."}),
                    ("none", "Unreachable with valid input.", {"c": "Free the table and return the answer found."}),
                ],
                complexity=["**Time O(n)** on average. **Space O(n)**: up to about n/2 distinct values can be stored."],
                limits=["The map remembers every distinct value even though only one of them matters. Voting needs just one candidate and one counter."],
            ),
            approach(
                "Boyer–Moore voting",
                "best",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    Keep `candidate` and `count`, starting at count 0. For each reading:

                    - count 0 → this reading becomes the candidate with count 1;
                    - same as the candidate → count + 1;
                    - different → count − 1 (it cancels one vote).

                    **Why it works:** every decrement pairs one candidate copy with one different reading and
                    discards both. Discarding two *different* values from a list keeps the majority a majority of
                    what remains (it loses at most one of its copies, while the list shrinks by two). At the end,
                    what's left uncancelled can only be the majority.
                    """
                ],
                walk=w4,
                build=["`candidate = 0`, `count = 0`.", "For each reading: if `count == 0`, set `candidate` to it.", "Then `count += 1` if it equals the candidate, else `count −= 1`.", "Return `candidate`."],
                code={
                    "python": """
                        class Solution:
                            def majorityValue(self, readings: List[int]) -> int:
                                candidate, count = 0, 0  #@init
                                for r in readings:  #@loop
                                    if count == 0:  #@new
                                        candidate = r  #@new
                                    count += 1 if r == candidate else -1  #@vote
                                return candidate  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int majorityValue(int[] readings) {
                                int candidate = 0, count = 0;  //@init
                                for (int r : readings) {  //@loop
                                    if (count == 0) candidate = r;  //@new
                                    count += (r == candidate) ? 1 : -1;  //@vote
                                }
                                return candidate;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int majorityValue(vector<int>& readings) {
                                int candidate = 0, count = 0;  //@init
                                for (int r : readings) {  //@loop
                                    if (count == 0) candidate = r;  //@new
                                    count += (r == candidate) ? 1 : -1;  //@vote
                                }
                                return candidate;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int majorityValue(int* readings, int readingsSize) {
                            int candidate = 0, count = 0;  //@init
                            for (int i = 0; i < readingsSize; i++) {  //@loop
                                if (count == 0) candidate = readings[i];  //@new
                                count += (readings[i] == candidate) ? 1 : -1;  //@vote
                            }
                            return candidate;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "No candidate yet: a count of 0 means \"the next reading takes over\"."),
                    ("loop", "One pass, left to right."),
                    ("new", "All earlier readings have cancelled each other out, so start fresh with this one."),
                    ("vote", "A match strengthens the candidate; a different value cancels one of its votes (both are discarded as a pair)."),
                    ("ret", "With a guaranteed majority, the survivor is it. (Without the guarantee you'd recount the candidate in a second pass to confirm.)"),
                ],
                complexity=["**Time O(n):** one pass. **Space O(1):** two variables."],
            ),
        ],
        takeaways=[
            """
            - A strict majority can't be cancelled out: pairing it against everything else leaves copies over.
              That's **Boyer–Moore voting**, O(1) space.
            - The guarantee matters. If a majority might not exist, verify the candidate with a second count.
            - The sorting trick (majority covers the middle index) is a handy one-liner when O(n log n) is fine.
            - The idea generalises: at most two values can exceed n/3 (see **Strong Candidates**), with two
              candidate slots.
            """
        ],
    )


@problem
def top_genres():
    plays, k = [3, 1, 3, 2, 1, 3, 4, 2, 1, 5], 3
    cnt = Counter(plays)
    want = sorted(cnt, key=lambda g: (-cnt[g], g))[:k]
    assert want == [1, 3, 2]
    ids = sorted(cnt)

    w1 = Steps("k rounds: each round counts every remaining genre with full scans and takes the best.")
    left = ids[:]
    out = []
    for r in range(k):
        best = max(left, key=lambda g: (plays.count(g), -g))
        out.append(best)
        w1.step(f"Round {r + 1}: counts {', '.join(f'{g}:{plays.count(g)}' for g in left)}. Best: {best}.", Row([f"{g}:{plays.count(g)}" for g in left], st={left.index(best): "answer"}, label="remaining genre:plays"), Vars(answer=str(out)))
        left.remove(best)
    w1.step(f"Answer {out}.", Row(out), result=out)

    w2 = Steps("Count once, then sort genres by (plays high → low, id low → high) and take k.")
    w2.step("Plays per genre.", Row(plays, slots=True), Row([f"{g}:{cnt[g]}" for g in ids], label="genre:plays"))
    ordered = sorted(cnt, key=lambda g: (-cnt[g], g))
    w2.step(f"Sorted: {', '.join(f'{g}:{cnt[g]}' for g in ordered)}. Genres 1 and 3 tie at 3; 1 has the smaller id.", Row([f"{g}:{cnt[g]}" for g in ordered], st={i: "answer" for i in range(k)}, label="sorted"), result=ordered[:k])

    import heapq
    w3 = Steps(f"Keep a min-heap of the best {k} so far; its top is the weakest, and gets replaced by anything better.")
    heap = []
    for g in ids:
        item = (cnt[g], -g)
        if len(heap) < k:
            heapq.heappush(heap, item)
            act = "heap not full: push"
        elif item > heap[0]:
            out_ = heap[0]
            heapq.heapreplace(heap, item)
            act = f"beats the weakest ({-out_[1]}:{out_[0]}): replace it"
        else:
            act = f"not better than the weakest ({-heap[0][1]}:{heap[0][0]}): skip"
        show = sorted(heap)
        w3.step(f"Genre {g} with {cnt[g]} plays: {act}.", Row([f"{-x[1]}:{x[0]}" for x in show], st={0: "mark"}, label="kept (weakest first)"))
    final = [-x[1] for x in sorted(heap, reverse=True)]
    w3.step(f"Pop and reverse: {final}.", Row([f"{g}:{cnt[g]}" for g in final], label="best first"), result=final)

    w4 = Steps("Drop genres into buckets by play count (in id order), then read buckets from the top.")
    n = len(plays)
    buckets = {c: [g for g in ids if cnt[g] == c] for c in range(1, n + 1)}
    w4.step("Bucket[c] lists genres played c times, smallest id first.", Row([(",".join(map(str, buckets[c])) or None) for c in range(1, 5)], label="buckets 1 … 4", slots=False))
    out = []
    for c in range(n, 0, -1):
        if not buckets[c]:
            continue
        for g in buckets[c]:
            if len(out) < k:
                out.append(g)
        w4.step(f"Bucket {c}: {buckets[c]} → answer {out}.", Row([(",".join(map(str, buckets[q])) or None) for q in range(1, 5)], st={c - 1: "active"}, label="buckets 1 … 4"), Vars(answer=str(out)))
        if len(out) == k:
            break
    w4.step(f"Answer {out}.", Row(out), result=out)

    sol(
        "top-genres",
        summary="""
            Count plays per genre (ids are small, −10⁴ … 10⁴, so an array works). Then pick the k best by (count
            high, id low). Sorting all genres works; a size-k heap avoids sorting everything; and because counts
            are integers up to n, bucketing by count makes the whole thing linear.
        """,
        question=[
            """
            Return the `k` most-played genres, best first. Ties in play count go to the **smaller genre id**.

            - **The order of the answer matters:** by count descending, then id ascending.
            - **Ids can be negative** (−10⁴ … 10⁴), so shift them by 10⁴ to use them as array indices.
            - **k is valid:** at least k different genres exist.
            - **Size:** up to 10⁵ plays, up to 20,001 distinct genres.
            """
        ],
        think=[
            """
            Take `plays = [3, 1, 3, 2, 1, 3, 4, 2, 1, 5]` with k = 3. Counts: 1→3, 3→3, 2→2, 4→1, 5→1.
            Order by count, ties by id: 1 (3 plays), 3 (3 plays), 2, 4, 5. The top 3 are `[1, 3, 2]`.
            """,
            fig(Row(["1:3", "3:3", "2:2", "4:1", "5:1"], st={0: "answer", 1: "answer", 2: "answer"}, label="genre:plays, best first"), caption="Genres 1 and 3 tie; 1 wins on id."),
            """
            So the work is: count (one pass), then **select the k best**. Selection is where the approaches
            differ:

            - sort all d genres: O(d log d);
            - keep only the best k seen so far in a heap: O(d log k), good when k is small;
            - put genres in buckets by count, since counts are integers between 1 and n: O(n + d), no comparisons
              at all.
            """,
        ],
        approaches=[
            approach(
                "Find the best remaining genre k times",
                "brute",
                "O(k · d · n)",
                "O(d)",
                idea=["List the distinct genres. k times: count every remaining genre with a scan of `plays`, take the best (most plays, then smallest id), and remove it."],
                walk=w1,
                build=["Collect the distinct genres in increasing id order.", "Repeat k times: find the genre with the most plays (scanning to count), keeping the earlier (smaller) id on ties.", "Move it to the answer."],
                code={
                    "python": """
                        class Solution:
                            def topGenres(self, plays: List[int], k: int) -> List[int]:
                                left = sorted(set(plays))  #@distinct
                                out = []
                                for _ in range(k):  #@round
                                    best = left[0]  #@pick
                                    for g in left:  #@pick
                                        if plays.count(g) > plays.count(best):  #@pick
                                            best = g  #@pick
                                    out.append(best)  #@take
                                    left.remove(best)  #@take
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] topGenres(int[] plays, int k) {
                                boolean[] left = new boolean[20001];  //@distinct
                                for (int g : plays) left[g + 10000] = true;  //@distinct
                                int[] out = new int[k];
                                for (int r = 0; r < k; r++) {  //@round
                                    int best = -1, bestCount = 0;  //@pick
                                    for (int i = 0; i < 20001; i++) {  //@pick
                                        if (!left[i]) continue;  //@pick
                                        int c = 0;  //@pick
                                        for (int g : plays) if (g == i - 10000) c++;  //@pick
                                        if (c > bestCount) { best = i; bestCount = c; }  //@pick
                                    }
                                    out[r] = best - 10000;  //@take
                                    left[best] = false;  //@take
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> topGenres(vector<int>& plays, int k) {
                                vector<bool> left(20001, false);  //@distinct
                                for (int g : plays) left[g + 10000] = true;  //@distinct
                                vector<int> out;
                                for (int r = 0; r < k; r++) {  //@round
                                    int best = -1, bestCount = 0;  //@pick
                                    for (int i = 0; i < 20001; i++) {  //@pick
                                        if (!left[i]) continue;  //@pick
                                        int c = count(plays.begin(), plays.end(), i - 10000);  //@pick
                                        if (c > bestCount) { best = i; bestCount = c; }  //@pick
                                    }
                                    out.push_back(best - 10000);  //@take
                                    left[best] = false;  //@take
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* topGenres(int* plays, int playsSize, int k, int* returnSize) {
                            bool* left = calloc(20001, sizeof(bool));  //@distinct
                            for (int i = 0; i < playsSize; i++) left[plays[i] + 10000] = true;  //@distinct
                            int* out = malloc(k * sizeof(int));
                            for (int r = 0; r < k; r++) {  //@round
                                int best = -1, bestCount = 0;  //@pick
                                for (int i = 0; i < 20001; i++) {  //@pick
                                    if (!left[i]) continue;  //@pick
                                    int c = 0;  //@pick
                                    for (int j = 0; j < playsSize; j++) if (plays[j] == i - 10000) c++;  //@pick
                                    if (c > bestCount) { best = i; bestCount = c; }  //@pick
                                }
                                out[r] = best - 10000;  //@take
                                left[best] = false;  //@take
                            }
                            free(left);  //@ret
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("distinct", "The genres still in the running.", {"java": "A flag per possible id, shifted by 10,000 so −10⁴ maps to index 0.", "cpp": "A flag per possible id, shifted by 10,000 so −10⁴ maps to index 0.", "c": "A flag per possible id, shifted by 10,000 so −10⁴ maps to index 0."}),
                    ("round", "Each round adds one genre to the answer."),
                    ("pick", "Count every remaining genre with a full scan. Genres are visited from the smallest id and only a strictly higher count replaces the best, which implements the tie rule."),
                    ("take", "Record the winner (shifting its index back to an id) and remove it from the running."),
                    ("ret", "The k winners in order.", {"c": "Free the flags and report the length."}),
                ],
                complexity=["**Time O(k · d · n):** k rounds × d genres × an n-long scan. **Space O(d).**"],
                limits=["Counts are recomputed every round although they never change. Count once, then choose."],
                slow=True,
            ),
            approach(
                "Count, then sort all genres",
                "better",
                "O(n + d log d)",
                "O(d)",
                idea=["Count plays into an array indexed by `id + 10000`. Collect the genres that appear and sort them by (count descending, id ascending). The first k are the answer."],
                walk=w2,
                build=["Count plays per genre (shifted index).", "Collect genres with a nonzero count.", "Sort by count descending, then id ascending.", "Return the first k."],
                code={
                    "python": """
                        class Solution:
                            def topGenres(self, plays: List[int], k: int) -> List[int]:
                                count = [0] * 20001  #@count
                                for g in plays:  #@count
                                    count[g + 10000] += 1  #@count
                                genres = [i - 10000 for i in range(20001) if count[i]]  #@collect
                                genres.sort(key=lambda g: (-count[g + 10000], g))  #@sort
                                return genres[:k]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] topGenres(int[] plays, int k) {
                                int[] count = new int[20001];  //@count
                                for (int g : plays) count[g + 10000]++;  //@count
                                List<Integer> genres = new ArrayList<>();  //@collect
                                for (int i = 0; i < 20001; i++) if (count[i] > 0) genres.add(i - 10000);  //@collect
                                genres.sort((a, b) -> count[a + 10000] != count[b + 10000]  //@sort
                                        ? count[b + 10000] - count[a + 10000] : a - b);  //@sort
                                int[] out = new int[k];  //@ret
                                for (int i = 0; i < k; i++) out[i] = genres.get(i);  //@ret
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> topGenres(vector<int>& plays, int k) {
                                vector<int> count(20001, 0);  //@count
                                for (int g : plays) count[g + 10000]++;  //@count
                                vector<int> genres;  //@collect
                                for (int i = 0; i < 20001; i++) if (count[i]) genres.push_back(i - 10000);  //@collect
                                sort(genres.begin(), genres.end(), [&](int a, int b) {  //@sort
                                    int ca = count[a + 10000], cb = count[b + 10000];  //@sort
                                    return ca != cb ? ca > cb : a < b;  //@sort
                                });  //@sort
                                return vector<int>(genres.begin(), genres.begin() + k);  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int* gCount;  //@cmp

                        static int byPlays(const void* a, const void* b) {  //@cmp
                            int x = *(const int*) a, y = *(const int*) b;  //@cmp
                            int cx = gCount[x + 10000], cy = gCount[y + 10000];  //@cmp
                            if (cx != cy) return cy - cx;  //@cmp
                            return x - y;  //@cmp
                        }  //@cmp

                        int* topGenres(int* plays, int playsSize, int k, int* returnSize) {
                            int* count = calloc(20001, sizeof(int));  //@count
                            for (int i = 0; i < playsSize; i++) count[plays[i] + 10000]++;  //@count
                            int* genres = malloc(20001 * sizeof(int));  //@collect
                            int d = 0;  //@collect
                            for (int i = 0; i < 20001; i++) if (count[i]) genres[d++] = i - 10000;  //@collect
                            gCount = count;  //@sort
                            qsort(genres, d, sizeof(int), byPlays);  //@sort
                            int* out = malloc(k * sizeof(int));  //@ret
                            memcpy(out, genres, k * sizeof(int));  //@ret
                            free(count);  //@ret
                            free(genres);  //@ret
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("cmp", "The comparator reads the counts through a file-level pointer (`qsort` can't pass extra data). Higher count first; ties by smaller id. Counts and ids are small, so subtraction is safe."),
                    ("count", "Ids −10⁴ … 10⁴ shifted by 10⁴ become indices 0 … 20,000."),
                    ("collect", "The genres that were actually played (d of them)."),
                    ("sort", "Best first: more plays, then smaller id."),
                    ("ret", "The first k.", {"c": "Copy them out, free the scratch arrays, report the length."}),
                ],
                complexity=["**Time O(n + R + d log d)** with R = 20,001 possible ids (a constant). **Space O(R).**"],
                limits=["It sorts all d genres just to keep k of them. When k is much smaller than d, keeping only the best k is cheaper."],
            ),
            approach(
                "Keep the best k in a min-heap",
                "better",
                "O(n + d log k)",
                "O(k)",
                idea=[
                    """
                    Visit the genres with their counts. Keep a heap of at most k entries whose **top is the weakest**
                    one kept (fewest plays; on a tie, the larger id). For each genre: if the heap has fewer than k,
                    push it; otherwise, if it beats the top, replace the top. At the end the heap holds the k best;
                    pop them weakest first and reverse.
                    """
                ],
                walk=w3,
                build=[
                    "Count plays per genre.",
                    "Define \"weaker\": fewer plays, or equal plays and a larger id.",
                    "For each played genre: push if the heap has < k entries; else if it's stronger than the top, replace the top.",
                    "Pop everything (weakest first) and fill the answer from the back.",
                ],
                code={
                    "python": """
                        import heapq

                        class Solution:
                            def topGenres(self, plays: List[int], k: int) -> List[int]:
                                count = [0] * 20001  #@count
                                for g in plays:  #@count
                                    count[g + 10000] += 1  #@count
                                heap = []  #@heap
                                for i in range(20001):  #@scan
                                    if not count[i]:  #@scan
                                        continue  #@scan
                                    item = (count[i], -(i - 10000))  #@key
                                    if len(heap) < k:  #@keep
                                        heapq.heappush(heap, item)  #@keep
                                    elif item > heap[0]:  #@keep
                                        heapq.heapreplace(heap, item)  #@keep
                                best = sorted(heap, reverse=True)  #@out
                                return [-g for _, g in best]  #@out
                    """,
                    "java": """
                        class Solution {
                            public int[] topGenres(int[] plays, int k) {
                                int[] count = new int[20001];  //@count
                                for (int g : plays) count[g + 10000]++;  //@count
                                PriorityQueue<int[]> heap = new PriorityQueue<>(  //@heap
                                    (a, b) -> a[1] != b[1] ? Integer.compare(a[1], b[1]) : Integer.compare(b[0], a[0]));  //@heap
                                for (int i = 0; i < 20001; i++) {  //@scan
                                    if (count[i] == 0) continue;  //@scan
                                    heap.offer(new int[] {i - 10000, count[i]});  //@keep
                                    if (heap.size() > k) heap.poll();  //@keep
                                }
                                int[] out = new int[k];  //@out
                                for (int i = k - 1; i >= 0; i--) out[i] = heap.poll()[0];  //@out
                                return out;  //@out
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> topGenres(vector<int>& plays, int k) {
                                vector<int> count(20001, 0);  //@count
                                for (int g : plays) count[g + 10000]++;  //@count
                                priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> heap;  //@heap
                                for (int i = 0; i < 20001; i++) {  //@scan
                                    if (!count[i]) continue;  //@scan
                                    heap.push({count[i], -(i - 10000)});  //@keep
                                    if ((int) heap.size() > k) heap.pop();  //@keep
                                }
                                vector<int> out(k);  //@out
                                for (int i = k - 1; i >= 0; i--) {  //@out
                                    out[i] = -heap.top().second;  //@out
                                    heap.pop();  //@out
                                }
                                return out;  //@out
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int plays, id; } Entry;  //@type

                        // a is weaker than b: fewer plays, or as many plays and a larger id.
                        static bool weaker(Entry a, Entry b) {  //@type
                            return a.plays != b.plays ? a.plays < b.plays : a.id > b.id;  //@type
                        }  //@type

                        static void siftDown(Entry* h, int size, int i) {  //@sift
                            while (true) {  //@sift
                                int l = 2 * i + 1, r = l + 1, w = i;  //@sift
                                if (l < size && weaker(h[l], h[w])) w = l;  //@sift
                                if (r < size && weaker(h[r], h[w])) w = r;  //@sift
                                if (w == i) return;  //@sift
                                Entry t = h[i]; h[i] = h[w]; h[w] = t;  //@sift
                                i = w;  //@sift
                            }  //@sift
                        }  //@sift

                        static void siftUp(Entry* h, int i) {  //@sift
                            while (i > 0 && weaker(h[i], h[(i - 1) / 2])) {  //@sift
                                Entry t = h[i]; h[i] = h[(i - 1) / 2]; h[(i - 1) / 2] = t;  //@sift
                                i = (i - 1) / 2;  //@sift
                            }  //@sift
                        }  //@sift

                        int* topGenres(int* plays, int playsSize, int k, int* returnSize) {
                            int* count = calloc(20001, sizeof(int));  //@count
                            for (int i = 0; i < playsSize; i++) count[plays[i] + 10000]++;  //@count
                            Entry* heap = malloc(k * sizeof(Entry));  //@heap
                            int size = 0;  //@heap
                            for (int i = 0; i < 20001; i++) {  //@scan
                                if (!count[i]) continue;  //@scan
                                Entry e = {count[i], i - 10000};  //@key
                                if (size < k) {  //@keep
                                    heap[size] = e;  //@keep
                                    siftUp(heap, size++);  //@keep
                                } else if (weaker(heap[0], e)) {  //@keep
                                    heap[0] = e;  //@keep
                                    siftDown(heap, size, 0);  //@keep
                                }
                            }
                            int* out = malloc(k * sizeof(int));  //@out
                            for (int i = k - 1; i >= 0; i--) {  //@out
                                out[i] = heap[0].id;  //@out
                                heap[0] = heap[--size];  //@out
                                siftDown(heap, size, 0);  //@out
                            }
                            free(count);  //@out
                            free(heap);  //@out
                            *returnSize = k;  //@out
                            return out;  //@out
                        }
                    """,
                },
                lines=[
                    ("type", "A heap entry and the ordering that matters: which of two genres is **weaker**. The weakest kept genre sits on top so it's the one we compare against and evict."),
                    ("sift", "A hand-written binary min-heap (C has none). `siftUp` moves a new entry up while it's weaker than its parent; `siftDown` moves the top down, swapping with its weaker child, until the heap order holds again. Both are O(log k)."),
                    ("count", "Plays per genre, ids shifted by 10⁴ into array indices."),
                    ("heap", "The k strongest genres seen so far, weakest on top.",
                     {"java": "The comparator puts fewer plays first, and on ties the larger id first: that's \"weakest first\".",
                      "cpp": "`greater<>` makes a min-heap of `(plays, −id)`: the smallest pair is fewest plays, and on a tie the most negative `−id`, i.e. the largest id: the weakest."}),
                    ("scan", "Visit each genre that was played."),
                    ("key", "Represent the genre so that \"bigger means stronger\".", {"python": "Tuples `(plays, −id)`: more plays is bigger, and on a tie a smaller id gives a bigger `−id`."}),
                    ("keep", "Fill the heap up to k; after that, a genre only gets in by beating the weakest kept one, which it replaces.",
                     {"java": "Simpler variant: always add, then drop the weakest if there are k + 1. Same result.",
                      "cpp": "Always push, then pop the weakest if there are k + 1."}),
                    ("out", "The heap pops weakest first, so fill the answer from the back to get best first.",
                     {"python": "Sorting the k kept tuples in reverse puts the strongest first.", "c": "Pop by moving the last entry to the top and sifting it down; free the scratch memory."}),
                ],
                complexity=["**Time O(n + R + d log k):** counting, then each of d genres costs at most one O(log k) heap operation. **Space O(k)** for the heap (plus the fixed count array)."],
                limits=["Still pays a log factor per genre. Since play counts are integers between 1 and n, buckets can order genres by count with no comparisons at all."],
            ),
            approach(
                "Buckets by play count",
                "best",
                "O(n + R)",
                "O(n + R)",
                idea=[
                    """
                    After counting, put each genre into `bucket[count]`, visiting genres in increasing id order so
                    every bucket is sorted by id. Then read buckets from the highest count (n) down, taking genres
                    until there are k. Ties are handled by the bucket's order; no sorting anywhere.
                    """
                ],
                walk=w4,
                build=["Count plays per genre (shifted index).", "Create buckets `0 … n`; for ids in increasing order, append each played genre to `bucket[count]`.", "Walk `c` from n down to 1, appending genres from `bucket[c]` until k are taken."],
                code={
                    "python": """
                        class Solution:
                            def topGenres(self, plays: List[int], k: int) -> List[int]:
                                count = [0] * 20001  #@count
                                for g in plays:  #@count
                                    count[g + 10000] += 1  #@count
                                bucket = [[] for _ in range(len(plays) + 1)]  #@fill
                                for i in range(20001):  #@fill
                                    if count[i]:  #@fill
                                        bucket[count[i]].append(i - 10000)  #@fill
                                out = []  #@read
                                for c in range(len(plays), 0, -1):  #@read
                                    for g in bucket[c]:  #@read
                                        if len(out) == k:  #@read
                                            return out  #@read
                                        out.append(g)  #@read
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] topGenres(int[] plays, int k) {
                                int n = plays.length;
                                int[] count = new int[20001];  //@count
                                for (int g : plays) count[g + 10000]++;  //@count
                                List<List<Integer>> bucket = new ArrayList<>();  //@fill
                                for (int c = 0; c <= n; c++) bucket.add(new ArrayList<>());  //@fill
                                for (int i = 0; i < 20001; i++) if (count[i] > 0) bucket.get(count[i]).add(i - 10000);  //@fill
                                int[] out = new int[k];  //@read
                                int taken = 0;  //@read
                                for (int c = n; c >= 1 && taken < k; c--)  //@read
                                    for (int g : bucket.get(c))  //@read
                                        if (taken < k) out[taken++] = g;  //@read
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> topGenres(vector<int>& plays, int k) {
                                int n = plays.size();
                                vector<int> count(20001, 0);  //@count
                                for (int g : plays) count[g + 10000]++;  //@count
                                vector<vector<int>> bucket(n + 1);  //@fill
                                for (int i = 0; i < 20001; i++) if (count[i]) bucket[count[i]].push_back(i - 10000);  //@fill
                                vector<int> out;  //@read
                                for (int c = n; c >= 1 && (int) out.size() < k; c--)  //@read
                                    for (int g : bucket[c])  //@read
                                        if ((int) out.size() < k) out.push_back(g);  //@read
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* topGenres(int* plays, int playsSize, int k, int* returnSize) {
                            int n = playsSize;
                            int* count = calloc(20001, sizeof(int));  //@count
                            for (int i = 0; i < n; i++) count[plays[i] + 10000]++;  //@count
                            int* head = malloc((n + 1) * sizeof(int));  //@fill
                            int* next = malloc(20001 * sizeof(int));  //@fill
                            for (int c = 0; c <= n; c++) head[c] = -1;  //@fill
                            for (int i = 20000; i >= 0; i--) {  //@fill
                                if (!count[i]) continue;  //@fill
                                next[i] = head[count[i]];  //@fill
                                head[count[i]] = i;  //@fill
                            }
                            int* out = malloc(k * sizeof(int));  //@read
                            int taken = 0;  //@read
                            for (int c = n; c >= 1 && taken < k; c--)  //@read
                                for (int i = head[c]; i != -1 && taken < k; i = next[i])  //@read
                                    out[taken++] = i - 10000;  //@read
                            free(count);  //@ret
                            free(head);  //@ret
                            free(next);  //@ret
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("count", "Plays per genre, ids shifted by 10⁴ into indices."),
                    ("fill", "Each played genre goes into the bucket for its count. Ids are visited smallest first, so each bucket is already ordered by id: exactly the tie rule.",
                     {"c": "Buckets as linked lists in two arrays: `head[c]` is the first genre with count c and `next[i]` the one after `i`. Walking ids from largest to smallest and pushing to the front leaves each list in increasing id order."}),
                    ("read", "From the highest possible count (n) downwards, take genres in bucket order until k are taken."),
                    ("ret", "The k most-played genres, best first.", {"c": "Free the scratch arrays and report the length."}),
                ],
                complexity=["**Time O(n + R):** counting, one pass over the R = 20,001 possible ids, and at most n buckets to read. **Space O(n + R).**"],
            ),
        ],
        takeaways=[
            """
            - **Top-k by frequency** = count, then select. Selection options: sort (d log d), size-k heap
              (d log k), buckets by count (linear).
            - For a heap of the "best k", keep the **weakest on top** so it's the one you compare against and
              evict.
            - Small, known id ranges (here −10⁴ … 10⁴) make an offset array a drop-in replacement for a hash map.
            - Ties are part of the order: encode them in the comparator, or get them for free by filling
              buckets in id order.
            """
        ],
    )
