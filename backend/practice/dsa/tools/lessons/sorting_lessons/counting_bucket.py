"""Lesson: Counting and bucket sort (Sorting, pattern 3)."""
from lesson import Bars, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

COUNT = {
    "python": """
        def sort_by_age(people, max_age):
            count = [0] * (max_age + 1)                     #@count
            for _, age in people:                           #@count
                count[age] += 1                             #@count
            start, total = [0] * (max_age + 1), 0           #@starts
            for age in range(max_age + 1):                  #@starts
                start[age] = total                          #@starts
                total += count[age]                         #@starts
            out = [None] * len(people)                      #@place
            for person in people:                           #@place
                out[start[person[1]]] = person              #@slot
                start[person[1]] += 1                       #@slot
            return out                                      #@ret
    """,
    "java": """
        record Person(String name, int age) {}

        static Person[] sortByAge(Person[] people, int maxAge) {
            int[] count = new int[maxAge + 1];              //@count
            for (Person p : people) count[p.age()]++;       //@count
            int[] start = new int[maxAge + 1];              //@starts
            for (int age = 0, total = 0; age <= maxAge; age++) {    //@starts
                start[age] = total;                         //@starts
                total += count[age];                        //@starts
            }
            Person[] out = new Person[people.length];       //@place
            for (Person p : people)                         //@place
                out[start[p.age()]++] = p;                  //@slot
            return out;                                     //@ret
        }
    """,
    "cpp": """
        struct Person {
            string name;
            int age;
        };

        vector<Person> sortByAge(const vector<Person>& people, int maxAge) {
            vector<int> count(maxAge + 1, 0);               //@count
            for (auto& p : people) count[p.age]++;          //@count
            vector<int> start(maxAge + 1, 0);               //@starts
            for (int age = 0, total = 0; age <= maxAge; age++) {    //@starts
                start[age] = total;                         //@starts
                total += count[age];                        //@starts
            }
            vector<Person> out(people.size());              //@place
            for (auto& p : people)                          //@place
                out[start[p.age]++] = p;                    //@slot
            return out;                                     //@ret
        }
    """,
    "c": """
        typedef struct {
            const char* name;
            int age;
        } Person;

        void sortByAge(const Person* people, int n, int maxAge, Person* out) {
            int* count = calloc(maxAge + 1, sizeof(int));   //@count
            for (int i = 0; i < n; i++) count[people[i].age]++;     //@count
            int* start = calloc(maxAge + 1, sizeof(int));   //@starts
            for (int age = 0, total = 0; age <= maxAge; age++) {    //@starts
                start[age] = total;                         //@starts
                total += count[age];                        //@starts
            }
            for (int i = 0; i < n; i++)                     //@place
                out[start[people[i].age]++] = people[i];    //@slot
            free(count);                                    //@ret
            free(start);                                    //@ret
        }
    """,
}
COUNT_RUN = {
    "python": """
        for name, age in sort_by_age([("ivy", 30), ("al", 25), ("bo", 30), ("cy", 22), ("di", 25)], 40):
            print(name, age)
    """,
    "java": """
        public static void main(String[] args) {
            Person[] ps = {new Person("ivy", 30), new Person("al", 25), new Person("bo", 30), new Person("cy", 22), new Person("di", 25)};
            for (Person p : sortByAge(ps, 40)) System.out.println(p.name() + " " + p.age());
        }
    """,
    "cpp": """
        int main() {
            vector<Person> ps = {{"ivy", 30}, {"al", 25}, {"bo", 30}, {"cy", 22}, {"di", 25}};
            for (auto& p : sortByAge(ps, 40)) cout << p.name << " " << p.age << "\\n";
        }
    """,
    "c": """
        int main(void) {
            Person ps[] = {{"ivy", 30}, {"al", 25}, {"bo", 30}, {"cy", 22}, {"di", 25}}, out[5];
            sortByAge(ps, 5, 40, out);
            for (int i = 0; i < 5; i++) printf("%s %d\\n", out[i].name, out[i].age);
            return 0;
        }
    """,
}

RADIX = {
    "python": """
        def radix_sort(nums):
            out = list(nums)                                #@copy
            biggest = max(out, default=0)                   #@copy
            place = 1                                       #@place
            while biggest // place > 0:                     #@digits
                count = [0] * 10                            #@count
                for x in out:                               #@count
                    count[x // place % 10] += 1             #@count
                for d in range(1, 10):                      #@ends
                    count[d] += count[d - 1]                #@ends
                nxt = [0] * len(out)                        #@back
                for x in reversed(out):                     #@back
                    d = x // place % 10                     #@back
                    count[d] -= 1                           #@back
                    nxt[count[d]] = x                       #@back
                out = nxt                                   #@next
                place *= 10                                 #@next
            return out                                      #@ret
    """,
    "java": """
        static int[] radixSort(int[] nums) {
            int[] out = nums.clone();                       //@copy
            int biggest = 0;                                //@copy
            for (int x : out) biggest = Math.max(biggest, x);   //@copy
            for (long place = 1; biggest / place > 0; place *= 10) {    //@digits
                int[] count = new int[10];                  //@count
                for (int x : out) count[(int) (x / place % 10)]++;  //@count
                for (int d = 1; d < 10; d++) count[d] += count[d - 1];  //@ends
                int[] next = new int[out.length];           //@back
                for (int i = out.length - 1; i >= 0; i--)   //@back
                    next[--count[(int) (out[i] / place % 10)]] = out[i];    //@back
                out = next;                                 //@next
            }
            return out;                                     //@ret
        }
    """,
    "cpp": """
        vector<int> radixSort(vector<int> out) {
            int biggest = out.empty() ? 0 : *max_element(out.begin(), out.end());   //@copy
            for (long long place = 1; biggest / place > 0; place *= 10) {   //@digits
                int count[10] = {0};                        //@count
                for (int x : out) count[x / place % 10]++;  //@count
                for (int d = 1; d < 10; d++) count[d] += count[d - 1];  //@ends
                vector<int> next(out.size());               //@back
                for (int i = (int)out.size() - 1; i >= 0; i--)  //@back
                    next[--count[out[i] / place % 10]] = out[i];    //@back
                out = std::move(next);                         //@next
            }
            return out;                                     //@ret
        }
    """,
    "c": """
        void radixSort(int* a, int n) {
            int biggest = 0;                                //@copy
            for (int i = 0; i < n; i++) if (a[i] > biggest) biggest = a[i];     //@copy
            int* next = malloc((n > 0 ? n : 1) * sizeof(int));  //@copy
            for (long long place = 1; biggest / place > 0; place *= 10) {   //@digits
                int count[10] = {0};                        //@count
                for (int i = 0; i < n; i++) count[a[i] / place % 10]++;     //@count
                for (int d = 1; d < 10; d++) count[d] += count[d - 1];  //@ends
                for (int i = n - 1; i >= 0; i--)            //@back
                    next[--count[a[i] / place % 10]] = a[i];    //@back
                memcpy(a, next, n * sizeof(int));           //@next
            }
            free(next);                                     //@ret
        }
    """,
}
RADIX_RUN = {
    "python": """
        print(*radix_sort([170, 45, 75, 90, 802, 24, 2, 66]))
        print(*radix_sort([5, 0, 5, 3]))
    """,
    "java": """
        static void show(int[] a) {
            StringBuilder sb = new StringBuilder();
            for (int x : a) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
        }

        public static void main(String[] args) {
            show(radixSort(new int[] {170, 45, 75, 90, 802, 24, 2, 66}));
            show(radixSort(new int[] {5, 0, 5, 3}));
        }
    """,
    "cpp": """
        void show(const vector<int>& a) {
            for (size_t i = 0; i < a.size(); i++) cout << (i ? " " : "") << a[i];
            cout << "\\n";
        }

        int main() {
            show(radixSort({170, 45, 75, 90, 802, 24, 2, 66}));
            show(radixSort({5, 0, 5, 3}));
        }
    """,
    "c": """
        static void show(const int* a, int n) {
            for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
        }

        int main(void) {
            int a[] = {170, 45, 75, 90, 802, 24, 2, 66}, b[] = {5, 0, 5, 3};
            radixSort(a, 8);
            radixSort(b, 4);
            show(a, 8);
            show(b, 4);
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

sort_by_age = py(COUNT["python"], "sort_by_age")
radix_sort = py(RADIX["python"], "radix_sort")

PEOPLE = [("ivy", 30), ("al", 25), ("bo", 30), ("cy", 22), ("di", 25)]
MAXAGE = 40
BY_AGE = sort_by_age(PEOPLE, MAXAGE)
assert BY_AGE == sorted(PEOPLE, key=lambda p: p[1])
WIN = list(range(20, 32))  # the ages drawn


def tag(p):
    return f"{p[0]} {p[1]}"


PRESENT = sorted({a for _, a in PEOPLE})
cw = Steps("`sort_by_age` on five people, ages 0 to 40. No comparisons at all: count, work out where each age starts, then drop everyone in.")
count = [0] * (MAXAGE + 1)
start = [None] * (MAXAGE + 1)
out = [None] * len(PEOPLE)


def cw_panels(st_in=None, st_bar=None, st_out=None):
    return (Row([tag(p) for p in PEOPLE], st=st_in, slots=True, label="people"),
            Bars([count[v] for v in WIN], labels=WIN, st=st_bar, label="count of each age (20 to 31 shown)", top=2),
            Row(list(out), st=st_out, slots=True, label="output"),
            M({f"start[{a}]": ("–" if start[a] is None else start[a]) for a in PRESENT}))


cw.step("The people as given. Ages are small whole numbers, so each age gets its own counter, all starting at 0.", *cw_panels())
for k, (n, a) in enumerate(PEOPLE):
    count[a] += 1
    cw.step(f"Pass 1, counting: {n} is {a}, so the counter for {a} goes up to {count[a]}.", *cw_panels({k: "active"}, {WIN.index(a): "active"}))
total = 0
for a in range(MAXAGE + 1):
    start[a] = total
    total += count[a]
cw.step("Running totals turn counts into starting positions. Age " + ", age ".join(f"{a} starts at {start[a]}" for a in PRESENT)
        + ": each age starts right after all the younger people.", *cw_panels())
for k, p in enumerate(PEOPLE):
    pos = start[p[1]]
    out[pos] = tag(p)
    start[p[1]] += 1
    cw.step(f"Pass 2, placing: {p[0]} ({p[1]}) goes to index {pos}, the next free slot for age {p[1]}. That age's start moves on to {start[p[1]]}.",
            *cw_panels({k: "active"}, {WIN.index(p[1]): "active"}, {pos: "found"}))
cw.steps[-1]["text"] += " Equal ages came out in their original order (al before di, ivy before bo): the sort is stable."
assert out == [tag(p) for p in BY_AGE]
CW_LEGEND = {"active": "the person (and age) being handled", "found": "just placed"}

# Radix sort, pass by pass, showing the digit each pass sorts on.
RX = [170, 45, 75, 90, 802, 24, 2, 66]
RX_OUT = radix_sort(RX)
assert RX_OUT == sorted(RX)
names = {1: "ones", 10: "tens", 100: "hundreds"}
rw = Steps(f"`radix_sort({RX})`, one digit at a time, starting with the ones.")
cur, place = list(RX), 1


def rw_panels(nums, place, st=None, buckets=None):
    digits = [x // place % 10 for x in nums] if place else [None] * len(nums)
    return (Row(nums, st=st, slots=True, label="numbers"),
            Row(digits, st=st, label="the digit this pass sorts by"),
            M(buckets or {"buckets": "–"}))


rw.step("Three digits at most (802), so three passes. Each pass is a stable counting sort on one digit, which has only 10 possible values.",
        *rw_panels(cur, 0))
while max(RX) // place > 0:
    rw.step(f"Pass on the {names[place]} digit. Read each number's {names[place]} digit (a missing digit counts as 0).", *rw_panels(cur, place, {k: "active" for k in range(len(cur))}))
    buckets = {d: [x for x in cur if x // place % 10 == d] for d in range(10)}
    cur = [x for d in range(10) for x in buckets[d]]
    rw.step(f"Stable counting sort on that digit: digit 0 first, then 1, and so on. Numbers with the same {names[place]} digit keep the order they already had.",
            *rw_panels(cur, place, {k: "found" for k in range(len(cur))}, {f"digit {d}": " ".join(map(str, v)) for d, v in buckets.items() if v}))
    place *= 10
rw.steps[-1]["text"] += " That was the last digit, so the whole array is sorted."
assert cur == RX_OUT
RW_LEGEND = {"active": "the digit being read", "found": "sorted by this digit"}

# Bucket sort on fractions.
FR = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51, 0.91]
NB = 5
BK = {b: sorted(x for x in FR if int(x * NB) == b) for b in range(NB)}
bucket_rows = [(f"[{b / NB:.1f}, {(b + 1) / NB:.1f})", " ".join(f"{x:.2f}" for x in sorted(x for x in FR if int(x * NB) == b)) or "empty") for b in range(NB)]

# Cost comparison: n + k vs n log n.
COST_ROWS = []
import math  # noqa: E402

for n, k in [(10**6, 101), (10**6, 10**6), (1000, 10**9)]:
    COST_ROWS.append((f"{n:,}", f"{k:,}", f"{n + k:,}", f"{round(n * math.log2(n)):,}"))

PLAIN = [3, 0, 2, 3, 1, 0, 3]
PLAIN_COUNTS = [PLAIN.count(v) for v in range(4)]

lesson(
    "sorting",
    "counting-bucket",
    """
    When the values are small whole numbers (ages, grades, digits, letters), you don't need to compare anything. Count
    how many times each value appears, and the sorted order falls straight out of the counts in O(n + k) time, where k
    is the number of possible values. Radix sort repeats the trick one digit at a time, and bucket sort spreads values
    into ranges first.
    """,
    [
        ("idea", "The idea", [
            f"""
            A teacher has a hundred quiz papers, each scored 0 to 10, and wants them in order. Comparing papers two at a
            time would work, but there's a faster way: make eleven piles, one for each score, and drop each paper on its
            pile. Then pick up the piles from 0 to 10. Every paper was touched twice, and not a single comparison was
            made.

            That's **counting sort**. It works whenever each value can be turned into a small index. The simplest form
            just counts: for `{PLAIN}` the counts of 0, 1, 2 and 3 are `{PLAIN_COUNTS}`, so the sorted array is two 0s,
            one 1, one 2 and three 3s.

            When the items carry more than their key (people sorted by age, records by grade), you can't just write the
            numbers out again. Instead, turn the counts into starting positions and drop each item into the next free
            slot for its key. Items with the same key stay in their original order, so the sort is stable.
            """,
            fig(Row(PLAIN, slots=True, label="values 0 to 3"), Bars(PLAIN_COUNTS, labels=[0, 1, 2, 3], label="counts"), Row(sorted(PLAIN), slots=True, label="read the counts back out"),
                caption="No comparisons: one pass to count, one pass to write."),
            key("""
            If keys are integers in `0..k-1`: count each key, turn the counts into starting positions with a running total,
            then place every item at `start[key]++`. O(n + k) time, stable. For bigger numbers, do it one digit at a
            time from the last digit (radix sort).
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The values come from a small, known range: grades 0 to 100, ages, letters `a` to `z`, digits, colours,
            ratings 1 to 5. Or the question demands O(n) sorting, which comparison sorts can't give. Or you need to group items by
            a small key, such as "by how many times they appear" (a count is at most `n`).

            Not a fit:

            - The range is huge compared with the number of items: 1,000 values spread up to 10⁹ would need a billion
              counters. Sort normally, or use radix sort.
            - Keys aren't integers and can't be mapped to small integers (arbitrary strings, real numbers with no known
              spread). Use a comparison sort, or bucket sort if the values are spread evenly over a known interval.
            """,
            table(["n items", "k possible keys", "counting sort: n + k", "comparison sort: n log₂ n"], *COST_ROWS),
            "Counting wins by a mile when `k` is small, and loses badly when `k` dwarfs `n`.",
        ]),
        ("theory", "Why it works", [
            """
            ### Counts become positions

            After counting, `count[v]` is how many items have key `v`. All items with smaller keys come first, so the
            first item with key `v` goes at index `count[0] + count[1] + … + count[v - 1]`. A running total over the counts
            computes all those starting positions in O(k).

            ### Placing items keeps them stable

            Walk the input from the front and put each item at `start[key]`, then move `start[key]` on by one. Two items
            with the same key are placed in the order they're met, so they come out in their original order. The same
            works walking from the *back* if you keep *end* positions and move them backwards instead; radix sort below
            does it that way.

            ### Why there's no n log n here

            The n log n limit is for sorts that only *compare* values. Counting sort uses each value as an array index,
            which tells it far more than one yes/no answer at a time. The price is memory: one counter per possible key.

            ### Radix sort: one digit at a time

            Numbers up to 999 have three digits, and each digit has just 10 possible values. Sort by the *last* digit
            with a stable counting sort, then by the middle digit, then by the first. Why does that work? After the pass
            on a digit, the numbers are sorted by the digits from there to the end. The next pass sorts by a more
            important digit, and because it's stable, numbers that tie on it keep the order of their less important
            digits. After the last pass, they're sorted by everything.

            With `d` digits, that's `d` passes of O(n + 10): O(d · n) overall. For 32-bit numbers, sorting by a byte at a
            time (k = 256) needs only 4 passes.

            ### Bucket sort: ranges instead of exact values

            If values are spread fairly evenly over a known range, such as fractions between 0 and 1, split the range
            into `n` equal buckets, drop each value into its bucket, sort each (small) bucket, and read them out in order.
            On even data each bucket gets about one value, so it's O(n) on average. Here are some values in 5 buckets:
            """,
            table(["bucket", "values in it (sorted)"], *bucket_rows),
            """
            If the data clumps, most values land in one bucket and you're back to the cost of whatever sorts the buckets.
            """,
        ]),
        ("template", "The template", [
            "Sort people by age (0 to `max_age`), keeping people of the same age in their original order.",
            code(
                "Stable counting sort by a small key",
                COUNT,
                [
                    ("count", "One counter per possible age, and one pass to fill them in."),
                    ("starts", "A running total turns counts into starting positions: age `a` starts after everyone younger."),
                    ("place", "A fresh output array, and one more pass over the input, front to back."),
                    ("slot", "Each person goes in the next free slot for their age, and that slot moves on.",
                     {"java": "`start[p.age()]++` uses the slot, then moves it on, in one expression.",
                      "cpp": "`start[p.age]++` uses the slot, then moves it on.",
                      "c": "`start[...]++` uses the slot, then moves it on."}),
                    ("ret", "Everyone sorted by age, ties in input order.", {"c": "The caller provides `out`; free the two counter arrays."}),
                ],
                COUNT_RUN,
                "sort_by_age([(\"ivy\", 30), (\"al\", 25), (\"bo\", 30), (\"cy\", 22), (\"di\", 25)], max_age=40)",
            ),
        ]),
        ("trace", "Trace it by hand", [
            "Watch the counters, then the starting positions, then the placement:",
            walk(cw, legend=CW_LEGEND),
        ]),
        ("examples", "More examples", [
            """
            ### Letters

            Sorting the letters of a word only needs 26 counters (`ch - 'a'` is the index). Checking whether two words are
            anagrams is the same counts compared, with no sorting at all; that's *Frequency counting* again.

            ### A range that doesn't start at 0

            Temperatures from -30 to 50 are 81 possible values. Shift every key by the minimum (`t + 30`), so the indices
            are 0 to 80. Work out the minimum and maximum first if they aren't given.

            ### Grouping by how often something happens

            Counting sort isn't only for sorting the input values. If you've counted how many times each item appears,
            those counts are integers between 1 and `n`, so items can be grouped by their count into `n` buckets without
            any comparison sort. That turns "most frequent first" into O(n).

            ### Numbers with several digits
            """,
            walk(rw, legend=RW_LEGEND),
        ]),
        ("variations", "Variations", [
            """
            ### Radix sort (least significant digit first)

            Counting sort on each digit, from the ones digit up. This version counts, turns counts into *end* positions,
            and places values walking backwards, which keeps each pass stable. It handles non-negative numbers; for
            negatives, sort them separately (or offset every value by the minimum).
            """,
            code(
                "Radix sort, base 10",
                RADIX,
                [
                    ("copy", "Work on a copy and find the biggest value, which decides how many digits to process.",
                     {"c": "C sorts the caller's array in place, with one scratch array for each pass's output."}),
                    ("place", "Start with the ones digit."),
                    ("digits", "Keep going while the biggest number still has a digit at this place.",
                     {"java": "`place` is a `long`, so multiplying by 10 can't overflow past the biggest `int`.",
                      "cpp": "`place` is `long long`, so it can't overflow.",
                      "c": "`place` is `long long`, so it can't overflow."}),
                    ("count", "Count how many numbers have each digit (0 to 9) at this place."),
                    ("ends", "Running totals: `count[d]` becomes the position just past the last number with digit `d`."),
                    ("back", "Walk backwards and place each number just before its digit's end position. Going backwards "
                             "keeps numbers with the same digit in their current order: stability, which radix sort "
                             "depends on."),
                    ("next", "This pass is done; move to the next digit.",
                     {"cpp": "`std::move` hands the vector over without copying.",
                      "c": "Copy the pass's output back into `a`."}),
                    ("ret", "Sorted.", {"c": "Free the scratch array."}),
                ],
                RADIX_RUN,
                "radix_sort([170, 45, 75, 90, 802, 24, 2, 66]); ([5, 0, 5, 3])",
            ),
            """
            ### Counting without a placement pass

            When the items *are* the keys (plain numbers), skip the starting positions: count, then write each value out
            `count[v]` times. It's shorter, but it can't carry other data along, and it isn't meaningful to call it
            stable.

            ### Buckets with a size you choose

            Bucket sort doesn't need one bucket per value, so pick a bucket width that suits the question. In some
            problems the trick is that `n` values between a minimum and a maximum can't fill every bucket of a certain
            width, so the answer must lie *between* buckets, and you never sort inside a bucket at all.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Counting sort: O(n + k) time, O(n + k) extra space (the counters, and the output array when items carry data).
            Radix sort: O(d · (n + b)) for `d` digits in base `b`, with O(n + b) extra space. Bucket sort: O(n) on average
            for evenly spread data, but as bad as the inner sort when the data clumps.
            """,
            table(
                ["Approach", "Time", "Extra space", "Needs"],
                ["Comparison sort", "O(n log n)", "O(1) to O(n)", "a way to compare"],
                ["Counting sort", "O(n + k)", "O(n + k)", "small integer keys"],
                ["Radix sort", "O(d · (n + b))", "O(n + b)", "fixed-length integer (or string) keys"],
                ["Bucket sort", "O(n) average", "O(n)", "evenly spread values in a known range"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `[0] * (k + 1)` for counters. `collections.Counter` counts, but for a dense small range a list is faster and
            keeps the keys in order for free. `max(nums, default=0)` handles an empty list.

            ### Java

            `new int[k + 1]` is already zeroed. A `record` with a small key field is a neat way to carry data through a
            stable counting sort. For radix sort, keep the place value in a `long`.

            ### C++

            `vector<int> count(k + 1, 0)`. `*max_element` finds the range (check for an empty vector first). For huge
            inputs, a byte-wise radix sort (`x >> (8 * pass) & 255`) is among the fastest ways to sort integers.

            ### C

            `calloc` gives zeroed counters; remember to `free` them. Watch for negative keys: they'd index before the
            array. Shift by the minimum first.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - A range far bigger than `n`: billions of counters. Check `k` before choosing counting sort.
            - Negative values used directly as indices. Shift by the minimum.
            - Forgetting the `+ 1`: values `0..k` need `k + 1` counters.
            - Walking forwards with *end* positions (or backwards with start positions), which reverses equal items and
              breaks stability; radix sort then gives wrong answers.
            - Radix sort starting from the most significant digit without handling each group separately.
            - Overflow in radix sort's place value for numbers near the top of `int`.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why isn't counting sort limited by the n log n lower bound?",
                 "That bound applies to sorts that only compare pairs of values. Counting sort uses each value as an array index, which isn't a comparison."),
                ("How do you turn counts into starting positions?",
                 "A running total: start[v] is the sum of the counts of all smaller keys."),
                ("Why must each pass of radix sort be stable?",
                 "The later pass sorts by a more important digit. Items that tie on it must keep the order the earlier passes gave them, which is the order of their less important digits."),
                ("You need to sort 1,000 numbers between 0 and 10⁹. Counting sort?",
                 "No: it would need a billion counters for a thousand items. Use a comparison sort, or radix sort by bytes."),
                ("When does bucket sort lose its O(n) average?",
                 "When values clump into a few buckets. Then the inner sorts do all the work, as if there were no buckets."),
            ),
        ]),
    ],
)
