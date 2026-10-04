"""Lesson: Group by key (Arrays & Hashing, pattern 3)."""
from lesson import Bars, Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

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
DEMO_KEYS = [digit_key(x) for x in DEMO]

steps = Steps(f"`group_by_digits({DEMO})`. Work out each number's key, then file the number under it.")
steps.step("No groups yet. The table maps each key to the position of its group in the `groups` list.", Row(DEMO, slots=True), M({"groups": "[ ]"}))
gof, gs = {}, []
for j, x in enumerate(DEMO):
    k = digit_key(x)
    if k not in gof:
        gof[k] = len(gs)
        gs.append([])
        msg = f"{x} has key {k}. We haven't seen that key, so it gets a new group, number {gof[k]}."
    else:
        msg = f"{x} has key {k}. We've seen it before, so {x} joins group {gof[k]} alongside {', '.join(map(str, gs[gof[k]]))}."
    gs[gof[k]].append(x)
    st = {i: "found" for i in range(j) if DEMO_KEYS[i] == k}
    st[j] = "active"
    steps.step(msg, Row(DEMO, st=st, ptr={"x": j}, slots=True), M({f"{kk}": str(gs[g]) for kk, g in gof.items()}, "key → group"))
steps.step(f"That's {len(gs)} groups. Numbers with equal keys ended up together, and the groups are in the order their first member appeared.",
           M({f"group {i}": str(g) for i, g in enumerate(gs)}), result=len(gs))

trace_rows = [(str(x), "".join(sorted(str(x), reverse=True)), str(digit_key(x))) for x in DEMO]

# Building one key, digit by digit.
KX = 20301
kc = [0] * 10
for ch in str(KX):
    kc[int(ch)] += 1
KEYX = digit_key(KX)
assert KEYX == 32100
kwalk = Steps(f"Building the key for {KX}: count its digits, then read them back out from 9 down to 0.")
kwalk.step("Ten counters, one for each digit.", Bars([0] * 10, labels=range(10), label="how many of each digit", top=2))
cnt = [0] * 10
x = KX
while x > 0:
    d = x % 10
    cnt[d] += 1
    x //= 10
    kwalk.step(f"The last digit is {d} (that's x % 10). Count it, then drop it with x // 10, leaving {x}.",
               Bars(list(cnt), labels=range(10), st={d: "new"}, label="how many of each digit", top=2), M({"x": x}))
built = ""
for d in range(9, -1, -1):
    if cnt[d]:
        built += str(d) * cnt[d]
        kwalk.step(f"Reading from the top: {cnt[d]} × digit {d}. The key so far is {built}.",
                   Bars(list(cnt), labels=range(10), st={d: "answer"}, label="how many of each digit", top=2), M({"key": built}))
assert int(built) == KEYX

# Rotation groups.
ROTS = ["cab", "bca", "acb", "abc", "bac", "cba"]


def min_rot(w):
    return min(w[i:] + w[:i] for i in range(len(w)))


rot_rows = [(f'"{w}"', ", ".join(f'"{w[i:] + w[:i]}"' for i in range(len(w))), f'"{min_rot(w)}"') for w in ROTS]
ROT_GROUPS = {}
for w in ROTS:
    ROT_GROUPS.setdefault(min_rot(w), []).append(w)
assert len(ROT_GROUPS) == 2

# Unordered pairs: friendships listed both ways.
FR = [(3, 1), (1, 3), (2, 5), (4, 4), (5, 2), (1, 3)]
fr_keys = [tuple(sorted(p)) for p in FR]
FR_DISTINCT = len(set(fr_keys))
assert FR_DISTINCT == 3


def shape(w):
    first = {}
    return tuple(first.setdefault(c, len(first)) for c in w)


def shift_sig(w):
    return tuple((ord(b) - ord(a)) % 26 for a, b in zip(w, w[1:]))


CATALOG = [
    ("same letters in any order", '"listen", "silent"', "the letters, sorted", f'"{"".join(sorted("listen"))}"'),
    ("same letters, faster", '"listen", "silent"', "how many of each of the 26 letters", "(0,0,0,0,1,0,0,0,1,…)"),
    ("same letter pattern", '"moon", "feet"', "where each letter first appeared", str(shape("moon")).replace(" ", "")),
    ("same up to shifting the alphabet", '"abc", "xyz"', "gaps between neighbours, mod 26", str(shift_sig("abc")).replace(" ", "")),
    ("same up to rotation", '"cab", "bca"', "the smallest rotation", f'"{min_rot("cab")}"'),
    ("the same pair, either way round", "(3, 1), (1, 3)", "the pair, sorted", "(1, 3)"),
    ("same digits (this lesson's code)", "123, 321", "digits sorted high to low", "321"),
]
assert shape("moon") == shape("feet") and shift_sig("abc") == shift_sig("xyz") and min_rot("cab") == min_rot("bca")

# A key that's right in one direction only: the sum of letter codes.
SUMW = ["ad", "bc", "da", "cb"]
SUMS = {w: sum(map(ord, w)) for w in SUMW}
assert len(set(SUMS.values())) == 1
AMB_A, AMB_B = [1, 11], [11, 1]
assert "".join(map(str, AMB_A)) == "".join(map(str, AMB_B))

lesson(
    "arrays-hashing",
    "group-by-key",
    """
    When items belong together under some rule (same letters, same digits, same pattern), give each one a label
    that comes out the same exactly when the rule says they belong together. Then a hash map from label to list sorts
    everything into groups in one pass.
    """,
    [
        ("idea", "The idea", [
            """
            Think about how a post office sorts mail. Nobody holds two envelopes side by side and asks "do these go to
            the same street?". Each envelope has a postcode, the sorter reads it, and the envelope goes into that
            postcode's bag. Letters for the same street end up together without ever being compared to each other.

            Group by key is the same thing for data. You come up with a **key** for each item, something you can work
            out from the item alone, which comes out identical for items that belong together and different for items
            that don't. Then you go through the items once and drop each one into the list for its key.
            """,
            fig(Row(DEMO, slots=True, label="numbers"), Row(DEMO_KEYS, slots=True, label="their keys (digits sorted, high to low)"),
                M({str(k): str(g) for k, g in zip(dict.fromkeys(DEMO_KEYS), GROUPS)}, "key → group"),
                caption="Two numbers share a key exactly when they use the same digits. The map does the rest."),
            key("""
            Don't compare items with each other. Turn each item into a key, so that "do these belong together?"
            becomes "are these keys equal?", which a hash map answers instantly.
            """),
            """
            The second half, filing items under their keys, is the same few lines every time. All the thinking goes
            into the key. Most of this lesson is about how to design a good one.
            """,
        ]),
        ("signals", "When to reach for it", [
            """
            Watch for problems that talk about items being "the same" in some loose sense: words that are anagrams of
            each other, strings that are rotations or shifts of each other, rows that match columns. Phrases like
            "group the …", "how many different kinds / families are there?" or "count the pairs that are equivalent"
            are strong hints.

            What these have in common is a "same as" rule where the problem doesn't care which member of a group you
            pick. That's what makes a key possible.

            It doesn't work for "similar" rules like "differ in at most one letter" or "within 2 of each other". Those
            aren't proper "same as" rules: `cat` is close to `cot`, and `cot` is close to `dot`, but `cat` and `dot`
            differ in two places. No single key can capture that, and you'd need union-find or a graph search instead.
            """,
        ]),
        ("theory", "Designing the key", [
            """
            ### What makes a rule "groupable"

            For a rule to split items into neat, non-overlapping groups, three things have to be true:

            1. Every item belongs with itself.
            2. If A belongs with B, then B belongs with A.
            3. If A belongs with B and B belongs with C, then A belongs with C.

            Rules like that are called **equivalence relations**, and the groups are called **equivalence classes**.
            "Is an anagram of" passes all three. "Differs by one letter" fails the third, which is exactly why it can't
            be grouped by key.

            ### Two ways a key can go wrong

            A good key has to get both directions right:

            - If two items belong together, their keys must be **equal**. Get this wrong and one real group gets split
              into two.
            - If two keys are equal, the items must really **belong together**. Get this wrong and two different groups
              get merged into one.

            A key that gets both right is called a **canonical form**: one standard representative for each group. The
            usual way to build one is to pick a fixed rule for choosing the representative. Sort the letters. Number
            the letters in order of first appearance. Shift everything so the word starts with `a`. Take the smallest
            rotation. Here are some you'll meet:
            """,
            table(["Items belong together when…", "example", "key", "key for the example"], *CATALOG),
            f"""
            ### A key that's only half right

            Here's a tempting key for anagrams: add up the letter codes. Anagrams have the same letters, so they always
            get the same sum, which is the first direction. But look what happens with these four words:
            """,
            fig(M({f'"{w}"': SUMS[w] for w in SUMW}, "sum of letter codes"),
                caption='All four get the same key, so they\'d land in one group, even though "bc" isn\'t an anagram of "ad".'),
            f"""
            The sum throws information away, so different groups collide. Hash values have the same problem, which is
            why a hash map always keeps the full key and checks it after the hash matches. Your key has to be complete
            on its own.

            ### Keys have to be fixed and unambiguous

            A hash map works out where to put a key once, when you insert it. If the key changes afterwards, it's now
            sitting in the wrong slot and you'll never find it again. That's why Python won't let you use a list as a
            dict key; use a tuple or a string. Java will let you use a `List`, which is worse, because nothing stops you
            changing it later.

            When you squash a structured key into a string, put separators in. The counts `{AMB_A}` and `{AMB_B}` both
            turn into `"{"".join(map(str, AMB_A))}"` if you just glue the numbers together, so two different keys
            collide. Write `"1#11"` and `"11#1"`, or use a tuple.

            ### Picking between two correct keys

            For anagrams of words of length `L`, both "sorted letters" and "26 letter counts" are correct. Sorting
            costs O(L log L) per word; counting costs O(L + 26). For short words it hardly matters. For long strings
            over a small alphabet, counting wins. Let the constraints decide.

            ### Numbers can be keys too

            A key doesn't have to be a string. This lesson's code groups numbers made of the same digits, and its key
            is the digits sorted from high to low, read back as a number: 213 becomes 321. It gets both directions
            right. Same digits always give the same key. And different digit counts always give different keys,
            because the zeros sort to the end and stay there, so 100 (key 100) and 10 (key 10) don't get mixed up. An
            integer key is cheap to hash and easy to store, even in C.
            """,
        ]),
        ("template", "The template", [
            """
            Group non-negative integers that use the same digits. Keep the groups in the order their first member
            appeared, and keep the numbers inside each group in input order.

            One small trick here: the map goes from key to the *position* of its group in a list, rather than straight
            to the group. That keeps the groups in first-seen order in every language. A plain hash map wouldn't, and
            the list of groups is the answer anyway.
            """,
            code(
                "Group numbers by their digits",
                GROUP,
                [
                    ("digits", "Count each digit from 0 to 9. The key only depends on how many of each digit there are, "
                               "not where they are.",
                     {"c": "For `x = 0` the loop never runs and the key is 0, which no positive number shares."}),
                    ("build", "Read the digits back out from 9 down to 0. Numbers with the same digits produce the same "
                              "result, and different digits produce different results. A 10-digit number makes a "
                              "10-digit key, which is too big for 32 bits, so the key is 64-bit."),
                    ("make", "A map from key to group position, and the list of groups itself.",
                     {"c": "The table's arrays (keys, group ids, used flags), plus `groupOfItem`, which remembers the group of every input position."}),
                    ("loop", "One pass over the input."),
                    ("sig", "Work out this number's key."),
                    ("new", "A key we haven't seen before gets a new, empty group at the end of the list.",
                     {"cpp": "`emplace` only inserts if the key is new, and `isNew` tells us which happened, all with one lookup.",
                      "java": "`get` gives back `null` for a key we haven't seen, and that's when we start a new group."}),
                    ("put", "Add the number to its group. Equal keys always lead to the same list.",
                     {"c": "Growing lists in C is fiddly, so we just note each number's group now and lay the groups out at the end."}),
                    ("probe", "Hash the 64-bit key (multiply by a big odd constant, keep the high bits) and walk forward "
                              "to the key or an empty slot."),
                    ("place", "Lay the groups out one after another. Count how big each group is, turn those sizes into "
                              "starting positions (a running total, which you'll see properly in *Prefix sums*), then "
                              "drop each number into the next free spot in its group. Numbers keep their input order."),
                    ("free", "Free the temporary arrays."),
                    ("ret", "The groups, in the order their first member appeared.",
                     {"c": "Returns how many groups there are. The grouped numbers are in `out`, and `start` says where each group begins."}),
                ],
                GROUP_RUN,
                "group_by_digits([123, 45, 321, 100, 54, 10, 213, 1, 10])",
            ),
        ]),
        ("trace", "Trace it by hand", [
            f"""
            First, here's how one key gets built. Take {KX}. We count its digits by peeling them off the end one at a
            time, then read them back from the biggest digit down:
            """,
            walk(kwalk),
            "And here are the keys for every number in the example:",
            table(["x", "digits sorted high to low", "key"], *trace_rows),
            "Now the grouping itself:",
            walk(steps),
            f"""
            Notice that no two numbers were ever compared. Each one only met the table. Also notice 100 and 10. They
            share the digits 1 and 0, but they have different keys ({digit_key(100)} and {digit_key(10)}), because the
            key remembers how many zeros there are.
            """,
        ]),
        ("examples", "More examples", [
            """
            ### Grouping words by rotation

            A rotation moves some letters from the front of a word to the back: `cab` → `abc` → `bca`. Which of these
            words are rotations of each other? The key is the smallest of all its rotations (the one that comes first
            alphabetically). Every word in a rotation group has the same set of rotations, so they all pick the same
            smallest one.
            """,
            table(["word", "all its rotations", "key"], *rot_rows),
            fig(M({f'"{k}"': str(v).replace("'", '"') for k, v in ROT_GROUPS.items()}, "key → group"),
                caption="Six words, two groups. Notice `acb` isn't a rotation of `abc`, and the keys keep them apart."),
            f"""
            ### Friendships listed both ways round

            A list of friendships `{FR}` mentions some of them twice, once as `(a, b)` and once as `(b, a)`. How many
            different friendships are there? The key is the pair sorted, so `(3, 1)` and `(1, 3)` both become `(1, 3)`:
            """,
            table(["pair", "key"], *[(str(p), str(k)) for p, k in zip(FR, fr_keys)]),
            f"""
            Put the keys in a set and count them: {FR_DISTINCT}. You don't even need lists of members here, because the
            question only asks how many groups there are.

            ### When you only care about one group

            "How many words have the same pattern as `moon`?" There's only one group you care about. Work out
            `moon`'s key once, (0, 1, 1, 2), then count the words whose key matches. No map needed at all.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Counting groups, not members

            "How many different families are there?" only needs a set of keys. Add every key, then return the size of
            the set. No lists.

            ### Counting matching pairs

            Count how many items share each key (a count map instead of lists). A key with `c` items gives
            `c × (c - 1) / 2` pairs. Or use the one-pass "add the count, then bump it" trick from *Frequency counting*.

            ### Keys built from other structures

            The key can be a whole row of a grid, as a tuple in Python or a string with separators elsewhere. Then
            "does this row match that column?" becomes "do they have the same key?". It can be several attributes at
            once: group people by `(city, age)`, and that tuple is the key. Or it can be a cleaned-up version of the
            item, like a lower-cased word with the punctuation stripped, when the rule is "the same, ignoring case".

            ### Sorting instead of hashing

            You can also sort the items by their key. Items with equal keys end up next to each other, and each run of
            equal keys is a group. That's O(n log n) key comparisons and no hash map, and the groups come out sorted by
            key. Handy in C, or when the answer has to be sorted anyway.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Say there are `n` items and building one key costs `K` (for strings of length `L`, O(L log L) to sort the
            letters, or O(L) to count them).

            Computing all the keys costs O(n · K). Then there are `n` hash map operations, which are O(1) on average,
            except that hashing a key of length `L` itself costs O(L). So for words it's O(n · (K + L)) overall: O(n ·
            L log L) with sorted-letter keys, or O(n · L) with counts. Memory is O(n · L), since every item and its key
            are stored once.

            The alternative, checking every pair of items to see whether they belong together, is O(n²) comparisons,
            each costing at least O(L).
            """,
            table(
                ["Approach", "Time (n words of length L)", "Extra space"],
                ["Compare every pair", "O(n² · L log L)", "O(n)"],
                ["Sorted-letters key + hash map", "O(n · L log L)", "O(n · L)"],
                ["Letter-counts key + hash map", "O(n · (L + 26))", "O(n · (L + 26))"],
                ["Sort the items by key, read off runs", "O(n · K + n log n · L)", "O(n · L)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `defaultdict(list)` with `groups[key].append(item)`. Keys have to be hashable, so use `tuple(...)` or
            `"".join(sorted(word))`, never a list. Dicts remember insertion order, so `list(groups.values())` comes out
            in first-seen order.

            ### Java

            `map.computeIfAbsent(key, k -> new ArrayList<>()).add(item)`. A `String` key is compared by its contents,
            but an `int[]` key is compared by identity, so two arrays with the same numbers count as different keys.
            Convert with `Arrays.toString(arr)` or `new String(charArray)`. `HashMap` doesn't keep any order; use
            `LinkedHashMap` for insertion order, or the position trick from the template.

            ### C++

            `unordered_map<string, vector<string>>`, and `groups[key].push_back(item)` creates the list for you. A
            `vector<int>` or `pair` key works in `std::map` (which is sorted) but needs a custom hash for
            `unordered_map`, so people often turn it into a string with separators. `std::array<int, 26>` works as a
            `map` key.

            ### C

            An integer key, like this lesson's, is the easiest: an open-addressing table on 64-bit keys. For string
            keys, either hash the string yourself (FNV-1a is a simple choice, checking with `strcmp` when hashes match)
            or sort an array of `(key, index)` pairs with `qsort` and read off the runs.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            Things to watch for:

            - A key that merges groups it shouldn't. Sums, lengths or a hash on its own do this. Test your key on two
              items that *shouldn't* end up together.
            - A key that splits a group. For shifted words, the gaps between letters have to be taken mod 26, or `"az"`
              (gap 25) and `"ba"` (gap -1) end up in different groups. Normalise every part of the key.
            - Ambiguous string keys. Join numbers with a separator: `"1#11"`, not `"111"`.
            - Changing a key after it's been used. Never modify a list or array you've already used as a key.
            - Output order. If the answer has to be sorted (groups, or items inside groups), sort it yourself at the
              end. Don't rely on the order the map gives you.
            - Empty items and duplicates. An empty string has an empty key and forms a group of its own. Identical
              items have identical keys and belong in the same group; keep both copies if the problem says to.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why isn't \"the number of different letters\" a good key for grouping anagrams?",
                 "It gets one direction right (anagrams always have the same number of different letters) but not the other: `\"ab\"` and `\"cd\"` both have two different letters, so they'd be grouped together even though they aren't anagrams."),
                ("Two words have the same pattern if you can turn one into the other by swapping letters consistently, one for one. What's a good key?",
                 "Replace each letter with the order it first appeared in: `\"moon\"` becomes (0, 1, 1, 2), and so does `\"feet\"`. Two words get the same tuple exactly when their patterns match."),
                ("Why does the template map each key to a group *position* rather than straight to a list?",
                 "So all the groups live in one list, in the order they first appeared, in every language. Looping over a Java `HashMap` or C++ `unordered_map` would give you the groups in some arbitrary order."),
                ("Rows `[1, 11]` and `[11, 1]` are turned into keys by gluing the numbers together. What goes wrong?",
                 "Both become `\"111\"`, so they're wrongly grouped together. Use a separator (`\"1#11\"` and `\"11#1\"`) or a tuple."),
                ("\"Group words that differ in at most one letter.\" Can a key do this?",
                 "No. That rule doesn't chain properly: `cat` is one letter from `cot`, and `cot` is one from `dot`, but `cat` and `dot` differ in two letters. So it doesn't split words into clean groups. You'd need union-find or a graph search."),
            ),
        ]),
    ],
)
