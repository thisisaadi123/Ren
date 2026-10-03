"""Two Pointers: checking whether one string is hidden in another (subsequences)."""
import bisect
from collections import defaultdict

from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def hidden(word, text):
    i = 0
    for c in text:
        if i < len(word) and c == word[i]:
            i += 1
    return i == len(word)


@problem
def hidden_word():
    word, text = "rent", "riverbend fountain"
    want = hidden(word, text)

    w = Steps("One pointer in the word, one in the text. Every text letter that matches the next needed word letter advances the word pointer.")
    i = 0
    for t, c in enumerate(text):
        if i < len(word) and c == word[i]:
            i += 1
            w.step(f"Text letter '{c}' at {t} matches '{c}': {i} of {len(word)} found.", Row(list(text), st={t: "found"}), Row(list(word), st={x: "found" for x in range(i)}, label="word"))
    w.step(f"All {len(word)} letters found in order: {str(want).lower()}.", result=str(want).lower())

    sol(
        "hidden-word",
        summary="""
            Walk the text once with a pointer into the word. Whenever the current text letter equals the next letter the
            word needs, advance the word pointer. The word is hidden exactly when the pointer reaches its end. Taking the
            earliest match is always safe. O(text length).
        """,
        question=[
            """
            Is `word` a subsequence of `text`: can its letters be found in `text` in order, not necessarily next to each
            other?

            - **The empty word** is hidden in every text.
            - **Text up to 10⁵ letters.**
            """
        ],
        think=[
            f"""
            `"{word}"` in `"{text}"`: r (r-iver), e (riv-e-r), n (be-n-d), t (moun-t-ain). **{str(want).lower()}**.

            Greedy works: when the next needed letter appears, use it immediately. Using a later copy instead can only
            leave less text for the remaining letters, never more.
            """,
            fig(Row(list(text), label="text"), Row(list(word), label="word")),
        ],
        approaches=[
            approach(
                "Greedy two pointers",
                "best",
                "O(n + m)",
                "O(1)",
                idea=["`i` indexes the word. For each text character `c`: if `i < len(word)` and `c == word[i]`, advance `i`. Return `i == len(word)`."],
                walk=w,
                build=["Word pointer at 0.", "Scan the text, advancing on matches.", "Check that the whole word was matched."],
                code={
                    "python": """
                        class Solution:
                            def isHidden(self, word: str, text: str) -> bool:
                                i = 0  #@init
                                for c in text:  #@scan
                                    if i < len(word) and c == word[i]:  #@match
                                        i += 1  #@match
                                return i == len(word)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean isHidden(String word, String text) {
                                int i = 0;  //@init
                                for (int t = 0; t < text.length(); t++)  //@scan
                                    if (i < word.length() && text.charAt(t) == word.charAt(i)) i++;  //@match
                                return i == word.length();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool isHidden(string& word, string& text) {
                                size_t i = 0;  //@init
                                for (char c : text)  //@scan
                                    if (i < word.size() && c == word[i]) i++;  //@match
                                return i == word.size();  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool isHidden(char* word, char* text) {
                            int i = 0;  //@init
                            for (int t = 0; text[t]; t++)  //@scan
                                if (word[i] && text[t] == word[i]) i++;  //@match
                            return word[i] == '\\0';  //@ret
                        }
                    """,
                },
                lines=[("init", "How many word letters have been found."), ("scan", "Every text letter, once."), ("match", "The next needed letter: use the earliest copy.", {"c": "`word[i]` is `'\\\\0'` once the word is fully matched."}), ("ret", "Hidden when every letter was found.")],
                complexity=["**Time O(n + m).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Subsequence check = greedy two pointers**: match each needed letter at its earliest chance.
            - For many queries against one text, precompute each letter's positions and binary-search them.
            - Empty word → true.
            """
        ],
    )


@problem
def count_hidden_words():
    text, words = "trainstation", ["tin", "rain", "sat", "ran", "tin", "zoo"]
    want = sum(hidden(w_, text) for w_ in words)

    w1 = Steps("Check each word separately with the two-pointer subsequence test.")
    for w_ in words:
        w1.step(f"'{w_}' is {'hidden' if hidden(w_, text) else 'not hidden'}.", Row(list(text)), Vars(word=w_, hidden=str(hidden(w_, text)).lower()))
    w1.step(f"{want} words are hidden.", result=want)

    pos = defaultdict(list)
    for i, c in enumerate(text):
        pos[c].append(i)
    w2 = Steps("List the positions of each letter in the text once. For each word, binary-search each letter's next position after the previous match.")
    w2.step("Positions per letter: " + ", ".join(f"{c}: {pos[c]}" for c in sorted(pos)) + ".", Row(list(text)))
    for w_ in words[:3]:
        at, ok, picks = -1, True, []
        for c in w_:
            lst = pos.get(c, [])
            k = bisect.bisect_right(lst, at)
            if k == len(lst):
                ok = False; break
            at = lst[k]; picks.append(at)
        w2.step(f"'{w_}': next positions {picks} → {'hidden' if ok else 'not hidden'}.", Row(list(text), st={p: "found" for p in picks}))
    w2.step(f"{want} words are hidden.", result=want)

    w3 = Steps("Read the text once. Each word waits in a bucket for the letter it needs next; when that letter is read, everyone in its bucket moves on.")
    waiting = defaultdict(list)
    for w_ in words:
        waiting[w_[0]].append((w_, 0))
    done = 0
    for t, c in enumerate(text):
        bucket = waiting.pop(c, [])
        moved = []
        for w_, i in bucket:
            i += 1
            if i == len(w_):
                done += 1; moved.append(f"{w_}✓")
            else:
                waiting[w_[i]].append((w_, i)); moved.append(f"{w_}→{w_[i]}")
        if bucket:
            w3.step(f"Read '{c}': {', '.join(moved)}.", Row(list(text), st={t: "active"}), Vars(finished=done))
    w3.step(f"{done} words finished.", result=done)

    sol(
        "count-hidden-words",
        summary="""
            Read the text **once** for all words. Each word waits in a bucket for the next letter it needs. Reading a letter
            empties that letter's bucket: each word in it advances to its next letter (and moves to that bucket) or, if it's
            complete, is counted. Total work O(text length + total word length).
        """,
        question=[
            """
            Count how many of `words` are subsequences of `text` (duplicates count each time).

            - **Text up to 5 × 10⁴**, up to 5000 words of length ≤ 50.
            - Checking each word separately reads the whole text 5000 times: 2.5 × 10⁸ steps.
            """
        ],
        think=[
            f"""
            Text `"{text}"`, words `{words}`: {[w_ for w_ in words if hidden(w_, text)]} are hidden, so **{want}**.

            The per-word check is fine, but repeating it rereads the text for every word. Flip it: read the text once, and
            let all words advance in parallel. A word only cares about one letter at a time (its next needed letter), so
            group words by that letter.
            """,
            fig(Row(list(text), label="text")),
        ],
        approaches=[
            approach(
                "Check each word separately",
                "brute",
                "O(W · T)",
                "O(1)",
                idea=["For each word, run the two-pointer subsequence check over the whole text."],
                walk=w1,
                build=["Subsequence check helper.", "Count words that pass."],
                code={
                    "python": """
                        class Solution:
                            def countHidden(self, text: str, words: List[str]) -> int:
                                count = 0  #@init
                                for w in words:  #@each
                                    i = 0  #@check
                                    for c in text:  #@check
                                        if i < len(w) and c == w[i]:  #@check
                                            i += 1  #@check
                                    if i == len(w):  #@each
                                        count += 1  #@each
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countHidden(String text, String[] words) {
                                int count = 0;  //@init
                                for (String w : words) {  //@each
                                    int i = 0;  //@check
                                    for (int t = 0; t < text.length() && i < w.length(); t++)  //@check
                                        if (text.charAt(t) == w.charAt(i)) i++;  //@check
                                    if (i == w.length()) count++;  //@each
                                }
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countHidden(string& text, vector<string>& words) {
                                int count = 0;  //@init
                                for (auto& w : words) {  //@each
                                    size_t i = 0;  //@check
                                    for (size_t t = 0; t < text.size() && i < w.size(); t++)  //@check
                                        if (text[t] == w[i]) i++;  //@check
                                    if (i == w.size()) count++;  //@each
                                }
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countHidden(char* text, char** words, int wordsSize) {
                            int count = 0;  //@init
                            for (int k = 0; k < wordsSize; k++) {  //@each
                                const char* w = words[k];  //@check
                                int i = 0;  //@check
                                for (int t = 0; text[t] && w[i]; t++)  //@check
                                    if (text[t] == w[i]) i++;  //@check
                                if (!w[i]) count++;  //@each
                            }
                            return count;  //@ret
                        }
                    """,
                },
                lines=[("init", "Hidden words found."), ("each", "Each word, counted if fully matched."), ("check", "The greedy subsequence test over the text."), ("ret", "Total.")],
                complexity=["**Time O(W · T):** the text is read once per word, up to 2.5 × 10⁸ steps. **Space O(1).**"],
                limits=["Rereads the whole text for every word. Precomputing where each letter occurs lets a word jump straight to its next letter."],
                slow=True,
            ),
            approach(
                "Letter positions + binary search",
                "better",
                "O(T + L log T)",
                "O(T)",
                idea=["List the positions of each letter in the text. For a word, keep the last matched position `at`; each next letter jumps to its first position after `at` (binary search). Missing → not hidden."],
                walk=w2,
                build=["Positions per letter.", "For each word, chain `upper_bound` lookups.", "Count successes."],
                code={
                    "python": """
                        import bisect

                        class Solution:
                            def countHidden(self, text: str, words: List[str]) -> int:
                                pos = {}  #@index
                                for i, c in enumerate(text):  #@index
                                    pos.setdefault(c, []).append(i)  #@index
                                count = 0  #@init
                                for w in words:  #@each
                                    at, ok = -1, True  #@jump
                                    for c in w:  #@jump
                                        lst = pos.get(c, [])  #@jump
                                        k = bisect.bisect_right(lst, at)  #@jump
                                        if k == len(lst):  #@jump
                                            ok = False  #@jump
                                            break  #@jump
                                        at = lst[k]  #@jump
                                    count += ok  #@each
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countHidden(String text, String[] words) {
                                List<List<Integer>> pos = new ArrayList<>();  //@index
                                for (int c = 0; c < 26; c++) pos.add(new ArrayList<>());  //@index
                                for (int i = 0; i < text.length(); i++) pos.get(text.charAt(i) - 'a').add(i);  //@index
                                int count = 0;  //@init
                                for (String w : words) {  //@each
                                    int at = -1;  //@jump
                                    boolean ok = true;  //@jump
                                    for (int t = 0; t < w.length() && ok; t++) {  //@jump
                                        List<Integer> lst = pos.get(w.charAt(t) - 'a');  //@jump
                                        int lo = 0, hi = lst.size();  //@jump
                                        while (lo < hi) { int mid = (lo + hi) >>> 1; if (lst.get(mid) <= at) lo = mid + 1; else hi = mid; }  //@jump
                                        if (lo == lst.size()) ok = false; else at = lst.get(lo);  //@jump
                                    }
                                    if (ok) count++;  //@each
                                }
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countHidden(string& text, vector<string>& words) {
                                vector<vector<int>> pos(26);  //@index
                                for (int i = 0; i < (int) text.size(); i++) pos[text[i] - 'a'].push_back(i);  //@index
                                int count = 0;  //@init
                                for (auto& w : words) {  //@each
                                    int at = -1;  //@jump
                                    bool ok = true;  //@jump
                                    for (char c : w) {  //@jump
                                        auto& lst = pos[c - 'a'];  //@jump
                                        auto it = upper_bound(lst.begin(), lst.end(), at);  //@jump
                                        if (it == lst.end()) { ok = false; break; }  //@jump
                                        at = *it;  //@jump
                                    }
                                    if (ok) count++;  //@each
                                }
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countHidden(char* text, char** words, int wordsSize) {
                            int n = strlen(text), start[27] = {0};  //@index
                            for (int i = 0; i < n; i++) start[text[i] - 'a' + 1]++;  //@index
                            for (int c = 0; c < 26; c++) start[c + 1] += start[c];  //@index
                            int* pos = malloc((n + 1) * sizeof(int));  //@index
                            int fill[26];  //@index
                            memcpy(fill, start, sizeof fill);  //@index
                            for (int i = 0; i < n; i++) pos[fill[text[i] - 'a']++] = i;  //@index
                            int count = 0;  //@init
                            for (int k = 0; k < wordsSize; k++) {  //@each
                                int at = -1, ok = 1;  //@jump
                                for (const char* w = words[k]; *w && ok; w++) {  //@jump
                                    int lo = start[*w - 'a'], hi = start[*w - 'a' + 1], end = hi;  //@jump
                                    while (lo < hi) { int mid = (lo + hi) / 2; if (pos[mid] <= at) lo = mid + 1; else hi = mid; }  //@jump
                                    if (lo == end) ok = 0; else at = pos[lo];  //@jump
                                }
                                count += ok;  //@each
                            }
                            free(pos);  //@ret
                            return count;  //@ret
                        }
                    """,
                },
                lines=[("index", "Every letter's positions in the text, increasing.", {"c": "One array holds all positions grouped by letter; `start[c]..start[c+1]` is letter `c`'s slice (a counting-sort layout)."}), ("init", "Hidden words found."), ("each", "Each word."), ("jump", "The next needed letter's first position after the last match; if there's none, the word isn't hidden."), ("ret", "Total.")],
                complexity=["**Time O(T + L log T)** with L the total length of all words. **Space O(T)** for the positions."],
                limits=["Each letter still costs a binary search. Reading the text once while all words wait for their next letter costs O(1) per letter."],
            ),
            approach(
                "One pass with waiting buckets",
                "best",
                "O(T + L)",
                "O(W)",
                idea=["26 buckets of (word, position) pairs, one per needed letter. Start each word in its first letter's bucket. For each text letter `c`, take out bucket `c`; each word advances one letter and either finishes (count it) or joins the bucket of its next letter."],
                walk=w3,
                build=["Buckets keyed by the next needed letter.", "Detach the current letter's bucket before processing it.", "Advance, count or re-bucket."],
                code={
                    "python": """
                        class Solution:
                            def countHidden(self, text: str, words: List[str]) -> int:
                                waiting = [[] for _ in range(26)]  #@init
                                for w in words:  #@init
                                    waiting[ord(w[0]) - 97].append((w, 0))  #@init
                                done = 0  #@init
                                for c in text:  #@read
                                    k = ord(c) - 97  #@read
                                    bucket, waiting[k] = waiting[k], []  #@read
                                    for w, i in bucket:  #@advance
                                        i += 1  #@advance
                                        if i == len(w):  #@advance
                                            done += 1  #@advance
                                        else:  #@advance
                                            waiting[ord(w[i]) - 97].append((w, i))  #@advance
                                return done  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countHidden(String text, String[] words) {
                                int W = words.length;  //@init
                                int[] head = new int[26], next = new int[W], at = new int[W];  //@init
                                Arrays.fill(head, -1);  //@init
                                for (int k = 0; k < W; k++) { int c = words[k].charAt(0) - 'a'; next[k] = head[c]; head[c] = k; }  //@init
                                int done = 0;  //@init
                                for (int t = 0; t < text.length(); t++) {  //@read
                                    int c = text.charAt(t) - 'a';  //@read
                                    int k = head[c];  //@read
                                    head[c] = -1;  //@read
                                    while (k != -1) {  //@advance
                                        int after = next[k];  //@advance
                                        if (++at[k] == words[k].length()) done++;  //@advance
                                        else { int d = words[k].charAt(at[k]) - 'a'; next[k] = head[d]; head[d] = k; }  //@advance
                                        k = after;  //@advance
                                    }
                                }
                                return done;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countHidden(string& text, vector<string>& words) {
                                vector<vector<pair<int, int>>> waiting(26);  //@init
                                for (int k = 0; k < (int) words.size(); k++) waiting[words[k][0] - 'a'].push_back({k, 0});  //@init
                                int done = 0;  //@init
                                for (char c : text) {  //@read
                                    vector<pair<int, int>> bucket;  //@read
                                    swap(bucket, waiting[c - 'a']);  //@read
                                    for (auto [k, i] : bucket) {  //@advance
                                        i++;  //@advance
                                        if (i == (int) words[k].size()) done++;  //@advance
                                        else waiting[words[k][i] - 'a'].push_back({k, i});  //@advance
                                    }
                                }
                                return done;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countHidden(char* text, char** words, int wordsSize) {
                            int head[26];  //@init
                            int* next = malloc((wordsSize + 1) * sizeof(int));  //@init
                            int* at = calloc(wordsSize + 1, sizeof(int));  //@init
                            for (int c = 0; c < 26; c++) head[c] = -1;  //@init
                            for (int k = 0; k < wordsSize; k++) { int c = words[k][0] - 'a'; next[k] = head[c]; head[c] = k; }  //@init
                            int done = 0;  //@init
                            for (int t = 0; text[t]; t++) {  //@read
                                int c = text[t] - 'a';  //@read
                                int k = head[c];  //@read
                                head[c] = -1;  //@read
                                while (k != -1) {  //@advance
                                    int after = next[k];  //@advance
                                    char want = words[k][++at[k]];  //@advance
                                    if (!want) done++;  //@advance
                                    else { int d = want - 'a'; next[k] = head[d]; head[d] = k; }  //@advance
                                    k = after;  //@advance
                                }
                            }
                            free(next); free(at);  //@ret
                            return done;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Each word waits for its first letter.", {"java": "Buckets as linked lists in arrays: `head[c]` is the first waiting word, `next[k]` the one after word k, `at[k]` how many letters word k has matched.", "c": "Buckets as linked lists in arrays: `head[c]` is the first waiting word, `next[k]` the one after word k, `at[k]` how many letters word k has matched."}),
                    ("read", "Detach the bucket for this letter first, so words that need the same letter again wait for its **next** occurrence."),
                    ("advance", "Each waiting word matches this letter: it either finishes (count it) or joins the bucket of its next needed letter."),
                    ("ret", "Words that finished."),
                ],
                complexity=["**Time O(T + L):** each text letter is read once and each word letter is matched once. **Space O(W)** for the buckets."],
            ),
        ],
        takeaways=[
            """
            - **Many subsequence queries against one text:** advance all words in parallel, bucketed by their next letter.
            - Alternative: per-letter position lists with binary search (also good for online queries).
            - Detach a bucket before processing it, so a word can't match the same text letter twice.
            """
        ],
    )


@problem
def longest_word_by_deleting():
    text, dictionary = "brazenpanda", ["band", "zebra", "bread", "brand", "apple", "zap"]
    can = [w_ for w_ in dictionary if hidden(w_, text)]
    want = min(can, key=lambda w_: (-len(w_), w_)) if can else ""

    w1 = Steps("Sort the dictionary by length (longest first), then alphabetically, and return the first word hidden in the text.")
    order = sorted(dictionary, key=lambda w_: (-len(w_), w_))
    w1.step(f"Candidate order: {order}.", Row(order))
    for w_ in order:
        ok = hidden(w_, text)
        w1.step(f"'{w_}': {'hidden, so this is the answer' if ok else 'not hidden'}.", Row(order, st={order.index(w_): 'found' if ok else 'mark'}))
        if ok:
            break
    w1.step(f"Answer: '{want}'.", result=want)

    w2 = Steps("One pass over the dictionary, keeping the best word so far. Only run the subsequence check on words that would beat it.")
    best = ""
    for w_ in dictionary:
        better = len(w_) > len(best) or (len(w_) == len(best) and w_ < best)
        if better and hidden(w_, text):
            best = w_
            w2.step(f"'{w_}' would win and is hidden: new best.", Row(dictionary, st={dictionary.index(w_): "found"}), Vars(best=best))
        else:
            w2.step(f"'{w_}': " + ("can't beat the best, so no check needed." if not better else "would win, but isn't hidden."), Row(dictionary, st={dictionary.index(w_): "mark"}), Vars(best=best or "''"))
    w2.step(f"Answer: '{best}'.", result=best)

    sol(
        "longest-word-by-deleting",
        summary="""
            A word can be made by deleting letters exactly when it's a subsequence of `text`. Go through the dictionary
            keeping the best word so far (longest, then alphabetically first); run the two-pointer subsequence check only
            for words that would beat it. O(D · T) in the worst case, often much less.
        """,
        question=[
            """
            Return the longest dictionary word that is a subsequence of `text`; ties go to the alphabetically first; if none,
            `""`.

            - **Up to 1000 words of length ≤ 1000** and text of length ≤ 1000.
            - Deleting letters = keeping some letters in order = subsequence.
            """
        ],
        think=[
            f"""
            Text `"{text}"`. Hidden words: {can}. The longest are five letters; alphabetically, **"{want}"** comes first.

            The test for each word is the two-pointer subsequence check. The only question is the order of checks: either
            sort candidates by the preference and stop at the first success, or scan once and skip words that can't win.
            """,
            fig(Row(list(text), label="text")),
        ],
        approaches=[
            approach(
                "Sort by preference, take the first hidden word",
                "better",
                "O(D log D · L + D · T)",
                "O(D)",
                idea=["Sort the words by (−length, word). Return the first one that is a subsequence of the text."],
                walk=w1,
                build=["Sort with the preference key.", "Check each in order.", "Return the first success, or \"\"."],
                code={
                    "python": """
                        class Solution:
                            def longestByDeleting(self, text: str, dictionary: List[str]) -> str:
                                def hidden(w):  #@check
                                    i = 0  #@check
                                    for c in text:  #@check
                                        if i < len(w) and c == w[i]:  #@check
                                            i += 1  #@check
                                    return i == len(w)  #@check
                                for w in sorted(dictionary, key=lambda w: (-len(w), w)):  #@order
                                    if hidden(w):  #@first
                                        return w  #@first
                                return ""  #@ret
                    """,
                    "java": """
                        class Solution {
                            private boolean hidden(String w, String text) {  //@check
                                int i = 0;  //@check
                                for (int t = 0; t < text.length() && i < w.length(); t++) if (text.charAt(t) == w.charAt(i)) i++;  //@check
                                return i == w.length();  //@check
                            }  //@check

                            public String longestByDeleting(String text, String[] dictionary) {
                                String[] order = dictionary.clone();  //@order
                                Arrays.sort(order, (a, b) -> a.length() != b.length() ? b.length() - a.length() : a.compareTo(b));  //@order
                                for (String w : order) if (hidden(w, text)) return w;  //@first
                                return "";  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static bool hidden(const string& w, const string& text) {  //@check
                                size_t i = 0;  //@check
                                for (size_t t = 0; t < text.size() && i < w.size(); t++) if (text[t] == w[i]) i++;  //@check
                                return i == w.size();  //@check
                            }  //@check

                        public:
                            string longestByDeleting(string& text, vector<string>& dictionary) {
                                vector<string> order = dictionary;  //@order
                                sort(order.begin(), order.end(), [](const string& a, const string& b) { return a.size() != b.size() ? a.size() > b.size() : a < b; });  //@order
                                for (auto& w : order) if (hidden(w, text)) return w;  //@first
                                return "";  //@ret
                            }
                        };
                    """,
                    "c": """
                        static bool hidden(const char* w, const char* text) {  //@check
                            for (; *text && *w; text++) if (*text == *w) w++;  //@check
                            return *w == '\\0';  //@check
                        }  //@check

                        static int prefer(const void* x, const void* y) {  //@order
                            const char *a = *(char* const*) x, *b = *(char* const*) y;  //@order
                            size_t la = strlen(a), lb = strlen(b);  //@order
                            return la != lb ? (lb > la) - (lb < la) : strcmp(a, b);  //@order
                        }  //@order

                        char* longestByDeleting(char* text, char** dictionary, int dictionarySize) {
                            char** order = malloc(dictionarySize * sizeof(char*));  //@order
                            memcpy(order, dictionary, dictionarySize * sizeof(char*));  //@order
                            qsort(order, dictionarySize, sizeof(char*), prefer);  //@order
                            const char* best = "";  //@first
                            for (int k = 0; k < dictionarySize; k++) if (hidden(order[k], text)) { best = order[k]; break; }  //@first
                            free(order);  //@ret
                            char* out = malloc(strlen(best) + 1);  //@ret
                            strcpy(out, best);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("check", "Greedy two-pointer subsequence test."), ("order", "Longest first; equal lengths alphabetically.", {"c": "Sort an array of pointers; the strings stay put."}), ("first", "The first hidden word in preference order is the answer."), ("ret", "None hidden: the empty string.", {"c": "Return a fresh copy, as the caller frees it."})],
                complexity=["**Time O(D log D · L)** for sorting with string comparisons, plus **O(D · T)** checks in the worst case. **Space O(D)** for the order."],
                limits=["The sort costs extra string comparisons, and words are reordered just to stop early. A single pass that skips words unable to beat the current best gets the same early cut-offs without sorting."],
            ),
            approach(
                "One pass, check only possible winners",
                "best",
                "O(D · T)",
                "O(1)",
                idea=["Keep `best = \"\"`. For each word, if it's longer than `best` or the same length and alphabetically smaller, run the subsequence check; on success it becomes `best`."],
                walk=w2,
                build=["`best` starts empty.", "Skip words that can't win.", "Check the rest."],
                code={
                    "python": """
                        class Solution:
                            def longestByDeleting(self, text: str, dictionary: List[str]) -> str:
                                def hidden(w):  #@check
                                    i = 0  #@check
                                    for c in text:  #@check
                                        if i < len(w) and c == w[i]:  #@check
                                            i += 1  #@check
                                    return i == len(w)  #@check
                                best = ""  #@init
                                for w in dictionary:  #@each
                                    wins = len(w) > len(best) or (len(w) == len(best) and w < best)  #@wins
                                    if wins and hidden(w):  #@wins
                                        best = w  #@wins
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            private boolean hidden(String w, String text) {  //@check
                                int i = 0;  //@check
                                for (int t = 0; t < text.length() && i < w.length(); t++) if (text.charAt(t) == w.charAt(i)) i++;  //@check
                                return i == w.length();  //@check
                            }  //@check

                            public String longestByDeleting(String text, String[] dictionary) {
                                String best = "";  //@init
                                for (String w : dictionary) {  //@each
                                    boolean wins = w.length() > best.length() || (w.length() == best.length() && w.compareTo(best) < 0);  //@wins
                                    if (wins && hidden(w, text)) best = w;  //@wins
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static bool hidden(const string& w, const string& text) {  //@check
                                size_t i = 0;  //@check
                                for (size_t t = 0; t < text.size() && i < w.size(); t++) if (text[t] == w[i]) i++;  //@check
                                return i == w.size();  //@check
                            }  //@check

                        public:
                            string longestByDeleting(string& text, vector<string>& dictionary) {
                                string best;  //@init
                                for (auto& w : dictionary) {  //@each
                                    bool wins = w.size() > best.size() || (w.size() == best.size() && w < best);  //@wins
                                    if (wins && hidden(w, text)) best = w;  //@wins
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static bool hidden(const char* w, const char* text) {  //@check
                            for (; *text && *w; text++) if (*text == *w) w++;  //@check
                            return *w == '\\0';  //@check
                        }  //@check

                        char* longestByDeleting(char* text, char** dictionary, int dictionarySize) {
                            const char* best = "";  //@init
                            size_t bestLen = 0;  //@init
                            for (int k = 0; k < dictionarySize; k++) {  //@each
                                size_t len = strlen(dictionary[k]);  //@wins
                                int wins = len > bestLen || (len == bestLen && strcmp(dictionary[k], best) < 0);  //@wins
                                if (wins && hidden(dictionary[k], text)) { best = dictionary[k]; bestLen = len; }  //@wins
                            }
                            char* out = malloc(bestLen + 1);  //@ret
                            strcpy(out, best);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("check", "Greedy two-pointer subsequence test."), ("init", "No word found yet."), ("each", "Each dictionary word once."), ("wins", "Only a word that would beat the current best needs the (costly) check."), ("ret", "The best word, or \"\".", {"c": "Return a fresh copy, as the caller frees it."})],
                complexity=["**Time O(D · T)** in the worst case (every word checked), often less. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **"Formed by deleting letters" = subsequence**, checked with two pointers.
            - Prune: only test candidates that could improve the answer.
            - Spell out the tie-break (length, then alphabetical) and apply it consistently.
            """
        ],
    )
