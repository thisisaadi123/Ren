"""Arrays & Hashing: index marking."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def double_booked():
    b = [5, 1, 4, 5, 2, 1, 7]
    n = len(b)
    want = sorted(x for x in set(b) if b.count(x) == 2)
    assert want == [1, 5]

    w1 = Steps("For each room 1 … n, scan the bookings and count it.")
    found = []
    for x in range(1, n + 1):
        c = b.count(x)
        if c == 2:
            found.append(x)
        w1.step(f"Room {x}: {c} booking{'s' if c != 1 else ''}" + (" → booked twice." if c == 2 else "."), Row(b, st={i: ("answer" if c == 2 else "found") for i, v in enumerate(b) if v == x}, slots=True), Vars(twice=str(found)))
    w1.step(f"Answer {found}.", Row(b, slots=True), result=found)

    w2 = Steps("Tally bookings per room in a count array, then read the rooms with count 2 in order.")
    cnt = [0] * (n + 1)
    for i, v in enumerate(b):
        cnt[v] += 1
        w2.step(f"Booking {v}: count[{v}] = {cnt[v]}.", Row(b, st={i: "active"}, slots=True), Row(cnt[1:], st={v - 1: "new"}, label="count of room 1 … n"))
    w2.step(f"Rooms with count 2, left to right: {want}.", Row(cnt[1:], st={x - 1: "answer" for x in want}, label="count of room 1 … n"), result=want)

    w3 = Steps("Use the sign of slot v − 1 as a 'room v seen' flag. Meeting an already negative slot means a second booking.")
    a = b[:]
    twice = []
    w3.step("Every value is a room 1 … n, so `value − 1` is a valid slot. A negative slot means 'that room was seen'.", Row(a, slots=True))
    for i in range(n):
        v = abs(a[i])
        j = v - 1
        if a[j] < 0:
            twice.append(v)
            w3.step(f"Read {v} (index {i}): slot {j} is already negative, so room {v} was seen before. Twice!", Row(a, st={i: "active", j: "answer"}, slots=True), Vars(twice=str(twice)))
        else:
            a[j] = -a[j]
            w3.step(f"Read {v} (index {i}): slot {j} was positive. Flip it to mark room {v} as seen.", Row(a, st={i: "active", j: "new"}, slots=True), Vars(twice=str(twice)))
    w3.step(f"Found in reading order {twice}; sort to get {sorted(twice)}.", Row(a, slots=True), result=sorted(twice))

    w4 = Steps("Add n to slot v − 1 for every booking of room v. Afterwards slot i holds original + n × (bookings of room i + 1).")
    a = b[:]
    w4.step(f"n = {n}. Read each value as (value − 1) mod n + 1 so additions made earlier don't hide it.", Row(a, slots=True))
    for i in range(n):
        v = (a[i] - 1) % n + 1
        a[v - 1] += n
        w4.step(f"Index {i} holds room {v}: slot {v - 1} += {n} → {a[v - 1]}.", Row(list(a), st={i: "active", v - 1: "new"}, slots=True))
    res = [i + 1 for i in range(n) if a[i] > 2 * n]
    w4.step(f"Slots above 2n = {2 * n} were bumped twice: rooms {res}, already in order. Then each slot is restored with (value − 1) mod n + 1.", Row(a, st={i: "answer" for i in range(n) if a[i] > 2 * n}, slots=True), result=res)
    assert res == want

    sol(
        "double-booked",
        summary="""
            Every room number is between 1 and n, so it also names a slot of the array (`room − 1`). That lets the
            array itself record which rooms have been seen, either with a sign or by adding n per booking, so no
            extra memory is needed. Adding n even keeps the answer in increasing order for free.
        """,
        question=[
            """
            `bookings` has n entries, each a room number from 1 to n, and no room appears more than twice. Return
            the rooms that appear **exactly twice**, in increasing order.

            - **Values 1 … n and length n:** every value is a valid index after subtracting 1. That's the
              property every clever approach here relies on.
            - **At most twice** means "seen before" is enough to identify a double booking: there's never a third
              copy to worry about.
            - **Sorted output**, even though the bookings come in any order.
            - **The challenge:** O(n) time with O(1) extra space besides the answer. A count array would be O(n)
              extra space.
            """
        ],
        think=[
            """
            Take `bookings = [5, 1, 4, 5, 2, 1, 7]` (n = 7). Rooms 1 and 5 each appear twice: the answer is
            `[1, 5]`.

            The easy way is a count array with one slot per room. But look at the input: it **is** an array with
            one slot per room. Slot 0 can stand for room 1, slot 1 for room 2, and so on. We just need to record
            information in it **without destroying** the values still to be read.
            """,
            fig(Row(b, slots=True), Row([f"room {i + 1}" for i in range(n)], label="slot i stands for room i + 1"),
                caption="Each slot keeps its own value and can also carry a mark for its room."),
            """
            Two ways to keep both pieces of information in one slot:

            - **Sign:** values are positive, so making a slot negative can mean "this room was seen", and
              `abs()` still recovers the value.
            - **Adding n:** values are at most n, so adding n once per booking stores a count in the "tens place";
              `(x − 1) mod n + 1` recovers the original value and `(x − 1) div n` the count.
            """,
        ],
        approaches=[
            approach(
                "Count each room by scanning",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each room 1 … n, count its bookings with a full scan; rooms with count 2 go into the answer, which comes out sorted because rooms are checked in order."],
                walk=w1,
                build=["For each room `x` from 1 to n, count how many bookings equal `x`.", "If the count is 2, append `x`.", "Return the list."],
                code={
                    "python": """
                        class Solution:
                            def findDoubleBooked(self, bookings: List[int]) -> List[int]:
                                n = len(bookings)
                                return [x for x in range(1, n + 1) if bookings.count(x) == 2]  #@scan
                    """,
                    "java": """
                        class Solution {
                            public int[] findDoubleBooked(int[] bookings) {
                                int n = bookings.length;
                                List<Integer> out = new ArrayList<>();
                                for (int x = 1; x <= n; x++) {  //@scan
                                    int c = 0;  //@scan
                                    for (int v : bookings) if (v == x) c++;  //@scan
                                    if (c == 2) out.add(x);  //@scan
                                }
                                return out.stream().mapToInt(Integer::intValue).toArray();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findDoubleBooked(vector<int>& bookings) {
                                int n = bookings.size();
                                vector<int> out;
                                for (int x = 1; x <= n; x++) {  //@scan
                                    if (count(bookings.begin(), bookings.end(), x) == 2) out.push_back(x);  //@scan
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* findDoubleBooked(int* bookings, int bookingsSize, int* returnSize) {
                            int n = bookingsSize;
                            int* out = malloc(n * sizeof(int));
                            *returnSize = 0;
                            for (int x = 1; x <= n; x++) {  //@scan
                                int c = 0;  //@scan
                                for (int i = 0; i < n; i++) if (bookings[i] == x) c++;  //@scan
                                if (c == 2) out[(*returnSize)++] = x;  //@scan
                            }
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("scan", "Rooms in increasing order, each counted with a full scan. Count 2 means double-booked.", {"c": "Append into `out` and grow `*returnSize`; at most n/2 rooms can be doubled, so n slots is plenty."}),
                    ("ret", "Already sorted, because rooms were checked from 1 upwards.", {"java": "Convert the list to an `int[]`."}),
                ],
                complexity=["**Time O(n²):** n scans of n bookings. **Space O(1)** besides the answer."],
                limits=["Every room needs its own full scan. One pass that tallies all rooms at once replaces n passes."],
                slow=True,
            ),
            approach(
                "Count array",
                "better",
                "O(n)",
                "O(n)",
                idea=["One pass fills `count[room]`. A second pass over rooms 1 … n collects those with count 2, in increasing order."],
                walk=w2,
                build=["Make `count` with n + 1 zeros.", "Add 1 to `count[v]` for each booking.", "Collect every room `x` with `count[x] == 2`, from 1 to n."],
                code={
                    "python": """
                        class Solution:
                            def findDoubleBooked(self, bookings: List[int]) -> List[int]:
                                n = len(bookings)
                                count = [0] * (n + 1)  #@tally
                                for v in bookings:  #@tally
                                    count[v] += 1  #@tally
                                return [x for x in range(1, n + 1) if count[x] == 2]  #@read
                    """,
                    "java": """
                        class Solution {
                            public int[] findDoubleBooked(int[] bookings) {
                                int n = bookings.length;
                                int[] count = new int[n + 1];  //@tally
                                for (int v : bookings) count[v]++;  //@tally
                                List<Integer> out = new ArrayList<>();  //@read
                                for (int x = 1; x <= n; x++) if (count[x] == 2) out.add(x);  //@read
                                return out.stream().mapToInt(Integer::intValue).toArray();  //@read
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findDoubleBooked(vector<int>& bookings) {
                                int n = bookings.size();
                                vector<int> count(n + 1, 0);  //@tally
                                for (int v : bookings) count[v]++;  //@tally
                                vector<int> out;  //@read
                                for (int x = 1; x <= n; x++) if (count[x] == 2) out.push_back(x);  //@read
                                return out;  //@read
                            }
                        };
                    """,
                    "c": """
                        int* findDoubleBooked(int* bookings, int bookingsSize, int* returnSize) {
                            int n = bookingsSize;
                            int* count = calloc(n + 1, sizeof(int));  //@tally
                            for (int i = 0; i < n; i++) count[bookings[i]]++;  //@tally
                            int* out = malloc(n * sizeof(int));  //@read
                            *returnSize = 0;  //@read
                            for (int x = 1; x <= n; x++) if (count[x] == 2) out[(*returnSize)++] = x;  //@read
                            free(count);  //@read
                            return out;  //@read
                        }
                    """,
                },
                lines=[
                    ("tally", "Rooms are 1 … n, so they index the count array directly (slot 0 unused)."),
                    ("read", "Walking rooms upward gives the answer already sorted.", {"c": "Free the counts; the caller frees `out`."}),
                ],
                complexity=["**Time O(n).** **Space O(n)** for the counts."],
                limits=["The count array duplicates something we already have: an array of n slots indexed by room. The problem asks for O(1) extra space, so the marks should go into the input itself."],
            ),
            approach(
                "Mark seen rooms with a minus sign",
                "better",
                "O(n + d log d)",
                "O(1)",
                idea=[
                    """
                    Read each value `v` as `abs(v)` (it may have been negated already). Look at slot `v − 1`: if it's
                    negative, room `v` was seen before, so it's double-booked; otherwise negate it to mark room `v` as
                    seen. Duplicates are discovered in input order, so sort them at the end, and flip the signs back so
                    the caller's array is unchanged.
                    """
                ],
                walk=w3,
                build=["For each index i: `v = abs(bookings[i])`, `j = v − 1`.", "If `bookings[j] < 0`, append `v` (second booking). Otherwise set `bookings[j] = −bookings[j]`.", "Restore every slot with `abs`, sort the answer, return it."],
                code={
                    "python": """
                        class Solution:
                            def findDoubleBooked(self, bookings: List[int]) -> List[int]:
                                twice = []
                                for i in range(len(bookings)):  #@loop
                                    v = abs(bookings[i])  #@read
                                    j = v - 1  #@read
                                    if bookings[j] < 0:  #@seen
                                        twice.append(v)  #@seen
                                    else:  #@mark
                                        bookings[j] = -bookings[j]  #@mark
                                for i in range(len(bookings)):  #@restore
                                    bookings[i] = abs(bookings[i])  #@restore
                                return sorted(twice)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] findDoubleBooked(int[] bookings) {
                                List<Integer> twice = new ArrayList<>();
                                for (int i = 0; i < bookings.length; i++) {  //@loop
                                    int v = Math.abs(bookings[i]);  //@read
                                    int j = v - 1;  //@read
                                    if (bookings[j] < 0) twice.add(v);  //@seen
                                    else bookings[j] = -bookings[j];  //@mark
                                }
                                for (int i = 0; i < bookings.length; i++) bookings[i] = Math.abs(bookings[i]);  //@restore
                                Collections.sort(twice);  //@ret
                                return twice.stream().mapToInt(Integer::intValue).toArray();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findDoubleBooked(vector<int>& bookings) {
                                vector<int> twice;
                                for (size_t i = 0; i < bookings.size(); i++) {  //@loop
                                    int v = abs(bookings[i]);  //@read
                                    int j = v - 1;  //@read
                                    if (bookings[j] < 0) twice.push_back(v);  //@seen
                                    else bookings[j] = -bookings[j];  //@mark
                                }
                                for (int& x : bookings) x = abs(x);  //@restore
                                sort(twice.begin(), twice.end());  //@ret
                                return twice;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@ret
                            int p = *(const int*) a, q = *(const int*) b;  //@ret
                            return (p > q) - (p < q);  //@ret
                        }  //@ret

                        int* findDoubleBooked(int* bookings, int bookingsSize, int* returnSize) {
                            int* twice = malloc(bookingsSize * sizeof(int));
                            *returnSize = 0;
                            for (int i = 0; i < bookingsSize; i++) {  //@loop
                                int v = abs(bookings[i]);  //@read
                                int j = v - 1;  //@read
                                if (bookings[j] < 0) twice[(*returnSize)++] = v;  //@seen
                                else bookings[j] = -bookings[j];  //@mark
                            }
                            for (int i = 0; i < bookingsSize; i++) bookings[i] = abs(bookings[i]);  //@restore
                            qsort(twice, *returnSize, sizeof(int), cmpInt);  //@ret
                            return twice;  //@ret
                        }
                    """,
                },
                lines=[
                    ("loop", "One pass over the bookings."),
                    ("read", "The value here may already carry a mark (a minus sign put there by an earlier booking), so `abs` recovers the room number. Its flag lives in slot `room − 1`."),
                    ("seen", "The flag is already set: this is the room's second booking (there's never a third)."),
                    ("mark", "First time: set the flag by negating the slot. The slot's own value survives as its absolute value."),
                    ("restore", "Undo the marks so the caller gets their array back unchanged."),
                    ("ret", "Duplicates were found in input order, so sort them.", {"c": "`qsort` with an overflow-safe comparator."}),
                ],
                complexity=["**Time O(n + d log d)** for d double-booked rooms (at most n/2): one pass plus sorting the answer. **Space O(1)** extra besides the answer."],
                limits=["The sign only says \"seen or not\", so duplicates are noticed in input order and must be sorted. Storing a small **count** in each slot instead lets a final left-to-right pass emit them already sorted."],
            ),
            approach(
                "Count in place by adding n",
                "best",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    For every booking of room `v`, add n to slot `v − 1`. A slot's original value is between 1 and n,
                    so after the pass slot `i` holds `original + n × (bookings of room i + 1)`:

                    - the original value is `(x − 1) mod n + 1` (that's how each value is read during the pass,
                      even if n has already been added to it);
                    - the room was booked twice exactly when `x > 2n`.

                    A final pass over slots 0 … n − 1 lists double-booked rooms in increasing order and restores
                    every slot.
                    """
                ],
                walk=w4,
                build=[
                    "For each index i: `v = (bookings[i] − 1) mod n + 1`, then `bookings[v − 1] += n`.",
                    "For each slot i in order: if `bookings[i] > 2n`, append room `i + 1`.",
                    "Restore the slot: `bookings[i] = (bookings[i] − 1) mod n + 1`.",
                ],
                code={
                    "python": """
                        class Solution:
                            def findDoubleBooked(self, bookings: List[int]) -> List[int]:
                                n = len(bookings)
                                for i in range(n):  #@add
                                    v = (bookings[i] - 1) % n + 1  #@add
                                    bookings[v - 1] += n  #@add
                                twice = []  #@read
                                for i in range(n):  #@read
                                    if bookings[i] > 2 * n:  #@read
                                        twice.append(i + 1)  #@read
                                    bookings[i] = (bookings[i] - 1) % n + 1  #@restore
                                return twice  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] findDoubleBooked(int[] bookings) {
                                int n = bookings.length;
                                for (int i = 0; i < n; i++) {  //@add
                                    int v = (bookings[i] - 1) % n + 1;  //@add
                                    bookings[v - 1] += n;  //@add
                                }
                                List<Integer> twice = new ArrayList<>();  //@read
                                for (int i = 0; i < n; i++) {  //@read
                                    if (bookings[i] > 2 * n) twice.add(i + 1);  //@read
                                    bookings[i] = (bookings[i] - 1) % n + 1;  //@restore
                                }
                                return twice.stream().mapToInt(Integer::intValue).toArray();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findDoubleBooked(vector<int>& bookings) {
                                int n = bookings.size();
                                for (int i = 0; i < n; i++) {  //@add
                                    int v = (bookings[i] - 1) % n + 1;  //@add
                                    bookings[v - 1] += n;  //@add
                                }
                                vector<int> twice;  //@read
                                for (int i = 0; i < n; i++) {  //@read
                                    if (bookings[i] > 2 * n) twice.push_back(i + 1);  //@read
                                    bookings[i] = (bookings[i] - 1) % n + 1;  //@restore
                                }
                                return twice;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* findDoubleBooked(int* bookings, int bookingsSize, int* returnSize) {
                            int n = bookingsSize;
                            for (int i = 0; i < n; i++) {  //@add
                                int v = (bookings[i] - 1) % n + 1;  //@add
                                bookings[v - 1] += n;  //@add
                            }
                            int* twice = malloc(n * sizeof(int));  //@read
                            *returnSize = 0;  //@read
                            for (int i = 0; i < n; i++) {  //@read
                                if (bookings[i] > 2 * n) twice[(*returnSize)++] = i + 1;  //@read
                                bookings[i] = (bookings[i] - 1) % n + 1;  //@restore
                            }
                            return twice;  //@ret
                        }
                    """,
                },
                lines=[
                    ("add", "Recover the room stored at `i`, then add n to that room's slot: one \"tick\" per booking. A slot can reach n + 2n = 3n ≤ 3 × 10⁵, far from overflowing. `(x − 1) mod n + 1` peels the ticks off: the original value minus 1 is in 0 … n − 1, so the remainder is untouched by multiples of n."),
                    ("read", "Two ticks push a slot above 2n (its original value is at least 1). Reading slots left to right lists the rooms in increasing order, with no sorting."),
                    ("restore", "Remove the ticks so the caller's array is exactly as it was."),
                    ("ret", "The double-booked rooms, already sorted."),
                ],
                complexity=["**Time O(n):** two passes. **Space O(1)** extra besides the answer, and the input ends up unchanged."],
            ),
        ],
        takeaways=[
            """
            - When values are `1 … n` in an array of length n, **value − 1 is an index**, so the array can be its
              own lookup table.
            - Hide extra information in a slot without losing its value: flip the **sign** for a yes/no flag, or
              add **multiples of n** for a small count (read back with `mod` and `div`).
            - Undo the marks afterwards if the caller might still use the array.
            """
        ],
    )


@problem
def first_missing_ticket():
    nums = [5, 3, -2, 1, 9, 2]
    n = len(nums)
    k = 1
    while k in nums:
        k += 1
    assert k == 4

    w1 = Steps("Try 1, 2, 3, … and scan the list for each.")
    for x in range(1, k + 1):
        hit = [i for i, v in enumerate(nums) if v == x]
        if hit:
            w1.step(f"{x}: found at index {hit[0]}.", Row(nums, st={hit[0]: "found"}, slots=True))
        else:
            w1.step(f"{x}: scanned all {n} values, not there.", Row(nums, st={i: "dim" for i in range(n)}, slots=True), result=x)

    w2 = Steps(f"The answer is at most n + 1 = {n + 1}. Flag which of 1 … {n + 1} appear, then find the first gap.")
    flags = [None] * (n + 1)
    for i, v in enumerate(nums):
        if 1 <= v <= n + 1:
            flags[v - 1] = v
            w2.step(f"{v} is in range: flag it.", Row(nums, st={i: "active"}, slots=True), Row(flags, st={v - 1: "new"}, label="present? 1 … n + 1"))
        else:
            w2.step(f"{v} is outside 1 … {n + 1}: it can't affect the answer. Ignore it.", Row(nums, st={i: "dim"}, slots=True), Row(flags, label="present? 1 … n + 1"))
    w2.step(f"First empty flag: {k}.", Row(flags, st={k - 1: "answer"}, label="present? 1 … n + 1"), result=k)

    w3 = Steps("Cyclic sort: swap each value v in 1 … n into slot v − 1. Then the first slot not holding its own number is the answer.")
    a = nums[:]
    w3.step("Goal: slot i holds i + 1 whenever that value exists.", Row(a, slots=True))
    for i in range(n):
        while 1 <= a[i] <= n and a[a[i] - 1] != a[i]:
            j = a[i] - 1
            w3.step(f"Slot {i} holds {a[i]}, whose home is slot {j} (holding {a[j]}). Swap.", Row(list(a), st={i: "active", j: "mark"}, ptr={"i": i}, slots=True))
            a[i], a[j] = a[j], a[i]
        w3.step(f"Slot {i} now holds {a[i]}: " + ("its own number." if a[i] == i + 1 else "out of range or a duplicate, leave it."), Row(list(a), st={i: "found" if a[i] == i + 1 else "dim"}, ptr={"i": i}, slots=True))
    w3.step(f"Slot {k - 1} doesn't hold {k}: the answer is {k}.", Row(a, st={q: "found" for q in range(k - 1)} | {k - 1: "answer"}, slots=True), result=k)

    w4 = Steps("Sign marking: clean out-of-range values, then make slot v − 1 negative for every v in 1 … n.")
    a = nums[:]
    w4.step("Step 1: anything outside 1 … n can't matter. Replace it with n + 1 so every value is positive.", Row(a, slots=True))
    for i in range(n):
        if not 1 <= a[i] <= n:
            a[i] = n + 1
    w4.step(f"Now all values are positive; {n + 1} means 'ignore'.", Row(list(a), st={i: "dim" for i in range(n) if a[i] == n + 1}, slots=True))
    for i in range(n):
        v = abs(a[i])
        if v <= n:
            a[v - 1] = -abs(a[v - 1])
            w4.step(f"Read {v}: make slot {v - 1} negative ('{v} is present').", Row(list(a), st={i: "active", v - 1: "new"}, slots=True))
        else:
            w4.step(f"Read {v}: out of range, skip.", Row(list(a), st={i: "dim"}, slots=True))
    w4.step(f"First slot still positive: {k - 1}, so {k} is missing.", Row(a, st={k - 1: "answer"}, slots=True), result=k)

    sol(
        "first-missing-ticket",
        summary="""
            The answer is always between 1 and n + 1 (n numbers can cover at most 1 … n). So only values in
            1 … n matter, and each has a natural slot `v − 1` in the array itself. Mark those slots in place (with
            a sign, or by swapping values home) and the first unmarked slot is the answer: O(n) time, O(1) extra
            space.
        """,
        question=[
            """
            Return the smallest positive integer that isn't in `nums`.

            - **Junk is allowed:** zeros, negatives and huge values (up to 2³¹ − 1) appear and must simply be
              ignored.
            - **Duplicates are allowed** and change nothing.
            - **The hard part is the requirement:** O(n) time **and** O(1) extra space. A hash set gives O(n) time
              but O(n) space; sorting gives O(1) space but O(n log n) time.
            - **Overflow trap:** values reach `−2³¹`, whose absolute value doesn't fit in a 32-bit `int`. Code
              that calls `abs` on raw input in Java, C++ or C must avoid that.
            """
        ],
        think=[
            """
            Take `nums = [5, 3, −2, 1, 9, 2]` (n = 6). Counting up: 1 ✓, 2 ✓, 3 ✓, **4** ✗. The answer is 4.

            The key observation: **the answer is at most n + 1.** With n numbers, the best they can do is cover
            1, 2, …, n exactly, and then the answer is n + 1. If anything is missing from 1 … n, the answer is
            smaller. So:

            - values ≤ 0 or > n (like −2 and 9 here) can never change the answer;
            - only the n values 1 … n matter, and there are exactly n slots, one per value: value `v` ↔ slot `v − 1`.
            """,
            fig(Row(nums, slots=True, st={2: "dim", 4: "dim"}), Row([1, 2, 3, None, 5, None], st={3: "answer"}, label="values 1 … 6 present?"),
                caption="−2 and 9 are junk. Of 1 … 6, the first one missing is 4."),
            """
            That turns the problem into "mark which of 1 … n appear, then find the first unmarked one". With an
            extra array that's easy. To meet O(1) space, the **input array itself** must hold the marks, which is
            what the last two approaches do.
            """,
        ],
        approaches=[
            approach(
                "Count up and scan",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["Check 1, 2, 3, … in turn; for each, scan the whole list. The first one not found is the answer. At most n + 1 candidates are needed."],
                walk=w1,
                build=["Start at `k = 1`.", "While `k` is in the list (by scanning), increase `k`.", "Return `k`."],
                code={
                    "python": """
                        class Solution:
                            def firstMissing(self, nums: List[int]) -> int:
                                k = 1  #@init
                                while k in nums:  #@scan
                                    k += 1  #@scan
                                return k  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int firstMissing(int[] nums) {
                                for (int k = 1; ; k++) {  //@init
                                    boolean found = false;  //@scan
                                    for (int v : nums) if (v == k) { found = true; break; }  //@scan
                                    if (!found) return k;  //@ret
                                }
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int firstMissing(vector<int>& nums) {
                                int k = 1;  //@init
                                while (find(nums.begin(), nums.end(), k) != nums.end()) k++;  //@scan
                                return k;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int firstMissing(int* nums, int numsSize) {
                            for (int k = 1; ; k++) {  //@init
                                bool found = false;  //@scan
                                for (int i = 0; i < numsSize && !found; i++) found = nums[i] == k;  //@scan
                                if (!found) return k;  //@ret
                            }
                        }
                    """,
                },
                lines=[
                    ("init", "Candidates start at 1, the smallest positive integer."),
                    ("scan", "Look for the candidate in the whole list; if it's there, try the next one."),
                    ("ret", "The first candidate not found. It's at most n + 1, so the loop always ends."),
                ],
                complexity=["**Time O(n²):** up to n + 1 scans of n values. **Space O(1).**"],
                limits=["Each membership test is a scan. Since only 1 … n + 1 matter, a table of n + 1 flags answers them in O(1)."],
                slow=True,
            ),
            approach(
                "Flags for 1 … n + 1",
                "better",
                "O(n)",
                "O(n)",
                idea=["Make n + 2 flags. Set the flag for every value in 1 … n + 1, ignoring everything else. The first unset flag from 1 upward is the answer."],
                walk=w2,
                build=["Make `seen` of size n + 2.", "For each value `v` with `1 ≤ v ≤ n + 1`, set `seen[v]`.", "Return the first `k ≥ 1` with `seen[k]` unset."],
                code={
                    "python": """
                        class Solution:
                            def firstMissing(self, nums: List[int]) -> int:
                                n = len(nums)
                                seen = [False] * (n + 2)  #@flags
                                for v in nums:  #@mark
                                    if 1 <= v <= n + 1:  #@mark
                                        seen[v] = True  #@mark
                                k = 1  #@find
                                while seen[k]:  #@find
                                    k += 1  #@find
                                return k  #@find
                    """,
                    "java": """
                        class Solution {
                            public int firstMissing(int[] nums) {
                                int n = nums.length;
                                boolean[] seen = new boolean[n + 2];  //@flags
                                for (int v : nums) if (v >= 1 && v <= n + 1) seen[v] = true;  //@mark
                                int k = 1;  //@find
                                while (seen[k]) k++;  //@find
                                return k;  //@find
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int firstMissing(vector<int>& nums) {
                                int n = nums.size();
                                vector<bool> seen(n + 2, false);  //@flags
                                for (int v : nums) if (v >= 1 && v <= n + 1) seen[v] = true;  //@mark
                                int k = 1;  //@find
                                while (seen[k]) k++;  //@find
                                return k;  //@find
                            }
                        };
                    """,
                    "c": """
                        int firstMissing(int* nums, int numsSize) {
                            int n = numsSize;
                            bool* seen = calloc(n + 2, sizeof(bool));  //@flags
                            for (int i = 0; i < n; i++) if (nums[i] >= 1 && nums[i] <= n + 1) seen[nums[i]] = true;  //@mark
                            int k = 1;  //@find
                            while (seen[k]) k++;  //@find
                            free(seen);  //@find
                            return k;  //@find
                        }
                    """,
                },
                lines=[
                    ("flags", "One flag per possible answer 1 … n + 1 (index 0 unused, and one spare so the search below always stops)."),
                    ("mark", "Only values in 1 … n + 1 can block an answer; junk is skipped, which also keeps the index in range."),
                    ("find", "The first unflagged value from 1 upward. n values can fill at most n of the n + 1 flags, so an empty one always exists and the loop stops by index n + 1.", {"c": "Free the flags first."}),
                ],
                complexity=["**Time O(n).** **Space O(n)** for the flags, which the problem doesn't allow."],
                limits=["The flags are a second array of size n. The input already has n slots, one for each value that matters, so the marks can live there."],
            ),
            approach(
                "Cyclic sort: put each value in its own slot",
                "better",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    Rearrange the array so that, whenever value `v` (1 ≤ v ≤ n) is present, slot `v − 1` holds it. For
                    each slot, keep swapping its value into the value's home slot until the value is out of range, or
                    its home already holds the same value (a duplicate). Then the first slot `i` not holding `i + 1`
                    gives the answer `i + 1`; if every slot is right, the answer is n + 1.
                    """
                ],
                walk=w3,
                build=[
                    "For each i: while `1 ≤ nums[i] ≤ n` and `nums[nums[i] − 1] != nums[i]`, swap `nums[i]` with `nums[nums[i] − 1]`.",
                    "Scan for the first i with `nums[i] != i + 1`; return `i + 1`.",
                    "If none, return n + 1.",
                ],
                code={
                    "python": """
                        class Solution:
                            def firstMissing(self, nums: List[int]) -> int:
                                n = len(nums)
                                for i in range(n):  #@place
                                    while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:  #@place
                                        j = nums[i] - 1  #@swap
                                        nums[i], nums[j] = nums[j], nums[i]  #@swap
                                for i in range(n):  #@find
                                    if nums[i] != i + 1:  #@find
                                        return i + 1  #@find
                                return n + 1  #@full
                    """,
                    "java": """
                        class Solution {
                            public int firstMissing(int[] nums) {
                                int n = nums.length;
                                for (int i = 0; i < n; i++) {  //@place
                                    while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {  //@place
                                        int j = nums[i] - 1;  //@swap
                                        int t = nums[i]; nums[i] = nums[j]; nums[j] = t;  //@swap
                                    }
                                }
                                for (int i = 0; i < n; i++) if (nums[i] != i + 1) return i + 1;  //@find
                                return n + 1;  //@full
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int firstMissing(vector<int>& nums) {
                                int n = nums.size();
                                for (int i = 0; i < n; i++) {  //@place
                                    while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {  //@place
                                        swap(nums[i], nums[nums[i] - 1]);  //@swap
                                    }
                                }
                                for (int i = 0; i < n; i++) if (nums[i] != i + 1) return i + 1;  //@find
                                return n + 1;  //@full
                            }
                        };
                    """,
                    "c": """
                        int firstMissing(int* nums, int numsSize) {
                            int n = numsSize;
                            for (int i = 0; i < n; i++) {  //@place
                                while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {  //@place
                                    int j = nums[i] - 1;  //@swap
                                    int t = nums[i]; nums[i] = nums[j]; nums[j] = t;  //@swap
                                }
                            }
                            for (int i = 0; i < n; i++) if (nums[i] != i + 1) return i + 1;  //@find
                            return n + 1;  //@full
                        }
                    """,
                },
                lines=[
                    ("place", "Keep working on slot `i` while its value belongs somewhere in 1 … n **and** its home doesn't already hold that value. The second condition stops endless swapping between two equal values.",
                     {"java": "The range check comes first, so `nums[i] − 1` is only computed for values 1 … n: no overflow and no out-of-range index.",
                      "cpp": "The range check comes first, so `nums[i] − 1` is only used for values 1 … n.",
                      "c": "The range check comes first, so `nums[i] − 1` is only used for values 1 … n."}),
                    ("swap", "Send the value home; whatever was there comes back to slot `i` and gets the same treatment.",
                     {"cpp": "`swap(nums[i], nums[nums[i] − 1])` is safe: both references are formed before anything changes."}),
                    ("find", "Now every present value 1 … n sits at its home. The first slot without its own number names the missing value."),
                    ("full", "Every slot holds its own number: 1 … n are all present, so the answer is n + 1."),
                ],
                complexity=[
                    """
                    **Time O(n):** every swap puts one value in its final home, and a value at home is never moved
                    again, so there are at most n swaps in total, however the `while` loops are distributed.

                    **Space O(1)** extra, but the array is rearranged.
                    """
                ],
                limits=[
                    """
                    It meets both requirements, but the swap loop is the trickiest code in this problem: the guard
                    must compare values (not indices) to avoid infinite loops on duplicates, and the O(n) bound needs
                    the "each swap finalises one value" argument. Sign marking gets the same bounds with three
                    straight passes and no swaps.
                    """
                ],
            ),
            approach(
                "Mark presence with negative signs",
                "best",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    Three passes over the array:

                    1. **Clean:** replace every value outside 1 … n with n + 1. Now everything is positive, and n + 1
                       means "ignore".
                    2. **Mark:** for each value, read `v = abs(x)`. If `v ≤ n`, make slot `v − 1` negative (if it isn't
                       already): "value v is present". The slot keeps its own value as its absolute value.
                    3. **Find:** the first slot that's still positive is `i`, and `i + 1` is missing. If none is
                       positive, the answer is n + 1.

                    Cleaning first is what makes signs safe to use as marks: no original value is negative, and no
                    `abs(−2³¹)` overflow can happen.
                    """
                ],
                walk=w4,
                build=[
                    "Replace each value `≤ 0` or `> n` with `n + 1`.",
                    "For each slot: `v = abs(nums[i])`; if `v ≤ n`, set `nums[v − 1] = −abs(nums[v − 1])`.",
                    "Return `i + 1` for the first `nums[i] > 0`, else `n + 1`.",
                ],
                code={
                    "python": """
                        class Solution:
                            def firstMissing(self, nums: List[int]) -> int:
                                n = len(nums)
                                for i in range(n):  #@clean
                                    if nums[i] <= 0 or nums[i] > n:  #@clean
                                        nums[i] = n + 1  #@clean
                                for i in range(n):  #@mark
                                    v = abs(nums[i])  #@mark
                                    if v <= n:  #@mark
                                        nums[v - 1] = -abs(nums[v - 1])  #@mark
                                for i in range(n):  #@find
                                    if nums[i] > 0:  #@find
                                        return i + 1  #@find
                                return n + 1  #@full
                    """,
                    "java": """
                        class Solution {
                            public int firstMissing(int[] nums) {
                                int n = nums.length;
                                for (int i = 0; i < n; i++) if (nums[i] <= 0 || nums[i] > n) nums[i] = n + 1;  //@clean
                                for (int i = 0; i < n; i++) {  //@mark
                                    int v = Math.abs(nums[i]);  //@mark
                                    if (v <= n) nums[v - 1] = -Math.abs(nums[v - 1]);  //@mark
                                }
                                for (int i = 0; i < n; i++) if (nums[i] > 0) return i + 1;  //@find
                                return n + 1;  //@full
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int firstMissing(vector<int>& nums) {
                                int n = nums.size();
                                for (int& x : nums) if (x <= 0 || x > n) x = n + 1;  //@clean
                                for (int i = 0; i < n; i++) {  //@mark
                                    int v = abs(nums[i]);  //@mark
                                    if (v <= n) nums[v - 1] = -abs(nums[v - 1]);  //@mark
                                }
                                for (int i = 0; i < n; i++) if (nums[i] > 0) return i + 1;  //@find
                                return n + 1;  //@full
                            }
                        };
                    """,
                    "c": """
                        int firstMissing(int* nums, int numsSize) {
                            int n = numsSize;
                            for (int i = 0; i < n; i++) if (nums[i] <= 0 || nums[i] > n) nums[i] = n + 1;  //@clean
                            for (int i = 0; i < n; i++) {  //@mark
                                int v = abs(nums[i]);  //@mark
                                if (v <= n) nums[v - 1] = -abs(nums[v - 1]);  //@mark
                            }
                            for (int i = 0; i < n; i++) if (nums[i] > 0) return i + 1;  //@find
                            return n + 1;  //@full
                        }
                    """,
                },
                lines=[
                    ("clean", "Junk can't change the answer, so overwrite it with the harmless value n + 1. After this pass every value is between 1 and n + 1, so later `abs` calls are safe (no `abs(−2³¹)`)."),
                    ("mark", "A value `v` in 1 … n marks its slot by making it negative. Using `−abs(…)` rather than plain negation keeps an already-marked slot marked when a duplicate comes along. The slot's own value is still readable as `abs`."),
                    ("find", "A slot that never got marked means its value `i + 1` never appeared."),
                    ("full", "All of 1 … n appeared, so n + 1 is the first missing."),
                ],
                complexity=["**Time O(n):** three passes. **Space O(1)** extra; the input is modified (it can be cleaned up afterwards if needed)."],
            ),
        ],
        takeaways=[
            """
            - **Bound the answer** first: the smallest missing positive of n numbers is in `1 … n + 1`.
            - With values that matter limited to `1 … n`, the array's own slots can store "present" marks: a
              minus sign, or the value parked at its home index (cyclic sort).
            - Normalise junk before marking (here to n + 1) so marks can't collide with real data, and watch out for
              `abs(INT_MIN)`.
            """
        ],
    )


@problem
def missing_seat():
    seats = [3, 0, 1, 5, 2]
    n = len(seats)
    miss = (set(range(n + 1)) - set(seats)).pop()
    assert miss == 4

    w1 = Steps("Try each seat 0 … n and scan for it.")
    for s in range(n + 1):
        hit = [i for i, v in enumerate(seats) if v == s]
        if hit:
            w1.step(f"Seat {s}: taken (index {hit[0]}).", Row(seats, st={hit[0]: "found"}, slots=True))
        else:
            w1.step(f"Seat {s}: not in the list. It's free.", Row(seats, st={i: "dim" for i in range(n)}, slots=True), result=s)
            break

    w2 = Steps("Flag each taken seat, then find the unflagged one.")
    flags = [None] * (n + 1)
    for i, v in enumerate(seats):
        flags[v] = v
        w2.step(f"Seat {v} is taken.", Row(seats, st={i: "active"}, slots=True), Row(flags, st={v: "new"}, label="seats 0 … n", slots=True))
    w2.step(f"Seat {miss} has no flag.", Row(flags, st={miss: "answer"}, label="seats 0 … n", slots=True), result=miss)

    w3 = Steps("All seats add up to 0 + 1 + … + n. Subtract the taken ones; what's left is the free seat.")
    full = n * (n + 1) // 2
    run = 0
    w3.step(f"0 + 1 + … + {n} = {n}·{n + 1}/2 = {full}.", Row(list(range(n + 1)), label="all seats"), Vars(all=full))
    for i, v in enumerate(seats):
        run += v
        w3.step(f"Add seat {v}: taken total {run}.", Row(seats, st={i: "active", **{q: "found" for q in range(i)}}, slots=True), Vars(all=full, taken=run))
    w3.step(f"{full} − {run} = {full - run}.", Row(seats, slots=True), result=full - run)

    w4 = Steps("XOR every seat number 0 … n with every taken seat. Pairs cancel (x ^ x = 0); the free seat is left.")
    acc = 0
    w4.step("Start with x = 0. XOR is order-independent and x ^ x = 0, x ^ 0 = x.", Row(seats, slots=True), Vars(x=0))
    for i, v in enumerate(seats):
        acc ^= i ^ v
        w4.step(f"x ^= index {i} ^ seat {v} → {acc}.", Row(seats, st={i: "active"}, slots=True), Vars(x=acc))
    acc ^= n
    w4.step(f"Finally x ^= n = {n} (the one index the loop never reaches) → {acc}.", Row(seats, slots=True), result=acc)

    sol(
        "missing-seat",
        summary="""
            You know exactly which numbers should be there: 0 to n. Combine all of them and all the taken seats in
            a way where every taken seat cancels its partner, and only the free seat survives. A sum does that in
            O(n) time and O(1) space; XOR does it without any risk of overflow.
        """,
        question=[
            """
            Seats are numbered 0 to n (that's **n + 1 seats**), and `seats` lists the n taken ones, all different.
            Return the one free seat.

            - **The range includes 0 and n.** For `[0, 1]` the free seat is 2; for `[1]` it's 0.
            - **Exactly one seat is free**, and all listed seats are distinct and valid.
            - **Size:** n up to 10⁵, so the total of all seat numbers, n(n + 1)/2, is about 5 × 10⁹, more than a
              32-bit `int` holds.
            """
        ],
        think=[
            """
            Take `seats = [3, 0, 1, 5, 2]` (n = 5, seats 0 … 5). By hand you'd tick off seats 0, 1, 2, 3 and 5 and
            see that 4 is unticked.

            But there's a shortcut that needs no ticking: you know the full set {0, 1, 2, 3, 4, 5}, and you know
            everything except one of them. If you **add** them all up, 0 + 1 + … + 5 = 15, and add the taken seats,
            3 + 0 + 1 + 5 + 2 = 11, the difference 15 − 11 = 4 is the free seat.
            """,
            fig(Row(list(range(n + 1)), st={4: "answer"}, label="all seats 0 … 5"), Row(seats, label="taken"), caption="Everything cancels except seat 4."),
            """
            Any operation where "a number combined with itself cancels" works. Subtraction is one; **XOR** is
            another (x ^ x = 0) and has the bonus of never overflowing.
            """,
        ],
        approaches=[
            approach(
                "Scan for each seat",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["Check seats 0, 1, …, n in turn; the first one that doesn't appear in the list is free."],
                walk=w1,
                build=["For `s` from 0 to n, scan the list for `s`.", "Return the first `s` not found."],
                code={
                    "python": """
                        class Solution:
                            def missingSeat(self, seats: List[int]) -> int:
                                for s in range(len(seats) + 1):  #@each
                                    if s not in seats:  #@scan
                                        return s  #@scan
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int missingSeat(int[] seats) {
                                for (int s = 0; s <= seats.length; s++) {  //@each
                                    boolean taken = false;  //@scan
                                    for (int v : seats) if (v == s) { taken = true; break; }  //@scan
                                    if (!taken) return s;  //@scan
                                }
                                return -1;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int missingSeat(vector<int>& seats) {
                                for (int s = 0; s <= (int) seats.size(); s++) {  //@each
                                    if (find(seats.begin(), seats.end(), s) == seats.end()) return s;  //@scan
                                }
                                return -1;  //@none
                            }
                        };
                    """,
                    "c": """
                        int missingSeat(int* seats, int seatsSize) {
                            for (int s = 0; s <= seatsSize; s++) {  //@each
                                bool taken = false;  //@scan
                                for (int i = 0; i < seatsSize && !taken; i++) taken = seats[i] == s;  //@scan
                                if (!taken) return s;  //@scan
                            }
                            return -1;  //@none
                        }
                    """,
                },
                lines=[
                    ("each", "Every seat number from 0 to n inclusive."),
                    ("scan", "Look for it in the list; the first seat not found is free."),
                    ("none", "Unreachable with valid input."),
                ],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["n + 1 scans, each answering a single membership question. A flag array answers them all after one pass."],
                slow=True,
            ),
            approach(
                "Flag the taken seats",
                "better",
                "O(n)",
                "O(n)",
                idea=["Make n + 1 flags, set one for each taken seat, then return the seat whose flag is unset."],
                walk=w2,
                build=["Make `taken` with n + 1 falses.", "Set `taken[s]` for each seat.", "Return the index that's still false."],
                code={
                    "python": """
                        class Solution:
                            def missingSeat(self, seats: List[int]) -> int:
                                taken = [False] * (len(seats) + 1)  #@flags
                                for s in seats:  #@flags
                                    taken[s] = True  #@flags
                                return taken.index(False)  #@find
                    """,
                    "java": """
                        class Solution {
                            public int missingSeat(int[] seats) {
                                boolean[] taken = new boolean[seats.length + 1];  //@flags
                                for (int s : seats) taken[s] = true;  //@flags
                                int s = 0;  //@find
                                while (taken[s]) s++;  //@find
                                return s;  //@find
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int missingSeat(vector<int>& seats) {
                                vector<bool> taken(seats.size() + 1, false);  //@flags
                                for (int s : seats) taken[s] = true;  //@flags
                                int s = 0;  //@find
                                while (taken[s]) s++;  //@find
                                return s;  //@find
                            }
                        };
                    """,
                    "c": """
                        int missingSeat(int* seats, int seatsSize) {
                            bool* taken = calloc(seatsSize + 1, sizeof(bool));  //@flags
                            for (int i = 0; i < seatsSize; i++) taken[seats[i]] = true;  //@flags
                            int s = 0;  //@find
                            while (taken[s]) s++;  //@find
                            free(taken);  //@find
                            return s;  //@find
                        }
                    """,
                },
                lines=[
                    ("flags", "One flag per seat 0 … n; each taken seat sets its own."),
                    ("find", "Exactly one flag stays unset: the free seat.", {"c": "Free the flags before returning."}),
                ],
                complexity=["**Time O(n).** **Space O(n)** for the flags."],
                limits=["We store n + 1 flags to recover a single number. Arithmetic can recover it with one running total."],
            ),
            approach(
                "Total of all seats minus the taken ones",
                "better",
                "O(n)",
                "O(1)",
                idea=["0 + 1 + … + n = n(n + 1)/2. Subtracting the sum of the taken seats leaves exactly the free seat. Use 64-bit arithmetic: the totals reach about 5 × 10⁹."],
                walk=w3,
                build=["Compute `n(n + 1)/2` as a 64-bit number.", "Subtract every taken seat.", "Return what's left."],
                code={
                    "python": """
                        class Solution:
                            def missingSeat(self, seats: List[int]) -> int:
                                n = len(seats)
                                return n * (n + 1) // 2 - sum(seats)  #@diff
                    """,
                    "java": """
                        class Solution {
                            public int missingSeat(int[] seats) {
                                long n = seats.length;
                                long left = n * (n + 1) / 2;  //@full
                                for (int s : seats) left -= s;  //@diff
                                return (int) left;  //@diff
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int missingSeat(vector<int>& seats) {
                                long long n = seats.size();
                                long long left = n * (n + 1) / 2;  //@full
                                for (int s : seats) left -= s;  //@diff
                                return (int) left;  //@diff
                            }
                        };
                    """,
                    "c": """
                        int missingSeat(int* seats, int seatsSize) {
                            long long n = seatsSize;
                            long long left = n * (n + 1) / 2;  //@full
                            for (int i = 0; i < seatsSize; i++) left -= seats[i];  //@diff
                            return (int) left;  //@diff
                        }
                    """,
                },
                lines=[
                    ("full", "The sum of every seat 0 … n by Gauss's formula, in 64 bits (about 5 × 10⁹ for n = 10⁵)."),
                    ("diff", "Remove each taken seat; only the free seat's number remains, which fits back in an `int`.", {"python": "Python integers never overflow, so the formula and `sum` can be used directly."}),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Correct, but in fixed-width languages it depends on choosing a wide enough type. Forget the 64-bit `n` and `n * (n + 1)` silently overflows. XOR needs no wide type at all."],
            ),
            approach(
                "XOR everything together",
                "best",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    XOR has three useful properties: `x ^ x = 0`, `x ^ 0 = x`, and the order doesn't matter. XOR all
                    seat numbers 0 … n together with all taken seats: every taken seat appears twice and cancels, the
                    free seat appears once and remains.

                    A compact way to include 0 … n: in the loop, XOR in both the index `i` (0 … n − 1) and `seats[i]`,
                    then XOR in `n` at the end.
                    """
                ],
                walk=w4,
                build=["`x = 0`.", "For each index i: `x ^= i ^ seats[i]`.", "`x ^= n`, then return `x`."],
                code={
                    "python": """
                        class Solution:
                            def missingSeat(self, seats: List[int]) -> int:
                                x = len(seats)  #@init
                                for i, s in enumerate(seats):  #@loop
                                    x ^= i ^ s  #@loop
                                return x  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int missingSeat(int[] seats) {
                                int x = seats.length;  //@init
                                for (int i = 0; i < seats.length; i++) x ^= i ^ seats[i];  //@loop
                                return x;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int missingSeat(vector<int>& seats) {
                                int x = seats.size();  //@init
                                for (int i = 0; i < (int) seats.size(); i++) x ^= i ^ seats[i];  //@loop
                                return x;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int missingSeat(int* seats, int seatsSize) {
                            int x = seatsSize;  //@init
                            for (int i = 0; i < seatsSize; i++) x ^= i ^ seats[i];  //@loop
                            return x;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Start with n: the one seat number the indices 0 … n − 1 below don't cover. Starting there is the same as XOR-ing it in at the end."),
                    ("loop", "Fold in every index (seat numbers 0 … n − 1) and every taken seat. Each taken seat meets its matching index somewhere in the stream and they cancel."),
                    ("ret", "Only the free seat appeared an odd number of times (once), so it's what remains. XOR never carries, so nothing can overflow."),
                ],
                complexity=["**Time O(n).** **Space O(1).** No overflow concerns."],
            ),
        ],
        takeaways=[
            """
            - When you know the full set and one element is missing, **cancel** everything that's present:
              expected sum − actual sum, or XOR of both.
            - XOR is the overflow-free cancellation: `x ^ x = 0`, `x ^ 0 = x`, order irrelevant.
            - Check sums against your integer width; n(n + 1)/2 overflows 32 bits from n ≈ 65,536.
            """
        ],
    )


@problem
def unclaimed_numbers():
    t = [3, 1, 3, 6, 1, 2]
    n = len(t)
    want = [x for x in range(1, n + 1) if x not in t]
    assert want == [4, 5]

    w1 = Steps("For each number 1 … n, scan the tickets.")
    for x in range(1, n + 1):
        hit = [i for i, v in enumerate(t) if v == x]
        w1.step(f"{x}: " + (f"on ticket {hit[0]}." if hit else "on no ticket → unclaimed."), Row(t, st={h: "found" for h in hit} if hit else {i: "dim" for i in range(n)}, slots=True), Vars(unclaimed=str([y for y in range(1, x + 1) if y not in t])))
    w1.step(f"Answer {want}.", Row(t, slots=True), result=want)

    w2 = Steps("Flag every number that appears, then list the unflagged ones.")
    flags = [None] * n
    for i, v in enumerate(t):
        flags[v - 1] = v
        w2.step(f"Ticket {v}: flag it.", Row(t, st={i: "active"}, slots=True), Row(flags, st={v - 1: "new"}, label="numbers 1 … n"))
    w2.step(f"Unflagged: {want}.", Row(flags, st={x - 1: "answer" for x in want}, label="numbers 1 … n"), result=want)

    w3 = Steps("Use the array as the flags: for each value v, make slot v − 1 negative. Slots left positive are unclaimed numbers.")
    a = t[:]
    w3.step("Values are 1 … n, so slot v − 1 can carry the mark 'v appears' as a minus sign.", Row(a, slots=True))
    for i in range(n):
        v = abs(a[i])
        already = a[v - 1] < 0
        a[v - 1] = -abs(a[v - 1])
        w3.step(f"Read {v}: slot {v - 1} " + ("is already negative (a repeat)." if already else "becomes negative."), Row(list(a), st={i: "active", v - 1: "found" if already else "new"}, slots=True))
    w3.step(f"Slots {', '.join(str(x - 1) for x in want)} stayed positive: numbers {want} never appeared. Then flip all signs back.", Row(a, st={x - 1: "answer" for x in want}, slots=True), result=want)

    sol(
        "unclaimed-numbers",
        summary="""
            Every ticket number is between 1 and n, so it names a slot of the array (`number − 1`). Mark slot
            `v − 1` negative for every value `v`; afterwards the slots that are still positive are exactly the
            numbers nobody holds. O(n) time, O(1) extra space, and the signs can be flipped back.
        """,
        question=[
            """
            There are n tickets, each showing a number from 1 to n; some numbers repeat and others are missing.
            Return the missing numbers in increasing order.

            - **Values 1 … n in an array of length n:** each value is a valid index after subtracting 1.
            - **Repeats are allowed** (any number of times) and must not confuse the marking.
            - **Increasing order** for the answer.
            - **Goal:** O(n) time and O(1) extra space apart from the answer.
            """
        ],
        think=[
            """
            Take `tickets = [3, 1, 3, 6, 1, 2]` (n = 6). The numbers present are 1, 2, 3 and 6, so 4 and 5 are
            unclaimed.

            A checklist with one box per number 1 … n solves it: tick a box for each ticket, then read off the empty
            boxes in order. The array already has n slots, so **slot `v − 1` can be number v's box**. We only need a
            way to tick a box without losing the value stored in it, and since all values are positive, a minus
            sign works perfectly.
            """,
            fig(Row(t, slots=True), Row(["1", "2", "3", "4?", "5?", "6"], st={3: "answer", 4: "answer"}, label="box for number slot + 1"),
                caption="Boxes 3 and 4 (numbers 4 and 5) never get ticked."),
        ],
        approaches=[
            approach(
                "Scan for each number",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each number 1 … n, scan the tickets; collect the ones never found. Checking in order keeps the answer sorted."],
                walk=w1,
                build=["For `x` from 1 to n: if `x` is on no ticket (scan), append it.", "Return the list."],
                code={
                    "python": """
                        class Solution:
                            def findUnclaimed(self, tickets: List[int]) -> List[int]:
                                return [x for x in range(1, len(tickets) + 1) if x not in tickets]  #@scan
                    """,
                    "java": """
                        class Solution {
                            public int[] findUnclaimed(int[] tickets) {
                                int n = tickets.length;
                                List<Integer> out = new ArrayList<>();
                                for (int x = 1; x <= n; x++) {  //@scan
                                    boolean found = false;  //@scan
                                    for (int v : tickets) if (v == x) { found = true; break; }  //@scan
                                    if (!found) out.add(x);  //@scan
                                }
                                return out.stream().mapToInt(Integer::intValue).toArray();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findUnclaimed(vector<int>& tickets) {
                                int n = tickets.size();
                                vector<int> out;
                                for (int x = 1; x <= n; x++) {  //@scan
                                    if (find(tickets.begin(), tickets.end(), x) == tickets.end()) out.push_back(x);  //@scan
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* findUnclaimed(int* tickets, int ticketsSize, int* returnSize) {
                            int n = ticketsSize;
                            int* out = malloc(n * sizeof(int));
                            *returnSize = 0;
                            for (int x = 1; x <= n; x++) {  //@scan
                                bool found = false;  //@scan
                                for (int i = 0; i < n && !found; i++) found = tickets[i] == x;  //@scan
                                if (!found) out[(*returnSize)++] = x;  //@scan
                            }
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("scan", "Every number from 1 to n, each looked up with a full scan; missing ones are collected in increasing order."),
                    ("ret", "The unclaimed numbers.", {"java": "Convert the list to an `int[]`.", "c": "The caller frees `out`; `returnSize` holds its length."}),
                ],
                complexity=["**Time O(n²).** **Space O(1)** besides the answer."],
                limits=["n separate scans. One pass that records every number at once is enough."],
                slow=True,
            ),
            approach(
                "Flag array",
                "better",
                "O(n)",
                "O(n)",
                idea=["One pass sets `seen[v]` for every ticket; a second pass over 1 … n collects the unset ones in order."],
                walk=w2,
                build=["`seen` with n + 1 falses.", "Set `seen[v]` for each ticket.", "Collect every `x` in 1 … n with `seen[x]` false."],
                code={
                    "python": """
                        class Solution:
                            def findUnclaimed(self, tickets: List[int]) -> List[int]:
                                n = len(tickets)
                                seen = [False] * (n + 1)  #@flags
                                for v in tickets:  #@flags
                                    seen[v] = True  #@flags
                                return [x for x in range(1, n + 1) if not seen[x]]  #@read
                    """,
                    "java": """
                        class Solution {
                            public int[] findUnclaimed(int[] tickets) {
                                int n = tickets.length;
                                boolean[] seen = new boolean[n + 1];  //@flags
                                for (int v : tickets) seen[v] = true;  //@flags
                                List<Integer> out = new ArrayList<>();  //@read
                                for (int x = 1; x <= n; x++) if (!seen[x]) out.add(x);  //@read
                                return out.stream().mapToInt(Integer::intValue).toArray();  //@read
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findUnclaimed(vector<int>& tickets) {
                                int n = tickets.size();
                                vector<bool> seen(n + 1, false);  //@flags
                                for (int v : tickets) seen[v] = true;  //@flags
                                vector<int> out;  //@read
                                for (int x = 1; x <= n; x++) if (!seen[x]) out.push_back(x);  //@read
                                return out;  //@read
                            }
                        };
                    """,
                    "c": """
                        int* findUnclaimed(int* tickets, int ticketsSize, int* returnSize) {
                            int n = ticketsSize;
                            bool* seen = calloc(n + 1, sizeof(bool));  //@flags
                            for (int i = 0; i < n; i++) seen[tickets[i]] = true;  //@flags
                            int* out = malloc(n * sizeof(int));  //@read
                            *returnSize = 0;  //@read
                            for (int x = 1; x <= n; x++) if (!seen[x]) out[(*returnSize)++] = x;  //@read
                            free(seen);  //@read
                            return out;  //@read
                        }
                    """,
                },
                lines=[
                    ("flags", "A box per number; each ticket ticks its number's box (repeats just tick it again)."),
                    ("read", "Unticked boxes, read in order, are the unclaimed numbers.", {"c": "Free the flags; the caller frees `out`."}),
                ],
                complexity=["**Time O(n).** **Space O(n)** for the flags."],
                limits=["The flags are a second length-n array, while the input already offers n slots indexed by number. Marking the input itself meets the O(1)-space goal."],
            ),
            approach(
                "Negate slot v − 1 for every value v",
                "best",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    For each slot, read its value as `v = abs(x)` (an earlier step may have negated it) and make slot
                    `v − 1` negative with `−abs(…)`, so repeats leave it negative instead of flipping it back. After the
                    pass, slot `i` is positive exactly when `i + 1` never appeared. Collect those in order, then restore
                    the signs.
                    """
                ],
                walk=w3,
                build=["For each slot: `v = abs(tickets[i])`; set `tickets[v − 1] = −abs(tickets[v − 1])`.", "Collect `i + 1` for every slot that's still positive.", "Flip every slot back to positive; return the list."],
                code={
                    "python": """
                        class Solution:
                            def findUnclaimed(self, tickets: List[int]) -> List[int]:
                                for x in tickets:  #@mark
                                    v = abs(x)  #@mark
                                    tickets[v - 1] = -abs(tickets[v - 1])  #@mark
                                out = [i + 1 for i, x in enumerate(tickets) if x > 0]  #@read
                                for i in range(len(tickets)):  #@restore
                                    tickets[i] = abs(tickets[i])  #@restore
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] findUnclaimed(int[] tickets) {
                                for (int x : tickets) {  //@mark
                                    int v = Math.abs(x);  //@mark
                                    tickets[v - 1] = -Math.abs(tickets[v - 1]);  //@mark
                                }
                                List<Integer> out = new ArrayList<>();  //@read
                                for (int i = 0; i < tickets.length; i++) if (tickets[i] > 0) out.add(i + 1);  //@read
                                for (int i = 0; i < tickets.length; i++) tickets[i] = Math.abs(tickets[i]);  //@restore
                                return out.stream().mapToInt(Integer::intValue).toArray();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findUnclaimed(vector<int>& tickets) {
                                for (int x : tickets) {  //@mark
                                    int v = abs(x);  //@mark
                                    tickets[v - 1] = -abs(tickets[v - 1]);  //@mark
                                }
                                vector<int> out;  //@read
                                for (int i = 0; i < (int) tickets.size(); i++) if (tickets[i] > 0) out.push_back(i + 1);  //@read
                                for (int& x : tickets) x = abs(x);  //@restore
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* findUnclaimed(int* tickets, int ticketsSize, int* returnSize) {
                            int n = ticketsSize;
                            for (int i = 0; i < n; i++) {  //@mark
                                int v = abs(tickets[i]);  //@mark
                                tickets[v - 1] = -abs(tickets[v - 1]);  //@mark
                            }
                            int* out = malloc(n * sizeof(int));  //@read
                            *returnSize = 0;  //@read
                            for (int i = 0; i < n; i++) if (tickets[i] > 0) out[(*returnSize)++] = i + 1;  //@read
                            for (int i = 0; i < n; i++) tickets[i] = abs(tickets[i]);  //@restore
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("mark", "The value being read may already carry a mark, so `abs` recovers it. Then tick number `v`'s box: make slot `v − 1` negative. `−abs(…)` (instead of `−x`) keeps a box ticked when a repeat ticks it again.",
                     {"java": "Iterating with `for (int x : tickets)` reads each slot's current value, marks included, which is why `abs` is needed.",
                      "cpp": "`for (int x : tickets)` copies each slot's current value, marks included, which is why `abs` is needed."}),
                    ("read", "A slot that's still positive was never ticked: number `i + 1` is unclaimed. Reading slots in order gives increasing numbers."),
                    ("restore", "Remove the marks so the caller's array is unchanged."),
                    ("ret", "The unclaimed numbers.", {"c": "`returnSize` holds the count; the caller frees `out`."}),
                ],
                complexity=["**Time O(n):** three passes. **Space O(1)** extra besides the answer."],
            ),
        ],
        takeaways=[
            """
            - Values in `1 … n` + array of length n = **the array can be its own checklist**.
            - Mark with `−abs(slot)` rather than `−slot`, so a repeated value can't un-mark a slot.
            - Always read values through `abs` once marking has started, and restore the array if the caller may
              still need it.
            """
        ],
    )
