"""Lesson: Cyclic sort (Arrays & Hashing, pattern 10)."""
from lesson import Bars, Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

PLACE = {
    "python": """
        def cyclic_place(nums):
            i = 0                                           #@start
            while i < len(nums):                            #@loop
                home = nums[i] - 1                          #@home
                if nums[home] != nums[i]:                   #@check
                    nums[i], nums[home] = nums[home], nums[i]   #@swap
                else:                                       #@next
                    i += 1                                  #@next
            return nums                                     #@ret
    """,
    "java": """
        static int[] cyclicPlace(int[] nums) {
            int i = 0;                                      //@start
            while (i < nums.length) {                       //@loop
                int home = nums[i] - 1;                     //@home
                if (nums[home] != nums[i]) {                //@check
                    int t = nums[home];                     //@swap
                    nums[home] = nums[i];                   //@swap
                    nums[i] = t;                            //@swap
                } else {                                    //@next
                    i++;                                    //@next
                }
            }
            return nums;                                    //@ret
        }
    """,
    "cpp": """
        vector<int>& cyclicPlace(vector<int>& nums) {
            size_t i = 0;                                   //@start
            while (i < nums.size()) {                       //@loop
                int home = nums[i] - 1;                     //@home
                if (nums[home] != nums[i]) {                //@check
                    swap(nums[i], nums[home]);              //@swap
                } else {                                    //@next
                    i++;                                    //@next
                }
            }
            return nums;                                    //@ret
        }
    """,
    "c": """
        void cyclicPlace(int* nums, int n) {
            int i = 0;                                      //@start
            while (i < n) {                                 //@loop
                int home = nums[i] - 1;                     //@home
                if (nums[home] != nums[i]) {                //@check
                    int t = nums[home];                     //@swap
                    nums[home] = nums[i];                   //@swap
                    nums[i] = t;                            //@swap
                } else {                                    //@next
                    i++;                                    //@next
                }
            }
        }
    """,
}
PLACE_RUN = {
    "python": """
        print(*cyclic_place([3, 1, 5, 4, 2]))
        print(*cyclic_place([4, 3, 4, 1, 3]))
    """,
    "java": """
        public static void main(String[] args) {
            for (int[] nums : new int[][] {{3, 1, 5, 4, 2}, {4, 3, 4, 1, 3}}) {
                StringBuilder sb = new StringBuilder();
                for (int x : cyclicPlace(nums)) sb.append(sb.length() > 0 ? " " : "").append(x);
                System.out.println(sb);
            }
        }
    """,
    "cpp": """
        int main() {
            vector<vector<int>> cases = {{3, 1, 5, 4, 2}, {4, 3, 4, 1, 3}};
            for (auto& nums : cases) {
                auto& v = cyclicPlace(nums);
                for (size_t i = 0; i < v.size(); i++) cout << (i ? " " : "") << v[i];
                cout << "\\n";
            }
        }
    """,
    "c": """
        int main(void) {
            int a[] = {3, 1, 5, 4, 2}, b[] = {4, 3, 4, 1, 3};
            cyclicPlace(a, 5);
            cyclicPlace(b, 5);
            for (int i = 0; i < 5; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
            for (int i = 0; i < 5; i++) printf(i ? " %d" : "%d", b[i]);
            printf("\\n");
            return 0;
        }
    """,
}

APPLY = {
    "python": """
        def apply_in_place(items, dest):
            n = len(items)                                  #@n
            for start in range(n):                          #@start
                if dest[start] < 0:                         #@skip
                    continue                                #@skip
                carry = items[start]                        #@carry
                j = dest[start]                             #@carry
                dest[start] = ~dest[start]                  #@carry
                while j != start:                           #@cycle
                    items[j], carry = carry, items[j]       #@drop
                    nxt = dest[j]                           #@follow
                    dest[j] = ~dest[j]                      #@follow
                    j = nxt                                 #@follow
                items[start] = carry                        #@close
            for i in range(n):                              #@restore
                dest[i] = ~dest[i]                          #@restore
            return items                                    #@ret
    """,
    "java": """
        static int[] applyInPlace(int[] items, int[] dest) {
            int n = items.length;                           //@n
            for (int start = 0; start < n; start++) {       //@start
                if (dest[start] < 0) continue;              //@skip
                int carry = items[start];                   //@carry
                int j = dest[start];                        //@carry
                dest[start] = ~dest[start];                 //@carry
                while (j != start) {                        //@cycle
                    int t = items[j];                       //@drop
                    items[j] = carry;                       //@drop
                    carry = t;                              //@drop
                    int nxt = dest[j];                      //@follow
                    dest[j] = ~dest[j];                     //@follow
                    j = nxt;                                //@follow
                }
                items[start] = carry;                       //@close
            }
            for (int i = 0; i < n; i++) dest[i] = ~dest[i]; //@restore
            return items;                                   //@ret
        }
    """,
    "cpp": """
        vector<int>& applyInPlace(vector<int>& items, vector<int>& dest) {
            int n = items.size();                           //@n
            for (int start = 0; start < n; start++) {       //@start
                if (dest[start] < 0) continue;              //@skip
                int carry = items[start];                   //@carry
                int j = dest[start];                        //@carry
                dest[start] = ~dest[start];                 //@carry
                while (j != start) {                        //@cycle
                    swap(items[j], carry);                  //@drop
                    int nxt = dest[j];                      //@follow
                    dest[j] = ~dest[j];                     //@follow
                    j = nxt;                                //@follow
                }
                items[start] = carry;                       //@close
            }
            for (int& d : dest) d = ~d;                     //@restore
            return items;                                   //@ret
        }
    """,
    "c": """
        void applyInPlace(int* items, int* dest, int n) {
            for (int start = 0; start < n; start++) {       //@start
                if (dest[start] < 0) continue;              //@skip
                int carry = items[start];                   //@carry
                int j = dest[start];                        //@carry
                dest[start] = ~dest[start];                 //@carry
                while (j != start) {                        //@cycle
                    int t = items[j];                       //@drop
                    items[j] = carry;                       //@drop
                    carry = t;                              //@drop
                    int nxt = dest[j];                      //@follow
                    dest[j] = ~dest[j];                     //@follow
                    j = nxt;                                //@follow
                }
                items[start] = carry;                       //@close
            }
            for (int i = 0; i < n; i++) dest[i] = ~dest[i]; //@restore
        }
    """,
}
APPLY_RUN = {
    "python": """
        items, dest = [10, 20, 30, 40, 50, 60], [2, 0, 1, 5, 4, 3]
        print(*apply_in_place(items, dest))
        print(*dest)
    """,
    "java": """
        public static void main(String[] args) {
            int[] items = {10, 20, 30, 40, 50, 60}, dest = {2, 0, 1, 5, 4, 3};
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int x : applyInPlace(items, dest)) a.append(a.length() > 0 ? " " : "").append(x);
            for (int x : dest) b.append(b.length() > 0 ? " " : "").append(x);
            System.out.println(a);
            System.out.println(b);
        }
    """,
    "cpp": """
        int main() {
            vector<int> items = {10, 20, 30, 40, 50, 60}, dest = {2, 0, 1, 5, 4, 3};
            auto& v = applyInPlace(items, dest);
            for (size_t i = 0; i < v.size(); i++) cout << (i ? " " : "") << v[i];
            cout << "\\n";
            for (size_t i = 0; i < dest.size(); i++) cout << (i ? " " : "") << dest[i];
            cout << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int items[] = {10, 20, 30, 40, 50, 60}, dest[] = {2, 0, 1, 5, 4, 3};
            applyInPlace(items, dest, 6);
            for (int i = 0; i < 6; i++) printf(i ? " %d" : "%d", items[i]);
            printf("\\n");
            for (int i = 0; i < 6; i++) printf(i ? " %d" : "%d", dest[i]);
            printf("\\n");
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

cyclic_place = py(PLACE["python"], "cyclic_place")
apply_in_place = py(APPLY["python"], "apply_in_place")

DEMO = [3, 1, 5, 4, 2]
assert cyclic_place(list(DEMO)) == [1, 2, 3, 4, 5]

cw = Steps(f"`cyclic_place({DEMO})`. Value v belongs at index v - 1. Swap each value home until index i holds the right thing.")
arr, i, swaps = list(DEMO), 0, 0
cw.step("Every value is between 1 and 5, so each has exactly one home: value v lives at index v - 1.", Row(arr, slots=True), M({"swaps": 0}))
while i < len(arr):
    home = arr[i] - 1
    if arr[home] != arr[i]:
        v, w = arr[i], arr[home]
        arr[i], arr[home] = arr[home], arr[i]
        swaps += 1
        homed = {k: "found" for k in range(len(arr)) if arr[k] == k + 1}
        cw.step(f"Index {i} holds {v}, whose home is index {home}. Swap: {v} goes home, and {w} comes back to index {i} to be looked at next.",
                Row(list(arr), st={**homed, home: "new", i: "active" if arr[i] != i + 1 else "found"}, ptr={"i": i}, slots=True), M({"swaps": swaps}))
    else:
        cw.step(f"Index {i} holds {arr[i]}, which is already home. Move on to index {i + 1}.",
                Row(list(arr), st={k: "found" for k in range(len(arr)) if arr[k] == k + 1}, ptr={"i": i}, slots=True), M({"swaps": swaps}))
        i += 1
cw.steps[-1]["text"] += " Every value is home: sorted."

DUP = [4, 3, 4, 1, 3]
DUP_OUT = cyclic_place(list(DUP))
dw = Steps(f"`cyclic_place({DUP})`. Some values repeat and some are missing. What happens to the extra copies?")
arr, i = list(DUP), 0
dw.step("Same rule. This time two values (2 and 5) are missing and two (3 and 4) appear twice.", Row(arr, slots=True))
while i < len(arr):
    home = arr[i] - 1
    if arr[home] != arr[i]:
        v, w = arr[i], arr[home]
        arr[i], arr[home] = arr[home], arr[i]
        dw.step(f"Index {i}: {v} goes home to index {home}, and {w} comes back to index {i}.",
                Row(list(arr), st={**{k: "found" for k in range(len(arr)) if arr[k] == k + 1}, home: "new"}, ptr={"i": i}, slots=True))
    else:
        if home == i:
            msg = f"Index {i} holds {arr[i]}, already home. Move on."
        else:
            msg = f"Index {i} holds {arr[i]}, but its home (index {home}) already has a {arr[i]}. This one is an extra copy: leave it here and move on. Without this check the loop would swap the two equal values forever."
        dw.step(msg, Row(list(arr), st={**{k: "found" for k in range(len(arr)) if arr[k] == k + 1}, **({i: "mark"} if home != i else {})}, ptr={"i": i}, slots=True))
        i += 1
assert arr == DUP_OUT
MISFITS = [(k, arr[k]) for k in range(len(arr)) if arr[k] != k + 1]

# Cycles of a permutation.
PERM = [3, 5, 1, 2, 4, 6]  # values 1..6
seen, CYCLES = set(), []
for s in range(len(PERM)):
    if s in seen:
        continue
    cyc, k = [], s
    while k not in seen:
        seen.add(k)
        cyc.append(k)
        k = PERM[k] - 1
    CYCLES.append(cyc)
cyc_rows = [(" → ".join(f"index {k} ({PERM[k]})" for k in c) + (" → back" if len(c) > 1 else " (already home)"), str(len(c))) for c in CYCLES]
cyc_state = {}
for t, c in enumerate(CYCLES):
    for k in c:
        cyc_state[k] = ["answer", "found", "mark", "active"][t % 4]

# Applying a reordering in place.
ITEMS, DEST = [10, 20, 30, 40, 50, 60], [2, 0, 1, 5, 4, 3]
AP = apply_in_place(list(ITEMS), list(DEST))
expect = [None] * 6
for k in range(6):
    expect[DEST[k]] = ITEMS[k]
assert AP == expect
aw = Steps(f"Moving `{ITEMS}` so item k lands at index dest[k] = `{DEST}`, with one spare variable.")
items, dest = list(ITEMS), list(DEST)
aw.step("Each item has a destination. Following destinations from any index goes round a loop and comes back.", Row(items, slots=True, label="items"), Row(dest, slots=True, label="dest"))
for start in range(6):
    if dest[start] < 0:
        continue
    carry, j = items[start], dest[start]
    dest[start] = ~dest[start]
    aw.step(f"Start a loop at index {start}: pick up {carry} (it's going to index {j}).", Row(list(items), st={start: "mark"}, slots=True, label="items"), M({"carrying": carry}))
    while j != start:
        old = items[j]
        items[j], carry = carry, items[j]
        aw.step(f"Put it down at index {j} and pick up the {old} that was there.", Row(list(items), st={j: "new"}, ptr={"j": j}, slots=True, label="items"), M({"carrying": carry}))
        nxt = dest[j]
        dest[j] = ~dest[j]
        j = nxt
    items[start] = carry
    aw.step(f"The loop is back at index {start}: put down {carry}. This loop is done.", Row(list(items), st={start: "new"}, slots=True, label="items"), M({"carrying": "nothing"}))
assert items == AP

Q3 = cyclic_place([2, 2, 3, 3])
assert Q3 == [2, 2, 3, 3]
HOME_ROWS = [("1 to n", "v - 1", "every number 1..n once (or mostly)"), ("0 to n - 1", "v", "every number 0..n-1 once"), ("lo to lo + n - 1", "v - lo", "any run of n consecutive numbers")]

lesson(
    "arrays-hashing",
    "cyclic-sort",
    """
    When an array holds the numbers 1 to n (or nearly so), every value has an obvious home: value v belongs at index
    v - 1. Swap each value into its home, and in O(n) time with no extra memory the array is sorted, and every value
    that's missing or doubled shows up as a slot holding the wrong number.
    """,
    [
        ("idea", "The idea", [
            """
            Think of a row of numbered parking spaces, 1 to 5, and five cars with matching numbers that parked in the
            wrong spaces. You don't need a clever sorting algorithm. Walk to space 1: car 3 is there, so drive it to space
            3 (and whatever was in space 3 comes back with you to space 1). Keep doing that until the car in space 1 is
            car 1, then move on to space 2. Every move puts one car in its final spot, so you're done after at most four
            moves.

            That's cyclic sort. It isn't a general-purpose sort; it only works because each value tells you exactly where
            it belongs. But when that's true, it beats O(n log n) sorting and needs no extra memory.
            """,
            fig(Row(DEMO, slots=True, label="parked anywhere"), Row(sorted(DEMO), st={k: "found" for k in range(5)}, slots=True, label="every value at index v - 1"),
                caption="Each value names its own home. Moving it there takes one swap, and it never has to move again."),
            key("""
            If values are 1 to n, value `v` belongs at index `v - 1`. At each index, keep swapping the current value to its
            home until the index holds its own value (or a duplicate), then move on. Each swap fixes one value for good, so
            it's O(n).
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The same tell as *In-place index marking*: values tied to the array's length ("1 to n", "0 to n", "n + 1
            numbers from 1 to n"), together with O(n) time and O(1) extra space. Questions about missing numbers,
            duplicates, the smallest missing positive, or "put each number in its place".

            Marking and cyclic sort solve many of the same problems. Choose cyclic sort when it helps to have values
            physically in place (afterwards, slot `i` either holds `i + 1` or tells you something is wrong), and marking
            when you'd rather keep everything where it is.

            Not a fit:

            - Values not tied to the length (arbitrary integers). They have no home index. Use real sorting or hashing.
            - You mustn't reorder the input. Cyclic sort rearranges it (copy it first, or use marking and restore).
            - Junk values (0, negatives, numbers bigger than n) are fine, but they have no home. They need a rule: leave
              them where they are and skip them.
            """,
            table(["values are", "home of v", "works for"], *HOME_ROWS),
        ]),
        ("theory", "Why it works", [
            """
            ### Every swap finishes a value

            When we swap `nums[i]` into index `home`, the value now at `home` is exactly `home + 1`. It's in its final
            place, and the algorithm never moves a value that's already home (the check `nums[home] != nums[i]` would be
            false for it). So each swap permanently places one value. There are only `n` values, so there are at most `n`
            swaps (in fact at most `n - 1`, since the last value is placed automatically).

            The index `i` only moves forward, and it moves exactly `n` times. Every loop iteration either swaps or moves
            `i`, so there are at most about `2n` iterations. That's O(n), even though there's a `while` loop that sometimes
            stays on the same index for a while.

            ### Why duplicates don't loop forever

            Suppose `nums[i]` is 4 and index 3 already holds a 4. Swapping them would change nothing, and we'd swap again
            forever. The check `nums[home] != nums[i]` catches exactly this: if home already has the right value, the one
            at `i` is an extra copy, so leave it and move on. It sits in some other value's slot, which tells you that
            other value is missing.

            ### What the array tells you afterwards

            After the placement pass, every value that appears at least once is sitting in its home. So for each index `i`:

            - if `nums[i] == i + 1`, then `i + 1` is present;
            - otherwise `i + 1` is missing, and whatever sits there is an extra copy of some value.

            That single scan answers "which numbers are missing", "which are doubled", "what's the first missing one".

            ### Cycles

            A permutation (every value exactly once) breaks into **cycles**. Start at any index, look at its value, jump to
            that value's home, and repeat; you always come back to where you started. Cyclic sort fixes one cycle at a
            time: the swaps at an index walk around its cycle until it closes. Here are the cycles of `{PERM}`:
            """.replace("{PERM}", str(PERM)),
            table(["cycle (following each value to its home)", "length"], *cyc_rows),
            fig(Row(PERM, st=cyc_state, slots=True, label="each colour is one cycle"),
                caption=f"{len(CYCLES)} cycles. A cycle of length 1 is a value that's already home."),
            """
            Thinking in cycles is useful well beyond sorting. Rearranging an array by a list of destinations, rotating in
            place, and several counting questions all come down to "follow the cycle, carrying one value".
            """,
        ]),
        ("template", "The template", [
            """
            Put every value of an array holding numbers from 1 to `n` into its home, in place. Values can repeat; extra
            copies end up in the slots of the missing values.
            """,
            code(
                "Cyclic placement",
                PLACE,
                [
                    ("start", "Start at index 0."),
                    ("loop", "Keep going until every index has been settled."),
                    ("home", "Where the current value belongs. Values must be 1 to `n` for this to be a valid index; junk "
                             "values would need to be skipped before this line."),
                    ("check", "Is the home free of this value? If home already holds the same number (because it's home, or "
                              "because this is a duplicate), there's nothing to do."),
                    ("swap", "Send the value home. Whatever was there comes to index `i`, and we look at it next without "
                             "moving `i`.",
                     {"python": "The tuple swap works because `home` was computed beforehand; writing `nums[nums[i] - 1]` on the left would go wrong mid-swap."}),
                    ("next", "Index `i` is settled: it holds its own value or an extra copy. Move on.",
                     {"c": "C works on the caller's array in place and returns nothing."}),
                    ("ret", "Every value that appears is home. Each slot holding the wrong number marks a missing value."),
                ],
                PLACE_RUN,
                "cyclic_place([3, 1, 5, 4, 2]); cyclic_place([4, 3, 4, 1, 3])",
            ),
        ]),
        ("trace", "Trace it by hand", [
            "First a clean permutation. Watch index 0 do most of the work, then the rest are already home:",
            walk(cw),
            "Now with repeats and gaps. The interesting moment is when a value's home already holds a copy of it:",
            walk(dw),
            f"""
            The result is `{DUP_OUT}`. The slots that don't hold their own number are {', '.join(f'index {k} (holding {v})' for k, v in MISFITS)}.
            So {', '.join(str(k + 1) for k, _ in MISFITS)} are missing, and the values sitting there are the extra copies.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Values that start at 0

            For values 0 to `n - 1`, the home of `v` is index `v` itself. Everything else is identical. In general, for any
            block of `n` consecutive numbers starting at `lo`, the home of `v` is `v - lo`.

            ### Junk values

            If the array can hold 0, negatives or numbers bigger than `n`, they have no home. Add a check before the swap:
            if `v < 1 or v > n`, treat it like a duplicate and move on. After the pass, those junk values sit in the slots
            of missing numbers, just like extra copies.

            ### Rearranging by a list of destinations

            Say each item must move to a given index: item `k` goes to `dest[k]`. With a second array that's trivial. With
            one spare variable, follow the cycles: pick up an item, drop it at its destination, pick up the one that was
            there, and keep going until the loop comes back to where it started.
            """,
            walk(aw),
        ]),
        ("variations", "Variations", [
            """
            ### Applying a reordering in place

            The routine from *More examples*. To know which items have already moved, it marks visited destinations with
            `~` (bitwise NOT, which turns 0 into -1 so even index 0 can be marked) and restores them at the end.
            """,
            code(
                "Move every item to its destination, in place",
                APPLY,
                [
                    ("n", "The number of items."),
                    ("start", "Try every index as the start of a cycle."),
                    ("skip", "A negative destination means this index was already handled as part of an earlier cycle."),
                    ("carry", "Pick up the item at `start`. `j` is where it's going. Mark `start` as visited."),
                    ("cycle", "Walk around the cycle until it comes back to `start`."),
                    ("drop", "Put the carried item down at `j`, and pick up the item that was there.",
                     {"cpp": "`swap(items[j], carry)` does both at once."}),
                    ("follow", "Go to where the newly carried item is heading, marking this index as visited."),
                    ("close", "Back at the start: the carried item is the one whose destination is `start`."),
                    ("restore", "Undo the `~` marks so `dest` is unchanged for the caller.",
                     {"c": "C rearranges the caller's array in place and returns nothing."}),
                    ("ret", "The rearranged items."),
                ],
                APPLY_RUN,
                "apply_in_place([10, 20, 30, 40, 50, 60], dest=[2, 0, 1, 5, 4, 3]); then print dest",
            ),
            """
            The second line of output shows `dest` came back exactly as it went in.

            ### Cyclic sort or index marking?

            Both use "value v belongs at index v - 1", both are O(n) time and O(1) extra space, and both work on the
            same kinds of question. Marking leaves the array in place and only flips signs, so it's easy to restore.
            Cyclic sort moves values, so afterwards you can read off which value sits where, which is sometimes exactly
            what the answer needs. If you're unsure, try both on a small example and see which makes the answer easier
            to read.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Each swap places one value for good, so there are at most `n - 1` swaps. The index moves forward `n` times. So
            the loop runs at most about `2n` times: O(n) time. Extra memory is O(1): an index and a temporary for the
            swap. The scan afterwards is another O(n).

            The in-place reordering visits every index once as part of exactly one cycle, so it's O(n) too, with O(1)
            extra memory (the marks live in `dest` and are undone).
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Comparison sort, then scan", "O(n log n)", "O(1) to O(n)"],
                ["Hash set of values", "O(n) on average", "O(n)"],
                ["Index marking", "O(n)", "O(1)"],
                ["Cyclic sort", "O(n)", "O(1)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            Compute the home index into a variable before swapping: `nums[i], nums[home] = nums[home], nums[i]`. Writing
            `nums[i], nums[nums[i] - 1] = …` is a classic bug, because Python assigns left to right and `nums[i]` has already
            changed by the time the second target is worked out.

            ### Java

            No built-in swap for arrays; use a temporary. For-each loops can't be used here, because the index doesn't
            always advance.

            ### C++

            `std::swap(nums[i], nums[home])`. Use an index loop (`while`), not a range-for, for the same reason as Java.

            ### C

            A temporary for the swap. Pass `n` explicitly, and check `1 ≤ v ≤ n` before indexing if junk values are
            possible.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Infinite loops on duplicates. Always compare `nums[home]` with `nums[i]`, not `home` with `i`.
            - Advancing `i` after a swap. The value that came back to `i` hasn't been placed yet; stay on `i`.
            - Values with no home (0, negatives, larger than `n`). Check the range before using a value as an index.
            - Mixing up 1-based and 0-based homes: `v - 1` versus `v`.
            - Python's swap with a computed index on the left side.
            - Modifying the caller's array when that's not allowed. Copy it first.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why is cyclic sort O(n) even though it has a loop that can stay on the same index several times?",
                 "Every swap puts one value in its final place, and placed values never move again, so there are at most n - 1 swaps in total. The index moves forward n times. So the total number of iterations is at most about 2n."),
                ("What happens without the `nums[home] != nums[i]` check when a value is duplicated?",
                 "The two equal values would be swapped with each other forever, since swapping them changes nothing and the loop never advances."),
                ("After cyclic placement of [2, 2, 3, 3], what's in the array and what does it tell you?",
                 f"It stays {Q3}. The 2 at index 0 finds a 2 already at its home (index 1), so it's an extra copy and stays put; the 3 at index 3 does the same. Indices 0 and 3 hold the wrong numbers, so 1 and 4 are missing, and 2 and 3 are the doubled values."),
                ("Values are 0 to n - 1. What changes?",
                 "Only the home: value v belongs at index v instead of v - 1."),
                ("In `apply_in_place`, why mark with `~` rather than making the destination negative?",
                 "Destination 0 can't be made negative (-0 is 0), so index 0 couldn't be marked. `~0` is -1, and applying `~` again restores it."),
            ),
        ]),
    ],
)
