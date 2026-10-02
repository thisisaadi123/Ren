"""Arrays & Hashing: group by key."""
from collections import defaultdict

from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

# Shared C tail for Anagram Groups: sort each group, order the groups, hand them back.
C_ANAGRAM_FINISH = """
    typedef struct { char** words; int size; } Group;  //@order

    static int cmpStr(const void* a, const void* b) {  //@order
        return strcmp(*(char* const*) a, *(char* const*) b);  //@order
    }  //@order

    static int byFirstWord(const void* a, const void* b) {  //@order
        return strcmp(((const Group*) a)->words[0], ((const Group*) b)->words[0]);  //@order
    }  //@order

    // Sort each group's words, order the groups by their first word, and return them.
    static char*** finish(Group* groups, int g, int* returnSize, int** returnColumnSizes) {  //@order
        for (int k = 0; k < g; k++) qsort(groups[k].words, groups[k].size, sizeof(char*), cmpStr);  //@order
        qsort(groups, g, sizeof(Group), byFirstWord);  //@order
        char*** out = malloc(g * sizeof(char**));  //@order
        *returnColumnSizes = malloc(g * sizeof(int));  //@order
        for (int k = 0; k < g; k++) {  //@order
            out[k] = groups[k].words;  //@order
            (*returnColumnSizes)[k] = groups[k].size;  //@order
        }  //@order
        *returnSize = g;  //@order
        free(groups);  //@order
        return out;  //@order
    }  //@order
"""
ORDER_ROW = ("order", "The required output order: words sorted inside each group, groups ordered by their first word. Different groups can never share a first word (equal words are anagrams), so that order is unambiguous.",
             {"c": "A group is an array of word pointers and its size. `finish` sorts each group with `strcmp`, sorts the groups by first word, and returns them with each group's length in `returnColumnSizes`. The words themselves are the input's strings; only the arrays are new."})


@problem
def anagram_groups():
    words = ["pots", "tea", "stop", "eat", "opts", "tan", "ate"]
    expect = sorted(sorted(g) for g in _anagram_ref(words).values())
    assert expect == [["ate", "eat", "tea"], ["opts", "pots", "stop"], ["tan"]]

    w1 = Steps("Compare each word's letter counts with each existing group's; join the first match or start a group.")
    groups = []
    for i, w in enumerate(words):
        hit = None
        for k, g in enumerate(groups):
            if sorted(g[0]) == sorted(w):
                hit = k
                break
        if hit is None:
            groups.append([w])
            text = f"'{w}' matches none of the {len(groups) - 1} group{'s' if len(groups) != 2 else ''}: new group."
        else:
            groups[hit].append(w)
            text = f"'{w}' has the same letter counts as '{groups[hit][0]}' (checked {hit + 1} group{'s' if hit else ''}): join it."
        w1.step(text, Row(words, st={**{q: "dim" for q in range(i)}, i: "active"}), *[Row(g, label=f"group {k + 1}", st={len(g) - 1: "new"} if (hit == k or (hit is None and k == len(groups) - 1)) else None) for k, g in enumerate(groups)])
    w1.step("Sort inside groups, then order groups by first word.", *[Row(g, label=f"group {k + 1}") for k, g in enumerate(expect)], result=expect)

    w2 = Steps("Pair each word with its letters sorted. Sorting the pairs puts anagrams side by side.")
    pairs = sorted(("".join(sorted(w)), w) for w in words)
    w2.step("Each word's key is its letters in alphabetical order. Anagrams get the same key.", Row(words, label="word"), Row(["".join(sorted(w)) for w in words], label="key"))
    w2.step("Sort by (key, word).", Row([p[0] for p in pairs], label="key"), Row([p[1] for p in pairs], label="word"))
    runs, i = [], 0
    while i < len(pairs):
        j = i
        while j < len(pairs) and pairs[j][0] == pairs[i][0]:
            j += 1
        runs.append((i, j))
        w2.step(f"Key '{pairs[i][0]}' runs from {i} to {j - 1}: one group, {[p[1] for p in pairs[i:j]]}.", Row([p[0] for p in pairs], st={q: "answer" for q in range(i, j)}, label="key"), Row([p[1] for p in pairs], st={q: "answer" for q in range(i, j)}, label="word"))
        i = j
    w2.step("Order the groups by first word.", *[Row(g) for g in expect], result=expect)

    w3 = Steps("Turn each word into its 26 letter counts and use that as a hash-map key.")
    m = defaultdict(list)
    for i, w in enumerate(words):
        sig = "".join(f"{c}{w.count(c)}" for c in sorted(set(w)))
        new = sig not in m
        m[sig].append(w)
        keys = list(m)
        w3.step(f"'{w}' → counts {sig}" + (": a new key." if new else f": key already there, append."), Row(words, st={**{q: "dim" for q in range(i)}, i: "active"}),
                Row([f"{k}: {','.join(m[k])}" for k in keys], st={keys.index(sig): "new"}, label="counts → words"))
    w3.step("Each map entry is one group. Sort and order them for the output.", *[Row(g) for g in expect], result=expect)

    sol(
        "anagram-groups",
        summary="""
            Two words are anagrams exactly when they have the same letters in the same amounts. Turn every word
            into a **key** that captures just that (its letters sorted, or its 26 letter counts), and group words
            by key with a hash map. Then sort for the required output order.
        """,
        question=[
            """
            Put words that are anagrams of each other (same letters, rearranged) in the same group.

            - **"Same letters" means same counts.** `"aab"` and `"abb"` both use a and b, but they aren't
              anagrams.
            - **The output order is fixed**, so there's one right answer: words sorted inside each group, groups
              ordered by their first word.
            - **Duplicates stay:** `["ab", "ba", "ab"]` gives `[["ab", "ab", "ba"]]`.
            - **The empty word** is a valid word and forms a group with other empty words.
            - **Size:** up to 10⁴ words of at most 30 lowercase letters.
            """
        ],
        think=[
            """
            Take `["pots", "tea", "stop", "eat", "opts", "tan", "ate"]`. By hand you'd notice that tea, eat and
            ate all "spell" a-e-t if you rearrange the letters. That's the trick: give each word a **fingerprint**
            that doesn't depend on letter order.
            """,
            fig(Row(words, label="word"), Row(["".join(sorted(w)) for w in words], label="letters sorted"),
                caption="Anagrams get the same fingerprint: aet, opst, ant."),
            """
            Two good fingerprints:

            - **The letters in sorted order:** `"tea"` → `"aet"`. Costs a small sort per word.
            - **The 26 letter counts:** `"tea"` → a:1, e:1, t:1, zeros elsewhere. Costs one pass per word.

            Once every word has a fingerprint, "group anagrams" becomes "group equal keys", which a hash map
            does in one pass (or a sort, which puts equal keys next to each other).
            """,
        ],
        approaches=[
            approach(
                "Compare each word with every group",
                "brute",
                "O(n · g · L)",
                "O(n · L)",
                idea=["Keep a list of groups, each with its letter counts. For each word, count its letters and compare against every group until one matches; if none does, start a new group. Finally sort for the output order."],
                walk=w1,
                build=[
                    "For each word, count its 26 letters.",
                    "Scan the existing groups; join the first group with identical counts.",
                    "If none matches, start a new group with these counts.",
                    "Sort words in each group, then order groups by first word.",
                ],
                code={
                    "python": """
                        class Solution:
                            def groupAnagrams(self, words: List[str]) -> List[List[str]]:
                                counts, groups = [], []  #@lists
                                for w in words:  #@each
                                    c = [0] * 26  #@count
                                    for ch in w:  #@count
                                        c[ord(ch) - 97] += 1  #@count
                                    for k in range(len(groups)):  #@scan
                                        if counts[k] == c:  #@scan
                                            groups[k].append(w)  #@scan
                                            break  #@scan
                                    else:  #@new
                                        counts.append(c)  #@new
                                        groups.append([w])  #@new
                                result = [sorted(g) for g in groups]  #@order
                                result.sort(key=lambda g: g[0])  #@order
                                return result  #@order
                    """,
                    "java": """
                        class Solution {
                            public String[][] groupAnagrams(String[] words) {
                                List<int[]> counts = new ArrayList<>();  //@lists
                                List<List<String>> groups = new ArrayList<>();  //@lists
                                for (String w : words) {  //@each
                                    int[] c = new int[26];  //@count
                                    for (char ch : w.toCharArray()) c[ch - 'a']++;  //@count
                                    int k = 0;  //@scan
                                    while (k < groups.size() && !Arrays.equals(counts.get(k), c)) k++;  //@scan
                                    if (k == groups.size()) {  //@new
                                        counts.add(c);  //@new
                                        groups.add(new ArrayList<>());  //@new
                                    }
                                    groups.get(k).add(w);  //@scan
                                }
                                for (List<String> g : groups) Collections.sort(g);  //@order
                                groups.sort(Comparator.comparing(g -> g.get(0)));  //@order
                                String[][] out = new String[groups.size()][];  //@order
                                for (int i = 0; i < out.length; i++) out[i] = groups.get(i).toArray(new String[0]);  //@order
                                return out;  //@order
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<string>> groupAnagrams(vector<string>& words) {
                                vector<array<int, 26>> counts;  //@lists
                                vector<vector<string>> groups;  //@lists
                                for (const string& w : words) {  //@each
                                    array<int, 26> c{};  //@count
                                    for (char ch : w) c[ch - 'a']++;  //@count
                                    size_t k = 0;  //@scan
                                    while (k < groups.size() && counts[k] != c) k++;  //@scan
                                    if (k == groups.size()) {  //@new
                                        counts.push_back(c);  //@new
                                        groups.push_back({});  //@new
                                    }
                                    groups[k].push_back(w);  //@scan
                                }
                                for (auto& g : groups) sort(g.begin(), g.end());  //@order
                                sort(groups.begin(), groups.end(), [](auto& a, auto& b) { return a[0] < b[0]; });  //@order
                                return groups;  //@order
                            }
                        };
                    """,
                    "c": C_ANAGRAM_FINISH + """
                        char*** groupAnagrams(char** words, int wordsSize, int* returnSize, int** returnColumnSizes) {
                            int (*counts)[26] = malloc(wordsSize * sizeof *counts);  //@lists
                            int* gid = malloc(wordsSize * sizeof(int));  //@lists
                            int* size = calloc(wordsSize, sizeof(int));  //@lists
                            int g = 0;  //@lists
                            for (int i = 0; i < wordsSize; i++) {  //@each
                                int c[26] = {0};  //@count
                                for (char* p = words[i]; *p; p++) c[*p - 'a']++;  //@count
                                int k = 0;  //@scan
                                while (k < g && memcmp(counts[k], c, sizeof c) != 0) k++;  //@scan
                                if (k == g) memcpy(counts[g++], c, sizeof c);  //@new
                                gid[i] = k;  //@scan
                                size[k]++;  //@scan
                            }
                            Group* groups = malloc(g * sizeof(Group));  //@build
                            for (int k = 0; k < g; k++) {  //@build
                                groups[k].words = malloc(size[k] * sizeof(char*));  //@build
                                groups[k].size = 0;  //@build
                            }  //@build
                            for (int i = 0; i < wordsSize; i++) {  //@build
                                Group* t = &groups[gid[i]];  //@build
                                t->words[t->size++] = words[i];  //@build
                            }  //@build
                            free(counts);  //@build
                            free(gid);  //@build
                            free(size);  //@build
                            return finish(groups, g, returnSize, returnColumnSizes);  //@order
                        }
                    """,
                },
                lines=[
                    ORDER_ROW,
                    ("lists", "Each group's letter counts, kept side by side with the group's words.",
                     {"c": "One row of 26 counts per group (at most n groups), plus each word's group id and each group's size, so the groups can be built at exactly the right size afterwards."}),
                    ("each", "One word at a time."),
                    ("count", "The word's fingerprint: how many of each letter."),
                    ("scan", "Compare with every group's counts until one matches; the word joins that group.",
                     {"c": "`memcmp` compares the 26 counts as raw memory: equal bytes means equal counts. Record the group id and grow its size."}),
                    ("new", "No group matched: this word starts a new one, and its counts become the group's fingerprint."),
                    ("build", "Second pass: allocate each group at its final size and drop the words in.", {}),
                ],
                complexity=[
                    """
                    **Time O(n · g · L)** in the spirit of the problem (each of n words is compared with up to g groups;
                    with 26 counts per comparison and L ≤ 30, each comparison is O(26)). With 10⁴ distinct groups that's
                    ~10⁸ comparisons, plus the output sort.

                    **Space O(n · L)** for the groups.
                    """
                ],
                limits=["Finding a word's group is a linear search through all groups. A key that can be **looked up** (hash map) or **sorted** removes that search."],
                slow=True,
            ),
            approach(
                "Sort by sorted-letter key, then cut into runs",
                "better",
                "O(n · L · log n)",
                "O(n · L)",
                idea=[
                    """
                    Give every word the key "its letters sorted" (`"tea"` → `"aet"`). Sort the (key, word) pairs.
                    Anagrams now sit next to each other, and since ties are broken by the word, each run is already
                    sorted inside. Cut the list wherever the key changes, then order the groups by first word.
                    """
                ],
                walk=w2,
                build=[
                    "For each word, build its key by sorting its letters.",
                    "Sort (key, word) pairs by key, then word.",
                    "Walk the sorted pairs; start a new group whenever the key changes.",
                    "Order the groups by their first word.",
                ],
                code={
                    "python": """
                        class Solution:
                            def groupAnagrams(self, words: List[str]) -> List[List[str]]:
                                pairs = sorted(("".join(sorted(w)), w) for w in words)  #@sort
                                result = []  #@runs
                                for i, (key, w) in enumerate(pairs):  #@runs
                                    if i == 0 or key != pairs[i - 1][0]:  #@runs
                                        result.append([])  #@runs
                                    result[-1].append(w)  #@runs
                                result.sort(key=lambda g: g[0])  #@order
                                return result  #@order
                    """,
                    "java": """
                        class Solution {
                            public String[][] groupAnagrams(String[] words) {
                                int n = words.length;
                                String[] key = new String[n];  //@sort
                                Integer[] idx = new Integer[n];  //@sort
                                for (int i = 0; i < n; i++) {  //@sort
                                    char[] c = words[i].toCharArray();  //@sort
                                    Arrays.sort(c);  //@sort
                                    key[i] = new String(c);  //@sort
                                    idx[i] = i;  //@sort
                                }  //@sort
                                Arrays.sort(idx, (a, b) -> {  //@sort
                                    int c = key[a].compareTo(key[b]);  //@sort
                                    return c != 0 ? c : words[a].compareTo(words[b]);  //@sort
                                });  //@sort
                                List<List<String>> groups = new ArrayList<>();  //@runs
                                for (int i = 0; i < n; i++) {  //@runs
                                    if (i == 0 || !key[idx[i]].equals(key[idx[i - 1]])) groups.add(new ArrayList<>());  //@runs
                                    groups.get(groups.size() - 1).add(words[idx[i]]);  //@runs
                                }
                                groups.sort(Comparator.comparing(g -> g.get(0)));  //@order
                                String[][] out = new String[groups.size()][];  //@order
                                for (int i = 0; i < out.length; i++) out[i] = groups.get(i).toArray(new String[0]);  //@order
                                return out;  //@order
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<string>> groupAnagrams(vector<string>& words) {
                                vector<pair<string, string>> pairs;  //@sort
                                for (const string& w : words) {  //@sort
                                    string key = w;  //@sort
                                    sort(key.begin(), key.end());  //@sort
                                    pairs.push_back({key, w});  //@sort
                                }  //@sort
                                sort(pairs.begin(), pairs.end());  //@sort
                                vector<vector<string>> groups;  //@runs
                                for (size_t i = 0; i < pairs.size(); i++) {  //@runs
                                    if (i == 0 || pairs[i].first != pairs[i - 1].first) groups.push_back({});  //@runs
                                    groups.back().push_back(pairs[i].second);  //@runs
                                }
                                sort(groups.begin(), groups.end(), [](auto& a, auto& b) { return a[0] < b[0]; });  //@order
                                return groups;  //@order
                            }
                        };
                    """,
                    "c": C_ANAGRAM_FINISH + """
                        typedef struct { char* key; char* word; } Pair;  //@pair

                        static int cmpChar(const void* a, const void* b) {  //@pair
                            return *(const char*) a - *(const char*) b;  //@pair
                        }  //@pair

                        static int byKeyThenWord(const void* a, const void* b) {  //@pair
                            const Pair* x = a;  //@pair
                            const Pair* y = b;  //@pair
                            int c = strcmp(x->key, y->key);  //@pair
                            return c ? c : strcmp(x->word, y->word);  //@pair
                        }  //@pair

                        char*** groupAnagrams(char** words, int wordsSize, int* returnSize, int** returnColumnSizes) {
                            int n = wordsSize;
                            Pair* pairs = malloc(n * sizeof(Pair));  //@sort
                            for (int i = 0; i < n; i++) {  //@sort
                                size_t len = strlen(words[i]);  //@sort
                                pairs[i].key = malloc(len + 1);  //@sort
                                memcpy(pairs[i].key, words[i], len + 1);  //@sort
                                qsort(pairs[i].key, len, 1, cmpChar);  //@sort
                                pairs[i].word = words[i];  //@sort
                            }  //@sort
                            qsort(pairs, n, sizeof(Pair), byKeyThenWord);  //@sort
                            Group* groups = malloc(n * sizeof(Group));  //@runs
                            int g = 0;  //@runs
                            for (int i = 0; i < n;) {  //@runs
                                int j = i;  //@runs
                                while (j < n && strcmp(pairs[j].key, pairs[i].key) == 0) j++;  //@runs
                                groups[g].words = malloc((j - i) * sizeof(char*));  //@runs
                                groups[g].size = j - i;  //@runs
                                for (int k = i; k < j; k++) groups[g].words[k - i] = pairs[k].word;  //@runs
                                g++;  //@runs
                                i = j;  //@runs
                            }  //@runs
                            for (int i = 0; i < n; i++) free(pairs[i].key);  //@runs
                            free(pairs);  //@runs
                            return finish(groups, g, returnSize, returnColumnSizes);  //@order
                        }
                    """,
                },
                lines=[
                    ORDER_ROW,
                    ("pair", "A word together with its key, and a comparator that orders by key, then by the word itself."),
                    ("sort", "Every word gets its sorted-letter key, and the (key, word) pairs are sorted. Equal keys become adjacent, and within a key the words come out in order.",
                     {"java": "Sorting an index array lets the keys and words stay in their own arrays.", "c": "Each key is a sorted copy of the word; the pairs are sorted with `qsort`."}),
                    ("runs", "A new group starts wherever the key differs from the previous pair's key.", {"c": "Find where each run of equal keys ends, copy its words into a group, then free the keys."}),
                ],
                complexity=[
                    """
                    **Time O(n · L · log n):** building keys costs O(L log L) per word, and sorting n pairs costs
                    O(n log n) comparisons of up to L characters each. **Space O(n · L)** for the keys.
                    """
                ],
                limits=[
                    """
                    The big sort does the grouping by comparing strings, about n log n times. A hash map groups
                    equal keys in one pass instead; only the (required) output ordering still needs a sort.
                    """
                ],
            ),
            approach(
                "Hash map keyed by letter counts",
                "best",
                "O(n · L · log n)",
                "O(n · L)",
                idea=[
                    """
                    Use the 26 letter counts as the key of a hash map from key to the list of words. Each word costs
                    one O(L) pass to count and one map lookup; the map's lists are the groups. Then sort each group
                    and order the groups, because the output format requires it.

                    The grouping itself is O(n · L), linear in the input size. The final O(n log n) ordering is only
                    there because the problem asks for a canonical order.
                    """
                ],
                walk=w3,
                build=[
                    "For each word, count its 26 letters.",
                    "Turn the counts into a hashable key and append the word to `groups[key]`.",
                    "Sort each group's words, then order the groups by first word.",
                ],
                code={
                    "python": """
                        from collections import defaultdict

                        class Solution:
                            def groupAnagrams(self, words: List[str]) -> List[List[str]]:
                                groups = defaultdict(list)  #@map
                                for w in words:  #@each
                                    count = [0] * 26  #@count
                                    for ch in w:  #@count
                                        count[ord(ch) - 97] += 1  #@count
                                    groups[tuple(count)].append(w)  #@put
                                result = [sorted(g) for g in groups.values()]  #@order
                                result.sort(key=lambda g: g[0])  #@order
                                return result  #@order
                    """,
                    "java": """
                        class Solution {
                            public String[][] groupAnagrams(String[] words) {
                                Map<String, List<String>> groups = new HashMap<>();  //@map
                                for (String w : words) {  //@each
                                    char[] count = new char[26];  //@count
                                    for (char ch : w.toCharArray()) count[ch - 'a']++;  //@count
                                    groups.computeIfAbsent(new String(count), k -> new ArrayList<>()).add(w);  //@put
                                }
                                List<List<String>> list = new ArrayList<>(groups.values());  //@order
                                for (List<String> g : list) Collections.sort(g);  //@order
                                list.sort(Comparator.comparing(g -> g.get(0)));  //@order
                                String[][] out = new String[list.size()][];  //@order
                                for (int i = 0; i < out.length; i++) out[i] = list.get(i).toArray(new String[0]);  //@order
                                return out;  //@order
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<string>> groupAnagrams(vector<string>& words) {
                                unordered_map<string, vector<string>> groups;  //@map
                                for (const string& w : words) {  //@each
                                    string count(26, '\\0');  //@count
                                    for (char ch : w) count[ch - 'a']++;  //@count
                                    groups[count].push_back(w);  //@put
                                }
                                vector<vector<string>> result;  //@order
                                for (auto& [key, g] : groups) {  //@order
                                    sort(g.begin(), g.end());  //@order
                                    result.push_back(move(g));  //@order
                                }  //@order
                                sort(result.begin(), result.end(), [](auto& a, auto& b) { return a[0] < b[0]; });  //@order
                                return result;  //@order
                            }
                        };
                    """,
                    "c": C_ANAGRAM_FINISH + """
                        static unsigned long long hashCounts(const int* c) {  //@hash
                            unsigned long long h = 1469598103934665603ULL;  //@hash
                            for (int i = 0; i < 26; i++) h = (h ^ (unsigned) c[i]) * 1099511628211ULL;  //@hash
                            return h;  //@hash
                        }  //@hash

                        char*** groupAnagrams(char** words, int wordsSize, int* returnSize, int** returnColumnSizes) {
                            int n = wordsSize;
                            unsigned cap = 1;  //@map
                            while (cap < 2u * n) cap <<= 1;  //@map
                            int* slot = malloc(cap * sizeof(int));  //@map
                            for (unsigned s = 0; s < cap; s++) slot[s] = -1;  //@map
                            int (*counts)[26] = malloc(n * sizeof *counts);  //@map
                            int* gid = malloc(n * sizeof(int));  //@map
                            int* size = calloc(n, sizeof(int));  //@map
                            int g = 0;  //@map
                            for (int i = 0; i < n; i++) {  //@each
                                int c[26] = {0};  //@count
                                for (char* p = words[i]; *p; p++) c[*p - 'a']++;  //@count
                                unsigned s = (unsigned) (hashCounts(c) >> 32) & (cap - 1);  //@put
                                while (slot[s] != -1 && memcmp(counts[slot[s]], c, sizeof c) != 0) s = (s + 1) & (cap - 1);  //@put
                                if (slot[s] == -1) {  //@put
                                    memcpy(counts[g], c, sizeof c);  //@put
                                    slot[s] = g++;  //@put
                                }  //@put
                                gid[i] = slot[s];  //@put
                                size[slot[s]]++;  //@put
                            }
                            Group* groups = malloc(g * sizeof(Group));  //@build
                            for (int k = 0; k < g; k++) {  //@build
                                groups[k].words = malloc(size[k] * sizeof(char*));  //@build
                                groups[k].size = 0;  //@build
                            }  //@build
                            for (int i = 0; i < n; i++) groups[gid[i]].words[groups[gid[i]].size++] = words[i];  //@build
                            free(slot);  //@build
                            free(counts);  //@build
                            free(gid);  //@build
                            free(size);  //@build
                            return finish(groups, g, returnSize, returnColumnSizes);  //@order
                        }
                    """,
                },
                lines=[
                    ORDER_ROW,
                    ("hash", "C has no hash map, so this turns 26 counts into a 64-bit hash (FNV-1a: mix in each value with XOR, then multiply by a large prime)."),
                    ("map", "A hash map from a word's letter counts to its group.",
                     {"python": "`defaultdict(list)` creates an empty list the first time a key is used.",
                      "c": "The table stores group ids (−1 = empty); each group's counts live in `counts[id]`, so a probe compares the actual counts and hash collisions can't merge different groups."}),
                    ("each", "One pass over the words."),
                    ("count", "The fingerprint: 26 letter counts, one O(L) pass.",
                     {"java": "A `char` per letter is enough (counts ≤ 30), and 26 chars make a compact `String` key.",
                      "cpp": "26 chars as a `string`: compact and already hashable."}),
                    ("put", "Append the word to its key's list, creating the list the first time.",
                     {"python": "Lists can't be dictionary keys, so the counts become a tuple.",
                      "java": "`computeIfAbsent` makes the list on first use.",
                      "cpp": "`groups[count]` creates an empty vector for a new key.",
                      "c": "Probe from the hash's slot until we find the group with identical counts or an empty slot, which becomes a new group."}),
                    ("build", "Allocate each group at its final size and fill in the words."),
                ],
                complexity=[
                    """
                    **Time:** grouping is **O(n · L)** (one counting pass and one O(1) map operation per word). The
                    required output order adds a sort, **O(n · L · log n)** in total. Without the fixed output order the
                    whole solution would be linear.

                    **Space O(n · L)** for the groups and keys.
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - **Group by key:** design a key that is equal exactly for items that belong together, then let a hash
              map collect them.
            - For anagrams the key can be the sorted letters (O(L log L)) or the letter counts (O(L) with a small
              alphabet).
            - Sorting by key is the hash-free fallback: equal keys become adjacent runs.
            - Read the required output format carefully; a canonical order can dominate the running time.
            """
        ],
    )


def _anagram_ref(words):
    g = defaultdict(list)
    for w in words:
        g["".join(sorted(w))].append(w)
    return g


@problem
def matching_rows_and_columns():
    grid = [[3, 1, 2, 2], [1, 4, 4, 5], [2, 4, 2, 2], [2, 4, 2, 2]]
    n = len(grid)
    cols = [[grid[k][c] for k in range(n)] for c in range(n)]
    total = sum(grid[r] == cols[c] for r in range(n) for c in range(n))
    assert total == 3

    def col_st(c, state):
        return {(k, c): state for k in range(n)}

    def row_st(r, state):
        return {(r, k): state for k in range(n)}

    w1 = Steps("Compare every row with every column, cell by cell.")
    t = 0
    for r in range(n):
        for c in range(n):
            ok = grid[r] == cols[c]
            t += ok
            if ok or (r + c) % 3 == 0:
                st = {**row_st(r, "active"), **col_st(c, "answer" if ok else "mark")}
                if ok:
                    st.update(row_st(r, "answer"))
                w1.step(f"Row {r} {grid[r]} vs column {c} {cols[c]}: " + ("equal. Count " + str(t) + "." if ok else "differ."), Grid(grid, st=st), Vars(count=t))
    w1.step(f"All {n * n} pairs checked: {t}.", Grid(grid), result=t)

    w2 = Steps("Sort the rows. Then each column can binary-search for rows equal to it.")
    srows = sorted(grid)
    w2.step("Rows in sorted (lexicographic) order. Equal rows end up together.", Grid(srows))
    t = 0
    for c in range(n):
        eq = [i for i, r in enumerate(srows) if r == cols[c]]
        t += len(eq)
        w2.step(f"Column {c} = {cols[c]}: binary search finds {len(eq)} equal row{'s' if len(eq) != 1 else ''}. Total {t}.", Grid(srows, st={(i, k): "answer" for i in eq for k in range(n)}), Row(cols[c], label=f"column {c}"), Vars(count=t))
    w2.step(f"Answer {t}.", Grid(grid), result=t)

    w3 = Steps("Count whole rows in a hash map. Each column is then one lookup.")
    cnt = {}
    for r in range(n):
        key = tuple(grid[r])
        cnt[key] = cnt.get(key, 0) + 1
        keys = list(cnt)
        w3.step(f"Row {r} {grid[r]} → count {cnt[key]}.", Grid(grid, st=row_st(r, "active")), Row([f"{list(k)}×{cnt[k]}" for k in keys], st={keys.index(key): "new"}, label="row → count"))
    t = 0
    keys = list(cnt)
    for c in range(n):
        got = cnt.get(tuple(cols[c]), 0)
        t += got
        w3.step(f"Column {c} {cols[c]}: " + (f"{got} equal row{'s' if got > 1 else ''}. Total {t}." if got else "no equal row."), Grid(grid, st=col_st(c, "answer" if got else "active")), Row([f"{list(k)}×{cnt[k]}" for k in keys], st={keys.index(tuple(cols[c])): "answer"} if got else None, label="row → count"), Vars(count=t))
    w3.step(f"Answer {t}.", Grid(grid), result=t)

    sol(
        "matching-rows-and-columns",
        summary="""
            Treat each whole row as a single key: count rows in a hash map, then for each column look up how many
            rows equal it. That's O(n²), which is the size of the grid, instead of comparing every row with every
            column cell by cell, O(n³).
        """,
        question=[
            """
            Count pairs `(r, c)` where row `r`, read left to right, is exactly the same sequence as column `c`, read
            top to bottom.

            - **Same values in the same order**, element by element: row `[2, 7, 7]` matches column `[2, 7, 7]`
              but not `[7, 2, 7]`.
            - **Pairs, not distinct rows.** If two identical rows both match a column, that's 2 pairs. In
              `[[1, 1], [1, 1]]` every row matches every column: 4 pairs.
            - **Square grid**, so rows and columns have the same length n.
            - **Size:** n up to 600, so n³ = 2.16 × 10⁸ cell comparisons is too slow for a 1-second limit in
              most languages, while n² = 360,000 cells is trivial.
            """
        ],
        think=[
            """
            Take this 4 × 4 grid. Row 0 is `[3, 1, 2, 2]`; column 0 (read downwards) is also `[3, 1, 2, 2]`, so
            `(0, 0)` counts. Column 2 is `[2, 4, 2, 2]`, which equals both row 2 and row 3: two more pairs.
            Total: 3.
            """,
            fig(Grid(grid, st={**{(r, 2): "answer" for r in range(n)}, **{(2, k): "found" for k in range(n)}, **{(3, k): "found" for k in range(n)}}),
                caption="Column 2 (dark) reads 2, 4, 2, 2: the same as rows 2 and 3 (light)."),
            """
            Comparing a row and a column costs n steps, and there are n² pairs, so brute force is n³. But we
            don't need to compare *pairs*. We need, for each column, **how many rows are equal to it**. That's a
            counting question: if rows could be looked up as whole values, each column would be one lookup.

            A whole row can be a key: a tuple in Python, a `List<Integer>` in Java, a `vector<int>` (with a
            hash function) in C++, or a hash of its values plus a full comparison in C.
            """,
        ],
        approaches=[
            approach(
                "Compare every row with every column",
                "brute",
                "O(n³)",
                "O(1)",
                idea=["For every `(r, c)`, walk `k` from 0 to n − 1 and check `grid[r][k] == grid[k][c]`. Count the pairs where all n match."],
                walk=w1,
                build=["Loop over rows `r` and columns `c`.", "Check every position `k`: `grid[r][k]` against `grid[k][c]`, stopping at the first difference.", "Count the pairs that never differ."],
                code={
                    "python": """
                        class Solution:
                            def countMatchingPairs(self, grid: List[List[int]]) -> int:
                                n = len(grid)
                                total = 0
                                for r in range(n):  #@pairs
                                    for c in range(n):  #@pairs
                                        if all(grid[r][k] == grid[k][c] for k in range(n)):  #@cmp
                                            total += 1  #@cmp
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countMatchingPairs(int[][] grid) {
                                int n = grid.length, total = 0;
                                for (int r = 0; r < n; r++) {  //@pairs
                                    for (int c = 0; c < n; c++) {  //@pairs
                                        int k = 0;  //@cmp
                                        while (k < n && grid[r][k] == grid[k][c]) k++;  //@cmp
                                        if (k == n) total++;  //@cmp
                                    }
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countMatchingPairs(vector<vector<int>>& grid) {
                                int n = grid.size(), total = 0;
                                for (int r = 0; r < n; r++) {  //@pairs
                                    for (int c = 0; c < n; c++) {  //@pairs
                                        int k = 0;  //@cmp
                                        while (k < n && grid[r][k] == grid[k][c]) k++;  //@cmp
                                        if (k == n) total++;  //@cmp
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countMatchingPairs(int** grid, int gridSize, int* gridColSize) {
                            int n = gridSize, total = 0;
                            for (int r = 0; r < n; r++) {  //@pairs
                                for (int c = 0; c < n; c++) {  //@pairs
                                    int k = 0;  //@cmp
                                    while (k < n && grid[r][k] == grid[k][c]) k++;  //@cmp
                                    if (k == n) total++;  //@cmp
                                }
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("pairs", "Every (row, column) pair: n² of them."),
                    ("cmp", "Row `r`'s k-th value is `grid[r][k]`; column `c`'s k-th value is `grid[k][c]`. Walk until they differ; reaching `n` means all matched."),
                    ("ret", "The number of matching pairs (at most n² = 360,000, fine for `int`)."),
                ],
                complexity=["**Time O(n³):** n² pairs × up to n comparisons. **Space O(1).**"],
                limits=["Each row is compared against every column separately, even though many rows (or columns) may be identical. Organising the rows once, by sorting or hashing, lets each column find its matches directly."],
                slow=3000,
            ),
            approach(
                "Sort the rows, binary-search each column",
                "better",
                "O(n² log n)",
                "O(n²)",
                idea=["Sort the rows lexicographically (like words in a dictionary). Identical rows become neighbours. For each column, binary-search the first and last row equal to it; the distance is the number of matching rows."],
                walk=w2,
                build=["Copy the rows and sort them lexicographically.", "For each column, build it as a list.", "Find the range of rows equal to it with two binary searches; add its length."],
                code={
                    "python": """
                        from bisect import bisect_left, bisect_right

                        class Solution:
                            def countMatchingPairs(self, grid: List[List[int]]) -> int:
                                rows = sorted(tuple(r) for r in grid)  #@sort
                                total = 0
                                for col in zip(*grid):  #@col
                                    total += bisect_right(rows, col) - bisect_left(rows, col)  #@range
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countMatchingPairs(int[][] grid) {
                                int n = grid.length;
                                int[][] rows = grid.clone();  //@sort
                                Arrays.sort(rows, Arrays::compare);  //@sort
                                int total = 0;
                                int[] col = new int[n];  //@col
                                for (int c = 0; c < n; c++) {  //@col
                                    for (int k = 0; k < n; k++) col[k] = grid[k][c];  //@col
                                    total += bound(rows, col, true) - bound(rows, col, false);  //@range
                                }
                                return total;  //@ret
                            }

                            // First row > col (upper) or >= col (lower).
                            private int bound(int[][] rows, int[] col, boolean upper) {  //@bound
                                int lo = 0, hi = rows.length;  //@bound
                                while (lo < hi) {  //@bound
                                    int mid = (lo + hi) / 2;  //@bound
                                    int c = Arrays.compare(rows[mid], col);  //@bound
                                    if (c < 0 || (upper && c == 0)) lo = mid + 1; else hi = mid;  //@bound
                                }  //@bound
                                return lo;  //@bound
                            }  //@bound
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countMatchingPairs(vector<vector<int>>& grid) {
                                int n = grid.size();
                                vector<vector<int>> rows = grid;  //@sort
                                sort(rows.begin(), rows.end());  //@sort
                                int total = 0;
                                vector<int> col(n);  //@col
                                for (int c = 0; c < n; c++) {  //@col
                                    for (int k = 0; k < n; k++) col[k] = grid[k][c];  //@col
                                    auto [lo, hi] = equal_range(rows.begin(), rows.end(), col);  //@range
                                    total += hi - lo;  //@range
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int gN;  //@bound

                        static int cmpSeq(const int* a, const int* b) {  //@bound
                            for (int k = 0; k < gN; k++) if (a[k] != b[k]) return a[k] < b[k] ? -1 : 1;  //@bound
                            return 0;  //@bound
                        }  //@bound

                        static int cmpRow(const void* a, const void* b) {  //@bound
                            return cmpSeq(*(int* const*) a, *(int* const*) b);  //@bound
                        }  //@bound

                        // First row > col (upper) or >= col (lower).
                        static int bound(int** rows, int n, const int* col, bool upper) {  //@bound
                            int lo = 0, hi = n;  //@bound
                            while (lo < hi) {  //@bound
                                int mid = (lo + hi) / 2;  //@bound
                                int c = cmpSeq(rows[mid], col);  //@bound
                                if (c < 0 || (upper && c == 0)) lo = mid + 1; else hi = mid;  //@bound
                            }  //@bound
                            return lo;  //@bound
                        }  //@bound

                        int countMatchingPairs(int** grid, int gridSize, int* gridColSize) {
                            int n = gridSize;
                            gN = n;  //@sort
                            int** rows = malloc(n * sizeof(int*));  //@sort
                            memcpy(rows, grid, n * sizeof(int*));  //@sort
                            qsort(rows, n, sizeof(int*), cmpRow);  //@sort
                            int total = 0;
                            int* col = malloc(n * sizeof(int));  //@col
                            for (int c = 0; c < n; c++) {  //@col
                                for (int k = 0; k < n; k++) col[k] = grid[k][c];  //@col
                                total += bound(rows, n, col, true) - bound(rows, n, col, false);  //@range
                            }
                            free(rows);  //@ret
                            free(col);  //@ret
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("bound", "Lexicographic comparison of two length-n sequences, and a binary search for the first row that is ≥ (lower bound) or > (upper bound) a given column. The rows equal to the column lie between the two bounds.",
                     {"java": "`Arrays.compare` compares two int arrays lexicographically.", "c": "The comparison needs n, which `qsort` can't pass, so it's kept in `gN`. Sorting an array of row *pointers* moves no data."}),
                    ("sort", "Sort a copy of the rows lexicographically; identical rows become adjacent.",
                     {"python": "Tuples compare lexicographically, so `sorted` does exactly this.", "cpp": "`vector<int>` already compares lexicographically."}),
                    ("col", "Read column `c` top to bottom into a list.", {"python": "`zip(*grid)` yields the columns as tuples."}),
                    ("range", "Rows equal to the column form one block in the sorted order; its length is the number of matching rows.",
                     {"python": "`bisect_right − bisect_left` is the size of the block of equal tuples.", "cpp": "`equal_range` returns both ends of the block of equal rows."}),
                    ("ret", "Total matching pairs.", {"c": "Free the pointer array and the column buffer."}),
                ],
                complexity=["**Time O(n² log n):** sorting n rows takes O(n log n) comparisons of length n; each column does two binary searches of O(log n) comparisons of length n. **Space O(n²)** for the copy (O(n) in C, which copies pointers)."],
                limits=["The log factor comes from comparisons. Hashing a row lets a column jump straight to its equal rows."],
            ),
            approach(
                "Count rows in a hash map",
                "best",
                "O(n²)",
                "O(n²)",
                idea=[
                    """
                    Count how many times each whole row occurs, using the row itself as the hash-map key. Then for every
                    column, add the count of rows equal to it (0 if none). Each row and column is hashed once in O(n),
                    and there are 2n of them: O(n²) overall, the size of the input.
                    """
                ],
                walk=w3,
                build=["Build a map from row (as a whole sequence) to how many times it occurs.", "For each column, build it as a sequence and add `map[column]` to the total."],
                code={
                    "python": """
                        from collections import Counter

                        class Solution:
                            def countMatchingPairs(self, grid: List[List[int]]) -> int:
                                rows = Counter(tuple(r) for r in grid)  #@count
                                return sum(rows[col] for col in zip(*grid))  #@look
                    """,
                    "java": """
                        class Solution {
                            public int countMatchingPairs(int[][] grid) {
                                int n = grid.length;
                                Map<List<Integer>, Integer> rows = new HashMap<>();  //@count
                                for (int[] r : grid) {  //@count
                                    List<Integer> key = new ArrayList<>(n);  //@count
                                    for (int v : r) key.add(v);  //@count
                                    rows.merge(key, 1, Integer::sum);  //@count
                                }
                                int total = 0;
                                for (int c = 0; c < n; c++) {  //@look
                                    List<Integer> col = new ArrayList<>(n);  //@look
                                    for (int k = 0; k < n; k++) col.add(grid[k][c]);  //@look
                                    total += rows.getOrDefault(col, 0);  //@look
                                }
                                return total;  //@look
                            }
                        }
                    """,
                    "cpp": """
                        struct SeqHash {  //@hash
                            size_t operator()(const vector<int>& v) const {  //@hash
                                size_t h = v.size();  //@hash
                                for (int x : v) h ^= x + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2);  //@hash
                                return h;  //@hash
                            }  //@hash
                        };  //@hash

                        class Solution {
                        public:
                            int countMatchingPairs(vector<vector<int>>& grid) {
                                int n = grid.size();
                                unordered_map<vector<int>, int, SeqHash> rows;  //@count
                                for (auto& r : grid) rows[r]++;  //@count
                                int total = 0;
                                vector<int> col(n);  //@look
                                for (int c = 0; c < n; c++) {  //@look
                                    for (int k = 0; k < n; k++) col[k] = grid[k][c];  //@look
                                    auto it = rows.find(col);  //@look
                                    if (it != rows.end()) total += it->second;  //@look
                                }
                                return total;  //@look
                            }
                        };
                    """,
                    "c": """
                        static unsigned long long hashSeq(int** g, int n, int fixed, bool isRow) {  //@hash
                            unsigned long long h = 1469598103934665603ULL;  //@hash
                            for (int k = 0; k < n; k++) {  //@hash
                                int v = isRow ? g[fixed][k] : g[k][fixed];  //@hash
                                h = (h ^ (unsigned) v) * 1099511628211ULL;  //@hash
                            }  //@hash
                            return h;  //@hash
                        }  //@hash

                        int countMatchingPairs(int** grid, int gridSize, int* gridColSize) {
                            int n = gridSize;
                            unsigned cap = 1;  //@count
                            while (cap < 2u * n) cap <<= 1;  //@count
                            int* rep = malloc(cap * sizeof(int));  //@count
                            int* count = calloc(cap, sizeof(int));  //@count
                            unsigned long long* hs = malloc(cap * sizeof(unsigned long long));  //@count
                            for (unsigned s = 0; s < cap; s++) rep[s] = -1;  //@count
                            for (int r = 0; r < n; r++) {  //@count
                                unsigned long long h = hashSeq(grid, n, r, true);  //@count
                                unsigned s = (unsigned) (h >> 32) & (cap - 1);  //@count
                                while (rep[s] != -1 && !(hs[s] == h && memcmp(grid[rep[s]], grid[r], n * sizeof(int)) == 0)) s = (s + 1) & (cap - 1);  //@count
                                if (rep[s] == -1) { rep[s] = r; hs[s] = h; }  //@count
                                count[s]++;  //@count
                            }
                            int total = 0;
                            for (int c = 0; c < n; c++) {  //@look
                                unsigned long long h = hashSeq(grid, n, c, false);  //@look
                                for (unsigned s = (unsigned) (h >> 32) & (cap - 1); rep[s] != -1; s = (s + 1) & (cap - 1)) {  //@look
                                    if (hs[s] != h) continue;  //@look
                                    int k = 0;  //@look
                                    while (k < n && grid[rep[s]][k] == grid[k][c]) k++;  //@look
                                    if (k == n) { total += count[s]; break; }  //@look
                                }
                            }
                            free(rep);  //@look
                            free(count);  //@look
                            free(hs);  //@look
                            return total;  //@look
                        }
                    """,
                },
                lines=[
                    ("hash", "A hash for a whole sequence of numbers.",
                     {"cpp": "The standard library can't hash a `vector<int>`, so `SeqHash` mixes the values one by one (the same mixing `boost::hash_combine` uses).",
                      "c": "FNV-1a over the n values, read along a row (`g[fixed][k]`) or down a column (`g[k][fixed]`), so a column never has to be copied."}),
                    ("count", "Count each distinct row once. Identical rows share one entry with a count.",
                     {"python": "Lists can't be keys, tuples can.",
                      "java": "`List<Integer>` has value-based `equals` and `hashCode`, so two lists with the same values are the same key.",
                      "c": "The table stores a representative row index, its count and its hash. A probe only counts as equal when the hashes match **and** a full `memcmp` agrees, so collisions can never merge different rows."}),
                    ("look", "For each column, add how many rows equal it. Every matching row is a separate pair, which is why the map stores counts.",
                     {"python": "`zip(*grid)` gives the columns as tuples; a `Counter` returns 0 for missing keys.",
                      "c": "Hash the column in place, probe, and confirm a candidate by comparing the representative row with the column value by value. Free everything at the end."}),
                ],
                complexity=["**Time O(n²)** on average: 2n sequences, each hashed and compared in O(n). **Space O(n²)** for the keys (O(n) in C, which stores row indices)."],
            ),
        ],
        takeaways=[
            """
            - A **whole sequence can be a hash key**. Turning "compare these two lists" into "look this list up"
              removes a factor of n.
            - Count occurrences when duplicates each form their own pair.
            - In languages without sequence hashing, combine a hash with a full equality check; never trust the
              hash alone.
            - Sorting sequences lexicographically is the comparison-based alternative, at an extra log factor.
            """
        ],
    )


@problem
def same_shape_words():
    words, pattern = ["feet", "moon", "moan", "deed", "abba", "keep"], "boot"

    def shape(w):
        first = {}
        return [first.setdefault(c, len(first)) for c in w]

    target = shape(pattern)
    want = sum(shape(w) == target for w in words)
    assert want == 3

    w1 = Steps("For every pair of positions, letters must be equal in the word exactly when they're equal in the pattern.")
    w1.step(f"Pattern '{pattern}': positions 1 and 2 are equal, every other pair differs.", Row(list(pattern), slots=True, label="pattern"))
    for w in ["moon", "moan", "deed"]:
        bad = next(((i, j) for i in range(len(w)) for j in range(i + 1, len(w)) if (w[i] == w[j]) != (pattern[i] == pattern[j])), None)
        if bad:
            i, j = bad
            w1.step(f"'{w}': positions {i} and {j} are {'equal' if w[i] == w[j] else 'different'} in the word but {'equal' if pattern[i] == pattern[j] else 'different'} in the pattern. Not the same shape.",
                    Row(list(w), st={i: "mark", j: "mark"}, slots=True, label=w), Row(list(pattern), st={i: "mark", j: "mark"}, slots=True, label="pattern"))
        else:
            w1.step(f"'{w}': all 6 position pairs agree with the pattern. Same shape.", Row(list(w), st={q: "found" for q in range(len(w))}, slots=True, label=w), Row(list(pattern), slots=True, label="pattern"))
    w1.step(f"Checking all six words this way: {want} match (feet, moon, keep).", Row(words, st={i: "answer" for i, x in enumerate(words) if shape(x) == target}), result=want)

    w2 = Steps("Build the letter mapping word → pattern and pattern → word as you go; any conflict means a different shape.")
    for w in ["moon", "moan", "deed"]:
        fwd, back = {}, {}
        ok = True
        for i, (x, y) in enumerate(zip(w, pattern)):
            if fwd.setdefault(x, y) != y:
                w2.step(f"'{w}' position {i}: '{x}' was already mapped to '{fwd[x]}', now it would need '{y}'. Conflict.", Row(list(w), st={i: "mark"}, slots=True, label=w), Row([f"{a}→{b}" for a, b in fwd.items()], label="word → pattern"), Row([f"{b}→{a}" for b, a in back.items()], label="pattern → word"))
                ok = False
                break
            if back.setdefault(y, x) != x:
                w2.step(f"'{w}' position {i}: pattern letter '{y}' already stands for '{back[y]}', now it would be '{x}'. Conflict.", Row(list(w), st={i: "mark"}, slots=True, label=w), Row([f"{a}→{b}" for a, b in fwd.items()], label="word → pattern"), Row([f"{b}→{a}" for b, a in back.items()], label="pattern → word"))
                ok = False
                break
        if ok:
            w2.step(f"'{w}': mappings {', '.join(f'{a}→{b}' for a, b in fwd.items())} stay consistent both ways. Same shape.", Row(list(w), st={q: "found" for q in range(len(w))}, slots=True, label=w), Row([f"{a}→{b}" for a, b in fwd.items()], label="word → pattern"), Row([f"{b}→{a}" for b, a in back.items()], label="pattern → word"))
    w2.step(f"Count of words passing the check: {want}.", Row(words, st={i: "answer" for i, x in enumerate(words) if shape(x) == target}), result=want)

    w3 = Steps("Replace each letter by the order in which it first appeared. Words with the same shape get the same numbers.")
    w3.step(f"Pattern '{pattern}' → {target}: b is the 0th new letter, o the 1st, t the 2nd.", Row(list(pattern), label="pattern"), Row(target, label="shape"))
    for i, w in enumerate(words):
        s = shape(w)
        w3.step(f"'{w}' → {s}" + (": equal, count it." if s == target else ": different."), Row(list(w), label=w), Row(s, st={q: ("answer" if s == target else "mark") for q in range(len(s))}, label="shape"), Row(target, label="pattern shape"))
    w3.step(f"{want} words share the pattern's shape.", Row(words, st={i: "answer" for i, x in enumerate(words) if shape(x) == target}), result=want)

    sol(
        "same-shape-words",
        summary="""
            Describe a word by its **shape**: replace each letter by the order in which that letter first appeared
            (`"boot"` → 0, 1, 1, 2). Two words have the same shape exactly when these sequences are equal. Compute
            the pattern's shape once and compare every word's shape to it, O(total letters).
        """,
        question=[
            """
            Count the words that can be turned into `pattern` by a **consistent, one-to-one** letter replacement.

            - **Consistent:** a letter always becomes the same letter. In `"moon"` → `"feet"`, both o's become e.
            - **One-to-one:** different letters must become different letters. `"moan"` can't become `"feet"`
              (o and a would both have to become e), and `"cc"` can't become `"xy"` (one c can't become two
              letters).
            - **Lengths must match.** Different lengths can never have the same shape.
            - **Single letters all match:** any one-letter word has the shape of any other.
            - **Size:** up to 10⁴ words, each at most 20 letters.
            """
        ],
        think=[
            """
            Take pattern `"boot"` and the words feet, moon, moan, deed, abba, keep.

            Ignore what the letters *are* and look at where they **repeat**. In `boot` the middle two letters are
            the same and everything else is different. Write that down by numbering letters in order of first
            appearance: b is new (0), o is new (1), o again (1), t is new (2): **0 1 1 2**.
            """,
            fig(Row(["boot", "feet", "moon", "keep", "moan", "deed", "abba"], label="word"), Row(["0112", "0112", "0112", "0112", "0123", "0110", "0110"], st={0: "answer", 1: "answer", 2: "answer", 3: "answer"}, label="shape"),
                caption="feet, moon and keep have the pattern's shape 0 1 1 2."),
            """
            This numbering captures exactly the two rules: a repeated letter repeats its number (consistent), and
            a new letter always gets a new number (one-to-one). So "same shape" becomes "same number sequence",
            a plain equality check, and the sequence works as a **group key** too.
            """,
        ],
        approaches=[
            approach(
                "Check every pair of positions",
                "brute",
                "O(N · L²)",
                "O(1)",
                idea=["Two strings of equal length have the same shape exactly when, for every pair of positions `i < j`, the word's letters are equal if and only if the pattern's letters are equal. Check all pairs."],
                walk=w1,
                build=["For each word of the right length, loop over all position pairs `i < j`.", "If `(w[i] == w[j]) != (p[i] == p[j])`, the shapes differ.", "Count the words with no disagreement."],
                code={
                    "python": """
                        class Solution:
                            def countSameShape(self, words: List[str], pattern: str) -> int:
                                L = len(pattern)
                                total = 0
                                for w in words:  #@each
                                    if len(w) != L:  #@len
                                        continue  #@len
                                    if all((w[i] == w[j]) == (pattern[i] == pattern[j])  #@pairs
                                           for i in range(L) for j in range(i + 1, L)):  #@pairs
                                        total += 1  #@pairs
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countSameShape(String[] words, String pattern) {
                                int L = pattern.length(), total = 0;
                                for (String w : words) {  //@each
                                    if (w.length() != L) continue;  //@len
                                    boolean ok = true;  //@pairs
                                    for (int i = 0; i < L && ok; i++)  //@pairs
                                        for (int j = i + 1; j < L && ok; j++)  //@pairs
                                            ok = (w.charAt(i) == w.charAt(j)) == (pattern.charAt(i) == pattern.charAt(j));  //@pairs
                                    if (ok) total++;  //@pairs
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countSameShape(vector<string>& words, string& pattern) {
                                int L = pattern.size(), total = 0;
                                for (const string& w : words) {  //@each
                                    if ((int) w.size() != L) continue;  //@len
                                    bool ok = true;  //@pairs
                                    for (int i = 0; i < L && ok; i++)  //@pairs
                                        for (int j = i + 1; j < L && ok; j++)  //@pairs
                                            ok = (w[i] == w[j]) == (pattern[i] == pattern[j]);  //@pairs
                                    if (ok) total++;  //@pairs
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countSameShape(char** words, int wordsSize, char* pattern) {
                            int L = strlen(pattern), total = 0;
                            for (int k = 0; k < wordsSize; k++) {  //@each
                                char* w = words[k];  //@each
                                if ((int) strlen(w) != L) continue;  //@len
                                bool ok = true;  //@pairs
                                for (int i = 0; i < L && ok; i++)  //@pairs
                                    for (int j = i + 1; j < L && ok; j++)  //@pairs
                                        ok = (w[i] == w[j]) == (pattern[i] == pattern[j]);  //@pairs
                                if (ok) total++;  //@pairs
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("each", "Check each word against the pattern."),
                    ("len", "A different length can't have the same shape."),
                    ("pairs", "Equal letters in the word must sit exactly where the pattern has equal letters, for every pair of positions. That single rule covers both \"consistent\" and \"one-to-one\"."),
                    ("ret", "The number of matching words."),
                ],
                complexity=["**Time O(N · L²)** for N words of length L: L(L − 1)/2 pairs per word. **Space O(1).**"],
                limits=["Each pair is compared from scratch. Remembering what each letter maps to as you scan replaces the pairs with a single pass."],
            ),
            approach(
                "Two-way letter mapping",
                "better",
                "O(N · L)",
                "O(1)",
                idea=[
                    """
                    Scan the word and pattern together, building two maps: word letter → pattern letter, and pattern
                    letter → word letter. A word letter that's already mapped to something else breaks consistency; a
                    pattern letter that already stands for a different word letter breaks one-to-one. If neither
                    happens, the shapes match. With 26 letters, both maps are arrays of 26.
                    """
                ],
                walk=w2,
                build=["Skip words of a different length.", "Keep `fwd[26]` and `back[26]`, both empty.", "At each position with letters x (word) and y (pattern): if `fwd[x]` is set and isn't y, or `back[y]` is set and isn't x, fail. Otherwise set both.", "Count the words that never fail."],
                code={
                    "python": """
                        class Solution:
                            def countSameShape(self, words: List[str], pattern: str) -> int:
                                total = 0
                                for w in words:  #@each
                                    if len(w) != len(pattern):  #@each
                                        continue  #@each
                                    fwd, back = {}, {}  #@maps
                                    ok = True  #@maps
                                    for x, y in zip(w, pattern):  #@scan
                                        if fwd.setdefault(x, y) != y or back.setdefault(y, x) != x:  #@check
                                            ok = False  #@check
                                            break  #@check
                                    total += ok  #@ret
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countSameShape(String[] words, String pattern) {
                                int total = 0;
                                for (String w : words) {  //@each
                                    if (w.length() != pattern.length()) continue;  //@each
                                    char[] fwd = new char[26], back = new char[26];  //@maps
                                    boolean ok = true;  //@maps
                                    for (int i = 0; i < w.length() && ok; i++) {  //@scan
                                        char x = w.charAt(i), y = pattern.charAt(i);  //@scan
                                        if (fwd[x - 'a'] == 0 && back[y - 'a'] == 0) {  //@set
                                            fwd[x - 'a'] = y;  //@set
                                            back[y - 'a'] = x;  //@set
                                        } else if (fwd[x - 'a'] != y || back[y - 'a'] != x) {  //@check
                                            ok = false;  //@check
                                        }
                                    }
                                    if (ok) total++;  //@ret
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countSameShape(vector<string>& words, string& pattern) {
                                int total = 0;
                                for (const string& w : words) {  //@each
                                    if (w.size() != pattern.size()) continue;  //@each
                                    char fwd[26] = {0}, back[26] = {0};  //@maps
                                    bool ok = true;  //@maps
                                    for (size_t i = 0; i < w.size() && ok; i++) {  //@scan
                                        char x = w[i], y = pattern[i];  //@scan
                                        if (fwd[x - 'a'] == 0 && back[y - 'a'] == 0) {  //@set
                                            fwd[x - 'a'] = y;  //@set
                                            back[y - 'a'] = x;  //@set
                                        } else if (fwd[x - 'a'] != y || back[y - 'a'] != x) {  //@check
                                            ok = false;  //@check
                                        }
                                    }
                                    if (ok) total++;  //@ret
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countSameShape(char** words, int wordsSize, char* pattern) {
                            int L = strlen(pattern), total = 0;
                            for (int k = 0; k < wordsSize; k++) {  //@each
                                char* w = words[k];  //@each
                                if ((int) strlen(w) != L) continue;  //@each
                                char fwd[26] = {0}, back[26] = {0};  //@maps
                                bool ok = true;  //@maps
                                for (int i = 0; i < L && ok; i++) {  //@scan
                                    char x = w[i], y = pattern[i];  //@scan
                                    if (fwd[x - 'a'] == 0 && back[y - 'a'] == 0) {  //@set
                                        fwd[x - 'a'] = y;  //@set
                                        back[y - 'a'] = x;  //@set
                                    } else if (fwd[x - 'a'] != y || back[y - 'a'] != x) {  //@check
                                        ok = false;  //@check
                                    }
                                }
                                if (ok) total++;  //@ret
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("each", "Only words of the pattern's length can match."),
                    ("maps", "`fwd` maps word letters to pattern letters; `back` maps the other way. Both start empty (0 means unmapped).", {"python": "Plain dictionaries; with 26 letters an array would work too."}),
                    ("scan", "Walk the word and the pattern side by side."),
                    ("set", "Neither letter has a partner yet: pair them up in both directions."),
                    ("check", "Otherwise both must already be paired **with each other**. A mismatch in `fwd` breaks consistency (one word letter would need two different pattern letters). A mismatch in `back` breaks one-to-one: in `\"moan\"` against `\"boot\"`, o and a would both have to become o, and only the reverse map notices.",
                     {"python": "`setdefault` returns the existing value or stores the new one, so one comparison per direction does both the check and the insert."}),
                    ("ret", "Count words with a consistent two-way mapping."),
                ],
                complexity=["**Time O(N · L):** one pass per word. **Space O(1):** two 26-letter maps."],
                limits=["Correct and linear, but it needs two maps, and forgetting the reverse map is the classic bug. It also only answers \"does this word match that pattern?\"; it doesn't give each word a key you could group or hash by."],
            ),
            approach(
                "Compare canonical shapes",
                "best",
                "O(N · L)",
                "O(L)",
                idea=[
                    """
                    Map each string to its shape: walk it and replace each letter by the order of its first appearance
                    (0 for the first new letter, 1 for the second, …). Compute the pattern's shape once, then count the
                    words whose shape is equal. One map per string, no reverse map needed: two different letters can
                    never receive the same number, so one-to-one is built in.
                    """
                ],
                walk=w3,
                build=["Write `shape(s)`: a 26-slot table of first-appearance numbers, filled as letters are first seen.", "Compute `target = shape(pattern)`.", "Count the words with `shape(word) == target` (different lengths give different shapes)."],
                code={
                    "python": """
                        class Solution:
                            def countSameShape(self, words: List[str], pattern: str) -> int:
                                def shape(s):  #@shape
                                    first = {}  #@shape
                                    return [first.setdefault(ch, len(first)) for ch in s]  #@shape
                                target = shape(pattern)  #@target
                                return sum(shape(w) == target for w in words)  #@count
                    """,
                    "java": """
                        class Solution {
                            public int countSameShape(String[] words, String pattern) {
                                int[] target = shape(pattern);  //@target
                                int total = 0;
                                for (String w : words) if (Arrays.equals(shape(w), target)) total++;  //@count
                                return total;  //@count
                            }

                            private int[] shape(String s) {  //@shape
                                int[] first = new int[26];  //@shape
                                Arrays.fill(first, -1);  //@shape
                                int[] out = new int[s.length()];  //@shape
                                int next = 0;  //@shape
                                for (int i = 0; i < s.length(); i++) {  //@shape
                                    int c = s.charAt(i) - 'a';  //@shape
                                    if (first[c] < 0) first[c] = next++;  //@shape
                                    out[i] = first[c];  //@shape
                                }  //@shape
                                return out;  //@shape
                            }  //@shape
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countSameShape(vector<string>& words, string& pattern) {
                                auto shape = [](const string& s) {  //@shape
                                    int first[26];  //@shape
                                    fill(first, first + 26, -1);  //@shape
                                    vector<int> out;  //@shape
                                    int next = 0;  //@shape
                                    for (char ch : s) {  //@shape
                                        if (first[ch - 'a'] < 0) first[ch - 'a'] = next++;  //@shape
                                        out.push_back(first[ch - 'a']);  //@shape
                                    }  //@shape
                                    return out;  //@shape
                                };  //@shape
                                vector<int> target = shape(pattern);  //@target
                                int total = 0;
                                for (const string& w : words) if (shape(w) == target) total++;  //@count
                                return total;  //@count
                            }
                        };
                    """,
                    "c": """
                        // Writes the shape of s into out and returns its length.
                        static int shape(const char* s, int* out) {  //@shape
                            int first[26], next = 0, n = 0;  //@shape
                            for (int i = 0; i < 26; i++) first[i] = -1;  //@shape
                            for (; s[n]; n++) {  //@shape
                                int c = s[n] - 'a';  //@shape
                                if (first[c] < 0) first[c] = next++;  //@shape
                                out[n] = first[c];  //@shape
                            }  //@shape
                            return n;  //@shape
                        }  //@shape

                        int countSameShape(char** words, int wordsSize, char* pattern) {
                            int target[21], mine[21];  //@target
                            int L = shape(pattern, target);  //@target
                            int total = 0;
                            for (int k = 0; k < wordsSize; k++) {  //@count
                                int len = shape(words[k], mine);  //@count
                                if (len == L && memcmp(mine, target, L * sizeof(int)) == 0) total++;  //@count
                            }
                            return total;  //@count
                        }
                    """,
                },
                lines=[
                    ("shape", "The canonical shape: each letter is replaced by the order of its first appearance. A letter seen before reuses its number; a new letter takes the next number.",
                     {"python": "`first.setdefault(ch, len(first))` returns the letter's existing number, or gives it the next one (the current size of the map).",
                      "c": "Words are at most 20 letters, so a fixed buffer of 21 ints holds any shape."}),
                    ("target", "The pattern's shape, computed once."),
                    ("count", "A word matches exactly when its shape equals the pattern's. Different lengths give different-length shapes, so they never compare equal.",
                     {"c": "Compare lengths first, then the numbers with `memcmp`."}),
                ],
                complexity=["**Time O(N · L):** each string's shape takes one pass. **Space O(L)** for the shape being compared."],
            ),
        ],
        takeaways=[
            """
            - "Equal up to renaming" problems (isomorphic strings, word patterns) become simple equality once you
              map each item to a **canonical form**: number things in order of first appearance.
            - A canonical form is also a **group key**: you could count how many words share each shape with a
              hash map.
            - If you check a mapping directly instead, check **both directions**; one map alone lets two letters
              collapse into one.
            """
        ],
    )


@problem
def shift_families():
    words = ["abc", "bcd", "xyz", "az", "ba", "a", "z", "acd"]

    def norm(w):
        return "".join(chr((ord(c) - ord(w[0])) % 26 + 97) for c in w)

    fams = len({norm(w) for w in words})
    assert fams == 4

    def shift(w, k):
        return "".join(chr((ord(c) - 97 + k) % 26 + 97) for c in w)

    w1 = Steps("Keep one representative per family. A word joins a family if some shift of the representative equals it.")
    reps = []
    for i, w in enumerate(words):
        hit = next((r for r in reps if len(r) == len(w) and any(shift(r, k) == w for k in range(26))), None)
        if hit:
            k = next(k for k in range(26) if shift(hit, k) == w)
            w1.step(f"'{w}': shifting representative '{hit}' by {k} gives '{w}'. Same family.", Row(words, st={**{q: "dim" for q in range(i)}, i: "active"}), Row(reps, st={reps.index(hit): "answer"}, label="representatives"))
        else:
            reps.append(w)
            w1.step(f"'{w}': no representative of length {len(w)} shifts into it (each tried with all 26 shifts). New family.", Row(words, st={**{q: "dim" for q in range(i)}, i: "active"}), Row(reps, st={len(reps) - 1: "new"}, label="representatives"))
    w1.step(f"{len(reps)} families.", Row(reps, label="representatives"), result=len(reps))

    w2 = Steps("Shift every word so it starts with 'a'. Family members become identical; sort and count distinct.")
    normed = [norm(w) for w in words]
    w2.step("Shift each word back by its first letter's distance from 'a'.", Row(words, label="word"), Row(normed, label="starts at a"))
    s = sorted(normed)
    w2.step(f"Sorted: equal normal forms are neighbours.", Row(s, st={i: ("answer" if i == 0 or s[i] != s[i - 1] else "dim") for i in range(len(s))}, label="sorted"))
    w2.step(f"Count the positions where a new value starts: {fams}.", Row(s, st={i: "answer" for i in range(len(s)) if i == 0 or s[i] != s[i - 1]}, label="sorted"), result=fams)

    w3 = Steps("Shift every word so it starts with 'a' and put the result in a hash set. The set's size is the answer.")
    seen = []
    for i, w in enumerate(words):
        nw = norm(w)
        new = nw not in seen
        if new:
            seen.append(nw)
        w3.step(f"'{w}' → '{nw}'" + (": new, add it." if new else ": already in the set."), Row(words, st={**{q: "dim" for q in range(i)}, i: "active"}), Row(seen, st={seen.index(nw): "new" if new else "found"}, label="set"))
    w3.step(f"The set holds {len(seen)} normal forms: {len(seen)} families.", Row(seen, label="set"), result=len(seen))

    sol(
        "shift-families",
        summary="""
            A shift changes every letter by the same amount, so it doesn't change the **gaps** between letters.
            Normalise each word by shifting it until it starts with `a`; two words are in the same family exactly
            when their normal forms are equal. Count distinct normal forms with a hash set: O(total letters).
        """,
        question=[
            """
            Shifting moves every letter of a word forward by the same number of places, wrapping `z` → `a`. Words
            that can be shifted into one another form a **family**. Count the families.

            - **Wrap-around counts:** `"az"` shifted by 1 is `"ba"`, so they're one family.
            - **Lengths must match:** a shift never changes length, so `"a"` and `"aa"` are different families.
            - **Identical words** are one family (a shift by 0).
            - **Every one-letter word** is in a single family: any letter shifts into any other.
            - **Size:** up to 10⁴ words of at most 50 letters.
            """
        ],
        think=[
            """
            Take `["abc", "bcd", "xyz", "az", "ba", "a", "z", "acd"]`.

            What doesn't change when you shift? The **distance from each letter to the next**: abc goes +1, +1;
            so do bcd and xyz. az goes +25 (a to z), and ba goes from b to a, which is also +25 with wrap-around.
            So family = same length and same sequence of gaps.

            An equivalent, easier-to-code fingerprint: **shift every word so its first letter becomes `a`**. Every
            member of a family lands on the same word.
            """,
            fig(Row(words, label="word"), Row([norm(w) for w in words], label="shifted to start at a"),
                caption="abc, bcd, xyz → abc;  az, ba → az;  a, z → a;  acd → acd. Four families."),
            """
            The normal form is a **key**: same key, same family. Counting families becomes counting distinct
            keys.
            """,
        ],
        approaches=[
            approach(
                "Try all 26 shifts against each family's representative",
                "brute",
                "O(n · f · 26 · L)",
                "O(n · L)",
                idea=["Keep one representative word per family found so far. For a new word, try every representative of the same length with all 26 shifts; if one equals the word, it joins that family. Otherwise it's a new family."],
                walk=w1,
                build=["Keep a list of representatives.", "For each word, for each representative of the same length, for each shift k in 0 … 25: compare the shifted representative with the word.", "No match anywhere: add the word as a new representative.", "Return the number of representatives."],
                code={
                    "python": """
                        class Solution:
                            def countShiftFamilies(self, words: List[str]) -> int:
                                def shifted_equal(r, w, k):  #@shift
                                    return all((ord(a) - 97 + k) % 26 == ord(b) - 97 for a, b in zip(r, w))  #@shift
                                reps = []  #@reps
                                for w in words:  #@each
                                    if not any(len(r) == len(w) and any(shifted_equal(r, w, k) for k in range(26))  #@try
                                               for r in reps):  #@try
                                        reps.append(w)  #@new
                                return len(reps)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countShiftFamilies(String[] words) {
                                List<String> reps = new ArrayList<>();  //@reps
                                for (String w : words) {  //@each
                                    boolean found = false;  //@try
                                    for (String r : reps) {  //@try
                                        if (r.length() != w.length()) continue;  //@try
                                        for (int k = 0; k < 26 && !found; k++) found = shiftedEqual(r, w, k);  //@try
                                        if (found) break;  //@try
                                    }
                                    if (!found) reps.add(w);  //@new
                                }
                                return reps.size();  //@ret
                            }

                            private boolean shiftedEqual(String r, String w, int k) {  //@shift
                                for (int i = 0; i < r.length(); i++)  //@shift
                                    if ((r.charAt(i) - 'a' + k) % 26 != w.charAt(i) - 'a') return false;  //@shift
                                return true;  //@shift
                            }  //@shift
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countShiftFamilies(vector<string>& words) {
                                auto shiftedEqual = [](const string& r, const string& w, int k) {  //@shift
                                    for (size_t i = 0; i < r.size(); i++)  //@shift
                                        if ((r[i] - 'a' + k) % 26 != w[i] - 'a') return false;  //@shift
                                    return true;  //@shift
                                };  //@shift
                                vector<string> reps;  //@reps
                                for (const string& w : words) {  //@each
                                    bool found = false;  //@try
                                    for (const string& r : reps) {  //@try
                                        if (r.size() != w.size()) continue;  //@try
                                        for (int k = 0; k < 26 && !found; k++) found = shiftedEqual(r, w, k);  //@try
                                        if (found) break;  //@try
                                    }
                                    if (!found) reps.push_back(w);  //@new
                                }
                                return reps.size();  //@ret
                            }
                        };
                    """,
                    "c": """
                        static bool shiftedEqual(const char* r, const char* w, int k) {  //@shift
                            for (int i = 0; r[i]; i++)  //@shift
                                if ((r[i] - 'a' + k) % 26 != w[i] - 'a') return false;  //@shift
                            return true;  //@shift
                        }  //@shift

                        int countShiftFamilies(char** words, int wordsSize) {
                            char** reps = malloc(wordsSize * sizeof(char*));  //@reps
                            int f = 0;  //@reps
                            for (int i = 0; i < wordsSize; i++) {  //@each
                                bool found = false;  //@try
                                for (int j = 0; j < f && !found; j++) {  //@try
                                    if (strlen(reps[j]) != strlen(words[i])) continue;  //@try
                                    for (int k = 0; k < 26 && !found; k++) found = shiftedEqual(reps[j], words[i], k);  //@try
                                }
                                if (!found) reps[f++] = words[i];  //@new
                            }
                            free(reps);  //@ret
                            return f;  //@ret
                        }
                    """,
                },
                lines=[
                    ("shift", "Does shifting `r` by `k` places produce `w`? Letter by letter, `(r − 'a' + k) mod 26` must equal `w − 'a'` (the `mod 26` is the wrap-around). Assumes equal lengths."),
                    ("reps", "One representative word per family found so far."),
                    ("each", "Place each word into a family."),
                    ("try", "Only same-length representatives can match; try all 26 shifts of each."),
                    ("new", "Nothing matched: the word founds a new family."),
                    ("ret", "One representative per family.", {"c": "Free the list (it only holds pointers to the input words)."}),
                ],
                complexity=["**Time O(n · f · 26 · L)** for f families: up to 10⁴ × 10⁴ × 26 × 50 in the worst case. **Space O(n · L)** in the worst case (representatives)."],
                limits=["Membership in a family is tested by trying shifts against every family. A fingerprint that's identical for the whole family would make membership an equality test, and equal fingerprints can be sorted or hashed."],
                slow=True,
            ),
            approach(
                "Normalise, sort, count distinct",
                "better",
                "O(n · L · log n)",
                "O(n · L)",
                idea=["Shift every word back so its first letter is `a`: letter `c` becomes `(c − first) mod 26`. Family members all become the same string. Sort the normal forms and count how many differ from their predecessor."],
                walk=w2,
                build=["For each word, build its normal form with `(c − w[0] + 26) % 26 + 'a'`.", "Sort the normal forms.", "Count positions where the value differs from the one before (plus the first)."],
                code={
                    "python": """
                        class Solution:
                            def countShiftFamilies(self, words: List[str]) -> int:
                                def normal(w):  #@norm
                                    return "".join(chr((ord(c) - ord(w[0])) % 26 + 97) for c in w)  #@norm
                                keys = sorted(normal(w) for w in words)  #@sort
                                return sum(1 for i in range(len(keys)) if i == 0 or keys[i] != keys[i - 1])  #@count
                    """,
                    "java": """
                        class Solution {
                            public int countShiftFamilies(String[] words) {
                                String[] keys = new String[words.length];  //@sort
                                for (int i = 0; i < words.length; i++) keys[i] = normal(words[i]);  //@sort
                                Arrays.sort(keys);  //@sort
                                int families = 0;  //@count
                                for (int i = 0; i < keys.length; i++) if (i == 0 || !keys[i].equals(keys[i - 1])) families++;  //@count
                                return families;  //@count
                            }

                            private String normal(String w) {  //@norm
                                char[] out = new char[w.length()];  //@norm
                                for (int i = 0; i < out.length; i++) out[i] = (char) ((w.charAt(i) - w.charAt(0) + 26) % 26 + 'a');  //@norm
                                return new String(out);  //@norm
                            }  //@norm
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countShiftFamilies(vector<string>& words) {
                                vector<string> keys;  //@sort
                                for (const string& w : words) {  //@sort
                                    string k = w;  //@norm
                                    for (char& c : k) c = (c - w[0] + 26) % 26 + 'a';  //@norm
                                    keys.push_back(k);  //@sort
                                }  //@sort
                                sort(keys.begin(), keys.end());  //@sort
                                return unique(keys.begin(), keys.end()) - keys.begin();  //@count
                            }
                        };
                    """,
                    "c": """
                        static int cmpStr(const void* a, const void* b) {  //@sort
                            return strcmp(*(char* const*) a, *(char* const*) b);  //@sort
                        }  //@sort

                        int countShiftFamilies(char** words, int wordsSize) {
                            char** keys = malloc(wordsSize * sizeof(char*));  //@sort
                            for (int i = 0; i < wordsSize; i++) {  //@norm
                                size_t len = strlen(words[i]);  //@norm
                                keys[i] = malloc(len + 1);  //@norm
                                for (size_t j = 0; j < len; j++) keys[i][j] = (words[i][j] - words[i][0] + 26) % 26 + 'a';  //@norm
                                keys[i][len] = '\\0';  //@norm
                            }  //@norm
                            qsort(keys, wordsSize, sizeof(char*), cmpStr);  //@sort
                            int families = 0;  //@count
                            for (int i = 0; i < wordsSize; i++) if (i == 0 || strcmp(keys[i], keys[i - 1]) != 0) families++;  //@count
                            for (int i = 0; i < wordsSize; i++) free(keys[i]);  //@count
                            free(keys);  //@count
                            return families;  //@count
                        }
                    """,
                },
                lines=[
                    ("norm", "Shift the word back by its first letter: `(c − first + 26) mod 26` keeps every gap and turns the first letter into `a`. The `+ 26` keeps the value non-negative before `mod` in languages where `%` can return negatives."),
                    ("sort", "Sort the normal forms so equal ones sit together.", {"c": "`qsort` on the array of string pointers with `strcmp`."}),
                    ("count", "Each new value in sorted order starts a new family.", {"cpp": "`unique` squeezes out adjacent duplicates and returns the new end; the distance from the start is the number of distinct keys.", "c": "Count, then free every key."}),
                ],
                complexity=["**Time O(n · L · log n):** normalising is O(n · L); sorting compares strings of length L about n log n times. **Space O(n · L)** for the keys."],
                limits=["The sort is only there to bring equal keys together. A hash set recognises equal keys directly, without ordering anything."],
            ),
            approach(
                "Normalise into a hash set",
                "best",
                "O(n · L)",
                "O(n · L)",
                idea=["Same normal form (shift so the word starts with `a`), but put every normal form into a hash set. Equal forms collapse into one entry, so the set's size is the number of families."],
                walk=w3,
                build=["Create an empty hash set of strings.", "For each word, add its normal form.", "Return the set's size."],
                code={
                    "python": """
                        class Solution:
                            def countShiftFamilies(self, words: List[str]) -> int:
                                seen = set()  #@set
                                for w in words:  #@each
                                    seen.add("".join(chr((ord(c) - ord(w[0])) % 26 + 97) for c in w))  #@norm
                                return len(seen)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countShiftFamilies(String[] words) {
                                Set<String> seen = new HashSet<>();  //@set
                                for (String w : words) {  //@each
                                    char[] key = new char[w.length()];  //@norm
                                    for (int i = 0; i < key.length; i++) key[i] = (char) ((w.charAt(i) - w.charAt(0) + 26) % 26 + 'a');  //@norm
                                    seen.add(new String(key));  //@norm
                                }
                                return seen.size();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countShiftFamilies(vector<string>& words) {
                                unordered_set<string> seen;  //@set
                                for (const string& w : words) {  //@each
                                    string key = w;  //@norm
                                    for (char& c : key) c = (c - w[0] + 26) % 26 + 'a';  //@norm
                                    seen.insert(key);  //@norm
                                }
                                return seen.size();  //@ret
                            }
                        };
                    """,
                    "c": """
                        static unsigned long long fnv(const char* s) {  //@hash
                            unsigned long long h = 1469598103934665603ULL;  //@hash
                            for (; *s; s++) h = (h ^ (unsigned char) *s) * 1099511628211ULL;  //@hash
                            return h;  //@hash
                        }  //@hash

                        int countShiftFamilies(char** words, int wordsSize) {
                            unsigned cap = 1;  //@set
                            while (cap < 2u * wordsSize) cap <<= 1;  //@set
                            char** table = calloc(cap, sizeof(char*));  //@set
                            int families = 0;  //@set
                            for (int i = 0; i < wordsSize; i++) {  //@each
                                size_t len = strlen(words[i]);  //@norm
                                char* key = malloc(len + 1);  //@norm
                                for (size_t j = 0; j < len; j++) key[j] = (words[i][j] - words[i][0] + 26) % 26 + 'a';  //@norm
                                key[len] = '\\0';  //@norm
                                unsigned s = (unsigned) (fnv(key) >> 32) & (cap - 1);  //@add
                                while (table[s] && strcmp(table[s], key) != 0) s = (s + 1) & (cap - 1);  //@add
                                if (table[s]) free(key);  //@add
                                else { table[s] = key; families++; }  //@add
                            }
                            for (unsigned s = 0; s < cap; s++) free(table[s]);  //@ret
                            free(table);  //@ret
                            return families;  //@ret
                        }
                    """,
                },
                lines=[
                    ("hash", "C has no string set; FNV-1a turns a string into a 64-bit hash, byte by byte."),
                    ("set", "A set of normal forms; its size will be the answer.", {"c": "An open-addressing table of string pointers (NULL = empty slot), at least twice as many slots as words. `families` counts the distinct keys added."}),
                    ("each", "One pass over the words."),
                    ("norm", "Shift the word so it starts with `a`. Every member of a family produces the same string.", {"python": "Python's `%` is never negative, so no `+ 26` is needed."}),
                    ("add", "Probe from the key's slot: finding an equal string means the family is already counted (free the duplicate key); reaching an empty slot means a new family."),
                    ("ret", "The number of distinct normal forms is the number of families.", {"c": "Free every stored key and the table."}),
                ],
                complexity=["**Time O(n · L)** on average: one normalising pass and one hash insert (hashing L characters) per word. **Space O(n · L)** for the set."],
            ),
        ],
        takeaways=[
            """
            - For "equivalent under some transformation", find an **invariant** or a **canonical representative**:
              here, the gaps between letters, or the word shifted to start at `a`.
            - Counting equivalence classes = counting distinct canonical keys: a hash set's size.
            - Modular arithmetic handles wrap-around; add the modulus before `%` in languages where `%` can be
              negative.
            """
        ],
    )
