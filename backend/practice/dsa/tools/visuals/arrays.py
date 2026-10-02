import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from collections import Counter, defaultdict
from lib import *

DONE = []


CUSTOM = {
    "loudest-letters-first": [{"s": "mississippi"}],
    "matching-rows-and-columns": [{"grid": [[3, 1, 2, 2], [1, 4, 4, 5], [2, 4, 2, 2], [2, 4, 2, 2]]}],
    "running-balance": [{"changes": [5, -2, 10, -7, 3]}],
    "range-totals": [{"sales": [3, -1, 4, 1, 5, 9, -2], "queries": [[0, 2], [1, 4], [3, 3], [2, 6]]}],
    "balance-point": [{"weights": [1, 2, 3, 4, 6]}],
    "subarrays-hitting-target": [{"nums": [1, 2, 1, 2, 1, 3], "target": 3}],
    "stadium-sections": [{"n": 6, "groups": [[0, 2, 10], [1, 4, 5], [3, 5, 2]]}],
    "shuttle-seats": [{"capacity": 5, "trips": [[2, 1, 5], [3, 3, 7], [1, 6, 8]]}],
    "missing-seat": [{"seats": [3, 0, 1, 5, 2]}],
    "first-k-missing": [{"nums": [4, 3, 2, 7, 8, 2, 3, 1], "k": 3}],
    "fewest-swaps-to-sort": [{"order": [2, 3, 1, 5, 4, 7, 6]}],
    "longest-streak": [{"days": [100, 4, 200, 1, 3, 2, 101, 102, 50]}],
    "longest-chain-with-step": [{"values": [10, 4, 1, 7, 5, 13, 8, 2, 20, 23], "step": 3}],
    "influence-score": [{"citations": [3, 0, 6, 1, 5, 4, 8]}],
    "closest-heights": [{"heights": [170, 182, 165, 180, 176, 190]}],
    "flip-the-grid": [{"grid": [[1, 2, 3, 4], [5, 6, 7, 8]]}],
    "first-missing-ticket": [{"nums": [3, 4, -1, 1, 7]}],
    "swapped-label": [{"labels": [3, 1, 2, 5, 3]}],
    "two-gifts": [{"prices": [3, 8, 11, 2, 15, 7], "budget": 9}],
    "rotate-the-carousel": [{"slots": [1, 2, 3, 4, 5, 6, 7], "k": 3}],
    "next-arrangement": [{"values": [1, 5, 8, 4, 7, 6, 5, 3, 1]}],
    "next-badge-number": [{"code": "158476531"}],
    "one-step-back": [{"ratings": [1, 5, 8, 4, 1, 3, 5, 6, 7]}],
}
run = make_runner(DONE, CUSTOM)


def kv(d, label, st=None):
    """A hash map drawn as key:value cells."""
    items = list(d.items())
    return Row([f"{k}:{v}" for k, v in items], st=st, label=label)


def scan(v, i, done="dim", label=None, st=None, ptr=None):
    s = {k: done for k in range(i)}
    if 0 <= i < len(v):
        s[i] = "active"
    s.update(st or {})
    return Row(v, st=s, ptr=ptr, label=label)


# ======================================================================== frequency-counting

@run
def duplicate_badges(pid):
    a, exp = example(pid)
    v = a["badges"]
    W = Walk(pid, "Keep a set of numbers seen so far; the first number already in it is a duplicate.")
    seen, res = [], False
    for i, x in enumerate(v):
        if x in seen:
            res = True
            W.step(f"{x} is already in the set: a duplicate.", scan(v, i, st={i: "answer", v.index(x): "answer"}), Row(seen, label="seen"), result=True)
            break
        seen.append(x)
        W.step(f"{x} is new: add it.", scan(v, i), Row(seen, st={len(seen) - 1: "new"}, label="seen"))
    if not res:
        W.step("Every number was new.", Row(v), result=False)
    assert res == exp
    return W.save()


@run
def letter_tiles(pid):
    a, exp = example(pid)
    sign, tiles = a["sign"], a["tiles"]
    W = Walk(pid, "Count the tiles by letter, then spend one count for each letter of the sign.")
    have = Counter(tiles)
    W.step("Tile counts.", Row(list(tiles), label="tiles"), kv(dict(sorted(have.items())), "counts"))
    ok = True
    for i, ch in enumerate(sign):
        have[ch] -= 1
        if have[ch] < 0:
            ok = False
            W.step(f"No \"{ch}\" tile left: the sign can't be spelled.", Row(list(sign), st={i: "mark"}, label="sign"), kv(dict(sorted(have.items())), "counts"), result=False)
            break
        W.step(f"Use a \"{ch}\".", Row(list(sign), st={**{k: "found" for k in range(i)}, i: "active"}, label="sign"), kv(dict(sorted(have.items())), "counts"))
    if ok:
        W.step("Every letter was covered.", Row(list(sign), st={k: "found" for k in range(len(sign))}, label="sign"), result=True)
    assert ok == exp
    return W.save()


def boyer_moore(W, v, verify=True, need_half=True):
    cand, count = None, 0
    for i, x in enumerate(v):
        if count == 0:
            cand, count = x, 1
            text = f"Count is 0, so {x} becomes the candidate."
        elif x == cand:
            count += 1
            text = f"{x} matches the candidate: count {count}."
        else:
            count -= 1
            text = f"{x} differs: it cancels one vote, count {count}."
        W.step(text, scan(v, i), Vars(candidate=cand, count=count))
    return cand


@run
def majority_reading(pid):
    a, exp = example(pid)
    v = a["readings"]
    W = Walk(pid, "Boyer–Moore voting: pair off different readings so they cancel; the majority reading always survives.")
    c = boyer_moore(W, v)
    W.step(f"The survivor is {c}.", Row(v, st={i: "answer" for i, x in enumerate(v) if x == c}), result=c)
    assert c == exp
    return W.save()


@run
def half_or_more(pid):
    a, exp = example(pid)
    v = a["votes"]
    W = Walk(pid, "Find a candidate with Boyer–Moore voting, then count its votes to check it really has more than half.")
    c = boyer_moore(W, v)
    n = v.count(c)
    res = c if n * 2 > len(v) else -1
    W.step(f"{c} has {n} of {len(v)} votes: " + ("more than half." if res != -1 else "not more than half, so -1."), Row(v, st={i: "answer" for i, x in enumerate(v) if x == c}), result=res)
    assert res == exp
    return W.save()


@run
def strong_candidates(pid):
    a, exp = example(pid)
    v = a["votes"]
    W = Walk(pid, "At most two options can have more than a third. Keep two candidates with counts; a vote for neither cancels one of each.")
    c1 = c2 = None
    n1 = n2 = 0
    for i, x in enumerate(v):
        if x == c1:
            n1 += 1
        elif x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:
            n1 -= 1
            n2 -= 1
        W.step(f"Vote {x}.", scan(v, i), Vars(first=f"{c1} ×{n1}", second=f"{c2} ×{n2}"))
    out = sorted(c for c in {c1, c2} if c is not None and v.count(c) * 3 > len(v))
    W.step(f"Recount the two candidates: {out or 'none'} beat {len(v) // 3} votes.", Row(v, st={i: "answer" for i, x in enumerate(v) if x in out}), result=out)
    assert out == exp
    return W.save()


@run
def loudest_letters_first(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Count each character, sort by count (high first, then by character), and write each one count times.")
    c = Counter(s)
    W.step("Counts.", Row(list(s)), kv(dict(sorted(c.items())), "counts"))
    order = sorted(c.items(), key=lambda t: (-t[1], t[0]))
    out = ""
    for ch, n in order:
        out += ch * n
        W.step(f"\"{ch}\" × {n}.", kv(dict(order), "sorted by count", st={order.index((ch, n)): "active"}), Vars(output=out))
    assert out == exp
    return W.save()


@run
def top_genres(pid):
    a, exp = example(pid)
    v, k = a["plays"], a["k"]
    W = Walk(pid, f"Count plays per genre, then take the {k} highest counts (smaller id first on ties). Buckets by count make it O(n).")
    c = Counter()
    for i, x in enumerate(v):
        c[x] += 1
        W.step(f"Genre {x}: {c[x]} play{'s' if c[x] > 1 else ''}.", scan(v, i), kv(dict(sorted(c.items())), "plays"))
    out = [g for g, _ in sorted(c.items(), key=lambda t: (-t[1], t[0]))[:k]]
    W.step(f"Top {k}: {out}.", kv(dict(sorted(c.items(), key=lambda t: (-t[1], t[0]))), "by count", st={i: "answer" for i in range(k)}), result=out)
    assert out == exp
    return W.save()


# ======================================================================== complement-lookup

@run
def two_gifts(pid):
    a, exp = example(pid)
    v, b = a["prices"], a["budget"]
    W = Walk(pid, f"Remember each price's index. For each new price, look up whether {b} − price has been seen.")
    seen = {}
    for i, x in enumerate(v):
        need = b - x
        if need in seen:
            res = [seen[need], i]
            W.step(f"{x} needs {need}, seen at index {seen[need]}.", scan(v, i, st={seen[need]: "answer", i: "answer"}), kv(seen, "price:index"), result=res)
            break
        seen[x] = i
        W.step(f"{x} needs {need}: not seen yet. Remember {x}.", scan(v, i), kv(seen, "price:index", st={len(seen) - 1: "new"}))
    W.intro(f"For each price x we need {b} − x. A hash map from price to index answers \"have I seen it?\" in O(1).", Row(v))
    assert res == exp
    return W.save()


@run
def pairs_a_gap_apart(pid):
    a, exp = example(pid)
    v, k = a["nums"], a["k"]
    c = Counter(v)
    W = Walk(pid, f"Count the values. For each distinct x, the pair (x, x + {k}) exists if x + {k} is in the counts" + (" (for k = 0, x must appear twice)." if k == 0 else "."))
    W.step("Distinct values and counts.", Row(v), kv(dict(sorted(c.items())), "counts"))
    res = 0
    for i, x in enumerate(sorted(c)):
        ok = c[x] > 1 if k == 0 else x + k in c
        res += ok
        W.step(f"{x}: {'pair with ' + str(x + k) if ok else 'no partner'}. Pairs {res}.", kv(dict(sorted(c.items())), "counts", st={i: "answer" if ok else "active"}))
    assert res == exp
    return W.save()


@run
def four_lists_zero(pid):
    a, exp = example(pid)
    A, B, C, D = a["a"], a["b"], a["c"], a["d"]
    W = Walk(pid, "Count every a + b sum in a hash map. Then for every c + d, look up how many a + b sums equal −(c + d).")
    ab = Counter(x + y for x in A for y in B)
    W.step("All a + b sums with their counts.", kv(dict(sorted(ab.items())), "a + b"))
    total = 0
    for z in C:
        for w in D:
            hit = ab[-(z + w)]
            total += hit
            W.step(f"c + d = {z} + {w} = {z + w}; {hit} a + b sum{'s' if hit != 1 else ''} equal {-(z + w)}. Total {total}.", kv(dict(sorted(ab.items())), "a + b", st={list(sorted(ab)).index(-(z + w)): "answer"} if hit else None))
    assert total == exp
    return W.save()


@run
def divisible_pairs(pid):
    a, exp = example(pid)
    v, k = a["nums"], a["k"]
    W = Walk(pid, f"Two numbers sum to a multiple of {k} when their remainders add up to 0 mod {k}. Count remainders as you go.")
    rem, total = Counter(), 0
    for i, x in enumerate(v):
        r = x % k
        need = (k - r) % k
        total += rem[need]
        rem[r] += 1
        W.step(f"{x} leaves {r}; it pairs with the {rem[need] - (1 if need == r else 0) if need == r else rem[need]} earlier number{'s' if rem[need] != 1 else ''} leaving {need}. Total {total}.", scan(v, i), kv(dict(sorted(rem.items())), "remainder counts"))
    assert total == exp
    return W.save()


# ======================================================================== group-by-key

def group_steps(W, words, key, keytext):
    groups = defaultdict(list)
    for w in words:
        k = key(w)
        groups[k].append(w)
        W.step(f"\"{w}\" has key {keytext(k)}.", Row(list(words), st={words.index(w): "active"}), Row([f"{keytext(g)}: {' '.join(ws)}" for g, ws in groups.items()], label="groups"))
    return groups


@run
def anagram_groups(pid):
    a, exp = example(pid)
    words = a["words"]
    W = Walk(pid, "Anagrams have the same letters, so sorting a word's letters gives a key shared by its whole group.")
    g = group_steps(W, words, lambda w: "".join(sorted(w)), lambda k: k)
    out = sorted(sorted(ws) for ws in g.values())
    W.step("Sort each group and the groups.", Row([" ".join(x) for x in out], label="groups"), result=out)
    assert out == exp
    return W.save()


@run
def shift_families(pid):
    a, exp = example(pid)
    words = a["words"]
    W = Walk(pid, "Shifting keeps the gaps between neighbouring letters (mod 26). Those gaps are a word's family key.")
    key = lambda w: tuple((ord(w[i + 1]) - ord(w[i])) % 26 for i in range(len(w) - 1))
    g = group_steps(W, words, key, lambda k: "(" + ",".join(map(str, k)) + ")")
    W.step(f"{len(g)} famil{'ies' if len(g) != 1 else 'y'}.", Row([" ".join(ws) for ws in g.values()], label="families"), result=len(g))
    assert len(g) == exp
    return W.save()


@run
def same_shape_words(pid):
    a, exp = example(pid)
    words, p = a["words"], a["pattern"]
    sig = lambda w: tuple(w.index(c) for c in w)
    W = Walk(pid, "Replace each letter by the position where it first appears. Two words have the same shape exactly when those lists match.")
    target = sig(p)
    W.step(f"\"{p}\" becomes {list(target)}.", Row(list(p), label="pattern"), Row(list(target), label="shape"))
    count = 0
    for w in words:
        ok = sig(w) == target
        count += ok
        W.step(f"\"{w}\" becomes {list(sig(w))}: {'same shape' if ok else 'different'}. Count {count}.", Row(list(w), st={i: "found" if ok else "mark" for i in range(len(w))}), Row(list(sig(w)), label="shape"))
    assert count == exp
    return W.save()


@run
def matching_rows_and_columns(pid):
    a, exp = example(pid)
    g = a["grid"]
    n = len(g)
    W = Walk(pid, "Count each row (as a tuple) in a hash map. Then each column adds the number of rows equal to it.")
    rows = Counter(tuple(r) for r in g)
    W.step("Row counts.", Grid(g), kv({"(" + ",".join(map(str, r)) + ")": c for r, c in rows.items()}, "rows"))
    total = 0
    for c in range(n):
        col = tuple(g[r][c] for r in range(n))
        total += rows[col]
        st = {(r, c): "active" for r in range(n)}
        for r in range(n):
            if tuple(g[r]) == col:
                for cc in range(n):
                    st[(r, cc)] = "answer"
                for rr in range(n):
                    st[(rr, c)] = "answer"
        W.step(f"Column {c} reads {list(col)}: {rows[col]} matching row{'s' if rows[col] != 1 else ''}. Total {total}.", Grid(g, st))
    assert total == exp
    return W.save()


# ======================================================================== prefix-sums

def prefix(v):
    out = [0]
    for x in v:
        out.append(out[-1] + x)
    return out


@run
def running_balance(pid):
    a, exp = example(pid)
    v = a["changes"]
    W = Walk(pid, "Each day's balance is the previous balance plus that day's change.")
    out, bal = [], 0
    for i, x in enumerate(v):
        bal += x
        out.append(bal)
        W.step(f"{'+' if x >= 0 else ''}{x}: balance {bal}.", scan(v, i), Row(out, st={i: "new"}, label="balance"))
    assert out == exp
    return W.save()


@run
def range_totals(pid):
    a, exp = example(pid)
    v = a["sales"]
    p = prefix(v)
    W = Walk(pid, "Build prefix totals once: P[i] = sales of days 0..i−1. Then days l..r total P[r + 1] − P[l].")
    W.step("Prefix totals.", Row(v, label="sales"), Row(p, label="P"))
    out = []
    for l_, r in a["queries"]:
        out.append(p[r + 1] - p[l_])
        W.step(f"Days {l_}–{r}: P[{r + 1}] − P[{l_}] = {p[r + 1]} − {p[l_]} = {out[-1]}.", Row(v, st={i: "found" for i in range(l_, r + 1)}, label="sales"), Row(p, st={r + 1: "active", l_: "mark"}, label="P"), result=out[-1])
    assert out == exp
    return W.save()


@run
def balance_point(pid):
    a, exp = example(pid)
    v = a["weights"]
    total = sum(v)
    W = Walk(pid, f"The right side is total − left − weights[i]. Walk once, keeping the left sum (total {total}).")
    left, res = 0, -1
    for i, x in enumerate(v):
        right = total - left - x
        if left == right:
            res = i
            W.step(f"At {i}: left {left}, right {right}. Balanced.", scan(v, i, st={i: "answer"}), Vars(left=left, right=right), result=i)
            break
        W.step(f"At {i}: left {left}, right {right}.", scan(v, i), Vars(left=left, right=right))
        left += x
    assert res == exp
    return W.save()


@run
def subarrays_hitting_target(pid):
    a, exp = example(pid)
    v, t = a["nums"], a["target"]
    W = Walk(pid, f"A stretch ending here sums to {t} once for each earlier prefix equal to (current prefix − {t}). Count prefixes in a hash map.")
    seen, s, total = Counter({0: 1}), 0, 0
    for i, x in enumerate(v):
        s += x
        total += seen[s - t]
        W.step(f"Prefix {s}: {seen[s - t]} earlier prefix{'es' if seen[s - t] != 1 else ''} equal {s - t}. Total {total}.", scan(v, i), kv(dict(sorted(seen.items())), "prefix counts"))
        seen[s] += 1
    assert total == exp
    return W.save()


@run
def longest_even_stretch(pid):
    a, exp = example(pid)
    v = a["bits"]
    W = Walk(pid, "Count 1 as +1 and 0 as −1. A stretch is even when its sum is 0: when the running sum returns to a value seen before.")
    first, s, best = {0: -1}, 0, 0
    for i, x in enumerate(v):
        s += 1 if x else -1
        if s in first:
            best = max(best, i - first[s])
            W.step(f"Running sum {s} was first seen at {first[s]}: positions {first[s] + 1}–{i} are even. Best {best}.", scan(v, i, st={k: "found" for k in range(first[s] + 1, i + 1)}), kv(first, "first seen"))
        else:
            first[s] = i
            W.step(f"Running sum {s} is new: remember it at {i}.", scan(v, i), kv(first, "first seen"))
    assert best == exp
    return W.save()


@run
def sums_in_bounds(pid):
    a, exp = example(pid)
    v, lo, hi = a["nums"], a["lower"], a["upper"]
    p = prefix(v)
    W = Walk(pid, f"A run i..j sums to P[j + 1] − P[i]. Count pairs of prefixes whose difference is in [{lo}, {hi}] (merge sort counts them in O(n log n)).")
    W.step("Prefix sums.", Row(v, label="nums"), Row(p, label="P"))
    total = 0
    for j in range(1, len(p)):
        hits = [i for i in range(j) if lo <= p[j] - p[i] <= hi]
        total += len(hits)
        W.step(f"Runs ending at {j - 1}: {len(hits)} of them sum into the range. Total {total}.", Row(v, st={k: "found" for k in range(j)}, label="nums"), Row(p, st={**{i: "answer" for i in hits}, j: "active"}, label="P"))
    assert total == exp
    return W.save()


# ======================================================================== difference-arrays

@run
def stadium_sections(pid):
    a, exp = example(pid)
    n = a["n"]
    W = Walk(pid, "For each group, add at l and subtract just after r. One running sum at the end fills in every section.")
    d = [0] * (n + 1)
    for l_, r, ppl in a["groups"]:
        d[l_] += ppl
        d[r + 1] -= ppl
        W.step(f"Group [{l_}, {r}, {ppl}]: +{ppl} at {l_}, −{ppl} at {r + 1}.", Row(d, st={l_: "new", r + 1: "new"}, label="difference"))
    out, s = [], 0
    for i in range(n):
        s += d[i]
        out.append(s)
    W.step("Running sum of the differences.", Row(d, label="difference"), Row(out, st={i: "found" for i in range(n)}, label="fans"), result=out)
    assert out == exp
    return W.save()


@run
def shuttle_seats(pid):
    a, exp = example(pid)
    cap, trips = a["capacity"], a["trips"]
    end = max(t[2] for t in trips) + 1
    W = Walk(pid, f"Add passengers where they get on and subtract where they get off; the running sum is the load at each mark (capacity {cap}).")
    d = [0] * end
    for p, f, t in trips:
        d[f] += p
        d[t] -= p
        W.step(f"Trip [{p}, {f}, {t}]: +{p} at {f}, −{p} at {t}.", Row(d, st={f: "new", t: "new"}, label="change"))
    load, s, ok = [], 0, True
    for i in range(end):
        s += d[i]
        load.append(s)
    over = [i for i, x in enumerate(load) if x > cap]
    ok = not over
    W.step("Load at each mark: " + ("never over capacity." if ok else f"over {cap} at mark {over[0]}."), Row(load, st={i: ("mark" if i in over else "found") for i in range(end)}, label="load"), result=ok)
    assert ok == exp
    return W.save()


@run
def brightest_spot(pid):
    a, exp = example(pid)
    lamps = a["lamps"]
    W = Walk(pid, "Each lamp adds +1 where its light starts and −1 just after it ends. Sweep the events in order; the running sum is the brightness.")
    ev = Counter()
    for p, r in lamps:
        ev[p - r] += 1
        ev[p + r + 1] -= 1
    keys = sorted(ev)
    W.step("Events: position:change.", kv({k: ev[k] for k in keys}, "events"))
    cur, best, at = 0, -1, None
    for i, k in enumerate(keys):
        cur += ev[k]
        if cur > best:
            best, at = cur, k
        W.step(f"At {k}: brightness {cur}. Brightest {best} at {at}.", kv({k_: ev[k_] for k_ in keys}, "events", st={i: "active"}), Vars(brightness=cur, best=best))
    assert at == exp
    return W.save()


# ======================================================================== index-marking / cyclic-sort

@run
def missing_seat(pid):
    a, exp = example(pid)
    v = a["seats"]
    n = len(v)
    W = Walk(pid, f"Seats 0..{n} add up to {n * (n + 1) // 2}. Subtract the taken seats; what's left is the free one.")
    left = n * (n + 1) // 2
    for i, x in enumerate(v):
        left -= x
        W.step(f"Take away {x}: {left} left.", scan(v, i), Vars(remaining=left))
    assert left == exp
    return W.save()


@run
def unclaimed_numbers(pid):
    a, exp = example(pid)
    v = list(a["tickets"])
    W = Walk(pid, "Use the list itself as the 'seen' marks: for each number x, make position x − 1 negative.")
    for i in range(len(v)):
        x = abs(v[i])
        if v[x - 1] > 0:
            v[x - 1] = -v[x - 1]
        W.step(f"Saw {x}: mark position {x - 1}.", Row(v, st={**{k: "found" for k in range(len(v)) if v[k] < 0}, i: "active"}))
    out = [i + 1 for i, x in enumerate(v) if x > 0]
    W.step(f"Positions still positive were never marked: numbers {out}.", Row(v, st={i: "answer" for i in range(len(v)) if v[i] > 0}), result=out)
    assert out == exp
    return W.save()


@run
def double_booked(pid):
    a, exp = example(pid)
    v = list(a["bookings"])
    W = Walk(pid, "Mark room x by making position x − 1 negative. If it's already negative, room x was booked before.")
    out = []
    for i in range(len(v)):
        x = abs(v[i])
        if v[x - 1] < 0:
            out.append(x)
            W.step(f"Room {x} is already marked: booked twice.", Row(v, st={x - 1: "answer", i: "active"}), Row(sorted(out), label="twice"))
        else:
            v[x - 1] = -v[x - 1]
            W.step(f"Mark room {x}.", Row(v, st={**{k: "found" for k in range(len(v)) if v[k] < 0}, i: "active"}), Row(sorted(out), label="twice"))
    out.sort()
    assert out == exp
    return W.save()


def cyclic_place(W, v, valid, say):
    i = 0
    while i < len(v):
        x = v[i]
        if valid(x) and v[x - 1] != x:
            v[i], v[x - 1] = v[x - 1], v[i]
            W.step(say(x), Row(v, st={x - 1: "new", i: "active"}))
        else:
            i += 1
    return v


@run
def first_missing_ticket(pid):
    a, exp = example(pid)
    v = list(a["nums"])
    n = len(v)
    W = Walk(pid, f"Swap every value x in 1..{n} to position x − 1. Then the first position that doesn't hold its own number gives the answer.")
    cyclic_place(W, v, lambda x: 1 <= x <= n, lambda x: f"Send {x} to position {x - 1}.")
    res = next((i + 1 for i, x in enumerate(v) if x != i + 1), n + 1)
    W.step(f"The first gap is {res}.", Row(v, st={res - 1: "mark"} if res <= n else {i: "found" for i in range(n)}), result=res)
    W.intro(f"If every number 1..{n} were present, each could sit at its own position (x at x − 1). Junk values (≤ 0 or > {n}) can be ignored.", Row(a["nums"], st={i: ("dim" if not 1 <= x <= n else "") for i, x in enumerate(a["nums"])}))
    assert res == exp
    return W.save()


@run
def swapped_label(pid):
    a, exp = example(pid)
    v = list(a["labels"])
    W = Walk(pid, "Cyclic sort: swap each label to its home position. The one position left without its own label holds the duplicate.")
    cyclic_place(W, v, lambda x: True, lambda x: f"Send {x} home to position {x - 1}.")
    i = next(i for i, x in enumerate(v) if x != i + 1)
    res = [v[i], i + 1]
    W.step(f"Position {i} holds {v[i]} instead of {i + 1}: {v[i]} is doubled and {i + 1} is missing.", Row(v, st={i: "answer"}), result=res)
    W.intro("Each label x belongs at position x − 1. One label appears twice, so one position can never get its own label.", Row(a["labels"], ptr={"home of 1": 0}))
    assert res == exp
    return W.save()


@run
def first_k_missing(pid):
    a, exp = example(pid)
    v, k = list(a["nums"]), a["k"]
    n = len(v)
    W = Walk(pid, f"Place each value x in 1..{n} at position x − 1, then read the gaps; if fewer than {k}, continue past {n} skipping values that appeared.")
    cyclic_place(W, v, lambda x: 1 <= x <= n, lambda x: f"Send {x} to position {x - 1}.")
    out, extra = [], set()
    for i, x in enumerate(v):
        if x != i + 1 and len(out) < k:
            out.append(i + 1)
            extra.add(x)
    nxt = n + 1
    while len(out) < k:
        if nxt not in extra:
            out.append(nxt)
        nxt += 1
    W.step(f"Missing: {out}.", Row(v, st={i: "mark" for i, x in enumerate(v) if x != i + 1}), Row(out, label="missing"), result=out)
    assert out == exp
    return W.save()


@run
def fewest_swaps_to_sort(pid):
    a, exp = example(pid)
    v = a["order"]
    W = Walk(pid, "Follow where each bib should go. Bibs form cycles; a cycle of length L takes L − 1 swaps.")
    seen, total = set(), 0
    for i in range(len(v)):
        if i in seen:
            continue
        cyc, j = [], i
        while j not in seen:
            seen.add(j)
            cyc.append(j)
            j = v[j] - 1
        total += len(cyc) - 1
        W.step(f"Cycle through positions {cyc}: {len(cyc) - 1} swap{'s' if len(cyc) != 2 else ''}. Total {total}.", Row(v, st={**{k: "dim" for k in seen}, **{k: "active" for k in cyc}}))
    W.intro("Bib x belongs at position x − 1. Draw an arrow from each position to where its bib belongs: the arrows form cycles.", Row(v), Row([i + 1 for i in range(len(v))], label="should be"))
    assert total == exp
    return W.save()


# ======================================================================== consecutive-runs / sort-then-scan

@run
def longest_streak(pid):
    a, exp = example(pid)
    s = sorted(set(a["days"]))
    W = Walk(pid, "Put the days in a set. Only count from a day whose previous day is missing: that's where a streak starts.")
    best = 0
    for x in s:
        if x - 1 in s:
            continue
        n = 1
        while x + n in s:
            n += 1
        best = max(best, n)
        W.step(f"Streak from {x}: {n} day{'s' if n != 1 else ''}. Best {best}.", Row(s, st={s.index(x + k): "active" for k in range(n)}, label="days (set, shown sorted)"))
    assert best == exp
    return W.save()


@run
def longest_chain_with_step(pid):
    a, exp = example(pid)
    s, step = sorted(set(a["values"])), a["step"]
    W = Walk(pid, f"Put the values in a set. Start a chain only at x when x − {step} is missing, then hop by {step}.")
    best = 0
    for x in s:
        if x - step in s:
            continue
        n = 1
        while x + n * step in s:
            n += 1
        best = max(best, n)
        W.step(f"Chain from {x}: {n} long. Best {best}.", Row(s, st={s.index(x + k * step): "active" for k in range(n)}, label="values (set, shown sorted)"))
    W.intro(f"Order doesn't matter, so put the values in a set: every lookup of \"is x + {step} there?\" is O(1).", Row(a["values"], label="values"))
    assert best == exp
    return W.save()


@run
def is_it_a_straight(pid):
    a, exp = example(pid)
    v = a["cards"]
    W = Walk(pid, "A straight has no repeats and its largest card is exactly n − 1 above its smallest. One pass with a set and running min and max checks both.")
    seen, lo, hi, ok = [], None, None, True
    for i, x in enumerate(v):
        if x in seen:
            ok = False
            W.step(f"{x} repeats: not a straight.", Row(v, st={i: "mark", v.index(x): "mark"}), Row(seen, label="seen"), result=False)
            break
        seen.append(x)
        lo = x if lo is None else min(lo, x)
        hi = x if hi is None else max(hi, x)
        W.step(f"Card {x}: min {lo}, max {hi}.", Row(v, st={**{k: "found" for k in range(i)}, i: "active"}), Row(seen, label="seen"), Vars(min=lo, max=hi))
    if ok:
        ok = hi - lo == len(v) - 1
        W.step(f"{hi} − {lo} = {hi - lo}, and n − 1 = {len(v) - 1}: " + ("a straight." if ok else "not a straight."), Vars(answer=ok), result=ok)
    assert ok == exp
    return W.save()



@run
def influence_score(pid):
    a, exp = example(pid)
    v = sorted(a["citations"], reverse=True)
    W = Walk(pid, "Sort citations from most to least. The score is the last position i (1-based) where the paper there still has at least i citations.")
    h = 0
    for i, x in enumerate(v):
        if x >= i + 1:
            h = i + 1
            W.step(f"Paper {i + 1} has {x} ≥ {i + 1}: score at least {h}.", Row(v, st={**{k: "found" for k in range(i)}, i: "answer"}))
        else:
            W.step(f"Paper {i + 1} has {x} < {i + 1}: stop.", Row(v, st={**{k: "found" for k in range(i)}, i: "mark"}))
            break
    assert h == exp
    return W.save()


@run
def closest_heights(pid):
    a, exp = example(pid)
    v = sorted(a["heights"])
    W = Walk(pid, "After sorting, the closest pair must be neighbours. Check each neighbouring gap.")
    best = None
    for i in range(len(v) - 1):
        d = v[i + 1] - v[i]
        best = d if best is None else min(best, d)
        W.step(f"{v[i + 1]} − {v[i]} = {d}. Smallest {best}.", Row(v, st={i: "active", i + 1: "active"}))
    assert best == exp
    return W.save()


# ======================================================================== prefix-suffix

@run
def taller_ahead(pid):
    a, exp = example(pid)
    v = a["heights"]
    W = Walk(pid, "Walk from the end keeping the tallest building seen so far; that's the answer for the building just before it.")
    out = [None] * len(v)
    best = -1
    for i in range(len(v) - 1, -1, -1):
        out[i] = best
        W.step(f"Tallest after building {i}: {best}.", Row(v, st={**{k: "dim" for k in range(i + 1, len(v))}, i: "active"}), Row(out, st={i: "new"}, label="answer"))
        best = max(best, v[i])
    assert out == exp
    return W.save()


@run
def rain_on_the_skyline(pid):
    a, exp = example(pid)
    v = a["walls"]
    n = len(v)
    left, right = [0] * n, [0] * n
    for i in range(n):
        left[i] = max(v[i], left[i - 1] if i else 0)
    for i in range(n - 1, -1, -1):
        right[i] = max(v[i], right[i + 1] if i < n - 1 else 0)
    W = Walk(pid, "Water above column i rises to the lower of the tallest wall on its left and on its right.")
    W.step("Tallest wall up to each column, from the left and from the right.", Row(v, label="walls"), Row(left, label="max from left"), Row(right, label="max from right"))
    water = [min(left[i], right[i]) - v[i] for i in range(n)]
    total = 0
    for i in range(n):
        total += water[i]
        W.step(f"Column {i}: min({left[i]}, {right[i]}) − {v[i]} = {water[i]}. Total {total}.", Row(v, st={i: "active"}, label="walls"), Row(water[:i + 1], st={i: "new"}, label="water"))
    assert total == exp
    return W.save()


@run
def everyone_elses_product(pid):
    a, exp = example(pid)
    v = a["nums"]
    n = len(v)
    W = Walk(pid, "Product of everything else = (product of everything before i) × (product of everything after i). Two passes, no division.")
    pre = [1] * n
    for i in range(1, n):
        pre[i] = pre[i - 1] * v[i - 1]
    W.step("Left pass: products of everything before each position.", Row(v, label="nums"), Row(pre, label="before"))
    out, suf = pre[:], 1
    for i in range(n - 1, -1, -1):
        out[i] = pre[i] * suf
        W.step(f"Right pass at {i}: {pre[i]} × {suf} (everything after) = {out[i]}.", Row(v, st={i: "active"}, label="nums"), Row(out, st={i: "new"}, label="answer"))
        suf *= v[i]
    assert out == exp
    return W.save()


# ======================================================================== matrix-traversal

@run
def spiral_readout(pid):
    a, exp = example(pid)
    g = a["grid"]
    W = Walk(pid, "Keep four walls (top, bottom, left, right). Read one side, then move that wall inward.")
    top, bottom, left, right = 0, len(g) - 1, 0, len(g[0]) - 1
    out, done = [], {}
    while top <= bottom and left <= right:
        sides = [("top row", [(top, c) for c in range(left, right + 1)])]
        sides.append(("right side", [(r, right) for r in range(top + 1, bottom + 1)]))
        if top < bottom:
            sides.append(("bottom row", [(bottom, c) for c in range(right - 1, left - 1, -1)]))
        if left < right:
            sides.append(("left side", [(r, left) for r in range(bottom - 1, top, -1)]))
        for name, cells in sides:
            if not cells:
                continue
            out += [g[r][c] for r, c in cells]
            W.step(f"Read the {name}: {[g[r][c] for r, c in cells]}.", Grid(g, {**done, **{x: "active" for x in cells}}), Row(out, label="read"))
            for x in cells:
                done[x] = "dim"
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    assert out == exp
    return W.save()


@run
def blackout_lines(pid):
    a, exp = example(pid)
    g = [r[:] for r in a["grid"]]
    m, n = len(g), len(g[0])
    W = Walk(pid, "First scan for dead pixels and note their rows and columns; only then black them out, so new zeros don't spread further.")
    rows, cols = set(), set()
    for r in range(m):
        z = [c for c in range(n) if g[r][c] == 0]
        rows |= {r} if z else set()
        cols |= set(z)
        W.step(f"Row {r}: " + (f"dead pixels in columns {z}." if z else "no dead pixels."), Grid(g, {**{(r, c): "active" for c in range(n)}, **{(rr, c): "mark" for rr in range(m) for c in range(n) if a['grid'][rr][c] == 0 and rr <= r}}), Vars(rows=sorted(rows), cols=sorted(cols)))
    for r in range(m):
        for c in range(n):
            if r in rows or c in cols:
                g[r][c] = 0
        W.step(f"Black out row {r}" + (" (it had a dead pixel)." if r in rows else f" in columns {sorted(cols)}."), Grid(g, {(rr, c): "dim" for rr in range(r + 1) for c in range(n) if rr in rows or c in cols}))
    assert g == exp
    return W.save()



@run
def flip_the_grid(pid):
    a, exp = example(pid)
    g = a["grid"]
    m, n = len(g), len(g[0])
    W = Walk(pid, "Row r, column c moves to row c, column r: each column of the input becomes a row of the output.")
    out = []
    for c in range(n):
        out.append([g[r][c] for r in range(m)])
        W.step(f"Column {c} becomes row {c}.", Grid(g, {(r, c): "active" for r in range(m)}, label="input"), Grid(out, {(c, r): "new" for r in range(m)}, label="output"))
    assert out == exp
    return W.save()


@run
def rotate_the_photo(pid):
    a, exp = example(pid)
    g = [r[:] for r in a["photo"]]
    n = len(g)
    W = Walk(pid, "A clockwise turn = flip over the main diagonal, then reverse each row. Both steps work in place.")
    W.step("The photo.", Grid(g))
    for r in range(n):
        for c in range(r + 1, n):
            g[r][c], g[c][r] = g[c][r], g[r][c]
            W.step(f"Flip: swap ({r}, {c}) with ({c}, {r}).", Grid(g, {(r, c): "new", (c, r): "new"}))
    for r in range(n):
        g[r].reverse()
        W.step(f"Reverse row {r}.", Grid(g, {(r, c): "new" for c in range(n)}))
    assert g == exp
    return W.save()



# ======================================================================== rotate-reverse / next-permutation

def next_perm_steps(W, d, label="values", wrap=True):
    i = len(d) - 2
    while i >= 0 and d[i] >= d[i + 1]:
        W.step(f"{d[i]} ≥ {d[i + 1]}: still descending from the right, keep scanning.", Row(d, st={i: "active", **{k: "dim" for k in range(i + 1, len(d))}}, label=label))
        i -= 1
    if i < 0:
        W.step("It's fully descending, the last arrangement.", Row(d, label=label))
        if wrap:
            d.reverse()
            W.step("Wrap around to the first arrangement.", Row(d, st={k: "new" for k in range(len(d))}, label=label))
        return None
    W.step(f"{d[i]} < {d[i + 1]}: position {i} is where the next arrangement differs.", Row(d, st={i: "mark", **{k: "dim" for k in range(i + 1, len(d))}}, label=label))
    j = len(d) - 1
    while d[j] <= d[i]:
        j -= 1
    W.step(f"The smallest value after it that's still bigger is {d[j]}: swap them.", Row(d, st={i: "mark", j: "active"}, label=label))
    d[i], d[j] = d[j], d[i]
    lo, hi = i + 1, len(d) - 1
    while lo < hi:
        d[lo], d[hi] = d[hi], d[lo]
        W.step(f"Reverse the tail: swap positions {lo} and {hi}.", Row(d, st={i: "found", lo: "new", hi: "new"}, label=label))
        lo += 1
        hi -= 1
    return d



@run
def next_arrangement(pid):
    a, exp = example(pid)
    d = list(a["values"])
    W = Walk(pid, "Keep the longest possible prefix; change as little as possible at the right end.")
    next_perm_steps(W, d)
    assert d == exp
    return W.save()


@run
def next_badge_number(pid):
    a, exp = example(pid)
    d = list(a["code"])
    W = Walk(pid, "The next larger number with the same digits changes as little as possible at the right end.")
    r = next_perm_steps(W, d, "code", wrap=False)
    res = "".join(d) if r is not None else ""
    if r is None:
        W.step("No larger number exists: \"\".", Row(d, label="code"), result="")
    assert res == exp
    return W.save()


@run
def one_step_back(pid):
    a, exp = example(pid)
    d = list(a["ratings"])
    W = Walk(pid, "The mirror image of next arrangement: find the rightmost DROP, swap it with the largest smaller value after it (its last copy), then reverse the rest.")
    i = len(d) - 2
    while i >= 0 and d[i] <= d[i + 1]:
        W.step(f"{d[i]} ≤ {d[i + 1]}: still rising from the right, keep scanning.", Row(d, st={i: "active", **{k: "dim" for k in range(i + 1, len(d))}}))
        i -= 1
    if i < 0:
        W.step("It's the first arrangement (ascending): wrap to the last.", Row(d))
        d.reverse()
    else:
        W.step(f"{d[i]} > {d[i + 1]}: position {i} is where the previous arrangement differs.", Row(d, st={i: "mark"}))
        j = len(d) - 1
        while d[j] >= d[i]:
            j -= 1
        W.step(f"The largest smaller value after it is {d[j]} (its last copy): swap.", Row(d, st={i: "mark", j: "active"}))
        d[i], d[j] = d[j], d[i]
        lo, hi = i + 1, len(d) - 1
        while lo < hi:
            d[lo], d[hi] = d[hi], d[lo]
            W.step(f"Reverse the tail: swap positions {lo} and {hi}.", Row(d, st={i: "found", lo: "new", hi: "new"}))
            lo += 1
            hi -= 1
    assert d == exp
    return W.save()



@run
def next_mirror_number(pid):
    a, exp = example(pid)
    code = a["code"]
    n = len(code)
    W = Walk(pid, "A palindrome is decided by its left half. Take the next arrangement of the left half, keep the middle, and mirror.")
    half = list(code[:n // 2])
    W.step(f"Left half {''.join(half)}" + (f", middle {code[n // 2]}" if n % 2 else "") + ".", Row(list(code), st={i: "active" for i in range(n // 2)}))
    r = next_perm_steps(W, half, "left half", wrap=False)
    if r is None:
        res = ""
        W.step("The half can't grow, so there's no larger mirror number.", Row(list(code)), result="")
    else:
        left = "".join(half)
        res = left + code[n // 2:(n + 1) // 2] + left[::-1]
        W.step(f"Mirror it: {res}.", Row(list(res), st={i: "new" for i in range(n)}), result=res)
    assert res == exp
    return W.save()


@run
def rotate_the_carousel(pid):
    a, exp = example(pid)
    v, k = list(a["slots"]), a["k"]
    n = len(v)
    k %= n
    W = Walk(pid, f"Turning right by {k} = reverse everything, then reverse the first {k} and the last {n - k}. Each reversal swaps pairs from the outside in.")

    def rev(lo, hi, what):
        while lo < hi:
            v[lo], v[hi] = v[hi], v[lo]
            W.step(f"{what}: swap positions {lo} and {hi}.", Row(v, st={lo: "new", hi: "new"}))
            lo += 1
            hi -= 1

    rev(0, n - 1, "Reverse all")
    rev(0, k - 1, f"Reverse the first {k}")
    rev(k, n - 1, f"Reverse the last {n - k}")
    assert v == exp
    return W.save()



# ======================================================================== matrix-in-place

@run
def colony_next_generation(pid):
    a, exp = example(pid)
    g = a["board"]
    m, n = len(g), len(g[0])
    W = Walk(pid, "Count each cell's living neighbours on the OLD board, then apply the rules. Here it goes one row at a time.")
    out = [["" for _ in range(n)] for _ in range(m)]
    for r in range(m):
        for c in range(n):
            live = sum(g[r + dr][c + dc] for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr or dc) and 0 <= r + dr < m and 0 <= c + dc < n)
            out[r][c] = 1 if live == 3 or (live == 2 and g[r][c]) else 0
        W.step(f"Row {r}: each cell survives with 2–3 neighbours or is born with exactly 3.", Grid(g, {**{(rr, c): "found" for rr in range(m) for c in range(n) if g[rr][c]}, **{(r, c): "active" for c in range(n)}}, label="now"), Grid(out, {(r, c): "new" for c in range(n)}, label="next"))
    assert out == exp
    return W.save()



@run
def soften_the_photo(pid):
    a, exp = example(pid)
    g = a["image"]
    m, n = len(g), len(g[0])
    W = Walk(pid, "Each pixel becomes the rounded-down average of the up-to-9 pixels around it, all from the original photo.")
    out = [[None] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            cells = [(rr, cc) for rr in range(max(0, r - 1), min(m, r + 2)) for cc in range(max(0, c - 1), min(n, c + 2))]
            s = sum(g[rr][cc] for rr, cc in cells)
            out[r][c] = s // len(cells)
            W.step(f"Pixel ({r}, {c}): {s} / {len(cells)} = {out[r][c]}.", Grid(g, {**{x: "found" for x in cells}, (r, c): "active"}, label="original"), Grid([[x if x is not None else "" for x in row] for row in out], {(r, c): "new"}, label="softened"))
    assert out == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
