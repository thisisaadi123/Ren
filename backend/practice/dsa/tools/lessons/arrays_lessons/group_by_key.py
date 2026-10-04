"""Lesson: Group by key (Arrays & Hashing, pattern 3)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

GROUP = {
    "python": """
        def digit_key(x):
            count = [0] * 10                        #@digits
            while x > 0:                            #@digits
                count[x % 10] += 1                  #@digits
                x //= 10                            #@digits
            k = 0                                   #@build
            for d in range(9, -1, -1):              #@build
                for _ in range(count[d]):           #@build
                    k = k * 10 + d                  #@build
            return k                                #@build

        def group_by_digits(nums):
            group_of = {}                           #@make
            groups = []                             #@make
            for x in nums:                          #@loop
                k = digit_key(x)                    #@sig
                if k not in group_of:               #@new
                    group_of[k] = len(groups)       #@new
                    groups.append([])               #@new
                groups[group_of[k]].append(x)       #@put
            return groups                           #@ret
    """,
    "java": """
        static long digitKey(int x) {
            int[] count = new int[10];                          //@digits
            for (; x > 0; x /= 10) count[x % 10]++;             //@digits
            long k = 0;                                         //@build
            for (int d = 9; d >= 0; d--) {                      //@build
                for (int c = 0; c < count[d]; c++) k = k * 10 + d;  //@build
            }
            return k;                                           //@build
        }

        static List<List<Integer>> groupByDigits(int[] nums) {
            Map<Long, Integer> groupOf = new HashMap<>();       //@make
            List<List<Integer>> groups = new ArrayList<>();     //@make
            for (int x : nums) {                                //@loop
                long k = digitKey(x);                           //@sig
                Integer g = groupOf.get(k);                     //@new
                if (g == null) {                                //@new
                    g = groups.size();                          //@new
                    groupOf.put(k, g);                          //@new
                    groups.add(new ArrayList<>());              //@new
                }
                groups.get(g).add(x);                           //@put
            }
            return groups;                                      //@ret
        }
    """,
    "cpp": """
        long long digitKey(int x) {
            int count[10] = {0};                                //@digits
            for (; x > 0; x /= 10) count[x % 10]++;             //@digits
            long long k = 0;                                    //@build
            for (int d = 9; d >= 0; d--) {                      //@build
                for (int c = 0; c < count[d]; c++) k = k * 10 + d;  //@build
            }
            return k;                                           //@build
        }

        vector<vector<int>> groupByDigits(const vector<int>& nums) {
            unordered_map<long long, int> groupOf;              //@make
            vector<vector<int>> groups;                         //@make
            for (int x : nums) {                                //@loop
                long long k = digitKey(x);                      //@sig
                auto [it, isNew] = groupOf.emplace(k, (int)groups.size());  //@new
                if (isNew) groups.emplace_back();               //@new
                groups[it->second].push_back(x);                //@put
            }
            return groups;                                      //@ret
        }
    """,
    "c": """
        long long digitKey(int x) {
            int count[10] = {0};                                //@digits
            for (; x > 0; x /= 10) count[x % 10]++;             //@digits
            long long k = 0;                                    //@build
            for (int d = 9; d >= 0; d--) {                      //@build
                for (int c = 0; c < count[d]; c++) k = k * 10 + d;  //@build
            }
            return k;                                           //@build
        }

        // Writes nums grouped into out (group by group, input order inside each),
        // the start of group g at start[g] (start[groups] = n), and returns the number of groups.
        int groupByDigits(const int* nums, int n, int* out, int* start) {
            size_t cap = 16;                                    //@make
            while (cap < 2 * (size_t)n) cap <<= 1;              //@make
            long long* keys = malloc(cap * sizeof(long long));  //@make
            int* gid = malloc(cap * sizeof(int));               //@make
            bool* used = calloc(cap, sizeof(bool));             //@make
            int* groupOfItem = malloc((n + 1) * sizeof(int));   //@make
            int groups = 0;                                     //@make
            for (int j = 0; j < n; j++) {                       //@loop
                long long k = digitKey(nums[j]);                //@sig
                size_t i = (size_t)(((uint64_t)k * 0x9E3779B97F4A7C15ull) >> 32) & (cap - 1);  //@probe
                while (used[i] && keys[i] != k) i = (i + 1) & (cap - 1);  //@probe
                if (!used[i]) {                                 //@new
                    used[i] = true;                             //@new
                    keys[i] = k;                                //@new
                    gid[i] = groups++;                          //@new
                }
                groupOfItem[j] = gid[i];                        //@put
            }
            for (int g = 0; g <= groups; g++) start[g] = 0;     //@place
            for (int j = 0; j < n; j++) start[groupOfItem[j] + 1]++;  //@place
            for (int g = 0; g < groups; g++) start[g + 1] += start[g];  //@place
            int* fill = malloc((groups + 1) * sizeof(int));     //@place
            memcpy(fill, start, (groups + 1) * sizeof(int));    //@place
            for (int j = 0; j < n; j++) out[fill[groupOfItem[j]]++] = nums[j];  //@place
            free(keys); free(gid); free(used); free(groupOfItem); free(fill);  //@free
            return groups;                                      //@ret
        }
    """,
}
GROUP_RUN = {
    "python": """
        for g in group_by_digits([123, 45, 321, 100, 54, 10, 213, 1, 10]):
            print(*g)
    """,
    "java": """
        public static void main(String[] args) {
            for (List<Integer> g : groupByDigits(new int[] {123, 45, 321, 100, 54, 10, 213, 1, 10})) {
                StringBuilder sb = new StringBuilder();
                for (int x : g) sb.append(sb.length() > 0 ? " " : "").append(x);
                System.out.println(sb);
            }
        }
    """,
    "cpp": """
        int main() {
            for (auto& g : groupByDigits({123, 45, 321, 100, 54, 10, 213, 1, 10})) {
                for (size_t i = 0; i < g.size(); i++) cout << (i ? " " : "") << g[i];
                cout << "\\n";
            }
        }
    """,
    "c": """
        int main(void) {
            int nums[] = {123, 45, 321, 100, 54, 10, 213, 1, 10}, out[9], start[10];
            int groups = groupByDigits(nums, 9, out, start);
            for (int g = 0; g < groups; g++) {
                for (int i = start[g]; i < start[g + 1]; i++) printf(i > start[g] ? " %d" : "%d", out[i]);
                printf("\\n");
            }
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

digit_key = py(GROUP["python"], "digit_key")
group_by_digits = py(GROUP["python"], "group_by_digits")

DEMO = [123, 45, 321, 100, 54, 10, 213, 1, 10]
GROUPS = group_by_digits(DEMO)
assert [len(g) for g in GROUPS] == [3, 2, 1, 2, 1]

steps = Steps(f"`group_by_digits({DEMO})`: compute each number's key, then file it under that key.")
steps.step("No groups yet. The table maps a key to the index of its group in `groups`.", Row(DEMO, slots=True), M({"groups": "[ ]"}))
gof, gs = {}, []
for j, x in enumerate(DEMO):
    k = digit_key(x)
    if k not in gof:
        gof[k] = len(gs)
        gs.append([])
        msg = f"{x} has key {k}. That key is new: open group {gof[k]} for it."
    else:
        msg = f"{x} has key {k}, already seen: it joins group {gof[k]}, next to {', '.join(map(str, gs[gof[k]]))}."
    gs[gof[k]].append(x)
    st = {i: "found" for i in range(j) if digit_key(DEMO[i]) == k}
    st[j] = "active"
    steps.step(msg, Row(DEMO, st=st, ptr={"x": j}, slots=True), M({f"{kk}": str(gs[g]) for kk, g in gof.items()}, "key → group"))
steps.step(f"{len(gs)} groups. Items with equal keys ended up together, in the order they first appeared.", M({f"group {i}": str(g) for i, g in enumerate(gs)}), result=len(gs))

trace_rows = []
for x in DEMO:
    trace_rows.append((str(x), "".join(sorted(str(x), reverse=True)), str(digit_key(x))))


def shape(w):
    first = {}
    return tuple(first.setdefault(c, len(first)) for c in w)


def shift_sig(w):
    return tuple((ord(b) - ord(a)) % 26 for a, b in zip(w, w[1:]))


def min_rot(w):
    return min(w[i:] + w[:i] for i in range(len(w)))


CATALOG = [
    ("rearrangements (anagrams)", '"listen", "silent"', "letters sorted", f'"{"".join(sorted("listen"))}"'),
    ("rearrangements, faster key", '"listen", "silent"', "26 letter counts", "(0,0,0,0,1,0,0,0,1,…)"),
    ("same letter pattern", '"moon", "feet"', "first-seen index of each letter", str(shape("moon")).replace(" ", "")),
    ("same up to a shift of the alphabet", '"abc", "xyz"', "gaps between neighbours, mod 26", str(shift_sig("abc")).replace(" ", "")),
    ("same up to rotation", '"cab", "bca"', "smallest rotation", f'"{min_rot("cab")}"'),
    ("unordered pairs", "(3, 1), (1, 3)", "the pair sorted", "(1, 3)"),
    ("same digits (this lesson's code)", "123, 321", "digits sorted high to low", "321"),
]
assert shape("moon") == shape("feet") and shift_sig("abc") == shift_sig("xyz") and min_rot("cab") == min_rot("bca")

# A key that is sound but not complete: the sum of letter codes.
SUMS = {w: sum(map(ord, w)) for w in ["ad", "bc", "da"]}
assert SUMS["ad"] == SUMS["bc"] == SUMS["da"]
# Ambiguous concatenation without separators.
AMB_A, AMB_B = [1, 11], [11, 1]
assert "".join(map(str, AMB_A)) == "".join(map(str, AMB_B))

lesson(
    "arrays-hashing",
    "group-by-key",
    """
    When items belong together under some rule (same letters, same shape, same digits), give every item a **key**
    that is equal exactly when the rule says they belong together. Then a hash map from key to list does all the
    grouping in one pass.
    """,
    [
        ("idea", "The idea", [
            """
            A post office doesn't compare every letter with every other letter to decide which ones go to the same
            street. It reads one thing off each envelope, the **postcode**, and drops the letter into that postcode's
            bag. Letters that belong together end up in the same bag without ever being compared to each other.

            Group by key is that idea for data:

            1. Design a **key function** `key(item)`: a value that is the same for two items exactly when they belong in
               the same group.
            2. Walk the items once. For each, compute its key and append the item to `groups[key]`, creating the list
               the first time a key is seen.

            All the difficulty lives in step 1. Step 2 is the same few lines every time.
            """,
            key("""
            Don't compare items with each other. Map each item to a **canonical key**, so that "these two belong
            together" becomes "these two keys are equal", which a hash map checks in O(1).
            """),
            fig(Row([123, 321, 45, 54], slots=False, label="items"), M({"321": "[123, 321]", "54": "[45, 54]"}, "key → group"),
                caption="`123` and `321` share the key `321` (their digits, sorted), so they land in the same group."),
        ]),
        ("signals", "When to reach for it", [
            """
            - "Group the words / items / rows that are …" (anagrams of each other, the same up to a shift, isomorphic).
            - "How many **different kinds** / classes / families are there?" (the number of distinct keys).
            - "Count pairs that are equivalent" (group, then each group of size `s` gives `s(s - 1)/2` pairs; the counting
              trick from *Frequency counting*, applied to keys).
            - "Find all duplicates up to …" (rotation, reordering, case).

            The tell-tale sign is an **equivalence**: a "same as" rule where the problem doesn't care which member of a
            group you pick.

            **When it's the wrong tool**

            - **"Similar", not "same".** If the rule is "within distance 2" or "differs in at most one letter", it isn't
              an equivalence (A ~ B and B ~ C doesn't give A ~ C), and no single key can capture it. That's union-find
              or graph search.
            - **No cheap canonical form.** Some equivalences (graphs that are the same up to relabelling) have no known
              fast key. For array and string problems you'll almost always find one.
            """,
        ]),
        ("theory", "Designing the key", [
            """
            ### Equivalence classes

            The rule "belongs with" has to be an **equivalence relation**:

            - **reflexive:** every item belongs with itself;
            - **symmetric:** if A belongs with B, then B belongs with A;
            - **transitive:** if A belongs with B and B with C, then A belongs with C.

            Exactly those rules split the items into non-overlapping **classes**. Group by key finds the classes.

            ### The two properties of a good key

            For every pair of items A, B:

            1. **Sound:** if A and B belong together, then `key(A) = key(B)`. Otherwise one class gets split across
               two groups.
            2. **Complete:** if `key(A) = key(B)`, then A and B belong together. Otherwise two classes get merged.

            A key with both properties is a **canonical form**: one standard representative per class. The usual
            recipe is "pick the representative by a fixed rule": sort the letters, start the pattern numbering at 0,
            shift so the first letter is `a`, rotate to the smallest rotation.
            """,
            table(["Belong together when…", "Example", "Canonical key", "Key of the example"], *CATALOG),
            f"""
            **A sound but incomplete key.** For anagrams, the sum of the letter codes is equal for any two anagrams
            (sound), but `"ad"`, `"bc"` and `"da"` all sum to {SUMS["ad"]} even though `"bc"` is not an anagram of
            `"ad"`. A key that loses information merges classes. Hashes have this problem too, which is why a hash map
            stores the full key and compares it on a hash match: the key itself must be complete.

            ### Keys must be immutable and unambiguous

            - **Immutable:** a hash map hashes the key once, when it's inserted. If the key object changes afterwards,
              it's in the wrong slot. Python refuses lists as keys for this reason; use a tuple or a string. In Java, a
              `List` key is allowed but dangerous if you modify it.
            - **Unambiguous:** when you flatten a structured key into a string, use separators. Without them, counts
              `{AMB_A}` and `{AMB_B}` both become `"{"".join(map(str, AMB_A))}"`: two different keys collide into one.
              Write `"1#11"` and `"11#1"` instead, or use a tuple.

            ### Choosing between equally correct keys

            For anagrams of words of length `L`, two keys are both canonical:

            - **sorted letters:** O(L log L) to build, key length `L`;
            - **26 counts:** O(L + 26) to build, fixed key size.

            For short words, either is fine. For long strings over a small alphabet, the counts win. Pick by the
            constraints, not by habit.

            ### Numbers can be keys too

            A key doesn't have to be a string. This lesson's code groups numbers that use the same digits: its key is
            the digits **sorted from high to low, read as a number** (`213 → 321`, `100 → 100`, `10 → 10`). It's sound
            (same digits, same sorted order) and complete (zeros sort last, so the digit count is preserved: `100` and
            `10` stay apart). An integer key is cheap to hash and easy to store, even in C.
            """,
        ]),
        ("template", "The template", [
            """
            Group non-negative integers that are made of the same digits, keeping groups in the order they first
            appear and items in input order within each group.

            The map goes from key to the **index** of its group in a list. That small choice keeps the groups in
            first-appearance order in every language (a plain hash map would not), and the list of groups is the
            answer.
            """,
            code(
                "Group numbers by their digits",
                GROUP,
                [
                    ("digits", "Count each digit 0–9: the key only depends on how many of each digit there are.",
                     {"c": "For `x = 0` the loop doesn't run and the key is 0, which no positive number shares."}),
                    ("build", "Read the digits out from 9 down to 0. Any two numbers with the same digit counts produce "
                              "the same number here, and different counts produce different numbers. A 10-digit input "
                              "makes a 10-digit key, beyond 32 bits, so the key is 64-bit."),
                    ("make", "`key → group index`, plus the list of groups itself.",
                     {"c": "The table's arrays (keys, group ids, used flags) and `groupOfItem`, the group of every input position."}),
                    ("loop", "One pass over the input."),
                    ("sig", "The canonical key for this item."),
                    ("new", "A key seen for the first time opens a new, empty group at the end of the list.",
                     {"cpp": "`emplace` inserts only if the key is new and tells us which happened (`isNew`), with one hash lookup.",
                      "java": "`get` returns `null` for an unseen key; that's when we open a group."}),
                    ("put", "Append the item to its group. Equal keys always reach the same list.",
                     {"c": "C can't grow lists easily, so record the item's group now and lay the groups out afterwards."}),
                    ("probe", "Hash the 64-bit key (multiply by a large odd constant, keep high bits) and probe linearly "
                              "to the key or an empty slot."),
                    ("place", "Lay the groups out contiguously: count each group's size, turn the sizes into start "
                              "offsets (a prefix sum), then drop each item into its group's next free spot. Items keep "
                              "their input order."),
                    ("free", "Release the temporary arrays."),
                    ("ret", "The groups, in order of first appearance.",
                     {"c": "Returns the number of groups; the grouped items are in `out`, delimited by `start`."}),
                ],
                GROUP_RUN,
                "group_by_digits([123, 45, 321, 100, 54, 10, 213, 1, 10])",
            ),
        ]),
        ("trace", "Trace it by hand", [
            table(["x", "digits sorted high → low", "key"], *trace_rows),
            walk(steps),
            f"""
            Notice what never happened: no two numbers were compared. Every number met only the table. `100` and `10`
            share digits `1` and `0` but have different keys ({digit_key(100)} and {digit_key(10)}), because the key
            remembers how many zeros there are.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Count classes, not members

            "How many different families are there?" only needs a **set of keys**: insert every key, then return the
            set's size. No lists at all.

            ### Count equivalent pairs

            Count how many items share each key (a count map instead of lists), then add `c(c - 1)/2` for every count
            `c`, or use the one-pass "add the count before incrementing" trick from *Frequency counting*.

            ### Match against one reference

            "How many words have the same shape as this pattern?" There's only one class you care about: compute the
            pattern's key once and count the items whose key equals it. No map needed.

            ### Keys made of other structures

            - **Rows or columns of a grid:** the whole row as a tuple (Python) or a joined string with separators.
              Matching a row to a column then becomes "same key".
            - **Several attributes:** group people by `(city, age)`: the tuple of attributes is the key.
            - **Normalised strings:** lower-case, trim, remove punctuation; for "same up to case", the lower-cased word
              is canonical.

            ### Sort instead of hashing

            Sort the items by key; equal keys become neighbours, and each run is a group. O(n log n) comparisons of
            keys, no hash map, and the groups come out ordered by key. Useful in C, or when the output must be sorted
            anyway.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Let `n` be the number of items and `K` the cost of computing one key (for strings of length `L`: O(L log L)
            to sort the letters, O(L) to count them).

            - **Time:** O(n · K) for the keys, plus O(n) expected hash-map operations. But hashing a key of length `L`
              costs O(L) too, so for strings the total is O(n · (K + L)). For words up to length `L`: O(n · L log L)
              with sorted keys, O(n · L) with counts.
            - **Space:** O(n · L) for the keys and the groups (every item is stored once in some group).

            The alternative, comparing every pair of items for equivalence, is O(n²) comparisons, each O(L) or more.
            """,
            table(
                ["Approach", "Time (n words, length L)", "Extra space"],
                ["Compare every pair", "O(n² · L log L)", "O(n)"],
                ["Sort-letters key + hash map", "O(n · L log L)", "O(n · L)"],
                ["Letter-counts key + hash map", "O(n · (L + 26))", "O(n · (L + 26))"],
                ["Sort items by key, then scan runs", "O(n · K + n log n · L)", "O(n · L)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            **Python:** `defaultdict(list)` with `groups[key].append(item)`. Keys must be hashable: `tuple(...)` or
            `"".join(sorted(word))`, never a list. Dicts keep insertion order, so `list(groups.values())` is in
            first-appearance order.

            **Java:** `map.computeIfAbsent(key, k -> new ArrayList<>()).add(item)`. A `String` key compares by content;
            an `int[]` key compares by **identity** (two equal arrays are different keys), so convert to
            `Arrays.toString(arr)` or `new String(charArray)`. `HashMap` order is arbitrary; use `LinkedHashMap` for
            insertion order, or the index map in the template.

            **C++:** `unordered_map<string, vector<string>>`; `groups[key].push_back(item)` creates the list. A
            `vector<int>` or `pair` key works with `std::map` (ordered) but needs a custom hash for `unordered_map`, so
            people often convert to a string with separators. `std::array<int, 26>` keys work in `map`.

            **C:** an integer key (like this lesson's) is the easiest: open addressing on 64-bit keys. For string keys,
            either hash the string yourself (FNV-1a, comparing with `strcmp` on collision) or sort an array of
            `(key, index)` pairs with `qsort` and read off runs.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - **Key not complete.** Sums, lengths, or a hash of the item alone merge different classes. Test your key on
              two items that *shouldn't* group.
            - **Key not sound.** For shift families, using the raw gaps without `mod 26` splits `"az"` (gap 25) from
              `"ba"` (gap -1). Normalise every part of the key.
            - **Ambiguous string keys.** Join numbers with a separator: `"1#11"`, not `"111"`.
            - **Mutable keys.** Never modify a list or array after using it as a key.
            - **Output order.** If the answer must be in a particular order (sorted groups, sorted inside each group),
              sort explicitly at the end. Don't rely on the map's iteration order.
            - **Empty items and duplicates.** An empty string has an empty key and forms its own group. Identical items
              have identical keys and belong to the same group; keep both copies if the problem says so.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why isn't \"the number of distinct letters\" a valid key for grouping anagrams?",
                 "It's sound (anagrams have the same distinct letters) but not complete: `\"ab\"` and `\"cd\"` both have 2 distinct letters and would be grouped together."),
                ("Two words have the same shape if one maps to the other by a consistent one-to-one letter replacement. Give a canonical key.",
                 "Replace each letter with the index of its first appearance: `\"moon\"` → (0, 1, 1, 2), `\"feet\"` → (0, 1, 1, 2). Same tuple exactly when the shapes match."),
                ("Why does the template map a key to a group **index** instead of directly to a list?",
                 "So the groups live in one list in order of first appearance, in every language. Iterating a Java `HashMap` or C++ `unordered_map` would give an arbitrary order."),
                ("Rows `[1, 11]` and `[11, 1]` are turned into string keys by joining the numbers. What can go wrong?",
                 "Both become `\"111\"` and are wrongly grouped together. Join with a separator (`\"1#11\"`, `\"11#1\"`) or use a tuple."),
                ("\"Group words that differ in at most one letter.\" Can a key do it?",
                 "No: that relation isn't transitive (`cat` ~ `cot` ~ `dot`, but `cat` and `dot` differ in two letters), so it doesn't split words into classes. It needs union-find or a graph search."),
            ),
        ]),
    ],
)
