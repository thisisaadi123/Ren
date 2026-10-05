"""Lesson: Read/write pointers (Two Pointers, pattern 2)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

SQUEEZE = {
    "python": """
        def squeeze_spaces(text):
            chars = list(text)                              #@chars
            write = 0                                       #@write
            for read in range(len(chars)):                  #@read
                ch = chars[read]                            #@read
                if ch == " " and (write == 0 or chars[write - 1] == " "):  #@skip
                    continue                                #@skip
                chars[write] = ch                           #@keep
                write += 1                                  #@keep
            if write > 0 and chars[write - 1] == " ":       #@trail
                write -= 1                                  #@trail
            return "".join(chars[:write])                   #@ret
    """,
    "java": """
        static String squeezeSpaces(String text) {
            char[] chars = text.toCharArray();              //@chars
            int write = 0;                                  //@write
            for (int read = 0; read < chars.length; read++) {   //@read
                char ch = chars[read];                      //@read
                if (ch == ' ' && (write == 0 || chars[write - 1] == ' '))  //@skip
                    continue;                               //@skip
                chars[write++] = ch;                        //@keep
            }
            if (write > 0 && chars[write - 1] == ' ') write--;  //@trail
            return new String(chars, 0, write);             //@ret
        }
    """,
    "cpp": """
        string squeezeSpaces(string chars) {
            int write = 0;                                  //@write
            for (int read = 0; read < (int)chars.size(); read++) {  //@read
                char ch = chars[read];                      //@read
                if (ch == ' ' && (write == 0 || chars[write - 1] == ' '))  //@skip
                    continue;                               //@skip
                chars[write++] = ch;                        //@keep
            }
            if (write > 0 && chars[write - 1] == ' ') write--;  //@trail
            chars.resize(write);                            //@ret
            return chars;                                   //@ret
        }
    """,
    "c": """
        void squeezeSpaces(char* chars) {
            int write = 0;                                  //@write
            for (int read = 0; chars[read] != '\\0'; read++) {  //@read
                char ch = chars[read];                      //@read
                if (ch == ' ' && (write == 0 || chars[write - 1] == ' '))  //@skip
                    continue;                               //@skip
                chars[write++] = ch;                        //@keep
            }
            if (write > 0 && chars[write - 1] == ' ') write--;  //@trail
            chars[write] = '\\0';                           //@ret
        }
    """,
}
SQUEEZE_RUN = {
    "python": """
        for t in ["  the   sky  is blue  ", "hello", "   ", "a  b"]:
            print("[" + squeeze_spaces(t) + "]")
    """,
    "java": """
        public static void main(String[] args) {
            for (String t : new String[] {"  the   sky  is blue  ", "hello", "   ", "a  b"})
                System.out.println("[" + squeezeSpaces(t) + "]");
        }
    """,
    "cpp": """
        int main() {
            for (string t : {"  the   sky  is blue  ", "hello", "   ", "a  b"})
                cout << "[" << squeezeSpaces(t) << "]\\n";
        }
    """,
    "c": """
        int main(void) {
            char a[] = "  the   sky  is blue  ", b[] = "hello", c[] = "   ", d[] = "a  b";
            char* ts[] = {a, b, c, d};
            for (int i = 0; i < 4; i++) {
                squeezeSpaces(ts[i]);
                printf("[%s]\\n", ts[i]);
            }
            return 0;
        }
    """,
}

RECORDS = {
    "python": """
        def keep_records(nums):
            write = 0                                       #@write
            for read in range(len(nums)):                   #@read
                if write == 0 or nums[read] > nums[write - 1]:  #@test
                    nums[write] = nums[read]                #@keep
                    write += 1                              #@keep
            return nums[:write]                             #@ret
    """,
    "java": """
        static int[] keepRecords(int[] nums) {
            int write = 0;                                  //@write
            for (int read = 0; read < nums.length; read++) {    //@read
                if (write == 0 || nums[read] > nums[write - 1])     //@test
                    nums[write++] = nums[read];             //@keep
            }
            return Arrays.copyOf(nums, write);              //@ret
        }
    """,
    "cpp": """
        vector<int> keepRecords(vector<int> nums) {
            int write = 0;                                  //@write
            for (int read = 0; read < (int)nums.size(); read++) {   //@read
                if (write == 0 || nums[read] > nums[write - 1])     //@test
                    nums[write++] = nums[read];             //@keep
            }
            nums.resize(write);                             //@ret
            return nums;                                    //@ret
        }
    """,
    "c": """
        int keepRecords(int* nums, int n) {
            int write = 0;                                  //@write
            for (int read = 0; read < n; read++) {          //@read
                if (write == 0 || nums[read] > nums[write - 1])     //@test
                    nums[write++] = nums[read];             //@keep
            }
            return write;                                   //@ret
        }
    """,
}
RECORDS_RUN = {
    "python": """
        print(*keep_records([3, 1, 4, 1, 5, 9, 2, 6]))
        print(*keep_records([5, 5, 5]))
        print(*keep_records([9, 8, 7]))
    """,
    "java": """
        static void show(int[] a) {
            StringBuilder sb = new StringBuilder();
            for (int x : a) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
        }

        public static void main(String[] args) {
            show(keepRecords(new int[] {3, 1, 4, 1, 5, 9, 2, 6}));
            show(keepRecords(new int[] {5, 5, 5}));
            show(keepRecords(new int[] {9, 8, 7}));
        }
    """,
    "cpp": """
        void show(const vector<int>& a) {
            for (size_t i = 0; i < a.size(); i++) cout << (i ? " " : "") << a[i];
            cout << "\\n";
        }

        int main() {
            show(keepRecords({3, 1, 4, 1, 5, 9, 2, 6}));
            show(keepRecords({5, 5, 5}));
            show(keepRecords({9, 8, 7}));
        }
    """,
    "c": """
        static void show(const int* a, int n) {
            for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
        }

        int main(void) {
            int a[] = {3, 1, 4, 1, 5, 9, 2, 6}, b[] = {5, 5, 5}, c[] = {9, 8, 7};
            show(a, keepRecords(a, 8));
            show(b, keepRecords(b, 3));
            show(c, keepRecords(c, 3));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

squeeze_spaces = py(SQUEEZE["python"], "squeeze_spaces")
keep_records = py(RECORDS["python"], "keep_records")
for t in ["  the   sky  is blue  ", "hello", "   ", "a  b", "", " x ", "a b  c   d"]:
    assert squeeze_spaces(t) == " ".join(t.split()), t

# The basic shape: keep the readings that pass a test.
FD = [3, -1, 4, -1, -5, 9, 2]
fw = Steps(f"Keeping the readings in `{FD}` that aren't negative, in place, in their original order.")
arr, write = list(FD), 0
fw.step("`read` will visit every slot once. `write` is where the next kept value goes. Nothing is kept yet.",
        Row(list(arr), ptr={"read": 0, "write": 0}, slots=True, label="readings"), M({"kept": 0}))
for read in range(len(arr)):
    x = arr[read]
    if x >= 0:
        same = read == write
        arr[write] = x
        write += 1
        if same:
            msg = f"`read` = {read}: {x} passes. Nothing has been dropped yet, so it's already in the right slot. Both pointers move on."
        else:
            msg = f"`read` = {read}: {x} passes. Copy it down to slot {write - 1}; `write` moves on."
        st = {k: "found" for k in range(write)}
    else:
        msg = f"`read` = {read}: {x} is negative. Skip it. Only `read` moves, so the gap between the pointers grows by one."
        st = {**{k: "found" for k in range(write)}, read: "dim"}
    fw.step(msg, Row(list(arr), st=st, ptr={"read": read, "write": write if write < len(arr) else None}, slots=True, label="readings"), M({"kept": write}))
FKEPT = arr[:write]
assert FKEPT == [x for x in FD if x >= 0]
fw.steps[-1]["text"] += f" `read` has seen everything. The answer is the first {write} slots: {FKEPT}. What's after them is leftover and can be ignored."
F_LEGEND = {"found": "the kept part, already final", "dim": "read and dropped"}

# Trace of the template.
SD = " a  bc  d "
SHOW = lambda cs: ["␣" if c == " " else c for c in cs]
sw = Steps(f"`squeeze_spaces(\"{SD}\")`, with ␣ for each space. A space is kept only if the last character kept isn't a space.")
cs, write = list(SD), 0
sw.step("Nothing kept yet, so a space here would be a leading space.", Row(SHOW(cs), ptr={"read": 0, "write": 0}, slots=True, label="chars"), M({"last kept": "nothing"}))
for read in range(len(cs)):
    ch = cs[read]
    if ch == " " and (write == 0 or cs[write - 1] == " "):
        why = "nothing has been kept yet, so it would be a leading space" if write == 0 else "the last character kept is already a space"
        msg = f"`read` = {read}: a space, and {why}. Skip it."
        st = {**{k: "found" for k in range(write)}, read: "dim"}
    else:
        cs[write] = ch
        write += 1
        what = "a space after a letter: keep one" if ch == " " else f"a letter, '{ch}': always kept"
        msg = f"`read` = {read}: {what}. It goes to slot {write - 1}."
        st = {k: "found" for k in range(write)}
    last = "nothing" if write == 0 else ("a space" if cs[write - 1] == " " else f"'{cs[write - 1]}'")
    sw.step(msg, Row(SHOW(cs), st=st, ptr={"read": read, "write": write if write < len(cs) else None}, slots=True, label="chars"), M({"last kept": last}))
trail = write > 0 and cs[write - 1] == " "
if trail:
    write -= 1
sw.step(("The last character kept is a space, a trailing one. Drop it by stepping `write` back. " if trail else "")
        + f"The result is the first {write} slots: \"{''.join(cs[:write])}\".",
        Row(SHOW(cs), st={k: "found" for k in range(write)}, ptr={"write": write}, slots=True, label="chars"), M({"last kept": "done"}), result=f'"{"".join(cs[:write])}"')
assert "".join(cs[:write]) == squeeze_spaces(SD)
S_LEGEND = {"found": "kept: the finished part", "dim": "read and dropped"}

# Example: removal when order doesn't matter (swap the last element in).
UD, UV = [3, 1, 3, 4, 3, 2], 3
u_rows, a_, i_, n_ = [], list(UD), 0, len(UD)
while i_ < n_:
    if a_[i_] == UV:
        u_rows.append((str(i_), " ".join(map(str, a_[:n_])), f"{a_[i_]} is a {UV}: overwrite it with the last value in play, {a_[n_ - 1]}, and shrink the end"))
        a_[i_] = a_[n_ - 1]
        n_ -= 1
    else:
        u_rows.append((str(i_), " ".join(map(str, a_[:n_])), f"{a_[i_]} stays; move on"))
        i_ += 1
assert sorted(a_[:n_]) == sorted(x for x in UD if x != UV)
UN = n_
UOUT = a_[:n_]

# Example: an output that grows, so write from the back.
ZD = [1, 0, 2, 3, 0, 4, 5, 0]
ZOUT = []
for x in ZD:
    ZOUT += [x, x] if x == 0 else [x]
ZOUT = ZOUT[:len(ZD)]

N = 10**5

lesson(
    "two-pointers",
    "read-write-pointers",
    """
    Walk one pointer (`read`) over every element, and keep a second one (`write`) at the end of the part you've
    decided to keep. Whatever passes the test gets copied down to `write`. The array is filtered, compacted or cleaned
    up in a single pass, in place, with the order kept.
    """,
    [
        ("idea", "The idea", [
            """
            A librarian is taking damaged books off a shelf. They don't pull everything off and put the good ones back.
            They walk along the shelf, and every time they reach a good book they slide it left to just after the last
            good book they placed. Bad books get left behind. By the end, the good books sit together at
            the start of the shelf in their original order, and whatever is to their right doesn't matter any more.

            The place they're looking at is the **read** pointer. The spot where the next good book goes is the **write**
            pointer. `read` moves every step. `write` only moves when something is kept, so it never gets ahead of
            `read`, and copying to it never destroys a book that hasn't been looked at yet.
            """,
            fig(Row(FD, st={k: "dim" for k, x in enumerate(FD) if x < 0}, slots=True, label="before (negatives dropped)"),
                Row(FKEPT + FD[len(FKEPT):], st={k: "found" for k in range(len(FKEPT))}, slots=True, label="after one pass"),
                caption=f"The first {len(FKEPT)} slots are the answer, in the original order. The rest is leftover."),
            key("""
            `write = 0`, then for every `read`: if `a[read]` should stay, copy it to `a[write]` and move `write` on.
            At the end, `a[0:write]` is the result. One pass, O(1) extra space, order kept.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The question says "in place", "O(1) extra space" or "return the new length", and the job is to remove,
            filter, compact, deduplicate or clean up a sequence while keeping its order.
            """,
            table(
                ["The problem says…", "the test for keeping `a[read]`"],
                ["remove every copy of `v`", "`a[read] != v`"],
                ["move the zeros to the end, keep the rest in order", "`a[read] != 0`, then fill the tail with zeros"],
                ["remove duplicates from a sorted list", "`write == 0` or `a[read] != a[write - 1]`"],
                ["collapse runs of spaces, trim the ends", "not a space, or the last kept isn't a space"],
                ["keep only new highs", "`write == 0` or `a[read] > a[write - 1]`"],
                ["compress runs (\"aaab\" → \"a3b\")", "write once per run, at the run's end"],
            ),
            """
            The second column often looks at `a[write - 1]`, the last thing *kept*, rather than `a[read - 1]`, the last
            thing *read*. Mixing the two up is a common bug.

            Not a fit:

            - Order doesn't matter. Then removing is even simpler: overwrite the unwanted element with the last one
              and shrink the array (see *More examples*). Or partition (*Partition*).
            - The output is longer than the input, like doubling every zero. Writing forwards would overwrite values
              you haven't read. Work out the final length first and fill from the back.
            - Extra memory is fine. Building a new list with a loop or a filter is clearer, and just as fast.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### What the loop keeps true

            > Before each step, `a[0:write]` holds exactly the elements of `a[0:read]` that pass the test, in their
            > original order. And `write ≤ read`.

            It's true at the start (both are 0, both parts empty). In a step, if `a[read]` passes, it's copied to
            `a[write]`, which extends the kept part by exactly the element that `a[0:read]` gained. If it fails, the
            kept part stays the same and so does the answer for `a[0:read + 1]`. Either way `read` moves on, and `write`
            moves at most as far, so `write ≤ read` still holds. When `read` reaches the end, `a[0:write]` is the answer.
            """,
            walk(fw, legend=F_LEGEND),
            """
            ### Why the copy is always safe

            `write ≤ read`, so the slot being written is either the one being read or one that was already read
            earlier. No unread value is ever overwritten. This is why it works in place, and also why it needs the
            output to be no longer than the input.

            ### Looking back at what you kept

            Many tests depend on the output so far: "skip a value if it equals the last one kept", "skip a space if the
            last character kept was a space". The last thing kept is `a[write - 1]`, and it's final, because nothing
            before `write` changes again. The last thing *read*, `a[read - 1]`, may have been dropped, so comparing with
            it asks the wrong question. Keeping record highs from `[3, 1, 2]` shows the difference: compared with the
            last value read (1), the 2 looks like a new high, but compared with the last value kept (3), it isn't.

            ### Leftovers

            After the loop, everything from `write` onwards is junk: old values, some of them duplicates of kept
            ones. Problems handle it in different ways. "Return the new length" means you leave it. "Move the zeros to
            the end" means you fill it with zeros. A language with resizable arrays can cut it off (`resize`, slicing).
            """,
        ]),
        ("template", "The template", [
            """
            Clean up the spaces in a piece of text: drop leading and trailing spaces, and squeeze every run of spaces
            between words down to one. Work in place on the characters.
            """,
            code(
                "Squeeze the spaces in place",
                SQUEEZE,
                [
                    ("chars", "Strings can't be changed in Python and Java, so work on a list or array of characters."),
                    ("write", "Where the next kept character goes."),
                    ("read", "Look at every character once, left to right.",
                     {"c": "A C string ends at `'\\0'`, so the loop stops there instead of at a length."}),
                    ("skip", "A space is dropped if nothing has been kept yet (it would be a leading space) or if the last "
                             "character *kept* is already a space. Note `chars[write - 1]`, not `chars[read - 1]`."),
                    ("keep", "Everything else is copied down. `write` never passes `read`, so nothing unread is lost.",
                     {"java": "`write++` uses the slot, then moves it on.",
                      "cpp": "`write++` uses the slot, then moves it on.",
                      "c": "`write++` uses the slot, then moves it on."}),
                    ("trail", "Runs were squeezed to one space, so at most one trailing space can be left. Drop it."),
                    ("ret", "The first `write` characters are the result.",
                     {"cpp": "`resize` cuts off the leftovers.",
                      "c": "Writing `'\\0'` at `write` ends the string there."}),
                ],
                SQUEEZE_RUN,
                'squeeze_spaces("  the   sky  is blue  "); ("hello"); ("   "); ("a  b")',
            ),
            """
            The brackets in the output show where each result starts and ends. Three spaces on their own clean up to an
            empty string.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "A short one, character by character. The kept part is final the moment it's written:",
            walk(sw, legend=S_LEGEND),
            """
            On paper, write the input once, and underneath it write the output as it grows. Draw `read` on the top line
            and `write` on the bottom one. You'll see the bottom line never gets longer than the top line so far.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### When order doesn't matter

            Remove every {UV} from `{UD}`, and the order of what's left doesn't matter. Instead of shifting the kept
            values left, overwrite each {UV} with the last value still in play and shrink the end. Don't move `i` after
            an overwrite, because the value that just arrived hasn't been checked.
            """,
            table(["i", "values in play", "what happens"], *u_rows),
            f"""
            {UN} values remain: `{UOUT}`. This does fewer writes when there's little to remove, since it only touches
            the removed slots. It also scrambles the order, which is why the template doesn't do it.

            ### When the output grows

            Double every zero in `{ZD}`, keeping the same length (values pushed off the end are lost): the answer is
            `{ZOUT}`. Copying forwards would overwrite the 2 with the second 0 before reading it. So first count how
            far each value moves, then copy from the right end, with the read pointer on the left of the write
            pointer. Now `read ≤ write` is the guarantee, mirrored, and again nothing unread is lost.

            ### Two lists, one writer

            The write pointer doesn't care where the values come from. Merging two sorted lists into a third uses two
            read pointers and one write pointer. *Merge two sorted sequences* covers that, including merging into the
            spare space at the end of one of the lists.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### A test that looks back

            Keep only the readings that beat every reading before them: the record highs. Every value kept is a new
            high, so the kept part is increasing and its last value, `nums[write - 1]`, is the highest so far. One
            comparison with it decides each value.
            """,
            code(
                "Keep the record highs in place",
                RECORDS,
                [
                    ("write", "Nothing kept yet."),
                    ("read", "Every value, once."),
                    ("test", "The first value is always a record. After that, a value is a record only if it beats the last "
                             "record kept, which is the highest value so far."),
                    ("keep", "Copy it down to `write`."),
                    ("ret", "The records, in the order they were set.",
                     {"java": "`Arrays.copyOf` returns just the first `write` values.",
                      "cpp": "`resize` cuts off the leftovers.",
                      "c": "C returns how many there are; they're at the start of `nums`."}),
                ],
                RECORDS_RUN,
                "keep_records([3, 1, 4, 1, 5, 9, 2, 6]); ([5, 5, 5]); ([9, 8, 7])",
            ),
            """
            Equal values aren't records (`>` rather than `>=`), so `[5, 5, 5]` keeps just one 5.

            ### Writing more than one thing per read

            Run-length style output writes a character and then a count. The write pointer still can't pass the read
            pointer as long as each run of length `k` produces at most `k` characters, which is why "a run of 1 is
            written as just the letter" matters: writing "a1" for a single "a" would grow the output.

            ### Strings in languages without mutable strings

            In Python and Java, convert to a list or `char[]`, run the same loop, and build a string from the first
            `write` characters at the end. That's still one pass; the conversions are O(n) each.
            """,
        ]),
        ("complexity", "What it costs", [
            f"""
            `read` visits each element once and every step does O(1) work, so it's O(n) time. Extra space is O(1):
            two indices. (Python and Java pay O(n) to turn a string into a mutable list and back, because strings can't
            be changed.)

            The naive in-place version, which deletes each unwanted element by shifting everything after it left, is
            O(n²) in the worst case: for `n = {N:,}` with half the values removed, that's billions of moves.
            """,
            table(
                ["Approach", "Time", "Extra space", "Keeps order"],
                ["Delete and shift, one at a time", "O(n²)", "O(1)", "yes"],
                ["Build a new list", "O(n)", "O(n)", "yes"],
                ["Read/write pointers", "O(n)", "O(1)", "yes"],
                ["Overwrite with the last element", "O(n)", "O(1)", "no"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `del a[write:]` or `a[:write]` cuts off the leftovers. Calling `list.remove` or `del a[i]` inside a loop is
            the O(n²) shifting version, and modifying a list while a `for x in a` loop runs over it skips elements.
            `" ".join(text.split())` does the space squeeze in one line, with a new string.

            ### Java

            Arrays can't shrink, so return the new length or `Arrays.copyOf(a, write)`. For strings, `toCharArray()`
            and `new String(chars, 0, write)`. With an `ArrayList`, calling `remove(i)` in a loop is the slow shifting
            version.

            ### C++

            `resize(write)` drops the tail. The standard library has this pattern built in: `std::remove_if` does the
            read/write loop and returns an iterator to the new end, which you pass to `erase`. `std::unique` does the
            "differs from the last kept" version.

            ### C

            Return the new length, or for strings write `'\\0'` at `write`. Make sure the string is in writable memory: a
            string literal like `char* s = "a  b"` can't be changed, but `char s[] = "a  b"` can.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Comparing with `a[read - 1]` when the rule is about what was *kept*. Use `a[write - 1]`.
            - Forgetting `write == 0` before reading `a[write - 1]`.
            - Forgetting what to do with the leftovers: cut them, fill them, or just return the length.
            - Moving `write` when nothing was written.
            - Writing forwards when the output can be longer than the input.
            - Deleting from a list while looping over it.
            - In C, trying to modify a string literal.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why can't the write pointer overwrite a value that hasn't been read yet?",
                 "`write` only moves when something is kept, and `read` moves every step, so `write ≤ read`. The slot being written has always been read already."),
                ("In `keep_records`, why compare with `nums[write - 1]` rather than `nums[read - 1]`?",
                 "`nums[write - 1]` is the last record kept, which is the highest value so far. `nums[read - 1]` is just the previous value, which may be lower: in [3, 1, 2], 2 beats 1 but not 3."),
                ("After the loop, what's in `a[write:]`?",
                 "Leftovers: old values that have either been copied further left or dropped. They aren't part of the answer."),
                ("Remove every 0 from [0, 0, 1], keeping order. What are read and write after each step?",
                 "Read 0: skip (write 0). Read 1: skip (write 0). Read 2: keep 1 at slot 0 (write 1). The answer is [1]."),
                ("Why does doubling every zero need to be done from the back?",
                 "The output is longer than the input, so writing forwards would get ahead of reading and overwrite values before they're read. From the back, the write pointer stays ahead (to the right) of the read pointer."),
            ),
        ]),
    ],
)
