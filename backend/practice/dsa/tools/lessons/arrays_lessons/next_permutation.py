"""Lesson: Next permutation (Arrays & Hashing, pattern 14)."""
from itertools import permutations

from lesson import Bars, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

NEXT = {
    "python": """
        def next_permutation(a):
            i = len(a) - 2                          #@pivot
            while i >= 0 and a[i] >= a[i + 1]:      #@pivot
                i -= 1                              #@pivot
            if i < 0:                               #@last
                return False                        #@last
            j = len(a) - 1                          #@succ
            while a[j] <= a[i]:                     #@succ
                j -= 1                              #@succ
            a[i], a[j] = a[j], a[i]                 #@swap
            lo, hi = i + 1, len(a) - 1              #@rev
            while lo < hi:                          #@rev
                a[lo], a[hi] = a[hi], a[lo]         #@rev
                lo, hi = lo + 1, hi - 1             #@rev
            return True                             #@ret
    """,
    "java": """
        static boolean nextPermutation(int[] a) {
            int i = a.length - 2;                   //@pivot
            while (i >= 0 && a[i] >= a[i + 1]) i--; //@pivot
            if (i < 0) return false;                //@last
            int j = a.length - 1;                   //@succ
            while (a[j] <= a[i]) j--;               //@succ
            int t = a[i]; a[i] = a[j]; a[j] = t;    //@swap
            for (int lo = i + 1, hi = a.length - 1; lo < hi; lo++, hi--) {  //@rev
                t = a[lo]; a[lo] = a[hi]; a[hi] = t;    //@rev
            }
            return true;                            //@ret
        }
    """,
    "cpp": """
        bool nextPermutation(vector<int>& a) {
            int i = (int)a.size() - 2;              //@pivot
            while (i >= 0 && a[i] >= a[i + 1]) i--; //@pivot
            if (i < 0) return false;                //@last
            int j = (int)a.size() - 1;              //@succ
            while (a[j] <= a[i]) j--;               //@succ
            swap(a[i], a[j]);                       //@swap
            reverse(a.begin() + i + 1, a.end());    //@rev
            return true;                            //@ret
        }
    """,
    "c": """
        bool nextPermutation(int* a, int n) {
            int i = n - 2;                          //@pivot
            while (i >= 0 && a[i] >= a[i + 1]) i--; //@pivot
            if (i < 0) return false;                //@last
            int j = n - 1;                          //@succ
            while (a[j] <= a[i]) j--;               //@succ
            int t = a[i]; a[i] = a[j]; a[j] = t;    //@swap
            for (int lo = i + 1, hi = n - 1; lo < hi; lo++, hi--) {     //@rev
                t = a[lo]; a[lo] = a[hi]; a[hi] = t;    //@rev
            }
            return true;                            //@ret
        }
    """,
}
NEXT_RUN = {
    "python": """
        for a in ([1, 3, 5, 4, 2], [3, 2, 1], [1, 1, 2]):
            ok = next_permutation(a)
            print("true" if ok else "false", *a)
    """,
    "java": """
        public static void main(String[] args) {
            for (int[] a : new int[][] {{1, 3, 5, 4, 2}, {3, 2, 1}, {1, 1, 2}}) {
                StringBuilder sb = new StringBuilder(String.valueOf(nextPermutation(a)));
                for (int x : a) sb.append(" ").append(x);
                System.out.println(sb);
            }
        }
    """,
    "cpp": """
        int main() {
            vector<vector<int>> cases = {{1, 3, 5, 4, 2}, {3, 2, 1}, {1, 1, 2}};
            for (auto& a : cases) {
                cout << (nextPermutation(a) ? "true" : "false");
                for (int x : a) cout << " " << x;
                cout << "\\n";
            }
        }
    """,
    "c": """
        static void run(int* a, int n) {
            printf("%s", nextPermutation(a, n) ? "true" : "false");
            for (int i = 0; i < n; i++) printf(" %d", a[i]);
            printf("\\n");
        }

        int main(void) {
            int a[] = {1, 3, 5, 4, 2}, b[] = {3, 2, 1}, c[] = {1, 1, 2};
            run(a, 5);
            run(b, 3);
            run(c, 3);
            return 0;
        }
    """,
}

ALL = {
    "python": """
        def next_permutation(a):
            i = len(a) - 2                          #@np
            while i >= 0 and a[i] >= a[i + 1]:      #@np
                i -= 1                              #@np
            if i < 0:                               #@np
                return False                        #@np
            j = len(a) - 1                          #@np
            while a[j] <= a[i]:                     #@np
                j -= 1                              #@np
            a[i], a[j] = a[j], a[i]                 #@np
            a[i + 1:] = reversed(a[i + 1:])         #@np
            return True                             #@np


        def all_arrangements(a):
            a = sorted(a)                           #@sort
            out = [list(a)]                         #@first
            while next_permutation(a):              #@loop
                out.append(list(a))                 #@loop
            return out                              #@ret
    """,
    "java": """
        static boolean nextPermutation(int[] a) {
            int i = a.length - 2;                   //@np
            while (i >= 0 && a[i] >= a[i + 1]) i--; //@np
            if (i < 0) return false;                //@np
            int j = a.length - 1;                   //@np
            while (a[j] <= a[i]) j--;               //@np
            int t = a[i]; a[i] = a[j]; a[j] = t;    //@np
            for (int lo = i + 1, hi = a.length - 1; lo < hi; lo++, hi--) {  //@np
                t = a[lo]; a[lo] = a[hi]; a[hi] = t;    //@np
            }
            return true;                            //@np
        }

        static List<int[]> allArrangements(int[] input) {
            int[] a = input.clone();                //@sort
            Arrays.sort(a);                         //@sort
            List<int[]> out = new ArrayList<>();    //@first
            out.add(a.clone());                     //@first
            while (nextPermutation(a)) out.add(a.clone());  //@loop
            return out;                             //@ret
        }
    """,
    "cpp": """
        vector<vector<int>> allArrangements(vector<int> a) {
            sort(a.begin(), a.end());               //@sort
            vector<vector<int>> out = {a};          //@first
            while (next_permutation(a.begin(), a.end())) out.push_back(a);  //@loop
            return out;                             //@ret
        }
    """,
    "c": """
        static bool nextPermutation(int* a, int n) {
            int i = n - 2;                          //@np
            while (i >= 0 && a[i] >= a[i + 1]) i--; //@np
            if (i < 0) return false;                //@np
            int j = n - 1;                          //@np
            while (a[j] <= a[i]) j--;               //@np
            int t = a[i]; a[i] = a[j]; a[j] = t;    //@np
            for (int lo = i + 1, hi = n - 1; lo < hi; lo++, hi--) {     //@np
                t = a[lo]; a[lo] = a[hi]; a[hi] = t;    //@np
            }
            return true;                            //@np
        }

        static int cmp_int(const void* x, const void* y) {
            int p = *(const int*)x, q = *(const int*)y;     //@sort
            return (p > q) - (p < q);               //@sort
        }

        // Calls visit(a, n) for every distinct arrangement, in order; returns how many.
        int allArrangements(int* a, int n, void (*visit)(const int*, int)) {
            qsort(a, n, sizeof(int), cmp_int);      //@sort
            int count = 0;                          //@first
            do {                                    //@loop
                if (visit) visit(a, n);             //@loop
                count++;                            //@loop
            } while (nextPermutation(a, n));        //@loop
            return count;                           //@ret
        }
    """,
}
ALL_RUN = {
    "python": """
        for p in all_arrangements([2, 1, 1]):
            print(*p)
        print(len(all_arrangements([3, 2, 2, 1])))
    """,
    "java": """
        public static void main(String[] args) {
            for (int[] p : allArrangements(new int[] {2, 1, 1})) {
                StringBuilder sb = new StringBuilder();
                for (int x : p) sb.append(sb.length() > 0 ? " " : "").append(x);
                System.out.println(sb);
            }
            System.out.println(allArrangements(new int[] {3, 2, 2, 1}).size());
        }
    """,
    "cpp": """
        int main() {
            for (auto& p : allArrangements({2, 1, 1})) {
                for (size_t i = 0; i < p.size(); i++) cout << (i ? " " : "") << p[i];
                cout << "\\n";
            }
            cout << allArrangements({3, 2, 2, 1}).size() << "\\n";
        }
    """,
    "c": """
        static void print_it(const int* a, int n) {
            for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
        }

        int main(void) {
            int a[] = {2, 1, 1}, b[] = {3, 2, 2, 1};
            allArrangements(a, 3, print_it);
            printf("%d\\n", allArrangements(b, 4, NULL));
            return 0;
        }
    """,
}

KTH = {
    "python": """
        def kth_permutation(n, k):
            fact = [1] * (n + 1)                    #@fact
            for i in range(1, n + 1):               #@fact
                fact[i] = fact[i - 1] * i           #@fact
            left = list(range(1, n + 1))            #@pool
            k -= 1                                  #@zero
            out = []                                #@zero
            for slots in range(n, 0, -1):           #@each
                block = fact[slots - 1]             #@block
                out.append(left.pop(k // block))    #@pick
                k %= block                          #@rest
            return out                              #@ret
    """,
    "java": """
        static int[] kthPermutation(int n, long k) {
            long[] fact = new long[n + 1];          //@fact
            fact[0] = 1;                            //@fact
            for (int i = 1; i <= n; i++) fact[i] = fact[i - 1] * i;    //@fact
            List<Integer> left = new ArrayList<>(); //@pool
            for (int v = 1; v <= n; v++) left.add(v);   //@pool
            k--;                                    //@zero
            int[] out = new int[n];                 //@zero
            for (int slots = n; slots >= 1; slots--) {  //@each
                long block = fact[slots - 1];       //@block
                out[n - slots] = left.remove((int) (k / block));   //@pick
                k %= block;                         //@rest
            }
            return out;                             //@ret
        }
    """,
    "cpp": """
        vector<int> kthPermutation(int n, long long k) {
            vector<long long> fact(n + 1, 1);       //@fact
            for (int i = 1; i <= n; i++) fact[i] = fact[i - 1] * i;    //@fact
            vector<int> left(n);                    //@pool
            iota(left.begin(), left.end(), 1);      //@pool
            k--;                                    //@zero
            vector<int> out;                        //@zero
            for (int slots = n; slots >= 1; slots--) {  //@each
                long long block = fact[slots - 1];  //@block
                auto it = left.begin() + k / block; //@pick
                out.push_back(*it);                 //@pick
                left.erase(it);                     //@pick
                k %= block;                         //@rest
            }
            return out;                             //@ret
        }
    """,
    "c": """
        void kthPermutation(int n, long long k, int* out) {
            long long fact[21] = {1};               //@fact
            for (int i = 1; i <= n; i++) fact[i] = fact[i - 1] * i;    //@fact
            int left[20];                           //@pool
            for (int v = 0; v < n; v++) left[v] = v + 1;    //@pool
            k--;                                    //@zero
            for (int slots = n; slots >= 1; slots--) {  //@each
                long long block = fact[slots - 1];  //@block
                int idx = (int)(k / block);         //@pick
                out[n - slots] = left[idx];         //@pick
                for (int t = idx; t < slots - 1; t++) left[t] = left[t + 1];   //@pick
                k %= block;                         //@rest
            }
        }
    """,
}
KTH_RUN = {
    "python": """
        print(*kth_permutation(4, 9))
        print(*kth_permutation(3, 1))
        print(*kth_permutation(3, 6))
    """,
    "java": """
        static void show(int[] a) {
            StringBuilder sb = new StringBuilder();
            for (int x : a) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
        }

        public static void main(String[] args) {
            show(kthPermutation(4, 9));
            show(kthPermutation(3, 1));
            show(kthPermutation(3, 6));
        }
    """,
    "cpp": """
        void show(const vector<int>& a) {
            for (size_t i = 0; i < a.size(); i++) cout << (i ? " " : "") << a[i];
            cout << "\\n";
        }

        int main() {
            show(kthPermutation(4, 9));
            show(kthPermutation(3, 1));
            show(kthPermutation(3, 6));
        }
    """,
    "c": """
        static void show(const int* a, int n) {
            for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
        }

        int main(void) {
            int out[20];
            kthPermutation(4, 9, out);
            show(out, 4);
            kthPermutation(3, 1, out);
            show(out, 3);
            kthPermutation(3, 6, out);
            show(out, 3);
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

next_permutation = py(NEXT["python"], "next_permutation")
all_arrangements = py(ALL["python"], "all_arrangements")
kth_permutation = py(KTH["python"], "kth_permutation")

DEMO = [1, 3, 5, 4, 2]
DOUT = list(DEMO)
assert next_permutation(DOUT) and DOUT == [1, 4, 2, 3, 5]
assert list(min(p for p in permutations(DEMO) if list(p) > DEMO)) == DOUT
TOP = max(DEMO)
Q4 = [2, 4, 3, 1]
assert next_permutation(Q4) and Q4 == [3, 1, 2, 4]

# The step-by-step walk.
nw = Steps(f"`next_permutation({DEMO})`. Find the pivot, swap it with its successor, then reverse the suffix.")
a = list(DEMO)
nw.step("Drawn as heights. We want the arrangement that comes right after this one in dictionary order: bigger, but by as little as possible.",
        Bars(a, top=TOP), Row(a, slots=True))
i = len(a) - 2
while i >= 0 and a[i] >= a[i + 1]:
    nw.step(f"Walk left from the end. a[{i}] = {a[i]} ≥ a[{i + 1}] = {a[i + 1]}: still going downhill towards the end, so keep walking.",
            Bars(a, st={k: "mark" for k in range(i, len(a))}, top=TOP), Row(a, st={k: "mark" for k in range(i + 1, len(a))}, ptr={"i": i}, slots=True))
    i -= 1
PIV = i
nw.step(f"a[{i}] = {a[i]} < a[{i + 1}] = {a[i + 1]}. Found the pivot at index {i}. Everything right of it ({', '.join(map(str, a[i + 1:]))}) slopes downhill, so that part is already as big as it can be on its own.",
        Bars(a, st={**{k: "mark" for k in range(i + 1, len(a))}, i: "active"}, top=TOP), Row(a, st={**{k: "mark" for k in range(i + 1, len(a))}, i: "active"}, ptr={"pivot": i}, slots=True))
j = len(a) - 1
while a[j] <= a[i]:
    nw.step(f"Find the pivot's successor: walk left from the end. a[{j}] = {a[j]} isn't bigger than {a[i]}.",
            Bars(a, st={i: "active", j: "dim"}, top=TOP), Row(a, st={i: "active", j: "dim"}, ptr={"pivot": i, "j": j}, slots=True))
    j -= 1
SUCC = j
nw.step(f"a[{j}] = {a[j]} is the first value bigger than {a[i]} from the right, so it's the smallest one in the suffix that's bigger than {a[i]}.",
        Bars(a, st={i: "active", j: "found"}, top=TOP), Row(a, st={i: "active", j: "found"}, ptr={"pivot": i, "j": j}, slots=True))
a[i], a[j] = a[j], a[i]
nw.step(f"Swap them. Index {i} now holds {a[i]}: the smallest step up at that position. The suffix is still downhill.",
        Bars(a, st={i: "answer", **{k: "mark" for k in range(i + 1, len(a))}}, top=TOP), Row(a, st={i: "answer", j: "new"}, slots=True))
a[i + 1:] = a[i + 1:][::-1]
nw.step(f"Reverse the suffix so it runs uphill: the smallest it can be. Result: {' '.join(map(str, a))}.",
        Bars(a, st={i: "answer", **{k: "found" for k in range(i + 1, len(a))}}, top=TOP), Row(a, st={i: "answer", **{k: "found" for k in range(i + 1, len(a))}}, slots=True),
        result=" ".join(map(str, a)))
assert a == DOUT

# Every permutation of [1, 2, 3], with the pivot and swap for each step.
ORDER_ROWS = []
a = [1, 2, 3]
while True:
    b = list(a)
    i = len(b) - 2
    while i >= 0 and b[i] >= b[i + 1]:
        i -= 1
    if i < 0:
        ORDER_ROWS.append((" ".join(map(str, a)), "none: it's the last", "", ""))
        break
    j = len(b) - 1
    while b[j] <= b[i]:
        j -= 1
    nxt = list(a)
    next_permutation(nxt)
    ORDER_ROWS.append((" ".join(map(str, a)), f"index {i} ({a[i]})", f"{a[i]} ↔ {a[j]}", " ".join(map(str, nxt))))
    a = nxt
assert len(ORDER_ROWS) == 6

DUP_ALL = all_arrangements([2, 1, 1])
assert [list(p) for p in DUP_ALL] == [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
assert len(all_arrangements([3, 2, 2, 1])) == 12

# Letters example.
WORD = "dkhc"
wl = list(WORD)
assert next_permutation(wl)
WORD_NEXT = "".join(wl)
assert WORD_NEXT == "hcdk"

# k-th permutation walk.
KN, KK = 4, 9
KOUT = kth_permutation(KN, KK)
allp = sorted(permutations(range(1, KN + 1)))
assert list(allp[KK - 1]) == KOUT
kw = Steps(f"`kth_permutation({KN}, {KK})`: the {KK}th arrangement of 1 to {KN} in dictionary order, without listing the first {KK - 1}.")
fact = [1] * (KN + 1)
for t in range(1, KN + 1):
    fact[t] = fact[t - 1] * t
left, k, out = list(range(1, KN + 1)), KK - 1, []
kw.step(f"Count from 0: we want the arrangement with {KK - 1} arrangements before it. There are {fact[KN]} in all.", Row(left, label="still to place"), M({"before it": k}))
for slots in range(KN, 0, -1):
    block = fact[slots - 1]
    idx = k // block
    pick = left[idx]
    sizes = f"each choice of the next value leads to a block of {slots - 1}! = {block} arrangement{'s' if block > 1 else ''}"
    msg = (f"{slots} values left, so {sizes}. {k} before it means skipping {idx} whole block{'s' if idx != 1 else ''}: the next value is the one at position {idx} of {left}, which is {pick}."
           if slots > 1 else f"One value left: {pick}.")
    left.pop(idx)
    out.append(pick)
    k %= block
    kw.step(msg + (f" {k} still to skip inside that block." if slots > 1 else ""), Row(left if left else [], label="still to place"),
            Row(out, st={len(out) - 1: "new"}, label="placed"), M({"before it": k}))
kw.steps[-1]["text"] += f" The {KK}th arrangement is {' '.join(map(str, out))}."
assert out == KOUT

# Ranking: the inverse of kth.
RP = KOUT
rank_rows, rank, pool = [], 0, sorted(RP)
for pos, v in enumerate(RP):
    smaller = pool.index(v)
    blocksz = fact[len(RP) - pos - 1]
    rank += smaller * blocksz
    rank_rows.append((str(v), f"{smaller} smaller still unused", f"{smaller} × {blocksz} = {smaller * blocksz}"))
    pool.remove(v)
assert rank + 1 == KK

lesson(
    "arrays-hashing",
    "next-permutation",
    """
    List every arrangement of some values in dictionary order. Which one comes right after the one you have? Find the
    rightmost place where the values go up, bump that value to the next bigger one from its right, and put everything
    after it in increasing order. Three short scans, O(n), in place.
    """,
    [
        ("idea", "The idea", [
            """
            Think of a car's odometer, but one that can only use the digits it already has. It reads `1 3 5 4 2` and you
            want the next reading: the smallest arrangement of these digits that's bigger than the current one.

            To make a number a little bigger, you change it as far to the right as you can. Changing the last digits
            is a small step; changing the first digit is a huge one. So look at the end first. `4 2` can't be made bigger
            on its own: it already runs downhill, which is its biggest arrangement. Neither can `5 4 2`. But `3 5 4 2`
            can, because the 3 has something bigger to its right.

            So the 3 has to go up, by as little as possible: the smallest value to its right that beats it is 4. Swap
            them to get `1 4 _ _ _`, with 5, 3, 2 left over. Everything after the 4 should now be as *small* as
            possible, so put it in increasing order: `1 4 2 3 5`.
            """,
            fig(Bars(DEMO, st={**{k: "mark" for k in range(PIV + 1, len(DEMO))}, PIV: "active", SUCC: "found"}, label="before: a downhill tail", top=TOP),
                Bars(DOUT, st={PIV: "answer", **{k: "found" for k in range(PIV + 1, len(DEMO))}}, label="after: pivot bumped, tail uphill", top=TOP),
                caption="The tail that slopes downhill is already at its maximum. The value just before it (the pivot) is the one to bump."),
            key("""
            From the right, find the first `i` with `a[i] < a[i + 1]` (the pivot). If there's none, this is the last
            arrangement. Otherwise, from the right, find the first `a[j] > a[i]`, swap `a[i]` and `a[j]`, and reverse
            everything after `i`.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            "The next arrangement", "the next bigger number with the same digits", "the next string in dictionary order
            using these letters", "list all permutations in order without repeats", "the k-th permutation". Anything that
            treats arrangements as a sorted list and asks you to move one step (or `k` steps) along it.

            Signs it's this rather than backtracking: you're asked for *one* neighbouring arrangement, or the
            arrangements in order, and the input can be long (backtracking through `n!` arrangements is hopeless beyond
            about 10 values, while one step here is O(n)).

            Not a fit:

            - Arrangements with a rule attached (no two equal neighbours, must stay a palindrome, …). The basic step
              ignores rules; you'll need to adapt it to the structure (for example, work on half of the values) or
              search.
            - "All subsets" or "all combinations": different objects. Backtracking or bitmasks.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Dictionary order

            Arrangements compare like words: look at the first position where they differ, and the smaller value there
            wins. `1 3 5 4 2` comes before `1 4 2 3 5` because at index 1, 3 < 4, and nothing after that matters. So the
            *next* arrangement is the smallest one that's bigger.

            Here are all six arrangements of `[1, 2, 3]`, each with the pivot and the swap that produced the next one:
            """,
            table(["arrangement", "pivot", "swap", "next"], *ORDER_ROWS),
            """
            ### A downhill tail is already at its maximum

            Call the longest stretch at the end that never goes up (each value ≥ the next) the **tail**. Any arrangement
            of the tail's values that runs downhill is the biggest one possible. So you can't get a bigger arrangement by
            only shuffling the tail: the change has to reach at least one position further left.

            The position just left of the tail is the **pivot**, and by definition `a[pivot] < a[pivot + 1]`. Changing
            anything further left than the pivot would be a bigger jump than changing the pivot, so the next arrangement
            keeps everything before the pivot and changes the pivot itself.

            ### Bump the pivot by as little as possible

            The pivot must get a bigger value, and it can only come from the tail. To keep the step small, take the
            *smallest* tail value that's bigger than `a[pivot]`. The tail runs downhill, so scanning from the right, the
            first value bigger than the pivot is that one. (With duplicates, this also picks the rightmost of equal
            candidates, which matters below.)

            ### Then make the tail as small as possible

            After the swap, the pivot position is settled. The rest should be the smallest arrangement of what's left,
            which is increasing order. And the swap kept the tail downhill: the value placed into the tail (the old
            pivot) is smaller than everything left of where it lands and at least as big as everything right of it.
            A downhill stretch reversed is an uphill one, so reversing the tail sorts it in O(n), no sort needed.

            ### Duplicates take care of themselves

            The scans use `>=` and `<=`, so equal neighbours count as "not going up", and equal values never get swapped
            with each other. Starting from the sorted order and stepping repeatedly, you visit each *distinct*
            arrangement exactly once. For `[1, 1, 2]` that's 3 arrangements, not 6.

            ### How many are there?

            `n` different values have `n!` arrangements. With repeats, divide by the factorial of each count:
            `[3, 2, 2, 1]` has `4! / 2! = 12`.
            """,
        ]),
        ("template", "The template", [
            """
            Change `a` into the next arrangement in place and return true, or return false if `a` is already the last
            one (fully downhill), leaving it unchanged.
            """,
            code(
                "Next permutation",
                NEXT,
                [
                    ("pivot", "Walk left from the second-to-last index while the values don't go up. Where it stops is the "
                              "pivot: the rightmost `i` with `a[i] < a[i + 1]`."),
                    ("last", "No pivot: the whole array runs downhill, so this is the last arrangement."),
                    ("succ", "Walk left from the end to the first value strictly bigger than the pivot. The tail runs "
                             "downhill, so that's the smallest value in it that beats the pivot. There's always one: "
                             "`a[i + 1]` is bigger."),
                    ("swap", "Bump the pivot up to it."),
                    ("rev", "The tail is still downhill. Reverse it so it runs uphill: the smallest possible ending.",
                     {"cpp": "`reverse` on the half-open range from just after the pivot to the end."}),
                    ("ret", "A next arrangement existed."),
                ],
                NEXT_RUN,
                "next_permutation([1, 3, 5, 4, 2]); ([3, 2, 1]); ([1, 1, 2])",
            ),
            """
            `[3, 2, 1]` is the last arrangement, so it comes back false and unchanged. Some libraries (C++'s
            `std::next_permutation`) instead wrap round to the first arrangement and return false; that's the same as
            reversing the whole array when there's no pivot.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "The heights make the downhill tail easy to see:",
            walk(nw),
        ]),
        ("examples", "More examples", [
            f"""
            ### Letters work the same way

            Characters compare by their codes, so the same steps give the next word made of the same letters. For
            `{WORD}`: the tail is `k h c` (downhill), the pivot is `d`, the smallest tail letter bigger than `d` is `h`.
            Swap to get `h k d c`, reverse the tail to get `{WORD_NEXT}`.

            ### Every arrangement, in order, with repeats

            Sort the values (that's the first arrangement), then step until there's no next one. For `[2, 1, 1]` that's
            {', '.join('`' + ' '.join(map(str, p)) + '`' for p in DUP_ALL)}. Each distinct arrangement once, in order.

            ### Jumping straight to the k-th

            Stepping `k` times costs O(n·k). For distinct values you can jump: with `n` values left, each choice of the
            first value starts a block of `(n - 1)!` arrangements. So divide to find which block you're in, which tells
            you the first value, and repeat with the rest.
            """,
            walk(kw),
            f"""
            ### The other way: where does an arrangement sit?

            Running that backwards gives the **rank** of an arrangement: how many come before it. For each position,
            count the unused values smaller than the one there, and multiply by the size of the block that follows. For
            `{' '.join(map(str, RP))}`:
            """,
            table(["value", "smaller ones not yet used", "arrangements skipped"], *rank_rows),
            f"So {rank} arrangements come before it, and it's number {rank + 1}, matching the walk above.",
        ]),
        ("variations", "Variations", [
            """
            ### Listing every distinct arrangement

            Sorting and then stepping lists the arrangements in order and skips duplicates for free. It's also
            iterative: no recursion, and you can stop early. On average a step costs O(1) (most steps only touch the
            last couple of positions), so the whole listing is O(n!) arrangements' worth of output plus a little.
            """,
            code(
                "Every distinct arrangement, in dictionary order",
                ALL,
                [
                    ("np", "The template's `next_permutation`, unchanged.",
                     {"python": "`a[i + 1:] = reversed(a[i + 1:])` is the tail reversal written as a slice assignment."}),
                    ("sort", "The smallest arrangement is the sorted one. Work on a copy so the caller's array is left alone.",
                     {"c": "`qsort` with a comparator that returns -1, 0 or 1 without subtracting (subtracting can overflow)."}),
                    ("first", "Start the list with it."),
                    ("loop", "Step until there's no next arrangement, keeping each one.",
                     {"cpp": "`std::next_permutation` does exactly what our template does, and returns false after the last one.",
                      "c": "Instead of building a list of arrays, C hands each arrangement to a callback and counts them."}),
                    ("ret", "All of them, in order."),
                ],
                ALL_RUN,
                "all_arrangements([2, 1, 1]); then the count for [3, 2, 2, 1]",
            ),
            """
            ### The k-th arrangement of 1 to n

            The jumping idea from *More examples*, written out. It picks one value per position, and removing it from
            the list of unused values is O(n), so it's O(n²) overall, fine for the small `n` where `n!` still fits in a
            64-bit integer (`n ≤ 20`).
            """,
            code(
                "The k-th permutation of 1 to n",
                KTH,
                [
                    ("fact", "Factorials: `fact[m]` is how many arrangements `m` values have.",
                     {"c": "`fact[21] = {1}` sets `fact[0] = 1` and the rest to 0 before they're filled in."}),
                    ("pool", "The values not placed yet, in increasing order."),
                    ("zero", "Count from 0: `k` is now how many arrangements come before the one we want."),
                    ("each", "Fill the positions left to right."),
                    ("block", "With `slots` values left, each choice for this position leads to `(slots - 1)!` arrangements."),
                    ("pick", "Skip `k // block` whole blocks; the value that starts the block we land in goes here, and "
                             "leaves the pool.",
                     {"java": "`remove(int index)` removes by position and returns the value. The cast matters: `remove(Integer)` would remove by value.",
                      "c": "Shift the rest of the pool down by one to close the gap."}),
                    ("rest", "What's left of `k` is the position inside that block."),
                    ("ret", "The arrangement."),
                ],
                KTH_RUN,
                "kth_permutation(4, 9); (3, 1); (3, 6)",
            ),
            """
            ### Going the other way

            There's a mirror-image *previous* arrangement too: the largest one that's smaller. It has the same shape (a
            scan for a pivot, a swap, a reversal), and working out exactly which comparisons change is a good way to
            check you understand why each step of the template is there.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            One step is three scans over at most the whole array: O(n) time, O(1) extra space. In the worst case (a step
            like `1 5 4 3 2 → 2 1 3 4 5`) it touches every position; usually it only touches a short tail.

            Listing all arrangements with repeated steps costs O(1) per step on average, so it's dominated by the number
            of arrangements. Jumping to the k-th is O(n²) with a plain list for the pool, independent of `k`.
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Generate all arrangements, sort, find the next", "O(n! · n log n)", "O(n! · n)"],
                ["Next permutation", "O(n)", "O(1)"],
                ["k steps of next permutation", "O(n·k) worst case", "O(1)"],
                ["k-th permutation by factorial blocks", "O(n²)", "O(n)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            There's no built-in next permutation. `itertools.permutations` lists arrangements by *position*, so with
            repeated values it repeats arrangements, and it only comes out in dictionary order if the input was sorted.
            Strings are immutable: work on `list(s)` and `"".join` at the end.

            ### Java

            No library version; write the template. For a `String`, use `toCharArray()` and `new String(chars)`. When
            removing from a `List<Integer>` by position, make sure the argument is an `int`, not an `Integer`.

            ### C++

            `std::next_permutation(first, last)` and `std::prev_permutation` are built in. Both return false when they
            wrap round (and leave the range at the first or last arrangement). They work on strings too:
            `next_permutation(s.begin(), s.end())`.

            ### C

            Write the template with an explicit length. For the k-th permutation, keep `k` and the factorials in
            `long long`; `13!` already overflows a 32-bit `int`.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Using `>` instead of `>=` in the pivot scan (or `<` instead of `<=` in the successor scan). With repeated
              values that either swaps equal values or picks the wrong successor.
            - Sorting the tail instead of reversing it. It works, but it's O(n log n), and it hides the fact that the
              tail is already sorted the other way.
            - Forgetting the "no pivot" case: an array that runs downhill all the way, including a single value.
            - Picking the *largest* tail value bigger than the pivot rather than the smallest.
            - Treating k as 1-based in some places and 0-based in others in the k-th permutation.
            - Overflowing factorials for `n ≥ 13` in 32-bit integers.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why does the change have to happen at the pivot, and not further right?",
                 "Everything right of the pivot runs downhill, which is already the largest arrangement of those values. No rearrangement of them alone can make the whole thing bigger."),
                ("Why scan from the right for the successor?",
                 "The tail runs downhill, so the values get smaller as you go right. The first value bigger than the pivot that you meet from the right is the smallest such value."),
                ("Why can you reverse the tail instead of sorting it?",
                 "The swap keeps the tail running downhill, and a downhill run reversed is sorted in increasing order."),
                ("What is the next arrangement of 2 4 3 1?",
                 "The pivot is 2 (index 0); the smallest bigger value to its right is 3. Swap to get 3 4 2 1, then reverse the tail: 3 1 2 4."),
                ("How many distinct arrangements does [1, 1, 2, 2] have?",
                 "4! / (2! · 2!) = 6."),
            ),
        ]),
    ],
)
