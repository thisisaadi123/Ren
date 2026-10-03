"""Arrays & Hashing: majority vote."""
from collections import Counter

from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def half_or_more():
    good, bad = [4, 9, 4, 4, 2, 4, 9], [6, 1, 6, 2, 6, 3]
    assert Counter(good)[4] * 2 > len(good) and max(Counter(bad).values()) * 2 <= len(bad)

    w1 = Steps("Count each vote's option with a full scan until one has more than half.")
    for v in (good, bad):
        n = len(v)
        win = None
        for i, x in enumerate(v):
            c = v.count(x)
            if c * 2 > n:
                win = x
                w1.step(f"{v}: option {x} has {c} of {n} votes, more than half.", Row(v, st={j: "answer" for j, y in enumerate(v) if y == x}, slots=True), result=x)
                break
        if win is None:
            best = max(set(v), key=v.count)
            w1.step(f"{v}: every option counted; the most any has is {v.count(best)} of {n}, not more than half.", Row(v, st={j: "mark" for j, y in enumerate(v) if y == best}, slots=True), result=-1)

    w2 = Steps("Count every option in a hash map; check whether the largest count passes n/2.")
    cnt = {}
    for i, x in enumerate(good):
        cnt[x] = cnt.get(x, 0) + 1
        keys = list(cnt)
        w2.step(f"Vote {x}: count {cnt[x]}.", Row(good, st={**{q: "dim" for q in range(i)}, i: "active"}, slots=True), Row([f"{k}:{cnt[k]}" for k in keys], st={keys.index(x): "new"}, label="option:votes"))
    w2.step(f"Option 4 has {cnt[4]} > {len(good)}/2.", Row([f"{k}:{cnt[k]}" for k in cnt], st={list(cnt).index(4): "answer"}, label="option:votes"), result=4)

    w3 = Steps("Voting finds the only possible winner; a second pass checks it really has more than half.")
    for v in (good, bad):
        cand, count = None, 0
        for i, x in enumerate(v):
            if count == 0:
                cand, count = x, 1
                t = f"count 0 → {x} becomes the candidate"
            elif x == cand:
                count += 1
                t = f"{x} supports it → {count}"
            else:
                count -= 1
                t = f"{x} cancels a vote → {count}"
            w3.step(f"{v}, vote {x}: {t}.", Row(v, st={**{q: "dim" for q in range(i)}, i: "active"}, slots=True), Vars(candidate=cand, count=count))
        c = v.count(cand)
        res = cand if c * 2 > len(v) else -1
        w3.step(f"Check: {cand} has {c} of {len(v)} votes → " + ("more than half, it wins." if res != -1 else "not more than half, so −1."), Row(v, st={j: ("answer" if res != -1 else "mark") for j, y in enumerate(v) if y == cand}, slots=True), result=res)

    sol(
        "half-or-more",
        summary="""
            At most one option can have more than half the votes. Boyer–Moore voting finds the only option that
            *could* (pairs of different votes cancel, and a true majority survives), then one counting pass checks
            whether it really does. O(n) time, O(1) space.
        """,
        question=[
            """
            Return the option that received **strictly more than half** of the votes, or −1 if none did.

            - **"More than half" is strict:** in 4 votes, 2 isn't enough; you need 3. `[1, 2, 1, 2]` gives −1.
            - **There may be no winner.** This is the difference from a problem that *promises* a majority: any
              shortcut that guesses a winner must then **verify** it.
            - **At most one winner exists**: two options each with more than half would need more than n votes.
            - **Size:** up to 10⁵ votes, option ids up to 10⁹ (so they can't index an array). The goal is O(1)
              extra space.
            """
        ],
        think=[
            """
            Take `[4, 9, 4, 4, 2, 4, 9]`: option 4 has 4 of 7 votes, a winner. And `[6, 1, 6, 2, 6, 3]`: option 6 has 3
            of 6, exactly half, so no winner.

            Imagine pairing up votes for **different** options and throwing each pair away. A winner has more
            votes than all the others combined, so it can't be paired off completely; something of it always
            survives. But the reverse fails: in `[6, 1, 6, 2, 6, 3]` the cancelling still ends with 6 as the
            survivor, even though 6 has only half the votes, not more.
            """,
            fig(Row([6, 1, 6, 2, 6, 3], st={0: "mark", 2: "mark", 4: "mark"}, slots=True),
                caption="6 survives the cancelling, yet 3 of 6 votes is not more than half. A survivor is only a candidate."),
            """
            So the plan has two steps: **find the candidate** cheaply by cancelling, then **count** it once to see
            whether it truly passes n/2.
            """,
        ],
        approaches=[
            approach(
                "Count each option by scanning",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each vote, count how many votes share its option. The first option whose count is more than n/2 wins; if none is, return −1."],
                walk=w1,
                build=["For each vote `x`, count the votes equal to `x` with a scan.", "If `count × 2 > n`, return `x`.", "After all votes, return −1."],
                code={
                    "python": """
                        class Solution:
                            def strictMajority(self, votes: List[int]) -> int:
                                n = len(votes)
                                for x in votes:  #@each
                                    if votes.count(x) * 2 > n:  #@count
                                        return x  #@count
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int strictMajority(int[] votes) {
                                int n = votes.length;
                                for (int x : votes) {  //@each
                                    int c = 0;  //@count
                                    for (int y : votes) if (y == x) c++;  //@count
                                    if (c * 2 > n) return x;  //@count
                                }
                                return -1;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int strictMajority(vector<int>& votes) {
                                int n = votes.size();
                                for (int x : votes) {  //@each
                                    if (count(votes.begin(), votes.end(), x) * 2 > n) return x;  //@count
                                }
                                return -1;  //@none
                            }
                        };
                    """,
                    "c": """
                        int strictMajority(int* votes, int votesSize) {
                            for (int i = 0; i < votesSize; i++) {  //@each
                                int c = 0;  //@count
                                for (int j = 0; j < votesSize; j++) if (votes[j] == votes[i]) c++;  //@count
                                if (c * 2 > votesSize) return votes[i];  //@count
                            }
                            return -1;  //@none
                        }
                    """,
                },
                lines=[
                    ("each", "Try each vote's option as the possible winner."),
                    ("count", "Count its votes with a full scan. `c × 2 > n` is \"more than half\" without the rounding of `n / 2`."),
                    ("none", "No option passed half."),
                ],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["The same option is recounted for every one of its votes. Counting all options in one pass removes the repetition, at the cost of memory."],
                slow=True,
            ),
            approach(
                "Count in a hash map",
                "better",
                "O(n)",
                "O(n)",
                idea=["One pass counts every option in a hash map; return the option whose count passes n/2 (stop as soon as one does), else −1."],
                walk=w2,
                build=["Empty map option → votes.", "For each vote, increment its count; if `count × 2 > n`, return it.", "Return −1."],
                code={
                    "python": """
                        class Solution:
                            def strictMajority(self, votes: List[int]) -> int:
                                n = len(votes)
                                count = {}  #@map
                                for x in votes:  #@loop
                                    count[x] = count.get(x, 0) + 1  #@loop
                                    if count[x] * 2 > n:  #@check
                                        return x  #@check
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int strictMajority(int[] votes) {
                                int n = votes.length;
                                Map<Integer, Integer> count = new HashMap<>();  //@map
                                for (int x : votes) {  //@loop
                                    if (count.merge(x, 1, Integer::sum) * 2 > n) return x;  //@check
                                }
                                return -1;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int strictMajority(vector<int>& votes) {
                                int n = votes.size();
                                unordered_map<int, int> count;  //@map
                                for (int x : votes) {  //@loop
                                    if (++count[x] * 2 > n) return x;  //@check
                                }
                                return -1;  //@none
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int key; int count; bool used; } Slot;  //@table

                        static unsigned slotOf(int key, unsigned mask) {  //@table
                            unsigned long long h = (unsigned long long) (long long) key * 0x9E3779B97F4A7C15ULL;  //@table
                            return (unsigned) (h >> 32) & mask;  //@table
                        }  //@table

                        int strictMajority(int* votes, int votesSize) {
                            unsigned cap = 1;  //@map
                            while (cap < 2u * votesSize) cap <<= 1;  //@map
                            Slot* count = calloc(cap, sizeof(Slot));  //@map
                            int winner = -1;  //@map
                            for (int i = 0; i < votesSize && winner < 0; i++) {  //@loop
                                unsigned s = slotOf(votes[i], cap - 1);  //@loop
                                while (count[s].used && count[s].key != votes[i]) s = (s + 1) & (cap - 1);  //@loop
                                count[s].key = votes[i];  //@loop
                                count[s].used = true;  //@loop
                                if (++count[s].count * 2 > votesSize) winner = votes[i];  //@check
                            }
                            free(count);  //@none
                            return winner;  //@none
                        }
                    """,
                },
                lines=[
                    ("table", "C has no hash map: a slot holds an option, its count and an in-use flag; `slotOf` scrambles an option into a starting slot."),
                    ("map", "Votes per option.", {"c": "A power-of-two table at least 2n big; `winner` stays −1 until an option passes half (option ids are ≥ 0, so −1 can't be confused with one)."}),
                    ("loop", "Add this vote to its option's count.", {"c": "Probe forward from the option's slot to its entry or an empty slot, and claim it."}),
                    ("check", "The moment a count passes half, that option has won; nothing later can change it."),
                    ("none", "No option passed half.", {"c": "Free the table and return the result."}),
                ],
                complexity=["**Time O(n)** on average. **Space O(n)** for the counts."],
                limits=["It keeps a count for every option, although at most one can win. Voting needs only one candidate and one counter; the price is a second pass to verify."],
            ),
            approach(
                "Boyer–Moore vote, then verify",
                "best",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    **Pass 1 (find a candidate):** keep `candidate` and `count`. When `count` is 0 the current vote
                    becomes the candidate; a matching vote adds 1, a different vote subtracts 1. Each subtraction
                    discards one candidate vote together with one different vote. A real winner has more votes than
                    everyone else together, so it can never be fully discarded: if a winner exists, it is the final
                    candidate.

                    **Pass 2 (verify):** the candidate might not be a winner (when there is none, the survivor is
                    arbitrary). Count its votes and return it only if the count passes n/2.
                    """
                ],
                walk=w3,
                build=["`candidate = −1`, `count = 0`.", "For each vote: if `count == 0`, adopt it; then `count += 1` if it equals the candidate, else `count −= 1`.", "Count the candidate's votes in a second pass.", "Return it if `votes × 2 > n`, else −1."],
                code={
                    "python": """
                        class Solution:
                            def strictMajority(self, votes: List[int]) -> int:
                                candidate, count = -1, 0  #@init
                                for x in votes:  #@vote
                                    if count == 0:  #@vote
                                        candidate = x  #@vote
                                    count += 1 if x == candidate else -1  #@vote
                                support = sum(1 for x in votes if x == candidate)  #@verify
                                return candidate if support * 2 > len(votes) else -1  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int strictMajority(int[] votes) {
                                int candidate = -1, count = 0;  //@init
                                for (int x : votes) {  //@vote
                                    if (count == 0) candidate = x;  //@vote
                                    count += (x == candidate) ? 1 : -1;  //@vote
                                }
                                int support = 0;  //@verify
                                for (int x : votes) if (x == candidate) support++;  //@verify
                                return support * 2 > votes.length ? candidate : -1;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int strictMajority(vector<int>& votes) {
                                int candidate = -1, count = 0;  //@init
                                for (int x : votes) {  //@vote
                                    if (count == 0) candidate = x;  //@vote
                                    count += (x == candidate) ? 1 : -1;  //@vote
                                }
                                int support = std::count(votes.begin(), votes.end(), candidate);  //@verify
                                return support * 2 > (int) votes.size() ? candidate : -1;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int strictMajority(int* votes, int votesSize) {
                            int candidate = -1, count = 0;  //@init
                            for (int i = 0; i < votesSize; i++) {  //@vote
                                if (count == 0) candidate = votes[i];  //@vote
                                count += (votes[i] == candidate) ? 1 : -1;  //@vote
                            }
                            int support = 0;  //@verify
                            for (int i = 0; i < votesSize; i++) if (votes[i] == candidate) support++;  //@verify
                            return support * 2 > votesSize ? candidate : -1;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "No candidate yet; a count of 0 means the next vote takes over."),
                    ("vote", "The cancelling pass: matching votes strengthen the candidate, different ones cancel one of its votes.", {"cpp": "The local `count` shadows `std::count`, which is why the verify step names `std::count` in full."}),
                    ("verify", "The survivor is only the *possible* winner. Count its real votes."),
                    ("ret", "It wins only with strictly more than half."),
                ],
                complexity=["**Time O(n):** two passes. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Boyer–Moore voting returns the majority **if one exists**. When it might not, always verify with a
              second count.
            - "More than half" in integer code: `count * 2 > n`, avoiding `n / 2` rounding mistakes.
            - Compare with **Majority Reading**, where the majority is guaranteed and the verify pass can be dropped.
            """
        ],
    )


@problem
def strong_candidates():
    v = [3, 8, 3, 5, 8, 3, 8, 1, 3, 8]
    n = len(v)
    want = sorted(c for c in set(v) if v.count(c) > n // 3)
    assert want == [3, 8] and n // 3 == 3

    w1 = Steps(f"Count each distinct option with a full scan; keep those above ⌊n/3⌋ = {n // 3}.")
    for x in sorted(set(v)):
        c = v.count(x)
        w1.step(f"Option {x}: {c} vote{'s' if c != 1 else ''}" + (f" > {n // 3}: strong." if c > n // 3 else f", not more than {n // 3}."), Row(v, st={j: ("answer" if c > n // 3 else "found") for j, y in enumerate(v) if y == x}, slots=True))
    w1.step(f"Strong: {want}.", Row(v, slots=True), result=want)

    w2 = Steps("Count all options in a hash map, then keep counts above ⌊n/3⌋.")
    cnt = {}
    for i, x in enumerate(v):
        cnt[x] = cnt.get(x, 0) + 1
        keys = list(cnt)
        w2.step(f"Vote {x}: count {cnt[x]}.", Row(v, st={**{q: "dim" for q in range(i)}, i: "active"}, slots=True), Row([f"{k}:{cnt[k]}" for k in keys], st={keys.index(x): "new"}, label="option:votes"))
    w2.step(f"Counts above {n // 3}: options {want}, sorted.", Row([f"{k}:{cnt[k]}" for k in cnt], st={list(cnt).index(c): "answer" for c in want}, label="option:votes"), result=want)

    w3 = Steps("Two candidate slots. A vote for neither cancels one vote from each.")
    a = b = None
    ca = cb = 0
    for i, x in enumerate(v):
        if x == a:
            ca += 1
            t = f"matches A → A has {ca}"
        elif x == b:
            cb += 1
            t = f"matches B → B has {cb}"
        elif ca == 0:
            a, ca = x, 1
            t = f"A is free → A = {x}"
        elif cb == 0:
            b, cb = x, 1
            t = f"B is free → B = {x}"
        else:
            ca -= 1
            cb -= 1
            t = f"matches neither → it and one vote from each candidate cancel (A {ca}, B {cb})"
        w3.step(f"Vote {x}: {t}.", Row(v, st={**{q: "dim" for q in range(i)}, i: "active"}, slots=True), Vars(A=f"{a} ×{ca}", B=f"{b} ×{cb}"))
    w3.step(f"Verify by counting: {a} has {v.count(a)}, {b} has {v.count(b)}; both are more than {n // 3}.", Row(v, st={j: "answer" for j, y in enumerate(v) if y in want}, slots=True), result=want)

    sol(
        "strong-candidates",
        summary="""
            At most **two** options can each have more than n/3 votes (three such options would need more than n
            votes). So two candidate slots are enough: a vote for a third option cancels one vote from each
            candidate. The survivors are the only options that *could* be strong, and one counting pass confirms
            which really are. O(n) time, O(1) space.
        """,
        question=[
            """
            Return every option with **more than ⌊n/3⌋** votes, in increasing order.

            - **Strictly more than ⌊n/3⌋:** with 10 votes, ⌊10/3⌋ = 3, so an option needs at least 4. With 3 votes it
              needs 2, so `[1, 2, 3]` has no strong option.
            - **0, 1 or 2 options can be strong**, never 3 (that would take more than n votes).
            - **Increasing order** in the output.
            - **Ids from −10⁹ to 10⁹**, so they can't index an array. The goal is O(1) extra space.
            """
        ],
        think=[
            """
            Take `[3, 8, 3, 5, 8, 3, 8, 1, 3, 8]` (n = 10, ⌊n/3⌋ = 3). Option 3 has 4 votes and option 8 has 4: both
            strong. 5 and 1 have one each.
            """,
            fig(Row(v, st={j: "answer" for j, y in enumerate(v) if y == 3} | {j: "found" for j, y in enumerate(v) if y == 8}, slots=True),
                caption="3 (dark) and 8 (light) each hold 4 of the 10 votes."),
            """
            The O(1)-space idea extends majority voting. Throw away **three votes for three different options** at
            a time. Each such triple removes at most one vote from any single option, and there are at most n/3
            triples, so an option with more than n/3 votes always has something left over.

            Two slots implement "three different options": when a vote matches neither candidate (and both slots
            are occupied), that vote plus one vote of each candidate form a triple, and all three disappear. Every
            strong option survives into a slot. But a survivor isn't necessarily strong, so finish with a counting
            pass, exactly as with the strict majority.
            """,
        ],
        approaches=[
            approach(
                "Count each option by scanning",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each distinct option (process an option only at its first appearance), count its votes with a full scan and keep it if the count exceeds ⌊n/3⌋. Sort the (at most two) results."],
                walk=w1,
                build=["For each index i, skip it if the same option appeared earlier.", "Count the option's votes with a scan.", "Keep it if `count > n / 3` (integer division).", "Return the kept options sorted."],
                code={
                    "python": """
                        class Solution:
                            def strongCandidates(self, votes: List[int]) -> List[int]:
                                n = len(votes)
                                out = []
                                for i, x in enumerate(votes):  #@each
                                    if x in votes[:i]:  #@dup
                                        continue  #@dup
                                    if votes.count(x) > n // 3:  #@count
                                        out.append(x)  #@count
                                return sorted(out)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] strongCandidates(int[] votes) {
                                int n = votes.length;
                                List<Integer> out = new ArrayList<>();
                                for (int i = 0; i < n; i++) {  //@each
                                    boolean seen = false;  //@dup
                                    for (int j = 0; j < i && !seen; j++) seen = votes[j] == votes[i];  //@dup
                                    if (seen) continue;  //@dup
                                    int c = 0;  //@count
                                    for (int x : votes) if (x == votes[i]) c++;  //@count
                                    if (c > n / 3) out.add(votes[i]);  //@count
                                }
                                Collections.sort(out);  //@ret
                                return out.stream().mapToInt(Integer::intValue).toArray();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> strongCandidates(vector<int>& votes) {
                                int n = votes.size();
                                vector<int> out;
                                for (int i = 0; i < n; i++) {  //@each
                                    if (find(votes.begin(), votes.begin() + i, votes[i]) != votes.begin() + i) continue;  //@dup
                                    if (count(votes.begin(), votes.end(), votes[i]) > n / 3) out.push_back(votes[i]);  //@count
                                }
                                sort(out.begin(), out.end());  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* strongCandidates(int* votes, int votesSize, int* returnSize) {
                            int n = votesSize;
                            int* out = malloc(2 * sizeof(int));
                            *returnSize = 0;
                            for (int i = 0; i < n; i++) {  //@each
                                bool seen = false;  //@dup
                                for (int j = 0; j < i && !seen; j++) seen = votes[j] == votes[i];  //@dup
                                if (seen) continue;  //@dup
                                int c = 0;  //@count
                                for (int j = 0; j < n; j++) if (votes[j] == votes[i]) c++;  //@count
                                if (c > n / 3) out[(*returnSize)++] = votes[i];  //@count
                            }
                            if (*returnSize == 2 && out[0] > out[1]) { int t = out[0]; out[0] = out[1]; out[1] = t; }  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("each", "Consider each option once, at its first appearance."),
                    ("dup", "If this option already appeared to the left, it was already counted."),
                    ("count", "Count its votes; more than ⌊n/3⌋ (integer division) makes it strong."),
                    ("ret", "At most two results; put them in increasing order.", {"c": "Two strong options at most, so room for 2 is enough, and one comparison sorts them."}),
                ],
                complexity=["**Time O(n²).** **Space O(1)** besides the (at most 2) answers."],
                limits=["Each option costs a full scan. One counting pass with a hash map handles all options together."],
                slow=True,
            ),
            approach(
                "Count in a hash map",
                "better",
                "O(n)",
                "O(n)",
                idea=["Count every option in one pass, then keep the options whose count exceeds ⌊n/3⌋ and sort them."],
                walk=w2,
                build=["Count votes per option in a hash map.", "Collect options with `count > n / 3`.", "Sort and return."],
                code={
                    "python": """
                        from collections import Counter

                        class Solution:
                            def strongCandidates(self, votes: List[int]) -> List[int]:
                                count = Counter(votes)  #@map
                                return sorted(x for x, c in count.items() if c > len(votes) // 3)  #@keep
                    """,
                    "java": """
                        class Solution {
                            public int[] strongCandidates(int[] votes) {
                                Map<Integer, Integer> count = new HashMap<>();  //@map
                                for (int x : votes) count.merge(x, 1, Integer::sum);  //@map
                                List<Integer> out = new ArrayList<>();  //@keep
                                for (Map.Entry<Integer, Integer> e : count.entrySet()) if (e.getValue() > votes.length / 3) out.add(e.getKey());  //@keep
                                Collections.sort(out);  //@keep
                                return out.stream().mapToInt(Integer::intValue).toArray();  //@keep
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> strongCandidates(vector<int>& votes) {
                                unordered_map<int, int> count;  //@map
                                for (int x : votes) count[x]++;  //@map
                                vector<int> out;  //@keep
                                for (auto& [x, c] : count) if (c > (int) votes.size() / 3) out.push_back(x);  //@keep
                                sort(out.begin(), out.end());  //@keep
                                return out;  //@keep
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int key; int count; bool used; } Slot;  //@table

                        static unsigned slotOf(int key, unsigned mask) {  //@table
                            unsigned long long h = (unsigned long long) (long long) key * 0x9E3779B97F4A7C15ULL;  //@table
                            return (unsigned) (h >> 32) & mask;  //@table
                        }  //@table

                        int* strongCandidates(int* votes, int votesSize, int* returnSize) {
                            unsigned cap = 1;  //@map
                            while (cap < 2u * votesSize) cap <<= 1;  //@map
                            Slot* count = calloc(cap, sizeof(Slot));  //@map
                            for (int i = 0; i < votesSize; i++) {  //@map
                                unsigned s = slotOf(votes[i], cap - 1);  //@map
                                while (count[s].used && count[s].key != votes[i]) s = (s + 1) & (cap - 1);  //@map
                                count[s].key = votes[i];  //@map
                                count[s].used = true;  //@map
                                count[s].count++;  //@map
                            }  //@map
                            int* out = malloc(2 * sizeof(int));  //@keep
                            *returnSize = 0;  //@keep
                            for (unsigned s = 0; s < cap; s++) if (count[s].used && count[s].count > votesSize / 3) out[(*returnSize)++] = count[s].key;  //@keep
                            if (*returnSize == 2 && out[0] > out[1]) { int t = out[0]; out[0] = out[1]; out[1] = t; }  //@keep
                            free(count);  //@keep
                            return out;  //@keep
                        }
                    """,
                },
                lines=[
                    ("table", "C has no hash map: a slot holds an option, its count and an in-use flag."),
                    ("map", "Votes per option, one pass.", {"c": "Probe from each option's slot to its entry (or an empty slot) and bump the count."}),
                    ("keep", "Options above ⌊n/3⌋, in increasing order.", {"c": "Walk the table's used slots; at most two qualify, so one comparison orders them."}),
                ],
                complexity=["**Time O(n)** on average. **Space O(n)** for the counts."],
                limits=["It stores a count for every option, but at most two options can be strong. Two candidate slots suffice, with a verification pass."],
            ),
            approach(
                "Two-candidate voting, then verify",
                "best",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    Keep candidates A and B with counters. For each vote, in this order:

                    1. equal to A → A's count + 1; equal to B → B's count + 1;
                    2. otherwise, if a slot's count is 0, the vote takes that slot with count 1;
                    3. otherwise it matches neither and both slots are busy: decrement both counts. This discards
                       three votes for three different options.

                    Every option with more than n/3 votes ends in a slot. Then count A and B exactly and keep those
                    above ⌊n/3⌋.
                    """
                ],
                walk=w3,
                build=["Slots `a`, `b` with counts `ca = cb = 0`.", "Apply the three rules above to each vote; check matches before empty slots, so one option never occupies both.", "Count the real votes of `a` and `b`.", "Return those with more than `n / 3`, sorted."],
                code={
                    "python": """
                        class Solution:
                            def strongCandidates(self, votes: List[int]) -> List[int]:
                                a, b, ca, cb = None, None, 0, 0  #@init
                                for x in votes:  #@loop
                                    if x == a:  #@match
                                        ca += 1  #@match
                                    elif x == b:  #@match
                                        cb += 1  #@match
                                    elif ca == 0:  #@take
                                        a, ca = x, 1  #@take
                                    elif cb == 0:  #@take
                                        b, cb = x, 1  #@take
                                    else:  #@cancel
                                        ca -= 1  #@cancel
                                        cb -= 1  #@cancel
                                n = len(votes)  #@verify
                                return sorted(c for c in {a, b} if c is not None and votes.count(c) > n // 3)  #@verify
                    """,
                    "java": """
                        class Solution {
                            public int[] strongCandidates(int[] votes) {
                                int a = 0, b = 0, ca = 0, cb = 0;  //@init
                                for (int x : votes) {  //@loop
                                    if (ca > 0 && x == a) ca++;  //@match
                                    else if (cb > 0 && x == b) cb++;  //@match
                                    else if (ca == 0) { a = x; ca = 1; }  //@take
                                    else if (cb == 0) { b = x; cb = 1; }  //@take
                                    else { ca--; cb--; }  //@cancel
                                }
                                int na = 0, nb = 0;  //@verify
                                for (int x : votes) {  //@verify
                                    if (ca > 0 && x == a) na++;  //@verify
                                    else if (cb > 0 && x == b) nb++;  //@verify
                                }  //@verify
                                List<Integer> out = new ArrayList<>();  //@verify
                                if (na > votes.length / 3) out.add(a);  //@verify
                                if (nb > votes.length / 3) out.add(b);  //@verify
                                Collections.sort(out);  //@verify
                                return out.stream().mapToInt(Integer::intValue).toArray();  //@verify
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> strongCandidates(vector<int>& votes) {
                                int a = 0, b = 0, ca = 0, cb = 0;  //@init
                                for (int x : votes) {  //@loop
                                    if (ca > 0 && x == a) ca++;  //@match
                                    else if (cb > 0 && x == b) cb++;  //@match
                                    else if (ca == 0) { a = x; ca = 1; }  //@take
                                    else if (cb == 0) { b = x; cb = 1; }  //@take
                                    else { ca--; cb--; }  //@cancel
                                }
                                int na = 0, nb = 0;  //@verify
                                for (int x : votes) {  //@verify
                                    if (ca > 0 && x == a) na++;  //@verify
                                    else if (cb > 0 && x == b) nb++;  //@verify
                                }  //@verify
                                vector<int> out;  //@verify
                                int n = votes.size();  //@verify
                                if (na > n / 3) out.push_back(a);  //@verify
                                if (nb > n / 3) out.push_back(b);  //@verify
                                sort(out.begin(), out.end());  //@verify
                                return out;  //@verify
                            }
                        };
                    """,
                    "c": """
                        int* strongCandidates(int* votes, int votesSize, int* returnSize) {
                            int a = 0, b = 0, ca = 0, cb = 0;  //@init
                            for (int i = 0; i < votesSize; i++) {  //@loop
                                int x = votes[i];  //@loop
                                if (ca > 0 && x == a) ca++;  //@match
                                else if (cb > 0 && x == b) cb++;  //@match
                                else if (ca == 0) { a = x; ca = 1; }  //@take
                                else if (cb == 0) { b = x; cb = 1; }  //@take
                                else { ca--; cb--; }  //@cancel
                            }
                            int na = 0, nb = 0;  //@verify
                            for (int i = 0; i < votesSize; i++) {  //@verify
                                if (ca > 0 && votes[i] == a) na++;  //@verify
                                else if (cb > 0 && votes[i] == b) nb++;  //@verify
                            }  //@verify
                            int* out = malloc(2 * sizeof(int));  //@verify
                            *returnSize = 0;  //@verify
                            if (na > votesSize / 3) out[(*returnSize)++] = a;  //@verify
                            if (nb > votesSize / 3) out[(*returnSize)++] = b;  //@verify
                            if (*returnSize == 2 && out[0] > out[1]) { int t = out[0]; out[0] = out[1]; out[1] = t; }  //@verify
                            return out;  //@verify
                        }
                    """,
                },
                lines=[
                    ("init", "Two empty slots.", {"java": "A slot with count 0 is treated as empty, so the starting value of `a` and `b` doesn't matter: every match test also checks the count.", "cpp": "A slot with count 0 is treated as empty, so every match test also checks the count.", "c": "A slot with count 0 is treated as empty, so every match test also checks the count."}),
                    ("loop", "One pass over the votes."),
                    ("match", "A vote for a current candidate strengthens it. Matches are tested **before** filling empty slots, so the same option never ends up in both slots."),
                    ("take", "An empty slot adopts the new option."),
                    ("cancel", "Three different options (A, B and this vote) each lose one vote. An option with more than n/3 votes can't be wiped out by such triples."),
                    ("verify", "Survivors are only candidates. Count them exactly, keep those above ⌊n/3⌋, and sort.",
                     {"python": "`{a, b}` removes the case where both slots hold the same value; `None` means an empty slot.",
                      "java": "Only slots that are still occupied (count > 0) are counted; an emptied slot's value may be stale.",
                      "cpp": "Only slots that are still occupied (count > 0) are counted; an emptied slot's value may be stale.",
                      "c": "Only slots that are still occupied (count > 0) are counted; an emptied slot's value may be stale."}),
                ],
                complexity=["**Time O(n):** two passes. **Space O(1):** four variables."],
            ),
        ],
        takeaways=[
            """
            - **Generalised Boyer–Moore:** to find options with more than n/k votes, keep k − 1 candidate slots; a vote
              matching none cancels one vote from every slot (k different votes discarded at once).
            - Survivors are candidates, not answers: always verify with exact counts.
            - Check "matches a candidate" before "take an empty slot", or one option can occupy two slots.
            """
        ],
    )
