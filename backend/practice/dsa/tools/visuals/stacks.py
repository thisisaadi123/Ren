import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from collections import deque
from fractions import Fraction
from lib import *

DONE = []


def run(fn):
    pid = fn.__name__.replace("_", "-")
    DONE.append((pid, fn(pid)))
    return fn


def S(text, st=None, ptr=None, label=None):
    return Row(list(text), st=st, ptr=ptr, label=label)


def stack_row(items, label="stack (top on the right)", new=False):
    return Row(items, st={len(items) - 1: "new"} if new and items else None, label=label)


# ======================================================================== bracket-matching

@run
def sealed_brackets(pid):
    a, exp = example(pid)
    s = a["s"]
    pair = {")": "(", "]": "[", "}": "{"}
    W = Walk(pid, "Push every opener. A closer must match the opener on top of the stack; at the end the stack must be empty.")
    st, ok = [], True
    for i, c in enumerate(s):
        if c in "([{":
            st.append(c)
            W.step(f"Push {c}.", S(s, st={i: "active"}), stack_row(st, new=True))
        else:
            good = bool(st) and st[-1] == pair[c]
            W.step(f"{c} {'matches the top ' + st[-1] + ', pop it' if good else 'has no matching opener on top'}.", S(s, st={i: "found" if good else "mark"}), stack_row(st))
            if not good:
                ok = False
                break
            st.pop()
    ok = ok and not st
    W.step("Sealed." if ok else "Not sealed.", Vars(answer=ok), result=ok)
    assert ok == exp
    return W.save()


@run
def patch_the_brackets(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Track how many ( are open. A ) with nothing open needs an inserted (; whatever is still open at the end needs a ).")
    open_, add = 0, 0
    for i, c in enumerate(s):
        if c == "(":
            open_ += 1
            text = "Open one more."
        elif open_:
            open_ -= 1
            text = "Close one."
        else:
            add += 1
            text = "Nothing to close: insert a ( for it."
        W.step(text, S(s, st={i: "active"}), Vars(open=open_, inserted=add))
    res = add + open_
    W.step(f"{open_} still open: insert that many ). Total {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def longest_balanced_stretch(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Keep a stack of indexes, starting with −1 as a floor. A ) pops; if the stack empties, this ) becomes the new floor; otherwise the stretch since the top is balanced.")
    st, best = [-1], 0
    for i, c in enumerate(s):
        if c == "(":
            st.append(i)
            text = f"Push index {i}."
        else:
            st.pop()
            if not st:
                st.append(i)
                text = f"Nothing to match: index {i} is the new floor."
            else:
                best = max(best, i - st[-1])
                text = f"Balanced from {st[-1] + 1} to {i}: length {i - st[-1]}. Best {best}."
        W.step(text, S(s, st={**({k: "found" for k in range(st[-1] + 1, i + 1)} if c == ")" and st[-1] != i else {}), i: "active"}), stack_row(st, label="index stack"))
    assert best == exp
    return W.save()


@run
def nested_box_value(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Keep a stack of running scores, one per open box. ( starts a new score; ) closes it: an empty box is worth 1, otherwise double, added to the box around it.")
    st = [0]
    for i, c in enumerate(s):
        if c == "(":
            st.append(0)
            text = "Open a box."
        else:
            inner = st.pop()
            val = 1 if inner == 0 else 2 * inner
            st[-1] += val
            text = f"Close a box worth {'1 (empty)' if inner == 0 else f'2 × {inner} = {val}'}."
        W.step(text, S(s, st={i: "active"}), stack_row(st, label="scores"))
    res = st[0] % (10**9 + 7)
    assert res == exp
    return W.save()


@run
def strip_stray_brackets(pid):
    a, exp = example(pid)
    s = list(a["s"])
    W = Walk(pid, "Scan once with a stack of open ( indexes: a ) with nothing open is stray. Any ( still open at the end is stray too.")
    st, drop = [], set()
    for i, c in enumerate(s):
        if c == "(":
            st.append(i)
            W.step("Push its index.", S(s, st={i: "active", **{k: "mark" for k in drop}}), stack_row(st, label="open ( indexes"))
        elif c == ")":
            if st:
                j = st.pop()
                W.step(f"Matches the ( at {j}.", S(s, st={i: "found", j: "found", **{k: "mark" for k in drop}}), stack_row(st, label="open ( indexes"))
            else:
                drop.add(i)
                W.step("Nothing open: this ) is stray.", S(s, st={k: "mark" for k in drop}), stack_row(st, label="open ( indexes"))
    drop |= set(st)
    out = "".join(c for i, c in enumerate(s) if i not in drop)
    W.step(f"Remove the stray brackets: \"{out}\".", S(s, st={k: "mark" for k in drop}), result=out)
    assert out == exp
    return W.save()


# ======================================================================== expression-eval

@run
def postfix_calculator(pid):
    a, exp = example(pid)
    toks = a["tokens"]
    W = Walk(pid, "Push numbers. An operator pops two values (second, then first), combines them and pushes the result.")
    st = []
    for i, t in enumerate(toks):
        if t in "+-*/" and len(t) == 1:
            b, x = st.pop(), st.pop()
            r = x + b if t == "+" else x - b if t == "-" else x * b if t == "*" else int(x / b)
            st.append(r)
            W.step(f"{x} {t} {b} = {r}.", Row(toks, st={i: "active"}), stack_row(st, new=True))
        else:
            st.append(int(t))
            W.step(f"Push {t}.", Row(toks, st={i: "active"}), stack_row(st, new=True))
    assert st[-1] == exp
    return W.save()


def tokenize(e):
    out, i = [], 0
    while i < len(e):
        if e[i].isdigit():
            j = i
            while j < len(e) and e[j].isdigit():
                j += 1
            out.append(e[i:j])
            i = j
        elif e[i] != " ":
            out.append(e[i])
            i += 1
        else:
            i += 1
    return out


@run
def desk_calculator(pid):
    a, exp = example(pid)
    toks = tokenize(a["expr"])
    W = Walk(pid, "Keep a stack of terms to add. + and − push the next number (negated for −); * and / combine with the top term right away.")
    st, op = [], "+"
    for i, t in enumerate(toks):
        if t.isdigit():
            n = int(t)
            if op == "+":
                st.append(n)
            elif op == "-":
                st.append(-n)
            elif op == "*":
                st.append(st.pop() * n)
            else:
                x = st.pop()
                st.append(int(x / n))
            W.step(f"{op} {t}: terms are now {st}.", Row(toks, st={i: "active"}), stack_row(st, label="terms", new=True))
        else:
            op = t
    res = sum(st)
    W.step(f"Add up the terms: {res}.", stack_row(st, label="terms"), result=res)
    assert res == exp
    return W.save()


@run
def pocket_calculator(pid):
    a, exp = example(pid)
    toks = tokenize(a["expr"])
    W = Walk(pid, "Evaluate with a running total and sign, like the desk calculator. A ( saves the current total and sign on a stack; ) finishes the inner value and folds it back in.")
    pos = [0]

    def expr():
        terms, op, prev_open = [], "+", True
        while pos[0] < len(toks) and toks[pos[0]] != ")":
            t = toks[pos[0]]
            if t in "+-*/":
                if t == "-" and prev_open and op == "+":
                    op = "neg"
                else:
                    op = t
                pos[0] += 1
                prev_open = False
                continue
            if t == "(":
                start = pos[0]
                pos[0] += 1
                W.step("Open a bracket: save the work so far.", Row(toks, st={start: "active"}), stack_row(terms, label="terms outside"))
                val = expr()
                pos[0] += 1
                W.step(f"Close the bracket: it's worth {val}.", Row(toks, st={pos[0] - 1: "active"}), Vars(inner=val))
            else:
                val = int(t)
                pos[0] += 1
            if op in ("+", "neg"):
                terms.append(val if op == "+" else -val)
            elif op == "-":
                terms.append(-val)
            elif op == "*":
                terms.append(terms.pop() * val)
            else:
                x = terms.pop()
                terms.append(int(x / val))
            W.step(f"Terms: {terms}.", Row(toks, st={pos[0] - 1: "found"}), stack_row(terms, label="terms", new=True))
            prev_open = False
        return sum(terms)

    res = expr()
    W.step(f"Total: {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def rewrite_in_postfix(pid):
    a, exp = example(pid)
    e = a["expr"]
    prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    W = Walk(pid, "Shunting-yard: letters go straight to the output; an operator first pops operators that bind tighter (or as tight, for left-grouping ones).")
    out, st = "", []
    for i, c in enumerate(e):
        if c.isalpha():
            out += c
            text = f"{c} goes to the output."
        elif c == "(":
            st.append(c)
            text = "Push (."
        elif c == ")":
            while st[-1] != "(":
                out += st.pop()
            st.pop()
            text = "Pop operators back to the (."
        else:
            while st and st[-1] != "(" and (prec[st[-1]] > prec[c] or (prec[st[-1]] == prec[c] and c != "^")):
                out += st.pop()
            st.append(c)
            text = f"Push {c} after popping anything that binds tighter."
        W.step(text, S(e, st={i: "active"}), stack_row(st, label="operators"), Vars(output=out))
    while st:
        out += st.pop()
    W.step(f"Pop the rest: \"{out}\".", Vars(output=out), result=out)
    assert out == exp
    return W.save()


# ======================================================================== monotonic-stack

@run
def warmer_day_wait(pid):
    a, exp = example(pid)
    t = a["temps"]
    W = Walk(pid, "Keep a stack of days still waiting for a warmer day. Each new day answers every waiting day that is colder.")
    out, st = [0] * len(t), []
    for i, x in enumerate(t):
        done = []
        while st and t[st[-1]] < x:
            j = st.pop()
            out[j] = i - j
            done.append(j)
        st.append(i)
        W.step(f"Day {i} ({x}°)" + (f" is warmer than days {done}: they waited {[out[j] for j in done]}." if done else ": nobody waiting is colder."), Row(t, st={**{j: "answer" for j in done}, i: "active"}), stack_row([t[j] for j in st], label="waiting (temps)"), Row(out, label="wait"))
    assert out == exp
    return W.save()


@run
def next_bigger_on_the_ring(pid):
    a, exp = example(pid)
    v = a["ring"]
    n = len(v)
    W = Walk(pid, "Walk the ring twice (index i % n) with a stack of tiles still waiting for something bigger.")
    out, st = [-1] * n, []
    for k in range(2 * n):
        i = k % n
        done = []
        while st and v[st[-1]] < v[i]:
            j = st.pop()
            out[j] = v[i]
            done.append(j)
        if k < n:
            st.append(i)
        if done or k < n:
            W.step(f"{'Second lap, ' if k >= n else ''}tile {i} ({v[i]})" + (f" answers tiles {done}." if done else "."), Row(v, st={**{j: "answer" for j in done}, i: "active"}), stack_row([v[j] for j in st], label="waiting"), Row(out, label="answer"))
    assert out == exp
    return W.save()


@run
def who_can_you_see(pid):
    a, exp = example(pid)
    h = a["heights"]
    W = Walk(pid, "Go from the back of the line with a stack of people still visible. Everyone shorter gets seen and then hidden; the first person at least as tall is seen too.")
    out, st = [0] * len(h), []
    for i in range(len(h) - 1, -1, -1):
        c = 0
        while st and st[-1] < h[i]:
            st.pop()
            c += 1
        if st:
            c += 1
            if st[-1] == h[i]:
                st.pop()
        out[i] = c
        st.append(h[i])
        W.step(f"Person {i} (height {h[i]}) sees {c}.", Row(h, st={i: "active", **{k: "dim" for k in range(i + 1, len(h))}}), stack_row(st, label="visible from here (heights)"), Row(out, label="sees"))
    assert out == exp
    return W.save()


@run
def low_high_between(pid):
    a, exp = example(pid)
    v = a["values"]
    W = Walk(pid, "Scan from the right keeping a stack of candidate 'highs' and the best 'in-between' value popped so far. Any value below that in-between completes the pattern.")
    st, third, found = [], None, False
    for i in range(len(v) - 1, -1, -1):
        x = v[i]
        if third is not None and x < third:
            found = True
            W.step(f"{x} < {third}: {x}, then something higher, then {third} — found.", Row(v, st={i: "answer"}), stack_row(st, label="highs"), Vars(in_between=third), result=True)
            break
        while st and st[-1] < x:
            third = st.pop()
        st.append(x)
        W.step(f"{x}: pop smaller values; the best in-between is now {third}.", Row(v, st={i: "active"}), stack_row(st, label="highs"), Vars(in_between=third if third is not None else "–"))
    if not found:
        W.step("No such three moments.", Row(v), result=False)
    assert found == exp
    return W.save()


@run
def trim_the_reading(pid):
    a, exp = example(pid)
    num, k = a["num"], a["k"]
    W = Walk(pid, f"Keep the kept digits on a stack. While a new digit is smaller than the top and erasures are left, erase the top: an earlier smaller digit always wins.")
    st, left = [], k
    for i, d in enumerate(num):
        popped = []
        while left and st and st[-1] > d:
            popped.append(st.pop())
            left -= 1
        st.append(d)
        W.step((f"{d} beats {', '.join(popped)}: erase {'them' if len(popped) > 1 else 'it'}. " if popped else f"Keep {d}. ") + f"{left} erasure{'s' if left != 1 else ''} left.", S(num, st={i: "active"}), stack_row(st, label="kept"))
    st = st[:len(st) - left]
    res = "".join(st).lstrip("0") or "0"
    W.step(f"Result: {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def strongest_crew_stretch(pid):
    a, exp = example(pid)
    v = a["strength"]
    n = len(v)
    W = Walk(pid, "If worker i is the weakest, the crew stretches until a weaker worker on each side. Find those bounds with monotonic stacks; prefix sums give each crew's total.")
    left, right, st = [-1] * n, [n] * n, []
    for i in range(n):
        while st and v[st[-1]] >= v[i]:
            right[st.pop()] = i
        left[i] = st[-1] if st else -1
        st.append(i)
    pre = [0]
    for x in v:
        pre.append(pre[-1] + x)
    best = 0
    for i in range(n):
        tot = pre[right[i]] - pre[left[i] + 1]
        best = max(best, v[i] * tot)
        W.step(f"{v[i]} weakest over positions {left[i] + 1}–{right[i] - 1}: {v[i]} × {tot} = {v[i] * tot}. Best {best}.", Row(v, st={**{k: "found" for k in range(left[i] + 1, right[i])}, i: "active"}))
    assert best == exp
    return W.save()


# ======================================================================== histogram-area

def smaller_bounds(v):
    n = len(v)
    left, right, st = [-1] * n, [n] * n, []
    for i in range(n):
        while st and v[st[-1]] > v[i]:
            right[st.pop()] = i
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and v[st[-1]] > v[i]:
            left[st.pop()] = i
        st.append(i)
    return left, right


@run
def poster_reach(pid):
    a, exp = example(pid)
    v = a["panels"]
    W = Walk(pid, "A poster for panel i stops at the first shorter panel on each side. One monotonic-stack pass per side finds those.")
    left, right = smaller_bounds(v)
    out = []
    for i in range(len(v)):
        out.append(right[i] - left[i] - 1)
        W.step(f"Panel {i} ({v[i]}): shorter panels at {left[i]} and {right[i]}, width {out[-1]}.", Row(v, st={**{k: "found" for k in range(left[i] + 1, right[i])}, i: "active"}), Row(out, label="width"))
    assert out == exp
    return W.save()


@run
def biggest_billboard(pid):
    a, exp = example(pid)
    v = a["heights"]
    W = Walk(pid, "Keep a stack of rising heights. When a shorter building arrives, each taller one popped is done: its billboard runs from just after the new top to just before here.")
    st, best = [], 0
    for i, x in enumerate(v + [0]):
        while st and v[st[-1]] > x:
            h = v[st.pop()]
            left = st[-1] if st else -1
            area = h * (i - left - 1)
            best = max(best, area)
            W.step(f"Height {h} spans positions {left + 1}–{i - 1}: area {area}. Best {best}.", Row(v, st={k: "found" for k in range(left + 1, i)}), stack_row([v[j] for j in st], label="rising heights"))
        st.append(i)
    assert best == exp
    return W.save()


@run
def largest_clear_plot(pid):
    a, exp = example(pid)
    land = a["land"]
    m, n = len(land), len(land[0])
    W = Walk(pid, "Row by row, build a histogram: each column's height is how many clear cells stand above it. The best plot is the biggest billboard of some row's histogram.")
    h, best = [0] * n, 0
    for r in range(m):
        h = [h[c] + 1 if land[r][c] == "1" else 0 for c in range(n)]
        st, row_best = [], 0
        for i, x in enumerate(h + [0]):
            while st and h[st[-1]] > x:
                hh = h[st.pop()]
                left = st[-1] if st else -1
                row_best = max(row_best, hh * (i - left - 1))
            st.append(i)
        best = max(best, row_best)
        W.step(f"Row {r}: heights {h}, best rectangle {row_best}. Best overall {best}.", Grid(land, {(rr, c): "found" for rr in range(r + 1) for c in range(n) if land[rr][c] == "1" and r - rr < h[c]}), Row(h, label="histogram"))
    assert best == exp
    return W.save()


@run
def largest_pool(pid):
    a, exp = example(pid)
    v = a["walls"]
    n = len(v)
    lm, rm = [0] * n, [0] * n
    for i in range(n):
        lm[i] = max(v[i], lm[i - 1] if i else 0)
    for i in range(n - 1, -1, -1):
        rm[i] = max(v[i], rm[i + 1] if i < n - 1 else 0)
    water = [min(lm[i], rm[i]) - v[i] for i in range(n)]
    W = Walk(pid, "Water over each column = min(tallest left, tallest right) − its height. Then group neighbouring wet columns into pools.")
    W.step("Water over each column.", Row(v, label="walls"), Row(water, label="water"))
    best, cur, start = 0, 0, None
    for i in range(n + 1):
        if i < n and water[i] > 0:
            if start is None:
                start = i
            cur += water[i]
        elif start is not None:
            best = max(best, cur)
            W.step(f"Pool over columns {start}–{i - 1}: {cur}. Largest {best}.", Row(v, label="walls"), Row(water, st={k: "answer" for k in range(start, i)}, label="water"))
            cur, start = 0, None
    assert best == exp
    return W.save()


# ======================================================================== contribution-counting

@run
def sum_of_stretch_lows(pid):
    a, exp = example(pid)
    v = a["prices"]
    n = len(v)
    W = Walk(pid, "Price i is the low of every stretch that starts after the previous smaller price and ends before the next smaller-or-equal one. That's left × right stretches.")
    left, right, st = [0] * n, [0] * n, []
    for i in range(n):
        while st and v[st[-1]] >= v[i]:
            st.pop()
        left[i] = i - (st[-1] if st else -1)
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and v[st[-1]] > v[i]:
            st.pop()
        right[i] = (st[-1] if st else n) - i
        st.append(i)
    total = 0
    for i in range(n):
        total += v[i] * left[i] * right[i]
        W.step(f"{v[i]} is the low of {left[i]} × {right[i]} = {left[i] * right[i]} stretches: adds {v[i] * left[i] * right[i]}. Total {total}.",
               Row(v, st={**{k: "found" for k in range(i - left[i] + 1, i + right[i])}, i: "active"}))
    res = total % (10**9 + 7)
    assert res == exp
    return W.save()


@run
def total_swing(pid):
    a, exp = example(pid)
    v = a["readings"]
    n = len(v)
    W = Walk(pid, "Total swing = (sum of every stretch's max) − (sum of every stretch's min). Count how many stretches each reading is the max of, and the min of.")

    def counts(better):
        left, right, st = [0] * n, [0] * n, []
        for i in range(n):
            while st and not better(v[st[-1]], v[i]):
                st.pop()
            left[i] = i - (st[-1] if st else -1)
            st.append(i)
        st = []
        for i in range(n - 1, -1, -1):
            while st and better(v[i], v[st[-1]]):
                st.pop()
            right[i] = (st[-1] if st else n) - i
            st.append(i)
        return [l_ * r for l_, r in zip(left, right)]

    mx, mn = counts(lambda x, y: x > y), counts(lambda x, y: x < y)
    total = 0
    for i in range(n):
        total += v[i] * (mx[i] - mn[i])
        W.step(f"{v[i]} is the max of {mx[i]} stretches and the min of {mn[i]}: adds {v[i]} × ({mx[i]} − {mn[i]}). Total {total}.", Row(v, st={i: "active"}), Row(mx, st={i: "found"}, label="as max"), Row(mn, st={i: "found"}, label="as min"))
    assert total == exp
    return W.save()


# ======================================================================== monotonic-deque

@run
def window_peaks(pid):
    a, exp = example(pid)
    v, k = a["temps"], a["k"]
    W = Walk(pid, "Keep a deque of indexes with falling readings: drop smaller readings from the back (they can never be a peak), drop the front once it leaves the window.")
    dq, out = deque(), []
    for i, x in enumerate(v):
        while dq and v[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(v[dq[0]])
            W.step(f"Window {i - k + 1}–{i}: the peak is at the deque's front, {v[dq[0]]}.", Row(v, st={**{j: "active" for j in range(i - k + 1, i + 1)}, dq[0]: "answer"}), Row([v[j] for j in dq], label="deque"), Row(out, label="peaks"))
    assert out == exp
    return W.save()


@run
def shortest_net_gain(pid):
    a, exp = example(pid)
    v, t = a["changes"], a["target"]
    n = len(v)
    pre = [0]
    for x in v:
        pre.append(pre[-1] + x)
    W = Walk(pid, f"In prefix sums, find j > i with P[j] − P[i] ≥ {t} and j − i smallest. A deque of rising prefixes holds the only starts worth keeping.")
    W.step("Prefix sums.", Row(v, label="changes"), Row(pre, label="P"))
    best, dq = n + 1, deque()
    for j in range(n + 1):
        while dq and pre[j] - pre[dq[0]] >= t:
            best = min(best, j - dq[0])
            W.step(f"P[{j}] − P[{dq[0]}] = {pre[j] - pre[dq[0]]} ≥ {t}: length {j - dq[0]}. Shortest {best}.", Row(pre, st={dq[0]: "answer", j: "answer"}, label="P"), Row(list(dq), label="deque (indexes)"))
            dq.popleft()
        while dq and pre[dq[-1]] >= pre[j]:
            dq.pop()
        dq.append(j)
    res = best if best <= n else -1
    W.step(f"Answer: {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def stepping_stones_score(pid):
    a, exp = example(pid)
    v, k = a["stones"], a["k"]
    n = len(v)
    W = Walk(pid, f"best[i] = stones[i] + the largest best among the previous {k}. A deque of indexes with falling best values keeps that maximum at its front.")
    best = [None] * n
    best[0] = v[0]
    dq = deque([0])
    W.step("Start on stone 0.", Row(v, label="stones"), Row(best, st={0: "new"}, label="best"))
    for i in range(1, n):
        if dq[0] < i - k:
            dq.popleft()
        best[i] = v[i] + best[dq[0]]
        W.step(f"Stone {i}: {v[i]} + best[{dq[0]}] ({best[dq[0]]}) = {best[i]}.", Row(v, st={i: "active"}, label="stones"), Row(best, st={i: "new", dq[0]: "found"}, label="best"), Row(list(dq), label="deque"))
        while dq and best[dq[-1]] <= best[i]:
            dq.pop()
        dq.append(i)
    assert best[-1] == exp
    return W.save()


@run
def best_pair_of_posts(pid):
    a, exp = example(pid)
    posts, k = a["posts"], a["k"]
    W = Walk(pid, f"For i < j the value is (y_j + x_j) + (y_i − x_i). Keep a deque of earlier posts within {k}, best y − x at the front.")
    dq, best = deque(), None
    xs = [p[0] for p in posts]
    for j, (x, y) in enumerate(posts):
        while dq and x - posts[dq[0]][0] > k:
            dq.popleft()
        if dq:
            xi, yi = posts[dq[0]]
            val = y + x + yi - xi
            best = val if best is None else max(best, val)
            W.step(f"Post at {x}: pair with the post at {xi} for {val}. Best {best}.", Row(xs, st={j: "active", dq[0]: "answer"}, label="positions"), Row([posts[i][1] - posts[i][0] for i in dq], label="deque: y − x"))
        while dq and posts[dq[-1]][1] - posts[dq[-1]][0] <= y - x:
            dq.pop()
        dq.append(j)
    W.intro(f"Posts are sorted by position. A pair counts only if they're at most {k} apart.", Row(xs, label="positions"), Row([p[1] for p in posts], label="heights"))
    assert best == exp
    return W.save()


# ======================================================================== queue-simulation

@run
def ticket_line(pid):
    a, exp = example(pid)
    v, k = a["wants"], a["k"]
    need = v[k]
    W = Walk(pid, f"No need to simulate: by the time person {k} buys their last ticket, people up to {k} bought min(want, {need}) and people after bought min(want, {need - 1}).")
    parts = [min(w, need) if i <= k else min(w, need - 1) for i, w in enumerate(v)]
    W.step("Tickets each person buys before person k finishes.", Row(v, st={k: "mark"}, label="wants"), Row(parts, label="bought by then"))
    W.step(f"Seconds = {' + '.join(map(str, parts))} = {sum(parts)}.", Vars(answer=sum(parts)), result=sum(parts))
    W.intro(f"Each second the front person buys one ticket and rejoins the back if they still want more. Person {k} wants {need}.", Row(v, st={k: "mark"}, label="wants"))
    assert sum(parts) == exp
    return W.save()


@run
def lunch_line(pid):
    a, exp = example(pid)
    p, t = a["prefers"], a["trays"]
    W = Walk(pid, "Order in the queue doesn't matter: students rotate until someone wants the top tray. Count each preference and serve trays until one isn't wanted.")
    want = [p.count(0), p.count(1)]
    for i, tray in enumerate(t):
        if want[tray] == 0:
            W.step(f"Tray {i} is type {tray}, but nobody left wants it: the line is stuck.", Row(t, st={i: "mark"}, label="trays"), Vars(want_0=want[0], want_1=want[1]))
            break
        want[tray] -= 1
        W.step(f"Tray {i} (type {tray}) is taken.", Row(t, st={**{j: "dim" for j in range(i)}, i: "active"}, label="trays"), Vars(want_0=want[0], want_1=want[1]))
    res = sum(want)
    W.step(f"{res} student{'s' if res != 1 else ''} go hungry.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def council_vote(pid):
    a, exp = example(pid)
    s = a["council"]
    n = len(s)
    L_ = deque(i for i, c in enumerate(s) if c == "L")
    O = deque(i for i, c in enumerate(s) if c == "O")
    W = Walk(pid, "Two queues of speaking turns. The earlier speaker silences the other and rejoins its queue for the next round (turn + n).")
    while L_ and O:
        x, y = L_.popleft(), O.popleft()
        if x < y:
            L_.append(x + n)
            text = f"Lark (turn {x}) speaks first and silences the Owl at turn {y}."
        else:
            O.append(y + n)
            text = f"Owl (turn {y}) speaks first and silences the Lark at turn {x}."
        W.step(text, Row(list(L_), label="Larks' turns"), Row(list(O), label="Owls' turns"))
    res = "Larks" if L_ else "Owls"
    W.step(f"{res} win.", Vars(answer=res), result=res)
    W.intro("The best move is always to silence the next opponent due to speak. Put each party's speaking turns in its own queue.", S(s))
    assert res == exp
    return W.save()


@run
def magic_card_reveal(pid):
    a, exp = example(pid)
    cards = sorted(a["cards"])
    n = len(cards)
    W = Walk(pid, "Simulate the trick on positions: take the front position (revealed next), then move the new front to the back. Put the smallest unused card in each revealed position.")
    q, out = deque(range(n)), [None] * n
    for c in cards:
        pos = q.popleft()
        out[pos] = c
        if q:
            q.append(q.popleft())
        W.step(f"Position {pos} is revealed next: put {c} there.", Row(list(q), label="positions queue"), Row(out, st={pos: "new"}, label="deck"))
    assert out == exp
    return W.save()


# ======================================================================== stack-string-building

@run
def typing_with_backspace(pid):
    a, exp = example(pid)
    x, y = a["a"], a["b"]
    W = Walk(pid, "Type each string onto a stack: letters push, # pops (if there's anything). Compare the two stacks.")

    def typed(s, label):
        st = []
        for i, c in enumerate(s):
            if c == "#":
                if st:
                    st.pop()
            else:
                st.append(c)
            W.step(f"{label}: '{c}'.", S(s, st={i: "active"}, label=label), stack_row(st, label="screen"))
        return st

    p, q = typed(x, "a"), typed(y, "b")
    ok = p == q
    W.step(f"Screens: \"{''.join(p)}\" and \"{''.join(q)}\": {'same' if ok else 'different'}.", Vars(answer=ok), result=ok)
    assert ok == exp
    return W.save()


@run
def crush_the_runs(pid):
    a, exp = example(pid)
    s, k = a["s"], a["k"]
    W = Walk(pid, f"Keep a stack of [letter, count]. A letter matching the top adds to its count; reaching {k} crushes it, which lets the run below meet the next letter.")
    st = []
    for i, c in enumerate(s):
        if st and st[-1][0] == c:
            st[-1][1] += 1
            if st[-1][1] == k:
                st.pop()
                W.step(f"{c} makes {k} in a row: crush.", S(s, st={i: "mark"}), stack_row([f"{x}×{n}" for x, n in st]))
                continue
        else:
            st.append([c, 1])
        W.step(f"Add {c}.", S(s, st={i: "active"}), stack_row([f"{x}×{n}" for x, n in st], new=True))
    out = "".join(x * n for x, n in st)
    assert out == exp
    return W.save()


@run
def expand_the_pattern(pid):
    a, exp = example(pid)
    s = a["pattern"]
    W = Walk(pid, "On [ save (text so far, repeat count) on a stack and start fresh. On ] pop them and set text = saved + current × count.")
    st, cur, num = [], "", 0
    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
            continue
        if c == "[":
            st.append((cur, num))
            cur, num = "", 0
            text = "Save and start fresh."
        elif c == "]":
            prev, k = st.pop()
            cur = prev + cur * k
            text = f"Close: repeat × {k}."
        else:
            cur += c
            text = f"Add {c}."
        W.step(text, S(s, st={i: "active"}), stack_row([f"{p or '∅'}·{k}" for p, k in st], label="saved (text·count)"), Vars(current=cur))
    assert cur == exp
    return W.save()


@run
def tidy_the_path(pid):
    a, exp = example(pid)
    p = a["path"]
    W = Walk(pid, "Split on /. Skip empty parts and '.', pop on '..', push any other name.")
    st = []
    parts = p.split("/")
    for i, part in enumerate(parts):
        if part == "..":
            if st:
                st.pop()
            text = "'..': go up."
        elif part and part != ".":
            st.append(part)
            text = f"Enter '{part}'."
        else:
            continue
        W.step(text, Row([x or "∅" for x in parts], st={i: "active"}, label="parts"), stack_row(st, label="folders"))
    out = "/" + "/".join(st)
    W.step(f"Result: {out}", Vars(path=out), result=out)
    W.intro("Every part between slashes is a step: a folder name goes down, '..' goes up, '.' and empty parts do nothing.", S(p))
    assert out == exp
    return W.save()


# ======================================================================== stack-simulation

@run
def comet_collisions(pid):
    a, exp = example(pid)
    v = a["comets"]
    W = Walk(pid, "Survivors sit on a stack. A left-mover crashes into right-movers on top: smaller ones break, equal ones both break, a bigger one stops it.")
    st = []
    for i, c in enumerate(v):
        alive, notes = True, []
        while alive and c < 0 and st and st[-1] > 0:
            if st[-1] < -c:
                notes.append(f"{st.pop()} breaks")
            elif st[-1] == -c:
                notes.append(f"{st.pop()} and {c} both break")
                alive = False
            else:
                notes.append(f"{c} breaks on {st[-1]}")
                alive = False
        if alive:
            st.append(c)
        W.step(f"Comet {c}: " + ("; ".join(notes) if notes else "nothing to hit") + ".", Row(v, st={i: "active"}), stack_row(st, label="survivors"))
    assert st == exp
    return W.save()


@run
def plate_stack_check(pid):
    a, exp = example(pid)
    w, s = a["washed"], a["served"]
    W = Walk(pid, "Replay it: push each washed plate, then pop while the top is the next plate to serve.")
    st, j = [], 0
    for i, p in enumerate(w):
        st.append(p)
        popped = []
        while st and st[-1] == s[j]:
            popped.append(st.pop())
            j += 1
        W.step(f"Stack {p}" + (f"; serve {popped}." if popped else "."), Row(w, st={i: "active"}, label="washed"), Row(s, st={k: "found" for k in range(j)}, label="served"), stack_row(st))
    ok = j == len(s)
    W.step("Every plate was served in order." if ok else "Stuck: the next plate to serve is buried.", Vars(answer=ok), result=ok)
    assert ok == exp
    return W.save()


@run
def convoys_to_the_depot(pid):
    a, exp = example(pid)
    d, pos, sp = a["depot"], a["position"], a["speed"]
    trucks = sorted(zip(pos, sp), reverse=True)
    W = Walk(pid, "Go from the truck closest to the depot. A truck that would arrive later than the convoy ahead starts a new convoy; otherwise it catches up and joins.")
    lead, count = None, 0
    times = [Fraction(d - p, s) for p, s in trucks]
    for i, ((p, s), t) in enumerate(zip(trucks, times)):
        if lead is None or t > lead:
            count += 1
            lead = t
            text = f"Truck at {p} arrives at {float(t):g}h, later than the convoy ahead: a new convoy ({count})."
        else:
            text = f"Truck at {p} would arrive at {float(t):g}h but catches the convoy ahead."
        W.step(text, Row([p for p, _ in trucks], st={i: "active"}, label="positions (closest first)"), Row([f"{float(x):g}" for x in times], st={i: "active"}, label="hours alone"))
    assert count == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
