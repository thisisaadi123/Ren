"""Lesson: Frequency counting (Arrays & Hashing, pattern 1)."""
from lesson import Bars, Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

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
same_letters = py(SAME_LETTERS["python"], "same_letters")

DEMO = [4, 7, 4, 9, 7, 2]
TALLY = {}
for x in DEMO:
    TALLY[x] = TALLY.get(x, 0) + 1
ANSWER = first_unique(DEMO)
assert ANSWER == 9
KEYS = list(TALLY)

# How much work re-scanning does: for each element, a full pass.
RESCAN = len(DEMO) * len(DEMO)

# The walkthrough: tally pass, then the scan in input order.
steps = Steps(f"`first_unique({DEMO})`. First we tally, then we walk the list again with the counts in hand.")
steps.step("Nothing counted yet. The table is empty.", Row(DEMO, slots=True), Bars([0] * len(KEYS), labels=KEYS, label="count", top=2))
seen = {}
for i, x in enumerate(DEMO):
    seen[x] = seen.get(x, 0) + 1
    what = f"We haven't met {x} before, so it goes in with a count of 1." if seen[x] == 1 else f"We've met {x} before. Its count goes up to {seen[x]}."
    steps.step(f"Index {i} holds {x}. {what}", Row(DEMO, st={i: "active"}, ptr={"x": i}, slots=True),
               Bars([seen.get(k, 0) for k in KEYS], labels=KEYS, st={KEYS.index(x): "new"}, label="count", top=2))
for i, x in enumerate(DEMO):
    st_b = {KEYS.index(x): "answer" if TALLY[x] == 1 else "active"}
    if TALLY[x] == 1:
        steps.step(f"Second pass, index {i}: {x} has a count of 1. Nothing before it qualified, so {x} is our answer.",
                   Row(DEMO, st={**{j: "dim" for j in range(i)}, i: "answer"}, ptr={"x": i}, slots=True), Bars([TALLY[k] for k in KEYS], labels=KEYS, st=st_b, label="count", top=2), result=x)
        break
    steps.step(f"Second pass, index {i}: {x} has a count of {TALLY[x]}, so it repeats somewhere. Move on.",
               Row(DEMO, st={**{j: "dim" for j in range(i)}, i: "active"}, ptr={"x": i}, slots=True), Bars([TALLY[k] for k in KEYS], labels=KEYS, st=st_b, label="count", top=2))

trace_rows = []
run = {}
for i, x in enumerate(DEMO):
    before = run.get(x, 0)
    run[x] = before + 1
    trace_rows.append((str(i), str(x), str(before), str(run[x]), "{" + ", ".join(f"{k}: {v}" for k, v in run.items()) + "}"))

# Linear probing into 8 slots with hash(k) = k mod 8, step by step.
PROBE_KEYS = [12, 5, 20, 13]
probe = Steps("Inserting `12, 5, 20, 13` into 8 slots, using the toy hash `key mod 8`.")
slots = [None] * 8
probe.step("Eight empty slots. Each key's home slot is `key mod 8`.", Row(slots, slots=True, label="slots"))
probe_rows = []
for k in PROBE_KEYS:
    home = k % 8
    i, tried = home, []
    while slots[i] is not None:
        tried.append(i)
        i = (i + 1) % 8
    slots[i] = k
    if tried:
        msg = f"{k} mod 8 = {home}, but slot {home} is taken" + (f", and so is {', '.join(map(str, tried[1:]))}" if len(tried) > 1 else "") + f". It walks forward and settles in slot {i}."
    else:
        msg = f"{k} mod 8 = {home}. Slot {home} is free, so {k} goes straight in."
    probe.step(msg, Row(list(slots), st={**{t: "dim" for t in tried}, i: "new"}, ptr={"home": home}, slots=True, label="slots"))
    probe_rows.append((str(k), f"{k} mod 8 = {home}", ", ".join(map(str, tried)) if tried else "none", str(i)))
probe.step("Looking up 13 later follows the same path: start at slot 5, step past 5 and 20, find 13 in slot 7. "
           "Looking up 4 would start at slot 4 and keep walking until it hits an empty slot, which tells us 4 isn't there.",
           Row(list(slots), st={5: "dim", 6: "dim", 7: "found"}, ptr={"home": 5}, slots=True, label="slots"))
PROBE_FINAL = list(slots)

PAIRS_DEMO = [3, 1, 3, 3, 1]
pair_rows = []
pairs_walk = Steps(f"`equal_pairs({PAIRS_DEMO})`: read how many copies came before, then add this one.")
s_seen, total = {}, 0
PK = sorted(set(PAIRS_DEMO))
pairs_walk.step("No values seen yet, no pairs yet.", Row(PAIRS_DEMO, slots=True), Bars([0] * len(PK), labels=PK, label="seen", top=3), M({"pairs": 0}))
for i, x in enumerate(PAIRS_DEMO):
    add = s_seen.get(x, 0)
    total += add
    s_seen[x] = add + 1
    pair_rows.append((str(i), str(x), str(add), str(total)))
    earlier = [j for j in range(i) if PAIRS_DEMO[j] == x]
    msg = (f"{x} has {add} earlier cop{'y' if add == 1 else 'ies'} (index {', '.join(map(str, earlier))}), so it makes {add} new pair{'s' if add != 1 else ''}. "
           if add else f"No earlier {x}, so no new pairs. ") + f"Then seen[{x}] becomes {add + 1}."
    pairs_walk.step(msg, Row(PAIRS_DEMO, st={**{j: "found" for j in earlier}, i: "active"}, ptr={"x": i}, slots=True),
                    Bars([s_seen.get(k, 0) for k in PK], labels=PK, st={PK.index(x): "new"}, label="seen", top=3), M({"pairs": total}))
assert total == equal_pairs(PAIRS_DEMO) == 4
BIG = equal_pairs([7] * 100000)
assert BIG == 100000 * 99999 // 2 > 2**31

# Worked example: same letters, drawn as the +1 / -1 table.
SA, SB = "dusty", "study"
assert same_letters(SA, SB)
LETTERS = sorted(set(SA + SB))
diff = {c: 0 for c in LETTERS}
for c in SA:
    diff[c] += 1
AFTER_A = [diff[c] for c in LETTERS]
for c in SB:
    diff[c] -= 1
AFTER_B = [diff[c] for c in LETTERS]
assert AFTER_B == [0] * len(LETTERS)
NA, NB = "seen", "sene"
nd = {}
for c in NA:
    nd[c] = nd.get(c, 0) + 1
bad = None
for c in NB:
    nd[c] = nd.get(c, 0) - 1
    if nd[c] < 0:
        bad = c
        break
assert same_letters(NA, NB) and bad is None
XA, XB = "aab", "abb"
xd = {c: 0 for c in "ab"}
for c in XA:
    xd[c] += 1
stop = None
for c in XB:
    xd[c] -= 1
    if xd[c] < 0:
        stop = c
        break
assert stop == "b" and not same_letters(XA, XB)

# Worked example: most common rating.
RATINGS = [4, 5, 4, 3, 5, 4, 2, 4, 5]
RC = {r: RATINGS.count(r) for r in range(1, 6)}
TOP = max(RC, key=lambda r: (RC[r], -r))
assert TOP == 4 and RC[4] == 4

# Worked example: first value whose second copy shows up earliest.
REP = [3, 8, 1, 8, 3]
seen_set, rep_rows, FIRST_REPEAT = [], [], None
for i, x in enumerate(REP):
    if x in seen_set:
        rep_rows.append((str(i), str(x), "{" + ", ".join(map(str, seen_set)) + "}", "seen it: stop"))
        FIRST_REPEAT = x
        break
    rep_rows.append((str(i), str(x), "{" + ", ".join(map(str, seen_set)) + "}" if seen_set else "{ }", "new: remember it"))
    seen_set.append(x)
assert FIRST_REPEAT == 8

N = 10**5
NAIVE = N * (N - 1) // 2

lesson(
    "arrays-hashing",
    "frequency-counting",
    """
    Read the input once and keep a running count for each value. After that, questions like "how many times does
    this appear?", "is anything repeated?" or "are these two lists the same items shuffled?" stop needing another
    scan. You just look the answer up.
    """,
    [
        ("idea", "The idea", [
            """
            Think about how votes get counted after a class election. The teacher doesn't reread the whole pile every
            time someone asks how Asha is doing. They go through the ballots once, put a tick next to the name on each
            one, and from then on any question about the result is answered by glancing at the ticks.

            That's frequency counting. You walk through the array once, and every time you see a value `x` you add 1
            to `count[x]`. Then you answer the question from that table, sometimes with a second walk through the
            input.
            """,
            fig(Row(DEMO, slots=True, label="input"), Bars([TALLY[k] for k in KEYS], labels=KEYS, label="count after one pass"),
                caption=f"One pass over `{DEMO}` and we know how often every value appears: two 4s, two 7s, one 9, one 2."),
            f"""
            Why bother? Without the table, "how many times does `x` appear?" means scanning the whole list. Ask it for
            each of the `n` elements and you've done about `n × n` steps. For our six numbers that's {RESCAN} looks,
            which is nothing. For 100,000 numbers it's ten billion, and your program sits there for minutes. With the
            table, each of those questions costs one lookup.
            """,
            key("""
            Count once, then look things up. One pass builds `value → count`, and every question about counts after
            that is a single lookup instead of another scan.
            """),
            """
            It helps to notice what the table throws away. It keeps which values appear and how often, and forgets
            where they were and in what order. A lot of problems only care about that much. "Can this word be
            rearranged into that one?" doesn't care where the letters sit, only how many of each there are. For
            questions like that, the table holds exactly the information you need and nothing else.

            When order does matter, say you want the *first* value that appears once, you still build the table, but
            you answer by walking the original array again. The table tells you the counts and the array tells you
            the order.
            """,
        ]),
        ("signals", "When to reach for it", [
            """
            The giveaway is a problem that's about *how often* something happens rather than *where*. Here are the
            phrasings you'll keep running into:
            """,
            table(
                ["If the problem says…", "count this", "and then"],
                ["any duplicate / all distinct", "each value (or just whether you've seen it)", "stop at the first repeat"],
                ["most / least frequent, top k, majority", "each value", "pick the entries with the biggest counts"],
                ["anagram, rearrangement, permutation", "each character, in both strings", "check the counts match"],
                ["can A be made from B", "what B has to offer", "use it up while walking A; fail if anything runs out"],
                ["first / last unique, appears exactly k times", "each value", "walk the input again in order"],
                ["number of equal pairs", "each value as you go", "add the count before bumping it"],
            ),
            """
            A quick test I like: imagine shuffling the input. If the answer wouldn't change (apart from maybe a
            tie-break), counting is almost certainly part of the solution.

            It's the wrong tool when position is the whole point. "Is `abc` a subsequence of `aXbYc`?" depends on
            order, and a count table can't see order, so that one's two pointers. If you need counts for every window
            of a moving range, you'll still count, but you'll update the table as the window slides instead of
            starting over (that's the Sliding Window topic). And sometimes sorting the array and reading off runs of
            equal values is simpler and needs no extra memory at all.
            """,
        ]),
        ("theory", "How the table works", [
            """
            Every counting solution makes one choice up front: what is the table? You've got two options, and it's
            worth understanding both, because they fail in different ways.

            ### Option 1: a plain array

            If the values are small whole numbers in a known range, use an array and let the value be the index. For
            lowercase letters, `ch - 'a'` turns `'a'..'z'` into `0..25`, so 26 slots cover everything. Ratings from 1
            to 5 fit in 5 (or 6) slots. Every update is exactly one memory access, with no hashing involved.

            The catch is the range. An array of 26 is free. An array big enough for values up to a billion is not. And
            if values can be negative you need to shift them first (`count[v - lowest]`), or you'll index outside the
            array.

            ### Option 2: a hash map

            When values are huge, negative, or not numbers at all (words, pairs), you want a hash map. It only stores
            the keys that actually show up. Underneath, though, it's still an array of slots. A **hash function** turns
            each key into a number, and that number (mod the number of slots) says which slot the key should live in.

            Two different keys can want the same slot. That's a **collision**, and one common fix is to just walk
            forward to the next free slot. This is called linear probing, and it's what Python's dict does (in a
            fancier form) and what our C code below does. Step through it:
            """,
            walk(probe),
            table(["key", "home slot", "already taken", "ends up in"], *probe_rows),
            """
            The table can't be allowed to fill up, or those walks get long. So it tracks how full it is (the **load
            factor**, keys divided by slots) and when that passes a limit it doubles in size and re-inserts everything.
            Java's HashMap does this at 75% full, Python's dict at about two thirds, C++'s `unordered_map` at 100% by
            default.

            ### So is it really O(1)?

            On average, yes. With a decent hash function and the table kept from getting too full, a lookup touches a
            small, constant number of slots. That's what people mean by "O(1) expected".

            Two caveats are worth knowing, because interviewers like asking about them. First, the worst case is bad: if
            lots of keys land on the same slot, a lookup can walk past all of them, which is O(n). That can happen by
            bad luck, or on purpose if someone builds inputs against a known hash function. (Java switches long chains
            into trees to soften this; C++ doesn't.) Second, the doubling is expensive when it happens, because every
            key moves. But it happens at sizes 8, 16, 32, 64… and all those moves add up to less than twice the final
            size. Spread over every insertion, that's still O(1) each. This is called **amortised** cost.

            One more thing a hash map doesn't give you is order. Iterating over it visits keys in whatever order the
            slots happen to be in. Python's dict remembers insertion order as a bonus; Java's HashMap and C++'s
            `unordered_map` don't. If your answer needs an order, sort the entries or walk the original array.
            """,
            table(
                ["", "Plain array", "Hash map"],
                ["Works for", "small whole numbers in a known range", "anything you can hash"],
                ["Each update", "O(1), always", "O(1) on average, O(n) worst case"],
                ["Memory", "one slot per possible value", "roughly one slot per value that appears"],
                ["Order", "by value, for free", "none you can rely on"],
                ["Good for", "letters, digits, small ids", "big or negative numbers, strings, tuples"],
            ),
            """
            ### A fact you'll use a lot

            After the tally, the counts add up to `n`, the length of the input. That sounds obvious, but it's handy.
            Say two strings have the same length and you add 1 for every letter of the first and subtract 1 for every
            letter of the second. When you're done, the table adds up to zero. So if nothing ever went below zero,
            nothing can be above zero either, and every count is exactly zero. You'll see this used in the
            *same letters* code below, where it saves a final check.
            """,
        ]),
        ("template", "The template", [
            """
            Almost every counting solution has the same two parts: build the table, then use it. Here's a small but
            complete example. It returns the first value in the list that appears exactly once, or `-1` if every value
            repeats.
            """,
            code(
                "First value that appears once",
                FIRST_UNIQUE,
                [
                    ("make", "An empty table. The values can be any integers, so we use a hash map rather than an array.",
                     {"c": "C doesn't come with a hash map, so `cm_new` (above) builds a small one: an array of slots at least twice as big as the input, so it never gets more than half full."}),
                    ("reserve", "This tells the map how big it'll get, so it doesn't have to stop and grow halfway "
                                "through. Nice to have, not required."),
                    ("tally", "The first pass. Each value bumps its own count, starting from 0 the first time we see it.",
                     {"python": "`count.get(x, 0)` gives 0 for a key that isn't there yet, so new and old keys are handled the same way.",
                      "java": "`merge(x, 1, Integer::sum)` stores 1 for a new key and adds 1 to an existing one.",
                      "cpp": "`count[x]` quietly creates `x` with a value of 0 if it's missing, then `++` makes it 1. Convenient here, but watch out when you only want to read (see *Pitfalls*).",
                      "c": "`cm_add` finds the key's slot, or the empty slot where it should go, marks it used and bumps its count."}),
                    ("scan", "The second pass goes over the original array, not the table. The table doesn't know the "
                             "order things came in; the array does."),
                    ("hit", "The first value with a count of 1 is the answer. Everything before it had a count of 2 or "
                            "more."),
                    ("none", "Nothing appeared exactly once. Returning `-1` only works if real values can't be `-1`; "
                             "otherwise return something like `None` or a flag."),
                    ("struct", "The table's storage: keys and counts side by side, a `used` flag for each slot, and a "
                               "`mask`. The slot count is a power of two, so `& mask` does the same job as `% size`, "
                               "only faster."),
                    ("cap", "Pick a power of two that's at least twice the number of values, so the table stays at most "
                            "half full and probe walks stay short."),
                    ("alloc", "`calloc` starts the counts and `used` flags at zero. The keys don't need zeroing, because "
                              "we only read a slot's key after checking that it's used."),
                    ("hash", "Multiply by a big odd number and keep the low bits. This spreads nearby keys like 1, 2, 3 "
                             "far apart in the table."),
                    ("probe", "Walk forward until we find the key or hit an empty slot. If we hit an empty slot, that's "
                              "where the key would go, so the same walk works for both looking up and inserting."),
                    ("add", "Find the slot, claim it, write the key, bump the count."),
                    ("get", "A key that was never added ends at an empty slot, so its count is 0."),
                    ("free", "In C you give memory back yourself."),
                ],
                FIRST_UNIQUE_RUN,
                "first_unique([4, 7, 4, 9, 7, 2]); first_unique([5, 5])",
            ),
            """
            If you remember one shape from this lesson, make it those two loops. Most counting problems only change
            what the second loop does: compare two tables, find the biggest count, or stop as soon as something runs
            out.
            """,
        ]),
        ("trace", "Trace it by hand", [
            f"""
            Here's `first_unique({DEMO})` one step at a time. Watch the bars grow during the first pass. Then notice
            that the second pass never counts anything. It just reads the bar.
            """,
            walk(steps),
            "The same first pass written out as a table:",
            table(["i", "x", "count before", "count after", "table so far"], *trace_rows),
            f"""
            In the second pass, 4 has a count of {TALLY[4]} (skip), 7 has {TALLY[7]} (skip), and 9 has {TALLY[9]}, so
            the answer is {ANSWER}. The 2 at the end also appears once, but it comes later. The table alone
            couldn't have told us which of the two comes first, which is exactly why the second pass walks the array.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Is `"{SB}"` a rearrangement of `"{SA}"`?

            Same length, so it's possible. Add 1 for each letter of `"{SA}"`, then take 1 away for each letter of
            `"{SB}"`. If they hold the same letters, everything cancels:
            """,
            fig(Bars(AFTER_A, labels=LETTERS, label=f'after "{SA}"', height=48),
                Bars(AFTER_B, labels=LETTERS, label=f'after "{SB}"', height=48),
                caption="Every letter of the first word went up by one, and the second word took each one back down. All zeros: yes."),
            f"""
            Now try `"{XA}"` and `"{XB}"`. After the first word, `a` is at 2 and `b` is at 1. The second word takes
            `a` down to 1, then `b` to 0, then wants another `b`, and the count drops to -1. We can stop right there:
            the second word uses `b` more often than the first one has it.

            ### What's the most common rating?

            The ratings are `{RATINGS}`. Ratings only go from 1 to 5, so an array of five counters does the job:
            """,
            fig(Bars([RC[r] for r in range(1, 6)], labels=range(1, 6), st={TOP - 1: "answer"}, label="how many of each rating"),
                caption=f"Rating {TOP} shows up {RC[TOP]} times, more than any other."),
            f"""
            If two ratings tied, you'd need a rule for which one wins (the problem will usually tell you, like "the
            smaller one"). Write that rule into your comparison instead of hoping the table's order matches it.

            ### Which value repeats first?

            In `{REP}`, which value is the first to show up a second time? You don't need counts at all here, just
            "have I seen this before?", so a set is enough. And you can stop as soon as you get a hit:
            """,
            table(["i", "x", "seen so far", "what happens"], *rep_rows),
            f"""
            The answer is {FIRST_REPEAT}. 3 also repeats, and it appeared first, but its second copy comes later. "The
            first value to appear twice" and "the earliest value that has a duplicate" are different questions, so check
            which one you've been asked.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Small alphabets: use an array

            When the values are lowercase letters, 26 counters beat a hash map. There's no hashing, nothing to
            allocate per key, and every step costs the same. Here's the rearrangement check from the examples, written
            with a single table: up for each letter of `a`, down for each letter of `b`.
            """,
            code(
                "Same letters, different order",
                SAME_LETTERS,
                [
                    ("len", "If the lengths differ, one string has a letter the other doesn't. This check also makes "
                            "the early exit below safe, for the reason in *How the table works*."),
                    ("make", "26 counters, one for each letter, all starting at 0."),
                    ("up", "Count every letter of `a`."),
                    ("down", "Use those letters up while reading `b`."),
                    ("neg", "If a count drops below zero, `b` used some letter more times than `a` had it. We can stop "
                            "right away."),
                    ("ok", "Same length and nothing went negative. The counts add up to zero and none is negative, so "
                           "they're all zero, which means the letters match exactly."),
                ],
                SAME_LETTERS_RUN,
                'same_letters("listen", "silent"), ("table", "bleat"), ("loop", "polo"), ("eel", "lee"), ("seen", "sene"), ("aab", "abb")',
            ),
            """
            ### Counting as you go: pairs of equal values

            How many pairs of positions `i < j` hold the same value? One way is to count everything first and then use
            a bit of maths: a value that appears `c` times can be paired up in `c × (c - 1) / 2` ways. There's a neater
            way that does it in the same pass, and you'll see it again in the next two lessons:

            > When you reach `x`, every earlier copy of `x` makes a new pair with it. So add `seen[x]` to the answer
            > first, and only then add 1 to `seen[x]`.

            Those two lines have to be in that order. Read first, and `x` only pairs with copies that came before it,
            so each pair is counted once and nothing pairs with itself. Swap them, and every element also pairs with
            itself, so you'd be off by `n`.
            """,
            walk(pairs_walk),
            code(
                "Pairs of equal values (values 0..100)",
                EQUAL_PAIRS,
                [
                    ("make", "The values are between 0 and 100, so 101 counters are enough. The total gets a 64-bit "
                             "type, because there can be a lot of pairs (look at the second example run)."),
                    ("loop", "One pass, left to right."),
                    ("read", "Read before you write. `seen[x]` copies of `x` came earlier, and each one pairs with this `x`."),
                    ("write", "Now count this copy too, so later copies can pair with it."),
                    ("ret", "Every pair got counted exactly once, at the moment we reached its second element."),
                ],
                EQUAL_PAIRS_RUN,
                "equal_pairs([3, 1, 3, 3, 1]); equal_pairs([7] * 100000)",
            ),
            f"""
            The second run is 100,000 copies of the same number. That's {BIG:,} pairs, which doesn't fit in a 32-bit
            `int` (the limit is 2,147,483,647). That's why the total is a `long`.

            ### Spending down: can A be paid for out of B?

            Count what you have, then walk through what you need and subtract. The first count that goes negative is
            the thing you're short of. The rearrangement check above is exactly this, plus a length check. The same
            idea answers "can I build this word from these tiles?" or "do these coins cover the bill?".

            ### Ranking by count: most common first, top k

            Build the table, then put the distinct values in order of their counts. The simple way is to sort the
            entries by count (biggest first), breaking ties however the problem says. That costs O(n + d log d) for `d`
            distinct values.

            There's a cute trick when you want to avoid sorting. A count can only be between 1 and `n`, so make `n + 1`
            buckets and drop each value into `bucket[count]`. Reading the buckets from the top down gives you values
            from most to least common in O(n). You still need the tie-break rule inside each bucket. And if you only
            need the top few, a small heap that keeps the best `k` while you scan works well too.

            ### Just "seen or not": a set

            For "is there a duplicate?" or "are all of these different?", you don't need counts, only whether you've
            met a value before. A set says that directly, uses less memory, and lets you stop at the first repeat,
            which on real data often means you barely scan anything.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            Let's say the input has `n` values, `d` of them distinct, and (for the array version) the values range over
            `R` possibilities.

            The first pass does `n` updates. With an array each one is a single memory access, so that's O(n), plus
            O(R) to set the array up. With a hash map each update is O(1) on average, so O(n) on average overall, even
            counting the occasional resize. The second pass is another O(n) over the array, or O(d) over the table.
            Two passes are still O(n); constants don't change the big picture.

            Memory is O(R) for the array or O(d) for the map, and `d` can't be bigger than `n`.

            Compare that with re-scanning. Checking every pair of elements for `n = 100,000` is {NAIVE:,} comparisons,
            while counting is about {2 * N:,} table operations.
            """,
            table(
                ["Method", "Time", "Extra space", "Notes"],
                ["Re-scan for every element", "O(n²)", "O(1)", "only for tiny inputs"],
                ["Sort, then count runs of equal values", "O(n log n)", "O(1) to O(n)", "reorders the input"],
                ["Array tally (range R)", "O(n + R)", "O(R)", "guaranteed speed"],
                ["Hash map tally", "O(n) on average", "O(d)", "any kind of key"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `count[x] = count.get(x, 0) + 1` works everywhere. `collections.Counter(nums)` does the whole tally in one
            call and returns 0 for keys it hasn't seen instead of raising an error. `Counter.most_common(k)` hands you
            the top `k`, but its ties come out in first-seen order, so don't lean on it if the problem has its own
            tie-break rule. Also, `Counter` subtraction (`a - b`) quietly throws away anything that drops to zero or
            below, which is great for "what's left over" and wrong for "did anything run out". For letters in a tight
            loop, `[0] * 26` with `ord(ch) - ord('a')` is faster than a dict.

            ### Java

            `map.merge(x, 1, Integer::sum)` or `map.put(x, map.getOrDefault(x, 0) + 1)`. A `HashMap<Integer, Integer>`
            wraps every key and count in an object, so for small ranges a plain `int[]` is much faster and smaller.
            Watch out for comparing two `Integer`s with `==`: it compares the objects, not the numbers, and only
            happens to work for values between -128 and 127. Use `.equals`, or compare with an `int` so Java unboxes
            it, like the template does. If you need keys in sorted order, `TreeMap` keeps them that way at O(log n)
            per operation.

            ### C++

            `count[x]++` on an `unordered_map` creates `x` at 0 if it's missing, then increments. That's handy for
            counting and a trap for reading: `if (count[y] == 0)` silently adds `y` to the map. To look without
            touching, use `count.find(y)` or `count.count(y)` (or `contains` in C++20). Call `reserve(n)` up front to
            avoid rehashing. For letters, `int cnt[26] = {0};` or `array<int, 26>{}`.

            ### C

            For small ranges, `int cnt[26] = {0};` or `calloc(R, sizeof(int))` when the range is only known at run
            time. For arbitrary integers there's no built-in map, so either use the little open-addressing table from
            the template or sort with `qsort` and count runs of equal values. One gotcha: `char` can be signed, so
            cast to `unsigned char` before using it as an index if the input might contain bytes above 127.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            Most bugs in counting code come from a handful of places:

            - `ch - 'a'` assumes lowercase letters. One capital letter, digit or space and you're indexing outside the
              array. Check the constraints, or size the table for all 128 ASCII characters.
            - Negative values in an array table need shifting: `cnt[v - lowest]`.
            - Reading can create entries. C++'s `map[key]` (and Python's `defaultdict`) insert missing keys when you
              read them. That can make the table grow, break a later size check, or change it while you're looping
              over it.
            - Don't rely on the order a hash map gives you. When ties matter, sort with the rule the problem gives.
            - Pair counts get big fast. `c × (c - 1) / 2` for `c = 100,000` is about five billion, which needs 64 bits.
            - When comparing two separate tables, one can have a key the other doesn't. Compare sizes too, or use a
              single table with +1 and -1 like the template does.
            - For "is there a duplicate?" or "can we afford it?", stop as soon as you know. Same worst case, much
              faster on real inputs.
            - Try your code on an empty list and on a single element. One element has no duplicates and no pairs.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("The values are ids up to a billion, and you need to know whether any id repeats. Array or hash set?",
                 "A hash set. An array would need a billion slots. A set only stores the ids that actually appear, each check is O(1) on average, and you can stop as soon as you see an id that's already in it."),
                ("Why can *same letters* return true without checking the table for leftover positive counts at the end?",
                 "The strings have the same length, so after both loops the counts add up to zero. If none of them went negative, none can be positive either (it would need a negative somewhere to balance it). So they're all zero."),
                ("In *equal pairs*, what goes wrong if you swap the two lines inside the loop?",
                 "Incrementing first means `seen[x]` already includes the current element, so every element pairs with itself once. The answer comes out `n` too big."),
                ("Why does the template's second pass walk `nums` instead of the table?",
                 "We want the *first* unique value in the order of the input. The table knows counts but not positions, and a hash map won't give you its keys in input order."),
                ("People say a hash map lookup is O(1). What are they leaving out?",
                 "That it's an average. It assumes a hash that spreads keys out and a table that resizes before it gets too full. A single lookup can be O(n) in a bad case, and a resize costs O(n) when it happens, though only O(1) per insertion when you average it out."),
            ),
        ]),
    ],
)
