"""Sorting: sorting by a custom order."""
import bisect
import functools

from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def follow_the_guide():
    items, guide = [5, 9, 2, 7, 9, 4, 5, 1], [9, 5, 3]
    rank = {v: i for i, v in enumerate(guide)}
    want = sorted(items, key=lambda x: (rank.get(x, len(guide)), x))

    w1 = Steps("Walk the guide; for each guide value, pull every matching item. Then sort whatever is left.")
    out, left = [], items[:]
    for g in guide:
        hits = [x for x in left if x == g]
        left = [x for x in left if x != g]
        out += hits
        w1.step(f"Guide value {g}: scan all items, take {len(hits)} match(es).", Row(out or ["·"], label="output"), Row(left or ["·"], label="left"))
    out += sorted(left)
    w1.step(f"Sort the leftovers {sorted(left)} and append: {out}.", Row(out, label="output"), result=str(out))

    w2 = Steps("Give every value a sort key: (its position in the guide, or 'after the guide'; then the value itself). One sort does the rest.")
    keys = [(rank.get(x, len(guide)), x) for x in items]
    w2.step(f"Guide positions: {rank}. Values not in the guide get position {len(guide)} (after all of them).", Row(items, label="items"), Row([f"{a},{b}" for a, b in keys], label="key (rank, value)"))
    w2.step(f"Sort by key: {want}.", Row(want, label="output"), result=str(want))

    sol(
        "follow-the-guide",
        summary="""
            Map each guide value to its position. Sort the items by the key (guide position, or one past the end if the
            value isn't in the guide; then the value itself). Guide values come out in guide order with repeats together,
            and the rest come after in increasing order. O((n + g) log n).
        """,
        question=[
            """
            Order `items` so values that appear in `guide` come first, in guide order (copies together), and all other values
            follow in increasing order.

            - **Guide values are distinct**; items can repeat.
            - **Up to 10⁵ items and guide entries**, values up to 10⁹.
            """
        ],
        think=[
            f"""
            Items `{items}`, guide `{guide}`. First both 9s, then both 5s; the guide's 3 isn't among the items, so it
            contributes nothing. Then 1, 2, 4, 7 in order. Answer: `{want}`.

            Any custom order is just a sort with the right **key**. Here the key is a pair: first the value's place in the
            guide (values not in the guide all share the place "after the guide"), then the value itself to order those
            leftovers.
            """,
            fig(Row(items, label="items"), Row(guide, label="guide"), Row(want, label="ordered")),
        ],
        approaches=[
            approach(
                "Pull matches for each guide value",
                "brute",
                "O(n·g + n log n)",
                "O(n)",
                idea=["For each guide value in order, scan the items and move every match to the output. Sort what's left and append it."],
                walk=w1,
                build=["Mark items as used.", "For each guide value, scan all items for matches.", "Sort the unused items and append."],
                code={
                    "python": """
                        class Solution:
                            def orderByGuide(self, items: List[int], guide: List[int]) -> List[int]:
                                out, used = [], [False] * len(items)  #@init
                                for g in guide:  #@pull
                                    for i, x in enumerate(items):  #@pull
                                        if x == g:  #@pull
                                            out.append(x)  #@pull
                                            used[i] = True  #@pull
                                rest = sorted(x for i, x in enumerate(items) if not used[i])  #@rest
                                return out + rest  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] orderByGuide(int[] items, int[] guide) {
                                int n = items.length, w = 0;  //@init
                                int[] out = new int[n];  //@init
                                boolean[] used = new boolean[n];  //@init
                                for (int g : guide)  //@pull
                                    for (int i = 0; i < n; i++)  //@pull
                                        if (items[i] == g) { out[w++] = g; used[i] = true; }  //@pull
                                int start = w;  //@rest
                                for (int i = 0; i < n; i++) if (!used[i]) out[w++] = items[i];  //@rest
                                Arrays.sort(out, start, n);  //@rest
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> orderByGuide(vector<int>& items, vector<int>& guide) {
                                int n = items.size();  //@init
                                vector<int> out;  //@init
                                vector<char> used(n, 0);  //@init
                                for (int g : guide)  //@pull
                                    for (int i = 0; i < n; i++)  //@pull
                                        if (items[i] == g) { out.push_back(g); used[i] = 1; }  //@pull
                                size_t start = out.size();  //@rest
                                for (int i = 0; i < n; i++) if (!used[i]) out.push_back(items[i]);  //@rest
                                sort(out.begin() + start, out.end());  //@rest
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmp_int(const void* x, const void* y) {  //@rest
                            int a = *(const int*) x, b = *(const int*) y;  //@rest
                            return (a > b) - (a < b);  //@rest
                        }  //@rest

                        int* orderByGuide(int* items, int itemsSize, int* guide, int guideSize, int* returnSize) {
                            int n = itemsSize, w = 0;  //@init
                            int* out = malloc(n * sizeof(int));  //@init
                            char* used = calloc(n, 1);  //@init
                            for (int g = 0; g < guideSize; g++)  //@pull
                                for (int i = 0; i < n; i++)  //@pull
                                    if (items[i] == guide[g]) { out[w++] = guide[g]; used[i] = 1; }  //@pull
                            int start = w;  //@rest
                            for (int i = 0; i < n; i++) if (!used[i]) out[w++] = items[i];  //@rest
                            qsort(out + start, n - start, sizeof(int), cmp_int);  //@rest
                            free(used);  //@ret
                            *returnSize = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "The output, and which items have been placed."), ("pull", "Guide values in order: every matching item goes out, so copies stay together."), ("rest", "Items not in the guide, sorted, go last."), ("ret", "Guide part, then the rest.")],
                complexity=["**Time O(n·g + n log n):** a full scan of the items for every guide value, up to 10¹⁰. **Space O(n).**"],
                limits=["Each guide value rescans every item. Instead, look up each item's guide position once (a hash map) and let a single sort place everything."],
                slow=True,
            ),
            approach(
                "Sort by (guide position, value)",
                "best",
                "O(n log n + g)",
                "O(n + g)",
                idea=["Build `rank[value] = position in guide`. Sort items by `(rank.get(x, g), x)`: values not in the guide all get rank `g`, after every guide value, and are then ordered by value."],
                walk=w2,
                build=["`rank` from the guide.", "Sort with the pair key.", "Return."],
                code={
                    "python": """
                        class Solution:
                            def orderByGuide(self, items: List[int], guide: List[int]) -> List[int]:
                                rank = {v: i for i, v in enumerate(guide)}  #@rank
                                after = len(guide)  #@rank
                                return sorted(items, key=lambda x: (rank.get(x, after), x))  #@sort
                    """,
                    "java": """
                        class Solution {
                            public int[] orderByGuide(int[] items, int[] guide) {
                                Map<Integer, Integer> rank = new HashMap<>();  //@rank
                                for (int i = 0; i < guide.length; i++) rank.put(guide[i], i);  //@rank
                                int after = guide.length;  //@rank
                                Integer[] boxed = Arrays.stream(items).boxed().toArray(Integer[]::new);  //@sort
                                Arrays.sort(boxed, Comparator.<Integer>comparingInt(x -> rank.getOrDefault(x, after)).thenComparingInt(x -> x));  //@sort
                                return Arrays.stream(boxed).mapToInt(Integer::intValue).toArray();  //@sort
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> orderByGuide(vector<int>& items, vector<int>& guide) {
                                unordered_map<int, int> rank;  //@rank
                                for (int i = 0; i < (int) guide.size(); i++) rank[guide[i]] = i;  //@rank
                                int after = guide.size();  //@rank
                                vector<pair<int, int>> keyed;  //@sort
                                for (int x : items) keyed.push_back({rank.count(x) ? rank[x] : after, x});  //@sort
                                sort(keyed.begin(), keyed.end());  //@sort
                                vector<int> out;  //@sort
                                for (auto& [r, x] : keyed) out.push_back(x);  //@sort
                                return out;  //@sort
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int value, rank; } Key;

                        static int by_value(const void* x, const void* y) {  //@rank
                            const Key *a = x, *b = y;  //@rank
                            return (a->value > b->value) - (a->value < b->value);  //@rank
                        }  //@rank

                        static int by_key(const void* x, const void* y) {  //@sort
                            const Key *a = x, *b = y;  //@sort
                            if (a->rank != b->rank) return a->rank - b->rank;  //@sort
                            return (a->value > b->value) - (a->value < b->value);  //@sort
                        }  //@sort

                        int* orderByGuide(int* items, int itemsSize, int* guide, int guideSize, int* returnSize) {
                            Key* g = malloc(guideSize * sizeof(Key));  //@rank
                            for (int i = 0; i < guideSize; i++) g[i] = (Key){guide[i], i};  //@rank
                            qsort(g, guideSize, sizeof(Key), by_value);  //@rank
                            Key* keyed = malloc(itemsSize * sizeof(Key));  //@sort
                            for (int i = 0; i < itemsSize; i++) {  //@sort
                                Key probe = {items[i], 0};  //@sort
                                Key* hit = bsearch(&probe, g, guideSize, sizeof(Key), by_value);  //@sort
                                keyed[i] = (Key){items[i], hit ? hit->rank : guideSize};  //@sort
                            }
                            qsort(keyed, itemsSize, sizeof(Key), by_key);  //@sort
                            int* out = malloc(itemsSize * sizeof(int));  //@sort
                            for (int i = 0; i < itemsSize; i++) out[i] = keyed[i].value;  //@sort
                            free(g); free(keyed);  //@sort
                            *returnSize = itemsSize;  //@sort
                            return out;  //@sort
                        }
                    """,
                },
                lines=[
                    ("rank", "Each guide value's position. Values not in the guide get `g`, which sorts after all of them.", {"c": "No hash map in C: sort the guide's (value, position) pairs by value and look values up with `bsearch`."}),
                    ("sort", "One sort by the pair (rank, value) puts guide values in guide order and the rest in increasing order after them.", {"java": "Sorting with a comparator needs boxed `Integer`s.", "c": "Attach each item's rank, then sort by (rank, value)."}),
                ],
                complexity=["**Time O(n log n + g).** **Space O(n + g).**"],
            ),
        ],
        takeaways=[
            """
            - **Custom orders are sorts with a composite key.** Put the most important rule first in the tuple.
            - Give "not in the list" a single rank larger than every listed one.
            - In C, a sorted array plus `bsearch` stands in for a hash map lookup.
            """
        ],
    )


@problem
def largest_number_from_pieces():
    pieces = [30, 3, 34, 5, 9]
    s = sorted(map(str, pieces), key=functools.cmp_to_key(lambda a, b: (a + b < b + a) - (a + b > b + a)))
    want = "".join(s)

    w1 = Steps("Bubble sort with the rule 'a goes before b when a+b is the bigger number'. Repeatedly swap neighbours that break the rule.")
    a = list(map(str, pieces))
    w1.step("Start.", Row(a))
    changed = True
    while changed:
        changed = False
        for i in range(len(a) - 1):
            if a[i] + a[i + 1] < a[i + 1] + a[i]:
                w1.step(f"{a[i]}{a[i + 1]} < {a[i + 1]}{a[i]}, so swap.", Row(a, st={i: "mark", i + 1: "mark"}))
                a[i], a[i + 1] = a[i + 1], a[i]
                changed = True
    w1.step(f"No more swaps: {''.join(a)}.", Row(a), result=want)

    w2 = Steps("Compare two pieces by gluing them both ways: put first whichever glued order makes the bigger number. Sort with that rule.")
    w2.step("Why not just sort by digits? '3' vs '30': '330' beats '303', so 3 goes first, even though 30 is bigger.", Row(["3", "30"]), Vars(**{"3+30": "330", "30+3": "303"}))
    w2.step("'3' vs '34': '343' beats '334', so 34 goes first.", Row(["34", "3"]), Vars(**{"34+3": "343", "3+34": "334"}))
    w2.step(f"Sort every piece with the rule: {s}.", Row(s))
    w2.step(f"Join: {want}.", result=want)

    sol(
        "largest-number-from-pieces",
        summary="""
            Put piece `a` before piece `b` exactly when the string `a + b` is larger than `b + a`. This rule is a consistent
            ordering, so sorting the pieces (as strings) by it and joining gives the largest number. Answer `"0"` if the
            result starts with 0 (all pieces were 0). O(n log n · L) for L digits.
        """,
        question=[
            """
            Arrange all the number pieces side by side to make the largest possible number, returned as a string with no
            leading zeros.

            - **Every piece is used**, each exactly once.
            - **Plain numeric order fails:** 30 is bigger than 3, but `330` beats `303`.
            - **All zeros** must give `"0"`, not `"000"`.
            """
        ],
        think=[
            f"""
            Pieces `{pieces}`. The best is `{want}`.

            Think about just two pieces side by side, `a` then `b`. Swapping them only changes that stretch of digits,
            `a + b` versus `b + a`, which have the same length. So `a` belongs first exactly when `a + b > b + a`. This
            pairwise rule turns out to be transitive (a proper ordering), so a sort with it arranges every pair correctly
            at once.
            """,
            fig(Row(pieces, label="pieces"), Row(s, label="arranged")),
        ],
        approaches=[
            approach(
                "Bubble sort with the glue rule",
                "brute",
                "O(n² · L)",
                "O(n · L)",
                idea=["Turn pieces into strings. Keep passing over the list, swapping neighbours whenever `b + a > a + b`, until a pass makes no swap."],
                walk=w1,
                build=["Strings.", "Repeat passes with neighbour swaps until stable.", "Join; fix the all-zero case."],
                code={
                    "python": """
                        class Solution:
                            def largestNumber(self, pieces: List[int]) -> str:
                                s = [str(p) for p in pieces]  #@strings
                                changed = True  #@bubble
                                while changed:  #@bubble
                                    changed = False  #@bubble
                                    for i in range(len(s) - 1):  #@bubble
                                        if s[i] + s[i + 1] < s[i + 1] + s[i]:  #@rule
                                            s[i], s[i + 1] = s[i + 1], s[i]  #@rule
                                            changed = True  #@rule
                                out = "".join(s)  #@ret
                                return "0" if out[0] == "0" else out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String largestNumber(int[] pieces) {
                                String[] s = new String[pieces.length];  //@strings
                                for (int i = 0; i < s.length; i++) s[i] = String.valueOf(pieces[i]);  //@strings
                                boolean changed = true;  //@bubble
                                while (changed) {  //@bubble
                                    changed = false;  //@bubble
                                    for (int i = 0; i + 1 < s.length; i++) {  //@bubble
                                        if ((s[i] + s[i + 1]).compareTo(s[i + 1] + s[i]) < 0) {  //@rule
                                            String t = s[i]; s[i] = s[i + 1]; s[i + 1] = t;  //@rule
                                            changed = true;  //@rule
                                        }
                                    }
                                }
                                String out = String.join("", s);  //@ret
                                return out.charAt(0) == '0' ? "0" : out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string largestNumber(vector<int>& pieces) {
                                vector<string> s;  //@strings
                                for (int p : pieces) s.push_back(to_string(p));  //@strings
                                bool changed = true;  //@bubble
                                while (changed) {  //@bubble
                                    changed = false;  //@bubble
                                    for (size_t i = 0; i + 1 < s.size(); i++) {  //@bubble
                                        if (s[i] + s[i + 1] < s[i + 1] + s[i]) {  //@rule
                                            swap(s[i], s[i + 1]);  //@rule
                                            changed = true;  //@rule
                                        }
                                    }
                                }
                                string out;  //@ret
                                for (auto& x : s) out += x;  //@ret
                                return out[0] == '0' ? "0" : out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int before(int a, int b) {  //@rule
                            char x[24], y[24];  //@rule
                            sprintf(x, "%d%d", a, b);  //@rule
                            sprintf(y, "%d%d", b, a);  //@rule
                            return strcmp(x, y) > 0;  //@rule
                        }  //@rule

                        char* largestNumber(int* pieces, int piecesSize) {
                            int* s = malloc(piecesSize * sizeof(int));  //@strings
                            memcpy(s, pieces, piecesSize * sizeof(int));  //@strings
                            int changed = 1;  //@bubble
                            while (changed) {  //@bubble
                                changed = 0;  //@bubble
                                for (int i = 0; i + 1 < piecesSize; i++)  //@bubble
                                    if (before(s[i + 1], s[i])) { int t = s[i]; s[i] = s[i + 1]; s[i + 1] = t; changed = 1; }  //@bubble
                            }
                            char* out = malloc(piecesSize * 11 + 1);  //@ret
                            int w = 0;  //@ret
                            for (int i = 0; i < piecesSize; i++) w += sprintf(out + w, "%d", s[i]);  //@ret
                            if (out[0] == '0') strcpy(out, "0");  //@ret
                            free(s);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("strings", "Work with the pieces' digits.", {"c": "Keep the numbers; the rule prints both glued orders to compare them."}), ("bubble", "Pass over the pieces until nothing moves."), ("rule", "`b` should come first when `b + a` is the bigger number. Both glued strings have the same length, so comparing them as text compares them as numbers."), ("ret", "Join; if the biggest arrangement starts with 0, every piece was 0.")],
                complexity=["**Time O(n² · L)** comparisons of glued strings. **Space O(n · L).**"],
                limits=["Bubble sort is quadratic: 10⁴ pieces means ~10⁸ string comparisons. The rule is a valid ordering, so any O(n log n) sort can use it."],
                slow=True,
            ),
            approach(
                "Sort with the glue comparator",
                "best",
                "O(n log n · L)",
                "O(n · L)",
                idea=["Sort the strings with the comparator `a before b ⟺ a + b > b + a`, join them, and return `\"0\"` if the result starts with 0."],
                walk=w2,
                build=["Strings.", "Sort with the comparator.", "Join; all-zero fix."],
                code={
                    "python": """
                        import functools

                        class Solution:
                            def largestNumber(self, pieces: List[int]) -> str:
                                s = [str(p) for p in pieces]  #@strings
                                rule = lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)  #@rule
                                s.sort(key=functools.cmp_to_key(rule))  #@sort
                                out = "".join(s)  #@ret
                                return "0" if out[0] == "0" else out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String largestNumber(int[] pieces) {
                                String[] s = new String[pieces.length];  //@strings
                                for (int i = 0; i < s.length; i++) s[i] = String.valueOf(pieces[i]);  //@strings
                                Arrays.sort(s, (a, b) -> (b + a).compareTo(a + b));  //@rule
                                String out = String.join("", s);  //@ret
                                return out.charAt(0) == '0' ? "0" : out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string largestNumber(vector<int>& pieces) {
                                vector<string> s;  //@strings
                                for (int p : pieces) s.push_back(to_string(p));  //@strings
                                sort(s.begin(), s.end(), [](const string& a, const string& b) { return a + b > b + a; });  //@rule
                                string out;  //@ret
                                for (auto& x : s) out += x;  //@ret
                                return out[0] == '0' ? "0" : out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int rule(const void* p, const void* q) {  //@rule
                            char x[24], y[24];  //@rule
                            sprintf(x, "%d%d", *(const int*) p, *(const int*) q);  //@rule
                            sprintf(y, "%d%d", *(const int*) q, *(const int*) p);  //@rule
                            return strcmp(y, x);  //@rule
                        }  //@rule

                        char* largestNumber(int* pieces, int piecesSize) {
                            int* s = malloc(piecesSize * sizeof(int));  //@strings
                            memcpy(s, pieces, piecesSize * sizeof(int));  //@strings
                            qsort(s, piecesSize, sizeof(int), rule);  //@sort
                            char* out = malloc(piecesSize * 11 + 1);  //@ret
                            int w = 0;  //@ret
                            for (int i = 0; i < piecesSize; i++) w += sprintf(out + w, "%d", s[i]);  //@ret
                            if (out[0] == '0') strcpy(out, "0");  //@ret
                            free(s);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("strings", "Pieces as digit strings.", {"c": "Keep the numbers; the comparator prints them glued both ways."}),
                    ("rule", "`a` before `b` when `a + b` is the bigger number (same length, so text comparison works).", {"java": "Comparing `b + a` with `a + b` puts the larger glued order first.", "cpp": "The comparator returns true when `a` should come first.", "c": "`strcmp(y, x)` is negative when `x = a b` is bigger, which puts `a` first."}),
                    ("sort", "Any comparison sort works, because the rule is a consistent ordering."),
                    ("ret", "Join; all zeros collapse to `\"0\"`."),
                ],
                complexity=["**Time O(n log n · L)** with L ≤ 10 digits per piece. **Space O(n · L).**"],
            ),
        ],
        takeaways=[
            """
            - When the best order depends on **how two items combine**, compare them by combining both ways.
            - Exchange argument: if swapping two neighbours never helps, the arrangement is optimal.
            - Watch the edge case where the "number" is all zeros.
            """
        ],
    )


@problem
def nesting_boxes():
    boxes = [[5, 4], [6, 4], [6, 7], [2, 3], [5, 6]]
    srt = sorted(boxes, key=lambda b: (b[0], -b[1]))
    tails = []
    for _, h in srt:
        i = bisect.bisect_left(tails, h)
        tails[i:i + 1] = [h]
    want = len(tails)

    w1 = Steps("Sort by width, then for each box find the longest chain ending with it by checking every smaller box before it.")
    a = sorted(boxes)
    dp = []
    for i, (w, h) in enumerate(a):
        best = max([dp[j] for j in range(i) if a[j][0] < w and a[j][1] < h], default=0) + 1
        dp.append(best)
        w1.step(f"Box {w}×{h}: the best chain it can end is {best} long.", Row([f"{x}×{y}" for x, y in a], st={i: "active", **{j: "found" for j in range(i) if a[j][0] < w and a[j][1] < h}}), Row(dp + ["·"] * (len(a) - i - 1), label="chain"))
    w1.step(f"Longest chain: {max(dp)}.", result=max(dp))

    w2 = Steps("Sort by width ascending, and equal widths by height descending. Now we only need the longest strictly increasing run of heights, found with 'patience' tails.")
    w2.step(f"Sorted: {[f'{x}×{y}' for x, y in srt]}. Equal widths go tallest first so two of them can't both join a chain.", Row([f"{x}×{y}" for x, y in srt]))
    tails = []
    for w, h in srt:
        i = bisect.bisect_left(tails, h)
        action = "extends the longest chain" if i == len(tails) else f"replaces {tails[i]} (a chain of length {i + 1} can now end lower)"
        tails[i:i + 1] = [h]
        w2.step(f"Height {h} (box {w}×{h}) {action}.", Row(tails, label="tails (smallest last height per chain length)"))
    w2.step(f"{len(tails)} chain lengths: the answer is {len(tails)}.", result=want)

    sol(
        "nesting-boxes",
        summary="""
            Sort boxes by width ascending, breaking width ties by height **descending**. Then a valid nesting is exactly a
            strictly increasing run of heights, so the answer is the longest increasing subsequence of the heights, found
            in O(n log n) with patience tails and binary search.
        """,
        question=[
            """
            A box fits in another only if it's strictly smaller in **both** width and height (no rotating). Return the most
            boxes you can nest in one chain.

            - **Equal widths can't nest**, even if the heights differ.
            - **Up to 10⁵ boxes**, so O(n²) is too slow.
            """
        ],
        think=[
            f"""
            Boxes `{boxes}`. One best chain is 2×3 ⊂ 5×4 ⊂ 6×7: **{want}** boxes.

            With two dimensions, fix one by sorting. After sorting by width, a chain must use increasing widths and
            increasing heights, so it's an increasing subsequence of the heights. The catch is equal widths: 6×4 and 6×7
            would look like an increasing pair. Sorting equal widths by height **descending** makes them a decreasing run,
            so an increasing subsequence can never take two of them.
            """,
            fig(Row([f"{w}×{h}" for w, h in boxes], label="boxes"), Row([f"{w}×{h}" for w, h in srt], label="sorted (w ↑, h ↓)")),
        ],
        approaches=[
            approach(
                "Sort by width, quadratic chain DP",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Sort by width. `chain[i]` = the longest nesting ending with box `i` = 1 + the best `chain[j]` over earlier boxes strictly smaller in both dimensions."],
                walk=w1,
                build=["Sort by width.", "For each `i`, scan all `j < i`.", "Answer = max of `chain`."],
                code={
                    "python": """
                        class Solution:
                            def maxNested(self, boxes: List[List[int]]) -> int:
                                a = sorted(boxes)  #@sort
                                chain = [1] * len(a)  #@dp
                                for i in range(len(a)):  #@dp
                                    for j in range(i):  #@dp
                                        if a[j][0] < a[i][0] and a[j][1] < a[i][1]:  #@fits
                                            chain[i] = max(chain[i], chain[j] + 1)  #@fits
                                return max(chain)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int maxNested(int[][] boxes) {
                                int[][] a = boxes.clone();  //@sort
                                Arrays.sort(a, (x, y) -> x[0] != y[0] ? x[0] - y[0] : x[1] - y[1]);  //@sort
                                int n = a.length, best = 0;  //@dp
                                int[] chain = new int[n];  //@dp
                                for (int i = 0; i < n; i++) {  //@dp
                                    chain[i] = 1;  //@dp
                                    for (int j = 0; j < i; j++)  //@dp
                                        if (a[j][0] < a[i][0] && a[j][1] < a[i][1]) chain[i] = Math.max(chain[i], chain[j] + 1);  //@fits
                                    best = Math.max(best, chain[i]);  //@ret
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int maxNested(vector<vector<int>>& boxes) {
                                vector<vector<int>> a = boxes;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                int n = a.size(), best = 0;  //@dp
                                vector<int> chain(n, 1);  //@dp
                                for (int i = 0; i < n; i++) {  //@dp
                                    for (int j = 0; j < i; j++)  //@dp
                                        if (a[j][0] < a[i][0] && a[j][1] < a[i][1]) chain[i] = max(chain[i], chain[j] + 1);  //@fits
                                    best = max(best, chain[i]);  //@ret
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int by_size(const void* x, const void* y) {  //@sort
                            const int *a = *(int* const*) x, *b = *(int* const*) y;  //@sort
                            return a[0] != b[0] ? a[0] - b[0] : a[1] - b[1];  //@sort
                        }  //@sort

                        int maxNested(int** boxes, int boxesSize, int* boxesColSize) {
                            int** a = malloc(boxesSize * sizeof(int*));  //@sort
                            memcpy(a, boxes, boxesSize * sizeof(int*));  //@sort
                            qsort(a, boxesSize, sizeof(int*), by_size);  //@sort
                            int* chain = malloc(boxesSize * sizeof(int));  //@dp
                            int best = 0;  //@dp
                            for (int i = 0; i < boxesSize; i++) {  //@dp
                                chain[i] = 1;  //@dp
                                for (int j = 0; j < i; j++)  //@dp
                                    if (a[j][0] < a[i][0] && a[j][1] < a[i][1] && chain[j] + 1 > chain[i]) chain[i] = chain[j] + 1;  //@fits
                                if (chain[i] > best) best = chain[i];  //@ret
                            }
                            free(a); free(chain);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("sort", "By width (then height): any box that fits inside box `i` comes before it.", {"c": "Sort an array of row pointers; the rows themselves don't move."}), ("dp", "`chain[i]`: longest nesting whose outermost box is `i`; every box alone is a chain of 1."), ("fits", "An earlier box strictly smaller in both dimensions can sit inside `i`."), ("ret", "The best chain over all outermost boxes.")],
                complexity=["**Time O(n²):** up to 5 × 10⁹ pairs for 10⁵ boxes. **Space O(n).**"],
                limits=["The inner scan looks at every earlier box. Once equal widths are ordered tallest first, the problem becomes a plain longest increasing subsequence of heights, which binary search solves in O(n log n)."],
                slow=True,
            ),
            approach(
                "Sort, then longest increasing heights",
                "best",
                "O(n log n)",
                "O(n)",
                idea=["Sort by `(width ascending, height descending)`. Keep `tails[L]` = the smallest possible height that ends a chain of length `L + 1`. For each height `h`, find the first tail `≥ h` (binary search): replace it with `h`, or append `h` if there's none. The answer is the number of tails."],
                walk=w2,
                build=["Sort with the tie rule.", "For each height, lower-bound search in `tails`.", "Replace or append.", "Return `len(tails)`."],
                code={
                    "python": """
                        import bisect

                        class Solution:
                            def maxNested(self, boxes: List[List[int]]) -> int:
                                tails = []  #@tails
                                for w, h in sorted(boxes, key=lambda b: (b[0], -b[1])):  #@sort
                                    i = bisect.bisect_left(tails, h)  #@search
                                    if i == len(tails):  #@place
                                        tails.append(h)  #@place
                                    else:  #@place
                                        tails[i] = h  #@place
                                return len(tails)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int maxNested(int[][] boxes) {
                                int[][] a = boxes.clone();  //@sort
                                Arrays.sort(a, (x, y) -> x[0] != y[0] ? x[0] - y[0] : y[1] - x[1]);  //@sort
                                int[] tails = new int[a.length];  //@tails
                                int len = 0;  //@tails
                                for (int[] b : a) {  //@sort
                                    int lo = 0, hi = len;  //@search
                                    while (lo < hi) { int mid = (lo + hi) >>> 1; if (tails[mid] < b[1]) lo = mid + 1; else hi = mid; }  //@search
                                    tails[lo] = b[1];  //@place
                                    if (lo == len) len++;  //@place
                                }
                                return len;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int maxNested(vector<vector<int>>& boxes) {
                                vector<vector<int>> a = boxes;  //@sort
                                sort(a.begin(), a.end(), [](auto& x, auto& y) { return x[0] != y[0] ? x[0] < y[0] : x[1] > y[1]; });  //@sort
                                vector<int> tails;  //@tails
                                for (auto& b : a) {  //@sort
                                    auto it = lower_bound(tails.begin(), tails.end(), b[1]);  //@search
                                    if (it == tails.end()) tails.push_back(b[1]);  //@place
                                    else *it = b[1];  //@place
                                }
                                return tails.size();  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int by_rule(const void* x, const void* y) {  //@sort
                            const int *a = *(int* const*) x, *b = *(int* const*) y;  //@sort
                            return a[0] != b[0] ? a[0] - b[0] : b[1] - a[1];  //@sort
                        }  //@sort

                        int maxNested(int** boxes, int boxesSize, int* boxesColSize) {
                            int** a = malloc(boxesSize * sizeof(int*));  //@sort
                            memcpy(a, boxes, boxesSize * sizeof(int*));  //@sort
                            qsort(a, boxesSize, sizeof(int*), by_rule);  //@sort
                            int* tails = malloc(boxesSize * sizeof(int));  //@tails
                            int len = 0;  //@tails
                            for (int i = 0; i < boxesSize; i++) {  //@sort
                                int h = a[i][1], lo = 0, hi = len;  //@search
                                while (lo < hi) { int mid = (lo + hi) / 2; if (tails[mid] < h) lo = mid + 1; else hi = mid; }  //@search
                                tails[lo] = h;  //@place
                                if (lo == len) len++;  //@place
                            }
                            free(a); free(tails);  //@ret
                            return len;  //@ret
                        }
                    """,
                },
                lines=[
                    ("sort", "Width ascending; equal widths tallest first, so at most one box per width can be in an increasing run of heights."),
                    ("tails", "`tails[L]` is the lowest height that can end a chain of length `L + 1`; it's always increasing."),
                    ("search", "The first tail that is `≥ h`. Using `≥` (not `>`) keeps the chain strictly increasing: an equal height can't extend a chain."),
                    ("place", "Replace that tail with the smaller `h` (more room for later boxes), or append if `h` beats every tail."),
                    ("ret", "The number of tails is the longest chain."),
                ],
                complexity=["**Time O(n log n)**: the sort plus a binary search per box. **Space O(n)** for the tails."],
            ),
        ],
        takeaways=[
            """
            - **2-D nesting = sort one dimension, longest increasing subsequence on the other.**
            - The tie rule (equal first key → second key descending) is what makes "strictly smaller in both" work.
            - Patience tails give LIS in O(n log n); `bisect_left` gives strict increase, `bisect_right` non-strict.
            """
        ],
    )


@problem
def reconstruct_the_line():
    people = [[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]
    line = []
    for h, k in sorted(people, key=lambda p: (-p[0], p[1])):
        line.insert(k, [h, k])
    want = line

    w1 = Steps("Shortest first: each person takes the empty spot that leaves exactly 'ahead' spots in front for taller-or-equal people still to come.")
    n = len(people)
    slots = [None] * n
    for h, k in sorted(people, key=lambda p: (p[0], -p[1])):
        empty = [i for i in range(n) if slots[i] is None]
        slots[empty[k]] = [h, k]
        w1.step(f"{h},{k}: everyone placed so far is shorter, so they don't count. Take empty spot number {k + 1} (index {empty[k]}).", Row([f"{s[0]},{s[1]}" if s else "·" for s in slots], st={empty[k]: "new"}))
    w1.step(f"Line: {slots}.", result=str(slots))

    w2 = Steps("Tallest first: when a person is placed, everyone already in line is at least as tall, so they slot in at index 'ahead'. Shorter people inserted later never change that count.")
    line = []
    for h, k in sorted(people, key=lambda p: (-p[0], p[1])):
        line.insert(k, [h, k])
        w2.step(f"{h},{k}: insert at index {k}.", Row([f"{a},{b}" for a, b in line], st={k: "new"}))
    w2.step(f"Line: {line}.", result=str(want))

    sol(
        "reconstruct-the-line",
        summary="""
            Place people tallest first (equal heights by `ahead` ascending), inserting each at index `ahead`: everyone
            already placed is at least as tall, so exactly `ahead` of them end up in front, and shorter people inserted
            later don't affect that count. O(n²) with list insertions, fine for n ≤ 2000.
        """,
        question=[
            """
            Each person is `[height, ahead]`: `ahead` people at least as tall stood in front of them. Rebuild the line from
            front to back.

            - **"At least as tall"** includes equal heights.
            - **A valid line always exists**, and at most 2000 people.
        """
        ],
        think=[
            f"""
            People `{people}` rebuild to `{want}`.

            Shorter people are invisible to a taller person's count. So if we place the tallest people first, each new
            person (shorter or equal) only cares about the people already placed, all of whom are at least as tall: put
            them at index `ahead`. Later, shorter people can be inserted anywhere without breaking anyone's count. Equal
            heights must go in increasing `ahead` order, so the one with more equals in front is placed after them.
            """,
            fig(Row([f"{h},{k}" for h, k in people], label="given"), Row([f"{h},{k}" for h, k in want], label="line")),
        ],
        approaches=[
            approach(
                "Shortest first into empty spots",
                "better",
                "O(n²)",
                "O(n)",
                idea=["Sort by height ascending, equal heights by `ahead` descending. Each person goes to the `(ahead + 1)`-th still-empty spot: the empty spots before it will be filled by taller (or equal) people later, exactly `ahead` of them."],
                walk=w1,
                build=["`n` empty slots.", "Sort shortest first (ties: larger `ahead` first).", "Count empty slots to find the `ahead`-th one (0-based); place there."],
                code={
                    "python": """
                        class Solution:
                            def rebuildLine(self, people: List[List[int]]) -> List[List[int]]:
                                n = len(people)  #@init
                                line = [None] * n  #@init
                                for h, k in sorted(people, key=lambda p: (p[0], -p[1])):  #@sort
                                    empty = -1  #@slot
                                    for i in range(n):  #@slot
                                        if line[i] is None:  #@slot
                                            empty += 1  #@slot
                                            if empty == k:  #@slot
                                                line[i] = [h, k]  #@slot
                                                break  #@slot
                                return line  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] rebuildLine(int[][] people) {
                                int n = people.length;  //@init
                                int[][] line = new int[n][];  //@init
                                int[][] a = people.clone();  //@sort
                                Arrays.sort(a, (x, y) -> x[0] != y[0] ? x[0] - y[0] : y[1] - x[1]);  //@sort
                                for (int[] p : a) {  //@slot
                                    int empty = -1;  //@slot
                                    for (int i = 0; i < n; i++)  //@slot
                                        if (line[i] == null && ++empty == p[1]) { line[i] = new int[] {p[0], p[1]}; break; }  //@slot
                                }
                                return line;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> rebuildLine(vector<vector<int>>& people) {
                                int n = people.size();  //@init
                                vector<vector<int>> line(n);  //@init
                                vector<vector<int>> a = people;  //@sort
                                sort(a.begin(), a.end(), [](auto& x, auto& y) { return x[0] != y[0] ? x[0] < y[0] : x[1] > y[1]; });  //@sort
                                for (auto& p : a) {  //@slot
                                    int empty = -1;  //@slot
                                    for (int i = 0; i < n; i++)  //@slot
                                        if (line[i].empty() && ++empty == p[1]) { line[i] = p; break; }  //@slot
                                }
                                return line;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int shortest_first(const void* x, const void* y) {  //@sort
                            const int *a = *(int* const*) x, *b = *(int* const*) y;  //@sort
                            return a[0] != b[0] ? a[0] - b[0] : b[1] - a[1];  //@sort
                        }  //@sort

                        int** rebuildLine(int** people, int peopleSize, int* peopleColSize, int* returnSize, int** returnColumnSizes) {
                            int n = peopleSize;  //@init
                            int** line = calloc(n, sizeof(int*));  //@init
                            int** a = malloc(n * sizeof(int*));  //@sort
                            memcpy(a, people, n * sizeof(int*));  //@sort
                            qsort(a, n, sizeof(int*), shortest_first);  //@sort
                            for (int p = 0; p < n; p++) {  //@slot
                                int empty = -1;  //@slot
                                for (int i = 0; i < n; i++)  //@slot
                                    if (!line[i] && ++empty == a[p][1]) {  //@slot
                                        line[i] = malloc(2 * sizeof(int));  //@slot
                                        line[i][0] = a[p][0];  //@slot
                                        line[i][1] = a[p][1];  //@slot
                                        break;  //@slot
                                    }
                            }
                            free(a);  //@ret
                            *returnSize = n;  //@ret
                            *returnColumnSizes = malloc(n * sizeof(int));  //@ret
                            for (int i = 0; i < n; i++) (*returnColumnSizes)[i] = 2;  //@ret
                            return line;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "An empty line of `n` spots."),
                    ("sort", "Shortest first. Among equal heights, larger `ahead` first: the equal person placed later must land in front of it, among the empty spots it left."),
                    ("slot", "Spots already filled hold shorter people, who don't count for this person. The empty spots in front will all get taller-or-equal people, so leave exactly `ahead` of them free in front."),
                    ("ret", "The full line.", {"c": "Every row has 2 columns."}),
                ],
                complexity=["**Time O(n²):** a scan of the slots per person. **Space O(n).**"],
                limits=["Correct, but the tie rule and slot counting are easy to get wrong. Placing the tallest first lets a plain list insertion at index `ahead` do the work."],
            ),
            approach(
                "Tallest first, insert at index ahead",
                "best",
                "O(n²)",
                "O(n)",
                idea=["Sort by height descending, equal heights by `ahead` ascending. Insert each person into the line at index `ahead`."],
                walk=w2,
                build=["Sort with the rule.", "`line.insert(ahead, person)` for each.", "Return the line."],
                code={
                    "python": """
                        class Solution:
                            def rebuildLine(self, people: List[List[int]]) -> List[List[int]]:
                                line = []  #@init
                                for h, k in sorted(people, key=lambda p: (-p[0], p[1])):  #@sort
                                    line.insert(k, [h, k])  #@insert
                                return line  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] rebuildLine(int[][] people) {
                                int[][] a = people.clone();  //@sort
                                Arrays.sort(a, (x, y) -> x[0] != y[0] ? y[0] - x[0] : x[1] - y[1]);  //@sort
                                List<int[]> line = new ArrayList<>();  //@init
                                for (int[] p : a) line.add(p[1], p);  //@insert
                                return line.toArray(new int[0][]);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> rebuildLine(vector<vector<int>>& people) {
                                vector<vector<int>> a = people;  //@sort
                                sort(a.begin(), a.end(), [](auto& x, auto& y) { return x[0] != y[0] ? x[0] > y[0] : x[1] < y[1]; });  //@sort
                                vector<vector<int>> line;  //@init
                                for (auto& p : a) line.insert(line.begin() + p[1], p);  //@insert
                                return line;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int tallest_first(const void* x, const void* y) {  //@sort
                            const int *a = *(int* const*) x, *b = *(int* const*) y;  //@sort
                            return a[0] != b[0] ? b[0] - a[0] : a[1] - b[1];  //@sort
                        }  //@sort

                        int** rebuildLine(int** people, int peopleSize, int* peopleColSize, int* returnSize, int** returnColumnSizes) {
                            int n = peopleSize;  //@init
                            int** a = malloc(n * sizeof(int*));  //@sort
                            memcpy(a, people, n * sizeof(int*));  //@sort
                            qsort(a, n, sizeof(int*), tallest_first);  //@sort
                            int** line = malloc(n * sizeof(int*));  //@init
                            for (int p = 0; p < n; p++) {  //@insert
                                int k = a[p][1];  //@insert
                                memmove(line + k + 1, line + k, (p - k) * sizeof(int*));  //@insert
                                line[k] = malloc(2 * sizeof(int));  //@insert
                                line[k][0] = a[p][0];  //@insert
                                line[k][1] = k;  //@insert
                            }
                            free(a);  //@ret
                            *returnSize = n;  //@ret
                            *returnColumnSizes = malloc(n * sizeof(int));  //@ret
                            for (int i = 0; i < n; i++) (*returnColumnSizes)[i] = 2;  //@ret
                            return line;  //@ret
                        }
                    """,
                },
                lines=[
                    ("sort", "Tallest first; equal heights by `ahead` ascending, so equals already placed are the ones that stand in front."),
                    ("init", "The line being built."),
                    ("insert", "Everyone already in line is at least as tall, so index `ahead` puts exactly `ahead` of them in front. Later (shorter) arrivals don't change this person's count.", {"c": "Shift the tail of the array one place right with `memmove` to open index `ahead`."}),
                    ("ret", "The line, front to back.", {"c": "Every row has 2 columns."}),
                ],
                complexity=["**Time O(n²):** each insertion shifts up to n entries (≈ 2 × 10⁶ moves for n = 2000). **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - Process items in the order where **later items can't disturb earlier decisions**: here, tallest first.
            - A greedy that inserts by position is easy to prove when the counted things are exactly the ones placed so far.
            - Tie rules matter: equal heights must go in increasing `ahead` order.
            """
        ],
    )
