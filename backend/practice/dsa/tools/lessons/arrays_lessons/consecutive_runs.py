"""Lesson: Consecutive runs with a set (Arrays & Hashing, pattern 12)."""
from lesson import Bars, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

RUN = {
    "python": """
        def longest_run(nums):
            values = set(nums)                      #@set
            best = 0                                #@best
            for x in values:                        #@loop
                if x - 1 in values:                 #@skip
                    continue                        #@skip
                length = 1                          #@start
                while x + length in values:         #@extend
                    length += 1                     #@extend
                best = max(best, length)            #@keep
            return best                             #@ret
    """,
    "java": """
        static int longestRun(int[] nums) {
            Set<Integer> values = new HashSet<>();          //@set
            for (int x : nums) values.add(x);               //@set
            int best = 0;                                   //@best
            for (int x : values) {                          //@loop
                if (values.contains(x - 1)) continue;       //@skip
                int length = 1;                             //@start
                while (values.contains(x + length)) length++;   //@extend
                best = Math.max(best, length);              //@keep
            }
            return best;                                    //@ret
        }
    """,
    "cpp": """
        int longestRun(const vector<int>& nums) {
            unordered_set<int> values(nums.begin(), nums.end());   //@set
            int best = 0;                                   //@best
            for (int x : values) {                          //@loop
                if (values.count(x - 1)) continue;          //@skip
                int length = 1;                             //@start
                while (values.count(x + length)) length++;  //@extend
                best = max(best, length);                   //@keep
            }
            return best;                                    //@ret
        }
    """,
    "c": """
        typedef struct {
            int* keys;
            bool* used;
            size_t mask;
        } IntSet;                                                           //@table

        static size_t set_slot(const IntSet* s, int key) {
            size_t i = ((uint32_t)key * 2654435761u) & s->mask;             //@table
            while (s->used[i] && s->keys[i] != key) i = (i + 1) & s->mask;  //@table
            return i;
        }

        static bool set_has(const IntSet* s, int key) {
            return s->used[set_slot(s, key)];                               //@table
        }

        int longestRun(const int* nums, int n) {
            size_t cap = 16;                                                //@set
            while (cap < 2 * (size_t)n) cap <<= 1;                          //@set
            IntSet values = {malloc(cap * sizeof(int)), calloc(cap, sizeof(bool)), cap - 1};  //@set
            for (int i = 0; i < n; i++) {                                   //@set
                size_t j = set_slot(&values, nums[i]);                      //@set
                values.used[j] = true;                                      //@set
                values.keys[j] = nums[i];                                   //@set
            }
            int best = 0;                                                   //@best
            for (size_t j = 0; j <= values.mask; j++) {                     //@loop
                if (!values.used[j]) continue;                              //@loop
                int x = values.keys[j];                                     //@loop
                if (set_has(&values, x - 1)) continue;                      //@skip
                int length = 1;                                             //@start
                while (set_has(&values, x + length)) length++;              //@extend
                if (length > best) best = length;                           //@keep
            }
            free(values.keys);                                              //@free
            free(values.used);                                              //@free
            return best;                                                    //@ret
        }
    """,
}
RUN_RUN = {
    "python": """
        print(longest_run([8, 3, 10, 1, 2, 9, 20, 11, 4, 5]))
        print(longest_run([7, 7, 7]))
        print(longest_run([-1, 0, 1, 1, -2]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(longestRun(new int[] {8, 3, 10, 1, 2, 9, 20, 11, 4, 5}));
            System.out.println(longestRun(new int[] {7, 7, 7}));
            System.out.println(longestRun(new int[] {-1, 0, 1, 1, -2}));
        }
    """,
    "cpp": """
        int main() {
            cout << longestRun({8, 3, 10, 1, 2, 9, 20, 11, 4, 5}) << "\\n";
            cout << longestRun({7, 7, 7}) << "\\n";
            cout << longestRun({-1, 0, 1, 1, -2}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {8, 3, 10, 1, 2, 9, 20, 11, 4, 5}, b[] = {7, 7, 7}, c[] = {-1, 0, 1, 1, -2};
            printf("%d\\n%d\\n%d\\n", longestRun(a, 10), longestRun(b, 3), longestRun(c, 5));
            return 0;
        }
    """,
}

BRIDGE = {
    "python": """
        def longest_with_one_added(nums):
            values = set(nums)                              #@set
            runs = {}                                       #@runs
            for x in values:                                #@runs
                if x - 1 not in values:                     #@runs
                    length = 1                              #@runs
                    while x + length in values:             #@runs
                        length += 1                         #@runs
                    runs[x] = length                        #@runs
            best = 0                                        #@best
            for start, length in runs.items():              #@each
                after = start + length + 1                  #@after
                best = max(best, length + 1 + runs.get(after, 0))   #@join
            return best                                     #@ret
    """,
    "java": """
        static int longestWithOneAdded(int[] nums) {
            Set<Integer> values = new HashSet<>();                  //@set
            for (int x : nums) values.add(x);                       //@set
            Map<Integer, Integer> runs = new HashMap<>();           //@runs
            for (int x : values) {                                  //@runs
                if (values.contains(x - 1)) continue;               //@runs
                int length = 1;                                     //@runs
                while (values.contains(x + length)) length++;       //@runs
                runs.put(x, length);                                //@runs
            }
            int best = 0;                                           //@best
            for (Map.Entry<Integer, Integer> e : runs.entrySet()) { //@each
                int start = e.getKey(), length = e.getValue();      //@each
                int after = start + length + 1;                     //@after
                best = Math.max(best, length + 1 + runs.getOrDefault(after, 0));   //@join
            }
            return best;                                            //@ret
        }
    """,
    "cpp": """
        int longestWithOneAdded(const vector<int>& nums) {
            unordered_set<int> values(nums.begin(), nums.end());    //@set
            unordered_map<int, int> runs;                           //@runs
            for (int x : values) {                                  //@runs
                if (values.count(x - 1)) continue;                  //@runs
                int length = 1;                                     //@runs
                while (values.count(x + length)) length++;          //@runs
                runs[x] = length;                                   //@runs
            }
            int best = 0;                                           //@best
            for (auto [start, length] : runs) {                     //@each
                int after = start + length + 1;                     //@after
                auto it = runs.find(after);                         //@join
                best = max(best, length + 1 + (it == runs.end() ? 0 : it->second));   //@join
            }
            return best;                                            //@ret
        }
    """,
    "c": """
        typedef struct {
            int *keys, *vals;
            bool* used;
            size_t mask;
        } IntMap;                                                           //@table

        static IntMap map_new(int n) {
            size_t cap = 16;                                                //@table
            while (cap < 2 * (size_t)n) cap <<= 1;                          //@table
            IntMap m = {malloc(cap * sizeof(int)), malloc(cap * sizeof(int)), calloc(cap, sizeof(bool)), cap - 1};  //@table
            return m;
        }

        static size_t map_slot(const IntMap* m, int key) {
            size_t i = ((uint32_t)key * 2654435761u) & m->mask;             //@table
            while (m->used[i] && m->keys[i] != key) i = (i + 1) & m->mask;  //@table
            return i;
        }

        static void map_put(IntMap* m, int key, int val) {
            size_t i = map_slot(m, key);                                    //@table
            m->used[i] = true;                                              //@table
            m->keys[i] = key;                                               //@table
            m->vals[i] = val;                                               //@table
        }

        static int map_get(const IntMap* m, int key, int missing) {
            size_t i = map_slot(m, key);                                    //@table
            return m->used[i] ? m->vals[i] : missing;                       //@table
        }

        int longestWithOneAdded(const int* nums, int n) {
            IntMap values = map_new(n), runs = map_new(n);                  //@set
            for (int i = 0; i < n; i++) map_put(&values, nums[i], 1);       //@set
            for (size_t j = 0; j <= values.mask; j++) {                     //@runs
                if (!values.used[j]) continue;                              //@runs
                int x = values.keys[j];                                     //@runs
                if (map_get(&values, x - 1, 0)) continue;                   //@runs
                int length = 1;                                             //@runs
                while (map_get(&values, x + length, 0)) length++;           //@runs
                map_put(&runs, x, length);                                  //@runs
            }
            int best = 0;                                                   //@best
            for (size_t j = 0; j <= runs.mask; j++) {                       //@each
                if (!runs.used[j]) continue;                                //@each
                int start = runs.keys[j], length = runs.vals[j];            //@each
                int after = start + length + 1;                             //@after
                int total = length + 1 + map_get(&runs, after, 0);          //@join
                if (total > best) best = total;                             //@join
            }
            free(values.keys); free(values.vals); free(values.used);        //@free
            free(runs.keys); free(runs.vals); free(runs.used);              //@free
            return best;                                                    //@ret
        }
    """,
}
BRIDGE_RUN = {
    "python": """
        print(longest_with_one_added([1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 14]))
        print(longest_with_one_added([4, 4, 4]))
        print(longest_with_one_added([10, 30]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(longestWithOneAdded(new int[] {1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 14}));
            System.out.println(longestWithOneAdded(new int[] {4, 4, 4}));
            System.out.println(longestWithOneAdded(new int[] {10, 30}));
        }
    """,
    "cpp": """
        int main() {
            cout << longestWithOneAdded({1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 14}) << "\\n";
            cout << longestWithOneAdded({4, 4, 4}) << "\\n";
            cout << longestWithOneAdded({10, 30}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 14}, b[] = {4, 4, 4}, c[] = {10, 30};
            printf("%d\\n%d\\n%d\\n", longestWithOneAdded(a, 11), longestWithOneAdded(b, 3), longestWithOneAdded(c, 2));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

longest_run = py(RUN["python"], "longest_run")
longest_with_one_added = py(BRIDGE["python"], "longest_with_one_added")

DEMO = [8, 3, 10, 1, 2, 9, 20, 11, 4, 5]
DSET = set(DEMO)
assert longest_run(DEMO) == 5
LINE = list(range(1, 12))


def line(present, st=None, label="number line 1 to 11"):
    """Values 1..11 drawn on a number line; missing ones are blank."""
    return Row([v if v in present else None for v in LINE], st={LINE.index(v): s for v, s in (st or {}).items() if v in LINE}, label=label)


RUNS = {}
for x in DSET:
    if x - 1 not in DSET:
        n = 1
        while x + n in DSET:
            n += 1
        RUNS[x] = n
run_rows = [(f"{s}" if n == 1 else f"{s} to {s + n - 1}", str(n)) for s, n in sorted(RUNS.items())]

# Walkthrough of the template, in the order values first appear.
rw = Steps(f"`longest_run({DEMO})`. Put everything in a set, then count only from the start of each run.")
rw.step("The set answers \"is v here?\" in O(1). On a number line the values fall into runs with gaps between them. 20 sits far off to the right, alone.",
        Row(DEMO, slots=True), line(DSET), M({"best": 0}))
best, order = 0, list(dict.fromkeys(DEMO))
for i, x in enumerate(order):
    pos = DEMO.index(x)
    if x - 1 in DSET:
        rw.step(f"{x}: is {x - 1} in the set? Yes. So {x} is in the middle of a run that starts further left. Don't count from here; that run gets counted once, from its start.",
                Row(DEMO, st={pos: "dim"}, ptr={"x": pos}, slots=True), line(DSET, {x: "dim", x - 1: "mark"}), M({"best": best}))
        continue
    n = 1
    while x + n in DSET:
        n += 1
    best = max(best, n)
    span = list(range(x, x + n))
    walked = f"walk right: {', '.join(map(str, span[1:]))} are all there, and {x + n} isn't" if n > 1 else f"{x + 1} isn't in the set, so the run is just {x}"
    rw.step(f"{x}: is {x - 1} in the set? No, so {x} starts a run. Now {walked}. Run length {n}.",
            Row(DEMO, st={pos: "active"}, ptr={"x": pos}, slots=True), line(DSET, {v: "found" for v in span}),
            M({"length": n, "best": best}))
rw.steps[-1]["text"] += f" Every value has been looked at once as a possible start, and walked over at most once. Longest run: {best}."

# How much walking the naive version does on one long run.
LONG = list(range(1, 9))
NAIVE = [len(LONG) - i for i in range(len(LONG))]
SMART = [len(LONG)] + [0] * (len(LONG) - 1)

# Ranges summary, worked by hand.
SUM_IN = [5, 1, 2, 9, 3, 10, 7]
SS = set(SUM_IN)
SUMMARY = []
for x in sorted(SS):
    if x - 1 not in SS:
        n = 1
        while x + n in SS:
            n += 1
        SUMMARY.append(f"{x}" if n == 1 else f"{x}→{x + n - 1}")

# Bridging one gap.
BR = [1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 14]
BR_OUT = longest_with_one_added(BR)
assert BR_OUT == 8
BS = set(BR)
BRUNS = {}
for x in sorted(BS):
    if x - 1 not in BS:
        n = 1
        while x + n in BS:
            n += 1
        BRUNS[x] = n
BLINE = list(range(1, 16))
colors = ["found", "answer", "mark", "active"]


def bline(st=None, label="1 to 15"):
    return Row([v if v in BS else None for v in BLINE], st={BLINE.index(v): s for v, s in (st or {}).items()}, label=label)


run_color = {v: colors[k % 4] for k, (s, n) in enumerate(BRUNS.items()) for v in range(s, s + n)}
bw = Steps(f"`longest_with_one_added({BR})`. Add one number of your choice. How long can the longest run get?")
bw.step("First, find every run exactly as in the template, and remember each one's start and length.", bline(run_color),
        M({f"run at {s}": n for s, n in BRUNS.items()}))
bbest = 0
for s, n in BRUNS.items():
    after = s + n + 1
    joined = BRUNS.get(after, 0)
    total = n + 1 + joined
    bbest = max(bbest, total)
    filler = s + n
    if joined:
        msg = f"The run {s}→{s + n - 1} ends just before a gap of one: {filler} is missing and {after} starts another run of {joined}. Adding {filler} joins them: {n} + 1 + {joined} = {total}."
        st = {**{v: "found" for v in range(s, s + n)}, **{v: "found" for v in range(after, after + joined)}}
    else:
        msg = f"After the run {s}→{s + n - 1}, {after} isn't a run start, so adding {filler} only makes this run one longer: {total}."
        st = {v: "found" for v in range(s, s + n)}
    bw.step(msg, bline(st), M({"this one": total, "best": bbest}))
bw.steps[-1]["text"] += f" The best you can do is {bbest}."
assert bbest == BR_OUT

DUP = [4, 4, 4, 5]

lesson(
    "arrays-hashing",
    "consecutive-runs",
    """
    To find runs of consecutive values (like 3, 4, 5, 6) in an unsorted array, put everything in a hash set and only
    start counting at a value whose predecessor is missing. Each run is then walked exactly once, from its first value,
    so the whole thing is O(n) without sorting.
    """,
    [
        ("idea", "The idea", [
            """
            Imagine the pages of a book have come loose and been shuffled, and you want to know the longest stretch of
            pages you still have in order, with nothing missing in between. You don't have to sort the pile. Spread the
            pages out so you can tell at a glance whether any page number is there. Then, for each page, ask one
            question: "is the page before this one here?"

            If it is, this page is somewhere in the middle of a stretch, so ignore it for now. If it isn't, this page is
            the *first* page of a stretch, and you count forwards from it: is the next page here, and the next? Every
            stretch gets counted once, from its first page, and no page is counted twice.

            The hash set is "spread out on the table". The "is the one before here?" check is what keeps it fast.
            """,
            fig(Row(DEMO, label="as given"), line(DSET, {v: ("found" if v in range(1, 6) else "mark") for v in DSET}),
                caption=f"The same values on a number line: runs 1→5 and 8→11, and 20 on its own (off to the right). The answer is 5."),
            key("""
            Put the values in a set. A value `x` starts a run only if `x - 1` isn't in the set. From each start, count
            `x + 1`, `x + 2`, … while they're present. Every value is walked over once, so it's O(n).
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The question is about values that follow on from each other (`v`, `v + 1`, `v + 2`, …) but the array is in no
            particular order, and the positions don't matter. "Longest consecutive sequence", "longest streak of days",
            "group the numbers into ranges", "how many runs", usually with "in O(n)" or "without sorting".

            The thing to notice is that the *order* in the array is irrelevant. Only which values are present matters.
            That's the moment to throw the values into a set.

            Not a fit:

            - The run must be consecutive in **position** (adjacent in the array), like "longest increasing
              subarray". That's a simple left-to-right scan; a set throws away positions.
            - "Longest increasing subsequence" (keep the order, values just increase). That's dynamic programming.
            - Small inputs, or when you need the values sorted anyway. Sorting and scanning (*Sort then scan*) gives
              the same runs in O(n log n) and is often simpler.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Runs are separated by gaps

            Lay the distinct values out on a number line. They clump into runs, with at least one missing number between
            neighbouring runs. Every value belongs to exactly one run, and every run has exactly one first value: the
            one whose predecessor is missing. For `{DEMO}` the runs are:
            """.replace("{DEMO}", str(DEMO)),
            table(["run", "length"], *run_rows),
            f"""
            If you think of each value as a node joined to `v + 1` when it's present, every run is a chain. The start is
            the only node with nothing joined on its left. So "find every chain and its length" becomes "find every
            start and walk right".

            ### Why skipping the middles matters

            You could start walking from *every* value. It gives the right answer, but on one long run it's slow: from the
            first value you walk the whole run, from the second you walk all but one, and so on. That's about `n² / 2`
            steps. Starting only at the run's first value walks it once.
            """,
            fig(Bars(NAIVE, labels=LONG, label="steps walked from each value, starting everywhere", top=len(LONG)),
                Bars(SMART, labels=LONG, st={0: "answer"}, label="starting only at a run's first value", top=len(LONG)),
                caption=f"On the run {LONG[0]}→{LONG[-1]}: {sum(NAIVE)} steps against {sum(SMART)}. The gap grows like n²."),
            """
            ### Counting the work

            The outer loop looks at each distinct value once and does one set lookup (`x - 1`). The inner `while` loop
            only runs from starts, and the walk from a start covers exactly that run's values. Runs don't overlap, so
            all the inner walks together cover each value once. Total: about `2n` lookups, O(n) on average.

            ### Duplicates

            The set holds each value once, so duplicates disappear before the counting starts. Loop over the **set**,
            not the original array. Looping over the array still gives the right answer, but if the start of a long run
            appears a thousand times, you'd walk that run a thousand times.
            """,
        ]),
        ("template", "The template", [
            "The length of the longest run of consecutive values, in any order, duplicates allowed.",
            code(
                "Longest run of consecutive values",
                RUN,
                [
                    ("table", "C has no hash set, so here's a small open-addressing one: a power-of-two table, at least twice "
                              "as big as the input, where a key that collides moves to the next slot."),
                    ("set", "Every distinct value, with O(1) lookups.",
                     {"cpp": "`unordered_set` can be built straight from the vector's range.",
                      "c": "Insert each value into its slot. Inserting a duplicate just finds its existing slot again."}),
                    ("best", "The longest run found so far. An empty array has no runs, so 0."),
                    ("loop", "Look at each distinct value once.",
                     {"c": "Walking the table's used slots visits each distinct value exactly once."}),
                    ("skip", "If `x - 1` is present, `x` is in the middle of a run. That run is counted from its start "
                             "instead."),
                    ("start", "`x` is the first value of a run."),
                    ("extend", "Walk right while the next value is present."),
                    ("keep", "Remember the longest."),
                    ("free", "Give the table back."),
                    ("ret", "The longest run."),
                ],
                RUN_RUN,
                "longest_run([8, 3, 10, 1, 2, 9, 20, 11, 4, 5]); ([7, 7, 7]); ([-1, 0, 1, 1, -2])",
            ),
            """
            `[7, 7, 7]` is one value, so one run of length 1. `[-1, 0, 1, 1, -2]` is the run -2 → 1: negatives work the
            same as anything else.
            """,
        ]),
        ("trace", "Trace it by hand", [
            """
            A set has no fixed order, so the code may visit the values in any order. The answer doesn't depend on it.
            Here we go in the order they first appear in the array:
            """,
            walk(rw),
        ]),
        ("examples", "More examples", [
            f"""
            ### Summarising into ranges

            Given `{SUM_IN}`, describe the values as ranges: `{', '.join(SUMMARY)}`. Find each run start the same way,
            and walk to its end. If you want the ranges in increasing order, sort the starts (there are usually far
            fewer starts than values) or, if the input is small, just sort everything and scan.

            ### A streak of days

            A user's activity log lists the dates they practised, in any order, with repeats. Turn every date into a day
            number (days since some fixed date), and the longest streak is the longest run of day numbers. Repeated
            dates collapse in the set, which is exactly what you want: practising twice on one day is still one day.

            ### Filling one gap

            Suppose you may add one number of your choice. The best place is either the end of some run (making it one
            longer) or a gap of exactly one between two runs (joining them). So find all the runs, remember each one's
            length by its start, and for each run look at the start that would sit just after a one-number gap.
            """,
            walk(bw),
        ]),
        ("variations", "Variations", [
            """
            ### Keep the runs, not just the longest

            Once the starts are found, store each run's length in a map keyed by its start. Then questions about runs
            next to each other are one lookup away: the run after `start` with a gap of one would begin at
            `start + length + 1`.
            """,
            code(
                "Longest run after adding one number",
                BRIDGE,
                [
                    ("table", "A small open-addressing hash map from `int` to `int`, used twice: once as the set of values "
                              "and once for the runs."),
                    ("set", "The distinct values."),
                    ("runs", "The template's loop, but instead of keeping only the best, store each run's length under "
                             "its start."),
                    ("best", "Best total so far."),
                    ("each", "Look at every run."),
                    ("after", "Where a run would start if it sat just past a gap of one."),
                    ("join", "Add the missing number: it makes this run one longer, and if a run starts at `after`, it "
                             "joins that one too.",
                     {"java": "`getOrDefault` gives 0 when no run starts there.",
                      "cpp": "`find` avoids `runs[after]`, which would insert a zero-length run while we're looping over the map."}),
                    ("free", "Give both tables back."),
                    ("ret", "The longest run you can make."),
                ],
                BRIDGE_RUN,
                "longest_with_one_added([1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 14]); ([4, 4, 4]); ([10, 30])",
            ),
            """
            ### Union-find

            Another way to build the runs: treat each value as its own group, and for each value `v`, merge it with the
            group of `v + 1` if that's present. The groups at the end are the runs. It's more machinery than this
            problem needs, but it's the right tool when values arrive one at a time and you need the longest run after
            every arrival.

            ### Sort and scan

            Sort, then walk the array: a run continues while `a[i] == a[i - 1] + 1`, ignores `a[i] == a[i - 1]`
            (duplicates), and breaks otherwise. O(n log n), O(1) extra space if you may sort in place. It's a fine answer
            when O(n) isn't required.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Building the set is O(n). The loop does one lookup per distinct value, and the walks from run starts cover
            each value once more, so O(n) on average overall. Extra space is the set: O(n). Storing runs adds at most one
            map entry per run.
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Walk from every value", "O(n²) worst case", "O(n)"],
                ["Sort, then scan", "O(n log n)", "O(1) to O(n)"],
                ["Set, walk only from run starts", "O(n) on average", "O(n)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `set(nums)` and `in` do everything. Iterate over the set, not the list. Python integers don't overflow, so
            `x - 1` and `x + length` are always safe.

            ### Java

            `HashSet<Integer>` boxes every value, which is fine at this size. `x - 1` overflows for
            `Integer.MIN_VALUE` and wraps to `Integer.MAX_VALUE`; if both can appear, compare as `long`.

            ### C++

            `unordered_set<int>` built from the vector's range. `count(x)` returns 0 or 1, handy as a condition. For very
            large inputs, `values.reserve(n)` avoids rehashing as it grows.

            ### C

            Write a small open-addressing set as above. Make the table at least twice the input size so probes stay
            short, and loop over its used slots to visit distinct values. `x - 1` at `INT_MIN` is undefined behaviour in
            C; widen to `long long` if the full range is possible.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            f"""
            - Walking from every value. It's correct but O(n²) on one long run. The `x - 1` check is the whole point.
            - Looping over the original array with many duplicates of a run start. Loop over the set.
            - Counting duplicates as part of a run: `{DUP}` has a run of length 2, not 4.
            - An empty input: the answer is 0, not 1.
            - Overflow at the extremes of `int` when computing `x - 1` or `x + length` in Java, C++ or C.
            - Confusing "consecutive values" with "adjacent positions". Re-read the question.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why does checking `x - 1` make the algorithm O(n)?",
                 "It means walking only starts at the first value of each run. Runs don't overlap, so all the walks together cover each value once."),
                (f"What is the longest run in {DUP}?",
                 "2 (the run 4 → 5). The set holds {4, 5}; the repeated 4s don't make the run longer."),
                ("Would the template still be correct if you looped over the array instead of the set?",
                 "Yes, it still finds the right lengths, but a run start that's repeated many times would be walked many times, so it can become slow."),
                ("When is sorting a better choice?",
                 "When the input is small, when O(n log n) is acceptable and you want O(1) extra space, or when you need the runs in increasing order anyway."),
                ("In `longest_with_one_added`, why only look at `start + length + 1`?",
                 "Adding one number can only join this run to a run that begins right after a gap of exactly one. The number that fills the gap is `start + length`, so the next run would have to begin at `start + length + 1`."),
            ),
        ]),
    ],
)
