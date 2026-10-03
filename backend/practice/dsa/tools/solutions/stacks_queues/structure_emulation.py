"""Stacks & Queues: structure emulation (design problems, so no C version)."""
from collections import deque

from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

DESIGN = ["python", "java", "cpp"]


@problem
def queue_from_two_stacks():
    calls = [("push", 1), ("push", 2), ("push", 3), ("pop",), ("push", 4), ("peek",), ("pop",), ("pop",), ("empty",)]

    w1 = Steps("One stack holds the queue with the front at the bottom. To reach the front, pour everything into a spare stack, use the top, then pour it all back.")
    main = []
    for c in calls:
        if c[0] == "push":
            main.append(c[1])
            w1.step(f"push({c[1]}): onto the top.", Row(main, label="stack (bottom → top)"))
        elif c[0] in ("pop", "peek"):
            spare = []
            while main:
                spare.append(main.pop())
            v = spare[-1]
            w1.step(f"{c[0]}(): pour all {len(spare)} items into the spare stack; the front ({v}) is now on top.", Row(main or ["·"], label="stack"), Row(spare, st={len(spare) - 1: "found"}, label="spare (bottom → top)"))
            if c[0] == "pop":
                spare.pop()
            while spare:
                main.append(spare.pop())
            w1.step(f"{'Remove it, then pour' if c[0] == 'pop' else 'Pour'} everything back. Returns {v}.", Row(main or ["·"], label="stack (bottom → top)"), Vars(returned=v))
        else:
            w1.step(f"empty(): {not main}.", Row(main or ["·"], label="stack"), Vars(returned=str(not main).lower()))
    w1.step("Every pop and peek moved the whole queue twice.", result="done")

    w2 = Steps("Two stacks: 'in' takes new items, 'out' serves the front. Only when 'out' runs dry, pour all of 'in' into it, which reverses the order so the oldest item lands on top.")
    inbox, outbox = [], []
    results = []
    for c in calls:
        if c[0] == "push":
            inbox.append(c[1])
            msg = f"push({c[1]}): onto 'in'."
        elif c[0] in ("pop", "peek"):
            poured = False
            if not outbox:
                while inbox:
                    outbox.append(inbox.pop())
                poured = True
            v = outbox[-1]
            if c[0] == "pop":
                outbox.pop()
            results.append(v)
            msg = (f"{c[0]}(): 'out' is empty, so pour 'in' into it (order reverses). " if poured else f"{c[0]}(): 'out' still has items; no pouring. ") + f"The front is {v}" + (", removed." if c[0] == "pop" else ".")
        else:
            v = not inbox and not outbox
            msg = f"empty(): both stacks empty? {str(v).lower()}."
        w2.step(msg, Row(inbox or ["·"], label="in (bottom → top)"), Row(outbox or ["·"], label="out (bottom → top)"))
    w2.step(f"pop/peek returned {results}, in first-in, first-out order.", result="done")

    sol(
        "queue-from-two-stacks",
        summary="""
            Use one stack for arrivals ('in') and one for departures ('out'). Pouring 'in' into 'out' reverses it, so the
            oldest item ends up on top of 'out'. Pour only when 'out' is empty: each item is moved at most once, so every
            operation is amortised O(1).
        """,
        question=[
            """
            Implement a queue (`push` to the back, `pop` / `peek` at the front, `empty`) using only stack operations: push,
            top, pop, size, is-empty.

            - **A stack gives back the newest item; a queue must give back the oldest.** The orders are opposite.
            - **`pop` and `peek` are only called on a non-empty queue.**
            - **Up to 10⁵ calls**, so each should be cheap, at least on average.
            """
        ],
        think=[
            """
            Push 1, 2, 3. A stack holds them with 3 on top, but the queue's front is 1, at the bottom. Popping everything
            onto a second stack **reverses** the order: now 1 is on top. That's the whole trick; the question is how often
            to pay for the reversal.
            """,
            fig(Row([1, 2, 3], label="in (bottom → top)"), Row([3, 2, 1], label="after pouring into out")),
            """
            Once items are in 'out', they're already in queue order (oldest on top), and newer arrivals can't be older than
            them. So leave them there. New arrivals go to 'in'. Only when 'out' is empty does the next-oldest item sit at
            the bottom of 'in'; pour then, and not before.
            """,
        ],
        approaches=[
            approach(
                "Pour back and forth on every read",
                "brute",
                "O(n) per pop/peek",
                "O(n)",
                idea=["Keep the queue in one stack (front at the bottom). For `pop`/`peek`, pour everything into a spare stack so the front is on top, read or remove it, then pour everything back."],
                walk=w1,
                build=["`push`: push onto the main stack.", "`pop`/`peek`: pour main → spare, take the top, pour spare → main.", "`empty`: is the main stack empty?"],
                code={
                    "python": """
                        class TwoStackQueue:
                            def __init__(self):
                                self.main = []  #@init
                                self.spare = []  #@init

                            def push(self, x: int) -> None:
                                self.main.append(x)  #@push

                            def _front(self, remove):  #@front
                                while self.main:  #@pour
                                    self.spare.append(self.main.pop())  #@pour
                                value = self.spare.pop() if remove else self.spare[-1]  #@front
                                while self.spare:  #@back
                                    self.main.append(self.spare.pop())  #@back
                                return value  #@front

                            def pop(self) -> int:
                                return self._front(True)  #@front

                            def peek(self) -> int:
                                return self._front(False)  #@front

                            def empty(self) -> bool:
                                return not self.main  #@empty
                    """,
                    "java": """
                        class TwoStackQueue {
                            private final ArrayDeque<Integer> main = new ArrayDeque<>(), spare = new ArrayDeque<>();  //@init

                            public TwoStackQueue() {
                            }

                            public void push(int x) {
                                main.push(x);  //@push
                            }

                            private int front(boolean remove) {  //@front
                                while (!main.isEmpty()) spare.push(main.pop());  //@pour
                                int value = remove ? spare.pop() : spare.peek();  //@front
                                while (!spare.isEmpty()) main.push(spare.pop());  //@back
                                return value;  //@front
                            }  //@front

                            public int pop() {
                                return front(true);  //@front
                            }

                            public int peek() {
                                return front(false);  //@front
                            }

                            public boolean empty() {
                                return main.isEmpty();  //@empty
                            }
                        }
                    """,
                    "cpp": """
                        class TwoStackQueue {
                            stack<int> main, spare;  //@init

                            int front(bool remove) {  //@front
                                while (!main.empty()) { spare.push(main.top()); main.pop(); }  //@pour
                                int value = spare.top();  //@front
                                if (remove) spare.pop();  //@front
                                while (!spare.empty()) { main.push(spare.top()); spare.pop(); }  //@back
                                return value;  //@front
                            }  //@front

                        public:
                            TwoStackQueue() {
                            }

                            void push(int x) {
                                main.push(x);  //@push
                            }

                            int pop() {
                                return front(true);  //@front
                            }

                            int peek() {
                                return front(false);  //@front
                            }

                            bool empty() {
                                return main.empty();  //@empty
                            }
                        };
                    """,
                },
                lines=[("init", "The queue lives in `main`, front at the bottom; `spare` is scratch space.", {"java": "`ArrayDeque` used strictly as a stack: `push`, `pop`, `peek` and `isEmpty`."}), ("push", "New items go on top: the back of the queue."), ("pour", "Reverse the queue into `spare`: the front is now on top."), ("front", "Read (and for `pop`, remove) the front."), ("back", "Restore `main` so the next `push` lands at the back again."), ("empty", "The queue is empty when `main` is.")],
                complexity=["**Time O(n) per `pop`/`peek`** (two full pours), O(1) per `push`. **Space O(n).**"],
                limits=["Pouring back is wasted work: after the first pour, 'spare' already holds the queue in exactly the right order for the next reads. Keep it there, and send new items to the other stack."],
                slow=True,
                langs=DESIGN,
            ),
            approach(
                "Inbox and outbox, pour only when empty",
                "best",
                "O(1) amortised",
                "O(n)",
                idea=["`push` goes onto `in`. `pop`/`peek` read from the top of `out`; if `out` is empty, first pour all of `in` into it. `empty` is true when both are empty."],
                walk=w2,
                build=["Two stacks, `in` and `out`.", "`push`: onto `in`.", "Before reading: if `out` is empty, pour `in` into it.", "`pop`/`peek`: top of `out`. `empty`: both empty."],
                code={
                    "python": """
                        class TwoStackQueue:
                            def __init__(self):
                                self.inbox = []  #@init
                                self.outbox = []  #@init

                            def _turn(self):  #@turn
                                if not self.outbox:  #@turn
                                    while self.inbox:  #@turn
                                        self.outbox.append(self.inbox.pop())  #@turn

                            def push(self, x: int) -> None:
                                self.inbox.append(x)  #@push

                            def pop(self) -> int:
                                self._turn()  #@read
                                return self.outbox.pop()  #@read

                            def peek(self) -> int:
                                self._turn()  #@read
                                return self.outbox[-1]  #@read

                            def empty(self) -> bool:
                                return not self.inbox and not self.outbox  #@empty
                    """,
                    "java": """
                        class TwoStackQueue {
                            private final ArrayDeque<Integer> in = new ArrayDeque<>(), out = new ArrayDeque<>();  //@init

                            public TwoStackQueue() {
                            }

                            private void turn() {  //@turn
                                if (out.isEmpty()) while (!in.isEmpty()) out.push(in.pop());  //@turn
                            }  //@turn

                            public void push(int x) {
                                in.push(x);  //@push
                            }

                            public int pop() {
                                turn();  //@read
                                return out.pop();  //@read
                            }

                            public int peek() {
                                turn();  //@read
                                return out.peek();  //@read
                            }

                            public boolean empty() {
                                return in.isEmpty() && out.isEmpty();  //@empty
                            }
                        }
                    """,
                    "cpp": """
                        class TwoStackQueue {
                            stack<int> in, out;  //@init

                            void turn() {  //@turn
                                if (out.empty())  //@turn
                                    while (!in.empty()) { out.push(in.top()); in.pop(); }  //@turn
                            }  //@turn

                        public:
                            TwoStackQueue() {
                            }

                            void push(int x) {
                                in.push(x);  //@push
                            }

                            int pop() {
                                turn();  //@read
                                int value = out.top();  //@read
                                out.pop();  //@read
                                return value;  //@read
                            }

                            int peek() {
                                turn();  //@read
                                return out.top();  //@read
                            }

                            bool empty() {
                                return in.empty() && out.empty();  //@empty
                            }
                        };
                    """,
                },
                lines=[
                    ("init", "`in` collects new arrivals (newest on top); `out` holds older items in queue order (oldest on top)."),
                    ("turn", "Only when `out` is empty: pour `in` into it. Pouring reverses the order, so the oldest arrival ends on top. If `out` still has items, they're older than everything in `in`, so they must go first anyway."),
                    ("push", "Arrivals always go to `in`, in O(1)."),
                    ("read", "The front of the queue is the top of `out`."),
                    ("empty", "Items can be in either stack."),
                ],
                complexity=["**Time O(1) amortised per call:** each item is pushed onto `in` once, poured once, and popped from `out` once. A single `pop` can cost O(n) when it triggers a pour, but that pays for the next n reads. **Space O(n).**"],
                langs=DESIGN,
            ),
        ],
        takeaways=[
            """
            - **Two stacks make a queue:** pouring one into the other reverses the order.
            - Pour lazily (only when the output side is empty) for amortised O(1) per operation.
            - Amortised analysis: count how many times each item can be moved over its whole life.
            """
        ],
    )


@problem
def stack_from_a_queue():
    calls = [("push", 1), ("push", 2), ("push", 3), ("top",), ("pop",), ("push", 4), ("pop",), ("top",)]

    w1 = Steps("Keep items in arrival order (newest at the back). To reach the top, rotate everything in front of it to the back.")
    q = deque()
    for c in calls:
        if c[0] == "push":
            q.append(c[1])
            w1.step(f"push({c[1]}): add to the back.", Row(list(q), label="queue (front → back)"))
        else:
            for _ in range(len(q) - 1):
                q.append(q.popleft())
            v = q[0]
            if c[0] == "pop":
                q.popleft()
                w1.step(f"pop(): rotate {len(q)} item(s) to the back so the newest ({v}) is at the front; remove it.", Row(list(q) or ["·"], label="queue (front → back)"), Vars(returned=v))
            else:
                q.append(q.popleft())
                w1.step(f"top(): rotate so the newest ({v}) is at the front, read it, then send it to the back too, restoring the order.", Row(list(q), label="queue (front → back)"), Vars(returned=v))
    w1.step("Each pop or top rotated almost the whole queue.", result="done")

    w2 = Steps("Keep the queue in stack order: newest at the front. Each push adds at the back and then rotates everything older behind it.")
    q = deque()
    for c in calls:
        if c[0] == "push":
            q.append(c[1])
            for _ in range(len(q) - 1):
                q.append(q.popleft())
            w2.step(f"push({c[1]}): add at the back, then move the {len(q) - 1} older item(s) from the front to the back. {c[1]} is now at the front.", Row(list(q), st={0: "new"}, label="queue (front = top)"))
        elif c[0] == "pop":
            v = q.popleft()
            w2.step(f"pop(): remove the front, {v}.", Row(list(q) or ["·"], label="queue (front = top)"), Vars(returned=v))
        else:
            w2.step(f"top(): the front, {q[0]}.", Row(list(q), st={0: "found"}, label="queue (front = top)"), Vars(returned=q[0]))
    w2.step("Pushes cost O(n); pops and tops are O(1).", result="done")

    sol(
        "stack-from-a-queue",
        summary="""
            A queue can rotate: move the front to the back, repeatedly. After adding a new item at the back, rotate the
            `size − 1` older items behind it, and the new item sits at the front. The queue is then always in stack order,
            so `pop` and `top` just use the front. `push` is O(n), everything else O(1).
        """,
        question=[
            """
            Implement a stack (`push`, `pop`, `top`, `empty`) with a single queue and only queue operations: add to the back,
            look at or remove the front, size, is-empty.

            - **A queue gives back the oldest item; a stack must give back the newest.**
            - **One queue only**, no second container.
            - **At most 3000 calls**, so O(n) per call is acceptable.
            """
        ],
        think=[
            """
            Push 1, 2, 3 into a queue: front 1, back 3. The stack's top is 3, at the back, out of reach. But a queue can
            **rotate**: removing the front and adding it to the back keeps the cyclic order. Rotate twice and the queue
            reads 3, 1, 2, with 3 at the front.
            """,
            fig(Row([1, 2, 3], label="queue"), Row([3, 1, 2], label="after 2 rotations")),
            """
            We can pay for the rotation when reading (every `pop`/`top`) or when writing (every `push`). If we rotate right
            after each push, the queue is always in exact stack order (newest first), so reads cost nothing.
            """,
        ],
        approaches=[
            approach(
                "Rotate when reading",
                "better",
                "O(n) per pop/top",
                "O(n)",
                idea=["`push` adds to the back (O(1)). `pop`/`top` rotate `size − 1` items to the back so the newest is at the front; `pop` removes it, `top` reads it and rotates it to the back as well, restoring the original order."],
                walk=w1,
                build=["`push`: add to the back.", "`pop`: rotate `size − 1` times, remove the front.", "`top`: rotate `size − 1` times, read the front, rotate once more.", "`empty`: queue empty."],
                code={
                    "python": """
                        from collections import deque

                        class QueueStack:
                            def __init__(self):
                                self.q = deque()  #@init

                            def push(self, x: int) -> None:
                                self.q.append(x)  #@push

                            def _bring_newest_forward(self):  #@rotate
                                for _ in range(len(self.q) - 1):  #@rotate
                                    self.q.append(self.q.popleft())  #@rotate

                            def pop(self) -> int:
                                self._bring_newest_forward()  #@pop
                                return self.q.popleft()  #@pop

                            def top(self) -> int:
                                self._bring_newest_forward()  #@top
                                value = self.q.popleft()  #@top
                                self.q.append(value)  #@top
                                return value  #@top

                            def empty(self) -> bool:
                                return not self.q  #@empty
                    """,
                    "java": """
                        class QueueStack {
                            private final ArrayDeque<Integer> q = new ArrayDeque<>();  //@init

                            public QueueStack() {
                            }

                            public void push(int x) {
                                q.offer(x);  //@push
                            }

                            private void bringNewestForward() {  //@rotate
                                for (int i = 0; i < q.size() - 1; i++) q.offer(q.poll());  //@rotate
                            }  //@rotate

                            public int pop() {
                                bringNewestForward();  //@pop
                                return q.poll();  //@pop
                            }

                            public int top() {
                                bringNewestForward();  //@top
                                int value = q.poll();  //@top
                                q.offer(value);  //@top
                                return value;  //@top
                            }

                            public boolean empty() {
                                return q.isEmpty();  //@empty
                            }
                        }
                    """,
                    "cpp": """
                        class QueueStack {
                            queue<int> q;  //@init

                            void bringNewestForward() {  //@rotate
                                for (size_t i = 0; i + 1 < q.size(); i++) { q.push(q.front()); q.pop(); }  //@rotate
                            }  //@rotate

                        public:
                            QueueStack() {
                            }

                            void push(int x) {
                                q.push(x);  //@push
                            }

                            int pop() {
                                bringNewestForward();  //@pop
                                int value = q.front();  //@pop
                                q.pop();  //@pop
                                return value;  //@pop
                            }

                            int top() {
                                bringNewestForward();  //@top
                                int value = q.front();  //@top
                                q.pop();  //@top
                                q.push(value);  //@top
                                return value;  //@top
                            }

                            bool empty() {
                                return q.empty();  //@empty
                            }
                        };
                    """,
                },
                lines=[("init", "One queue, items in arrival order.", {"java": "`ArrayDeque` used strictly as a queue: `offer` at the back, `poll` from the front.", "python": "`deque` used strictly as a queue: `append` at the back, `popleft` from the front."}), ("push", "New item at the back."), ("rotate", "Move everything except the newest from the front to the back; the newest is now at the front."), ("pop", "Remove the newest. The remaining items are still in arrival order (just rotated), so the next read works the same way."), ("top", "Read the newest, then put it back at the back, which restores arrival order exactly."), ("empty", "Nothing in the queue.")],
                complexity=["**Time:** `push` O(1); `pop` and `top` O(n). **Space O(n).**"],
                limits=["Every read pays a full rotation, and `top` is usually called more often than `push`. Rotating once per push instead keeps the queue permanently in stack order, so both reads become O(1)."],
                langs=DESIGN,
            ),
            approach(
                "Rotate after every push",
                "best",
                "O(n) push, O(1) pop/top",
                "O(n)",
                idea=["`push(x)`: add `x` at the back, then move the `size − 1` older items from the front to the back. Now the queue's front is the newest item and the order behind it is newest-to-oldest. `pop` removes the front; `top` reads it."],
                walk=w2,
                build=["`push`: add at the back, rotate `size − 1` times.", "`pop`: remove and return the front.", "`top`: return the front.", "`empty`: queue empty."],
                code={
                    "python": """
                        from collections import deque

                        class QueueStack:
                            def __init__(self):
                                self.q = deque()  #@init

                            def push(self, x: int) -> None:
                                self.q.append(x)  #@push
                                for _ in range(len(self.q) - 1):  #@rotate
                                    self.q.append(self.q.popleft())  #@rotate

                            def pop(self) -> int:
                                return self.q.popleft()  #@read

                            def top(self) -> int:
                                return self.q[0]  #@read

                            def empty(self) -> bool:
                                return not self.q  #@empty
                    """,
                    "java": """
                        class QueueStack {
                            private final ArrayDeque<Integer> q = new ArrayDeque<>();  //@init

                            public QueueStack() {
                            }

                            public void push(int x) {
                                q.offer(x);  //@push
                                for (int i = 0; i < q.size() - 1; i++) q.offer(q.poll());  //@rotate
                            }

                            public int pop() {
                                return q.poll();  //@read
                            }

                            public int top() {
                                return q.peek();  //@read
                            }

                            public boolean empty() {
                                return q.isEmpty();  //@empty
                            }
                        }
                    """,
                    "cpp": """
                        class QueueStack {
                            queue<int> q;  //@init

                        public:
                            QueueStack() {
                            }

                            void push(int x) {
                                q.push(x);  //@push
                                for (size_t i = 0; i + 1 < q.size(); i++) { q.push(q.front()); q.pop(); }  //@rotate
                            }

                            int pop() {
                                int value = q.front();  //@read
                                q.pop();  //@read
                                return value;  //@read
                            }

                            int top() {
                                return q.front();  //@read
                            }

                            bool empty() {
                                return q.empty();  //@empty
                            }
                        };
                    """,
                },
                lines=[("init", "One queue, kept in stack order: front = top.", {"java": "`ArrayDeque` used strictly as a queue: `offer`, `poll`, `peek`.", "python": "`deque` used strictly as a queue: `append`, `popleft`, and reading `[0]`."}), ("push", "The new item joins at the back."), ("rotate", "Move every older item from the front to the back, behind the new one. The new item is now at the front, and the older ones keep their newest-first order behind it."), ("read", "The front is the top of the stack."), ("empty", "Nothing in the queue.")],
                complexity=["**Time:** `push` O(n); `pop`, `top`, `empty` O(1). With at most 3000 calls, that's at most ~4.5 × 10⁶ rotations. **Space O(n).**"],
                langs=DESIGN,
            ),
        ],
        takeaways=[
            """
            - A queue can **rotate** (front to back) without changing its cyclic order; that's enough to reach any item.
            - Decide where to pay: on writes or on reads. Pay where calls are rarer.
            - Unlike two stacks → queue, one queue → stack can't be amortised O(1): every push really reorders everything.
            """
        ],
    )


@problem
def ring_buffer():
    k = 3
    calls = [("enqueue", 1), ("enqueue", 2), ("enqueue", 3), ("enqueue", 4), ("rear",), ("isFull",), ("dequeue",), ("enqueue", 4), ("rear",), ("front",)]

    w1 = Steps(f"A list that grows at the back and shifts everything left when the front leaves. Capacity {k}.")
    items = []
    for c in calls:
        if c[0] == "enqueue":
            ok = len(items) < k
            if ok:
                items.append(c[1])
            msg = f"enqueue({c[1]}): " + ("added at the back → true." if ok else "full → false.")
        elif c[0] == "dequeue":
            ok = bool(items)
            moved = len(items) - 1
            if ok:
                items.pop(0)
            msg = f"dequeue(): remove the front and shift the other {moved} item(s) left → {str(ok).lower()}."
        elif c[0] == "front":
            msg = f"front(): {items[0] if items else -1}."
        elif c[0] == "rear":
            msg = f"rear(): {items[-1] if items else -1}."
        else:
            msg = f"isFull(): {str(len(items) == k).lower()}."
        w1.step(msg, Row(items or ["·"], label="list (front → back)"))
    w1.step("Every dequeue shifted the whole list.", result="done")

    w2 = Steps(f"A fixed array of {k} slots, the index of the front item, and the count. The back is at (head + size − 1) mod k; indices wrap around.")
    buf, head, size = ["·"] * k, 0, 0
    for c in calls:
        if c[0] == "enqueue":
            if size == k:
                msg = f"enqueue({c[1]}): size = {k} = capacity → false."
            else:
                slot = (head + size) % k
                buf[slot] = c[1]
                size += 1
                msg = f"enqueue({c[1]}): write slot (head + size) mod k = {slot}; size {size} → true."
        elif c[0] == "dequeue":
            if size == 0:
                msg = "dequeue(): empty → false."
            else:
                buf[head] = "·"
                head = (head + 1) % k
                size -= 1
                msg = f"dequeue(): just advance head to {head} (nothing moves); size {size} → true."
        elif c[0] == "front":
            msg = f"front(): slot {head} → {buf[head] if size else -1}."
        elif c[0] == "rear":
            msg = f"rear(): slot (head + size − 1) mod k = {(head + size - 1) % k} → {buf[(head + size - 1) % k] if size else -1}."
        else:
            msg = f"isFull(): size {size} == {k} → {str(size == k).lower()}."
        w2.step(msg, Row(buf, st={**({head: "active"} if size else {}), **({(head + size - 1) % k: "found"} if size else {})}, label="slots"), Vars(head=head, size=size))
    w2.step("Every operation is O(1): the data never moves, only the head index and the count change.", result="done")

    sol(
        "ring-buffer",
        summary="""
            Allocate `k` slots once and keep two numbers: `head` (where the front item is) and `size`. The back slot is
            `(head + size − 1) mod k` and the next free slot is `(head + size) mod k`, so indices wrap around the end of
            the array. Enqueue writes a slot, dequeue advances `head`: nothing ever shifts, and every operation is O(1).
        """,
        question=[
            """
            Implement a bounded FIFO buffer of capacity `k` with `enqueue`, `dequeue`, `front`, `rear`, `isEmpty` and
            `isFull`. Failed operations report `false` (or −1 for reading an empty buffer) and change nothing.

            - **Full and empty must be told apart**, even though in both cases the front and back 'meet' in a circular
              layout.
            - **`rear` is the most recently added item still in the buffer.**
            - **Up to 10⁵ calls with `k ≤ 1000`.**
            """
        ],
        think=[
            f"""
            Capacity {k}: enqueue 1, 2, 3; a fourth enqueue fails. Dequeue removes 1. Now 4 fits, and it can go into the
            slot 0 just vacated. The items are 2, 3, 4 in queue order, but in the array they sit as `[4, 2, 3]` with the
            front at index 1. That's the 'ring': the array's end wraps to its start.
            """,
            fig(Row([4, 2, 3], st={1: "active", 0: "found"}, label="slots"), caption="Front at slot 1 (2), back at slot 0 (4)."),
            """
            With `head` and `size`, every position is arithmetic: the i-th item of the queue is at `(head + i) mod k`.
            Keeping `size` (instead of a separate tail index) also settles full vs empty: `size == k` versus `size == 0`.
            """,
        ],
        approaches=[
            approach(
                "List with shifting",
                "brute",
                "O(k) per dequeue",
                "O(k)",
                idea=["Keep the items in a list in queue order. Enqueue appends (if fewer than `k`); dequeue removes index 0, shifting everything left."],
                walk=w1,
                build=["A list and the capacity.", "`enqueue`: append unless full.", "`dequeue`: remove the first element unless empty.", "`front` / `rear`: first / last element, or −1."],
                code={
                    "python": """
                        class RingBuffer:
                            def __init__(self, k: int):
                                self.items = []  #@init
                                self.k = k  #@init

                            def enqueue(self, x: int) -> bool:
                                if len(self.items) == self.k:  #@enq
                                    return False  #@enq
                                self.items.append(x)  #@enq
                                return True  #@enq

                            def dequeue(self) -> bool:
                                if not self.items:  #@deq
                                    return False  #@deq
                                self.items.pop(0)  #@deq
                                return True  #@deq

                            def front(self) -> int:
                                return self.items[0] if self.items else -1  #@peek

                            def rear(self) -> int:
                                return self.items[-1] if self.items else -1  #@peek

                            def isEmpty(self) -> bool:
                                return not self.items  #@state

                            def isFull(self) -> bool:
                                return len(self.items) == self.k  #@state
                    """,
                    "java": """
                        class RingBuffer {
                            private final List<Integer> items = new ArrayList<>();  //@init
                            private final int k;  //@init

                            public RingBuffer(int k) {
                                this.k = k;  //@init
                            }

                            public boolean enqueue(int x) {
                                if (items.size() == k) return false;  //@enq
                                items.add(x);  //@enq
                                return true;  //@enq
                            }

                            public boolean dequeue() {
                                if (items.isEmpty()) return false;  //@deq
                                items.remove(0);  //@deq
                                return true;  //@deq
                            }

                            public int front() {
                                return items.isEmpty() ? -1 : items.get(0);  //@peek
                            }

                            public int rear() {
                                return items.isEmpty() ? -1 : items.get(items.size() - 1);  //@peek
                            }

                            public boolean isEmpty() {
                                return items.isEmpty();  //@state
                            }

                            public boolean isFull() {
                                return items.size() == k;  //@state
                            }
                        }
                    """,
                    "cpp": """
                        class RingBuffer {
                            vector<int> items;  //@init
                            int k;  //@init

                        public:
                            RingBuffer(int k) : k(k) {  //@init
                            }

                            bool enqueue(int x) {
                                if ((int) items.size() == k) return false;  //@enq
                                items.push_back(x);  //@enq
                                return true;  //@enq
                            }

                            bool dequeue() {
                                if (items.empty()) return false;  //@deq
                                items.erase(items.begin());  //@deq
                                return true;  //@deq
                            }

                            int front() {
                                return items.empty() ? -1 : items.front();  //@peek
                            }

                            int rear() {
                                return items.empty() ? -1 : items.back();  //@peek
                            }

                            bool isEmpty() {
                                return items.empty();  //@state
                            }

                            bool isFull() {
                                return (int) items.size() == k;  //@state
                            }
                        };
                    """,
                },
                lines=[("init", "Items in queue order, and the capacity."), ("enq", "Refuse when full; otherwise append at the back."), ("deq", "Refuse when empty; otherwise remove the front, which shifts every remaining item one place left."), ("peek", "Front and back are the ends of the list; −1 when empty."), ("state", "Empty and full come straight from the length.")],
                complexity=["**Time:** `dequeue` O(k) for the shift; everything else O(1). **Space O(k).**"],
                limits=["A real ring buffer exists to avoid moving data: audio samples stream in and out constantly. Shifting on every dequeue (and growing the list) defeats the purpose. Fixed slots with a moving head index make every operation O(1)."],
                langs=DESIGN,
            ),
            approach(
                "Fixed array, head index and size",
                "best",
                "O(1)",
                "O(k)",
                idea=["Allocate `k` slots. Track `head` (the front item's slot) and `size`. Enqueue writes at `(head + size) % k`; dequeue sets `head = (head + 1) % k`; rear reads `(head + size − 1) % k`. Empty is `size == 0`, full is `size == k`."],
                walk=w2,
                build=["Array of `k` slots, `head = 0`, `size = 0`.", "`enqueue`: if not full, write the next free slot and grow `size`.", "`dequeue`: if not empty, advance `head` and shrink `size`.", "`front`/`rear`: read by index, or −1."],
                code={
                    "python": """
                        class RingBuffer:
                            def __init__(self, k: int):
                                self.buf = [0] * k  #@init
                                self.k = k  #@init
                                self.head = 0  #@init
                                self.size = 0  #@init

                            def enqueue(self, x: int) -> bool:
                                if self.size == self.k:  #@enq
                                    return False  #@enq
                                self.buf[(self.head + self.size) % self.k] = x  #@enq
                                self.size += 1  #@enq
                                return True  #@enq

                            def dequeue(self) -> bool:
                                if self.size == 0:  #@deq
                                    return False  #@deq
                                self.head = (self.head + 1) % self.k  #@deq
                                self.size -= 1  #@deq
                                return True  #@deq

                            def front(self) -> int:
                                return self.buf[self.head] if self.size else -1  #@front

                            def rear(self) -> int:
                                return self.buf[(self.head + self.size - 1) % self.k] if self.size else -1  #@rear

                            def isEmpty(self) -> bool:
                                return self.size == 0  #@state

                            def isFull(self) -> bool:
                                return self.size == self.k  #@state
                    """,
                    "java": """
                        class RingBuffer {
                            private final int[] buf;  //@init
                            private int head = 0, size = 0;  //@init

                            public RingBuffer(int k) {
                                buf = new int[k];  //@init
                            }

                            public boolean enqueue(int x) {
                                if (size == buf.length) return false;  //@enq
                                buf[(head + size) % buf.length] = x;  //@enq
                                size++;  //@enq
                                return true;  //@enq
                            }

                            public boolean dequeue() {
                                if (size == 0) return false;  //@deq
                                head = (head + 1) % buf.length;  //@deq
                                size--;  //@deq
                                return true;  //@deq
                            }

                            public int front() {
                                return size == 0 ? -1 : buf[head];  //@front
                            }

                            public int rear() {
                                return size == 0 ? -1 : buf[(head + size - 1) % buf.length];  //@rear
                            }

                            public boolean isEmpty() {
                                return size == 0;  //@state
                            }

                            public boolean isFull() {
                                return size == buf.length;  //@state
                            }
                        }
                    """,
                    "cpp": """
                        class RingBuffer {
                            vector<int> buf;  //@init
                            int head = 0, size = 0;  //@init

                        public:
                            RingBuffer(int k) : buf(k) {  //@init
                            }

                            bool enqueue(int x) {
                                if (size == (int) buf.size()) return false;  //@enq
                                buf[(head + size) % buf.size()] = x;  //@enq
                                size++;  //@enq
                                return true;  //@enq
                            }

                            bool dequeue() {
                                if (size == 0) return false;  //@deq
                                head = (head + 1) % buf.size();  //@deq
                                size--;  //@deq
                                return true;  //@deq
                            }

                            int front() {
                                return size == 0 ? -1 : buf[head];  //@front
                            }

                            int rear() {
                                return size == 0 ? -1 : buf[(head + size - 1) % buf.size()];  //@rear
                            }

                            bool isEmpty() {
                                return size == 0;  //@state
                            }

                            bool isFull() {
                                return size == (int) buf.size();  //@state
                            }
                        };
                    """,
                },
                lines=[
                    ("init", "`k` slots allocated once; `head` = slot of the front item; `size` = items stored."),
                    ("enq", "Full → refuse. Otherwise the first free slot is `size` steps after `head`, wrapping with `% k`."),
                    ("deq", "Empty → refuse. Otherwise the front slot is simply abandoned: advance `head` (wrapping) and shrink `size`. No data moves."),
                    ("front", "The item at `head`, or −1."),
                    ("rear", "The last stored item is `size − 1` steps after `head`, wrapping. (`head + size − 1` is never negative when `size ≥ 1`.)"),
                    ("state", "Counting items makes empty (`0`) and full (`k`) unambiguous, which a head/tail pair alone can't do."),
                ],
                complexity=["**Time O(1)** for every operation. **Space O(k)**, allocated once."],
                langs=DESIGN,
            ),
        ],
        takeaways=[
            """
            - **Circular buffer = fixed array + head + size**, with `% k` for wrap-around.
            - Store the size (or waste one slot) to tell full from empty.
            - Dequeuing moves an index, never the data.
            """
        ],
    )
