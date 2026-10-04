"""In-depth text for the expression-evaluation problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

EXPR = """
**Why stacks fit expressions.** In an expression, an operator can't be applied until both of its operands are
complete, and a later operator may bind tighter (`*` before `+`) or a parenthesis may open a whole sub-expression. A
stack holds the parts that are **finished but not yet combined**, in exactly the order they'll be needed: the most
recent part is combined first.

**Truncating division.** "Toward zero" means `−7 / 2 = −3`, not −4. Python's `//` rounds down, so the solutions divide
the absolute values and then put the sign back.
"""


def tdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


# ---------------------------------------------------------------- postfix-calculator
toks = ["6", "2", "-", "-9", "4", "/", "*", "5", "+"]
st, prow = [], []
for t in toks:
    if t in ("+", "-", "*", "/"):
        b, a = st.pop(), st.pop()
        r = a + b if t == "+" else a - b if t == "-" else a * b if t == "*" else tdiv(a, b)
        st.append(r)
        prow.append((t, f"{a} {t} {b} = {r}", list(st)))
    else:
        st.append(int(t))
        prow.append((t, "push", list(st)))
EXTRA["postfix-calculator"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Negative numbers like `-9` are numbers, not the `-` operator: compare the whole token.
        - Operand order matters for `-` and `/`: the second popped value is the left operand.
        - Division truncates toward zero.
        """
    ],
    "think": [
        EXPR,
        """
        **Postfix needs no precedence rules.** Each operator comes right after its two operands, so when an operator
        arrives, its operands are the two most recent values: pop them, combine, push the result.
        """,
        f"**Trace on `{' '.join(toks)}`:**",
        table(["token", "action", "stack after"], *prow),
        f"Result **{st[0]}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Repeatedly find the first operator in the token list, combine the two tokens before it, and splice the result in. Each step shortens the list by two."],
            "build": ["Find the first operator.", "Combine its two operands.", "Splice and repeat."],
            "complexity": ["**Time O(n²):** each splice shifts the rest of the list. **Space O(n).**"],
            "limits": ["Searching and splicing repeatedly is quadratic. A stack keeps the pending values right where they're needed."],
        },
        1: {
            "idea": [
                """
                Push numbers; on an operator pop `b` then `a` and push `a op b`. The final stack holds the answer.

                **Invariant.** The stack holds the values of the complete sub-expressions read so far, in order.
                """
            ],
            "build": ["Empty stack.", "Number → push.", "Operator → pop two, apply, push.", "Return the single value left."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Postfix evaluation:** stack of values; operators combine the top two.
        - Pop order: right operand first.
        - **Pitfall:** floor division instead of truncation for negative results.
        """
    ],
}


# ---------------------------------------------------------------- desk-calculator
ex = "14 - 3*4/5 + 2*3"
total = last = num = 0
op, drows = "+", []
for c in ex + "+":
    if c == " ":
        continue
    if c.isdigit():
        num = num * 10 + int(c)
        continue
    if op in "+-":
        total += last
        last = num if op == "+" else -num
        act = f"'{op}{num}' starts a new term; the previous term is added to the total"
    elif op == "*":
        last *= num
        act = f"multiply the current term by {num}"
    else:
        last = tdiv(last, num)
        act = f"divide the current term by {num} (toward zero)"
    drows.append((f"{op} {num}", act, total, last))
    op, num = c, 0
EXTRA["desk-calculator"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Spaces anywhere between tokens.
        - Multi-digit numbers.
        - Division truncates toward zero, even when the current term is negative.
        """
    ],
    "think": [
        EXPR,
        f"""
        **Think in terms.** Without parentheses, the expression is a sum of **signed terms**, where each term is a chain
        of `*` and `/`. A `+` or `−` starts a new term; `*` and `/` modify the current one. So keep the running `total` of
        finished terms and the `last` (current) term. When an operator (or the end) arrives, apply the **previous**
        operator to the number just read. For `{ex}`:
        """,
        table(["operator and number", "action", "total", "current term"], *drows),
        f"Result: total + current term = **{total + last}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Tokenise into numbers and operators; first reduce all `*` and `/` left to right, then all `+` and `−`."],
            "build": ["Tokenise.", "Reduce multiplicative operators.", "Reduce additive operators."],
            "complexity": ["**Time O(n²)** because each reduction splices the token list. **Space O(n).**"],
            "limits": ["Two passes with list splicing. Handling terms as they're read needs a single pass."],
        },
        1: {
            "idea": ["Stack of signed terms: `+` pushes `num`, `−` pushes `−num`, `*` and `/` modify the top. The answer is the sum of the stack."],
            "build": ["Read numbers digit by digit.", "Apply the previous operator when a new one (or the end) arrives.", "Sum the stack."],
            "complexity": ["**Time O(n).** **Space O(n)** for the terms."],
            "limits": ["Only the top term ever changes, so the stack can be replaced by a running total plus the current term."],
        },
        2: {
            "idea": [
                """
                Keep `total` (finished terms) and `last` (the current term). On `+`/`−`, add `last` to `total` and start a
                new term; on `*`/`/`, modify `last`. A sentinel `+` at the end flushes the final term.
                """
            ],
            "build": ["`total = last = 0`, previous operator `+`.", "Build numbers digit by digit.", "Apply the previous operator.", "Return `total + last`."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **`+ − * /` without parentheses:** sum of signed terms; only the current term changes.
        - Apply the **previous** operator when the next one arrives; add a sentinel to flush the end.
        - **Pitfall:** truncating with floor division when the term is negative.
        """
    ],
}


# ---------------------------------------------------------------- pocket-calculator
pe = "-(6-2*4)/2 + 3*(1+2)"
frames, terms, op, num, crows = [], [], "+", 0, []
for c in pe + "#":
    if c == " ":
        continue
    if c.isdigit():
        num = num * 10 + int(c)
        continue
    if c == "(":
        frames.append((terms, op))
        crows.append(("(", f"save terms {terms} and pending operator '{op}'; start a fresh level", len(frames)))
        terms, op, num = [], "+", 0
        continue
    if op == "+":
        terms.append(num)
    elif op == "-":
        terms.append(-num)
    elif op == "*":
        terms[-1] *= num
    else:
        terms[-1] = tdiv(terms[-1], num)
    if c == ")":
        num = sum(terms)
        terms, op = frames.pop()
        crows.append((")", f"the level sums to {num}; restore the outer level and treat {num} as a number", len(frames)))
    else:
        crows.append((c, f"apply the previous operator; terms now {terms}", len(frames)))
        op, num = c, 0
EXTRA["pocket-calculator"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A leading `-`, or a `-` right after `(`, is a sign: `-(2+3)` is −5. It works like `0 − …`.
        - Nested parentheses, possibly deep.
        - Division truncates toward zero, including negative results from inside parentheses.
        """
    ],
    "think": [
        EXPR,
        """
        **Parentheses as fresh levels.** Inside a pair of parentheses, the expression is evaluated exactly like a whole
        expression (signed terms). So on `(`, **save** the current level's terms and pending operator on a stack of frames
        and start a new level. On `)`, the new level's value (the sum of its terms) becomes a plain number for the outer
        level, which is restored from the stack.

        **The sign.** A `-` at the start of a level arrives with no number read yet, so it applies to `num = 0`: the term
        `0` is pushed and the next term is negated. That's exactly `0 − (…)`.
        """,
        f"**Trace on `{pe}`:**",
        table(["character", "action", "open levels"], *crows),
        f"Result **{sum(terms)}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Recursive descent: `expression` reads terms separated by `+`/`−` (with an optional leading sign), `term` reads factors separated by `*`/`/`, and `factor` reads a number or a parenthesised expression."],
            "build": ["Strip spaces.", "Three mutually recursive functions, one per precedence level.", "Parentheses recurse into `expression`."],
            "complexity": ["**Time O(n).** **Space O(depth)** for recursion: deep nesting can hit recursion limits."],
            "limits": ["Recursion depth equals the nesting depth, which can be huge. An explicit stack of frames handles any depth."],
        },
        1: {
            "idea": [
                """
                One pass with a stack of frames. Each level keeps signed terms and its pending operator. `(` pushes the
                current level and starts a new one; `)` closes the level, turning its sum into the current number of the
                restored outer level. A sentinel at the end flushes the last term.
                """
            ],
            "build": ["Frames stack, current terms and operator.", "`(` saves and resets.", "Operators apply the pending one.", "`)` sums the level and restores the outer one."],
            "complexity": ["**Time O(n).** **Space O(n)** for the frames and terms."],
        },
    },
    "takeaways": [
        """
        - **Full calculator:** signed terms per level, plus a stack of saved levels for parentheses.
        - A unary minus is `0 − …`, which falls out of the term logic.
        - **Pitfall:** applying the pending operator after `)` before restoring the outer level.
        """
    ],
}


# ---------------------------------------------------------------- rewrite-in-postfix
fx = "a+b*(c^d-e)^f"
prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
out, ops, srows = [], [], []
for c in fx:
    if c == "(":
        ops.append(c)
        act = "push '('"
    elif c == ")":
        moved = []
        while ops[-1] != "(":
            moved.append(ops.pop())
        ops.pop()
        out += moved
        act = f"pop {moved} to the output until '('"
    elif c in prec:
        moved = []
        while ops and ops[-1] != "(" and (prec[ops[-1]] > prec[c] or (prec[ops[-1]] == prec[c] and c != "^")):
            moved.append(ops.pop())
        out += moved
        ops.append(c)
        act = (f"pop {moved} (they bind at least as tightly), then push '{c}'" if moved else f"push '{c}'")
    else:
        out.append(c)
        act = "letter → output"
    srows.append((c, act, "".join(out), "".join(ops)))
out += reversed(ops)
EXTRA["rewrite-in-postfix"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `^` groups from the right: `a^b^c` is `a^(b^c)`, so its postfix is `abc^^`.
        - `+ − * /` group from the left: `a-b-c` → `ab-c-`.
        - Parentheses override precedence.
        """
    ],
    "think": [
        EXPR,
        """
        **Shunting-yard.** Letters go straight to the output, in their original order. Operators wait on a stack until
        both of their operands are complete. When a new operator arrives, every waiting operator that binds **at least as
        tightly** (higher precedence, or equal precedence and left-grouping) must be applied first, so it moves to the
        output. For right-grouping `^`, an equal-precedence `^` waits instead. `(` blocks popping; `)` pops back to its
        `(`.
        """,
        f"**Trace on `{fx}`:**",
        table(["char", "action", "output so far", "operator stack"], *srows),
        f"Flush the stack at the end: **`{''.join(out)}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["Precedence climbing: parse an operand, then while the next operator binds at least as tightly as allowed, parse its right side with a higher minimum precedence (the same minimum for right-grouping `^`) and emit the operator after it."],
            "build": ["Precedence table.", "`atom`: a letter or a parenthesised expression.", "`parse(min_prec)` loops over operators and recurses for the right side."],
            "complexity": ["**Time O(n).** **Space O(depth)** for recursion."],
            "limits": ["Recursion depth grows with nesting and chains of `^`. Shunting-yard does the same with an explicit stack."],
        },
        1: {
            "idea": [
                """
                Letters go to the output. On an operator, pop operators that bind at least as tightly (respecting
                right-grouping for `^`), then push it. `(` is pushed; `)` pops to the matching `(`. At the end, pop
                everything.
                """
            ],
            "build": ["Precedence table.", "Output list and operator stack.", "Handle letters, operators, `(` and `)`.", "Flush the stack."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Infix → postfix:** shunting-yard with precedence and associativity rules.
        - Right-associative operators don't pop equal-precedence ones.
        - **Pitfall:** treating `^` as left-associative.
        """
    ],
}
