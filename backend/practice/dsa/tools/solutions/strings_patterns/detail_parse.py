"""In-depth text for the parsing and simulation problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table
from strings_patterns.parsing_simulation import cmp_ref, justify_ref, meter_ref, pack, zig_row

PARSE = """
**How to approach any parsing task.** Write the format as a sequence of phases, each with a clear rule for which
characters it consumes and what makes it stop. Then walk the text once with an index, handling one phase after
another. Most bugs come from the boundaries between phases, so list them explicitly as edge cases before coding.
"""

# ---------------------------------------------------------------- justify-the-column
words, width = ["Rain", "fell", "on", "the", "old", "tin", "roof", "all", "night."], 14
out = justify_ref(words, width)
jrows, i, n = [], 0, len(words)
while i < n:
    j, size = i + 1, len(words[i])
    while j < n and size + 1 + len(words[j]) <= width:
        size += 1 + len(words[j])
        j += 1
    gaps, letters = j - i - 1, size - (j - i - 1)
    if j == n or gaps == 0:
        rule = "last line" if j == n else "one word"
        spaces = f"left-aligned, {width - size} at the end"
    else:
        q, r = divmod(width - letters, gaps)
        rule = f"{width - letters} spare over {gaps} gaps"
        spaces = f"{q} each, first {r} get +1" if r else f"{q} each"
    jrows.append((" ".join(words[i:j]), letters, rule, spaces, out[len(jrows)].replace(" ", "·")))
    i = j
EXTRA["justify-the-column"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A line with a single word is left-aligned even if it isn't the last line.
        - The last line is always left-aligned, however many words it has.
        - A word exactly `width` long fills a line by itself.
        - Spaces that don't divide evenly go to the **leftmost** gaps.
        """
    ],
    "think": [
        PARSE,
        """
        **Two independent decisions per line.**

        1. **Which words?** Take words while `letters + (one space between each) ≤ width`. Greedy filling is what the
           statement asks for, and the spacing chosen later never changes this decision.
        2. **How many spaces?** On a full line with `g` gaps and `spare = width − letters` spaces, every gap gets
           `spare // g` and the first `spare % g` gaps get one extra.
        """,
        f"**Line by line** for width {width}:",
        table(["words", "letters", "rule", "spaces", "line (· = space)"], *jrows),
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Walk the words with index `i`. For each line, extend `j` while the next word still fits with one space,
                tracking `size` = letters plus single spaces. Then build the line: left-aligned for the last line or a
                one-word line, otherwise justified with `divmod(spare, gaps)`. Continue from `j`.

                **Why the arithmetic is right.** `size − gaps` is the letter count, so `spare = width − letters` spaces
                must be distributed. `q = spare // gaps` and `r = spare % gaps` give `q·gaps + r = spare` spaces in total
                when the first `r` gaps get `q + 1`, so the line is exactly `width` long.
                """
            ],
            "build": [
                "Start at word 0.",
                "Grow the line while `size + 1 + len(next) ≤ width`.",
                "Last line or one word: join with single spaces, pad the end.",
                "Otherwise give each gap `q` spaces, the first `r` gaps `q + 1`, no spaces after the last word.",
                "Store the line and continue after it.",
            ],
            "complexity": ["**Time O(L)**, where L is the total output length (lines × width): each word is measured once and each output character written once. **Space O(L)** for the output."],
            "lines": {
                "init": "The output and the index of the first word not yet placed. C allocates one slot per word, the most lines there can be.",
                "pick": "Grow the line greedily. `size` counts letters plus one space between neighbours, which is the narrowest the line can be; `gaps` is the number of spaces between its words.",
                "left": "The last line, or a line with one word: single spaces between words, then spaces at the end up to `width`.",
                "full": "Justify: `spare = width − letters` spaces over `gaps` gaps, `q` each and one more for the first `r` gaps. The last word gets no trailing spaces.",
                "next": "Store the finished line and start the next line at word `j`.",
                "ret": "All lines, top to bottom.",
            },
        },
    },
    "takeaways": [
        """
        - **Separate layout from formatting:** choose the words greedily, then compute the spacing.
        - **Distributing `s` items over `g` slots, left-heavy:** `s // g` each, plus one for the first `s % g`.
        - **Pitfalls:** the one-word line (division by zero gaps), and justifying the last line by mistake.
        """
    ],
}


# ---------------------------------------------------------------- read-the-meter
cases = ["  -12_405_kWh", "+7", "5__6", "_42", "12_", "  - 3", "99_999_999_999", "-99999999999", "abc", ""]
EXTRA["read-the-meter"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Only spaces are skipped at the start, not other characters.
        - At most one sign; `+-5` and `- 5` read as 0 (the sign must be followed directly by a digit).
        - An underscore needs a digit on **both** sides; anywhere else it stops the reading.
        - Values beyond 32 bits clamp to `−2³¹` or `2³¹ − 1`.
        """
    ],
    "think": [
        PARSE,
        """
        **The phases here:**

        1. **Spaces:** consume `' '` characters.
        2. **Sign:** consume one `+` or `−` if present.
        3. **Digits:** consume digits, and an underscore only if a digit was read before it and the next character is a
           digit. Anything else stops.
        4. **Finish:** no digits means 0; otherwise apply the sign and clamp.

        **Overflow without big numbers.** Once the magnitude passes 2³¹ the final answer is already decided: it clamps.
        So cap the running value at 2³¹ after every digit; it then always fits in 64 bits.
        """,
        "**Readings of tricky inputs:**",
        table(["text", "value"], *[(f'"{c}"', meter_ref(c)) for c in cases]),
    ],
    "approaches": {
        0: {
            "idea": [
                """
                One index walks through the phases above. In the digit phase keep `value = min(2³¹, value · 10 + digit)`
                and a flag `seen` that turns on at the first digit. At the end return `clamp(sign · value)`.

                **Why capping at 2³¹ is safe.** Any magnitude of at least 2³¹ clamps to the same answer (`2³¹ − 1` for
                positive, `−2³¹` for negative, and `−2³¹` is exactly `−1 · 2³¹`). So replacing a larger value by 2³¹ never
                changes the result.
                """
            ],
            "build": [
                "Skip leading spaces.",
                "Read an optional sign.",
                "Read digits and valid underscores, capping the value.",
                "Apply the sign and clamp.",
            ],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "lines": {
                "spaces": "Phase 1: only the space character is skipped.",
                "sign": "Phase 2: at most one sign character; it isn't required.",
                "digits": "Phase 3: each digit shifts the value left one decimal place. Capping at 2³¹ keeps it small while still remembering that it's out of range. `seen` records that a digit was read.",
                "under": "An underscore is skipped only between two digits (one already read, one next). Any other character, including a misplaced underscore, ends the number.",
                "clamp": "Apply the sign and clamp into the 32-bit range. With no digits, `value` is 0.",
            },
        },
    },
    "takeaways": [
        """
        - **Parsing = phases + one index.** Write down each phase's stop condition.
        - **Cap early** when the result is known to clamp, instead of using big integers.
        - **Pitfalls:** treating a lone sign as a number; accepting underscores at the edges.
        """
    ],
}


# ---------------------------------------------------------------- unpack-the-bundle
items = ["a#1", "", "12#"]
bundle = pack(items)
urows, i = [], 0
while i < len(bundle):
    j = bundle.index("#", i)
    size = int(bundle[i:j])
    urows.append((i, bundle[i:j], j, size, f'"{bundle[j + 1:j + 1 + size]}"', j + 1 + size))
    i = j + 1 + size
EXTRA["unpack-the-bundle"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Empty strings in the list (`0#`), which take no characters after the `#`.
        - Strings that contain `#` or digits; these must be copied, not interpreted.
        - Lengths with several digits (`12#…`).
        - An empty bundle means an empty list.
        """
    ],
    "think": [
        f"""
        **Why splitting on `#` fails.** `{items}` packs as `"{bundle}"`. Splitting on `#` would cut inside `a#1` and
        `12#`. The `#` is only trustworthy in one place: right after a length.

        **The format as phases.** Each item is: digits (the length `k`), a `#`, then exactly `k` characters. Because the
        length is read first, we always know where the current item ends, so we never have to look inside it.
        """,
        "**Trace:**",
        table(["item starts at", "length text", "# at", "length", "item", "next item starts at"], *urows),
        """
        **Why the first `#` after the digits is the separator.** At the start of an item we're reading the length, and
        lengths contain only digits. The first non-digit we meet is therefore the separator; a `#` inside the item comes
        after it and is never examined.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Keep a pointer `i`. Read digits up to the next `#` to get the length `k`. The item is the `k` characters
                after the `#`. Jump to just past them and repeat until the end.
                """
            ],
            "build": ["Pointer at 0.", "Parse the length up to `#`.", "Take the next `k` characters as one item.", "Jump past it."],
            "complexity": ["**Time O(n):** each character is read once, either as a digit, the `#`, or copied as content. **Space O(n)** for the output."],
            "lines": {
                "init": "The output list and the read pointer. C allocates `n / 2 + 1` slots, since every item takes at least two characters (`0#`).",
                "loop": "Each pass decodes exactly one item.",
                "len": "Read the length one digit at a time until the `#`. This `#` is guaranteed to be the separator, because the item's content hasn't started yet.",
                "take": "The next `size` characters are the item, whatever they contain. Then jump past them to the next item's length.",
                "ret": "The items in order, empty ones included.",
            },
        },
    },
    "takeaways": [
        """
        - **Length-prefixed encoding** handles any content: never search inside the payload.
        - Trust a delimiter only where the format guarantees it.
        - **Pitfalls:** splitting on the delimiter; reading only one digit of the length.
        """
    ],
}


# ---------------------------------------------------------------- which-release-is-newer
pairs = [("3.010.0.0", "3.9.000"), ("1.0", "1"), ("1.01", "1.001"), ("2.5", "2.10"), ("0.1", "0.0.1"), ("10", "9.99")]


def why(x, y):
    ra, rb = x.split("."), y.split(".")
    for k in range(max(len(ra), len(rb))):
        u = ra[k] if k < len(ra) else "0"
        v = rb[k] if k < len(rb) else "0"
        su, sv = u.lstrip("0") or "0", v.lstrip("0") or "0"
        if su != sv:
            how = "more digits" if len(su) != len(sv) else "larger digit"
            return f"revision {k}: {u} vs {v} → {su} vs {sv}, {how}"
    return "every revision equal (missing ones count as 0)"
EXTRA["which-release-is-newer"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Leading zeros: `01` and `1` are the same revision; `000` is 0.
        - Missing revisions are 0: `1.0.0` equals `1`.
        - Revisions longer than 64-bit integers (up to 50 digits).
        - Text comparison alone is wrong: `"9" > "10"` as text.
        """
    ],
    "think": [
        PARSE,
        """
        **Comparing huge numbers written as text.** Strip leading zeros. Then a number with more digits is larger; with
        the same number of digits, comparing the digits from the left (text comparison) gives the numeric order. That
        avoids any conversion to integers.

        **Comparing releases.** Walk revision by revision from the left; the first revision that differs decides. When
        one release runs out, its missing revisions count as 0 (an empty revision after stripping zeros).
        """,
        "**Examples:**",
        table(["a", "b", "result", "why"], *[(x, y, cmp_ref(x, y), why(x, y)) for x, y in pairs]),
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Split both strings at the dots. For `k` up to the longer list, compare `a[k]` and `b[k]` (or `"0"` if a
                list is shorter) with the strip-then-length-then-digits rule. The first non-zero result is the answer.
                """
            ],
            "build": ["Split into revisions.", "Pad the shorter list with `\"0\"`.", "Compare revisions with the big-number rule."],
            "complexity": ["**Time O(n + m).** **Space O(n + m)** for the split lists."],
            "limits": ["Splitting copies the input. Two pointers can cut each revision on the fly and compare it in place."],
            "lines": {
                "split": "Cut both releases at the dots. C records each revision's start and length instead of copying it.",
                "loop": "Up to the longer release.",
                "pad": "A release that has run out contributes `\"0\"`.",
                "rev": "Strip leading zeros; the longer number is bigger; equal lengths compare digit by digit. The first difference decides.",
                "ret": "Every revision was equal: the same release.",
            },
        },
        1: {
            "idea": [
                """
                Two pointers `i` and `j` cut one revision at a time from `a` and `b`. For each pair: skip leading zeros,
                measure the digits up to the next dot, compare by length and then digit by digit, then step over the dots.
                A finished string keeps producing empty revisions (value 0) until both are done.

                **Why the zero-skip is enough.** After skipping zeros, the measured part has no leading zero (or is empty,
                meaning 0), so length really does order the values.
                """
            ],
            "build": [
                "Pointers at the start of both strings.",
                "Skip zeros, then measure each revision.",
                "Compare lengths, then digits.",
                "Step over the dots; stop when both are exhausted.",
            ],
            "complexity": ["**Time O(n + m):** each character is visited once. **Space O(1).**"],
            "lines": {
                "init": "One pointer per release.",
                "loop": "Continue while either release has characters left.",
                "zeros": "Leading zeros don't change a revision's value; skipping them leaves the significant digits (or nothing, meaning 0).",
                "measure": "Find where each revision ends: the next dot or the end of the string.",
                "cmp": "More significant digits means a larger revision. With the same count, the first differing digit decides.",
                "dot": "Step over the dots. Stepping past the end is harmless: the loop condition checks both lengths.",
                "ret": "All revisions equal.",
            },
        },
    },
    "takeaways": [
        """
        - **Big numbers as text:** strip leading zeros, compare lengths, then digits.
        - **Missing parts default to 0**, so `1.0` equals `1`.
        - **Pitfalls:** converting to integers (overflow); comparing text without stripping zeros.
        """
    ],
}


# ---------------------------------------------------------------- zigzag-banner
text, rows = "SUMMERFAIR", 4
cycle = 2 * (rows - 1)
grid = [[text[i] if zig_row(i, rows) == r else "·" for i in range(len(text))] for r in range(rows)]
pos = []
for r in range(rows):
    got = []
    for start in range(0, len(text), cycle):
        if start + r < len(text):
            got.append(start + r)
        if 0 < r < rows - 1 and start + cycle - r < len(text):
            got.append(start + cycle - r)
    pos.append((r, got, "".join(text[g] for g in got)))
EXTRA["zigzag-banner"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `rows = 1`: the text is unchanged (and the cycle length would be 0).
        - `rows ≥ n`: every character is on its own row going down, so the text is unchanged.
        - The top and bottom rows get one character per cycle; middle rows get two.
        """
    ],
    "think": [
        f"""
        **Draw it first.** `"{text}"` over {rows} rows:
        """,
        table(["row"] + list(range(len(text))), *[[r] + g for r, g in enumerate(grid)]),
        f"""
        **The pattern repeats.** Going down takes `rows` steps and coming back up (not counting row 0 again) takes
        `rows − 2`, so a full cycle is `2·(rows − 1) = {cycle}` characters. Within a cycle starting at position `k`:

        - the way down puts position `k + r` on row `r`;
        - the way up puts position `k + cycle − r` on row `r`, for the middle rows only.

        **Row by row:**
        """,
        table(["row", "positions", "characters"], *pos),
        f"Reading the rows in order gives **`{''.join(p[2] for p in pos)}`**.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Simulate the drawing: keep a buffer per row, a current row and a direction. Append each character to its
                row, flip the direction at the top and bottom rows, then concatenate the buffers.

                Easy to get right, and already O(n), but it builds an intermediate copy of the text.
                """
            ],
            "build": ["One row: return the text.", "Row buffers, current row 0, direction down.", "Place each character and bounce at the ends.", "Join the rows."],
            "complexity": ["**Time O(n)** (C's simple gathering is O(n · rows)). **Space O(n)** for the buffers."],
            "limits": ["It needs buffers for the whole text. The cycle positions say directly which characters belong to each row, so the answer can be written straight out."],
            "lines": {
                "one": "With one row there's nothing to zigzag, and the bounce below would never move.",
                "init": "A buffer per row, starting on row 0 heading down. C records each character's row instead of building buffers.",
                "walk": "Put the character on the current row, then move one row in the current direction.",
                "bounce": "At the top row head down, at the bottom row head up.",
                "ret": "Concatenate the rows from top to bottom. C gathers characters row by row, which costs O(n · rows).",
            },
        },
        1: {
            "idea": [
                """
                For each row `r`, loop over cycle starts `k = 0, cycle, 2·cycle, …` and emit `text[k + r]` and, for middle
                rows, `text[k + cycle − r]`, skipping positions past the end.

                **Why every character is emitted exactly once.** Within a cycle, offsets `0 … rows − 1` are the way down
                and offsets `rows … cycle − 1` are the way up, where offset `cycle − r` belongs to row `r`. These cover each
                offset once, so each position appears in exactly one row's list.
                """
            ],
            "build": ["Handle `rows = 1` or `rows ≥ n`.", "Compute the cycle length.", "For each row, walk the cycles and emit the down and up positions."],
            "complexity": ["**Time O(n):** each character is emitted once, plus O(rows) loop overhead. **Space O(1)** besides the output."],
            "lines": {
                "one": "No zigzag happens with one row or with at least as many rows as characters.",
                "cycle": "The length of one full down-and-up trip.",
                "rows": "Build the answer row by row; within a row, cycle by cycle from left to right.",
                "down": "On the way down, row `r` is reached at offset `r` of each cycle.",
                "up": "On the way up, middle rows are reached again at offset `cycle − r`. The top and bottom rows aren't revisited.",
                "ret": "The code.",
            },
        },
    },
    "takeaways": [
        """
        - **Periodic layouts → index arithmetic:** find the period, then write each row as a formula.
        - Simulation is a fine first answer when it's already linear.
        - **Pitfalls:** `rows = 1` (cycle 0, infinite loop); emitting the top or bottom row twice per cycle.
        """
    ],
}
