"""Stacks & Queues: stack simulation."""
from fractions import Fraction

from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def comet_collisions():
    comets = [5, 10, -5, 8, -12, 3, -3, -1]

    def survive(cs):
        st = []
        for c in cs:
            alive = True
            while alive and c < 0 and st and st[-1] > 0:
                if st[-1] < -c:
                    st.pop()
                elif st[-1] == -c:
                    st.pop()
                    alive = False
                else:
                    alive = False
            if alive:
                st.append(c)
        return st

    want = survive(comets)
    arrow = lambda v: f"{v}→" if v > 0 else f"←{-v}"  # noqa: E731

    w1 = Steps("Find the first neighbouring pair that faces each other (→ then ←), resolve that one collision, and start scanning again.")
    a = list(comets)
    w1.step("Start. Positive comets fly right (→), negative ones fly left (←).", Row([arrow(v) for v in a]))
    while True:
        i = next((k for k in range(len(a) - 1) if a[k] > 0 and a[k + 1] < 0), None)
        if i is None:
            break
        x, y = a[i], -a[i + 1]
        if x > y:
            what, b = f"{x} beats {y}", a[:i + 1] + a[i + 2:]
        elif x < y:
            what, b = f"{y} beats {x}", a[:i] + a[i + 1:]
        else:
            what, b = f"both size {x}: both break", a[:i] + a[i + 2:]
        w1.step(f"First facing pair at positions {i},{i + 1}: {what}. Rescan from the start.", Row([arrow(v) for v in a], st={i: "mark", i + 1: "mark"}))
        a = b
    w1.step("No pair faces each other any more: these survive.", Row([arrow(v) for v in a] or ["·"]), result=str(a))

    w2 = Steps("Survivors so far sit on a stack. Only a left-mover can hit anything, and the first thing it meets is the stack's top.")
    st = []
    for idx, c in enumerate(comets):
        if c > 0 or not st or st[-1] < 0:
            st.append(c)
            why = "moves right: it can't hit anything to its left" if c > 0 else ("nothing to its left" if len(st) == 1 else "the top also moves left; they never meet")
            w2.step(f"{arrow(c)}: {why}. Push.", Row([arrow(v) for v in comets], st={idx: "active"}), Row([arrow(v) for v in st], st={len(st) - 1: "new"}, label="survivors"))
            continue
        alive = True
        while alive and st and st[-1] > 0:
            top = st[-1]
            if top < -c:
                st.pop()
                w2.step(f"{arrow(c)} meets {arrow(top)}: {-c} > {top}, the top breaks. Pop and keep going.", Row([arrow(v) for v in comets], st={idx: "active"}), Row([arrow(v) for v in st] or ["·"], label="survivors"))
            elif top == -c:
                st.pop()
                alive = False
                w2.step(f"{arrow(c)} meets {arrow(top)}: same size, both break.", Row([arrow(v) for v in comets], st={idx: "mark"}), Row([arrow(v) for v in st] or ["·"], label="survivors"))
            else:
                alive = False
                w2.step(f"{arrow(c)} meets {arrow(top)}: {top} > {-c}, the incoming comet breaks.", Row([arrow(v) for v in comets], st={idx: "mark"}), Row([arrow(v) for v in st], label="survivors"))
        if alive:
            st.append(c)
            w2.step(f"{arrow(c)} cleared everything moving right; nothing left to hit. Push.", Row([arrow(v) for v in comets], st={idx: "active"}), Row([arrow(v) for v in st], st={len(st) - 1: "new"}, label="survivors"))
    w2.step(f"The stack, bottom to top, is the answer: {st}.", Row([arrow(v) for v in st]), result=str(st))

    sol(
        "comet-collisions",
        summary="""
            Only a left-moving comet can crash, and the first thing it meets is the nearest survivor to its left, if that
            one moves right. Keep survivors on a stack: a left-mover pops smaller right-movers off the top, stops at a bigger
            one (and breaks), or ties (both go). O(n): every comet is pushed and popped at most once.
        """,
        question=[
            """
            Comets are listed in order of position. The sign is the direction (positive → right, negative → left), the
            absolute value is the size. All fly at the same speed. When two meet, the smaller breaks; equal sizes both
            break. Return the survivors, still in position order.

            - **Only a → followed (somewhere to its right) by a ← can meet.** Two comets moving the same way keep their gap
              forever, and ← … → move apart.
            - **One comet can win many collisions:** a big ← sweeps up several smaller → in a row.
            - **Up to 10⁵ comets.**
            """
        ],
        think=[
            f"""
            Take `{comets}`. The `−5` meets the `10` first and breaks. The `−12` meets `8`, then `10`, then `5`, winning
            each time, so it survives and flies off to the left. `3` and `−3` destroy each other. `−1` has only `−12` to its
            left, which flies the same way. Survivors: `{want}`.
            """,
            fig(Row([arrow(v) for v in comets], label="before"), Row([arrow(v) for v in want], label="after")),
            """
            Look at it from a ← comet's point of view. Everything to its left has already settled among itself: it's some
            ←s (flying away) followed by some →s (waiting to meet it). The nearest one is the first it will hit. If it wins,
            the next nearest is next. That's always the **most recent survivor**, the top of a stack. A → comet just joins
            the stack: nothing to its left can hit it, and whatever comes from the right will deal with it later.
            """,
        ],
        approaches=[
            approach(
                "Resolve one collision at a time",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Collisions only ever happen between neighbours facing each other (→ immediately followed by ←). Find the first such pair, remove the loser (or both), and scan again. When a full scan finds none, everything left survives."],
                walk=w1,
                build=["Copy the comets into a list.", "Loop: find the first index with `a[i] > 0 and a[i+1] < 0`; if none, stop.", "Remove the smaller one (both if equal) and repeat."],
                code={
                    "python": """
                        class Solution:
                            def afterCollisions(self, comets: List[int]) -> List[int]:
                                a = list(comets)  #@copy
                                i = 0  #@scan
                                while i < len(a) - 1:  #@scan
                                    if a[i] > 0 and a[i + 1] < 0:  #@pair
                                        if a[i] > -a[i + 1]:  #@resolve
                                            del a[i + 1]  #@resolve
                                        elif a[i] < -a[i + 1]:  #@resolve
                                            del a[i]  #@resolve
                                        else:  #@resolve
                                            del a[i:i + 2]  #@resolve
                                        i = 0  #@restart
                                    else:  #@scan
                                        i += 1  #@scan
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] afterCollisions(int[] comets) {
                                List<Integer> a = new ArrayList<>();  //@copy
                                for (int c : comets) a.add(c);  //@copy
                                int i = 0;  //@scan
                                while (i < a.size() - 1) {  //@scan
                                    int x = a.get(i), y = a.get(i + 1);  //@pair
                                    if (x > 0 && y < 0) {  //@pair
                                        if (x > -y) a.remove(i + 1);  //@resolve
                                        else if (x < -y) a.remove(i);  //@resolve
                                        else { a.remove(i + 1); a.remove(i); }  //@resolve
                                        i = 0;  //@restart
                                    } else i++;  //@scan
                                }
                                int[] out = new int[a.size()];  //@ret
                                for (int k = 0; k < out.length; k++) out[k] = a.get(k);  //@ret
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> afterCollisions(vector<int>& comets) {
                                vector<int> a = comets;  //@copy
                                size_t i = 0;  //@scan
                                while (i + 1 < a.size()) {  //@scan
                                    if (a[i] > 0 && a[i + 1] < 0) {  //@pair
                                        if (a[i] > -a[i + 1]) a.erase(a.begin() + i + 1);  //@resolve
                                        else if (a[i] < -a[i + 1]) a.erase(a.begin() + i);  //@resolve
                                        else a.erase(a.begin() + i, a.begin() + i + 2);  //@resolve
                                        i = 0;  //@restart
                                    } else i++;  //@scan
                                }
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static void removeAt(int* a, int* n, int i, int count) {  //@resolve
                            for (int k = i; k + count < *n; k++) a[k] = a[k + count];  //@resolve
                            *n -= count;  //@resolve
                        }  //@resolve

                        int* afterCollisions(int* comets, int cometsSize, int* returnSize) {
                            int* a = malloc(cometsSize * sizeof(int));  //@copy
                            memcpy(a, comets, cometsSize * sizeof(int));  //@copy
                            int n = cometsSize, i = 0;  //@scan
                            while (i < n - 1) {  //@scan
                                if (a[i] > 0 && a[i + 1] < 0) {  //@pair
                                    if (a[i] > -a[i + 1]) removeAt(a, &n, i + 1, 1);  //@resolve
                                    else if (a[i] < -a[i + 1]) removeAt(a, &n, i, 1);  //@resolve
                                    else removeAt(a, &n, i, 2);  //@resolve
                                    i = 0;  //@restart
                                } else i++;  //@scan
                            }
                            *returnSize = n;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("copy", "Work on a copy we can delete from."), ("scan", "Walk left to right looking for a collision."), ("pair", "Neighbours facing each other: the left one flies right, the right one flies left."), ("resolve", "The smaller breaks; equal sizes both break.", {"c": "`removeAt` shifts the tail left over the removed comets."}), ("restart", "Removing comets can create a new facing pair further left, so scan from the start again."), ("ret", "No facing neighbours remain: these are the survivors.")],
                complexity=["**Time O(n²):** up to n collisions, and each costs a rescan plus a deletion that shifts the list. **Space O(n)** for the copy."],
                limits=["Each collision restarts the scan and shifts the array, so 10⁵ comets can take ~10¹⁰ steps. But a collision only ever involves the newest survivor to the left, so nothing needs rescanning: a stack keeps exactly the comets still in play."],
                slow=True,
            ),
            approach(
                "Stack of survivors",
                "best",
                "O(n)",
                "O(n)",
                idea=["Go left to right with a stack of survivors so far. A → comet (or a ← with nothing to hit) is pushed. A ← comet of size `s` fights the top while the top is →: a smaller top is popped and the fight continues; an equal top is popped and `s` breaks too; a bigger top survives and `s` breaks. If `s` clears every → it meets, push it."],
                walk=w2,
                build=["An empty stack.", "For each comet, set `alive = true`.", "While alive, the comet moves left, and the top moves right: compare sizes and pop/kill as described.", "If still alive, push it.", "The stack, bottom to top, is the answer."],
                code={
                    "python": """
                        class Solution:
                            def afterCollisions(self, comets: List[int]) -> List[int]:
                                stack = []  #@init
                                for c in comets:  #@loop
                                    alive = True  #@loop
                                    while alive and c < 0 and stack and stack[-1] > 0:  #@fight
                                        if stack[-1] < -c:  #@smaller
                                            stack.pop()  #@smaller
                                        elif stack[-1] == -c:  #@equal
                                            stack.pop()  #@equal
                                            alive = False  #@equal
                                        else:  #@bigger
                                            alive = False  #@bigger
                                    if alive:  #@push
                                        stack.append(c)  #@push
                                return stack  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] afterCollisions(int[] comets) {
                                int[] stack = new int[comets.length];  //@init
                                int top = 0;  //@init
                                for (int c : comets) {  //@loop
                                    boolean alive = true;  //@loop
                                    while (alive && c < 0 && top > 0 && stack[top - 1] > 0) {  //@fight
                                        if (stack[top - 1] < -c) top--;  //@smaller
                                        else if (stack[top - 1] == -c) { top--; alive = false; }  //@equal
                                        else alive = false;  //@bigger
                                    }
                                    if (alive) stack[top++] = c;  //@push
                                }
                                return Arrays.copyOf(stack, top);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> afterCollisions(vector<int>& comets) {
                                vector<int> stack;  //@init
                                for (int c : comets) {  //@loop
                                    bool alive = true;  //@loop
                                    while (alive && c < 0 && !stack.empty() && stack.back() > 0) {  //@fight
                                        if (stack.back() < -c) stack.pop_back();  //@smaller
                                        else if (stack.back() == -c) { stack.pop_back(); alive = false; }  //@equal
                                        else alive = false;  //@bigger
                                    }
                                    if (alive) stack.push_back(c);  //@push
                                }
                                return stack;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* afterCollisions(int* comets, int cometsSize, int* returnSize) {
                            int* stack = malloc(cometsSize * sizeof(int));  //@init
                            int top = 0;  //@init
                            for (int i = 0; i < cometsSize; i++) {  //@loop
                                int c = comets[i];  //@loop
                                bool alive = true;  //@loop
                                while (alive && c < 0 && top > 0 && stack[top - 1] > 0) {  //@fight
                                    if (stack[top - 1] < -c) top--;  //@smaller
                                    else if (stack[top - 1] == -c) { top--; alive = false; }  //@equal
                                    else alive = false;  //@bigger
                                }
                                if (alive) stack[top++] = c;  //@push
                            }
                            *returnSize = top;  //@ret
                            return stack;  //@ret
                        }
                    """,
                },
                lines=[("init", "Survivors so far, in position order.", {"java": "An array with a `top` counter is the stack.", "c": "An array with a `top` counter is the stack."}), ("loop", "Each comet enters alive."), ("fight", "A fight happens only when the incoming comet flies left and the nearest survivor flies right."), ("smaller", "The top is smaller: it breaks, and the incoming comet goes on to meet the next one."), ("equal", "Equal sizes: both break."), ("bigger", "The top is bigger: the incoming comet breaks, and the top stays."), ("push", "Still alive (it flies right, or it flies left with nothing left to hit): it's a survivor for now."), ("ret", "The stack, bottom to top, is in position order.")],
                complexity=["**Time O(n):** each comet is pushed at most once and popped at most once, so the inner loop runs O(n) times in total. **Space O(n)** for the stack."],
            ),
        ],
        takeaways=[
            """
            - When each new item only interacts with **the most recent survivors**, keep the survivors on a stack.
            - Amortised O(n): the inner `while` can run many times for one item, but every pop removes something for good.
            - Spell out which pairs can interact at all (here only → … ←) before simulating.
            """
        ],
    )


@problem
def convoys_to_the_depot():
    depot, position, speed = 12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]
    t = [Fraction(depot - p, s) for p, s in zip(position, speed)]
    order = sorted(range(len(position)), key=lambda i: -position[i])

    def count():
        c, slow = 0, Fraction(0)
        for i in order:
            if t[i] > slow:
                c, slow = c + 1, t[i]
        return c

    want = count()

    w1 = Steps("For every truck, check every truck ahead of it. It leads its own convoy only if every truck ahead would reach the depot strictly sooner.")
    labels = [f"@{p}" for p in position]
    for i in range(len(position)):
        ahead = [j for j in range(len(position)) if position[j] > position[i]]
        blocker = next((j for j in ahead if t[j] >= t[i]), None)
        if blocker is None:
            msg = f"Truck at mile {position[i]} arrives at {t[i]} h alone; every truck ahead arrives sooner{'' if ahead else ' (there are none)'}. It leads a convoy."
            st = {i: "found"}
        else:
            msg = f"Truck at mile {position[i]} (alone: {t[i]} h) is held up by the truck at mile {position[blocker]} ({t[blocker]} h). It joins a convoy."
            st = {i: "active", blocker: "mark"}
        w1.step(msg, Row(labels, st=st, label="trucks"), Row([str(x) for x in t], st=st, label="hours alone"))
    w1.step(f"{want} trucks lead: {want} convoys.", result=want)

    w2 = Steps("Sort by position, nearest to the depot first. Keep the arrival time of the convoy just ahead; a truck that would arrive later starts a new convoy.")
    slow, c = Fraction(0), 0
    sorted_labels = [f"@{position[i]}" for i in order]
    w2.step("Sorted nearest-first, with each truck's arrival time if it drove alone.", Row(sorted_labels, label="trucks"), Row([str(t[i]) for i in order], label="hours alone"), Vars(convoys=0))
    for k, i in enumerate(order):
        if t[i] > slow:
            c += 1
            msg = f"Mile {position[i]}: {t[i]} h > {slow} h, so it never catches the convoy ahead. New convoy; the time to beat becomes {t[i]} h."
            slow = t[i]
            s = "found"
        else:
            msg = f"Mile {position[i]}: {t[i]} h ≤ {slow} h, so it catches the convoy ahead{' exactly at the depot' if t[i] == slow else ''} and joins it."
            s = "active"
        w2.step(msg, Row(sorted_labels, st={k: s}, label="trucks"), Row([str(t[j]) for j in order], st={k: s}, label="hours alone"), Vars(convoy_ahead_arrives=f"{slow} h", convoys=c))
    w2.step(f"{c} convoys.", result=c)

    sol(
        "convoys-to-the-depot",
        summary="""
            A truck can only be slowed by trucks ahead of it, and a whole convoy arrives when its front truck does. So sort
            trucks nearest-to-depot first and remember the arrival time of the convoy just ahead: a truck that would arrive
            later than it can never catch up and starts a new convoy; otherwise it joins. Compare times by cross-multiplying,
            in 64-bit, so they stay exact. O(n log n).
        """,
        question=[
            """
            Trucks on a one-lane road drive toward the depot. Each has a start mile and a speed. A faster truck that catches
            a slower one ahead can't pass, so they continue together at the slower speed as a convoy. Catching up exactly at
            the depot still counts. Return the number of convoys that arrive.

            - **Positions are distinct**, but times can tie: a tie means "caught up exactly at the depot" and counts as
              one convoy.
            - **Times are fractions** `(depot − position) / speed`. Distances and speeds go up to 10⁶, so cross-products
              reach 10¹²: they need 64-bit integers.
            - **Up to 10⁵ trucks.**
            """
        ],
        think=[
            f"""
            Depot at mile {depot}; trucks at miles `{position}` with speeds `{speed}`. Alone, they'd arrive after
            `{[str(x) for x in t]}` hours.
            """,
            table(["mile", "speed", "hours alone"], *[(position[i], speed[i], t[i]) for i in order]),
            f"""
            Read from the depot backwards. The truck at mile 10 is in front, arriving at hour 1. The truck at mile 8 also
            needs 1 hour alone, so it reaches the front truck exactly at the depot: one convoy. The truck at mile 5 needs 7
            hours, far behind, so it's a new convoy front. The truck at mile 3 would need 3 hours, but the truck at mile 5
            is in its way and arrives at hour 7: it gets stuck behind. The truck at mile 0 needs 12 hours, later than 7: a
            new convoy. Total: **{want}**.

            The key fact: a truck joins a convoy exactly when **some truck ahead of it would arrive no sooner**. A convoy's
            arrival time is its slowest-so-far front truck's time, so walking nearest-first we only need the latest arrival
            time seen so far.
            """,
        ],
        approaches=[
            approach(
                "Compare with every truck ahead",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["Truck `i` leads a convoy exactly when every truck ahead of it (bigger position) would arrive strictly earlier than it would alone. If any truck ahead arrives at the same time or later, `i` catches up with it (or with whatever is holding it up) and joins. Count the leaders with a double loop."],
                walk=w1,
                build=["For each truck `i`, compute its distance to the depot.", "Check every truck `j` with `position[j] > position[i]`: does it arrive no earlier? Compare `d_j / s_j ≥ d_i / s_i` as `d_j · s_i ≥ d_i · s_j`.", "If none does, count `i`."],
                code={
                    "python": """
                        class Solution:
                            def convoys(self, depot: int, position: List[int], speed: List[int]) -> int:
                                count = 0  #@init
                                for i in range(len(position)):  #@outer
                                    di = depot - position[i]  #@outer
                                    leads = True  #@outer
                                    for j in range(len(position)):  #@inner
                                        dj = depot - position[j]  #@inner
                                        if position[j] > position[i] and dj * speed[i] >= di * speed[j]:  #@cmp
                                            leads = False  #@cmp
                                            break  #@cmp
                                    if leads:  #@count
                                        count += 1  #@count
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int convoys(int depot, int[] position, int[] speed) {
                                int count = 0;  //@init
                                for (int i = 0; i < position.length; i++) {  //@outer
                                    long di = depot - position[i];  //@outer
                                    boolean leads = true;  //@outer
                                    for (int j = 0; j < position.length && leads; j++) {  //@inner
                                        long dj = depot - position[j];  //@inner
                                        if (position[j] > position[i] && dj * speed[i] >= di * speed[j]) leads = false;  //@cmp
                                    }
                                    if (leads) count++;  //@count
                                }
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int convoys(int depot, vector<int>& position, vector<int>& speed) {
                                int count = 0;  //@init
                                for (size_t i = 0; i < position.size(); i++) {  //@outer
                                    long long di = depot - position[i];  //@outer
                                    bool leads = true;  //@outer
                                    for (size_t j = 0; j < position.size() && leads; j++) {  //@inner
                                        long long dj = depot - position[j];  //@inner
                                        if (position[j] > position[i] && dj * speed[i] >= di * speed[j]) leads = false;  //@cmp
                                    }
                                    if (leads) count++;  //@count
                                }
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int convoys(int depot, int* position, int positionSize, int* speed, int speedSize) {
                            int count = 0;  //@init
                            for (int i = 0; i < positionSize; i++) {  //@outer
                                long long di = depot - position[i];  //@outer
                                bool leads = true;  //@outer
                                for (int j = 0; j < positionSize && leads; j++) {  //@inner
                                    long long dj = depot - position[j];  //@inner
                                    if (position[j] > position[i] && dj * speed[i] >= di * speed[j]) leads = false;  //@cmp
                                }
                                if (leads) count++;  //@count
                            }
                            return count;  //@ret
                        }
                    """,
                },
                lines=[("init", "Number of trucks that lead a convoy."), ("outer", "Truck `i`, its distance to the depot, and an assumption that it leads."), ("inner", "Look at every other truck.", {"java": "Distances are `long` so the products below don't overflow.", "cpp": "Distances are `long long` so the products below don't overflow.", "c": "Distances are `long long` so the products below don't overflow."}), ("cmp", "A truck ahead that arrives no sooner (`d_j/s_j ≥ d_i/s_i`, cross-multiplied to stay exact) means `i` will be held up."), ("count", "No truck ahead is in the way: `i` leads its own convoy."), ("ret", "Leaders = convoys.")],
                complexity=["**Time O(n²)** pairs. **Space O(1).**"],
                limits=["10⁵ trucks means 10¹⁰ comparisons. Most of them are wasted: only the **latest** arrival time ahead matters, and sorting by position lets us carry that one number forward."],
                slow=True,
            ),
            approach(
                "Sort, then carry the latest arrival time",
                "best",
                "O(n log n)",
                "O(n)",
                idea=["Sort trucks by position, nearest to the depot first. Keep the arrival time of the convoy just ahead (start at 0). A truck whose own time is strictly later can't catch that convoy: it's a new convoy and its time becomes the one to beat. Otherwise it joins, and the time to beat doesn't change. Store the time as a fraction (distance, speed) and compare by cross-multiplying."],
                walk=w2,
                build=["Pair up (position, speed) and sort by position, descending.", "Time to beat = 0/1, convoys = 0.", "For each truck: if `dist · leadSpeed > leadDist · speed`, it's later: count it and make it the time to beat.", "Return the count."],
                code={
                    "python": """
                        class Solution:
                            def convoys(self, depot: int, position: List[int], speed: List[int]) -> int:
                                trucks = sorted(zip(position, speed), reverse=True)  #@sort
                                count = 0  #@init
                                lead_dist, lead_speed = 0, 1  #@init
                                for p, s in trucks:  #@loop
                                    dist = depot - p  #@loop
                                    if dist * lead_speed > lead_dist * s:  #@later
                                        count += 1  #@new
                                        lead_dist, lead_speed = dist, s  #@new
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int convoys(int depot, int[] position, int[] speed) {
                                int n = position.length;
                                long[] trucks = new long[n];  //@sort
                                for (int i = 0; i < n; i++) trucks[i] = (long) position[i] << 20 | speed[i];  //@sort
                                Arrays.sort(trucks);  //@sort
                                int count = 0;  //@init
                                long leadDist = 0, leadSpeed = 1;  //@init
                                for (int k = n - 1; k >= 0; k--) {  //@loop
                                    long dist = depot - (trucks[k] >> 20), s = trucks[k] & ((1 << 20) - 1);  //@loop
                                    if (dist * leadSpeed > leadDist * s) {  //@later
                                        count++;  //@new
                                        leadDist = dist;  //@new
                                        leadSpeed = s;  //@new
                                    }
                                }
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int convoys(int depot, vector<int>& position, vector<int>& speed) {
                                vector<pair<int, int>> trucks;  //@sort
                                for (size_t i = 0; i < position.size(); i++) trucks.push_back({position[i], speed[i]});  //@sort
                                sort(trucks.rbegin(), trucks.rend());  //@sort
                                int count = 0;  //@init
                                long long leadDist = 0, leadSpeed = 1;  //@init
                                for (auto [p, s] : trucks) {  //@loop
                                    long long dist = depot - p;  //@loop
                                    if (dist * leadSpeed > leadDist * s) {  //@later
                                        count++;  //@new
                                        leadDist = dist;  //@new
                                        leadSpeed = s;  //@new
                                    }
                                }
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int p, s; } Truck;

                        static int nearestFirst(const void* a, const void* b) {  //@sort
                            return ((const Truck*)b)->p - ((const Truck*)a)->p;  //@sort
                        }  //@sort

                        int convoys(int depot, int* position, int positionSize, int* speed, int speedSize) {
                            Truck* trucks = malloc(positionSize * sizeof(Truck));  //@sort
                            for (int i = 0; i < positionSize; i++) trucks[i] = (Truck){position[i], speed[i]};  //@sort
                            qsort(trucks, positionSize, sizeof(Truck), nearestFirst);  //@sort
                            int count = 0;  //@init
                            long long leadDist = 0, leadSpeed = 1;  //@init
                            for (int k = 0; k < positionSize; k++) {  //@loop
                                long long dist = depot - trucks[k].p;  //@loop
                                if (dist * leadSpeed > leadDist * trucks[k].s) {  //@later
                                    count++;  //@new
                                    leadDist = dist;  //@new
                                    leadSpeed = trucks[k].s;  //@new
                                }
                            }
                            free(trucks);  //@ret
                            return count;  //@ret
                        }
                    """,
                },
                lines=[
                    ("sort", "Trucks nearest to the depot first: each truck is only affected by those before it in this order.", {"java": "Each truck is packed into one `long` (position in the high bits, speed below 2²⁰), so a plain sort orders by position; we then walk from the end (nearest first).", "c": "Positions are distinct, so the comparator only needs positions; their difference fits in an `int`."}),
                    ("init", "No convoy ahead yet, which is like one that arrives at time 0 = 0/1."),
                    ("loop", "Each truck's distance to the depot."),
                    ("later", "`dist/s > leadDist/leadSpeed`, cross-multiplied (both denominators are positive). Strictly later means it never catches up; a tie means it catches up exactly at the depot and joins."),
                    ("new", "A new convoy, and its front truck's time is now the one any truck behind must beat."),
                    ("ret", "Number of convoys."),
                ],
                complexity=["**Time O(n log n)** for the sort; the scan is O(n). **Space O(n)** for the sorted copy."],
            ),
        ],
        takeaways=[
            """
            - "Can't overtake" problems: process from the front; each item only cares about the **binding constraint ahead**,
              which here is the latest arrival time so far.
            - Compare fractions by cross-multiplying, in 64-bit; floating point can make a catch-up-at-the-depot tie look
              like a near miss.
            - The stack version (push a time when it's later than the top) works too, but the stack only ever matters
              through its top, so one variable is enough.
            """
        ],
    )


@problem
def plate_stack_check():
    washed, served = [3, 1, 4, 2, 5], [1, 4, 2, 5, 3]
    bad = [4, 3, 5, 1, 2]

    def check(sv):
        st, j = [], 0
        for p in washed:
            st.append(p)
            while st and st[-1] == sv[j]:
                st.pop()
                j += 1
        return j == len(sv)

    assert check(served) and not check(bad)

    pos = {v: i for i, v in enumerate(washed)}
    w1 = Steps("Rule: when a plate is served, every plate washed before it and still unserved is in the stack below it, and those must come out newest-washed first.")
    ok = True
    for j, x in enumerate(served):
        below = [y for y in served[j + 1:] if pos[y] < pos[x]]
        dec = all(pos[below[k]] > pos[below[k + 1]] for k in range(len(below) - 1))
        st = {j: "active"}
        msg = f"Serve {x}. Plates washed before it and served later: {below or 'none'}."
        if below:
            msg += f" Their washing positions {[pos[y] for y in below]} {'decrease, so the order works.' if dec else 'do not decrease: impossible.'}"
        w1.step(msg, Row(served, st=st, label="served"), Row(washed, st={pos[x]: "active", **{pos[y]: "mark" for y in below}}, label="washed"))
        if not dec:
            ok = False
            break
    w1.step("Every plate passes the rule: it could happen.", result="true")

    def sim_walk(sv, w):
        st, j = [], 0
        for p in washed:
            st.append(p)
            w.step(f"Wash {p}: push it.", Row(sv, st={j: "active"}, label="served"), Row(list(st), st={len(st) - 1: "new"}, label="stack"))
            while st and st[-1] == sv[j]:
                st.pop()
                j += 1
                w.step(f"The top is {sv[j - 1]}, the next plate to serve: take it now.", Row(sv, st={**{k: "found" for k in range(j)}}, label="served"), Row(list(st) or ["·"], label="stack"))
        return j

    w2 = Steps("Replay with a real stack: push each washed plate, and whenever the top is the next plate to serve, serve it immediately.")
    j = sim_walk(served, w2)
    w2.step(f"All {j} plates were served in order: it could happen.", result="true")

    sol(
        "plate-stack-check",
        summary="""
            Replay the evening with a real stack. Push the washed plates in order; whenever the top is the next plate to
            serve, take it at once (waiting never helps: the plate can only get buried). It could happen exactly when every
            plate gets served. O(n).
        """,
        question=[
            """
            Plates are stacked in `washed` order, and at any moment a waiter can take the top plate. Given the order they
            were served, could that order have happened?

            - **Pushes follow `washed` exactly**, but pops can be interleaved anywhere.
            - **Every plate is pushed once and served once**, and all numbers are distinct.
            - **Up to 10⁵ plates.**
            """
        ],
        think=[
            f"""
            Washed `{washed}`, served `{served}`. Wash 3, wash 1, serve 1. Wash 4, serve 4. Wash 2, serve 2. Wash 5, serve
            5. Serve 3, which was waiting at the bottom all along. Yes.

            Now served `{bad}`. To serve 4 first, 3 and 1 must already be on the stack, 1 on top. Serve 4, then 3 is needed
            but 1 is on top of it, and 1 can't be served yet. No.
            """,
            fig(Row(washed, label="washed"), Row(served, label="served ✓"), Row(bad, label="served ✗")),
            """
            The choice at every moment is "serve the top now" or "wash the next plate". If the top is the plate that must go
            next, serving it now is always right: pushing more plates would only bury it. If the top is some other plate,
            serving is not allowed, so wash the next one. With no real choices left, a single replay decides the answer.
            """,
        ],
        approaches=[
            approach(
                "Check the reverse-order rule for every plate",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["When plate `x` is served, every plate washed before `x` and not yet served is on the stack below it, in washing order. They can only leave newest-washed first. So for each `x`, the later-served plates that were washed before `x` must appear in decreasing washing position. If every plate passes, the order is possible."],
                walk=w1,
                build=["Find each served plate's washing position (a linear search is fine here, since the check is quadratic anyway).", "For each `j`, scan `served[j+1:]`; among plates washed before `served[j]`, positions must keep decreasing.", "Any increase → false; otherwise true."],
                code={
                    "python": """
                        class Solution:
                            def couldHappen(self, washed: List[int], served: List[int]) -> bool:
                                n = len(washed)  #@pos
                                pos = [washed.index(x) for x in served]  #@pos
                                for j in range(n):  #@each
                                    last = pos[j]  #@each
                                    for k in range(j + 1, n):  #@later
                                        if pos[k] < pos[j]:  #@later
                                            if pos[k] > last:  #@bad
                                                return False  #@bad
                                            last = pos[k]  #@later
                                return True  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean couldHappen(int[] washed, int[] served) {
                                int n = washed.length;  //@pos
                                int[] pos = new int[n];  //@pos
                                for (int j = 0; j < n; j++) for (int i = 0; i < n; i++) if (washed[i] == served[j]) pos[j] = i;  //@pos
                                for (int j = 0; j < n; j++) {  //@each
                                    int last = pos[j];  //@each
                                    for (int k = j + 1; k < n; k++) {  //@later
                                        if (pos[k] < pos[j]) {  //@later
                                            if (pos[k] > last) return false;  //@bad
                                            last = pos[k];  //@later
                                        }
                                    }
                                }
                                return true;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool couldHappen(vector<int>& washed, vector<int>& served) {
                                int n = washed.size();  //@pos
                                vector<int> pos(n);  //@pos
                                for (int j = 0; j < n; j++) pos[j] = find(washed.begin(), washed.end(), served[j]) - washed.begin();  //@pos
                                for (int j = 0; j < n; j++) {  //@each
                                    int last = pos[j];  //@each
                                    for (int k = j + 1; k < n; k++) {  //@later
                                        if (pos[k] < pos[j]) {  //@later
                                            if (pos[k] > last) return false;  //@bad
                                            last = pos[k];  //@later
                                        }
                                    }
                                }
                                return true;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool couldHappen(int* washed, int washedSize, int* served, int servedSize) {
                            int n = washedSize;  //@pos
                            int* pos = malloc(n * sizeof(int));  //@pos
                            for (int j = 0; j < n; j++) for (int i = 0; i < n; i++) if (washed[i] == served[j]) pos[j] = i;  //@pos
                            bool ok = true;  //@each
                            for (int j = 0; j < n && ok; j++) {  //@each
                                int last = pos[j];  //@each
                                for (int k = j + 1; k < n && ok; k++) {  //@later
                                    if (pos[k] < pos[j]) {  //@later
                                        if (pos[k] > last) ok = false;  //@bad
                                        last = pos[k];  //@later
                                    }
                                }
                            }
                            free(pos);  //@ret
                            return ok;  //@ret
                        }
                    """,
                },
                lines=[("pos", "Translate each served plate into its washing position (when it was pushed)."), ("each", "Take the plate served at step `j`; `last` tracks the most recent position seen below it."), ("later", "Plates served later but washed earlier were under `served[j]` when it left. Walk them in serving order."), ("bad", "Their positions must decrease (newest-washed leaves first). An increase means a plate had to come out from under another one."), ("ret", "Every plate passed: the order is possible.")],
                complexity=["**Time O(n²)** for the position lookups and the nested check. **Space O(n)** for positions."],
                limits=["Correct, but it re-derives the stack's contents from scratch for every plate. Simply replaying the stack answers the same question in one pass."],
                slow=True,
            ),
            approach(
                "Replay with a stack",
                "best",
                "O(n)",
                "O(n)",
                idea=["Push the washed plates in order. After each push, while the top is `served[j]`, pop it and advance `j`. At the end, the order could happen exactly when `j == n` (equivalently, the stack is empty)."],
                walk=w2,
                build=["An empty stack and `j = 0`.", "For each washed plate: push it, then serve greedily while the top matches `served[j]`.", "Return whether `j` reached `n`."],
                code={
                    "python": """
                        class Solution:
                            def couldHappen(self, washed: List[int], served: List[int]) -> bool:
                                stack = []  #@init
                                j = 0  #@init
                                for plate in washed:  #@push
                                    stack.append(plate)  #@push
                                    while stack and stack[-1] == served[j]:  #@serve
                                        stack.pop()  #@serve
                                        j += 1  #@serve
                                return j == len(served)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean couldHappen(int[] washed, int[] served) {
                                int[] stack = new int[washed.length];  //@init
                                int top = 0, j = 0;  //@init
                                for (int plate : washed) {  //@push
                                    stack[top++] = plate;  //@push
                                    while (top > 0 && stack[top - 1] == served[j]) {  //@serve
                                        top--;  //@serve
                                        j++;  //@serve
                                    }
                                }
                                return j == served.length;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool couldHappen(vector<int>& washed, vector<int>& served) {
                                vector<int> stack;  //@init
                                size_t j = 0;  //@init
                                for (int plate : washed) {  //@push
                                    stack.push_back(plate);  //@push
                                    while (!stack.empty() && stack.back() == served[j]) {  //@serve
                                        stack.pop_back();  //@serve
                                        j++;  //@serve
                                    }
                                }
                                return j == served.size();  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool couldHappen(int* washed, int washedSize, int* served, int servedSize) {
                            int* stack = malloc(washedSize * sizeof(int));  //@init
                            int top = 0, j = 0;  //@init
                            for (int i = 0; i < washedSize; i++) {  //@push
                                stack[top++] = washed[i];  //@push
                                while (top > 0 && stack[top - 1] == served[j]) {  //@serve
                                    top--;  //@serve
                                    j++;  //@serve
                                }
                            }
                            free(stack);  //@ret
                            return j == servedSize;  //@ret
                        }
                    """,
                },
                lines=[("init", "The plate stack and `j`, the next plate that must be served."), ("push", "Wash the next plate onto the stack."), ("serve", "If the top is the plate that must go next, serve it now; waiting would only bury it. Repeat, since the plate below might be next too. `j` can't run past the end: once all plates are served the stack is empty."), ("ret", "Possible exactly when every plate got served.")],
                complexity=["**Time O(n):** each plate is pushed once and popped at most once. **Space O(n)** for the stack."],
            ),
        ],
        takeaways=[
            """
            - To ask "could this sequence of stack operations happen?", **replay it**, choosing greedily when only one choice
              can be right.
            - The forced choice here: pop as soon as the top is needed. A plate that's needed and buried is a dead end.
            - The same check works for any push order and pop order, and it tells you which plate breaks the order, too.
            """
        ],
    )
