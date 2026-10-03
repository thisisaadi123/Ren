"""Stacks & Queues: building strings with a stack."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def typing_with_backspace():
    a, b = "xy#z##w", "q#xw"

    def screen(keys):
        out = []
        for c in keys:
            if c == "#":
                if out:
                    out.pop()
            else:
                out.append(c)
        return "".join(out)

    w1 = Steps("Replay each person's keystrokes into a stack: letters push, '#' pops.")
    for name, keys in (("a", a), ("b", b)):
        out = []
        for i, c in enumerate(keys):
            if c == "#":
                if out:
                    out.pop()
            else:
                out.append(c)
            w1.step(f"{name}: key '{c}' → screen '{''.join(out)}'.", Row(list(keys), st={i: "active"}, label=name), Row(list(out), label="screen"))
    w1.step(f"Both screens show '{screen(a)}' and '{screen(b)}': {'equal' if screen(a) == screen(b) else 'different'}.", Row(list(screen(a)), label="a"), Row(list(screen(b)), label="b"), result="true" if screen(a) == screen(b) else "false")

    w2 = Steps("Walk both strings from the end. Skip characters that a later '#' deletes; compare the surviving characters one by one.")
    i, j = len(a) - 1, len(b) - 1
    while True:
        si = sk = 0
        while i >= 0 and (a[i] == "#" or si):
            si += 1 if a[i] == "#" else -1
            i -= 1
        while j >= 0 and (b[j] == "#" or sk):
            sk += 1 if b[j] == "#" else -1
            j -= 1
        ca = a[i] if i >= 0 else None
        cb = b[j] if j >= 0 else None
        if ca is None and cb is None:
            w2.step("Both ran out together: the screens match.", Row(list(a), label="a"), Row(list(b), label="b"), result="true")
            break
        if ca != cb:
            w2.step(f"Survivors differ: {ca!r} vs {cb!r}.", Row(list(a), st={i: "mark"} if i >= 0 else None, label="a"), Row(list(b), st={j: "mark"} if j >= 0 else None, label="b"), result="false")
            break
        w2.step(f"Next surviving characters from the end: '{ca}' and '{cb}' match.", Row(list(a), st={i: "found"}, label="a"), Row(list(b), st={j: "found"}, label="b"))
        i -= 1
        j -= 1

    sol(
        "typing-with-backspace",
        summary="""
            Simulate each text box with a stack (letters push, `#` pops) and compare the results: O(n + m). To avoid building
            the texts, read both inputs **backwards**: a `#` means "skip the next real character to the left", so the
            surviving characters come out in reverse order and can be compared on the fly in O(1) space.
        """,
        question=[
            """
            `#` is a backspace that deletes the previous character, if any. Return whether both keystroke sequences produce
            the same text.

            - **Backspace on empty text does nothing:** `"##a"` shows `a`.
            - **Several backspaces chain:** `"ab##"` shows nothing.
            - **Only the final text matters**, not how it was typed.
            """
        ],
        think=[
            f"""
            Take `a = "{a}"` and `b = "{b}"`. Typing `a`: x, y, ⌫ (removes y), z, ⌫ (removes z), ⌫ (removes x), w → "w".
            Typing `b`: q, ⌫, x, w → "xw". Different.
            """,
            fig(Row(list(screen(a)), label="a shows"), Row(list(screen(b)), label="b shows")),
            """
            The forward simulation is a stack. For O(1) space, notice that a character's fate depends only on what comes
            **after** it: it survives unless there are more unconsumed `#` to its right. So scan from the end, counting
            pending backspaces, and you meet the surviving characters last-to-first.
            """,
        ],
        approaches=[
            approach(
                "Build both texts with a stack",
                "better",
                "O(n + m)",
                "O(n + m)",
                idea=["For each input: letters are pushed; `#` pops if the stack isn't empty. Compare the two stacks."],
                walk=w1,
                build=["Write `screen(keys)` with a stack.", "Return `screen(a) == screen(b)`."],
                code={
                    "python": """
                        class Solution:
                            def sameText(self, a: str, b: str) -> bool:
                                def screen(keys):  #@screen
                                    out = []  #@screen
                                    for c in keys:  #@screen
                                        if c == "#":  #@screen
                                            if out:  #@screen
                                                out.pop()  #@screen
                                        else:  #@screen
                                            out.append(c)  #@screen
                                    return out  #@screen
                                return screen(a) == screen(b)  #@cmp
                    """,
                    "java": """
                        class Solution {
                            public boolean sameText(String a, String b) {
                                return screen(a).equals(screen(b));  //@cmp
                            }

                            private String screen(String keys) {  //@screen
                                StringBuilder out = new StringBuilder();  //@screen
                                for (char c : keys.toCharArray()) {  //@screen
                                    if (c == '#') { if (out.length() > 0) out.deleteCharAt(out.length() - 1); }  //@screen
                                    else out.append(c);  //@screen
                                }  //@screen
                                return out.toString();  //@screen
                            }  //@screen
                        }
                    """,
                    "cpp": """
                        class Solution {
                            string screen(const string& keys) {  //@screen
                                string out;  //@screen
                                for (char c : keys) {  //@screen
                                    if (c == '#') { if (!out.empty()) out.pop_back(); }  //@screen
                                    else out.push_back(c);  //@screen
                                }  //@screen
                                return out;  //@screen
                            }  //@screen

                        public:
                            bool sameText(string& a, string& b) {
                                return screen(a) == screen(b);  //@cmp
                            }
                        };
                    """,
                    "c": """
                        // Rewrites keys into out (as a stack) and returns the text length.
                        static int screen(const char* keys, char* out) {  //@screen
                            int top = 0;  //@screen
                            for (const char* p = keys; *p; p++) {  //@screen
                                if (*p == '#') { if (top > 0) top--; }  //@screen
                                else out[top++] = *p;  //@screen
                            }  //@screen
                            return top;  //@screen
                        }  //@screen

                        bool sameText(char* a, char* b) {
                            char* x = malloc(strlen(a) + 1);  //@cmp
                            char* y = malloc(strlen(b) + 1);  //@cmp
                            int nx = screen(a, x), ny = screen(b, y);  //@cmp
                            bool same = nx == ny && memcmp(x, y, nx) == 0;  //@cmp
                            free(x);  //@cmp
                            free(y);  //@cmp
                            return same;  //@cmp
                        }
                    """,
                },
                lines=[("screen", "Replay keystrokes: a letter goes on top; `#` removes the top letter if there is one."), ("cmp", "Same final text?")],
                complexity=["**Time O(n + m).** **Space O(n + m)** for the two texts."],
                limits=["Builds both texts in full even when they differ early at the end. Reading backwards needs no extra memory."],
            ),
            approach(
                "Two pointers from the end",
                "best",
                "O(n + m)",
                "O(1)",
                idea=["Pointers i and j at the ends. For each, skip backwards over characters deleted by later `#` (count pending backspaces: `#` adds one, a letter consumes one). Compare the next survivors; move both on. Equal all the way, and both exhausted together, means equal texts."],
                walk=w2,
                build=["Write `next(s, i)`: from i leftwards, return the index of the next surviving letter (or −1).", "Loop: compare `a[i]` with `b[j]` at the survivors; stop on a mismatch or when either runs out."],
                code={
                    "python": """
                        class Solution:
                            def sameText(self, a: str, b: str) -> bool:
                                def survivor(s, i):  #@skip
                                    skip = 0  #@skip
                                    while i >= 0:  #@skip
                                        if s[i] == "#":  #@skip
                                            skip += 1  #@skip
                                        elif skip:  #@skip
                                            skip -= 1  #@skip
                                        else:  #@skip
                                            return i  #@skip
                                        i -= 1  #@skip
                                    return -1  #@skip
                                i, j = len(a) - 1, len(b) - 1  #@init
                                while True:  #@loop
                                    i, j = survivor(a, i), survivor(b, j)  #@loop
                                    if i < 0 or j < 0:  #@end
                                        return i < 0 and j < 0  #@end
                                    if a[i] != b[j]:  #@cmp
                                        return False  #@cmp
                                    i, j = i - 1, j - 1  #@cmp
                    """,
                    "java": """
                        class Solution {
                            public boolean sameText(String a, String b) {
                                int i = a.length() - 1, j = b.length() - 1;  //@init
                                while (true) {  //@loop
                                    i = survivor(a, i);  //@loop
                                    j = survivor(b, j);  //@loop
                                    if (i < 0 || j < 0) return i < 0 && j < 0;  //@end
                                    if (a.charAt(i) != b.charAt(j)) return false;  //@cmp
                                    i--;  //@cmp
                                    j--;  //@cmp
                                }
                            }

                            private int survivor(String s, int i) {  //@skip
                                int skip = 0;  //@skip
                                for (; i >= 0; i--) {  //@skip
                                    if (s.charAt(i) == '#') skip++;  //@skip
                                    else if (skip > 0) skip--;  //@skip
                                    else return i;  //@skip
                                }  //@skip
                                return -1;  //@skip
                            }  //@skip
                        }
                    """,
                    "cpp": """
                        class Solution {
                            int survivor(const string& s, int i) {  //@skip
                                int skip = 0;  //@skip
                                for (; i >= 0; i--) {  //@skip
                                    if (s[i] == '#') skip++;  //@skip
                                    else if (skip > 0) skip--;  //@skip
                                    else return i;  //@skip
                                }  //@skip
                                return -1;  //@skip
                            }  //@skip

                        public:
                            bool sameText(string& a, string& b) {
                                int i = a.size() - 1, j = b.size() - 1;  //@init
                                while (true) {  //@loop
                                    i = survivor(a, i);  //@loop
                                    j = survivor(b, j);  //@loop
                                    if (i < 0 || j < 0) return i < 0 && j < 0;  //@end
                                    if (a[i] != b[j]) return false;  //@cmp
                                    i--;  //@cmp
                                    j--;  //@cmp
                                }
                            }
                        };
                    """,
                    "c": """
                        static int survivor(const char* s, int i) {  //@skip
                            int skip = 0;  //@skip
                            for (; i >= 0; i--) {  //@skip
                                if (s[i] == '#') skip++;  //@skip
                                else if (skip > 0) skip--;  //@skip
                                else return i;  //@skip
                            }  //@skip
                            return -1;  //@skip
                        }  //@skip

                        bool sameText(char* a, char* b) {
                            int i = strlen(a) - 1, j = strlen(b) - 1;  //@init
                            while (1) {  //@loop
                                i = survivor(a, i);  //@loop
                                j = survivor(b, j);  //@loop
                                if (i < 0 || j < 0) return i < 0 && j < 0;  //@end
                                if (a[i] != b[j]) return false;  //@cmp
                                i--;  //@cmp
                                j--;  //@cmp
                            }
                        }
                    """,
                },
                lines=[("skip", "From position i leftwards: each `#` means one more letter to the left is deleted; a letter either cancels a pending backspace or is the next survivor."), ("init", "Start at both ends."), ("loop", "Jump both pointers to their next surviving letters."), ("end", "If either text is exhausted, they're equal only if both are."), ("cmp", "Survivors must match; then move past them.")],
                complexity=["**Time O(n + m):** each character is passed once. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Backspace processing is a stack; reading **backwards** with a pending-deletes counter avoids the stack.
            - When an element's fate depends on what comes after it, try scanning from the end.
            """
        ],
    )


@problem
def tidy_the_path():
    path = "/usr//local/./bin/../lib/.../"

    def tidy(p):
        st = []
        for part in p.split("/"):
            if part == "..":
                if st:
                    st.pop()
            elif part and part != ".":
                st.append(part)
        return "/" + "/".join(st)

    want = tidy(path)

    w1 = Steps("Repeatedly apply text rewrites: '//' → '/', '/./' → '/', '/name/../' → '/', until nothing changes.")
    t = path + "/"
    w1.step(f"Add a trailing '/' so every part is wrapped in slashes: {t}", Vars(path=t))
    import re
    changed = True
    while changed:
        changed = False
        for pat, rep, label in ((r"//+", "/", "collapse repeated slashes"), (r"/\./", "/", "drop a '.' part"), (r"/(?!\.\./)[^/]+/\.\./", "/", "cancel 'name/..'"), (r"^/\.\./", "/", "'..' at the root stays at the root")):
            nt = re.sub(pat, rep, t, count=1)
            if nt != t:
                w1.step(f"{label}: {nt}", Vars(path=nt))
                t = nt
                changed = True
                break
    final = t.rstrip("/") or "/"
    w1.step(f"Drop the trailing slash: {final}", Vars(path=final), result=final)

    w2 = Steps("Split on '/', then use a stack of folder names: skip empty parts and '.', pop on '..', push anything else.")
    st = []
    for part in path.split("/"):
        if part == "..":
            if st:
                st.pop()
            note = "'..' → go up (pop)."
        elif part and part != ".":
            st.append(part)
            note = f"'{part}' → push."
        else:
            note = f"'{part}' → ignore." if part else "empty part (from '//' or the ends) → ignore."
        w2.step(note, Row(list(st), label="folders"))
    w2.step(f"Join with '/': {want}", Row(list(st), label="folders"), result=want)

    sol(
        "tidy-the-path",
        summary="""
            Split the path on `/` and process the parts with a stack of folder names: empty parts and `.` change nothing,
            `..` pops (if anything is there), and every other name is pushed. Join the stack with `/` behind a leading `/`.
            O(n).
        """,
        question=[
            """
            Rewrite an absolute path into its tidy form: single slashes, no `.` or `..`, no trailing slash (except the root
            itself).

            - **`..` at the root stays at the root:** `/../a` → `/a`.
            - **`...` is just a folder name**, as is anything that isn't exactly `.` or `..`.
            - **Repeated slashes collapse:** `/a//b` → `/a/b`.
            """
        ],
        think=[
            f"""
            Take `{path}`. Reading folder by folder: `usr`, `local`, `.` (stay), `bin`, `..` (back out of bin), `lib`,
            `...` (a normal name). Result: `{want}`.
            """,
            fig(Row(path.split("/"), label="parts after splitting on '/'"), Row(want.strip("/").split("/"), label="kept"), caption="Empty parts come from repeated or trailing slashes."),
            """
            `..` undoes the most recently entered folder: last in, first out. That's a stack of folder names.
            """,
        ],
        approaches=[
            approach(
                "Rewrite the text until it stops changing",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Apply local rewrite rules repeatedly: collapse `//`, delete `/./`, cancel `/name/../`, and turn a leading `/../` into `/`. When nothing applies, trim the trailing slash."],
                walk=w1,
                build=["Append `/` so every part is surrounded by slashes.", "Loop over the rules until a full round changes nothing.", "Remove the trailing `/` (keep `/` for the root)."],
                code={
                    "python": """
                        import re

                        class Solution:
                            def tidyPath(self, path: str) -> str:
                                t = path + "/"  #@wrap
                                rules = [(r"//+", "/"), (r"/\\./", "/"), (r"/(?!\\.\\./)[^/]+/\\.\\./", "/"), (r"^/\\.\\./", "/")]  #@rules
                                changed = True  #@loop
                                while changed:  #@loop
                                    changed = False  #@loop
                                    for pattern, repl in rules:  #@loop
                                        new = re.sub(pattern, repl, t, count=1)  #@loop
                                        if new != t:  #@loop
                                            t, changed = new, True  #@loop
                                return t.rstrip("/") or "/"  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String tidyPath(String path) {
                                String t = path + "/";  //@wrap
                                String[][] rules = {{"//+", "/"}, {"/\\\\./", "/"}, {"/(?!\\\\.\\\\./)[^/]+/\\\\.\\\\./", "/"}, {"^/\\\\.\\\\./", "/"}};  //@rules
                                boolean changed = true;  //@loop
                                while (changed) {  //@loop
                                    changed = false;  //@loop
                                    for (String[] r : rules) {  //@loop
                                        String next = t.replaceFirst(r[0], r[1]);  //@loop
                                        if (!next.equals(t)) { t = next; changed = true; }  //@loop
                                    }
                                }
                                while (t.length() > 1 && t.endsWith("/")) t = t.substring(0, t.length() - 1);  //@ret
                                return t;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            // One rewrite step on t (which always ends with '/'); returns true if something changed.
                            bool rewrite(string& t) {  //@rules
                                int n = t.size();  //@rules
                                for (int i = 0; i + 1 < n; i++) {  //@rules
                                    if (t[i] != '/') continue;  //@rules
                                    int j = i + 1;  //@rules
                                    while (j < n && t[j] != '/') j++;  //@rules
                                    if (j == n) break;  //@rules
                                    string part = t.substr(i + 1, j - i - 1);  //@rules
                                    if (part.empty() || part == ".") { t.erase(i, j - i); return true; }  //@rules
                                    if (part == "..") {  //@rules
                                        int s = i - 1;  //@rules
                                        while (s >= 0 && t[s] != '/') s--;  //@rules
                                        if (s < 0) s = i;  //@rules
                                        t.erase(s, j - s);  //@rules
                                        return true;  //@rules
                                    }  //@rules
                                }  //@rules
                                return false;  //@rules
                            }  //@rules

                        public:
                            string tidyPath(string& path) {
                                string t = path + "/";  //@wrap
                                while (rewrite(t)) {}  //@loop
                                while (t.size() > 1 && t.back() == '/') t.pop_back();  //@ret
                                return t;  //@ret
                            }
                        };
                    """,
                    "c": """
                        // One rewrite step on t (which always ends with '/'); returns true if something changed.
                        static bool rewrite(char* t) {  //@rules
                            int n = strlen(t);  //@rules
                            for (int i = 0; i + 1 < n; i++) {  //@rules
                                if (t[i] != '/') continue;  //@rules
                                int j = i + 1;  //@rules
                                while (j < n && t[j] != '/') j++;  //@rules
                                int len = j - i - 1;  //@rules
                                if (j == n) break;  //@rules
                                if (len == 0 || (len == 1 && t[i + 1] == '.')) {  //@rules
                                    memmove(t + i, t + j, n - j + 1);  //@rules
                                    return true;  //@rules
                                }  //@rules
                                if (len == 2 && t[i + 1] == '.' && t[i + 2] == '.') {  //@rules
                                    int s = i - 1;  //@rules
                                    while (s >= 0 && t[s] != '/') s--;  //@rules
                                    if (s < 0) s = i;  //@rules
                                    memmove(t + s, t + j, n - j + 1);  //@rules
                                    return true;  //@rules
                                }  //@rules
                            }  //@rules
                            return false;  //@rules
                        }  //@rules

                        char* tidyPath(char* path) {
                            int n = strlen(path);
                            char* t = malloc(n + 2);  //@wrap
                            memcpy(t, path, n);  //@wrap
                            t[n] = '/';  //@wrap
                            t[n + 1] = '\\0';  //@wrap
                            while (rewrite(t)) {}  //@loop
                            int len = strlen(t);  //@ret
                            while (len > 1 && t[len - 1] == '/') t[--len] = '\\0';  //@ret
                            return t;  //@ret
                        }
                    """,
                },
                lines=[("wrap", "A trailing `/` makes every part, including the last, look like `/part/`."), ("rules", "Local simplifications: empty part (`//`), `.` part, `name/..` pair, and `..` right at the root.", {"cpp": "One scan finds the first part that is empty, `.` or `..`, and removes it (for `..`, together with the folder before it, unless it's at the root).", "c": "One scan finds the first part that is empty, `.` or `..`, and removes it (for `..`, together with the folder before it, unless it's at the root)."}), ("loop", "Apply rewrites until none applies."), ("ret", "Remove trailing slashes, keeping a lone `/` for the root.")],
                complexity=["**Time O(n²):** each rewrite rescans and shifts the string. **Space O(n).**"],
                limits=["Each fix rescans from the start. The structure is just \"enter folder / leave folder\", which a stack processes in one pass."],
                slow=True,
            ),
            approach(
                "Split, then a stack of folders",
                "best",
                "O(n)",
                "O(n)",
                idea=["Split on `/`. For each part: empty or `.` → nothing; `..` → pop if non-empty; else push. Answer: `/` + parts joined by `/`."],
                walk=w2,
                build=["Split the path on `/`.", "Process parts with the stack rules.", "Return `\"/\" + join(stack, \"/\")`."],
                code={
                    "python": """
                        class Solution:
                            def tidyPath(self, path: str) -> str:
                                stack = []  #@stack
                                for part in path.split("/"):  #@split
                                    if part == "..":  #@up
                                        if stack:  #@up
                                            stack.pop()  #@up
                                    elif part and part != ".":  #@name
                                        stack.append(part)  #@name
                                return "/" + "/".join(stack)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String tidyPath(String path) {
                                Deque<String> stack = new ArrayDeque<>();  //@stack
                                for (String part : path.split("/")) {  //@split
                                    if (part.equals("..")) { if (!stack.isEmpty()) stack.pollLast(); }  //@up
                                    else if (!part.isEmpty() && !part.equals(".")) stack.addLast(part);  //@name
                                }
                                return "/" + String.join("/", stack);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string tidyPath(string& path) {
                                vector<string> stack;  //@stack
                                stringstream in(path);  //@split
                                string part;  //@split
                                while (getline(in, part, '/')) {  //@split
                                    if (part == "..") { if (!stack.empty()) stack.pop_back(); }  //@up
                                    else if (!part.empty() && part != ".") stack.push_back(part);  //@name
                                }
                                string out;  //@ret
                                for (auto& p : stack) out += "/" + p;  //@ret
                                return out.empty() ? "/" : out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* tidyPath(char* path) {
                            int n = strlen(path), top = 0;
                            int* start = malloc((n + 1) * sizeof(int));  //@stack
                            int* len = malloc((n + 1) * sizeof(int));  //@stack
                            for (int i = 0; i < n;) {  //@split
                                while (i < n && path[i] == '/') i++;  //@split
                                int j = i;  //@split
                                while (j < n && path[j] != '/') j++;  //@split
                                int L = j - i;  //@split
                                if (L == 2 && path[i] == '.' && path[i + 1] == '.') { if (top > 0) top--; }  //@up
                                else if (L > 0 && !(L == 1 && path[i] == '.')) { start[top] = i; len[top] = L; top++; }  //@name
                                i = j;  //@split
                            }
                            char* out = malloc(n + 2);  //@ret
                            int w = 0;  //@ret
                            for (int k = 0; k < top; k++) {  //@ret
                                out[w++] = '/';  //@ret
                                memcpy(out + w, path + start[k], len[k]);  //@ret
                                w += len[k];  //@ret
                            }  //@ret
                            if (w == 0) out[w++] = '/';  //@ret
                            out[w] = '\\0';  //@ret
                            free(start);  //@ret
                            free(len);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("stack", "Folder names currently entered, deepest last.", {"c": "The stack stores where each kept name starts in the input and how long it is; no copying until the end."}), ("split", "Pieces between slashes; repeated or trailing slashes produce empty pieces.", {"cpp": "`getline` with `'/'` as the delimiter yields each piece.", "c": "Skip slashes, then take the run of non-slash characters as the next piece."}), ("up", "`..` leaves the current folder; at the root there's nothing to leave."), ("name", "Anything else that isn't empty or `.` is a folder to enter (including `...`)."), ("ret", "Rebuild with single slashes; an empty stack is the root `/`.")],
                complexity=["**Time O(n).** **Space O(n)** for the parts and the result."],
            ),
        ],
        takeaways=[
            """
            - Path normalisation = **stack of components**: push names, pop on `..`, ignore `.` and empty parts.
            - Split first; work with tokens rather than characters.
            """
        ],
    )


@problem
def crush_the_runs():
    s, k = "abbbacca", 3

    def crush(t):
        st = []
        for c in t:
            if st and st[-1][0] == c:
                st[-1][1] += 1
                if st[-1][1] == k:
                    st.pop()
            else:
                st.append([c, 1])
        return "".join(c * n for c, n in st)

    want = crush(s)

    w1 = Steps(f"Find any run of {k} identical tiles, remove it, and start over; stop when no run is left.")
    t = s
    w1.step(f"Start: {t}", Row(list(t)))
    while True:
        pos = next((i for i in range(len(t) - k + 1) if len(set(t[i:i + k])) == 1), None)
        if pos is None:
            break
        w1.step(f"'{t[pos] * k}' at {pos}: crush it.", Row(list(t), st={q: "mark" for q in range(pos, pos + k)}))
        t = t[:pos] + t[pos + k:]
    w1.step(f"No run of {k} left: '{t}'.", Row(list(t)), result=t)

    w2 = Steps("Stack of (tile, run length). A tile equal to the top extends its run; reaching k pops it. Otherwise push a new run of 1.")
    st = []
    for i, c in enumerate(s):
        if st and st[-1][0] == c:
            st[-1][1] += 1
            if st[-1][1] == k:
                st.pop()
                note = f"'{c}' makes a run of {k}: crush it (pop)."
            else:
                note = f"'{c}' extends the top run to {st[-1][1]}."
        else:
            st.append([c, 1])
            note = f"'{c}' starts a new run."
        w2.step(note, Row(list(s), st={i: "active"}), Row([f"{c}×{n}" for c, n in st], label="stack (tile × run)"))
    w2.step(f"Write the remaining runs out: '{want}'.", Row([f"{c}×{n}" for c, n in st], label="stack"), result=want)

    sol(
        "crush-the-runs",
        summary="""
            Keep a stack of runs: (tile, how many in a row). A new tile either extends the top run or starts a new one; when
            a run reaches k it's crushed by popping it, which automatically lets the run below meet the next tiles. One
            pass, O(n), and the result is the stack's runs written out.
        """,
        question=[
            """
            Repeatedly crush any k identical adjacent tiles until none remain. Return the final row.

            - **Chain reactions:** crushing `bbb` in `abbba` (k = 3) brings the two `a`s together, and with a third `a` they
              could crush too.
            - **The order of crushes doesn't change the result** (given in the statement), so any convenient order works.
            - **Size:** up to 10⁵ tiles; repeatedly rescanning after each crush is too slow.
            """
        ],
        think=[
            f"""
            Take `{s}` with k = {k}. Crush `bbb`: `aacca`. No other run of 3 yet... `cc` isn't long enough, so the result is
            `{want}`.
            """,
            fig(Row(list(s), st={1: "mark", 2: "mark", 3: "mark"}), Row(list(want), label="result")),
            """
            A crush affects only what's immediately to its left and right. Process tiles left to right while remembering the
            runs to the left: when a run is completed and removed, the run before it becomes the new neighbour of the next
            tile. "The most recent unfinished run" is the top of a stack; storing counts with each run makes the k-check
            O(1).
            """,
        ],
        approaches=[
            approach(
                "Find and crush, repeat",
                "brute",
                "O(n² / k)",
                "O(n)",
                idea=["Scan for any k identical adjacent tiles; remove them; rescan from the start. Stop when a full scan finds nothing."],
                walk=w1,
                build=["Loop: scan, keeping the length of the current run of equal tiles.", "When it reaches k, cut those tiles out and restart.", "Stop when a scan completes with no cut."],
                code={
                    "python": """
                        class Solution:
                            def crushRuns(self, s: str, k: int) -> str:
                                changed = True  #@loop
                                while changed:  #@loop
                                    changed = False  #@loop
                                    run = 1  #@scan
                                    for i in range(1, len(s) + 1):  #@scan
                                        if i < len(s) and s[i] == s[i - 1]:  #@scan
                                            run += 1  #@scan
                                            if run == k:  #@cut
                                                s = s[:i - k + 1] + s[i + 1:]  #@cut
                                                changed = True  #@cut
                                                break  #@cut
                                        else:  #@scan
                                            run = 1  #@scan
                                return s  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String crushRuns(String s, int k) {
                                StringBuilder t = new StringBuilder(s);  //@loop
                                boolean changed = true;  //@loop
                                while (changed) {  //@loop
                                    changed = false;  //@loop
                                    int run = 1;  //@scan
                                    for (int i = 1; i < t.length(); i++) {  //@scan
                                        run = t.charAt(i) == t.charAt(i - 1) ? run + 1 : 1;  //@scan
                                        if (run == k) {  //@cut
                                            t.delete(i - k + 1, i + 1);  //@cut
                                            changed = true;  //@cut
                                            break;  //@cut
                                        }
                                    }
                                }
                                return t.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string crushRuns(string& s, int k) {
                                string t = s;  //@loop
                                bool changed = true;  //@loop
                                while (changed) {  //@loop
                                    changed = false;  //@loop
                                    int run = 1;  //@scan
                                    for (int i = 1; i < (int) t.size(); i++) {  //@scan
                                        run = t[i] == t[i - 1] ? run + 1 : 1;  //@scan
                                        if (run == k) {  //@cut
                                            t.erase(i - k + 1, k);  //@cut
                                            changed = true;  //@cut
                                            break;  //@cut
                                        }
                                    }
                                }
                                return t;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* crushRuns(char* s, int k) {
                            int n = strlen(s);
                            char* t = malloc(n + 1);  //@loop
                            memcpy(t, s, n + 1);  //@loop
                            bool changed = true;  //@loop
                            while (changed) {  //@loop
                                changed = false;  //@loop
                                int run = 1, len = strlen(t);  //@scan
                                for (int i = 1; i < len; i++) {  //@scan
                                    run = t[i] == t[i - 1] ? run + 1 : 1;  //@scan
                                    if (run == k) {  //@cut
                                        memmove(t + i - k + 1, t + i + 1, len - i);  //@cut
                                        changed = true;  //@cut
                                        break;  //@cut
                                    }
                                }
                            }
                            return t;  //@ret
                        }
                    """,
                },
                lines=[("loop", "Keep going while the last scan crushed something."), ("scan", "Length of the current run of equal tiles."), ("cut", "A run of k: remove it and rescan from the beginning (neighbours may now form new runs)."), ("ret", "Nothing left to crush.")],
                complexity=["**Time O(n² / k)** scans of O(n) each in the worst case (each crush removes k tiles). **Space O(n).**"],
                limits=["Every crush triggers a full rescan, although only the tiles around the crush can change. A stack keeps exactly that neighbourhood at hand."],
                slow=True,
            ),
            approach(
                "Stack of (tile, run length)",
                "best",
                "O(n)",
                "O(n)",
                idea=["For each tile: if it equals the top run's tile, increment that run's count, popping it when the count hits k; otherwise push (tile, 1). Finally, write each remaining run out."],
                walk=w2,
                build=["Stack of `[tile, count]`.", "Extend or push; pop at count k.", "Concatenate `tile × count` for the remaining runs."],
                code={
                    "python": """
                        class Solution:
                            def crushRuns(self, s: str, k: int) -> str:
                                stack = []  #@stack
                                for c in s:  #@loop
                                    if stack and stack[-1][0] == c:  #@extend
                                        stack[-1][1] += 1  #@extend
                                        if stack[-1][1] == k:  #@crush
                                            stack.pop()  #@crush
                                    else:  #@push
                                        stack.append([c, 1])  #@push
                                return "".join(c * n for c, n in stack)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String crushRuns(String s, int k) {
                                int n = s.length(), top = 0;
                                char[] tile = new char[n];  //@stack
                                int[] count = new int[n];  //@stack
                                for (char c : s.toCharArray()) {  //@loop
                                    if (top > 0 && tile[top - 1] == c) {  //@extend
                                        if (++count[top - 1] == k) top--;  //@crush
                                    } else {  //@push
                                        tile[top] = c;  //@push
                                        count[top++] = 1;  //@push
                                    }
                                }
                                StringBuilder out = new StringBuilder();  //@ret
                                for (int i = 0; i < top; i++) for (int j = 0; j < count[i]; j++) out.append(tile[i]);  //@ret
                                return out.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string crushRuns(string& s, int k) {
                                vector<pair<char, int>> stack;  //@stack
                                for (char c : s) {  //@loop
                                    if (!stack.empty() && stack.back().first == c) {  //@extend
                                        if (++stack.back().second == k) stack.pop_back();  //@crush
                                    } else {  //@push
                                        stack.push_back({c, 1});  //@push
                                    }
                                }
                                string out;  //@ret
                                for (auto& [c, cnt] : stack) out.append(cnt, c);  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* crushRuns(char* s, int k) {
                            int n = strlen(s), top = 0;
                            char* tile = malloc(n + 1);  //@stack
                            int* count = malloc((n + 1) * sizeof(int));  //@stack
                            for (int i = 0; i < n; i++) {  //@loop
                                if (top > 0 && tile[top - 1] == s[i]) {  //@extend
                                    if (++count[top - 1] == k) top--;  //@crush
                                } else {  //@push
                                    tile[top] = s[i];  //@push
                                    count[top++] = 1;  //@push
                                }
                            }
                            char* out = malloc(n + 1);  //@ret
                            int w = 0;  //@ret
                            for (int i = 0; i < top; i++) for (int j = 0; j < count[i]; j++) out[w++] = tile[i];  //@ret
                            out[w] = '\\0';  //@ret
                            free(tile);  //@ret
                            free(count);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("stack", "Runs still standing, left to right, each with its length.", {"java": "Two parallel arrays act as the stack of runs.", "c": "Two parallel arrays act as the stack of runs."}), ("loop", "One pass over the tiles."), ("extend", "Same tile as the top run: it grows."), ("crush", "A run reaching k disappears; the run beneath becomes the top and can be extended by the next tiles."), ("push", "A different tile starts a new run."), ("ret", "Write the surviving runs out in order.")],
                complexity=["**Time O(n):** each tile is pushed or counted once, and popped at most once. **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - "Remove adjacent groups, then let neighbours meet" → stack, so the new neighbour is always the top.
            - Store **(value, count)** on the stack to check run lengths in O(1).
            """
        ],
    )


@problem
def expand_the_pattern():
    pat = "2[ab3[c]]d"

    def expand(p):
        stack, cur, num = [], [], 0
        for c in p:
            if c.isdigit():
                num = num * 10 + int(c)
            elif c == "[":
                stack.append((cur, num))
                cur, num = [], 0
            elif c == "]":
                prev, k = stack.pop()
                prev.append("".join(cur) * k)
                cur = prev
            else:
                cur.append(c)
        return "".join(cur)

    want = expand(pat)

    w1 = Steps("Repeatedly find an innermost group k[letters] (no brackets inside) and replace it by its expansion.")
    import re
    t = pat
    w1.step(f"Start: {t}", Vars(text=t))
    while "[" in t:
        m = re.search(r"(\d+)\[([a-z]*)\]", t)
        t = t[:m.start()] + m.group(2) * int(m.group(1)) + t[m.end():]
        w1.step(f"Innermost group '{m.group(0)}' → '{m.group(2) * int(m.group(1))}': {t}", Vars(text=t))
    w1.steps[-1]["result"] = t

    w2 = Steps("Explicit stack: '[' saves (text so far, repeat count) and starts fresh; ']' repeats the group and appends it to the saved text.")
    stack, cur, num = [], "", 0
    for c in pat:
        if c.isdigit():
            num = num * 10 + int(c)
            note = f"digit: count = {num}."
        elif c == "[":
            stack.append((cur, num))
            note = f"'[': save ('{cur}', {num}); start an empty group."
            cur, num = "", 0
        elif c == "]":
            prev, k = stack.pop()
            note = f"']': group '{cur}' × {k} = '{cur * k}', appended to '{prev}'."
            cur = prev + cur * k
        else:
            cur += c
            note = f"letter '{c}': current = '{cur}'."
        w2.step(note, Row([f"'{p}'×{k}" for p, k in stack], label="saved (text before group × count)"), Vars(current=cur))
    w2.steps[-1]["result"] = cur

    sol(
        "expand-the-pattern",
        summary="""
            Nested `k[...]` groups are a stack problem: on `[`, save the text built so far and the repeat count, then build
            the group's contents fresh; on `]`, repeat those contents and append them to the saved text. One pass over the
            pattern, O(pattern + output).
        """,
        question=[
            """
            Expand every `k[...]` (repeat the inside k times), including nested groups.

            - **Counts can have several digits:** `12[a]`.
            - **Groups nest:** `3[a2[c]]` → `accaccacc`.
            - **Letters can appear outside groups:** `2[abc]3[cd]ef`.
            - **Output ≤ 10⁵ characters**, though the pattern is only up to 3000.
            """
        ],
        think=[
            f"""
            Take `{pat}`. The innermost group `3[c]` becomes `ccc`, so the outer group is `2[abccc]` → `abcccabccc`, then
            `d`: `{want}`.
            """,
            fig(Row(list(pat), slots=True), caption="Groups expand from the inside out."),
            """
            Inside-out evaluation suggests recursion (evaluate the inside, then repeat it) or, equivalently, an explicit
            stack: when a group opens, park what you've built so far; when it closes, combine. The stack remembers exactly
            the outer contexts that are waiting for the inner group to finish.
            """,
        ],
        approaches=[
            approach(
                "Expand the innermost group, repeat",
                "brute",
                "O(groups × output)",
                "O(output)",
                idea=["Find a group with no brackets inside (`k[letters]`), replace it by its expansion, and repeat until no brackets remain."],
                walk=w1,
                build=["While the text contains `[`: locate an innermost `k[letters]`.", "Replace it with `letters × k`.", "Return the text."],
                code={
                    "python": """
                        import re

                        class Solution:
                            def expand(self, pattern: str) -> str:
                                inner = re.compile(r"(\\d+)\\[([a-z]*)\\]")  #@find
                                while "[" in pattern:  #@loop
                                    m = inner.search(pattern)  #@find
                                    pattern = pattern[:m.start()] + m.group(2) * int(m.group(1)) + pattern[m.end():]  #@replace
                                return pattern  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String expand(String pattern) {
                                java.util.regex.Pattern inner = java.util.regex.Pattern.compile("(\\\\d+)\\\\[([a-z]*)\\\\]");  //@find
                                while (pattern.indexOf('[') >= 0) {  //@loop
                                    java.util.regex.Matcher m = inner.matcher(pattern);  //@find
                                    m.find();  //@find
                                    String body = m.group(2).repeat(Integer.parseInt(m.group(1)));  //@replace
                                    pattern = pattern.substring(0, m.start()) + body + pattern.substring(m.end());  //@replace
                                }
                                return pattern;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string expand(string& pattern) {
                                string t = pattern;  //@loop
                                while (t.find('[') != string::npos) {  //@loop
                                    size_t close = t.find(']');  //@find
                                    size_t open = t.rfind('[', close);  //@find
                                    size_t start = open;  //@find
                                    while (start > 0 && isdigit(t[start - 1])) start--;  //@find
                                    int k = stoi(t.substr(start, open - start));  //@find
                                    string body = t.substr(open + 1, close - open - 1), rep;  //@replace
                                    for (int i = 0; i < k; i++) rep += body;  //@replace
                                    t = t.substr(0, start) + rep + t.substr(close + 1);  //@replace
                                }
                                return t;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* expand(char* pattern) {
                            int cap = strlen(pattern) + 1;
                            char* t = malloc(cap);  //@loop
                            strcpy(t, pattern);  //@loop
                            char* close;  //@loop
                            while ((close = strchr(t, ']')) != NULL) {  //@loop
                                char* open = close;  //@find
                                while (*open != '[') open--;  //@find
                                char* start = open;  //@find
                                while (start > t && start[-1] >= '0' && start[-1] <= '9') start--;  //@find
                                int k = atoi(start);  //@find
                                int bodyLen = close - open - 1, before = start - t, after = strlen(close + 1);  //@replace
                                int need = before + k * bodyLen + after + 1;  //@replace
                                char* u = malloc(need);  //@replace
                                memcpy(u, t, before);  //@replace
                                for (int i = 0; i < k; i++) memcpy(u + before + i * bodyLen, open + 1, bodyLen);  //@replace
                                memcpy(u + before + k * bodyLen, close + 1, after + 1);  //@replace
                                free(t);  //@replace
                                t = u;  //@replace
                            }
                            return t;  //@ret
                        }
                    """,
                },
                lines=[("loop", "Keep going while any group remains."), ("find", "An innermost group: the first `]` closes the nearest `[` before it, and the digits right before that `[` are the count.", {"python": "A regular expression for `digits[letters]` only matches groups with no brackets inside.", "java": "A regular expression for `digits[letters]` only matches groups with no brackets inside."}), ("replace", "Splice in the repeated body, rebuilding the whole string."), ("ret", "No brackets left.")],
                complexity=["**Time O(groups × output):** every replacement copies the whole (growing) string. **Space O(output).**"],
                limits=["Each replacement rebuilds the entire text. Processing the pattern once, left to right, with saved contexts builds each piece only as many times as it's actually repeated."],
                slow=True,
            ),
            approach(
                "Recursive descent",
                "better",
                "O(pattern + output)",
                "O(output + depth)",
                idea=["`parse()` reads from a shared position until `]` or the end: letters are appended; a number is followed by `[`, so recursively parse the group, then append its result k times. The recursion depth equals the nesting depth."],
                walk=w2,
                build=["Shared index `i`.", "`parse()`: loop until `]`/end; letters → append; digits → read k, skip `[`, `inner = parse()`, skip `]`, append inner k times.", "Return `parse()` on the whole pattern."],
                code={
                    "python": """
                        class Solution:
                            def expand(self, pattern: str) -> str:
                                i = 0  #@pos
                                def parse():  #@parse
                                    nonlocal i  #@parse
                                    out = []  #@parse
                                    while i < len(pattern) and pattern[i] != "]":  #@parse
                                        c = pattern[i]  #@parse
                                        if c.isdigit():  #@group
                                            k = 0  #@group
                                            while pattern[i].isdigit():  #@group
                                                k = k * 10 + int(pattern[i])  #@group
                                                i += 1  #@group
                                            i += 1  #@group
                                            inner = parse()  #@group
                                            i += 1  #@group
                                            out.append(inner * k)  #@group
                                        else:  #@letter
                                            out.append(c)  #@letter
                                            i += 1  #@letter
                                    return "".join(out)  #@parse
                                return parse()  #@ret
                    """,
                    "java": """
                        class Solution {
                            private String p;
                            private int i;

                            public String expand(String pattern) {
                                p = pattern;  //@pos
                                i = 0;  //@pos
                                return parse();  //@ret
                            }

                            private String parse() {  //@parse
                                StringBuilder out = new StringBuilder();  //@parse
                                while (i < p.length() && p.charAt(i) != ']') {  //@parse
                                    char c = p.charAt(i);  //@parse
                                    if (Character.isDigit(c)) {  //@group
                                        int k = 0;  //@group
                                        while (Character.isDigit(p.charAt(i))) k = k * 10 + (p.charAt(i++) - '0');  //@group
                                        i++;  //@group
                                        String inner = parse();  //@group
                                        i++;  //@group
                                        out.append(inner.repeat(k));  //@group
                                    } else {  //@letter
                                        out.append(c);  //@letter
                                        i++;  //@letter
                                    }
                                }
                                return out.toString();  //@parse
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            string p;
                            size_t i = 0;

                            string parse() {  //@parse
                                string out;  //@parse
                                while (i < p.size() && p[i] != ']') {  //@parse
                                    if (isdigit(p[i])) {  //@group
                                        int k = 0;  //@group
                                        while (isdigit(p[i])) k = k * 10 + (p[i++] - '0');  //@group
                                        i++;  //@group
                                        string inner = parse();  //@group
                                        i++;  //@group
                                        for (int r = 0; r < k; r++) out += inner;  //@group
                                    } else {  //@letter
                                        out += p[i++];  //@letter
                                    }
                                }
                                return out;  //@parse
                            }

                        public:
                            string expand(string& pattern) {
                                p = pattern;  //@pos
                                i = 0;  //@pos
                                return parse();  //@ret
                            }
                        };
                    """,
                    "c": """
                        typedef struct { char* s; int len, cap; } Buf;  //@pos

                        static void put(Buf* b, const char* src, int n) {  //@pos
                            if (b->len + n + 1 > b->cap) {  //@pos
                                while (b->len + n + 1 > b->cap) b->cap *= 2;  //@pos
                                b->s = realloc(b->s, b->cap);  //@pos
                            }  //@pos
                            memcpy(b->s + b->len, src, n);  //@pos
                            b->len += n;  //@pos
                        }  //@pos

                        static Buf parse(const char* p, int* i) {  //@parse
                            Buf out = {malloc(16), 0, 16};  //@parse
                            while (p[*i] && p[*i] != ']') {  //@parse
                                if (p[*i] >= '0' && p[*i] <= '9') {  //@group
                                    int k = 0;  //@group
                                    while (p[*i] >= '0' && p[*i] <= '9') k = k * 10 + (p[(*i)++] - '0');  //@group
                                    (*i)++;  //@group
                                    Buf inner = parse(p, i);  //@group
                                    (*i)++;  //@group
                                    for (int r = 0; r < k; r++) put(&out, inner.s, inner.len);  //@group
                                    free(inner.s);  //@group
                                } else {  //@letter
                                    put(&out, p + *i, 1);  //@letter
                                    (*i)++;  //@letter
                                }
                            }
                            out.s[out.len] = '\\0';  //@parse
                            return out;  //@parse
                        }

                        char* expand(char* pattern) {
                            int i = 0;
                            return parse(pattern, &i).s;  //@ret
                        }
                    """,
                },
                lines=[("pos", "A read position shared by all recursive calls.", {"c": "A growable buffer (doubling capacity) holds the text built at each level; `put` appends to it."}), ("parse", "Parse a sequence of letters and groups until the `]` that closes the current group (or the end)."), ("group", "Read the count, skip `[`, recursively expand the inside, skip `]`, append the inside k times."), ("letter", "A plain letter is copied."), ("ret", "Expand the whole pattern.")],
                complexity=["**Time O(pattern + output)** for building and copying pieces. **Space O(output)** plus a call stack as deep as the nesting (up to ~1500 levels)."],
                limits=["Deep nesting means deep recursion, which can overflow the call stack in some environments. An explicit stack holds the same information in ordinary memory."],
            ),
            approach(
                "Explicit stack",
                "best",
                "O(pattern + output)",
                "O(output)",
                idea=["Keep `cur` (text of the current group) and `num` (count being read). On `[`: push `(cur, num)`, start empty. On `]`: pop `(prev, k)`, set `cur = prev + cur × k`. Letters append to `cur`."],
                walk=w2,
                build=["`stack = []`, `cur = \"\"`, `num = 0`.", "Digits build num; `[` pushes and resets; `]` pops and combines; letters append.", "Return `cur`."],
                code={
                    "python": """
                        class Solution:
                            def expand(self, pattern: str) -> str:
                                stack, cur, num = [], [], 0  #@state
                                for c in pattern:  #@loop
                                    if c.isdigit():  #@digit
                                        num = num * 10 + int(c)  #@digit
                                    elif c == "[":  #@open
                                        stack.append((cur, num))  #@open
                                        cur, num = [], 0  #@open
                                    elif c == "]":  #@close
                                        prev, k = stack.pop()  #@close
                                        prev.append("".join(cur) * k)  #@close
                                        cur = prev  #@close
                                    else:  #@letter
                                        cur.append(c)  #@letter
                                return "".join(cur)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String expand(String pattern) {
                                Deque<StringBuilder> texts = new ArrayDeque<>();  //@state
                                Deque<Integer> counts = new ArrayDeque<>();  //@state
                                StringBuilder cur = new StringBuilder();  //@state
                                int num = 0;  //@state
                                for (char c : pattern.toCharArray()) {  //@loop
                                    if (Character.isDigit(c)) num = num * 10 + (c - '0');  //@digit
                                    else if (c == '[') {  //@open
                                        texts.push(cur);  //@open
                                        counts.push(num);  //@open
                                        cur = new StringBuilder();  //@open
                                        num = 0;  //@open
                                    } else if (c == ']') {  //@close
                                        StringBuilder prev = texts.pop();  //@close
                                        prev.append(cur.toString().repeat(counts.pop()));  //@close
                                        cur = prev;  //@close
                                    } else cur.append(c);  //@letter
                                }
                                return cur.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string expand(string& pattern) {
                                vector<pair<string, int>> stack;  //@state
                                string cur;  //@state
                                int num = 0;  //@state
                                for (char c : pattern) {  //@loop
                                    if (isdigit(c)) num = num * 10 + (c - '0');  //@digit
                                    else if (c == '[') {  //@open
                                        stack.push_back({cur, num});  //@open
                                        cur.clear();  //@open
                                        num = 0;  //@open
                                    } else if (c == ']') {  //@close
                                        auto [prev, k] = stack.back();  //@close
                                        stack.pop_back();  //@close
                                        for (int r = 0; r < k; r++) prev += cur;  //@close
                                        cur = prev;  //@close
                                    } else cur += c;  //@letter
                                }
                                return cur;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* expand(char* pattern) {
                            int cap = 1 << 17;  //@state
                            char* out = malloc(cap);  //@state
                            int len = 0, top = 0, num = 0;  //@state
                            int* startAt = malloc(strlen(pattern) * sizeof(int) + sizeof(int));  //@state
                            int* times = malloc(strlen(pattern) * sizeof(int) + sizeof(int));  //@state
                            for (char* p = pattern; *p; p++) {  //@loop
                                if (*p >= '0' && *p <= '9') num = num * 10 + (*p - '0');  //@digit
                                else if (*p == '[') {  //@open
                                    startAt[top] = len;  //@open
                                    times[top++] = num;  //@open
                                    num = 0;  //@open
                                } else if (*p == ']') {  //@close
                                    int start = startAt[--top], body = len - start;  //@close
                                    for (int r = 1; r < times[top]; r++) {  //@close
                                        memcpy(out + len, out + start, body);  //@close
                                        len += body;  //@close
                                    }
                                } else out[len++] = *p;  //@letter
                            }
                            out[len] = '\\0';  //@ret
                            free(startAt);  //@ret
                            free(times);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("state", "Saved outer contexts, the current group's text, and the count being read.", {"c": "One output buffer (2¹⁷ bytes covers the 10⁵-character limit). The stack stores where each open group's text starts in that buffer, and its repeat count."}),
                    ("loop", "One pass over the pattern."),
                    ("digit", "Counts can have several digits."),
                    ("open", "A group starts: park the text built so far and the count, and build the group from scratch.", {"c": "Just remember where the group begins in the buffer; its text is written in place."}),
                    ("close", "The group ends: repeat its text k times and continue the parked outer text.", {"c": "The group's text is already in the buffer once; copy it k − 1 more times right after itself."}),
                    ("letter", "Letters extend the current group."),
                    ("ret", "The fully expanded text."),
                ],
                complexity=["**Time O(pattern + output).** **Space O(output)** for the text, plus a stack as deep as the nesting."],
            ),
        ],
        takeaways=[
            """
            - Nested repetition (`k[...]`) → **stack of (outer text, count)**, or recursion.
            - An explicit stack avoids call-stack overflow on deep nesting.
            - Read multi-digit numbers by accumulating `num = num × 10 + digit`.
            """
        ],
    )
