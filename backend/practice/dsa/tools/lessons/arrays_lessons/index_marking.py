"""Lesson: In-place index marking (Arrays & Hashing, pattern 6)."""
from lesson import Bars, Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

IS_PERM = {
    "python": """
        def is_permutation(nums):
            n = len(nums)                                   #@n
            ok = True                                       #@n
            for x in nums:                                  #@loop
                v = abs(x)                                  #@read
                if v < 1 or v > n or nums[v - 1] < 0:       #@check
                    ok = False                              #@check
                    break                                   #@check
                nums[v - 1] = -nums[v - 1]                  #@mark
            for i in range(n):                              #@restore
                nums[i] = abs(nums[i])                      #@restore
            return ok                                       #@ret
    """,
    "java": """
        static boolean isPermutation(int[] nums) {
            int n = nums.length;                            //@n
            boolean ok = true;                              //@n
            for (int i = 0; i < n; i++) {                   //@loop
                int v = Math.abs(nums[i]);                  //@read
                if (v < 1 || v > n || nums[v - 1] < 0) {    //@check
                    ok = false;                             //@check
                    break;                                  //@check
                }
                nums[v - 1] = -nums[v - 1];                 //@mark
            }
            for (int i = 0; i < n; i++) nums[i] = Math.abs(nums[i]);  //@restore
            return ok;                                      //@ret
        }
    """,
    "cpp": """
        bool isPermutation(vector<int>& nums) {
            int n = nums.size();                            //@n
            bool ok = true;                                 //@n
            for (int i = 0; i < n; i++) {                   //@loop
                int v = abs(nums[i]);                       //@read
                if (v < 1 || v > n || nums[v - 1] < 0) {    //@check
                    ok = false;                             //@check
                    break;                                  //@check
                }
                nums[v - 1] = -nums[v - 1];                 //@mark
            }
            for (int& x : nums) x = abs(x);                 //@restore
            return ok;                                      //@ret
        }
    """,
    "c": """
        bool isPermutation(int* nums, int n) {
            bool ok = true;                                 //@n
            for (int i = 0; i < n; i++) {                   //@loop
                int v = abs(nums[i]);                       //@read
                if (v < 1 || v > n || nums[v - 1] < 0) {    //@check
                    ok = false;                             //@check
                    break;                                  //@check
                }
                nums[v - 1] = -nums[v - 1];                 //@mark
            }
            for (int i = 0; i < n; i++) nums[i] = abs(nums[i]);  //@restore
            return ok;                                      //@ret
        }
    """,
}
IS_PERM_RUN = {
    "python": """
        for nums in [[3, 1, 4, 2], [3, 1, 3, 2], [5, 1, 2, 3], [1]]:
            ok = is_permutation(nums)
            print(str(ok).lower(), *nums)
    """,
    "java": """
        public static void main(String[] args) {
            int[][] cases = {{3, 1, 4, 2}, {3, 1, 3, 2}, {5, 1, 2, 3}, {1}};
            for (int[] nums : cases) {
                StringBuilder sb = new StringBuilder(String.valueOf(isPermutation(nums)));
                for (int x : nums) sb.append(" ").append(x);
                System.out.println(sb);
            }
        }
    """,
    "cpp": """
        int main() {
            vector<vector<int>> cases = {{3, 1, 4, 2}, {3, 1, 3, 2}, {5, 1, 2, 3}, {1}};
            for (auto& nums : cases) {
                cout << boolalpha << isPermutation(nums);
                for (int x : nums) cout << " " << x;
                cout << "\\n";
            }
        }
    """,
    "c": """
        int main(void) {
            int a[] = {3, 1, 4, 2}, b[] = {3, 1, 3, 2}, c[] = {5, 1, 2, 3}, d[] = {1};
            int* cases[] = {a, b, c, d};
            int sizes[] = {4, 4, 4, 1};
            for (int k = 0; k < 4; k++) {
                printf("%s", isPermutation(cases[k], sizes[k]) ? "true" : "false");
                for (int i = 0; i < sizes[k]; i++) printf(" %d", cases[k][i]);
                printf("\\n");
            }
            return 0;
        }
    """,
}

COUNTS = {
    "python": """
        def counts_in_place(nums):
            n = len(nums)                           #@n
            for x in nums:                          #@loop
                nums[(x - 1) % n] += n              #@add
            for i in range(n):                      #@read
                nums[i] = (nums[i] - 1) // n        #@read
            return nums                             #@ret
    """,
    "java": """
        static int[] countsInPlace(int[] nums) {
            int n = nums.length;                            //@n
            for (int i = 0; i < n; i++) {                   //@loop
                nums[(nums[i] - 1) % n] += n;               //@add
            }
            for (int i = 0; i < n; i++) nums[i] = (nums[i] - 1) / n;  //@read
            return nums;                                    //@ret
        }
    """,
    "cpp": """
        vector<int>& countsInPlace(vector<int>& nums) {
            int n = nums.size();                            //@n
            for (int i = 0; i < n; i++) {                   //@loop
                nums[(nums[i] - 1) % n] += n;               //@add
            }
            for (int& x : nums) x = (x - 1) / n;            //@read
            return nums;                                    //@ret
        }
    """,
    "c": """
        void countsInPlace(int* nums, int n) {
            for (int i = 0; i < n; i++) {                   //@loop
                nums[(nums[i] - 1) % n] += n;               //@add
            }
            for (int i = 0; i < n; i++) nums[i] = (nums[i] - 1) / n;  //@read
        }
    """,
}
COUNTS_RUN = {
    "python": """
        print(*counts_in_place([3, 1, 3, 4, 1, 3]))
        print(*counts_in_place([2, 2, 2]))
    """,
    "java": """
        public static void main(String[] args) {
            for (int[] nums : new int[][] {{3, 1, 3, 4, 1, 3}, {2, 2, 2}}) {
                int[] c = countsInPlace(nums);
                StringBuilder sb = new StringBuilder();
                for (int x : c) sb.append(sb.length() > 0 ? " " : "").append(x);
                System.out.println(sb);
            }
        }
    """,
    "cpp": """
        int main() {
            vector<vector<int>> cases = {{3, 1, 3, 4, 1, 3}, {2, 2, 2}};
            for (auto& nums : cases) {
                auto& c = countsInPlace(nums);
                for (size_t i = 0; i < c.size(); i++) cout << (i ? " " : "") << c[i];
                cout << "\\n";
            }
        }
    """,
    "c": """
        int main(void) {
            int a[] = {3, 1, 3, 4, 1, 3}, b[] = {2, 2, 2};
            countsInPlace(a, 6);
            countsInPlace(b, 3);
            for (int i = 0; i < 6; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
            for (int i = 0; i < 3; i++) printf(i ? " %d" : "%d", b[i]);
            printf("\\n");
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

is_permutation = py(IS_PERM["python"], "is_permutation")
counts_in_place = py(COUNTS["python"], "counts_in_place")

DEMO = [3, 1, 4, 2]
assert is_permutation(list(DEMO))

walk1 = Steps(f"`is_permutation({DEMO})`. Each value v flips the sign of slot v - 1, so a minus sign means \"I've seen v\".")
arr = list(DEMO)
walk1.step("Values should be 1 to 4, and there are 4 slots, so value v gets slot v - 1. Nothing is marked yet.",
           Row(arr, slots=True), M({"marked": "none"}))
for i in range(len(arr)):
    v = abs(arr[i])
    arr[v - 1] = -arr[v - 1]
    marked = sorted(j + 1 for j in range(len(arr)) if arr[j] < 0)
    walk1.step(f"Index {i} holds {v} (we read abs, since the sign may already be flipped). Slot {v - 1} is positive, so {v} is new: flip it to {arr[v - 1]}.",
               Row(list(arr), st={**{j: "found" for j in range(len(arr)) if arr[j] < 0}, v - 1: "new"}, ptr={"i": i}, slots=True),
               M({"seen": ", ".join(map(str, marked))}))
walk1.step("Every value landed on an unmarked slot, so each of 1 to 4 appears exactly once. Now flip the signs back so the caller gets their array unchanged.",
           Row(DEMO, slots=True), result="true")

BAD = [3, 1, 3, 2]
walk2 = Steps(f"`is_permutation({BAD})`: what happens when a value repeats.")
arr = list(BAD)
walk2.step("Same rule: value v flips slot v - 1.", Row(arr, slots=True))
for i in range(len(arr)):
    v = abs(arr[i])
    if arr[v - 1] < 0:
        walk2.step(f"Index {i} holds {v}, but slot {v - 1} is already negative. We've seen {v} before, so this can't be a permutation. Stop.",
                   Row(list(arr), st={v - 1: "answer", i: "active"}, ptr={"i": i}, slots=True), result="false")
        break
    arr[v - 1] = -arr[v - 1]
    walk2.step(f"Index {i} holds {v}. Slot {v - 1} is positive: mark it.",
               Row(list(arr), st={**{j: "found" for j in range(len(arr)) if arr[j] < 0}, v - 1: "new"}, ptr={"i": i}, slots=True))

CD = [3, 1, 3, 4, 1, 3]
CN = len(CD)
CRES = counts_in_place(list(CD))
assert CRES == [CD.count(v) for v in range(1, CN + 1)]
walk3 = Steps(f"`counts_in_place({CD})`. Each value v adds n = {CN} to slot v - 1. A slot can still tell you its original value with mod.")
arr = list(CD)
walk3.step(f"Each slot holds a value from 1 to {CN}. Adding {CN} doesn't hide it: (slot - 1) % {CN} + 1 is still the original value.", Row(arr, slots=True))
for i in range(CN):
    x = arr[i]
    v = (x - 1) % CN + 1
    arr[v - 1] += CN
    walk3.step(f"Index {i} now reads {x}, which is really {v} ({x} - 1 mod {CN}, plus 1). Add {CN} to slot {v - 1}, making it {arr[v - 1]}.",
               Row(list(arr), st={v - 1: "new", i: "active"} if v - 1 != i else {i: "new"}, ptr={"i": i}, slots=True))
final = [(a - 1) // CN for a in arr]
walk3.step(f"Each slot is now original + {CN} × count. Since the original is between 1 and {CN}, (slot - 1) // {CN} is exactly the count.",
           Row(list(arr), slots=True, label="encoded"), Bars(final, labels=range(1, CN + 1), label="how many of each value"), result=final)
assert final == CRES

# Zero-based values and the ~ trick.
ZB = [2, 0, 3, 1]
zmark = list(ZB)
for x in ZB:
    v = x if x >= 0 else ~x
    zmark[v] = ~zmark[v]
z_rows = [(str(x), str(~x)) for x in [0, 1, 2, 3]]

# Memory comparison for n = 10**6.
N6 = 10**6

lesson(
    "arrays-hashing",
    "index-marking",
    """
    When the values in an array are numbers from 1 to n and the array has n slots, the array can be its own
    "seen" table. Value `v` leaves a mark at index `v - 1`, usually by flipping its sign, and you get set-like
    answers with no extra memory.
    """,
    [
        ("idea", "The idea", [
            """
            Imagine a cloakroom with hooks numbered 1 to 20 and twenty tickets handed out. You want to know whether every
            ticket number was given out exactly once. You could write the numbers down on a separate sheet. Or you could
            just walk along the tickets and, for ticket 7, hang a little tag on hook 7. If you ever go to tag a hook that
            already has one, that number was handed out twice.

            The hooks are already there. You didn't need a separate sheet, because every ticket number points at its own
            hook.

            Arrays work the same way when the values are 1 to `n` and there are `n` slots. Value `v` "belongs to" index
            `v - 1`. So instead of a hash set of values you've seen, you leave a mark at index `v - 1`. The usual mark is
            flipping that slot's number to negative, because:

            - the slot still remembers its own value (take `abs`), and
            - the sign tells you whether `v` has been seen.
            """,
            fig(Row(DEMO, slots=True, label="before"), Row([-x for x in DEMO], st={i: "found" for i in range(4)}, slots=True, label="after marking 3, 1, 4, 2"),
                caption="Every slot ended up negative: each of 1 to 4 was seen. The numbers themselves are still readable with abs."),
            key("""
            Values from 1 to n can index their own array. Leave a mark at index `v - 1` (flip the sign, or add n) and the
            array works as a "seen" table, using O(1) extra memory.
            """),
            """
            You'd only bother with this when the problem asks for O(1) extra space, because a hash set does the same job
            more simply. But interviewers ask for exactly that constraint a lot, and this is how you meet it.
            """,
        ]),
        ("signals", "When to reach for it", [
            """
            The tell is a combination of two things. First, the values are tied to the size of the array: "numbers from
            1 to n", "n + 1 numbers from 1 to n", "seats 0 to n". Second, the problem asks for O(1) extra space, or says
            "without extra memory", or "modify the array in place".

            Questions that usually fit: which values are missing, which appear twice, is this a permutation, how many
            times does each value appear, what's the smallest positive number not present.

            When it doesn't fit:

            - The values aren't tied to the length (any integers up to 10⁹). Then they can't index the array, and you
              need a hash set or sorting.
            - You're not allowed to change the input, even temporarily. Marking changes it. (You can often restore it
              afterwards, but check what the problem allows.)
            - O(n) extra memory is fine. Then just use a set or a boolean array. It's clearer and harder to get wrong.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### The array is already a table

            A "seen" table for values 1 to `n` is just a boolean array of size `n`, indexed by `v - 1`. The input array already has `n` slots indexed `0` to `n - 1`, and each slot holds a number we still need. So
            the trick is to squeeze one extra bit of information (seen or not) into each slot without losing the
            number already there.

            ### Ways to hide a bit in a slot

            - The sign. Values are positive, so the sign bit is free. Negative means "seen". `abs(slot)` gives the
              original back. This is the most common choice.
            - Adding n. Values are 1 to `n`. Add `n` once per sighting and the slot holds `original + n × count`.
              `(slot - 1) % n + 1` recovers the original, and `(slot - 1) // n` gives the count. It stores a whole count,
              not just one bit.
            - Bitwise NOT (`~x`). For values from 0 to `n - 1`, the sign trick fails on 0 (there's no "-0"). `~x`
              turns 0 into -1, 1 into -2 and so on, and applying it again undoes it. Negative still means marked.
            """,
            table(["value x", "~x"], *z_rows),
            """
            ### Reading values while marking

            While you walk the array, some slots you'll read have already been marked by earlier values. So never use
            the raw slot value as an index. Always decode it first: `abs(x)` for signs, `(x - 1) % n + 1` for the +n trick,
            `~x` if negative for NOT marks. Forgetting this is the most common bug in this pattern.

            ### Putting it back

            Marking changes the caller's array. Good manners (and sometimes the problem) say you restore it afterwards:
            one more pass taking `abs`, or `(x - 1) % n + 1`. That keeps the extra space at O(1) and the input unchanged.

            ### How it relates to cyclic sort

            *Cyclic sort* (pattern 10) uses the same "value v belongs at index v - 1" idea, but instead of leaving a mark
            it physically moves each value to its home with swaps. Marking keeps everything where it is and only changes
            signs. Both are O(n) time and O(1) extra space. Marking is usually shorter when you only need yes/no
            information; moving values is handy when you need to know which value sits where.
            """,
        ]),
        ("template", "The template", [
            """
            Is `nums` a permutation of 1 to `n`, meaning every number from 1 to `n` appears exactly once? Answer with
            O(1) extra space, and leave the array the way you found it. (Values are positive.)
            """,
            code(
                "Is it a permutation of 1 to n?",
                IS_PERM,
                [
                    ("n", "`n` is both the length and the largest value allowed. `ok` starts true; any problem flips it.",
                     {"c": "In C, `n` comes in as a parameter."}),
                    ("loop", "One pass over the array."),
                    ("read", "Decode the value first. An earlier value may already have flipped this slot negative, but "
                             "`abs` gives back the number that was there."),
                    ("check", "Three ways to fail: the value is too small, too big, or its slot is already marked "
                              "(we've seen it before). We stop at the first one but still restore the array below."),
                    ("mark", "Flip slot `v - 1` negative: \"`v` has been seen\". Its own value is still readable with `abs`."),
                    ("restore", "Undo every mark so the caller gets the array back unchanged."),
                    ("ret", "True only if every value was in range and new. With `n` values all different and all between "
                            "1 and `n`, every number from 1 to `n` must appear exactly once."),
                ],
                IS_PERM_RUN,
                "is_permutation([3, 1, 4, 2]); [3, 1, 3, 2]; [5, 1, 2, 3]; [1]",
            ),
            """
            The second number on each line of output is the array after the call, showing it came back unchanged even
            when we stopped early.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "A permutation first. Watch the minus signs appear:",
            walk(walk1),
            "And a repeat. The second `3` finds its slot already marked:",
            walk(walk2),
        ]),
        ("examples", "More examples", [
            f"""
            ### Counting every value in place

            The sign only stores one bit: seen or not. If you need actual counts, add `n` for every sighting instead.
            Here's `{CD}` with `n = {CN}`. Watch slot 2 (value 3's home) climb by {CN} three times:
            """,
            walk(walk3),
            f"""
            So value 1 appears {CRES[0]} times, value 3 appears {CRES[2]} times, and values 2, 5 and 6 don't appear.

            ### Values from 0 instead of 1

            If the values are 0 to `n - 1`, value `v` belongs at index `v` directly. But flipping the sign of 0 does
            nothing. Use `~x` as the mark instead: for `{ZB}`, marking every value turns the array into `{zmark}`. Every
            slot is negative, so every value was seen, and `~` on each one gives the original numbers back.

            ### How much memory are we saving?

            For a million values, a separate boolean array is a million bytes, and a hash set of a million ints is
            tens of megabytes once you count its overhead. Marking uses none of that. It rarely matters in practice, but
            it's exactly the kind of constraint interviewers like to add to an easy problem to make it a medium one.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Counts with +n

            The function from *More examples*, in all four languages. Each value adds `n` to its home slot, and at the
            end each slot is decoded into a count.
            """,
            code(
                "Count each value of 1 to n, in place",
                COUNTS,
                [
                    ("n", "Values are 1 to `n`, and `n` is also the amount we add per sighting."),
                    ("loop", "One pass. Some slots we read have already been increased by earlier values."),
                    ("add", "`(x - 1) % n` decodes the value's home index however many times `n` has been added. Then add "
                            "`n` there to record one more sighting."),
                    ("read", "Each slot is now `original + n × count`, with the original between 1 and `n`. Subtracting 1 "
                             "and dividing by `n` drops the original and leaves the count.",
                     {"c": "C returns nothing: the counts are written straight into `nums`."}),
                    ("ret", "The array now holds counts: slot `i` is how many times `i + 1` appeared."),
                ],
                COUNTS_RUN,
                "counts_in_place([3, 1, 3, 4, 1, 3]); counts_in_place([2, 2, 2])",
            ),
            """
            Watch the size of the numbers. A slot can grow to `n + n × n`. With `n = 100,000` that's ten billion, which
            overflows a 32-bit `int`. For big `n`, use a 64-bit array or stick to sign marks.

            ### Finding which values are missing or repeated

            After a marking pass, the marks tell you everything a set would: an unmarked slot `i` means value `i + 1`
            never appeared, and running into an already-marked slot means you've hit a repeat. Several of the practice
            problems are exactly this idea with different questions on top.

            ### Junk values

            If the array can contain zeros, negatives or numbers bigger than `n`, first decide what to do with them.
            Usually they can't be the answer and can be skipped or replaced with a harmless value (like `n + 1`) before
            the marking pass, so they never point at a slot.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Marking is one pass, O(n), plus one pass to restore or read the marks, another O(n). Extra memory is O(1),
            a couple of variables, not counting the answer itself if the problem asks you to return a list.

            Compare the alternatives: a hash set is O(n) time on average and O(n) memory; sorting is O(n log n) time and
            changes the order; checking every value against every other is O(n²).
            """,
            table(
                ["Approach", "Time", "Extra space", "Changes the input?"],
                ["Compare every pair", "O(n²)", "O(1)", "no"],
                ["Sort, then scan", "O(n log n)", "O(1) to O(n)", "yes, reorders it"],
                ["Hash set / boolean array", "O(n)", "O(n)", "no"],
                ["Mark in place", "O(n)", "O(1)", "temporarily (restore it)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `abs(x)` and `~x` work as you'd expect. Python ints don't overflow, so the +n trick is always safe. Careful
            with `for x in nums:` while you modify `nums`: it reads the current values, which is fine here because we
            decode them, but it's easy to forget that they've changed.

            ### Java

            `Math.abs(x)`. Be aware that `Math.abs(Integer.MIN_VALUE)` is still negative, so if values could be that
            small, this isn't the right pattern anyway. Use an index loop rather than for-each if you find it clearer to
            see that you're reading updated values.

            ### C++

            `abs` from `<cstdlib>` for `int`. Pass the vector by reference if you mean to modify it, and restore it
            before returning. `~x` works on `int`.

            ### C

            Same as C++: `abs` from `<stdlib.h>`. Since you can't return the array, the marks are visible to the caller
            unless you restore them, so always add the restore loop.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Using a marked value as an index. Always decode first (`abs`, mod, `~`), or you'll index with a negative
              or oversized number.
            - Zero. `-0` is `0`, so the sign trick can't mark a slot holding 0. Shift the values, use `~`, or use +n.
            - Values outside 1 to `n`. They don't have a slot. Check the range before indexing.
            - Marking twice. Flipping a negative slot back to positive "unsees" a value. Check before flipping, or set
              it to `-abs(slot)` so a second mark does nothing.
            - Overflow with +n. Slots can reach `n + n²`.
            - Forgetting to restore. The caller (and sometimes the judge) sees your marks.
            - Using it when you don't need to. If extra memory is allowed, a set is clearer.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why do we read `abs(nums[i])` instead of `nums[i]` inside the marking loop?",
                 "An earlier value may already have flipped this slot negative. The number it holds is still the original value, just with a minus sign. `abs` gets it back so we can use it as an index."),
                ("Values are 0 to n - 1. Why does flipping signs fail, and what do you use instead?",
                 "You can't make 0 negative, so value 0's slot can never be marked if it holds a 0. Use `~x` (0 becomes -1), or add n."),
                ("After `counts_in_place`, how do you get the count from a slot holding 13 when n = 6?",
                 "`(13 - 1) // 6 = 2`. The slot held an original value of 1 plus 6 × 2."),
                ("When would you choose a hash set over marking?",
                 "When values aren't limited to 1..n, when you're not allowed to change the input, or simply when O(n) extra memory is fine. A set is easier to read and harder to get wrong."),
                ("`is_permutation` stops early on a repeated value. Why is the restore loop still important?",
                 "By the time it stops, some slots are already negative. Without the restore pass the caller would get back a partly negated array."),
            ),
        ]),
    ],
)
