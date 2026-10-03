"""Stacks & Queues: histogram area."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def spans(a):
    """Previous strictly smaller and next strictly smaller index for every bar."""
    n = len(a)
    left, right, st = [-1] * n, [n] * n, []
    for i in range(n):
        while st and a[st[-1]] >= a[i]:
            st.pop()
        left[i] = st[-1] if st else -1
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and a[st[-1]] >= a[i]:
            st.pop()
        right[i] = st[-1] if st else n
        st.append(i)
    return left, right


def best_bar_area(h):
    l, r = spans(h)
    return max(h[i] * (r[i] - l[i] - 1) for i in range(len(h)))


@problem
def poster_reach():
    panels = [3, 5, 4, 1, 4, 6, 2]
    n = len(panels)
    L, R = spans(panels)
    want = [R[i] - L[i] - 1 for i in range(n)]

    w1 = Steps("For each panel, spread the poster left and right while the neighbouring panels are at least as tall.")
    for i in range(n):
        lo, hi = L[i] + 1, R[i] - 1
        w1.step(f"Panel {i} (height {panels[i]}): spreads over panels {lo}..{hi}, stopped by {'panel ' + str(L[i]) if L[i] >= 0 else 'the left end'} and {'panel ' + str(R[i]) if R[i] < n else 'the right end'}. Width {want[i]}.", Row(panels, st={**{k: "mark" for k in range(lo, hi + 1)}, i: "active"}), Row(want[:i + 1] + ["·"] * (n - i - 1), label="width"))
    w1.step(f"Widths: {want}.", result=str(want))

    w2 = Steps("Two monotonic-stack passes: the nearest shorter panel on the left, then on the right. The poster fills the gap between them.")
    st, lv = [], []
    for i in range(n):
        popped = []
        while st and panels[st[-1]] >= panels[i]:
            popped.append(st.pop())
        lv.append(st[-1] if st else -1)
        w2.step(f"Left pass, panel {i} ({panels[i]}): pop {('panels ' + str(popped)) if popped else 'nothing'} (not shorter). Nearest shorter on the left: {lv[-1] if lv[-1] >= 0 else 'none (−1)'}.", Row(panels, st={i: "active"}), Row([f"{k}:{panels[k]}" for k in st] or ["·"], label="stack (index:height)"), Row(lv + ["·"] * (n - i - 1), label="left stop"))
        st.append(i)
    st, rv = [], [n] * n
    for i in range(n - 1, -1, -1):
        popped = []
        while st and panels[st[-1]] >= panels[i]:
            popped.append(st.pop())
        rv[i] = st[-1] if st else n
        w2.step(f"Right pass, panel {i} ({panels[i]}): pop {('panels ' + str(popped)) if popped else 'nothing'}. Nearest shorter on the right: {rv[i] if rv[i] < n else f'none ({n})'}. Width {rv[i]} − {lv[i]} − 1 = {rv[i] - lv[i] - 1}.", Row(panels, st={i: "active"}), Row([f"{k}:{panels[k]}" for k in st] or ["·"], label="stack (index:height)"), Row(["·"] * i + [rv[k] - lv[k] - 1 for k in range(i, n)], label="width"))
        st.append(i)
    w2.step(f"Widths: {want}.", result=str(want))

    sol(
        "poster-reach",
        summary="""
            A poster on panel `i` spreads until it hits a strictly shorter panel on each side. So its width is the gap
            between the nearest shorter panel on the left and the nearest shorter panel on the right. A monotonic stack
            finds the nearest shorter panel for every position in one pass per side: O(n).
        """,
        question=[
            """
            For every panel, imagine a poster exactly as tall as that panel. It must cover the panel and may extend sideways
            over neighbouring panels, but only ones at least as tall. How wide can it get?

            - **Equal heights don't stop it**, only strictly shorter panels do.
            - **The answer is one width per panel**, in order.
            - **Up to 10⁵ panels.**
            """
        ],
        think=[
            f"""
            Panels `{panels}`. Panel 1 (height 5) is boxed in by 3 and 4 on either side: width 1. Panel 2 (height 4) covers
            panel 1 (5 ≥ 4), then stops at panel 0 (3 < 4) on the left and at panel 3 (height 1) on the right: width 2. Panel 3 (height 1) is the shortest, so it covers all
            {n}. Widths: `{want}`.
            """,
            fig(Row(panels, label="panels"), Row(want, label="width")),
            """
            Each poster is fenced in by the **nearest strictly shorter panel** on each side, so the whole problem is
            "nearest shorter to the left" and "nearest shorter to the right" for every index.

            Scanning left to right, a panel that has a shorter-or-equal panel after it can never be anyone's nearest
            shorter panel again: the later one is closer and at least as short. Throwing such panels away leaves a stack of
            strictly increasing heights, and its top (after popping) is exactly the nearest shorter panel.
            """,
        ],
        approaches=[
            approach(
                "Spread each poster panel by panel",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each panel, walk left while the next panel is at least as tall, then right the same way. The width is the number of panels covered."],
                walk=w1,
                build=["For each `i`: move `l` left while `panels[l − 1] ≥ panels[i]`.", "Move `r` right while `panels[r + 1] ≥ panels[i]`.", "Width `r − l + 1`."],
                code={
                    "python": """
                        class Solution:
                            def posterReach(self, panels: List[int]) -> List[int]:
                                n = len(panels)  #@init
                                width = [0] * n  #@init
                                for i in range(n):  #@each
                                    l = i  #@left
                                    while l > 0 and panels[l - 1] >= panels[i]:  #@left
                                        l -= 1  #@left
                                    r = i  #@right
                                    while r < n - 1 and panels[r + 1] >= panels[i]:  #@right
                                        r += 1  #@right
                                    width[i] = r - l + 1  #@set
                                return width  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] posterReach(int[] panels) {
                                int n = panels.length;  //@init
                                int[] width = new int[n];  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    int l = i;  //@left
                                    while (l > 0 && panels[l - 1] >= panels[i]) l--;  //@left
                                    int r = i;  //@right
                                    while (r < n - 1 && panels[r + 1] >= panels[i]) r++;  //@right
                                    width[i] = r - l + 1;  //@set
                                }
                                return width;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> posterReach(vector<int>& panels) {
                                int n = panels.size();  //@init
                                vector<int> width(n);  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    int l = i;  //@left
                                    while (l > 0 && panels[l - 1] >= panels[i]) l--;  //@left
                                    int r = i;  //@right
                                    while (r < n - 1 && panels[r + 1] >= panels[i]) r++;  //@right
                                    width[i] = r - l + 1;  //@set
                                }
                                return width;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* posterReach(int* panels, int panelsSize, int* returnSize) {
                            int n = panelsSize;  //@init
                            int* width = malloc(n * sizeof(int));  //@init
                            for (int i = 0; i < n; i++) {  //@each
                                int l = i;  //@left
                                while (l > 0 && panels[l - 1] >= panels[i]) l--;  //@left
                                int r = i;  //@right
                                while (r < n - 1 && panels[r + 1] >= panels[i]) r++;  //@right
                                width[i] = r - l + 1;  //@set
                            }
                            *returnSize = n;  //@ret
                            return width;  //@ret
                        }
                    """,
                },
                lines=[("init", "One width per panel."), ("each", "Measure panel `i`'s poster."), ("left", "Spread left over panels at least as tall."), ("right", "Spread right the same way."), ("set", "Panels `l..r` are covered."), ("ret", "All widths.")],
                complexity=["**Time O(n²)** in the worst case (all panels equal: every poster spreads over everything). **Space O(1)** beyond the answer."],
                limits=["Each panel re-walks ground its neighbours already walked. With 10⁵ equal panels that's 10¹⁰ steps. The only facts needed are the nearest shorter panels, which a stack provides for everyone in O(n)."],
                slow=True,
            ),
            approach(
                "Nearest shorter panel, from both sides",
                "best",
                "O(n)",
                "O(n)",
                idea=["Left to right, keep a stack of indices with strictly increasing heights. For panel `i`, pop every panel at least as tall; the top is now the nearest shorter panel on the left (or −1). Push `i`. Do the same right to left for the nearest shorter on the right (or `n`). The width is `right − left − 1`."],
                walk=w2,
                build=["`left[i]` from a left-to-right stack pass (pop while `≥`).", "`right[i]` from a right-to-left pass (pop while `≥`).", "`width[i] = right[i] − left[i] − 1`."],
                code={
                    "python": """
                        class Solution:
                            def posterReach(self, panels: List[int]) -> List[int]:
                                n = len(panels)  #@init
                                left, right = [-1] * n, [n] * n  #@init
                                stack = []  #@lpass
                                for i in range(n):  #@lpass
                                    while stack and panels[stack[-1]] >= panels[i]:  #@pop
                                        stack.pop()  #@pop
                                    left[i] = stack[-1] if stack else -1  #@lpass
                                    stack.append(i)  #@lpass
                                stack = []  #@rpass
                                for i in range(n - 1, -1, -1):  #@rpass
                                    while stack and panels[stack[-1]] >= panels[i]:  #@rpass
                                        stack.pop()  #@rpass
                                    right[i] = stack[-1] if stack else n  #@rpass
                                    stack.append(i)  #@rpass
                                return [right[i] - left[i] - 1 for i in range(n)]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] posterReach(int[] panels) {
                                int n = panels.length;  //@init
                                int[] left = new int[n], stack = new int[n], width = new int[n];  //@init
                                int top = 0;  //@lpass
                                for (int i = 0; i < n; i++) {  //@lpass
                                    while (top > 0 && panels[stack[top - 1]] >= panels[i]) top--;  //@pop
                                    left[i] = top > 0 ? stack[top - 1] : -1;  //@lpass
                                    stack[top++] = i;  //@lpass
                                }
                                top = 0;  //@rpass
                                for (int i = n - 1; i >= 0; i--) {  //@rpass
                                    while (top > 0 && panels[stack[top - 1]] >= panels[i]) top--;  //@rpass
                                    int right = top > 0 ? stack[top - 1] : n;  //@rpass
                                    width[i] = right - left[i] - 1;  //@ret
                                    stack[top++] = i;  //@rpass
                                }
                                return width;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> posterReach(vector<int>& panels) {
                                int n = panels.size();  //@init
                                vector<int> left(n), width(n), stack;  //@init
                                for (int i = 0; i < n; i++) {  //@lpass
                                    while (!stack.empty() && panels[stack.back()] >= panels[i]) stack.pop_back();  //@pop
                                    left[i] = stack.empty() ? -1 : stack.back();  //@lpass
                                    stack.push_back(i);  //@lpass
                                }
                                stack.clear();  //@rpass
                                for (int i = n - 1; i >= 0; i--) {  //@rpass
                                    while (!stack.empty() && panels[stack.back()] >= panels[i]) stack.pop_back();  //@rpass
                                    int right = stack.empty() ? n : stack.back();  //@rpass
                                    width[i] = right - left[i] - 1;  //@ret
                                    stack.push_back(i);  //@rpass
                                }
                                return width;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* posterReach(int* panels, int panelsSize, int* returnSize) {
                            int n = panelsSize;  //@init
                            int* left = malloc(n * sizeof(int));  //@init
                            int* stack = malloc(n * sizeof(int));  //@init
                            int* width = malloc(n * sizeof(int));  //@init
                            int top = 0;  //@lpass
                            for (int i = 0; i < n; i++) {  //@lpass
                                while (top > 0 && panels[stack[top - 1]] >= panels[i]) top--;  //@pop
                                left[i] = top > 0 ? stack[top - 1] : -1;  //@lpass
                                stack[top++] = i;  //@lpass
                            }
                            top = 0;  //@rpass
                            for (int i = n - 1; i >= 0; i--) {  //@rpass
                                while (top > 0 && panels[stack[top - 1]] >= panels[i]) top--;  //@rpass
                                int right = top > 0 ? stack[top - 1] : n;  //@rpass
                                width[i] = right - left[i] - 1;  //@ret
                                stack[top++] = i;  //@rpass
                            }
                            free(left);  //@ret
                            free(stack);  //@ret
                            *returnSize = n;  //@ret
                            return width;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Nearest shorter panel on each side, defaulting to the ends (−1 and `n`)."),
                    ("lpass", "Left to right: after popping, the top of the stack is the nearest strictly shorter panel to the left. Then `i` joins the stack."),
                    ("pop", "A panel at least as tall as panel `i` can never be the nearest shorter panel for anything further right: `i` is closer and no taller. Discard it for good."),
                    ("rpass", "The mirror pass from the right gives the nearest strictly shorter panel on the right."),
                    ("ret", "The poster fills the open gap between the two stoppers: `right − left − 1` panels.", {"java": "The width is filled in during the right pass, once both stoppers are known.", "cpp": "The width is filled in during the right pass, once both stoppers are known.", "c": "The width is filled in during the right pass, once both stoppers are known."}),
                ],
                complexity=["**Time O(n):** each index is pushed and popped at most once per pass. **Space O(n)** for the stack and the left stoppers."],
            ),
        ],
        takeaways=[
            """
            - "How far can I extend while everything stays ≥ me?" = gap between the **nearest strictly smaller** elements.
            - A monotonic (increasing) stack finds the nearest smaller element for every index in O(n) total.
            - This is the building block of the largest-rectangle problems that follow.
            """
        ],
    )


@problem
def biggest_billboard():
    heights = [2, 4, 5, 3, 1, 3]
    n = len(heights)
    L, R = spans(heights)
    areas = [heights[i] * (R[i] - L[i] - 1) for i in range(n)]
    want = max(areas)

    w1 = Steps("Every start building, extended right one building at a time: the billboard's height is the shortest building so far.")
    best = 0
    for i in range(n):
        low, ar = heights[i], []
        for j in range(i, n):
            low = min(low, heights[j])
            ar.append(low * (j - i + 1))
        best = max(best, max(ar))
        w1.step(f"Start at building {i}: areas {ar} for ends {i}..{n - 1}.", Row(heights, st={i: "active"}), Row(["·"] * i + ar, label="area"), Vars(best=best))
    w1.step(f"Biggest: {best}.", result=best)

    w2 = Steps("Each building's own billboard: as tall as the building, as wide as its poster reach. The biggest billboard is one of these.")
    for i in range(n):
        w2.step(f"Building {i} (height {heights[i]}): reach {L[i] + 1}..{R[i] - 1}, width {R[i] - L[i] - 1}, area {areas[i]}.", Row(heights, st={**{k: "mark" for k in range(L[i] + 1, R[i])}, i: "active"}), Row(areas[:i + 1] + ["·"] * (n - i - 1), label="area"))
    w2.step(f"Largest of these: {want}.", result=want)

    w3 = Steps("One pass with a stack of increasing heights (plus a height-0 building at the end). When a building is popped, both of its boundaries are known at once.")
    st, best = [], 0
    for i in range(n + 1):
        h = heights[i] if i < n else 0
        while st and heights[st[-1]] >= h:
            top = st.pop()
            left = st[-1] if st else -1
            area = heights[top] * (i - left - 1)
            best = max(best, area)
            w3.step(f"{'End sentinel' if i == n else f'Building {i} ({h})'} is no taller than building {top} ({heights[top]}): pop it. Its billboard spans {left + 1}..{i - 1}: {heights[top]} × {i - left - 1} = {area}.", Row(heights + ["0"], st={i: "active", top: "mark"}), Row([f"{k}:{heights[k]}" for k in st] or ["·"], label="stack (index:height)"), Vars(best=best))
        if i < n:
            st.append(i)
            w3.step(f"Push building {i} ({h}).", Row(heights + ["0"], st={i: "active"}), Row([f"{k}:{heights[k]}" for k in st], label="stack (index:height)"), Vars(best=best))
    w3.step(f"Biggest billboard: {best}.", result=best)

    sol(
        "biggest-billboard",
        summary="""
            The biggest billboard is as tall as the shortest building under it, so it's always some building's own
            billboard: as tall as that building, stretched until a shorter building on each side. A stack of increasing
            heights finds both stoppers for every building in one pass: when a building is popped, the new top is its left
            stopper and the current building its right stopper. O(n).
        """,
        question=[
            """
            Buildings of width 1 stand side by side. Choose a run of neighbouring buildings and paint a rectangle from the
            ground up, no taller than any building in the run. Return the largest area.

            - **Height-0 buildings exist**: nothing can be painted across them.
            - **Heights reach 10⁹ and there are up to 10⁵ buildings**, so areas reach 10¹⁴: the answer is a `long`.
            """
        ],
        think=[
            f"""
            Heights `{heights}`. The run 4, 5, 3 gives height 3 × width 3 = 9. The run 4, 5 gives 4 × 2 = 8; all six give
            1 × 6 = 6. The best is **{want}**.
            """,
            fig(Row(heights, st={k: "found" for k in range(1, 4)}), caption="Height 3 across buildings 1–3: area 9."),
            """
            For a best billboard, look at the shortest building under it. The billboard's height is that building's
            height, and it can't be any wider than that building's reach (until a strictly shorter building on each side),
            otherwise it would be wider at the same height. So **the answer is the best of n candidates**, one per building:
            `height[i] × reach[i]`. That's the poster-reach problem, plus a multiplication.
            """,
            table(["building", "height", "reach", "area"], *[(i, heights[i], R[i] - L[i] - 1, areas[i]) for i in range(n)]),
        ],
        approaches=[
            approach(
                "Every run, with a running minimum",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start, extend right one building at a time, keeping the shortest height so far; each run's area is `shortest × width`. Keep the maximum."],
                walk=w1,
                build=["For each start `i`, `low = heights[i]`.", "For each end `j`, `low = min(low, heights[j])`, area `low × (j − i + 1)`.", "Return the largest area."],
                code={
                    "python": """
                        class Solution:
                            def biggestBillboard(self, heights: List[int]) -> int:
                                best = 0  #@init
                                for i in range(len(heights)):  #@start
                                    low = heights[i]  #@start
                                    for j in range(i, len(heights)):  #@extend
                                        low = min(low, heights[j])  #@extend
                                        best = max(best, low * (j - i + 1))  #@area
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long biggestBillboard(int[] heights) {
                                long best = 0;  //@init
                                for (int i = 0; i < heights.length; i++) {  //@start
                                    int low = heights[i];  //@start
                                    for (int j = i; j < heights.length; j++) {  //@extend
                                        low = Math.min(low, heights[j]);  //@extend
                                        best = Math.max(best, (long) low * (j - i + 1));  //@area
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long biggestBillboard(vector<int>& heights) {
                                long long best = 0;  //@init
                                for (size_t i = 0; i < heights.size(); i++) {  //@start
                                    int low = heights[i];  //@start
                                    for (size_t j = i; j < heights.size(); j++) {  //@extend
                                        low = min(low, heights[j]);  //@extend
                                        best = max(best, (long long) low * (long long) (j - i + 1));  //@area
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long biggestBillboard(int* heights, int heightsSize) {
                            long long best = 0;  //@init
                            for (int i = 0; i < heightsSize; i++) {  //@start
                                int low = heights[i];  //@start
                                for (int j = i; j < heightsSize; j++) {  //@extend
                                    if (heights[j] < low) low = heights[j];  //@extend
                                    long long area = (long long) low * (j - i + 1);  //@area
                                    if (area > best) best = area;  //@area
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Best area so far (64-bit)."), ("start", "Runs starting at building `i`."), ("extend", "The billboard can be no taller than the shortest building in the run."), ("area", "Height × width, in 64 bits: up to 10⁹ × 10⁵."), ("ret", "The largest area.")],
                complexity=["**Time O(n²)** runs. **Space O(1).**"],
                limits=["About 5 × 10⁹ runs for 10⁵ buildings. Only n runs can be the answer (each building's full reach), so there's no need to look at the rest."],
                slow=True,
            ),
            approach(
                "Each building's reach, from two stack passes",
                "better",
                "O(n)",
                "O(n)",
                idea=["Compute every building's nearest strictly shorter neighbour on the left and on the right with monotonic stacks (exactly as in poster reach). Building `i`'s billboard has area `heights[i] × (right[i] − left[i] − 1)`. Return the largest."],
                walk=w2,
                build=["Left pass: nearest shorter on the left (−1 if none).", "Right pass: nearest shorter on the right (`n` if none), computing the area as you go.", "Keep the maximum."],
                code={
                    "python": """
                        class Solution:
                            def biggestBillboard(self, heights: List[int]) -> int:
                                n = len(heights)  #@init
                                left, stack = [-1] * n, []  #@init
                                for i in range(n):  #@lpass
                                    while stack and heights[stack[-1]] >= heights[i]:  #@lpass
                                        stack.pop()  #@lpass
                                    left[i] = stack[-1] if stack else -1  #@lpass
                                    stack.append(i)  #@lpass
                                best, stack = 0, []  #@rpass
                                for i in range(n - 1, -1, -1):  #@rpass
                                    while stack and heights[stack[-1]] >= heights[i]:  #@rpass
                                        stack.pop()  #@rpass
                                    right = stack[-1] if stack else n  #@rpass
                                    best = max(best, heights[i] * (right - left[i] - 1))  #@area
                                    stack.append(i)  #@rpass
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long biggestBillboard(int[] heights) {
                                int n = heights.length;  //@init
                                int[] left = new int[n], stack = new int[n];  //@init
                                int top = 0;  //@lpass
                                for (int i = 0; i < n; i++) {  //@lpass
                                    while (top > 0 && heights[stack[top - 1]] >= heights[i]) top--;  //@lpass
                                    left[i] = top > 0 ? stack[top - 1] : -1;  //@lpass
                                    stack[top++] = i;  //@lpass
                                }
                                long best = 0;  //@rpass
                                top = 0;  //@rpass
                                for (int i = n - 1; i >= 0; i--) {  //@rpass
                                    while (top > 0 && heights[stack[top - 1]] >= heights[i]) top--;  //@rpass
                                    int right = top > 0 ? stack[top - 1] : n;  //@rpass
                                    best = Math.max(best, (long) heights[i] * (right - left[i] - 1));  //@area
                                    stack[top++] = i;  //@rpass
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long biggestBillboard(vector<int>& heights) {
                                int n = heights.size();  //@init
                                vector<int> left(n), stack;  //@init
                                for (int i = 0; i < n; i++) {  //@lpass
                                    while (!stack.empty() && heights[stack.back()] >= heights[i]) stack.pop_back();  //@lpass
                                    left[i] = stack.empty() ? -1 : stack.back();  //@lpass
                                    stack.push_back(i);  //@lpass
                                }
                                long long best = 0;  //@rpass
                                stack.clear();  //@rpass
                                for (int i = n - 1; i >= 0; i--) {  //@rpass
                                    while (!stack.empty() && heights[stack.back()] >= heights[i]) stack.pop_back();  //@rpass
                                    int right = stack.empty() ? n : stack.back();  //@rpass
                                    best = max(best, (long long) heights[i] * (right - left[i] - 1));  //@area
                                    stack.push_back(i);  //@rpass
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long biggestBillboard(int* heights, int heightsSize) {
                            int n = heightsSize;  //@init
                            int* left = malloc(n * sizeof(int));  //@init
                            int* stack = malloc(n * sizeof(int));  //@init
                            int top = 0;  //@lpass
                            for (int i = 0; i < n; i++) {  //@lpass
                                while (top > 0 && heights[stack[top - 1]] >= heights[i]) top--;  //@lpass
                                left[i] = top > 0 ? stack[top - 1] : -1;  //@lpass
                                stack[top++] = i;  //@lpass
                            }
                            long long best = 0;  //@rpass
                            top = 0;  //@rpass
                            for (int i = n - 1; i >= 0; i--) {  //@rpass
                                while (top > 0 && heights[stack[top - 1]] >= heights[i]) top--;  //@rpass
                                int right = top > 0 ? stack[top - 1] : n;  //@rpass
                                long long area = (long long) heights[i] * (right - left[i] - 1);  //@area
                                if (area > best) best = area;  //@area
                                stack[top++] = i;  //@rpass
                            }
                            free(left);  //@ret
                            free(stack);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Left stoppers and a stack."), ("lpass", "Nearest strictly shorter building on the left, via a stack of increasing heights."), ("rpass", "The same from the right; now both stoppers of building `i` are known."), ("area", "Building `i`'s billboard: its height across its whole reach."), ("ret", "The best candidate is the answer.")],
                complexity=["**Time O(n).** **Space O(n)** for the left stoppers and the stack."],
                limits=["Already linear, but it needs two passes and an extra array. In the left pass, the moment a building is **popped**, the building popping it is its right stopper and the new top is its left stopper: one pass is enough."],
            ),
            approach(
                "One pass: measure each building when it's popped",
                "best",
                "O(n)",
                "O(n)",
                idea=["Keep a stack of indices with increasing heights. When building `i` is no taller than the top, the top's reach ends at `i − 1` on the right, and on the left it ends just after the next index down the stack. Pop it and record `height × (i − newTop − 1)`. A height-0 sentinel after the last building pops everything left at the end."],
                walk=w3,
                build=["Loop `i` from 0 to `n`, with height 0 at `i = n`.", "While the top is at least as tall as the current height: pop it, width = `i − (new top or −1) − 1`, update the best.", "Push `i`."],
                code={
                    "python": """
                        class Solution:
                            def biggestBillboard(self, heights: List[int]) -> int:
                                best, stack = 0, []  #@init
                                for i, h in enumerate(heights + [0]):  #@loop
                                    while stack and heights[stack[-1]] >= h:  #@pop
                                        height = heights[stack.pop()]  #@pop
                                        left = stack[-1] if stack else -1  #@width
                                        best = max(best, height * (i - left - 1))  #@width
                                    stack.append(i)  #@push
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long biggestBillboard(int[] heights) {
                                int n = heights.length;  //@init
                                int[] stack = new int[n + 1];  //@init
                                int top = 0;  //@init
                                long best = 0;  //@init
                                for (int i = 0; i <= n; i++) {  //@loop
                                    int h = i < n ? heights[i] : 0;  //@loop
                                    while (top > 0 && heights[stack[top - 1]] >= h) {  //@pop
                                        int height = heights[stack[--top]];  //@pop
                                        int left = top > 0 ? stack[top - 1] : -1;  //@width
                                        best = Math.max(best, (long) height * (i - left - 1));  //@width
                                    }
                                    stack[top++] = i;  //@push
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long biggestBillboard(vector<int>& heights) {
                                int n = heights.size();  //@init
                                vector<int> stack;  //@init
                                long long best = 0;  //@init
                                for (int i = 0; i <= n; i++) {  //@loop
                                    int h = i < n ? heights[i] : 0;  //@loop
                                    while (!stack.empty() && heights[stack.back()] >= h) {  //@pop
                                        int height = heights[stack.back()];  //@pop
                                        stack.pop_back();  //@pop
                                        int left = stack.empty() ? -1 : stack.back();  //@width
                                        best = max(best, (long long) height * (i - left - 1));  //@width
                                    }
                                    stack.push_back(i);  //@push
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long biggestBillboard(int* heights, int heightsSize) {
                            int n = heightsSize;  //@init
                            int* stack = malloc((n + 1) * sizeof(int));  //@init
                            int top = 0;  //@init
                            long long best = 0;  //@init
                            for (int i = 0; i <= n; i++) {  //@loop
                                int h = i < n ? heights[i] : 0;  //@loop
                                while (top > 0 && heights[stack[top - 1]] >= h) {  //@pop
                                    int height = heights[stack[--top]];  //@pop
                                    int left = top > 0 ? stack[top - 1] : -1;  //@width
                                    long long area = (long long) height * (i - left - 1);  //@width
                                    if (area > best) best = area;  //@width
                                }
                                stack[top++] = i;  //@push
                            }
                            free(stack);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "A stack of indices whose heights increase from bottom to top, and the best area."),
                    ("loop", "All buildings, then a height-0 sentinel so every building still on the stack gets popped and measured.", {"python": "The sentinel is pushed as index `n`, but it's never popped, so `heights[n]` is never read."}),
                    ("pop", "The current building is no taller than the top, so the top's billboard can't extend past `i − 1`. Pop it: its right stopper is `i`."),
                    ("width", "The building below it on the stack is the nearest shorter one on its left (everything between was popped because it was taller). So the billboard spans `left + 1 .. i − 1`. With equal heights, the earlier copy is measured short, but the last copy gets the full width, so the maximum is unaffected."),
                    ("push", "The current building waits until something no taller shows up."),
                    ("ret", "Every building was measured exactly once."),
                ],
                complexity=["**Time O(n):** each index is pushed and popped once. **Space O(n)** for the stack."],
            ),
        ],
        takeaways=[
            """
            - **Largest rectangle under a histogram:** the answer is some bar's height times that bar's reach.
            - One pass: a bar's reach is known the moment it's popped (right stopper = the popper, left stopper = the new
              top). A 0-height sentinel flushes the stack.
            - Use 64-bit areas when heights and widths are both large.
            """
        ],
    )


@problem
def largest_clear_plot():
    land = ["01101", "11110", "11111", "01101"]
    R, C = len(land), len(land[0])
    grid = [list(r) for r in land]

    def biggest_from(r1, c1):
        best, box = 0, None
        for r2 in range(r1, R):
            for c2 in range(c1, C):
                if all(land[r][c] == "1" for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)):
                    a = (r2 - r1 + 1) * (c2 - c1 + 1)
                    if a > best:
                        best, box = a, (r2, c2)
        return best, box

    w1 = Steps("Try every rectangle, checking that it has no rocks. Here: for each clear top-left cell, the biggest clear rectangle starting there.")
    best = 0
    for r in range(R):
        for c in range(C):
            if land[r][c] != "1":
                continue
            a, (r2, c2) = biggest_from(r, c)
            best = max(best, a)
            w1.step(f"Top-left ({r}, {c}): the biggest clear rectangle reaches ({r2}, {c2}), area {a}.", Grid(grid, st={(i, j): "mark" for i in range(r, r2 + 1) for j in range(c, c2 + 1)} | {(r, c): "active"}), Vars(best=best))
    w1.step(f"Largest clear plot: {best}.", result=best)

    w2 = Steps("Fix the top and bottom rows of the plot. A column is usable if it's clear in every row between them; the widest run of usable columns gives the best plot for that band.")
    best = 0
    for top in range(R):
        ok = [True] * C
        for bot in range(top, R):
            ok = [ok[c] and land[bot][c] == "1" for c in range(C)]
            run = width = 0
            for c in range(C):
                run = run + 1 if ok[c] else 0
                width = max(width, run)
            best = max(best, width * (bot - top + 1))
            w2.step(f"Rows {top}..{bot}: usable columns {[c for c in range(C) if ok[c]]}; widest run {width} × height {bot - top + 1} = {width * (bot - top + 1)}.", Grid(grid, st={(r, c): ("found" if ok[c] else "mark") for r in range(top, bot + 1) for c in range(C)}), Row(["✓" if x else "·" for x in ok], label="usable"), Vars(best=best))
    w2.step(f"Largest clear plot: {best}.", result=best)

    w3 = Steps("Row by row, count how many clear cells stand directly above-and-including each cell. Each row is then a histogram, and the biggest rectangle in it is the biggest plot whose bottom edge is that row.")
    h, best = [0] * C, 0
    for r in range(R):
        h = [h[c] + 1 if land[r][c] == "1" else 0 for c in range(C)]
        a = best_bar_area(h)
        best = max(best, a)
        w3.step(f"Row {r}: column heights {h}. Biggest rectangle in this histogram: {a}.", Grid(grid, st={(r, c): "active" for c in range(C)}), Row(h, label="heights"), Vars(best=best))
    w3.step(f"Largest clear plot: {best}.", result=best)
    want = best
    assert want == 8

    sol(
        "largest-clear-plot",
        summary="""
            Treat each row as the bottom edge of the plot. For every column, count the clear cells stacked up to and
            including this row; that turns the row into a histogram, and the largest plot with this bottom edge is the
            largest rectangle in that histogram (the stack method). Heights update in O(1) per cell from the row above.
            O(rows × cols).
        """,
        question=[
            """
            The field is a grid of `'1'` (clear) and `'0'` (rocks). Find the largest axis-aligned rectangle made only of
            clear cells, and return its area. If there are no clear cells, return 0.

            - **Cells are characters**, `'0'` and `'1'`, not numbers.
            - **Up to 500 × 500 cells**: there are about 1.6 × 10¹⁰ rectangles, so they can't all be checked.
            """
        ],
        think=[
            f"""
            Here is a 4 × 5 field. The largest clear plot has area **{want}**: for example, rows 1–2 × columns 0–3.
            """,
            fig(Grid(grid, st={(r, c): "found" for r in range(1, 3) for c in range(0, 4)}), caption="A clear 2 × 4 plot."),
            """
            Every plot has a bottom row. Fix that row: going up from it, each column has some number of consecutive clear
            cells (its height). A plot sitting on this row, spanning some columns, can be as tall as the shortest of those
            columns' heights. That's exactly the largest-rectangle-in-a-histogram problem, once per row.

            The heights are easy to keep up to date: going down one row, a clear cell adds 1 to its column's height and a
            rock resets it to 0.
            """,
        ],
        approaches=[
            approach(
                "Check every rectangle",
                "brute",
                "O(R²·C²·R·C)",
                "O(1)",
                idea=["Enumerate every top-left and bottom-right corner, check every cell inside for rocks, and keep the largest all-clear area. (2-D prefix sums of rocks would make each check O(1), but the number of rectangles alone is already too large.)"],
                walk=w1,
                build=["Loop over top-left (`r1`, `c1`) and bottom-right (`r2`, `c2`).", "Check every cell inside; stop at the first rock.", "Track the largest clear area."],
                code={
                    "python": """
                        class Solution:
                            def largestClearPlot(self, land: List[List[str]]) -> int:
                                R, C = len(land), len(land[0])  #@init
                                best = 0  #@init
                                for r1 in range(R):  #@corners
                                    for c1 in range(C):  #@corners
                                        for r2 in range(r1, R):  #@corners
                                            for c2 in range(c1, C):  #@corners
                                                if all(land[r][c] == "1" for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)):  #@check
                                                    best = max(best, (r2 - r1 + 1) * (c2 - c1 + 1))  #@area
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int largestClearPlot(char[][] land) {
                                int R = land.length, C = land[0].length;  //@init
                                int best = 0;  //@init
                                for (int r1 = 0; r1 < R; r1++)  //@corners
                                    for (int c1 = 0; c1 < C; c1++)  //@corners
                                        for (int r2 = r1; r2 < R; r2++)  //@corners
                                            for (int c2 = c1; c2 < C; c2++) {  //@corners
                                                boolean clear = true;  //@check
                                                for (int r = r1; r <= r2 && clear; r++)  //@check
                                                    for (int c = c1; c <= c2 && clear; c++)  //@check
                                                        if (land[r][c] != '1') clear = false;  //@check
                                                if (clear) best = Math.max(best, (r2 - r1 + 1) * (c2 - c1 + 1));  //@area
                                            }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int largestClearPlot(vector<vector<char>>& land) {
                                int R = land.size(), C = land[0].size();  //@init
                                int best = 0;  //@init
                                for (int r1 = 0; r1 < R; r1++)  //@corners
                                    for (int c1 = 0; c1 < C; c1++)  //@corners
                                        for (int r2 = r1; r2 < R; r2++)  //@corners
                                            for (int c2 = c1; c2 < C; c2++) {  //@corners
                                                bool clear = true;  //@check
                                                for (int r = r1; r <= r2 && clear; r++)  //@check
                                                    for (int c = c1; c <= c2 && clear; c++)  //@check
                                                        if (land[r][c] != '1') clear = false;  //@check
                                                if (clear) best = max(best, (r2 - r1 + 1) * (c2 - c1 + 1));  //@area
                                            }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int largestClearPlot(char** land, int landSize, int* landColSize) {
                            int R = landSize, C = landColSize[0];  //@init
                            int best = 0;  //@init
                            for (int r1 = 0; r1 < R; r1++)  //@corners
                                for (int c1 = 0; c1 < C; c1++)  //@corners
                                    for (int r2 = r1; r2 < R; r2++)  //@corners
                                        for (int c2 = c1; c2 < C; c2++) {  //@corners
                                            bool clear = true;  //@check
                                            for (int r = r1; r <= r2 && clear; r++)  //@check
                                                for (int c = c1; c <= c2 && clear; c++)  //@check
                                                    if (land[r][c] != '1') clear = false;  //@check
                                            int area = (r2 - r1 + 1) * (c2 - c1 + 1);  //@area
                                            if (clear && area > best) best = area;  //@area
                                        }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Grid size and the best area."), ("corners", "Every rectangle, by its top-left and bottom-right corners."), ("check", "Is every cell inside clear? Stop at the first rock."), ("area", "Clear: compare its area with the best."), ("ret", "The largest clear area.")],
                complexity=["**Time O(R²C²)** rectangles, each checked in up to O(RC). **Space O(1).**"],
                limits=["Hopeless beyond tiny fields: a 500 × 500 grid has ~1.6 × 10¹⁰ rectangles before even checking them. Fixing two rows and reusing the work between bands removes most of it."],
                slow=True,
            ),
            approach(
                "Fix the top and bottom rows",
                "better",
                "O(R²·C)",
                "O(C)",
                idea=["For each top row, grow the bottom row downward while keeping, per column, whether the column is clear in every row of the band (AND it with the new row). The best plot in the band is the longest run of usable columns times the band's height."],
                walk=w2,
                build=["For each `top`: reset `usable[c] = true`.", "For each `bottom` from `top` down: `usable[c] &= land[bottom][c] == '1'`.", "Scan the columns for the longest run of usable ones; area = run × (bottom − top + 1)."],
                code={
                    "python": """
                        class Solution:
                            def largestClearPlot(self, land: List[List[str]]) -> int:
                                R, C = len(land), len(land[0])  #@init
                                best = 0  #@init
                                for top in range(R):  #@top
                                    usable = [True] * C  #@top
                                    for bottom in range(top, R):  #@bottom
                                        run = 0  #@bottom
                                        for c in range(C):  #@and
                                            usable[c] = usable[c] and land[bottom][c] == "1"  #@and
                                            run = run + 1 if usable[c] else 0  #@run
                                            best = max(best, run * (bottom - top + 1))  #@run
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int largestClearPlot(char[][] land) {
                                int R = land.length, C = land[0].length;  //@init
                                int best = 0;  //@init
                                boolean[] usable = new boolean[C];  //@init
                                for (int top = 0; top < R; top++) {  //@top
                                    Arrays.fill(usable, true);  //@top
                                    for (int bottom = top; bottom < R; bottom++) {  //@bottom
                                        int run = 0;  //@bottom
                                        for (int c = 0; c < C; c++) {  //@and
                                            usable[c] = usable[c] && land[bottom][c] == '1';  //@and
                                            run = usable[c] ? run + 1 : 0;  //@run
                                            best = Math.max(best, run * (bottom - top + 1));  //@run
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
                            int largestClearPlot(vector<vector<char>>& land) {
                                int R = land.size(), C = land[0].size();  //@init
                                int best = 0;  //@init
                                vector<char> usable(C);  //@init
                                for (int top = 0; top < R; top++) {  //@top
                                    fill(usable.begin(), usable.end(), 1);  //@top
                                    for (int bottom = top; bottom < R; bottom++) {  //@bottom
                                        int run = 0;  //@bottom
                                        for (int c = 0; c < C; c++) {  //@and
                                            usable[c] = usable[c] && land[bottom][c] == '1';  //@and
                                            run = usable[c] ? run + 1 : 0;  //@run
                                            best = max(best, run * (bottom - top + 1));  //@run
                                        }
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int largestClearPlot(char** land, int landSize, int* landColSize) {
                            int R = landSize, C = landColSize[0];  //@init
                            int best = 0;  //@init
                            bool* usable = malloc(C * sizeof(bool));  //@init
                            for (int top = 0; top < R; top++) {  //@top
                                for (int c = 0; c < C; c++) usable[c] = true;  //@top
                                for (int bottom = top; bottom < R; bottom++) {  //@bottom
                                    int run = 0;  //@bottom
                                    for (int c = 0; c < C; c++) {  //@and
                                        usable[c] = usable[c] && land[bottom][c] == '1';  //@and
                                        run = usable[c] ? run + 1 : 0;  //@run
                                        if (run * (bottom - top + 1) > best) best = run * (bottom - top + 1);  //@run
                                    }
                                }
                            }
                            free(usable);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Grid size, the best area, and a per-column flag.", {"cpp": "`vector<char>` instead of `vector<bool>`, which packs bits and is slower to index."}), ("top", "A new top row: every column starts usable."), ("bottom", "Grow the band one row down."), ("and", "A column stays usable only if the new row is clear there too."), ("run", "The current run of usable columns ending at `c` gives a clear plot of `run × band height`."), ("ret", "The largest clear area.")],
                complexity=["**Time O(R²C):** each (top, bottom) band costs one pass over the columns, about 6 × 10⁷ steps for 500 × 500. **Space O(C).**"],
                limits=["Fine in a compiled language at this size, but still quadratic in the rows. A band from `top` to `bottom` is just 'columns whose clear streak above `bottom` is at least the band height', so tracking the streak heights per row and solving a histogram removes the `top` loop entirely."],
                slow=True,
            ),
            approach(
                "One histogram per row",
                "best",
                "O(R·C)",
                "O(C)",
                idea=["Keep `h[c]`: the number of consecutive clear cells in column `c` ending at the current row. For each row, update `h` (clear → +1, rock → 0) and run the one-pass largest-rectangle stack over `h`, with a height-0 sentinel at the end. The best rectangle over all rows is the answer."],
                walk=w3,
                build=["`h` has `C + 1` entries; the last stays 0 as a sentinel.", "For each row: update `h`.", "Stack pass: pop while the top is at least as tall as `h[i]`; width = `i − newTop − 1` (or `i` if the stack is empty); update the best.", "Return the best."],
                code={
                    "python": """
                        class Solution:
                            def largestClearPlot(self, land: List[List[str]]) -> int:
                                C = len(land[0])  #@init
                                h = [0] * (C + 1)  #@init
                                best = 0  #@init
                                for row in land:  #@heights
                                    for c in range(C):  #@heights
                                        h[c] = h[c] + 1 if row[c] == "1" else 0  #@heights
                                    stack = []  #@hist
                                    for i in range(C + 1):  #@hist
                                        while stack and h[stack[-1]] >= h[i]:  #@pop
                                            height = h[stack.pop()]  #@pop
                                            width = i - stack[-1] - 1 if stack else i  #@pop
                                            best = max(best, height * width)  #@pop
                                        stack.append(i)  #@hist
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int largestClearPlot(char[][] land) {
                                int C = land[0].length;  //@init
                                int[] h = new int[C + 1], stack = new int[C + 1];  //@init
                                int best = 0;  //@init
                                for (char[] row : land) {  //@heights
                                    for (int c = 0; c < C; c++) h[c] = row[c] == '1' ? h[c] + 1 : 0;  //@heights
                                    int top = 0;  //@hist
                                    for (int i = 0; i <= C; i++) {  //@hist
                                        while (top > 0 && h[stack[top - 1]] >= h[i]) {  //@pop
                                            int height = h[stack[--top]];  //@pop
                                            int width = top > 0 ? i - stack[top - 1] - 1 : i;  //@pop
                                            best = Math.max(best, height * width);  //@pop
                                        }
                                        stack[top++] = i;  //@hist
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int largestClearPlot(vector<vector<char>>& land) {
                                int C = land[0].size();  //@init
                                vector<int> h(C + 1, 0), stack;  //@init
                                int best = 0;  //@init
                                for (auto& row : land) {  //@heights
                                    for (int c = 0; c < C; c++) h[c] = row[c] == '1' ? h[c] + 1 : 0;  //@heights
                                    stack.clear();  //@hist
                                    for (int i = 0; i <= C; i++) {  //@hist
                                        while (!stack.empty() && h[stack.back()] >= h[i]) {  //@pop
                                            int height = h[stack.back()];  //@pop
                                            stack.pop_back();  //@pop
                                            int width = stack.empty() ? i : i - stack.back() - 1;  //@pop
                                            best = max(best, height * width);  //@pop
                                        }
                                        stack.push_back(i);  //@hist
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int largestClearPlot(char** land, int landSize, int* landColSize) {
                            int C = landColSize[0];  //@init
                            int* h = calloc(C + 1, sizeof(int));  //@init
                            int* stack = malloc((C + 1) * sizeof(int));  //@init
                            int best = 0;  //@init
                            for (int r = 0; r < landSize; r++) {  //@heights
                                for (int c = 0; c < C; c++) h[c] = land[r][c] == '1' ? h[c] + 1 : 0;  //@heights
                                int top = 0;  //@hist
                                for (int i = 0; i <= C; i++) {  //@hist
                                    while (top > 0 && h[stack[top - 1]] >= h[i]) {  //@pop
                                        int height = h[stack[--top]];  //@pop
                                        int width = top > 0 ? i - stack[top - 1] - 1 : i;  //@pop
                                        if (height * width > best) best = height * width;  //@pop
                                    }
                                    stack[top++] = i;  //@hist
                                }
                            }
                            free(h);  //@ret
                            free(stack);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Column heights with one extra 0 at the end (the sentinel that flushes the stack), and the best area."),
                    ("heights", "Clear cell: the column's clear streak grows by one. Rock: the streak is broken."),
                    ("hist", "Largest rectangle in this row's histogram, with a stack of increasing heights."),
                    ("pop", "A column popped by a no-taller one has its right stopper at `i` and its left stopper at the new top (or the left edge, giving width `i`). That's the best plot with this bottom row whose height is that column's streak."),
                    ("ret", "The best plot over every possible bottom row."),
                ],
                complexity=["**Time O(R·C):** each row updates C heights and runs an O(C) stack pass. **Space O(C).**"],
            ),
        ],
        takeaways=[
            """
            - **Maximal rectangle in a 0/1 grid = one histogram per row**, solved with the largest-rectangle stack.
            - Column streak heights update in O(1) per cell from the previous row.
            - Reducing a 2-D problem to a 1-D one, row by row, is a pattern worth trying first.
            """
        ],
    )


@problem
def largest_pool():
    walls = [2, 0, 3, 1, 1, 4, 0, 2, 2, 0, 1]
    n = len(walls)
    lmax = [max(walls[:i + 1]) for i in range(n)]
    rmax = [max(walls[i:]) for i in range(n)]
    water = [min(lmax[i], rmax[i]) - walls[i] for i in range(n)]
    pools, run = [], 0
    for w in water + [0]:
        if w > 0:
            run += w
        elif run:
            pools.append(run)
            run = 0
    want = max(pools or [0])
    m = walls.index(max(walls))

    w1 = Steps("For each column, scan everything to its left and right for the tallest walls. The water level is the lower of the two.")
    best = run = 0
    for i in range(n):
        run = run + water[i] if water[i] > 0 else 0
        best = max(best, run)
        w1.step(f"Column {i}: tallest left {lmax[i]}, tallest right {rmax[i]}, level {min(lmax[i], rmax[i])}, water {water[i]}. {'Current pool: ' + str(run) if water[i] > 0 else 'Dry: any pool ends here.'}", Row(walls, st={i: "active"}, label="walls"), Row(water[:i + 1] + ["·"] * (n - i - 1), label="water"), Vars(best_pool=best))
    w1.step(f"Pools {pools}; the largest holds {want}.", result=want)

    w2 = Steps("Precompute the tallest wall up to each column from the left, and from the right, in two passes. Then water and pools take one more pass.")
    w2.step("Left-to-right running maximum.", Row(walls, label="walls"), Row(lmax, label="max from left"))
    w2.step("Right-to-left running maximum.", Row(walls, label="walls"), Row(lmax, label="max from left"), Row(rmax, label="max from right"))
    w2.step("Water = min of the two − wall.", Row(walls, label="walls"), Row(water, st={i: "found" for i in range(n) if water[i] > 0}, label="water"))
    w2.step(f"Runs of positive water are the pools: {pools}. Largest {want}.", Row(water, st={i: "found" for i in range(n) if water[i] > 0}, label="water"), result=want)

    w3 = Steps(f"The tallest wall (column {m}, height {walls[m]}) holds no water and splits the ground. Left of it, the right side is always high enough, so the level is just the running max from the left; right of it, the running max from the right.")
    best = run = level = 0
    for i in range(m):
        level = max(level, walls[i])
        w = level - walls[i]
        run = run + w if w > 0 else 0
        best = max(best, run)
        w3.step(f"Left part, column {i}: level {level}, water {w}. Pool so far {run}.", Row(walls, st={i: "active", m: "mark"}, label="walls"), Vars(level=level, pool=run, best=best))
    run = level = 0
    for i in range(n - 1, m, -1):
        level = max(level, walls[i])
        w = level - walls[i]
        run = run + w if w > 0 else 0
        best = max(best, run)
        w3.step(f"Right part (scanning back), column {i}: level {level}, water {w}. Pool so far {run}.", Row(walls, st={i: "active", m: "mark"}, label="walls"), Vars(level=level, pool=run, best=best))
    w3.step(f"Largest pool: {best}.", result=best)

    sol(
        "largest-pool",
        summary="""
            Water above a column rises to the lower of the tallest wall on its left and the tallest on its right. Pools
            are runs of columns that hold water. The tallest wall holds none and splits the problem: to its left the
            level is just the running maximum from the left, and to its right the running maximum from the right. Two
            scans add up each pool as they go: O(n) time, O(1) space.
        """,
        question=[
            """
            Columns of rock of width 1 are given by height. Rain fills every dip; water spills off both ends. Neighbouring
            water-holding columns form one pool, and a dry column separates pools. Return the largest pool's volume.

            - **A dry column splits pools**, even when water stands on both sides of it (possibly at different levels).
            - **Heights reach 10⁹ and there are up to 10⁵ columns**, so a pool can hold ~10¹⁴: the answer is a `long`.
            - **No water anywhere** (for example, heights only rise) → 0.
            """
        ],
        think=[
            f"""
            Walls `{walls}`. Columns 1, 3 and 4 hold 2 each, but column 2 (height 3) is dry and splits them: a pool of 2
            and a pool of 4. On the right, column 6 holds 2 and column 9 holds 1. Pools: `{pools}`, so the answer is
            **{want}**, not the total water {sum(water)}.
            """,
            fig(Row(walls, label="walls"), Row(water, st={i: "found" for i in range(n) if water[i] > 0}, label="water")),
            f"""
            How high does water stand over a column? It's held by the tallest wall to its left and the tallest to its right,
            and spills over the lower of the two: `level = min(maxLeft, maxRight)`, water = level − height.

            Now the observation that removes the extra arrays: take the tallest wall overall (column {m}). For any column
            left of it, the tallest wall on the right is at least as high as anything on the left, so the level is simply
            the running maximum from the left. Mirror that on the right side. The tallest wall itself is dry, so no pool
            crosses it, and each side can be scanned on its own.
            """,
        ],
        approaches=[
            approach(
                "Scan both sides for every column",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each column, find the tallest wall to its left (including itself) and to its right by scanning. Water = min of those − height. Walk the columns in order, adding water into the current pool and resetting at dry columns; keep the biggest pool."],
                walk=w1,
                build=["For each `i`, scan `0..i` for the max and `i..n−1` for the max.", "Water = min − `walls[i]`.", "Pool: add if water > 0, else reset to 0. Track the maximum."],
                code={
                    "python": """
                        class Solution:
                            def largestPool(self, walls: List[int]) -> int:
                                n = len(walls)  #@init
                                best = pool = 0  #@init
                                for i in range(n):  #@each
                                    left = max(walls[:i + 1])  #@scan
                                    right = max(walls[i:])  #@scan
                                    water = min(left, right) - walls[i]  #@water
                                    pool = pool + water if water > 0 else 0  #@pool
                                    best = max(best, pool)  #@pool
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long largestPool(int[] walls) {
                                int n = walls.length;  //@init
                                long best = 0, pool = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    int left = 0, right = 0;  //@scan
                                    for (int k = 0; k <= i; k++) left = Math.max(left, walls[k]);  //@scan
                                    for (int k = i; k < n; k++) right = Math.max(right, walls[k]);  //@scan
                                    int water = Math.min(left, right) - walls[i];  //@water
                                    pool = water > 0 ? pool + water : 0;  //@pool
                                    best = Math.max(best, pool);  //@pool
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long largestPool(vector<int>& walls) {
                                int n = walls.size();  //@init
                                long long best = 0, pool = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@each
                                    int left = *max_element(walls.begin(), walls.begin() + i + 1);  //@scan
                                    int right = *max_element(walls.begin() + i, walls.end());  //@scan
                                    int water = min(left, right) - walls[i];  //@water
                                    pool = water > 0 ? pool + water : 0;  //@pool
                                    best = max(best, pool);  //@pool
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long largestPool(int* walls, int wallsSize) {
                            int n = wallsSize;  //@init
                            long long best = 0, pool = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@each
                                int left = 0, right = 0;  //@scan
                                for (int k = 0; k <= i; k++) if (walls[k] > left) left = walls[k];  //@scan
                                for (int k = i; k < n; k++) if (walls[k] > right) right = walls[k];  //@scan
                                int water = (left < right ? left : right) - walls[i];  //@water
                                pool = water > 0 ? pool + water : 0;  //@pool
                                if (pool > best) best = pool;  //@pool
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Largest pool and the pool currently being filled (64-bit)."), ("each", "Columns in order, so neighbouring water adds up into one pool."), ("scan", "Tallest wall on each side, counting the column itself (so the level is never below the column)."), ("water", "Water spills over the lower side."), ("pool", "Water extends the current pool; a dry column ends it."), ("ret", "The largest pool.")],
                complexity=["**Time O(n²):** two scans per column. **Space O(1).**"],
                limits=["Every column rescans the whole array. Both maxima are running maxima, so they can be computed once for all columns."],
                slow=True,
            ),
            approach(
                "Running maxima from both ends",
                "better",
                "O(n)",
                "O(n)",
                idea=["Precompute `maxLeft[i]` (tallest in `0..i`) in one pass and `maxRight[i]` (tallest in `i..n−1`) in a backwards pass. Then a third pass computes each column's water and adds up the pools."],
                walk=w2,
                build=["Fill `maxLeft` left to right.", "Fill `maxRight` right to left.", "Pass over the columns: water = min − height; grow or reset the pool; track the best."],
                code={
                    "python": """
                        class Solution:
                            def largestPool(self, walls: List[int]) -> int:
                                n = len(walls)  #@init
                                max_left, max_right = [0] * n, [0] * n  #@init
                                for i in range(n):  #@left
                                    max_left[i] = max(walls[i], max_left[i - 1] if i else 0)  #@left
                                for i in range(n - 1, -1, -1):  #@right
                                    max_right[i] = max(walls[i], max_right[i + 1] if i < n - 1 else 0)  #@right
                                best = pool = 0  #@pool
                                for i in range(n):  #@pool
                                    water = min(max_left[i], max_right[i]) - walls[i]  #@water
                                    pool = pool + water if water > 0 else 0  #@pool
                                    best = max(best, pool)  #@pool
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long largestPool(int[] walls) {
                                int n = walls.length;  //@init
                                int[] maxLeft = new int[n], maxRight = new int[n];  //@init
                                for (int i = 0; i < n; i++) maxLeft[i] = Math.max(walls[i], i > 0 ? maxLeft[i - 1] : 0);  //@left
                                for (int i = n - 1; i >= 0; i--) maxRight[i] = Math.max(walls[i], i < n - 1 ? maxRight[i + 1] : 0);  //@right
                                long best = 0, pool = 0;  //@pool
                                for (int i = 0; i < n; i++) {  //@pool
                                    int water = Math.min(maxLeft[i], maxRight[i]) - walls[i];  //@water
                                    pool = water > 0 ? pool + water : 0;  //@pool
                                    best = Math.max(best, pool);  //@pool
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long largestPool(vector<int>& walls) {
                                int n = walls.size();  //@init
                                vector<int> maxLeft(n), maxRight(n);  //@init
                                for (int i = 0; i < n; i++) maxLeft[i] = max(walls[i], i > 0 ? maxLeft[i - 1] : 0);  //@left
                                for (int i = n - 1; i >= 0; i--) maxRight[i] = max(walls[i], i < n - 1 ? maxRight[i + 1] : 0);  //@right
                                long long best = 0, pool = 0;  //@pool
                                for (int i = 0; i < n; i++) {  //@pool
                                    int water = min(maxLeft[i], maxRight[i]) - walls[i];  //@water
                                    pool = water > 0 ? pool + water : 0;  //@pool
                                    best = max(best, pool);  //@pool
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long largestPool(int* walls, int wallsSize) {
                            int n = wallsSize;  //@init
                            int* maxLeft = malloc(n * sizeof(int));  //@init
                            int* maxRight = malloc(n * sizeof(int));  //@init
                            for (int i = 0; i < n; i++) maxLeft[i] = i > 0 && maxLeft[i - 1] > walls[i] ? maxLeft[i - 1] : walls[i];  //@left
                            for (int i = n - 1; i >= 0; i--) maxRight[i] = i < n - 1 && maxRight[i + 1] > walls[i] ? maxRight[i + 1] : walls[i];  //@right
                            long long best = 0, pool = 0;  //@pool
                            for (int i = 0; i < n; i++) {  //@pool
                                int water = (maxLeft[i] < maxRight[i] ? maxLeft[i] : maxRight[i]) - walls[i];  //@water
                                pool = water > 0 ? pool + water : 0;  //@pool
                                if (pool > best) best = pool;  //@pool
                            }
                            free(maxLeft);  //@ret
                            free(maxRight);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Two arrays of running maxima."), ("left", "Tallest wall from the left end up to and including `i`."), ("right", "Tallest wall from the right end back to and including `i`."), ("pool", "Columns in order, growing the current pool or resetting it at a dry column."), ("water", "Level = the lower of the two maxima."), ("ret", "The largest pool.")],
                complexity=["**Time O(n):** three passes. **Space O(n)** for the two arrays."],
                limits=["Linear, but two extra arrays of n integers. Splitting at the tallest wall makes one of the two maxima unnecessary on each side, so a single running variable does the job."],
            ),
            approach(
                "Split at the tallest wall",
                "best",
                "O(n)",
                "O(1)",
                idea=["Find the tallest column `m`. Scan `0..m−1` left to right with a running max as the water level, adding up pools. Scan `n−1` down to `m+1` with a running max from the right, the same way. Column `m` is dry, so no pool is cut in two."],
                walk=w3,
                build=["Find `m`, the index of the tallest wall.", "Left scan: `level = max(level, walls[i])`, water = level − height, grow or reset the pool, track the best.", "Reset the pool and level; scan from the right end down to `m + 1`.", "Return the best."],
                code={
                    "python": """
                        class Solution:
                            def largestPool(self, walls: List[int]) -> int:
                                n = len(walls)  #@init
                                m = walls.index(max(walls))  #@peak
                                best = 0  #@init
                                for side in (range(m), range(n - 1, m, -1)):  #@sides
                                    level = pool = 0  #@sides
                                    for i in side:  #@scan
                                        level = max(level, walls[i])  #@scan
                                        water = level - walls[i]  #@scan
                                        pool = pool + water if water > 0 else 0  #@pool
                                        best = max(best, pool)  #@pool
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long largestPool(int[] walls) {
                                int n = walls.length, m = 0;  //@init
                                for (int i = 1; i < n; i++) if (walls[i] > walls[m]) m = i;  //@peak
                                long best = 0, pool = 0;  //@init
                                int level = 0;  //@sides
                                for (int i = 0; i < m; i++) {  //@scan
                                    level = Math.max(level, walls[i]);  //@scan
                                    int water = level - walls[i];  //@scan
                                    pool = water > 0 ? pool + water : 0;  //@pool
                                    best = Math.max(best, pool);  //@pool
                                }
                                level = 0;  //@sides
                                pool = 0;  //@sides
                                for (int i = n - 1; i > m; i--) {  //@scan
                                    level = Math.max(level, walls[i]);  //@scan
                                    int water = level - walls[i];  //@scan
                                    pool = water > 0 ? pool + water : 0;  //@pool
                                    best = Math.max(best, pool);  //@pool
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long largestPool(vector<int>& walls) {
                                int n = walls.size();  //@init
                                int m = max_element(walls.begin(), walls.end()) - walls.begin();  //@peak
                                long long best = 0, pool = 0;  //@init
                                int level = 0;  //@sides
                                for (int i = 0; i < m; i++) {  //@scan
                                    level = max(level, walls[i]);  //@scan
                                    int water = level - walls[i];  //@scan
                                    pool = water > 0 ? pool + water : 0;  //@pool
                                    best = max(best, pool);  //@pool
                                }
                                level = 0;  //@sides
                                pool = 0;  //@sides
                                for (int i = n - 1; i > m; i--) {  //@scan
                                    level = max(level, walls[i]);  //@scan
                                    int water = level - walls[i];  //@scan
                                    pool = water > 0 ? pool + water : 0;  //@pool
                                    best = max(best, pool);  //@pool
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long largestPool(int* walls, int wallsSize) {
                            int n = wallsSize, m = 0;  //@init
                            for (int i = 1; i < n; i++) if (walls[i] > walls[m]) m = i;  //@peak
                            long long best = 0, pool = 0;  //@init
                            int level = 0;  //@sides
                            for (int i = 0; i < m; i++) {  //@scan
                                if (walls[i] > level) level = walls[i];  //@scan
                                int water = level - walls[i];  //@scan
                                pool = water > 0 ? pool + water : 0;  //@pool
                                if (pool > best) best = pool;  //@pool
                            }
                            level = 0;  //@sides
                            pool = 0;  //@sides
                            for (int i = n - 1; i > m; i--) {  //@scan
                                if (walls[i] > level) level = walls[i];  //@scan
                                int water = level - walls[i];  //@scan
                                pool = water > 0 ? pool + water : 0;  //@pool
                                if (pool > best) best = pool;  //@pool
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Size, best pool (64-bit) and the pool in progress."),
                    ("peak", "The tallest wall (the first one, if several tie). It can't hold water, so it separates the two sides."),
                    ("sides", "Each side starts with level 0 and no pool.", {"python": "The left side is scanned left to right, the right side right to left, each towards the peak."}),
                    ("scan", "Scanning towards the peak, the wall on the far side (the peak) is at least as tall as anything seen, so the water level is just the running maximum from the near end."),
                    ("pool", "Water extends the current pool; a dry column ends it. Scanning the right side backwards doesn't matter: a pool's volume is the same in either direction."),
                    ("ret", "The largest pool on either side."),
                ],
                complexity=["**Time O(n):** one pass to find the peak, one scan per side. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Trapped water at a column = `min(maxLeft, maxRight) − height`.
            - The global maximum splits the array: on each side only one running maximum matters, so no extra arrays.
            - The water can also be filled layer by layer with a stack of decreasing walls (each pop fills one horizontal
              layer between two walls); that's useful when you need the water while scanning in a single direction.
            """
        ],
    )
