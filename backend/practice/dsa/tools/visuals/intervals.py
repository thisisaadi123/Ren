import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from bisect import bisect_left, bisect_right
from collections import Counter
from lib import *

DONE = []
CUSTOM = {
    "total-covered-length": [{"strips": [[1, 4], [2, 6], [8, 9], [7, 8], [12, 15]]}],
    "most-talks": [{"talks": [[0, 10], [1, 2], [2, 3], [3, 4], [5, 7], [6, 8]]}],
    "calendars-clash": [{"a": [[1, 3], [5, 8], [10, 12]], "b": [[3, 5], [8, 10], [11, 14]]}],
    "cut-a-range": [{"slots": [[0, 2], [3, 4], [5, 7], [8, 9]], "cut": [1, 6]}],
}
run = make_runner(DONE, CUSTOM)


def iv(xs):
    return [f"{s}–{e}" for s, e in xs]


def merge_steps(W, xs, join, say_join, say_new, key=None):
    out = []
    order = sorted(xs, key=key) if key else sorted(xs)
    W.step("Sort by start.", Row(iv(order), label="sorted"))
    for i, (s, e) in enumerate(order):
        if out and join(out[-1], s):
            out[-1][1] = max(out[-1][1], e)
            W.step(say_join(s, e, out[-1]), Row(iv(order), st={i: "active"}, label="sorted"), Row(iv(out), st={len(out) - 1: "new"}, label="merged"))
        else:
            out.append([s, e])
            W.step(say_new(s, e), Row(iv(order), st={i: "active"}, label="sorted"), Row(iv(out), st={len(out) - 1: "new"}, label="merged"))
    return out


@run
def combine_bookings(pid):
    a, exp = example(pid)
    W = Walk(pid, "Sort by start; each booking either stretches the last merged one or starts a new one.")
    out = merge_steps(W, a["bookings"], lambda last, s: s <= last[1], lambda s, e, m: f"{s}–{e} starts by {m[1]}: stretch the merged booking to {m[0]}–{m[1]}.", lambda s, e: f"{s}–{e} starts after the last one ends: new booking.")
    assert out == exp
    return W.save()


@run
def total_covered_length(pid):
    a, exp = example(pid)
    W = Walk(pid, "Merge overlapping strips, then add up the merged lengths so overlaps count once.")
    out = merge_steps(W, a["strips"], lambda last, s: s <= last[1], lambda s, e, m: f"{s}–{e} overlaps: the painted stretch grows to {m[0]}–{m[1]}.", lambda s, e: f"{s}–{e} is a new painted stretch.")
    total = sum(e - s for s, e in out)
    W.step(f"Total: {' + '.join(str(e - s) for s, e in out)} = {total}.", Row(iv(out), label="merged"), result=total)
    assert total == exp
    return W.save()


@run
def merge_within_reach(pid):
    a, exp = example(pid)
    g = a["gap"]
    W = Walk(pid, f"Sort by start; a shift joins the current block when its start is at most the block's end + {g}.")
    out = merge_steps(W, a["shifts"], lambda last, s: s - last[1] <= g, lambda s, e, m: f"{s}–{e}: the break is short enough, so the block becomes {m[0]}–{m[1]}.", lambda s, e: f"{s}–{e}: the break is longer than {g}, so a new block.")
    assert out == exp
    return W.save()


@run
def slot_in_a_booking(pid):
    a, exp = example(pid)
    b, (s, e) = a["bookings"], a["extra"]
    W = Walk(pid, f"Copy bookings that end before {s}, merge everything that overlaps {s}–{e}, then copy the rest.")
    out, i = [], 0
    while i < len(b) and b[i][1] < s:
        out.append(b[i])
        W.step(f"{b[i][0]}–{b[i][1]} ends before {s}: copy it.", Row(iv(b), st={i: "found"}, label="bookings"), Row(iv(out), label="result"))
        i += 1
    while i < len(b) and b[i][0] <= e:
        s, e = min(s, b[i][0]), max(e, b[i][1])
        W.step(f"{b[i][0]}–{b[i][1]} overlaps or touches: the new booking grows to {s}–{e}.", Row(iv(b), st={i: "active"}, label="bookings"), Row(iv(out + [[s, e]]), st={len(out): "new"}, label="result"))
        i += 1
    out.append([s, e])
    W.step(f"Place {s}–{e}, then copy the rest.", Row(iv(b), st={k: "found" for k in range(i, len(b))}, label="bookings"), Row(iv(out + b[i:]), st={len(out) - 1: "new"}, label="result"))
    out += b[i:]
    assert out == exp
    return W.save()


@run
def cut_a_range(pid):
    a, exp = example(pid)
    sl, (x, y) = a["slots"], a["cut"]
    W = Walk(pid, f"Each slot keeps whatever lies before {x} and after {y}; slots outside the cut stay whole.")
    out = []
    for i, (s, e) in enumerate(sl):
        if e <= x or s >= y:
            out.append([s, e])
            text = f"{s}–{e} misses the cut: keep it."
        else:
            kept = []
            if s < x:
                kept.append([s, x])
            if y < e:
                kept.append([y, e])
            out += kept
            text = f"{s}–{e} overlaps the cut: keep " + (", ".join(f"{p}–{q}" for p, q in kept) if kept else "nothing") + "."
        W.step(text, Row(iv(sl), st={i: "active"}, label=f"slots (cut {x}–{y})"), Row(iv(out), label="result"))
    assert out == exp
    return W.save()


@run
def rooms_needed(pid):
    a, exp = example(pid)
    m = a["meetings"]
    starts = sorted(s for s, _ in m)
    ends = sorted(e for _, e in m)
    W = Walk(pid, "Sort starts and ends separately. Before each start, free every room whose meeting has ended; the peak number of rooms in use is the answer.")
    j = used = best = 0
    for i, s in enumerate(starts):
        freed = 0
        while ends[j] <= s:
            j += 1
            used -= 1
            freed += 1
        used += 1
        best = max(best, used)
        W.step(f"Meeting starts at {s}" + (f"; {freed} room{'s' if freed > 1 else ''} freed first" if freed else "") + f". In use: {used}. Peak {best}.",
               Row(starts, st={i: "active"}, label="starts"), Row(ends, st={k: "dim" for k in range(j)}, ptr={"next end": j if j < len(ends) else None}, label="ends"), Vars(rooms=used, peak=best))
    assert best == exp
    return W.save()


@run
def busiest_moment(pid):
    a, exp = example(pid)
    ev = Counter()
    for s, e in a["visits"]:
        ev[s] += 1
        ev[e + 1] -= 1
    times = sorted(ev)
    W = Walk(pid, "A visit adds +1 at arrival and −1 the minute after leaving. Sweep the event times in order.")
    W.step("Events (time: change).", Row([f"{t}:{ev[t]:+d}" for t in times], label="events"))
    cur = best = 0
    at = None
    for i, t in enumerate(times):
        cur += ev[t]
        if cur > best:
            best, at = cur, t
        W.step(f"At minute {t}: {cur} inside. Busiest so far: {best} at minute {at}.", Row([f"{x}:{ev[x]:+d}" for x in times], st={i: "active"}, label="events"), Vars(inside=cur, best=best))
    assert at == exp
    return W.save()


@run
def lamps_at_each_spot(pid):
    a, exp = example(pid)
    starts = sorted(s for s, _ in a["lamps"])
    ends = sorted(e for _, e in a["lamps"])
    W = Walk(pid, "Lit lamps at p = (lamps started by p) − (lamps that ended before p). Two binary searches in the sorted starts and ends.")
    out = []
    for p in a["spots"]:
        on, off = bisect_right(starts, p), bisect_left(ends, p)
        out.append(on - off)
        W.step(f"Spot {p}: {on} started, {off} ended before it, so {on - off} lit.", Row(starts, st={k: "found" for k in range(on)}, label="starts"), Row(ends, st={k: "dim" for k in range(off)}, label="ends"), result=on - off)
    assert out == exp
    return W.save()


def by_end_steps(W, xs, ok, keep_text, skip_text):
    order = sorted(xs, key=lambda t: t[1])
    W.step("Sort by end time.", Row(iv(order), label="by end"))
    free, kept = None, []
    for i, (s, e) in enumerate(order):
        if ok(free, s):
            kept.append(i)
            W.step(keep_text(s, e, free), Row(iv(order), st={**{k: "found" for k in kept[:-1]}, i: "answer"}, label="by end"))
            free = e
        else:
            W.step(skip_text(s, e, free), Row(iv(order), st={**{k: "found" for k in kept}, i: "mark"}, label="by end"))
    return len(kept), len(order) - len(kept)


@run
def most_talks(pid):
    a, exp = example(pid)
    W = Walk(pid, "Always take the talk that ends first among those you can still reach: it leaves the most time for the rest.")
    k, _ = by_end_steps(W, a["talks"], lambda f, s: f is None or s >= f, lambda s, e, f: f"{s}–{e} starts after the last talk ends: attend.", lambda s, e, f: f"{s}–{e} starts before {f}: skip.")
    W.step(f"{k} talks.", Vars(answer=k), result=k)
    assert k == exp
    return W.save()


@run
def cancel_fewest_talks(pid):
    a, exp = example(pid)
    W = Walk(pid, "Keep as many talks as possible (earliest end first); everything else is cancelled.")
    k, cancel = by_end_steps(W, a["talks"], lambda f, s: f is None or s >= f, lambda s, e, f: f"{s}–{e} fits: keep it.", lambda s, e, f: f"{s}–{e} overlaps the last kept talk (ends {f}): cancel.")
    W.step(f"Cancel {cancel}.", Vars(cancelled=cancel), result=cancel)
    assert cancel == exp
    return W.save()


@run
def fewest_pins(pid):
    a, exp = example(pid)
    W = Walk(pid, "Sort by end. A pin at the first poster's end holds every poster starting at or before it; the next poster it misses needs a new pin.")
    k, _ = by_end_steps(W, a["posters"], lambda f, s: f is None or s > f, lambda s, e, f: f"{s}–{e} isn't held: pin it at {e}.", lambda s, e, f: f"{s}–{e} starts by {f}: the pin at {f} holds it.")
    W.step(f"{k} pins.", Vars(pins=k), result=k)
    assert k == exp
    return W.save()


@run
def shared_free_slots(pid):
    a, exp = example(pid)
    A, B = a["a"], a["b"]
    W = Walk(pid, "Two pointers. The overlap of the current slots is [max of starts, min of ends] when that's not empty; then move past whichever slot ends first.")
    i = j = 0
    out = []
    while i < len(A) and j < len(B):
        s, e = max(A[i][0], B[j][0]), min(A[i][1], B[j][1])
        if s <= e:
            out.append([s, e])
        W.step(f"{A[i][0]}–{A[i][1]} and {B[j][0]}–{B[j][1]}: " + (f"both free {s}–{e}." if s <= e else "no overlap.") + f" Move past the one ending first.",
               Row(iv(A), st={i: "active"}, label="a"), Row(iv(B), st={j: "active"}, label="b"), Row(iv(out), label="shared"))
        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1
    assert out == exp
    return W.save()


@run
def calendars_clash(pid):
    a, exp = example(pid)
    A, B = a["a"], a["b"]
    W = Walk(pid, "Walk both calendars together. Two events clash when each starts before the other ends; otherwise move past the one that ends first.")
    i = j = 0
    res = False
    while i < len(A) and j < len(B):
        clash = A[i][0] < B[j][1] and B[j][0] < A[i][1]
        W.step(f"{A[i][0]}–{A[i][1]} vs {B[j][0]}–{B[j][1]}: " + ("they clash." if clash else "no clash."), Row(iv(A), st={i: "mark" if clash else "active"}, label="a"), Row(iv(B), st={j: "mark" if clash else "active"}, label="b"), result=True if clash else None)
        if clash:
            res = True
            break
        if A[i][1] <= B[j][1]:
            i += 1
        else:
            j += 1
    if not res:
        W.step("One calendar ran out without a clash.", Vars(answer=False), result=False)
    assert res == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
