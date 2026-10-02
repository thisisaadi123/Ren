import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import *

DONE = []


CUSTOM = {
    "budget-pair": [{"prices": [1, 3, 4, 6, 8, 11, 15], "budget": 10}],
    "closest-pair-sum": [{"nums": [-7, -3, 0, 2, 5, 9, 12], "target": 4}],
    "reverse-letters-only": [{"text": "Ab-cD=ef-Gh"}],
    "fewest-swaps-to-palindrome": [{"word": "aabbcc"}, {"word": "mamad"}],
    "triples-under-a-cap": [{"values": [-2, 0, 1, 3, 4, -1], "cap": 3}],
    "triples-in-a-band": [{"values": [1, 2, 3, 4, 5], "low": 7, "high": 10}],
    "three-weights": [{"weights": [4, 9, 2, 7, 1, 12, 3], "target": 24}],
    "closest-triple-sum": [{"values": [-4, -1, 1, 2, 6, 9], "target": 5}],
    "hidden-word": [{"word": "rena", "text": "recentgains"}],
    "count-hidden-words": [{"text": "abcdefg", "words": ["a", "bb", "ace", "gfe", "bdf", "acg"]}],
    "longest-word-by-deleting": [{"text": "abpcplea", "dictionary": ["ale", "apple", "monkey", "plea", "pal", "bpc"]}],
    "pairs-within-budget": [{"mains": [3, 5, 8, 12, 15], "sides": [1, 2, 4, 7, 9], "budget": 13}],
    "sort-k-colours": [{"balls": [3, 1, 4, 2, 5, 2, 4, 1, 3, 5], "k": 5}],
    "fewest-swaps-three-colours": [{"balls": [2, 0, 1, 2, 1, 0, 0, 2, 1]}],
}
run = make_runner(DONE, CUSTOM)


def S(text, st=None, ptr=None, label=None):
    """A string drawn as a row of letters."""
    return Row(list(text), st=st, ptr=ptr, label=label)


# ======================================================================== opposite-ends

@run
def budget_pair(pid):
    a, exp = example(pid)
    p, b = a["prices"], a["budget"]
    W = Walk(pid, f"The prices are sorted, so start at both ends: too much → move right end in; too little → move left end out.")
    i, j = 0, len(p) - 1
    while i < j:
        s = p[i] + p[j]
        if s == b:
            W.step(f"{p[i]} + {p[j]} = {b}: found it.", Row(p, st={i: "answer", j: "answer"}, ptr={"i": i, "j": j}), result=[i, j])
            break
        W.step(f"{p[i]} + {p[j]} = {s} {'>' if s > b else '<'} {b}: move {'j left' if s > b else 'i right'}.", Row(p, st={i: "active", j: "active"}, ptr={"i": i, "j": j}))
        if s > b:
            j -= 1
        else:
            i += 1
    assert [i, j] == exp
    return W.save()


@run
def closest_pair_sum(pid):
    a, exp = example(pid)
    v, t = sorted(a["nums"]), a["target"]
    W = Walk(pid, f"Sort, then squeeze from both ends, keeping the sum closest to {t}.")
    W.step("Sorted: " + ", ".join(map(str, v)) + ".", Row(v))
    i, j, best = 0, len(v) - 1, None
    while i < j:
        s = v[i] + v[j]
        if best is None or abs(s - t) < abs(best - t) or (abs(s - t) == abs(best - t) and s < best):
            best = s
        W.step(f"{v[i]} + {v[j]} = {s}. Closest so far: {best}.", Row(v, st={i: "active", j: "active"}, ptr={"i": i, "j": j}), Vars(best=best))
        if s == t:
            break
        if s < t:
            i += 1
        else:
            j -= 1
    assert best == exp
    return W.save()


@run
def biggest_water_tank(pid):
    a, exp = example(pid)
    h = a["posts"]
    W = Walk(pid, "Start with the widest tank. The shorter post limits it, so only moving that post inward can ever help.")
    i, j, best = 0, len(h) - 1, 0
    while i < j:
        area = (j - i) * min(h[i], h[j])
        best = max(best, area)
        W.step(f"Posts {i} and {j}: width {j - i} × height {min(h[i], h[j])} = {area}. Best {best}. Move the shorter post in.", Row(h, st={i: "active", j: "active"}, ptr={"i": i, "j": j}), Vars(best=best))
        if h[i] < h[j]:
            i += 1
        else:
            j -= 1
    assert best == exp
    return W.save()


@run
def squares_in_order(pid):
    a, exp = example(pid)
    v = a["values"]
    n = len(v)
    W = Walk(pid, "The biggest square is at one of the two ends. Fill the answer from the back, taking the larger end each time.")
    out = [None] * n
    i, j = 0, n - 1
    for k in range(n - 1, -1, -1):
        if abs(v[i]) > abs(v[j]):
            out[k] = v[i] * v[i]
            took = i
            i += 1
        else:
            out[k] = v[j] * v[j]
            took = j
            j -= 1
        W.step(f"|{v[took]}| is the larger end: write {out[k]} at position {k}.", Row(v, st={took: "active"}, ptr={"i": i if i <= j else None, "j": j if j >= i else None}), Row(out, st={k: "new"}, label="squares"))
    assert out == exp
    return W.save()


@run
def reverse_letters_only(pid):
    a, exp = example(pid)
    s = list(a["text"])
    W = Walk(pid, "Two pointers from both ends skip anything that isn't a letter, then swap.")
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalpha():
            i += 1
            continue
        if not s[j].isalpha():
            j -= 1
            continue
        s[i], s[j] = s[j], s[i]
        W.step(f"Swap {s[j]} and {s[i]}.", S(s, st={i: "new", j: "new"}, ptr={"i": i, "j": j}))
        i += 1
        j -= 1
    res = "".join(s)
    W.step(f"Result: {res}", S(s))
    assert res == exp
    return W.save()


@run
def boats_for_hikers(pid):
    a, exp = example(pid)
    w, lim = sorted(a["weights"]), a["limit"]
    W = Walk(pid, f"Sort the weights. The heaviest hiker always takes a boat; the lightest joins them if they fit under {lim}.")
    i, j, boats = 0, len(w) - 1, 0
    W.step("Sorted: " + ", ".join(map(str, w)) + ".", Row(w))
    while i <= j:
        boats += 1
        if i < j and w[i] + w[j] <= lim:
            W.step(f"{w[j]} and {w[i]} share boat {boats} ({w[i] + w[j]} ≤ {lim}).", Row(w, st={i: "answer", j: "answer"}, ptr={"light": i, "heavy": j}))
            i += 1
        else:
            W.step(f"{w[j]} goes alone in boat {boats}.", Row(w, st={j: "answer"}, ptr={"light": i, "heavy": j}))
        j -= 1
    assert boats == exp
    return W.save()


@run
def fewest_swaps_to_palindrome(pid):
    a, exp = example(pid)
    s = list(a["word"])
    W = Walk(pid, "Fix the outer letters first: for the left letter, find its partner nearest the right end and swap it there step by step.")
    i, j, moves = 0, len(s) - 1, 0
    while i < j:
        k = j
        while k > i and s[k] != s[i]:
            k -= 1
        if k == i:
            # The odd letter: move it one step towards the middle and retry.
            s[i], s[i + 1] = s[i + 1], s[i]
            moves += 1
            W.step(f"{s[i + 1]} has no partner: it's the middle letter. Nudge it one step inward.", S(s, st={i + 1: "mark"}, ptr={"i": i, "j": j}), Vars(moves=moves))
            continue
        for t in range(k, j):
            s[t], s[t + 1] = s[t + 1], s[t]
            moves += 1
        W.step(f"Move the partner of {s[i]} from position {k} to {j}: {j - k} swap{'s' if j - k != 1 else ''}.", S(s, st={i: "found", j: "found"}, ptr={"i": i, "j": j}), Vars(moves=moves))
        i += 1
        j -= 1
    W.intro("Work from the outside in. Bringing a letter's partner to the far end costs one swap per position it moves.", S(a["word"]))
    assert moves == exp
    return W.save()


# ======================================================================== k-sum

def ksum_frame(v, i, j, k):
    return Row(v, st={i: "mark", j: "active", k: "active"}, ptr={"i": i, "lo": j, "hi": k})


@run
def zero_sum_triples(pid):
    a, exp = example(pid)
    v = sorted(a["values"])
    W = Walk(pid, "Sort. Fix the first value, then find pairs after it that add up to its negative with two pointers. Skip repeats.")
    W.step("Sorted: " + ", ".join(map(str, v)) + ".", Row(v))
    out = []
    for i in range(len(v) - 2):
        if i and v[i] == v[i - 1]:
            continue
        j, k = i + 1, len(v) - 1
        while j < k:
            s = v[i] + v[j] + v[k]
            if s == 0:
                out.append([v[i], v[j], v[k]])
                W.step(f"{v[i]} + {v[j]} + {v[k]} = 0: record it.", ksum_frame(v, i, j, k), Row([str(t) for t in out], label="found"))
                j += 1
                while j < k and v[j] == v[j - 1]:
                    j += 1
                k -= 1
            elif s < 0:
                W.step(f"{v[i]} + {v[j]} + {v[k]} = {s} < 0: move lo right.", ksum_frame(v, i, j, k))
                j += 1
            else:
                W.step(f"{v[i]} + {v[j]} + {v[k]} = {s} > 0: move hi left.", ksum_frame(v, i, j, k))
                k -= 1
    assert out == exp
    return W.save()


@run
def triples_under_a_cap(pid):
    a, exp = example(pid)
    v, cap = sorted(a["values"]), a["cap"]
    W = Walk(pid, f"Sort. For each first value, if lo + hi works then every pair from lo with something up to hi works too.")
    count = 0
    for i in range(len(v) - 2):
        j, k = i + 1, len(v) - 1
        while j < k:
            s = v[i] + v[j] + v[k]
            if s < cap:
                count += k - j
                W.step(f"{v[i]} + {v[j]} + {v[k]} = {s} < {cap}: all {k - j} choices of the third value up to hi work. Count {count}.", ksum_frame(v, i, j, k))
                j += 1
            else:
                W.step(f"{v[i]} + {v[j]} + {v[k]} = {s} ≥ {cap}: move hi left.", ksum_frame(v, i, j, k))
                k -= 1
    assert count == exp
    return W.save()


@run
def triples_in_a_band(pid):
    a, exp = example(pid)
    v, lo, hi = sorted(a["values"]), a["low"], a["high"]
    W = Walk(pid, f"Count triples with sum < {hi + 1}, then subtract those with sum < {lo}. Each count is a two-pointer sweep for every first value.")

    def below(cap):
        c = 0
        for i in range(len(v) - 2):
            j, k = i + 1, len(v) - 1
            while j < k:
                s = v[i] + v[j] + v[k]
                if s < cap:
                    c += k - j
                    W.step(f"Sum below {cap}: {v[i]} + {v[j]} + {v[k]} = {s}, so all {k - j} choices up to hi work. Count {c}.", ksum_frame(v, i, j, k))
                    j += 1
                else:
                    W.step(f"Sum below {cap}: {v[i]} + {v[j]} + {v[k]} = {s} is too big, move hi left.", ksum_frame(v, i, j, k))
                    k -= 1
        return c

    up, down = below(hi + 1), below(lo)
    res = up - down
    W.step(f"{up} − {down} = {res} triples in the band.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()



@run
def three_weights(pid):
    a, exp = example(pid)
    v, t = sorted(a["weights"]), a["target"]
    W = Walk(pid, f"Sort, fix one weight, and look for two more that make up the rest of {t}.")
    found = False
    for i in range(len(v) - 2):
        j, k = i + 1, len(v) - 1
        while j < k:
            s = v[i] + v[j] + v[k]
            if s == t:
                W.step(f"{v[i]} + {v[j]} + {v[k]} = {t}.", Row(v, st={i: "answer", j: "answer", k: "answer"}, ptr={"i": i, "lo": j, "hi": k}), result=True)
                found = True
                break
            W.step(f"{v[i]} + {v[j]} + {v[k]} = {s}: move {'lo right' if s < t else 'hi left'}.", ksum_frame(v, i, j, k))
            if s < t:
                j += 1
            else:
                k -= 1
        if found:
            break
    assert found == exp
    return W.save()


@run
def closest_triple_sum(pid):
    a, exp = example(pid)
    v, t = sorted(a["values"]), a["target"]
    W = Walk(pid, f"Sort, fix one value, and squeeze the other two, keeping the sum closest to {t}.")
    best = None
    for i in range(len(v) - 2):
        j, k = i + 1, len(v) - 1
        while j < k:
            s = v[i] + v[j] + v[k]
            if best is None or abs(s - t) < abs(best - t) or (abs(s - t) == abs(best - t) and s < best):
                best = s
            W.step(f"{v[i]} + {v[j]} + {v[k]} = {s}. Closest so far: {best}.", ksum_frame(v, i, j, k), Vars(best=best))
            if s < t:
                j += 1
            elif s > t:
                k -= 1
            else:
                break
    assert best == exp
    return W.save()


# ======================================================================== subsequence-check

def subseq_steps(W, word, text, final_text=None):
    i = 0
    for j, ch in enumerate(text):
        if i < len(word) and word[i] == ch:
            i += 1
            W.step(f"text[{j}] = {ch} matches the next letter of \"{word}\".", S(word, st={k: "found" for k in range(i)}, label="word"), S(text, st={j: "answer"}, ptr={"j": j}, label="text"))
    return i == len(word)


@run
def hidden_word(pid):
    a, exp = example(pid)
    w, t = a["word"], a["text"]
    W = Walk(pid, "Scan the text once. Whenever it shows the next letter you need, tick that letter off.")
    ok = subseq_steps(W, w, t)
    W.step("Every letter was found in order." if ok else "The text ran out first.", S(w, st={k: "found" for k in range(len(w))} if ok else {}, label="word"), result=ok)
    assert ok == exp
    return W.save()


def is_sub(w, t):
    it = iter(t)
    return all(c in it for c in w)


@run
def count_hidden_words(pid):
    a, exp = example(pid)
    t = a["text"]
    W = Walk(pid, "Check each word with the tick-off scan: walk the text once, matching the word's letters in order.")
    count = 0
    for w in a["words"]:
        ok = is_sub(w, t)
        count += ok
        W.step(f"\"{w}\" is {'hidden' if ok else 'not hidden'}. Count {count}.", S(t, label="text"), S(w, st={k: "found" if ok else "mark" for k in range(len(w))}, label="word"))
    assert count == exp
    return W.save()


@run
def longest_word_by_deleting(pid):
    a, exp = example(pid)
    t = a["text"]
    W = Walk(pid, "Test each dictionary word against the text with the tick-off scan, and keep the longest (alphabetically first on ties).")
    best = ""
    for w in a["dictionary"]:
        ok = is_sub(w, t)
        if ok and (len(w) > len(best) or (len(w) == len(best) and w < best)):
            best = w
        W.step(f"\"{w}\": {'can be made' if ok else 'cannot be made'}. Best so far: \"{best}\".", S(t, label="text"), S(w, st={k: "found" if ok else "mark" for k in range(len(w))}, label="word"))
    assert best == exp
    return W.save()


# ======================================================================== merge-sorted

@run
def merge_two_shelves(pid):
    a, exp = example(pid)
    x, y = a["left"], a["right"]
    W = Walk(pid, "Compare the front book of each shelf and move the shorter one across.")
    i = j = 0
    out = []
    while i < len(x) or j < len(y):
        take = j >= len(y) or (i < len(x) and x[i] <= y[j])
        out.append(x[i] if take else y[j])
        W.step(f"Take {out[-1]} from the {'left' if take else 'right'} shelf.", Row(x, st={k: "dim" for k in range(i)}, ptr={"i": i if i < len(x) else None}, label="left"),
               Row(y, st={k: "dim" for k in range(j)}, ptr={"j": j if j < len(y) else None}, label="right"), Row(out, st={len(out) - 1: "new"}, label="merged"))
        if take:
            i += 1
        else:
            j += 1
    assert out == exp
    return W.save()


@run
def merge_two_train_lines(pid):
    a, exp = example(pid)
    x, y = a["first"], a["second"]
    W = Walk(pid, "Keep a tail on the merged train and attach whichever front car is smaller.")
    i = j = 0
    out = []
    while i < len(x) or j < len(y):
        take = j >= len(y) or (i < len(x) and x[i] <= y[j])
        out.append(x[i] if take else y[j])
        W.step(f"Attach car {out[-1]} from the {'first' if take else 'second'} train.", L(x, st={k: "dim" for k in range(i)}, ptr={"a": i if i < len(x) else None}, label="first"),
               L(y, st={k: "dim" for k in range(j)}, ptr={"b": j if j < len(y) else None}, label="second"), L(out, st={len(out) - 1: "new"}, label="merged"))
        if take:
            i += 1
        else:
            j += 1
    assert out == exp
    return W.save()


@run
def closest_across_lists(pid):
    a, exp = example(pid)
    x, y = a["a"], a["b"]
    W = Walk(pid, "Walk both sorted lists together, always moving the pointer at the smaller value: that's the only move that can shrink the gap.")
    i = j = 0
    best = None
    while i < len(x) and j < len(y):
        d = abs(x[i] - y[j])
        best = d if best is None else min(best, d)
        W.step(f"|{x[i]} − {y[j]}| = {d}. Smallest so far: {best}.", Row(x, st={i: "active"}, ptr={"i": i}, label="a"), Row(y, st={j: "active"}, ptr={"j": j}, label="b"), Vars(best=best))
        if x[i] < y[j]:
            i += 1
        else:
            j += 1
    assert best == exp
    return W.save()


@run
def pairs_within_budget(pid):
    a, exp = example(pid)
    m, s, b = a["mains"], a["sides"], a["budget"]
    W = Walk(pid, f"Go through mains from cheapest; the dearest affordable side only moves left as mains get pricier.")
    j, count = len(s) - 1, 0
    for i, price in enumerate(m):
        while j >= 0 and price + s[j] > b:
            j -= 1
        count += j + 1
        W.step(f"Main {price}: sides up to {s[j] if j >= 0 else 'none'} fit, {j + 1} combination{'s' if j != 0 else ''}. Total {count}.", Row(m, st={i: "active"}, label="mains"),
               Row(s, st={k: "found" for k in range(j + 1)}, ptr={"j": j if j >= 0 else None}, label="sides"))
    assert count == exp
    return W.save()


# ======================================================================== read-write-pointers

def rw_walk(W, v, keep, why, out_check):
    w = 0
    cells = list(v)
    for r in range(len(cells)):
        k = keep(cells, w, r)
        if k:
            cells[w] = cells[r]
            w += 1
        W.step(f"read {r} ({v[r]}): {why(k, v[r])}", Row(cells, st={**{x: "found" for x in range(w)}, r: "active"}, ptr={"write": w if w < len(cells) else None, "read": r}))
    return cells[:w]


@run
def unique_stock_codes(pid):
    a, exp = example(pid)
    v = a["codes"]
    W = Walk(pid, "A read pointer scans everything; a write pointer marks where the next new code goes.")
    out = rw_walk(W, v, lambda c, w, r: w == 0 or c[r] != c[w - 1], lambda k, x: "a new code, write it." if k else "a repeat, skip.", None)
    assert out == exp
    return W.save()


@run
def at_most_twice(pid):
    a, exp = example(pid)
    v = a["values"]
    W = Walk(pid, "Write a value unless it equals the value two places back in what's been written.")
    out = rw_walk(W, v, lambda c, w, r: w < 2 or c[r] != c[w - 2], lambda k, x: "keep it." if k else "a third copy, skip.", None)
    assert out == exp
    return W.save()


@run
def remove_the_blanks(pid):
    a, exp = example(pid)
    v, blank = a["cells"], a["blank"]
    W = Walk(pid, f"Copy every cell that isn't {blank} to the write position.")
    out = rw_walk(W, v, lambda c, w, r: c[r] != blank, lambda k, x: "keep it." if k else "blank, skip.", None)
    assert out == exp
    return W.save()


@run
def compact_the_shelf(pid):
    a, exp = example(pid)
    v = list(a["slots"])
    W = Walk(pid, "Swap each item into the write position; the empty slots drift to the right.")
    w = 0
    for r in range(len(v)):
        if v[r] != 0:
            v[w], v[r] = v[r], v[w]
            w += 1
            W.step(f"Item {v[w - 1]}: swap it into slot {w - 1}.", Row(v, st={w - 1: "new"}, ptr={"write": w if w < len(v) else None, "read": r}))
        else:
            W.step("Empty slot: skip.", Row(v, st={r: "dim"}, ptr={"write": w, "read": r}))
    assert v == exp
    return W.save()


@run
def run_length_code(pid):
    a, exp = example(pid)
    t = a["text"]
    W = Walk(pid, "Find each run with a second pointer, then write the character and (if longer than 1) its length.")
    out, i = "", 0
    while i < len(t):
        j = i
        while j < len(t) and t[j] == t[i]:
            j += 1
        out += t[i] + (str(j - i) if j - i > 1 else "")
        W.step(f"Run of {j - i} \"{t[i]}\": write \"{t[i]}{j - i if j - i > 1 else ''}\".", S(t, st={k: "active" for k in range(i, j)}, ptr={"i": i, "j": j if j < len(t) else None}), Vars(output=out))
        i = j
    assert out == exp
    return W.save()


# ======================================================================== partition

@run
def three_colours(pid):
    a, exp = example(pid)
    v = list(a["balls"])
    W = Walk(pid, "Three regions: 0s before low, 2s after high, and mid scanning the unknown middle.")
    lo, mid, hi = 0, 0, len(v) - 1
    while mid <= hi:
        x = v[mid]
        if x == 0:
            v[lo], v[mid] = v[mid], v[lo]
            text = "0: swap it to low; move low and mid."
            lo += 1
            mid += 1
        elif x == 1:
            text = "1: already in the middle; move mid."
            mid += 1
        else:
            v[mid], v[hi] = v[hi], v[mid]
            text = "2: swap it to high; move high in (mid stays to check what came back)."
            hi -= 1
        W.step(text, Row(v, st={**{k: "found" for k in range(lo)}, **{k: "found" for k in range(hi + 1, len(v))}}, ptr={"low": lo if lo < len(v) else None, "mid": mid if mid < len(v) else None, "high": hi if hi >= 0 else None}))
    assert v == exp
    return W.save()


@run
def split_around_a_pivot(pid):
    a, exp = example(pid)
    v, p = a["values"], a["pivot"]
    W = Walk(pid, f"One pass to collect each group in order: less than {p}, equal, greater. Then join them.")
    less, eq, more = [], [], []
    for i, x in enumerate(v):
        (less if x < p else eq if x == p else more).append(x)
        W.step(f"{x} goes in the {'less' if x < p else 'equal' if x == p else 'greater'} group.", Row(v, st={**{k: "dim" for k in range(i)}, i: "active"}), Row(less, label="less"), Row(eq, label="equal"), Row(more, label="greater"))
    out = less + eq + more
    W.step("Join the groups.", Row(out))
    assert out == exp
    return W.save()


@run
def sort_k_colours(pid):
    a, exp = example(pid)
    v, k = list(a["balls"]), a["k"]
    W = Walk(pid, "Rainbow sort: split the colour range in half, partition the balls around it, and recurse on each side. That's O(n log k).")

    def go(lo, hi, c1, c2):
        if lo >= hi or c1 >= c2:
            return
        mid = (c1 + c2) // 2
        i, j = lo, hi
        while i <= j:
            while i <= j and v[i] <= mid:
                i += 1
            while i <= j and v[j] > mid:
                j -= 1
            if i < j:
                v[i], v[j] = v[j], v[i]
        W.step(f"Colours {c1}–{c2}: put colours ≤ {mid} on the left of positions {lo}–{hi}.", Row(v, st={**{x: "found" for x in range(lo, i)}, **{x: "active" for x in range(i, hi + 1)}}))
        go(lo, i - 1, c1, mid)
        go(i, hi, mid + 1, c2)

    go(0, len(v) - 1, 1, k)
    assert v == exp
    return W.save()


@run
def fewest_swaps_three_colours(pid):
    a, exp = example(pid)
    v = a["balls"]
    W = Walk(pid, "Count which colour sits in which target zone. Swap mismatched pairs directly first; whatever is left forms 3-way cycles that need 2 swaps each.")
    c = [v.count(i) for i in range(3)]
    zone = [0] * c[0] + [1] * c[1] + [2] * c[2]
    m = [[0] * 3 for _ in range(3)]
    for i, (z, x) in enumerate(zip(zone, v)):
        m[z][x] += 1
        W.step(f"Position {i} is in the {z}-zone and holds a {x}" + (": already right." if z == x else ": misplaced."), Row(v, st={**{k: ("found" if v[k] == zone[k] else "mark") for k in range(i)}, i: "active"}), Row(zone, label="target zone"))
    swaps = 0
    for x, y in ((0, 1), (0, 2), (1, 2)):
        d = min(m[x][y], m[y][x])
        swaps += d
        m[x][y] -= d
        m[y][x] -= d
        if d:
            W.step(f"{d} {x} ↔ {y} pair{'s' if d != 1 else ''} swap straight into place. Swaps {swaps}.", Vars(swaps=swaps))
    left = sum(m[x][y] for x in range(3) for y in range(3) if x != y)
    swaps += 2 * (left // 3)
    W.step(f"{left} balls remain in {left // 3} three-way cycle{'s' if left // 3 != 1 else ''}, 2 swaps each. Total {swaps}.", Vars(total=swaps), result=swaps)
    assert swaps == exp
    return W.save()



if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
