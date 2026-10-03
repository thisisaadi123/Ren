"""Sliding Window: windows that keep a frequency map of their contents."""
from collections import Counter

from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401
from window_patterns.shortest_window import COMPRESS_C


@problem
def best_unique_bundle():
    prices, k = [4, 2, 4, 5, 3, 3, 1, 6, 1], 3
    n = len(prices)
    wins = [(i, prices[i:i + k]) for i in range(n - k + 1)]
    want = max([sum(w) for _, w in wins if len(set(w)) == k] or [0])

    w1 = Steps("Check every window of k items: are the prices all different? If so, compare its total.")
    best = 0
    for i, w in wins:
        ok = len(set(w)) == k
        if ok:
            best = max(best, sum(w))
        w1.step(f"{w}: " + (f"all different, total {sum(w)}." if ok else "has a repeat."), Row(prices, st={x: ("found" if ok else "mark") for x in range(i, i + k)}), Vars(best=best))
    w1.step(f"Best bundle: {want}.", result=want)

    w2 = Steps("Slide the window keeping its total, a count per price, and dup = how many prices appear more than once. A window counts when dup is 0.")
    count, dup, total, best = Counter(), 0, 0, 0
    for i, v in enumerate(prices):
        count[v] += 1
        dup += count[v] == 2
        total += v
        if i >= k:
            u = prices[i - k]
            count[u] -= 1
            dup -= count[u] == 1
            total -= u
        if i >= k - 1:
            if dup == 0:
                best = max(best, total)
            w2.step(f"Window {prices[i - k + 1:i + 1]}: total {total}, dup {dup}.", Row(prices, st={x: ("found" if dup == 0 else "mark") for x in range(i - k + 1, i + 1)}), Vars(total=total, dup=dup, best=best))
    w2.step(f"Best bundle: {best}.", result=best)

    sol(
        "best-unique-bundle",
        summary="""
            A fixed-size window that also tracks duplicates. Keep the window total, a count per price, and `dup` = number
            of prices with count ≥ 2 (it changes only when a count crosses 1 ↔ 2). Each full window with `dup == 0` is a
            candidate. O(n).
        """,
        question=[
            """
            Among windows of exactly `k` consecutive prices with no repeated value, return the largest total (0 if none).

            - **n up to 10⁵**, prices up to 10⁵; totals need 64 bits.
            """
        ],
        think=[
            f"""
            `prices = {prices}`, `k = {k}` → **{want}**.

            Two things change as the window slides: its total (one price in, one out) and whether it has a repeat. Checking
            for repeats from scratch costs O(k); but "number of values that appear twice or more" changes by at most one
            per added or removed price, so it can be maintained in O(1).
            """,
            fig(Row(prices, label="prices")),
        ],
        approaches=[
            approach(
                "Check every window",
                "brute",
                "O(n · k)",
                "O(k)",
                idea=["For each window, build a set; if it has `k` values, compare the sum."],
                walk=w1,
                build=["Every window.", "Distinctness via a set.", "Keep the best total."],
                code={
                    "python": """
                        class Solution:
                            def bestUniqueBundle(self, prices: List[int], k: int) -> int:
                                best = 0  #@init
                                for i in range(len(prices) - k + 1):  #@windows
                                    window = prices[i:i + k]  #@windows
                                    if len(set(window)) == k:  #@check
                                        best = max(best, sum(window))  #@check
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long bestUniqueBundle(int[] prices, int k) {
                                long best = 0;  //@init
                                for (int i = 0; i + k <= prices.length; i++) {  //@windows
                                    Set<Integer> seen = new HashSet<>();  //@check
                                    long total = 0;  //@check
                                    for (int j = i; j < i + k; j++) { seen.add(prices[j]); total += prices[j]; }  //@check
                                    if (seen.size() == k) best = Math.max(best, total);  //@check
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long bestUniqueBundle(vector<int>& prices, int k) {
                                long long best = 0;  //@init
                                for (int i = 0; i + k <= (int) prices.size(); i++) {  //@windows
                                    unordered_set<int> seen;  //@check
                                    long long total = 0;  //@check
                                    for (int j = i; j < i + k; j++) { seen.insert(prices[j]); total += prices[j]; }  //@check
                                    if ((int) seen.size() == k) best = max(best, total);  //@check
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long bestUniqueBundle(int* prices, int pricesSize, int k) {
                            int* mark = calloc(100001, sizeof(int));  //@init
                            long long best = 0;  //@init
                            for (int i = 0; i + k <= pricesSize; i++) {  //@windows
                                long long total = 0;  //@check
                                int ok = 1;  //@check
                                for (int j = i; j < i + k && ok; j++) {  //@check
                                    if (mark[prices[j]] == i + 1) ok = 0;  //@check
                                    mark[prices[j]] = i + 1;  //@check
                                    total += prices[j];  //@check
                                }
                                if (ok && total > best) best = total;  //@check
                            }
                            free(mark);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "0 if no window qualifies.", {"c": "`mark[v] = i + 1` means 'seen in window `i`', so nothing needs clearing."}),
                    ("windows", "Every window of `k` prices."),
                    ("check", "All different, and its total."),
                    ("ret", "Best total."),
                ],
                complexity=["**Time O(n · k).** **Space O(k).**"],
                limits=["Rebuilds each window's set and sum from scratch."],
                slow=True,
            ),
            approach(
                "Sliding window with a duplicate counter",
                "best",
                "O(n)",
                "O(V)",
                idea=["Add `prices[i]` (count 1 → 2 means `dup += 1`), remove `prices[i − k]` (count 2 → 1 means `dup −= 1`), update the total. Full windows with `dup == 0` are candidates."],
                walk=w2,
                build=["Counts, `dup`, and the total.", "Add the new price, remove the old one.", "Candidates when no duplicates."],
                code={
                    "python": """
                        class Solution:
                            def bestUniqueBundle(self, prices: List[int], k: int) -> int:
                                count = [0] * 100001  #@init
                                dup = total = best = 0  #@init
                                for i, v in enumerate(prices):  #@add
                                    count[v] += 1  #@add
                                    if count[v] == 2:  #@add
                                        dup += 1  #@add
                                    total += v  #@add
                                    if i >= k:  #@remove
                                        u = prices[i - k]  #@remove
                                        count[u] -= 1  #@remove
                                        if count[u] == 1:  #@remove
                                            dup -= 1  #@remove
                                        total -= u  #@remove
                                    if i >= k - 1 and dup == 0:  #@best
                                        best = max(best, total)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long bestUniqueBundle(int[] prices, int k) {
                                int[] count = new int[100001];  //@init
                                int dup = 0;  //@init
                                long total = 0, best = 0;  //@init
                                for (int i = 0; i < prices.length; i++) {  //@add
                                    if (++count[prices[i]] == 2) dup++;  //@add
                                    total += prices[i];  //@add
                                    if (i >= k) {  //@remove
                                        if (--count[prices[i - k]] == 1) dup--;  //@remove
                                        total -= prices[i - k];  //@remove
                                    }
                                    if (i >= k - 1 && dup == 0) best = Math.max(best, total);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long bestUniqueBundle(vector<int>& prices, int k) {
                                vector<int> count(100001, 0);  //@init
                                int dup = 0;  //@init
                                long long total = 0, best = 0;  //@init
                                for (int i = 0; i < (int) prices.size(); i++) {  //@add
                                    if (++count[prices[i]] == 2) dup++;  //@add
                                    total += prices[i];  //@add
                                    if (i >= k) {  //@remove
                                        if (--count[prices[i - k]] == 1) dup--;  //@remove
                                        total -= prices[i - k];  //@remove
                                    }
                                    if (i >= k - 1 && dup == 0) best = max(best, total);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long bestUniqueBundle(int* prices, int pricesSize, int k) {
                            int* count = calloc(100001, sizeof(int));  //@init
                            int dup = 0;  //@init
                            long long total = 0, best = 0;  //@init
                            for (int i = 0; i < pricesSize; i++) {  //@add
                                if (++count[prices[i]] == 2) dup++;  //@add
                                total += prices[i];  //@add
                                if (i >= k) {  //@remove
                                    if (--count[prices[i - k]] == 1) dup--;  //@remove
                                    total -= prices[i - k];  //@remove
                                }
                                if (i >= k - 1 && dup == 0 && total > best) best = total;  //@best
                            }
                            free(count);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "A count per possible price (≤ 10⁵), the number of repeated prices, and the window total."),
                    ("add", "Price `i` enters; reaching count 2 makes it a duplicate."),
                    ("remove", "Price `i − k` leaves; dropping to count 1 means it's no longer duplicated."),
                    ("best", "A full window with no duplicates."),
                    ("ret", "Best total, or 0."),
                ],
                complexity=["**Time O(n).** **Space O(V)** for the price counts (V = 10⁵; a hash map would make it O(k))."],
            ),
        ],
        takeaways=[
            """
            - **Fixed window + "all distinct":** maintain a count map and a duplicate counter.
            - Update aggregate flags only on threshold crossings (1 ↔ 2).
            - Keep the sum alongside; both update in O(1).
            """
        ],
    )

WORD_IDS_C = """
                        static int L_;  //@ids

                        static int cmp_word(const void* a, const void* b) {  //@ids
                            return strcmp(*(char* const*) a, *(char* const*) b);  //@ids
                        }  //@ids

                        static int cmp_chunk(const void* key, const void* item) {  //@ids
                            return strncmp((const char*) key, *(char* const*) item, L_);  //@ids
                        }  //@ids

                        static int* chunk_ids(const char* s, int n, char** words, int w, int L, int** need, int* distinct) {  //@ids
                            char** uniq = malloc(w * sizeof(char*));  //@ids
                            memcpy(uniq, words, w * sizeof(char*));  //@ids
                            qsort(uniq, w, sizeof(char*), cmp_word);  //@ids
                            int d = 0;  //@ids
                            *need = calloc(w, sizeof(int));  //@ids
                            for (int i = 0; i < w; i++) {  //@ids
                                if (d == 0 || strcmp(uniq[d - 1], uniq[i]) != 0) uniq[d++] = uniq[i];  //@ids
                                (*need)[d - 1]++;  //@ids
                            }
                            L_ = L;  //@ids
                            int* id = malloc((n + 1) * sizeof(int));  //@ids
                            for (int j = 0; j + L <= n; j++) {  //@ids
                                char** hit = bsearch(s + j, uniq, d, sizeof(char*), cmp_chunk);  //@ids
                                id[j] = hit ? (int) (hit - uniq) : -1;  //@ids
                            }
                            free(uniq);  //@ids
                            *distinct = d;  //@ids
                            return id;  //@ids
                        }  //@ids
                    """


@problem
def every_word_once():
    s, words = "catdogcatcatdogdog", ["cat", "dog"]
    L, w = len(words[0]), len(words)
    need = Counter(words)
    want = [i for i in range(len(s) - w * L + 1) if Counter(s[i + j * L:i + (j + 1) * L] for j in range(w)) == need]

    w1 = Steps(f"Every start i: cut s[i : i + {w * L}] into {w} pieces of {L} letters and compare their counts with the word list.")
    for i in range(len(s) - w * L + 1):
        pieces = [s[i + j * L:i + (j + 1) * L] for j in range(w)]
        ok = Counter(pieces) == need
        w1.step(f"Start {i}: {pieces} → {'a full chain' if ok else 'no'}.", Row(list(s), st={x: ("found" if ok else "active") for x in range(i, i + w * L)}))
    w1.step(f"Starts: {want}.", result=want)

    w2 = Steps(f"Words start at multiples of {L} from some offset 0..{L - 1}. For each offset, slide a window over whole words with word counts; shrink when a word is over-used or unknown.")
    for off in range(L):
        have, left, used = Counter(), off, 0
        for j in range(off, len(s) - L + 1, L):
            chunk = s[j:j + L]
            if chunk not in need:
                have.clear()
                used, left = 0, j + L
                w2.step(f"Offset {off}: '{chunk}' isn't a word; restart after it.", Row(list(s), st={x: "mark" for x in range(j, j + L)}))
                continue
            have[chunk] += 1
            used += 1
            while have[chunk] > need[chunk]:
                have[s[left:left + L]] -= 1
                used -= 1
                left += L
            hit = used == w
            w2.step(f"Offset {off}: take '{chunk}'. Window '{s[left:j + L]}'" + (f" uses every word: start {left}." if hit else "."), Row(list(s), st={x: ("found" if hit else "active") for x in range(left, j + L)}))
            if hit:
                have[s[left:left + L]] -= 1
                used -= 1
                left += L
    w2.step(f"Starts, sorted: {want}.", result=want)

    sol(
        "every-word-once",
        summary="""
            All words have length `L`, so a chain starting at `i` is made of the chunks at `i, i + L, i + 2L, …`. Group the
            start positions by `i mod L`; within one group, slide a window over consecutive chunks with a count per word.
            Grow by one chunk; shrink from the left while that word is over-used; reset after an unknown chunk. A window of
            exactly all words is a match. O(n · L) chunk work instead of O(n · words · L).
        """,
        question=[
            """
            `words` all have the same length. Return every index of `s` where some ordering of all the words (with their
            multiplicities) appears concatenated.

            - **s up to 10⁴**, **up to 5000 words**, word length up to 30.
            """
        ],
        think=[
            f"""
            `s = "{s}"`, `words = {words}` → **{want}**.

            Checking a start means cutting `{w}` chunks and comparing word counts. Neighbouring starts that differ by `L`
            share all but one chunk, so they belong to the same sliding window. Starts at different offsets mod `L` never
            share chunks, so we run `L` independent windows, each stepping one whole word at a time.
            """,
            fig(Row(list(s), label="s"), Row(words, label="words")),
        ],
        approaches=[
            approach(
                "Check every start",
                "brute",
                "O(n · w · L)",
                "O(w · L)",
                idea=["For each start, cut `w` chunks and compare their counts with the word counts."],
                walk=w1,
                build=["Word counts.", "Every start.", "Chunk counts and compare."],
                code={
                    "python": """
                        from collections import Counter


                        class Solution:
                            def everyWordOnce(self, s: str, words: List[str]) -> List[int]:
                                L, w = len(words[0]), len(words)  #@init
                                need = Counter(words)  #@init
                                out = []  #@init
                                for i in range(len(s) - w * L + 1):  #@starts
                                    have = Counter(s[i + j * L:i + (j + 1) * L] for j in range(w))  #@check
                                    if have == need:  #@check
                                        out.append(i)  #@check
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public List<Integer> everyWordOnce(String s, String[] words) {
                                int L = words[0].length(), w = words.length;  //@init
                                Map<String, Integer> need = new HashMap<>();  //@init
                                for (String x : words) need.merge(x, 1, Integer::sum);  //@init
                                List<Integer> out = new ArrayList<>();  //@init
                                for (int i = 0; i + w * L <= s.length(); i++) {  //@starts
                                    Map<String, Integer> have = new HashMap<>();  //@check
                                    int j = 0;  //@check
                                    for (; j < w; j++) {  //@check
                                        String chunk = s.substring(i + j * L, i + (j + 1) * L);  //@check
                                        if (have.merge(chunk, 1, Integer::sum) > need.getOrDefault(chunk, 0)) break;  //@check
                                    }
                                    if (j == w) out.add(i);  //@check
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> everyWordOnce(string& s, vector<string>& words) {
                                int L = words[0].size(), w = words.size();  //@init
                                unordered_map<string, int> need;  //@init
                                for (auto& x : words) need[x]++;  //@init
                                vector<int> out;  //@init
                                for (int i = 0; i + w * L <= (int) s.size(); i++) {  //@starts
                                    unordered_map<string, int> have;  //@check
                                    int j = 0;  //@check
                                    for (; j < w; j++) {  //@check
                                        string chunk = s.substr(i + j * L, L);  //@check
                                        auto it = need.find(chunk);  //@check
                                        if (it == need.end() || ++have[chunk] > it->second) break;  //@check
                                    }
                                    if (j == w) out.push_back(i);  //@check
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": WORD_IDS_C.rstrip(" ") + """
                        int* everyWordOnce(char* s, char** words, int wordsSize, int* returnSize) {
                            int n = strlen(s), L = strlen(words[0]), w = wordsSize, d, count = 0;  //@init
                            int* need;  //@init
                            int* id = chunk_ids(s, n, words, w, L, &need, &d);  //@init
                            int* have = calloc(d, sizeof(int));  //@init
                            int* out = malloc((n + 1) * sizeof(int));  //@init
                            for (int i = 0; i + w * L <= n; i++) {  //@starts
                                int j = 0;  //@check
                                for (; j < w; j++) {  //@check
                                    int c = id[i + j * L];  //@check
                                    if (c < 0 || ++have[c] > need[c]) { if (c >= 0) have[c]--; break; }  //@check
                                }
                                for (int t = 0; t < j; t++) have[id[i + t * L]]--;  //@check
                                if (j == w) out[count++] = i;  //@check
                            }
                            free(id); free(need); free(have);  //@ret
                            *returnSize = count;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Word length, number of words, and how many times each word is required.", {"c": "Give each distinct word an id, and precompute the id of the chunk starting at every position (−1 if it isn't a word)."}),
                    ("ids", "Sort the words, merge duplicates into counts, and binary-search each chunk of `s` among them."),
                    ("starts", "Every start where a full chain fits."),
                    ("check", "Count the chunks; any chunk used more often than required (or unknown) rules this start out.", {"c": "Undo the counts after each start instead of clearing the whole array."}),
                    ("ret", "Starts in increasing order."),
                ],
                complexity=["**Time O(n · w · L)** (cutting and hashing `w` chunks per start). **Space O(w · L).**"],
                limits=["Starts `L` apart share almost all chunks, but each is checked from scratch."],
                slow=True,
            ),
            approach(
                "One word-sized window per offset",
                "best",
                "O(n · L)",
                "O(w · L)",
                idea=["For each offset `0..L−1`: walk chunks `j = off, off + L, …`. Unknown chunk: reset. Otherwise count it; while it's over-used, drop the window's first chunk. When the window holds `w` chunks, record `left` and drop its first chunk. Sort the results."],
                walk=w2,
                build=["Word counts.", "Offsets.", "Grow by a word, shrink on overuse, reset on unknown.", "Record full windows; sort."],
                code={
                    "python": """
                        class Solution:
                            def everyWordOnce(self, s: str, words: List[str]) -> List[int]:
                                L, w = len(words[0]), len(words)  #@init
                                need = {}  #@init
                                for x in words:  #@init
                                    need[x] = need.get(x, 0) + 1  #@init
                                out = []  #@init
                                for off in range(L):  #@offsets
                                    have, left, used = {}, off, 0  #@offsets
                                    for j in range(off, len(s) - L + 1, L):  #@grow
                                        chunk = s[j:j + L]  #@grow
                                        if chunk not in need:  #@reset
                                            have, left, used = {}, j + L, 0  #@reset
                                            continue  #@reset
                                        have[chunk] = have.get(chunk, 0) + 1  #@grow
                                        used += 1  #@grow
                                        while have[chunk] > need[chunk]:  #@shrink
                                            have[s[left:left + L]] -= 1  #@shrink
                                            used -= 1  #@shrink
                                            left += L  #@shrink
                                        if used == w:  #@hit
                                            out.append(left)  #@hit
                                            have[s[left:left + L]] -= 1  #@hit
                                            used -= 1  #@hit
                                            left += L  #@hit
                                return sorted(out)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public List<Integer> everyWordOnce(String s, String[] words) {
                                int L = words[0].length(), w = words.length, n = s.length();  //@init
                                Map<String, Integer> need = new HashMap<>();  //@init
                                for (String x : words) need.merge(x, 1, Integer::sum);  //@init
                                List<Integer> out = new ArrayList<>();  //@init
                                for (int off = 0; off < L; off++) {  //@offsets
                                    Map<String, Integer> have = new HashMap<>();  //@offsets
                                    int left = off, used = 0;  //@offsets
                                    for (int j = off; j + L <= n; j += L) {  //@grow
                                        String chunk = s.substring(j, j + L);  //@grow
                                        if (!need.containsKey(chunk)) { have.clear(); used = 0; left = j + L; continue; }  //@reset
                                        have.merge(chunk, 1, Integer::sum);  //@grow
                                        used++;  //@grow
                                        while (have.get(chunk) > need.get(chunk)) {  //@shrink
                                            have.merge(s.substring(left, left + L), -1, Integer::sum);  //@shrink
                                            used--;  //@shrink
                                            left += L;  //@shrink
                                        }
                                        if (used == w) {  //@hit
                                            out.add(left);  //@hit
                                            have.merge(s.substring(left, left + L), -1, Integer::sum);  //@hit
                                            used--;  //@hit
                                            left += L;  //@hit
                                        }
                                    }
                                }
                                Collections.sort(out);  //@ret
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> everyWordOnce(string& s, vector<string>& words) {
                                int L = words[0].size(), w = words.size(), n = s.size();  //@init
                                unordered_map<string, int> need;  //@init
                                for (auto& x : words) need[x]++;  //@init
                                vector<int> out;  //@init
                                for (int off = 0; off < L; off++) {  //@offsets
                                    unordered_map<string, int> have;  //@offsets
                                    int left = off, used = 0;  //@offsets
                                    for (int j = off; j + L <= n; j += L) {  //@grow
                                        string chunk = s.substr(j, L);  //@grow
                                        if (!need.count(chunk)) { have.clear(); used = 0; left = j + L; continue; }  //@reset
                                        have[chunk]++;  //@grow
                                        used++;  //@grow
                                        while (have[chunk] > need[chunk]) {  //@shrink
                                            have[s.substr(left, L)]--;  //@shrink
                                            used--;  //@shrink
                                            left += L;  //@shrink
                                        }
                                        if (used == w) {  //@hit
                                            out.push_back(left);  //@hit
                                            have[s.substr(left, L)]--;  //@hit
                                            used--;  //@hit
                                            left += L;  //@hit
                                        }
                                    }
                                }
                                sort(out.begin(), out.end());  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": WORD_IDS_C.rstrip(" ") + """
                        static int cmp_int(const void* a, const void* b) {  //@ret
                            return *(const int*) a - *(const int*) b;  //@ret
                        }  //@ret

                        int* everyWordOnce(char* s, char** words, int wordsSize, int* returnSize) {
                            int n = strlen(s), L = strlen(words[0]), w = wordsSize, d, count = 0;  //@init
                            int* need;  //@init
                            int* id = chunk_ids(s, n, words, w, L, &need, &d);  //@init
                            int* have = calloc(d, sizeof(int));  //@init
                            int* out = malloc((n + 1) * sizeof(int));  //@init
                            for (int off = 0; off < L; off++) {  //@offsets
                                int left = off, used = 0;  //@offsets
                                for (int j = off; j + L <= n; j += L) {  //@grow
                                    int c = id[j];  //@grow
                                    if (c < 0) {  //@reset
                                        for (; left < j; left += L) have[id[left]]--;  //@reset
                                        used = 0;  //@reset
                                        left = j + L;  //@reset
                                        continue;  //@reset
                                    }
                                    have[c]++;  //@grow
                                    used++;  //@grow
                                    while (have[c] > need[c]) { have[id[left]]--; used--; left += L; }  //@shrink
                                    if (used == w) { out[count++] = left; have[id[left]]--; used--; left += L; }  //@hit
                                }
                                for (; left + L <= n && used > 0; left += L, used--) have[id[left]]--;  //@offsets
                            }
                            qsort(out, count, sizeof(int), cmp_int);  //@ret
                            free(id); free(need); free(have);  //@ret
                            *returnSize = count;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Required count of each word.", {"c": "Ids for the distinct words and for the chunk at every position."}),
                    ("ids", "Sort the words, merge duplicates into counts, and binary-search each chunk of `s` among them."),
                    ("offsets", "Starts with the same remainder mod `L` share chunks; each offset gets its own window.", {"c": "Before the next offset, undo the counts still held by this window."}),
                    ("grow", "Take the next whole word into the window."),
                    ("reset", "An unknown chunk can't be in any chain: empty the window and start after it."),
                    ("shrink", "This word is now used too often: drop words from the left until it isn't."),
                    ("hit", "Exactly all words: a chain starts at `left`. Drop the first word to keep looking."),
                    ("ret", "Offsets interleave, so sort the starts."),
                ],
                complexity=["**Time O(n · L):** each offset walks `n / L` chunks, each hashed in O(L), and every chunk enters and leaves once. **Space O(w · L)** for the word table."],
            ),
        ],
        takeaways=[
            """
            - **Fixed-length tokens:** split the starts by offset mod `L` and slide over whole tokens.
            - Shrink on over-use, reset on an unknown token.
            - Same idea as anagram windows, with words instead of letters.
            """
        ],
    )



@problem
def repeat_within_reach():
    codes, k = [5, 1, 8, 2, 1, 9, 8, 3], 2
    n = len(codes)
    want = any(codes[i] == codes[j] for i in range(n) for j in range(i + 1, min(n, i + k + 1)))
    want2 = 3
    assert any(codes[i] == codes[j] for i in range(n) for j in range(i + 1, min(n, i + want2 + 1)))

    w1 = Steps(f"For each code, compare it with the next k = {k} codes.")
    for i in range(n):
        hit = next((j for j in range(i + 1, min(n, i + k + 1)) if codes[j] == codes[i]), None)
        w1.step(f"Code {codes[i]} at {i}: " + (f"repeats at {hit}." if hit is not None else "no repeat within reach."), Row(codes, st={**{x: "active" for x in range(i + 1, min(n, i + k + 1))}, i: "found"}))
    w1.step(f"Answer: {str(want).lower()}.", result=str(want).lower())

    pairs = sorted((v, i) for i, v in enumerate(codes))
    w2 = Steps("Sort (code, position) pairs. Equal codes become neighbours, ordered by position, so only neighbouring pairs need checking.")
    w2.step(f"Sorted: {pairs}.", Row([f'{v}@{i}' for v, i in pairs]))
    for a, b in zip(pairs, pairs[1:]):
        if a[0] == b[0]:
            w2.step(f"Code {a[0]} at {a[1]} and {b[1]}: {b[1] - a[1]} apart, " + ("within reach." if b[1] - a[1] <= k else f"more than {k}."), Row([f'{v}@{i}' for v, i in pairs], st={pairs.index(a): "active", pairs.index(b): "active"}))
    w2.step(f"Answer: {str(want).lower()}.", result=str(want).lower())

    w3 = Steps("Remember the last position of every code. A code is a repeat within reach if its last position is at most k back.")
    last = {}
    for i, c in enumerate(codes):
        prev = last.get(c)
        w3.step(f"Code {c} at {i}: " + (f"last seen at {prev}, {i - prev} back." if prev is not None else "first time."), Row(codes, st={i: "active", **({prev: "found"} if prev is not None else {})}), Vars(last=", ".join(f"{x}@{y}" for x, y in last.items()) or "—"))
        last[c] = i
    w3.step(f"No gap was ≤ {k}: {str(want).lower()}.", result=str(want).lower())

    sol(
        "repeat-within-reach",
        summary="""
            Remember the last index of every code in a hash map. When a code appears again, check whether its previous
            index is at most `k` back. Only the most recent occurrence matters, since it's the closest. O(n) expected.
            Sorting `(code, index)` pairs and checking neighbours is an O(n log n) alternative.
        """,
        question=[
            """
            Return whether some code appears twice at positions `i < j` with `j − i ≤ k`.

            - **n up to 10⁵**, codes from −10⁹ to 10⁹, `k` up to 10⁵.
            """
        ],
        think=[
            f"""
            `codes = {codes}`, `k = {k}` → **{str(want).lower()}** (the 1s are 3 apart, the 8s 4 apart). With `k = {want2}`
            the answer would be true.

            Looking back from position `j`, only the window of the previous `k` codes matters, and only whether `codes[j]`
            is in it. The closest earlier copy is the last one, so a last-position map answers that in O(1).
            """,
            fig(Row(codes, label="codes")),
        ],
        approaches=[
            approach(
                "Compare with the next k codes",
                "brute",
                "O(n · k)",
                "O(1)",
                idea=["For each `i`, look at `i+1 .. i+k` for an equal code."],
                walk=w1,
                build=["Every position.", "Look ahead at most `k`."],
                code={
                    "python": """
                        class Solution:
                            def repeatWithinReach(self, codes: List[int], k: int) -> bool:
                                n = len(codes)  #@init
                                for i in range(n):  #@each
                                    for j in range(i + 1, min(n, i + k + 1)):  #@ahead
                                        if codes[j] == codes[i]:  #@ahead
                                            return True  #@ahead
                                return False  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean repeatWithinReach(int[] codes, int k) {
                                int n = codes.length;  //@init
                                for (int i = 0; i < n; i++)  //@each
                                    for (int j = i + 1; j < n && j <= i + k; j++)  //@ahead
                                        if (codes[j] == codes[i]) return true;  //@ahead
                                return false;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool repeatWithinReach(vector<int>& codes, int k) {
                                int n = codes.size();  //@init
                                for (int i = 0; i < n; i++)  //@each
                                    for (int j = i + 1; j < n && j <= i + k; j++)  //@ahead
                                        if (codes[j] == codes[i]) return true;  //@ahead
                                return false;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool repeatWithinReach(int* codes, int codesSize, int k) {
                            for (int i = 0; i < codesSize; i++)  //@each
                                for (int j = i + 1; j < codesSize && j <= i + k; j++)  //@ahead
                                    if (codes[j] == codes[i]) return true;  //@ahead
                            return false;  //@ret
                        }
                    """,
                },
                lines=[("init", "Length."), ("each", "Each code."), ("ahead", "Any equal code within the next `k` positions."), ("ret", "None found.")],
                complexity=["**Time O(n · k):** 10¹⁰ comparisons at the limits. **Space O(1).**"],
                limits=["Each code is compared with up to `k` others. Remembering where each code was last seen makes it one lookup."],
                slow=True,
            ),
            approach(
                "Sort by code, check neighbours",
                "better",
                "O(n log n)",
                "O(n)",
                idea=["Sort indices by `(code, index)`. Equal codes end up adjacent and in increasing index order; check each adjacent pair with equal code for a gap ≤ `k`."],
                walk=w2,
                build=["Index array.", "Sort by code then position.", "Check neighbours."],
                code={
                    "python": """
                        class Solution:
                            def repeatWithinReach(self, codes: List[int], k: int) -> bool:
                                order = sorted(range(len(codes)), key=lambda i: (codes[i], i))  #@sort
                                for a, b in zip(order, order[1:]):  #@pairs
                                    if codes[a] == codes[b] and b - a <= k:  #@pairs
                                        return True  #@pairs
                                return False  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean repeatWithinReach(int[] codes, int k) {
                                int n = codes.length;  //@sort
                                long[] keyed = new long[n];  //@sort
                                for (int i = 0; i < n; i++) keyed[i] = ((long) codes[i] << 20) | i;  //@sort
                                Arrays.sort(keyed);  //@sort
                                for (int t = 1; t < n; t++) {  //@pairs
                                    long a = keyed[t - 1], b = keyed[t];  //@pairs
                                    if ((a >> 20) == (b >> 20) && (b & 0xFFFFF) - (a & 0xFFFFF) <= k) return true;  //@pairs
                                }
                                return false;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool repeatWithinReach(vector<int>& codes, int k) {
                                int n = codes.size();  //@sort
                                vector<pair<int, int>> keyed(n);  //@sort
                                for (int i = 0; i < n; i++) keyed[i] = {codes[i], i};  //@sort
                                sort(keyed.begin(), keyed.end());  //@sort
                                for (int t = 1; t < n; t++)  //@pairs
                                    if (keyed[t].first == keyed[t - 1].first && keyed[t].second - keyed[t - 1].second <= k) return true;  //@pairs
                                return false;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int by_code(const void* x, const void* y) {  //@sort
                            const int* a = x;  //@sort
                            const int* b = y;  //@sort
                            if (a[0] != b[0]) return a[0] < b[0] ? -1 : 1;  //@sort
                            return a[1] - b[1];  //@sort
                        }  //@sort

                        bool repeatWithinReach(int* codes, int codesSize, int k) {
                            int n = codesSize;  //@sort
                            int* keyed = malloc(2 * n * sizeof(int));  //@sort
                            for (int i = 0; i < n; i++) { keyed[2 * i] = codes[i]; keyed[2 * i + 1] = i; }  //@sort
                            qsort(keyed, n, 2 * sizeof(int), by_code);  //@sort
                            bool found = false;  //@pairs
                            for (int t = 1; t < n && !found; t++)  //@pairs
                                if (keyed[2 * t] == keyed[2 * t - 2] && keyed[2 * t + 1] - keyed[2 * t - 1] <= k) found = true;  //@pairs
                            free(keyed);  //@ret
                            return found;  //@ret
                        }
                    """,
                },
                lines=[
                    ("sort", "Order positions by code, then by position.", {"java": "Pack code and position into one long (positions fit in 20 bits) and sort primitives.", "c": "Sort (code, position) pairs stored side by side."}),
                    ("pairs", "Between equal codes, the closest pair is adjacent in this order."),
                    ("ret", "No close repeat."),
                ],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Sorting costs O(n log n); a hash map of last positions answers each check in O(1) expected time."],
            ),
            approach(
                "Last position of each code",
                "best",
                "O(n)",
                "O(n)",
                idea=["Scan left to right with a map `last[code] = index`. If `code` was seen and `i − last[code] ≤ k`, return true; then update `last[code] = i`."],
                walk=w3,
                build=["Map from code to last index.", "Check the gap.", "Update."],
                code={
                    "python": """
                        class Solution:
                            def repeatWithinReach(self, codes: List[int], k: int) -> bool:
                                last = {}  #@init
                                for i, c in enumerate(codes):  #@scan
                                    if c in last and i - last[c] <= k:  #@check
                                        return True  #@check
                                    last[c] = i  #@update
                                return False  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean repeatWithinReach(int[] codes, int k) {
                                Map<Integer, Integer> last = new HashMap<>();  //@init
                                for (int i = 0; i < codes.length; i++) {  //@scan
                                    Integer prev = last.put(codes[i], i);  //@update
                                    if (prev != null && i - prev <= k) return true;  //@check
                                }
                                return false;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool repeatWithinReach(vector<int>& codes, int k) {
                                unordered_map<int, int> last;  //@init
                                for (int i = 0; i < (int) codes.size(); i++) {  //@scan
                                    auto it = last.find(codes[i]);  //@check
                                    if (it != last.end() && i - it->second <= k) return true;  //@check
                                    last[codes[i]] = i;  //@update
                                }
                                return false;  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool repeatWithinReach(int* codes, int codesSize, int k) {
                            int cap = 1;  //@init
                            while (cap < 2 * codesSize) cap <<= 1;  //@init
                            int* keys = malloc(cap * sizeof(int));  //@init
                            int* at = malloc(cap * sizeof(int));  //@init
                            char* used = calloc(cap, 1);  //@init
                            bool found = false;  //@init
                            for (int i = 0; i < codesSize && !found; i++) {  //@scan
                                unsigned h = ((unsigned) codes[i] * 2654435761u) & (cap - 1);  //@scan
                                while (used[h] && keys[h] != codes[i]) h = (h + 1) & (cap - 1);  //@scan
                                if (used[h] && i - at[h] <= k) found = true;  //@check
                                used[h] = 1;  //@update
                                keys[h] = codes[i];  //@update
                                at[h] = i;  //@update
                            }
                            free(keys); free(at); free(used);  //@ret
                            return found;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Code → last index.", {"c": "A small open-addressing hash table: at least twice as many slots as codes, so probes stay short."}),
                    ("scan", "Each code in order.", {"c": "Hash the code and probe forward to its slot (or an empty one)."}),
                    ("check", "The previous copy is the closest one; within `k` means yes.", {"java": "`put` returns the previous index, if any."}),
                    ("update", "This position is now the last one."),
                    ("ret", "No close repeat."),
                ],
                complexity=["**Time O(n)** expected. **Space O(n)** (a window set of the last `k` codes would be O(k))."],
            ),
        ],
        takeaways=[
            """
            - **"Duplicate within distance k":** last-index map, or a set of the last `k` items.
            - Only the most recent occurrence matters.
            - Sorting pairs is the no-hashing fallback.
            """
        ],
    )


@problem
def scrambled_copies():
    text, word = "baacabcaab", "abc"
    m = len(word)
    want = [i for i in range(len(text) - m + 1) if sorted(text[i:i + m]) == sorted(word)]

    w1 = Steps("Count the letters of every window of length m and compare them with the word's counts.")
    for i in range(len(text) - m + 1):
        ok = sorted(text[i:i + m]) == sorted(word)
        w1.step(f"'{text[i:i + m]}' {'has the same letters' if ok else 'differs'}.", Row(list(text), st={x: ("found" if ok else "active") for x in range(i, i + m)}))
    w1.step(f"Starts: {want}.", result=want)

    w2 = Steps("Keep the window's letter counts and diff = how many letters have a different count from the word. One letter in, one out per step; the window matches when diff is 0.")
    need, have = Counter(word), Counter()
    letters = set(word) | set(text)
    for i, c in enumerate(text):
        have[c] += 1
        if i >= m:
            have[text[i - m]] -= 1
        if i >= m - 1:
            diff = sum(1 for x in letters if have[x] != need[x])
            w2.step(f"Window '{text[i - m + 1:i + 1]}': diff = {diff}" + (" → match." if diff == 0 else "."), Row(list(text), st={x: ("found" if diff == 0 else "active") for x in range(i - m + 1, i + 1)}), Vars(diff=diff))
    w2.step(f"Starts: {want}.", result=want)

    sol(
        "scrambled-copies",
        summary="""
            A window is a rearrangement of `word` exactly when its letter counts equal the word's. Slide a window of length
            `m`, updating two counts per step, and keep `diff` = number of letters whose counts disagree; each update
            changes it by at most one per letter touched. Record starts with `diff == 0`. O(n + m).
        """,
        question=[
            """
            Return every start index in `text` of a substring that is a rearrangement of `word`.

            - **Both up to 10⁵ letters.**
            """
        ],
        think=[
            f"""
            `text = "{text}"`, `word = "{word}"` → **{want}**.

            Rearrangements share letter counts, so we compare count tables. Recounting each window is O(m); sliding by one
            changes only the entering and leaving letters, and tracking how many of the 26 letters currently disagree lets
            us test equality in O(1).
            """,
            fig(Row(list(text), label="text"), Row(list(word), label="word")),
        ],
        approaches=[
            approach(
                "Count every window",
                "brute",
                "O(n · m)",
                "O(1)",
                idea=["For each start, count the window's letters into a 26-array and compare with the word's."],
                walk=w1,
                build=["Word counts.", "Every window.", "Count and compare."],
                code={
                    "python": """
                        class Solution:
                            def scrambledCopies(self, text: str, word: str) -> List[int]:
                                m = len(word)  #@init
                                need = [0] * 26  #@init
                                for c in word:  #@init
                                    need[ord(c) - 97] += 1  #@init
                                out = []  #@init
                                for i in range(len(text) - m + 1):  #@windows
                                    have = [0] * 26  #@count
                                    for c in text[i:i + m]:  #@count
                                        have[ord(c) - 97] += 1  #@count
                                    if have == need:  #@count
                                        out.append(i)  #@count
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public List<Integer> scrambledCopies(String text, String word) {
                                int m = word.length();  //@init
                                int[] need = new int[26];  //@init
                                for (char c : word.toCharArray()) need[c - 'a']++;  //@init
                                List<Integer> out = new ArrayList<>();  //@init
                                for (int i = 0; i + m <= text.length(); i++) {  //@windows
                                    int[] have = new int[26];  //@count
                                    for (int j = i; j < i + m; j++) have[text.charAt(j) - 'a']++;  //@count
                                    if (Arrays.equals(have, need)) out.add(i);  //@count
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> scrambledCopies(string& text, string& word) {
                                int m = word.size();  //@init
                                array<int, 26> need{};  //@init
                                for (char c : word) need[c - 'a']++;  //@init
                                vector<int> out;  //@init
                                for (int i = 0; i + m <= (int) text.size(); i++) {  //@windows
                                    array<int, 26> have{};  //@count
                                    for (int j = i; j < i + m; j++) have[text[j] - 'a']++;  //@count
                                    if (have == need) out.push_back(i);  //@count
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* scrambledCopies(char* text, char* word, int* returnSize) {
                            int n = strlen(text), m = strlen(word), need[26] = {0}, count = 0;  //@init
                            for (int i = 0; i < m; i++) need[word[i] - 'a']++;  //@init
                            int* out = malloc((n + 1) * sizeof(int));  //@init
                            for (int i = 0; i + m <= n; i++) {  //@windows
                                int have[26] = {0};  //@count
                                for (int j = i; j < i + m; j++) have[text[j] - 'a']++;  //@count
                                if (memcmp(have, need, sizeof(have)) == 0) out[count++] = i;  //@count
                            }
                            *returnSize = count;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "Letter counts of the word."), ("windows", "Every window of length `m`."), ("count", "Count its letters and compare all 26."), ("ret", "Starts in order.")],
                complexity=["**Time O(n · m).** **Space O(1).**"],
                limits=["Recounts `m` letters per window although only two change."],
                slow=True,
            ),
            approach(
                "Sliding counts with a mismatch counter",
                "best",
                "O(n + m)",
                "O(1)",
                idea=["`delta[c] = window count − word count`, starting at `−need`. `diff` = letters with `delta ≠ 0`. Adding or removing a letter changes one `delta`; adjust `diff` when it moves to or from 0. Record when `diff == 0` for a full window."],
                walk=w2,
                build=["Start from the word's counts as a deficit.", "Add the entering letter, remove the leaving one.", "Record full windows with no mismatch."],
                code={
                    "python": """
                        class Solution:
                            def scrambledCopies(self, text: str, word: str) -> List[int]:
                                m = len(word)  #@init
                                delta = [0] * 26  #@init
                                for c in word:  #@init
                                    delta[ord(c) - 97] -= 1  #@init
                                diff = sum(1 for d in delta if d)  #@init
                                out = []  #@init

                                def bump(x, by):  #@bump
                                    nonlocal diff  #@bump
                                    if delta[x] == 0:  #@bump
                                        diff += 1  #@bump
                                    delta[x] += by  #@bump
                                    if delta[x] == 0:  #@bump
                                        diff -= 1  #@bump

                                for i, c in enumerate(text):  #@slide
                                    bump(ord(c) - 97, 1)  #@slide
                                    if i >= m:  #@slide
                                        bump(ord(text[i - m]) - 97, -1)  #@slide
                                    if i >= m - 1 and diff == 0:  #@hit
                                        out.append(i - m + 1)  #@hit
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int[] delta = new int[26];  //@init
                            private int diff = 0;  //@init

                            private void bump(int x, int by) {  //@bump
                                if (delta[x] == 0) diff++;  //@bump
                                delta[x] += by;  //@bump
                                if (delta[x] == 0) diff--;  //@bump
                            }  //@bump

                            public List<Integer> scrambledCopies(String text, String word) {
                                int m = word.length();  //@init
                                for (char c : word.toCharArray()) bump(c - 'a', -1);  //@init
                                List<Integer> out = new ArrayList<>();  //@init
                                for (int i = 0; i < text.length(); i++) {  //@slide
                                    bump(text.charAt(i) - 'a', 1);  //@slide
                                    if (i >= m) bump(text.charAt(i - m) - 'a', -1);  //@slide
                                    if (i >= m - 1 && diff == 0) out.add(i - m + 1);  //@hit
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            int delta[26] = {0}, diff = 0;  //@init

                            void bump(int x, int by) {  //@bump
                                if (delta[x] == 0) diff++;  //@bump
                                delta[x] += by;  //@bump
                                if (delta[x] == 0) diff--;  //@bump
                            }  //@bump

                        public:
                            vector<int> scrambledCopies(string& text, string& word) {
                                int m = word.size();  //@init
                                for (char c : word) bump(c - 'a', -1);  //@init
                                vector<int> out;  //@init
                                for (int i = 0; i < (int) text.size(); i++) {  //@slide
                                    bump(text[i] - 'a', 1);  //@slide
                                    if (i >= m) bump(text[i - m] - 'a', -1);  //@slide
                                    if (i >= m - 1 && diff == 0) out.push_back(i - m + 1);  //@hit
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static void bump(int* delta, int* diff, int x, int by) {  //@bump
                            if (delta[x] == 0) (*diff)++;  //@bump
                            delta[x] += by;  //@bump
                            if (delta[x] == 0) (*diff)--;  //@bump
                        }  //@bump

                        int* scrambledCopies(char* text, char* word, int* returnSize) {
                            int n = strlen(text), m = strlen(word), delta[26] = {0}, diff = 0, count = 0;  //@init
                            for (int i = 0; i < m; i++) bump(delta, &diff, word[i] - 'a', -1);  //@init
                            int* out = malloc((n + 1) * sizeof(int));  //@init
                            for (int i = 0; i < n; i++) {  //@slide
                                bump(delta, &diff, text[i] - 'a', 1);  //@slide
                                if (i >= m) bump(delta, &diff, text[i - m] - 'a', -1);  //@slide
                                if (i >= m - 1 && diff == 0) out[count++] = i - m + 1;  //@hit
                            }
                            *returnSize = count;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Before any window, every letter of the word is a deficit; `diff` counts the letters out of balance."),
                    ("bump", "Change one letter's balance, keeping `diff` right: leaving 0 adds a mismatch, reaching 0 removes one."),
                    ("slide", "The entering letter adds to the window; once it's longer than `m`, the leaving letter is removed."),
                    ("hit", "A full window with no mismatched letter is a rearrangement."),
                    ("ret", "Starts in order."),
                ],
                complexity=["**Time O(n + m).** **Space O(1)** (26 counters)."],
            ),
        ],
        takeaways=[
            """
            - **Anagram windows:** fixed-size window + count balance.
            - A **mismatch counter** turns a 26-way comparison into O(1).
            - Combine "need" and "have" into one signed `delta` array.
            """
        ],
    )


@problem
def variety_per_window():
    items, k = [4, 1, 4, 4, 7, 1, 7, 2], 3
    n = len(items)
    want = [len(set(items[i:i + k])) for i in range(n - k + 1)]

    w1 = Steps("Put each window's items into a set and take its size.")
    for i in range(n - k + 1):
        w1.step(f"{items[i:i + k]} → {want[i]} type(s).", Row(items, st={x: "active" for x in range(i, i + k)}))
    w1.step(f"Answer: {want}.", result=want)

    w2 = Steps("Keep a count per type in the window and the number of types with a positive count. Each step adds one item and removes one.")
    count, distinct, out = Counter(), 0, []
    for i, v in enumerate(items):
        count[v] += 1
        distinct += count[v] == 1
        note = f"add {v}"
        if i >= k:
            u = items[i - k]
            count[u] -= 1
            distinct -= count[u] == 0
            note += f", remove {u}"
        if i >= k - 1:
            out.append(distinct)
            w2.step(f"Window {items[i - k + 1:i + 1]} ({note}): {distinct} type(s).", Row(items, st={x: "active" for x in range(i - k + 1, i + 1)}), Vars(answer=list(out)))
    w2.step(f"Answer: {out}.", result=out)

    sol(
        "variety-per-window",
        summary="""
            Slide a window of `k` items with a count per type and a `distinct` counter. Adding an item whose count goes
            0 → 1 raises `distinct`; removing one whose count goes 1 → 0 lowers it. Record `distinct` for every full
            window. O(n) expected (types up to 10⁹, so use a hash map, or compress the values).
        """,
        question=[
            """
            For every window of `k` consecutive `items`, return the number of different values in it.

            - **n up to 10⁵**, values up to 10⁹.
            """
        ],
        think=[
            f"""
            `items = {items}`, `k = {k}` → **{want}**.

            Recomputing each window's distinct count is O(k). But one slide changes just two items, and the distinct count
            only changes when an item's count crosses zero, so keeping counts makes each step O(1).
            """,
            fig(Row(items, label="items")),
        ],
        approaches=[
            approach(
                "A set per window",
                "brute",
                "O(n · k)",
                "O(k)",
                idea=["For each window, build a set and record its size."],
                walk=w1,
                build=["Every window.", "Set size."],
                code={
                    "python": """
                        class Solution:
                            def varietyPerWindow(self, items: List[int], k: int) -> List[int]:
                                return [len(set(items[i:i + k])) for i in range(len(items) - k + 1)]  #@windows
                    """,
                    "java": """
                        class Solution {
                            public int[] varietyPerWindow(int[] items, int k) {
                                int[] out = new int[items.length - k + 1];  //@windows
                                for (int i = 0; i < out.length; i++) {  //@windows
                                    Set<Integer> seen = new HashSet<>();  //@windows
                                    for (int j = i; j < i + k; j++) seen.add(items[j]);  //@windows
                                    out[i] = seen.size();  //@windows
                                }
                                return out;  //@windows
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> varietyPerWindow(vector<int>& items, int k) {
                                vector<int> out;  //@windows
                                for (int i = 0; i + k <= (int) items.size(); i++)  //@windows
                                    out.push_back(unordered_set<int>(items.begin() + i, items.begin() + i + k).size());  //@windows
                                return out;  //@windows
                            }
                        };
                    """,
                    "c": COMPRESS_C.rstrip(" ") + """
                        int* varietyPerWindow(int* items, int itemsSize, int k, int* returnSize) {
                            int n = itemsSize, d, count = n - k + 1;  //@windows
                            int* id = compress(items, n, &d);  //@windows
                            int* mark = calloc(d, sizeof(int));  //@windows
                            int* out = malloc(count * sizeof(int));  //@windows
                            for (int i = 0; i < count; i++) {  //@windows
                                out[i] = 0;  //@windows
                                for (int j = i; j < i + k; j++) if (mark[id[j]] != i + 1) { mark[id[j]] = i + 1; out[i]++; }  //@windows
                            }
                            free(id); free(mark);  //@windows
                            *returnSize = count;  //@windows
                            return out;  //@windows
                        }
                    """,
                },
                lines=[
                    ("windows", "Each window's distinct count, from scratch.", {"c": "Values are compressed to ids; `mark[id] = i + 1` means 'seen in window `i`'."}),
                    ("compress", "Sort a copy, remove duplicates, and find each value's position by binary search."),
                ],
                complexity=["**Time O(n · k).** **Space O(k).**"],
                limits=["Each window costs O(k), although consecutive windows differ by two items."],
                slow=True,
            ),
            approach(
                "Sliding counts",
                "best",
                "O(n)",
                "O(k)",
                idea=["Add `items[i]` (0 → 1 raises `distinct`), remove `items[i − k]` (1 → 0 lowers it); from `i = k − 1` on, append `distinct`."],
                walk=w2,
                build=["Count map and `distinct`.", "Add and remove.", "Record each full window."],
                code={
                    "python": """
                        class Solution:
                            def varietyPerWindow(self, items: List[int], k: int) -> List[int]:
                                count, distinct, out = {}, 0, []  #@init
                                for i, v in enumerate(items):  #@add
                                    count[v] = count.get(v, 0) + 1  #@add
                                    if count[v] == 1:  #@add
                                        distinct += 1  #@add
                                    if i >= k:  #@remove
                                        u = items[i - k]  #@remove
                                        count[u] -= 1  #@remove
                                        if count[u] == 0:  #@remove
                                            distinct -= 1  #@remove
                                    if i >= k - 1:  #@record
                                        out.append(distinct)  #@record
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] varietyPerWindow(int[] items, int k) {
                                Map<Integer, Integer> count = new HashMap<>();  //@init
                                int distinct = 0;  //@init
                                int[] out = new int[items.length - k + 1];  //@init
                                for (int i = 0; i < items.length; i++) {  //@add
                                    if (count.merge(items[i], 1, Integer::sum) == 1) distinct++;  //@add
                                    if (i >= k && count.merge(items[i - k], -1, Integer::sum) == 0) distinct--;  //@remove
                                    if (i >= k - 1) out[i - k + 1] = distinct;  //@record
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> varietyPerWindow(vector<int>& items, int k) {
                                unordered_map<int, int> count;  //@init
                                int distinct = 0;  //@init
                                vector<int> out;  //@init
                                for (int i = 0; i < (int) items.size(); i++) {  //@add
                                    if (++count[items[i]] == 1) distinct++;  //@add
                                    if (i >= k && --count[items[i - k]] == 0) distinct--;  //@remove
                                    if (i >= k - 1) out.push_back(distinct);  //@record
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": COMPRESS_C.rstrip(" ") + """
                        int* varietyPerWindow(int* items, int itemsSize, int k, int* returnSize) {
                            int n = itemsSize, d, distinct = 0;  //@init
                            int* id = compress(items, n, &d);  //@init
                            int* count = calloc(d, sizeof(int));  //@init
                            int* out = malloc((n - k + 1) * sizeof(int));  //@init
                            for (int i = 0; i < n; i++) {  //@add
                                if (count[id[i]]++ == 0) distinct++;  //@add
                                if (i >= k && --count[id[i - k]] == 0) distinct--;  //@remove
                                if (i >= k - 1) out[i - k + 1] = distinct;  //@record
                            }
                            free(id); free(count);  //@ret
                            *returnSize = n - k + 1;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Counts of the window's values and how many are present.", {"c": "Compress values to ids `0..d−1` so the counts are an array."}),
                    ("compress", "Sort a copy, remove duplicates, and find each value's position by binary search."),
                    ("add", "Item `i` enters; a value going 0 → 1 is a new type."),
                    ("remove", "Item `i − k` leaves; a value going 1 → 0 is gone."),
                    ("record", "Every full window's count, left to right."),
                    ("ret", "One number per window."),
                ],
                complexity=["**Time O(n)** expected (O(n log n) for C's compression). **Space O(k)** for the map (O(n) in C)."],
            ),
        ],
        takeaways=[
            """
            - **Distinct count per window:** a count map + a counter updated on 0 ↔ 1 transitions.
            - Large values: hash map, or compress once.
            - The same machinery powers "at most k distinct" windows.
            """
        ],
    )
