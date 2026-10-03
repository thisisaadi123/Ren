"""Sliding Window: the longest window that satisfies a rule (grow right, shrink left when it breaks)."""
import bisect
from collections import deque

from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def _fmt(d):
    return ", ".join(f"{k} {v}" for k, v in d.items())


SHOW = 6


def extend_walk(w, shown, n, ok, every=1):
    """Brute force: from each start, extend while valid. Shows the first starts, then summarises the rest."""
    best, best_l, work = 0, 0, 0
    for l in range(0, n, every):
        r = l
        while r < n and ok(l, r):
            r += 1
        work += r - l + 1
        if r - l > best:
            best, best_l = r - l, l
        if l < SHOW:
            stop = f" Adding {shown[r]} at {r} would break the rule, so this start stops." if r < n else " It reaches the end."
            w.step(f"Start {l}: the window grows to {l}..{r - 1} (length {r - l}).{stop}", Row(shown, st={**{x: "active" for x in range(l, r)}, **({r: "mark"} if r < n else {})}, ptr={"L": l, "R": r - 1}), Vars(best=best))
    if n > SHOW:
        w.step(f"Starts {SHOW}..{n - 1} are checked the same way. The longest window starts at {best_l}. In total about {work} cells were re-read, which grows like n²: the same cells are scanned again from every start.", Row(shown, st={x: "found" for x in range(best_l, best_l + best)}, ptr={"L": best_l, "R": best_l + best - 1}), Vars(best=best))
    return best


def grow_shrink_walk(w, shown, n, ok, info=None):
    """Two pointers: R adds a cell; if that breaks the rule, L moves right until it holds again."""
    l = best = 0
    for r in range(n):
        broken = not ok(l, r)
        before = _fmt(info(l, r)) if (broken and info) else ""
        start = l
        while not ok(l, r):
            l += 1
        new_best = r - l + 1 > best
        best = max(best, r - l + 1)
        if broken:
            why = f" That breaks the rule ({before})." if before else " That breaks the rule."
            text = f"R adds {shown[r]} at {r}.{why} L moves past {start}..{l - 1} until it holds again: window {l}..{r}."
        else:
            text = f"R adds {shown[r]} at {r}; the rule still holds, so the window just grows to {l}..{r}."
        text += f" New best: {best}." if new_best else ""
        st = {x: ("found" if new_best else "active") for x in range(l, r + 1)}
        st.update({x: "dim" for x in range(start, l)})
        w.step(text, Row(shown, st=st, ptr={"L": l, "R": r}), Vars(best=best, **(info(l, r) if info else {})))
    w.step(f"R visited each index once and L only ever moved right, so the pointers made at most {2 * n} moves in total: O(n).")
    return best


@problem
def longest_fresh_run():
    s = "abcabdcbb"
    n = len(s)
    fresh = lambda l, r: len(set(s[l:r + 1])) == r - l + 1
    want = max(r - l + 1 for l in range(n) for r in range(l, n) if fresh(l, r))

    w1 = Steps("From each start, extend until a character repeats.")
    extend_walk(w1, list(s), n, fresh)
    w1.step(f"Longest: {want}.", result=want)

    w2 = Steps("Grow the window to the right. When the new character already sits inside the window, jump the left edge just past its previous position.")
    last, l, best = {}, 0, 0
    for r, c in enumerate(s):
        jumped = last.get(c, -1) >= l
        if jumped:
            l = last[c] + 1
        last[c] = r
        best = max(best, r - l + 1)
        w2.step(f"'{c}' at {r}" + (f" was last seen inside the window, so left jumps to {l}" if jumped else "") + f". Window '{s[l:r + 1]}'.", Row(list(s), st={x: "active" for x in range(l, r + 1)}), Vars(left=l, best=best))
    w2.step(f"Longest fresh run: {best}.", result=best)

    sol(
        "longest-fresh-run",
        summary="""
            Sliding window with the last index of each character. Move the right edge one step at a time; if the new
            character was last seen inside the window, the window can't contain both copies, so jump the left edge to just
            after that last position. The window is always fresh; track its largest length. O(n).
        """,
        question=[
            """
            Return the length of the longest substring of `s` with no repeated character.

            - **n up to 10⁵**, letters and digits (36 possible characters).
            """
        ],
        think=[
            f"""
            `"{s}"` → **{want}** (`cabd`).

            If a window is fresh, every smaller window inside it is too, so for each right end there's a leftmost valid
            start, and that start only moves right as the right end grows. When a repeat appears, everything up to and
            including the earlier copy must leave, and remembering each character's last index tells us exactly where
            that is.
            """,
            fig(Row(list(s), label="s")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n · σ)",
                "O(σ)",
                idea=["For each start, add characters to a seen set until one repeats. A fresh run has at most σ = 36 characters, so each start stops quickly."],
                walk=w1,
                build=["Loop over starts.", "Extend with a seen set.", "Keep the longest."],
                code={
                    "python": """
                        class Solution:
                            def longestFresh(self, s: str) -> int:
                                best = 0  #@init
                                for i in range(len(s)):  #@starts
                                    seen = set()  #@extend
                                    j = i  #@extend
                                    while j < len(s) and s[j] not in seen:  #@extend
                                        seen.add(s[j])  #@extend
                                        j += 1  #@extend
                                    best = max(best, j - i)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestFresh(String s) {
                                int n = s.length(), best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    boolean[] seen = new boolean[128];  //@extend
                                    int j = i;  //@extend
                                    while (j < n && !seen[s.charAt(j)]) seen[s.charAt(j++)] = true;  //@extend
                                    best = Math.max(best, j - i);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestFresh(string& s) {
                                int n = s.size(), best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    bool seen[128] = {false};  //@extend
                                    int j = i;  //@extend
                                    while (j < n && !seen[(int) s[j]]) seen[(int) s[j++]] = true;  //@extend
                                    best = max(best, j - i);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestFresh(char* s) {
                            int n = strlen(s), best = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                bool seen[128] = {false};  //@extend
                                int j = i;  //@extend
                                while (j < n && !seen[(int) s[j]]) seen[(int) s[j++]] = true;  //@extend
                                if (j - i > best) best = j - i;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Longest so far."), ("starts", "Each possible start."), ("extend", "Grow until the next character was already used."), ("best", "This start's longest fresh run."), ("ret", "Longest overall.")],
                complexity=["**Time O(n · σ)** with σ = 36 distinct characters (O(n²) for a large alphabet). **Space O(σ).**"],
                limits=["Each new start re-reads characters the previous start already checked, and the cost grows with the alphabet size."],
            ),
            approach(
                "Sliding window with last positions",
                "best",
                "O(n)",
                "O(σ)",
                idea=["`last[c]` = most recent index of `c`. For each `r`: if `last[s[r]] ≥ left`, set `left = last[s[r]] + 1`. Update `last`, then `best = max(best, r − left + 1)`."],
                walk=w2,
                build=["Last-seen table.", "Jump the left edge past a repeat.", "Track the longest window."],
                code={
                    "python": """
                        class Solution:
                            def longestFresh(self, s: str) -> int:
                                last = {}  #@init
                                left = best = 0  #@init
                                for i, c in enumerate(s):  #@grow
                                    if last.get(c, -1) >= left:  #@jump
                                        left = last[c] + 1  #@jump
                                    last[c] = i  #@grow
                                    best = max(best, i - left + 1)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestFresh(String s) {
                                int[] last = new int[128];  //@init
                                Arrays.fill(last, -1);  //@init
                                int left = 0, best = 0;  //@init
                                for (int i = 0; i < s.length(); i++) {  //@grow
                                    char c = s.charAt(i);  //@grow
                                    if (last[c] >= left) left = last[c] + 1;  //@jump
                                    last[c] = i;  //@grow
                                    best = Math.max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestFresh(string& s) {
                                vector<int> last(128, -1);  //@init
                                int left = 0, best = 0;  //@init
                                for (int i = 0; i < (int) s.size(); i++) {  //@grow
                                    int c = s[i];  //@grow
                                    if (last[c] >= left) left = last[c] + 1;  //@jump
                                    last[c] = i;  //@grow
                                    best = max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestFresh(char* s) {
                            int last[128], left = 0, best = 0, n = strlen(s);  //@init
                            for (int c = 0; c < 128; c++) last[c] = -1;  //@init
                            for (int i = 0; i < n; i++) {  //@grow
                                int c = s[i];  //@grow
                                if (last[c] >= left) left = last[c] + 1;  //@jump
                                last[c] = i;  //@grow
                                if (i - left + 1 > best) best = i - left + 1;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "No character seen yet; the window is empty.", {"java": "An array indexed by character code beats a map.", "cpp": "An array indexed by character code beats a map.", "c": "An array indexed by character code."}),
                    ("grow", "Add `s[i]` on the right and record where it was seen."),
                    ("jump", "Its previous copy is inside the window: the window must start after it. A copy left of `left` is already outside and doesn't matter."),
                    ("best", "The window `left..i` is fresh."),
                    ("ret", "Longest fresh window."),
                ],
                complexity=["**Time O(n):** each character is processed once, and `left` jumps directly. **Space O(σ).**"],
            ),
        ],
        takeaways=[
            """
            - **Longest window with a rule that survives shrinking:** grow right, move left only as needed.
            - Store **last positions** to jump the left edge instead of stepping.
            - Ignore stale positions that are already left of the window.
            """
        ],
    )


@problem
def one_colour_banner():
    s, k = "ABAABBBAB", 1
    n = len(s)

    def ok(l, r):
        t = s[l:r + 1]
        return len(t) - max(t.count(c) for c in set(t)) <= k
    want = max(r - l + 1 for l in range(n) for r in range(l, n) if ok(l, r))

    w1 = Steps("From each start, extend while the tiles that differ from the most common colour are at most k.")
    extend_walk(w1, list(s), n, ok)
    w1.step(f"Longest: {want}.", result=want)

    w2 = Steps("Window with colour counts: a window works when its length minus its most common colour's count is at most k. Shrink from the left whenever it doesn't.")
    grow_shrink_walk(w2, list(s), n, ok, lambda l, r: {"repaints": (r - l + 1) - max(s[l:r + 1].count(c) for c in set(s[l:r + 1]))})
    w2.step(f"Longest: {want}.", result=want)

    w3 = Steps("Keep maxf = the highest count ever seen. The window never shrinks: when it's too big for maxf, it slides one step right. It grows only when some colour beats maxf.")
    count, l, maxf, best = {}, 0, 0, 0
    for r, c in enumerate(s):
        count[c] = count.get(c, 0) + 1
        maxf = max(maxf, count[c])
        slid = (r - l + 1) - maxf > k
        if slid:
            count[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
        w3.step(f"Add '{c}': maxf = {maxf}." + (" Too many repaints for that, so slide (left +1)." if slid else " Fits, so the window grows.") + f" Length {r - l + 1}.", Row(list(s), st={x: "active" for x in range(l, r + 1)}), Vars(maxf=maxf, best=best))
    w3.step(f"Longest: {best}.", result=best)

    sol(
        "one-colour-banner",
        summary="""
            A window can be made one colour with `length − (count of its most common colour)` repaints. Slide a window with
            colour counts, shrinking when that exceeds `k`. Refinement: keep `maxf` as the highest count ever seen; the
            answer only improves when `maxf` grows, so the window never needs to shrink, only slide. O(n).
        """,
        question=[
            """
            Repaint at most `k` tiles of `s`. Return the longest run of consecutive tiles that can end up one colour.

            - **n up to 10⁵**, 26 colours.
            """
        ],
        think=[
            f"""
            `"{s}"`, `k = {k}` → **{want}**.

            For a fixed run, the cheapest choice is to keep its most common colour and repaint everything else, so it
            needs `length − maxCount` repaints. Shrinking a valid run keeps it valid, so this is a longest-window problem.

            The subtle refinement: we only care about windows **longer** than the best so far. A longer valid window needs
            a larger `maxCount` than we've ever had. So `maxf` may safely be a historical maximum: while it's stale, the
            window just slides at its current length and can't produce a wrong (too large) answer.
            """,
            fig(Row(list(s), label="s")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start, extend while `length − maxCount ≤ k`, updating counts and `maxCount` incrementally."],
                walk=w1,
                build=["Loop over starts.", "Counts and running max.", "Stop when repaints exceed `k`."],
                code={
                    "python": """
                        class Solution:
                            def longestUniform(self, s: str, k: int) -> int:
                                n, best = len(s), 0  #@init
                                for i in range(n):  #@starts
                                    count, top = [0] * 26, 0  #@extend
                                    for j in range(i, n):  #@extend
                                        x = ord(s[j]) - 65  #@extend
                                        count[x] += 1  #@extend
                                        top = max(top, count[x])  #@extend
                                        if j - i + 1 - top > k:  #@extend
                                            break  #@extend
                                        best = max(best, j - i + 1)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestUniform(String s, int k) {
                                int n = s.length(), best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int[] count = new int[26];  //@extend
                                    int top = 0;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        top = Math.max(top, ++count[s.charAt(j) - 'A']);  //@extend
                                        if (j - i + 1 - top > k) break;  //@extend
                                        best = Math.max(best, j - i + 1);  //@best
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestUniform(string& s, int k) {
                                int n = s.size(), best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int count[26] = {0}, top = 0;  //@extend
                                    for (int j = i; j < n; j++) {  //@extend
                                        top = max(top, ++count[s[j] - 'A']);  //@extend
                                        if (j - i + 1 - top > k) break;  //@extend
                                        best = max(best, j - i + 1);  //@best
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestUniform(char* s, int k) {
                            int n = strlen(s), best = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                int count[26] = {0}, top = 0;  //@extend
                                for (int j = i; j < n; j++) {  //@extend
                                    int c = ++count[s[j] - 'A'];  //@extend
                                    if (c > top) top = c;  //@extend
                                    if (j - i + 1 - top > k) break;  //@extend
                                    if (j - i + 1 > best) best = j - i + 1;  //@best
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Longest so far."), ("starts", "Each start."), ("extend", "Add tiles, keeping counts and the top count; stop when the repaints needed (`length − top`) exceed `k`."), ("best", "A valid run."), ("ret", "Longest run.")],
                complexity=["**Time O(n²)** in the worst case (large `k`). **Space O(1)** (26 counters)."],
                limits=["Each start rebuilds its counts from nothing. One window that grows on the right and shrinks on the left reuses them."],
                slow=True,
            ),
            approach(
                "Sliding window, recount the top colour",
                "better",
                "O(26 · n)",
                "O(1)",
                idea=["Add `s[r]` to the counts. While `length − max(count) > k`, remove `s[left]` and advance. Track the longest window."],
                walk=w2,
                build=["Counts for the window.", "Shrink while too many repaints.", "Track the longest."],
                code={
                    "python": """
                        class Solution:
                            def longestUniform(self, s: str, k: int) -> int:
                                count = [0] * 26  #@init
                                left = best = 0  #@init
                                for i, c in enumerate(s):  #@grow
                                    count[ord(c) - 65] += 1  #@grow
                                    while i - left + 1 - max(count) > k:  #@shrink
                                        count[ord(s[left]) - 65] -= 1  #@shrink
                                        left += 1  #@shrink
                                    best = max(best, i - left + 1)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int top(int[] count) {  //@shrink
                                int t = 0;  //@shrink
                                for (int c : count) t = Math.max(t, c);  //@shrink
                                return t;  //@shrink
                            }  //@shrink

                            public int longestUniform(String s, int k) {
                                int[] count = new int[26];  //@init
                                int left = 0, best = 0;  //@init
                                for (int i = 0; i < s.length(); i++) {  //@grow
                                    count[s.charAt(i) - 'A']++;  //@grow
                                    while (i - left + 1 - top(count) > k) count[s.charAt(left++) - 'A']--;  //@shrink
                                    best = Math.max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestUniform(string& s, int k) {
                                int count[26] = {0}, left = 0, best = 0;  //@init
                                for (int i = 0; i < (int) s.size(); i++) {  //@grow
                                    count[s[i] - 'A']++;  //@grow
                                    while (i - left + 1 - *max_element(count, count + 26) > k) count[s[left++] - 'A']--;  //@shrink
                                    best = max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int top(const int* count) {  //@shrink
                            int t = 0;  //@shrink
                            for (int c = 0; c < 26; c++) if (count[c] > t) t = count[c];  //@shrink
                            return t;  //@shrink
                        }  //@shrink

                        int longestUniform(char* s, int k) {
                            int count[26] = {0}, left = 0, best = 0, n = strlen(s);  //@init
                            for (int i = 0; i < n; i++) {  //@grow
                                count[s[i] - 'A']++;  //@grow
                                while (i - left + 1 - top(count) > k) count[s[left++] - 'A']--;  //@shrink
                                if (i - left + 1 > best) best = i - left + 1;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Colour counts of the window `left..i`."), ("grow", "Add the next tile."), ("shrink", "Too many repaints: drop tiles from the left. The top count is recomputed over 26 colours each check."), ("best", "The window is now valid."), ("ret", "Longest valid window.")],
                complexity=["**Time O(26 · n).** **Space O(1).**"],
                limits=["Recomputes the top count over all 26 colours on every check. It doesn't need to be exact: a historical maximum is enough."],
            ),
            approach(
                "Window that never shrinks (historical max)",
                "best",
                "O(n)",
                "O(1)",
                idea=["Keep `maxf` = largest count seen in any window so far. After adding `s[r]`, if `length − maxf > k`, remove one tile from the left (the window slides at constant length). The final window length (or the max seen) is the answer."],
                walk=w3,
                build=["Counts and `maxf`.", "Grow; slide by one if too long for `maxf`.", "Track the length."],
                code={
                    "python": """
                        class Solution:
                            def longestUniform(self, s: str, k: int) -> int:
                                count = [0] * 26  #@init
                                left = maxf = best = 0  #@init
                                for i, c in enumerate(s):  #@grow
                                    x = ord(c) - 65  #@grow
                                    count[x] += 1  #@grow
                                    maxf = max(maxf, count[x])  #@maxf
                                    if i - left + 1 - maxf > k:  #@slide
                                        count[ord(s[left]) - 65] -= 1  #@slide
                                        left += 1  #@slide
                                    best = max(best, i - left + 1)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestUniform(String s, int k) {
                                int[] count = new int[26];  //@init
                                int left = 0, maxf = 0, best = 0;  //@init
                                for (int i = 0; i < s.length(); i++) {  //@grow
                                    int x = s.charAt(i) - 'A';  //@grow
                                    maxf = Math.max(maxf, ++count[x]);  //@maxf
                                    if (i - left + 1 - maxf > k) count[s.charAt(left++) - 'A']--;  //@slide
                                    best = Math.max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestUniform(string& s, int k) {
                                int count[26] = {0}, left = 0, maxf = 0, best = 0;  //@init
                                for (int i = 0; i < (int) s.size(); i++) {  //@grow
                                    int x = s[i] - 'A';  //@grow
                                    maxf = max(maxf, ++count[x]);  //@maxf
                                    if (i - left + 1 - maxf > k) count[s[left++] - 'A']--;  //@slide
                                    best = max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestUniform(char* s, int k) {
                            int count[26] = {0}, left = 0, maxf = 0, best = 0, n = strlen(s);  //@init
                            for (int i = 0; i < n; i++) {  //@grow
                                int x = s[i] - 'A';  //@grow
                                if (++count[x] > maxf) maxf = count[x];  //@maxf
                                if (i - left + 1 - maxf > k) count[s[left++] - 'A']--;  //@slide
                                if (i - left + 1 > best) best = i - left + 1;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Counts, the left edge, and `maxf`."),
                    ("grow", "Add the next tile."),
                    ("maxf", "Only the colour just added can raise the maximum."),
                    ("slide", "If the window is one too long for `maxf`, drop one tile: the window keeps its length and moves right. `maxf` isn't lowered; a smaller value could never give a longer window anyway."),
                    ("best", "The window length only grows when a colour reaches a new `maxf`."),
                    ("ret", "Longest valid length."),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **"Make a window uniform with ≤ k changes":** cost = length − most frequent count.
            - When you only want the maximum length, the window may **slide instead of shrink**, and a stale maximum is fine.
            - Same template as "longest run of 1s with k flips".
            """
        ],
    )


@problem
def patch_the_outage():
    status, k = [1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1], 2
    n = len(status)
    ok = lambda l, r: status[l:r + 1].count(0) <= k
    want = max(r - l + 1 for l in range(n) for r in range(l, n) if ok(l, r))

    w1 = Steps("From each start, extend while at most k down minutes are inside.")
    extend_walk(w1, status, n, ok)
    w1.step(f"Longest: {want}.", result=want)

    w2 = Steps("Grow the window and count its zeros; when there are more than k, move the left edge until one zero leaves.")
    grow_shrink_walk(w2, status, n, ok, lambda l, r: {"zeros": status[l:r + 1].count(0)})
    w2.step(f"Longest: {want}.", result=want)

    sol(
        "patch-the-outage",
        summary="""
            The longest run of 1s after flipping at most `k` zeros is the longest window containing at most `k` zeros. Grow
            the window right, counting zeros; when the count exceeds `k`, advance the left edge until a zero leaves. O(n).
        """,
        question=[
            """
            Turn at most `k` zeros of `status` into ones. Return the longest run of consecutive ones you can get.

            - **n up to 10⁵.**
            """
        ],
        think=[
            f"""
            `status = {status}`, `k = {k}` → **{want}**.

            Which zeros to patch? Only those inside the run we end up with. So a run is achievable exactly when it holds
            at most `k` zeros: we're looking for the longest window with at most `k` zeros. A sub-window of a valid window
            is valid, so the left edge only ever moves right.
            """,
            fig(Row(status, label="status")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start, extend while the zero count stays at most `k`."],
                walk=w1,
                build=["Loop over starts.", "Count zeros while extending.", "Keep the longest."],
                code={
                    "python": """
                        class Solution:
                            def longestOnline(self, status: List[int], k: int) -> int:
                                n, best = len(status), 0  #@init
                                for i in range(n):  #@starts
                                    zeros, j = 0, i  #@extend
                                    while j < n and zeros + (status[j] == 0) <= k:  #@extend
                                        zeros += status[j] == 0  #@extend
                                        j += 1  #@extend
                                    best = max(best, j - i)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestOnline(int[] status, int k) {
                                int n = status.length, best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int zeros = 0, j = i;  //@extend
                                    while (j < n && zeros + (status[j] == 0 ? 1 : 0) <= k) zeros += status[j++] == 0 ? 1 : 0;  //@extend
                                    best = Math.max(best, j - i);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestOnline(vector<int>& status, int k) {
                                int n = status.size(), best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int zeros = 0, j = i;  //@extend
                                    while (j < n && zeros + (status[j] == 0) <= k) zeros += status[j++] == 0;  //@extend
                                    best = max(best, j - i);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestOnline(int* status, int statusSize, int k) {
                            int n = statusSize, best = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                int zeros = 0, j = i;  //@extend
                                while (j < n && zeros + (status[j] == 0) <= k) zeros += status[j++] == 0;  //@extend
                                if (j - i > best) best = j - i;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Longest so far."), ("starts", "Each start."), ("extend", "Take the next minute if patching it (when down) stays within `k`."), ("best", "This start's longest run."), ("ret", "Longest overall.")],
                complexity=["**Time O(n²)** when `k` is large. **Space O(1).**"],
                limits=["Each start rescans minutes the previous start already counted."],
                slow=True,
            ),
            approach(
                "Window with at most k zeros",
                "best",
                "O(n)",
                "O(1)",
                idea=["Add `status[r]`; if it's 0, `zeros += 1`. While `zeros > k`, drop `status[left]` (decrementing `zeros` if it was 0) and advance. Track the longest window."],
                walk=w2,
                build=["Zero count of the window.", "Shrink when over `k`.", "Track the longest."],
                code={
                    "python": """
                        class Solution:
                            def longestOnline(self, status: List[int], k: int) -> int:
                                left = zeros = best = 0  #@init
                                for i, v in enumerate(status):  #@grow
                                    if v == 0:  #@grow
                                        zeros += 1  #@grow
                                    while zeros > k:  #@shrink
                                        if status[left] == 0:  #@shrink
                                            zeros -= 1  #@shrink
                                        left += 1  #@shrink
                                    best = max(best, i - left + 1)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestOnline(int[] status, int k) {
                                int left = 0, zeros = 0, best = 0;  //@init
                                for (int i = 0; i < status.length; i++) {  //@grow
                                    if (status[i] == 0) zeros++;  //@grow
                                    while (zeros > k) if (status[left++] == 0) zeros--;  //@shrink
                                    best = Math.max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestOnline(vector<int>& status, int k) {
                                int left = 0, zeros = 0, best = 0;  //@init
                                for (int i = 0; i < (int) status.size(); i++) {  //@grow
                                    if (status[i] == 0) zeros++;  //@grow
                                    while (zeros > k) if (status[left++] == 0) zeros--;  //@shrink
                                    best = max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestOnline(int* status, int statusSize, int k) {
                            int left = 0, zeros = 0, best = 0;  //@init
                            for (int i = 0; i < statusSize; i++) {  //@grow
                                if (status[i] == 0) zeros++;  //@grow
                                while (zeros > k) if (status[left++] == 0) zeros--;  //@shrink
                                if (i - left + 1 > best) best = i - left + 1;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Empty window, no zeros."), ("grow", "Add minute `i`; a down minute needs a patch."), ("shrink", "Over budget: drop minutes from the left until a zero leaves."), ("best", "The window has at most `k` zeros, so it can become all ones."), ("ret", "Longest.")],
                complexity=["**Time O(n):** `left` and `i` each move at most `n` times. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **"Flip at most k" = window with at most k bad items.**
            - Both pointers only move forward: O(n) total.
            - Count the bad items; the good ones don't need tracking.
            """
        ],
    )


@problem
def ride_on_a_budget():
    fares, budget = [4, 2, 6, 1, 1, 3, 5, 2, 2], 10
    n = len(fares)
    ok = lambda l, r: sum(fares[l:r + 1]) <= budget
    want = max([r - l + 1 for l in range(n) for r in range(l, n) if ok(l, r)] + [0])
    pre = [0]
    for f in fares:
        pre.append(pre[-1] + f)

    w1 = Steps("From each stop, keep riding while the fares fit the budget.")
    extend_walk(w1, fares, n, ok)
    w1.step(f"Longest: {want}.", result=want)

    w2 = Steps("Prefix sums are increasing (fares are positive), so for each start the furthest affordable end can be binary-searched.")
    for i in range(n):
        j = bisect.bisect_right(pre, pre[i] + budget) - 1
        w2.step(f"Start {i}: the largest prefix ≤ {pre[i]} + {budget} = {pre[i] + budget} is pre[{j}] = {pre[j]}, so {j - i} hop(s).", Row(pre, st={i: "active", j: "found"}, label="prefix"))
    w2.step(f"Longest: {want}.", result=want)

    w3 = Steps("Grow the ride on the right; while it costs more than the budget, drop hops from the left.")
    grow_shrink_walk(w3, fares, n, ok, lambda l, r: {"cost": sum(fares[l:r + 1])})
    w3.step(f"Longest: {want}.", result=want)

    sol(
        "ride-on-a-budget",
        summary="""
            All fares are positive, so a longer ride always costs more and dropping a hop always helps. That makes the
            two-pointer window exact: add the next hop's fare; while the total exceeds the budget, remove hops from the
            left. The longest window seen is the answer. O(n).
        """,
        question=[
            """
            Return the largest number of consecutive hops (contiguous fares) whose total is at most `budget` (0 if no single
            hop is affordable).

            - **n up to 10⁵**, fares positive, budget up to 10⁹.
            """
        ],
        think=[
            f"""
            `fares = {fares}`, `budget = {budget}` → **{want}** hops.

            Positivity is what makes a window work: if a ride fits the budget, every shorter ride inside it fits too, and
            for each end the cheapest way to fix an over-budget ride is to drop hops from the start. Without positive
            fares (e.g. refunds), shrinking wouldn't necessarily lower the cost and this would break.
            """,
            fig(Row(fares, label="fares"), Row(pre, label="prefix sums")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start, add fares while the total stays within the budget."],
                walk=w1,
                build=["Loop over starts.", "Extend while affordable.", "Keep the longest."],
                code={
                    "python": """
                        class Solution:
                            def longestRide(self, fares: List[int], budget: int) -> int:
                                n, best = len(fares), 0  #@init
                                for i in range(n):  #@starts
                                    total, j = 0, i  #@extend
                                    while j < n and total + fares[j] <= budget:  #@extend
                                        total += fares[j]  #@extend
                                        j += 1  #@extend
                                    best = max(best, j - i)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestRide(int[] fares, int budget) {
                                int n = fares.length, best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    long total = 0;  //@extend
                                    int j = i;  //@extend
                                    while (j < n && total + fares[j] <= budget) total += fares[j++];  //@extend
                                    best = Math.max(best, j - i);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestRide(vector<int>& fares, int budget) {
                                int n = fares.size(), best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    long long total = 0;  //@extend
                                    int j = i;  //@extend
                                    while (j < n && total + fares[j] <= budget) total += fares[j++];  //@extend
                                    best = max(best, j - i);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestRide(int* fares, int faresSize, int budget) {
                            int n = faresSize, best = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                long long total = 0;  //@extend
                                int j = i;  //@extend
                                while (j < n && total + fares[j] <= budget) total += fares[j++];  //@extend
                                if (j - i > best) best = j - i;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Longest so far."), ("starts", "Each boarding stop."), ("extend", "Ride while the next fare still fits."), ("best", "Hops from this start."), ("ret", "Longest ride.")],
                complexity=["**Time O(n²)** with a big budget. **Space O(1).**"],
                limits=["Re-adds fares for every start. Prefix sums with binary search, or the two-pointer window, avoid that."],
                slow=True,
            ),
            approach(
                "Prefix sums + binary search",
                "better",
                "O(n log n)",
                "O(n)",
                idea=["`pre[j]` = total of the first `j` fares (strictly increasing). For each start `i`, the furthest end is the largest `j` with `pre[j] ≤ pre[i] + budget`: binary search."],
                walk=w2,
                build=["Prefix sums.", "Upper-bound search per start.", "Keep the longest."],
                code={
                    "python": """
                        from bisect import bisect_right


                        class Solution:
                            def longestRide(self, fares: List[int], budget: int) -> int:
                                pre = [0]  #@prefix
                                for f in fares:  #@prefix
                                    pre.append(pre[-1] + f)  #@prefix
                                best = 0  #@search
                                for i in range(len(fares)):  #@search
                                    j = bisect_right(pre, pre[i] + budget) - 1  #@search
                                    best = max(best, j - i)  #@search
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestRide(int[] fares, int budget) {
                                int n = fares.length, best = 0;  //@prefix
                                long[] pre = new long[n + 1];  //@prefix
                                for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + fares[i];  //@prefix
                                for (int i = 0; i < n; i++) {  //@search
                                    long cap = pre[i] + budget;  //@search
                                    int lo = i, hi = n;  //@search
                                    while (lo < hi) {  //@search
                                        int mid = (lo + hi + 1) / 2;  //@search
                                        if (pre[mid] <= cap) lo = mid; else hi = mid - 1;  //@search
                                    }
                                    best = Math.max(best, lo - i);  //@search
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestRide(vector<int>& fares, int budget) {
                                int n = fares.size(), best = 0;  //@prefix
                                vector<long long> pre(n + 1, 0);  //@prefix
                                for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + fares[i];  //@prefix
                                for (int i = 0; i < n; i++) {  //@search
                                    int j = upper_bound(pre.begin(), pre.end(), pre[i] + budget) - pre.begin() - 1;  //@search
                                    best = max(best, j - i);  //@search
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestRide(int* fares, int faresSize, int budget) {
                            int n = faresSize, best = 0;  //@prefix
                            long long* pre = malloc((n + 1) * sizeof(long long));  //@prefix
                            pre[0] = 0;  //@prefix
                            for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + fares[i];  //@prefix
                            for (int i = 0; i < n; i++) {  //@search
                                long long cap = pre[i] + budget;  //@search
                                int lo = i, hi = n;  //@search
                                while (lo < hi) {  //@search
                                    int mid = (lo + hi + 1) / 2;  //@search
                                    if (pre[mid] <= cap) lo = mid; else hi = mid - 1;  //@search
                                }
                                if (lo - i > best) best = lo - i;  //@search
                            }
                            free(pre);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("prefix", "Running totals; the cost of hops `i..j−1` is `pre[j] − pre[i]`."), ("search", "The last prefix within `pre[i] + budget` marks the furthest affordable end."), ("ret", "Longest ride.")],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["A binary search per start ignores that the best end only moves right as the start moves right."],
            ),
            approach(
                "Two-pointer window",
                "best",
                "O(n)",
                "O(1)",
                idea=["Add `fares[r]` to `total`. While `total > budget`, subtract `fares[left]` and advance. Track `r − left + 1`."],
                walk=w3,
                build=["Running total.", "Shrink while over budget.", "Track the longest."],
                code={
                    "python": """
                        class Solution:
                            def longestRide(self, fares: List[int], budget: int) -> int:
                                left = total = best = 0  #@init
                                for i, f in enumerate(fares):  #@grow
                                    total += f  #@grow
                                    while total > budget:  #@shrink
                                        total -= fares[left]  #@shrink
                                        left += 1  #@shrink
                                    best = max(best, i - left + 1)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestRide(int[] fares, int budget) {
                                int left = 0, best = 0;  //@init
                                long total = 0;  //@init
                                for (int i = 0; i < fares.length; i++) {  //@grow
                                    total += fares[i];  //@grow
                                    while (total > budget) total -= fares[left++];  //@shrink
                                    best = Math.max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestRide(vector<int>& fares, int budget) {
                                int left = 0, best = 0;  //@init
                                long long total = 0;  //@init
                                for (int i = 0; i < (int) fares.size(); i++) {  //@grow
                                    total += fares[i];  //@grow
                                    while (total > budget) total -= fares[left++];  //@shrink
                                    best = max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestRide(int* fares, int faresSize, int budget) {
                            int left = 0, best = 0;  //@init
                            long long total = 0;  //@init
                            for (int i = 0; i < faresSize; i++) {  //@grow
                                total += fares[i];  //@grow
                                while (total > budget) total -= fares[left++];  //@shrink
                                if (i - left + 1 > best) best = i - left + 1;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Empty ride."),
                    ("grow", "Take hop `i`."),
                    ("shrink", "Over budget: give up hops from the start. If even hop `i` alone is too expensive, the window becomes empty (`left = i + 1`)."),
                    ("best", "An affordable ride of `i − left + 1` hops (0 when empty)."),
                    ("ret", "Longest ride."),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Positive values + "sum ≤ budget"** → shrinkable window, O(n).
            - Prefix sums + binary search is the fallback that also needs only monotone prefixes.
            - With negative values, neither works; use prefix sums with a monotonic structure instead.
            """
        ],
    )


@problem
def steady_readings():
    readings, limit = [8, 2, 4, 7, 5, 6, 9, 3, 4], 3
    n = len(readings)
    ok = lambda l, r: max(readings[l:r + 1]) - min(readings[l:r + 1]) <= limit
    want = max(r - l + 1 for l in range(n) for r in range(l, n) if ok(l, r))

    w1 = Steps("From each start, extend while the running max − min stays within the limit.")
    extend_walk(w1, readings, n, ok)
    w1.step(f"Longest: {want}.", result=want)

    w2 = Steps("Two monotonic deques: hi keeps indices with decreasing readings (front = window max), lo keeps increasing readings (front = window min). Shrink while max − min > limit.")
    hi, lo = deque(), deque()
    left = best = 0
    for i, v in enumerate(readings):
        while hi and readings[hi[-1]] <= v:
            hi.pop()
        hi.append(i)
        while lo and readings[lo[-1]] >= v:
            lo.pop()
        lo.append(i)
        moved = 0
        while readings[hi[0]] - readings[lo[0]] > limit:
            left += 1
            moved += 1
            if hi[0] < left:
                hi.popleft()
            if lo[0] < left:
                lo.popleft()
        best = max(best, i - left + 1)
        w2.step(f"Add {v}." + (f" Max − min was over {limit}: left moves {moved}." if moved else "") + f" Window {readings[left:i + 1]}: max {readings[hi[0]]}, min {readings[lo[0]]}.", Row(readings, st={x: "active" for x in range(left, i + 1)}), Vars(hi=[readings[x] for x in hi], lo=[readings[x] for x in lo], best=best))
    w2.step(f"Longest steady run: {best}.", result=best)

    sol(
        "steady-readings",
        summary="""
            Longest window whose max − min ≤ limit. The window shrinks correctly from the left (a sub-window's spread is
            no larger), but we need its max and min as it slides. Two monotonic deques give both in amortised O(1): one
            keeps candidates for the maximum in decreasing order, the other for the minimum in increasing order. O(n).
        """,
        question=[
            """
            Return the length of the longest run of consecutive `readings` whose highest and lowest values differ by at most
            `limit`.

            - **n up to 10⁵.**
            """
        ],
        think=[
            f"""
            `readings = {readings}`, `limit = {limit}` → **{want}**.

            It's a longest-window problem (shrinking never increases the spread). The hard part is the window's max and
            min after removing from the left. A reading that is smaller than a later reading can never be the window's
            maximum again while that later one is inside, so it can be discarded. What remains is a decreasing list whose
            front is the max. The same, mirrored, for the min.
            """,
            fig(Row(readings, label="readings")),
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start, extend while tracking the running max and min; stop when they differ by more than `limit`."],
                walk=w1,
                build=["Loop over starts.", "Running max/min.", "Keep the longest."],
                code={
                    "python": """
                        class Solution:
                            def longestSteady(self, readings: List[int], limit: int) -> int:
                                n, best = len(readings), 0  #@init
                                for i in range(n):  #@starts
                                    hi = lo = readings[i]  #@extend
                                    j = i  #@extend
                                    while j < n and max(hi, readings[j]) - min(lo, readings[j]) <= limit:  #@extend
                                        hi, lo = max(hi, readings[j]), min(lo, readings[j])  #@extend
                                        j += 1  #@extend
                                    best = max(best, j - i)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestSteady(int[] readings, int limit) {
                                int n = readings.length, best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int hi = readings[i], lo = readings[i], j = i;  //@extend
                                    while (j < n && (long) Math.max(hi, readings[j]) - Math.min(lo, readings[j]) <= limit) {  //@extend
                                        hi = Math.max(hi, readings[j]);  //@extend
                                        lo = Math.min(lo, readings[j++]);  //@extend
                                    }
                                    best = Math.max(best, j - i);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestSteady(vector<int>& readings, int limit) {
                                int n = readings.size(), best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int hi = readings[i], lo = readings[i], j = i;  //@extend
                                    while (j < n && (long long) max(hi, readings[j]) - min(lo, readings[j]) <= limit) {  //@extend
                                        hi = max(hi, readings[j]);  //@extend
                                        lo = min(lo, readings[j++]);  //@extend
                                    }
                                    best = max(best, j - i);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestSteady(int* readings, int readingsSize, int limit) {
                            int n = readingsSize, best = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                int hi = readings[i], lo = readings[i], j = i;  //@extend
                                while (j < n) {  //@extend
                                    int h = readings[j] > hi ? readings[j] : hi, l = readings[j] < lo ? readings[j] : lo;  //@extend
                                    if ((long long) h - l > limit) break;  //@extend
                                    hi = h; lo = l; j++;  //@extend
                                }
                                if (j - i > best) best = j - i;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Longest so far."), ("starts", "Each start."), ("extend", "Include the next reading if the spread stays within `limit`."), ("best", "This start's longest steady run."), ("ret", "Longest overall.")],
                complexity=["**Time O(n²)** with a generous limit. **Space O(1).**"],
                limits=["Restarts for every left edge. A sliding window needs the max and min after removals, which monotonic deques provide."],
                slow=True,
            ),
            approach(
                "Sliding window with max and min deques",
                "best",
                "O(n)",
                "O(n)",
                idea=["`hi`: indices with decreasing readings; `lo`: increasing. On adding `i`, pop smaller (resp. larger) readings from the back, then push `i`. While `readings[hi[0]] − readings[lo[0]] > limit`, advance `left` and drop deque fronts that fall out of the window."],
                walk=w2,
                build=["Two deques.", "Push with back-pops.", "Shrink while the spread is too big.", "Track the longest."],
                code={
                    "python": """
                        from collections import deque


                        class Solution:
                            def longestSteady(self, readings: List[int], limit: int) -> int:
                                hi, lo = deque(), deque()  #@init
                                left = best = 0  #@init
                                for i, v in enumerate(readings):  #@push
                                    while hi and readings[hi[-1]] <= v:  #@push
                                        hi.pop()  #@push
                                    hi.append(i)  #@push
                                    while lo and readings[lo[-1]] >= v:  #@push
                                        lo.pop()  #@push
                                    lo.append(i)  #@push
                                    while readings[hi[0]] - readings[lo[0]] > limit:  #@shrink
                                        left += 1  #@shrink
                                        if hi[0] < left:  #@shrink
                                            hi.popleft()  #@shrink
                                        if lo[0] < left:  #@shrink
                                            lo.popleft()  #@shrink
                                    best = max(best, i - left + 1)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestSteady(int[] readings, int limit) {
                                Deque<Integer> hi = new ArrayDeque<>(), lo = new ArrayDeque<>();  //@init
                                int left = 0, best = 0;  //@init
                                for (int i = 0; i < readings.length; i++) {  //@push
                                    int v = readings[i];  //@push
                                    while (!hi.isEmpty() && readings[hi.peekLast()] <= v) hi.pollLast();  //@push
                                    hi.addLast(i);  //@push
                                    while (!lo.isEmpty() && readings[lo.peekLast()] >= v) lo.pollLast();  //@push
                                    lo.addLast(i);  //@push
                                    while (readings[hi.peekFirst()] - readings[lo.peekFirst()] > limit) {  //@shrink
                                        left++;  //@shrink
                                        if (hi.peekFirst() < left) hi.pollFirst();  //@shrink
                                        if (lo.peekFirst() < left) lo.pollFirst();  //@shrink
                                    }
                                    best = Math.max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestSteady(vector<int>& readings, int limit) {
                                deque<int> hi, lo;  //@init
                                int left = 0, best = 0;  //@init
                                for (int i = 0; i < (int) readings.size(); i++) {  //@push
                                    int v = readings[i];  //@push
                                    while (!hi.empty() && readings[hi.back()] <= v) hi.pop_back();  //@push
                                    hi.push_back(i);  //@push
                                    while (!lo.empty() && readings[lo.back()] >= v) lo.pop_back();  //@push
                                    lo.push_back(i);  //@push
                                    while (readings[hi.front()] - readings[lo.front()] > limit) {  //@shrink
                                        left++;  //@shrink
                                        if (hi.front() < left) hi.pop_front();  //@shrink
                                        if (lo.front() < left) lo.pop_front();  //@shrink
                                    }
                                    best = max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestSteady(int* readings, int readingsSize, int limit) {
                            int* hi = malloc(readingsSize * sizeof(int));  //@init
                            int* lo = malloc(readingsSize * sizeof(int));  //@init
                            int hh = 0, ht = 0, lh = 0, lt = 0, left = 0, best = 0;  //@init
                            for (int i = 0; i < readingsSize; i++) {  //@push
                                int v = readings[i];  //@push
                                while (ht > hh && readings[hi[ht - 1]] <= v) ht--;  //@push
                                hi[ht++] = i;  //@push
                                while (lt > lh && readings[lo[lt - 1]] >= v) lt--;  //@push
                                lo[lt++] = i;  //@push
                                while (readings[hi[hh]] - readings[lo[lh]] > limit) {  //@shrink
                                    left++;  //@shrink
                                    if (hi[hh] < left) hh++;  //@shrink
                                    if (lo[lh] < left) lh++;  //@shrink
                                }
                                if (i - left + 1 > best) best = i - left + 1;  //@best
                            }
                            free(hi); free(lo);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Two deques of indices and the window's left edge.", {"c": "Each deque is an array with a head and a tail index; nothing is pushed more than once, so `n` slots suffice."}),
                    ("push", "Readings that can no longer be the max (smaller than `v`) leave `hi`; those that can't be the min leave `lo`. Then `i` joins both."),
                    ("shrink", "The fronts are the window's max and min. While they're too far apart, move `left`, and drop a front once it's outside the window."),
                    ("best", "The window `left..i` is steady."),
                    ("ret", "Longest steady run."),
                ],
                complexity=["**Time O(n):** every index enters and leaves each deque at most once. **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - **Window max/min under removals → monotonic deques**, amortised O(1).
            - Max − min is monotone under shrinking, so the longest-window template applies.
            - Store indices in the deques so you can tell when a front has left the window.
            """
        ],
    )


@problem
def two_flavour_basket():
    flavours = [3, 3, 1, 2, 1, 1, 2, 4, 4, 2]
    n = len(flavours)
    ok = lambda l, r: len(set(flavours[l:r + 1])) <= 2
    want = max(r - l + 1 for l in range(n) for r in range(l, n) if ok(l, r))

    w1 = Steps("From each tub, walk until a third flavour appears.")
    extend_walk(w1, flavours, n, ok)
    w1.step(f"Most scoops: {want}.", result=want)

    w2 = Steps("Keep a count per flavour in the window and the number of distinct flavours. When a third flavour appears, drop tubs from the left until one flavour's count hits zero.")
    grow_shrink_walk(w2, flavours, n, ok, lambda l, r: {"flavours": sorted(set(flavours[l:r + 1]))})
    w2.step(f"Most scoops: {want}.", result=want)

    sol(
        "two-flavour-basket",
        summary="""
            The longest contiguous stretch with at most two distinct values. Slide a window with a count per flavour and a
            distinct counter; when a third flavour enters, advance the left edge until some flavour's count drops to
            zero. O(n), with an array of counts since flavours are below `n`.
        """,
        question=[
            """
            Return the length of the longest run of consecutive tubs that uses at most two different flavours.

            - **n up to 10⁵**, flavours in `[0, n)`.
            """
        ],
        think=[
            f"""
            `flavours = {flavours}` → **{want}** scoops.

            "Walk from any tub and stop before a forbidden one" is just "pick a contiguous window". A window with at most two
            flavours stays valid if you shrink it, so for each right end the best start only moves right. We need to know
            how many distinct flavours are inside, which a count per flavour plus a distinct counter maintains in O(1).
            """,
            fig(Row(flavours, label="flavours")),
        ],
        approaches=[
            approach(
                "Walk from every tub",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["For each start, extend while the window holds at most two flavours (remember the two you've taken)."],
                walk=w1,
                build=["Loop over starts.", "Track up to two flavours.", "Keep the longest."],
                code={
                    "python": """
                        class Solution:
                            def mostScoops(self, flavours: List[int]) -> int:
                                n, best = len(flavours), 0  #@init
                                for i in range(n):  #@starts
                                    taken, j = set(), i  #@extend
                                    while j < n and (flavours[j] in taken or len(taken) < 2):  #@extend
                                        taken.add(flavours[j])  #@extend
                                        j += 1  #@extend
                                    best = max(best, j - i)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int mostScoops(int[] flavours) {
                                int n = flavours.length, best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int a = flavours[i], b = -1, j = i;  //@extend
                                    while (j < n && (flavours[j] == a || flavours[j] == b || b == -1)) {  //@extend
                                        if (flavours[j] != a && b == -1) b = flavours[j];  //@extend
                                        j++;  //@extend
                                    }
                                    best = Math.max(best, j - i);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int mostScoops(vector<int>& flavours) {
                                int n = flavours.size(), best = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@starts
                                    int a = flavours[i], b = -1, j = i;  //@extend
                                    while (j < n && (flavours[j] == a || flavours[j] == b || b == -1)) {  //@extend
                                        if (flavours[j] != a && b == -1) b = flavours[j];  //@extend
                                        j++;  //@extend
                                    }
                                    best = max(best, j - i);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int mostScoops(int* flavours, int flavoursSize) {
                            int n = flavoursSize, best = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@starts
                                int a = flavours[i], b = -1, j = i;  //@extend
                                while (j < n && (flavours[j] == a || flavours[j] == b || b == -1)) {  //@extend
                                    if (flavours[j] != a && b == -1) b = flavours[j];  //@extend
                                    j++;  //@extend
                                }
                                if (j - i > best) best = j - i;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Most scoops so far."), ("starts", "Each starting tub."), ("extend", "Take the tub if its flavour is one of the (up to) two already chosen, or a second one is still free.", {"java": "Flavours are non-negative, so `b = −1` means 'second flavour not chosen yet'.", "cpp": "Flavours are non-negative, so `b = −1` means 'second flavour not chosen yet'.", "c": "Flavours are non-negative, so `b = −1` means 'second flavour not chosen yet'."}), ("best", "Scoops from this start."), ("ret", "Most scoops.")],
                complexity=["**Time O(n²)** (e.g. two alternating flavours). **Space O(1)** (O(1) set in Python too, at most two items)."],
                limits=["Re-walks the same tubs from every start."],
                slow=True,
            ),
            approach(
                "Window with flavour counts",
                "best",
                "O(n)",
                "O(n)",
                idea=["`count[f]` for the window and `distinct`. Add `flavours[r]` (a count going 0 → 1 adds a distinct). While `distinct > 2`, remove `flavours[left]` (a count going 1 → 0 removes one) and advance. Track the longest."],
                walk=w2,
                build=["Counts and distinct counter.", "Shrink while three flavours.", "Track the longest."],
                code={
                    "python": """
                        class Solution:
                            def mostScoops(self, flavours: List[int]) -> int:
                                count = [0] * len(flavours)  #@init
                                left = distinct = best = 0  #@init
                                for i, f in enumerate(flavours):  #@grow
                                    count[f] += 1  #@grow
                                    if count[f] == 1:  #@grow
                                        distinct += 1  #@grow
                                    while distinct > 2:  #@shrink
                                        g = flavours[left]  #@shrink
                                        count[g] -= 1  #@shrink
                                        if count[g] == 0:  #@shrink
                                            distinct -= 1  #@shrink
                                        left += 1  #@shrink
                                    best = max(best, i - left + 1)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int mostScoops(int[] flavours) {
                                int n = flavours.length, left = 0, distinct = 0, best = 0;  //@init
                                int[] count = new int[n];  //@init
                                for (int i = 0; i < n; i++) {  //@grow
                                    if (count[flavours[i]]++ == 0) distinct++;  //@grow
                                    while (distinct > 2) if (--count[flavours[left++]] == 0) distinct--;  //@shrink
                                    best = Math.max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int mostScoops(vector<int>& flavours) {
                                int n = flavours.size(), left = 0, distinct = 0, best = 0;  //@init
                                vector<int> count(n, 0);  //@init
                                for (int i = 0; i < n; i++) {  //@grow
                                    if (count[flavours[i]]++ == 0) distinct++;  //@grow
                                    while (distinct > 2) if (--count[flavours[left++]] == 0) distinct--;  //@shrink
                                    best = max(best, i - left + 1);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int mostScoops(int* flavours, int flavoursSize) {
                            int n = flavoursSize, left = 0, distinct = 0, best = 0;  //@init
                            int* count = calloc(n, sizeof(int));  //@init
                            for (int i = 0; i < n; i++) {  //@grow
                                if (count[flavours[i]]++ == 0) distinct++;  //@grow
                                while (distinct > 2) if (--count[flavours[left++]] == 0) distinct--;  //@shrink
                                if (i - left + 1 > best) best = i - left + 1;  //@best
                            }
                            free(count);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Counts indexed by flavour (all flavours are below `n`), and the number of flavours present."),
                    ("grow", "Add tub `i`; a flavour entering from zero is a new distinct one."),
                    ("shrink", "Three flavours: drop tubs from the left until a flavour disappears completely."),
                    ("best", "At most two flavours in `left..i`."),
                    ("ret", "Most scoops."),
                ],
                complexity=["**Time O(n).** **Space O(n)** for the counts (a map would be O(1) extra: at most 3 keys)."],
            ),
        ],
        takeaways=[
            """
            - **At most k distinct values in a window:** counts + a distinct counter, shrink while over k.
            - Update `distinct` only on 0 ↔ 1 transitions of a count.
            - The same code with `k` as a parameter solves "at most k distinct".
            """
        ],
    )
