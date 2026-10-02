import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import *

DONE = []


def run(fn):
    pid = fn.__name__.replace("_", "-")
    DONE.append((pid, fn(pid)))
    return fn


# ======================================================================== reversal

@run
def reverse_the_train(pid):
    a, exp = example(pid)
    v = a["head"]
    n = len(v)
    W = Walk(pid, "Walk the list once, turning each node's arrow around to point at the node before it.")
    W.step("prev starts at nothing and cur at the head.", L(v, ptr={"cur": 0}))
    for cur in range(n):
        links = [[i, i - 1] for i in range(1, cur + 1)] + [[i, i + 1] for i in range(cur + 1, n - 1)]
        W.step(f"Point {v[cur]} back at {v[cur - 1] if cur else 'nothing'}, then move prev and cur one step on.",
               L(v, st={cur: "active"}, ptr={"prev": cur, "cur": cur + 1 if cur + 1 < n else None}, links=links))
    W.step(f"cur ran off the end, so prev ({v[-1]}) is the new head.", L(list(reversed(v)), st={0: "answer"}, label="result"))
    assert list(reversed(v)) == exp
    return W.save()


@run
def flip_in_batches(pid):
    a, exp = example(pid)
    v, k = list(a["head"]), a["k"]
    W = Walk(pid, f"Work in batches of {k}: reverse each full batch in place and leave a short last batch alone.")
    W.step("The list before any flips.", L(v))
    i = 0
    while i + k <= len(v):
        v[i:i + k] = reversed(v[i:i + k])
        W.step(f"Positions {i}–{i + k - 1} form a full batch: reverse it and reconnect both ends.", L(v, st={j: "new" for j in range(i, i + k)}))
        i += k
    if i < len(v):
        W.step(f"Only {len(v) - i} node{'s' if len(v) - i > 1 else ''} left, fewer than {k}: keep them as they are.", L(v, st={j: "dim" for j in range(i, len(v))}))
    assert v == exp
    return W.save()


@run
def flip_the_even_groups(pid):
    a, exp = example(pid)
    v = list(a["head"])
    W = Walk(pid, "Cut the list into groups of 1, 2, 3, … nodes. Reverse each group whose ACTUAL size is even.")
    i, size = 0, 1
    while i < len(v):
        real = min(size, len(v) - i)
        if real % 2 == 0:
            v[i:i + real] = reversed(v[i:i + real])
            W.step(f"Group {size} has {real} nodes, an even count: reverse it.", L(v, st={j: "new" for j in range(i, i + real)}))
        else:
            W.step(f"Group {size} has {real} node{'s' if real > 1 else ''}, an odd count: leave it.", L(v, st={j: "active" for j in range(i, i + real)}))
        i += real
        size += 1
    assert v == exp
    return W.save()


@run
def flip_a_stretch(pid):
    a, exp = example(pid)
    v, lo, hi = list(a["head"]), a["left"] - 1, a["right"] - 1
    W = Walk(pid, f"Stop at the node before position {lo + 1}. Then, again and again, move the node after the stretch's first node to the front of the stretch.")
    W.step(f"before is the node just in front of the stretch.", L(v, st={j: "active" for j in range(lo, hi + 1)}, ptr={"before": lo - 1 if lo else None}))
    first = lo
    for step in range(hi - lo):
        moved = v.pop(first + 1)
        v.insert(lo, moved)
        first += 1
        W.step(f"Move {moved} to just after before.", L(v, st={lo: "new", **{j: "active" for j in range(lo + 1, hi + 1)}}, ptr={"before": lo - 1 if lo else None, "first": first}))
    assert v == exp
    return W.save()


@run
def reads_the_same_backwards(pid):
    a, exp = example(pid)
    v = a["head"]
    n = len(v)
    W = Walk(pid, "Find the middle with slow and fast pointers, reverse the second half, then compare the halves.")
    slow = fast = 0
    W.step("slow moves one step, fast two.", L(v, ptr={"slow": 0, "fast": 0}))
    while fast + 1 < n and fast + 2 < n:
        slow += 1
        fast += 2
        W.step("Step both pointers.", L(v, ptr={"slow": slow, "fast": fast}))
    second = list(reversed(v[slow + 1:]))
    W.step(f"Reverse everything after {v[slow]}: the second half reads {second}.", L(v[:slow + 1], label="first half"), L(second, st={i: "new" for i in range(len(second))}, label="second half, reversed"))
    ok = all(v[i] == second[i] for i in range(len(second)))
    W.step("Compare them node by node: " + ("all equal, so it reads the same backwards." if ok else "they differ."), L(v[:slow + 1], st={i: "found" if ok else "mark" for i in range(len(second))}, label="first half"),
           L(second, st={i: "found" if ok else "mark" for i in range(len(second))}, label="second half, reversed"), result=ok)
    assert ok == exp
    return W.save()


# ======================================================================== fast-slow

@run
def halfway_car(pid):
    a, exp = example(pid)
    v = a["head"]
    W = Walk(pid, "Move slow one car and fast two cars at a time. When fast reaches the end, slow is halfway.")
    slow = fast = 0
    W.step("Both start at the front.", L(v, ptr={"slow": 0, "fast": 0}))
    while fast < len(v) and fast + 1 < len(v):
        slow += 1
        fast += 2
        W.step("slow +1, fast +2.", L(v, ptr={"slow": slow, "fast": fast if fast < len(v) else None}))
    W.step(f"fast can't go on, so slow ({v[slow]}) is the halfway car.", L(v, st={i: "answer" for i in range(slow, len(v))}, ptr={"slow": slow}))
    assert v[slow:] == exp
    return W.save()


@run
def drop_kth_from_the_back(pid):
    a, exp = example(pid)
    v, k = a["head"], a["k"]
    n = len(v)
    W = Walk(pid, f"Send lead {k} nodes ahead, then move both pointers until lead reaches the last node: trail is just before the node to drop.")
    lead = k - 1
    W.step(f"lead goes {k} nodes ahead of a dummy in front of the head.", L(v, ptr={"lead": lead}))
    trail = -1
    while lead < n - 1:
        lead += 1
        trail += 1
        W.step("Move both one step.", L(v, ptr={"trail": trail if trail >= 0 else None, "lead": lead}))
    target = trail + 1
    W.step(f"lead is on the last node, so {v[target]} is {k}-th from the back: skip over it.", L(v, st={target: "mark"}, ptr={"trail": trail if trail >= 0 else None}))
    out = v[:target] + v[target + 1:]
    W.step("The result.", L(out))
    assert out == exp
    return W.save()


@run
def loop_in_the_track(pid):
    a, exp = example(pid)
    v, c = a["head"]["values"], a["head"].get("cycle_at", -1)
    n = len(v)
    nxt = lambda i: (i + 1 if i + 1 < n else (c if c >= 0 else None))
    W = Walk(pid, "Send a slow runner (1 step) and a fast runner (2 steps). If the track loops, fast laps slow and they meet.")
    s = f = 0
    W.step("Both start at the head.", L(v, ptr={"slow": 0, "fast": 0}, cycle=c if c >= 0 else None))
    met = False
    for _ in range(2 * n + 2):
        s = nxt(s)
        f = nxt(f)
        f = nxt(f) if f is not None else None
        if f is None or s is None:
            W.step("fast fell off the end: no loop.", L(v, cycle=c if c >= 0 else None), result=False)
            break
        same = s == f
        W.step("slow +1, fast +2." + (" They meet: there's a loop." if same else ""), L(v, st={s: "answer"} if same else {}, ptr={"slow": s, "fast": f}, cycle=c if c >= 0 else None), result=True if same else None)
        if same:
            met = True
            break
    assert met == exp
    return W.save()


@run
def laps_around_the_loop(pid):
    a, exp = example(pid)
    v, c = a["head"]["values"], a["head"].get("cycle_at", -1)
    n = len(v)
    W = Walk(pid, "Measure the lead-in (nodes before the loop) and the loop length once; then any step count is arithmetic.")
    if c >= 0:
        W.step(f"The lead-in has {c} node{'s' if c != 1 else ''} and the loop has {n - c}.", L(v, st={i: ("found" if i >= c else "dim") for i in range(n)}, cycle=c))
    out = []
    for s in a["steps"]:
        if s < n:
            pos = s
        elif c < 0:
            pos = -1
        else:
            pos = c + (s - c) % (n - c)
        out.append(v[pos] if pos >= 0 else -1)
        W.step(f"After {s} steps: " + (f"position {pos}, value {v[pos]}." if pos >= 0 else "past the end, -1.") + (f" ({s} − {c}) mod {n - c} = {(s - c) % (n - c)} into the loop." if c >= 0 and s >= n else ""),
               L(v, st={pos: "answer"} if pos >= 0 else {}, ptr={"runner": pos} if pos >= 0 else None, cycle=c if c >= 0 else None), result=out[-1])
    assert out == exp
    return W.save()


# ======================================================================== dummy-node

@run
def slot_into_sorted_chain(pid):
    a, exp = example(pid)
    v, x = a["head"], a["value"]
    W = Walk(pid, f"Start at a dummy before the head and walk while the next value is smaller than {x}.")
    i = -1
    W.step("cur starts on the dummy.", L(v, ptr={}))
    while i + 1 < len(v) and v[i + 1] < x:
        i += 1
        W.step(f"{v[i]} < {x}: step forward.", L(v, st={i: "active"}, ptr={"cur": i}))
    out = v[:i + 1] + [x] + v[i + 1:]
    W.step(f"Insert {x} after " + (str(v[i]) if i >= 0 else "the dummy (it's the new head)") + ".", L(out, st={i + 1: "new"}))
    assert out == exp
    return W.save()


@run
def cancel_out_runs(pid):
    a, exp = example(pid)
    v = a["head"]
    W = Walk(pid, "Copy entries one by one while tracking the running sum. A repeated running sum means the entries since then add up to 0.")
    sheet, sums = [], [0]
    for x in v:
        sheet.append(x)
        s = sums[-1] + x
        if s in sums:
            j = sums.index(s)
            W.step(f"Copy {x}: the running sum is {s} again, so the last {len(sheet) - j} entries cancel out.", L(sheet, st={i: "mark" for i in range(j, len(sheet))}), Vars(running_sum=s))
            sheet = sheet[:j]
            sums = sums[:j + 1]
        else:
            sums.append(s)
            W.step(f"Copy {x}: running sum {s}.", L(sheet, st={len(sheet) - 1: "new"}), Vars(running_sum=s))
    W.step("The clean sheet.", L(sheet))
    assert sheet == exp
    return W.save()


@run
def purge_repeated_readings(pid):
    a, exp = example(pid)
    v = a["head"]
    W = Walk(pid, "From a dummy before the head, look at each run of equal readings: keep a run of one, cut out a longer run entirely.")
    out, i = [], 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[i]:
            j += 1
        if j > i:
            W.step(f"{v[i]} appears {j - i + 1} times: link past all of them.", L(v, st={**{k: "dim" for k in range(i)}, **{k: "mark" for k in range(i, j + 1)}}))
        else:
            out.append(v[i])
            W.step(f"{v[i]} appears once: keep it.", L(v, st={**{k: "dim" for k in range(i)}, i: "found"}))
        i = j + 1
    W.step("The result.", L(out))
    assert out == exp
    return W.save()


@run
def drop_faulty_beads(pid):
    a, exp = example(pid)
    v, bad = a["head"], a["bad"]
    W = Walk(pid, f"With a dummy before the head, look one bead ahead: if it's {bad}, link past it; otherwise step forward.")
    out = []
    for i, x in enumerate(v):
        if x == bad:
            W.step(f"{x} is faulty: link past it.", L(v, st={**{k: ("found" if v[k] != bad else "dim") for k in range(i)}, i: "mark"}))
        else:
            out.append(x)
            W.step(f"{x} is fine: keep it.", L(v, st={**{k: ("found" if v[k] != bad else "dim") for k in range(i)}, i: "found"}))
    W.step("The result.", L(out))
    assert out == exp
    return W.save()


# ======================================================================== arithmetic

@run
def tick_the_odometer(pid):
    a, exp = example(pid)
    v = list(a["head"])
    W = Walk(pid, "Find the last digit that isn't 9. Add 1 there and turn every 9 after it into 0.")
    last = -1
    for i, d in enumerate(v):
        if d != 9:
            last = i
    W.step(f"The last non-9 digit is at position {last}" + (f" ({v[last]})." if last >= 0 else ": there isn't one, so a new leading 1 is needed."), L(v, st={**({last: "active"} if last >= 0 else {}), **{i: "mark" for i in range(last + 1, len(v))}}))
    if last >= 0:
        v[last] += 1
    else:
        v = [1] + v
        last = 0
    for i in range(last + 1, len(v)):
        v[i] = 0
    W.step("Add 1 there and zero the rest.", L(v, st={i: "new" for i in range(last, len(v))}))
    assert v == exp
    return W.save()


@run
def add_two_tallies(pid):
    a, exp = example(pid)
    x, y = a["a"], a["b"]
    W = Walk(pid, "The ones digits come first, so add column by column from the front, carrying as on paper.")
    out, carry, i = [], 0, 0
    while i < len(x) or i < len(y) or carry:
        dx = x[i] if i < len(x) else 0
        dy = y[i] if i < len(y) else 0
        s = dx + dy + carry
        out.append(s % 10)
        W.step(f"{dx} + {dy} + carry {carry} = {s}: write {s % 10}, carry {s // 10}.", L(x, st={i: "active"} if i < len(x) else {}, label="a"), L(y, st={i: "active"} if i < len(y) else {}, label="b"), L(out, st={len(out) - 1: "new"}, label="sum"))
        carry = s // 10
        i += 1
    assert out == exp
    return W.save()


@run
def front_first_sum(pid):
    a, exp = example(pid)
    x, y = a["a"], a["b"]
    W = Walk(pid, "Carries start at the ones digit, which is at the END here. Push both lists' digits onto stacks and pop to add from the back.")
    sx, sy = list(x), list(y)
    W.step("Push every digit onto two stacks.", Row(sx, label="stack a (top on the right)"), Row(sy, label="stack b (top on the right)"))
    out, carry = [], 0
    while sx or sy or carry:
        dx = sx.pop() if sx else 0
        dy = sy.pop() if sy else 0
        s = dx + dy + carry
        out.insert(0, s % 10)
        W.step(f"{dx} + {dy} + carry {carry} = {s}: put {s % 10} at the FRONT of the answer.", Row(sx, label="stack a"), Row(sy, label="stack b"), L(out, st={0: "new"}, label="sum"))
        carry = s // 10
    assert out == exp
    return W.save()


# ======================================================================== merge-split

@run
def combine_sorted_rosters(pid):
    a, exp = example(pid)
    x, y = a["first"], a["second"]
    W = Walk(pid, "Merge the two sorted lists, always taking the smaller head, and skip any number equal to the last one written.")
    i = j = 0
    out = []
    while i < len(x) or j < len(y):
        take_x = j >= len(y) or (i < len(x) and x[i] <= y[j])
        v = x[i] if take_x else y[j]
        src = "first" if take_x else "second"
        if out and out[-1] == v:
            text = f"{v} from {src} repeats the last number: skip it."
        else:
            out.append(v)
            text = f"Take {v} from {src}."
        W.step(text, L(x, st={k: "dim" for k in range(i)}, ptr={"i": i if i < len(x) else None}, label="first"), L(y, st={k: "dim" for k in range(j)}, ptr={"j": j if j < len(y) else None}, label="second"), L(out, st={len(out) - 1: "new"}, label="merged"))
        if take_x:
            i += 1
        else:
            j += 1
    assert out == exp
    return W.save()


@run
def merge_checkout_queues(pid):
    a, exp = example(pid)
    qs = [list(q) for q in a["queues"]]
    W = Walk(pid, "Keep the front of every queue in a min-heap. Take the smallest front, then push that queue's next node.")
    idx = [0] * len(qs)
    out = []
    while True:
        fronts = [(qs[k][idx[k]], k) for k in range(len(qs)) if idx[k] < len(qs[k])]
        if not fronts:
            break
        v, k = min(fronts)
        out.append(v)
        W.step(f"Fronts are {sorted(f[0] for f in fronts)}; the smallest is {v} from queue {k}.", *[L(qs[q], st={**{t: "dim" for t in range(idx[q])}, **({idx[q]: "answer"} if q == k else {})}, label=f"queue {q}") for q in range(len(qs))], L(out, st={len(out) - 1: "new"}, label="merged"))
        idx[k] += 1
    assert out == exp
    return W.save()


@run
def closest_to_zero_first(pid):
    a, exp = example(pid)
    v = a["head"]
    W = Walk(pid, "Merge sort by absolute value: split the list in half, sort each half, then merge, taking from the left half on ties so equal values keep their order.")
    steps = []

    def sort(lst):
        if len(lst) <= 1:
            return lst
        mid = (len(lst) + 1) // 2
        left, right = sort(lst[:mid]), sort(lst[mid:])
        out, i, j = [], 0, 0
        while i < len(left) or j < len(right):
            if j >= len(right) or (i < len(left) and abs(left[i]) <= abs(right[j])):
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
        W.step(f"Merge {left} and {right} by absolute value.", L(left, label="left half"), L(right, label="right half"), L(out, st={k: "new" for k in range(len(out))}, label="merged"))
        return out

    res = sort(list(v))
    assert res == exp
    return W.save()


@run
def low_notes_first(pid):
    a, exp = example(pid)
    v, p = a["head"], a["pivot"]
    W = Walk(pid, f"Build two chains as you walk: notes below {p}, and the rest. Then join the first chain to the second.")
    low, high = [], []
    for i, x in enumerate(v):
        (low if x < p else high).append(x)
        W.step(f"{x} {'<' if x < p else '≥'} {p}: add it to the {'low' if x < p else 'high'} chain.", L(v, st={**{k: "dim" for k in range(i)}, i: "active"}), L(low, label="low"), L(high, label="high"))
    out = low + high
    W.step("Join low to high.", L(out, st={k: ("found" if k < len(low) else "") for k in range(len(out))}))
    assert out == exp
    return W.save()


# ======================================================================== reorder

@run
def swap_dance_partners(pid):
    a, exp = example(pid)
    v = list(a["head"])
    W = Walk(pid, "From a dummy, take the next two nodes and swap their links so the second comes first.")
    for i in range(0, len(v) - 1, 2):
        v[i], v[i + 1] = v[i + 1], v[i]
        W.step(f"Swap the pair {v[i + 1]} and {v[i]}.", L(v, st={i: "new", i + 1: "new"}))
    assert v == exp
    return W.save()


@run
def odd_seats_first(pid):
    a, exp = example(pid)
    v = a["head"]
    W = Walk(pid, "Thread two chains at once: odd seats and even seats. At the end, hang the even chain after the odd one.")
    odd, even = [], []
    for i, x in enumerate(v):
        (odd if i % 2 == 0 else even).append(x)
        W.step(f"Seat {i + 1} ({x}) goes on the {'odd' if i % 2 == 0 else 'even'} chain.", L(v, st={**{k: "dim" for k in range(i)}, i: "active"}), L(odd, label="odd"), L(even, label="even"))
    out = odd + even
    W.step("Link the odd chain's last node to the even chain's head.", L(out))
    assert out == exp
    return W.save()


@run
def shift_the_conga_line(pid):
    a, exp = example(pid)
    v, k = a["head"], a["k"]
    n = len(v)
    W = Walk(pid, "k beats move the last k dancers to the front. Only k mod n matters.")
    r = k % n if n else 0
    W.step(f"The line has {n} dancers, so {k} beats act like {r}.", L(v, st={i: "active" for i in range(n - r, n)}))
    if r:
        W.step(f"Cut after {v[n - r - 1]} (the new tail) and close the line into a loop.", L(v, st={n - r - 1: "mark", **{i: "active" for i in range(n - r, n)}}, cycle=0))
    out = v[n - r:] + v[:n - r]
    W.step(f"{out[0]} is the new head.", L(out, st={0: "answer"}))
    assert out == exp
    return W.save()


@run
def fold_the_chain(pid):
    a, exp = example(pid)
    v = a["head"]
    n = len(v)
    W = Walk(pid, "Three moves: find the middle, reverse the second half, then weave the halves together.")
    mid = (n - 1) // 2
    W.step(f"Slow and fast pointers stop slow at {v[mid]}, the end of the first half.", L(v, st={i: "found" for i in range(mid + 1)}, ptr={"slow": mid}))
    first, second = v[:mid + 1], list(reversed(v[mid + 1:]))
    W.step("Cut after it and reverse the second half.", L(first, label="first half"), L(second, st={i: "new" for i in range(len(second))}, label="second half, reversed"))
    out = []
    for i in range(len(first)):
        out.append(first[i])
        if i < len(second):
            out.append(second[i])
        W.step(f"Weave: take {first[i]}" + (f", then {second[i]}." if i < len(second) else "."), L(out, st={len(out) - 1: "new"}, label="folded"))
    assert out == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
