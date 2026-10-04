"""Lesson: Frequency counting (Arrays & Hashing, pattern 1)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

FIRST_UNIQUE = {
    "python": """
        def first_unique(nums):
            count = {}                              #@make
            for x in nums:                          #@tally
                count[x] = count.get(x, 0) + 1      #@tally
            for x in nums:                          #@scan
                if count[x] == 1:                   #@hit
                    return x                        #@hit
            return -1                               #@none
    """,
    "java": """
        static int firstUnique(int[] nums) {
            Map<Integer, Integer> count = new HashMap<>();          //@make
            for (int x : nums) count.merge(x, 1, Integer::sum);     //@tally
            for (int x : nums) {                                    //@scan
                if (count.get(x) == 1) return x;                    //@hit
            }
            return -1;                                              //@none
        }
    """,
    "cpp": """
        int firstUnique(const vector<int>& nums) {
            unordered_map<int, int> count;              //@make
            count.reserve(nums.size() * 2);             //@reserve
            for (int x : nums) count[x]++;              //@tally
            for (int x : nums) {                        //@scan
                if (count[x] == 1) return x;            //@hit
            }
            return -1;                                  //@none
        }
    """,
    "c": """
        typedef struct {
            int *keys, *counts;
            bool *used;
            size_t mask;
        } CountMap;                                                         //@struct

        CountMap cm_new(size_t n) {
            size_t cap = 16;                                                //@cap
            while (cap < 2 * n) cap <<= 1;                                  //@cap
            CountMap m;
            m.keys = malloc(cap * sizeof(int));                             //@alloc
            m.counts = calloc(cap, sizeof(int));                            //@alloc
            m.used = calloc(cap, sizeof(bool));                             //@alloc
            m.mask = cap - 1;                                               //@alloc
            return m;
        }

        static size_t cm_slot(const CountMap* m, int key) {
            size_t i = ((uint32_t)key * 2654435761u) & m->mask;             //@hash
            while (m->used[i] && m->keys[i] != key) i = (i + 1) & m->mask;  //@probe
            return i;
        }

        void cm_add(CountMap* m, int key) {
            size_t i = cm_slot(m, key);                                     //@add
            m->used[i] = true;                                              //@add
            m->keys[i] = key;                                               //@add
            m->counts[i]++;                                                 //@add
        }

        int cm_get(const CountMap* m, int key) {
            size_t i = cm_slot(m, key);                                     //@get
            return m->used[i] ? m->counts[i] : 0;                           //@get
        }

        int firstUnique(const int* nums, int n) {
            CountMap count = cm_new(n);                                     //@make
            for (int i = 0; i < n; i++) cm_add(&count, nums[i]);            //@tally
            int answer = -1;                                                //@none
            for (int i = 0; i < n; i++) {                                   //@scan
                if (cm_get(&count, nums[i]) == 1) {                         //@hit
                    answer = nums[i];                                       //@hit
                    break;                                                  //@hit
                }
            }
            free(count.keys); free(count.counts); free(count.used);         //@free
            return answer;                                                  //@none
        }
    """,
}
FIRST_UNIQUE_RUN = {
    "python": """
        print(first_unique([4, 7, 4, 9, 7, 2]))
        print(first_unique([5, 5]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(firstUnique(new int[] {4, 7, 4, 9, 7, 2}));
            System.out.println(firstUnique(new int[] {5, 5}));
        }
    """,
    "cpp": """
        int main() {
            cout << firstUnique({4, 7, 4, 9, 7, 2}) << "\\n" << firstUnique({5, 5}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {4, 7, 4, 9, 7, 2}, b[] = {5, 5};
            printf("%d\\n%d\\n", firstUnique(a, 6), firstUnique(b, 2));
            return 0;
        }
    """,
}

SAME_LETTERS = {
    "python": """
        def same_letters(a, b):
            if len(a) != len(b):                    #@len
                return False                        #@len
            diff = [0] * 26                         #@make
            for ch in a:                            #@up
                diff[ord(ch) - ord('a')] += 1       #@up
            for ch in b:                            #@down
                k = ord(ch) - ord('a')              #@down
                diff[k] -= 1                        #@down
                if diff[k] < 0:                     #@neg
                    return False                    #@neg
            return True                             #@ok
    """,
    "java": """
        static boolean sameLetters(String a, String b) {
            if (a.length() != b.length()) return false;     //@len
            int[] diff = new int[26];                       //@make
            for (char ch : a.toCharArray()) diff[ch - 'a']++;   //@up
            for (char ch : b.toCharArray()) {               //@down
                if (--diff[ch - 'a'] < 0) return false;     //@neg
            }
            return true;                                    //@ok
        }
    """,
    "cpp": """
        bool sameLetters(const string& a, const string& b) {
            if (a.size() != b.size()) return false;         //@len
            int diff[26] = {0};                             //@make
            for (char ch : a) diff[ch - 'a']++;             //@up
            for (char ch : b) {                             //@down
                if (--diff[ch - 'a'] < 0) return false;     //@neg
            }
            return true;                                    //@ok
        }
    """,
    "c": """
        bool sameLetters(const char* a, const char* b) {
            if (strlen(a) != strlen(b)) return false;       //@len
            int diff[26] = {0};                             //@make
            for (const char* p = a; *p; p++) diff[*p - 'a']++;  //@up
            for (const char* p = b; *p; p++) {              //@down
                if (--diff[*p - 'a'] < 0) return false;     //@neg
            }
            return true;                                    //@ok
        }
    """,
}
SAME_LETTERS_RUN = {
    "python": """
        for a, b in [("listen", "silent"), ("table", "bleat"), ("loop", "polo"), ("eel", "lee"), ("seen", "sene"), ("aab", "abb")]:
            print(str(same_letters(a, b)).lower())
    """,
    "java": """
        public static void main(String[] args) {
            String[][] pairs = {{"listen", "silent"}, {"table", "bleat"}, {"loop", "polo"}, {"eel", "lee"}, {"seen", "sene"}, {"aab", "abb"}};
            for (String[] p : pairs) System.out.println(sameLetters(p[0], p[1]));
        }
    """,
    "cpp": """
        int main() {
            vector<pair<string, string>> pairs = {{"listen", "silent"}, {"table", "bleat"}, {"loop", "polo"}, {"eel", "lee"}, {"seen", "sene"}, {"aab", "abb"}};
            for (auto& [a, b] : pairs) cout << boolalpha << sameLetters(a, b) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* pairs[][2] = {{"listen", "silent"}, {"table", "bleat"}, {"loop", "polo"}, {"eel", "lee"}, {"seen", "sene"}, {"aab", "abb"}};
            for (int i = 0; i < 6; i++) printf("%s\\n", sameLetters(pairs[i][0], pairs[i][1]) ? "true" : "false");
            return 0;
        }
    """,
}

EQUAL_PAIRS = {
    "python": """
        def equal_pairs(nums):
            seen = [0] * 101        #@make
            pairs = 0               #@make
            for x in nums:          #@loop
                pairs += seen[x]    #@read
                seen[x] += 1        #@write
            return pairs            #@ret
    """,
    "java": """
        static long equalPairs(int[] nums) {
            int[] seen = new int[101];      //@make
            long pairs = 0;                 //@make
            for (int x : nums) {            //@loop
                pairs += seen[x];           //@read
                seen[x]++;                  //@write
            }
            return pairs;                   //@ret
        }
    """,
    "cpp": """
        long long equalPairs(const vector<int>& nums) {
            int seen[101] = {0};            //@make
            long long pairs = 0;            //@make
            for (int x : nums) {            //@loop
                pairs += seen[x];           //@read
                seen[x]++;                  //@write
            }
            return pairs;                   //@ret
        }
    """,
    "c": """
        long long equalPairs(const int* nums, int n) {
            int seen[101] = {0};            //@make
            long long pairs = 0;            //@make
            for (int i = 0; i < n; i++) {   //@loop
                pairs += seen[nums[i]];     //@read
                seen[nums[i]]++;            //@write
            }
            return pairs;                   //@ret
        }
    """,
}
EQUAL_PAIRS_RUN = {
    "python": """
        print(equal_pairs([3, 1, 3, 3, 1]))
        print(equal_pairs([7] * 100000))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(equalPairs(new int[] {3, 1, 3, 3, 1}));
            int[] big = new int[100000];
            Arrays.fill(big, 7);
            System.out.println(equalPairs(big));
        }
    """,
    "cpp": """
        int main() {
            cout << equalPairs({3, 1, 3, 3, 1}) << "\\n" << equalPairs(vector<int>(100000, 7)) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {3, 1, 3, 3, 1};
            static int big[100000];
            for (int i = 0; i < 100000; i++) big[i] = 7;
            printf("%lld\\n%lld\\n", equalPairs(a, 5), equalPairs(big, 100000));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

first_unique = py(FIRST_UNIQUE["python"], "first_unique")
equal_pairs = py(EQUAL_PAIRS["python"], "equal_pairs")

DEMO = [4, 7, 4, 9, 7, 2]
TALLY = {}
for x in DEMO:
    TALLY[x] = TALLY.get(x, 0) + 1
ANSWER = first_unique(DEMO)
assert ANSWER == 9

# The walkthrough: tally pass, then the scan in input order.
steps = Steps(f"`first_unique({DEMO})`: tally every value, then scan in the original order.")
steps.step("Start with an empty table. Nothing has been counted yet.", Row(DEMO, slots=True), M({"count": "{ }"}))
seen = {}
for i, x in enumerate(DEMO):
    seen[x] = seen.get(x, 0) + 1
    what = "new, so it enters the table with 1" if seen[x] == 1 else f"already in the table, so its count goes up to {seen[x]}"
    steps.step(f"Pass 1, index {i}: value {x} is {what}.", Row(DEMO, st={i: "active"}, ptr={"x": i}, slots=True), M(seen, "count"))
for i, x in enumerate(DEMO):
    if TALLY[x] == 1:
        steps.step(f"Pass 2, index {i}: count[{x}] is 1. This is the first value, in input order, that appears exactly once: return {x}.",
                   Row(DEMO, st={**{j: "dim" for j in range(i)}, i: "answer"}, ptr={"x": i}, slots=True), M(TALLY, "count"), result=x)
        break
    steps.step(f"Pass 2, index {i}: count[{x}] is {TALLY[x]}, so {x} repeats somewhere. Skip it.",
               Row(DEMO, st={**{j: "dim" for j in range(i)}, i: "active"}, ptr={"x": i}, slots=True), M(TALLY, "count"))

trace_rows = []
run = {}
for i, x in enumerate(DEMO):
    before = run.get(x, 0)
    run[x] = before + 1
    trace_rows.append((str(i), str(x), str(before), str(run[x]), "{" + ", ".join(f"{k}: {v}" for k, v in run.items()) + "}"))

# Linear probing into 8 slots with hash(k) = k mod 8, for the theory section.
PROBE_KEYS = [12, 5, 20, 13]
slots = [None] * 8
probe_rows = []
for k in PROBE_KEYS:
    home = k % 8
    i, tried = home, []
    while slots[i] is not None:
        tried.append(str(i))
        i = (i + 1) % 8
    slots[i] = k
    probe_rows.append((str(k), f"{k} mod 8 = {home}", ", ".join(tried) if tried else "none", str(i)))
PROBE_FINAL = list(slots)

PAIRS_DEMO = [3, 1, 3, 3, 1]
pair_rows = []
s_seen, total = {}, 0
for i, x in enumerate(PAIRS_DEMO):
    add = s_seen.get(x, 0)
    total += add
    s_seen[x] = add + 1
    pair_rows.append((str(i), str(x), str(add), str(total)))
assert total == equal_pairs(PAIRS_DEMO) == 4
BIG = equal_pairs([7] * 100000)
assert BIG == 100000 * 99999 // 2 > 2**31

N = 10**5
NAIVE = N * (N - 1) // 2

lesson(
    "arrays-hashing",
    "frequency-counting",
    """
    Walk the input once and keep a tally per value. Every question of the form "how many times", "is there a
    repeat", "which is most common" or "are these the same items in a different order" then becomes a table lookup
    instead of another scan.
    """,
    [
        ("idea", "The idea", [
            """
            Picture an election count. Nobody re-reads the whole pile of ballots every time someone asks "how many
            votes does Asha have?". The counter reads each ballot **once** and adds a mark next to the name on a tally
            sheet. After that, any question about votes is answered by looking at the sheet.

            Frequency counting is exactly that, for arrays and strings:

            1. **Tally pass.** Walk the input once. For each value `x`, add 1 to `count[x]`.
            2. **Answer pass.** Read the answer off the table, or walk the input (or the table) a second time with the
               counts in hand.

            The table is the whole trick. Without it, "how many times does `x` appear?" costs a full scan, O(n), and
            asking it for every element costs O(n²). With it, the same question costs O(1).
            """,
            fig(Row(DEMO, slots=True, label="input"), M(TALLY, "count after one pass"),
                caption=f"One pass over `{DEMO}` builds the whole tally. Every value's count is now one lookup away."),
            key("""
            Turn "how many times?" into a lookup: one O(n) pass builds `value → count`, and every later question about
            counts costs O(1).
            """),
            """
            **What the table forgets, and why that's the point.** A count table keeps *which* values appear and *how
            often*, and throws away *where* and *in what order*. Mathematicians call that a **multiset**. Many problems
            secretly only care about the multiset: "can this word be rearranged into that one?", "can I build the sign
            from these tiles?", "is there a duplicate?". For those, the order is noise and the table is the exact
            information you need, in the smallest form.

            When the order *does* matter (the first value that appears once, the earliest repeat), keep the table for
            the counts and use the original array for the order: that's what the second pass is for.
            """,
        ]),
        ("signals", "When to reach for it", [
            """
            Reach for a count table when the problem statement talks about **how often** rather than **where**:
            """,
            table(
                ["The problem says…", "Count what", "Then"],
                ["appears twice / any duplicate / all distinct", "each value (or just presence)", "stop at the first count of 2"],
                ["most / least frequent, top k, majority", "each value", "rank the table's entries by count"],
                ["rearrange, anagram, permutation, same characters", "each character in both strings", "compare the two tables"],
                ["can A be built / spelled / paid from B", "what B offers", "spend it while walking A; fail below 0"],
                ["first / last unique, appears exactly k times", "each value", "second pass in input order"],
                ["number of equal pairs, how many share a value", "each value as you go", "add the count before incrementing"],
            ),
            """
            **Quick self-test.** If you could shuffle the input and the answer would not change (or would only change in
            an order-dependent tie-break), counting is very likely part of the solution.

            **When it is the wrong tool**

            - **The position or order is the question**, as in "is `a` a subsequence of `b`?" A count table can't see
              order. That's two pointers.
            - **The counts are needed for every window of a fixed or moving size.** You still count, but you update
              the table as the window slides instead of recounting. That's the Sliding Window topic, built on this one.
            - **The value range is huge and you only need sorted order.** Sometimes sorting and reading off runs of
              equal values is simpler and uses O(1) extra memory (see *Sort then scan*).
            """,
        ]),
        ("theory", "How the table works", [
            """
            Every counting solution makes one decision: **what is the table?** There are two answers, and knowing how
            each works tells you when it's safe and what it costs.

            **1. A plain array (direct addressing).** If every value is an integer in a small known range `lo..hi`,
            use an array of size `R = hi - lo + 1` and store the count of `v` at index `v - lo`. Lowercase letters
            map to `ch - 'a'` (R = 26), ASCII characters to their code (R = 128), ratings 1..5 to `v - 1`.

            - Every update and lookup is **one memory access, worst case O(1)**. No hashing, no collisions.
            - The array costs O(R) memory and O(R) time to create (and to scan or compare). That's free when R is 26,
              and impossible when values go up to 10⁹.
            - Negative values need the offset `v - lo`; forgetting it is the classic out-of-bounds bug.
            """,
            """
            **2. A hash map.** When values are large, sparse, negative or not integers at all (strings, tuples), a hash
            map stores only the keys that actually occur. Inside, it is still an array of **slots**:

            1. A **hash function** turns the key into a big integer, and `hash mod capacity` picks a home slot.
            2. Two different keys can land on the same slot: a **collision**. *Chaining* keeps a small list per slot;
               *open addressing* (used by Python's dict and by the C code below) walks to the next free slot.
            3. The **load factor** α = keys / slots measures how full it is. Lookups stay short while α is bounded,
               so the table **grows (usually doubles) and re-inserts everything** when α passes a threshold: about
               0.75 for Java's HashMap, 2/3 for Python's dict, 1.0 by default for C++'s `unordered_map`.
            """,
            f"Here is open addressing with linear probing, inserting `{PROBE_KEYS}` into 8 slots with the toy hash `key mod 8`:",
            table(["key", "home slot", "slots already taken", "lands in"], *probe_rows),
            fig(Row(PROBE_FINAL, st={i: "new" for i, v in enumerate(PROBE_FINAL) if v is not None}, slots=True, label="slots after inserting"),
                caption="Collisions push keys to the next free slot. A lookup follows the same path and stops at the key or at an empty slot."),
            """
            **Why "O(1)" is an *expected* cost.** With a hash function that spreads keys well and α kept below a
            constant, the expected number of slots a lookup inspects is a small constant (about `1 + α` with chaining).
            That's where "O(1) average" comes from. Two honest caveats:

            - **Worst case is O(n) per operation.** If many keys share a home slot (a weak hash, or inputs crafted
              against a known hash), every lookup walks a long chain. Java turns long chains into balanced trees
              (O(log n)); C++'s `unordered_map` does not, which is why competitive programmers sometimes add a random
              salt to the hash.
            - **Growing is occasionally expensive, but cheap on average.** A resize re-inserts every key, O(n). But
              doubling means resizes happen at sizes 8, 16, 32, …, n, and those costs add up to less than 2n in total.
              Spread over n insertions, that is O(1) **amortised** per insertion.

            **What a hash map does not give you:** any useful order. Iterating over a hash map visits keys in slot
            order, which depends on hashes and history. Python's dict happens to remember insertion order; Java's
            HashMap and C++'s `unordered_map` do not. If the answer needs an order (by value, by count, by first
            appearance), impose it yourself: sort the entries, or walk the original array.
            """,
            table(
                ["", "Array (direct addressing)", "Hash map"],
                ["Keys allowed", "small integer range lo..hi", "anything hashable"],
                ["Update / lookup", "O(1) worst case", "O(1) expected, O(n) worst"],
                ["Memory", "O(R), even for absent values", "O(distinct keys), with a constant factor"],
                ["Order of keys", "by value, for free", "none you can rely on"],
                ["Use it for", "letters, digits, small ids", "big or negative numbers, strings, tuples"],
            ),
            """
            **One invariant to lean on.** After the tally pass, the counts add up to exactly `n`, and the number of
            keys is at most `min(n, R)`. Two consequences show up all the time:

            - If two strings have the same length and you add 1 per character of one and subtract 1 per character of
              the other, the table sums to 0. So **if no entry ever goes negative, every entry is exactly 0**, and the
              strings are rearrangements of each other. You don't need a final scan for positive leftovers.
            - A count can never exceed `n`, which bounds things like "bucket by frequency": the buckets are 1..n.
            """,
        ]),
        ("template", "The template", [
            """
            The template is two passes over the same array: **tally**, then **use the tally**. The example below returns
            the first value (in input order) that appears exactly once, or `-1` if every value repeats. It's small, but
            it has every part: the table, the tally loop, and a second pass that reads counts while keeping the input's
            order.
            """,
            code(
                "First value that appears once",
                FIRST_UNIQUE,
                [
                    ("make", "Create the empty table. In Python a dict, in Java a `HashMap`, in C++ an `unordered_map`. "
                             "The values here can be any integers, so a plain array won't do.",
                     {"c": "C has no hash map, so `cm_new` (above) builds one: an array of slots sized to at least twice the input, which keeps the load factor at or below 1/2."}),
                    ("reserve", "Reserving room for twice as many entries as there are values means the table never "
                                "has to grow mid-loop. It's an optimisation, not a requirement."),
                    ("tally", "**Pass 1, the tally.** One update per element: increment `x`'s count, creating it at 0 the "
                              "first time.",
                     {"python": "`count.get(x, 0)` returns 0 for a key that isn't there yet, so new and old keys take the same path.",
                      "java": "`merge(x, 1, Integer::sum)` puts 1 for a new key and otherwise adds 1 to the old value.",
                      "cpp": "`count[x]` inserts `x` with value 0 if it's missing, then `++` makes it 1. Handy for tallying, a trap for reading (see *Pitfalls*).",
                      "c": "`cm_add` finds the key's slot (or the empty slot where it belongs), marks it used and increments its count."}),
                    ("scan", "**Pass 2, in input order.** Walk the original array again, not the table. The table "
                             "doesn't remember order; the array does, which is how we find the *first* unique value."),
                    ("hit", "The first `x` whose count is exactly 1 is the answer. Every value before it has a count of 2 "
                            "or more, so none of them qualifies."),
                    ("none", "Every value repeats. `-1` is a sentinel that works when values are known to be "
                             "non-negative; otherwise return a flag or an optional instead."),
                    ("struct", "The table's storage: parallel arrays of keys and counts, a `used` flag per slot, and "
                               "`mask = capacity - 1` (capacity is a power of two, so `& mask` is a fast `mod`)."),
                    ("cap", "Pick a power of two at least twice the number of values. With at most n keys in 2n slots, the "
                            "load factor stays at or below 1/2, so probe chains stay short."),
                    ("alloc", "`calloc` zeroes the counts and the `used` flags; the keys array needs no zeroing because a "
                              "slot's key is only read when its `used` flag is set."),
                    ("hash", "Multiplicative hashing: multiply by a large odd constant (close to 2³² divided by the golden "
                             "ratio) and keep the low bits. It scatters nearby keys like 1, 2, 3 across the table."),
                    ("probe", "**Linear probing.** Walk forward until we find the key or an empty slot. The empty slot is "
                              "where the key would go, so the same function serves both lookup and insert."),
                    ("add", "Find the slot, claim it, store the key, bump the count."),
                    ("get", "A key that was never inserted ends at an empty slot, so its count is 0."),
                    ("free", "Release the three arrays. In C, the table's memory is yours to give back."),
                ],
                FIRST_UNIQUE_RUN,
                "first_unique([4, 7, 4, 9, 7, 2]); first_unique([5, 5])",
            ),
            """
            **The shape to remember** is the two loops: build, then query. Most frequency problems differ only in the
            second loop: compare two tables, find the max, bucket by count, or stop at a threshold.
            """,
        ]),
        ("trace", "Trace it by hand", [
            f"""
            Step through `first_unique({DEMO})`. Watch the table fill during pass 1, then watch pass 2 use it. Notice
            that pass 2 never asks "how many 4s are there?" by scanning; it reads `count[4]` directly.
            """,
            walk(steps),
            "The same tally as a table. Each row is one iteration of pass 1:",
            table(["i", "x", "count[x] before", "count[x] after", "table after the step"], *trace_rows),
            f"""
            Pass 2 then checks `count[4] = {TALLY[4]}` (skip), `count[7] = {TALLY[7]}` (skip), `count[9] = {TALLY[9]}`:
            the answer is **{ANSWER}**. Note that `2` is also unique, but it comes later in the input, and the table on
            its own could not have told us which unique value comes first.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Fixed alphabet: an array instead of a map

            When keys are lowercase letters, a 26-slot array beats a hash map: no hashing, no allocation per key,
            worst-case O(1). The function below asks whether `b` is a rearrangement of `a`. It uses **one** table:
            +1 for each letter of `a`, −1 for each letter of `b`.
            """,
            code(
                "Same letters, different order",
                SAME_LETTERS,
                [
                    ("len", "Different lengths can never be rearrangements. This check also makes the early exit "
                            "below correct (see the invariant in *How the table works*)."),
                    ("make", "26 counters, one per letter, all 0. `ch - 'a'` maps `'a'..'z'` to `0..25`."),
                    ("up", "Count every letter of `a` up."),
                    ("down", "Spend letters of `b` against those counts."),
                    ("neg", "A count below zero means `b` uses some letter more often than `a` has it. Stop now."),
                    ("ok", "Same length, and no count ever went negative. The counts add up to 0 and none is negative, "
                           "so all of them are 0: the two strings hold the same letters the same number of times."),
                ],
                SAME_LETTERS_RUN,
                'same_letters("listen", "silent"), ("table", "bleat"), ("loop", "polo"), ("eel", "lee"), ("seen", "sene"), ("aab", "abb")',
            ),
            """
            ### Count while you scan: equal pairs

            How many pairs of positions `i < j` hold equal values? You could count everything first and then add
            `c · (c − 1) / 2` for each count `c` (choose 2 of the `c` copies). There is a neater one-pass form that
            reappears in later patterns:

            > When you reach `x`, every earlier copy of `x` forms a new pair with it. So **add `seen[x]` first, then
            > increment it.**

            The order of those two lines is the whole correctness argument. Read first, and `x` pairs only with copies
            strictly before it (so `i < j`, and nothing pairs with itself). Increment first, and every element pairs
            with itself.
            """,
            code(
                "Pairs of equal values (values 0..100)",
                EQUAL_PAIRS,
                [
                    ("make", "Values are known to be in 0..100, so an array of 101 counters is the table. The total "
                             "needs 64 bits (see the second example run)."),
                    ("loop", "One pass, left to right."),
                    ("read", "**Read before write.** `seen[x]` copies of `x` came earlier; `x` forms a pair with each."),
                    ("write", "Now count this copy, so later copies pair with it too."),
                    ("ret", "Every pair `(i, j)` with `i < j` was counted exactly once: at `j`, when `i` was already in the table."),
                ],
                EQUAL_PAIRS_RUN,
                "equal_pairs([3, 1, 3, 3, 1]); equal_pairs([7] * 100000)",
            ),
            f"For `{PAIRS_DEMO}`:",
            table(["i", "x", "pairs added (seen[x] before)", "running total"], *pair_rows),
            f"""
            The second run is 100,000 copies of one value: {BIG:,} pairs, more than a 32-bit `int` can hold
            (2,147,483,647). That's why the total is a `long`.

            ### Spend-down: can A be paid from B?

            Count what the *supply* offers, then walk the *demand* and decrement. The first count to drop below 0 is
            a shortfall, and you can stop there. The *same letters* code above is this idea plus a length check. Use it
            for "build a word from tiles", "pay with these coins", "cover these requirements".

            ### Rank by count: most common first, top k

            Tally, then order the distinct values by count:

            - **Sort the entries** by `(−count, tie-break)`: O(n + d log d) for `d` distinct values. Simple, and the
              usual choice.
            - **Bucket by count:** a count is between 1 and n, so make n + 1 buckets and drop each value into
              `bucket[count]`. Reading buckets from high to low gives values from most to least frequent in O(n + d),
              no comparison sort. Ties inside a bucket still need the problem's tie-break.
            - **A heap of size k** keeps only the k best while scanning the entries: O(d log k), handy when k is tiny.

            ### Presence only: a set

            If you only need "seen or not" (duplicates, distinctness), a hash set is a count table with counts capped
            at 1. It saves memory and states the intent. The early exit (stop at the first repeat) often matters more
            than the asymptotics.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            Let `n` be the input length, `d` the number of distinct values and `R` the size of the value range.

            **Time.** The tally pass does `n` table updates. With an array, each is one memory access, so it's O(n)
            worst case, plus O(R) to create the array. With a hash map, each is O(1) expected, so O(n) expected in
            total, and O(n) amortised once resizing is included. The second pass is another O(n) (over the array) or
            O(d) (over the table). Two passes are still O(n): constants don't change the class.

            **Space.** O(R) for the array, O(d) for a map, where `d ≤ n`.

            **Compared with re-scanning.** Counting by re-scanning asks, for each element, "how many times does this
            appear?", which compares every pair: for n = 10⁵ that's {NAIVE:,} comparisons against about
            {2 * N:,} table operations. That's the difference between minutes and milliseconds.
            """,
            table(
                ["Method", "Time", "Extra space", "Notes"],
                ["Re-scan for every element", "O(n²)", "O(1)", "only for tiny inputs"],
                ["Sort, then count runs of equal values", "O(n log n)", "O(1) to O(n)", "changes the input order"],
                ["Array tally (range R)", "O(n + R)", "O(R)", "worst-case guarantees"],
                ["Hash map tally", "O(n) expected", "O(d)", "any key type"],
            ),
        ]),
        ("languages", "In your language", [
            """
            **Python**

            - `count[x] = count.get(x, 0) + 1` works everywhere. `collections.Counter(nums)` does the whole tally in
              one call and returns 0 for missing keys instead of raising.
            - `Counter.most_common(k)` gives the k largest counts; ties come out in first-seen order, so don't rely on
              it when the problem defines its own tie-break.
            - `Counter` subtraction (`a - b`) silently drops counts that fall to 0 or below. Great for "what's left",
              wrong if you need to detect a shortfall.
            - For letters, `[0] * 26` with `ord(ch) - ord('a')` is faster than a dict in tight loops.

            **Java**

            - `map.merge(x, 1, Integer::sum)` or `map.put(x, map.getOrDefault(x, 0) + 1)`.
            - `HashMap<Integer, Integer>` boxes every key and count into objects. For small ranges, an `int[]` is
              several times faster and far smaller.
            - Comparing two `Integer` values with `==` compares object identity, which only happens to work for -128..127.
              Use `.equals`, or compare against an `int` so it unboxes (as the template does).
            - `TreeMap` keeps keys sorted, at O(log n) per operation.

            **C++**

            - `count[x]++` on an `unordered_map` inserts `x` with 0 when missing, then increments.
            - **Reading with `[]` also inserts.** `if (count[y] == 0)` adds `y` to the map. To only look, use
              `count.find(y)` or `count.count(y)` (C++20: `contains`).
            - `reserve(n)` up front avoids rehashing. `std::map` is the sorted, O(log n) alternative.
            - For letters: `int cnt[26] = {0};` or `array<int, 26>{}`.

            **C**

            - Small ranges: `int cnt[26] = {0};` (zero-initialised), or `calloc(R, sizeof(int))` for a range known at
              run time.
            - Arbitrary integers: there is no standard hash map. The open-addressing table in the template (about 25
              lines) is a solid default; sorting with `qsort` and counting runs is the other common route.
            - `char` may be signed: index with `(unsigned char)ch` when the input can contain bytes above 127.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - **Wrong offset.** `ch - 'a'` assumes lowercase letters. Uppercase, digits or spaces index out of bounds.
              Check the constraints, or size the table for all of ASCII (128).
            - **Negative values in an array table.** Shift by the minimum: `cnt[v - lo]`.
            - **Reading creates entries.** C++'s `map[key]` (and Python's `defaultdict` on read) inserts missing keys.
              That can grow the table, break a later `size()` check, or change iteration while you're iterating.
            - **Relying on map order.** Iterating a hash map is not "in order of first appearance" (except Python's
              dict) and not "sorted". When ties matter, sort explicitly with the stated tie-break.
            - **Overflowing counts of pairs.** `c · (c − 1) / 2` for c = 10⁵ is about 5 · 10⁹. Use 64-bit totals.
            - **Comparing tables of different alphabets.** Two maps can be equal in every key they share and still
              differ because one has an extra key. Comparing sizes first, or using one table with +1/−1, avoids that.
            - **Forgetting the early exit.** For "any duplicate?" or "can we pay?", stop at the first repeat or the first
              shortfall. Same O(n) worst case, much faster on typical inputs.
            - **Empty input and single elements.** One element has no duplicates and no pairs; make sure your loops
              and sentinels handle `n = 0` and `n = 1`.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Values are ids up to 10⁹, and you need to know whether any id repeats. Array or hash set, and why?",
                 "A hash set. An array indexed by id would need 10⁹ slots. A set stores only the ids that occur, with O(1) expected per check, and you can stop at the first id already in the set."),
                ("Why does *same letters* return true without scanning the table for leftover positive counts?",
                 "The lengths are equal, so after both loops the counts add up to 0. If none went negative, a positive entry would force a negative one somewhere to keep the sum at 0. So every entry is 0."),
                ("In *equal pairs*, what goes wrong if you swap the two lines inside the loop?",
                 "Incrementing first means `seen[x]` already includes the current element, so every element also pairs with itself. The result grows by exactly n."),
                ("Why does the template's second pass walk `nums` instead of the table?",
                 "The question asks for the *first* unique value in input order. The table keeps counts, not positions, and a hash map's iteration order is not the input order."),
                ("A hash map lookup is \"O(1)\". What's hidden behind that word?",
                 "It's an expected cost, assuming a hash that spreads keys and a load factor kept bounded by resizing. A single lookup can be O(n) in the worst case, and resizes cost O(n) occasionally but O(1) amortised per insertion."),
            ),
        ]),
    ],
)
