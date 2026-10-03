"""Stacks & Queues: queue simulation."""
from collections import deque

from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def ticket_line():
    wants, k = [2, 5, 3, 1, 4], 2
    n = len(wants)
    need = wants[k]
    take = [min(w, need) if i <= k else min(w, need - 1) for i, w in enumerate(wants)]
    want = sum(take)

    w1 = Steps("Simulate second by second: the front person buys one ticket, then leaves or goes to the back.")
    line = deque((w, i) for i, w in enumerate(wants))
    t = 0
    while True:
        w, i = line.popleft()
        t += 1
        if w == 1:
            note = f"Second {t}: person {i} buys their last ticket and leaves."
        else:
            line.append((w - 1, i))
            note = f"Second {t}: person {i} buys one ({w - 1} still wanted), goes to the back."
        w1.step(note, Row([f"P{j}:{x}" for x, j in line] or ["·"], label="line (person:still wants)"), Vars(seconds=t))
        if w == 1 and i == k:
            break
    w1.step(f"Person {k} is done after {t} seconds.", result=t)

    w2 = Steps(f"Count each person's purchases until person {k} finishes. Person {k} needs {need} rounds; people in front of them get up to {need} turns, people behind up to {need - 1}.")
    acc = 0
    for i in range(n):
        acc += take[i]
        cap = need if i <= k else need - 1
        w2.step(f"Person {i} wants {wants[i]}, {'in front of (or is)' if i <= k else 'behind'} person {k}: buys min({wants[i]}, {cap}) = {take[i]}.", Row(wants, st={i: "active", k: "found"} if i != k else {k: "found"}, label="wants"), Row(take[:i + 1] + ["·"] * (n - i - 1), label="bought"), Vars(seconds=acc))
    w2.step(f"Total: {want} seconds.", result=want)

    sol(
        "ticket-line",
        summary=f"""
            Each second sells exactly one ticket, so the answer is how many tickets are sold by the moment person `k`
            buys their last one. That takes `wants[k]` rounds. Everyone at or in front of `k` gets up to `wants[k]` turns;
            everyone behind gets one fewer, since the line stops mid-round. Sum `min(wants[i], cap)`: O(n).
        """,
        question=[
            """
            One ticket is sold per second to the person at the front, who then leaves (if done) or goes to the back. Return
            the second at which person `k` buys their last ticket.

            - **The line cycles**, so a person's turns come once per round, in the original order (people only leave).
            - **Up to 10⁵ people wanting up to 10⁵ tickets**: up to 10¹⁰ seconds, so simulating is too slow and the answer
              needs 64 bits.
            """
        ],
        think=[
            f"""
            Line `{wants}`, `k = {k}` (wants {need}). Person {k} gets one ticket per round, so they finish in round {need}.
            In each round, everyone still in line buys one, in the original order. During rounds 1..{need}, a person at or
            before position {k} buys at most {need} (fewer if they want fewer). A person after position {k} only gets
            {need - 1} full rounds, because round {need} stops the moment person {k} is served.
            """,
            table(["person", "wants", "turns before k is done", "bought"], *[(i, wants[i], need if i <= k else need - 1, take[i]) for i in range(n)]),
            f"""
            Every second sells one ticket, so the answer is the total bought: **{want}**.
            """,
        ],
        approaches=[
            approach(
                "Simulate the queue",
                "brute",
                "O(total tickets)",
                "O(n)",
                idea=["Put `(wants, index)` pairs in a queue. Each second: pop the front, add a second, and either finish them or push them back with one fewer. Stop when person `k` buys their last ticket."],
                walk=w1,
                build=["Queue of `(remaining, index)`.", "Loop: pop, `t += 1`.", "If remaining was 1: if it's `k`, return `t`; else drop. Otherwise push back with one fewer."],
                code={
                    "python": """
                        from collections import deque

                        class Solution:
                            def secondsToFinish(self, wants: List[int], k: int) -> int:
                                line = deque((w, i) for i, w in enumerate(wants))  #@init
                                t = 0  #@init
                                while True:  #@loop
                                    w, i = line.popleft()  #@loop
                                    t += 1  #@loop
                                    if w == 1:  #@done
                                        if i == k:  #@done
                                            return t  #@done
                                    else:  #@back
                                        line.append((w - 1, i))  #@back
                    """,
                    "java": """
                        class Solution {
                            public long secondsToFinish(int[] wants, int k) {
                                int n = wants.length;  //@init
                                int[] left = wants.clone();  //@init
                                ArrayDeque<Integer> line = new ArrayDeque<>();  //@init
                                for (int i = 0; i < n; i++) line.add(i);  //@init
                                long t = 0;  //@init
                                while (true) {  //@loop
                                    int i = line.poll();  //@loop
                                    t++;  //@loop
                                    left[i]--;  //@loop
                                    if (left[i] == 0) {  //@done
                                        if (i == k) return t;  //@done
                                    } else line.add(i);  //@back
                                }
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long secondsToFinish(vector<int>& wants, int k) {
                                vector<int> left = wants;  //@init
                                deque<int> line;  //@init
                                for (int i = 0; i < (int) wants.size(); i++) line.push_back(i);  //@init
                                long long t = 0;  //@init
                                while (true) {  //@loop
                                    int i = line.front();  //@loop
                                    line.pop_front();  //@loop
                                    t++;  //@loop
                                    if (--left[i] == 0) {  //@done
                                        if (i == k) return t;  //@done
                                    } else line.push_back(i);  //@back
                                }
                            }
                        };
                    """,
                    "c": """
                        long long secondsToFinish(int* wants, int wantsSize, int k) {
                            int n = wantsSize;  //@init
                            int* left = malloc(n * sizeof(int));  //@init
                            int* line = malloc(n * sizeof(int));  //@init
                            for (int i = 0; i < n; i++) { left[i] = wants[i]; line[i] = i; }  //@init
                            int head = 0, size = n;  //@init
                            long long t = 0;  //@init
                            while (1) {  //@loop
                                int i = line[head];  //@loop
                                head = (head + 1) % n;  //@loop
                                size--;  //@loop
                                t++;  //@loop
                                if (--left[i] == 0) {  //@done
                                    if (i == k) break;  //@done
                                } else {  //@back
                                    line[(head + size) % n] = i;  //@back
                                    size++;  //@back
                                }
                            }
                            free(left);  //@ret
                            free(line);  //@ret
                            return t;  //@ret
                        }
                    """,
                },
                lines=[("init", "The line, in order, with each person's remaining tickets.", {"c": "A circular buffer of `n` slots: the line never holds more than `n` people."}), ("loop", "One second: the front person buys a ticket."), ("done", "Their last ticket: if it's person `k`, that's the answer; otherwise they just leave."), ("back", "Still wanting more: back of the line."), ("ret", "Clean up and return the time.")],
                complexity=["**Time O(total tickets sold):** up to 10¹⁰ seconds. **Space O(n).**"],
                limits=["Simulating one second at a time is hopeless for large orders. But the order of turns is completely regular (rounds in the original order), so each person's purchases can be counted directly."],
                slow=True,
            ),
            approach(
                "Count each person's purchases",
                "best",
                "O(n)",
                "O(1)",
                idea=["Let `need = wants[k]`. Person `i ≤ k` buys `min(wants[i], need)` tickets before `k` is done; person `i > k` buys `min(wants[i], need − 1)`. The answer is the sum."],
                walk=w2,
                build=["`need = wants[k]`.", "Sum `min(wants[i], need)` for `i ≤ k` and `min(wants[i], need − 1)` for `i > k`, in 64 bits."],
                code={
                    "python": """
                        class Solution:
                            def secondsToFinish(self, wants: List[int], k: int) -> int:
                                need = wants[k]  #@need
                                total = 0  #@sum
                                for i, w in enumerate(wants):  #@sum
                                    total += min(w, need if i <= k else need - 1)  #@cap
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long secondsToFinish(int[] wants, int k) {
                                int need = wants[k];  //@need
                                long total = 0;  //@sum
                                for (int i = 0; i < wants.length; i++)  //@sum
                                    total += Math.min(wants[i], i <= k ? need : need - 1);  //@cap
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long secondsToFinish(vector<int>& wants, int k) {
                                int need = wants[k];  //@need
                                long long total = 0;  //@sum
                                for (int i = 0; i < (int) wants.size(); i++)  //@sum
                                    total += min(wants[i], i <= k ? need : need - 1);  //@cap
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long secondsToFinish(int* wants, int wantsSize, int k) {
                            int need = wants[k];  //@need
                            long long total = 0;  //@sum
                            for (int i = 0; i < wantsSize; i++) {  //@sum
                                int cap = i <= k ? need : need - 1;  //@cap
                                total += wants[i] < cap ? wants[i] : cap;  //@cap
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("need", "Person `k` finishes in round `need`."), ("sum", "Tickets sold before person `k` is done = seconds elapsed (64-bit)."), ("cap", "People at or in front of `k` get a turn in each of the `need` rounds; people behind miss the last one. Nobody buys more than they want."), ("ret", "The total.")],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - When a simulation is perfectly regular (round-robin), **count instead of simulating**.
            - "One unit per second" turns a time question into a counting question.
            - Be careful about the partial last round: who comes before the target and who comes after.
            """
        ],
    )


@problem
def lunch_line():
    prefers, trays = [1, 1, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1]

    def simulate(record=None):
        q, top, misses = deque(prefers), 0, 0
        while q and misses < len(q):
            s = q.popleft()
            if s == trays[top]:
                top += 1
                misses = 0
                msg = f"Front student wants {s}, the top tray is {s}: takes it."
            else:
                q.append(s)
                misses += 1
                msg = f"Front student wants {s}, the top tray is {trays[top]}: back of the line ({misses} in a row)."
            if record:
                record.step(msg, Row(list(q) or ["·"], label="queue (front first)"), Row(trays[top:] or ["·"], label="trays (top first)"))
        return len(q)

    want = simulate()
    w1 = Steps("Simulate turn by turn. If every student left has looked at the top tray and passed, nobody wants it and lunch is over.")
    w1.step("Start.", Row(prefers, label="queue (front first)"), Row(trays, label="trays (top first)"))
    simulate(w1)
    w1.step(f"Everyone left passed on the top tray: {want} hungry.", result=want)
    assert 2 <= len(w1.steps) <= 40

    w2 = Steps("The queue can rotate freely, so only how many students want each kind matters. Go down the tray stack.")
    cnt = [prefers.count(0), prefers.count(1)]
    w2.step(f"Students wanting 0: {cnt[0]}, wanting 1: {cnt[1]}.", Row(trays, label="trays"), Vars(want_0=cnt[0], want_1=cnt[1]))
    for idx, t in enumerate(trays):
        if cnt[t] == 0:
            w2.step(f"Tray {idx} is {t}, but nobody left wants {t}. It blocks the stack for good.", Row(trays, st={idx: "mark"}), Vars(want_0=cnt[0], want_1=cnt[1]))
            break
        cnt[t] -= 1
        w2.step(f"Tray {idx} is {t}: someone wants it, and the line will rotate until they reach the front. They take it.", Row(trays, st={idx: "found"}), Vars(want_0=cnt[0], want_1=cnt[1]))
    w2.step(f"Hungry: {cnt[0]} + {cnt[1]} = {cnt[0] + cnt[1]}.", result=cnt[0] + cnt[1])

    sol(
        "lunch-line",
        summary="""
            Students who don't want the top tray just rotate to the back, so the queue's order never matters, only how
            many want each kind. Go down the tray stack: if anyone still wants this tray, one of them takes it; the first
            tray nobody wants blocks everything. The students left over are hungry. O(n).
        """,
        question=[
            """
            Students queue; trays are stacked. The front student takes the top tray if it's their kind, otherwise goes to the
            back. Stop when nobody in the queue wants the top tray. Return how many students go hungry.

            - **Trays can't be skipped**: the top tray must be taken before anyone sees the next one.
            - **There are exactly as many trays as students**, so if every tray gets taken, nobody is hungry.
            - **Up to 10⁵ students.**
            """
        ],
        think=[
            f"""
            Queue `{prefers}`, trays `{trays}` (top first). Three students want 0 and three want 1. The first four trays
            (0, 1, 0, 0) are taken, each by someone who eventually reaches the front. Then the top tray is 0, but nobody
            left wants 0: lunch stops with **{want}** hungry.
            """,
            fig(Row(prefers, label="queue"), Row(trays, label="trays (top first)")),
            """
            The rotation is the key: a student who doesn't want the top tray goes to the back, and the line keeps turning
            until someone who wants it reaches the front. So the top tray is taken **if and only if at least one waiting
            student wants its kind**; which student, and the queue's order, never matter. Two counters are enough.
            """,
        ],
        approaches=[
            approach(
                "Simulate the queue",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Run the canteen literally with a queue. Count consecutive students who passed on the current top tray; if that count reaches the queue's length, nobody wants it and the simulation stops."],
                walk=w1,
                build=["Queue of preferences, a pointer to the top tray, a 'passes in a row' counter.", "Match → pop, advance the tray, reset the counter. No match → rotate, count the pass.", "Stop when the counter equals the queue length (or the queue empties)."],
                code={
                    "python": """
                        from collections import deque

                        class Solution:
                            def hungryStudents(self, prefers: List[int], trays: List[int]) -> int:
                                q = deque(prefers)  #@init
                                top = passes = 0  #@init
                                while q and passes < len(q):  #@loop
                                    s = q.popleft()  #@loop
                                    if s == trays[top]:  #@take
                                        top += 1  #@take
                                        passes = 0  #@take
                                    else:  #@rotate
                                        q.append(s)  #@rotate
                                        passes += 1  #@rotate
                                return len(q)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int hungryStudents(int[] prefers, int[] trays) {
                                ArrayDeque<Integer> q = new ArrayDeque<>();  //@init
                                for (int p : prefers) q.add(p);  //@init
                                int top = 0, passes = 0;  //@init
                                while (!q.isEmpty() && passes < q.size()) {  //@loop
                                    int s = q.poll();  //@loop
                                    if (s == trays[top]) { top++; passes = 0; }  //@take
                                    else { q.add(s); passes++; }  //@rotate
                                }
                                return q.size();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int hungryStudents(vector<int>& prefers, vector<int>& trays) {
                                deque<int> q(prefers.begin(), prefers.end());  //@init
                                int top = 0, passes = 0;  //@init
                                while (!q.empty() && passes < (int) q.size()) {  //@loop
                                    int s = q.front();  //@loop
                                    q.pop_front();  //@loop
                                    if (s == trays[top]) { top++; passes = 0; }  //@take
                                    else { q.push_back(s); passes++; }  //@rotate
                                }
                                return q.size();  //@ret
                            }
                        };
                    """,
                    "c": """
                        int hungryStudents(int* prefers, int prefersSize, int* trays, int traysSize) {
                            int n = prefersSize;  //@init
                            int* q = malloc(n * sizeof(int));  //@init
                            for (int i = 0; i < n; i++) q[i] = prefers[i];  //@init
                            int head = 0, size = n, top = 0, passes = 0;  //@init
                            while (size > 0 && passes < size) {  //@loop
                                int s = q[head];  //@loop
                                head = (head + 1) % n;  //@loop
                                size--;  //@loop
                                if (s == trays[top]) { top++; passes = 0; }  //@take
                                else { q[(head + size) % n] = s; size++; passes++; }  //@rotate
                            }
                            free(q);  //@ret
                            return size;  //@ret
                        }
                    """,
                },
                lines=[("init", "The queue, the top tray's index, and how many students in a row have passed on it.", {"c": "A circular buffer of `n` slots holds the queue."}), ("loop", "Continue while someone might still want the top tray."), ("take", "A match: the student leaves with the tray, a new tray is on top, and the pass count restarts."), ("rotate", "No match: to the back of the line."), ("ret", "Everyone still queued goes hungry.")],
                complexity=["**Time O(n²)** in the worst case: each tray can take a full rotation of the queue to find its student. **Space O(n).**"],
                limits=["The rotations carry no information: they only bring a matching student to the front, if one exists. Counting students per kind answers 'does one exist?' in O(1)."],
                slow=True,
            ),
            approach(
                "Count preferences, walk the trays",
                "best",
                "O(n)",
                "O(1)",
                idea=["Count students wanting 0 and wanting 1. For each tray from the top: if its kind's count is 0, stop; otherwise decrement it. Return the sum of the counts."],
                walk=w2,
                build=["`want[0]`, `want[1]` = counts of each preference.", "For each tray: stop if `want[tray] == 0`, else `want[tray]--`.", "Return `want[0] + want[1]`."],
                code={
                    "python": """
                        class Solution:
                            def hungryStudents(self, prefers: List[int], trays: List[int]) -> int:
                                want = [prefers.count(0), prefers.count(1)]  #@count
                                for t in trays:  #@trays
                                    if want[t] == 0:  #@stuck
                                        break  #@stuck
                                    want[t] -= 1  #@take
                                return want[0] + want[1]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int hungryStudents(int[] prefers, int[] trays) {
                                int[] want = new int[2];  //@count
                                for (int p : prefers) want[p]++;  //@count
                                for (int t : trays) {  //@trays
                                    if (want[t] == 0) break;  //@stuck
                                    want[t]--;  //@take
                                }
                                return want[0] + want[1];  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int hungryStudents(vector<int>& prefers, vector<int>& trays) {
                                int want[2] = {0, 0};  //@count
                                for (int p : prefers) want[p]++;  //@count
                                for (int t : trays) {  //@trays
                                    if (want[t] == 0) break;  //@stuck
                                    want[t]--;  //@take
                                }
                                return want[0] + want[1];  //@ret
                            }
                        };
                    """,
                    "c": """
                        int hungryStudents(int* prefers, int prefersSize, int* trays, int traysSize) {
                            int want[2] = {0, 0};  //@count
                            for (int i = 0; i < prefersSize; i++) want[prefers[i]]++;  //@count
                            for (int i = 0; i < traysSize; i++) {  //@trays
                                if (want[trays[i]] == 0) break;  //@stuck
                                want[trays[i]]--;  //@take
                            }
                            return want[0] + want[1];  //@ret
                        }
                    """,
                },
                lines=[("count", "How many students want each kind; the order of the queue is irrelevant."), ("trays", "Trays from the top, in the only order they can be taken."), ("stuck", "Nobody wants this tray: it never leaves the top, so lunch is over."), ("take", "Someone wants it; the queue rotates until they get it."), ("ret", "Students who never got a tray.")],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - If a queue can rotate freely, its **order doesn't matter**, only its contents.
            - Look for the quantity a simulation really depends on (here, two counts) and track only that.
            - The stack of trays is the real constraint: its order is fixed.
            """
        ],
    )


@problem
def magic_card_reveal():
    cards = [5, 2, 9, 7, 1, 4]
    n = len(cards)
    spots = deque(range(n))
    out = [0] * n
    order = sorted(cards)
    for c in order:
        out[spots.popleft()] = c
        if spots:
            spots.append(spots.popleft())
    want = out

    deck = list(want)
    shown = []
    while deck:
        shown.append(deck.pop(0))
        if deck:
            deck.append(deck.pop(0))
    assert shown == order

    w1 = Steps("Undo the trick from the end. Take cards from largest to smallest; each step reverses one round: move the bottom card back to the top, then put the card back on top.")
    deck = []
    for c in reversed(order):
        moved = None
        if deck:
            moved = deck.pop()
            deck.insert(0, moved)
        deck.insert(0, c)
        w1.step(f"Put back {c}: " + (f"first move the bottom card {moved} to the top (undoing 'top to bottom'), " if moved is not None else "") + f"then place {c} on top.", Row(deck, st={0: "active"}, label="deck (top first)"))
    w1.step(f"Deck from top to bottom: {deck}.", result=str(deck))

    w2 = Steps("Run the trick on the empty positions 0..n−1 with a queue. The position revealed at each turn receives the next smallest card.")
    spots, res = deque(range(n)), ["·"] * n
    for c in order:
        p = spots.popleft()
        res[p] = c
        moved = None
        if spots:
            moved = spots.popleft()
            spots.append(moved)
        w2.step(f"Reveal position {p}: it gets {c}." + (f" Position {moved} goes to the bottom." if moved is not None else ""), Row(res, st={p: "found"}, label="deck positions"), Row(list(spots) or ["·"], label="queue of positions"))
    w2.step(f"Deck from top to bottom: {res}.", result=str(res))

    sol(
        "magic-card-reveal",
        summary="""
            The trick's order of revealing positions doesn't depend on the numbers at all. So run the trick on the
            positions `0..n−1` with a queue (reveal the front, move the next to the back) and hand out the sorted cards in
            that order: the k-th revealed position gets the k-th smallest card. O(n log n) for the sort.
        """,
        question=[
            """
            Repeatedly: reveal the top card, then move the next top card to the bottom. Arrange the deck so the cards come
            out in increasing order, and return it top to bottom.

            - **Cards are distinct**, so "increasing order" fixes exactly which card is revealed at each turn.
            - **The last card** is just revealed; there's nothing to move.
            - **Up to 10⁵ cards.**
            """
        ],
        think=[
            f"""
            Cards `{cards}`. The answer is `{want}`: running the trick on it reveals {', '.join(map(str, order))}.

            Notice the trick never looks at the numbers: it moves **positions** around in a fixed pattern. Number the deck
            positions 0 (top) to {n - 1}. Run the trick on the positions: the first position revealed must hold the smallest
            card, the second the next smallest, and so on.
            """,
            fig(Row(list(range(n)), label="positions"), Row(want, label="deck")),
            """
            "Reveal the front, move the next to the back" is exactly a queue. Alternatively, the trick can be **run in
            reverse**: starting from the largest card, put cards back on top, undoing the move each time.
            """,
        ],
        approaches=[
            approach(
                "Undo the trick with an array",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Go through the sorted cards from largest to smallest and rebuild the deck backwards. Undoing one round means: undo 'move the top card to the bottom' (take the bottom card back to the top), then undo 'reveal' (put the card back on top). With a plain array, each move to the front costs O(n)."],
                walk=w1,
                build=["Sort the cards.", "From the largest: if the deck isn't empty, move its last card to the front; then insert the card at the front.", "Return the deck."],
                code={
                    "python": """
                        class Solution:
                            def stackDeck(self, cards: List[int]) -> List[int]:
                                deck = []  #@init
                                for card in sorted(cards, reverse=True):  #@order
                                    if deck:  #@undo
                                        deck.insert(0, deck.pop())  #@undo
                                    deck.insert(0, card)  #@place
                                return deck  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] stackDeck(int[] cards) {
                                int n = cards.length;  //@init
                                int[] sorted = cards.clone();  //@order
                                Arrays.sort(sorted);  //@order
                                List<Integer> deck = new ArrayList<>();  //@init
                                for (int k = n - 1; k >= 0; k--) {  //@order
                                    if (!deck.isEmpty()) deck.add(0, deck.remove(deck.size() - 1));  //@undo
                                    deck.add(0, sorted[k]);  //@place
                                }
                                int[] out = new int[n];  //@ret
                                for (int i = 0; i < n; i++) out[i] = deck.get(i);  //@ret
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> stackDeck(vector<int>& cards) {
                                vector<int> sorted = cards;  //@order
                                sort(sorted.rbegin(), sorted.rend());  //@order
                                vector<int> deck;  //@init
                                for (int card : sorted) {  //@order
                                    if (!deck.empty()) {  //@undo
                                        int bottom = deck.back();  //@undo
                                        deck.pop_back();  //@undo
                                        deck.insert(deck.begin(), bottom);  //@undo
                                    }
                                    deck.insert(deck.begin(), card);  //@place
                                }
                                return deck;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int descending(const void* a, const void* b) {  //@order
                            int x = *(const int*) a, y = *(const int*) b;  //@order
                            return (y > x) - (y < x);  //@order
                        }  //@order

                        int* stackDeck(int* cards, int cardsSize, int* returnSize) {
                            int n = cardsSize, size = 0;  //@init
                            int* sorted = malloc(n * sizeof(int));  //@order
                            memcpy(sorted, cards, n * sizeof(int));  //@order
                            qsort(sorted, n, sizeof(int), descending);  //@order
                            int* deck = malloc(n * sizeof(int));  //@init
                            for (int k = 0; k < n; k++) {  //@order
                                if (size > 0) {  //@undo
                                    int bottom = deck[size - 1];  //@undo
                                    memmove(deck + 1, deck, (size - 1) * sizeof(int));  //@undo
                                    deck[0] = bottom;  //@undo
                                }
                                memmove(deck + 1, deck, size * sizeof(int));  //@place
                                deck[0] = sorted[k];  //@place
                                size++;  //@place
                            }
                            free(sorted);  //@ret
                            *returnSize = n;  //@ret
                            return deck;  //@ret
                        }
                    """,
                },
                lines=[("init", "The deck being rebuilt, top first."), ("order", "Cards from largest to smallest: the last card revealed is put back first.", {"c": "The comparator returns the sign without subtracting, so it can't overflow."}), ("undo", "The forward trick moved the top card to the bottom right after revealing; undo it by taking the bottom card back to the top."), ("place", "Undo the reveal: this card goes back on top.", {"c": "`memmove` shifts the deck down one slot to make room at the front."}), ("ret", "The deck, top to bottom.")],
                complexity=["**Time O(n²):** each insertion at the front shifts the whole array. **Space O(n).**"],
                limits=["Front insertions make it quadratic: ~10¹⁰ shifts for 10⁵ cards. A deque would fix that, and so does running the trick forwards on positions with a queue."],
                slow=True,
            ),
            approach(
                "Deal sorted cards into positions with a queue",
                "best",
                "O(n log n)",
                "O(n)",
                idea=["Queue the positions `0..n−1`. For each card in increasing order: pop the front position and put the card there; then, if positions remain, move the next front position to the back."],
                walk=w2,
                build=["Sort the cards.", "Queue of positions `0..n−1`.", "For each card: assign it to the popped front; rotate one position to the back.", "Return the filled deck."],
                code={
                    "python": """
                        from collections import deque

                        class Solution:
                            def stackDeck(self, cards: List[int]) -> List[int]:
                                n = len(cards)  #@init
                                spots = deque(range(n))  #@init
                                deck = [0] * n  #@init
                                for card in sorted(cards):  #@order
                                    deck[spots.popleft()] = card  #@reveal
                                    if spots:  #@move
                                        spots.append(spots.popleft())  #@move
                                return deck  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] stackDeck(int[] cards) {
                                int n = cards.length;  //@init
                                int[] spots = new int[2 * n], deck = new int[n];  //@init
                                int head = 0, tail = 0;  //@init
                                for (int i = 0; i < n; i++) spots[tail++] = i;  //@init
                                int[] sorted = cards.clone();  //@order
                                Arrays.sort(sorted);  //@order
                                for (int card : sorted) {  //@order
                                    deck[spots[head++]] = card;  //@reveal
                                    if (head < tail) spots[tail++] = spots[head++];  //@move
                                }
                                return deck;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> stackDeck(vector<int>& cards) {
                                int n = cards.size();  //@init
                                deque<int> spots;  //@init
                                for (int i = 0; i < n; i++) spots.push_back(i);  //@init
                                vector<int> deck(n), sorted = cards;  //@init
                                sort(sorted.begin(), sorted.end());  //@order
                                for (int card : sorted) {  //@order
                                    deck[spots.front()] = card;  //@reveal
                                    spots.pop_front();  //@reveal
                                    if (!spots.empty()) {  //@move
                                        spots.push_back(spots.front());  //@move
                                        spots.pop_front();  //@move
                                    }
                                }
                                return deck;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int ascending(const void* a, const void* b) {  //@order
                            int x = *(const int*) a, y = *(const int*) b;  //@order
                            return (x > y) - (x < y);  //@order
                        }  //@order

                        int* stackDeck(int* cards, int cardsSize, int* returnSize) {
                            int n = cardsSize;  //@init
                            int* spots = malloc(2 * n * sizeof(int));  //@init
                            int* deck = malloc(n * sizeof(int));  //@init
                            int* sorted = malloc(n * sizeof(int));  //@init
                            int head = 0, tail = 0;  //@init
                            for (int i = 0; i < n; i++) spots[tail++] = i;  //@init
                            memcpy(sorted, cards, n * sizeof(int));  //@order
                            qsort(sorted, n, sizeof(int), ascending);  //@order
                            for (int k = 0; k < n; k++) {  //@order
                                deck[spots[head++]] = sorted[k];  //@reveal
                                if (head < tail) spots[tail++] = spots[head++];  //@move
                            }
                            free(spots);  //@ret
                            free(sorted);  //@ret
                            *returnSize = n;  //@ret
                            return deck;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "A queue of deck positions, top (0) first, and the deck to fill.", {"java": "A plain array works as the queue: `n` positions start in it and at most `n − 1` are re-added, so `2n` slots never run out.", "c": "A plain array works as the queue: `n` positions start in it and at most `n − 1` are re-added, so `2n` slots never run out."}),
                    ("order", "Cards in the order they must be revealed: increasing."),
                    ("reveal", "The trick reveals whatever is at the front position now, so the next smallest card must sit there."),
                    ("move", "Then the next top card goes to the bottom: rotate one position. Skipped after the last card."),
                    ("ret", "The deck, top to bottom."),
                ],
                complexity=["**Time O(n log n)** for the sort; the dealing is O(n). **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - If a process moves **positions** in a fixed pattern regardless of values, simulate it on indices and then
              assign values.
            - Any shuffle can also be undone step by step in reverse; use a deque so front operations are O(1).
            - "Take from the front, put at the back" = queue.
            """
        ],
    )


@problem
def council_vote():
    council = "LOOLLO"
    n = len(council)

    def queues():
        larks = deque(i for i, c in enumerate(council) if c == "L")
        owls = deque(i for i, c in enumerate(council) if c == "O")
        while larks and owls:
            a, b = larks.popleft(), owls.popleft()
            if a < b:
                larks.append(a + n)
            else:
                owls.append(b + n)
        return "Larks" if larks else "Owls"

    want = queues()
    name = {"L": "Lark", "O": "Owl"}

    w1 = Steps("Replay the rounds. Each speaker silences the next opponent who would speak after them (wrapping into the next round).")
    banned = [False] * n
    alive = {"L": council.count("L"), "O": council.count("O")}
    done = False
    rnd = 0
    while not done:
        rnd += 1
        for i, c in enumerate(council):
            if banned[i]:
                continue
            other = "O" if c == "L" else "L"
            if alive[other] == 0:
                w1.step(f"Round {rnd}, member {i} ({name[c]}): no {name[other]}s can speak. Victory for the {name[c]}s.", Row(list(council), st={**{x: "mark" for x in range(n) if banned[x]}, i: "found"}), result=f"{name[c]}s")
                done = True
                break
            for d in range(1, n + 1):
                j = (i + d) % n
                if not banned[j] and council[j] == other:
                    banned[j] = True
                    alive[other] -= 1
                    break
            w1.step(f"Round {rnd}, member {i} ({name[c]}) silences member {j}, the next {name[other]} due to speak.", Row(list(council), st={**{x: "mark" for x in range(n) if banned[x]}, i: "active"}), Vars(larks=alive["L"], owls=alive["O"]))

    w2 = Steps("Two queues of speaking turns. The earlier of the two front members speaks first, silences the other front member, and rejoins its queue for the next round (turn + n).")
    larks = deque(i for i, c in enumerate(council) if c == "L")
    owls = deque(i for i, c in enumerate(council) if c == "O")
    w2.step("Turn numbers per party.", Row(list(larks), label="Larks"), Row(list(owls), label="Owls"))
    while larks and owls:
        a, b = larks.popleft(), owls.popleft()
        if a < b:
            larks.append(a + n)
            msg = f"Lark at turn {a} speaks before Owl at turn {b}: silences them, and speaks again at turn {a + n}."
        else:
            owls.append(b + n)
            msg = f"Owl at turn {b} speaks before Lark at turn {a}: silences them, and speaks again at turn {b + n}."
        w2.step(msg, Row(list(larks) or ["·"], label="Larks"), Row(list(owls) or ["·"], label="Owls"))
    w2.step(f"Only {want} remain.", result=want)

    sol(
        "council-vote",
        summary="""
            The best move is always to silence the next opponent due to speak: that removes the most immediate threat,
            and any other target is no better. With that rule, keep each party's speaking turns in a queue. The earlier
            front speaks, silences the other party's front, and rejoins at the back with its turn plus `n` (next round).
            The party whose queue survives wins. O(n).
        """,
        question=[
            """
            Members of two parties speak in a fixed order, round after round. On their turn, a member who hasn't been
            silenced either silences any member of the other party, or declares victory if only their own party can still
            speak. Both parties play optimally. Who wins?

            - **Silenced members are gone for good**, in this round and later ones.
            - **Rounds wrap around**: after the last member, the first surviving member speaks again.
            - **Up to 10⁵ members.**
            """
        ],
        think=[
            f"""
            Council `{council}`. Member 0 (Lark) silences member 1, the next Owl due to speak. Member 2 (Owl) silences
            member 3, the next Lark. Member 4 (Lark) silences member 5. Round two: member 0 silences member 2, and the
            Larks win. Winner: **{want}**.
            """,
            fig(Row(list(council), label="speaking order")),
            """
            Why silence the **next** opponent due to speak? An opponent who speaks soon is about to silence one of us;
            removing them now prevents that. Silencing an opponent further away instead leaves the nearer one free to act
            first. Any member of the other party who has already spoken this round will speak again only after the ones
            still to come, so the next one in speaking order (wrapping) is always the most urgent.

            With that rule fixed, it's pure bookkeeping: whose turn comes first? Give each member a turn number, keep each
            party's turns in a queue, and let survivors take turn `t + n` in the next round.
            """,
        ],
        approaches=[
            approach(
                "Replay rounds, scanning for the next opponent",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Loop over the members round after round. A member who isn't silenced checks whether the other party still has speakers (keep counts); if not, their party wins. Otherwise scan forward (wrapping) for the next unsilenced opponent and silence them."],
                walk=w1,
                build=["Counts of active Larks and Owls; a `silenced` flag per member.", "Repeat rounds; skip silenced members.", "If the other party's count is 0, return this party.", "Else scan forward from `i + 1` (mod n) for the next active opponent; silence them."],
                code={
                    "python": """
                        class Solution:
                            def councilWinner(self, council: str) -> str:
                                n = len(council)  #@init
                                silenced = [False] * n  #@init
                                active = {"L": council.count("L"), "O": council.count("O")}  #@init
                                while True:  #@rounds
                                    for i, c in enumerate(council):  #@rounds
                                        if silenced[i]:  #@rounds
                                            continue  #@rounds
                                        other = "O" if c == "L" else "L"  #@win
                                        if active[other] == 0:  #@win
                                            return "Larks" if c == "L" else "Owls"  #@win
                                        j = (i + 1) % n  #@scan
                                        while silenced[j] or council[j] != other:  #@scan
                                            j = (j + 1) % n  #@scan
                                        silenced[j] = True  #@ban
                                        active[other] -= 1  #@ban
                    """,
                    "java": """
                        class Solution {
                            public String councilWinner(String council) {
                                int n = council.length();  //@init
                                boolean[] silenced = new boolean[n];  //@init
                                int[] active = new int[2];  //@init
                                for (int i = 0; i < n; i++) active[council.charAt(i) == 'L' ? 0 : 1]++;  //@init
                                while (true) {  //@rounds
                                    for (int i = 0; i < n; i++) {  //@rounds
                                        if (silenced[i]) continue;  //@rounds
                                        char c = council.charAt(i);  //@win
                                        int me = c == 'L' ? 0 : 1, other = 1 - me;  //@win
                                        if (active[other] == 0) return me == 0 ? "Larks" : "Owls";  //@win
                                        int j = (i + 1) % n;  //@scan
                                        while (silenced[j] || council.charAt(j) == c) j = (j + 1) % n;  //@scan
                                        silenced[j] = true;  //@ban
                                        active[other]--;  //@ban
                                    }
                                }
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string councilWinner(string& council) {
                                int n = council.size();  //@init
                                vector<char> silenced(n, 0);  //@init
                                int active[2] = {0, 0};  //@init
                                for (char c : council) active[c == 'L' ? 0 : 1]++;  //@init
                                while (true) {  //@rounds
                                    for (int i = 0; i < n; i++) {  //@rounds
                                        if (silenced[i]) continue;  //@rounds
                                        int me = council[i] == 'L' ? 0 : 1, other = 1 - me;  //@win
                                        if (active[other] == 0) return me == 0 ? "Larks" : "Owls";  //@win
                                        int j = (i + 1) % n;  //@scan
                                        while (silenced[j] || council[j] == council[i]) j = (j + 1) % n;  //@scan
                                        silenced[j] = 1;  //@ban
                                        active[other]--;  //@ban
                                    }
                                }
                            }
                        };
                    """,
                    "c": """
                        static char* answer(const char* party) {  //@win
                            char* out = malloc(6);  //@win
                            strcpy(out, party);  //@win
                            return out;  //@win
                        }  //@win

                        char* councilWinner(char* council) {
                            int n = strlen(council);  //@init
                            bool* silenced = calloc(n, sizeof(bool));  //@init
                            int active[2] = {0, 0};  //@init
                            for (int i = 0; i < n; i++) active[council[i] == 'L' ? 0 : 1]++;  //@init
                            while (1) {  //@rounds
                                for (int i = 0; i < n; i++) {  //@rounds
                                    if (silenced[i]) continue;  //@rounds
                                    int me = council[i] == 'L' ? 0 : 1, other = 1 - me;  //@win
                                    if (active[other] == 0) { free(silenced); return answer(me == 0 ? "Larks" : "Owls"); }  //@win
                                    int j = (i + 1) % n;  //@scan
                                    while (silenced[j] || council[j] == council[i]) j = (j + 1) % n;  //@scan
                                    silenced[j] = true;  //@ban
                                    active[other]--;  //@ban
                                }
                            }
                        }
                    """,
                },
                lines=[("init", "Who's been silenced, and how many of each party can still speak."), ("rounds", "Round after round, in speaking order; silenced members are skipped."), ("win", "Nobody from the other party can speak: declare victory.", {"c": "A string answer must be `malloc`ed; `answer` copies the party name."}), ("scan", "Find the next opponent due to speak, wrapping into the next round. One exists, since the other party's count isn't 0."), ("ban", "Silence them.")],
                complexity=["**Time O(n²):** each silencing may scan past many members. **Space O(n).**"],
                limits=["The scans step over the same silenced members again and again. Keeping each party's upcoming turns in its own queue makes 'the next opponent' simply the front of the other queue."],
                slow=True,
            ),
            approach(
                "Two queues of turns",
                "best",
                "O(n)",
                "O(n)",
                idea=["Queue the indices of the Larks and of the Owls. While both are non-empty, pop both fronts; the smaller index speaks first and silences the other; the speaker rejoins its queue with index + n (its turn in the next round). When a queue empties, the other party wins."],
                walk=w2,
                build=["Two queues of turn numbers.", "Pop both fronts; the smaller turn wins the duel and is re-queued at turn + n.", "Return the party whose queue is non-empty."],
                code={
                    "python": """
                        from collections import deque

                        class Solution:
                            def councilWinner(self, council: str) -> str:
                                n = len(council)  #@init
                                larks = deque(i for i, c in enumerate(council) if c == "L")  #@init
                                owls = deque(i for i, c in enumerate(council) if c == "O")  #@init
                                while larks and owls:  #@duel
                                    a, b = larks.popleft(), owls.popleft()  #@duel
                                    if a < b:  #@speak
                                        larks.append(a + n)  #@speak
                                    else:  #@speak
                                        owls.append(b + n)  #@speak
                                return "Larks" if larks else "Owls"  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String councilWinner(String council) {
                                int n = council.length();  //@init
                                ArrayDeque<Integer> larks = new ArrayDeque<>(), owls = new ArrayDeque<>();  //@init
                                for (int i = 0; i < n; i++) (council.charAt(i) == 'L' ? larks : owls).add(i);  //@init
                                while (!larks.isEmpty() && !owls.isEmpty()) {  //@duel
                                    int a = larks.poll(), b = owls.poll();  //@duel
                                    if (a < b) larks.add(a + n);  //@speak
                                    else owls.add(b + n);  //@speak
                                }
                                return larks.isEmpty() ? "Owls" : "Larks";  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string councilWinner(string& council) {
                                int n = council.size();  //@init
                                queue<int> larks, owls;  //@init
                                for (int i = 0; i < n; i++) (council[i] == 'L' ? larks : owls).push(i);  //@init
                                while (!larks.empty() && !owls.empty()) {  //@duel
                                    int a = larks.front(), b = owls.front();  //@duel
                                    larks.pop();  //@duel
                                    owls.pop();  //@duel
                                    if (a < b) larks.push(a + n);  //@speak
                                    else owls.push(b + n);  //@speak
                                }
                                return larks.empty() ? "Owls" : "Larks";  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* councilWinner(char* council) {
                            int n = strlen(council);  //@init
                            int* larks = malloc(2 * n * sizeof(int));  //@init
                            int* owls = malloc(2 * n * sizeof(int));  //@init
                            int lh = 0, lt = 0, oh = 0, ot = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@init
                                if (council[i] == 'L') larks[lt++] = i;  //@init
                                else owls[ot++] = i;  //@init
                            }
                            while (lh < lt && oh < ot) {  //@duel
                                int a = larks[lh++], b = owls[oh++];  //@duel
                                if (a < b) larks[lt++] = a + n;  //@speak
                                else owls[ot++] = b + n;  //@speak
                            }
                            char* out = malloc(6);  //@ret
                            strcpy(out, lh < lt ? "Larks" : "Owls");  //@ret
                            free(larks);  //@ret
                            free(owls);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Each party's speaking turns, in order.", {"c": "Plain arrays as queues: every duel removes one member for good, so at most `n` re-entries happen and `2n` slots suffice."}),
                    ("duel", "The next speaker of each party."),
                    ("speak", "The earlier turn speaks first and silences the other party's next speaker (the optimal move). The speaker will speak again next round, at turn + n, after everyone still due this round."),
                    ("ret", "The party with members left declares victory."),
                ],
                complexity=["**Time O(n):** every duel silences one member, so there are fewer than `n` duels. **Space O(n).** Turn numbers stay small: everyone still standing after a round silenced someone during it, so each round at least halves the council. That means at most about log₂ n + 1 rounds, and turns stay below n · (log₂ n + 2), about 2 × 10⁶."],
            ),
        ],
        takeaways=[
            """
            - Prove the greedy move first (silence the next opponent due to act); then the simulation is simple.
            - **Round-robin with removals = queues with "turn + n"** to mark the next round.
            - Each step removes someone, which bounds the total work at O(n).
            """
        ],
    )
