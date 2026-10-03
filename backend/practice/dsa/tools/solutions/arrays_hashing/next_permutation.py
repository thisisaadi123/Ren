"""Arrays & Hashing: next permutation."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def next_perm(d):
    d = list(d)
    i = len(d) - 2
    while i >= 0 and d[i] >= d[i + 1]:
        i -= 1
    if i < 0:
        return None
    j = len(d) - 1
    while d[j] <= d[i]:
        j -= 1
    d[i], d[j] = d[j], d[i]
    d[i + 1:] = reversed(d[i + 1:])
    return d


def pivot_walk(W, d, word="digit", reverse_label="reverse the suffix"):
    """Record the pivot / swap / reverse steps of next permutation on list d."""
    d = list(d)
    n = len(d)
    W.step(f"Scan from the right while each {word} is ≥ the one after it: that tail is already as large as it can be.", Row(d, slots=True))
    i = n - 2
    while i >= 0 and d[i] >= d[i + 1]:
        W.step(f"{d[i]} ≥ {d[i + 1]}: still descending, keep going left.", Row(d, st={k: "dim" for k in range(i + 1, n)} | {i: "active"}, slots=True))
        i -= 1
    W.step(f"{d[i]} < {d[i + 1]}: index {i} is the pivot. Everything after it is descending.", Row(d, st={k: "found" for k in range(i + 1, n)} | {i: "mark"}, ptr={"pivot": i}, slots=True))
    j = n - 1
    while d[j] <= d[i]:
        j -= 1
    W.step(f"The rightmost {word} in the tail that is bigger than {d[i]} is {d[j]} (index {j}). Swap them.", Row(d, st={i: "mark", j: "answer"}, ptr={"pivot": i, "j": j}, slots=True))
    d[i], d[j] = d[j], d[i]
    W.step(f"After the swap the tail is still descending: {d[i + 1:]}.", Row(d, st={k: "found" for k in range(i + 1, n)} | {i: "new"}, slots=True))
    d[i + 1:] = reversed(d[i + 1:])
    W.step(f"Now {reverse_label} to make it as small as possible.", Row(d, st={k: "new" for k in range(i + 1, n)}, slots=True))
    return d


@problem
def next_badge_number():
    code = "158476531"
    want = "".join(next_perm(code))
    assert want == "158513467"

    w1 = Steps("List the arrangements of the digits in increasing order and stop at the first one larger than the code.")
    small = "1243"
    from itertools import permutations
    perms = sorted(set("".join(p) for p in permutations(small)))
    for p in perms:
        if p > small:
            w1.step(f"{p} > {small}: this is the answer.", Row(list(p), st={k: "answer" for k in range(len(p))}), result=p)
            break
        w1.step(f"{p} is not larger than {small}" + (" (it is the code itself)." if p == small else "."), Row(list(p), st={k: "dim" for k in range(len(p))}))
    w1.steps.insert(0, {"text": f"A smaller example, code = {small}: its digits 1, 2, 3, 4 have {len(perms)} arrangements, generated smallest first.", "panels": [Row(list(small))]})

    w2 = Steps("Find the pivot, swap in the smallest larger digit from the tail, then sort the tail ascending.")
    d = list(code)
    i = len(d) - 2
    while d[i] >= d[i + 1]:
        i -= 1
    w2.step(f"Scanning from the right, the tail {''.join(d[i + 1:])} never increases; the first digit that breaks it is {d[i]} at index {i}: the pivot.", Row(d, st={k: "found" for k in range(i + 1, len(d))} | {i: "mark"}, ptr={"pivot": i}, slots=True))
    bigger = [k for k in range(i + 1, len(d)) if d[k] > d[i]]
    j = min(bigger, key=lambda k: (d[k], -k))
    w2.step(f"In the tail, the smallest digit larger than {d[i]} is {d[j]}. Swap them.", Row(d, st={i: "mark", j: "answer"}, slots=True))
    d[i], d[j] = d[j], d[i]
    w2.step("Sort the tail ascending: the smallest possible ending.", Row(d[:i + 1] + sorted(d[i + 1:]), st={k: "new" for k in range(i + 1, len(d))}, slots=True), result="".join(d[:i + 1] + sorted(d[i + 1:])))

    w3 = Steps("Pivot, swap with the rightmost larger digit, reverse the tail.")
    res = pivot_walk(w3, code)
    w3.steps[-1]["result"] = "".join(res)

    sol(
        "next-badge-number",
        summary="""
            To make the next larger number from the same digits, change as little as possible, as far right as
            possible. Find the rightmost digit that has a larger digit after it (the pivot), swap it with the smallest
            such larger digit, and arrange everything after it in increasing order. Because that tail is always in
            decreasing order, "arrange increasing" is just a reversal: O(n).
        """,
        question=[
            """
            Rearrange the digits of `code` into the **smallest number larger than `code`**, using every digit exactly
            as often as it appears. Return `""` if no rearrangement is larger.

            - **Same multiset of digits:** `"115"` can become `"151"` or `"511"`; the next larger is `"151"`.
            - **No answer** when the digits are already in decreasing order (`"4321"` is the largest arrangement).
            - **Same length**, so comparing as strings is the same as comparing as numbers. Leading zeros can't
              appear in the answer: anything starting with 0 is smaller than `code`.
            - **Up to 10⁵ digits:** far beyond any integer type, so work on the characters. Trying all arrangements
              is out of the question.
            """
        ],
        think=[
            """
            Take `code = "158476531"`. To grow a number by the smallest amount, change it as far to the **right** as
            possible, because changing an earlier digit makes a bigger jump.

            Look at the tail from the right: 1, 3, 5, 6, 7 read leftwards keep increasing, i.e. the tail `76531`
            is in **decreasing** order. A decreasing tail is already the largest arrangement of its digits; no
            reshuffle of `76531` alone can grow the number. So the change has to involve the digit just before it:
            the **4** (index 3), the pivot.
            """,
            fig(Row(list(code), st={3: "mark"} | {k: "found" for k in range(4, 9)}, slots=True),
                caption="The tail 7 6 5 3 1 is decreasing. The pivot is 4, the first digit that is smaller than the one after it."),
            """
            Now make the pivot position grow by as little as possible: replace 4 with the **smallest digit in the
            tail that is bigger than 4**, which is 5. That gives `1585…` with the leftover digits 7, 6, 4, 3, 1. To
            make the result as small as possible, put those in increasing order: `13467`. Answer: `158513467`.

            One more observation saves a sort: after swapping 4 and 5, the tail `76431` is **still decreasing** (5
            was the smallest digit above 4, so 4 slots into the same position). Reversing a decreasing sequence makes
            it increasing, so the "sort" is just a reversal.
            """,
        ],
        approaches=[
            approach(
                "Generate arrangements in order",
                "brute",
                "O(n! · n)",
                "O(n)",
                idea=["Build arrangements of the digits recursively, always trying smaller digits first, so they come out in increasing order. The first complete arrangement that is larger than `code` is the answer. Counting how many of each digit is left (10 counters) avoids generating duplicates."],
                walk=w1,
                build=["Count the digits.", "Recursively fill positions left to right, trying digits 0 … 9 that still have copies.", "When all positions are filled, compare with `code`; return the first arrangement that's larger.", "If none is, return `\"\"`."],
                code={
                    "python": """
                        class Solution:
                            def nextBadge(self, code: str) -> str:
                                count = [0] * 10  #@count
                                for ch in code:  #@count
                                    count[ord(ch) - 48] += 1  #@count
                                buf = []  #@build
                                def build():  #@build
                                    if len(buf) == len(code):  #@full
                                        s = "".join(buf)  #@full
                                        return s if s > code else None  #@full
                                    for d in range(10):  #@try
                                        if count[d]:  #@try
                                            count[d] -= 1  #@try
                                            buf.append(chr(48 + d))  #@try
                                            found = build()  #@try
                                            buf.pop()  #@undo
                                            count[d] += 1  #@undo
                                            if found:  #@undo
                                                return found  #@undo
                                    return None  #@build
                                return build() or ""  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int[] count = new int[10];  //@count
                            private char[] buf;  //@build
                            private String code;  //@build

                            public String nextBadge(String code) {
                                this.code = code;  //@build
                                buf = new char[code.length()];  //@build
                                for (char ch : code.toCharArray()) count[ch - '0']++;  //@count
                                String found = build(0);  //@ret
                                return found == null ? "" : found;  //@ret
                            }

                            private String build(int pos) {  //@build
                                if (pos == buf.length) {  //@full
                                    String s = new String(buf);  //@full
                                    return s.compareTo(code) > 0 ? s : null;  //@full
                                }
                                for (int d = 0; d < 10; d++) {  //@try
                                    if (count[d] == 0) continue;  //@try
                                    count[d]--;  //@try
                                    buf[pos] = (char) ('0' + d);  //@try
                                    String found = build(pos + 1);  //@try
                                    count[d]++;  //@undo
                                    if (found != null) return found;  //@undo
                                }
                                return null;  //@build
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            int count[10] = {0};  //@count
                            string buf, code;  //@build

                            bool build(size_t pos) {  //@build
                                if (pos == buf.size()) return buf > code;  //@full
                                for (int d = 0; d < 10; d++) {  //@try
                                    if (!count[d]) continue;  //@try
                                    count[d]--;  //@try
                                    buf[pos] = '0' + d;  //@try
                                    bool found = build(pos + 1);  //@try
                                    count[d]++;  //@undo
                                    if (found) return true;  //@undo
                                }
                                return false;  //@build
                            }

                        public:
                            string nextBadge(string& code) {
                                this->code = code;  //@build
                                buf.assign(code.size(), '0');  //@build
                                for (char ch : code) count[ch - '0']++;  //@count
                                return build(0) ? buf : "";  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int count[10];  //@count
                        static char* buf;  //@build
                        static const char* target;  //@build
                        static int len;  //@build

                        static bool build(int pos) {  //@build
                            if (pos == len) return strcmp(buf, target) > 0;  //@full
                            for (int d = 0; d < 10; d++) {  //@try
                                if (!count[d]) continue;  //@try
                                count[d]--;  //@try
                                buf[pos] = '0' + d;  //@try
                                bool found = build(pos + 1);  //@try
                                count[d]++;  //@undo
                                if (found) return true;  //@undo
                            }
                            return false;  //@build
                        }

                        char* nextBadge(char* code) {
                            len = strlen(code);  //@build
                            target = code;  //@build
                            buf = calloc(len + 1, 1);  //@build
                            memset(count, 0, sizeof count);  //@count
                            for (int i = 0; i < len; i++) count[code[i] - '0']++;  //@count
                            if (!build(0)) buf[0] = '\\0';  //@ret
                            return buf;  //@ret
                        }
                    """,
                },
                lines=[
                    ("count", "How many copies of each digit are still available to place."),
                    ("build", "Recursive builder: fills positions left to right in a shared buffer.", {"c": "The buffer, the target and the length are file-level so the recursive helper can reach them; `calloc` leaves room for the terminating `\\0`."}),
                    ("full", "A complete arrangement: is it larger than the code? Same length, so string comparison is numeric comparison."),
                    ("try", "Try each available digit in increasing order at this position and recurse. Trying small digits first is what makes arrangements appear in increasing order."),
                    ("undo", "Give the digit back before trying the next one. If a deeper call already found the answer, stop immediately."),
                    ("ret", "The first larger arrangement, or empty if there is none.", {"c": "On failure, turn the buffer into the empty string."}),
                ],
                complexity=["**Time O(n! · n)** in the worst case: every arrangement up to the answer is built (each costs O(n) to compare). **Space O(n)** for the recursion and buffer. Hopeless beyond about 10 digits."],
                limits=["Almost all of the work generates arrangements *smaller* than the code. The answer is determined by a local change near the right end, which can be found directly."],
                slow=19,
            ),
            approach(
                "Pivot, swap, then sort the tail",
                "better",
                "O(n log n)",
                "O(n)",
                idea=[
                    """
                    1. **Pivot:** scan from the right for the first index `i` with `d[i] < d[i + 1]`. If there is none,
                       the digits are in decreasing order and no larger arrangement exists.
                    2. **Swap:** in the tail after `i`, find the smallest digit that is larger than `d[i]` and swap them.
                    3. **Sort the tail ascending**, making the end as small as possible.
                    """
                ],
                walk=w2,
                build=["Copy the digits into a mutable array.", "Find the pivot from the right; return `\"\"` if none.", "Find the smallest digit in the tail that's larger than the pivot (taking the rightmost of equal ones); swap.", "Sort the tail ascending and return."],
                code={
                    "python": """
                        class Solution:
                            def nextBadge(self, code: str) -> str:
                                d = list(code)  #@copy
                                i = len(d) - 2  #@pivot
                                while i >= 0 and d[i] >= d[i + 1]:  #@pivot
                                    i -= 1  #@pivot
                                if i < 0:  #@none
                                    return ""  #@none
                                j = min((k for k in range(i + 1, len(d)) if d[k] > d[i]), key=lambda k: d[k])  #@swap
                                d[i], d[j] = d[j], d[i]  #@swap
                                d[i + 1:] = sorted(d[i + 1:])  #@sort
                                return "".join(d)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String nextBadge(String code) {
                                char[] d = code.toCharArray();  //@copy
                                int i = d.length - 2;  //@pivot
                                while (i >= 0 && d[i] >= d[i + 1]) i--;  //@pivot
                                if (i < 0) return "";  //@none
                                int j = -1;  //@swap
                                for (int k = i + 1; k < d.length; k++)  //@swap
                                    if (d[k] > d[i] && (j < 0 || d[k] < d[j])) j = k;  //@swap
                                char t = d[i]; d[i] = d[j]; d[j] = t;  //@swap
                                Arrays.sort(d, i + 1, d.length);  //@sort
                                return new String(d);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string nextBadge(string& code) {
                                string d = code;  //@copy
                                int i = (int) d.size() - 2;  //@pivot
                                while (i >= 0 && d[i] >= d[i + 1]) i--;  //@pivot
                                if (i < 0) return "";  //@none
                                int j = -1;  //@swap
                                for (int k = i + 1; k < (int) d.size(); k++)  //@swap
                                    if (d[k] > d[i] && (j < 0 || d[k] < d[j])) j = k;  //@swap
                                swap(d[i], d[j]);  //@swap
                                sort(d.begin() + i + 1, d.end());  //@sort
                                return d;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpChar(const void* a, const void* b) {  //@sort
                            return *(const char*) a - *(const char*) b;  //@sort
                        }  //@sort

                        char* nextBadge(char* code) {
                            int n = strlen(code);
                            char* d = malloc(n + 1);  //@copy
                            memcpy(d, code, n + 1);  //@copy
                            int i = n - 2;  //@pivot
                            while (i >= 0 && d[i] >= d[i + 1]) i--;  //@pivot
                            if (i < 0) { d[0] = '\\0'; return d; }  //@none
                            int j = -1;  //@swap
                            for (int k = i + 1; k < n; k++)  //@swap
                                if (d[k] > d[i] && (j < 0 || d[k] < d[j])) j = k;  //@swap
                            char t = d[i]; d[i] = d[j]; d[j] = t;  //@swap
                            qsort(d + i + 1, n - i - 1, 1, cmpChar);  //@sort
                            return d;  //@ret
                        }
                    """,
                },
                lines=[
                    ("copy", "A mutable copy of the digits."),
                    ("pivot", "From the right, skip while the digits don't increase going leftwards. The first digit smaller than its right neighbour is the pivot: the rightmost place where the number can grow."),
                    ("none", "No pivot: the whole number is in decreasing order, the largest arrangement.", {"c": "Return an empty string (the caller frees it)."}),
                    ("swap", "Bring in the smallest tail digit that is still larger than the pivot. That raises this position by the least possible amount."),
                    ("sort", "Everything after the pivot should now be as small as possible: ascending order."),
                    ("ret", "The next larger arrangement."),
                ],
                complexity=["**Time O(n log n)** because of the sort (the scans are O(n)). **Space O(n)** for the copy."],
                limits=["The sort ignores something we already know: the tail was in decreasing order before the swap and still is after it. Reversing a decreasing sequence sorts it in O(n)."],
            ),
            approach(
                "Pivot, swap, reverse the tail",
                "best",
                "O(n)",
                "O(n)",
                idea=[
                    """
                    Same three steps, using the fact that the tail is **decreasing**:

                    - The smallest digit larger than the pivot is the **rightmost** tail digit larger than the pivot:
                      scan from the end until you find one.
                    - After the swap the tail is still decreasing (the new digit takes the old one's place in the order),
                      so **reversing** it gives ascending order.
                    """
                ],
                walk=w3,
                build=["Find the pivot `i` from the right; return `\"\"` if none.", "Scan `j` from the end while `d[j] ≤ d[i]`; swap `d[i]` and `d[j]`.", "Reverse `d[i + 1 …]` with two pointers.", "Return the digits as a string."],
                code={
                    "python": """
                        class Solution:
                            def nextBadge(self, code: str) -> str:
                                d = list(code)  #@copy
                                i = len(d) - 2  #@pivot
                                while i >= 0 and d[i] >= d[i + 1]:  #@pivot
                                    i -= 1  #@pivot
                                if i < 0:  #@none
                                    return ""  #@none
                                j = len(d) - 1  #@swap
                                while d[j] <= d[i]:  #@swap
                                    j -= 1  #@swap
                                d[i], d[j] = d[j], d[i]  #@swap
                                d[i + 1:] = reversed(d[i + 1:])  #@rev
                                return "".join(d)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String nextBadge(String code) {
                                char[] d = code.toCharArray();  //@copy
                                int i = d.length - 2;  //@pivot
                                while (i >= 0 && d[i] >= d[i + 1]) i--;  //@pivot
                                if (i < 0) return "";  //@none
                                int j = d.length - 1;  //@swap
                                while (d[j] <= d[i]) j--;  //@swap
                                char t = d[i]; d[i] = d[j]; d[j] = t;  //@swap
                                for (int a = i + 1, b = d.length - 1; a < b; a++, b--) {  //@rev
                                    t = d[a]; d[a] = d[b]; d[b] = t;  //@rev
                                }
                                return new String(d);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string nextBadge(string& code) {
                                string d = code;  //@copy
                                int i = (int) d.size() - 2;  //@pivot
                                while (i >= 0 && d[i] >= d[i + 1]) i--;  //@pivot
                                if (i < 0) return "";  //@none
                                int j = d.size() - 1;  //@swap
                                while (d[j] <= d[i]) j--;  //@swap
                                swap(d[i], d[j]);  //@swap
                                reverse(d.begin() + i + 1, d.end());  //@rev
                                return d;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* nextBadge(char* code) {
                            int n = strlen(code);
                            char* d = malloc(n + 1);  //@copy
                            memcpy(d, code, n + 1);  //@copy
                            int i = n - 2;  //@pivot
                            while (i >= 0 && d[i] >= d[i + 1]) i--;  //@pivot
                            if (i < 0) { d[0] = '\\0'; return d; }  //@none
                            int j = n - 1;  //@swap
                            while (d[j] <= d[i]) j--;  //@swap
                            char t = d[i]; d[i] = d[j]; d[j] = t;  //@swap
                            for (int a = i + 1, b = n - 1; a < b; a++, b--) {  //@rev
                                t = d[a]; d[a] = d[b]; d[b] = t;  //@rev
                            }
                            return d;  //@ret
                        }
                    """,
                },
                lines=[
                    ("copy", "A mutable copy."),
                    ("pivot", "The first digit from the right that is smaller than its right neighbour."),
                    ("none", "Fully decreasing: no larger arrangement.", {"c": "Return an empty string."}),
                    ("swap", "The tail is decreasing, so scanning from the far right, the first digit larger than the pivot is the smallest such digit. Swap it in. `j` always stops inside the tail, because `d[i + 1] > d[i]`."),
                    ("rev", "The tail is still decreasing after the swap; reversing it makes it the smallest arrangement of those digits."),
                    ("ret", "The next larger number."),
                ],
                complexity=["**Time O(n):** at most three linear scans. **Space O(n)** for the mutable copy (O(1) extra if the input could be modified)."],
            ),
        ],
        takeaways=[
            """
            - **Next permutation:** pivot = rightmost `a[i] < a[i + 1]`; swap with the rightmost element larger than
              it; reverse the suffix. No pivot means it's the last permutation.
            - A suffix that never increases is already at its maximum; growth must happen just before it.
            - Knowing a range is sorted (here, descending) often turns a sort into a reversal.
            """
        ],
    )


@problem
def next_mirror_number():
    code = "1323231"
    n = len(code)
    half = code[:n // 2]
    nh = next_perm(half)
    left = "".join(nh)
    want = left + code[n // 2:(n + 1) // 2] + left[::-1]
    assert want == "2133312"

    w1 = Steps("List arrangements of the left half in increasing order; the first one larger than the current half gives the answer.")
    from itertools import permutations
    perms = sorted(set("".join(p) for p in permutations(half)))
    w1.step(f"code = {code}. The left half is {half}; the middle digit is {code[n // 2]}. Arrangements of {half}, smallest first:", Row(list(code), st={k: "mark" for k in range(n // 2)}, slots=True))
    for p in perms:
        if p > half:
            w1.step(f"{p} > {half}: mirror it → {p + code[n // 2] + p[::-1]}.", Row(list(p + code[n // 2] + p[::-1]), st={k: "answer" for k in range(n // 2)}), result=p + code[n // 2] + p[::-1])
            break
        w1.step(f"{p}: not larger than {half}.", Row(list(p), st={k: "dim" for k in range(len(p))}))

    w2 = Steps("Run next permutation on the left half only, then mirror it.")
    w2.step(f"A mirror number is fixed by its left half ({half}) and middle ({code[n // 2]}). Make the left half the next larger arrangement.", Row(list(code), st={k: "mark" for k in range(n // 2)}, slots=True))
    res = pivot_walk(w2, half)
    w2.step(f"Mirror the new half around the middle: {left} + {code[n // 2]} + {left[::-1]}.", Row(list(want), st={k: "new" for k in range(n // 2)} | {k: "found" for k in range((n + 1) // 2, n)}, slots=True), result=want)

    sol(
        "next-mirror-number",
        summary="""
            A mirror number is completely determined by its **left half** (and the middle digit, if the length is odd,
            which can never move). Making the smallest larger mirror number therefore means making the smallest
            larger arrangement of the left half, which is exactly next permutation, then mirroring it. O(n).
        """,
        question=[
            """
            `code` reads the same forwards and backwards. Rearrange its digits into the **smallest larger** number that
            also reads the same both ways, or return `""`.

            - **The result must be a mirror number too**, using exactly the same digits.
            - **Odd length:** exactly one digit value appears an odd number of times, and one copy of it must sit
              in the middle. So the middle digit never changes.
            - **No answer** when the left half is already in decreasing order: `"32123"` has left half `"32"`, the
              largest arrangement of 3 and 2.
            - **Up to 10⁵ digits**, so trying arrangements is out.
            """
        ],
        think=[
            """
            Take `code = "1323231"` (7 digits). Its left half is `132`, the middle is `3`, and the right half is
            just `132` reversed.

            Any mirror number made from these digits also has a left half, middle and mirrored right half. Its middle
            must be 3 (the only digit with an odd count), and its left half must use the remaining digits split
            evenly: one 1, one 2 and one 3. So mirror numbers from these digits correspond one-to-one with
            arrangements of `{1, 2, 3}` for the left half.
            """,
            fig(Row(list(code), st={0: "mark", 1: "mark", 2: "mark", 3: "found", 4: "dim", 5: "dim", 6: "dim"}, slots=True),
                caption="Left half (dark) decides everything; the middle (light) is fixed; the right half is the mirror image."),
            """
            And the order matches too: comparing two mirror numbers, the first difference appears in the left half
            (the middles are equal, and the right halves only repeat the left). So the **next larger mirror number**
            comes from the **next larger left half**: `132` → `213`, giving `213` + `3` + `312` = `2133312`.
            """,
        ],
        approaches=[
            approach(
                "Generate left halves in order",
                "brute",
                "O(h! · h)",
                "O(h)",
                idea=["Generate arrangements of the left half's digits in increasing order (recursively, smallest digit first, with digit counts to avoid duplicates). The first one larger than the current left half is the new left half; mirror it. If none exists, return `\"\"`."],
                walk=w1,
                build=["Take the left half `h = code[0 … n/2 − 1]` and count its digits.", "Build arrangements recursively, trying digits 0 … 9 in order.", "Return the first arrangement larger than `h`, mirrored around the middle.", "If none, return `\"\"`."],
                code={
                    "python": """
                        class Solution:
                            def nextMirror(self, code: str) -> str:
                                n = len(code)
                                half = code[:n // 2]  #@half
                                count = [0] * 10  #@half
                                for ch in half:  #@half
                                    count[ord(ch) - 48] += 1  #@half
                                buf = []
                                def build():  #@gen
                                    if len(buf) == len(half):  #@gen
                                        s = "".join(buf)  #@gen
                                        return s if s > half else None  #@gen
                                    for d in range(10):  #@gen
                                        if count[d]:  #@gen
                                            count[d] -= 1  #@gen
                                            buf.append(chr(48 + d))  #@gen
                                            found = build()  #@gen
                                            buf.pop()  #@gen
                                            count[d] += 1  #@gen
                                            if found:  #@gen
                                                return found  #@gen
                                    return None  #@gen
                                left = build()  #@mirror
                                if left is None:  #@mirror
                                    return ""  #@mirror
                                return left + code[n // 2:(n + 1) // 2] + left[::-1]  #@mirror
                    """,
                    "java": """
                        class Solution {
                            private int[] count = new int[10];
                            private char[] buf;
                            private String half;

                            public String nextMirror(String code) {
                                int n = code.length();
                                half = code.substring(0, n / 2);  //@half
                                for (char ch : half.toCharArray()) count[ch - '0']++;  //@half
                                buf = new char[half.length()];  //@half
                                if (!build(0)) return "";  //@mirror
                                String left = new String(buf);  //@mirror
                                return left + code.substring(n / 2, (n + 1) / 2) + new StringBuilder(left).reverse();  //@mirror
                            }

                            private boolean build(int pos) {  //@gen
                                if (pos == buf.length) return new String(buf).compareTo(half) > 0;  //@gen
                                for (int d = 0; d < 10; d++) {  //@gen
                                    if (count[d] == 0) continue;  //@gen
                                    count[d]--;  //@gen
                                    buf[pos] = (char) ('0' + d);  //@gen
                                    boolean found = build(pos + 1);  //@gen
                                    count[d]++;  //@gen
                                    if (found) return true;  //@gen
                                }
                                return false;  //@gen
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            int count[10] = {0};
                            string buf, half;

                            bool build(size_t pos) {  //@gen
                                if (pos == buf.size()) return buf > half;  //@gen
                                for (int d = 0; d < 10; d++) {  //@gen
                                    if (!count[d]) continue;  //@gen
                                    count[d]--;  //@gen
                                    buf[pos] = '0' + d;  //@gen
                                    bool found = build(pos + 1);  //@gen
                                    count[d]++;  //@gen
                                    if (found) return true;  //@gen
                                }
                                return false;  //@gen
                            }

                        public:
                            string nextMirror(string& code) {
                                int n = code.size();
                                half = code.substr(0, n / 2);  //@half
                                for (char ch : half) count[ch - '0']++;  //@half
                                buf.assign(half.size(), '0');  //@half
                                if (!build(0)) return "";  //@mirror
                                string right(buf.rbegin(), buf.rend());  //@mirror
                                return buf + code.substr(n / 2, n % 2) + right;  //@mirror
                            }
                        };
                    """,
                    "c": """
                        static int count[10];
                        static char* buf;
                        static char* half;
                        static int h;

                        static bool build(int pos) {  //@gen
                            if (pos == h) return strcmp(buf, half) > 0;  //@gen
                            for (int d = 0; d < 10; d++) {  //@gen
                                if (!count[d]) continue;  //@gen
                                count[d]--;  //@gen
                                buf[pos] = '0' + d;  //@gen
                                bool found = build(pos + 1);  //@gen
                                count[d]++;  //@gen
                                if (found) return true;  //@gen
                            }
                            return false;  //@gen
                        }

                        char* nextMirror(char* code) {
                            int n = strlen(code);
                            h = n / 2;  //@half
                            half = calloc(h + 1, 1);  //@half
                            memcpy(half, code, h);  //@half
                            buf = calloc(h + 1, 1);  //@half
                            memset(count, 0, sizeof count);  //@half
                            for (int i = 0; i < h; i++) count[half[i] - '0']++;  //@half
                            char* out = calloc(n + 1, 1);  //@mirror
                            if (build(0)) {  //@mirror
                                memcpy(out, buf, h);  //@mirror
                                if (n % 2) out[h] = code[h];  //@mirror
                                for (int i = 0; i < h; i++) out[n - 1 - i] = buf[i];  //@mirror
                            }
                            free(half);  //@mirror
                            free(buf);  //@mirror
                            return out;  //@mirror
                        }
                    """,
                },
                lines=[
                    ("half", "The left half determines the whole mirror number; count its digits for the generator."),
                    ("gen", "Recursive generator: fills the half left to right, smallest available digit first, so arrangements appear in increasing order; returns at the first one larger than the current half (equal length, so string order is numeric order)."),
                    ("mirror", "Glue the new left half, the unchanged middle digit (if any) and the reversed left half. If no larger half exists, there's no answer."),
                ],
                complexity=["**Time O(h! · h)** for a half of length h = n/2. **Space O(h).** Only feasible for very short codes."],
                limits=["Nearly all generated halves are smaller than the current one. The next larger half can be computed directly with the next-permutation steps."],
                slow=24,
            ),
            approach(
                "Next permutation of the left half, then mirror",
                "best",
                "O(n)",
                "O(n)",
                idea=[
                    """
                    Apply next permutation to the left half: find the pivot (rightmost `h[i] < h[i + 1]`), swap it with
                    the rightmost larger digit after it, reverse the tail. If there's no pivot, the half is already its
                    largest arrangement and there is no answer. Otherwise the answer is
                    `newHalf + middle + reverse(newHalf)`.
                    """
                ],
                walk=w2,
                build=["Copy the left half `code[0 … n/2 − 1]`.", "Find the pivot from the right; return `\"\"` if none.", "Swap with the rightmost larger digit; reverse the tail.", "Return `half + middle + reversed half`."],
                code={
                    "python": """
                        class Solution:
                            def nextMirror(self, code: str) -> str:
                                n = len(code)
                                h = list(code[:n // 2])  #@half
                                i = len(h) - 2  #@pivot
                                while i >= 0 and h[i] >= h[i + 1]:  #@pivot
                                    i -= 1  #@pivot
                                if i < 0:  #@none
                                    return ""  #@none
                                j = len(h) - 1  #@swap
                                while h[j] <= h[i]:  #@swap
                                    j -= 1  #@swap
                                h[i], h[j] = h[j], h[i]  #@swap
                                h[i + 1:] = reversed(h[i + 1:])  #@rev
                                left = "".join(h)  #@mirror
                                return left + code[n // 2:(n + 1) // 2] + left[::-1]  #@mirror
                    """,
                    "java": """
                        class Solution {
                            public String nextMirror(String code) {
                                int n = code.length();
                                char[] h = code.substring(0, n / 2).toCharArray();  //@half
                                int i = h.length - 2;  //@pivot
                                while (i >= 0 && h[i] >= h[i + 1]) i--;  //@pivot
                                if (i < 0) return "";  //@none
                                int j = h.length - 1;  //@swap
                                while (h[j] <= h[i]) j--;  //@swap
                                char t = h[i]; h[i] = h[j]; h[j] = t;  //@swap
                                for (int a = i + 1, b = h.length - 1; a < b; a++, b--) { t = h[a]; h[a] = h[b]; h[b] = t; }  //@rev
                                String left = new String(h);  //@mirror
                                return left + code.substring(n / 2, (n + 1) / 2) + new StringBuilder(left).reverse();  //@mirror
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string nextMirror(string& code) {
                                int n = code.size();
                                string h = code.substr(0, n / 2);  //@half
                                int i = (int) h.size() - 2;  //@pivot
                                while (i >= 0 && h[i] >= h[i + 1]) i--;  //@pivot
                                if (i < 0) return "";  //@none
                                int j = h.size() - 1;  //@swap
                                while (h[j] <= h[i]) j--;  //@swap
                                swap(h[i], h[j]);  //@swap
                                reverse(h.begin() + i + 1, h.end());  //@rev
                                string right(h.rbegin(), h.rend());  //@mirror
                                return h + code.substr(n / 2, n % 2) + right;  //@mirror
                            }
                        };
                    """,
                    "c": """
                        char* nextMirror(char* code) {
                            int n = strlen(code), m = n / 2;
                            char* out = calloc(n + 1, 1);  //@half
                            memcpy(out, code, m);  //@half
                            int i = m - 2;  //@pivot
                            while (i >= 0 && out[i] >= out[i + 1]) i--;  //@pivot
                            if (i < 0) { out[0] = '\\0'; return out; }  //@none
                            int j = m - 1;  //@swap
                            while (out[j] <= out[i]) j--;  //@swap
                            char t = out[i]; out[i] = out[j]; out[j] = t;  //@swap
                            for (int a = i + 1, b = m - 1; a < b; a++, b--) { t = out[a]; out[a] = out[b]; out[b] = t; }  //@rev
                            if (n % 2) out[m] = code[m];  //@mirror
                            for (int k = 0; k < m; k++) out[n - 1 - k] = out[k];  //@mirror
                            return out;  //@mirror
                        }
                    """,
                },
                lines=[
                    ("half", "Work on a copy of the left half only.", {"c": "Build the answer directly in the output buffer: its first n/2 characters are the half."}),
                    ("pivot", "Rightmost position in the half where a digit is smaller than its right neighbour."),
                    ("none", "The half is in decreasing order: it's already the largest arrangement, so no larger mirror number exists.", {"c": "Return an empty string."}),
                    ("swap", "Swap the pivot with the rightmost (= smallest) larger digit after it."),
                    ("rev", "Reverse the tail into ascending order: the smallest ending."),
                    ("mirror", "Middle digit unchanged (only for odd lengths), then the half reversed.", {"python": "`code[n // 2:(n + 1) // 2]` is the middle character for odd n and empty for even n.", "cpp": "`substr(n / 2, n % 2)` is the middle character for odd n and empty for even n."}),
                ],
                complexity=["**Time O(n).** **Space O(n)** for the output."],
            ),
        ],
        takeaways=[
            """
            - A palindrome is defined by its first half (plus a fixed middle). Reduce palindrome problems to the half.
            - Ordering palindromes by value = ordering their halves, so "next larger palindrome with the same digits"
              is next permutation of the half.
            - Reuse proven building blocks (next permutation) instead of reinventing them.
            """
        ],
    )


@problem
def one_step_back():
    a = [1, 5, 8, 4, 1, 3, 5, 6, 7]

    def prev_perm(x):
        x = list(x)
        i = len(x) - 2
        while i >= 0 and x[i] <= x[i + 1]:
            i -= 1
        if i < 0:
            return x[::-1]
        j = len(x) - 1
        while x[j] >= x[i]:
            j -= 1
        x[i], x[j] = x[j], x[i]
        x[i + 1:] = x[i + 1:][::-1]
        return x

    want = prev_perm(a)
    assert want == [1, 5, 8, 3, 7, 6, 5, 4, 1]

    w1 = Steps("List the orderings from largest to smallest; the first one smaller than the current ordering is the answer.")
    from itertools import permutations
    small = [3, 1, 1]
    perms = sorted(set(permutations(small)), reverse=True)
    w1.step(f"A small case, {small}: its distinct orderings, largest first.", Row(small))
    for p in perms:
        if list(p) < small:
            w1.step(f"{list(p)} < {small}: the previous ordering.", Row(list(p), st={k: "answer" for k in range(3)}), result=list(p))
            break
        w1.step(f"{list(p)}: not smaller.", Row(list(p), st={k: "dim" for k in range(3)}))

    w2 = Steps("Mirror of next permutation: pivot is the rightmost a[i] > a[i + 1]; swap with the rightmost smaller value; reverse the tail.")
    x = list(a)
    n = len(x)
    i = n - 2
    while x[i] <= x[i + 1]:
        w2.step(f"{x[i]} ≤ {x[i + 1]}: the tail is still ascending (already the smallest arrangement of its values). Move left.", Row(x, st={k: "dim" for k in range(i + 1, n)} | {i: "active"}, slots=True))
        i -= 1
    w2.step(f"{x[i]} > {x[i + 1]}: pivot at index {i}. The tail after it is ascending.", Row(x, st={k: "found" for k in range(i + 1, n)} | {i: "mark"}, ptr={"pivot": i}, slots=True))
    j = n - 1
    while x[j] >= x[i]:
        j -= 1
    w2.step(f"The rightmost tail value smaller than {x[i]} is {x[j]} (the largest one below it). Swap.", Row(x, st={i: "mark", j: "answer"}, slots=True))
    x[i], x[j] = x[j], x[i]
    x[i + 1:] = x[i + 1:][::-1]
    w2.step("Reverse the tail into descending order: the largest ending, so this is the ordering just before.", Row(x, st={k: "new" for k in range(i + 1, n)}, slots=True), result=x)

    sol(
        "one-step-back",
        summary="""
            "The ordering just before" is the **previous permutation**: the mirror image of next permutation. Find
            the rightmost position where a value is bigger than the one after it, swap it with the largest smaller
            value to its right, and reverse the tail into descending order. If no such position exists, the input is
            the first ordering, and the answer wraps around to the last (descending) one. O(n).
        """,
        question=[
            """
            Among all distinct orderings of the ratings, sorted in dictionary order, return the one **immediately
            before** the given ordering. If the given ordering is the very first (ascending), return the last one
            (descending).

            - **Dictionary order on lists:** compare the first element, then the second, and so on.
            - **Repeated values** make some orderings identical; they count once. `[3, 1, 1]` steps back to
              `[1, 3, 1]`.
            - **Wrap-around:** `[1, 2, 3]` is the first ordering, so the answer is `[3, 2, 1]`.
            - **Up to 10⁵ ratings**, so listing orderings is impossible.
            """
        ],
        think=[
            """
            Take `[1, 5, 8, 4, 1, 3, 5, 6, 7]`. To get the ordering just **below**, change it as far right as
            possible and by as little as possible.

            From the right, the tail `1, 3, 5, 6, 7` is **ascending**: that's already the *smallest* arrangement of
            those values, so no reshuffle of the tail alone can make the list smaller. The first value that breaks
            the ascent (scanning leftwards) is the **4** at index 3: it's larger than the 1 after it. That's the
            pivot.
            """,
            fig(Row(a, st={3: "mark"} | {k: "found" for k in range(4, 9)}, slots=True), caption="Ascending tail; the pivot 4 is the first value larger than its right neighbour."),
            """
            Replace the pivot with the **largest tail value smaller than 4**, which is 3, and then make the tail as
            **large** as possible (descending): `1, 5, 8, 3` + `7, 6, 5, 4, 1`. Since the tail is ascending, the
            largest value below the pivot is the rightmost one below it, and after the swap the tail is still
            ascending, so "make it descending" is a reversal.
            """,
        ],
        approaches=[
            approach(
                "Generate orderings from largest to smallest",
                "brute",
                "O(n! · n)",
                "O(n)",
                idea=["Generate distinct orderings in **decreasing** order (try larger values first at each position, using counts for repeated values). The first ordering smaller than the input is the answer. If none is smaller, the input is the first ordering, so return the largest one (the input sorted descending)."],
                walk=w1,
                build=["Count each rating value (0 … 100).", "Recursively fill positions, trying values from 100 down to 0.", "At a full ordering, return it if it's smaller than the input.", "If nothing is smaller, return the ratings sorted in descending order."],
                code={
                    "python": """
                        class Solution:
                            def stepBack(self, ratings: List[int]) -> List[int]:
                                count = [0] * 101  #@count
                                for x in ratings:  #@count
                                    count[x] += 1  #@count
                                buf = []
                                def build():  #@gen
                                    if len(buf) == len(ratings):  #@gen
                                        return list(buf) if buf < ratings else None  #@gen
                                    for v in range(100, -1, -1):  #@gen
                                        if count[v]:  #@gen
                                            count[v] -= 1  #@gen
                                            buf.append(v)  #@gen
                                            found = build()  #@gen
                                            buf.pop()  #@gen
                                            count[v] += 1  #@gen
                                            if found:  #@gen
                                                return found  #@gen
                                    return None  #@gen
                                return build() or sorted(ratings, reverse=True)  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int[] count = new int[101], buf, target;

                            public int[] stepBack(int[] ratings) {
                                target = ratings;  //@count
                                buf = new int[ratings.length];  //@count
                                for (int x : ratings) count[x]++;  //@count
                                if (build(0)) return buf;  //@ret
                                int[] out = ratings.clone();  //@ret
                                Arrays.sort(out);  //@ret
                                for (int a = 0, b = out.length - 1; a < b; a++, b--) { int t = out[a]; out[a] = out[b]; out[b] = t; }  //@ret
                                return out;  //@ret
                            }

                            private boolean build(int pos) {  //@gen
                                if (pos == buf.length) return Arrays.compare(buf, target) < 0;  //@gen
                                for (int v = 100; v >= 0; v--) {  //@gen
                                    if (count[v] == 0) continue;  //@gen
                                    count[v]--;  //@gen
                                    buf[pos] = v;  //@gen
                                    boolean found = build(pos + 1);  //@gen
                                    count[v]++;  //@gen
                                    if (found) return true;  //@gen
                                }
                                return false;  //@gen
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            int count[101] = {0};
                            vector<int> buf, target;

                            bool build(size_t pos) {  //@gen
                                if (pos == buf.size()) return buf < target;  //@gen
                                for (int v = 100; v >= 0; v--) {  //@gen
                                    if (!count[v]) continue;  //@gen
                                    count[v]--;  //@gen
                                    buf[pos] = v;  //@gen
                                    bool found = build(pos + 1);  //@gen
                                    count[v]++;  //@gen
                                    if (found) return true;  //@gen
                                }
                                return false;  //@gen
                            }

                        public:
                            vector<int> stepBack(vector<int>& ratings) {
                                target = ratings;  //@count
                                buf.assign(ratings.size(), 0);  //@count
                                for (int x : ratings) count[x]++;  //@count
                                if (build(0)) return buf;  //@ret
                                vector<int> out = ratings;  //@ret
                                sort(out.rbegin(), out.rend());  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int count[101];
                        static int* buf;
                        static int* target;
                        static int len;

                        static bool build(int pos) {  //@gen
                            if (pos == len) {  //@gen
                                for (int i = 0; i < len; i++) if (buf[i] != target[i]) return buf[i] < target[i];  //@gen
                                return false;  //@gen
                            }  //@gen
                            for (int v = 100; v >= 0; v--) {  //@gen
                                if (!count[v]) continue;  //@gen
                                count[v]--;  //@gen
                                buf[pos] = v;  //@gen
                                bool found = build(pos + 1);  //@gen
                                count[v]++;  //@gen
                                if (found) return true;  //@gen
                            }
                            return false;  //@gen
                        }

                        int* stepBack(int* ratings, int ratingsSize, int* returnSize) {
                            len = ratingsSize;  //@count
                            target = ratings;  //@count
                            buf = malloc(len * sizeof(int));  //@count
                            memset(count, 0, sizeof count);  //@count
                            for (int i = 0; i < len; i++) count[ratings[i]]++;  //@count
                            *returnSize = len;  //@ret
                            if (build(0)) return buf;  //@ret
                            int k = 0;  //@ret
                            for (int v = 100; v >= 0; v--) for (int c = 0; c < count[v]; c++) buf[k++] = v;  //@ret
                            return buf;  //@ret
                        }
                    """,
                },
                lines=[
                    ("count", "How many copies of each rating value (0 … 100) can still be placed."),
                    ("gen", "Fill positions left to right, trying **larger** values first, so orderings appear from largest to smallest. Return at the first ordering that is smaller than the input (lexicographic comparison of lists)."),
                    ("ret", "No smaller ordering means the input is the first one; wrap around to the last: all ratings in descending order.", {"c": "The counts are all restored after the search, so writing each value `count[v]` times from 100 down gives the descending order."}),
                ],
                complexity=["**Time O(n! · n)** in the worst case. **Space O(n).** Only usable for a handful of ratings."],
                limits=["Generates everything larger than the answer first. The previous ordering differs from the input only in a suffix, which can be computed directly."],
                slow=24,
            ),
            approach(
                "Previous permutation: pivot, swap, reverse",
                "best",
                "O(n)",
                "O(n)",
                idea=[
                    """
                    1. **Pivot:** scan from the right for the first `i` with `a[i] > a[i + 1]`. If none exists, the list is
                       ascending (the first ordering): return it reversed.
                    2. **Swap:** scan `j` from the right end while `a[j] ≥ a[i]`; the first `a[j] < a[i]` is the largest
                       tail value below the pivot (the tail is ascending). With duplicates, taking the **rightmost**
                       occurrence keeps the tail ascending. Swap.
                    3. **Reverse** the tail, turning it from ascending to descending: the largest possible ending.
                    """
                ],
                walk=w2,
                build=["Copy the ratings.", "Find the pivot from the right; if none, return the copy reversed.", "Scan `j` from the end while `a[j] ≥ a[i]`; swap `a[i]`, `a[j]`.", "Reverse `a[i + 1 …]` and return."],
                code={
                    "python": """
                        class Solution:
                            def stepBack(self, ratings: List[int]) -> List[int]:
                                a = ratings[:]  #@copy
                                i = len(a) - 2  #@pivot
                                while i >= 0 and a[i] <= a[i + 1]:  #@pivot
                                    i -= 1  #@pivot
                                if i < 0:  #@wrap
                                    return a[::-1]  #@wrap
                                j = len(a) - 1  #@swap
                                while a[j] >= a[i]:  #@swap
                                    j -= 1  #@swap
                                a[i], a[j] = a[j], a[i]  #@swap
                                a[i + 1:] = a[i + 1:][::-1]  #@rev
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] stepBack(int[] ratings) {
                                int[] a = ratings.clone();  //@copy
                                int n = a.length, i = n - 2;  //@pivot
                                while (i >= 0 && a[i] <= a[i + 1]) i--;  //@pivot
                                int start = i + 1;  //@wrap
                                if (i >= 0) {  //@swap
                                    int j = n - 1;  //@swap
                                    while (a[j] >= a[i]) j--;  //@swap
                                    int t = a[i]; a[i] = a[j]; a[j] = t;  //@swap
                                }
                                for (int x = start, y = n - 1; x < y; x++, y--) { int t = a[x]; a[x] = a[y]; a[y] = t; }  //@rev
                                return a;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> stepBack(vector<int>& ratings) {
                                vector<int> a = ratings;  //@copy
                                int n = a.size(), i = n - 2;  //@pivot
                                while (i >= 0 && a[i] <= a[i + 1]) i--;  //@pivot
                                if (i >= 0) {  //@swap
                                    int j = n - 1;  //@swap
                                    while (a[j] >= a[i]) j--;  //@swap
                                    swap(a[i], a[j]);  //@swap
                                }
                                reverse(a.begin() + i + 1, a.end());  //@rev
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* stepBack(int* ratings, int ratingsSize, int* returnSize) {
                            int n = ratingsSize;
                            int* a = malloc(n * sizeof(int));  //@copy
                            memcpy(a, ratings, n * sizeof(int));  //@copy
                            int i = n - 2;  //@pivot
                            while (i >= 0 && a[i] <= a[i + 1]) i--;  //@pivot
                            if (i >= 0) {  //@swap
                                int j = n - 1;  //@swap
                                while (a[j] >= a[i]) j--;  //@swap
                                int t = a[i]; a[i] = a[j]; a[j] = t;  //@swap
                            }
                            for (int x = i + 1, y = n - 1; x < y; x++, y--) { int t = a[x]; a[x] = a[y]; a[y] = t; }  //@rev
                            *returnSize = n;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[
                    ("copy", "Work on a copy."),
                    ("pivot", "From the right, skip while values don't decrease going leftwards (the tail is ascending). The first value larger than its right neighbour is the pivot."),
                    ("wrap", "No pivot: the list is fully ascending, the first ordering. Reversing it gives the last ordering.",
                     {"java": "With no pivot, `i` is −1 and `start` is 0, so the reversal below covers the whole array: exactly the wrap-around.", }),
                    ("swap", "Largest tail value below the pivot = the first one found scanning from the right (the tail is ascending). Swapping it in lowers this position by the least possible amount."),
                    ("rev", "Turn the ascending tail into descending: the largest arrangement of the rest, so nothing lies between the input and this ordering.",
                     {"cpp": "With no pivot, `i` is −1 and the reversal starts at index 0: the whole list is reversed, which is the wrap-around.", "c": "With no pivot, `i` is −1 and the reversal starts at index 0: the whole list is reversed, which is the wrap-around."}),
                    ("ret", "The previous ordering."),
                ],
                complexity=["**Time O(n):** at most three linear scans. **Space O(n)** for the copy."],
            ),
        ],
        takeaways=[
            """
            - **Previous permutation** is next permutation with every comparison flipped: pivot is the rightmost
              `a[i] > a[i + 1]`, swap with the rightmost smaller value, reverse the suffix.
            - No pivot ⇒ first ordering; reversing everything wraps to the last.
            - With duplicates, scanning from the right for the swap partner keeps the suffix sorted, which is what
              makes the final reversal correct.
            """
        ],
    )
