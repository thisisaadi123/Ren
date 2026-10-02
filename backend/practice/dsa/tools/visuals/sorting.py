import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
import heapq
from collections import Counter
from functools import cmp_to_key
from lib import *

DONE = []
CUSTOM = {
    "middle-reading": [{"readings": [7, -2, 4, 12, 9, 1, 15, 3, 8]}],
    "kth-highest-bid": [{"bids": [3, 2, 1, 5, 6, 4, 9, 7, 8], "k": 4}],
    "nesting-boxes": [{"boxes": [[5, 4], [6, 4], [6, 7], [2, 3], [1, 1], [7, 8]]}],
    "sort-the-scoreboard": [{"scores": [5, -2, 9, 0, 7, 3, -4, 6]}],
    "out-of-order-pairs": [{"ranks": [3, 1, 2, 6, 4, 5]}],
    "fewest-neighbour-swaps": [{"heights": [3, 1, 2, 5, 4]}],
    "big-drops": [{"prices": [5, 3, 2, 8, 1, 4]}],
    "shorter-behind": [{"heights": [5, 2, 6, 1, 3]}],
    "widest-gap-after-sorting": [{"nums": [3, 9, 1, 6, 15, 12]}],
    "sort-the-train-cars": [{"head": [4, 2, 1, 3, 7, 5]}],
    "sort-with-many-repeats": [{"readings": [4, 1, 4, 4, 1, 7, 3, 7, 4, 1, 9, 3]}],
}
run = make_runner(DONE, CUSTOM)


# ======================================================================== quickselect

def quickselect(W, v, target, describe):
    """Lomuto partitioning until position `target` holds its sorted value."""
    lo, hi = 0, len(v) - 1
    while True:
        pivot = v[hi]
        store = lo
        for i in range(lo, hi):
            if v[i] < pivot:
                v[i], v[store] = v[store], v[i]
                store += 1
        v[store], v[hi] = v[hi], v[store]
        W.step(f"Partition positions {lo}–{hi} around {pivot}: smaller values go left; {pivot} lands at {store}. " + describe(store, target),
               Row(v, st={**{i: "dim" for i in range(len(v)) if i < lo or i > hi}, **{i: "found" for i in range(lo, store)}, store: "active"}, ptr={"target": target}))
        if store == target:
            return v[store]
        if store < target:
            lo = store + 1
        else:
            hi = store - 1


@run
def middle_reading(pid):
    a, exp = example(pid)
    v = list(a["readings"])
    mid = len(v) // 2
    W = Walk(pid, f"Quickselect: partition around a pivot, then keep only the side that holds position {mid}, the middle.")
    W.step(f"{len(v)} readings: the median sits at sorted position {mid}.", Row(v, ptr={"target": mid}))
    res = quickselect(W, v, mid, lambda s, t: "That's the middle." if s == t else f"The middle is to the {'right' if s < t else 'left'}.")
    W.step(f"The median is {res}.", Row(v, st={mid: "answer"}), result=res)
    assert res == exp
    return W.save()


@run
def kth_highest_bid(pid):
    a, exp = example(pid)
    v, k = list(a["bids"]), a["k"]
    t = len(v) - k
    W = Walk(pid, f"The {k}-th highest is the value at sorted position {t}. Quickselect partitions until that position is settled.")
    W.step(f"Looking for sorted position {t}.", Row(v, ptr={"target": t}))
    res = quickselect(W, v, t, lambda s, tt: "Found it." if s == tt else f"Keep the {'right' if s < tt else 'left'} side.")
    W.step(f"The {k}-th highest bid is {res}.", Row(v, st={t: "answer"}), result=res)
    assert res == exp
    return W.save()


@run
def nearest_stations(pid):
    a, exp = example(pid)
    pts, k = a["stations"], a["k"]
    W = Walk(pid, f"Compare squared distances (no square roots needed), then keep the {k} smallest with quickselect; ties go by x, then y.")
    d = []
    for i, (x, y) in enumerate(pts):
        d.append(x * x + y * y)
        W.step(f"Station [{x}, {y}]: {x}² + {y}² = {d[-1]}.", Row([f"[{p[0]},{p[1]}]" for p in pts], st={i: "active"}, label="stations"), Row(d, label="squared distance"))
    order = sorted(range(len(pts)), key=lambda i: (d[i], pts[i][0], pts[i][1]))
    out = [pts[i] for i in order[:k]]
    W.step(f"The {k} closest: {out}.", Row([f"[{p[0]},{p[1]}]" for p in pts], st={i: "answer" for i in order[:k]}, label="stations"), Row(d, st={i: "answer" for i in order[:k]}, label="squared distance"), result=out)
    assert out == exp
    return W.save()


# ======================================================================== custom-order

@run
def nesting_boxes(pid):
    a, exp = example(pid)
    boxes = sorted(a["boxes"], key=lambda b: (b[0], -b[1]))
    W = Walk(pid, "Sort by width (ties: taller first, so equal widths can't nest). Then the answer is the longest strictly increasing run of heights, kept with a 'tails' list.")
    W.step("Sorted boxes.", Row([f"{w}×{h}" for w, h in boxes]))
    import bisect
    tails = []
    for i, (w, h) in enumerate(boxes):
        j = bisect.bisect_left(tails, h)
        if j == len(tails):
            tails.append(h)
            text = f"Height {h} extends the longest chain to {len(tails)}."
        else:
            tails[j] = h
            text = f"Height {h} replaces {j + 1}-chain's ending, so future chains start lower."
        W.step(text, Row([f"{x}×{y}" for x, y in boxes], st={i: "active"}), Row(tails, st={j: "new"}, label="smallest end of a chain of each length"))
    assert len(tails) == exp
    return W.save()


@run
def follow_the_guide(pid):
    a, exp = example(pid)
    items, guide = a["items"], a["guide"]
    W = Walk(pid, "Count each item, write guide values in guide order (with all their copies), then the rest in increasing order.")
    c = Counter(items)
    W.step("Counts of each item.", Row(items), Row([f"{k}:{v}" for k, v in sorted(c.items())], label="counts"))
    out = []
    for g in guide:
        out += [g] * c.pop(g, 0)
        W.step(f"Guide value {g}: write its copies.", Row(guide, st={guide.index(g): "active"}, label="guide"), Row(out, label="result"))
    for x in sorted(c):
        out += [x] * c[x]
        W.step(f"{x} isn't in the guide: write it in increasing order.", Row(out, st={len(out) - 1: "new"}, label="result"))
    assert out == exp
    return W.save()


@run
def reconstruct_the_line(pid):
    a, exp = example(pid)
    people = sorted(a["people"], key=lambda p: (-p[0], p[1]))
    W = Walk(pid, "Place the tallest first. Then each shorter person goes in at position 'ahead': everyone already placed is at least as tall, and shorter people inserted later can't change that.")
    W.step("Sorted tallest first (ties by 'ahead').", Row([f"{h},{k}" for h, k in people]))
    line = []
    for h, k in people:
        line.insert(k, [h, k])
        W.step(f"Insert [{h}, {k}] at position {k}.", Row([f"{x},{y}" for x, y in line], st={k: "new"}, label="line"))
    assert line == exp
    return W.save()


@run
def largest_number_from_pieces(pid):
    a, exp = example(pid)
    p = [str(x) for x in a["pieces"]]
    W = Walk(pid, "Order two pieces a and b by which is bigger: a + b or b + a (as strings). Insertion sort with that rule shows each comparison.")
    out = []
    for x in p:
        i = 0
        while i < len(out) and out[i] + x >= x + out[i]:
            i += 1
        out.insert(i, x)
        W.step(f"Place \"{x}\" at position {i}: it beats everything after it under the a + b vs b + a rule.", Row(out, st={i: "new"}))
    res = "".join(out).lstrip("0") or "0"
    W.step(f"Join them: {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


# ======================================================================== counting-bucket

@run
def sort_the_grades(pid):
    a, exp = example(pid)
    v = a["grades"]
    W = Walk(pid, "Grades only go from 0 to 100, so count how many of each grade there are, then write them out in order: O(n + 101).")
    c = Counter()
    for i, g in enumerate(v):
        c[g] += 1
        W.step(f"Count grade {g}.", Row(v, st={i: "active"}), Row([f"{k}:{c[k]}" for k in sorted(c)], label="counts"))
    out = []
    for g in sorted(c):
        out += [g] * c[g]
    W.step("Write each grade as many times as it was counted.", Row(out, st={i: "found" for i in range(len(out))}), result=out)
    assert out == exp
    return W.save()


@run
def most_played_songs(pid):
    a, exp = example(pid)
    v, k = a["plays"], a["k"]
    W = Walk(pid, f"Count plays, then drop each song into a bucket by its count. Read buckets from the highest count down until {k} songs are taken.")
    c = Counter()
    for i, x in enumerate(v):
        c[x] += 1
        W.step(f"Song {x}: {c[x]} play{'s' if c[x] > 1 else ''}.", Row(v, st={i: "active"}), Row([f"{s}:{n}" for s, n in sorted(c.items())], label="plays"))
    out = [s for s, _ in sorted(c.items(), key=lambda t: (-t[1], t[0]))[:k]]
    W.step(f"Top {k}: {out}.", Row([f"{s}:{n}" for s, n in sorted(c.items(), key=lambda t: (-t[1], t[0]))], st={i: "answer" for i in range(k)}, label="by count"), result=out)
    assert out == exp
    return W.save()


@run
def widest_gap_after_sorting(pid):
    a, exp = example(pid)
    v = a["nums"]
    n = len(v)
    W = Walk(pid, "Pigeonhole: n − 1 buckets of equal width between min and max. The widest gap can't hide inside a bucket, so only compare one bucket's max with the next non-empty bucket's min.")
    if n < 2:
        W.step("Fewer than two numbers: 0.", Row(v), result=0)
        assert exp == 0
        return W.save()
    lo, hi = min(v), max(v)
    size = max(1, (hi - lo) // (n - 1))
    count = (hi - lo) // size + 1
    mins, maxs = [None] * count, [None] * count
    for x in v:
        b = (x - lo) // size
        mins[b] = x if mins[b] is None else min(mins[b], x)
        maxs[b] = x if maxs[b] is None else max(maxs[b], x)
        W.step(f"{x} goes in bucket {b}.", Row(v, st={v.index(x): "active"}), Row([f"{mins[i]}–{maxs[i]}" if mins[i] is not None else "" for i in range(count)], label=f"buckets (width {size})"))
    best, prev = 0, None
    for i in range(count):
        if mins[i] is None:
            continue
        if prev is not None:
            best = max(best, mins[i] - prev)
        prev = maxs[i]
    W.step(f"Largest jump between neighbouring buckets: {best}.", Row([f"{mins[i]}–{maxs[i]}" if mins[i] is not None else "" for i in range(count)], label="buckets"), result=best)
    assert best == exp
    return W.save()


# ======================================================================== merge-count

def merge_sort_count(W, v, count_pair, merge_key=lambda x: x, describe="pairs"):
    """Merge sort that counts cross pairs; count_pair(left, right) -> number counted for this merge."""
    total = [0]

    def sort(lst):
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left, right = sort(lst[:mid]), sort(lst[mid:])
        c = count_pair(left, right)
        total[0] += c
        out = sorted(left + right, key=merge_key)
        W.step(f"Merge {left} and {right}: {c} {describe} cross between them. Total {total[0]}.", Row(left, label="left"), Row(right, label="right"), Row(out, st={i: "new" for i in range(len(out))}, label="merged"))
        return out

    sort(list(v))
    return total[0]


def inversions_between(left, right):
    import bisect
    return sum(len(left) - bisect.bisect_right(left, x) for x in right)


@run
def out_of_order_pairs(pid):
    a, exp = example(pid)
    v = a["ranks"]
    W = Walk(pid, "Merge sort, and while merging count how many left-half values are bigger than each right-half value: those are out-of-order pairs that cross the halves.")
    res = merge_sort_count(W, v, inversions_between, describe="out-of-order pairs")
    assert res == exp
    return W.save()


@run
def fewest_neighbour_swaps(pid):
    a, exp = example(pid)
    v = a["heights"]
    W = Walk(pid, "Each neighbour swap fixes exactly one out-of-order pair, so the answer is the number of such pairs. Merge sort counts them half by half.")
    res = merge_sort_count(W, v, inversions_between, describe="out-of-order pairs")
    assert res == exp
    return W.save()


@run
def big_drops(pid):
    a, exp = example(pid)
    v = a["prices"]
    W = Walk(pid, "Merge sort. Before merging two sorted halves, count pairs with left > 2 × right using two pointers.")

    def cross(left, right):
        c, j = 0, 0
        for x in left:
            while j < len(right) and x > 2 * right[j]:
                j += 1
            c += j
        return c

    res = merge_sort_count(W, v, cross, describe="big drops")
    assert res == exp
    return W.save()


@run
def shorter_behind(pid):
    a, exp = example(pid)
    v = a["heights"]
    W = Walk(pid, "Walk from the back, keeping the heights behind in sorted order. A binary search counts how many are strictly shorter (a Fenwick tree or merge sort makes it O(n log n)).")
    import bisect
    behind, out = [], [0] * len(v)
    for i in range(len(v) - 1, -1, -1):
        out[i] = bisect.bisect_left(behind, v[i])
        bisect.insort(behind, v[i])
        W.step(f"Person {i} (height {v[i]}): {out[i]} shorter behind.", Row(v, st={i: "active", **{k: "dim" for k in range(i + 1, len(v))}}), Row(behind, label="behind, sorted"), Row(out, label="count"))
    assert out == exp
    return W.save()


# ======================================================================== comparison-sorts

def merge_sort_steps(W, v, as_list=False):
    def sort(lst):
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left, right = sort(lst[:mid]), sort(lst[mid:])
        out, i, j = [], 0, 0
        while i < len(left) or j < len(right):
            if j >= len(right) or (i < len(left) and left[i] <= right[j]):
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
        P = L if as_list else Row
        W.step(f"Merge {left} and {right}, always taking the smaller front.", P(left, label="left"), P(right, label="right"), P(out, st={k: "new" for k in range(len(out))}, label="merged"))
        return out

    return sort(list(v))


@run
def sort_the_scoreboard(pid):
    a, exp = example(pid)
    W = Walk(pid, "Merge sort: split in half until single items, then merge sorted halves back up.")
    out = merge_sort_steps(W, a["scores"])
    assert out == exp
    return W.save()


@run
def sort_the_train_cars(pid):
    a, exp = example(pid)
    W = Walk(pid, "Merge sort suits linked lists: split at the middle (slow/fast pointers), sort both halves, then merge by relinking.")
    out = merge_sort_steps(W, a["head"], as_list=True)
    assert out == exp
    return W.save()


@run
def sort_with_many_repeats(pid):
    a, exp = example(pid)
    v = list(a["readings"])
    W = Walk(pid, "Three-way quick sort: partition into < pivot, = pivot, > pivot. Everything equal to the pivot is done at once, so repeats don't slow it down.")

    def qs(lo, hi):
        if lo >= hi:
            return
        p = v[lo]
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if v[i] < p:
                v[lt], v[i] = v[i], v[lt]
                lt += 1
                i += 1
            elif v[i] > p:
                v[i], v[gt] = v[gt], v[i]
                gt -= 1
            else:
                i += 1
        W.step(f"Pivot {p} on positions {lo}–{hi}: smaller to the left, the {gt - lt + 1} copies of {p} settle in the middle, larger to the right.", Row(v, st={**{k: "dim" for k in range(len(v)) if k < lo or k > hi}, **{k: "found" for k in range(lt, gt + 1)}}))
        qs(lo, lt - 1)
        qs(gt + 1, hi)

    W.step("The readings.", Row(v))
    qs(0, len(v) - 1)
    assert v == exp
    return W.save()


@run
def nearly_sorted_log(pid):
    a, exp = example(pid)
    v, k = a["times"], a["k"]
    W = Walk(pid, f"Every entry is at most {k} places from home, so the smallest remaining one is always among the next {k + 1}. Keep those in a min-heap.")
    heap, out = [], []
    for i, x in enumerate(v):
        heapq.heappush(heap, x)
        if len(heap) > k:
            out.append(heapq.heappop(heap))
            W.step(f"Add {x}; the heap now holds {k + 1}, so pop its smallest, {out[-1]}.", Row(v, st={i: "active"}), Row(sorted(heap), label="heap"), Row(out, st={len(out) - 1: "new"}, label="sorted"))
    while heap:
        out.append(heapq.heappop(heap))
        W.step(f"Input done: pop {out[-1]}.", Row(sorted(heap), label="heap"), Row(out, st={len(out) - 1: "new"}, label="sorted"))
    assert out == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
