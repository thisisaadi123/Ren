import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import *

DONE = []


CUSTOM = {}
run = make_runner(DONE, CUSTOM)


def call_text(c):
    return f"{c[0]}({', '.join(json.dumps(x) if isinstance(x, str) else str(x) for x in c[1:])})"


def check(out, exp, pid):
    assert [None if x is None else x for x in out] == exp, (pid, out, exp)


@run
def queue_from_two_stacks(pid):
    a, exp = example(pid)
    inbox, outbox, out = [], [], [None]
    W = Walk(pid, "New items go on the inbox stack. The outbox is refilled from the inbox only when it's empty, which reverses the order.")
    for c in a["calls"]:
        if c[0] == "TwoStackQueue":
            W.step("Two empty stacks.", Row(inbox, label="inbox (top on the right)"), Row(outbox, label="outbox (top on the right)"), call=call_text(c))
            continue
        moved = False
        if c[0] in ("pop", "peek") and not outbox:
            while inbox:
                outbox.append(inbox.pop())
            moved = True
        if c[0] == "push":
            inbox.append(c[1])
            r, text = None, f"Push {c[1]} onto the inbox."
            st_in, st_out = {len(inbox) - 1: "new"}, {}
        elif c[0] == "pop":
            r = outbox.pop()
            text = ("The outbox was empty, so pour the inbox into it first. " if moved else "") + f"Pop {r} off the outbox: it's the oldest item."
            st_in, st_out = {}, {}
        elif c[0] == "peek":
            r = outbox[-1]
            text = ("The outbox was empty, so pour the inbox into it first. " if moved else "") + f"The top of the outbox, {r}, is the front of the queue."
            st_in, st_out = {}, {len(outbox) - 1: "answer"}
        else:
            r = not inbox and not outbox
            text = "Both stacks are empty." if r else "Something is still stored."
            st_in, st_out = {}, {}
        out.append(r)
        W.step(text, Row(inbox, st=st_in, label="inbox"), Row(outbox, st=st_out, label="outbox"), call=call_text(c), result=r)
    check(out, exp, pid)
    return W.save()


@run
def stack_from_a_queue(pid):
    a, exp = example(pid)
    q, out = [], [None]
    W = Walk(pid, "After each push, rotate the queue so the newest item is at the front.")
    for c in a["calls"]:
        if c[0] == "QueueStack":
            W.step("An empty queue.", Row(q, label="queue (front on the left)"), call=call_text(c))
            continue
        if c[0] == "push":
            q.append(c[1])
            W.step(f"Add {c[1]} at the back.", Row(q, st={len(q) - 1: "new"}, label="queue"), call=call_text(c))
            for _ in range(len(q) - 1):
                q.append(q.pop(0))
            out.append(None)
            if len(q) > 1:
                W.step(f"Move the {len(q) - 1} older item{'s' if len(q) > 2 else ''} from the front to the back, so {c[1]} is at the front.", Row(q, st={0: "new"}, label="queue"))
            continue
        if c[0] == "pop":
            r = q.pop(0)
            text = f"Remove the front: {r}."
        elif c[0] == "top":
            r = q[0]
            text = f"The front, {r}, is the top of the stack."
        else:
            r = not q
            text = "The queue is empty." if r else "Something is still stored."
        out.append(r)
        W.step(text, Row(q, st={0: "answer"} if c[0] == "top" else {}, label="queue"), call=call_text(c), result=r)
    check(out, exp, pid)
    return W.save()


@run
def price_streak_tracker(pid):
    a, exp = example(pid)
    st, out = [], [None]
    W = Walk(pid, "Keep a stack of (price, streak) with falling prices. A new price swallows every entry it beats and adds up their streaks.")
    for c in a["calls"]:
        if c[0] == "PriceStreak":
            W.step("An empty stack.", Row([], label="stack: price·streak"), call=call_text(c))
            continue
        p = c[1]
        streak, eaten = 1, []
        while st and st[-1][0] <= p:
            eaten.append(st.pop())
            streak += eaten[-1][1]
        st.append((p, streak))
        out.append(streak)
        text = (f"{p} beats " + ", ".join(str(e[0]) for e in eaten) + f", so it absorbs their streaks: 1 + {' + '.join(str(e[1]) for e in eaten)} = {streak}.") if eaten else f"{p} doesn't beat the top, so its streak is 1."
        W.step(text, Row([f"{x}·{y}" for x, y in st], st={len(st) - 1: "new"}, label="stack: price·streak"), call=call_text(c), result=streak)
    check(out, exp, pid)
    return W.save()


@run
def recent_files_cache(pid):
    a, exp = example(pid)
    cap = a["calls"][0][1]
    order, size, out = [], {}, [None]
    W = Walk(pid, "A hash map finds each file; a list ordered by use (oldest on the left) says which file to evict.")
    for c in a["calls"]:
        if c[0] == "RecentFilesCache":
            W.step(f"An empty cache with room for {cap} files.", Row([], label="least recent → most recent"), call=call_text(c))
            continue
        if c[0] == "open":
            f = c[1]
            if f in size:
                order.remove(f)
                order.append(f)
                r = size[f]
                text = f"File {f} is cached: return its size and move it to the most-recent end."
            else:
                r = -1
                text = f"File {f} isn't cached."
            out.append(r)
            W.step(text, Row([f"{x}:{size[x]}" for x in order], st={len(order) - 1: "answer"} if r != -1 else {}, label="least recent → most recent"), call=call_text(c), result=r)
        else:
            f, s = c[1], c[2]
            evicted = None
            if f in size:
                order.remove(f)
            elif len(order) == cap:
                evicted = order.pop(0)
                del size[evicted]
            order.append(f)
            size[f] = s
            out.append(None)
            W.step((f"The cache is full: evict file {evicted}, used longest ago. " if evicted is not None else "") + f"Save file {f} as the most recent.",
                   Row([f"{x}:{size[x]}" for x in order], st={len(order) - 1: "new"}, label="least recent → most recent"), call=call_text(c))
    check(out, exp, pid)
    return W.save()


@run
def ring_buffer(pid):
    a, exp = example(pid)
    k = a["calls"][0][1]
    buf, head, size, out = [None] * k, 0, 0, [None]
    W = Walk(pid, f"A fixed array of {k} slots with a front index and a count; positions wrap around with % {k}.")

    def ptr():
        return {"front": head, "rear": (head + size - 1) % k} if size else {}

    for c in a["calls"]:
        name = c[0]
        if name == "RingBuffer":
            W.step(f"{k} empty slots.", Row(buf, label="slots", slots=True), call=call_text(c))
            continue
        active = {}
        if name == "enqueue":
            if size == k:
                r, text = False, "No free slot, so nothing changes."
            else:
                slot = (head + size) % k
                buf[slot] = c[1]
                size += 1
                r, text = True, f"The next free slot is (front + count) % {k} = {slot}."
                active = {slot: "new"}
        elif name == "dequeue":
            if size == 0:
                r, text = False, "Nothing to remove."
            else:
                buf[head] = None
                active = {head: "dim"}
                head = (head + 1) % k
                size -= 1
                r, text = True, f"The front item leaves; front moves to slot {head}."
        elif name == "front":
            r = buf[head] if size else -1
            text = "front reads the front slot." if size else "Empty: -1."
            active = {head: "answer"} if size else {}
        elif name == "rear":
            r = buf[(head + size - 1) % k] if size else -1
            text = f"rear reads slot (front + count − 1) % {k}." if size else "Empty: -1."
            active = {(head + size - 1) % k: "answer"} if size else {}
        elif name == "isEmpty":
            r, text = size == 0, f"The count is {size}."
        else:
            r, text = size == k, f"The count is {size} of {k}."
        out.append(r)
        W.step(text, Row(buf, st=active, ptr=ptr(), label="slots", slots=True), call=call_text(c), result=r)
    check(out, exp, pid)
    return W.save()


class Trie:
    def __init__(self):
        self.nodes = [{"id": 0, "label": "•", "parent": None}]
        self.kids = {0: {}}
        self.end = set()

    def insert(self, w):
        cur, path = 0, [0]
        for ch in w:
            if ch not in self.kids[cur]:
                nid = len(self.nodes)
                self.nodes.append({"id": nid, "label": ch, "parent": cur})
                self.kids[cur][ch] = nid
                self.kids[nid] = {}
            cur = self.kids[cur][ch]
            path.append(cur)
        self.end.add(cur)
        return path

    def walk(self, s):
        cur, path = 0, [0]
        for ch in s:
            if ch not in self.kids[cur]:
                return None, path
            cur = self.kids[cur][ch]
            path.append(cur)
        return cur, path

    def panel(self, st=None):
        states = {i: "found" for i in self.end}
        states.update(st or {})
        return NT([dict(n) for n in self.nodes], states, label="trie (filled = end of a word)")


@run
def prefix_tree(pid):
    a, exp = example(pid)
    t, out = Trie(), [None]
    W = Walk(pid, "Words share nodes for shared beginnings. A node is marked when a word ends there.")
    for c in a["calls"]:
        if c[0] == "PrefixTree":
            W.step("Just the root.", t.panel(), call=call_text(c))
            continue
        if c[0] == "insert":
            path = t.insert(c[1])
            out.append(None)
            W.step(f"Walk/create one node per letter of \"{c[1]}\" and mark the last one.", t.panel({i: "active" for i in path[1:-1]} | {path[-1]: "new"}), call=call_text(c))
            continue
        node, path = t.walk(c[1])
        if c[0] == "search":
            r = node is not None and node in t.end
            text = f"The path for \"{c[1]}\" " + ("exists and ends at a marked node." if r else ("exists, but no word ends there." if node is not None else "breaks off."))
        else:
            r = node is not None
            text = f"The path for \"{c[1]}\" " + ("exists." if r else "breaks off.")
        out.append(r)
        W.step(text, t.panel({i: "active" for i in path[1:]} | ({path[-1]: "answer"} if r else {})), call=call_text(c), result=r)
    check(out, exp, pid)
    return W.save()


@run
def wildcard_dictionary(pid):
    a, exp = example(pid)
    t, out = Trie(), [None]
    W = Walk(pid, "Store words in a trie. A letter follows one branch; a dot follows every branch at that level.")
    for c in a["calls"]:
        if c[0] == "WildcardDictionary":
            W.step("Just the root.", t.panel(), call=call_text(c))
            continue
        if c[0] == "addWord":
            path = t.insert(c[1])
            out.append(None)
            W.step(f"Add \"{c[1]}\".", t.panel({path[-1]: "new"}), call=call_text(c))
            continue
        frontier, seen = [0], set()
        for ch in c[1]:
            nxt = []
            for f in frontier:
                if ch == ".":
                    nxt += list(t.kids[f].values())
                elif ch in t.kids[f]:
                    nxt.append(t.kids[f][ch])
            frontier = nxt
            seen.update(frontier)
        hits = [f for f in frontier if f in t.end]
        r = bool(hits)
        out.append(r)
        W.step(f"\"{c[1]}\": " + (f"reaches {len(hits)} word end{'s' if len(hits) > 1 else ''}." if r else "no path matches."), t.panel({i: "active" for i in seen} | {h: "answer" for h in hits}), call=call_text(c), result=r)
    check(out, exp, pid)
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
