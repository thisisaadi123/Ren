import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from collections import Counter, defaultdict
from lib import *

DONE = []


CUSTOM = {
    "one-slip-palindrome": [{"s": "levexvel"}],
    "cut-out-the-middle": [{"s": "abxyzcdcba"}],
    "justify-the-column": [{"words": ["the", "quick", "brown", "fox", "jumps", "over", "a", "lazy", "dog"], "width": 12}],
    "unpack-the-bundle": [{"bundle": "3#a#10#2#hi4#ab#c"}],
    "shared-tune": [{"a": "abcdxyzpq", "b": "zpqxyzabcd"}],
    "scrambled-name-tag": [{"a": "Listen", "b": "Silent"}],
    "repeating-unit": [{"s": "abcabcabcabc"}],
    "front-padding": [{"s": "aacecaaa"}],
}
run = make_runner(DONE, CUSTOM)


def S(text, st=None, ptr=None, label=None):
    return Row(list(text), st=st, ptr=ptr, label=label)


def kv(d, label, st=None):
    return Row([f"{k}→{v}" for k, v in d.items()], st=st, label=label)


# ======================================================================== char-mapping

@run
def crack_the_cipher(pid):
    a, exp = example(pid)
    plain, coded, msg = a["plain"], a["coded"], a["message"]
    W = Walk(pid, "Line the two versions up letter by letter to learn the cipher (coded → plain), then decode the message with it.")
    key = {}
    for i, (p, c) in enumerate(zip(plain, coded)):
        if c != " " and c not in key:
            key[c] = p
            W.step(f"\"{c}\" stands for \"{p}\".", S(coded, st={i: "active"}, label="coded"), S(plain, st={i: "active"}, label="plain"), kv(key, "key", st={len(key) - 1: "new"}))
    out = "".join(key.get(c, c) for c in msg)
    W.step(f"Decode: \"{out}\".", S(msg, label="message"), S(out, st={i: "found" for i in range(len(out)) if out[i] != " "}, label="decoded"), result=out)
    assert out == exp
    return W.save()


@run
def rhythm_of_words(pid):
    a, exp = example(pid)
    pat, words = a["pattern"], a["sentence"].split()
    W = Walk(pid, "Keep two maps, letter → word and word → letter. Every pair must agree with both maps.")
    if len(pat) != len(words):
        W.step(f"{len(pat)} letters but {len(words)} words: no match.", S(pat), Row(words), result=False)
        assert exp is False
        return W.save()
    l2w, w2l, ok = {}, {}, True
    for i, (c, w) in enumerate(zip(pat, words)):
        good = l2w.get(c, w) == w and w2l.get(w, c) == c
        l2w.setdefault(c, w)
        w2l.setdefault(w, c)
        W.step(f"\"{c}\" with \"{w}\": {'consistent' if good else 'clashes with an earlier pairing'}.", S(pat, st={i: "active" if good else "mark"}, label="pattern"), Row(words, st={i: "active" if good else "mark"}, label="sentence"), kv(l2w, "letter → word"))
        if not good:
            ok = False
            break
    W.step("Follows the pattern." if ok else "Doesn't follow it.", Vars(answer=ok), result=ok)
    assert ok == exp
    return W.save()


@run
def repaint_the_letters(pid):
    a, exp = example(pid)
    s, t, m = a["s"], a["t"], a["m"]
    W = Walk(pid, "Every colour in s must always become the same colour in t. And unless s already equals t, you need one spare colour to break repaint cycles.")
    mp, ok = {}, True
    for i, (x, y) in enumerate(zip(s, t)):
        if mp.get(x, y) != y:
            ok = False
            W.step(f"\"{x}\" would have to become both \"{mp[x]}\" and \"{y}\": impossible.", S(s, st={i: "mark"}, label="s"), S(t, st={i: "mark"}, label="t"), kv(mp, "colour map"), result=False)
            break
        mp[x] = y
        W.step(f"\"{x}\" must become \"{y}\".", S(s, st={i: "active"}, label="s"), S(t, st={i: "active"}, label="t"), kv(mp, "colour map"))
    if ok and s != t:
        used = len(set(t))
        ok = used < m
        W.step(f"t uses {used} of the {m} colours: " + ("a spare colour exists, so cycles can be broken." if ok else "no spare colour, so a cycle can't be untangled."), Vars(colours_in_t=used, m=m), result=ok)
    elif ok:
        W.step("s already equals t.", Vars(answer=True), result=True)
    assert ok == exp
    return W.save()


# ======================================================================== string-signature

@run
def scrambled_name_tag(pid):
    a, exp = example(pid)
    x, y = a["a"], a["b"]
    W = Walk(pid, "Ignore spaces and case. Add one for each letter of a, take one away for each letter of b; scrambles end with every count at zero.")
    c = Counter()
    for i, ch in enumerate(x):
        if ch != " ":
            c[ch.lower()] += 1
            W.step(f"a: +1 for \"{ch.lower()}\".", S(x, st={i: "active"}, label="a"), Row([f"{k}:{v}" for k, v in sorted(c.items())], label="counts"))
    for i, ch in enumerate(y):
        if ch != " ":
            c[ch.lower()] -= 1
            W.step(f"b: −1 for \"{ch.lower()}\".", S(y, st={i: "active"}, label="b"), Row([f"{k}:{v}" for k, v in sorted(c.items())], label="counts"))
    ok = all(v == 0 for v in c.values())
    W.step("Every count is zero: scrambles." if ok else "Some count isn't zero: not scrambles.", Vars(answer=ok), result=ok)
    assert ok == exp
    return W.save()



@run
def swap_and_relabel(pid):
    a, exp = example(pid)
    x, y = a["a"], a["b"]
    W = Walk(pid, "Swaps reorder freely; relabels trade counts between letters already present. So both words need the same letters and the same multiset of counts.")
    cx, cy = Counter(), Counter()
    for i, ch in enumerate(x):
        cx[ch] += 1
        W.step(f"Count a's \"{ch}\".", S(x, st={i: "active"}, label="a"), Row([f"{k}:{v}" for k, v in sorted(cx.items())], label="a counts"))
    for i, ch in enumerate(y):
        cy[ch] += 1
        W.step(f"Count b's \"{ch}\".", S(y, st={i: "active"}, label="b"), Row([f"{k}:{v}" for k, v in sorted(cy.items())], label="b counts"))
    same_letters = set(cx) == set(cy)
    same_counts = sorted(cx.values()) == sorted(cy.values())
    ok = same_letters and same_counts
    W.step(f"Same letters: {same_letters}. Same counts once sorted ({sorted(cx.values())} vs {sorted(cy.values())}): {same_counts}.", Vars(answer=ok), result=ok)
    assert ok == exp
    return W.save()



@run
def anagram_twins_in_a_word(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "For each length, give every substring a signature (its sorted letters). Substrings with the same signature are twins: a group of c makes c(c − 1)/2 pairs.")
    total = 0
    for L_ in range(1, len(s)):
        sig = Counter("".join(sorted(s[i:i + L_])) for i in range(len(s) - L_ + 1))
        pairs = sum(c * (c - 1) // 2 for c in sig.values())
        total += pairs
        W.step(f"Length {L_}: signatures {dict(sig)} give {pairs} pair{'s' if pairs != 1 else ''}. Total {total}.", S(s), kv(dict(sig), f"length {L_}"))
    assert total == exp
    return W.save()


# ======================================================================== expand-center

def centers(W, s, on_found):
    """Expand around every centre (letters and gaps), calling on_found for each palindrome found."""
    for c in range(2 * len(s) - 1):
        l, r = c // 2, c // 2 + c % 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            on_found(l, r)
            l -= 1
            r += 1


@run
def count_mirrors(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Every palindrome has a centre (a letter or a gap). Expand outward from each centre while both ends match; each step is one more palindrome.")
    total = [0]

    def found(l, r):
        total[0] += 1
        W.step(f"\"{s[l:r + 1]}\" is a palindrome. Count {total[0]}.", S(s, st={i: "answer" for i in range(l, r + 1)}))

    centers(W, s, found)
    assert total[0] == exp
    return W.save()


@run
def palindrome_census(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Expand from every centre while both ends match. (Manacher's algorithm reuses earlier expansions to make this O(n).)")
    total = [0]

    def found(l, r):
        total[0] += 1
        W.step(f"\"{s[l:r + 1]}\". Count {total[0]}.", S(s, st={i: "answer" for i in range(l, r + 1)}))

    centers(W, s, found)
    assert total[0] == exp
    return W.save()


@run
def longest_echo(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Try every centre (each letter, and each gap between letters) and expand while both ends match. Keep the longest.")
    best = 0
    for c in range(2 * len(s) - 1):
        l, r = c // 2, c // 2 + c % 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        length = r - l - 1
        if length > best:
            best = length
        where = f"letter {c // 2}" if c % 2 == 0 else f"the gap after {c // 2}"
        W.step(f"Centre at {where}: expands to length {length}. Longest {best}.", S(s, st={i: ("answer" if length == best else "active") for i in range(l + 1, r)} if length else {}))
    assert best == exp
    return W.save()



@run
def longest_echo_text(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Try every centre left to right and expand while both ends match. Keep the first palindrome of the greatest length.")
    best, at = "", len(s)
    for c in range(2 * len(s) - 1):
        l, r = c // 2, c // 2 + c % 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        cand = s[l + 1:r]
        if len(cand) > len(best) or (len(cand) == len(best) and l + 1 < at):
            best, at = cand, l + 1
        where = f"letter {c // 2}" if c % 2 == 0 else f"the gap after {c // 2}"
        W.step(f"Centre at {where}: \"{cand}\". Best \"{best}\".", S(s, st={i: ("answer" if cand == best and l + 1 == at else "active") for i in range(l + 1, r)} if cand else {}))
    assert best == exp
    return W.save()



# ======================================================================== palindrome-checks

@run
def mirror_sentence(pid):
    a, exp = example(pid)
    t = a["text"]
    W = Walk(pid, "Two pointers from both ends skip anything that isn't a letter or digit, and compare the rest ignoring case.")
    i, j, ok = 0, len(t) - 1, True
    while i < j:
        if not t[i].isalnum():
            i += 1
            continue
        if not t[j].isalnum():
            j -= 1
            continue
        same = t[i].lower() == t[j].lower()
        W.step(f"\"{t[i]}\" vs \"{t[j]}\": {'match' if same else 'different'}.", S(t, st={i: "found" if same else "mark", j: "found" if same else "mark"}, ptr={"i": i, "j": j}))
        if not same:
            ok = False
            break
        i += 1
        j -= 1
    W.step("It's a mirror." if ok else "Not a mirror.", Vars(answer=ok), result=ok)
    assert ok == exp
    return W.save()


@run
def one_slip_palindrome(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Match from both ends. At the first mismatch, try skipping either the left or the right letter; one of the rest must be a palindrome.")
    i, j = 0, len(s) - 1
    while i < j and s[i] == s[j]:
        W.step(f"\"{s[i]}\" = \"{s[j]}\".", S(s, st={i: "found", j: "found"}, ptr={"i": i, "j": j}))
        i += 1
        j -= 1
    if i >= j:
        ok = True
        W.step("Already a palindrome.", S(s), result=True)
    else:
        a1, a2 = s[i + 1:j + 1], s[i:j]
        ok = a1 == a1[::-1] or a2 == a2[::-1]
        W.step(f"\"{s[i]}\" ≠ \"{s[j]}\". Skip left → \"{a1}\" {'is' if a1 == a1[::-1] else 'isn’t'} a palindrome; skip right → \"{a2}\" {'is' if a2 == a2[::-1] else 'isn’t'}.",
               S(s, st={i: "mark", j: "mark"}, ptr={"i": i, "j": j}), result=ok)
    assert ok == exp
    return W.save()


@run
def cut_out_the_middle(pid):
    a, exp = example(pid)
    s = a["s"]
    n = len(s)
    W = Walk(pid, "Match letters from both ends as long as they agree. The cut must lie in the middle that's left; keep the longest palindrome at either end of that middle.")
    i = 0
    while i < n - 1 - i and s[i] == s[n - 1 - i]:
        W.step(f"\"{s[i]}\" at both ends: keep them.", S(s, st={**{k: "found" for k in range(i)}, **{n - 1 - k: "found" for k in range(i)}, i: "active", n - 1 - i: "active"}))
        i += 1
    mid = s[i:n - i]
    W.step(f"The ends disagree. The middle left is \"{mid}\".", S(s, st={k: "mark" for k in range(i, n - i)}))
    pre = max(L_ for L_ in range(len(mid) + 1) if mid[:L_] == mid[:L_][::-1])
    W.step(f"Longest palindrome at the start of the middle: \"{mid[:pre]}\" ({pre}).", S(mid, st={k: "found" for k in range(pre)}, label="middle"))
    suf = max(L_ for L_ in range(len(mid) + 1) if mid[len(mid) - L_:] == mid[len(mid) - L_:][::-1])
    W.step(f"Longest palindrome at its end: \"{mid[len(mid) - suf:]}\" ({suf}).", S(mid, st={k: "found" for k in range(len(mid) - suf, len(mid))}, label="middle"))
    cut = len(mid) - max(pre, suf)
    W.step(f"Keep the longer one; cut the other {cut} letter{'s' if cut != 1 else ''}.", Vars(cut=cut), result=cut)
    assert cut == exp
    return W.save()



# ======================================================================== parsing-simulation

@run
def read_the_meter(pid):
    a, exp = example(pid)
    t = a["text"]
    W = Walk(pid, "Read left to right: spaces, an optional sign, then digits (a single _ between two digits is skipped). Stop at anything else.")
    i = 0
    while i < len(t) and t[i] == " ":
        i += 1
    W.step(f"Skip {i} leading space{'s' if i != 1 else ''}.", S(t, st={k: "dim" for k in range(i)}, ptr={"i": i}))
    sign = 1
    if i < len(t) and t[i] in "+-":
        sign = -1 if t[i] == "-" else 1
        W.step(f"Sign {t[i]}.", S(t, st={i: "active"}, ptr={"i": i}))
        i += 1
    val, read = 0, False
    while i < len(t):
        if t[i].isdigit():
            val = val * 10 + int(t[i])
            read = True
            W.step(f"Digit {t[i]}: value {val}.", S(t, st={i: "found"}, ptr={"i": i}), Vars(value=val))
            i += 1
        elif t[i] == "_" and read and i + 1 < len(t) and t[i + 1].isdigit():
            W.step("A separator between digits: skip it.", S(t, st={i: "dim"}, ptr={"i": i}))
            i += 1
        else:
            break
    res = max(-2**31, min(2**31 - 1, sign * val)) if read else 0
    W.step(f"Stop. Reading: {res}.", S(t, st={k: "dim" for k in range(i, len(t))}), result=res)
    assert res == exp
    return W.save()


@run
def justify_the_column(pid):
    a, exp = example(pid)
    words, width = a["words"], a["width"]
    W = Walk(pid, f"Fill each line greedily, then spread its extra spaces between the gaps (leftmost gaps get any extra). The last line is left-aligned.")
    out, i = [], 0
    while i < len(words):
        j, length = i, len(words[i])
        while j + 1 < len(words) and length + 1 + len(words[j + 1]) <= width:
            j += 1
            length += 1 + len(words[j])
        line = words[i:j + 1]
        if j == len(words) - 1 or len(line) == 1:
            text = " ".join(line).ljust(width)
            how = "last line or a single word: left-align."
        else:
            spaces = width - sum(map(len, line))
            gaps = len(line) - 1
            text = ""
            for k, w in enumerate(line[:-1]):
                text += w + " " * (spaces // gaps + (1 if k < spaces % gaps else 0))
            text += line[-1]
            how = f"{spaces} spaces over {gaps} gap{'s' if gaps != 1 else ''}."
        out.append(text)
        W.step(f"Line {len(out)}: {line} — {how}", Row(words, st={k: "active" for k in range(i, j + 1)}), Row([o.replace(' ', '·') for o in out], label="lines (· = space)"))
        i = j + 1
    assert out == exp
    return W.save()


@run
def zigzag_banner(pid):
    a, exp = example(pid)
    t, rows = a["text"], a["rows"]
    W = Walk(pid, "Walk down the rows and back up again, dropping each character on its row. Then read the rows top to bottom.")
    if rows == 1:
        W.step("One row: nothing moves.", S(t), result=t)
        assert t == exp
        return W.save()
    lines, r, step = [""] * rows, 0, 1
    for i, ch in enumerate(t):
        lines[r] += ch
        if i % 3 == 2 or i == len(t) - 1:
            W.step(f"Placed up to \"{ch}\" (position {i}).", S(t, st={k: "dim" for k in range(i + 1)}), *[Row(list(l), label=f"row {k}") for k, l in enumerate(lines)])
        if r == 0:
            step = 1
        elif r == rows - 1:
            step = -1
        r += step
    out = "".join(lines)
    W.step(f"Read the rows in order: \"{out}\".", S(out, st={i: "found" for i in range(len(out))}), result=out)
    assert out == exp
    return W.save()


@run
def unpack_the_bundle(pid):
    a, exp = example(pid)
    b = a["bundle"]
    W = Walk(pid, "Read digits up to the first #: that's the length. Then take exactly that many characters, whatever they are.")
    out, i = [], 0
    while i < len(b):
        j = b.index("#", i)
        n = int(b[i:j])
        piece = b[j + 1:j + 1 + n]
        out.append(piece)
        W.step(f"Length {n}: take \"{piece}\".", S(b, st={**{k: "mark" for k in range(i, j + 1)}, **{k: "answer" for k in range(j + 1, j + 1 + n)}}, ptr={"start": i}), Row([repr(p)[1:-1] or "∅" for p in out], label="strings"))
        i = j + 1 + n
    assert out == exp
    return W.save()


@run
def which_release_is_newer(pid):
    a, exp = example(pid)
    x, y = a["a"].split("."), a["b"].split(".")
    W = Walk(pid, "Compare revision by revision as numbers (strip leading zeros, then compare length and digits); missing revisions count as 0.")
    n = max(len(x), len(y))
    res = 0
    for i in range(n):
        p = (x[i] if i < len(x) else "0").lstrip("0") or "0"
        q = (y[i] if i < len(y) else "0").lstrip("0") or "0"
        cmp = (len(p) > len(q)) - (len(p) < len(q)) or (p > q) - (p < q)
        W.step(f"Revision {i}: {p} vs {q}: {'equal' if cmp == 0 else ('a is newer' if cmp > 0 else 'b is newer')}.", Row(x, st={i: "active"} if i < len(x) else {}, label="a"), Row(y, st={i: "active"} if i < len(y) else {}, label="b"))
        if cmp:
            res = cmp
            break
    W.step({1: "a is newer: 1.", -1: "b is newer: -1.", 0: "Same release: 0."}[res], Vars(answer=res), result=res)
    assert res == exp
    return W.save()


# ======================================================================== pattern-matching (KMP)

def lps_table(p):
    lps = [0] * len(p)
    k = 0
    for i in range(1, len(p)):
        while k and p[i] != p[k]:
            k = lps[k - 1]
        if p[i] == p[k]:
            k += 1
        lps[i] = k
    return lps


@run
def find_every_tag(pid):
    a, exp = example(pid)
    text, tag = a["text"], a["tag"]
    W = Walk(pid, "KMP: precompute, for each prefix of the tag, its longest border (proper prefix that's also a suffix). On a mismatch or a full match, fall back to that border instead of restarting.")
    lps = lps_table(tag)
    W.step("Border lengths of the tag.", S(tag, label="tag"), Row(lps, label="border"))
    out, k = [], 0
    for i, ch in enumerate(text):
        while k and ch != tag[k]:
            k = lps[k - 1]
        if ch == tag[k]:
            k += 1
        if k == len(tag):
            out.append(i - k + 1)
            W.step(f"Full match ending at {i}: record {i - k + 1}, fall back to border {lps[k - 1]}.", S(text, st={j: "answer" for j in range(i - k + 1, i + 1)}, ptr={"i": i}), Row(out, label="starts"))
            k = lps[k - 1]
    assert out == exp
    return W.save()


@run
def repeating_unit(pid):
    a, exp = example(pid)
    s = a["s"]
    n = len(s)
    W = Walk(pid, "Build KMP's border table: border[i] is the longest proper prefix of s[0..i] that is also its suffix. The whole string's border gives the shortest period.")
    lps, k = [0] * n, 0
    for i in range(1, n):
        while k and s[i] != s[k]:
            k = lps[k - 1]
        if s[i] == s[k]:
            k += 1
        lps[i] = k
        W.step(f"border[{i}] = {k}" + (f": \"{s[:k]}\" starts and ends s[0..{i}]." if k else "."), S(s, st={**{j: "found" for j in range(k)}, **{j: "active" for j in range(i - k + 1, i + 1)}}), Row(lps[:i + 1], label="border"))
    p = n - lps[-1]
    res = p if n % p == 0 else n
    W.step(f"Period {n} − {lps[-1]} = {p}; {'it divides' if n % p == 0 else 'it does not divide'} {n}, so the answer is {res}.", S(s, st={i: "answer" for i in range(res)}), result=res)
    assert res == exp
    return W.save()



@run
def front_padding(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "The longest palindrome at the start of s is the last border of s + \"#\" + reverse(s). Build that border table, then copy the rest of s, reversed, to the front.")
    t = s + "#" + s[::-1]
    lps, k = [0] * len(t), 0
    for i in range(1, len(t)):
        while k and t[i] != t[k]:
            k = lps[k - 1]
        if t[i] == t[k]:
            k += 1
        lps[i] = k
        if i > len(s):
            W.step(f"border[{i}] = {k}.", S(t, st={**{j: "found" for j in range(k)}, i: "active"}), Row(lps[:i + 1], label="border"))
    k = lps[-1]
    W.step(f"\"{s[:k]}\" is the longest palindromic start.", S(s, st={i: "found" for i in range(k)}))
    res = s[k:][::-1] + s
    W.step(f"Add \"{s[k:][::-1]}\" to the front: \"{res}\".", S(res, st={i: "new" for i in range(len(s) - k)}), result=res)
    assert res == exp
    return W.save()



# ======================================================================== rolling-hash

@run
def distinct_windows(pid):
    a, exp = example(pid)
    s, k = a["s"], a["k"]
    W = Walk(pid, f"Slide a window of {k} letters, add each window's rolling hash to a set, and count the set.")
    seen = []
    for i in range(len(s) - k + 1):
        w = s[i:i + k]
        new = w not in seen
        if new:
            seen.append(w)
        W.step(f"\"{w}\" is {'new' if new else 'already seen'}.", S(s, st={j: "active" for j in range(i, i + k)}), Row(seen, label="distinct"))
    assert len(seen) == exp
    return W.save()


def longest_shared(W, length_ok, hi, show):
    lo = 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        ok, panels, text = show(mid)
        W.step(text, *panels)
        if ok:
            lo = mid
        else:
            hi = mid - 1
    return lo


@run
def longest_repeat(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "Binary search the length: for a length L, hash every substring of length L and see whether any hash repeats.")

    def show(L_):
        seen, hit = {}, None
        for i in range(len(s) - L_ + 1):
            w = s[i:i + L_]
            if w in seen:
                hit = (seen[w], i)
                break
            seen[w] = i
        st = {j: "answer" for j in range(hit[0], hit[0] + L_)} if hit else {}
        if hit:
            st.update({j: "found" for j in range(hit[1], hit[1] + L_) if j not in st})
        return bool(hit), [S(s, st=st)], f"Length {L_}: " + (f"\"{s[hit[0]:hit[0] + L_]}\" appears twice." if hit else "no repeat.")

    res = longest_shared(W, None, len(s) - 1, show)
    W.step(f"Longest repeat: {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


@run
def shared_tune(pid):
    a, exp = example(pid)
    x, y = a["a"], a["b"]
    W = Walk(pid, "Binary search the length: for a length L, put every L-note hash of a in a set and look for any L-note piece of b in it.")

    def show(L_):
        pieces = {x[i:i + L_]: i for i in range(len(x) - L_ + 1)}
        hit = next(((pieces[y[j:j + L_]], j) for j in range(len(y) - L_ + 1) if y[j:j + L_] in pieces), None)
        panels = [S(x, st={k: "answer" for k in range(hit[0], hit[0] + L_)} if hit else None, label="a"), S(y, st={k: "answer" for k in range(hit[1], hit[1] + L_)} if hit else None, label="b")]
        return bool(hit), panels, f"Length {L_}: " + (f"both have \"{x[hit[0]:hit[0] + L_]}\"." if hit else "nothing shared.")

    res = longest_shared(W, None, min(len(x), len(y)), show)
    W.step(f"Longest shared run: {res}.", Vars(answer=res), result=res)
    assert res == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
