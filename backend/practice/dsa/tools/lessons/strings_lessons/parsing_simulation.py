"""Lesson: Parsing and simulation (Strings, pattern 4)."""
from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

CSV = {
    "python": """
        def split_csv(line):
            fields, cur = [], []                            #@state
            quoted = False                                  #@state
            i = 0                                           #@state
            while i < len(line):                            #@loop
                ch = line[i]                                #@loop
                if quoted:
                    if ch == '"':
                        if i + 1 < len(line) and line[i + 1] == '"':    #@escape
                            cur.append('"')                 #@escape
                            i += 1                          #@escape
                        else:                               #@close
                            quoted = False                  #@close
                    else:                                   #@inq
                        cur.append(ch)                      #@inq
                elif ch == '"':                             #@open
                    quoted = True                           #@open
                elif ch == ',':                             #@comma
                    fields.append("".join(cur))             #@comma
                    cur = []                                #@comma
                else:                                       #@plain
                    cur.append(ch)                          #@plain
                i += 1                                      #@next
            fields.append("".join(cur))                     #@last
            return fields                                   #@ret
    """,
    "java": """
        static List<String> splitCsv(String line) {
            List<String> fields = new ArrayList<>();        //@state
            StringBuilder cur = new StringBuilder();        //@state
            boolean quoted = false;                         //@state
            for (int i = 0; i < line.length(); i++) {       //@loop
                char ch = line.charAt(i);                   //@loop
                if (quoted) {
                    if (ch == '"') {
                        if (i + 1 < line.length() && line.charAt(i + 1) == '"') {   //@escape
                            cur.append('"');                //@escape
                            i++;                            //@escape
                        } else {                            //@close
                            quoted = false;                 //@close
                        }
                    } else {                                //@inq
                        cur.append(ch);                     //@inq
                    }
                } else if (ch == '"') {                     //@open
                    quoted = true;                          //@open
                } else if (ch == ',') {                     //@comma
                    fields.add(cur.toString());             //@comma
                    cur.setLength(0);                       //@comma
                } else {                                    //@plain
                    cur.append(ch);                         //@plain
                }
            }
            fields.add(cur.toString());                     //@last
            return fields;                                  //@ret
        }
    """,
    "cpp": """
        vector<string> splitCsv(const string& line) {
            vector<string> fields;                          //@state
            string cur;                                     //@state
            bool quoted = false;                            //@state
            for (size_t i = 0; i < line.size(); i++) {      //@loop
                char ch = line[i];                          //@loop
                if (quoted) {
                    if (ch == '"') {
                        if (i + 1 < line.size() && line[i + 1] == '"') {    //@escape
                            cur += '"';                     //@escape
                            i++;                            //@escape
                        } else {                            //@close
                            quoted = false;                 //@close
                        }
                    } else {                                //@inq
                        cur += ch;                          //@inq
                    }
                } else if (ch == '"') {                     //@open
                    quoted = true;                          //@open
                } else if (ch == ',') {                     //@comma
                    fields.push_back(cur);                  //@comma
                    cur.clear();                            //@comma
                } else {                                    //@plain
                    cur += ch;                              //@plain
                }
            }
            fields.push_back(cur);                          //@last
            return fields;                                  //@ret
        }
    """,
    "c": """
        int splitCsv(const char* line, char* out) {
            int count = 0, w = 0;                           //@state
            bool quoted = false;                            //@state
            for (int i = 0; line[i] != '\\0'; i++) {        //@loop
                char ch = line[i];                          //@loop
                if (quoted) {
                    if (ch == '"') {
                        if (line[i + 1] == '"') {           //@escape
                            out[w++] = '"';                 //@escape
                            i++;                            //@escape
                        } else {                            //@close
                            quoted = false;                 //@close
                        }
                    } else {                                //@inq
                        out[w++] = ch;                      //@inq
                    }
                } else if (ch == '"') {                     //@open
                    quoted = true;                          //@open
                } else if (ch == ',') {                     //@comma
                    out[w++] = '\\0';                       //@comma
                    count++;                                //@comma
                } else {                                    //@plain
                    out[w++] = ch;                          //@plain
                }
            }
            out[w] = '\\0';                                 //@last
            return count + 1;                               //@ret
        }
    """,
}
CSV_RUN = {
    "python": '''
        for line in ['a,"b,c","say ""hi""",', '', 'x,,y', '"",z']:
            print(" ".join("[" + f + "]" for f in split_csv(line)))
    ''',
    "java": """
        public static void main(String[] args) {
            String[] lines = {"a,\\"b,c\\",\\"say \\"\\"hi\\"\\"\\",", "", "x,,y", "\\"\\",z"};
            for (String line : lines) {
                StringBuilder sb = new StringBuilder();
                for (String f : splitCsv(line)) sb.append(sb.length() > 0 ? " " : "").append("[").append(f).append("]");
                System.out.println(sb);
            }
        }
    """,
    "cpp": """
        int main() {
            vector<string> lines = {"a,\\"b,c\\",\\"say \\"\\"hi\\"\\"\\",", "", "x,,y", "\\"\\",z"};
            for (auto& line : lines) {
                vector<string> fs = splitCsv(line);
                for (size_t k = 0; k < fs.size(); k++) cout << (k ? " " : "") << "[" << fs[k] << "]";
                cout << "\\n";
            }
        }
    """,
    "c": """
        int main(void) {
            const char* lines[] = {"a,\\"b,c\\",\\"say \\"\\"hi\\"\\"\\",", "", "x,,y", "\\"\\",z"};
            char out[64];
            for (int t = 0; t < 4; t++) {
                int m = splitCsv(lines[t], out);
                const char* p = out;
                for (int k = 0; k < m; k++) {
                    printf(k ? " [%s]" : "[%s]", p);
                    p += strlen(p) + 1;
                }
                printf("\\n");
            }
            return 0;
        }
    """,
}

COMMAS = {
    "python": """
        def add_commas(n):
            digits = str(abs(n))                            #@digits
            out = []                                        #@build
            for i, ch in enumerate(digits):                 #@build
                if i > 0 and (len(digits) - i) % 3 == 0:    #@sep
                    out.append(",")                         #@sep
                out.append(ch)                              #@build
            return ("-" if n < 0 else "") + "".join(out)    #@sign
    """,
    "java": """
        static String addCommas(long n) {
            String digits = Long.toString(Math.abs(n));     //@digits
            StringBuilder out = new StringBuilder();        //@build
            for (int i = 0; i < digits.length(); i++) {     //@build
                if (i > 0 && (digits.length() - i) % 3 == 0)    //@sep
                    out.append(',');                        //@sep
                out.append(digits.charAt(i));               //@build
            }
            return (n < 0 ? "-" : "") + out;                //@sign
        }
    """,
    "cpp": """
        string addCommas(long long n) {
            string digits = to_string(n < 0 ? -n : n);      //@digits
            string out;                                     //@build
            for (size_t i = 0; i < digits.size(); i++) {    //@build
                if (i > 0 && (digits.size() - i) % 3 == 0)  //@sep
                    out += ',';                             //@sep
                out += digits[i];                           //@build
            }
            return (n < 0 ? "-" : "") + out;                //@sign
        }
    """,
    "c": """
        void addCommas(long long n, char* out) {
            char digits[24];                                //@digits
            unsigned long long mag = n < 0 ? 0ULL - (unsigned long long)n : (unsigned long long)n;  //@digits
            sprintf(digits, "%llu", mag);                   //@digits
            int len = strlen(digits), w = 0;                //@build
            if (n < 0) out[w++] = '-';                      //@sign
            for (int i = 0; i < len; i++) {                 //@build
                if (i > 0 && (len - i) % 3 == 0)            //@sep
                    out[w++] = ',';                         //@sep
                out[w++] = digits[i];                       //@build
            }
            out[w] = '\\0';                                 //@build
        }
    """,
}
COMMAS_RUN = {
    "python": """
        for n in [1234567, -1000, 999, 0, 9876543210]:
            print(add_commas(n))
    """,
    "java": """
        public static void main(String[] args) {
            for (long n : new long[] {1234567, -1000, 999, 0, 9876543210L}) System.out.println(addCommas(n));
        }
    """,
    "cpp": """
        int main() {
            for (long long n : {1234567LL, -1000LL, 999LL, 0LL, 9876543210LL}) cout << addCommas(n) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            long long ns[] = {1234567, -1000, 999, 0, 9876543210LL};
            char out[40];
            for (int i = 0; i < 5; i++) {
                addCommas(ns[i], out);
                printf("%s\\n", out);
            }
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

import csv  # noqa: E402
import io  # noqa: E402

split_csv = py(CSV["python"], "split_csv")
add_commas = py(COMMAS["python"], "add_commas")
for line in ['a,"b,c","say ""hi""",', '', 'x,,y', '"",z', 'id,"Lee, Ann","5"" tall"', '"a""b",c']:
    expect = next(csv.reader(io.StringIO(line)), [""])
    assert split_csv(line) == expect, (line, split_csv(line), expect)
for n in [1234567, -1000, 999, 0, 9876543210, -5, 100000]:
    assert add_commas(n) == f"{n:,}"

# Theory walk: a tokenizer, the "read while it's still a number" loop.
TK = "12+ 3*(45-6)"
SHOW = lambda s: ["␣" if c == " " else c for c in s]
kw = Steps(f"Splitting \"{TK}\" into tokens: numbers, operators and brackets, with spaces thrown away.")
tokens, i, st = [], 0, {}
kw.step("`i` starts at the first character. Each step reads one whole token, or skips one space.",
        Row(SHOW(TK), ptr={"i": 0}, slots=True, label="text"), M({"tokens": "none yet"}))
while i < len(TK):
    ch = TK[i]
    if ch == " ":
        st[i] = "dim"
        msg = f"A space at {i}: it separates tokens but isn't one. Skip it."
        i += 1
    elif ch.isdigit():
        j = i
        while j < len(TK) and TK[j].isdigit():
            j += 1
        tokens.append(TK[i:j])
        for k in range(i, j):
            st[k] = "answer"
        msg = (f"A digit at {i}. Keep reading while the characters are digits: \"{TK[i:j]}\" is one number token, "
               f"and `i` jumps to {j}." if j - i > 1 else f"A digit at {i}, and the next character isn't one: the number \"{TK[i:j]}\".")
        i = j
    else:
        tokens.append(ch)
        st[i] = "answer"
        msg = f"'{ch}' at {i} is a token on its own."
        i += 1
    kw.step(msg, Row(SHOW(TK), st=dict(st), ptr={"i": i if i < len(TK) else None}, slots=True, label="text"), M({"tokens": " ".join(tokens)}))
assert tokens == ["12", "+", "3", "*", "(", "45", "-", "6", ")"]
K_LEGEND = {"answer": "part of a token", "dim": "a space, skipped"}

# Trace walk: the CSV template.
TL = 'id,"Lee, Ann","5"" tall"'
tw = Steps(f"`split_csv('{TL}')`, one character per step.")
fields, cur, quoted, i, st = [], [], False, 0, {}


def t_panels():
    return (Row(list(TL), st=dict(st), ptr={"i": i if i < len(TL) else None}, slots=True, label="line"),
            M({"state": "inside quotes" if quoted else "outside quotes", "current field": "".join(cur) or "(empty)",
               "fields": " | ".join(fields) or "none yet"}))


tw.step("Outside quotes, with an empty field started.", *t_panels())
while i < len(TL):
    ch = TL[i]
    at = i
    if quoted:
        if ch == '"':
            if i + 1 < len(TL) and TL[i + 1] == '"':
                cur.append('"')
                st[at], st[at + 1] = "found", "found"
                msg = f"A quote inside quotes, followed by another quote: that pair is an escaped quote. Add one `\"` to the field and skip both."
                i += 1
            else:
                quoted = False
                st[at] = "dim"
                msg = "A quote inside quotes with no partner: the quoted part ends here."
        else:
            cur.append(ch)
            st[at] = "found"
            msg = ("A comma inside quotes: copied, because here it's data." if ch == "," else
                   "A space inside quotes: copied." if ch == " " else f"'{ch}' inside quotes: copied.")
    elif ch == '"':
        quoted = True
        st[at] = "dim"
        msg = "A quote outside quotes: the quoted part starts. The quote itself isn't copied."
    elif ch == ",":
        fields.append("".join(cur))
        cur = []
        st[at] = "dim"
        msg = f"A comma outside quotes ends the field \"{fields[-1]}\". Start a new one."
    else:
        cur.append(ch)
        st[at] = "found"
        msg = f"'{ch}': an ordinary character, copied."
    i += 1
    tw.step(msg, *t_panels())
fields.append("".join(cur))
cur = []
tw.step(f"The line ends, which closes the last field. Fields: {' | '.join(fields)}.", *t_panels(), result=" | ".join(fields))
assert fields == split_csv(TL)
FINAL_ST = dict(st)
T_LEGEND = {"found": "copied into a field", "dim": "punctuation: read, not copied"}

STATES = [
    ("outside quotes", "`,`", "finish the field; stay outside"),
    ("outside quotes", "`\"`", "go inside quotes"),
    ("outside quotes", "anything else", "copy it"),
    ("inside quotes", "`\"` then `\"`", "copy one `\"`; skip both"),
    ("inside quotes", "`\"` then anything else", "go outside quotes"),
    ("inside quotes", "anything else (even `,`)", "copy it"),
]

lesson(
    "strings",
    "parsing-simulation",
    """
    Some string problems have no clever trick: you read the text one character at a time and follow the rules
    exactly. Doing that well means keeping the state you're in explicit, reading whole tokens with an inner loop,
    checking bounds before you peek ahead, and testing the edge cases the rules mention.
    """,
    [
        ("idea", "The idea", [
            """
            Think of a cashier reading a handwritten order: "2 coffees, 1 tea with milk, 3 muffins". They read a number,
            then the item name up to the comma, then start the next item. A comma inside "tea, no sugar" written in
            brackets wouldn't end the item, because they know they're inside brackets. They never jump around; they
            keep a little bit of memory (am I reading a number? an item? inside brackets?) and decide what each
            character means from that.

            That's what a parser is: a loop over the characters, plus a small amount of *state* that says how to treat
            the next one. The hard part of these problems is never the algorithm. It's following the rules exactly:
            the empty field, the trailing separator, the sign with no digits after it, the number that's too big.
            """,
            fig(Row(list(TL), st=FINAL_ST, slots=True, label="line"),
                caption="The comma inside the quotes is data; the other commas and the quotes are punctuation."),
            key("""
            Walk the string with an index. Keep the state in named variables (a flag, a mode, a partial token). Read
            multi-character tokens with an inner loop that stops at the first character that doesn't belong. Check
            `i + 1 < n` before looking ahead. Finish the last token after the loop.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The statement is mostly rules: a format to read (numbers, versions, encoded lists, CSV, IP addresses), a
            layout to produce (justified text, a zigzag, a table), or a process to imitate step by step. Constraints
            are usually small enough that O(n) or even O(n²) is fine, and the risk is in the details.
            """,
            table(
                ["The problem says…", "the state you keep"],
                ["read a number with an optional sign and limits", "sign, value so far, whether any digit was seen"],
                ["split fields, with quotes or escapes", "inside quotes or not, the field so far"],
                ["compare dotted versions", "a position in each string, the current part's value"],
                ["decode `length#text` records", "where the next record starts"],
                ["lay text out in rows or lines", "the current row or line, and its width so far"],
                ["format a number for display", "how many digits are left to write"],
            ),
            """
            Not a fit for a hand-written loop:

            - Nested structure (brackets inside brackets, expressions with precedence). Use a stack (Stack & Queue
              topic) or recursion.
            - Real-world formats in production code. Use the library parser (`csv`, `json`, `ipaddress`), which already
              handles the cases you'd forget.
            """,
        ]),
        ("theory", "How to get it right", [
            """
            ### Tokens: read while it still belongs

            Most formats are made of tokens: a number, a word, an operator. The reliable way to read one is an inner loop
            that starts at the first character and keeps going while the next character still belongs, then leaves the
            index on the first character that doesn't. The outer loop never has to undo anything.
            """,
            walk(kw, legend=K_LEGEND),
            """
            ### State machines

            When the meaning of a character depends on what came before (inside quotes or not, before or after a sign),
            write the states down and decide what every kind of character does in every state. If a cell of that table
            is blank, the rules haven't told you yet, and you should check the statement. For a CSV line with quotes:
            """,
            table(["state", "next character", "action"], *STATES),
            """
            Six rules, no special cases left over. The code is a direct copy of the table.

            ### Peeking ahead

            Some rules need the next character (`""` is an escaped quote; `_` counts only if a digit follows). Always
            check that the next index exists before reading it, and decide what happens at the end of the string: in
            C the next character is the terminating `'\\0'`, which conveniently matches nothing.

            ### The last token

            A loop that finishes a token when it sees a separator never sees a separator after the last token. Finish
            it after the loop. Forgetting this loses the last field, the last word or the last number, and it's the most
            common bug in parsing code.

            ### Limits and overflow

            When digits build a number (`value = value * 10 + d`), check for overflow *before* the multiplication would
            pass the limit, or build in a wider type and clamp. When a number can be far too long for any integer type
            (version parts, big IDs), compare it as a string: strip leading zeros, then compare lengths, then compare
            digit by digit.
            """,
        ]),
        ("template", "The template", [
            """
            Split one line of comma-separated values into fields. A field may be wrapped in double quotes, and then it
            can contain commas; inside quotes, `""` stands for one `"`. An empty line is one empty field.
            """,
            code(
                "Split a CSV line, with quotes",
                CSV,
                [
                    ("state", "The fields so far, the field being built, and whether we're inside quotes.",
                     {"c": "C writes each field into `out`, ending each with `'\\0'`, and counts them."}),
                    ("loop", "One character at a time."),
                    ("escape", "Inside quotes, `\"\"` is an escaped quote: copy one and skip the second."),
                    ("close", "Inside quotes, a lone `\"` ends the quoted part.",
                     {"c": "At the very end of the string the next character is `'\\0'`, which isn't a quote, so this is safe."}),
                    ("inq", "Anything else inside quotes, including a comma, is data."),
                    ("open", "Outside quotes, a `\"` starts a quoted part. The quote itself isn't data."),
                    ("comma", "Outside quotes, a comma ends the current field."),
                    ("plain", "Anything else outside quotes is data."),
                    ("next", "Move on. The escape case already moved one extra place."),
                    ("last", "The line ends without a comma, so the last field is finished here. This also makes an empty "
                             "line one empty field, and a trailing comma an empty last field."),
                    ("ret", "All the fields, in order.", {"c": "C returns how many fields it wrote."}),
                ],
                CSV_RUN,
                'split_csv(\'a,"b,c","say ""hi""",\'); (\'\'); (\'x,,y\'); (\'"",z\')',
            ),
            """
            Each field is printed in brackets so empty ones show up. The trailing comma in the first line makes an empty
            fourth field, and `""` on its own is an empty quoted field.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "A line with a comma inside quotes and an escaped quote:",
            walk(tw, legend=T_LEGEND),
            """
            On paper, write the line once, and under it the state (in or out of quotes) after each character. Mark every
            character as data or punctuation. The fields are the runs of data between punctuation commas.
            """,
        ]),
        ("examples", "More examples", [
            """
            ### Reading a number carefully

            "Skip spaces, read an optional sign, read digits, stop at anything else, clamp to the 32-bit range" is a
            small state machine: before the sign, after the sign, in the digits. The edge cases are where the marks go:
            no digits at all (the answer is 0), a sign with nothing after it, two signs, leading zeros, and a value
            that passes `2³¹ - 1` partway through. Build the value in a 64-bit integer, or check
            `value > (LIMIT - d) / 10` before multiplying.

            ### Laying text out

            Problems that *produce* text (wrapping words into lines, padding columns, drawing a zigzag) are simulations
            too. Work in two phases: first decide what goes on each line (which words, or which characters), then format
            each line. Mixing the two is how off-by-one errors in spacing creep in.

            ### Length-prefixed records

            Writing each string as `length#string` lets the strings contain anything, including `#`. Reading it back is
            a loop: read digits up to the `#`, then take exactly that many characters, whatever they are. The length tells
            you where the next record starts; you never search for a separator inside the data.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Producing text: thousands separators

            Formatting is parsing in reverse. Write the digits of `|n|`, putting a comma before every digit whose
            distance from the end is a multiple of three, then put the sign back.
            """,
            code(
                "Add thousands separators",
                COMMAS,
                [
                    ("digits", "The digits of the absolute value.",
                     {"java": "`Math.abs(Long.MIN_VALUE)` is still negative; the full range would need special handling.",
                      "cpp": "`-n` overflows for the smallest `long long`; the full range would need special handling.",
                      "c": "Negating as `unsigned long long` handles even the smallest `long long`."}),
                    ("build", "Copy the digits left to right."),
                    ("sep", "A comma goes before a digit when the number of digits from it to the end is a multiple of 3, "
                            "except before the first digit."),
                    ("sign", "Put the minus sign back for negative numbers."),
                ],
                COMMAS_RUN,
                "add_commas(1234567); (-1000); (999); (0); (9876543210)",
            ),
            """
            ### Tokenize first, then work on tokens

            When a format has several kinds of token, split the text into a list of tokens first (as in the tokenizer
            walkthrough), then solve the problem on the list. Each phase is short and easy to test, and the second
            phase doesn't have to think about spaces or digit-by-digit reading.

            ### Comparing without converting

            To compare two numbers written as strings, possibly longer than any integer type: strip leading zeros, then
            the longer one is bigger, and equal lengths compare character by character (`"9" > "1"` as characters too).
            """,
        ]),
        ("complexity", "What it costs", [
            """
            One pass over the input, with O(1) work per character: O(n) time. Extra space is the output (the fields, the
            tokens, the formatted text). Watch out for hidden costs: building strings by repeated `+` in a loop can be
            O(n²) in some languages, and so can calling `strlen` inside a loop condition in C.
            """,
            table(
                ["Approach", "Time", "Notes"],
                ["One pass with explicit state", "O(n)", "the usual answer"],
                ["`split` and fix-ups afterwards", "O(n)", "breaks on quotes and escapes"],
                ["Regular expressions", "O(n) usually", "fine for simple formats, hard to get exactly right"],
                ["Repeated `str + ch` in a loop", "O(n²) in Java and C", "use a builder"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            Collect characters in a list and `"".join` once. `str.isdigit()` also accepts some non-ASCII digits; for
            strict parsing test `"0" <= ch <= "9"`. The `csv` module handles real CSV.

            ### Java

            `StringBuilder` for building, `Character.isDigit` (same non-ASCII caveat as Python), `charAt` for reading.
            `Integer.parseInt` throws on anything unexpected, which is a valid strategy if you catch it.

            ### C++

            `std::string` with `+=` is amortised O(1) per character. `isdigit` takes an `unsigned char` value; passing a
            negative `char` is undefined. `std::stoll` throws on bad input or overflow.

            ### C

            Write into a caller-provided buffer and terminate it with `'\\0'`. `strtol` parses numbers and reports
            overflow through `errno`. Make sure every buffer has room for the terminator.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Forgetting the last token after the loop.
            - Reading `s[i + 1]` without checking `i + 1 < n`.
            - Empty input, a trailing separator, two separators in a row: each usually means an empty field.
            - Signs without digits, digits without a sign, leading zeros.
            - Overflow while building a number from digits.
            - Using `split` on formats where the separator can appear inside quotes or escapes.
            - Building strings with `+` in a loop in Java or C.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("What fields does `split_csv` give for `a,,` and why?",
                 "Three: \"a\", \"\" and \"\". Each comma outside quotes ends a field, and the line's end finishes the last one, which is empty."),
                ("Why does the CSV loop need a state flag at all?",
                 "A comma means \"end of field\" outside quotes but is ordinary data inside them. The flag says which meaning applies."),
                ("Inside quotes the code sees `\"`. How does it decide what that quote means?",
                 "It peeks at the next character. Another `\"` means an escaped quote (copy one, skip both); anything else, or the end, means the quoted part is over."),
                ("A tokenizer reads digits with an inner loop. Where should that loop leave the index?",
                 "On the first character that isn't a digit, so the outer loop handles it next without skipping or re-reading anything."),
                ("How do you compare \"0012\" and \"9\" as numbers if they might be too long for any integer type?",
                 "Strip leading zeros (\"12\" and \"9\"). The longer one is bigger, so 12 > 9. Equal lengths would compare digit by digit."),
            ),
        ]),
    ],
)
