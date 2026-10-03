"""Sorting: counting and bucket ideas."""
import textwrap
from collections import Counter

from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

C_CMP = textwrap.indent("""
static int cmp_int(const void* x, const void* y) {  //@sort
    int a = *(const int*) x, b = *(const int*) y;  //@sort
    return (a > b) - (a < b);  //@sort
}  //@sort
""", " " * 24)


@problem
def sort_the_grades():
    grades = [72, 95, 72, 40, 95, 88, 72]
    want = sorted(grades)

    w = Steps("Counting sort: one tally per possible grade (0–100), then write each grade out as many times as it was counted.")
    count = Counter(grades)
    w.step("Tally every grade.", Row(grades, label="grades"), Row([f"{g}×{c}" for g, c in sorted(count.items())], label="grade × count"))
    out = []
    for g in sorted(count):
        out += [g] * count[g]
        w.step(f"Grade {g} was counted {count[g]} time(s): write it {count[g]} time(s).", Row(out, st={len(out) - 1 - i: "new" for i in range(count[g])}, label="output"))
    w.step(f"Sorted: {out}.", result=str(out))

    sol(
        "sort-the-grades",
        summary="""
            Grades only take 101 values, so count how many times each grade appears, then write grades 0 to 100 out in
            order, each as many times as counted. That's counting sort: O(n + 101) time, no comparisons.
        """,
        question=[
            """
            Sort up to 10⁵ grades, each between 0 and 100, in **O(n) time**.

            - **Many repeats:** 10⁵ grades but only 101 possible values.
            - O(n) rules out comparison sorts, which need O(n log n) in general.
            """
        ],
        think=[
            f"""
            Grades `{grades}`. We don't need to compare grades at all: we know every possible value in advance (0 to 100).
            Count each one, then read the counts in order. Sorted: `{want}`.
            """,
            fig(Row(grades, label="grades"), Row(want, label="sorted")),
        ],
        approaches=[
            approach(
                "Comparison sort",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Sort a copy with the language's sort."],
                build=["Copy and sort."],
                code={
                    "python": """
                        class Solution:
                            def sortGrades(self, grades: List[int]) -> List[int]:
                                return sorted(grades)  #@sort
                    """,
                    "java": """
                        class Solution {
                            public int[] sortGrades(int[] grades) {
                                int[] a = grades.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                return a;  //@sort
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortGrades(vector<int>& grades) {
                                vector<int> a = grades;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                return a;  //@sort
                            }
                        };
                    """,
                    "c": C_CMP + """
                        int* sortGrades(int* grades, int gradesSize, int* returnSize) {
                            int* a = malloc(gradesSize * sizeof(int));  //@sort
                            memcpy(a, grades, gradesSize * sizeof(int));  //@sort
                            qsort(a, gradesSize, sizeof(int), cmp_int);  //@sort
                            *returnSize = gradesSize;  //@sort
                            return a;  //@sort
                        }
                    """,
                },
                lines=[("sort", "A general O(n log n) sort.")],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Doesn't meet the O(n) requirement, and compares values even though only 101 different ones exist. Counting them skips comparisons entirely."],
            ),
            approach(
                "Counting sort",
                "best",
                "O(n + R)",
                "O(R)",
                idea=["An array of 101 counters. One pass counts each grade; a second pass over grades 0..100 writes each grade `count[g]` times."],
                walk=w,
                build=["`count = [0] * 101`.", "Count every grade.", "For `g` from 0 to 100, append `g` `count[g]` times."],
                code={
                    "python": """
                        class Solution:
                            def sortGrades(self, grades: List[int]) -> List[int]:
                                count = [0] * 101  #@count
                                for g in grades:  #@count
                                    count[g] += 1  #@count
                                out = []  #@write
                                for g in range(101):  #@write
                                    out.extend([g] * count[g])  #@write
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] sortGrades(int[] grades) {
                                int[] count = new int[101];  //@count
                                for (int g : grades) count[g]++;  //@count
                                int[] out = new int[grades.length];  //@write
                                int w = 0;  //@write
                                for (int g = 0; g <= 100; g++)  //@write
                                    for (int c = 0; c < count[g]; c++) out[w++] = g;  //@write
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortGrades(vector<int>& grades) {
                                int count[101] = {0};  //@count
                                for (int g : grades) count[g]++;  //@count
                                vector<int> out;  //@write
                                for (int g = 0; g <= 100; g++) out.insert(out.end(), count[g], g);  //@write
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* sortGrades(int* grades, int gradesSize, int* returnSize) {
                            int count[101] = {0};  //@count
                            for (int i = 0; i < gradesSize; i++) count[grades[i]]++;  //@count
                            int* out = malloc(gradesSize * sizeof(int));  //@write
                            int w = 0;  //@write
                            for (int g = 0; g <= 100; g++)  //@write
                                for (int c = 0; c < count[g]; c++) out[w++] = g;  //@write
                            *returnSize = gradesSize;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("count", "One counter per possible grade; the grade itself is the index."), ("write", "Read the counters in increasing grade order, writing each grade as often as it appeared."), ("ret", "Sorted, without a single comparison between grades.")],
                complexity=["**Time O(n + R)** with R = 101 possible grades. **Space O(R)** for the counters (plus the output)."],
            ),
        ],
        takeaways=[
            """
            - **Small range of values → counting sort**, O(n + range).
            - Comparison sorts can't beat O(n log n) in general; counting sidesteps comparisons by using the values as
              indexes.
            - It only pays off when the range is small compared with n (here 101 vs 10⁵).
            """
        ],
    )


@problem
def most_played_songs():
    plays, k = [7, 3, 7, 9, 3, 7, 12, 9, 3, 1], 3
    count = Counter(plays)
    ranked = sorted(count, key=lambda s: (-count[s], s))
    want = ranked[:k]

    w1 = Steps("For each different song, scan the whole log to count its plays; then pick the top k.")
    for s in sorted(count):
        w1.step(f"Song {s}: scan all {len(plays)} plays, count {count[s]}.", Row(plays, st={i: "found" for i, p in enumerate(plays) if p == s}))
    w1.step(f"Ranked by plays (ties by smaller id): {ranked}. Top {k}: {want}.", result=str(want))

    w2 = Steps("One pass with a hash map counts every song. Then sort only the different songs by (more plays first, smaller id first).")
    w2.step("Count in one pass.", Row(plays, label="plays"), Row([f"{s}×{count[s]}" for s in sorted(count)], label="song × plays"))
    w2.step(f"Sort the {len(count)} songs by plays descending, then id: {ranked}.", Row(ranked, st={i: "found" for i in range(k)}, label="ranked"))
    w2.step(f"Take the first {k}.", result=str(want))

    sol(
        "most-played-songs",
        summary="""
            Count plays per song with a hash map in one pass, then sort the **different** songs by play count (descending)
            and id (ascending) and take the first k. O(n + d log d) for d different songs.
        """,
        question=[
            """
            `plays` lists song ids, one per play. Return the `k` most-played songs, most played first; ties go to the
            smaller id.

            - **Ids reach 10⁹**, so they can't index an array directly.
            - **Up to 10⁵ plays**; the number of different songs `d` can be anything up to that.
            """
        ],
        think=[
            f"""
            Plays `{plays}`, `k = {k}`. Song 7 and song 3 were each played 3 times (3 has the smaller id, so it comes first),
            and song 9 twice. Answer: `{want}`.

            Two steps: **count** (a hash map from song to plays) and **rank** (sort the songs by the rule). Only the
            different songs need sorting, not every play.
            """,
            table(["song", "plays"], *[(s, count[s]) for s in ranked]),
        ],
        approaches=[
            approach(
                "Rescan the log for each song",
                "brute",
                "O(n·d)",
                "O(d)",
                idea=["Collect the different song ids, count each one by scanning the whole log, then sort the songs by (count descending, id) and take k."],
                walk=w1,
                build=["Distinct ids (a set).", "For each, count its occurrences with a full scan.", "Sort and slice."],
                code={
                    "python": """
                        class Solution:
                            def mostPlayed(self, plays: List[int], k: int) -> List[int]:
                                songs = set(plays)  #@distinct
                                counts = {s: sum(1 for p in plays if p == s) for s in songs}  #@count
                                ranked = sorted(songs, key=lambda s: (-counts[s], s))  #@rank
                                return ranked[:k]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] mostPlayed(int[] plays, int k) {
                                Set<Integer> songs = new HashSet<>();  //@distinct
                                for (int p : plays) songs.add(p);  //@distinct
                                Map<Integer, Integer> counts = new HashMap<>();  //@count
                                for (int s : songs) {  //@count
                                    int c = 0;  //@count
                                    for (int p : plays) if (p == s) c++;  //@count
                                    counts.put(s, c);  //@count
                                }
                                List<Integer> ranked = new ArrayList<>(songs);  //@rank
                                ranked.sort((a, b) -> !counts.get(a).equals(counts.get(b)) ? counts.get(b) - counts.get(a) : Integer.compare(a, b));  //@rank
                                int[] out = new int[k];  //@ret
                                for (int i = 0; i < k; i++) out[i] = ranked.get(i);  //@ret
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> mostPlayed(vector<int>& plays, int k) {
                                set<int> distinct(plays.begin(), plays.end());  //@distinct
                                vector<pair<int, int>> ranked;  //@count
                                for (int s : distinct) ranked.push_back({-(int) count(plays.begin(), plays.end(), s), s});  //@count
                                sort(ranked.begin(), ranked.end());  //@rank
                                vector<int> out;  //@ret
                                for (int i = 0; i < k; i++) out.push_back(ranked[i].second);  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int song, plays; } Pair;

                        static int by_rank(const void* x, const void* y) {  //@rank
                            const Pair *a = x, *b = y;  //@rank
                            if (a->plays != b->plays) return b->plays - a->plays;  //@rank
                            return (a->song > b->song) - (a->song < b->song);  //@rank
                        }  //@rank

                        int* mostPlayed(int* plays, int playsSize, int k, int* returnSize) {
                            Pair* songs = malloc(playsSize * sizeof(Pair));  //@distinct
                            int d = 0;  //@distinct
                            for (int i = 0; i < playsSize; i++) {  //@distinct
                                int seen = 0;  //@distinct
                                for (int j = 0; j < d && !seen; j++) seen = songs[j].song == plays[i];  //@distinct
                                if (!seen) songs[d++] = (Pair){plays[i], 0};  //@distinct
                            }
                            for (int j = 0; j < d; j++)  //@count
                                for (int i = 0; i < playsSize; i++) songs[j].plays += plays[i] == songs[j].song;  //@count
                            qsort(songs, d, sizeof(Pair), by_rank);  //@rank
                            int* out = malloc(k * sizeof(int));  //@ret
                            for (int i = 0; i < k; i++) out[i] = songs[i].song;  //@ret
                            free(songs);  //@ret
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("distinct", "The different song ids.", {"c": "Without a hash set, finding distinct ids is itself a quadratic scan."}), ("count", "Count each song with a full pass over the log."), ("rank", "More plays first; equal plays by smaller id."), ("ret", "The first k.")],
                complexity=["**Time O(n·d):** one full scan per different song, up to 10¹⁰ steps. **Space O(d).**"],
                limits=["Rescanning the log for every song is wasteful: a single pass can count every song at once if a hash map holds the running counts."],
                slow=True,
            ),
            approach(
                "Hash-map counts, sort the distinct songs",
                "best",
                "O(n + d log d)",
                "O(d)",
                idea=["One pass: `count[song] += 1`. Then sort the distinct songs by `(-count, id)` and return the first k."],
                walk=w2,
                build=["Count with a hash map.", "Sort the keys by the ranking rule.", "Take k."],
                code={
                    "python": """
                        from collections import Counter

                        class Solution:
                            def mostPlayed(self, plays: List[int], k: int) -> List[int]:
                                count = Counter(plays)  #@count
                                ranked = sorted(count, key=lambda s: (-count[s], s))  #@rank
                                return ranked[:k]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] mostPlayed(int[] plays, int k) {
                                Map<Integer, Integer> count = new HashMap<>();  //@count
                                for (int p : plays) count.merge(p, 1, Integer::sum);  //@count
                                List<Integer> ranked = new ArrayList<>(count.keySet());  //@rank
                                ranked.sort((a, b) -> !count.get(a).equals(count.get(b)) ? count.get(b) - count.get(a) : Integer.compare(a, b));  //@rank
                                int[] out = new int[k];  //@ret
                                for (int i = 0; i < k; i++) out[i] = ranked.get(i);  //@ret
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> mostPlayed(vector<int>& plays, int k) {
                                unordered_map<int, int> count;  //@count
                                for (int p : plays) count[p]++;  //@count
                                vector<pair<int, int>> ranked;  //@rank
                                for (auto& [song, c] : count) ranked.push_back({-c, song});  //@rank
                                sort(ranked.begin(), ranked.end());  //@rank
                                vector<int> out;  //@ret
                                for (int i = 0; i < k; i++) out.push_back(ranked[i].second);  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int song, plays; } Pair;

                        static int by_rank(const void* x, const void* y) {  //@rank
                            const Pair *a = x, *b = y;  //@rank
                            if (a->plays != b->plays) return b->plays - a->plays;  //@rank
                            return (a->song > b->song) - (a->song < b->song);  //@rank
                        }  //@rank

                        int* mostPlayed(int* plays, int playsSize, int k, int* returnSize) {
                            int cap = 1;  //@table
                            while (cap < 2 * playsSize) cap <<= 1;  //@table
                            int* keys = malloc(cap * sizeof(int));  //@table
                            int* hits = calloc(cap, sizeof(int));  //@table
                            for (int i = 0; i < playsSize; i++) {  //@count
                                unsigned h = (unsigned) plays[i] * 2654435761u & (cap - 1);  //@count
                                while (hits[h] && keys[h] != plays[i]) h = (h + 1) & (cap - 1);  //@count
                                keys[h] = plays[i];  //@count
                                hits[h]++;  //@count
                            }
                            Pair* songs = malloc(playsSize * sizeof(Pair));  //@rank
                            int d = 0;  //@rank
                            for (int h = 0; h < cap; h++) if (hits[h]) songs[d++] = (Pair){keys[h], hits[h]};  //@rank
                            qsort(songs, d, sizeof(Pair), by_rank);  //@rank
                            int* out = malloc(k * sizeof(int));  //@ret
                            for (int i = 0; i < k; i++) out[i] = songs[i].song;  //@ret
                            free(keys); free(hits); free(songs);  //@ret
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("table", "C has no hash map: an open-addressing table, at least twice the number of plays, so it stays at most half full.", {}),
                    ("count", "One pass: each play adds 1 to its song's counter.", {"c": "Hash the id, then step forward past slots holding other songs until finding this song's slot or an empty one."}),
                    ("rank", "Sort only the d different songs: more plays first, then smaller id."),
                    ("ret", "The first k."),
                ],
                complexity=["**Time O(n + d log d).** **Space O(d)** for the counts."],
            ),
        ],
        takeaways=[
            """
            - **Top-k by frequency = count (hash map) + rank.** Sort the distinct keys, or keep a size-k heap for
              O(d log k).
            - Bucket by count (an array indexed by frequency) is another linear-ish way to rank, since counts are at most n.
            - Make tie-breaking explicit: here, smaller id first.
            """
        ],
    )


@problem
def widest_gap_after_sorting():
    nums = [13, 2, 27, 8, 31, 20]
    s = sorted(nums)
    want = max(b - a for a, b in zip(s, s[1:]))
    lo, hi, n = min(nums), max(nums), len(nums)
    size = max(1, (hi - lo) // (n - 1))
    count = (hi - lo) // size + 1
    buckets = [[] for _ in range(count)]
    for x in nums:
        buckets[(x - lo) // size].append(x)

    w1 = Steps("Sort, then check every pair of neighbours.")
    w1.step(f"Sorted: {s}.", Row(s))
    gaps = [b - a for a, b in zip(s, s[1:])]
    w1.step(f"Neighbour gaps: {gaps}. The widest is {want}.", Row(s), Row(gaps, label="gaps"), result=want)

    w2 = Steps(f"Buckets of width {size} between min {lo} and max {hi}. With n values over that range, the widest gap is at least the average gap, so it never falls inside a bucket: only between one bucket's max and the next non-empty bucket's min.")
    w2.step(f"Average gap ≥ ({hi} − {lo}) / {n - 1} = {(hi - lo) / (n - 1):.1f}, so buckets of width {size} are enough.", Row(nums, label="nums"))
    w2.step("Drop each value into its bucket, keeping only each bucket's min and max.", Row([f"{min(b)}–{max(b)}" if b else "·" for b in buckets], label="buckets (min–max)"))
    best, prev = 0, lo
    for i, b in enumerate(buckets):
        if b:
            gap = min(b) - prev
            best = max(best, gap)
            w2.step(f"Bucket {i}: its min {min(b)} minus the previous max {prev} = {gap}. Best so far {best}.", Row([f"{min(x)}–{max(x)}" if x else "·" for x in buckets], st={i: "active"}, label="buckets"), Vars(best=best))
            prev = max(b)
    w2.step(f"Widest gap: {best}.", result=best)

    sol(
        "widest-gap-after-sorting",
        summary="""
            Pigeonhole: n numbers between `min` and `max` have an average neighbour gap of `(max − min) / (n − 1)`, so the
            widest gap is at least that. Use buckets narrower than that: no two values in one bucket can form the widest
            gap, so only compare each non-empty bucket's minimum with the previous bucket's maximum. O(n).
        """,
        question=[
            """
            Return the largest difference between neighbours in the sorted version of `nums`, or 0 with fewer than two
            numbers, in **O(n) time**.

            - **Values reach 10⁹**, so counting sort over the value range is out.
            - **Duplicates** are allowed (a gap of 0).
            """
        ],
        think=[
            f"""
            `{nums}` sorted is `{s}`; the gaps are `{gaps}`, so the answer is **{want}**.

            Sorting costs O(n log n). To avoid it, ask what the widest gap must be at least: the n − 1 gaps add up to
            `max − min = {hi - lo}`, so the widest is at least their average, {(hi - lo) / (n - 1):.1f}. If every bucket is
            narrower than that average, two values in the same bucket are closer than the widest gap, so the widest gap
            always jumps between buckets: from one non-empty bucket's max to the next one's min.
            """,
            fig(Row(s, label="sorted"), Row(gaps, label="gaps")),
        ],
        approaches=[
            approach(
                "Sort and scan",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Sort, then take the maximum difference between consecutive values."],
                walk=w1,
                build=["Fewer than 2 values → 0.", "Sort a copy.", "Max of `a[i] − a[i−1]`."],
                code={
                    "python": """
                        class Solution:
                            def widestGap(self, nums: List[int]) -> int:
                                a = sorted(nums)  #@sort
                                return max((a[i] - a[i - 1] for i in range(1, len(a))), default=0)  #@scan
                    """,
                    "java": """
                        class Solution {
                            public int widestGap(int[] nums) {
                                int[] a = nums.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                int best = 0;  //@scan
                                for (int i = 1; i < a.length; i++) best = Math.max(best, a[i] - a[i - 1]);  //@scan
                                return best;  //@scan
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int widestGap(vector<int>& nums) {
                                vector<int> a = nums;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                int best = 0;  //@scan
                                for (size_t i = 1; i < a.size(); i++) best = max(best, a[i] - a[i - 1]);  //@scan
                                return best;  //@scan
                            }
                        };
                    """,
                    "c": C_CMP + """
                        int widestGap(int* nums, int numsSize) {
                            int* a = malloc(numsSize * sizeof(int));  //@sort
                            memcpy(a, nums, numsSize * sizeof(int));  //@sort
                            qsort(a, numsSize, sizeof(int), cmp_int);  //@sort
                            int best = 0;  //@scan
                            for (int i = 1; i < numsSize; i++) if (a[i] - a[i - 1] > best) best = a[i] - a[i - 1];  //@scan
                            free(a);  //@scan
                            return best;  //@scan
                        }
                    """,
                },
                lines=[("sort", "Sort a copy."), ("scan", "The widest neighbour difference (0 for a single value).")],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Misses the O(n) requirement. We never need the full order, only the gaps between buckets of values."],
            ),
            approach(
                "Buckets narrower than the average gap",
                "best",
                "O(n)",
                "O(n)",
                idea=["With `lo`, `hi` and `n`: bucket width `size = max(1, (hi − lo) / (n − 1))` (whole-number division), `(hi − lo) / size + 1` buckets. Put each value in bucket `(x − lo) / size`, tracking only each bucket's min and max. Walk the buckets in order: the answer is the largest `bucket min − previous bucket max`."],
                walk=w2,
                build=["Handle n < 2 or all-equal → 0.", "Compute the bucket width and count.", "Track min/max per bucket.", "Scan non-empty buckets, comparing with the previous max."],
                code={
                    "python": """
                        class Solution:
                            def widestGap(self, nums: List[int]) -> int:
                                n, lo, hi = len(nums), min(nums), max(nums)  #@range
                                if n < 2 or lo == hi:  #@range
                                    return 0  #@range
                                size = max(1, (hi - lo) // (n - 1))  #@size
                                count = (hi - lo) // size + 1  #@size
                                bmin, bmax = [None] * count, [None] * count  #@fill
                                for x in nums:  #@fill
                                    b = (x - lo) // size  #@fill
                                    bmin[b] = x if bmin[b] is None else min(bmin[b], x)  #@fill
                                    bmax[b] = x if bmax[b] is None else max(bmax[b], x)  #@fill
                                best, prev = 0, lo  #@scan
                                for b in range(count):  #@scan
                                    if bmin[b] is not None:  #@scan
                                        best = max(best, bmin[b] - prev)  #@scan
                                        prev = bmax[b]  #@scan
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int widestGap(int[] nums) {
                                int n = nums.length, lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;  //@range
                                for (int x : nums) { lo = Math.min(lo, x); hi = Math.max(hi, x); }  //@range
                                if (n < 2 || lo == hi) return 0;  //@range
                                int size = Math.max(1, (hi - lo) / (n - 1));  //@size
                                int count = (hi - lo) / size + 1;  //@size
                                int[] bmin = new int[count], bmax = new int[count];  //@fill
                                boolean[] used = new boolean[count];  //@fill
                                for (int x : nums) {  //@fill
                                    int b = (x - lo) / size;  //@fill
                                    if (!used[b]) { used[b] = true; bmin[b] = x; bmax[b] = x; }  //@fill
                                    else { bmin[b] = Math.min(bmin[b], x); bmax[b] = Math.max(bmax[b], x); }  //@fill
                                }
                                int best = 0, prev = lo;  //@scan
                                for (int b = 0; b < count; b++) if (used[b]) { best = Math.max(best, bmin[b] - prev); prev = bmax[b]; }  //@scan
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int widestGap(vector<int>& nums) {
                                int n = nums.size();  //@range
                                int lo = *min_element(nums.begin(), nums.end()), hi = *max_element(nums.begin(), nums.end());  //@range
                                if (n < 2 || lo == hi) return 0;  //@range
                                int size = max(1, (hi - lo) / (n - 1));  //@size
                                int count = (hi - lo) / size + 1;  //@size
                                vector<int> bmin(count, INT_MAX), bmax(count, INT_MIN);  //@fill
                                for (int x : nums) {  //@fill
                                    int b = (x - lo) / size;  //@fill
                                    bmin[b] = min(bmin[b], x);  //@fill
                                    bmax[b] = max(bmax[b], x);  //@fill
                                }
                                int best = 0, prev = lo;  //@scan
                                for (int b = 0; b < count; b++) if (bmin[b] != INT_MAX) { best = max(best, bmin[b] - prev); prev = bmax[b]; }  //@scan
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int widestGap(int* nums, int numsSize) {
                            int n = numsSize, lo = nums[0], hi = nums[0];  //@range
                            for (int i = 1; i < n; i++) { if (nums[i] < lo) lo = nums[i]; if (nums[i] > hi) hi = nums[i]; }  //@range
                            if (n < 2 || lo == hi) return 0;  //@range
                            int size = (hi - lo) / (n - 1);  //@size
                            if (size < 1) size = 1;  //@size
                            int count = (hi - lo) / size + 1;  //@size
                            int* bmin = malloc(count * sizeof(int));  //@fill
                            int* bmax = malloc(count * sizeof(int));  //@fill
                            for (int b = 0; b < count; b++) { bmin[b] = INT_MAX; bmax[b] = INT_MIN; }  //@fill
                            for (int i = 0; i < n; i++) {  //@fill
                                int b = (nums[i] - lo) / size;  //@fill
                                if (nums[i] < bmin[b]) bmin[b] = nums[i];  //@fill
                                if (nums[i] > bmax[b]) bmax[b] = nums[i];  //@fill
                            }
                            int best = 0, prev = lo;  //@scan
                            for (int b = 0; b < count; b++) if (bmin[b] != INT_MAX) { if (bmin[b] - prev > best) best = bmin[b] - prev; prev = bmax[b]; }  //@scan
                            free(bmin); free(bmax);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("range", "The smallest and largest value; no gap exists if there's one value or they're all equal."),
                    ("size", "Bucket width at most the average gap (at least 1), and enough buckets to cover `lo..hi`. There are at most about n buckets."),
                    ("fill", "Each value goes to its bucket; only the bucket's min and max matter."),
                    ("scan", "Within a bucket, values are closer than the average gap, so the widest gap is between a bucket's min and the previous non-empty bucket's max."),
                    ("ret", "The widest gap."),
                ],
                complexity=["**Time O(n):** a pass to fill buckets and a pass over at most ~n buckets. **Space O(n)** for the buckets."],
            ),
        ],
        takeaways=[
            """
            - **Pigeonhole bucketing:** if the answer is at least the average, buckets smaller than the average can't hide
              it.
            - Keep only what you need per bucket (here min and max).
            - When a problem demands O(n) on large values, think buckets or radix rather than comparisons.
            """
        ],
    )
