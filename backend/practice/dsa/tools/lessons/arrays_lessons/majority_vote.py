"""Lesson: Majority vote (Arrays & Hashing, pattern 11)."""
from lesson import Bars, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

CAND = {
    "python": """
        def majority_candidate(nums):
            candidate, count = None, 0          #@init
            for x in nums:                      #@loop
                if count == 0:                  #@empty
                    candidate = x               #@empty
                if x == candidate:              #@same
                    count += 1                  #@same
                else:                           #@diff
                    count -= 1                  #@diff
            return candidate                    #@ret
    """,
    "java": """
        static int majorityCandidate(int[] nums) {
            int candidate = 0, count = 0;       //@init
            for (int x : nums) {                //@loop
                if (count == 0) candidate = x;  //@empty
                if (x == candidate) count++;    //@same
                else count--;                   //@diff
            }
            return candidate;                   //@ret
        }
    """,
    "cpp": """
        int majorityCandidate(const vector<int>& nums) {
            int candidate = 0, count = 0;       //@init
            for (int x : nums) {                //@loop
                if (count == 0) candidate = x;  //@empty
                if (x == candidate) count++;    //@same
                else count--;                   //@diff
            }
            return candidate;                   //@ret
        }
    """,
    "c": """
        int majorityCandidate(const int* nums, int n) {
            int candidate = 0, count = 0;       //@init
            for (int i = 0; i < n; i++) {       //@loop
                if (count == 0) candidate = nums[i];    //@empty
                if (nums[i] == candidate) count++;      //@same
                else count--;                           //@diff
            }
            return candidate;                   //@ret
        }
    """,
}
CAND_RUN = {
    "python": """
        print(majority_candidate([2, 7, 2, 2, 5, 2, 7, 2, 2]))
        print(majority_candidate([9, 4, 9, 4, 4]))
        print(majority_candidate([4, 4, 5, 5, 6]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(majorityCandidate(new int[] {2, 7, 2, 2, 5, 2, 7, 2, 2}));
            System.out.println(majorityCandidate(new int[] {9, 4, 9, 4, 4}));
            System.out.println(majorityCandidate(new int[] {4, 4, 5, 5, 6}));
        }
    """,
    "cpp": """
        int main() {
            cout << majorityCandidate({2, 7, 2, 2, 5, 2, 7, 2, 2}) << "\\n";
            cout << majorityCandidate({9, 4, 9, 4, 4}) << "\\n";
            cout << majorityCandidate({4, 4, 5, 5, 6}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {2, 7, 2, 2, 5, 2, 7, 2, 2}, b[] = {9, 4, 9, 4, 4}, c[] = {4, 4, 5, 5, 6};
            printf("%d\\n%d\\n%d\\n", majorityCandidate(a, 9), majorityCandidate(b, 5), majorityCandidate(c, 5));
            return 0;
        }
    """,
}

EQUI = {
    "python": """
        def equi_leaders(nums):
            leader, count = None, 0                         #@vote
            for x in nums:                                  #@vote
                if count == 0:                              #@vote
                    leader = x                              #@vote
                count += 1 if x == leader else -1           #@vote
            n = len(nums)                                   #@total
            total = sum(1 for x in nums if x == leader)     #@total
            if total * 2 <= n:                              #@none
                return 0                                    #@none
            splits, left = 0, 0                             #@scan
            for i in range(n - 1):                          #@cut
                if nums[i] == leader:                       #@left
                    left += 1                               #@left
                right = total - left                        #@right
                if left * 2 > i + 1 and right * 2 > n - i - 1:  #@both
                    splits += 1                             #@both
            return splits                                   #@ret
    """,
    "java": """
        static int equiLeaders(int[] nums) {
            int leader = 0, count = 0;                      //@vote
            for (int x : nums) {                            //@vote
                if (count == 0) leader = x;                 //@vote
                count += x == leader ? 1 : -1;              //@vote
            }
            int n = nums.length, total = 0;                 //@total
            for (int x : nums) if (x == leader) total++;    //@total
            if (total * 2 <= n) return 0;                   //@none
            int splits = 0, left = 0;                       //@scan
            for (int i = 0; i < n - 1; i++) {               //@cut
                if (nums[i] == leader) left++;              //@left
                int right = total - left;                   //@right
                if (left * 2 > i + 1 && right * 2 > n - i - 1) splits++;  //@both
            }
            return splits;                                  //@ret
        }
    """,
    "cpp": """
        int equiLeaders(const vector<int>& nums) {
            int leader = 0, count = 0;                      //@vote
            for (int x : nums) {                            //@vote
                if (count == 0) leader = x;                 //@vote
                count += x == leader ? 1 : -1;              //@vote
            }
            int n = nums.size();                            //@total
            int total = std::count(nums.begin(), nums.end(), leader);  //@total
            if (total * 2 <= n) return 0;                   //@none
            int splits = 0, left = 0;                       //@scan
            for (int i = 0; i < n - 1; i++) {               //@cut
                if (nums[i] == leader) left++;              //@left
                int right = total - left;                   //@right
                if (left * 2 > i + 1 && right * 2 > n - i - 1) splits++;  //@both
            }
            return splits;                                  //@ret
        }
    """,
    "c": """
        int equiLeaders(const int* nums, int n) {
            int leader = 0, count = 0;                      //@vote
            for (int i = 0; i < n; i++) {                   //@vote
                if (count == 0) leader = nums[i];           //@vote
                count += nums[i] == leader ? 1 : -1;        //@vote
            }
            int total = 0;                                  //@total
            for (int i = 0; i < n; i++) if (nums[i] == leader) total++;  //@total
            if (total * 2 <= n) return 0;                   //@none
            int splits = 0, left = 0;                       //@scan
            for (int i = 0; i < n - 1; i++) {               //@cut
                if (nums[i] == leader) left++;              //@left
                int right = total - left;                   //@right
                if (left * 2 > i + 1 && right * 2 > n - i - 1) splits++;  //@both
            }
            return splits;                                  //@ret
        }
    """,
}
EQUI_RUN = {
    "python": """
        print(equi_leaders([4, 4, 2, 4, 3, 4]))
        print(equi_leaders([1, 2, 1, 2]))
        print(equi_leaders([7, 7, 7]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(equiLeaders(new int[] {4, 4, 2, 4, 3, 4}));
            System.out.println(equiLeaders(new int[] {1, 2, 1, 2}));
            System.out.println(equiLeaders(new int[] {7, 7, 7}));
        }
    """,
    "cpp": """
        int main() {
            cout << equiLeaders({4, 4, 2, 4, 3, 4}) << "\\n";
            cout << equiLeaders({1, 2, 1, 2}) << "\\n";
            cout << equiLeaders({7, 7, 7}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {4, 4, 2, 4, 3, 4}, b[] = {1, 2, 1, 2}, c[] = {7, 7, 7};
            printf("%d\\n%d\\n%d\\n", equiLeaders(a, 6), equiLeaders(b, 4), equiLeaders(c, 3));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

majority_candidate = py(CAND["python"], "majority_candidate")
equi_leaders = py(EQUI["python"], "equi_leaders")

DEMO = [2, 7, 2, 2, 5, 2, 7, 2, 2]
assert majority_candidate(DEMO) == 2 and DEMO.count(2) == 6

# The candidate pass, step by step.
vw = Steps(f"`majority_candidate({DEMO})`. One candidate, one counter, one pass.")
cand, cnt = None, 0
vw.step("Nothing read yet. The counter is 0, which means \"no candidate\": the next value read takes the job.", Row(DEMO, slots=True), M({"candidate": "none", "count": 0}))
for i, x in enumerate(DEMO):
    took = cnt == 0
    if took:
        cand = x
    if x == cand:
        cnt += 1
        msg = (f"The counter is 0, so {x} becomes the candidate, with count 1." if took
               else f"{x} matches the candidate: one more vote for it, count {cnt}.")
        state = "found"
    else:
        cnt -= 1
        msg = (f"{x} isn't the candidate. Cross it out together with one copy of {cand}: count drops to {cnt}."
               + (f" Nothing is left standing, so whoever comes next takes over." if cnt == 0 else ""))
        state = "mark"
    vw.step(msg, Row(DEMO, st={**{k: "dim" for k in range(i)}, i: state}, ptr={"x": i}, slots=True), M({"candidate": cand, "count": cnt}))
vw.steps[-1]["text"] += f" The pass ends with candidate {cand}. Because this array is promised to have a majority, {cand} is it."

# Pairing picture: each decrement cancels the current value with one earlier copy of the candidate.
stack, PAIRS = [], []
for i, x in enumerate(DEMO):
    if not stack or DEMO[stack[-1]] == x:
        stack.append(i)
    else:
        PAIRS.append((stack.pop(), i))
SURV = stack
assert len(SURV) == 3 and all(DEMO[k] == 2 for k in SURV)
pair_state = {**{k: "dim" for p in PAIRS for k in p}, **{k: "answer" for k in SURV}}
pair_rows = [(f"index {a} ({DEMO[a]}) and index {b} ({DEMO[b]})", "different, so both go") for a, b in PAIRS]

# Without verification: a "candidate" that isn't a majority.
BAD = [4, 4, 5, 5, 6]
bad_rows, c, k = [], None, 0
for x in BAD:
    if k == 0:
        c = x
    k += 1 if x == c else -1
    bad_rows.append((str(x), str(c), str(k)))
assert majority_candidate(BAD) == 6 and BAD.count(6) == 1

# Not the most common value.
MODE = [1, 1, 2, 3, 4]
assert majority_candidate(MODE) == 4

# Generalising: k - 1 slots find every value with more than n / k copies.
MG, MGK = [3, 1, 3, 2, 4, 3, 1, 3, 5, 1, 3, 1], 4
gw = Steps(f"Three slots on `{MG}` (n = {len(MG)}). Anything with more than {len(MG)} / {MGK} = {len(MG) // MGK} copies must survive.")
slots = {}
gw.step(f"With k = {MGK} we keep k - 1 = {MGK - 1} candidates, each with its own counter.", Row(MG, slots=True), M({"slots": "empty"}))


def show(s):
    return {f"slot {v}": n for v, n in s.items()} or {"slots": "empty"}


for i, x in enumerate(MG):
    if x in slots:
        slots[x] += 1
        msg, stt = f"{x} already has a slot: its counter goes up to {slots[x]}.", "found"
    elif len(slots) < MGK - 1:
        slots[x] = 1
        msg, stt = f"{x} has no slot, and a slot is free: {x} moves in with count 1.", "new"
    else:
        before = ", ".join(map(str, slots))
        slots = {v: n - 1 for v, n in slots.items() if n > 1}
        msg = (f"{x} has no slot and all three are taken. Cross out {x} together with one copy each of {before}: "
               f"four different values gone in one go. Every counter drops by 1, and any that hit 0 free their slot.")
        stt = "mark"
    gw.step(msg, Row(MG, st={**{j: "dim" for j in range(i)}, i: stt}, ptr={"x": i}, slots=True), M(show(slots)))
SURVIVORS = sorted(slots)
MG_COUNTS = {v: MG.count(v) for v in sorted(set(MG))}
HEAVY = [v for v in SURVIVORS if MG_COUNTS[v] * MGK > len(MG)]
assert HEAVY == [1, 3]
gw.step(f"The survivors are {', '.join(map(str, SURVIVORS))}. They're only suspects: count each one again to see who really has more than {len(MG) // MGK} copies.",
        Bars(list(MG_COUNTS.values()), labels=list(MG_COUNTS), st={list(MG_COUNTS).index(v): "answer" for v in HEAVY}, label="real counts"),
        result=HEAVY)

# Equi-leaders.
EQ = [4, 4, 2, 4, 3, 4]
EQ_OUT = equi_leaders(EQ)
assert EQ_OUT == 3
ew = Steps(f"`equi_leaders({EQ})`. The leader is 4 ({EQ.count(4)} of {len(EQ)}). Try every cut and check both sides.")
tot, left = EQ.count(4), 0
ew.step(f"Boyer-Moore finds 4, and counting confirms {tot} copies out of {len(EQ)}: more than half. Now cut the array after each index.", Row(EQ, slots=True), M({"total 4s": tot}))
for i in range(len(EQ) - 1):
    if EQ[i] == 4:
        left += 1
    right = tot - left
    ln, rn = i + 1, len(EQ) - i - 1
    okl, okr = left * 2 > ln, right * 2 > rn
    verdict = "both sides are led by 4, so this cut counts." if okl and okr else (
        "the left side isn't led by 4." if not okl else "the right side isn't led by 4.")
    ew.step(f"Cut after index {i}: the left has {left} of {ln} fours, the right has {right} of {rn}. So {verdict}",
            Row(EQ, st={k: ("found" if k <= i else "mark") for k in range(len(EQ))}, ptr={"cut": i}, slots=True),
            M({"left 4s": f"{left} / {ln}", "right 4s": f"{right} / {rn}"}))
ew.steps[-1]["text"] += f" {EQ_OUT} cuts in total."

lesson(
    "arrays-hashing",
    "majority-vote",
    """
    When one value fills more than half of an array, you can find it with a single variable and a counter. Pair off
    different values and throw both away: the majority can't run out first, so whatever is left standing is the only
    value that could be it. Then count it once more to be sure.
    """,
    [
        ("idea", "The idea", [
            """
            Picture a room full of people, each wearing a team shirt. You want to know if one team has more than half
            the room. You could count every team, but there's a quieter way: ask any two people from *different* teams
            to leave together. Keep doing that until everyone left is on the same team.

            If one team really had more than half, it can't be the one that runs out. Every time a pair leaves, that
            team loses at most one person, and the rest of the room loses at least one too. So the team left standing
            is the only one that could have been the majority. Whether it actually was, you still have to check.

            Boyer-Moore's majority vote does exactly this while reading the array once. It keeps one **candidate** and a
            **count** of how many of the candidate's copies are still "standing". A matching value adds one. A
            different value cancels one copy. When the count reaches zero, the next value takes over.
            """,
            fig(Row(DEMO, st=pair_state, slots=True, label="crossed out in pairs"),
                caption=f"Every grey pair is two different values that cancelled. The {len(SURV)} survivors are all 2s, and 2 is the majority."),
            key("""
            Keep a `candidate` and a `count`. If `count` is 0, take the current value as the candidate. Then a match adds
            one and a mismatch takes one away. If any value fills more than half the array, it's the candidate at the
            end. If that isn't promised, count the candidate once more to check.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The tell is a threshold on frequency: "more than half", "more than n / 3", "appears more than ⌊n / k⌋ times",
            "the dominant element", "the leader". Usually there's a second hint too: O(1) extra space, one pass, or a
            stream too big to store.

            A hash map of counts (*Frequency counting*) solves the same questions in O(n) time, and is simpler to get
            right. Reach for majority vote when the space limit rules the map out, or when you're reading a stream and
            can't keep everything.

            Not a fit:

            - "The most common value" (the mode). The majority vote only finds a value with **more than half**. If no
              value has that many, the candidate it hands back can be anything, even a value that appears once.
            - "The top k most frequent". That's counting plus sorting or a heap.
            - "At least half" (rather than more than half). Two values can each fill exactly half, so there may be two
              answers. The cancelling argument needs a strict majority.
            """,
            table(["question says", "slots to keep", "survivors to check"],
                  ["more than n / 2", "1", "1"],
                  ["more than n / 3", "2", "up to 2"],
                  ["more than n / k", "k - 1", "up to k - 1"]),
        ]),
        ("theory", "Why it works", [
            """
            ### Throwing away two different values keeps the majority

            Say value `m` appears `c` times out of `n`, with `c > n / 2`. Remove two *different* values from the array. At
            most one of them is `m`, so `m` now appears at least `c - 1` times out of `n - 2`. And `c - 1 > (n - 2) / 2`
            is the same inequality as `c > n / 2`. So `m` is still a strict majority of what's left. Keep removing
            different pairs, and `m` stays a majority every time. When no different pair is left, everything remaining
            is one value, and it has to be `m`.

            ### The counter is that pairing, done on the fly

            You don't need to actually remove anything. Read the array left to right and keep this picture:

            - every value read so far is either *paired off* with a different value, or *standing*;
            - everything standing is the same value, the `candidate`, and `count` says how many are standing.

            A new value equal to the candidate joins the standing group: `count + 1`. A different value pairs off with
            one standing copy, and both are crossed out: `count - 1`. When `count` is 0 nothing is standing, so the next
            value starts a fresh group. That's the whole algorithm. Here are the pairs it made for `{DEMO}`:
            """.replace("{DEMO}", str(DEMO)),
            table(["crossed out together", "why"], *pair_rows),
            f"""
            What's left standing is {len(SURV)} copies of 2 (indices {', '.join(map(str, SURV))}), and the counter at the
            end is {len(SURV)}. Every crossed-out pair was two different values, so by the argument above a true majority
            can never be crossed out completely.

            ### Why you still have to check

            The argument runs one way only: *if* there is a majority, it's the candidate. If there isn't, the pass still
            hands back somebody. Here's `{BAD}`, which has no majority at all:
            """,
            table(["read", "candidate", "count"], *bad_rows),
            """
            The candidate is 6, which appears once. So unless the question promises a majority exists, count the
            candidate in a second pass and compare with `n / 2`. That keeps it O(n) time and O(1) space.

            ### More than n / k, with k - 1 slots

            The same idea scales. Keep up to `k - 1` candidates, each with a counter. A value with a slot adds one to its
            counter. A value with no slot takes a free slot if there is one. If all `k - 1` slots are full, cross out
            the new value *and one copy of every slot*: that's `k` different values gone at once, so every counter drops
            by one.

            Each such round removes `k` values, so it can happen at most `n / k` times. A value with more than `n / k`
            copies loses at most one copy per round, so it can't be wiped out, and it ends in a slot. At most `k - 1`
            values can have more than `n / k` copies, which is why `k - 1` slots are enough. As before, the survivors are
            only suspects, and you count them again.
            """,
            walk(gw),
        ]),
        ("template", "The template", [
            """
            The candidate pass. It returns the majority whenever one exists; when that isn't promised, check the answer
            with one more counting pass (the variation below shows that check).
            """,
            code(
                "Boyer-Moore candidate pass",
                CAND,
                [
                    ("init", "No candidate yet, and nothing standing.",
                     {"java": "`candidate` needs some starting value in Java; it's never read before the first value replaces it.",
                      "c": "Same as Java: 0 is a placeholder that the first value overwrites."}),
                    ("loop", "One pass, left to right."),
                    ("empty", "Nothing is standing, so this value becomes the new candidate. Check this *before* comparing, so "
                              "the value counts as a vote for itself in the next line."),
                    ("same", "Another copy of the candidate joins the standing group."),
                    ("diff", "A different value cancels one standing copy. Both are now crossed out."),
                    ("ret", "If a majority exists, this is it. Otherwise it's just whoever was standing last."),
                ],
                CAND_RUN,
                "majority_candidate([2, 7, 2, 2, 5, 2, 7, 2, 2]); ([9, 4, 9, 4, 4]); ([4, 4, 5, 5, 6])",
            ),
            """
            The third line of output is the warning from *Why it works*: `[4, 4, 5, 5, 6]` has no majority, and the pass
            still names 6.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "Watch the candidate change hands. The counter is the number of candidate copies still standing:",
            walk(vw),
            """
            Notice that the candidate was 2 the whole time here, but the counter dipped to 0 after index 1. If the next
            value had been a 5, the 5 would have taken over for a while. That's fine: a true majority always wins the
            job back, because it has more copies than everything else put together.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Not the most common value

            Run the pass on `{MODE}`. The 1s take the lead, then 2 and 3 cancel them, and 4 is standing at the end, so the
            candidate is 4. But 1 is the most common value. No value has more than half here, so the candidate means
            nothing until you check it, and checking says "no majority". If you want the most common value, count.

            ### A stream you can't store

            A server logs which region served each request, millions per hour, and you want to know if one region is
            handling more than half the traffic. You don't have room to store the log. Two variables, updated as each
            line goes past, give you the only region that could be over half. Read the log a second time (or count that
            one region as you go next hour) to confirm.

            ### The same leader on both sides

            Cut an array into a left part and a right part. Is the same value a strict majority of *both* parts? If so,
            it has to be the majority of the whole array too (more than half of each side is more than half of the
            total). So find the overall leader once, count it, and then slide the cut along, tracking how many copies
            are on the left. The variation below writes this out. Here it is on `{EQ}`:
            """,
            walk(ew),
        ]),
        ("variations", "Variations", [
            """
            ### Verify, then use the count

            Most real questions don't promise a majority, so the pass is followed by a counting pass. Once you've
            counted, the count itself is useful. Here it lets us test every cut in O(1): the left side has `left`
            copies, the right side has `total - left`.
            """,
            code(
                "Count the cuts where both sides share the leader",
                EQUI,
                [
                    ("vote", "Boyer-Moore: find the only value that could lead the whole array."),
                    ("total", "Count it for real."),
                    ("none", "Not a strict majority of the whole array, so it can't lead both halves of any cut. No cuts."),
                    ("scan", "`left` is how many copies of the leader are in the left part so far."),
                    ("cut", "Cut after index `i`, for every `i` except the last (both parts must be non-empty)."),
                    ("left", "Index `i` moves into the left part."),
                    ("right", "The rest of the copies are on the right."),
                    ("both", "Strict majority on both sides. Comparing `2 * count > size` avoids rounding mistakes "
                             "with `size / 2`."),
                    ("ret", "The number of cuts that work."),
                ],
                EQUI_RUN,
                "equi_leaders([4, 4, 2, 4, 3, 4]); ([1, 2, 1, 2]); ([7, 7, 7])",
            ),
            """
            ### Several thresholds

            For "more than `n / 3`" keep two slots, for "more than `n / k`" keep `k - 1`, exactly as in the walkthrough in
            *Why it works*. Two details matter when you write it:

            - Check "does this value already have a slot?" for **every** slot before you consider taking a free one.
              Otherwise the same value can end up in two slots.
            - When all slots are full and the value has none, the value itself is crossed out too; it doesn't move
              into a slot that just freed up.

            ### Majority in a sorted array

            If the array is sorted, a majority (if there is one) covers the middle index, so `a[n / 2]` is the only
            candidate. Confirm it by finding its first and last positions with binary search: O(log n) without even
            reading the whole array.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            The candidate pass reads each value once and does O(1) work: O(n) time, O(1) extra space. The check is another
            O(n) pass. With `k - 1` slots, each value may touch every slot, so it's O(n·k) time and O(k) space, which is
            still linear for a fixed `k` like 3.
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Count everything in a hash map", "O(n) on average", "O(distinct values)"],
                ["Sort, then look at the middle", "O(n log n)", "O(1) to O(n)"],
                ["Boyer-Moore + check", "O(n)", "O(1)"],
                ["k - 1 slots + check (more than n / k)", "O(n·k)", "O(k)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            Start the candidate at `None`; the `count == 0` branch replaces it before it's ever compared. For the check,
            `nums.count(candidate)` is one fast pass. `collections.Counter(nums).most_common(1)` also works but uses
            O(n) memory, which is usually the thing you were asked to avoid.

            ### Java

            With `int[]` comparisons are plain `==`. If you ever hold the candidate in an `Integer` (say from a
            `List<Integer>`), compare with `.equals`, since `==` on boxed values above 127 compares objects, not numbers.

            ### C++

            `std::count(nums.begin(), nums.end(), candidate)` does the check in one line. Compare `2 * count > n` with
            `count` and `n` as `int` or wider; for very large inputs, `long long` avoids overflow.

            ### C

            The same loop with an explicit length. Nothing to allocate, nothing to free.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Skipping the check when a majority isn't promised. The candidate of `[1, 2, 3]` is 3.
            - Comparing before taking over. If you compare first and only then reset on `count == 0`, the new candidate
              doesn't get its own vote.
            - `>= n / 2` instead of `> n / 2`. With `n = 4`, a value appearing twice is not a majority.
            - Integer division: `count > n / 2` with `n = 5` means `count > 2`, which is right, but it's easy to slip.
              `2 * count > n` says what you mean.
            - Expecting the mode. Boyer-Moore says nothing about the most common value when no majority exists.
            - With several slots, letting one value occupy two slots, or letting the crossed-out value take a slot.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why can't the true majority be the value that runs out?",
                 "Each cancellation removes two different values, so at most one of them is the majority. If it has more than half, it has more copies than everything else combined, and every other value can cancel at most one of its copies."),
                (f"What does the candidate pass return for {MODE}, and is it the answer to anything?",
                 "It returns 4. No value has more than half of the 5 entries, so 4 isn't a majority (and isn't the most common value either). A check would say there's no majority."),
                ("When is the second counting pass not needed?",
                 "When the problem promises that a majority exists. Then the candidate must be it."),
                ("How many slots do you need to find every value appearing more than n / 4 times, and why?",
                 "Three. At most three values can each have more than a quarter of the array, and each full-slots round crosses out four different values, which can happen at most n / 4 times, so a value with more than n / 4 copies survives."),
                ("In equi_leaders, why is it enough to only consider the leader of the whole array?",
                 "If one value is a strict majority of both parts, it has more than half of each, so more than half of the total. Any value that leads both sides must lead the whole array."),
            ),
        ]),
    ],
)
