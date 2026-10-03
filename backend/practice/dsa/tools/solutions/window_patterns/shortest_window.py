"""Sliding Window: the shortest window that satisfies a rule (grow until valid, then shrink while it stays valid)."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def shrink_walk(w, shown, n, valid, info=None):
    """Grow right; while the window is valid, record it and drop the left element."""
    l, best = 0, None
    for r in range(n):
        start = l
        while l <= r and valid(l, r):
            if best is None or r - l + 1 < best[0]:
                best = (r - l + 1, l)
            l += 1
        if l > start:
            note = f" Valid: shrink while it stays valid (shortest ending here: {l - 1}..{r}, length {r - l + 2})."
            st = {**{x: "found" for x in range(l - 1, r + 1)}, **{x: "dim" for x in range(start, l - 1)}}
        else:
            note = " Not valid yet."
            st = {x: "active" for x in range(l, r + 1)}
        w.step(f"Add {shown[r]} (index {r}).{note}", Row(shown, st=st), Vars(best=best[0] if best else "—", **(info(l, r) if info else {})))
    return best


def first_valid_walk(w, shown, n, valid):
    """Brute force: from each start, extend until the window first becomes valid."""
    best = None
    for l in range(n):
        r = l
        while r < n and not valid(l, r):
            r += 1
        if r < n:
            if best is None or r - l + 1 < best[0]:
                best = (r - l + 1, l)
            w.step(f"From {l}: first valid at {r}, length {r - l + 1}.", Row(shown, st={x: "found" for x in range(l, r + 1)}), Vars(best=best[0]))
        else:
            w.step(f"From {l}: never valid.", Row(shown, st={x: "dim" for x in range(l, n)}), Vars(best=best[0] if best else "—"))
            break
    return best


COMPRESS_C = """
                        static int cmp_int(const void* a, const void* b) {  //@compress
                            int x = *(const int*) a, y = *(const int*) b;  //@compress
                            return (x > y) - (x < y);  //@compress
                        }  //@compress

                        static int* compress(const int* v, int n, int* distinct) {  //@compress
                            int* sorted = malloc(n * sizeof(int));  //@compress
                            memcpy(sorted, v, n * sizeof(int));  //@compress
                            qsort(sorted, n, sizeof(int), cmp_int);  //@compress
                            int d = 0;  //@compress
                            for (int i = 0; i < n; i++) if (i == 0 || sorted[i] != sorted[i - 1]) sorted[d++] = sorted[i];  //@compress
                            int* id = malloc(n * sizeof(int));  //@compress
                            for (int i = 0; i < n; i++) id[i] = (int) ((int*) bsearch(&v[i], sorted, d, sizeof(int), cmp_int) - sorted);  //@compress
                            free(sorted);  //@compress
                            *distinct = d;  //@compress
                            return id;  //@compress
                        }  //@compress
                    """


@problem
def shortest_push():
    gains, target = [2, 3, 1, 2, 4, 3, 1, 5], 9
    n = len(gains)
    valid = lambda l, r: sum(gains[l:r + 1]) >= target
    want = min([r - l + 1 for l in range(n) for r in range(l, n) if valid(l, r)] or [0])

    w1 = Steps("From each hour, add hours until the total reaches the target.")
    first_valid_walk(w1, gains, n, valid)
    w1.step(f"Fewest hours: {want}.", result=want)

    w2 = Steps("Grow the window; whenever it reaches the target, record it and drop hours from the left while it still does.")
    shrink_walk(w2, gains, n, valid, lambda l, r: {"sum": sum(gains[l:r + 1])})
    w2.step(f"Fewest hours: {want}.", result=want)

    sol(
        "shortest-push",
        summary="""
            Gains are positive, so extending a window raises its total and shrinking lowers it. Grow the right edge; as
            soon as the total reaches the target, record the length and drop hours from the left while it still reaches
            it. Every window that is minimal for its right end gets recorded. O(n).
        """,
        question=[
            """
            Return the fewest consecutive hours whose gains sum to at least `target`, or 0 if none.

            - **n up to 10⁵**, gains positive.
            """
        ],
        think=[
            f"""
            `gains = {gains}`, `target = {target}` → **{want}** hours.

            The mirror image of "longest window under a budget": here valid windows are those with a large enough sum,
            and adding hours keeps a window valid. For each right end, the best window is the one with the left edge as
            far right as possible, and that left edge never moves back as the right end advances.
            """,
            fig(Row(gains, label="gains")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start, add hours until the total reaches the target; record the length."],
                walk=w1,
                build=["Loop over starts.", "Extend until reaching the target.", "Keep the shortest."],
                code={
                    "python": """
                        class Solution:
                            def shortestPush(self, gains: List[int], target: int) -> int:
                                n, best = len(gains), 0  #@init
                                for i in range(n):  #@starts
                                    total = 0  #@extend
                                    for j in range(i, n):  #@extend
                                        total += gains[j]  #@extend
                                        if total >= target:  #@record
                                            if best == 0 or j - i + 1 < best:  #@record
                                                best = j - i + 1  #@record
                                            break  #@record
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestPush(int[] gains, int target) {
                                int n = gains.length, best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    long total = 0;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        total += gains[j];  //@extend
                                        if (total >= target) {  //@record
                                            if (best == 0 || j - i + 1 < best) best = j - i + 1;  //@record
                                            break;  //@record
                                        }
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestPush(vector<int>& gains, int target) {
                                int n = gains.size(), best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    long long total = 0;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        total += gains[j];  //@extend
                                        if (total >= target) {  //@record
                                            if (best == 0 || j - i + 1 < best) best = j - i + 1;  //@record
                                            break;  //@record
                                        }
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int shortestPush(int* gains, int gainsSize, int target) {
                            int n = gainsSize, best = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                long long total = 0;  //@extend
                                for (int j = i; j < n; j++) {  //@extend
                                    total += gains[j];  //@extend
                                    if (total >= target) {  //@record
                                        if (best == 0 || j - i + 1 < best) best = j - i + 1;  //@record
                                        break;  //@record
                                    }
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "0 means nothing found yet."), ("starts", "Each starting hour."), ("extend", "Accumulate hours."), ("record", "The first time the total reaches the target is the shortest push from this start."), ("ret", "Fewest hours, or 0.")],
                complexity=["**Time O(n²)** when the target is large. **Space O(1).**"],
                limits=["Restarts the sum for every start; the window approach reuses it."],
                slow=True,
            ),
            approach(
                "Shrinking window",
                "best",
                "O(n)",
                "O(1)",
                idea=["Add `gains[r]`. While `total ≥ target`: record `r − left + 1`, subtract `gains[left]`, advance `left`."],
                walk=w2,
                build=["Running total.", "Record and shrink while the target is met.", "0 if never met."],
                code={
                    "python": """
                        class Solution:
                            def shortestPush(self, gains: List[int], target: int) -> int:
                                left = total = 0  #@init
                                best = len(gains) + 1  #@init
                                for i, g in enumerate(gains):  #@grow
                                    total += g  #@grow
                                    while total >= target:  #@shrink
                                        best = min(best, i - left + 1)  #@shrink
                                        total -= gains[left]  #@shrink
                                        left += 1  #@shrink
                                return best if best <= len(gains) else 0  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestPush(int[] gains, int target) {
                                int n = gains.length, left = 0, best = n + 1;  //@init
                                long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@grow
                                    total += gains[i];  //@grow
                                    while (total >= target) {  //@shrink
                                        best = Math.min(best, i - left + 1);  //@shrink
                                        total -= gains[left++];  //@shrink
                                    }
                                }
                                return best <= n ? best : 0;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestPush(vector<int>& gains, int target) {
                                int n = gains.size(), left = 0, best = n + 1;  //@init
                                long long total = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@grow
                                    total += gains[i];  //@grow
                                    while (total >= target) {  //@shrink
                                        best = min(best, i - left + 1);  //@shrink
                                        total -= gains[left++];  //@shrink
                                    }
                                }
                                return best <= n ? best : 0;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int shortestPush(int* gains, int gainsSize, int target) {
                            int n = gainsSize, left = 0, best = n + 1;  //@init
                            long long total = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@grow
                                total += gains[i];  //@grow
                                while (total >= target) {  //@shrink
                                    if (i - left + 1 < best) best = i - left + 1;  //@shrink
                                    total -= gains[left++];  //@shrink
                                }
                            }
                            return best <= n ? best : 0;  //@ret
                        }
                    """,
                },
                lines=[("init", "`n + 1` stands for 'not found'."), ("grow", "Add hour `i`."), ("shrink", "While the window reaches the target, it's a candidate; dropping the leftmost hour tries a shorter one."), ("ret", "Translate 'not found' to 0.")],
                complexity=["**Time O(n):** each hour enters and leaves once. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Shortest window with a "big enough" rule:** grow until valid, then shrink while valid, recording each time.
            - Needs monotonicity: positive values make sums grow with the window.
            - Use a sentinel (`n + 1`) for "not found".
            """
        ],
    )


@problem
def every_flavour_sampler():
    jars = [7, 3, 7, 7, 9, 3, 3, 9, 7, 1, 3]
    n, d = len(jars), len(set(jars))
    valid = lambda l, r: len(set(jars[l:r + 1])) == d
    want = min(r - l + 1 for l in range(n) for r in range(l, n) if valid(l, r))

    w1 = Steps(f"There are {d} flavours. From each jar, extend until all of them are in the stretch.")
    first_valid_walk(w1, jars, n, valid)
    w1.step(f"Shortest: {want}.", result=want)

    w2 = Steps("Grow the window with flavour counts. Once it holds every flavour, record it and drop jars from the left until a flavour is missing.")
    shrink_walk(w2, jars, n, valid, lambda l, r: {"flavours inside": len(set(jars[l:r + 1]))})
    w2.step(f"Shortest: {want}.", result=want)

    sol(
        "every-flavour-sampler",
        summary="""
            Count the distinct flavours `d` first. Then slide a window with a count per flavour and the number present;
            whenever all `d` are present, record the length and shrink from the left until one goes missing. Flavours are
            large numbers, so use a hash map (or compress them to small ids). O(n).
        """,
        question=[
            """
            Return the length of the shortest stretch of consecutive jars that includes every flavour appearing on the
            shelf.

            - **n up to 10⁵**, flavours up to 10⁹.
            """
        ],
        think=[
            f"""
            `jars = {jars}` has {d} flavours; the shortest stretch with all of them has length **{want}**.

            Adding jars never removes a flavour, so "contains everything" stays true when the window grows: for each right
            end there's a latest left edge that still works, and it only moves right. That's the shrinking-window
            pattern, with a counter of how many flavours are currently present.
            """,
            fig(Row(jars, label="jars")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["For each start, add jars to a set until it has all `d` flavours."],
                walk=w1,
                build=["Count flavours.", "Extend from each start.", "Keep the shortest."],
                code={
                    "python": """
                        class Solution:
                            def shortestSampler(self, jars: List[int]) -> int:
                                n, d = len(jars), len(set(jars))  #@init
                                best = n  #@init
                                for i in range(n):  #@starts
                                    seen = set()  #@extend
                                    for j in range(i, min(n, i + best)):  #@extend
                                        seen.add(jars[j])  #@extend
                                        if len(seen) == d:  #@extend
                                            best = j - i + 1  #@extend
                                            break  #@extend
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestSampler(int[] jars) {
                                int n = jars.length, d = (int) Arrays.stream(jars).distinct().count(), best = n;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    Set<Integer> seen = new HashSet<>();  //@extend
                                    for (int j = i; j < Math.min(n, i + best); j++) {  //@extend
                                        seen.add(jars[j]);  //@extend
                                        if (seen.size() == d) { best = j - i + 1; break; }  //@extend
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestSampler(vector<int>& jars) {
                                int n = jars.size(), d = unordered_set<int>(jars.begin(), jars.end()).size(), best = n;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    unordered_set<int> seen;  //@extend
                                    for (int j = i; j < min(n, i + best); j++) {  //@extend
                                        seen.insert(jars[j]);  //@extend
                                        if ((int) seen.size() == d) { best = j - i + 1; break; }  //@extend
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": COMPRESS_C.rstrip(" ") + """
                        int shortestSampler(int* jars, int jarsSize) {
                            int n = jarsSize, d;  //@init
                            int* id = compress(jars, n, &d);  //@init
                            int* mark = calloc(d, sizeof(int));  //@init
                            int best = n;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                int have = 0;  //@extend
                                for (int j = i; j < n && j < i + best; j++) {  //@extend
                                    if (mark[id[j]] != i + 1) { mark[id[j]] = i + 1; have++; }  //@extend
                                    if (have == d) { best = j - i + 1; break; }  //@extend
                                }
                            }
                            free(id); free(mark);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "`d` distinct flavours; the whole shelf always works.", {"c": "Compress the flavours to ids `0..d−1`."}),
                    ("starts", "Each start."),
                    ("extend", "Extend until every flavour is seen; only stretches shorter than the best are worth trying.", {"c": "`mark[f] = i + 1` means 'seen from start `i`', which avoids clearing an array per start."}),
                    ("compress", "Sort a copy, remove duplicates, and find each flavour's position by binary search."),
                    ("ret", "Shortest stretch."),
                ],
                complexity=["**Time O(n²)** in the worst case. **Space O(n).**"],
                limits=["Each start rebuilds the seen set from scratch."],
                slow=True,
            ),
            approach(
                "Shrinking window with flavour counts",
                "best",
                "O(n)",
                "O(n)",
                idea=["`count[f]` for the window, `have` = flavours with a positive count. Add `jars[r]`; while `have == d`, record and remove `jars[left]`."],
                walk=w2,
                build=["Number of flavours.", "Counts and `have`.", "Record and shrink while complete."],
                code={
                    "python": """
                        class Solution:
                            def shortestSampler(self, jars: List[int]) -> int:
                                d = len(set(jars))  #@init
                                count, have, left, best = {}, 0, 0, len(jars)  #@init
                                for i, f in enumerate(jars):  #@grow
                                    count[f] = count.get(f, 0) + 1  #@grow
                                    if count[f] == 1:  #@grow
                                        have += 1  #@grow
                                    while have == d:  #@shrink
                                        best = min(best, i - left + 1)  #@shrink
                                        g = jars[left]  #@shrink
                                        count[g] -= 1  #@shrink
                                        if count[g] == 0:  #@shrink
                                            have -= 1  #@shrink
                                        left += 1  #@shrink
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestSampler(int[] jars) {
                                int n = jars.length, d = (int) Arrays.stream(jars).distinct().count();  //@init
                                Map<Integer, Integer> count = new HashMap<>();  //@init
                                int have = 0, left = 0, best = n;  //@init
                                for (int i = 0; i < n; i++) {  //@grow
                                    if (count.merge(jars[i], 1, Integer::sum) == 1) have++;  //@grow
                                    while (have == d) {  //@shrink
                                        best = Math.min(best, i - left + 1);  //@shrink
                                        if (count.merge(jars[left++], -1, Integer::sum) == 0) have--;  //@shrink
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestSampler(vector<int>& jars) {
                                int n = jars.size(), d = unordered_set<int>(jars.begin(), jars.end()).size();  //@init
                                unordered_map<int, int> count;  //@init
                                int have = 0, left = 0, best = n;  //@init
                                for (int i = 0; i < n; i++) {  //@grow
                                    if (++count[jars[i]] == 1) have++;  //@grow
                                    while (have == d) {  //@shrink
                                        best = min(best, i - left + 1);  //@shrink
                                        if (--count[jars[left++]] == 0) have--;  //@shrink
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": COMPRESS_C.rstrip(" ") + """
                        int shortestSampler(int* jars, int jarsSize) {
                            int n = jarsSize, d;  //@init
                            int* id = compress(jars, n, &d);  //@init
                            int* count = calloc(d, sizeof(int));  //@init
                            int have = 0, left = 0, best = n;  //@init
                            for (int i = 0; i < n; i++) {  //@grow
                                if (count[id[i]]++ == 0) have++;  //@grow
                                while (have == d) {  //@shrink
                                    if (i - left + 1 < best) best = i - left + 1;  //@shrink
                                    if (--count[id[left++]] == 0) have--;  //@shrink
                                }
                            }
                            free(id); free(count);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Distinct flavours `d`, empty window.", {"c": "Compress flavours to ids so the counts can be a plain array."}),
                    ("compress", "Sort a copy, remove duplicates, and find each flavour's position by binary search."),
                    ("grow", "Add jar `i`; a flavour going from 0 to 1 is newly present."),
                    ("shrink", "Complete window: record it, then drop the leftmost jar; if that was its flavour's last copy, the window is incomplete again."),
                    ("ret", "Shortest complete stretch."),
                ],
                complexity=["**Time O(n)** expected (O(n log n) for C's compression). **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - **Shortest window containing all kinds:** counts + a "kinds present" counter.
            - Large keys: hash map, or compress to `0..d−1` once.
            - Record inside the shrink loop: each recorded window is minimal for its right end.
            """
        ],
    )



@problem
def balance_the_quartet():
    s = "SSATSSBS"
    n, q = len(s), len(s) // 4

    def outside_ok(l, r):
        rest = s[:l] + s[r + 1:]
        return all(rest.count(c) <= q for c in "SATB")
    want = min(r - l + 1 for l in range(n) for r in range(l, n) if outside_ok(l, r))
    extra = {c: s.count(c) - q for c in "SATB" if s.count(c) > q}

    w1 = Steps("From each start, extend the piece until the singers left outside have at most n/4 of every voice.")
    first_valid_walk(w1, list(s), n, outside_ok)
    w1.step(f"Shortest piece: {want}.", result=want)

    w2 = Steps("Count voices outside the window. Grow the window (removing singers from 'outside'); while every outside count is ≤ n/4, record the window and shrink it from the left.")
    shrink_walk(w2, list(s), n, outside_ok, lambda l, r: {"outside": " · ".join(f"{c} {(s[:l] + s[r + 1:]).count(c)}" for c in "SATB")})
    w2.step(f"Shortest piece: {want}.", result=want)

    sol(
        "balance-the-quartet",
        summary="""
            A piece works exactly when the singers outside it have at most `n/4` of each voice: then the piece can be
            repainted to fill every shortfall. Keep counts of the voices outside a sliding window; grow the window, and
            while the outside is within limits, record the window and shrink it. O(n).
        """,
        question=[
            """
            Repaint one contiguous piece of `s` (any voices you like) so each of `S A T B` appears exactly `n/4` times.
            Return the shortest such piece (0 if already balanced).

            - **n up to 10⁵**, a multiple of 4.
            """
        ],
        think=[
            f"""
            `"{s}"` (n/4 = {q}): the surplus is {extra}, so the piece must at least contain those extra singers. Answer:
            **{want}**.

            What's outside the piece stays as it is, so no voice may exceed `{q}` outside. Conversely, if every voice is
            at most `{q}` outside, the piece has exactly enough singers to top each voice up to `{q}` (the counts add up to
            `n`). So the condition only depends on the outside counts, and it stays true when the piece grows: a shortest
            window problem.
            """,
            fig(Row(list(s), label="s")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["If already balanced, 0. Otherwise, for each start, extend the piece (moving singers from the outside counts) until every outside count is ≤ `n/4`."],
                walk=w1,
                build=["Voice counts.", "Extend from each start.", "Keep the shortest."],
                code={
                    "python": """
                        class Solution:
                            def shortestFix(self, s: str) -> int:
                                n, q = len(s), len(s) // 4  #@init
                                total = {c: s.count(c) for c in "SATB"}  #@init
                                if all(v == q for v in total.values()):  #@init
                                    return 0  #@init
                                best = n  #@init
                                for i in range(n):  #@starts
                                    out = dict(total)  #@extend
                                    for j in range(i, n):  #@extend
                                        out[s[j]] -= 1  #@extend
                                        if all(v <= q for v in out.values()):  #@extend
                                            best = min(best, j - i + 1)  #@extend
                                            break  #@extend
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestFix(String s) {
                                int n = s.length(), q = n / 4, best = n;  //@init
                                int[] total = new int[128];  //@init
                                for (char c : s.toCharArray()) total[c]++;  //@init
                                if (total['S'] == q && total['A'] == q && total['T'] == q) return 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int[] out = total.clone();  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        out[s.charAt(j)]--;  //@extend
                                        if (out['S'] <= q && out['A'] <= q && out['T'] <= q && out['B'] <= q) { best = Math.min(best, j - i + 1); break; }  //@extend
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestFix(string& s) {
                                int n = s.size(), q = n / 4, best = n;  //@init
                                array<int, 128> total{};  //@init
                                for (char c : s) total[c]++;  //@init
                                if (total['S'] == q && total['A'] == q && total['T'] == q) return 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    array<int, 128> out = total;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        out[s[j]]--;  //@extend
                                        if (out['S'] <= q && out['A'] <= q && out['T'] <= q && out['B'] <= q) { best = min(best, j - i + 1); break; }  //@extend
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int shortestFix(char* s) {
                            int n = strlen(s), q = n / 4, best = n, total[128] = {0};  //@init
                            for (int i = 0; i < n; i++) total[(int) s[i]]++;  //@init
                            if (total['S'] == q && total['A'] == q && total['T'] == q) return 0;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                int out[128];  //@extend
                                memcpy(out, total, sizeof(out));  //@extend
                                for (int j = i; j < n; j++) {  //@extend
                                    out[(int) s[j]]--;  //@extend
                                    if (out['S'] <= q && out['A'] <= q && out['T'] <= q && out['B'] <= q) { if (j - i + 1 < best) best = j - i + 1; break; }  //@extend
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Voice counts; if three voices are at `n/4`, so is the fourth, and nothing needs changing."),
                    ("starts", "Each start of the piece."),
                    ("extend", "Move singers into the piece until no voice outside exceeds `n/4`."),
                    ("ret", "Shortest piece."),
                ],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["Restarts the outside counts for every start."],
                slow=True,
            ),
            approach(
                "Shrinking window on the outside counts",
                "best",
                "O(n)",
                "O(1)",
                idea=["`out[c]` = count of voice `c` outside the window (initially all of `s`). For each `r`: `out[s[r]] −= 1`; while every `out[c] ≤ n/4`: record, `out[s[left]] += 1`, `left += 1`."],
                walk=w2,
                build=["Counts start as the whole string.", "Window takes singers out of the counts.", "Record and shrink while the outside is fine."],
                code={
                    "python": """
                        class Solution:
                            def shortestFix(self, s: str) -> int:
                                n, q = len(s), len(s) // 4  #@init
                                out = {c: s.count(c) for c in "SATB"}  #@init
                                if all(v == q for v in out.values()):  #@init
                                    return 0  #@init
                                best, left = n, 0  #@init
                                for i, c in enumerate(s):  #@grow
                                    out[c] -= 1  #@grow
                                    while all(v <= q for v in out.values()):  #@shrink
                                        best = min(best, i - left + 1)  #@shrink
                                        out[s[left]] += 1  #@shrink
                                        left += 1  #@shrink
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int shortestFix(String s) {
                                int n = s.length(), q = n / 4, best = n, left = 0;  //@init
                                int[] out = new int[128];  //@init
                                for (char c : s.toCharArray()) out[c]++;  //@init
                                if (out['S'] == q && out['A'] == q && out['T'] == q) return 0;  //@init
                                for (int i = 0; i < n; i++) {  //@grow
                                    out[s.charAt(i)]--;  //@grow
                                    while (out['S'] <= q && out['A'] <= q && out['T'] <= q && out['B'] <= q) {  //@shrink
                                        best = Math.min(best, i - left + 1);  //@shrink
                                        out[s.charAt(left++)]++;  //@shrink
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int shortestFix(string& s) {
                                int n = s.size(), q = n / 4, best = n, left = 0;  //@init
                                array<int, 128> out{};  //@init
                                for (char c : s) out[c]++;  //@init
                                if (out['S'] == q && out['A'] == q && out['T'] == q) return 0;  //@init
                                for (int i = 0; i < n; i++) {  //@grow
                                    out[s[i]]--;  //@grow
                                    while (out['S'] <= q && out['A'] <= q && out['T'] <= q && out['B'] <= q) {  //@shrink
                                        best = min(best, i - left + 1);  //@shrink
                                        out[s[left++]]++;  //@shrink
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int shortestFix(char* s) {
                            int n = strlen(s), q = n / 4, best = n, left = 0, out[128] = {0};  //@init
                            for (int i = 0; i < n; i++) out[(int) s[i]]++;  //@init
                            if (out['S'] == q && out['A'] == q && out['T'] == q) return 0;  //@init
                            for (int i = 0; i < n; i++) {  //@grow
                                out[(int) s[i]]--;  //@grow
                                while (out['S'] <= q && out['A'] <= q && out['T'] <= q && out['B'] <= q) {  //@shrink
                                    if (i - left + 1 < best) best = i - left + 1;  //@shrink
                                    out[(int) s[left++]]++;  //@shrink
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Before any window, everyone is outside. Already balanced means 0."),
                    ("grow", "Singer `i` joins the piece."),
                    ("shrink", "The outside is within limits, so this piece works; try giving back the leftmost singer. (It can't shrink to empty, since the string isn't balanced.)"),
                    ("ret", "Shortest piece."),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Reframe "what to change" as "what stays":** the outside must already be within limits.
            - Track counts of the complement of the window.
            - Then it's the standard shortest-valid-window template.
            """
        ],
    )


def trail_ref(s, t):
    m = len(t)
    start = [-1] * (m + 1)
    best = (len(s) + 1, 0)
    for i, c in enumerate(s):
        for j in range(m, 0, -1):
            if t[j - 1] == c:
                start[j] = i if j == 1 else start[j - 1]
        if start[m] >= 0 and i - start[m] + 1 < best[0]:
            best = (i - start[m] + 1, start[m])
    return s[best[1]:best[1] + best[0]] if best[0] <= len(s) else ""


@problem
def shortest_trail_window():
    s, t = "cabxbcaxbyc", "abc"
    m = len(t)
    want = trail_ref(s, t)

    w1 = Steps(f"From every position holding '{t[0]}', follow the route greedily to the right; the first place it finishes gives the shortest window from that start.")
    best = None
    for i, c in enumerate(s):
        if c != t[0]:
            continue
        j, k = 0, i
        while k < len(s):
            if s[k] == t[j]:
                j += 1
                if j == m:
                    break
            k += 1
        if j == m:
            if best is None or k - i + 1 < best[0]:
                best = (k - i + 1, i)
            w1.step(f"From {i}: the route finishes at {k}, window '{s[i:k + 1]}'.", Row(list(s), st={x: "found" for x in range(i, k + 1)}), Vars(best=s[best[1]:best[1] + best[0]]))
        else:
            w1.step(f"From {i}: the route never finishes.", Row(list(s), st={x: "dim" for x in range(i, len(s))}))
    w1.step(f"Shortest: '{want}'.", result=want)

    w2 = Steps("start[j] = latest index where a window ending here can begin and still contain t[0..j) in order. Process s left to right; when s[i] = t[j−1], start[j] inherits start[j−1] (or i itself for j = 1).")
    start = [-1] * (m + 1)
    best = (len(s) + 1, 0)
    for i, c in enumerate(s):
        changed = False
        for j in range(m, 0, -1):
            if t[j - 1] == c:
                start[j] = i if j == 1 else start[j - 1]
                changed = True
        if start[m] >= 0 and i - start[m] + 1 < best[0]:
            best = (i - start[m] + 1, start[m])
        if changed:
            w2.step(f"'{c}' at {i}: start = {start[1:]}." + (f" Full route from {start[m]}: '{s[start[m]:i + 1]}'." if start[m] >= 0 else ""), Row(list(s), st=({x: "found" for x in range(start[m], i + 1)} if start[m] >= 0 else {i: "active"})), Vars(best=s[best[1]:best[1] + best[0]] if best[0] <= len(s) else "—"))
    w2.step(f"Shortest: '{want}'.", result=want)

    sol(
        "shortest-trail-window",
        summary="""
            For each prefix length `j` of the route, keep `start[j]`: the latest position from which `t[0..j)` can be found
            in order ending at the current position. When `s[i] == t[j−1]`, `start[j]` takes `start[j−1]` (update `j` from
            high to low so it uses the old value). Whenever `start[m]` is set, `s[start[m]..i]` is the shortest window
            ending at `i`. O(n · m).
        """,
        question=[
            """
            Return the shortest substring of `s` that contains `t` as a subsequence (leftmost on ties), or `""`.

            - **s up to 2 × 10⁴**, **t up to 100** letters.
            """
        ],
        think=[
            f"""
            `s = "{s}"`, `t = "{t}"` → **`{want}`**.

            The rule here is order-sensitive, so counts don't help, and windows don't shrink cleanly. But for a fixed end
            `i`, we want the latest possible start, and that can be built up letter by letter: the latest start of a
            window ending at `i` containing `t[0..j)` is the latest start for `t[0..j−1)` ending before `i`, once `s[i]` is
            `t[j−1]`. Keeping that for every `j` is a small table of `m + 1` numbers updated per character.
            """,
            fig(Row(list(s), label="s"), Row(list(t), label="t")),
        ],
        approaches=[
            approach(
                "Greedy match from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each `i` with `s[i] == t[0]`, match `t` greedily to the right; if it completes at `k`, the window `s[i..k]` is the shortest from `i`. Keep the shortest (first on ties)."],
                walk=w1,
                build=["Starts at `t[0]`.", "Greedy subsequence match.", "Keep the shortest."],
                code={
                    "python": """
                        class Solution:
                            def trailWindow(self, s: str, t: str) -> str:
                                n, m = len(s), len(t)  #@init
                                best_len, best_start = n + 1, 0  #@init
                                for i in range(n):  #@starts
                                    if s[i] != t[0]:  #@starts
                                        continue  #@starts
                                    j, k = 0, i  #@match
                                    while k < n:  #@match
                                        if s[k] == t[j]:  #@match
                                            j += 1  #@match
                                            if j == m:  #@match
                                                break  #@match
                                        k += 1  #@match
                                    if j == m and k - i + 1 < best_len:  #@best
                                        best_len, best_start = k - i + 1, i  #@best
                                return s[best_start:best_start + best_len] if best_len <= n else ""  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String trailWindow(String s, String t) {
                                int n = s.length(), m = t.length(), bestLen = n + 1, bestStart = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    if (s.charAt(i) != t.charAt(0)) continue;  //@starts
                                    int j = 0, k = i;  //@match
                                    for (; k < n; k++) if (s.charAt(k) == t.charAt(j) && ++j == m) break;  //@match
                                    if (j == m && k - i + 1 < bestLen) { bestLen = k - i + 1; bestStart = i; }  //@best
                                }
                                return bestLen <= n ? s.substring(bestStart, bestStart + bestLen) : "";  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string trailWindow(string& s, string& t) {
                                int n = s.size(), m = t.size(), bestLen = n + 1, bestStart = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    if (s[i] != t[0]) continue;  //@starts
                                    int j = 0, k = i;  //@match
                                    for (; k < n; k++) if (s[k] == t[j] && ++j == m) break;  //@match
                                    if (j == m && k - i + 1 < bestLen) { bestLen = k - i + 1; bestStart = i; }  //@best
                                }
                                return bestLen <= n ? s.substr(bestStart, bestLen) : "";  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* trailWindow(char* s, char* t) {
                            int n = strlen(s), m = strlen(t), bestLen = n + 1, bestStart = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                if (s[i] != t[0]) continue;  //@starts
                                int j = 0, k = i;  //@match
                                for (; k < n; k++) if (s[k] == t[j] && ++j == m) break;  //@match
                                if (j == m && k - i + 1 < bestLen) { bestLen = k - i + 1; bestStart = i; }  //@best
                            }
                            if (bestLen > n) bestLen = 0;  //@ret
                            char* out = malloc(bestLen + 1);  //@ret
                            memcpy(out, s + bestStart, bestLen);  //@ret
                            out[bestLen] = '\\0';  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "`n + 1` means nothing found."),
                    ("starts", "A shortest window starts with `t[0]`."),
                    ("match", "Greedy matching finishes `t` as early as possible, which gives the shortest window from this start."),
                    ("best", "Strictly shorter only, so the leftmost wins ties."),
                    ("ret", "The window, or empty."),
                ],
                complexity=["**Time O(n²)** in the worst case (4 × 10⁸ at the limit). **Space O(1).**"],
                limits=["Every start re-scans the rest of `s`. The latest-start table shares that work across all starts."],
                slow=True,
            ),
            approach(
                "Latest start for each route prefix",
                "best",
                "O(n · m)",
                "O(m)",
                idea=["`start[0..m]`, all −1. For each `i`, for `j = m..1`: if `s[i] == t[j−1]`, `start[j] = i` when `j == 1`, else `start[j−1]`. If `start[m] ≥ 0`, the window `start[m]..i` is a candidate."],
                walk=w2,
                build=["Table of latest starts.", "Update from high `j` to low.", "Candidate whenever the whole route is matched."],
                code={
                    "python": """
                        class Solution:
                            def trailWindow(self, s: str, t: str) -> str:
                                m = len(t)  #@init
                                start = [-1] * (m + 1)  #@init
                                spots = {}  #@init
                                for j in range(m, 0, -1):  #@init
                                    spots.setdefault(t[j - 1], []).append(j)  #@init
                                best_len, best_start = len(s) + 1, 0  #@init
                                for i, c in enumerate(s):  #@scan
                                    for j in spots.get(c, ()):  #@update
                                        start[j] = i if j == 1 else start[j - 1]  #@update
                                    if start[m] >= 0 and i - start[m] + 1 < best_len:  #@best
                                        best_len, best_start = i - start[m] + 1, start[m]  #@best
                                return s[best_start:best_start + best_len] if best_len <= len(s) else ""  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String trailWindow(String s, String t) {
                                int n = s.length(), m = t.length(), bestLen = n + 1, bestStart = 0;  //@init
                                int[] start = new int[m + 1];  //@init
                                Arrays.fill(start, -1);  //@init
                                for (int i = 0; i < n; i++) {  //@scan
                                    char c = s.charAt(i);  //@scan
                                    for (int j = m; j >= 1; j--)  //@update
                                        if (t.charAt(j - 1) == c) start[j] = j == 1 ? i : start[j - 1];  //@update
                                    if (start[m] >= 0 && i - start[m] + 1 < bestLen) { bestLen = i - start[m] + 1; bestStart = start[m]; }  //@best
                                }
                                return bestLen <= n ? s.substring(bestStart, bestStart + bestLen) : "";  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string trailWindow(string& s, string& t) {
                                int n = s.size(), m = t.size(), bestLen = n + 1, bestStart = 0;  //@init
                                vector<int> start(m + 1, -1);  //@init
                                for (int i = 0; i < n; i++) {  //@scan
                                    for (int j = m; j >= 1; j--)  //@update
                                        if (t[j - 1] == s[i]) start[j] = j == 1 ? i : start[j - 1];  //@update
                                    if (start[m] >= 0 && i - start[m] + 1 < bestLen) { bestLen = i - start[m] + 1; bestStart = start[m]; }  //@best
                                }
                                return bestLen <= n ? s.substr(bestStart, bestLen) : "";  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* trailWindow(char* s, char* t) {
                            int n = strlen(s), m = strlen(t), bestLen = n + 1, bestStart = 0;  //@init
                            int* start = malloc((m + 1) * sizeof(int));  //@init
                            for (int j = 0; j <= m; j++) start[j] = -1;  //@init
                            for (int i = 0; i < n; i++) {  //@scan
                                for (int j = m; j >= 1; j--)  //@update
                                    if (t[j - 1] == s[i]) start[j] = j == 1 ? i : start[j - 1];  //@update
                                if (start[m] >= 0 && i - start[m] + 1 < bestLen) { bestLen = i - start[m] + 1; bestStart = start[m]; }  //@best
                            }
                            free(start);  //@ret
                            if (bestLen > n) bestLen = 0;  //@ret
                            char* out = malloc(bestLen + 1);  //@ret
                            memcpy(out, s + bestStart, bestLen);  //@ret
                            out[bestLen] = '\\0';  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "`start[j] = −1` until `t[0..j)` has been seen in order.", {"python": "`spots[c]` lists the positions `j` with `t[j−1] == c`, high to low, so each character only touches the entries it can change."}),
                    ("scan", "Each position of `s` as the window's right end."),
                    ("update", "If `s[i]` is `t[j−1]`, the route prefix of length `j` can end here, starting where the prefix of length `j − 1` started. Going from high `j` to low ensures `start[j−1]` still describes positions before `i` (important when `t` repeats a letter)."),
                    ("best", "`start[m]` is the latest start of a full route ending at `i`: the shortest window ending here. Strictly shorter only, so the leftmost wins ties."),
                    ("ret", "The window, or empty."),
                ],
                complexity=["**Time O(n · m)** (2 × 10⁶). **Space O(m).**"],
            ),
        ],
        takeaways=[
            """
            - **Order matters → track progress through the pattern**, not counts.
            - "Latest start" per prefix turns many overlapping searches into one pass.
            - Update dependent entries in reverse order so each uses the previous step's values.
            """
        ],
    )


def cover_ref(s, t):
    need = {}
    for c in t:
        need[c] = need.get(c, 0) + 1
    missing, left, best = len(t), 0, (len(s) + 1, 0)
    for i, c in enumerate(s):
        if need.get(c, 0) > 0:
            missing -= 1
        need[c] = need.get(c, 0) - 1
        while missing == 0:
            if i - left + 1 < best[0]:
                best = (i - left + 1, left)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return s[best[1]:best[1] + best[0]] if best[0] <= len(s) else ""


@problem
def smallest_covering_window():
    s, t = "XBAYCBAXCA", "ABC"
    n = len(s)
    want = cover_ref(s, t)

    def covers(l, r):
        w = s[l:r + 1]
        return all(w.count(c) >= t.count(c) for c in set(t))

    w1 = Steps("From each start, extend until the window holds every character of t (with repeats).")
    first_valid_walk(w1, list(s), n, covers)
    w1.step(f"Shortest: '{want}'.", result=want)

    w2 = Steps("need[c] = how many more c the window still needs (negative = extra). missing = total still needed. Grow; when missing hits 0, record and shrink until a needed character leaves.")
    shrink_walk(w2, list(s), n, covers, lambda l, r: {"missing": sum(max(0, t.count(c) - s[l:r + 1].count(c)) for c in set(t))})
    w2.step(f"Shortest: '{want}'.", result=want)

    sol(
        "smallest-covering-window",
        summary="""
            Keep `need[c]` = copies of `c` the window still lacks (negative when it has extras) and `missing` = the total
            still lacking. Grow the window; a character reduces `missing` only if it was still needed. When `missing` hits
            0, record the window and shrink from the left; removing a character whose `need` turns positive makes the
            window incomplete. O(n + m).
        """,
        question=[
            """
            Return the shortest substring of `s` containing every character of `t` with multiplicity (leftmost on ties), or
            `""`. Case-sensitive.

            - **Both up to 10⁵ letters.**
            """
        ],
        think=[
            f"""
            `s = "{s}"`, `t = "{t}"` → **`{want}`**.

            Containing `t`'s characters is preserved by growing the window, so it's a shortest-valid-window problem. The
            only question is checking validity in O(1): instead of comparing whole count tables, keep one number,
            `missing`, that changes only when a character crosses its required count.
            """,
            fig(Row(list(s), label="s"), Row(list(t), label="t")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(σ)",
                idea=["For each start, copy the requirement counts and extend until nothing is missing; record the shortest."],
                walk=w1,
                build=["Requirement counts.", "Extend from each start.", "Keep the shortest."],
                code={
                    "python": """
                        class Solution:
                            def coverWindow(self, s: str, t: str) -> str:
                                n = len(s)  #@init
                                base = {}  #@init
                                for c in t:  #@init
                                    base[c] = base.get(c, 0) + 1  #@init
                                best_len, best_start = n + 1, 0  #@init
                                for i in range(n):  #@starts
                                    need, missing = dict(base), len(t)  #@extend
                                    for j in range(i, min(n, i + best_len - 1)):  #@extend
                                        if need.get(s[j], 0) > 0:  #@extend
                                            missing -= 1  #@extend
                                        need[s[j]] = need.get(s[j], 0) - 1  #@extend
                                        if missing == 0:  #@extend
                                            best_len, best_start = j - i + 1, i  #@extend
                                            break  #@extend
                                return s[best_start:best_start + best_len] if best_len <= n else ""  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String coverWindow(String s, String t) {
                                int n = s.length(), bestLen = n + 1, bestStart = 0;  //@init
                                int[] base = new int[128];  //@init
                                for (char c : t.toCharArray()) base[c]++;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int[] need = base.clone();  //@extend
                                    int missing = t.length();  //@extend
                                    for (int j = i; j < n && j - i + 1 < bestLen; j++) {  //@extend
                                        if (need[s.charAt(j)]-- > 0) missing--;  //@extend
                                        if (missing == 0) { bestLen = j - i + 1; bestStart = i; break; }  //@extend
                                    }
                                }
                                return bestLen <= n ? s.substring(bestStart, bestStart + bestLen) : "";  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string coverWindow(string& s, string& t) {
                                int n = s.size(), bestLen = n + 1, bestStart = 0;  //@init
                                array<int, 128> base{};  //@init
                                for (char c : t) base[c]++;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    array<int, 128> need = base;  //@extend
                                    int missing = t.size();  //@extend
                                    for (int j = i; j < n && j - i + 1 < bestLen; j++) {  //@extend
                                        if (need[s[j]]-- > 0) missing--;  //@extend
                                        if (missing == 0) { bestLen = j - i + 1; bestStart = i; break; }  //@extend
                                    }
                                }
                                return bestLen <= n ? s.substr(bestStart, bestLen) : "";  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* coverWindow(char* s, char* t) {
                            int n = strlen(s), m = strlen(t), bestLen = n + 1, bestStart = 0, base[128] = {0};  //@init
                            for (int i = 0; i < m; i++) base[(int) t[i]]++;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                int need[128], missing = m;  //@extend
                                memcpy(need, base, sizeof(need));  //@extend
                                for (int j = i; j < n && j - i + 1 < bestLen; j++) {  //@extend
                                    if (need[(int) s[j]]-- > 0) missing--;  //@extend
                                    if (missing == 0) { bestLen = j - i + 1; bestStart = i; break; }  //@extend
                                }
                            }
                            if (bestLen > n) bestLen = 0;  //@ret
                            char* out = malloc(bestLen + 1);  //@ret
                            memcpy(out, s + bestStart, bestLen);  //@ret
                            out[bestLen] = '\\0';  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "How many of each character `t` requires."),
                    ("starts", "Each start."),
                    ("extend", "Extend while shorter than the best; a character counts toward `missing` only while it's still needed."),
                    ("ret", "The window, or empty."),
                ],
                complexity=["**Time O(n²)** in the worst case. **Space O(σ).**"],
                limits=["Every start rebuilds its counts. The window keeps one set of counts and moves both edges forward."],
                slow=True,
            ),
            approach(
                "Shrinking window with a missing counter",
                "best",
                "O(n + m)",
                "O(σ)",
                idea=["`need` from `t`, `missing = len(t)`. For each `r`: if `need[s[r]] > 0`, `missing −= 1`; `need[s[r]] −= 1`. While `missing == 0`: record, then `need[s[left]] += 1`; if it becomes positive, `missing += 1`; `left += 1`."],
                walk=w2,
                build=["Requirement counts and `missing`.", "Grow, counting useful characters.", "Record and shrink while complete."],
                code={
                    "python": """
                        class Solution:
                            def coverWindow(self, s: str, t: str) -> str:
                                need = {}  #@init
                                for c in t:  #@init
                                    need[c] = need.get(c, 0) + 1  #@init
                                missing, left = len(t), 0  #@init
                                best_len, best_start = len(s) + 1, 0  #@init
                                for i, c in enumerate(s):  #@grow
                                    if need.get(c, 0) > 0:  #@grow
                                        missing -= 1  #@grow
                                    need[c] = need.get(c, 0) - 1  #@grow
                                    while missing == 0:  #@shrink
                                        if i - left + 1 < best_len:  #@shrink
                                            best_len, best_start = i - left + 1, left  #@shrink
                                        need[s[left]] += 1  #@shrink
                                        if need[s[left]] > 0:  #@shrink
                                            missing += 1  #@shrink
                                        left += 1  #@shrink
                                return s[best_start:best_start + best_len] if best_len <= len(s) else ""  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String coverWindow(String s, String t) {
                                int[] need = new int[128];  //@init
                                for (char c : t.toCharArray()) need[c]++;  //@init
                                int n = s.length(), missing = t.length(), left = 0, bestLen = n + 1, bestStart = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@grow
                                    if (need[s.charAt(i)]-- > 0) missing--;  //@grow
                                    while (missing == 0) {  //@shrink
                                        if (i - left + 1 < bestLen) { bestLen = i - left + 1; bestStart = left; }  //@shrink
                                        if (++need[s.charAt(left++)] > 0) missing++;  //@shrink
                                    }
                                }
                                return bestLen <= n ? s.substring(bestStart, bestStart + bestLen) : "";  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string coverWindow(string& s, string& t) {
                                array<int, 128> need{};  //@init
                                for (char c : t) need[c]++;  //@init
                                int n = s.size(), missing = t.size(), left = 0, bestLen = n + 1, bestStart = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@grow
                                    if (need[s[i]]-- > 0) missing--;  //@grow
                                    while (missing == 0) {  //@shrink
                                        if (i - left + 1 < bestLen) { bestLen = i - left + 1; bestStart = left; }  //@shrink
                                        if (++need[s[left++]] > 0) missing++;  //@shrink
                                    }
                                }
                                return bestLen <= n ? s.substr(bestStart, bestLen) : "";  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* coverWindow(char* s, char* t) {
                            int need[128] = {0}, n = strlen(s), m = strlen(t);  //@init
                            for (int i = 0; i < m; i++) need[(int) t[i]]++;  //@init
                            int missing = m, left = 0, bestLen = n + 1, bestStart = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@grow
                                if (need[(int) s[i]]-- > 0) missing--;  //@grow
                                while (missing == 0) {  //@shrink
                                    if (i - left + 1 < bestLen) { bestLen = i - left + 1; bestStart = left; }  //@shrink
                                    if (++need[(int) s[left++]] > 0) missing++;  //@shrink
                                }
                            }
                            if (bestLen > n) bestLen = 0;  //@ret
                            char* out = malloc(bestLen + 1);  //@ret
                            memcpy(out, s + bestStart, bestLen);  //@ret
                            out[bestLen] = '\\0';  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Requirements from `t`; `missing` counts required copies not yet in the window."),
                    ("grow", "A character that was still needed lowers `missing`; extras just push `need` below zero."),
                    ("shrink", "Complete: record (strictly shorter, so leftmost on ties), then drop the leftmost character. If that makes its `need` positive, the window lacks it again."),
                    ("ret", "The window, or empty."),
                ],
                complexity=["**Time O(n + m).** **Space O(σ)** (128 counters)."],
            ),
        ],
        takeaways=[
            """
            - **Minimum window substring:** shrinking window + a single `missing` counter.
            - `need` can go negative: extras don't change `missing`.
            - Record inside the shrink loop; use strict `<` for leftmost ties.
            """
        ],
    )
