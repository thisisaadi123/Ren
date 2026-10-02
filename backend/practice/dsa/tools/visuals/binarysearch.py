import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import *

DONE = []


def run(fn):
    pid = fn.__name__.replace("_", "-")
    DONE.append((pid, fn(pid)))
    return fn


def span(v, lo, hi, mid=None, st=None, label=None):
    """A sorted row with the live search range [lo, hi] highlighted."""
    s = {i: "dim" for i in range(len(v)) if i < lo or i > hi}
    if mid is not None and 0 <= mid < len(v):
        s[mid] = "active"
    s.update(st or {})
    ptr = {"lo": lo if 0 <= lo < len(v) else None, "hi": hi if 0 <= hi < len(v) else None}
    if mid is not None:
        ptr["mid"] = mid
    return Row(v, st=s, ptr=ptr, label=label)


def smallest_ok(W, lo, hi, ok, show):
    """Binary search for the smallest x in [lo, hi] with ok(x). show(lo, hi, mid, good) -> (text, panels)."""
    while lo < hi:
        mid = (lo + hi) // 2
        good = ok(mid)
        text, panels = show(lo, hi, mid, good)
        W.step(text, *panels)
        if good:
            hi = mid
        else:
            lo = mid + 1
    return lo


def largest_ok(W, lo, hi, ok, show):
    while lo < hi:
        mid = (lo + hi + 1) // 2
        good = ok(mid)
        text, panels = show(lo, hi, mid, good)
        W.step(text, *panels)
        if good:
            lo = mid
        else:
            hi = mid - 1
    return lo


# ======================================================================== classic-search

@run
def find_the_locker(pid):
    a, exp = example(pid)
    v, t = a["lockers"], a["target"]
    W = Walk(pid, f"Halve the range each step: compare the middle locker with {t} and keep the half that can still hold it.")
    lo, hi, res = 0, len(v) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if v[mid] == t:
            res = mid
            W.step(f"Middle is {v[mid]}: found at position {mid}.", span(v, lo, hi, mid, {mid: "answer"}), result=mid)
            break
        W.step(f"Middle is {v[mid]} {'<' if v[mid] < t else '>'} {t}: keep the {'right' if v[mid] < t else 'left'} half.", span(v, lo, hi, mid))
        if v[mid] < t:
            lo = mid + 1
        else:
            hi = mid - 1
    if res == -1:
        W.step("The range is empty: not found.", Row(v), result=-1)
    W.intro(f"Looking for {t}. The whole list is in range: lo at the start, hi at the end.", span(v, 0, len(v) - 1))
    assert res == exp
    return W.save()


@run
def perfect_square_tiles(pid):
    a, exp = example(pid)
    x = a["tiles"]
    W = Walk(pid, f"Search for a side length r with r × r = {x}: too big squares send hi down, too small send lo up.")
    lo, hi, found = 1, x, False
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        W.step(f"Try side {mid}: {mid} × {mid} = {sq} {'=' if sq == x else '<' if sq < x else '>'} {x}.", Vars(lo=lo, mid=mid, hi=hi, square=sq))
        if sq == x:
            found = True
            break
        if sq < x:
            lo = mid + 1
        else:
            hi = mid - 1
    W.step("A perfect square." if found else "No whole side length fits exactly.", Vars(answer=found), result=found)
    assert found == exp
    return W.save()


@run
def square_floor(pid):
    a, exp = example(pid)
    x = a["x"]
    W = Walk(pid, f"Find the largest r with r × r ≤ {x}.")
    r = largest_ok(W, 0, x, lambda m: m * m <= x, lambda lo, hi, m, g: (f"{m} × {m} = {m * m} {'≤' if g else '>'} {x}: {'r can be at least ' + str(m) if g else 'r is below ' + str(m)}.", [Vars(lo=lo, mid=m, hi=hi)]))
    W.step(f"lo and hi meet at {r}.", Vars(answer=r), result=r)
    assert r == exp
    return W.save()


# ======================================================================== bounds

def lower_bound(W, v, t, label=None, say=True):
    lo, hi = 0, len(v)
    while lo < hi:
        mid = (lo + hi) // 2
        if say:
            W.step(f"v[{mid}] = {v[mid]} {'<' if v[mid] < t else '≥'} {t}: the first position ≥ {t} is {'after' if v[mid] < t else 'at or before'} {mid}.", span(v, lo, hi - 1, mid, label=label))
        if v[mid] < t:
            lo = mid + 1
        else:
            hi = mid
    return lo


@run
def insert_position(pid):
    a, exp = example(pid)
    v, t = a["scores"], a["target"]
    W = Walk(pid, f"Find the first position whose score is ≥ {t}: that's where {t} is, or where it would go.")
    p = lower_bound(W, v, t)
    W.step(f"Position {p}.", Row(v, st={p: "answer"} if p < len(v) else {}), result=p)
    assert p == exp
    return W.save()


@run
def first_and_last_delivery(pid):
    a, exp = example(pid)
    v, t = a["times"], a["target"]
    W = Walk(pid, f"Two searches: the first position ≥ {t}, and the first position ≥ {t + 1}. The answer is between them.")
    first = lower_bound(W, v, t)
    W.step(f"First position ≥ {t}: {first}.", Row(v, st={first: "found"} if first < len(v) else {}))
    after = lower_bound(W, v, t + 1)
    res = [first, after - 1] if first < len(v) and v[first] == t else [-1, -1]
    W.step(f"First position ≥ {t + 1}: {after}, so {t} runs from {res[0]} to {res[1]}." if res[0] != -1 else f"{t} isn't there.", Row(v, st={i: "answer" for i in range(first, after)} if res[0] != -1 else {}), result=res)
    assert res == exp
    return W.save()


@run
def next_gate_letter(pid):
    a, exp = example(pid)
    g, c = a["gates"], a["current"]
    W = Walk(pid, f"Find the first gate letter strictly after \"{c}\". If every letter is ≤ \"{c}\", wrap around to the first gate.")
    v = list(g)
    lo, hi = 0, len(v)
    while lo < hi:
        mid = (lo + hi) // 2
        W.step(f"\"{v[mid]}\" is {'after' if v[mid] > c else 'not after'} \"{c}\".", span(v, lo, hi - 1, mid))
        if v[mid] <= c:
            lo = mid + 1
        else:
            hi = mid
    res = v[lo % len(v)]
    W.step(f"The answer is \"{res}\"" + (" (wrapped around)." if lo == len(v) else "."), Row(v, st={lo % len(v): "answer"}), result=res)
    assert res == exp
    return W.save()


@run
def scores_in_range(pid):
    a, exp = example(pid)
    v = sorted(a["scores"])
    W = Walk(pid, "Sort once. Then each query is two binary searches: the first score ≥ lo and the first score > hi.")
    W.step("Sorted scores: " + ", ".join(map(str, v)) + ".", Row(v))
    out = []
    import bisect
    for lo, hi in a["queries"]:
        i, j = bisect.bisect_left(v, lo), bisect.bisect_right(v, hi)
        out.append(j - i)
        W.step(f"Query [{lo}, {hi}]: positions {i} to {j - 1}, so {j - i} score{'s' if j - i != 1 else ''}.", Row(v, st={k: "answer" for k in range(i, j)}, ptr={"first": i if i < len(v) else None, "past": j if j < len(v) else None}), result=j - i)
    assert out == exp
    return W.save()


@run
def closest_prices(pid):
    a, exp = example(pid)
    v, k, x = a["prices"], a["k"], a["x"]
    W = Walk(pid, f"Binary search the START of the {k}-price window: compare how far x is from the window's left end and from the price just past its right end.")
    lo, hi = 0, len(v) - k
    while lo < hi:
        mid = (lo + hi) // 2
        right_better = x - v[mid] > v[mid + k] - x
        W.step(f"Window at {mid}: x − {v[mid]} = {x - v[mid]} vs {v[mid + k]} − x = {v[mid + k] - x}. {'Slide right' if right_better else 'Keep it or go left'}.", Row(v, st={**{i: "active" for i in range(mid, mid + k)}, mid + k: "mark"}, ptr={"start": mid}))
        if right_better:
            lo = mid + 1
        else:
            hi = mid
    res = v[lo:lo + k]
    W.step(f"The window starts at {lo}.", Row(v, st={i: "answer" for i in range(lo, lo + k)}), result=res)
    W.intro(f"The answer is {k} prices in a row. Its start can be anywhere from 0 to {len(v) - k}.", Row(v, st={i: "found" for i in range(len(v) - k + 1)}, ptr={"x": next((i for i, p in enumerate(v) if p >= x), None)}))
    assert res == exp
    return W.save()


# ======================================================================== rotated-array

@run
def rotated_playlist(pid):
    a, exp = example(pid)
    v, t = a["playlist"], a["target"]
    W = Walk(pid, "One half around the middle is always sorted. Check whether the target lies in that sorted half; if not, it's in the other.")
    lo, hi, res = 0, len(v) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if v[mid] == t:
            res = mid
            W.step(f"Middle is {t}: found at {mid}.", span(v, lo, hi, mid, {mid: "answer"}), result=mid)
            break
        if v[lo] <= v[mid]:
            inside = v[lo] <= t < v[mid]
            W.step(f"The left half {v[lo]}…{v[mid]} is sorted; {t} is {'inside it' if inside else 'not in it'}.", span(v, lo, hi, mid))
            if inside:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            inside = v[mid] < t <= v[hi]
            W.step(f"The right half {v[mid]}…{v[hi]} is sorted; {t} is {'inside it' if inside else 'not in it'}.", span(v, lo, hi, mid))
            if inside:
                lo = mid + 1
            else:
                hi = mid - 1
    assert res == exp
    return W.save()


@run
def rotation_low_point(pid):
    a, exp = example(pid)
    v = a["readings"]
    W = Walk(pid, "Compare the middle with the right end: if the middle is bigger, the drop is to its right; otherwise it's at the middle or to its left.")
    lo, hi = 0, len(v) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        W.step(f"{v[mid]} {'>' if v[mid] > v[hi] else '<'} {v[hi]}: the low point is {'right of' if v[mid] > v[hi] else 'at or left of'} {mid}.", span(v, lo, hi, mid))
        if v[mid] > v[hi]:
            lo = mid + 1
        else:
            hi = mid
    W.step(f"The low point is {v[lo]}.", Row(v, st={lo: "answer"}), result=v[lo])
    assert v[lo] == exp
    return W.save()


@run
def low_point_with_repeats(pid):
    a, exp = example(pid)
    v = a["readings"]
    W = Walk(pid, "Same as without repeats, except when the middle EQUALS the right end: then you can only safely drop the right end.")
    lo, hi = 0, len(v) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if v[mid] > v[hi]:
            W.step(f"{v[mid]} > {v[hi]}: go right.", span(v, lo, hi, mid))
            lo = mid + 1
        elif v[mid] < v[hi]:
            W.step(f"{v[mid]} < {v[hi]}: the low point is at or left of the middle.", span(v, lo, hi, mid))
            hi = mid
        else:
            W.step(f"{v[mid]} = {v[hi]}: can't tell which side; drop the right end.", span(v, lo, hi, mid))
            hi -= 1
    W.step(f"The low point is {v[lo]}.", Row(v, st={lo: "answer"}), result=v[lo])
    assert v[lo] == exp
    return W.save()


@run
def rotated_with_repeats(pid):
    a, exp = example(pid)
    v, t = a["shelf"], a["target"]
    W = Walk(pid, "Find the sorted half as usual; when both ends equal the middle, shrink both ends by one.")
    lo, hi, found = 0, len(v) - 1, False
    while lo <= hi:
        mid = (lo + hi) // 2
        if v[mid] == t:
            found = True
            W.step(f"Middle is {t}: found.", span(v, lo, hi, mid, {mid: "answer"}), result=True)
            break
        if v[lo] == v[mid] == v[hi]:
            W.step("Both ends equal the middle: shrink both ends.", span(v, lo, hi, mid))
            lo += 1
            hi -= 1
        elif v[lo] <= v[mid]:
            inside = v[lo] <= t < v[mid]
            W.step(f"The left half is sorted; {t} is {'inside' if inside else 'not inside'}.", span(v, lo, hi, mid))
            if inside:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            inside = v[mid] < t <= v[hi]
            W.step(f"The right half is sorted; {t} is {'inside' if inside else 'not inside'}.", span(v, lo, hi, mid))
            if inside:
                lo = mid + 1
            else:
                hi = mid - 1
    if not found:
        W.step("Not on the shelf.", Row(v), result=False)
    W.intro(f"Looking for {t}. The shelf is sorted but rotated, and ids can repeat.", span(v, 0, len(v) - 1))
    assert found == exp
    return W.save()


# ======================================================================== peak-finding

def climb(W, v):
    lo, hi = 0, len(v) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        up = v[mid] < v[mid + 1]
        W.step(f"{v[mid]} {'<' if up else '>'} {v[mid + 1]}: the trail is {'still rising, so a top is to the right' if up else 'falling, so a top is at or left of the middle'}.", span(v, lo, hi, mid, {mid + 1: "mark"}))
        if up:
            lo = mid + 1
        else:
            hi = mid
    return lo


@run
def mountain_top(pid):
    a, exp = example(pid)
    v = a["elevations"]
    W = Walk(pid, "Compare each middle point with the next one: rising means the top is further right.")
    top = climb(W, v)
    W.step(f"The top is at {top}.", Row(v, st={top: "answer"}), result=top)
    assert top == exp
    return W.save()


@run
def any_summit(pid):
    a, exp = example(pid)
    v = a["heights"]
    W = Walk(pid, "Walk uphill by halves: if the next point is higher, a summit must lie that way.")
    top = climb(W, v)
    W.step(f"Index {top} is a summit.", Row(v, st={top: "answer"}), result=top)
    assert v[top] == v[exp] or top == exp
    return W.save()


@run
def mountain_lookups(pid):
    a, exp = example(pid)
    v = a["elevations"]
    W = Walk(pid, "Find the top once. Then search the rising side first (it holds the smaller index), then the falling side in reverse order.")
    top = climb(W, v)
    W.step(f"Top at {top}.", Row(v, st={top: "mark"}))
    out = []
    import bisect
    for t in a["targets"]:
        i = bisect.bisect_left(v, t, 0, top + 1)
        if i <= top and v[i] == t:
            res = i
        else:
            down = [-x for x in v[top:]]
            j = bisect.bisect_left(down, -t)
            res = top + j if j < len(down) and down[j] == -t else -1
        out.append(res)
        W.step(f"{t}: " + (f"found at {res}." if res != -1 else "not on the mountain."), Row(v, st={**{top: "mark"}, **({res: "answer"} if res != -1 else {})}), result=res)
    assert out == exp
    return W.save()


# ======================================================================== kth-element

@run
def kth_free_number(pid):
    a, exp = example(pid)
    v, k = a["taken"], a["k"]
    W = Walk(pid, "Before taken[i], exactly taken[i] − (i + 1) numbers are free. Binary search the first i where that reaches k.")
    free = [x - (i + 1) for i, x in enumerate(v)]
    W.step("Free numbers before each taken one.", Row(v, label="taken"), Row(free, label="free before it"))
    lo, hi = 0, len(v)
    while lo < hi:
        mid = (lo + hi) // 2
        W.step(f"{free[mid]} free before {v[mid]}: {'≥' if free[mid] >= k else '<'} {k}.", span(v, lo, hi - 1, mid, label="taken"), Row(free, label="free before it"))
        if free[mid] >= k:
            hi = mid
        else:
            lo = mid + 1
    res = k + lo
    W.step(f"{lo} taken numbers come before the answer, so it's {k} + {lo} = {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def kth_in_times_table(pid):
    a, exp = example(pid)
    r, c, k = a["rows"], a["cols"], a["k"]
    W = Walk(pid, f"Binary search the VALUE. For a guess v, row i holds min(v // i, {c}) numbers ≤ v; find the smallest v with at least {k}.")
    grid = [[i * j for j in range(1, c + 1)] for i in range(1, r + 1)] if r * c <= 64 else None

    def count(v):
        return sum(min(v // i, c) for i in range(1, r + 1))

    def show(lo, hi, m, good):
        panels = [Vars(lo=lo, guess=m, hi=hi, count=count(m))]
        if grid:
            panels.insert(0, Grid(grid, st={(i, j): "found" for i in range(r) for j in range(c) if grid[i][j] <= m}))
        return f"{count(m)} numbers are ≤ {m}: {'enough' if good else 'too few'}.", panels

    res = smallest_ok(W, 1, r * c, lambda m: count(m) >= k, show)
    W.step(f"The {k}-th smallest is {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def kth_of_two_lists(pid):
    a, exp = example(pid)
    x, y, k = a["a"], a["b"], a["k"]
    W = Walk(pid, f"Take i values from a and k − i from b. The right i is where both cuts line up: every value before the cuts is ≤ every value after them.")
    lo, hi = max(0, k - len(y)), min(k, len(x))
    INF = float("inf")
    while lo <= hi:
        i = (lo + hi) // 2
        j = k - i
        al = x[i - 1] if i else -INF
        ar = x[i] if i < len(x) else INF
        bl = y[j - 1] if j else -INF
        br = y[j] if j < len(y) else INF
        if al > br:
            text, nxt = f"Taking {i} from a: {al} > {br}, too many from a.", ("hi", i - 1)
        elif bl > ar:
            text, nxt = f"Taking {i} from a: {bl} > {ar}, too few from a.", ("lo", i + 1)
        else:
            res = max(al, bl)
            W.step(f"Taking {i} from a and {j} from b lines up. The {k}-th value is the larger of the last ones taken: {res}.",
                   Row(x, st={t: "found" for t in range(i)}, ptr={"cut": i if i < len(x) else None}, label="a"), Row(y, st={t: "found" for t in range(j)}, ptr={"cut": j if j < len(y) else None}, label="b"), result=res)
            break
        W.step(text, Row(x, st={t: "found" for t in range(i)}, ptr={"cut": i if i < len(x) else None}, label="a"), Row(y, st={t: "found" for t in range(j)}, ptr={"cut": j if j < len(y) else None}, label="b"))
        if nxt[0] == "hi":
            hi = nxt[1]
        else:
            lo = nxt[1]
    W.intro(f"The answer uses some i values from a (between {max(0, k - len(y))} and {min(k, len(x))}) and the rest from b.", Row(x, label="a"), Row(y, label="b"), Vars(k=k))
    assert res == exp
    return W.save()


@run
def median_of_two_queues(pid):
    a, exp = example(pid)
    x, y = a["a"], a["b"]
    if len(x) > len(y):
        x, y = y, x
    total = len(x) + len(y)
    half = (total + 1) // 2
    W = Walk(pid, f"Cut both lists so the left parts hold {half} values in total and everything left ≤ everything right. The median sits at the cut.")
    lo, hi = 0, len(x)
    INF = float("inf")
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i
        al = x[i - 1] if i else -INF
        ar = x[i] if i < len(x) else INF
        bl = y[j - 1] if j else -INF
        br = y[j] if j < len(y) else INF
        panels = [Row(x, st={t: "found" for t in range(i)}, ptr={"cut": i if i < len(x) else None}), Row(y, st={t: "found" for t in range(j)}, ptr={"cut": j if j < len(y) else None})]
        if al > br:
            W.step(f"{i} from the shorter list: {al} > {br}, move the cut left.", *panels)
            hi = i - 1
        elif bl > ar:
            W.step(f"{i} from the shorter list: {bl} > {ar}, move the cut right.", *panels)
            lo = i + 1
        else:
            med = max(al, bl) if total % 2 else (max(al, bl) + min(ar, br)) / 2
            W.step(f"The cuts line up. Median = {fmt(med)}.", *panels, result=med)
            break
    W.intro(f"{total} waiting times in all, so the left side of the cut holds {half}.", Row(x, label="shorter list"), Row(y, label="longer list"))
    assert abs(med - exp) < 1e-9
    return W.save()


# ======================================================================== matrix-search

@run
def seat_map_lookup(pid):
    a, exp = example(pid)
    g, t = a["rows"], a["target"]
    m, n = len(g), len(g[0])
    W = Walk(pid, "Read the grid as one sorted list of m × n seats: position p is row p // n, column p % n.")
    lo, hi, found = 0, m * n - 1, False
    while lo <= hi:
        mid = (lo + hi) // 2
        r, c = divmod(mid, n)
        v = g[r][c]
        st = {(p // n, p % n): "dim" for p in range(m * n) if p < lo or p > hi}
        if v == t:
            found = True
            st[(r, c)] = "answer"
            W.step(f"Position {mid} is row {r}, column {c}: {v}. Found.", Grid(g, st), result=True)
            break
        st[(r, c)] = "active"
        W.step(f"Position {mid} is row {r}, column {c}: {v} {'<' if v < t else '>'} {t}.", Grid(g, st))
        if v < t:
            lo = mid + 1
        else:
            hi = mid - 1
    if not found:
        W.step("Not found.", Grid(g), result=False)
    assert found == exp
    return W.save()


@run
def staircase_search(pid):
    a, exp = example(pid)
    g, t = a["grid"], a["target"]
    W = Walk(pid, "Start at the top-right corner. Too big → step left (the whole column is bigger); too small → step down (the whole row is smaller).")
    r, c = 0, len(g[0]) - 1
    gone = {}
    found = False
    while r < len(g) and c >= 0:
        v = g[r][c]
        if v == t:
            found = True
            W.step(f"{v}: found.", Grid(g, {**gone, (r, c): "answer"}), result=True)
            break
        W.step(f"{v} {'>' if v > t else '<'} {t}: {'rule out this column, step left' if v > t else 'rule out this row, step down'}.", Grid(g, {**gone, (r, c): "active"}))
        if v > t:
            for rr in range(len(g)):
                gone[(rr, c)] = "dim"
            c -= 1
        else:
            for cc in range(len(g[0])):
                gone[(r, cc)] = "dim"
            r += 1
    if not found:
        W.step("Walked off the grid: not there.", Grid(g, gone), result=False)
    assert found == exp
    return W.save()


@run
def kth_in_sorted_grid(pid):
    a, exp = example(pid)
    g, k = a["grid"], a["k"]
    n = len(g)
    W = Walk(pid, f"Binary search the value. Counting entries ≤ a guess takes one staircase walk, O(n). Find the smallest value with at least {k} entries ≤ it.")

    def count(v):
        r, c, total = n - 1, 0, 0
        while r >= 0 and c < n:
            if g[r][c] <= v:
                total += r + 1
                c += 1
            else:
                r -= 1
        return total

    def show(lo, hi, m, good):
        return f"{count(m)} entries are ≤ {m}: {'enough' if good else 'too few'}.", [Grid(g, {(i, j): "found" for i in range(n) for j in range(n) if g[i][j] <= m}), Vars(lo=lo, guess=m, hi=hi)]

    res = smallest_ok(W, g[0][0], g[-1][-1], lambda m: count(m) >= k, show)
    W.step(f"The {k}-th smallest is {res}.", Grid(g, {(i, j): "answer" for i in range(n) for j in range(n) if g[i][j] == res}), result=res)
    assert res == exp
    return W.save()


# ======================================================================== search-on-answer

@run
def reading_speed(pid):
    a, exp = example(pid)
    b, h = a["books"], a["hours"]
    W = Walk(pid, f"Binary search the speed. A speed works if the hours needed (each book rounded up) total at most {h}.")

    def hours(s):
        return [-(-x // s) for x in b]

    res = smallest_ok(W, 1, max(b), lambda s: sum(hours(s)) <= h,
                      lambda lo, hi, m, g: (f"Speed {m}: {sum(hours(m))} hours {'≤' if g else '>'} {h}.", [Row(b, label="pages"), Row(hours(m), st={i: ("found" if g else "mark") for i in range(len(b))}, label=f"hours at {m}/h"), Vars(lo=lo, hi=hi)]))
    W.step(f"The slowest speed that works is {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def smallest_divisor(pid):
    a, exp = example(pid)
    v, t = a["loads"], a["threshold"]
    W = Walk(pid, f"Bigger divisors give smaller totals, so binary search the smallest d whose rounded-up total is ≤ {t}.")
    res = smallest_ok(W, 1, max(v), lambda d: sum(-(-x // d) for x in v) <= t,
                      lambda lo, hi, m, g: (f"d = {m}: total {sum(-(-x // m) for x in v)} {'≤' if g else '>'} {t}.", [Row(v, label="loads"), Row([-(-x // m) for x in v], label=f"÷ {m}, rounded up"), Vars(lo=lo, hi=hi)]))
    W.step(f"The smallest divisor is {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def print_shop_daily_limit(pid):
    a, exp = example(pid)
    p, days = a["pages"], a["days"]
    W = Walk(pid, f"Binary search the daily limit between the biggest job and all pages. For a limit, fill days greedily and count them.")

    def plan(cap):
        day, used, which = 1, 0, []
        for x in p:
            if used + x > cap:
                day += 1
                used = 0
            used += x
            which.append(day)
        return which

    res = smallest_ok(W, max(p), sum(p), lambda cap: plan(cap)[-1] <= days,
                      lambda lo, hi, m, g: (f"Limit {m}: needs {plan(m)[-1]} day{'s' if plan(m)[-1] != 1 else ''} {'≤' if g else '>'} {days}.", [Row(p, label="pages"), Row(plan(m), label=f"day for each job at limit {m}"), Vars(lo=lo, hi=hi)]))
    W.step(f"The smallest limit is {res}.", Row(p, label="pages"), Row(plan(res), label="day for each job"), result=res)
    assert res == exp
    return W.save()


@run
def spread_the_sensors(pid):
    a, exp = example(pid)
    s, k = sorted(a["spots"]), a["sensors"]
    W = Walk(pid, f"Binary search the gap. For a gap g, place sensors greedily from the left, each at the first spot at least g past the last one.")

    def placed(g):
        out, last = [], None
        for i, x in enumerate(s):
            if last is None or x - last >= g:
                out.append(i)
                last = x
        return out

    res = largest_ok(W, 1, s[-1] - s[0], lambda g: len(placed(g)) >= k,
                     lambda lo, hi, m, g: (f"Gap {m}: greedy places {len(placed(m))} sensor{'s' if len(placed(m)) != 1 else ''}, {'enough' if g else 'too few'}.", [Row(s, st={i: ("found" if g else "mark") for i in placed(m)}, label="spots"), Vars(lo=lo, hi=hi)]))
    W.step(f"The largest smallest gap is {res}.", Row(s, st={i: "answer" for i in placed(res)[:k]}), result=res)
    assert res == exp
    return W.save()


@run
def nth_beat(pid):
    a, exp = example(pid)
    n, x, y = a["n"], a["a"], a["b"]
    from math import gcd
    l = x * y // gcd(x, y)
    W = Walk(pid, f"Beats up to v: v // {x} + v // {y} − v // {l} (shared beats counted once). Binary search the smallest v with at least {n}.")
    res = smallest_ok(W, 1, n * min(x, y), lambda v: v // x + v // y - v // l >= n,
                      lambda lo, hi, m, g: (f"Up to {m}: {m // x + m // y - m // l} beats, {'enough' if g else 'too few'}.", [Vars(lo=lo, guess=m, hi=hi)]))
    W.step(f"The {n}-th beat is {res}.", Vars(answer=res), result=res % (10**9 + 7))
    first = sorted({m for m in range(1, 13 * max(x, y)) if m % x == 0 or m % y == 0})[:10]
    W.intro(f"The first beats are {', '.join(map(str, first))}, …: too many to list for big n, so count instead.", Row(first, label="beats"))
    assert res % (10**9 + 7) == exp
    return W.save()


@run
def kth_closest_pair(pid):
    a, exp = example(pid)
    h, k = sorted(a["heights"]), a["k"]
    W = Walk(pid, f"Sort, then binary search the gap. Pairs with gap ≤ g are counted with a sliding window in O(n).")

    def count(g):
        c, left = 0, 0
        for i, x in enumerate(h):
            while x - h[left] > g:
                left += 1
            c += i - left
        return c

    res = smallest_ok(W, 0, h[-1] - h[0], lambda g: count(g) >= k, lambda lo, hi, m, g: (f"Gap ≤ {m}: {count(m)} pair{'s' if count(m) != 1 else ''}, {'enough' if g else 'too few'}.", [Row(h, label="sorted heights"), Vars(lo=lo, guess=m, hi=hi)]))
    W.step(f"The {k}-th smallest gap is {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def shuttle_rounds(pid):
    a, exp = example(pid)
    r, total = a["roundTime"], a["totalRounds"]
    W = Walk(pid, f"In t minutes shuttle i finishes t // roundTime[i] rounds. Binary search the smallest t with at least {total} rounds.")
    res = smallest_ok(W, 1, min(r) * total, lambda t: sum(t // x for x in r) >= total,
                      lambda lo, hi, m, g: (f"{m} minutes: {sum(m // x for x in r)} rounds, {'enough' if g else 'too few'}.", [Row(r, label="minutes per round"), Row([m // x for x in r], label=f"rounds in {m} min"), Vars(lo=lo, hi=hi)]))
    W.step(f"{res} minutes.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def bouquet_day(pid):
    a, exp = example(pid)
    b, want, size = a["bloom"], a["bouquets"], a["size"]
    W = Walk(pid, f"Binary search the day. On a given day, walk the row counting runs of bloomed flowers; each {size} in a row make a bouquet.")
    if want * size > len(b):
        W.step("Not enough flowers at all.", Row(b), result=-1)
        assert exp == -1
        return W.save()

    def made(d):
        run_, out = 0, 0
        for x in b:
            run_ = run_ + 1 if x <= d else 0
            if run_ == size:
                out += 1
                run_ = 0
        return out

    res = smallest_ok(W, min(b), max(b), lambda d: made(d) >= want,
                      lambda lo, hi, m, g: (f"Day {m}: {made(m)} bouquet{'s' if made(m) != 1 else ''}, {'enough' if g else 'too few'}.", [Row(b, st={i: "found" for i, x in enumerate(b) if x <= m}, label="bloom day"), Vars(lo=lo, hi=hi)]))
    W.step(f"Earliest day: {res}.", Row(b, st={i: "answer" for i, x in enumerate(b) if x <= res}, label="bloom day"), result=res)
    assert res == exp
    return W.save()


# ======================================================================== real-valued

def real_search(W, lo, hi, ok, show, rounds=50, every=8):
    for it in range(rounds):
        mid = (lo + hi) / 2
        good = ok(mid)
        if it % every == 0 or it < 4:
            W.step(*show(lo, hi, mid, good))
        if good:
            lo = mid
        else:
            hi = mid
    return lo


@run
def rope_pieces(pid):
    a, exp = example(pid)
    ropes, k = a["ropes"], a["pieces"]
    W = Walk(pid, f"Binary search the length on real numbers: a length works if the ropes give at least {k} pieces. Stop when the range is tiny.")
    res = real_search(W, 0, max(ropes), lambda L_: sum(int(x // L_) for x in ropes) >= k,
                      lambda lo, hi, m, g: (f"Length {m:.4f}: {sum(int(x // m) for x in ropes)} pieces, {'works' if g else 'too long'}.", Vars(lo=f"{lo:.4f}", hi=f"{hi:.4f}")))
    W.step(f"The range closes on {res:.6f}.", Vars(answer=f"{res:.6f}"), result=round(res, 6))
    assert abs(res - exp) < 1e-5
    return W.save()


@run
def cube_root(pid):
    a, exp = example(pid)
    v = a["volume"]
    W = Walk(pid, "Binary search r between −max(1, |v|) and max(1, |v|): if r³ is too small, go up; otherwise go down.")
    m = max(1.0, abs(v))
    res = real_search(W, -m, m, lambda r: r * r * r <= v, lambda lo, hi, r, g: (f"{r:.4f}³ = {r ** 3:.4f} {'≤' if g else '>'} {v}.", Vars(lo=f"{lo:.4f}", hi=f"{hi:.4f}")), rounds=100, every=12)
    W.step(f"The cube root is {res:.6f}.", Vars(answer=f"{res:.6f}"), result=round(res, 6))
    assert abs(res - exp) < 1e-5
    return W.save()


@run
def charging_stations(pid):
    a, exp = example(pid)
    s, extra = a["stations"], a["extra"]
    gaps = [b - a_ for a_, b in zip(s, s[1:])]
    W = Walk(pid, f"Binary search the largest gap D. Each gap g needs ⌈g / D⌉ − 1 new stations; D works if they add up to at most {extra}.")
    import math

    def need(D):
        return sum(math.ceil(g / D) - 1 for g in gaps)

    res = real_search(W, 0, max(gaps), lambda D: need(D) > extra, lambda lo, hi, D, g: (f"D = {D:.4f} needs {need(D)} new stations: {'too many' if g else 'fits'}.", Vars(lo=f"{lo:.4f}", hi=f"{hi:.4f}")))
    res = (res + 0)  # lo converges to the answer from below
    W.step(f"The smallest largest gap is {res:.6f}.", Vars(answer=f"{res:.6f}"), result=round(res, 6))
    assert abs(res - exp) < 1e-5
    return W.save()


# ======================================================================== unknown-size

@run
def zeros_at_the_end(pid):
    a, exp = example(pid)
    z = a["zeros"]
    W = Walk(pid, f"n! ends with n//5 + n//25 + n//125 + … zeros. Double n until it has at least {z}, then binary search between the last two guesses.")

    def zs(n):
        c, p = 0, 5
        while p <= n:
            c += n // p
            p *= 5
        return c

    hi = 1
    while zs(hi) < z:
        W.step(f"{hi}! has {zs(hi)} zeros: double.", Vars(n=hi, zeros=zs(hi)))
        hi *= 2
    W.step(f"{hi}! has {zs(hi)} zeros: enough. Search between {hi // 2} and {hi}.", Vars(n=hi, zeros=zs(hi)))
    res = smallest_ok(W, hi // 2 if hi > 1 else 0, hi, lambda n: zs(n) >= z, lambda lo, h, m, g: (f"{m}! has {zs(m)} zeros: {'enough' if g else 'too few'}.", [Vars(lo=lo, mid=m, hi=h)]))
    W.step(f"The smallest n is {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def stack_of_cans(pid):
    a, exp = example(pid)
    c = a["cans"]
    W = Walk(pid, f"A stack of r rows holds r(r + 1)/2 cans. Double r until it holds {c}, then binary search.")
    hold = lambda r: r * (r + 1) // 2
    hi = 1
    while hold(hi) < c:
        W.step(f"{hi} rows hold {hold(hi)}: double.", Vars(rows=hi, cans=hold(hi)))
        hi *= 2
    W.step(f"{hi} rows hold {hold(hi)}: enough. Search between {hi // 2} and {hi}.", Vars(rows=hi, cans=hold(hi)))
    res = smallest_ok(W, max(1, hi // 2), hi, lambda r: hold(r) >= c, lambda lo, h, m, g: (f"{m} rows hold {hold(m)}: {'enough' if g else 'too few'}.", [Vars(lo=lo, mid=m, hi=h)]))
    W.step(f"{res} rows.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
