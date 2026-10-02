import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from collections import Counter
from lib import *

DONE = []
CUSTOM = {
    "feud-free-guest-lists": [{"ages": [2, 4, 6, 3], "k": 2}],
    "kth-ticket-arrangement": [{"n": 4, "k": 15}],
    "trace-the-word": [{"board": [["a", "b", "a"], ["b", "a", "c"], ["a", "c", "d"]], "word": "abacd"}],
    "flip-row-symbol": [{"n": 4, "k": 6}],
    "most-distinct-pieces": [{"s": "abab"}],
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


# ======================================================================== grid-word-search

NB4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


def path_grid(board, path, extra=None, label=None):
    st = {p: "active" for p in path}
    if path:
        st[path[-1]] = "new"
    st.update(extra or {})
    return Grid(board, st, label=label)


@run
def trace_the_word(pid):
    a, exp = example(pid)
    b, word = a["board"], a["word"]
    m, n = len(b), len(b[0])
    W = Walk(pid, f"Start at each cell holding '{word[0]}'. Step to a neighbour holding the next letter; on a dead end, unmark the cell and try another direction.")
    path = []
    found = [False]

    def go(r, c, i):
        if b[r][c] != word[i]:
            return False
        path.append((r, c))
        W.step(f"'{word[i]}' at ({r}, {c}): matched {i + 1} of {len(word)} letters.", path_grid(b, path), Vars(matched=word[:i + 1]))
        if i == len(word) - 1:
            return True
        for dr, dc in NB4:
            rr, cc = r + dr, c + dc
            if 0 <= rr < m and 0 <= cc < n and (rr, cc) not in path and go(rr, cc, i + 1):
                return True
        path.pop()
        W.step(f"No neighbour of ({r}, {c}) continues the word: unmark it and back up.", path_grid(b, path, {(r, c): "dim"}))
        return False

    for r in range(m):
        for c in range(n):
            if go(r, c, 0):
                found[0] = True
                break
        if found[0]:
            break
    W.step(f"'{word}' is traced." if found[0] else f"No starting cell works: '{word}' isn't on the board.", path_grid(b, path, {p: "answer" for p in path}) if found[0] else Grid(b), result=found[0])
    assert found[0] == exp
    return W.save()


@run
def gold_mine_walk(pid):
    a, exp = example(pid)
    g = [r[:] for r in a["mine"]]
    m, n = len(g), len(g[0])
    W = Walk(pid, "From each cell with gold, walk every route: take the gold, try each neighbour that still has gold, then put the gold back on the way out.")
    best = [0]
    path = []

    def go(r, c, total):
        path.append((r, c))
        ends = True
        for dr, dc in NB4:
            rr, cc = r + dr, c + dc
            if 0 <= rr < m and 0 <= cc < n and g[rr][cc] and (rr, cc) not in path:
                ends = False
                go(rr, cc, total + g[rr][cc])
        if ends:
            better = total > best[0]
            best[0] = max(best[0], total)
            W.step(f"Route {' → '.join(str(g[p][q]) for p, q in path)} collects {total}." + (" New best." if better else ""), path_grid(g, path, {path[-1]: "answer" if better else "new"}), Vars(route=total, best=best[0]))
        path.pop()

    for r in range(m):
        for c in range(n):
            if g[r][c]:
                go(r, c, g[r][c])
    W.step(f"The best route collects {best[0]}.", Vars(best=best[0]), result=best[0])
    assert best[0] == exp
    return W.save()


def floor_cells(f, order):
    sym = {-1: "■", 1: "S", 2: "E", 0: ""}
    return [[str(order[(r, c)]) if (r, c) in order and f[r][c] == 0 else sym[f[r][c]] for c in range(len(f[0]))] for r in range(len(f))]


@run
def visit_every_square(pid):
    a, exp = example(pid)
    f = a["floor"]
    m, n = len(f), len(f[0])
    need = sum(1 for r in f for v in r if v != -1)
    start = next((r, c) for r in range(m) for c in range(n) if f[r][c] == 1)
    W = Walk(pid, f"Walk from S, numbering squares as you step on them. Reaching E counts only if all {need} open squares are numbered.")
    order = {}
    count = [0]

    def go(r, c):
        order[(r, c)] = len(order) + 1
        if f[r][c] == 2:
            ok = len(order) == need
            count[0] += ok
            W.step(f"Reached E after {len(order)} of {need} squares: " + ("a full tour." if ok else "squares were skipped, so it doesn't count."), Grid(floor_cells(f, order), {p: ("answer" if ok else "mark") if p == (r, c) else "active" for p in order}), Vars(tours=count[0]))
        else:
            for dr, dc in NB4:
                rr, cc = r + dr, c + dc
                if 0 <= rr < m and 0 <= cc < n and f[rr][cc] != -1 and (rr, cc) not in order:
                    go(rr, cc)
        del order[(r, c)]

    go(*start)
    W.step(f"{count[0]} full tours.", Vars(tours=count[0]), result=count[0])
    assert count[0] == exp
    return W.save()


@run
def maze_escape_routes(pid):
    a, exp = example(pid)
    mz = a["maze"]
    m, n = len(mz), len(mz[0])
    W = Walk(pid, "Walk from the top-left, marking each cell on the route. Every arrival at the bottom-right is one route; unmark cells on the way back so other routes can use them.")
    order = {}
    count = [0]
    cells = lambda: [["■" if mz[r][c] else (str(order[(r, c)]) if (r, c) in order else "") for c in range(n)] for r in range(m)]

    def go(r, c):
        order[(r, c)] = len(order) + 1
        if (r, c) == (m - 1, n - 1):
            count[0] += 1
            W.step(f"Route {count[0]} reaches the exit in {len(order) - 1} steps.", Grid(cells(), {p: "answer" if p == (r, c) else "active" for p in order}), Vars(routes=count[0]))
        else:
            for dr, dc in NB4:
                rr, cc = r + dr, c + dc
                if 0 <= rr < m and 0 <= cc < n and not mz[rr][cc] and (rr, cc) not in order:
                    go(rr, cc)
        del order[(r, c)]

    go(0, 0)
    W.step(f"{count[0]} routes in total.", Vars(routes=count[0]), result=count[0])
    assert count[0] == exp
    return W.save()


# ======================================================================== string-partitioning

@run
def mirror_cuts(pid):
    a, exp = example(pid)
    s = a["s"]
    t = BT()
    W = Walk(pid, "Choose the first piece: it must read the same both ways. Then cut the rest the same way. A branch that reaches the end of the string is one answer.")
    out = []

    def go(i, cur, node, path):
        if i == len(s):
            out.append(cur[:])
            t.state[node] = "answer"
            W.step(f"Reached the end: {' | '.join(cur)}.", t.panel(path), Row([" | ".join(c) for c in out], label="found"))
            return
        for j in range(i + 1, len(s) + 1):
            p = s[i:j]
            if p == p[::-1]:
                child = t.add(node, p)
                W.step(f"\"{p}\" is a palindrome: cut it off, then split \"{s[j:]}\"." if j < len(s) else f"\"{p}\" is a palindrome and finishes the string.", t.panel(path + [child]))
                go(j, cur + [p], child, path + [child])
            else:
                child = t.add(node, p)
                t.state[child] = "dim"
                W.step(f"\"{p}\" isn't a palindrome: skip this cut.", t.panel(path))

    go(0, [], 0, [0])
    assert sorted(out) == exp
    return W.save()


@run
def rebuild_the_address(pid):
    a, exp = example(pid)
    d = a["digits"]
    t = BT()
    W = Walk(pid, "Pick each part's length (1 to 3 digits). A part can't be over 255 or start with 0, and a branch dies when the digits left can't fill the remaining parts.")
    out = []

    def go(i, parts, node, path):
        if len(parts) == 4:
            if i == len(d):
                out.append(".".join(parts))
                t.state[node] = "answer"
                W.step(f"{'.'.join(parts)} uses every digit.", t.panel(path), Row(out, label="found"))
            return
        left = 4 - len(parts)
        if not left <= len(d) - i <= 3 * left:
            t.state[node] = "dim"
            W.step(f"{len(d) - i} digits left can't make {left} more part{'s' if left > 1 else ''}: prune.", t.panel(path))
            return
        for k in range(1, 4):
            p = d[i:i + k]
            if len(p) < k or (len(p) > 1 and p[0] == "0") or int(p) > 255:
                break
            child = t.add(node, p)
            go(i + k, parts + [p], child, path + [child])

    go(0, [], 0, [0])
    assert sorted(out) == exp
    return W.save()


@run
def every_sentence(pid):
    a, exp = example(pid)
    text, ws = a["text"], set(a["words"])
    W = Walk(pid, "sentences(i) = every word that starts at i, followed by every sentence of what's left. Remember each answer, because different first words can leave the same tail.")
    memo = {}
    cells = list(text)

    def go(i):
        if i == len(text):
            return [[]]
        if i in memo:
            W.step(f"\"{text[i:]}\" was solved already: reuse {len(memo[i])} sentence{'s' if len(memo[i]) != 1 else ''}.", Row(cells, st={k: "found" for k in range(i, len(text))}, ptr={"i": i}), Vars(memo=len(memo)))
            return memo[i]
        out = []
        for j in range(i + 1, len(text) + 1):
            w = text[i:j]
            if w in ws:
                W.step(f"\"{w}\" is a word: split the rest, \"{text[j:]}\"." if j < len(text) else f"\"{w}\" is a word and ends the text.", Row(cells, st={**{k: "active" for k in range(i, j)}}, ptr={"i": i}))
                out += [[w] + r for r in go(j)]
        memo[i] = out
        if i:
            W.step(f"\"{text[i:]}\" can be said {len(out)} way{'s' if len(out) != 1 else ''}" + (": " + "; ".join(" ".join(x) for x in out[:3]) if out else "") + ".", Row(cells, st={k: "found" if out else "dim" for k in range(i, len(text))}, ptr={"i": i}), Vars(memo=len(memo)))
        return out

    res = sorted(" ".join(s) for s in go(0))
    W.step(f"{len(res)} sentence{'s' if len(res) != 1 else ''}.", Row(res or ["none"], label="sentences"), result=res)
    assert res == exp
    return W.save()


@run
def most_distinct_pieces(pid):
    a, exp = example(pid)
    s = a["s"]
    n = len(s)
    W = Walk(pid, "Try every length for the next piece, skipping pieces already used. Undo each choice on the way back. Prune when even all single letters couldn't beat the best.")
    best = [0]
    used = []

    def go(i):
        if len(used) + (n - i) <= best[0]:
            W.step(f"{len(used)} pieces + {n - i} letters left can't beat {best[0]}: prune.", Row(used + [s[i:]] if i < n else used, st={len(used): "dim"} if i < n else {}, label="pieces"), Vars(best=best[0]))
            return
        if i == n:
            best[0] = len(used)
            W.step(f"All cut: {len(used)} different pieces. New best.", Row(used[:], st={k: "found" for k in range(len(used))}, label="pieces"), Vars(best=best[0]))
            return
        for j in range(i + 1, n + 1):
            p = s[i:j]
            if p not in used:
                used.append(p)
                W.step(f"Take \"{p}\".", Row(used + ([s[j:]] if j < n else []), st={len(used) - 1: "new", **({len(used): "dim"} if j < n else {})}, label="pieces"), Vars(best=best[0]))
                go(j)
                used.pop()

    go(0)
    W.step(f"At most {best[0]} pieces.", Vars(best=best[0]), result=best[0])
    assert best[0] == exp
    return W.save()


# ======================================================================== recursion-basics

@run
def quick_power(pid):
    a, exp = example(pid)
    base, e0, mod = a["base"], a["exp"], a["mod"]
    b = base % mod
    W = Walk(pid, f"power(e) squares power(e / 2), and multiplies by the base once more when e is odd. Exponent {e0} needs only about log₂ {e0} calls.")
    chain = []
    e = e0
    while e:
        chain.append(e)
        e //= 2
    chain.append(0)
    for i, e in enumerate(chain[:-1]):
        W.step(f"power({e}) needs power({e // 2}) first.", Row(chain, st={i: "active"}, label="exponents"))
    h = 1 % mod
    W.step(f"power(0) = 1.", Row(chain, st={len(chain) - 1: "found"}, label="exponents"), Vars(value=h))
    for i in range(len(chain) - 2, -1, -1):
        e = chain[i]
        sq = h * h % mod
        h = sq * b % mod if e % 2 else sq
        W.step(f"power({e}) = power({e // 2})² " + (f"× {b} " if e % 2 else "") + f"mod {mod} = {h}.", Row(chain, st={**{k: "found" for k in range(i + 1, len(chain))}, i: "new"}, label="exponents"), Vars(value=h), result=h if i == 0 else None)
    assert h == exp
    return W.save()


@run
def stacking_rings(pid):
    a, exp = example(pid)
    n = a["n"]
    pegs = {1: list(range(n, 0, -1)), 2: [], 3: []}
    W = Walk(pid, f"To move {n} rings to peg 3: move the top {n - 1} to the spare peg, move the biggest ring, then move the {n - 1} back on top.")
    show = lambda hl=None: [Row(pegs[p] or [""], st={len(pegs[p]) - 1: "new"} if hl == p and pegs[p] else None, label=f"peg {p}") for p in (1, 2, 3)]
    W.step("Start: every ring on peg 1, biggest at the bottom.", *show())
    out = []

    def move(k, x, y, z):
        if k == 0:
            return
        move(k - 1, x, z, y)
        pegs[y].append(pegs[x].pop())
        out.append([x, y])
        W.step(f"Move ring {k} from peg {x} to peg {y}.", *show(y), Vars(moves=len(out)))
        move(k - 1, z, y, x)

    move(n, 1, 3, 2)
    W.step(f"Done in {len(out)} = 2^{n} − 1 moves.", *show(), result=len(out))
    assert out == exp
    return W.save()


@run
def flip_row_symbol(pid):
    a, exp = example(pid)
    n, k = a["n"], a["k"]
    rows = ["0"]
    for _ in range(n - 1):
        rows.append("".join("01" if c == "0" else "10" for c in rows[-1]))
    W = Walk(pid, "Symbol k of row n is born from symbol ⌈k/2⌉ of row n − 1: an odd k copies it, an even k flips it.")
    W.step("The rows double each time: 0 → 01, 1 → 10.", *[Row(list(r), label=f"row {i + 1}") for i, r in enumerate(rows)])
    trail = []
    r, kk = n, k
    while r > 1:
        trail.append((r, kk))
        W.step(f"Row {r}, position {kk} comes from row {r - 1}, position {(kk + 1) // 2}" + (" (same symbol)." if kk % 2 else " (flipped)."), *[Row(list(rows[i]), st={kk - 1: "active"} if i + 1 == r else ({(kk + 1) // 2 - 1: "mark"} if i + 2 == r else None), label=f"row {i + 1}") for i in range(n)])
        r, kk = r - 1, (kk + 1) // 2
    v = 0
    W.step("Row 1 is 0.", Row(["0"], st={0: "found"}, label="row 1"), Vars(symbol=0))
    for r, kk in reversed(trail):
        v = v if kk % 2 else 1 - v
        W.step(f"Row {r}, position {kk}: " + ("copy" if kk % 2 else "flip") + f" → {v}.", Row(list(rows[r - 1]), st={kk - 1: "found"}, label=f"row {r}"), Vars(symbol=v), result=v if r == n else None)
    assert v == exp
    return W.save()


@run
def last_seat_standing(pid):
    a, exp = example(pid)
    n, k = a["n"], a["k"]
    W = Walk(pid, f"Count {k} people around the circle; that person leaves and the count restarts after them. The recurrence J(n) = (J(n − 1) + k) mod n gives the same answer without simulating.")
    seats, at, gone = list(range(1, n + 1)), 0, []
    while len(seats) > 1:
        at = (at + k - 1) % len(seats)
        who = seats.pop(at)
        gone.append(who)
        W.step(f"Count {k}: seat {who} leaves.", Row(list(range(1, n + 1)), st={**{g - 1: "dim" for g in gone}, who - 1: "mark"}, label="seats"))
    j = 0
    for size in range(2, n + 1):
        j = (j + k) % size
    W.step(f"Seat {seats[0]} is the last one left. The recurrence agrees: J({n}) + 1 = {j + 1}.", Row(list(range(1, n + 1)), st={**{g - 1: "dim" for g in gone}, seats[0] - 1: "answer"}, label="seats"), result=seats[0])
    assert seats[0] == exp
    return W.save()


# ======================================================================== generate-valid

@run
def bracket_builder(pid):
    a, exp = example(pid)
    n = a["n"]
    t = BT()
    W = Walk(pid, f"Add '(' while fewer than {n} are open; add ')' only while it has something to close. Every branch that reaches length {2 * n} is balanced.")
    out = []

    def go(s, op, cl, node, path):
        if len(s) == 2 * n:
            out.append(s)
            t.state[node] = "answer"
            W.step(f"{s} is complete.", t.panel(path), Row(out, label="found"))
            return
        if op < n:
            c = t.add(node, "(")
            go(s + "(", op + 1, cl, c, path + [c])
        if cl < op:
            c = t.add(node, ")")
            go(s + ")", op, cl + 1, c, path + [c])

    go("", 0, 0, 0, [0])
    assert out == exp
    return W.save()


@run
def no_touching_ones(pid):
    a, exp = example(pid)
    n, ones = a["n"], a["ones"]
    t = BT()
    W = Walk(pid, f"Fill {n} positions left to right. A 1 can't follow a 1, and a branch stops once the 1s still needed can't fit.")
    out = []

    def go(s, left, node, path):
        room = n - len(s)
        if left == 0:
            res = s + "0" * room
            out.append(res)
            t.state[node] = "answer"
            W.step(f"All {ones} ones placed: fill with 0s → {res}.", t.panel(path), Row(out, label="found"))
            return
        if room < 2 * left - 1 + (1 if s.endswith("1") else 0):
            t.state[node] = "dim"
            W.step(f"{s or 'empty'}: {left} more 1{'s' if left > 1 else ''} can't fit in {room} spot{'s' if room != 1 else ''}. Prune.", t.panel(path))
            return
        c = t.add(node, "0")
        go(s + "0", left, c, path + [c])
        if not s.endswith("1"):
            c = t.add(node, "1")
            go(s + "1", left - 1, c, path + [c])

    go("", ones, 0, [0])
    assert out == exp
    return W.save()


@run
def kth_calm_word(pid):
    a, exp = example(pid)
    n, k = a["n"], a["k"]
    total = 3 << (n - 1)
    W = Walk(pid, f"Each first letter leads to 2^{n - 1} calm words, and after that every letter has 2 choices. Skip whole blocks to land on word {k}.")
    if k > total:
        W.step(f"There are only {total} calm words.", Vars(total=total), result="")
        assert exp == ""
        return W.save()
    kk, out = k - 1, []
    for i in range(n):
        block = 1 << (n - 1 - i)
        opts = [c for c in "abc" if not out or c != out[-1]]
        pick = kk // block
        W.step(f"Position {i + 1}: choices {', '.join(opts)}, {block} word{'s' if block > 1 else ''} each. Word {kk + 1} of these falls in the block for '{opts[pick]}'.", Row([f"{c}: {block}" for c in opts], st={pick: "active"}, label="blocks"), Row(out + ["?"] * (n - i), st={i: "new"}, label="word"))
        out.append(opts[pick])
        kk %= block
    res = "".join(out)
    W.step(f"Word {k} is {res}.", Row(list(res), st={i: "found" for i in range(n)}, label="word"), result=res)
    assert res == exp
    return W.save()


# ======================================================================== bucket-assignment

@run
def equal_teams(pid):
    a, exp = example(pid)
    xs, k = sorted(a["scores"], reverse=True), a["k"]
    total = sum(xs)
    W = Walk(pid, "Each team must reach total / k. Place the biggest players first into a team with room; teams with the same load are interchangeable, so try only one.")
    if total % k:
        W.step(f"The total {total} doesn't divide by {k}: impossible.", Row(xs, label="scores"), result=False)
        assert exp is False
        return W.save()
    target = total // k
    load = [0] * k
    teams = [[] for _ in range(k)]
    W.step(f"Total {total}, so each team needs {target}. Sort biggest first.", Row(xs, label="scores"))
    show = lambda hl=None: [Row(tm or [""], st={len(tm) - 1: "new"} if hl == t and tm else None, label=f"team {t + 1} ({load[t]}/{target})") for t, tm in enumerate(teams)]

    def go(i):
        if i == len(xs):
            return True
        tried = set()
        for t in range(k):
            if load[t] + xs[i] <= target and load[t] not in tried:
                tried.add(load[t])
                load[t] += xs[i]
                teams[t].append(xs[i])
                W.step(f"Put {xs[i]} in team {t + 1}.", *show(t))
                if go(i + 1):
                    return True
                load[t] -= xs[i]
                teams[t].pop()
                W.step(f"That led nowhere: take {xs[i]} back out of team {t + 1}.", *show())
        return False

    ok = xs[0] <= target and go(0)
    W.step("Every team reaches the target." if ok else "No arrangement works.", *show(), result=ok)
    assert ok == exp
    return W.save()


@run
def fair_snack_bags(pid):
    a, exp = example(pid)
    xs, kids = sorted(a["bags"], reverse=True), a["kids"]
    load = [0] * kids
    best = [float("inf")]
    bs = lambda: "∞" if best[0] == float("inf") else best[0]
    W = Walk(pid, "Hand out bags biggest first, trying each kid. Any branch where a kid already has as much as the best answer so far can stop.")
    W.step("Sort the bags biggest first.", Row(xs, label="bags"))

    def go(i):
        if i == len(xs):
            best[0] = max(load)
            W.step(f"Every bag handed out. The most any kid has is {best[0]}: new best.", Row(load, st={load.index(best[0]): "answer"}, label="per kid"), Vars(best=bs()))
            return
        seen = set()
        for t in range(kids):
            if load[t] in seen:
                continue
            seen.add(load[t])
            if load[t] + xs[i] >= best[0]:
                W.step(f"Giving {xs[i]} to kid {t + 1} reaches {load[t] + xs[i]} ≥ best {bs()}: prune.", Row(xs, st={i: "mark"}, label="bags"), Row(load, st={t: "dim"}, label="per kid"), Vars(best=bs()))
                continue
            load[t] += xs[i]
            W.step(f"Give {xs[i]} to kid {t + 1}.", Row(xs, st={**{q: "found" for q in range(i)}, i: "active"}, label="bags"), Row(load, st={t: "new"}, label="per kid"), Vars(best=bs()))
            go(i + 1)
            load[t] -= xs[i]

    go(0)
    W.step(f"The fairest split leaves at most {best[0]} with one kid.", Vars(best=best[0]), result=best[0])
    assert best[0] == exp
    return W.save()


@run
def fewest_van_trips(pid):
    a, exp = example(pid)
    xs, cap = sorted(a["boxes"], reverse=True), a["capacity"]
    W = Walk(pid, f"Place boxes biggest first: into a trip that still has room, or a new trip. Stop any branch that already uses as many trips as the best found.")
    best = [len(xs)]
    trips = []

    def show(hl=None):
        return [Row(tr, st={len(tr) - 1: "new"} if hl == t else None, label=f"trip {t + 1} ({sum(tr)}/{cap})") for t, tr in enumerate(trips)]

    def go(i):
        if len(trips) >= best[0]:
            return
        if i == len(xs):
            best[0] = len(trips)
            W.step(f"All boxes placed in {len(trips)} trips: new best.", *show(), Vars(best=best[0]))
            return
        seen = set()
        for t in range(len(trips)):
            room = cap - sum(trips[t])
            if room >= xs[i] and room not in seen:
                seen.add(room)
                trips[t].append(xs[i])
                W.step(f"Box {xs[i]} fits in trip {t + 1}.", *show(t), Vars(best=best[0]))
                go(i + 1)
                trips[t].pop()
        trips.append([xs[i]])
        W.step(f"Box {xs[i]} starts trip {len(trips)}.", *show(len(trips) - 1), Vars(best=best[0]))
        go(i + 1)
        trips.pop()

    go(0)
    W.step(f"{best[0]} trips.", Vars(trips=best[0]), result=best[0])
    assert best[0] == exp
    return W.save()


# ======================================================================== meet-in-the-middle

@run
def closest_subset_sum(pid):
    from bisect import bisect_left
    a, exp = example(pid)
    nums, goal = a["nums"], a["goal"]
    h = len(nums) // 2

    def sums(xs):
        out = [0]
        for x in xs:
            out += [s + x for s in out]
        return out

    A, B = sums(nums[:h]), sorted(sums(nums[h:]))
    W = Walk(pid, f"List every subset sum of each half. For each left sum a, binary-search the sorted right sums for {goal} − a and check its neighbours.")
    W.step(f"Left half {nums[:h]}, right half {nums[h:]}.", Row(A, label="left sums"), Row(B, label="right sums (sorted)"))
    best = abs(goal)
    for i, x in enumerate(A):
        j = bisect_left(B, goal - x)
        cand = [t for t in (j - 1, j) if 0 <= t < len(B)]
        for t in cand:
            best = min(best, abs(x + B[t] - goal))
        W.step(f"a = {x}: look for {goal - x}. Neighbours " + ", ".join(f"{B[t]} (total {x + B[t]})" for t in cand) + f". Closest gap {best}.", Row(A, st={i: "active"}, label="left sums"), Row(B, st={t: "found" for t in cand}, label="right sums (sorted)"), Vars(best=best))
        if best == 0:
            break
    W.step(f"Smallest gap: {best}.", Vars(best=best), result=best)
    assert best == exp
    return W.save()


@run
def even_teams_gap(pid):
    from bisect import bisect_left
    a, exp = example(pid)
    xs = a["skills"]
    n = len(xs) // 2

    def diffs(part):
        by = [[] for _ in range(len(part) + 1)]
        for mask in range(1 << len(part)):
            k = bin(mask).count("1")
            by[k].append(sum(v if mask >> i & 1 else -v for i, v in enumerate(part)))
        return by

    L, R = diffs(xs[:n]), diffs(xs[n:])
    W = Walk(pid, f"Each half sends some players to team A (+) and the rest to team B (−). If the left half sends k, the right half must send {n} − k. Pair the (A − B) differences closest to cancelling.")
    best = None
    for k in range(n + 1):
        right = sorted(R[n - k])
        W.step(f"Left sends {k} to team A, so right sends {n - k}.", Row(L[k], label=f"left, {k} in A"), Row(right, label=f"right, {n - k} in A (sorted)"))
        for d in L[k]:
            j = bisect_left(right, -d)
            for t in (j - 1, j):
                if 0 <= t < len(right):
                    v = abs(d + right[t])
                    if best is None or v < best:
                        best = v
                        W.step(f"{d} + {right[t]} → gap {v}. New best.", Row(L[k], st={L[k].index(d): "active"}, label=f"left, {k} in A"), Row(right, st={t: "found"}, label=f"right, {n - k} in A (sorted)"), Vars(best=best))
    W.step(f"The smallest gap is {best}.", Vars(best=best), result=best)
    assert best == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
