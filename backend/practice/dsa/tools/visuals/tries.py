import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
import bisect
from lib import *
from design import Trie

DONE = []


def run(fn):
    pid = fn.__name__.replace("_", "-")
    DONE.append((pid, fn(pid)))
    return fn


@run
def autocomplete_suggestions(pid):
    a, exp = example(pid)
    p, typed = sorted(a["products"]), a["typed"]
    W = Walk(pid, "Sort the products once. Products sharing a prefix sit together, so after each letter a binary search finds where they start.")
    W.step("Sorted products.", Row(p))
    out = []
    for i in range(1, len(typed) + 1):
        pre = typed[:i]
        k = bisect.bisect_left(p, pre)
        hits = [w for w in p[k:k + 3] if w.startswith(pre)]
        out.append(hits)
        W.step(f"\"{pre}\": matches start at position {k}; suggest {hits or 'nothing'}.", Row(p, st={**{j: "found" for j in range(len(p)) if p[j].startswith(pre)}, **{p.index(h, k): "answer" for h in hits}}, ptr={"start": k if k < len(p) else None}))
    assert out == exp
    return W.save()


@run
def prefix_scores(pid):
    a, exp = example(pid)
    words = a["words"]
    t = Trie()
    passes = {}
    W = Walk(pid, "Insert every word into a trie, counting how many words pass through each node. A word's score adds up the counts along its path.")
    for w in words:
        path = t.insert(w)
        for x in path[1:]:
            passes[x] = passes.get(x, 0) + 1
        W.step(f"Insert \"{w}\"; every node on its path gains 1.", NT([dict(n) for n in t.nodes], {x: "active" for x in path[1:]}, passes, label="trie (notes = words passing)"))
    out = []
    for w in words:
        _, path = t.walk(w)
        s = sum(passes[x] for x in path[1:])
        out.append(s)
        W.step(f"\"{w}\": {' + '.join(str(passes[x]) for x in path[1:])} = {s}.", NT([dict(n) for n in t.nodes], {x: "answer" for x in path[1:]}, passes, label="trie (notes = words passing)"), result=s)
    assert out == exp
    return W.save()


@run
def count_pattern_matches(pid):
    a, exp = example(pid)
    words, pats = a["words"], a["patterns"]
    t = Trie()
    ends = {}
    for w in words:
        path = t.insert(w)
        ends[path[-1]] = ends.get(path[-1], 0) + 1
    W = Walk(pid, "Put the words in a trie with a count of words ending at each node. A pattern walks the trie: a letter follows one branch, a dot follows all of them.")
    W.step("The trie of words (notes = words ending there).", NT([dict(n) for n in t.nodes], {x: "found" for x in ends}, ends))
    out = []
    for p in pats:
        frontier, seen = [0], set()
        for ch in p:
            nxt = []
            for f in frontier:
                nxt += list(t.kids[f].values()) if ch == "." else ([t.kids[f][ch]] if ch in t.kids[f] else [])
            frontier = nxt
            seen.update(frontier)
        c = sum(ends.get(f, 0) for f in frontier)
        out.append(c)
        W.step(f"\"{p}\" ends on {len(frontier)} node{'s' if len(frontier) != 1 else ''} holding {c} word{'s' if c != 1 else ''}.", NT([dict(n) for n in t.nodes], {**{x: "active" for x in seen}, **{f: "answer" for f in frontier if f in ends}}, ends), result=c)
    assert out == exp
    return W.save()


def trace_path(board, word, dirs):
    m, n = len(board), len(board[0])

    def go(r, c, i, used):
        if board[r][c] != word[i]:
            return None
        if i == len(word) - 1:
            return [(r, c)]
        used.add((r, c))
        for dr, dc in dirs:
            rr, cc = r + dr, c + dc
            if 0 <= rr < m and 0 <= cc < n and (rr, cc) not in used:
                rest = go(rr, cc, i + 1, used)
                if rest:
                    used.discard((r, c))
                    return [(r, c)] + rest
        used.discard((r, c))
        return None

    for r in range(m):
        for c in range(n):
            p = go(r, c, 0, set())
            if p:
                return p
    return None


@run
def word_hunt(pid):
    a, exp = example(pid)
    board, words = a["board"], a["words"]
    g = [list(r) for r in board]
    W = Walk(pid, "Put all the words in one trie and DFS from every cell, following the trie as you go. A path stops as soon as no word continues it.")
    W.step("The board.", Grid(g), Row(sorted(set(words)), label="words"))
    found = []
    for w in sorted(set(words)):
        p = trace_path(board, w, ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if p:
            found.append(w)
            W.step(f"\"{w}\" can be traced.", Grid(g, {x: "answer" for x in p}), Row(found, label="found"))
        else:
            W.step(f"\"{w}\" can't be traced: the trie walk dies out.", Grid(g), Row(found, label="found"))
    assert found == exp
    return W.save()


@run
def straight_line_words(pid):
    a, exp = example(pid)
    board, words = a["board"], a["words"]
    g = [list(r) for r in board]
    m, n = len(g), len(g[0])
    dirs = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]
    W = Walk(pid, "From every cell, walk the trie along each of the 8 straight directions. Any word that ends along the way is hidden.")
    W.step("The board.", Grid(g), Row(sorted(set(words)), label="words"))
    found = []
    for w in sorted(set(words)):
        line = None
        for r in range(m):
            for c in range(n):
                for dr, dc in dirs:
                    cells = [(r + i * dr, c + i * dc) for i in range(len(w))]
                    if all(0 <= x < m and 0 <= y < n and g[x][y] == w[i] for i, (x, y) in enumerate(cells)):
                        line = cells
                        break
                if line:
                    break
            if line:
                break
        if line:
            found.append(w)
            W.step(f"\"{w}\" runs in a straight line.", Grid(g, {x: "answer" for x in line}), Row(found, label="found"))
        else:
            W.step(f"\"{w}\" isn't in any straight line.", Grid(g), Row(found, label="found"))
    assert found == exp
    return W.save()


def bits(x, width):
    return format(x, f"0{width}b")


@run
def best_xor_pair(pid):
    a, exp = example(pid)
    v = a["nums"]
    width = max(1, max(v).bit_length())
    W = Walk(pid, "Build the answer bit by bit from the top: try setting the next bit, and keep it if two numbers' prefixes can produce it.")
    W.step("The numbers in binary.", Row([bits(x, width) for x in v]))
    best, mask = 0, 0
    for b in range(width - 1, -1, -1):
        mask |= 1 << b
        pre = {x & mask for x in v}
        want = best | (1 << b)
        ok = any(want ^ p in pre for p in pre)
        if ok:
            best = want
        W.step(f"Bit {b}: can the XOR reach {bits(want >> b, width - b)}…? {'Yes, keep it.' if ok else 'No.'}", Row([bits(x, width)[: width - b] for x in v], label="prefixes"), Vars(answer_so_far=bits(best, width)))
    W.step(f"Best XOR: {best}.", Vars(answer=best), result=best)
    assert best == exp
    return W.save()


@run
def xor_under_a_cap(pid):
    a, exp = example(pid)
    nums, qs = sorted(a["nums"]), a["queries"]
    W = Walk(pid, "Sort the numbers and the queries by cap. Insert numbers into a bit trie as the cap allows, then answer each query greedily bit by bit.")
    order = sorted(range(len(qs)), key=lambda i: qs[i][1])
    out = [-1] * len(qs)
    k = 0
    W.step("Numbers sorted.", Row(nums), Row([f"[{x},{m}]" for x, m in qs], label="queries [x, cap]"))
    for qi in order:
        x, m = qs[qi]
        while k < len(nums) and nums[k] <= m:
            k += 1
        allowed = nums[:k]
        out[qi] = max((x ^ y for y in allowed), default=-1)
        W.step(f"Query [{x}, {m}]: numbers ≤ {m} are in the trie; the best XOR with {x} is {out[qi]}.", Row(nums, st={i: "found" for i in range(k)}), result=out[qi])
    assert out == exp
    return W.save()


@run
def xor_pairs_in_range(pid):
    a, exp = example(pid)
    v, lo, hi = a["nums"], a["low"], a["high"]
    W = Walk(pid, f"Count pairs with XOR < {hi + 1}, minus pairs with XOR < {lo}. A bit trie with counts answers \"how many earlier numbers give XOR < limit\" for each new number.")
    width = max(v).bit_length()
    W.step("The numbers in binary.", Row([bits(x, width) for x in v]))

    def below(limit):
        c = 0
        for j in range(len(v)):
            c += sum(1 for i in range(j) if v[i] ^ v[j] < limit)
        return c

    for j in range(1, len(v)):
        good = [i for i in range(j) if lo <= v[i] ^ v[j] <= hi]
        W.step(f"{v[j]} XOR each earlier number: {[v[i] ^ v[j] for i in range(j)]}; {len(good)} in range.", Row(v, st={**{i: "answer" for i in good}, j: "active"}))
    res = below(hi + 1) - below(lo)
    W.step(f"{below(hi + 1)} − {below(lo)} = {res} nice pairs.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
