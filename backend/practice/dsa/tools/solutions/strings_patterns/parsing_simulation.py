"""Strings: parsing and simulating text formats."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def justify_ref(words, width):
    out, i, n = [], 0, len(words)
    while i < n:
        j, size = i + 1, len(words[i])
        while j < n and size + 1 + len(words[j]) <= width:
            size += 1 + len(words[j])
            j += 1
        line, gaps = words[i:j], j - i - 1
        if j == n or gaps == 0:
            s = " ".join(line)
            out.append(s + " " * (width - len(s)))
        else:
            q, r = divmod(width - (size - gaps), gaps)
            out.append("".join(w + " " * (q + (1 if k < r else 0)) for k, w in enumerate(line[:-1])) + line[-1])
        i = j
    return out


@problem
def justify_the_column():
    words, width = ["Rain", "fell", "on", "the", "old", "tin", "roof", "all", "night."], 14
    want = justify_ref(words, width)

    w = Steps("Fill each line greedily, then share out the spare spaces.")
    i, n = 0, len(words)
    while i < n:
        j, size = i + 1, len(words[i])
        while j < n and size + 1 + len(words[j]) <= width:
            size += 1 + len(words[j])
            j += 1
        gaps = j - i - 1
        letters = size - gaps
        if j == n or gaps == 0:
            why = "last line" if j == n else "a single word"
            note = f"{why}: left-aligned, padded at the end"
        else:
            q, r = divmod(width - letters, gaps)
            note = f"{width - letters} spare spaces over {gaps} gap(s): {q} each, and the first {r} get one more"
        w.step(f"Words {words[i:j]} ({letters} letters) fit. {note[0].upper() + note[1:]}.", Row([c if c != " " else "·" for c in justify_ref(words[i:], width)[0]]))
        i = j
    w.step(f"{len(want)} lines, each exactly {width} wide.", result=[x.replace(" ", "·") for x in want])

    sol(
        "justify-the-column",
        summary="""
            Two independent decisions per line. Which words: take words greedily while letters plus one space between each
            still fit. How many spaces: on a full line, `spare = width − letters` spaces go into `gaps` gaps, `spare / gaps`
            each and one extra for the first `spare % gaps`. The last line and single-word lines are left-aligned. O(total
            output).
        """,
        question=[
            """
            Lay `words` into lines of exactly `width` characters, each line holding as many words as fit with single spaces.
            Then fully justify every line except the last; spread uneven spaces so the left gaps are wider. The last line,
            and any one-word line, is left-aligned and padded with spaces at the end.

            - **Up to 300 words**, `width ≤ 100`.
            - **Every word fits** on a line by itself.
            """
        ],
        think=[
            f"""
            `{words}` at width {width} gives:

            {chr(10).join("- `" + x.replace(" ", "·") + "`" for x in want)}

            (`·` marks a space.) Deciding the words for a line never depends on the spacing, so do it first: the minimum
            length of a line is its letters plus one space per gap. Once the words are fixed, the spacing is arithmetic.
            """,
        ],
        approaches=[
            approach(
                "Greedy lines, then divide the spare spaces",
                "best",
                "O(L)",
                "O(L)",
                idea=["Grow a line from word `i` while `size + 1 + len(next) ≤ width`. If it's the last line or has one word, join with single spaces and pad. Otherwise give each gap `q = spare / gaps` spaces, and the first `r = spare % gaps` gaps one more."],
                walk=w,
                build=["Pick the words for the line.", "Left-align the last and one-word lines.", "Justify the rest with `divmod`."],
                code={
                    "python": """
                        class Solution:
                            def justify(self, words: List[str], width: int) -> List[str]:
                                out, i, n = [], 0, len(words)  #@init
                                while i < n:  #@pick
                                    j, size = i + 1, len(words[i])  #@pick
                                    while j < n and size + 1 + len(words[j]) <= width:  #@pick
                                        size += 1 + len(words[j])  #@pick
                                        j += 1  #@pick
                                    gaps = j - i - 1  #@pick
                                    if j == n or gaps == 0:  #@left
                                        line = " ".join(words[i:j])  #@left
                                        out.append(line + " " * (width - len(line)))  #@left
                                    else:  #@full
                                        q, r = divmod(width - (size - gaps), gaps)  #@full
                                        parts = [words[k] + " " * (q + (1 if k - i < r else 0)) for k in range(i, j - 1)]  #@full
                                        out.append("".join(parts) + words[j - 1])  #@full
                                    i = j  #@next
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public List<String> justify(String[] words, int width) {
                                List<String> out = new ArrayList<>();  //@init
                                int i = 0, n = words.length;  //@init
                                while (i < n) {  //@pick
                                    int j = i + 1, size = words[i].length();  //@pick
                                    while (j < n && size + 1 + words[j].length() <= width) size += 1 + words[j++].length();  //@pick
                                    int gaps = j - i - 1;  //@pick
                                    StringBuilder line = new StringBuilder();  //@pick
                                    if (j == n || gaps == 0) {  //@left
                                        for (int k = i; k < j; k++) line.append(k > i ? " " : "").append(words[k]);  //@left
                                        while (line.length() < width) line.append(' ');  //@left
                                    } else {  //@full
                                        int spare = width - (size - gaps), q = spare / gaps, r = spare % gaps;  //@full
                                        for (int k = i; k < j - 1; k++) line.append(words[k]).append(" ".repeat(q + (k - i < r ? 1 : 0)));  //@full
                                        line.append(words[j - 1]);  //@full
                                    }
                                    out.add(line.toString());  //@next
                                    i = j;  //@next
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<string> justify(vector<string>& words, int width) {
                                vector<string> out;  //@init
                                int i = 0, n = words.size();  //@init
                                while (i < n) {  //@pick
                                    int j = i + 1, size = words[i].size();  //@pick
                                    while (j < n && size + 1 + (int) words[j].size() <= width) size += 1 + words[j++].size();  //@pick
                                    int gaps = j - i - 1;  //@pick
                                    string line;  //@pick
                                    if (j == n || gaps == 0) {  //@left
                                        for (int k = i; k < j; k++) line += (k > i ? " " : "") + words[k];  //@left
                                        line.resize(width, ' ');  //@left
                                    } else {  //@full
                                        int spare = width - (size - gaps), q = spare / gaps, r = spare % gaps;  //@full
                                        for (int k = i; k < j - 1; k++) line += words[k] + string(q + (k - i < r ? 1 : 0), ' ');  //@full
                                        line += words[j - 1];  //@full
                                    }
                                    out.push_back(line);  //@next
                                    i = j;  //@next
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char** justify(char** words, int wordsSize, int width, int* returnSize) {
                            char** out = malloc(wordsSize * sizeof(char*));  //@init
                            int count = 0, i = 0, n = wordsSize;  //@init
                            while (i < n) {  //@pick
                                int j = i + 1, size = strlen(words[i]);  //@pick
                                while (j < n && size + 1 + (int) strlen(words[j]) <= width) size += 1 + strlen(words[j++]);  //@pick
                                int gaps = j - i - 1, pos = 0;  //@pick
                                char* line = malloc(width + 1);  //@pick
                                if (j == n || gaps == 0) {  //@left
                                    for (int k = i; k < j; k++) {  //@left
                                        if (k > i) line[pos++] = ' ';  //@left
                                        int len = strlen(words[k]);  //@left
                                        memcpy(line + pos, words[k], len);  //@left
                                        pos += len;  //@left
                                    }
                                    while (pos < width) line[pos++] = ' ';  //@left
                                } else {  //@full
                                    int spare = width - (size - gaps), q = spare / gaps, r = spare % gaps;  //@full
                                    for (int k = i; k < j; k++) {  //@full
                                        int len = strlen(words[k]);  //@full
                                        memcpy(line + pos, words[k], len);  //@full
                                        pos += len;  //@full
                                        if (k < j - 1) for (int t = q + (k - i < r ? 1 : 0); t > 0; t--) line[pos++] = ' ';  //@full
                                    }
                                }
                                line[pos] = '\\0';  //@next
                                out[count++] = line;  //@next
                                i = j;  //@next
                            }
                            *returnSize = count;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "The output lines and the index of the next unplaced word.", {"c": "At most one line per word."}),
                    ("pick", "Grow the line while one more space and the next word still fit. `size` is letters plus single spaces; `gaps` is the number of spaces between words."),
                    ("left", "Last line or a single word: single spaces, then pad the end to `width`."),
                    ("full", "`size − gaps` is the letter count, so `spare = width − letters` spaces go into `gaps` gaps: `q` each, and the first `r` gaps (the leftmost) get one more. No spaces after the final word."),
                    ("next", "Store the line; the next one starts at word `j`."),
                    ("ret", "All lines, top to bottom."),
                ],
                complexity=["**Time O(L)**, where L is the total output length (lines × width): every character is written once, and each word is measured a constant number of times. **Space O(L)** for the output."],
            ),
        ],
        takeaways=[
            """
            - **Separate layout from formatting:** greedily choose the words, then compute the spacing.
            - **Spreading `s` items over `g` slots, left-heavy:** `s // g` each, plus one for the first `s % g`.
            - Special cases (last line, single word) are where most bugs hide.
            """
        ],
    )


def meter_ref(text):
    n, i = len(text), 0
    while i < n and text[i] == " ":
        i += 1
    sign = 1
    if i < n and text[i] in "+-":
        sign = -1 if text[i] == "-" else 1
        i += 1
    cap = 1 << 31
    val, seen = 0, False
    while i < n:
        c = text[i]
        if "0" <= c <= "9":
            val = min(cap, val * 10 + ord(c) - 48)
            seen = True
        elif not (c == "_" and seen and i + 1 < n and "0" <= text[i + 1] <= "9"):
            break
        i += 1
    return max(-cap, min(cap - 1, val * sign))


@problem
def read_the_meter():
    text = "  -12_405_kWh"
    want = meter_ref(text)
    big = "99_999_999_999"
    assert meter_ref(big) == 2**31 - 1

    w = Steps("One pass: spaces, an optional sign, then digits (with single underscores between digits).")
    w.step("Skip the two leading spaces.", Row(list(text), st={0: "dim", 1: "dim"}))
    w.step("Read the sign '-'.", Row(list(text), st={2: "active"}), Vars(sign=-1))
    val, i = 0, 3
    while i < len(text):
        c = text[i]
        if c.isdigit():
            val = val * 10 + int(c)
            w.step(f"Digit {c}: value = {val}.", Row(list(text), st={i: "found"}), Vars(sign=-1, value=val))
        elif c == "_" and text[i + 1].isdigit():
            w.step("'_' sits between two digits: skip it.", Row(list(text), st={i: "dim"}), Vars(sign=-1, value=val))
        else:
            w.step(f"'{c}' stops the reading.", Row(list(text), st={i: "mark"}), Vars(sign=-1, value=val))
            break
        i += 1
    w.step(f"Apply the sign: {want}. It's inside the 32-bit range.", result=want)

    sol(
        "read-the-meter",
        summary="""
            Scan once as a tiny state machine: skip spaces, take at most one sign, then read digits. An underscore is
            skipped only if a digit came before it and a digit comes right after; anything else stops the reading. Cap
            the running value at 2³¹ as you go so it never overflows, then apply the sign and clamp.
        """,
        question=[
            """
            Read a signed 32-bit integer from the front of `text`: leading spaces, an optional `+`/`-`, then digits where a
            single `_` between two digits is ignored. Stop at anything else. No digits means 0; out-of-range values clamp
            to `−2³¹` or `2³¹ − 1`.

            - **Text up to 200 characters**, so the digits can describe numbers far beyond 64 bits.
            """
        ],
        think=[
            f"""
            `"{text}"` → **{want}**, and `"{big}"` → {2**31 - 1} (clamped).

            The rules are a sequence of phases, each consuming characters until something tells it to stop. The only
            subtle part is the underscore: it needs a digit on **both** sides, so `"5_"` and `"_5"` and `"5__6"` all stop at
            the underscore.

            Overflow: as soon as the magnitude passes 2³¹, the final answer is already decided (it clamps), so keep the
            value capped at 2³¹ and it fits comfortably in 64 bits.
            """,
            fig(Row(list(text), label="text")),
        ],
        approaches=[
            approach(
                "Single scan with a capped value",
                "best",
                "O(n)",
                "O(1)",
                idea=["Index `i` walks the text through three phases. Keep `value = min(2³¹, value · 10 + digit)`. Finally return `clamp(sign · value)`."],
                walk=w,
                build=["Skip spaces.", "Optional sign.", "Digits and valid underscores, capped.", "Apply sign and clamp."],
                code={
                    "python": """
                        class Solution:
                            def readMeter(self, text: str) -> int:
                                n, i = len(text), 0  #@spaces
                                while i < n and text[i] == " ":  #@spaces
                                    i += 1  #@spaces
                                sign = 1  #@sign
                                if i < n and text[i] in "+-":  #@sign
                                    sign = -1 if text[i] == "-" else 1  #@sign
                                    i += 1  #@sign
                                cap, value, seen = 1 << 31, 0, False  #@digits
                                while i < n:  #@digits
                                    c = text[i]  #@digits
                                    if c.isdigit():  #@digits
                                        value = min(cap, value * 10 + int(c))  #@digits
                                        seen = True  #@digits
                                    elif not (c == "_" and seen and i + 1 < n and text[i + 1].isdigit()):  #@under
                                        break  #@under
                                    i += 1  #@digits
                                return max(-cap, min(cap - 1, sign * value))  #@clamp
                    """,
                    "java": """
                        class Solution {
                            public int readMeter(String text) {
                                int n = text.length(), i = 0;  //@spaces
                                while (i < n && text.charAt(i) == ' ') i++;  //@spaces
                                int sign = 1;  //@sign
                                if (i < n && (text.charAt(i) == '+' || text.charAt(i) == '-')) sign = text.charAt(i++) == '-' ? -1 : 1;  //@sign
                                long cap = 1L << 31, value = 0;  //@digits
                                boolean seen = false;  //@digits
                                for (; i < n; i++) {  //@digits
                                    char c = text.charAt(i);  //@digits
                                    if (Character.isDigit(c)) { value = Math.min(cap, value * 10 + (c - '0')); seen = true; }  //@digits
                                    else if (!(c == '_' && seen && i + 1 < n && Character.isDigit(text.charAt(i + 1)))) break;  //@under
                                }
                                return (int) Math.max(-cap, Math.min(cap - 1, sign * value));  //@clamp
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int readMeter(string& text) {
                                int n = text.size(), i = 0;  //@spaces
                                while (i < n && text[i] == ' ') i++;  //@spaces
                                int sign = 1;  //@sign
                                if (i < n && (text[i] == '+' || text[i] == '-')) sign = text[i++] == '-' ? -1 : 1;  //@sign
                                long long cap = 1LL << 31, value = 0;  //@digits
                                bool seen = false;  //@digits
                                for (; i < n; i++) {  //@digits
                                    char c = text[i];  //@digits
                                    if (isdigit((unsigned char) c)) { value = min(cap, value * 10 + (c - '0')); seen = true; }  //@digits
                                    else if (!(c == '_' && seen && i + 1 < n && isdigit((unsigned char) text[i + 1]))) break;  //@under
                                }
                                return (int) max(-cap, min(cap - 1, sign * value));  //@clamp
                            }
                        };
                    """,
                    "c": """
                        #include <ctype.h>

                        int readMeter(char* text) {
                            int n = strlen(text), i = 0;  //@spaces
                            while (i < n && text[i] == ' ') i++;  //@spaces
                            int sign = 1;  //@sign
                            if (i < n && (text[i] == '+' || text[i] == '-')) sign = text[i++] == '-' ? -1 : 1;  //@sign
                            long long cap = 1LL << 31, value = 0;  //@digits
                            bool seen = false;  //@digits
                            for (; i < n; i++) {  //@digits
                                char c = text[i];  //@digits
                                if (isdigit((unsigned char) c)) { value = value * 10 + (c - '0'); if (value > cap) value = cap; seen = true; }  //@digits
                                else if (!(c == '_' && seen && i + 1 < n && isdigit((unsigned char) text[i + 1]))) break;  //@under
                            }
                            long long r = sign * value;  //@clamp
                            return (int) (r < -cap ? -cap : r > cap - 1 ? cap - 1 : r);  //@clamp
                        }
                    """,
                },
                lines=[
                    ("spaces", "Phase 1: leading spaces only (not other whitespace)."),
                    ("sign", "Phase 2: at most one sign character."),
                    ("digits", "Phase 3: accumulate digits. Capping at 2³¹ keeps the value small while still knowing it's out of range."),
                    ("under", "A `_` is allowed only between digits: a digit already read and a digit next. Any other character ends the number."),
                    ("clamp", "Apply the sign and clamp into `[−2³¹, 2³¹ − 1]`. No digits leaves `value = 0`."),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Parsing = phases + a pointer:** each phase consumes characters until its stop condition.
            - **Avoid overflow by capping early** once the result is known to clamp.
            - Separators "between two digits" need a look-behind (a digit seen) and a look-ahead.
            """
        ],
    )


def pack(items):
    return "".join(f"{len(x)}#{x}" for x in items)


@problem
def unpack_the_bundle():
    items = ["a#1", "", "12#"]
    bundle = pack(items)

    w = Steps("Read a length up to the next '#', then take exactly that many characters, whatever they are.")
    i = 0
    while i < len(bundle):
        j = bundle.index("#", i)
        size = int(bundle[i:j])
        w.step(f"Length '{bundle[i:j]}' = {size}; take '{bundle[j + 1:j + 1 + size]}'.", Row(list(bundle), st={**{t: "active" for t in range(i, j + 1)}, **{t: "found" for t in range(j + 1, j + 1 + size)}}))
        i = j + 1 + size
    w.step(f"The pointer reached the end: {items}.", result=items)

    sol(
        "unpack-the-bundle",
        summary="""
            Length-prefixed decoding with one pointer: read digits up to the next `#` to get the length `k`, then the next
            `k` characters are the string, regardless of what they contain. Jump past them and repeat. The first `#` after
            a length is always the length's terminator, because digits come first. O(n).
        """,
        question=[
            """
            Each string was written as `<length>#<string>`, all concatenated. The strings may contain `#` and digits and may
            be empty. Recover the list.

            - **Bundle up to 10⁵ characters.**
            - **Always a correct packing.**
            """
        ],
        think=[
            f"""
            `{items}` packs as `"{bundle}"`.

            Splitting on `#` fails because the strings contain `#`. But the length tells us exactly where each string ends,
            so we never need to look inside a string at all. And at the start of each item, the characters before the first
            `#` are all digits (the length), so the first `#` we meet ends the length.
            """,
            fig(Row(list(bundle), label="bundle")),
        ],
        approaches=[
            approach(
                "Read the length, then jump",
                "best",
                "O(n)",
                "O(n)",
                idea=["At `i`, find the `#` at `j ≥ i`; `k = int(bundle[i:j])`; the string is `bundle[j+1 : j+1+k]`; continue at `j + 1 + k`."],
                walk=w,
                build=["Pointer at the start.", "Parse the length.", "Slice and jump."],
                code={
                    "python": """
                        class Solution:
                            def unpack(self, bundle: str) -> List[str]:
                                out, i, n = [], 0, len(bundle)  #@init
                                while i < n:  #@loop
                                    j, size = i, 0  #@len
                                    while bundle[j] != "#":  #@len
                                        size = size * 10 + int(bundle[j])  #@len
                                        j += 1  #@len
                                    out.append(bundle[j + 1:j + 1 + size])  #@take
                                    i = j + 1 + size  #@take
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public List<String> unpack(String bundle) {
                                List<String> out = new ArrayList<>();  //@init
                                int i = 0, n = bundle.length();  //@init
                                while (i < n) {  //@loop
                                    int j = i, size = 0;  //@len
                                    while (bundle.charAt(j) != '#') size = size * 10 + (bundle.charAt(j++) - '0');  //@len
                                    out.add(bundle.substring(j + 1, j + 1 + size));  //@take
                                    i = j + 1 + size;  //@take
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<string> unpack(string& bundle) {
                                vector<string> out;  //@init
                                int i = 0, n = bundle.size();  //@init
                                while (i < n) {  //@loop
                                    int j = i, size = 0;  //@len
                                    while (bundle[j] != '#') size = size * 10 + (bundle[j++] - '0');  //@len
                                    out.push_back(bundle.substr(j + 1, size));  //@take
                                    i = j + 1 + size;  //@take
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char** unpack(char* bundle, int* returnSize) {
                            int n = strlen(bundle), i = 0, count = 0;  //@init
                            char** out = malloc((n / 2 + 1) * sizeof(char*));  //@init
                            while (i < n) {  //@loop
                                int j = i, size = 0;  //@len
                                while (bundle[j] != '#') size = size * 10 + (bundle[j++] - '0');  //@len
                                char* item = malloc(size + 1);  //@take
                                memcpy(item, bundle + j + 1, size);  //@take
                                item[size] = '\\0';  //@take
                                out[count++] = item;  //@take
                                i = j + 1 + size;  //@take
                            }
                            *returnSize = count;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Output list and the read pointer.", {"c": "Every item takes at least 2 characters (`0#`), so `n / 2 + 1` slots are enough."}),
                    ("loop", "Each iteration decodes one item."),
                    ("len", "Digits up to the first `#` form the length; this `#` can't be part of a string because the string hasn't started yet."),
                    ("take", "The next `size` characters are the item, even if they contain `#` or digits. Jump past them."),
                    ("ret", "Items in order (empty strings included)."),
                ],
                complexity=["**Time O(n):** each character is read once. **Space O(n)** for the output."],
            ),
        ],
        takeaways=[
            """
            - **Length-prefix encoding** handles any content: never search inside the payload.
            - The delimiter is only trusted where the format guarantees it (right after the length digits).
            - The same trick encodes lists of strings for storage or the network.
            """
        ],
    )


def cmp_ref(a, b):
    ra, rb = a.split("."), b.split(".")
    for k in range(max(len(ra), len(rb))):
        x = ra[k].lstrip("0") if k < len(ra) else ""
        y = rb[k].lstrip("0") if k < len(rb) else ""
        if len(x) != len(y):
            return 1 if len(x) > len(y) else -1
        if x != y:
            return 1 if x > y else -1
    return 0


CMP_REV = {
    "java": """
                            private int cmpRev(String x, String y) {  //@rev
                                x = x.replaceFirst("^0+", "");  //@rev
                                y = y.replaceFirst("^0+", "");  //@rev
                                if (x.length() != y.length()) return x.length() > y.length() ? 1 : -1;  //@rev
                                int c = x.compareTo(y);  //@rev
                                return c > 0 ? 1 : c < 0 ? -1 : 0;  //@rev
                            }  //@rev
    """,
}


@problem
def which_release_is_newer():
    a, b = "3.010.0.0", "3.9.000"
    want = cmp_ref(a, b)
    assert want == 1

    w1 = Steps("Split both at the dots, pad the shorter list with 0s, compare revision by revision.")
    ra, rb = a.split("."), b.split(".")
    for k in range(max(len(ra), len(rb))):
        x = ra[k] if k < len(ra) else "0"
        y = rb[k] if k < len(rb) else "0"
        r = cmp_ref(x, y)
        w1.step(f"Revision {k}: '{x}' vs '{y}' → {'equal' if r == 0 else ('a is newer' if r > 0 else 'b is newer')}.", Row(ra, st={k: "active"} if k < len(ra) else {}, label="a"), Row(rb, st={k: "active"} if k < len(rb) else {}, label="b"))
        if r:
            break
    w1.step(f"Answer: {want}.", result=want)

    w2 = Steps("Two pointers cut one revision at a time from each string; strip leading zeros; a longer number is bigger, equal lengths compare digit by digit.")
    w2.step("'3' vs '3': equal.", Row(list(a), st={0: "active"}, label="a"), Row(list(b), st={0: "active"}, label="b"))
    w2.step("'010' → '10' (2 digits) vs '9' (1 digit): a has the longer number, so a is newer.", Row(list(a), st={2: "active", 3: "active", 4: "active"}, label="a"), Row(list(b), st={2: "active"}, label="b"), result=want)

    sol(
        "which-release-is-newer",
        summary="""
            Compare revision by revision, treating missing ones as 0. Revisions can be 50 digits, so never convert them to
            numbers: strip leading zeros, then the longer one is bigger, and equal lengths compare as text. Walking both
            strings with pointers avoids splitting. O(n + m).
        """,
        question=[
            """
            Release numbers are dot-separated revisions such as `2.10.0`, possibly with leading zeros. Missing revisions
            count as 0. Return 1 if `a` is newer, −1 if `b` is, 0 if equal.

            - **Revisions up to 50 digits** (beyond 64-bit integers).
            - **Strings up to 10⁴ characters.**
            """
        ],
        think=[
            f"""
            `"{a}"` vs `"{b}"` → **{want}**: the first revisions tie, then `010` (ten) beats `9`.

            Two pitfalls: comparing text directly says `"9" > "10"`, and converting to integers overflows. After stripping
            leading zeros, a number with more digits is larger; with the same digit count, text comparison is numeric
            comparison. `"0.0"` and `"0"` are the same release, because the missing revisions are 0.
            """,
            fig(Row(a.split("."), label="a"), Row(b.split("."), label="b")),
        ],
        approaches=[
            approach(
                "Split at the dots",
                "better",
                "O(n + m)",
                "O(n + m)",
                idea=["Split both strings into lists of revisions. For `k` up to the longer list, compare `a[k]` and `b[k]` (or `0` if missing) with the strip-then-length-then-text rule."],
                walk=w1,
                build=["Split into revisions.", "Compare as big numbers in text.", "Missing revisions are 0."],
                code={
                    "python": """
                        class Solution:
                            def compareReleases(self, a: str, b: str) -> int:
                                ra, rb = a.split("."), b.split(".")  #@split
                                for k in range(max(len(ra), len(rb))):  #@loop
                                    x = ra[k].lstrip("0") if k < len(ra) else ""  #@pad
                                    y = rb[k].lstrip("0") if k < len(rb) else ""  #@pad
                                    if len(x) != len(y):  #@rev
                                        return 1 if len(x) > len(y) else -1  #@rev
                                    if x != y:  #@rev
                                        return 1 if x > y else -1  #@rev
                                return 0  #@ret
                    """,
                    "java": """
                        class Solution {
                    """ + CMP_REV["java"].rstrip(" ") + """
                            public int compareReleases(String a, String b) {
                                String[] ra = a.split("\\\\."), rb = b.split("\\\\.");  //@split
                                for (int k = 0; k < Math.max(ra.length, rb.length); k++) {  //@loop
                                    String x = k < ra.length ? ra[k] : "0", y = k < rb.length ? rb[k] : "0";  //@pad
                                    int c = cmpRev(x, y);  //@rev
                                    if (c != 0) return c;  //@rev
                                }
                                return 0;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static vector<string> split(const string& s) {  //@split
                                vector<string> out(1);  //@split
                                for (char c : s) if (c == '.') out.emplace_back(); else out.back() += c;  //@split
                                return out;  //@split
                            }  //@split

                            static int cmpRev(string x, string y) {  //@rev
                                x.erase(0, min(x.find_first_not_of('0'), x.size()));  //@rev
                                y.erase(0, min(y.find_first_not_of('0'), y.size()));  //@rev
                                if (x.size() != y.size()) return x.size() > y.size() ? 1 : -1;  //@rev
                                return x == y ? 0 : x > y ? 1 : -1;  //@rev
                            }  //@rev

                        public:
                            int compareReleases(string& a, string& b) {
                                vector<string> ra = split(a), rb = split(b);  //@split
                                for (size_t k = 0; k < max(ra.size(), rb.size()); k++) {  //@loop
                                    int c = cmpRev(k < ra.size() ? ra[k] : "0", k < rb.size() ? rb[k] : "0");  //@pad
                                    if (c != 0) return c;  //@rev
                                }
                                return 0;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int split(const char* s, const char*** starts, int** lens) {  //@split
                            int n = strlen(s), parts = 1;  //@split
                            for (int i = 0; i < n; i++) if (s[i] == '.') parts++;  //@split
                            *starts = malloc(parts * sizeof(char*));  //@split
                            *lens = malloc(parts * sizeof(int));  //@split
                            int p = 0, from = 0;  //@split
                            for (int i = 0; i <= n; i++)  //@split
                                if (i == n || s[i] == '.') { (*starts)[p] = s + from; (*lens)[p++] = i - from; from = i + 1; }  //@split
                            return parts;  //@split
                        }  //@split

                        static int cmp_rev(const char* x, int xl, const char* y, int yl) {  //@rev
                            while (xl > 0 && *x == '0') { x++; xl--; }  //@rev
                            while (yl > 0 && *y == '0') { y++; yl--; }  //@rev
                            if (xl != yl) return xl > yl ? 1 : -1;  //@rev
                            int c = strncmp(x, y, xl);  //@rev
                            return c > 0 ? 1 : c < 0 ? -1 : 0;  //@rev
                        }  //@rev

                        int compareReleases(char* a, char* b) {
                            const char **sa, **sb;  //@split
                            int *la, *lb;  //@split
                            int na = split(a, &sa, &la), nb = split(b, &sb, &lb), answer = 0;  //@split
                            for (int k = 0; k < (na > nb ? na : nb) && answer == 0; k++)  //@loop
                                answer = cmp_rev(k < na ? sa[k] : "0", k < na ? la[k] : 1, k < nb ? sb[k] : "0", k < nb ? lb[k] : 1);  //@pad
                            free(sa); free(sb); free(la); free(lb);  //@ret
                            return answer;  //@ret
                        }
                    """,
                },
                lines=[
                    ("split", "Cut both releases into their revisions.", {"c": "Record each revision's start and length instead of copying it."}),
                    ("loop", "Up to the longer release."),
                    ("pad", "A missing revision is 0."),
                    ("rev", "Strip leading zeros. More digits means bigger; the same digit count compares as text. The first difference decides."),
                    ("ret", "Every revision equal: the same release."),
                ],
                complexity=["**Time O(n + m).** **Space O(n + m)** for the split lists."],
                limits=["The split lists are an extra copy of the input. Two pointers can cut each revision on the fly."],
            ),
            approach(
                "Two pointers, no splitting",
                "best",
                "O(n + m)",
                "O(1)",
                idea=["Pointers `i` and `j` each skip leading zeros of their next revision, then measure its digits up to the next dot. Compare by length, then by digits. A finished string supplies an empty revision (0)."],
                walk=w2,
                build=["Loop while either string has revisions left.", "Skip zeros and measure each revision.", "Compare and move past the dot."],
                code={
                    "python": """
                        class Solution:
                            def compareReleases(self, a: str, b: str) -> int:
                                i, j, n, m = 0, 0, len(a), len(b)  #@init
                                while i < n or j < m:  #@loop
                                    while i < n and a[i] == "0":  #@zeros
                                        i += 1  #@zeros
                                    while j < m and b[j] == "0":  #@zeros
                                        j += 1  #@zeros
                                    si, sj = i, j  #@measure
                                    while i < n and a[i] != ".":  #@measure
                                        i += 1  #@measure
                                    while j < m and b[j] != ".":  #@measure
                                        j += 1  #@measure
                                    x, y = a[si:i], b[sj:j]  #@cmp
                                    if len(x) != len(y):  #@cmp
                                        return 1 if len(x) > len(y) else -1  #@cmp
                                    if x != y:  #@cmp
                                        return 1 if x > y else -1  #@cmp
                                    i, j = i + 1, j + 1  #@dot
                                return 0  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int compareReleases(String a, String b) {
                                int i = 0, j = 0, n = a.length(), m = b.length();  //@init
                                while (i < n || j < m) {  //@loop
                                    while (i < n && a.charAt(i) == '0') i++;  //@zeros
                                    while (j < m && b.charAt(j) == '0') j++;  //@zeros
                                    int si = i, sj = j;  //@measure
                                    while (i < n && a.charAt(i) != '.') i++;  //@measure
                                    while (j < m && b.charAt(j) != '.') j++;  //@measure
                                    if (i - si != j - sj) return i - si > j - sj ? 1 : -1;  //@cmp
                                    for (int k = 0; k < i - si; k++)  //@cmp
                                        if (a.charAt(si + k) != b.charAt(sj + k)) return a.charAt(si + k) > b.charAt(sj + k) ? 1 : -1;  //@cmp
                                    i++;  //@dot
                                    j++;  //@dot
                                }
                                return 0;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int compareReleases(string& a, string& b) {
                                int i = 0, j = 0, n = a.size(), m = b.size();  //@init
                                while (i < n || j < m) {  //@loop
                                    while (i < n && a[i] == '0') i++;  //@zeros
                                    while (j < m && b[j] == '0') j++;  //@zeros
                                    int si = i, sj = j;  //@measure
                                    while (i < n && a[i] != '.') i++;  //@measure
                                    while (j < m && b[j] != '.') j++;  //@measure
                                    if (i - si != j - sj) return i - si > j - sj ? 1 : -1;  //@cmp
                                    for (int k = 0; k < i - si; k++)  //@cmp
                                        if (a[si + k] != b[sj + k]) return a[si + k] > b[sj + k] ? 1 : -1;  //@cmp
                                    i++;  //@dot
                                    j++;  //@dot
                                }
                                return 0;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int compareReleases(char* a, char* b) {
                            int i = 0, j = 0, n = strlen(a), m = strlen(b);  //@init
                            while (i < n || j < m) {  //@loop
                                while (i < n && a[i] == '0') i++;  //@zeros
                                while (j < m && b[j] == '0') j++;  //@zeros
                                int si = i, sj = j;  //@measure
                                while (i < n && a[i] != '.') i++;  //@measure
                                while (j < m && b[j] != '.') j++;  //@measure
                                if (i - si != j - sj) return i - si > j - sj ? 1 : -1;  //@cmp
                                for (int k = 0; k < i - si; k++)  //@cmp
                                    if (a[si + k] != b[sj + k]) return a[si + k] > b[sj + k] ? 1 : -1;  //@cmp
                                i++;  //@dot
                                j++;  //@dot
                            }
                            return 0;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "One pointer per release."),
                    ("loop", "While either release has revisions left; a finished one keeps supplying empty revisions, which mean 0."),
                    ("zeros", "Skip leading zeros. A revision of only zeros becomes empty, i.e. 0."),
                    ("measure", "Find the end of each revision (the next dot or the end of the string)."),
                    ("cmp", "More significant digits wins; with the same count, the first differing digit decides."),
                    ("dot", "Step over the dots (or past the end, which is harmless)."),
                    ("ret", "No revision differed."),
                ],
                complexity=["**Time O(n + m).** **Space O(1)** (the Python slices are a convenience; the other languages compare in place)."],
            ),
        ],
        takeaways=[
            """
            - **Compare huge numbers as text:** strip leading zeros, compare lengths, then digits.
            - Missing parts default to 0, so `1.0` equals `1`.
            - Pointers that cut fields on the fly avoid splitting the whole string.
            """
        ],
    )


def zig_ref(text, rows):
    if rows == 1:
        return text
    lines = [""] * rows
    r, d = 0, 1
    for c in text:
        lines[r] += c
        if r == 0:
            d = 1
        elif r == rows - 1:
            d = -1
        r += d
    return "".join(lines)


@problem
def zigzag_banner():
    text, rows = "SUMMERFAIR", 4
    want = zig_ref(text, rows)
    n = len(text)

    lines = [[] for _ in range(rows)]
    w1 = Steps("Walk the characters down and up, appending each to its row's buffer.")
    r, d = 0, 1
    for k, c in enumerate(text):
        lines[r].append(c)
        if r == 0:
            d = 1
        elif r == rows - 1:
            d = -1
        if k in (0, 3, 6, n - 1):
            w1.step(f"'{c}' goes on row {r}.", *[Row(x or ["·"], label=f"row {q}") for q, x in enumerate(lines)])
        r += d
    w1.step(f"Read the rows in order: {want}.", result=want)

    cycle = 2 * (rows - 1)
    w2 = Steps(f"A full down-and-up trip is cycle = 2·(rows − 1) = {cycle} characters. Row r takes positions k·{cycle} + r, and middle rows also k·{cycle} + {cycle} − r.")
    out = []
    for rr in range(rows):
        got = []
        for start in range(0, n, cycle):
            if start + rr < n:
                got.append(start + rr)
            if 0 < rr < rows - 1 and start + cycle - rr < n:
                got.append(start + cycle - rr)
        out += got
        w2.step(f"Row {rr}: positions {got} → {''.join(text[g] for g in got)}.", Row(list(text), st={g: "found" for g in got}))
    w2.step(f"Code: {want}.", result=want)

    sol(
        "zigzag-banner",
        summary="""
            The zigzag repeats every `cycle = 2·(rows − 1)` characters. Row `r` receives the characters at positions
            `k·cycle + r`, and every middle row also gets `k·cycle + cycle − r` (the way back up). Emitting rows in order
            builds the code directly. One row is a special case (cycle 0). O(n).
        """,
        question=[
            """
            Write `text` in a zigzag over `rows` rows (down from row 0 to the last row, back up, and so on), then read the
            rows top to bottom.

            - **One row** means the text is unchanged.
            - **n up to 10⁵**, rows up to 1000.
            """
        ],
        think=[
            f"""
            `"{text}"` over {rows} rows → **{want}**.

            Simulating is easy: a buffer per row and a direction that flips at the top and bottom. But the pattern is
            periodic: after `{cycle}` characters the zigzag is back at row 0 going down. So the positions on each row form
            a simple arithmetic pattern and can be read directly from `text`.
            """,
            fig(*[Row(list("".join(ch if zig_row(i, rows) == q else "·" for i, ch in enumerate(text))), label=f"row {q}") for q in range(rows)]),
        ],
        approaches=[
            approach(
                "Simulate with a buffer per row",
                "better",
                "O(n)",
                "O(n)",
                idea=["Keep `rows` buffers and a current row with direction ±1. Append each character to its row, flipping direction at the top and bottom. Join the buffers."],
                walk=w1,
                build=["Row buffers.", "Bounce between the top and bottom rows.", "Concatenate."],
                code={
                    "python": """
                        class Solution:
                            def zigzagCode(self, text: str, rows: int) -> str:
                                if rows == 1:  #@one
                                    return text  #@one
                                lines = [[] for _ in range(rows)]  #@init
                                r, step = 0, 1  #@init
                                for c in text:  #@walk
                                    lines[r].append(c)  #@walk
                                    if r == 0:  #@bounce
                                        step = 1  #@bounce
                                    elif r == rows - 1:  #@bounce
                                        step = -1  #@bounce
                                    r += step  #@walk
                                return "".join("".join(line) for line in lines)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String zigzagCode(String text, int rows) {
                                if (rows == 1) return text;  //@one
                                StringBuilder[] lines = new StringBuilder[rows];  //@init
                                for (int q = 0; q < rows; q++) lines[q] = new StringBuilder();  //@init
                                int r = 0, step = 1;  //@init
                                for (char c : text.toCharArray()) {  //@walk
                                    lines[r].append(c);  //@walk
                                    if (r == 0) step = 1;  //@bounce
                                    else if (r == rows - 1) step = -1;  //@bounce
                                    r += step;  //@walk
                                }
                                StringBuilder out = new StringBuilder();  //@ret
                                for (StringBuilder line : lines) out.append(line);  //@ret
                                return out.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string zigzagCode(string& text, int rows) {
                                if (rows == 1) return text;  //@one
                                vector<string> lines(rows);  //@init
                                int r = 0, step = 1;  //@init
                                for (char c : text) {  //@walk
                                    lines[r] += c;  //@walk
                                    if (r == 0) step = 1;  //@bounce
                                    else if (r == rows - 1) step = -1;  //@bounce
                                    r += step;  //@walk
                                }
                                string out;  //@ret
                                for (string& line : lines) out += line;  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* zigzagCode(char* text, int rows) {
                            int n = strlen(text);  //@one
                            char* out = malloc(n + 1);  //@one
                            if (rows == 1) { memcpy(out, text, n + 1); return out; }  //@one
                            int* rowOf = malloc(n * sizeof(int));  //@init
                            int r = 0, step = 1, pos = 0;  //@init
                            for (int k = 0; k < n; k++) {  //@walk
                                rowOf[k] = r;  //@walk
                                if (r == 0) step = 1;  //@bounce
                                else if (r == rows - 1) step = -1;  //@bounce
                                r += step;  //@walk
                            }
                            for (int q = 0; q < rows; q++)  //@ret
                                for (int k = 0; k < n; k++) if (rowOf[k] == q) out[pos++] = text[k];  //@ret
                            out[pos] = '\\0';  //@ret
                            free(rowOf);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("one", "With one row there's no zigzag (and the bounce below would never move)."),
                    ("init", "A buffer per row, starting at row 0 going down.", {"c": "Record each character's row instead of growing per-row buffers."}),
                    ("walk", "Place the character, then move one row."),
                    ("bounce", "Turn around at the top and bottom rows."),
                    ("ret", "Rows top to bottom.", {"c": "Gather the characters row by row. This costs O(n · rows) in C, still fine for the limits, but the next approach avoids it."}),
                ],
                complexity=["**Time O(n)** (O(n · rows) for the simple C version). **Space O(n)** for the buffers."],
                limits=["Builds an intermediate copy of the text split into rows. The cycle positions give each row's characters directly."],
            ),
            approach(
                "Read each row by its cycle positions",
                "best",
                "O(n)",
                "O(1)",
                idea=["`cycle = 2·(rows − 1)`. For row `r`, for each cycle start `k`: take `k + r`, and for middle rows also `k + cycle − r`."],
                walk=w2,
                build=["Handle one row (or rows ≥ n).", "Loop rows, then cycles.", "Up-slope character for middle rows."],
                code={
                    "python": """
                        class Solution:
                            def zigzagCode(self, text: str, rows: int) -> str:
                                n = len(text)  #@one
                                if rows == 1 or rows >= n:  #@one
                                    return text  #@one
                                cycle = 2 * (rows - 1)  #@cycle
                                out = []  #@cycle
                                for r in range(rows):  #@rows
                                    for start in range(0, n, cycle):  #@rows
                                        if start + r < n:  #@down
                                            out.append(text[start + r])  #@down
                                        if 0 < r < rows - 1 and start + cycle - r < n:  #@up
                                            out.append(text[start + cycle - r])  #@up
                                return "".join(out)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String zigzagCode(String text, int rows) {
                                int n = text.length();  //@one
                                if (rows == 1 || rows >= n) return text;  //@one
                                int cycle = 2 * (rows - 1);  //@cycle
                                StringBuilder out = new StringBuilder();  //@cycle
                                for (int r = 0; r < rows; r++)  //@rows
                                    for (int start = 0; start < n; start += cycle) {  //@rows
                                        if (start + r < n) out.append(text.charAt(start + r));  //@down
                                        if (r > 0 && r < rows - 1 && start + cycle - r < n) out.append(text.charAt(start + cycle - r));  //@up
                                    }
                                return out.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string zigzagCode(string& text, int rows) {
                                int n = text.size();  //@one
                                if (rows == 1 || rows >= n) return text;  //@one
                                int cycle = 2 * (rows - 1);  //@cycle
                                string out;  //@cycle
                                for (int r = 0; r < rows; r++)  //@rows
                                    for (int start = 0; start < n; start += cycle) {  //@rows
                                        if (start + r < n) out += text[start + r];  //@down
                                        if (r > 0 && r < rows - 1 && start + cycle - r < n) out += text[start + cycle - r];  //@up
                                    }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* zigzagCode(char* text, int rows) {
                            int n = strlen(text), pos = 0;  //@one
                            char* out = malloc(n + 1);  //@one
                            if (rows == 1 || rows >= n) { memcpy(out, text, n + 1); return out; }  //@one
                            int cycle = 2 * (rows - 1);  //@cycle
                            for (int r = 0; r < rows; r++)  //@rows
                                for (int start = 0; start < n; start += cycle) {  //@rows
                                    if (start + r < n) out[pos++] = text[start + r];  //@down
                                    if (r > 0 && r < rows - 1 && start + cycle - r < n) out[pos++] = text[start + cycle - r];  //@up
                                }
                            out[pos] = '\\0';  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("one", "One row, or at least as many rows as characters: everything goes straight down, so the text is unchanged."),
                    ("cycle", "A full trip down and back up to (but not including) row 0."),
                    ("rows", "Emit row by row; within a row, cycle by cycle (left to right)."),
                    ("down", "On the way down, row `r` is hit at offset `r` of the cycle."),
                    ("up", "On the way up, middle rows are hit again at offset `cycle − r`. The top and bottom rows are hit only once per cycle."),
                    ("ret", "The code."),
                ],
                complexity=["**Time O(n):** each character is emitted once (plus O(rows) loop overhead). **Space O(1)** besides the output."],
            ),
        ],
        takeaways=[
            """
            - **Periodic layouts → index arithmetic:** find the period, then each row is a formula.
            - Simulation is a fine first answer; it's O(n) too.
            - Edge cases: one row (period 0) and more rows than characters.
            """
        ],
    )


def zig_row(i, rows):
    if rows == 1:
        return 0
    cycle = 2 * (rows - 1)
    k = i % cycle
    return k if k < rows else cycle - k
