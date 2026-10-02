import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from collections import Counter, deque
from lib import *

DONE = []


def run(fn):
    pid = fn.__name__.replace("_", "-")
    DONE.append((pid, fn(pid)))
    return fn


def win(cells, lo, hi, st=None, label=None, extra_ptr=None):
    """A row with the window [lo, hi] highlighted and its edges labelled."""
    s = {i: "active" for i in range(max(lo, 0), hi + 1)} if hi >= lo else {}
    s.update(st or {})
    ptr = {"L": lo if 0 <= lo < len(cells) else None, "R": hi if 0 <= hi < len(cells) else None}
    ptr.update(extra_ptr or {})
    return Row(list(cells), st=s, ptr=ptr, label=label)


# ======================================================================== fixed-window

@run
def best_sales_week(pid):
    a, exp = example(pid)
    v, k = a["sales"], a["k"]
    W = Walk(pid, f"Slide a window of {k} days: add the day that enters, subtract the day that leaves.")
    total = sum(v[:k])
    best = total
    W.step(f"First window totals {total}.", win(v, 0, k - 1), Vars(total=total, best=best))
    for i in range(k, len(v)):
        total += v[i] - v[i - k]
        best = max(best, total)
        W.step(f"Add {v[i]}, drop {v[i - k]}: total {total}. Best {best}.", win(v, i - k + 1, i, {i - k: "dim", i: "new"}), Vars(total=total, best=best))
    assert best == exp
    return W.save()


@run
def calm_stretches(pid):
    a, exp = example(pid)
    v, k, lim = a["noise"], a["k"], a["limit"]
    cap = lim * k
    W = Walk(pid, f"An average ≤ {lim} over {k} minutes means a total ≤ {cap}. Slide the window and compare totals.")
    total, count = sum(v[:k]), 0
    for i in range(k - 1, len(v)):
        if i >= k:
            total += v[i] - v[i - k]
        ok = total <= cap
        count += ok
        W.step(f"Window total {total} {'≤' if ok else '>'} {cap}: {'calm' if ok else 'too loud'}. Calm stretches: {count}.", win(v, i - k + 1, i, {j: "answer" for j in range(i - k + 1, i + 1)} if ok else None), Vars(total=total, calm=count))
    assert count == exp
    return W.save()


@run
def vowel_rich_window(pid):
    a, exp = example(pid)
    s, k = a["s"], a["k"]
    V = set("aeiou")
    W = Walk(pid, f"Slide a window of {k} letters, keeping a running count of vowels inside it.")
    count = sum(c in V for c in s[:k])
    best = count
    W.step(f"First window has {count} vowel{'s' if count != 1 else ''}.", win(s, 0, k - 1, {j: "found" for j in range(k) if s[j] in V}), Vars(vowels=count, best=best))
    for i in range(k, len(s)):
        count += (s[i] in V) - (s[i - k] in V)
        best = max(best, count)
        W.step(f"{s[i]} enters, {s[i - k]} leaves: {count} vowels. Best {best}.", win(s, i - k + 1, i, {**{j: "found" for j in range(i - k + 1, i + 1) if s[j] in V}, i - k: "dim"}), Vars(vowels=count, best=best))
    assert best == exp
    return W.save()


@run
def calm_shift(pid):
    a, exp = example(pid)
    c, m, k = a["customers"], a["moody"], a["minutes"]
    base = sum(x for x, y in zip(c, m) if not y)
    W = Walk(pid, f"Customers in good-mood minutes are happy anyway ({base}). Slide a {k}-minute window to find where calm saves the most moody minutes.")
    lost = [x * y for x, y in zip(c, m)]
    gain = sum(lost[:k])
    best = gain
    W.step(f"Happy anyway: {base}. The calm window saves {gain} at first.", Row(c, st={i: "mark" for i in range(len(c)) if m[i]}, label="customers (ringed = moody)"), win(lost, 0, k - 1, label="lost if moody"), Vars(saved=gain, best=best))
    for i in range(k, len(c)):
        gain += lost[i] - lost[i - k]
        best = max(best, gain)
        W.step(f"Slide: the window saves {gain}. Best {best}.", Row(c, st={j: "mark" for j in range(len(c)) if m[j]}, label="customers (ringed = moody)"), win(lost, i - k + 1, i, label="lost if moody"), Vars(saved=gain, best=best))
    W.step(f"Answer: {base} + {best} = {base + best}.", Vars(answer=base + best), result=base + best)
    assert base + best == exp
    return W.save()


@run
def seat_the_team(pid):
    a, exp = example(pid)
    v = a["seats"]
    n, t = len(v), sum(a["seats"])
    W = Walk(pid, f"The team has {t} members, so they'll fill some run of {t} seats round the table. Slide that window (wrapping round) and keep the run with most members already in it.")
    if t == 0:
        W.step("No team members: nothing to move.", Row(v), result=0)
        assert exp == 0
        return W.save()
    inside = sum(v[:t])
    best = inside
    W.step(f"Seats 0–{t - 1} already hold {inside}.", win(v, 0, t - 1), Vars(members_inside=inside, best=best))
    for i in range(t, n + t - 1):
        inside += v[i % n] - v[(i - t) % n]
        best = max(best, inside)
        lo = (i - t + 1) % n
        cells = {j % n: "active" for j in range(i - t + 1, i + 1)}
        W.step(f"Window starting at seat {lo}: {inside} members inside. Best {best}.", Row(v, st=cells, ptr={"start": lo}), Vars(members_inside=inside, best=best))
    W.step(f"Swaps needed: {t} − {best} = {t - best}.", Vars(swaps=t - best), result=t - best)
    assert t - best == exp
    return W.save()


# ======================================================================== longest-window

@run
def longest_fresh_run(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Grow the window to the right. When a letter repeats inside it, jump the left edge just past the earlier copy.")
    last, left, best = {}, 0, 0
    for i, c in enumerate(s):
        jumped = c in last and last[c] >= left
        if jumped:
            left = last[c] + 1
        last[c] = i
        best = max(best, i - left + 1)
        W.step((f"{c} repeats: move L past its earlier copy. " if jumped else f"Add {c}. ") + f"Window length {i - left + 1}, best {best}.", win(s, left, i), Vars(best=best))
    assert best == exp
    return W.save()


@run
def one_colour_banner(pid):
    a, exp = example(pid)
    s, k = a["s"], a["k"]
    W = Walk(pid, f"A window can become one colour if (length − its most common colour's count) ≤ {k}. Grow it; shrink from the left when it can't.")
    cnt, left, maxf, best = Counter(), 0, 0, 0
    for i, c in enumerate(s):
        cnt[c] += 1
        maxf = max(maxf, cnt[c])
        shrunk = False
        while i - left + 1 - maxf > k:
            cnt[s[left]] -= 1
            left += 1
            shrunk = True
        best = max(best, i - left + 1)
        W.step(f"Add {c}. Most common count {maxf}, repaints needed {i - left + 1 - maxf}" + (" after shrinking" if shrunk else "") + f". Best {best}.", win(s, left, i), Vars(repaints=i - left + 1 - maxf, best=best))
    assert best == exp
    return W.save()


@run
def patch_the_outage(pid):
    a, exp = example(pid)
    v, k = a["status"], a["k"]
    W = Walk(pid, f"Grow the window; while it holds more than {k} down minutes, drop minutes from the left.")
    left = zeros = best = 0
    for i, x in enumerate(v):
        zeros += x == 0
        while zeros > k:
            zeros -= v[left] == 0
            left += 1
        best = max(best, i - left + 1)
        W.step(f"Window has {zeros} down minute{'s' if zeros != 1 else ''} to patch. Length {i - left + 1}, best {best}.", win(v, left, i, {j: "mark" for j in range(left, i + 1) if v[j] == 0}), Vars(best=best))
    assert best == exp
    return W.save()


@run
def two_flavour_basket(pid):
    a, exp = example(pid)
    v = a["flavours"]
    W = Walk(pid, "Grow the window; when a third flavour enters, drop tubs from the left until only two flavours remain.")
    cnt, left, best = Counter(), 0, 0
    for i, f in enumerate(v):
        cnt[f] += 1
        while len(cnt) > 2:
            g = v[left]
            cnt[g] -= 1
            if not cnt[g]:
                del cnt[g]
            left += 1
        best = max(best, i - left + 1)
        W.step(f"Flavours in the window: {sorted(cnt)}. Length {i - left + 1}, best {best}.", win(v, left, i), Vars(best=best))
    assert best == exp
    return W.save()


@run
def steady_readings(pid):
    a, exp = example(pid)
    v, lim = a["readings"], a["limit"]
    W = Walk(pid, f"Two deques keep the window's max and min at their fronts. Shrink from the left while max − min > {lim}.")
    hi, lo = deque(), deque()
    left = best = 0
    for i, x in enumerate(v):
        while hi and v[hi[-1]] <= x:
            hi.pop()
        hi.append(i)
        while lo and v[lo[-1]] >= x:
            lo.pop()
        lo.append(i)
        while v[hi[0]] - v[lo[0]] > lim:
            left += 1
            if hi[0] < left:
                hi.popleft()
            if lo[0] < left:
                lo.popleft()
        best = max(best, i - left + 1)
        W.step(f"Window max {v[hi[0]]}, min {v[lo[0]]}, spread {v[hi[0]] - v[lo[0]]}. Length {i - left + 1}, best {best}.", win(v, left, i, {hi[0]: "mark", lo[0]: "mark"}), Row([v[j] for j in hi], label="max deque"), Row([v[j] for j in lo], label="min deque"))
    assert best == exp
    return W.save()


@run
def ride_on_a_budget(pid):
    a, exp = example(pid)
    v, b = a["fares"], a["budget"]
    W = Walk(pid, f"Grow the ride to the right; while it costs more than {b}, drop hops from the left.")
    left = total = best = 0
    for i, x in enumerate(v):
        total += x
        while total > b:
            total -= v[left]
            left += 1
        best = max(best, i - left + 1)
        W.step(f"Cost {total} ≤ {b}. Length {i - left + 1}, best {best}.", win(v, left, i) if left <= i else Row(v), Vars(cost=total, best=best))
    assert best == exp
    return W.save()


# ======================================================================== shortest-window

@run
def shortest_push(pid):
    a, exp = example(pid)
    v, t = a["gains"], a["target"]
    W = Walk(pid, f"Grow the window; as soon as it reaches {t}, record it and shrink from the left while it still does.")
    left = total = 0
    best = None
    for i, x in enumerate(v):
        total += x
        while total >= t:
            best = i - left + 1 if best is None else min(best, i - left + 1)
            W.step(f"Total {total} ≥ {t}: length {i - left + 1}. Shortest {best}. Drop {v[left]} from the left.", win(v, left, i, {j: "answer" for j in range(left, i + 1)}), Vars(total=total, shortest=best))
            total -= v[left]
            left += 1
        if total < t:
            W.step(f"Total {total} < {t}: keep growing.", win(v, left, i) if left <= i else Row(v), Vars(total=total, shortest=best if best is not None else "–"))
    res = best or 0
    assert res == exp
    return W.save()


@run
def smallest_covering_window(pid):
    a, exp = example(pid)
    s, t = a["s"], a["t"]
    need = Counter(t)
    missing = len(t)
    W = Walk(pid, f"Grow until the window covers \"{t}\", then shrink from the left while it still does. Keep the shortest.")
    left, best = 0, None
    have = Counter()
    for i, c in enumerate(s):
        have[c] += 1
        if have[c] <= need[c]:
            missing -= 1
        if missing:
            continue
        while True:
            d = s[left]
            if have[d] - 1 < need[d]:
                break
            have[d] -= 1
            left += 1
        if best is None or i - left + 1 < len(best):
            best = s[left:i + 1]
        W.step(f"Covered by \"{s[left:i + 1]}\". Shortest: \"{best}\". Drop {s[left]} to look for a shorter one.", win(s, left, i, {j: "answer" for j in range(left, i + 1)}), Vars(shortest=best))
        have[s[left]] -= 1
        missing += 1
        left += 1
    res = best or ""
    assert res == exp
    return W.save()


@run
def every_flavour_sampler(pid):
    a, exp = example(pid)
    v = a["jars"]
    d = len(set(v))
    W = Walk(pid, f"There are {d} flavours. Grow until the window holds all of them, then shrink from the left while it still does.")
    cnt, left, best = Counter(), 0, len(v)
    for i, f in enumerate(v):
        cnt[f] += 1
        while len(cnt) == d:
            best = min(best, i - left + 1)
            W.step(f"All {d} flavours in positions {left}–{i}: length {i - left + 1}. Shortest {best}.", win(v, left, i, {j: "answer" for j in range(left, i + 1)}), Vars(shortest=best))
            g = v[left]
            cnt[g] -= 1
            if not cnt[g]:
                del cnt[g]
            left += 1
    assert best == exp
    return W.save()


@run
def balance_the_quartet(pid):
    a, exp = example(pid, 2)
    s = a["s"]
    n = len(s)
    q = n // 4
    out = Counter(s)
    W = Walk(pid, f"Using example 3. Each voice needs {q}. A piece works if every voice OUTSIDE it appears at most {q} times; the piece can then be rewritten to fix the rest.")
    if all(out[c] == q for c in "SATB"):
        W.step("Already balanced.", Row(list(s)), result=0)
        assert exp == 0
        return W.save()
    W.step(f"Counts now: {dict((x, out[x]) for x in 'SATB')}. Every voice above {q} has to shrink, so the piece must cover the extra singers.", Row(list(s), st={j: "mark" for j in range(n) if out[s[j]] > q}), Vars(target=q))
    best, left = n, 0
    for i, c in enumerate(s):
        out[c] -= 1
        while left <= i and all(out[x] <= q for x in "SATB"):
            best = min(best, i - left + 1)
            W.step(f"Outside counts {dict((x, out[x]) for x in 'SATB')} are all ≤ {q}: piece length {i - left + 1}. Shortest {best}.", win(s, left, i, {j: "answer" for j in range(left, i + 1)}), Vars(shortest=best))
            out[s[left]] += 1
            left += 1
    assert best == exp
    return W.save()


@run
def shortest_trail_window(pid):
    a, exp = example(pid)
    s, t = a["s"], a["t"]
    W = Walk(pid, f"For every place the trail could end, find the latest start from which \"{t}\" still appears in order; keep the shortest window.")
    m = len(t)
    start = [-1] * (m + 1)
    best = None
    W.step(f"A window works if \"{t}\" can be read inside it left to right, skipping other letters. Track, for each prefix of \"{t}\", the latest place it could start.", Row(list(s)), Row(list(t), label="trail"))
    for i, c in enumerate(s):
        for j in range(m, 0, -1):
            if t[j - 1] == c:
                start[j] = i if j == 1 else start[j - 1]
        if start[m] >= 0 and c == t[-1]:
            cand = s[start[m]:i + 1]
            better = best is None or len(cand) < len(best)
            if better:
                best = cand
            W.step(f"Ending at position {i}: the latest start that still works is {start[m]}, giving \"{cand}\"" + (", the shortest so far." if better else f", not shorter than \"{best}\"."),
                   win(s, start[m], i, {j: "answer" for j in range(start[m], i + 1)} if better else None), Vars(shortest=best))
    res = best or ""
    if not W.steps:
        W.step(f"\"{t}\" never appears in order.", Row(list(s)), result="")
    assert res == exp
    return W.save()


# ======================================================================== at-most-k

def at_most(v, k, key):
    cnt, left, total = Counter(), 0, 0
    for i, x in enumerate(v):
        cnt[key(x)] += 1
        while key_count(cnt) > k:
            y = key(v[left])
            cnt[y] -= 1
            if not cnt[y]:
                del cnt[y]
            left += 1
        total += i - left + 1
    return total


def key_count(cnt):
    return len(cnt)


@run
def exactly_k_odd_tickets(pid):
    a, exp = example(pid)
    v, k = a["tickets"], a["k"]
    W = Walk(pid, f"Count windows with AT MOST {k} odd numbers, then subtract those with at most {k - 1}. For each right edge, every start from L works.")

    def sweep(limit, show):
        left = odd = total = 0
        for i, x in enumerate(v):
            odd += x & 1
            while odd > limit:
                odd -= v[left] & 1
                left += 1
            total += i - left + 1
            if show:
                W.step(f"At most {limit} odd: right edge {i} allows starts {left}–{i}, adding {i - left + 1}. Running total {total}.", win(v, left, i, {j: "mark" for j in range(left, i + 1) if v[j] & 1}))
        return total

    hi = sweep(k, True)
    lo = sweep(k - 1, False)
    W.step(f"At most {k - 1} odd gives {lo}. Exactly {k}: {hi} − {lo} = {hi - lo}.", Vars(at_most_k=hi, at_most_k_minus_1=lo), result=hi - lo)
    assert hi - lo == exp
    return W.save()


@run
def exactly_k_breeds(pid):
    a, exp = example(pid)
    v, k = a["pens"], a["k"]
    W = Walk(pid, f"Windows with exactly {k} breeds = (at most {k}) − (at most {k - 1}). Each count is one sliding window.")

    def sweep(limit, show):
        cnt, left, total = Counter(), 0, 0
        for i, x in enumerate(v):
            cnt[x] += 1
            while len(cnt) > limit:
                y = v[left]
                cnt[y] -= 1
                if not cnt[y]:
                    del cnt[y]
                left += 1
            total += i - left + 1
            if show:
                W.step(f"At most {limit} breeds: right edge {i} adds {i - left + 1}. Running total {total}.", win(v, left, i))
        return total

    hi = sweep(k, True)
    lo = sweep(k - 1, False)
    W.step(f"At most {k - 1} breeds gives {lo}. Exactly {k}: {hi} − {lo} = {hi - lo}.", Vars(at_most_k=hi, at_most_k_minus_1=lo), result=hi - lo)
    assert hi - lo == exp
    return W.save()


@run
def full_set_of_stamps(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Track the latest a, b and c. Once all three have appeared, every start up to the earliest of those three works.")
    last = {"a": -1, "b": -1, "c": -1}
    total = 0
    for i, c in enumerate(s):
        last[c] = i
        m = min(last.values())
        total += m + 1
        W.step(f"Ending at {i}: " + (f"starts 0–{m} contain a full set, adding {m + 1}." if m >= 0 else "not every letter has appeared yet.") + f" Total {total}.",
               Row(list(s), st={**{j: "found" for j in range(0, m + 1)}, **{p: "mark" for p in last.values() if p >= 0}}, ptr={"end": i}), Vars(total=total))
    assert total == exp
    return W.save()


@run
def products_under_a_cap(pid):
    a, exp = example(pid)
    v, cap = a["factors"], a["cap"]
    W = Walk(pid, f"Grow the window; while its product is at least {cap}, divide out the left factor. Every start from L to the right edge works.")
    if cap <= 1:
        W.step("No product of positive integers is below 1.", Row(v), result=0)
        assert exp == 0
        return W.save()
    prod, left, total = 1, 0, 0
    for i, x in enumerate(v):
        prod *= x
        while prod >= cap:
            prod //= v[left]
            left += 1
        total += i - left + 1
        W.step(f"Product {prod} < {cap}: {i - left + 1} new run{'s' if i - left + 1 != 1 else ''} end here. Total {total}.", win(v, left, i) if left <= i else Row(v), Vars(product=prod, total=total))
    assert total == exp
    return W.save()


# ======================================================================== window-frequency

@run
def scrambled_copies(pid):
    a, exp = example(pid)
    text, word = a["text"], a["word"]
    m = len(word)
    W = Walk(pid, f"Slide a window of {m} letters, updating its letter counts by one in and one out; record it when the counts equal \"{word}\"'s.")
    need = Counter(word)
    have = Counter(text[:m])
    out = []
    for i in range(m - 1, len(text)):
        if i >= m:
            have[text[i]] += 1
            have[text[i - m]] -= 1
            if not have[text[i - m]]:
                del have[text[i - m]]
        lo = i - m + 1
        ok = have == need
        if ok:
            out.append(lo)
        W.step(f"Window \"{text[lo:i + 1]}\" {'is' if ok else 'is not'} a scrambled copy.", win(text, lo, i, {j: "answer" for j in range(lo, i + 1)} if ok else None), Row(out, label="starts found"))
    assert out == exp
    return W.save()


@run
def repeat_within_reach(pid):
    a, exp = example(pid)
    v, k = a["codes"], a["k"]
    W = Walk(pid, f"Keep a set of the last {k} codes. A code already in the set repeats within reach.")
    window = []
    found = False
    for i, x in enumerate(v):
        if x in window:
            W.step(f"{x} is already among the last {k}: a repeat within reach.", Row(v, st={i: "answer", v.index(x, max(0, i - k)): "answer"}), Row(window, label="window set"), result=True)
            found = True
            break
        window.append(x)
        if len(window) > k:
            window.pop(0)
        W.step(f"{x} is new to the window.", win(v, i - len(window) + 1, i), Row(window, label="window set"))
    if not found:
        W.step("No repeats within reach.", Row(v), result=False)
    assert found == exp
    return W.save()


@run
def variety_per_window(pid):
    a, exp = example(pid)
    v, k = a["items"], a["k"]
    W = Walk(pid, "Keep counts per type. A type joins the variety when its count goes 0 → 1 and leaves it when it drops back to 0.")
    cnt, out = Counter(), []
    for i, x in enumerate(v):
        cnt[x] += 1
        if i >= k:
            y = v[i - k]
            cnt[y] -= 1
            if not cnt[y]:
                del cnt[y]
        if i >= k - 1:
            out.append(len(cnt))
            W.step(f"Window {v[i - k + 1:i + 1]}: {len(cnt)} different types.", win(v, i - k + 1, i), Row(out, st={len(out) - 1: "new"}, label="variety"))
    assert out == exp
    return W.save()


@run
def best_unique_bundle(pid):
    a, exp = example(pid)
    v, k = a["prices"], a["k"]
    W = Walk(pid, f"Slide a window of {k}, tracking its total and how many prices repeat inside it. Only windows with no repeats count.")
    cnt, dup, total, best = Counter(), 0, 0, 0
    for i, x in enumerate(v):
        cnt[x] += 1
        dup += cnt[x] == 2
        total += x
        if i >= k:
            y = v[i - k]
            cnt[y] -= 1
            dup -= cnt[y] == 1
            total -= y
        if i >= k - 1:
            ok = dup == 0
            if ok:
                best = max(best, total)
            W.step(f"Window total {total}, " + ("all different: a bundle." if ok else "has a repeat: not a bundle.") + f" Best {best}.", win(v, i - k + 1, i, {j: "answer" for j in range(i - k + 1, i + 1)} if ok else None), Vars(total=total, best=best))
    assert best == exp
    return W.save()


@run
def every_word_once(pid):
    a, exp = example(pid)
    s, words = a["s"], a["words"]
    L_ = len(words[0])
    w = len(words)
    need = Counter(words)
    W = Walk(pid, f"Words are {L_} letters long, so read s in {L_}-letter chunks from each offset 0–{L_ - 1} and slide a window of whole words.")
    out = []
    for off in range(L_):
        have, left, used = Counter(), off, 0
        for j in range(off, len(s) - L_ + 1, L_):
            chunk = s[j:j + L_]
            if chunk not in need:
                have.clear()
                used = 0
                left = j + L_
                W.step(f"Offset {off}: \"{chunk}\" isn't a word; restart after it.", Row(list(s), st={x: "mark" for x in range(j, j + L_)}))
                continue
            have[chunk] += 1
            used += 1
            while have[chunk] > need[chunk]:
                first = s[left:left + L_]
                have[first] -= 1
                used -= 1
                left += L_
            if used == w:
                out.append(left)
                W.step(f"Offset {off}: positions {left}–{left + w * L_ - 1} use every word once. Record {left}.", Row(list(s), st={x: "answer" for x in range(left, left + w * L_)}), Row(sorted(out), label="starts"))
                first = s[left:left + L_]
                have[first] -= 1
                used -= 1
                left += L_
    out.sort()
    assert out == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
