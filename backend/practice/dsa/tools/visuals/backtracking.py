import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from collections import Counter
from lib import *

DONE = []
CUSTOM = {
    "feud-free-guest-lists": [{"ages": [2, 4, 6, 3], "k": 2}],
    "kth-ticket-arrangement": [{"n": 4, "k": 15}],
}
run = make_runner(DONE, CUSTOM)


class BT:
    """A search tree that grows as the backtracking runs."""

    def __init__(self, root="•"):
        self.nodes = [{"id": 0, "label": root, "parent": None}]
        self.state = {}

    def add(self, parent, label):
        self.nodes.append({"id": len(self.nodes), "label": str(label), "parent": parent})
        return len(self.nodes) - 1

    def panel(self, path=(), label="search tree"):
        st = dict(self.state)
        for p in path:
            if st.get(p) != "answer":
                st[p] = "active"
        return NT([dict(n) for n in self.nodes], st, label=label)


def same_sets(a, b):
    return sorted(map(lambda x: tuple(x) if isinstance(x, list) else x, a)) == sorted(map(lambda x: tuple(x) if isinstance(x, list) else x, b))


# ======================================================================== combinations

@run
def committee_picks(pid):
    a, exp = example(pid)
    n, k = a["n"], a["k"]
    t = BT()
    W = Walk(pid, f"Pick members in increasing order: each branch adds one member bigger than the last. A branch stops when it has {k}.")
    out = []

    def go(start, chosen, node, path):
        if len(chosen) == k:
            out.append(chosen[:])
            t.state[node] = "answer"
            W.step(f"Committee {chosen}.", t.panel(path), Row([str(c) for c in out], label="found"))
            return
        for m in range(start, n + 1):
            if n - m + 1 < k - len(chosen):
                break
            child = t.add(node, m)
            go(m + 1, chosen + [m], child, path + [child])

    go(1, [], 0, [0])
    assert same_sets(out, exp)
    return W.save()


@run
def postage_stamp_mixes(pid):
    a, exp = example(pid)
    stamps, target = sorted(a["stamps"]), a["target"]
    t = BT()
    W = Walk(pid, f"Add stamps in non-decreasing order (so each mix is found once). A branch stops at exactly {target}, or as soon as it would go over.")
    out = []

    def go(start, chosen, total, node, path):
        if total == target:
            out.append(chosen[:])
            t.state[node] = "answer"
            W.step(f"{chosen} adds up to {target}.", t.panel(path), Row([str(c) for c in out], label="found"))
            return
        for i in range(start, len(stamps)):
            s = stamps[i]
            if total + s > target:
                child = t.add(node, s)
                t.state[child] = "dim"
                W.step(f"Adding {s} would make {total + s} > {target}: prune (bigger stamps would overshoot too).", t.panel(path + [child]))
                break
            child = t.add(node, s)
            go(i, chosen + [s], total + s, child, path + [child])

    go(0, [], 0, 0, [0])
    assert same_sets(out, exp)
    return W.save()


@run
def gift_card_bundles(pid):
    a, exp = example(pid)
    cards, target = sorted(a["cards"]), a["target"]
    t = BT()
    W = Walk(pid, f"Sort the cards. At each level, skip a value equal to the one just tried at the same level, so equal bundles aren't built twice.")
    out = []

    def go(start, chosen, total, node, path):
        if total == target:
            out.append(chosen[:])
            t.state[node] = "answer"
            W.step(f"{chosen} adds up to {target}.", t.panel(path), Row([str(c) for c in out], label="found"))
            return
        for i in range(start, len(cards)):
            if i > start and cards[i] == cards[i - 1]:
                continue
            if total + cards[i] > target:
                break
            child = t.add(node, cards[i])
            go(i + 1, chosen + [cards[i]], total + cards[i], child, path + [child])

    go(0, [], 0, 0, [0])
    assert same_sets(out, exp)
    return W.save()


@run
def numbered_tile_sums(pid):
    a, exp = example(pid)
    m, k, target = a["m"], a["k"], a["target"]
    t = BT()
    W = Walk(pid, f"Draw tiles in increasing order. Stop a branch when it has {k} tiles, or when the next tile already overshoots {target}.")
    out = []

    def go(start, chosen, total, node, path):
        if len(chosen) == k:
            if total == target:
                out.append(chosen[:])
                t.state[node] = "answer"
                W.step(f"{chosen} adds up to {target}.", t.panel(path), Row([str(c) for c in out], label="found"))
            else:
                t.state[node] = "dim"
            return
        for x in range(start, m + 1):
            if total + x > target:
                break
            child = t.add(node, x)
            go(x + 1, chosen + [x], total + x, child, path + [child])

    go(1, [], 0, 0, [0])
    assert same_sets(out, exp)
    return W.save()


@run
def keypad_letter_spellings(pid):
    a, exp = example(pid)
    digits = a["digits"]
    keys = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    t = BT()
    W = Walk(pid, "Each pressed key branches into its letters. Every path from the top to the bottom spells one string.")
    out = []

    def go(i, word, node, path):
        if i == len(digits):
            out.append(word)
            t.state[node] = "answer"
            W.step(f"\"{word}\".", t.panel(path), Row(out, label="spellings"))
            return
        for ch in keys[digits[i]]:
            child = t.add(node, ch)
            go(i + 1, word + ch, child, path + [child])

    if digits:
        go(0, "", 0, [0])
    else:
        W.step("No keys pressed: nothing to spell.", Row([]), result=[])
    assert same_sets(out, exp)
    return W.save()


# ======================================================================== subsets

@run
def pizza_topping_combos(pid):
    a, exp = example(pid)
    v = sorted(a["toppings"])
    t = BT("{}")
    W = Walk(pid, "Every node of the tree is a topping set: from each set, add one topping bigger than the last one added.")
    out = [[]]
    t.state[0] = "answer"
    W.step("Start with the empty set (plain cheese).", t.panel([0]), Row(["[]"], label="sets"))

    def go(start, chosen, node, path):
        for i in range(start, len(v)):
            child = t.add(node, v[i])
            out.append(chosen + [v[i]])
            t.state[child] = "answer"
            W.step(f"Set {chosen + [v[i]]}.", t.panel(path + [child]), Row([str(s) for s in out], label="sets"))
            go(i + 1, chosen + [v[i]], child, path + [child])

    go(0, [], 0, [0])
    assert same_sets(out, exp)
    return W.save()


@run
def distinct_coin_handfuls(pid):
    a, exp = example(pid)
    v = sorted(a["coins"])
    t = BT("{}")
    W = Walk(pid, "Sort the coins. From each handful, add one more coin, but at each level skip a value equal to the one just tried, so equal handfuls appear once.")
    out = [[]]
    t.state[0] = "answer"
    W.step("Start with the empty handful.", t.panel([0]), Row(["[]"], label="handfuls"))

    def go(start, chosen, node, path):
        for i in range(start, len(v)):
            if i > start and v[i] == v[i - 1]:
                continue
            child = t.add(node, v[i])
            out.append(chosen + [v[i]])
            t.state[child] = "answer"
            W.step(f"Handful {chosen + [v[i]]}.", t.panel(path + [child]), Row([str(s) for s in out], label="handfuls"))
            go(i + 1, chosen + [v[i]], child, path + [child])

    go(0, [], 0, [0])
    assert same_sets(out, exp)
    return W.save()


@run
def feud_free_guest_lists(pid):
    a, exp = example(pid)
    ages, k = a["ages"], a["k"]
    t = BT()
    W = Walk(pid, f"Decide cousin by cousin: invite or skip. Inviting is only allowed if nobody already invited is exactly {k} years older or younger.")
    count = [0]

    def go(i, invited, node, path):
        if i == len(ages):
            if invited:
                count[0] += 1
                t.state[node] = "answer"
                W.step(f"Guest list of ages {invited}. Lists so far: {count[0]}.", t.panel(path), Vars(lists=count[0]))
            return
        x = ages[i]
        bad = any(abs(x - y) == k for y in invited)
        inv = t.add(node, f"+{x}")
        if bad:
            t.state[inv] = "dim"
            W.step(f"Can't invite the cousin aged {x}: someone invited differs by exactly {k}.", t.panel(path + [inv]))
        else:
            go(i + 1, invited + [x], inv, path + [inv])
        skip = t.add(node, f"−{x}")
        go(i + 1, invited, skip, path + [skip])

    go(0, [], 0, [0])
    assert count[0] == exp
    return W.save()


@run
def best_scoring_word_set(pid):
    a, exp = example(pid)
    words, tiles, pts = a["words"], a["tiles"], a["points"]
    score = lambda w: sum(pts[ord(c) - 97] for c in w)
    t = BT()
    W = Walk(pid, "Decide word by word: spell it (if the tiles left allow) or skip it. Track the score and keep the best.")
    best = [0]

    def go(i, left, total, node, path):
        if i == len(words):
            if total > best[0]:
                best[0] = total
                t.state[node] = "answer"
                W.step(f"All words decided: score {total}, the best so far.", t.panel(path), Vars(best=best[0]))
            else:
                t.state[node] = "dim"
            return
        w = words[i]
        need = Counter(w)
        use = t.add(node, f"+{w}")
        if all(left[c] >= n for c, n in need.items()):
            go(i + 1, left - need, total + score(w), use, path + [use])
        else:
            t.state[use] = "dim"
            W.step(f"Not enough tiles left to spell \"{w}\".", t.panel(path + [use]), Vars(best=best[0]))
        skip = t.add(node, f"−{w}")
        go(i + 1, left, total, skip, path + [skip])

    go(0, Counter(tiles), 0, 0, [0])
    assert best[0] == exp
    return W.save()


# ======================================================================== permutations

@run
def parade_line_ups(pid):
    a, exp = example(pid)
    v = a["floats"]
    t = BT()
    W = Walk(pid, "Fill the order one place at a time with any float not used yet. A full path is one running order.")
    out = []

    def go(order, node, path):
        if len(order) == len(v):
            out.append(order[:])
            t.state[node] = "answer"
            W.step(f"Order {order}.", t.panel(path), Vars(orders=len(out)))
            return
        for x in v:
            if x not in order:
                child = t.add(node, x)
                go(order + [x], child, path + [child])

    go([], 0, [0])
    assert same_sets(out, exp)
    return W.save()


@run
def distinct_bead_orders(pid):
    a, exp = example(pid)
    v = sorted(a["beads"])
    t = BT()
    W = Walk(pid, "Sort the beads. At each place, try each COLOUR once: skip a bead whose colour equals the previous unused bead's, so repeats never branch twice.")
    out, used = [], [False] * len(v)

    def go(order, node, path):
        if len(order) == len(v):
            out.append(order[:])
            t.state[node] = "answer"
            W.step(f"Sequence {order}.", t.panel(path), Row([str(o) for o in out], label="found"))
            return
        for i in range(len(v)):
            if used[i] or (i and v[i] == v[i - 1] and not used[i - 1]):
                continue
            used[i] = True
            child = t.add(node, v[i])
            go(order + [v[i]], child, path + [child])
            used[i] = False

    go([], 0, [0])
    assert same_sets(out, exp)
    return W.save()


@run
def square_sum_line_ups(pid):
    a, exp = example(pid)
    v = sorted(a["nums"])
    is_sq = lambda x: int(x ** 0.5) ** 2 == x
    t = BT()
    W = Walk(pid, "Build line-ups card by card. A card may follow the last one only if their sum is a perfect square; repeats of the same value branch once.")
    count, used = [0], [False] * len(v)

    def go(order, node, path):
        if len(order) == len(v):
            count[0] += 1
            t.state[node] = "answer"
            W.step(f"Line-up {order} works. Count {count[0]}.", t.panel(path), Vars(count=count[0]))
            return
        for i in range(len(v)):
            if used[i] or (i and v[i] == v[i - 1] and not used[i - 1]):
                continue
            if order and not is_sq(order[-1] + v[i]):
                child = t.add(node, v[i])
                t.state[child] = "dim"
                W.step(f"{order[-1]} + {v[i]} = {order[-1] + v[i]} isn't a square: prune.", t.panel(path + [child]))
                continue
            used[i] = True
            child = t.add(node, v[i])
            go(order + [v[i]], child, path + [child])
            used[i] = False

    go([], 0, [0])
    assert count[0] == exp
    return W.save()


@run
def kth_ticket_arrangement(pid):
    a, exp = example(pid)
    n, k = a["n"], a["k"]
    W = Walk(pid, "No need to list orders. With m tickets left, each choice for the next place covers (m − 1)! orders, so k says which block to pick.")
    import math
    left, out, kk = list(range(1, n + 1)), [], k - 1
    while left:
        block = math.factorial(len(left) - 1)
        i = kk // block
        W.step(f"{len(left)} tickets left; each choice covers {block} orders. Position {kk} (0-based) falls in block {i}: take {left[i]}.", Row(left, st={i: "answer"}, label="tickets left"), Row(out + [left[i]], label="order so far"), Vars(remaining_k=kk, block=block))
        out.append(left.pop(i))
        kk %= block
    assert out == exp
    return W.save()


# ======================================================================== constraint-placement

def board(n, queens, holes=(), extra=None):
    cells = [["" for _ in range(n)] for _ in range(n)]
    st = {}
    for r, c in holes:
        cells[r][c] = "×"
        st[(r, c)] = "dim"
    for r, c in queens:
        cells[r][c] = "Q"
        st[(r, c)] = "answer"
    st.update(extra or {})
    return Grid(cells, st)


def queens(W, n, holes, fixed=()):
    holes = {tuple(h) for h in holes}
    fixed_rows = {r: c for r, c in fixed}
    sols = []

    def ok(r, c, placed):
        return all(c != pc and abs(r - pr) != abs(c - pc) for pr, pc in placed)

    def go(r, placed):
        if r == n:
            sols.append(list(placed))
            W.step(f"All {n} queens placed. Layouts so far: {len(sols)}.", board(n, placed, holes))
            return
        cols = [fixed_rows[r]] if r in fixed_rows else range(n)
        for c in cols:
            if (r, c) in holes or not ok(r, c, placed):
                continue
            W.step(f"Row {r}: put a queen in column {c}.", board(n, placed + [(r, c)], holes, {(r, c): "active"}))
            go(r + 1, placed + [(r, c)])
        if not any((r, c) not in holes and ok(r, c, placed) for c in cols):
            W.step(f"Row {r}: every square is attacked or missing. Back up.", board(n, placed, holes, {(r, c): "mark" for c in range(n)}))

    go(0, [])
    return sols


@run
def queens_on_a_damaged_board(pid):
    a, exp = example(pid)
    n, holes = a["n"], a["holes"]
    W = Walk(pid, "Place one queen per row. Try each column that isn't missing and isn't attacked; when a row has no option, back up to the row before.")
    sols = queens(W, n, holes)
    assert len(sols) == exp
    return W.save()


@run
def queen_layout_sketches(pid):
    a, exp = example(pid)
    n, fixed = a["n"], a["fixed"]
    W = Walk(pid, "Place one queen per row; rows with a glued queen only get that column. Every complete placement is a sketch.")
    sols = queens(W, n, [], fixed)
    out = [["".join("Q" if (r, c) in set(s) else "." for c in range(n)) for r in range(n)] for s in sols]
    assert sorted(out) == sorted(exp)
    return W.save()


@run
def colour_the_district_map(pid):
    a, exp = example(pid)
    n, borders, m = a["n"], a["borders"], a["m"]
    adj = {i: set() for i in range(n)}
    for x, y in borders:
        adj[x].add(y)
        adj[y].add(x)
    W = Walk(pid, f"Colour districts in order with colours 0–{m - 1}. A colour is allowed if no bordering district already has it; if none is, undo the last choice.")
    col = [None] * n

    def go(i):
        if i == n:
            W.step("Every district is coloured.", Row(col, st={k: "answer" for k in range(n)}, label="colour of each district"), result=True)
            return True
        for c in range(m):
            if all(col[j] != c for j in adj[i]):
                col[i] = c
                W.step(f"District {i} borders {sorted(adj[i])}: colour {c} is free.", Row(col, st={i: "new"}, label="colour of each district"))
                if go(i + 1):
                    return True
                col[i] = None
                W.step(f"Undo district {i}'s colour {c}.", Row(col, st={i: "mark"}, label="colour of each district"))
        return False

    ok = go(0)
    if not ok:
        W.step(f"No way to colour with {m} colours.", Row(col), result=False)
    assert ok == exp
    return W.save()


@run
def nine_by_nine_fill(pid):
    a, exp = example(pid)
    g = [row[:] for row in a["board"]]
    W = Walk(pid, "Fill the empty cells one by one with a digit that isn't already in its row, column or box. When a cell has no digit left, undo the previous choice.")
    empty = [(r, c) for r in range(9) for c in range(9) if g[r][c] == "."]

    def ok(r, c, d):
        if any(g[r][x] == d for x in range(9)) or any(g[x][c] == d for x in range(9)):
            return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        return all(g[br + i][bc + j] != d for i in range(3) for j in range(3))

    def go(i):
        if i == len(empty):
            return True
        r, c = empty[i]
        for d in "123456789":
            if ok(r, c, d):
                g[r][c] = d
                W.step(f"Cell ({r}, {c}): {d} fits.", Grid(g, {**{e: "found" for e in empty[:i]}, (r, c): "new"}))
                if go(i + 1):
                    return True
                g[r][c] = "."
                W.step(f"Cell ({r}, {c}): {d} leads to a dead end. Undo it.", Grid(g, {(r, c): "mark"}))
        return False

    go(0)
    W.step("Solved.", Grid(g, {e: "found" for e in empty}))
    assert g == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
