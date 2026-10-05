"""Lesson: Merge two sorted sequences (Two Pointers, pattern 5)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

MERGE = {
    "python": """
        def merge_into(a, m, b, n):
            i, j, k = m - 1, n - 1, m + n - 1           #@ends
            while j >= 0:                               #@loop
                if i >= 0 and a[i] > b[j]:              #@pick
                    a[k] = a[i]                         #@pick
                    i -= 1                              #@pick
                else:                                   #@pick
                    a[k] = b[j]                         #@pick
                    j -= 1                              #@pick
                k -= 1                                  #@next
            return a                                    #@ret
    """,
    "java": """
        static int[] mergeInto(int[] a, int m, int[] b, int n) {
            int i = m - 1, j = n - 1, k = m + n - 1;    //@ends
            while (j >= 0) {                            //@loop
                if (i >= 0 && a[i] > b[j]) a[k] = a[i--];   //@pick
                else a[k] = b[j--];                     //@pick
                k--;                                    //@next
            }
            return a;                                   //@ret
        }
    """,
    "cpp": """
        vector<int>& mergeInto(vector<int>& a, int m, const vector<int>& b, int n) {
            int i = m - 1, j = n - 1, k = m + n - 1;    //@ends
            while (j >= 0) {                            //@loop
                if (i >= 0 && a[i] > b[j]) a[k] = a[i--];   //@pick
                else a[k] = b[j--];                     //@pick
                k--;                                    //@next
            }
            return a;                                   //@ret
        }
    """,
    "c": """
        void mergeInto(int* a, int m, const int* b, int n) {
            int i = m - 1, j = n - 1, k = m + n - 1;    //@ends
            while (j >= 0) {                            //@loop
                if (i >= 0 && a[i] > b[j]) a[k] = a[i--];   //@pick
                else a[k] = b[j--];                     //@pick
                k--;                                    //@next
            }
        }
    """,
}
MERGE_RUN = {
    "python": """
        print(*merge_into([1, 4, 7, 0, 0, 0], 3, [2, 5, 6], 3))
        print(*merge_into([0, 0], 0, [3, 8], 2))
        print(*merge_into([5, 9], 2, [], 0))
        print(*merge_into([2, 2, 0, 0], 2, [1, 2], 2))
    """,
    "java": """
        static void show(int[] a) {
            StringBuilder sb = new StringBuilder();
            for (int x : a) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
        }

        public static void main(String[] args) {
            show(mergeInto(new int[] {1, 4, 7, 0, 0, 0}, 3, new int[] {2, 5, 6}, 3));
            show(mergeInto(new int[] {0, 0}, 0, new int[] {3, 8}, 2));
            show(mergeInto(new int[] {5, 9}, 2, new int[] {}, 0));
            show(mergeInto(new int[] {2, 2, 0, 0}, 2, new int[] {1, 2}, 2));
        }
    """,
    "cpp": """
        void show(const vector<int>& a) {
            for (size_t i = 0; i < a.size(); i++) cout << (i ? " " : "") << a[i];
            cout << "\\n";
        }

        int main() {
            vector<int> a = {1, 4, 7, 0, 0, 0}, b = {0, 0}, c = {5, 9}, d = {2, 2, 0, 0};
            show(mergeInto(a, 3, {2, 5, 6}, 3));
            show(mergeInto(b, 0, {3, 8}, 2));
            show(mergeInto(c, 2, {}, 0));
            show(mergeInto(d, 2, {1, 2}, 2));
        }
    """,
    "c": """
        static void show(const int* a, int n) {
            for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
        }

        int main(void) {
            int a[] = {1, 4, 7, 0, 0, 0}, b[] = {0, 0}, c[] = {5, 9}, d[] = {2, 2, 0, 0};
            int a2[] = {2, 5, 6}, b2[] = {3, 8}, c2[] = {0}, d2[] = {1, 2};
            mergeInto(a, 3, a2, 3);
            mergeInto(b, 0, b2, 2);
            mergeInto(c, 2, c2, 0);
            mergeInto(d, 2, d2, 2);
            show(a, 6);
            show(b, 2);
            show(c, 2);
            show(d, 4);
            return 0;
        }
    """,
}

ONLY = {
    "python": """
        def only_in_first(a, b):
            i = j = 0                                   #@start
            out = []                                    #@start
            while i < len(a):                           #@loop
                if j < len(b) and b[j] < a[i]:          #@behind
                    j += 1                              #@behind
                elif j < len(b) and b[j] == a[i]:       #@both
                    i += 1                              #@both
                else:                                   #@keep
                    if not out or out[-1] != a[i]:      #@once
                        out.append(a[i])                #@once
                    i += 1                              #@keep
            return out                                  #@ret
    """,
    "java": """
        static int[] onlyInFirst(int[] a, int[] b) {
            int i = 0, j = 0, w = 0;                    //@start
            int[] out = new int[a.length];              //@start
            while (i < a.length) {                      //@loop
                if (j < b.length && b[j] < a[i]) j++;   //@behind
                else if (j < b.length && b[j] == a[i]) i++;     //@both
                else {                                  //@keep
                    if (w == 0 || out[w - 1] != a[i])   //@once
                        out[w++] = a[i];                //@once
                    i++;                                //@keep
                }
            }
            return Arrays.copyOf(out, w);               //@ret
        }
    """,
    "cpp": """
        vector<int> onlyInFirst(const vector<int>& a, const vector<int>& b) {
            size_t i = 0, j = 0;                        //@start
            vector<int> out;                            //@start
            while (i < a.size()) {                      //@loop
                if (j < b.size() && b[j] < a[i]) j++;   //@behind
                else if (j < b.size() && b[j] == a[i]) i++;     //@both
                else {                                  //@keep
                    if (out.empty() || out.back() != a[i])  //@once
                        out.push_back(a[i]);            //@once
                    i++;                                //@keep
                }
            }
            return out;                                 //@ret
        }
    """,
    "c": """
        int onlyInFirst(const int* a, int na, const int* b, int nb, int* out) {
            int i = 0, j = 0, w = 0;                    //@start
            while (i < na) {                            //@loop
                if (j < nb && b[j] < a[i]) j++;         //@behind
                else if (j < nb && b[j] == a[i]) i++;   //@both
                else {                                  //@keep
                    if (w == 0 || out[w - 1] != a[i])   //@once
                        out[w++] = a[i];                //@once
                    i++;                                //@keep
                }
            }
            return w;                                   //@ret
        }
    """,
}
ONLY_RUN = {
    "python": """
        print(*only_in_first([1, 2, 2, 4, 6, 7, 9], [2, 3, 6, 8]))
        print(*only_in_first([1, 1, 1], []))
        print(*only_in_first([3, 5], [1, 3, 5, 7]))
    """,
    "java": """
        static void show(int[] a) {
            StringBuilder sb = new StringBuilder();
            for (int x : a) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
        }

        public static void main(String[] args) {
            show(onlyInFirst(new int[] {1, 2, 2, 4, 6, 7, 9}, new int[] {2, 3, 6, 8}));
            show(onlyInFirst(new int[] {1, 1, 1}, new int[] {}));
            show(onlyInFirst(new int[] {3, 5}, new int[] {1, 3, 5, 7}));
        }
    """,
    "cpp": """
        void show(const vector<int>& a) {
            for (size_t i = 0; i < a.size(); i++) cout << (i ? " " : "") << a[i];
            cout << "\\n";
        }

        int main() {
            show(onlyInFirst({1, 2, 2, 4, 6, 7, 9}, {2, 3, 6, 8}));
            show(onlyInFirst({1, 1, 1}, {}));
            show(onlyInFirst({3, 5}, {1, 3, 5, 7}));
        }
    """,
    "c": """
        static void show(const int* a, int n) {
            for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
        }

        int main(void) {
            int out[8];
            int a[] = {1, 2, 2, 4, 6, 7, 9}, b[] = {2, 3, 6, 8};
            int c[] = {1, 1, 1}, d[] = {0};
            int e[] = {3, 5}, f[] = {1, 3, 5, 7};
            show(out, onlyInFirst(a, 7, b, 4, out));
            show(out, onlyInFirst(c, 3, d, 0, out));
            show(out, onlyInFirst(e, 2, f, 4, out));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

import random  # noqa: E402

merge_into = py(MERGE["python"], "merge_into")
only_in_first = py(ONLY["python"], "only_in_first")
rng = random.Random(3)
for _ in range(300):
    xa = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 6)))
    xb = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 6)))
    assert merge_into(xa + [0] * len(xb), len(xa), xb, len(xb)) == sorted(xa + xb)
    assert only_in_first(xa, xb) == sorted(set(xa) - set(xb))

# Theory walk: values both sorted lists share (each once).
CA, CB = [1, 3, 4, 7, 9, 12], [2, 3, 7, 8, 12, 15]
cw = Steps(f"Values that appear in both `{CA}` and `{CB}`. Both lists are sorted, so the smaller front value can be thrown away.")
i = j = 0
common = []


def c_panels(ai=None, bj=None, hit=False):
    sa = {k: "dim" for k in range(i)}
    sb = {k: "dim" for k in range(j)}
    if ai is not None:
        sa[ai] = "answer" if hit else "active"
    if bj is not None:
        sb[bj] = "answer" if hit else "active"
    return (Row(CA, st=sa, ptr={"i": i if i < len(CA) else None}, slots=True, label="a"),
            Row(CB, st=sb, ptr={"j": j if j < len(CB) else None}, slots=True, label="b"),
            M({"common": " ".join(map(str, common)) or "none yet"}))


cw.step("`i` and `j` start at the front of each list.", *c_panels(0, 0))
while i < len(CA) and j < len(CB):
    x, y = CA[i], CB[j]
    if x == y:
        common.append(x)
        oi, oj = i, j
        i, j = i + 1, j + 1
        cw.step(f"{x} = {y}: in both lists. Record it and move both pointers.", *c_panels(oi, oj, hit=True))
    elif x < y:
        oi = i
        i += 1
        cw.step(f"{x} < {y}. Everything left in `b` is at least {y}, so nothing there can equal {x}. Drop {x}: move `i`.", *c_panels(oi, j))
    else:
        oj = j
        j += 1
        cw.step(f"{y} < {x}. Everything left in `a` is at least {x}, so {y} has no match. Move `j`.", *c_panels(i, oj))
cw.steps[-1]["text"] += f" {'`a`' if i >= len(CA) else '`b`'} has run out, so nothing else can be common: {common}."
assert common == sorted(set(CA) & set(CB))
C_LEGEND = {"active": "the two front values being compared", "answer": "in both lists", "dim": "dropped"}

# Trace walk: merge into the first array from the back.
TA, TM, TB = [1, 4, 7, 0, 0, 0], 3, [2, 5, 6]
tw = Steps(f"`merge_into([1, 4, 7, _, _, _], 3, {TB}, 3)`. The three blanks at the end of `a` are free space.")
a, i, j, k = list(TA), TM - 1, len(TB) - 1, TM + len(TB) - 1


def show_a():
    return [None if i < x <= k else a[x] for x in range(len(a))]


def t_panels(cmp=False):
    sa = {x: "found" for x in range(k + 1, len(a))}
    sb = {x: "dim" for x in range(j + 1, len(TB))}
    if cmp:
        if i >= 0:
            sa[i] = "active"
        if j >= 0:
            sb[j] = "active"
    return (Row(show_a(), st=sa, ptr={"i": i if i >= 0 else None, "k": k if k >= 0 else None}, slots=True, label="a"),
            Row(TB, st=sb, ptr={"j": j if j >= 0 else None}, slots=True, label="b"))


tw.step("`i` is the last real value of `a`, `j` the last of `b`, and `k` the last slot of `a`. The biggest of everything goes into slot `k`.", *t_panels(cmp=True))
while j >= 0:
    if i >= 0 and a[i] > TB[j]:
        msg = f"{a[i]} > {TB[j]}: {a[i]} is the biggest left. Write it into slot {k}. Its old slot becomes free space."
        a[k] = a[i]
        i -= 1
    else:
        msg = (f"{TB[j]} ≥ {a[i]}: take {TB[j]} from `b` and write it into slot {k}." if i >= 0
               else f"`a` has nothing left to compare. Copy {TB[j]} from `b` into slot {k}.")
        a[k] = TB[j]
        j -= 1
    k -= 1
    tw.step(msg, *t_panels(cmp=j >= 0))
tw.steps[-1]["text"] += f" `b` is used up. Whatever is left at the front of `a` was already in place: {a}."
assert a == sorted(TA[:TM] + TB)
T_LEGEND = {"found": "placed for good", "active": "the two values being compared", "dim": "taken from `b`"}

# Example: count pairs (x from a, y from b) with x < y, one pointer per list.
PA, PB = [1, 4, 5, 9], [2, 5, 6, 10]
p_rows, ii, tot = [], 0, 0
for y in PB:
    while ii < len(PA) and PA[ii] < y:
        ii += 1
    tot += ii
    p_rows.append((str(y), f"{ii} ({', '.join(map(str, PA[:ii])) or 'none'})", str(tot)))
assert tot == sum(1 for x in PA for y in PB if x < y)

N = 10**5

lesson(
    "two-pointers",
    "merge-sorted",
    """
    When two inputs are each sorted, one pointer per input is enough to merge them, find what they share, or find
    what one has and the other doesn't. At every step compare the two front values; the smaller one can be settled
    right away, because nothing still to come in the other input is smaller.
    """,
    [
        ("idea", "The idea", [
            """
            Two teachers each hand you a stack of exam papers, each stack already in alphabetical order by surname. You
            need one stack in order. You don't shuffle them together and start again. You look at the top paper of each
            stack, take whichever name comes first, and put it on your pile. Then look at the two tops again. Each look
            places one paper for good, because the paper you took comes before everything left in *both* stacks.

            Every two-list question in this pattern works by that same rule. Asking "which names are on both lists?"
            you compare the tops: if they match, note it and take both; if not, the one that comes first can't be on the
            other list (everything there comes later), so take just that one.
            """,
            fig(Row(CA, slots=True, label="a"), Row(CB, slots=True, label="b"), Row(sorted(CA + CB), slots=True, label="merged"),
                caption="One pass, one comparison per value placed. Neither list is ever searched."),
            key("""
            One pointer per sorted input. Compare the values they point at, act on the smaller one (take it, count it,
            or drop it), and move only that pointer. On a tie, act on both. Stop when an input runs out, then deal
            with what's left of the other. O(m + n).
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            Two (or a few) inputs that are each sorted: arrays, linked lists, lists of intervals sorted by start, sorted
            ID lists, events by time. The question merges them or compares them.
            """,
            table(
                ["The problem says…", "on each comparison"],
                ["merge into one sorted list", "write the smaller, move its pointer"],
                ["merge into the first array, which has room at the end", "same, but from the back"],
                ["values in both (intersection)", "equal: record, move both; else move the smaller"],
                ["values in one but not the other", "smaller in the first list: keep it; equal: drop it"],
                ["the closest pair, one from each list", "check the difference, move the smaller"],
                ["overlaps between two sorted interval lists", "record the overlap, move the interval that ends first"],
            ),
            """
            Not a fit:

            - The inputs aren't sorted and you can't sort them. A hash set handles membership questions in O(m + n)
              on average.
            - One list is tiny and the other is huge. Binary searching the big one for each small value is
              O(m log n), which beats O(m + n) when `m` is much smaller than `n`.
            - Many lists at once. Comparing `k` fronts every step is O(k) per value; a heap brings it down to O(log k)
              (Heaps topic).
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### The smaller front value can be settled

            Say the two front values are `a[i]` and `b[j]`, and `a[i] < b[j]`. Every value left in `b` is at least `b[j]`,
            so it's bigger than `a[i]` too. That means:

            - in a merge, `a[i]` comes before everything that's left, so it can be written now;
            - in an intersection, `a[i]` can't equal anything left in `b`, so it can be dropped now;
            - in a difference (`a` minus `b`), `a[i]` definitely isn't in `b`, so it can be kept now.

            Each comparison settles at least one value, so the walk takes at most `m + n` steps.
            """,
            walk(cw, legend=C_LEGEND),
            """
            ### Ties

            What to do on equal values depends on the question. A merge takes one of them (taking from the first list
            keeps the merge stable: equal values keep their original list order). An intersection records the value
            and moves both. A difference drops the value from the first list, but leaves the pointer into the second
            list where it is, in case the first list has another copy of the same value.

            ### The leftover tail

            When one input runs out, the rest of the other is untouched. In a merge it's already sorted and bigger than
            everything placed, so copy it as it is. In an intersection it can be ignored. In a difference, the leftover
            part of the first list is all kept.

            ### Merging into the space at the end

            If the first array has empty slots at its end, big enough for the second array, you can merge without a
            third array. Going forwards would overwrite values of `a` before they're read. Going *backwards* is safe:
            write the biggest value into the last slot, then the next biggest, and so on.

            > The write position is always `k = i + j + 1`.

            While `b` still has values (`j ≥ 0`), that makes `k > i`, so the slot being written is never a value of
            `a` that hasn't been read. And once `b` is used up, what's left of `a` is already sitting in the right place,
            so the loop can stop there.
            """,
        ]),
        ("template", "The template", [
            """
            `a` holds `m` sorted values followed by `n` free slots. `b` holds `n` sorted values. Merge `b` into `a` so that
            `a` ends up fully sorted, using no other array.
            """,
            code(
                "Merge into the free space at the end",
                MERGE,
                [
                    ("ends", "`i` is the last real value of `a`, `j` the last value of `b`, `k` the last slot of `a`.",
                     {"c": "C merges into the caller's array and returns nothing."}),
                    ("loop", "Keep going while `b` has values. When `b` runs out, the rest of `a` is already in place."),
                    ("pick", "Write the bigger of the two into slot `k`. On a tie, `b`'s value goes later, so `a`'s copy "
                             "stays before it, which keeps the merge stable. If `a` is used up (`i < 0`), take from `b`.",
                     {"java": "`a[i--]` reads the value, then moves `i` back.",
                      "cpp": "`a[i--]` reads the value, then moves `i` back.",
                      "c": "`a[i--]` reads the value, then moves `i` back."}),
                    ("next", "One slot filled for good; the next one to fill is to its left."),
                    ("ret", "The merged array."),
                ],
                MERGE_RUN,
                "merge_into([1, 4, 7, 0, 0, 0], 3, [2, 5, 6], 3); ([0, 0], 0, [3, 8], 2); ([5, 9], 2, [], 0); ([2, 2, 0, 0], 2, [1, 2], 2)",
            ),
            """
            When `a` has no real values (`m = 0`), everything comes from `b`. When `b` is empty, the loop doesn't run
            at all.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "The first example, one slot per step, from the right end:",
            walk(tw, legend=T_LEGEND),
            """
            On paper, write `a` with its blanks and `b` underneath, and fill the blanks right to left. If you ever need
            a value that you've already overwritten, you're going the wrong way.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Counting pairs across two lists

            How many pairs `(x, y)` with `x` from `{PA}` and `y` from `{PB}` have `x < y`? Walk `b` in order and keep a
            pointer into `a` that marks how many of its values are below the current `y`. As `y` grows, that pointer only
            moves forward, so the whole count is one pass over each list.
            """,
            table(["y", "values of a below it", "pairs so far"], *p_rows),
            f"""
            {tot} pairs, with each list read once.

            ### Two lists of intervals

            Each list holds non-overlapping intervals sorted by start, and you want every overlap between the two lists.
            Compare the current interval of each list: their overlap (if any) runs from the larger start to the smaller
            end. Then move past whichever interval *ends* first, since it can't overlap anything further along the
            other list. Same rule, a different notion of "smaller".

            ### Linked lists

            With linked lists, merging doesn't need any free space: relink the nodes. A dummy head node avoids a
            special case for the first node, and when one list runs out, the rest of the other is attached in one step.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### What one list has and the other doesn't

            Keep each value of `a` that never appears in `b`, once each. The pointer into `b` moves past values smaller
            than `a[i]`. If `b[j]` equals `a[i]`, the value is in both lists, so drop `a[i]` (but keep `j` where it is:
            `a` may have another copy). Otherwise `a[i]` isn't in `b`.
            """,
            code(
                "Values in the first sorted list but not the second",
                ONLY,
                [
                    ("start", "A pointer into each list, and the answer so far.",
                     {"java": "`out` is as long as `a`, the most it could need. `w` counts what's used.",
                      "c": "The caller provides `out`; `w` counts what's written."}),
                    ("loop", "Every value of `a` gets decided."),
                    ("behind", "`b[j]` is smaller than `a[i]`, so it can't match `a[i]` or anything after it. Move past it."),
                    ("both", "`a[i]` is in `b`. Drop it. `j` stays, in case the next value of `a` is the same."),
                    ("keep", "`b` has run out, or its front value is bigger: `a[i]` isn't in `b`."),
                    ("once", "Skip it if it's a repeat of the value just kept, so each answer appears once."),
                    ("ret", "The values only `a` has, in sorted order.", {"c": "C returns how many there are."}),
                ],
                ONLY_RUN,
                "only_in_first([1, 2, 2, 4, 6, 7, 9], [2, 3, 6, 8]); ([1, 1, 1], []); ([3, 5], [1, 3, 5, 7])",
            ),
            """
            The last run has nothing left over, so it prints an empty line.

            ### Union, intersection and difference

            The three set operations on sorted lists all share this loop. Union writes the smaller value (and on a tie,
            one copy). Intersection writes only on a tie. Difference writes from the first list when it's smaller.
            Decide once whether repeats should be kept, as in a multiset, or collapsed.

            ### Closest across two lists

            For the smallest `|x - y|` with one value from each list, check the difference of the two front values at
            every step, then move the pointer at the smaller value. Moving the larger one could only widen the gap.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            Each step moves at least one pointer, and the pointers only move forward (or, in the template, backward), so
            the walk is O(m + n). Merging into the free space uses O(1) extra memory. Building a new output takes
            O(m + n) for the output itself.

            Sorting the two lists together from scratch would be O((m + n) log(m + n)), and checking every pair for an
            intersection would be O(m · n): for two lists of {N:,} that's {N * N:,} comparisons.
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Concatenate and sort", "O((m + n) log(m + n))", "depends on the sort"],
                ["Check every pair", "O(m · n)", "O(1)"],
                ["Hash set of one list", "O(m + n) on average", "O(m)"],
                ["Binary search the longer list", "O(m log n)", "O(1)"],
                ["Walk both together", "O(m + n)", "O(1) besides the output"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `heapq.merge(a, b)` merges sorted iterables lazily. `sorted(a + b)` is shorter but O((m + n) log(m + n)).
            Slicing `a[i:]` to copy a leftover tail is fine; it's O(length).

            ### Java

            `System.arraycopy` copies a leftover tail in one call. For linked lists, build onto a dummy `ListNode`.

            ### C++

            `std::merge`, `std::set_intersection`, `std::set_difference` and `std::set_union` all do this walk on sorted
            ranges and write to an output iterator. `std::inplace_merge` merges two adjacent sorted ranges of one
            container.

            ### C

            Pass lengths explicitly, and make sure the output buffer is large enough: `m + n` for a merge or union,
            `min(m, n)` for an intersection, `m` for a difference.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Merging into `a` from the front, which overwrites values before they're read.
            - Forgetting the leftover tail of one list after the other runs out.
            - Stopping the in-place merge when `a` runs out instead of when `b` does.
            - On a tie in a difference, moving the pointer into the second list too early, so a repeated value in the
              first list slips through.
            - Not deciding whether repeats count once or every time.
            - Using it on unsorted input. The "smaller one can be settled" step depends on sorted order.
            - Empty lists on either side.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why can the smaller of the two front values always be settled?",
                 "Everything left in the other list is at least as big as that list's front value, which is bigger than the smaller one. So nothing still to come can come before it or equal it."),
                ("Why is merging into the end of `a` done backwards?",
                 "The free space is at the end. Writing the biggest values first into the last slots never touches an unread value of `a`, since the write position stays ahead of `i`."),
                ("In `merge_into`, why can the loop stop as soon as `b` runs out?",
                 "Whatever is left of `a` is already at the front of `a`, sorted, and smaller than everything placed after it. It's in its final position."),
                ("Intersection of [1, 2, 2, 3] and [2, 2, 4], keeping repeats: what comes out?",
                 "[2, 2]. 1 is dropped, the two 2s match one by one, then 3 < 4 is dropped and the first list runs out."),
                ("When does binary search beat walking both lists?",
                 "When one list is much shorter. Searching the long list for each of m short-list values costs O(m log n), less than O(m + n) when m is small."),
            ),
        ]),
    ],
)
