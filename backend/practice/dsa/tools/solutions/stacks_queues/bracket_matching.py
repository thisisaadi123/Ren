"""Stacks & Queues: bracket matching."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def sealed_brackets():
    s = "{[()]}([)]"
    good = "{[()]}()"

    w1 = Steps("Repeatedly delete adjacent matching pairs '()', '[]', '{}' until nothing changes. Sealed exactly when everything disappears.")
    t = good
    w1.step(f"Start: {t}", Row(list(t)))
    while any(p in t for p in ("()", "[]", "{}")):
        for p in ("()", "[]", "{}"):
            if p in t:
                i = t.index(p)
                w1.step(f"Delete the adjacent pair {p} at position {i}.", Row(list(t), st={i: "mark", i + 1: "mark"}))
                t = t[:i] + t[i + 2:]
                break
    w1.step("Nothing left: sealed.", Row([], label="remaining"), result="true")

    w2 = Steps("Push opening brackets; each closing bracket must match the top of the stack.")
    st = []
    pair = {")": "(", "]": "[", "}": "{"}
    for i, c in enumerate(s):
        if c in pair:
            if not st or st[-1] != pair[c]:
                w2.step(f"'{c}' needs '{pair[c]}' on top, but the top is '{st[-1] if st else 'nothing'}'. Not sealed.", Row(list(s), st={i: "mark"}), Row(st, label="stack"), result="false")
                break
            st.pop()
            w2.step(f"'{c}' matches the top '{pair[c]}': pop.", Row(list(s), st={i: "active"}), Row(list(st), label="stack"))
        else:
            st.append(c)
            w2.step(f"'{c}' opens: push.", Row(list(s), st={i: "active"}), Row(list(st), st={len(st) - 1: "new"}, label="stack"))

    sol(
        "sealed-brackets",
        summary="""
            The most recently opened bracket must be the first one closed: that's exactly a stack. Push every opening
            bracket; every closing bracket must match the top, which is then popped. The file is sealed if no closing
            bracket mismatches and the stack is empty at the end. O(n).
        """,
        question=[
            """
            Three bracket kinds, `()`, `[]`, `{}`. Every opener must be closed by the same kind, in last-opened-first-closed
            order. Return whether `s` is sealed.

            - **Order matters:** `([)]` has the right counts but closes `(` while `[` is still open: not sealed.
            - **Leftovers fail:** `((` never closes.
            - **A closer with nothing open** (`)` first) fails immediately.
            """
        ],
        think=[
            f"""
            Take `{s}`. Read left to right: `{{`, `[`, `(` open; `)` closes the most recent `(`; `]` closes `[`; `}}` closes
            `{{`. Then `(`, `[` open, and `)` arrives while `[` is the most recent: mismatch.
            """,
            fig(Row(list(s), st={8: "mark"}), caption="The ')' at position 8 tries to close '[' : not sealed."),
            """
            "Most recent open bracket" is the top of a stack. A counter isn't enough with several kinds: `([)]` keeps every
            count at or above zero but closes in the wrong order.
            """,
        ],
        approaches=[
            approach(
                "Delete matching pairs until stable",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["A sealed string always contains an adjacent pair like `()`, and deleting it leaves a sealed string. So keep deleting adjacent pairs; the original was sealed exactly when nothing remains."],
                walk=w1,
                build=["Work on a copy.", "While it contains `()`, `[]` or `{}`, delete one such pair.", "Return whether the copy is empty."],
                code={
                    "python": """
                        class Solution:
                            def isSealed(self, s: str) -> bool:
                                prev = None  #@loop
                                while prev != s:  #@loop
                                    prev = s  #@loop
                                    s = s.replace("()", "").replace("[]", "").replace("{}", "")  #@delete
                                return s == ""  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean isSealed(String s) {
                                String prev = null;  //@loop
                                while (!s.equals(prev)) {  //@loop
                                    prev = s;  //@loop
                                    s = s.replace("()", "").replace("[]", "").replace("{}", "");  //@delete
                                }
                                return s.isEmpty();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool isSealed(string& s) {
                                string t = s;  //@loop
                                bool changed = true;  //@loop
                                while (changed) {  //@loop
                                    changed = false;  //@loop
                                    for (const char* p : {"()", "[]", "{}"}) {  //@delete
                                        size_t i;  //@delete
                                        while ((i = t.find(p)) != string::npos) { t.erase(i, 2); changed = true; }  //@delete
                                    }
                                }
                                return t.empty();  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool isSealed(char* s) {
                            int n = strlen(s);
                            char* t = malloc(n + 1);  //@loop
                            memcpy(t, s, n + 1);  //@loop
                            bool changed = true;  //@loop
                            while (changed) {  //@loop
                                changed = false;  //@loop
                                int w = 0;  //@delete
                                for (int i = 0; t[i]; i++) {  //@delete
                                    char c = t[i], d = t[i + 1];  //@delete
                                    if ((c == '(' && d == ')') || (c == '[' && d == ']') || (c == '{' && d == '}')) { i++; changed = true; continue; }  //@delete
                                    t[w++] = c;  //@delete
                                }  //@delete
                                t[w] = '\\0';  //@delete
                            }
                            bool sealed = t[0] == '\\0';  //@ret
                            free(t);  //@ret
                            return sealed;  //@ret
                        }
                    """,
                },
                lines=[("loop", "Repeat until a round deletes nothing."), ("delete", "Remove adjacent matching pairs.", {"c": "One left-to-right pass copies characters, skipping every adjacent matching pair it sees."}), ("ret", "Everything cancelled out → sealed.")],
                complexity=["**Time O(n²):** each round is O(n) and nested strings like `((((…))))` need about n/2 rounds. **Space O(n)** for the copy."],
                limits=["Each round rescans the whole string to remove a layer. A stack processes each bracket exactly once."],
                slow=True,
            ),
            approach(
                "Stack of open brackets",
                "best",
                "O(n)",
                "O(n)",
                idea=["Push openers. On a closer: the stack must be non-empty and its top must be the matching opener; pop it. At the end the stack must be empty."],
                walk=w2,
                build=["Map each closer to its opener.", "For each character: opener → push; closer → check the top and pop, or fail.", "Return whether the stack is empty."],
                code={
                    "python": """
                        class Solution:
                            def isSealed(self, s: str) -> bool:
                                pair = {")": "(", "]": "[", "}": "{"}  #@pair
                                stack = []  #@stack
                                for c in s:  #@loop
                                    if c in pair:  #@close
                                        if not stack or stack[-1] != pair[c]:  #@close
                                            return False  #@close
                                        stack.pop()  #@close
                                    else:  #@open
                                        stack.append(c)  #@open
                                return not stack  #@ret
                    """,
                    "java": """
                        class Solution {
                            public boolean isSealed(String s) {
                                Deque<Character> stack = new ArrayDeque<>();  //@stack
                                for (char c : s.toCharArray()) {  //@loop
                                    if (c == '(' || c == '[' || c == '{') stack.push(c);  //@open
                                    else {  //@close
                                        char want = c == ')' ? '(' : c == ']' ? '[' : '{';  //@pair
                                        if (stack.isEmpty() || stack.pop() != want) return false;  //@close
                                    }
                                }
                                return stack.isEmpty();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool isSealed(string& s) {
                                vector<char> stack;  //@stack
                                for (char c : s) {  //@loop
                                    if (c == '(' || c == '[' || c == '{') stack.push_back(c);  //@open
                                    else {  //@close
                                        char want = c == ')' ? '(' : c == ']' ? '[' : '{';  //@pair
                                        if (stack.empty() || stack.back() != want) return false;  //@close
                                        stack.pop_back();  //@close
                                    }
                                }
                                return stack.empty();  //@ret
                            }
                        };
                    """,
                    "c": """
                        bool isSealed(char* s) {
                            int n = strlen(s), top = 0;
                            char* stack = malloc(n + 1);  //@stack
                            bool ok = true;  //@stack
                            for (int i = 0; i < n && ok; i++) {  //@loop
                                char c = s[i];  //@loop
                                if (c == '(' || c == '[' || c == '{') stack[top++] = c;  //@open
                                else {  //@close
                                    char want = c == ')' ? '(' : c == ']' ? '[' : '{';  //@pair
                                    if (top == 0 || stack[top - 1] != want) ok = false;  //@close
                                    else top--;  //@close
                                }
                            }
                            ok = ok && top == 0;  //@ret
                            free(stack);  //@ret
                            return ok;  //@ret
                        }
                    """,
                },
                lines=[("pair", "Which opener each closer needs."), ("stack", "Open brackets not yet closed, most recent on top.", {"c": "An array plus a `top` count works as a stack; it never holds more than n brackets."}), ("loop", "One pass over the characters."), ("open", "An opener waits on the stack for its closer."), ("close", "A closer must match the most recently opened bracket; otherwise (or with nothing open) the file isn't sealed.", {"java": "`pop()` removes and returns the top in one step."}), ("ret", "Sealed only if nothing is left open.")],
                complexity=["**Time O(n).** **Space O(n)** for the stack."],
            ),
        ],
        takeaways=[
            """
            - Nested structure with "last opened, first closed" → **stack**.
            - With one bracket kind a counter suffices; with several kinds you need the stack to check the kind.
            - Fail fast on a closer with an empty stack, and remember to require an empty stack at the end.
            """
        ],
    )


@problem
def patch_the_brackets():
    s = "())(()(("

    w1 = Steps("Repeatedly delete adjacent '()' pairs. Every bracket left over needs a partner inserted.")
    t = s
    w1.step(f"Start: {t}", Row(list(t)))
    while "()" in t:
        i = t.index("()")
        w1.step(f"Delete '()' at {i}.", Row(list(t), st={i: "mark", i + 1: "mark"}))
        t = t[:i] + t[i + 2:]
    w1.step(f"Left over: '{t}', {len(t)} brackets, each needing one insertion.", Row(list(t), st={k: "answer" for k in range(len(t))}), result=len(t))

    w2 = Steps("Count currently open '(' as you go. A ')' with nothing open needs an inserted '('; '(' still open at the end need inserted ')'.")
    open_, added = 0, 0
    for i, c in enumerate(s):
        if c == "(":
            open_ += 1
            note = f"'(' opens: open = {open_}."
        elif open_:
            open_ -= 1
            note = f"')' closes one: open = {open_}."
        else:
            added += 1
            note = f"')' with nothing open: insert a '(' before it (added = {added})."
        w2.step(note, Row(list(s), st={i: "active"}), Vars(open=open_, inserted=added))
    w2.step(f"{open_} '(' still open need ')' at the end: {added} + {open_} = {added + open_}.", Row(list(s)), result=added + open_)

    sol(
        "patch-the-brackets",
        summary="""
            Walk left to right counting unclosed `(`. A `)` with nothing open needs one inserted `(`; whatever `(` remain
            open at the end each need one inserted `)`. Those two kinds of leftover brackets can never fix each other, so
            the sum is the minimum. O(n) time, O(1) space.
        """,
        question=[
            """
            Insert the fewest brackets anywhere to make `s` balanced. Return how many.

            - **Insertions only:** nothing is deleted or moved.
            - **Two kinds of problem:** a `)` that arrives with nothing open, and a `(` that never gets closed. `))((` has
              both: it needs 4 insertions.
            """
        ],
        think=[
            f"""
            Take `{s}`. Match brackets like a person would: `()` pairs cancel. What can't be matched? The `)` at position 2
            arrives when nothing is open; and at the end, some `(` are still waiting. Each unmatched bracket needs exactly one
            partner inserted, and no insertion can serve two of them.
            """,
            fig(Row(list(s), st={2: "mark", 6: "mark", 7: "mark", 3: "mark"}), caption="Unmatched brackets (marked) each need one inserted partner."),
            """
            So count unmatched brackets. A single counter of "currently open `(`" does it, since there is only one bracket
            kind: `(` increments; `)` decrements if something is open, otherwise it's unmatched.
            """,
        ],
        approaches=[
            approach(
                "Delete matched pairs until none remain",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Keep removing adjacent `()` pairs. What's left looks like `)))((`: every remaining bracket is unmatched and needs one insertion. Return its length."],
                walk=w1,
                build=["While the string contains `()`, delete it.", "Return the remaining length."],
                code={
                    "python": """
                        class Solution:
                            def minInsertions(self, s: str) -> int:
                                while "()" in s:  #@delete
                                    s = s.replace("()", "")  #@delete
                                return len(s)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int minInsertions(String s) {
                                while (s.contains("()")) s = s.replace("()", "");  //@delete
                                return s.length();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int minInsertions(string& s) {
                                string t = s;  //@delete
                                size_t i;  //@delete
                                while ((i = t.find("()")) != string::npos) t.erase(i, 2);  //@delete
                                return t.size();  //@ret
                            }
                        };
                    """,
                    "c": """
                        int minInsertions(char* s) {
                            int n = strlen(s);
                            char* t = malloc(n + 1);  //@delete
                            memcpy(t, s, n + 1);  //@delete
                            bool changed = true;  //@delete
                            while (changed) {  //@delete
                                changed = false;  //@delete
                                int w = 0;  //@delete
                                for (int i = 0; t[i]; i++) {  //@delete
                                    if (t[i] == '(' && t[i + 1] == ')') { i++; changed = true; continue; }  //@delete
                                    t[w++] = t[i];  //@delete
                                }  //@delete
                                t[w] = '\\0';  //@delete
                            }  //@delete
                            int left = strlen(t);  //@ret
                            free(t);  //@ret
                            return left;  //@ret
                        }
                    """,
                },
                lines=[("delete", "Cancel matched pairs, layer by layer, until none are adjacent."), ("ret", "Every leftover bracket needs one inserted partner.")],
                complexity=["**Time O(n²)** for deeply nested input. **Space O(n).**"],
                limits=["Re-scans the string for every layer of nesting. A single counter recognises unmatched brackets in one pass."],
                slow=True,
            ),
            approach(
                "One counter",
                "best",
                "O(n)",
                "O(1)",
                idea=["`open` = unclosed `(` so far, `added` = insertions needed. `(` → `open += 1`. `)` → if `open > 0`, `open −= 1`; else `added += 1`. Answer `added + open`."],
                walk=w2,
                build=["`open = added = 0`.", "Scan and update as described.", "Return `added + open`."],
                code={
                    "python": """
                        class Solution:
                            def minInsertions(self, s: str) -> int:
                                open_, added = 0, 0  #@init
                                for c in s:  #@loop
                                    if c == "(":  #@open
                                        open_ += 1  #@open
                                    elif open_:  #@close
                                        open_ -= 1  #@close
                                    else:  #@stray
                                        added += 1  #@stray
                                return added + open_  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int minInsertions(String s) {
                                int open = 0, added = 0;  //@init
                                for (char c : s.toCharArray()) {  //@loop
                                    if (c == '(') open++;  //@open
                                    else if (open > 0) open--;  //@close
                                    else added++;  //@stray
                                }
                                return added + open;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int minInsertions(string& s) {
                                int open = 0, added = 0;  //@init
                                for (char c : s) {  //@loop
                                    if (c == '(') open++;  //@open
                                    else if (open > 0) open--;  //@close
                                    else added++;  //@stray
                                }
                                return added + open;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int minInsertions(char* s) {
                            int open = 0, added = 0;  //@init
                            for (char* p = s; *p; p++) {  //@loop
                                if (*p == '(') open++;  //@open
                                else if (open > 0) open--;  //@close
                                else added++;  //@stray
                            }
                            return added + open;  //@ret
                        }
                    """,
                },
                lines=[("init", "Nothing open, nothing inserted."), ("loop", "One pass."), ("open", "A new unclosed `(`."), ("close", "`)` closes the most recent open `(`."), ("stray", "`)` with nothing open: insert a `(` before it."), ("ret", "Plus one `)` for every `(` still open at the end.")],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - With a single bracket kind, a **depth counter** replaces the stack.
            - Unmatched closers (seen when depth is 0) and unmatched openers (depth left at the end) are counted
              separately; their sum is the minimum fix.
            """
        ],
    )


@problem
def longest_balanced_stretch():
    s = ")(()())(()"
    n = len(s)

    def brute(t):
        best = 0
        for i in range(len(t)):
            d = 0
            for j in range(i, len(t)):
                d += 1 if t[j] == "(" else -1
                if d < 0:
                    break
                if d == 0:
                    best = max(best, j - i + 1)
        return best

    want = brute(s)

    w1 = Steps("From every start, scan right keeping depth; stop when it goes negative; record lengths where depth returns to 0.")
    best = 0
    for i in range(n):
        d = 0
        for j in range(i, n):
            d += 1 if s[j] == "(" else -1
            if d < 0:
                break
            if d == 0 and j - i + 1 > best:
                best = j - i + 1
                w1.step(f"Start {i}, end {j}: depth back to 0. New best {best}.", Row(list(s), st={k: "answer" for k in range(i, j + 1)}, slots=True), Vars(best=best))
    w1.step(f"All starts tried: {best}.", Row(list(s), slots=True), result=best)

    w2 = Steps("Stack of indices, starting with −1 as a 'last invalid position'. Push '(' indices; on ')', pop, then measure from the new top.")
    st = [-1]
    best = 0
    for i, c in enumerate(s):
        if c == "(":
            st.append(i)
            note = f"'(' at {i}: push."
        else:
            st.pop()
            if not st:
                st.append(i)
                note = f"')' at {i} has no partner: it becomes the new boundary."
            else:
                L = i - st[-1]
                best = max(best, L)
                note = f"')' at {i} matches; balanced run from {st[-1] + 1} to {i}: length {L}."
        w2.step(note, Row(list(s), st={i: "active"}, slots=True), Row(list(st), label="stack (indices)"), Vars(best=best))
    w2.steps[-1]["result"] = str(best)

    w3 = Steps("Two counters, two passes. Left to right: reset when ')' outnumbers '('; record when equal. Then right to left with the roles swapped.")
    best = 0
    o = c_ = 0
    for i, ch in enumerate(s):
        if ch == "(":
            o += 1
        else:
            c_ += 1
        if o == c_:
            best = max(best, 2 * c_)
            w3.step(f"→ {i}: open {o} = close {c_}: balanced length {2 * c_}.", Row(list(s), st={i: "active"}, slots=True), Vars(best=best))
        elif c_ > o:
            o = c_ = 0
            w3.step(f"→ {i}: more ')' than '(': nothing balanced can cross here; reset.", Row(list(s), st={i: "mark"}, slots=True), Vars(best=best))
    o = c_ = 0
    for i in range(n - 1, -1, -1):
        ch = s[i]
        if ch == "(":
            o += 1
        else:
            c_ += 1
        if o == c_:
            best = max(best, 2 * o)
        elif o > c_:
            o = c_ = 0
    w3.step(f"The right-to-left pass catches runs like '(()' that the first pass misses. Best overall {best}.", Row(list(s), slots=True), result=best)

    sol(
        "longest-balanced-stretch",
        summary="""
            Unmatched brackets split the string into independent pieces, and the longest balanced stretch lives between two
            of them. A stack of indices finds every match and measures each balanced run from the last unmatched position:
            O(n). Two counter passes (left-to-right and right-to-left) do the same in O(1) space.
        """,
        question=[
            """
            Return the length of the longest **contiguous** piece of `s` that is balanced.

            - **Contiguous:** `()(()` has `()` and the inner `()`; the longest is 2, not 4.
            - **Balanced pieces can sit side by side:** `()()` is one balanced stretch of length 4.
            - **Size:** up to 10⁵ characters, so trying all O(n²) pieces is too slow.
            """
        ],
        think=[
            f"""
            Take `{s}`. The `)` at position 0 can never be matched, and neither can the `(` at position 7. Everything else is
            matched, so the balanced stretches are positions 1…6 (`(()())`, length 6) and 8…9 (`()`, length 2). The answer is
            {want}.
            """,
            fig(Row(list(s), st={0: "mark", 7: "mark"} | {k: "answer" for k in range(1, 7)}, slots=True), caption="Unmatched brackets (marked) act as walls; the longest balanced run between walls wins."),
            """
            So the job is: find which brackets are unmatched, and measure the gaps between them. A stack of indices does
            this naturally if it keeps, at its bottom, the position of the last "wall" (unmatched `)`, or −1 at the start):
            after any `)` is matched, the current balanced run reaches back to just after the index on top of the stack.
            """,
        ],
        approaches=[
            approach(
                "Scan from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start i, walk right keeping the depth (+1 for `(`, −1 for `)`). If it goes negative, nothing starting at i can extend further: stop. Whenever it's 0, `i … j` is balanced."],
                walk=w1,
                build=["For each i: depth 0.", "For each j ≥ i: update depth; stop if negative; record `j − i + 1` when depth is 0."],
                code={
                    "python": """
                        class Solution:
                            def longestBalanced(self, s: str) -> int:
                                best = 0
                                for i in range(len(s)):  #@start
                                    depth = 0  #@start
                                    for j in range(i, len(s)):  #@scan
                                        depth += 1 if s[j] == "(" else -1  #@scan
                                        if depth < 0:  #@stop
                                            break  #@stop
                                        if depth == 0:  #@record
                                            best = max(best, j - i + 1)  #@record
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestBalanced(String s) {
                                int n = s.length(), best = 0;
                                for (int i = 0; i < n; i++) {  //@start
                                    int depth = 0;  //@start
                                    for (int j = i; j < n; j++) {  //@scan
                                        depth += s.charAt(j) == '(' ? 1 : -1;  //@scan
                                        if (depth < 0) break;  //@stop
                                        if (depth == 0) best = Math.max(best, j - i + 1);  //@record
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestBalanced(string& s) {
                                int n = s.size(), best = 0;
                                for (int i = 0; i < n; i++) {  //@start
                                    int depth = 0;  //@start
                                    for (int j = i; j < n; j++) {  //@scan
                                        depth += s[j] == '(' ? 1 : -1;  //@scan
                                        if (depth < 0) break;  //@stop
                                        if (depth == 0) best = max(best, j - i + 1);  //@record
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestBalanced(char* s) {
                            int n = strlen(s), best = 0;
                            for (int i = 0; i < n; i++) {  //@start
                                int depth = 0;  //@start
                                for (int j = i; j < n; j++) {  //@scan
                                    depth += s[j] == '(' ? 1 : -1;  //@scan
                                    if (depth < 0) break;  //@stop
                                    if (depth == 0 && j - i + 1 > best) best = j - i + 1;  //@record
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("start", "Every possible start, at depth 0."), ("scan", "Extend one character at a time."), ("stop", "A `)` with nothing open: no balanced piece from i can contain it."), ("record", "Depth 0 means `i … j` is balanced."), ("ret", "Longest found.")],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["Each start re-reads the same characters. Matching brackets once with a stack gives every balanced run directly."],
                slow=True,
            ),
            approach(
                "Stack of indices with a boundary",
                "better",
                "O(n)",
                "O(n)",
                idea=["Start the stack with −1 (a virtual wall). `(` → push its index. `)` → pop; if the stack is now empty, this `)` is unmatched: push its index as the new wall; otherwise the balanced run ending here starts right after the index on top, so its length is `i − top`."],
                walk=w2,
                build=["Stack = [−1], best = 0.", "For each i: `(` → push i.", "`)` → pop; empty → push i; else best = max(best, i − top).", "Return best."],
                code={
                    "python": """
                        class Solution:
                            def longestBalanced(self, s: str) -> int:
                                stack = [-1]  #@init
                                best = 0  #@init
                                for i, c in enumerate(s):  #@loop
                                    if c == "(":  #@open
                                        stack.append(i)  #@open
                                    else:  #@close
                                        stack.pop()  #@close
                                        if not stack:  #@wall
                                            stack.append(i)  #@wall
                                        else:  #@measure
                                            best = max(best, i - stack[-1])  #@measure
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestBalanced(String s) {
                                Deque<Integer> stack = new ArrayDeque<>();  //@init
                                stack.push(-1);  //@init
                                int best = 0;  //@init
                                for (int i = 0; i < s.length(); i++) {  //@loop
                                    if (s.charAt(i) == '(') stack.push(i);  //@open
                                    else {  //@close
                                        stack.pop();  //@close
                                        if (stack.isEmpty()) stack.push(i);  //@wall
                                        else best = Math.max(best, i - stack.peek());  //@measure
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestBalanced(string& s) {
                                vector<int> stack = {-1};  //@init
                                int best = 0;  //@init
                                for (int i = 0; i < (int) s.size(); i++) {  //@loop
                                    if (s[i] == '(') stack.push_back(i);  //@open
                                    else {  //@close
                                        stack.pop_back();  //@close
                                        if (stack.empty()) stack.push_back(i);  //@wall
                                        else best = max(best, i - stack.back());  //@measure
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestBalanced(char* s) {
                            int n = strlen(s), top = 0, best = 0;
                            int* stack = malloc((n + 1) * sizeof(int));  //@init
                            stack[top++] = -1;  //@init
                            for (int i = 0; i < n; i++) {  //@loop
                                if (s[i] == '(') stack[top++] = i;  //@open
                                else {  //@close
                                    top--;  //@close
                                    if (top == 0) stack[top++] = i;  //@wall
                                    else if (i - stack[top - 1] > best) best = i - stack[top - 1];  //@measure
                                }
                            }
                            free(stack);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "The bottom of the stack is always the last wall; −1 stands for \"before the string\"."), ("loop", "One pass."), ("open", "Remember where this `(` is."), ("close", "Try to match: pop the most recent `(` (or the wall, if none is open)."), ("wall", "Nothing was open: this `)` is unmatched and becomes the new wall."), ("measure", "Matched: everything after the index now on top is balanced up to i."), ("ret", "Longest run measured.")],
                complexity=["**Time O(n).** **Space O(n)** for the stack."],
                limits=["The stack can hold up to n indices. With one bracket kind, counts of `(` and `)` can find the same runs in O(1) space, at the cost of a second pass."],
            ),
            approach(
                "Two counter passes",
                "best",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    Left to right, count `open` and `close`. When equal, the piece since the last reset is balanced: record
                    `2 × close`. When `close > open`, reset both (that `)` is a wall).

                    That pass misses pieces where `(` stays ahead until the end, like `(()`. So do a mirror pass right to left:
                    record when equal, reset when `open > close`. The best of both passes is the answer.
                    """
                ],
                walk=w3,
                build=["Left-to-right pass with the reset rule `close > open`.", "Right-to-left pass with the reset rule `open > close`.", "Return the best length seen."],
                code={
                    "python": """
                        class Solution:
                            def longestBalanced(self, s: str) -> int:
                                best = 0
                                opened = closed = 0  #@forward
                                for c in s:  #@forward
                                    if c == "(":  #@forward
                                        opened += 1  #@forward
                                    else:  #@forward
                                        closed += 1  #@forward
                                    if opened == closed:  #@forward
                                        best = max(best, 2 * closed)  #@forward
                                    elif closed > opened:  #@forward
                                        opened = closed = 0  #@forward
                                opened = closed = 0  #@backward
                                for c in reversed(s):  #@backward
                                    if c == "(":  #@backward
                                        opened += 1  #@backward
                                    else:  #@backward
                                        closed += 1  #@backward
                                    if opened == closed:  #@backward
                                        best = max(best, 2 * opened)  #@backward
                                    elif opened > closed:  #@backward
                                        opened = closed = 0  #@backward
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestBalanced(String s) {
                                int n = s.length(), best = 0, opened = 0, closed = 0;
                                for (int i = 0; i < n; i++) {  //@forward
                                    if (s.charAt(i) == '(') opened++; else closed++;  //@forward
                                    if (opened == closed) best = Math.max(best, 2 * closed);  //@forward
                                    else if (closed > opened) opened = closed = 0;  //@forward
                                }
                                opened = closed = 0;  //@backward
                                for (int i = n - 1; i >= 0; i--) {  //@backward
                                    if (s.charAt(i) == '(') opened++; else closed++;  //@backward
                                    if (opened == closed) best = Math.max(best, 2 * opened);  //@backward
                                    else if (opened > closed) opened = closed = 0;  //@backward
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestBalanced(string& s) {
                                int n = s.size(), best = 0, opened = 0, closed = 0;
                                for (int i = 0; i < n; i++) {  //@forward
                                    if (s[i] == '(') opened++; else closed++;  //@forward
                                    if (opened == closed) best = max(best, 2 * closed);  //@forward
                                    else if (closed > opened) opened = closed = 0;  //@forward
                                }
                                opened = closed = 0;  //@backward
                                for (int i = n - 1; i >= 0; i--) {  //@backward
                                    if (s[i] == '(') opened++; else closed++;  //@backward
                                    if (opened == closed) best = max(best, 2 * opened);  //@backward
                                    else if (opened > closed) opened = closed = 0;  //@backward
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestBalanced(char* s) {
                            int n = strlen(s), best = 0, opened = 0, closed = 0;
                            for (int i = 0; i < n; i++) {  //@forward
                                if (s[i] == '(') opened++; else closed++;  //@forward
                                if (opened == closed && 2 * closed > best) best = 2 * closed;  //@forward
                                else if (closed > opened) opened = closed = 0;  //@forward
                            }
                            opened = closed = 0;  //@backward
                            for (int i = n - 1; i >= 0; i--) {  //@backward
                                if (s[i] == '(') opened++; else closed++;  //@backward
                                if (opened == closed && 2 * opened > best) best = 2 * opened;  //@backward
                                else if (opened > closed) opened = closed = 0;  //@backward
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("forward", "Left to right: equal counts mean the piece since the last reset is balanced. More `)` than `(` can never recover, so start over after it. This pass misses balanced pieces followed only by surplus `(`."), ("backward", "Right to left with the roles reversed: more `(` than `)` (seen from the right) is the dead end. This catches exactly what the first pass missed."), ("ret", "The best length from either pass.")],
                complexity=["**Time O(n):** two passes. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Keep a **sentinel index** (−1 or the last unmatched `)`) at the bottom of an index stack to measure balanced runs.
            - With a single bracket kind, two counter passes in opposite directions replace the stack.
            - Unmatched brackets are walls: no balanced stretch can cross one.
            """
        ],
    )


@problem
def nested_box_value():
    s = "(()(()))()"
    MOD = 10**9 + 7

    def val(t):
        st = [0]
        for c in t:
            if c == "(":
                st.append(0)
            else:
                x = st.pop()
                st[-1] += 1 if x == 0 else 2 * x
        return st[0]

    want = val(s)

    def tops(t):
        out, d, start = [], 0, 0
        for i, c in enumerate(t):
            d += 1 if c == "(" else -1
            if d == 0:
                out.append(t[start:i + 1])
                start = i + 1
        return out

    w1 = Steps("Split into top-level boxes; a box '(A)' is 1 if A is empty, else 2 × value(A). Recurse.")
    for part in tops(s):
        inner = part[1:-1]
        w1.step(f"Top-level box '{part}': " + ("empty → 1." if not inner else f"2 × value('{inner}') = 2 × {val(inner)} = {2 * val(inner)}."), Row(list(s)), Vars(box=part, value=val(part)))
    w1.step(f"Sum of the top-level boxes: {want}.", Row(list(s)), result=want)

    w2 = Steps("Stack of running totals, one per open box. '(' pushes 0; ')' pops the box's total and adds 1 (empty) or 2 × total to its parent.")
    st = [0]
    for i, c in enumerate(s):
        if c == "(":
            st.append(0)
            note = "'(' opens a box: push 0."
        else:
            x = st.pop()
            add = 1 if x == 0 else 2 * x
            st[-1] += add
            note = f"')' closes a box with contents {x}: it's worth {add}; add to the parent → {st[-1]}."
        w2.step(note, Row(list(s), st={i: "active"}, slots=True), Row(list(st), label="totals (outermost first)"))
    w2.steps[-1]["result"] = str(st[0])

    w3 = Steps("Every '()' is worth 2^depth (depth = boxes around it). Sum those.")
    d = 0
    tot = 0
    for i, c in enumerate(s):
        if c == "(":
            d += 1
        else:
            d -= 1
            if s[i - 1] == "(":
                tot += 2 ** d
                w3.step(f"'()' at {i - 1}–{i} sits inside {d} box{'es' if d != 1 else ''}: worth 2^{d} = {2 ** d}. Total {tot}.", Row(list(s), st={i - 1: "answer", i: "answer"}, slots=True), Vars(depth=d, total=tot))
    w3.steps[-1]["result"] = str(tot)

    sol(
        "nested-box-value",
        summary="""
            Each empty box `()` gets doubled once for every box around it, and sums just add up. So the value is the sum,
            over every `()`, of 2 to the power of its nesting depth. One pass with a depth counter computes it; work modulo
            10⁹ + 7 since depth can reach 5 × 10⁴.
        """,
        question=[
            """
            Value rules: `()` = 1; `AB` = A + B; `(A)` = 2 × A for non-empty A. Return the value of the balanced string,
            modulo 10⁹ + 7.

            - **Deep nesting makes huge values:** 50,000 nested boxes are worth 2⁴⁹⁹⁹⁹, hence the modulo.
            - **The string is guaranteed balanced.**
            """
        ],
        think=[
            f"""
            Take `{s}`. Its top-level boxes are `(()(()))` and `()`. Expanding the first: `(A)` with A = `()(())`, which is
            1 + 2 × 1 = 3, so the box is 6. Plus 1 for the last `()`: total {want}.
            """,
            fig(Row(list(s), slots=True), caption="Each innermost '()' is a 1 that gets doubled by every box around it."),
            """
            Look at where the value comes from: only the innermost `()` pairs create value (each is a 1), and each
            enclosing box doubles everything inside it. Doubling distributes over sums, so a `()` at depth d contributes
            exactly 2ᵈ. That gives an O(1)-space method; a stack of partial sums is the more literal translation of the rules.
            """,
        ],
        approaches=[
            approach(
                "Recursive evaluation",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Split the string into top-level boxes (where the depth returns to 0). Each box `(A)` is 1 if empty, else 2 × value(A) computed recursively. Add the boxes."],
                walk=w1,
                build=["Walk with a depth counter to find each top-level box.", "For each box, recurse on its inside (or count 1 if empty).", "Sum modulo 10⁹ + 7."],
                code={
                    "python": """
                        import sys

                        class Solution:
                            def boxValue(self, s: str) -> int:
                                sys.setrecursionlimit(10000)
                                MOD = 10**9 + 7
                                def value(lo, hi):  #@rec
                                    total, depth, start = 0, 0, lo  #@split
                                    for i in range(lo, hi):  #@split
                                        depth += 1 if s[i] == "(" else -1  #@split
                                        if depth == 0:  #@box
                                            inner = 1 if i == start + 1 else 2 * value(start + 1, i)  #@box
                                            total = (total + inner) % MOD  #@box
                                            start = i + 1  #@box
                                    return total  #@rec
                                return value(0, len(s))  #@ret
                    """,
                    "java": """
                        class Solution {
                            private static final long MOD = 1_000_000_007L;
                            private String s;

                            public int boxValue(String s) {
                                this.s = s;
                                return (int) value(0, s.length());  //@ret
                            }

                            private long value(int lo, int hi) {  //@rec
                                long total = 0;  //@split
                                int depth = 0, start = lo;  //@split
                                for (int i = lo; i < hi; i++) {  //@split
                                    depth += s.charAt(i) == '(' ? 1 : -1;  //@split
                                    if (depth == 0) {  //@box
                                        long inner = (i == start + 1) ? 1 : 2 * value(start + 1, i) % MOD;  //@box
                                        total = (total + inner) % MOD;  //@box
                                        start = i + 1;  //@box
                                    }
                                }
                                return total;  //@rec
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static constexpr long long MOD = 1000000007LL;
                            string s;

                            long long value(int lo, int hi) {  //@rec
                                long long total = 0;  //@split
                                int depth = 0, start = lo;  //@split
                                for (int i = lo; i < hi; i++) {  //@split
                                    depth += s[i] == '(' ? 1 : -1;  //@split
                                    if (depth == 0) {  //@box
                                        long long inner = (i == start + 1) ? 1 : 2 * value(start + 1, i) % MOD;  //@box
                                        total = (total + inner) % MOD;  //@box
                                        start = i + 1;  //@box
                                    }
                                }
                                return total;  //@rec
                            }

                        public:
                            int boxValue(string& s) {
                                this->s = s;
                                return value(0, s.size());  //@ret
                            }
                        };
                    """,
                    "c": """
                        static const long long MOD = 1000000007LL;

                        static long long value(const char* s, int lo, int hi) {  //@rec
                            long long total = 0;  //@split
                            int depth = 0, start = lo;  //@split
                            for (int i = lo; i < hi; i++) {  //@split
                                depth += s[i] == '(' ? 1 : -1;  //@split
                                if (depth == 0) {  //@box
                                    long long inner = (i == start + 1) ? 1 : 2 * value(s, start + 1, i) % MOD;  //@box
                                    total = (total + inner) % MOD;  //@box
                                    start = i + 1;  //@box
                                }
                            }
                            return total;  //@rec
                        }

                        int boxValue(char* s) {
                            return (int) value(s, 0, strlen(s));  //@ret
                        }
                    """,
                },
                lines=[("rec", "`value(lo, hi)` evaluates a balanced substring."), ("split", "Track depth to find where each top-level box ends."), ("box", "An empty box is 1; otherwise double the value of its inside (recursively). Add it to the total, mod 10⁹ + 7."), ("ret", "Value of the whole string.")],
                complexity=["**Time O(n²)** for deep nesting (each level rescans its inside). **Space O(n)** recursion depth, which can overflow the call stack for 5 × 10⁴ levels."],
                limits=["Rescans nested parts once per level, and deep inputs risk a stack overflow. A stack of partial sums evaluates everything in one pass."],
                slow=True,
            ),
            approach(
                "Stack of partial sums",
                "better",
                "O(n)",
                "O(n)",
                idea=["Keep one running total per currently open box, plus one for the top level. `(` pushes 0. `)` pops the closing box's total t and adds `1` (if the box was empty, i.e. the previous character was `(`) or `2t` to the box below. The bottom entry is the answer."],
                walk=w2,
                build=["Stack = [0].", "`(` → push 0.", "`)` → t = pop; top += (1 if the previous character was `(` else 2t) mod 10⁹ + 7.", "Return the bottom value."],
                code={
                    "python": """
                        class Solution:
                            def boxValue(self, s: str) -> int:
                                MOD = 10**9 + 7
                                stack = [0]  #@init
                                for i, c in enumerate(s):  #@loop
                                    if c == "(":  #@open
                                        stack.append(0)  #@open
                                    else:  #@close
                                        t = stack.pop()  #@close
                                        stack[-1] = (stack[-1] + (1 if s[i - 1] == "(" else 2 * t)) % MOD  #@close
                                return stack[0]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int boxValue(String s) {
                                final long MOD = 1_000_000_007L;
                                long[] stack = new long[s.length() + 1];  //@init
                                int top = 0;  //@init
                                for (int i = 0; i < s.length(); i++) {  //@loop
                                    if (s.charAt(i) == '(') stack[++top] = 0;  //@open
                                    else {  //@close
                                        long t = stack[top--];  //@close
                                        stack[top] = (stack[top] + (s.charAt(i - 1) == '(' ? 1 : 2 * t)) % MOD;  //@close
                                    }
                                }
                                return (int) stack[0];  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int boxValue(string& s) {
                                const long long MOD = 1000000007LL;
                                vector<long long> stack = {0};  //@init
                                for (int i = 0; i < (int) s.size(); i++) {  //@loop
                                    if (s[i] == '(') stack.push_back(0);  //@open
                                    else {  //@close
                                        long long t = stack.back();  //@close
                                        stack.pop_back();  //@close
                                        stack.back() = (stack.back() + (s[i - 1] == '(' ? 1 : 2 * t)) % MOD;  //@close
                                    }
                                }
                                return stack[0];  //@ret
                            }
                        };
                    """,
                    "c": """
                        int boxValue(char* s) {
                            const long long MOD = 1000000007LL;
                            int n = strlen(s), top = 0;
                            long long* stack = calloc(n + 1, sizeof(long long));  //@init
                            for (int i = 0; i < n; i++) {  //@loop
                                if (s[i] == '(') stack[++top] = 0;  //@open
                                else {  //@close
                                    long long t = stack[top--];  //@close
                                    stack[top] = (stack[top] + (s[i - 1] == '(' ? 1 : 2 * t)) % MOD;  //@close
                                }
                            }
                            int answer = (int) stack[0];  //@ret
                            free(stack);  //@ret
                            return answer;  //@ret
                        }
                    """,
                },
                lines=[("init", "Entry 0 collects the top level."), ("loop", "One pass."), ("open", "A new box starts with an empty total."), ("close", "Finish the box: if the character just before this `)` was `(`, the box is empty and worth 1; otherwise it's worth double its contents. Add that to the enclosing box (mod 10⁹ + 7). Checking the previous character, rather than whether the total is 0, stays exact even after the modulus."), ("ret", "The top-level total.")],
                complexity=["**Time O(n).** **Space O(n)** for the stack."],
                limits=["Needs a stack as deep as the nesting. The contribution of each `()` depends only on its depth, which a single counter tracks."],
            ),
            approach(
                "Sum 2^depth over every '()'",
                "best",
                "O(n)",
                "O(1)",
                idea=["Walk with `depth`. On `(`, depth += 1. On `)`, depth −= 1; if the previous character was `(`, this is an innermost `()` at the new depth d, worth 2ᵈ. Keep a running power of two in step with depth (or precompute), all modulo 10⁹ + 7."],
                walk=w3,
                build=["Precompute `pow2[d] = 2ᵈ mod p` for d up to n/2.", "Walk: update depth; at each `()` add `pow2[depth]`.", "Return the sum mod p."],
                code={
                    "python": """
                        class Solution:
                            def boxValue(self, s: str) -> int:
                                MOD = 10**9 + 7
                                pow2 = [1] * (len(s) // 2 + 1)  #@pow
                                for d in range(1, len(pow2)):  #@pow
                                    pow2[d] = pow2[d - 1] * 2 % MOD  #@pow
                                total = depth = 0  #@init
                                for i, c in enumerate(s):  #@loop
                                    if c == "(":  #@open
                                        depth += 1  #@open
                                    else:  #@close
                                        depth -= 1  #@close
                                        if s[i - 1] == "(":  #@pair
                                            total = (total + pow2[depth]) % MOD  #@pair
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int boxValue(String s) {
                                final long MOD = 1_000_000_007L;
                                int n = s.length();
                                long[] pow2 = new long[n / 2 + 1];  //@pow
                                pow2[0] = 1;  //@pow
                                for (int d = 1; d < pow2.length; d++) pow2[d] = pow2[d - 1] * 2 % MOD;  //@pow
                                long total = 0;  //@init
                                int depth = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@loop
                                    if (s.charAt(i) == '(') depth++;  //@open
                                    else {  //@close
                                        depth--;  //@close
                                        if (s.charAt(i - 1) == '(') total = (total + pow2[depth]) % MOD;  //@pair
                                    }
                                }
                                return (int) total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int boxValue(string& s) {
                                const long long MOD = 1000000007LL;
                                int n = s.size();
                                vector<long long> pow2(n / 2 + 1, 1);  //@pow
                                for (int d = 1; d < (int) pow2.size(); d++) pow2[d] = pow2[d - 1] * 2 % MOD;  //@pow
                                long long total = 0;  //@init
                                int depth = 0;  //@init
                                for (int i = 0; i < n; i++) {  //@loop
                                    if (s[i] == '(') depth++;  //@open
                                    else {  //@close
                                        depth--;  //@close
                                        if (s[i - 1] == '(') total = (total + pow2[depth]) % MOD;  //@pair
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int boxValue(char* s) {
                            const long long MOD = 1000000007LL;
                            int n = strlen(s);
                            long long* pow2 = malloc((n / 2 + 1) * sizeof(long long));  //@pow
                            pow2[0] = 1;  //@pow
                            for (int d = 1; d <= n / 2; d++) pow2[d] = pow2[d - 1] * 2 % MOD;  //@pow
                            long long total = 0;  //@init
                            int depth = 0;  //@init
                            for (int i = 0; i < n; i++) {  //@loop
                                if (s[i] == '(') depth++;  //@open
                                else {  //@close
                                    depth--;  //@close
                                    if (s[i - 1] == '(') total = (total + pow2[depth]) % MOD;  //@pair
                                }
                            }
                            free(pow2);  //@ret
                            return (int) total;  //@ret
                        }
                    """,
                },
                lines=[("pow", "Powers of two up to the deepest possible nesting (n/2), reduced modulo 10⁹ + 7. (A table of n/2 numbers; a running power that doubles and halves with depth would avoid it but needs modular halving.)"), ("init", "Running sum and current depth."), ("loop", "One pass."), ("open", "One level deeper."), ("close", "Back out one level; `depth` is now the number of boxes around this pair."), ("pair", "`(` immediately followed by `)`: an innermost box worth 2^depth."), ("ret", "The value mod 10⁹ + 7.")],
                complexity=["**Time O(n).** **Space O(n)** for the power table here; O(1) extra beyond it if powers are tracked incrementally."],
            ),
        ],
        takeaways=[
            """
            - Evaluate nested grammars with a **stack of partial results**: push on open, fold into the parent on close.
            - Look for a closed form: here each `()` contributes 2^depth, so only depth matters.
            - Apply the modulus at every addition and doubling to keep numbers small.
            """
        ],
    )


@problem
def strip_stray_brackets():
    s = "a)b(c(d)e)f)(g"

    def strip(t):
        drop, st = set(), []
        for i, c in enumerate(t):
            if c == "(":
                st.append(i)
            elif c == ")":
                if st:
                    st.pop()
                else:
                    drop.add(i)
        drop.update(st)
        return "".join(c for i, c in enumerate(t) if i not in drop), drop

    want, dropped = strip(s)

    w1 = Steps("Push each '(' index. A ')' pops its partner, or is stray if the stack is empty. '(' left on the stack at the end are stray too.")
    st, drop = [], []
    for i, c in enumerate(s):
        if c == "(":
            st.append(i)
            w1.step(f"'(' at {i}: push.", Row(list(s), st={i: "active"}, slots=True), Row(list(st), label="open '(' indices"))
        elif c == ")":
            if st:
                j = st.pop()
                w1.step(f"')' at {i} matches '(' at {j}.", Row(list(s), st={i: "found", j: "found"}, slots=True), Row(list(st), label="open '(' indices"))
            else:
                drop.append(i)
                w1.step(f"')' at {i}: nothing open → stray.", Row(list(s), st={i: "mark"}, slots=True), Row(list(st), label="open '(' indices"))
    w1.step(f"Leftover '(' {st} are stray too. Remove positions {sorted(drop + st)}: '{want}'.", Row(list(s), st={k: "mark" for k in drop + st}, slots=True), result=want)

    w2 = Steps("Pass 1 (left to right) drops ')' that have no open '('. Pass 2 (right to left) drops '(' that have no ')' after them.")
    keep1, bal = [], 0
    for c in s:
        if c == ")":
            if bal == 0:
                continue
            bal -= 1
        elif c == "(":
            bal += 1
        keep1.append(c)
    w2.step(f"After pass 1 (stray ')' removed): '{''.join(keep1)}', with {bal} '(' still open.", Row(keep1, slots=True))
    out, bal2 = [], 0
    for c in reversed(keep1):
        if c == "(":
            if bal2 == 0:
                continue
            bal2 -= 1
        elif c == ")":
            bal2 += 1
        out.append(c)
    res = "".join(reversed(out))
    w2.step(f"After pass 2 (unclosed '(' removed from the right): '{res}'.", Row(list(res), slots=True), result=res)

    sol(
        "strip-stray-brackets",
        summary="""
            A bracket must be removed exactly when it has no partner: a `)` that arrives with nothing open, or a `(` never
            closed. Matching with a stack (or two counter passes) identifies exactly those, and removing only them is the
            minimum. O(n).
        """,
        question=[
            """
            Remove the fewest brackets so the remaining brackets are balanced; letters stay. Return any valid result.

            - **Letters never move or disappear.**
            - **Several answers can be valid** (which of two equivalent `)` to drop); any one is accepted.
            - **Removing unmatched brackets is enough and necessary:** every unmatched bracket must go, and once they're
              gone the rest is balanced.
            """
        ],
        think=[
            f"""
            Take `{s}`. Match brackets left to right: the first `)` has nothing open (stray). `(c(d)e)` is fully matched.
            The `)` after `f` has nothing open (stray). The final `(` is never closed (stray). Removing those three gives
            `{want}`.
            """,
            fig(Row(list(s), st={k: "mark" for k in dropped}, slots=True), caption="The stray brackets (marked) are exactly the unmatched ones."),
            """
            Why is that the minimum? Each unmatched bracket must be removed (nothing can partner with it), and removing
            only those leaves every remaining bracket with its partner. Greedy left-to-right matching (each `)` with the most
            recent open `(`) finds a maximum set of matched pairs, so it leaves the fewest strays.
            """,
        ],
        approaches=[
            approach(
                "Stack of '(' positions",
                "better",
                "O(n)",
                "O(n)",
                idea=["Scan once: push the index of every `(`; on `)`, pop a partner if any, otherwise mark the `)` for removal. After the scan, every index still on the stack is an unclosed `(`: mark those too. Build the result without the marked positions."],
                walk=w1,
                build=["Stack of `(` indices; a set (or boolean array) of indices to drop.", "Scan and match.", "Mark the leftover `(`.", "Copy every unmarked character."],
                code={
                    "python": """
                        class Solution:
                            def stripStray(self, s: str) -> str:
                                stack, drop = [], set()  #@init
                                for i, c in enumerate(s):  #@scan
                                    if c == "(":  #@scan
                                        stack.append(i)  #@scan
                                    elif c == ")":  #@scan
                                        if stack:  #@scan
                                            stack.pop()  #@scan
                                        else:  #@scan
                                            drop.add(i)  #@scan
                                drop.update(stack)  #@left
                                return "".join(c for i, c in enumerate(s) if i not in drop)  #@build
                    """,
                    "java": """
                        class Solution {
                            public String stripStray(String s) {
                                int n = s.length();
                                Deque<Integer> stack = new ArrayDeque<>();  //@init
                                boolean[] drop = new boolean[n];  //@init
                                for (int i = 0; i < n; i++) {  //@scan
                                    char c = s.charAt(i);  //@scan
                                    if (c == '(') stack.push(i);  //@scan
                                    else if (c == ')') {  //@scan
                                        if (!stack.isEmpty()) stack.pop();  //@scan
                                        else drop[i] = true;  //@scan
                                    }
                                }
                                for (int i : stack) drop[i] = true;  //@left
                                StringBuilder out = new StringBuilder();  //@build
                                for (int i = 0; i < n; i++) if (!drop[i]) out.append(s.charAt(i));  //@build
                                return out.toString();  //@build
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string stripStray(string& s) {
                                int n = s.size();
                                vector<int> stack;  //@init
                                vector<bool> drop(n, false);  //@init
                                for (int i = 0; i < n; i++) {  //@scan
                                    if (s[i] == '(') stack.push_back(i);  //@scan
                                    else if (s[i] == ')') {  //@scan
                                        if (!stack.empty()) stack.pop_back();  //@scan
                                        else drop[i] = true;  //@scan
                                    }
                                }
                                for (int i : stack) drop[i] = true;  //@left
                                string out;  //@build
                                for (int i = 0; i < n; i++) if (!drop[i]) out += s[i];  //@build
                                return out;  //@build
                            }
                        };
                    """,
                    "c": """
                        char* stripStray(char* s) {
                            int n = strlen(s), top = 0;
                            int* stack = malloc((n + 1) * sizeof(int));  //@init
                            bool* drop = calloc(n + 1, sizeof(bool));  //@init
                            for (int i = 0; i < n; i++) {  //@scan
                                if (s[i] == '(') stack[top++] = i;  //@scan
                                else if (s[i] == ')') {  //@scan
                                    if (top > 0) top--;  //@scan
                                    else drop[i] = true;  //@scan
                                }
                            }
                            while (top > 0) drop[stack[--top]] = true;  //@left
                            char* out = malloc(n + 1);  //@build
                            int w = 0;  //@build
                            for (int i = 0; i < n; i++) if (!drop[i]) out[w++] = s[i];  //@build
                            out[w] = '\\0';  //@build
                            free(stack);  //@build
                            free(drop);  //@build
                            return out;  //@build
                        }
                    """,
                },
                lines=[("init", "Indices of open `(`, and which positions to drop."), ("scan", "Each `)` closes the most recent open `(`; with none open, it's stray."), ("left", "`(` still open at the end are never closed: stray."), ("build", "Keep everything that isn't marked, letters included.")],
                complexity=["**Time O(n).** **Space O(n)** for the stack and marks."],
                limits=["The stack only needs to know *how many* `(` are open, not where, if strays are removed in two directional passes."],
            ),
            approach(
                "Two counting passes",
                "best",
                "O(n)",
                "O(1)",
                idea=["Pass 1, left to right: keep a balance; skip any `)` when the balance is 0 (stray), otherwise copy. Pass 2, right to left over that result: skip any `(` when the balance of `)` seen is 0 (an unclosed `(`), otherwise copy. Reverse."],
                walk=w2,
                build=["Left-to-right: drop `)` with no open `(`.", "Right-to-left: drop `(` with no `)` after it.", "Return the kept characters in order."],
                code={
                    "python": """
                        class Solution:
                            def stripStray(self, s: str) -> str:
                                first, open_ = [], 0  #@pass1
                                for c in s:  #@pass1
                                    if c == ")":  #@pass1
                                        if open_ == 0:  #@pass1
                                            continue  #@pass1
                                        open_ -= 1  #@pass1
                                    elif c == "(":  #@pass1
                                        open_ += 1  #@pass1
                                    first.append(c)  #@pass1
                                out, close = [], 0  #@pass2
                                for c in reversed(first):  #@pass2
                                    if c == "(":  #@pass2
                                        if close == 0:  #@pass2
                                            continue  #@pass2
                                        close -= 1  #@pass2
                                    elif c == ")":  #@pass2
                                        close += 1  #@pass2
                                    out.append(c)  #@pass2
                                return "".join(reversed(out))  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String stripStray(String s) {
                                StringBuilder first = new StringBuilder();  //@pass1
                                int open = 0;  //@pass1
                                for (char c : s.toCharArray()) {  //@pass1
                                    if (c == ')') { if (open == 0) continue; open--; }  //@pass1
                                    else if (c == '(') open++;  //@pass1
                                    first.append(c);  //@pass1
                                }
                                StringBuilder out = new StringBuilder();  //@pass2
                                int close = 0;  //@pass2
                                for (int i = first.length() - 1; i >= 0; i--) {  //@pass2
                                    char c = first.charAt(i);  //@pass2
                                    if (c == '(') { if (close == 0) continue; close--; }  //@pass2
                                    else if (c == ')') close++;  //@pass2
                                    out.append(c);  //@pass2
                                }
                                return out.reverse().toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string stripStray(string& s) {
                                string first;  //@pass1
                                int open = 0;  //@pass1
                                for (char c : s) {  //@pass1
                                    if (c == ')') { if (open == 0) continue; open--; }  //@pass1
                                    else if (c == '(') open++;  //@pass1
                                    first += c;  //@pass1
                                }
                                string out;  //@pass2
                                int close = 0;  //@pass2
                                for (int i = (int) first.size() - 1; i >= 0; i--) {  //@pass2
                                    char c = first[i];  //@pass2
                                    if (c == '(') { if (close == 0) continue; close--; }  //@pass2
                                    else if (c == ')') close++;  //@pass2
                                    out += c;  //@pass2
                                }
                                reverse(out.begin(), out.end());  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* stripStray(char* s) {
                            int n = strlen(s), w = 0, open = 0;
                            char* buf = malloc(n + 1);  //@pass1
                            for (int i = 0; i < n; i++) {  //@pass1
                                char c = s[i];  //@pass1
                                if (c == ')') { if (open == 0) continue; open--; }  //@pass1
                                else if (c == '(') open++;  //@pass1
                                buf[w++] = c;  //@pass1
                            }
                            int close = 0, r = w;  //@pass2
                            for (int i = w - 1; i >= 0; i--) {  //@pass2
                                char c = buf[i];  //@pass2
                                if (c == '(') { if (close == 0) continue; close--; }  //@pass2
                                else if (c == ')') close++;  //@pass2
                                buf[--r] = c;  //@pass2
                            }
                            memmove(buf, buf + r, w - r);  //@ret
                            buf[w - r] = '\\0';  //@ret
                            return buf;  //@ret
                        }
                    """,
                },
                lines=[("pass1", "Left to right: a `)` with no open `(` is stray and skipped; everything else is kept. Afterwards every `)` has a partner, but some `(` may be left open."), ("pass2", "Right to left over the kept text: a `(` with no `)` after it is an unclosed opener and is skipped.", {"c": "Written backwards into the same buffer from its end, so kept characters end up in order at the back of the buffer."}), ("ret", "Reverse back into reading order.", {"c": "Slide the kept block to the front and terminate it."})],
                complexity=["**Time O(n):** two passes. **Space O(1)** besides the output being built."],
            ),
        ],
        takeaways=[
            """
            - **Remove the minimum to balance** = remove exactly the unmatched brackets.
            - Unmatched `)` are found left to right; unmatched `(` right to left (or as leftovers on a stack).
            """
        ],
    )
