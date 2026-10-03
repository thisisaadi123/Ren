"""Stacks & Queues: evaluating expressions."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def tdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


@problem
def postfix_calculator():
    tokens = ["6", "2", "-", "-9", "4", "/", "*", "5", "+"]

    def ev(ts):
        st = []
        for t in ts:
            if t in "+-*/" and len(t) == 1:
                b, a = st.pop(), st.pop()
                st.append(a + b if t == "+" else a - b if t == "-" else a * b if t == "*" else tdiv(a, b))
            else:
                st.append(int(t))
        return st[0]

    want = ev(tokens)

    w1 = Steps("Find the first operator, combine the two values just before it, put the result in their place; repeat.")
    t = list(tokens)
    w1.step(f"Start: {' '.join(t)}", Row(t))
    while len(t) > 1:
        i = next(k for k, x in enumerate(t) if x in ("+", "-", "*", "/"))
        a, b = int(t[i - 2]), int(t[i - 1])
        r = a + b if t[i] == "+" else a - b if t[i] == "-" else a * b if t[i] == "*" else tdiv(a, b)
        w1.step(f"'{t[i - 2]} {t[i - 1]} {t[i]}' → {r}.", Row(t, st={i - 2: "mark", i - 1: "mark", i: "active"}))
        t = t[:i - 2] + [str(r)] + t[i + 1:]
    w1.step(f"One value left: {t[0]}.", Row(t), result=t[0])

    w2 = Steps("Numbers go on a stack. An operator pops the top two (right operand first), combines them, and pushes the result.")
    st = []
    for i, tok in enumerate(tokens):
        if tok in ("+", "-", "*", "/"):
            b, a = st.pop(), st.pop()
            r = a + b if tok == "+" else a - b if tok == "-" else a * b if tok == "*" else tdiv(a, b)
            st.append(r)
            note = f"'{tok}': pop {b} and {a}, push {a} {tok} {b} = {r}."
        else:
            st.append(int(tok))
            note = f"{tok}: push."
        w2.step(note, Row(tokens, st={i: "active"}), Row(list(st), label="stack"))
    w2.steps[-1]["result"] = str(st[0])

    sol(
        "postfix-calculator",
        summary="""
            In postfix, every operator applies to the two most recent values that haven't been used yet: exactly the top
            two items of a stack. Push numbers; on an operator, pop the right operand, then the left, combine, push the
            result. One pass, O(n).
        """,
        question=[
            """
            Evaluate a postfix expression given as tokens: integers and `+ - * /`, each operator after its two operands.

            - **Operand order matters** for `-` and `/`: `9 3 -` is 9 − 3.
            - **Division truncates toward zero:** −7 / 2 is −3 (not −4). Python's `//` floors, so it needs care there.
            - **Negative numbers** like `-7` are tokens of their own, not operators.
            - **No parentheses or precedence:** postfix order already encodes the grouping.
            """
        ],
        think=[
            f"""
            Take `{' '.join(tokens)}`. Read left to right: 6, 2, then `-` combines the two most recent values: 6 − 2 = 4.
            Then −9, 4, and `/`: −9 / 4 = −2 (truncated). Then `*` combines 4 and −2: −8. Then 5 and `+`: −3.
            """,
            fig(Row(tokens), caption=f"Value: {want}."),
            """
            "The two most recent unused values" is a stack: values are pushed as they appear, and each operator consumes
            the top two and leaves its result on top for later operators.
            """,
        ],
        approaches=[
            approach(
                "Reduce the first operator repeatedly",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["The first operator in the list always applies to the two tokens right before it. Replace those three tokens with the result and repeat until one value remains."],
                walk=w1,
                build=["Copy the tokens into a list.", "Find the first operator at index i; combine `list[i − 2]` and `list[i − 1]`.", "Replace the three tokens with the result; repeat."],
                code={
                    "python": """
                        class Solution:
                            def evalPostfix(self, tokens: List[str]) -> int:
                                t = list(tokens)  #@copy
                                while len(t) > 1:  #@loop
                                    i = next(k for k, x in enumerate(t) if x in ("+", "-", "*", "/"))  #@find
                                    a, b, op = int(t[i - 2]), int(t[i - 1]), t[i]  #@apply
                                    if op == "+": r = a + b  #@apply
                                    elif op == "-": r = a - b  #@apply
                                    elif op == "*": r = a * b  #@apply
                                    else: r = abs(a) // abs(b) * (1 if (a < 0) == (b < 0) else -1)  #@apply
                                    t[i - 2:i + 1] = [str(r)]  #@splice
                                return int(t[0])  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int evalPostfix(String[] tokens) {
                                List<String> t = new ArrayList<>(Arrays.asList(tokens));  //@copy
                                while (t.size() > 1) {  //@loop
                                    int i = 0;  //@find
                                    while (!"+-*/".contains(t.get(i)) || t.get(i).length() != 1) i++;  //@find
                                    int a = Integer.parseInt(t.get(i - 2)), b = Integer.parseInt(t.get(i - 1));  //@apply
                                    String op = t.get(i);  //@apply
                                    int r = op.equals("+") ? a + b : op.equals("-") ? a - b : op.equals("*") ? a * b : a / b;  //@apply
                                    t.subList(i - 2, i + 1).clear();  //@splice
                                    t.add(i - 2, String.valueOf(r));  //@splice
                                }
                                return Integer.parseInt(t.get(0));  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int evalPostfix(vector<string>& tokens) {
                                vector<string> t = tokens;  //@copy
                                auto isOp = [](const string& x) { return x.size() == 1 && string("+-*/").find(x[0]) != string::npos; };  //@find
                                while (t.size() > 1) {  //@loop
                                    size_t i = 0;  //@find
                                    while (!isOp(t[i])) i++;  //@find
                                    int a = stoi(t[i - 2]), b = stoi(t[i - 1]);  //@apply
                                    char op = t[i][0];  //@apply
                                    int r = op == '+' ? a + b : op == '-' ? a - b : op == '*' ? a * b : a / b;  //@apply
                                    t.erase(t.begin() + i - 2, t.begin() + i + 1);  //@splice
                                    t.insert(t.begin() + i - 2, to_string(r));  //@splice
                                }
                                return stoi(t[0]);  //@ret
                            }
                        };
                    """,
                    "c": """
                        static bool isOp(const char* x) {  //@find
                            return x[1] == '\\0' && (x[0] == '+' || x[0] == '-' || x[0] == '*' || x[0] == '/');  //@find
                        }  //@find

                        int evalPostfix(char** tokens, int tokensSize) {
                            int n = tokensSize;
                            int* val = malloc(n * sizeof(int));  //@copy
                            char* op = malloc(n);  //@copy
                            for (int i = 0; i < n; i++) {  //@copy
                                op[i] = isOp(tokens[i]) ? tokens[i][0] : 0;  //@copy
                                val[i] = op[i] ? 0 : atoi(tokens[i]);  //@copy
                            }  //@copy
                            while (n > 1) {  //@loop
                                int i = 0;  //@find
                                while (!op[i]) i++;  //@find
                                int a = val[i - 2], b = val[i - 1];  //@apply
                                int r = op[i] == '+' ? a + b : op[i] == '-' ? a - b : op[i] == '*' ? a * b : a / b;  //@apply
                                val[i - 2] = r;  //@splice
                                op[i - 2] = 0;  //@splice
                                memmove(val + i - 1, val + i + 1, (n - i - 1) * sizeof(int));  //@splice
                                memmove(op + i - 1, op + i + 1, n - i - 1);  //@splice
                                n -= 2;  //@splice
                            }
                            int answer = val[0];  //@ret
                            free(val);  //@ret
                            free(op);  //@ret
                            return answer;  //@ret
                        }
                    """,
                },
                lines=[("copy", "A working copy of the token list.", {"c": "Parse once into parallel arrays: the operator character (0 for numbers) and the number value."}), ("loop", "Until a single value remains."), ("find", "The first operator; the two tokens before it are its operands (they must be numbers, since it's the first operator)."), ("apply", "Combine them; division truncates toward zero.", {"python": "Python's `//` rounds down, so divide the absolute values and fix the sign.", "java": "Java's integer division already truncates toward zero.", "cpp": "C++ integer division already truncates toward zero.", "c": "C integer division already truncates toward zero."}), ("splice", "Replace the three tokens with the single result, shifting the rest left."), ("ret", "The final value.")],
                complexity=["**Time O(n²):** each reduction searches and shifts the list. **Space O(n).**"],
                limits=["Re-scans from the start and shifts the list for every operator. A stack keeps the pending values exactly where the next operator needs them."],
                slow=True,
            ),
            approach(
                "Stack of values",
                "best",
                "O(n)",
                "O(n)",
                idea=["Push numbers. For an operator: `b = pop()`, `a = pop()`, push `a op b`. The single value left is the answer."],
                walk=w2,
                build=["Empty stack.", "Number → push; operator → pop right, pop left, push the combination.", "Return the remaining value."],
                code={
                    "python": """
                        class Solution:
                            def evalPostfix(self, tokens: List[str]) -> int:
                                stack = []  #@stack
                                for t in tokens:  #@loop
                                    if t in ("+", "-", "*", "/"):  #@op
                                        b, a = stack.pop(), stack.pop()  #@op
                                        if t == "+": stack.append(a + b)  #@apply
                                        elif t == "-": stack.append(a - b)  #@apply
                                        elif t == "*": stack.append(a * b)  #@apply
                                        else: stack.append(abs(a) // abs(b) * (1 if (a < 0) == (b < 0) else -1))  #@apply
                                    else:  #@num
                                        stack.append(int(t))  #@num
                                return stack[0]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int evalPostfix(String[] tokens) {
                                int[] stack = new int[tokens.length];  //@stack
                                int top = 0;  //@stack
                                for (String t : tokens) {  //@loop
                                    if (t.length() == 1 && "+-*/".indexOf(t.charAt(0)) >= 0) {  //@op
                                        int b = stack[--top], a = stack[--top];  //@op
                                        switch (t.charAt(0)) {  //@apply
                                            case '+': stack[top++] = a + b; break;  //@apply
                                            case '-': stack[top++] = a - b; break;  //@apply
                                            case '*': stack[top++] = a * b; break;  //@apply
                                            default: stack[top++] = a / b;  //@apply
                                        }  //@apply
                                    } else {  //@num
                                        stack[top++] = Integer.parseInt(t);  //@num
                                    }
                                }
                                return stack[0];  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int evalPostfix(vector<string>& tokens) {
                                vector<int> stack;  //@stack
                                for (const string& t : tokens) {  //@loop
                                    if (t.size() == 1 && string("+-*/").find(t[0]) != string::npos) {  //@op
                                        int b = stack.back(); stack.pop_back();  //@op
                                        int a = stack.back(); stack.pop_back();  //@op
                                        switch (t[0]) {  //@apply
                                            case '+': stack.push_back(a + b); break;  //@apply
                                            case '-': stack.push_back(a - b); break;  //@apply
                                            case '*': stack.push_back(a * b); break;  //@apply
                                            default: stack.push_back(a / b);  //@apply
                                        }  //@apply
                                    } else {  //@num
                                        stack.push_back(stoi(t));  //@num
                                    }
                                }
                                return stack[0];  //@ret
                            }
                        };
                    """,
                    "c": """
                        int evalPostfix(char** tokens, int tokensSize) {
                            int* stack = malloc(tokensSize * sizeof(int));  //@stack
                            int top = 0;  //@stack
                            for (int i = 0; i < tokensSize; i++) {  //@loop
                                char* t = tokens[i];  //@loop
                                if (t[1] == '\\0' && (t[0] == '+' || t[0] == '-' || t[0] == '*' || t[0] == '/')) {  //@op
                                    int b = stack[--top], a = stack[--top];  //@op
                                    switch (t[0]) {  //@apply
                                        case '+': stack[top++] = a + b; break;  //@apply
                                        case '-': stack[top++] = a - b; break;  //@apply
                                        case '*': stack[top++] = a * b; break;  //@apply
                                        default: stack[top++] = a / b;  //@apply
                                    }  //@apply
                                } else {  //@num
                                    stack[top++] = atoi(t);  //@num
                                }
                            }
                            int answer = stack[0];  //@ret
                            free(stack);  //@ret
                            return answer;  //@ret
                        }
                    """,
                },
                lines=[("stack", "Values waiting for an operator.", {"java": "An array with a `top` index works as a stack (n values at most).", "c": "An array with a `top` index works as a stack (n values at most)."}), ("loop", "One pass over the tokens."), ("op", "A one-character token that is an operator (a token like `-7` is a number). Pop the right operand first, then the left."), ("apply", "Combine and push the result back.", {"python": "Python's `//` floors, so divide absolute values and restore the sign to truncate toward zero.", "java": "Integer division truncates toward zero, as required.", "cpp": "Integer division truncates toward zero, as required.", "c": "Integer division truncates toward zero, as required."}), ("num", "A number waits on the stack."), ("ret", "A valid expression leaves exactly one value.")],
                complexity=["**Time O(n).** **Space O(n)** for the stack."],
            ),
        ],
        takeaways=[
            """
            - **Postfix evaluation = stack:** numbers push; operators pop two (right first) and push one.
            - Mind truncation toward zero when your language's division floors (Python).
            """
        ],
    )


@problem
def desk_calculator():
    expr = "14 - 3*4/5 + 2*3"

    def calc(e):
        st, num, op = [], 0, "+"
        for c in e + "+":
            if c == " ":
                continue
            if c.isdigit():
                num = num * 10 + int(c)
                continue
            if op == "+":
                st.append(num)
            elif op == "-":
                st.append(-num)
            elif op == "*":
                st[-1] *= num
            else:
                st[-1] = tdiv(st[-1], num)
            op, num = c, 0
        return sum(st)

    want = calc(expr)

    import re
    toks = re.findall(r"\d+|[+\-*/]", expr)
    w1 = Steps("Tokenise. First collapse every * and / (leftmost first), then every + and -.")
    t = list(toks)
    w1.step(f"Tokens: {' '.join(t)}", Row(t))
    for ops in ("*/", "+-"):
        while any(x in ops for x in t if len(x) == 1):
            i = next(k for k, x in enumerate(t) if x in ops and len(x) == 1)
            a, b = int(t[i - 1]), int(t[i + 1])
            r = a * b if t[i] == "*" else tdiv(a, b) if t[i] == "/" else a + b if t[i] == "+" else a - b
            w1.step(f"'{t[i - 1]} {t[i]} {t[i + 1]}' → {r}.", Row(t, st={i - 1: "mark", i: "active", i + 1: "mark"}))
            t = t[:i - 1] + [str(r)] + t[i + 2:]
    w1.step(f"Result {t[0]}.", Row(t), result=t[0])

    w2 = Steps("Stack of terms to be added. '+' pushes the next number, '−' pushes its negative, '*' and '/' combine with the top term.")
    st, num, op = [], 0, "+"
    for c in expr + "+":
        if c == " ":
            continue
        if c.isdigit():
            num = num * 10 + int(c)
            continue
        if op == "+":
            st.append(num)
            note = f"{num} after '+': push {num}."
        elif op == "-":
            st.append(-num)
            note = f"{num} after '−': push −{num}."
        elif op == "*":
            st[-1] *= num
            note = f"{num} after '*': top becomes {st[-1]}."
        else:
            st[-1] = tdiv(st[-1], num)
            note = f"{num} after '/': top becomes {st[-1]}."
        w2.step(note, Row(list(st), label="terms"))
        op, num = c, 0
    w2.step(f"Add the terms: {' + '.join(map(str, st))} = {sum(st)}.", Row(st, label="terms"), result=sum(st))

    w3 = Steps("Only the last term can still change, so keep it in a variable; everything before it is already final in a running total.")
    total, last, num, op = 0, 0, 0, "+"
    for c in expr + "+":
        if c == " ":
            continue
        if c.isdigit():
            num = num * 10 + int(c)
            continue
        if op in "+-":
            total += last
            last = num if op == "+" else -num
            note = f"{num} starts a new term ({last}); bank the previous one: total {total}."
        elif op == "*":
            last *= num
            note = f"{num} multiplies the current term: {last}."
        else:
            last = tdiv(last, num)
            note = f"{num} divides the current term: {last}."
        w3.step(note, Vars(total=total, term=last))
        op, num = c, 0
    w3.step(f"Bank the last term: {total} + {last} = {total + last}.", Vars(answer=total + last), result=total + last)

    sol(
        "desk-calculator",
        summary="""
            Without parentheses, the expression is a sum of **terms**, where each term is a run of numbers joined by `*`
            and `/`. Read left to right: `+`/`−` start a new term, `*`/`/` modify the current one. Keep a running total of
            finished terms plus the current term: O(n) time, O(1) space.
        """,
        question=[
            """
            Evaluate an expression of non-negative integers with `+ - * /` and spaces: `*` and `/` before `+` and `-`, left to
            right otherwise. Division truncates toward zero.

            - **No parentheses, no leading minus.**
            - **Spaces can appear anywhere between tokens**, never inside a number.
            - **Truncation toward zero:** 1 − 7 / 2 = 1 − 3 = −2. Since only non-negative numbers are divided directly, but
              terms can be negative (`−8/3`), the truncation rule matters.
            - **Everything fits in 32 bits.**
            """
        ],
        think=[
            f"""
            Take `{expr}`. Group it into terms: `14`, `−3*4/5`, `+2*3`. Evaluate each: 14, −(12/5) = −2, 6. Sum: {want}.
            """,
            fig(Row(["14", "−3*4/5", "+2*3"], label="terms"), Row(["14", "−2", "6"], label="values"), caption=f"Sum: {want}."),
            """
            While reading, only the **current term** can still change (a following `*` or `/` modifies it); any earlier
            term is final as soon as a `+` or `−` arrives. So keep the finished terms (a stack, or just their running sum)
            plus the current term. Treat the sign as part of the term: `−3*4/5` is the term −3, then ×4, then /5,
            truncated toward zero.
            """,
        ],
        approaches=[
            approach(
                "Tokenise and reduce by precedence",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Split into numbers and operators. Repeatedly replace the leftmost `*` or `/` with its result; then repeatedly replace the leftmost `+` or `-`. Each replacement rebuilds the token list."],
                walk=w1,
                build=["Tokenise (skip spaces, read whole numbers).", "Pass 1: reduce `*` and `/` from the left.", "Pass 2: reduce `+` and `-` from the left.", "Return the last token."],
                code={
                    "python": """
                        class Solution:
                            def calculate(self, expr: str) -> int:
                                toks, num = [], None  #@tokens
                                for c in expr:  #@tokens
                                    if c.isdigit():  #@tokens
                                        num = (num or 0) * 10 + int(c)  #@tokens
                                    elif c != " ":  #@tokens
                                        toks += [num, c]  #@tokens
                                        num = None  #@tokens
                                toks.append(num)  #@tokens
                                for ops in ("*/", "+-"):  #@levels
                                    i = 1  #@reduce
                                    while i < len(toks):  #@reduce
                                        if toks[i] in ops:  #@reduce
                                            a, op, b = toks[i - 1], toks[i], toks[i + 1]  #@reduce
                                            if op == "*": r = a * b  #@reduce
                                            elif op == "/": r = abs(a) // b * (1 if a >= 0 else -1)  #@reduce
                                            elif op == "+": r = a + b  #@reduce
                                            else: r = a - b  #@reduce
                                            toks[i - 1:i + 2] = [r]  #@reduce
                                        else:  #@reduce
                                            i += 2  #@reduce
                                return toks[0]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int calculate(String expr) {
                                List<Object> toks = new ArrayList<>();  //@tokens
                                int num = 0;  //@tokens
                                for (char c : expr.toCharArray()) {  //@tokens
                                    if (Character.isDigit(c)) num = num * 10 + (c - '0');  //@tokens
                                    else if (c != ' ') { toks.add(num); toks.add(c); num = 0; }  //@tokens
                                }  //@tokens
                                toks.add(num);  //@tokens
                                for (String ops : new String[] {"*/", "+-"}) {  //@levels
                                    int i = 1;  //@reduce
                                    while (i < toks.size()) {  //@reduce
                                        char op = (Character) toks.get(i);  //@reduce
                                        if (ops.indexOf(op) < 0) { i += 2; continue; }  //@reduce
                                        int a = (Integer) toks.get(i - 1), b = (Integer) toks.get(i + 1);  //@reduce
                                        int r = op == '*' ? a * b : op == '/' ? a / b : op == '+' ? a + b : a - b;  //@reduce
                                        toks.subList(i - 1, i + 2).clear();  //@reduce
                                        toks.add(i - 1, r);  //@reduce
                                    }  //@reduce
                                }
                                return (Integer) toks.get(0);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int calculate(string& expr) {
                                vector<int> nums;  //@tokens
                                vector<char> ops;  //@tokens
                                int num = 0;  //@tokens
                                for (char c : expr) {  //@tokens
                                    if (isdigit(c)) num = num * 10 + (c - '0');  //@tokens
                                    else if (c != ' ') { nums.push_back(num); ops.push_back(c); num = 0; }  //@tokens
                                }  //@tokens
                                nums.push_back(num);  //@tokens
                                for (string level : {"*/", "+-"}) {  //@levels
                                    size_t i = 0;  //@reduce
                                    while (i < ops.size()) {  //@reduce
                                        char op = ops[i];  //@reduce
                                        if (level.find(op) == string::npos) { i++; continue; }  //@reduce
                                        int a = nums[i], b = nums[i + 1];  //@reduce
                                        nums[i] = op == '*' ? a * b : op == '/' ? a / b : op == '+' ? a + b : a - b;  //@reduce
                                        nums.erase(nums.begin() + i + 1);  //@reduce
                                        ops.erase(ops.begin() + i);  //@reduce
                                    }  //@reduce
                                }
                                return nums[0];  //@ret
                            }
                        };
                    """,
                    "c": """
                        int calculate(char* expr) {
                            int n = strlen(expr), cnt = 0, num = 0;
                            int* nums = malloc((n + 1) * sizeof(int));  //@tokens
                            char* ops = malloc(n + 1);  //@tokens
                            for (int i = 0; i < n; i++) {  //@tokens
                                char c = expr[i];  //@tokens
                                if (c >= '0' && c <= '9') num = num * 10 + (c - '0');  //@tokens
                                else if (c != ' ') { nums[cnt] = num; ops[cnt++] = c; num = 0; }  //@tokens
                            }  //@tokens
                            nums[cnt] = num;  //@tokens
                            const char* levels[] = {"*/", "+-"};  //@levels
                            for (int lv = 0; lv < 2; lv++) {  //@levels
                                int i = 0;  //@reduce
                                while (i < cnt) {  //@reduce
                                    char op = ops[i];  //@reduce
                                    if (!strchr(levels[lv], op)) { i++; continue; }  //@reduce
                                    int a = nums[i], b = nums[i + 1];  //@reduce
                                    nums[i] = op == '*' ? a * b : op == '/' ? a / b : op == '+' ? a + b : a - b;  //@reduce
                                    memmove(nums + i + 1, nums + i + 2, (cnt - i - 1) * sizeof(int));  //@reduce
                                    memmove(ops + i, ops + i + 1, cnt - i - 1);  //@reduce
                                    cnt--;  //@reduce
                                }  //@reduce
                            }
                            int answer = nums[0];  //@ret
                            free(nums);  //@ret
                            free(ops);  //@ret
                            return answer;  //@ret
                        }
                    """,
                },
                lines=[("tokens", "Numbers and operators in order, spaces skipped, multi-digit numbers assembled."), ("levels", "Higher precedence first: all `*` and `/`, then all `+` and `-`."), ("reduce", "Replace `a op b` (leftmost first) with its value and shift the rest of the list left. Division truncates toward zero.", {"python": "Python's `//` floors; with `a` possibly negative after earlier steps, divide the absolute value and restore the sign."}), ("ret", "One number remains.")],
                complexity=["**Time O(n²):** each reduction shifts the list. **Space O(n).**"],
                limits=["Shifting lists after every operator costs O(n) each time. The expression's shape (a sum of products) can be evaluated in a single left-to-right pass."],
                slow=True,
            ),
            approach(
                "Stack of signed terms",
                "better",
                "O(n)",
                "O(n)",
                idea=["Remember the operator before the current number. When the number ends: after `+` push it; after `−` push its negative; after `*` or `/` combine it with the top of the stack. The answer is the sum of the stack."],
                walk=w2,
                build=["`op = '+'`, `num = 0`, empty stack.", "Read digits into num; at each operator (and at the end), apply the previous op to num, then remember the new op.", "Return the stack's sum."],
                code={
                    "python": """
                        class Solution:
                            def calculate(self, expr: str) -> int:
                                stack, num, op = [], 0, "+"  #@init
                                for c in expr + "+":  #@loop
                                    if c == " ":  #@loop
                                        continue  #@loop
                                    if c.isdigit():  #@digit
                                        num = num * 10 + int(c)  #@digit
                                        continue  #@digit
                                    if op == "+":  #@apply
                                        stack.append(num)  #@apply
                                    elif op == "-":  #@apply
                                        stack.append(-num)  #@apply
                                    elif op == "*":  #@apply
                                        stack[-1] *= num  #@apply
                                    else:  #@apply
                                        q = abs(stack[-1]) // num  #@apply
                                        stack[-1] = q if stack[-1] >= 0 else -q  #@apply
                                    op, num = c, 0  #@next
                                return sum(stack)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int calculate(String expr) {
                                Deque<Integer> stack = new ArrayDeque<>();  //@init
                                int num = 0;  //@init
                                char op = '+';  //@init
                                for (int i = 0; i <= expr.length(); i++) {  //@loop
                                    char c = i < expr.length() ? expr.charAt(i) : '+';  //@loop
                                    if (c == ' ') continue;  //@loop
                                    if (Character.isDigit(c)) { num = num * 10 + (c - '0'); continue; }  //@digit
                                    if (op == '+') stack.push(num);  //@apply
                                    else if (op == '-') stack.push(-num);  //@apply
                                    else if (op == '*') stack.push(stack.pop() * num);  //@apply
                                    else stack.push(stack.pop() / num);  //@apply
                                    op = c;  //@next
                                    num = 0;  //@next
                                }
                                int sum = 0;  //@ret
                                for (int v : stack) sum += v;  //@ret
                                return sum;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int calculate(string& expr) {
                                vector<int> stack;  //@init
                                int num = 0;  //@init
                                char op = '+';  //@init
                                for (size_t i = 0; i <= expr.size(); i++) {  //@loop
                                    char c = i < expr.size() ? expr[i] : '+';  //@loop
                                    if (c == ' ') continue;  //@loop
                                    if (isdigit(c)) { num = num * 10 + (c - '0'); continue; }  //@digit
                                    if (op == '+') stack.push_back(num);  //@apply
                                    else if (op == '-') stack.push_back(-num);  //@apply
                                    else if (op == '*') stack.back() *= num;  //@apply
                                    else stack.back() /= num;  //@apply
                                    op = c;  //@next
                                    num = 0;  //@next
                                }
                                return accumulate(stack.begin(), stack.end(), 0);  //@ret
                            }
                        };
                    """,
                    "c": """
                        int calculate(char* expr) {
                            int n = strlen(expr), top = 0, num = 0;
                            int* stack = malloc((n + 1) * sizeof(int));  //@init
                            char op = '+';  //@init
                            for (int i = 0; i <= n; i++) {  //@loop
                                char c = i < n ? expr[i] : '+';  //@loop
                                if (c == ' ') continue;  //@loop
                                if (c >= '0' && c <= '9') { num = num * 10 + (c - '0'); continue; }  //@digit
                                if (op == '+') stack[top++] = num;  //@apply
                                else if (op == '-') stack[top++] = -num;  //@apply
                                else if (op == '*') stack[top - 1] *= num;  //@apply
                                else stack[top - 1] /= num;  //@apply
                                op = c;  //@next
                                num = 0;  //@next
                            }
                            int sum = 0;  //@ret
                            for (int i = 0; i < top; i++) sum += stack[i];  //@ret
                            free(stack);  //@ret
                            return sum;  //@ret
                        }
                    """,
                },
                lines=[("init", "The operator before the first number is effectively `+`."), ("loop", "Read characters, with a sentinel `+` at the end so the last number is applied too; spaces are skipped."), ("digit", "Build multi-digit numbers."), ("apply", "The number just finished is applied with the operator *before* it: `+`/`−` start a new signed term; `*`/`/` change the latest term. Integer division truncates toward zero.", {"python": "Python's `//` floors, so the sign is handled separately."}), ("next", "Remember this operator for the next number."), ("ret", "Add up the terms.")],
                complexity=["**Time O(n).** **Space O(n)** for the terms."],
                limits=["Terms below the top of the stack never change again, so storing them is unnecessary: a running sum holds them just as well."],
            ),
            approach(
                "Running total and current term",
                "best",
                "O(n)",
                "O(1)",
                idea=["Keep `total` (sum of finished terms) and `last` (the current term). When a number ends: after `+`/`−`, add `last` to total and start a new term `±num`; after `*`/`/`, update `last`. At the end, return `total + last`."],
                walk=w3,
                build=["`total = last = 0`, `op = '+'`.", "At each operator (and the end sentinel), apply the previous op to the finished number.", "Return `total + last`."],
                code={
                    "python": """
                        class Solution:
                            def calculate(self, expr: str) -> int:
                                total = last = num = 0  #@init
                                op = "+"  #@init
                                for c in expr + "+":  #@loop
                                    if c == " ":  #@loop
                                        continue  #@loop
                                    if c.isdigit():  #@digit
                                        num = num * 10 + int(c)  #@digit
                                        continue  #@digit
                                    if op in "+-":  #@term
                                        total += last  #@term
                                        last = num if op == "+" else -num  #@term
                                    elif op == "*":  #@modify
                                        last *= num  #@modify
                                    else:  #@modify
                                        q = abs(last) // num  #@modify
                                        last = q if last >= 0 else -q  #@modify
                                    op, num = c, 0  #@next
                                return total + last  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int calculate(String expr) {
                                int total = 0, last = 0, num = 0;  //@init
                                char op = '+';  //@init
                                for (int i = 0; i <= expr.length(); i++) {  //@loop
                                    char c = i < expr.length() ? expr.charAt(i) : '+';  //@loop
                                    if (c == ' ') continue;  //@loop
                                    if (Character.isDigit(c)) { num = num * 10 + (c - '0'); continue; }  //@digit
                                    if (op == '+' || op == '-') {  //@term
                                        total += last;  //@term
                                        last = op == '+' ? num : -num;  //@term
                                    } else if (op == '*') last *= num;  //@modify
                                    else last /= num;  //@modify
                                    op = c;  //@next
                                    num = 0;  //@next
                                }
                                return total + last;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int calculate(string& expr) {
                                int total = 0, last = 0, num = 0;  //@init
                                char op = '+';  //@init
                                for (size_t i = 0; i <= expr.size(); i++) {  //@loop
                                    char c = i < expr.size() ? expr[i] : '+';  //@loop
                                    if (c == ' ') continue;  //@loop
                                    if (isdigit(c)) { num = num * 10 + (c - '0'); continue; }  //@digit
                                    if (op == '+' || op == '-') {  //@term
                                        total += last;  //@term
                                        last = op == '+' ? num : -num;  //@term
                                    } else if (op == '*') last *= num;  //@modify
                                    else last /= num;  //@modify
                                    op = c;  //@next
                                    num = 0;  //@next
                                }
                                return total + last;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int calculate(char* expr) {
                            int n = strlen(expr), total = 0, last = 0, num = 0;  //@init
                            char op = '+';  //@init
                            for (int i = 0; i <= n; i++) {  //@loop
                                char c = i < n ? expr[i] : '+';  //@loop
                                if (c == ' ') continue;  //@loop
                                if (c >= '0' && c <= '9') { num = num * 10 + (c - '0'); continue; }  //@digit
                                if (op == '+' || op == '-') {  //@term
                                    total += last;  //@term
                                    last = op == '+' ? num : -num;  //@term
                                } else if (op == '*') last *= num;  //@modify
                                else last /= num;  //@modify
                                op = c;  //@next
                                num = 0;  //@next
                            }
                            return total + last;  //@ret
                        }
                    """,
                },
                lines=[("init", "No finished terms, an empty current term, and an implicit leading `+`."), ("loop", "Characters plus an end sentinel `+`; spaces skipped."), ("digit", "Build the number."), ("term", "`+`/`−` before this number: the previous term is final, bank it; this number starts a new signed term."), ("modify", "`*`/`/` before this number: it continues the current term. Truncation toward zero comes free in Java, C++ and C; Python needs the sign handled separately."), ("next", "Remember the operator for the next number."), ("ret", "Bank the last term.")],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Precedence without parentheses: the expression is a **sum of products**. `+`/`−` close a term; `*`/`/` extend it.
            - Apply each number with the operator **before** it, and add a sentinel at the end to flush the last number.
            - Only the current term can still change, so a running total replaces the stack.
            """
        ],
    )


@problem
def pocket_calculator():
    expr = "-(6-2*4)/2 + 3*(1+2)"

    def ev(e):
        frames = []
        st, op, num = [], "+", 0
        for c in e + "#":
            if c == " ":
                continue
            if c.isdigit():
                num = num * 10 + int(c)
                continue
            if c == "(":
                frames.append((st, op))
                st, op, num = [], "+", 0
                continue
            if op == "+":
                st.append(num)
            elif op == "-":
                st.append(-num)
            elif op == "*":
                st[-1] *= num
            else:
                st[-1] = tdiv(st[-1], num)
            if c == ")":
                num = sum(st)
                st, op = frames.pop()
            else:
                op, num = c, 0
        return sum(st)

    want = ev(expr)

    w1 = Steps("Recursive descent: expression = terms joined by + and −; term = factors joined by * and /; factor = number or (expression).")
    w1.step(f"'{expr}': a leading '−' negates the first term, (6−2*4)/2.", Vars(expression=expr))
    w1.step("Factor (6−2*4): recurse into the parentheses: 6 − 8 = −2. Then / 2 → −1. Negated: 1.", Vars(first_term=1))
    w1.step("Next term 3*(1+2): recurse: 1+2 = 3; 3 × 3 = 9.", Vars(second_term=9))
    w1.step(f"Sum of terms: 1 + 9 = {want}.", Vars(value=want), result=want)

    w2 = Steps("Desk-calculator loop plus a stack of frames: '(' saves the current terms and pending operator; ')' sums the inner terms into a number and restores the outer frame.")
    frames = []
    st, op, num = [], "+", 0
    for c in expr + "#":
        if c == " ":
            continue
        if c.isdigit():
            num = num * 10 + int(c)
            continue
        if c == "(":
            frames.append((st, op))
            w2.step(f"'(': save terms {st} and pending '{op}'; start a fresh frame.", Row([f"{s}|{o}" for s, o in frames], label="saved frames (terms|op)"), Row(["·"], label="current terms"))
            st, op, num = [], "+", 0
            continue
        if op == "+":
            st.append(num)
        elif op == "-":
            st.append(-num)
        elif op == "*":
            st[-1] *= num
        else:
            st[-1] = tdiv(st[-1], num)
        if c == ")":
            inner = sum(st)
            st, op = frames.pop()
            num = inner
            w2.step(f"')': the inner frame sums to {inner}; it becomes the number for the outer pending '{op}'.", Row([f"{s}|{o}" for s, o in frames] or ["·"], label="saved frames"), Row(list(st) or ["·"], label="current terms"), Vars(number=inner))
        else:
            w2.step(f"'{c}': apply '{op}' to the last number → terms {st}; pending operator is now '{c}'." if c != "#" else f"End: apply '{op}' → terms {st}.", Row([f"{s}|{o}" for s, o in frames] or ["·"], label="saved frames"), Row(list(st), label="current terms"))
            op, num = c, 0
    w2.step(f"Sum of the top-level terms: {sum(st)}.", Row(st, label="terms"), result=sum(st))

    sol(
        "pocket-calculator",
        summary="""
            Handle one level of the expression like the desk calculator (a running list of signed terms, with `*` and `/`
            modifying the last term). A `(` starts a new level: save the current terms and pending operator on a stack of
            frames. A `)` sums the inner level into a single number and hands it back to the saved operator. One pass, O(n).
        """,
        question=[
            """
            Evaluate an expression with non-negative integers, `+ - * /`, parentheses and spaces. Parentheses first, then
            `*` `/`, then `+` `−`, each left to right; division truncates toward zero.

            - **A unary `−` may appear only at the start or right after `(`**, and negates the term after it: `−2*3 = −6`,
              `(−4)*5 = −20`.
            - **Parenthesised results can be negative**, so `/` may divide a negative number: truncate toward zero
              (`−7/2 = −3`).
            - **Up to 10⁵ characters**, with possibly deep nesting.
            """
        ],
        think=[
            f"""
            Take `{expr}`. Inside the first parentheses: 6 − 2×4 = −2. Divide by 2: −1. The leading `−` negates that term: 1.
            The second term is 3 × (1 + 2) = 9. Total: {want}.
            """,
            fig(Row(list(expr.replace(" ", "")), slots=True), caption="Each parenthesised part is evaluated on its own and becomes a single number."),
            """
            Without parentheses this is the desk calculator: a sum of signed terms. Parentheses just mean "evaluate this
            sub-expression first and use its value as a number". So when a `(` arrives, pause the current level (its terms
            and the operator waiting for the next number) and start a fresh one; when the matching `)` arrives, the fresh
            level's sum is the number the paused operator was waiting for. Pausing and resuming in nested order is a stack.

            The unary minus fits in for free: at the start of a level, the pending operator is `+` with number 0, so a `−`
            there pushes 0 and makes the next term negative.
            """,
        ],
        approaches=[
            approach(
                "Recursive descent",
                "better",
                "O(n)",
                "O(depth)",
                idea=[
                    """
                    Write one function per precedence level, each reading from a shared position:

                    - `expr()`: an optional leading `−`, then a term, then any number of `+ term` / `− term`.
                    - `term()`: a factor, then any number of `* factor` / `/ factor`.
                    - `factor()`: a number, or `(` `expr()` `)`.

                    Each function returns the value of what it read. Nesting in the input becomes nesting of calls.
                    """
                ],
                walk=w1,
                build=["Remove spaces (or skip them as you read).", "Implement `expr`, `term`, `factor` with a shared index.", "`expr` handles the leading unary minus by negating its first term.", "Return `expr()` on the whole input."],
                code={
                    "python": """
                        import sys

                        class Solution:
                            def evaluate(self, expr: str) -> int:
                                sys.setrecursionlimit(100000)
                                s = expr.replace(" ", "")  #@clean
                                i = 0  #@clean
                                def expression():  #@expr
                                    nonlocal i  #@expr
                                    sign = 1  #@expr
                                    if i < len(s) and s[i] == "-":  #@expr
                                        sign, i = -1, i + 1  #@expr
                                    total = sign * term()  #@expr
                                    while i < len(s) and s[i] in "+-":  #@expr
                                        op = s[i]  #@expr
                                        i += 1  #@expr
                                        total = total + term() if op == "+" else total - term()  #@expr
                                    return total  #@expr
                                def term():  #@term
                                    nonlocal i  #@term
                                    value = factor()  #@term
                                    while i < len(s) and s[i] in "*/":  #@term
                                        op = s[i]  #@term
                                        i += 1  #@term
                                        rhs = factor()  #@term
                                        if op == "*":  #@term
                                            value *= rhs  #@term
                                        else:  #@term
                                            q = abs(value) // abs(rhs)  #@term
                                            value = q if (value < 0) == (rhs < 0) else -q  #@term
                                    return value  #@term
                                def factor():  #@factor
                                    nonlocal i  #@factor
                                    if s[i] == "(":  #@factor
                                        i += 1  #@factor
                                        value = expression()  #@factor
                                        i += 1  #@factor
                                        return value  #@factor
                                    value = 0  #@factor
                                    while i < len(s) and s[i].isdigit():  #@factor
                                        value = value * 10 + int(s[i])  #@factor
                                        i += 1  #@factor
                                    return value  #@factor
                                return expression()  #@ret
                    """,
                    "java": """
                        class Solution {
                            private String s;
                            private int i;

                            public int evaluate(String expr) {
                                s = expr.replace(" ", "");  //@clean
                                i = 0;  //@clean
                                return expression();  //@ret
                            }

                            private int expression() {  //@expr
                                int sign = 1;  //@expr
                                if (i < s.length() && s.charAt(i) == '-') { sign = -1; i++; }  //@expr
                                int total = sign * term();  //@expr
                                while (i < s.length() && (s.charAt(i) == '+' || s.charAt(i) == '-')) {  //@expr
                                    char op = s.charAt(i++);  //@expr
                                    total = op == '+' ? total + term() : total - term();  //@expr
                                }  //@expr
                                return total;  //@expr
                            }  //@expr

                            private int term() {  //@term
                                int value = factor();  //@term
                                while (i < s.length() && (s.charAt(i) == '*' || s.charAt(i) == '/')) {  //@term
                                    char op = s.charAt(i++);  //@term
                                    int rhs = factor();  //@term
                                    value = op == '*' ? value * rhs : value / rhs;  //@term
                                }  //@term
                                return value;  //@term
                            }  //@term

                            private int factor() {  //@factor
                                if (s.charAt(i) == '(') {  //@factor
                                    i++;  //@factor
                                    int value = expression();  //@factor
                                    i++;  //@factor
                                    return value;  //@factor
                                }  //@factor
                                int value = 0;  //@factor
                                while (i < s.length() && Character.isDigit(s.charAt(i))) value = value * 10 + (s.charAt(i++) - '0');  //@factor
                                return value;  //@factor
                            }  //@factor
                        }
                    """,
                    "cpp": """
                        class Solution {
                            string s;
                            size_t i = 0;

                            int expression() {  //@expr
                                int sign = 1;  //@expr
                                if (i < s.size() && s[i] == '-') { sign = -1; i++; }  //@expr
                                int total = sign * term();  //@expr
                                while (i < s.size() && (s[i] == '+' || s[i] == '-')) {  //@expr
                                    char op = s[i++];  //@expr
                                    total = op == '+' ? total + term() : total - term();  //@expr
                                }  //@expr
                                return total;  //@expr
                            }  //@expr

                            int term() {  //@term
                                int value = factor();  //@term
                                while (i < s.size() && (s[i] == '*' || s[i] == '/')) {  //@term
                                    char op = s[i++];  //@term
                                    int rhs = factor();  //@term
                                    value = op == '*' ? value * rhs : value / rhs;  //@term
                                }  //@term
                                return value;  //@term
                            }  //@term

                            int factor() {  //@factor
                                if (s[i] == '(') {  //@factor
                                    i++;  //@factor
                                    int value = expression();  //@factor
                                    i++;  //@factor
                                    return value;  //@factor
                                }  //@factor
                                int value = 0;  //@factor
                                while (i < s.size() && isdigit(s[i])) value = value * 10 + (s[i++] - '0');  //@factor
                                return value;  //@factor
                            }  //@factor

                        public:
                            int evaluate(string& expr) {
                                for (char c : expr) if (c != ' ') s += c;  //@clean
                                i = 0;  //@clean
                                return expression();  //@ret
                            }
                        };
                    """,
                    "c": """
                        static const char* src;
                        static int pos;
                        static int expression(void);

                        static void skip(void) { while (src[pos] == ' ') pos++; }  //@clean

                        static int factor(void) {  //@factor
                            skip();  //@factor
                            if (src[pos] == '(') {  //@factor
                                pos++;  //@factor
                                int value = expression();  //@factor
                                skip();  //@factor
                                pos++;  //@factor
                                return value;  //@factor
                            }  //@factor
                            int value = 0;  //@factor
                            while (src[pos] >= '0' && src[pos] <= '9') value = value * 10 + (src[pos++] - '0');  //@factor
                            return value;  //@factor
                        }  //@factor

                        static int term(void) {  //@term
                            int value = factor();  //@term
                            for (skip(); src[pos] == '*' || src[pos] == '/'; skip()) {  //@term
                                char op = src[pos++];  //@term
                                int rhs = factor();  //@term
                                value = op == '*' ? value * rhs : value / rhs;  //@term
                            }  //@term
                            return value;  //@term
                        }  //@term

                        static int expression(void) {  //@expr
                            skip();  //@expr
                            int sign = 1;  //@expr
                            if (src[pos] == '-') { sign = -1; pos++; }  //@expr
                            int total = sign * term();  //@expr
                            for (skip(); src[pos] == '+' || src[pos] == '-'; skip()) {  //@expr
                                char op = src[pos++];  //@expr
                                total = op == '+' ? total + term() : total - term();  //@expr
                            }  //@expr
                            return total;  //@expr
                        }  //@expr

                        int evaluate(char* expr) {
                            src = expr;  //@clean
                            pos = 0;  //@clean
                            return expression();  //@ret
                        }
                    """,
                },
                lines=[("clean", "Spaces carry no meaning; drop or skip them.", {"c": "`skip()` steps over spaces before every token."}), ("expr", "A sum of terms. A leading `−` negates the first term (that's the only place a sign can appear in a level)."), ("term", "A product of factors, left to right; division truncates toward zero.", {"python": "Python's `//` floors, so the sign is handled separately."}), ("factor", "A number, or a parenthesised expression evaluated recursively."), ("ret", "Evaluate the whole input.")],
                complexity=["**Time O(n).** **Space O(depth)** on the call stack."],
                limits=["Correct and elegant, but each level of parentheses adds call frames. With ~5 × 10⁴ nested parentheses, the call stack overflows in most languages (Python's default limit is 1000). An explicit stack of frames does the same work on the heap."],
                slow=True,
            ),
            approach(
                "One pass with a stack of frames",
                "best",
                "O(n)",
                "O(n)",
                idea=["Run the desk-calculator loop (terms list, pending `op`, current `num`). On `(`, push `(terms, op)` and start a fresh frame. On `)`, first apply the pending op to num, then set `num = sum(terms)` and pop the saved frame; the restored `op` will apply this num when the next operator (or `)`/end) arrives."],
                walk=w2,
                build=["Process characters plus an end sentinel; skip spaces; build numbers.", "`(` → push frame, reset.", "Any operator, `)` or end → apply the pending op to num.", "`)` → num = sum of the frame's terms; restore the outer frame. Otherwise remember the new operator.", "Return the sum of the outermost terms."],
                code={
                    "python": """
                        class Solution:
                            def evaluate(self, expr: str) -> int:
                                frames = []  #@init
                                terms, op, num = [], "+", 0  #@init
                                for c in expr + "#":  #@loop
                                    if c == " ":  #@loop
                                        continue  #@loop
                                    if c.isdigit():  #@digit
                                        num = num * 10 + int(c)  #@digit
                                        continue  #@digit
                                    if c == "(":  #@open
                                        frames.append((terms, op))  #@open
                                        terms, op, num = [], "+", 0  #@open
                                        continue  #@open
                                    if op == "+":  #@apply
                                        terms.append(num)  #@apply
                                    elif op == "-":  #@apply
                                        terms.append(-num)  #@apply
                                    elif op == "*":  #@apply
                                        terms[-1] *= num  #@apply
                                    else:  #@apply
                                        q = abs(terms[-1]) // abs(num)  #@apply
                                        terms[-1] = q if (terms[-1] < 0) == (num < 0) else -q  #@apply
                                    if c == ")":  #@close
                                        num = sum(terms)  #@close
                                        terms, op = frames.pop()  #@close
                                    else:  #@next
                                        op, num = c, 0  #@next
                                return sum(terms)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int evaluate(String expr) {
                                int n = expr.length();
                                int[] terms = new int[n + 1];  //@init
                                int[] frameStart = new int[n + 1];  //@init
                                char[] frameOp = new char[n + 1];  //@init
                                int top = 0, frames = 0, num = 0, start = 0;  //@init
                                char op = '+';  //@init
                                for (int i = 0; i <= n; i++) {  //@loop
                                    char c = i < n ? expr.charAt(i) : '#';  //@loop
                                    if (c == ' ') continue;  //@loop
                                    if (Character.isDigit(c)) { num = num * 10 + (c - '0'); continue; }  //@digit
                                    if (c == '(') {  //@open
                                        frameStart[frames] = start;  //@open
                                        frameOp[frames++] = op;  //@open
                                        start = top;  //@open
                                        op = '+';  //@open
                                        num = 0;  //@open
                                        continue;  //@open
                                    }
                                    if (op == '+') terms[top++] = num;  //@apply
                                    else if (op == '-') terms[top++] = -num;  //@apply
                                    else if (op == '*') terms[top - 1] *= num;  //@apply
                                    else terms[top - 1] /= num;  //@apply
                                    if (c == ')') {  //@close
                                        num = 0;  //@close
                                        for (int k = start; k < top; k++) num += terms[k];  //@close
                                        top = start;  //@close
                                        start = frameStart[--frames];  //@close
                                        op = frameOp[frames];  //@close
                                    } else {  //@next
                                        op = c;  //@next
                                        num = 0;  //@next
                                    }
                                }
                                int sum = 0;  //@ret
                                for (int k = 0; k < top; k++) sum += terms[k];  //@ret
                                return sum;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int evaluate(string& expr) {
                                vector<int> terms;  //@init
                                vector<pair<size_t, char>> frames;  //@init
                                size_t start = 0;  //@init
                                int num = 0;  //@init
                                char op = '+';  //@init
                                for (size_t i = 0; i <= expr.size(); i++) {  //@loop
                                    char c = i < expr.size() ? expr[i] : '#';  //@loop
                                    if (c == ' ') continue;  //@loop
                                    if (isdigit(c)) { num = num * 10 + (c - '0'); continue; }  //@digit
                                    if (c == '(') {  //@open
                                        frames.push_back({start, op});  //@open
                                        start = terms.size();  //@open
                                        op = '+';  //@open
                                        num = 0;  //@open
                                        continue;  //@open
                                    }
                                    if (op == '+') terms.push_back(num);  //@apply
                                    else if (op == '-') terms.push_back(-num);  //@apply
                                    else if (op == '*') terms.back() *= num;  //@apply
                                    else terms.back() /= num;  //@apply
                                    if (c == ')') {  //@close
                                        num = accumulate(terms.begin() + start, terms.end(), 0);  //@close
                                        terms.resize(start);  //@close
                                        start = frames.back().first;  //@close
                                        op = frames.back().second;  //@close
                                        frames.pop_back();  //@close
                                    } else {  //@next
                                        op = c;  //@next
                                        num = 0;  //@next
                                    }
                                }
                                return accumulate(terms.begin(), terms.end(), 0);  //@ret
                            }
                        };
                    """,
                    "c": """
                        int evaluate(char* expr) {
                            int n = strlen(expr);
                            int* terms = malloc((n + 1) * sizeof(int));  //@init
                            int* frameStart = malloc((n + 1) * sizeof(int));  //@init
                            char* frameOp = malloc(n + 1);  //@init
                            int top = 0, frames = 0, num = 0, start = 0;  //@init
                            char op = '+';  //@init
                            for (int i = 0; i <= n; i++) {  //@loop
                                char c = i < n ? expr[i] : '#';  //@loop
                                if (c == ' ') continue;  //@loop
                                if (c >= '0' && c <= '9') { num = num * 10 + (c - '0'); continue; }  //@digit
                                if (c == '(') {  //@open
                                    frameStart[frames] = start;  //@open
                                    frameOp[frames++] = op;  //@open
                                    start = top;  //@open
                                    op = '+';  //@open
                                    num = 0;  //@open
                                    continue;  //@open
                                }
                                if (op == '+') terms[top++] = num;  //@apply
                                else if (op == '-') terms[top++] = -num;  //@apply
                                else if (op == '*') terms[top - 1] *= num;  //@apply
                                else terms[top - 1] /= num;  //@apply
                                if (c == ')') {  //@close
                                    num = 0;  //@close
                                    for (int k = start; k < top; k++) num += terms[k];  //@close
                                    top = start;  //@close
                                    start = frameStart[--frames];  //@close
                                    op = frameOp[frames];  //@close
                                } else {  //@next
                                    op = c;  //@next
                                    num = 0;  //@next
                                }
                            }
                            int sum = 0;  //@ret
                            for (int k = 0; k < top; k++) sum += terms[k];  //@ret
                            free(terms);  //@ret
                            free(frameStart);  //@ret
                            free(frameOp);  //@ret
                            return sum;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Saved frames, the current frame's terms, the pending operator and the number being read.", {"java": "All frames share one `terms` array; each frame remembers where its terms start (`frameStart`) and the operator that was pending outside it (`frameOp`).", "cpp": "All frames share one `terms` vector; each saved frame remembers where its terms start and the operator pending outside it.", "c": "All frames share one `terms` array; each frame remembers where its terms start and the operator pending outside it."}),
                    ("loop", "Characters plus an end sentinel `#`; spaces skipped."),
                    ("digit", "Build multi-digit numbers."),
                    ("open", "Pause the current level and start a fresh one with pending `+` and number 0 (which is what makes a unary `−` right after `(` work)."),
                    ("apply", "The number just finished is applied with the pending operator: new signed term for `+`/`−`, or modify the last term for `*`/`/`. A leading unary `−` arrives with num 0: it pushes 0 and makes the next term negative.", {"python": "The divisor can be negative (a parenthesised value), so truncate toward zero with absolute values."}),
                    ("close", "The inner level is complete: its sum becomes the number for the outer pending operator, which is restored along with the outer terms."),
                    ("next", "Remember the operator for the next number."),
                    ("ret", "Sum of the outermost terms."),
                ],
                complexity=["**Time O(n):** each character is handled once and each term is summed once when its level closes. **Space O(n)** for terms and frames."],
            ),
        ],
        takeaways=[
            """
            - Parentheses = **save the current state on a stack, evaluate the inside, resume**.
            - Recursive descent is the textbook parser; an explicit stack is the same thing without call-stack limits.
            - A pending `+` with number 0 at the start of each level makes a unary minus work without special cases.
            """
        ],
    )


@problem
def rewrite_in_postfix():
    expr = "a+b*(c^d-e)^f"
    prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}

    def shunt(e):
        out, ops = [], []
        for c in e:
            if c == "(":
                ops.append(c)
            elif c == ")":
                while ops[-1] != "(":
                    out.append(ops.pop())
                ops.pop()
            elif c in prec:
                while ops and ops[-1] != "(" and (prec[ops[-1]] > prec[c] or (prec[ops[-1]] == prec[c] and c != "^")):
                    out.append(ops.pop())
                ops.append(c)
            else:
                out.append(c)
        while ops:
            out.append(ops.pop())
        return "".join(out)

    want = shunt(expr)

    w1 = Steps("Precedence climbing: parse an operand, then keep absorbing operators that bind at least as tightly as the current minimum.")
    w1.step(f"'{expr}': at the top level, '+' has the lowest precedence, so the expression is a + (everything after it).", Vars(output="a"))
    w1.step("Right of '+': b * X, where X = (c^d−e)^f binds tighter than '*'.", Vars(output="a b"))
    w1.step("Inside the parentheses: c^d is 'cd^', then − e → 'cd^e-'. That group ^ f → 'cd^e-f^'.", Vars(group="cd^e-f^"))
    w1.step(f"Combine: b X * → 'bcd^e-f^*', then a … + → '{want}'.", Vars(output=want), result=want)

    w2 = Steps("Shunting-yard: letters go straight to the output; operators wait on a stack and leave it when a looser (or equal, left-grouping) operator arrives.")
    out, ops = [], []
    for c in expr:
        if c == "(":
            ops.append(c)
            note = "'(' : push."
        elif c == ")":
            moved = []
            while ops[-1] != "(":
                moved.append(ops.pop())
            ops.pop()
            out += moved
            note = f"')': pop {moved or 'nothing'} to the output until '(' ."
        elif c in prec:
            moved = []
            while ops and ops[-1] != "(" and (prec[ops[-1]] > prec[c] or (prec[ops[-1]] == prec[c] and c != "^")):
                moved.append(ops.pop())
            out += moved
            ops.append(c)
            note = f"'{c}': first pop {moved} (they bind at least as tightly), then push '{c}'." if moved else f"'{c}': push."
        else:
            out.append(c)
            note = f"'{c}': operand → output."
        w2.step(note, Row(list(ops) or ["·"], label="operator stack"), Vars(output="".join(out)))
    rest = list(reversed(ops))
    w2.step(f"End: pop the rest {rest}. Output '{want}'.", Vars(output=want), result=want)

    sol(
        "rewrite-in-postfix",
        summary="""
            Shunting-yard: operands go straight to the output; operators wait on a stack until an operator that binds
            more loosely (or equally, for left-grouping ones) arrives, which pushes them to the output first. `(` blocks
            the stack, `)` flushes back to it, and `^` groups from the right, so an equal `^` doesn't flush. O(n).
        """,
        question=[
            """
            Convert an infix formula over single-letter operands to postfix. Precedence: `+ −` < `* /` < `^`. `+ − * /` group
            left to right; `^` groups right to left. Parentheses override everything and don't appear in the output.

            - **Left grouping:** `a−b−c` is `(a−b)−c` → `ab-c-`.
            - **Right grouping:** `a^b^c` is `a^(b^c)` → `abc^^`.
            - **Operand order never changes** in postfix; only operators move.
            """
        ],
        think=[
            f"""
            Take `{expr}`. Letters appear in the output in their original order: a, b, c, d, e, f. The question is only
            **where each operator goes**: right after both of its operands are complete. Here that gives `{want}`.

            Picture reading left to right with operators waiting in line. When `*` arrives after `a+b`, `+` must keep waiting
            (its right operand `b*…` isn't finished). When a `−` arrives after `c^d`, the `^` is complete (it binds tighter),
            so it goes to the output first. Waiting operators leave in last-in-first-out order: a stack.
            """,
            fig(Row(list(expr), slots=True), Row(list(want), label="postfix"), caption="Operands keep their order; operators move to just after their operands."),
            """
            The pop rule when a new operator `o` arrives: pop operators on top that bind **more tightly** than `o`, or **equally**
            when `o` groups left. For `^` (right-grouping), an equal `^` on the stack stays, because the new `^` belongs to the
            right operand of the old one.
            """,
        ],
        approaches=[
            approach(
                "Recursive precedence climbing",
                "better",
                "O(n)",
                "O(depth)",
                idea=["`parse(minPrec)` reads an operand (a letter, or a parenthesised `parse(1)`), then while the next operator's precedence is ≥ `minPrec`: take it, parse its right side with `parse(prec + 1)` for left-grouping operators or `parse(prec)` for `^`, and append `right + op` to the output."],
                walk=w1,
                build=["Shared index into the formula.", "`atom()`: letter, or `(` parse(1) `)`.", "`parse(min)`: atom, then loop over operators with precedence ≥ min, recursing for the right side.", "Return `parse(1)`."],
                code={
                    "python": """
                        import sys

                        class Solution:
                            def toPostfix(self, expr: str) -> str:
                                sys.setrecursionlimit(100000)
                                prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}  #@prec
                                i = 0  #@prec
                                def atom(out):  #@atom
                                    nonlocal i  #@atom
                                    if expr[i] == "(":  #@atom
                                        i += 1  #@atom
                                        parse(1, out)  #@atom
                                        i += 1  #@atom
                                    else:  #@atom
                                        out.append(expr[i])  #@atom
                                        i += 1  #@atom
                                def parse(min_prec, out):  #@parse
                                    nonlocal i  #@parse
                                    atom(out)  #@parse
                                    while i < len(expr) and expr[i] in prec and prec[expr[i]] >= min_prec:  #@loop
                                        op = expr[i]  #@loop
                                        i += 1  #@loop
                                        parse(prec[op] if op == "^" else prec[op] + 1, out)  #@right
                                        out.append(op)  #@right
                                out = []  #@ret
                                parse(1, out)  #@ret
                                return "".join(out)  #@ret
                    """,
                    "java": """
                        class Solution {
                            private String e;
                            private int i;
                            private StringBuilder out;

                            private int prec(char c) {  //@prec
                                return c == '+' || c == '-' ? 1 : c == '*' || c == '/' ? 2 : c == '^' ? 3 : 0;  //@prec
                            }  //@prec

                            public String toPostfix(String expr) {
                                e = expr;  //@ret
                                i = 0;  //@ret
                                out = new StringBuilder();  //@ret
                                parse(1);  //@ret
                                return out.toString();  //@ret
                            }

                            private void atom() {  //@atom
                                if (e.charAt(i) == '(') { i++; parse(1); i++; }  //@atom
                                else out.append(e.charAt(i++));  //@atom
                            }  //@atom

                            private void parse(int minPrec) {  //@parse
                                atom();  //@parse
                                while (i < e.length() && prec(e.charAt(i)) >= minPrec && prec(e.charAt(i)) > 0) {  //@loop
                                    char op = e.charAt(i++);  //@loop
                                    parse(op == '^' ? prec(op) : prec(op) + 1);  //@right
                                    out.append(op);  //@right
                                }
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            string e, out;
                            size_t i = 0;

                            int prec(char c) {  //@prec
                                return c == '+' || c == '-' ? 1 : c == '*' || c == '/' ? 2 : c == '^' ? 3 : 0;  //@prec
                            }  //@prec

                            void atom() {  //@atom
                                if (e[i] == '(') { i++; parse(1); i++; }  //@atom
                                else out += e[i++];  //@atom
                            }  //@atom

                            void parse(int minPrec) {  //@parse
                                atom();  //@parse
                                while (i < e.size() && prec(e[i]) > 0 && prec(e[i]) >= minPrec) {  //@loop
                                    char op = e[i++];  //@loop
                                    parse(op == '^' ? prec(op) : prec(op) + 1);  //@right
                                    out += op;  //@right
                                }
                            }

                        public:
                            string toPostfix(string& expr) {
                                e = expr;  //@ret
                                i = 0;  //@ret
                                out.clear();  //@ret
                                parse(1);  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static const char* e;
                        static int pos, w;
                        static char* out;

                        static int prec(char c) {  //@prec
                            return c == '+' || c == '-' ? 1 : c == '*' || c == '/' ? 2 : c == '^' ? 3 : 0;  //@prec
                        }  //@prec

                        static void parse(int minPrec);

                        static void atom(void) {  //@atom
                            if (e[pos] == '(') { pos++; parse(1); pos++; }  //@atom
                            else out[w++] = e[pos++];  //@atom
                        }  //@atom

                        static void parse(int minPrec) {  //@parse
                            atom();  //@parse
                            while (e[pos] && prec(e[pos]) > 0 && prec(e[pos]) >= minPrec) {  //@loop
                                char op = e[pos++];  //@loop
                                parse(op == '^' ? prec(op) : prec(op) + 1);  //@right
                                out[w++] = op;  //@right
                            }
                        }

                        char* toPostfix(char* expr) {
                            e = expr;  //@ret
                            pos = w = 0;  //@ret
                            out = malloc(strlen(expr) + 1);  //@ret
                            parse(1);  //@ret
                            out[w] = '\\0';  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("prec", "Binding strength of each operator (0 for anything else)."), ("atom", "An operand: a letter goes to the output; a parenthesised part is parsed in full (from the lowest precedence) and its closing `)` skipped."), ("parse", "Parse a sub-expression whose operators all bind at least `minPrec`."), ("loop", "Absorb the next operator if it binds tightly enough; a looser one belongs to an outer call."), ("right", "Parse the right operand: for left-grouping operators, only tighter operators may join it (`prec + 1`); for `^`, equal ones may too (right grouping). Then the operator follows its operands."), ("ret", "Parse everything and return the output.")],
                complexity=["**Time O(n).** **Space O(depth)** call stack, which overflows for very deeply nested input."],
                limits=["Deep nesting (tens of thousands of parentheses or a long `^` chain) means deep recursion and a possible stack overflow. Shunting-yard keeps the pending operators on an explicit stack instead."],
                slow=True,
            ),
            approach(
                "Shunting-yard",
                "best",
                "O(n)",
                "O(n)",
                idea=["Letter → output. `(` → push. `)` → pop to output until `(`, drop the `(`. Operator `o` → while the top is an operator (not `(`) that binds more tightly than `o`, or equally when `o` is left-grouping, pop it to the output; then push `o`. At the end, pop everything."],
                walk=w2,
                build=["Operator stack and output buffer.", "Handle letters, `(`, `)` and operators as described.", "Flush the stack at the end."],
                code={
                    "python": """
                        class Solution:
                            def toPostfix(self, expr: str) -> str:
                                prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}  #@prec
                                out, ops = [], []  #@init
                                for c in expr:  #@loop
                                    if c == "(":  #@open
                                        ops.append(c)  #@open
                                    elif c == ")":  #@close
                                        while ops[-1] != "(":  #@close
                                            out.append(ops.pop())  #@close
                                        ops.pop()  #@close
                                    elif c in prec:  #@op
                                        while ops and ops[-1] != "(" and (prec[ops[-1]] > prec[c] or (prec[ops[-1]] == prec[c] and c != "^")):  #@op
                                            out.append(ops.pop())  #@op
                                        ops.append(c)  #@op
                                    else:  #@letter
                                        out.append(c)  #@letter
                                while ops:  #@flush
                                    out.append(ops.pop())  #@flush
                                return "".join(out)  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int prec(char c) {  //@prec
                                return c == '+' || c == '-' ? 1 : c == '*' || c == '/' ? 2 : c == '^' ? 3 : 0;  //@prec
                            }  //@prec

                            public String toPostfix(String expr) {
                                StringBuilder out = new StringBuilder();  //@init
                                char[] ops = new char[expr.length()];  //@init
                                int top = 0;  //@init
                                for (char c : expr.toCharArray()) {  //@loop
                                    if (c == '(') ops[top++] = c;  //@open
                                    else if (c == ')') {  //@close
                                        while (ops[top - 1] != '(') out.append(ops[--top]);  //@close
                                        top--;  //@close
                                    } else if (prec(c) > 0) {  //@op
                                        while (top > 0 && ops[top - 1] != '(' && (prec(ops[top - 1]) > prec(c) || (prec(ops[top - 1]) == prec(c) && c != '^'))) out.append(ops[--top]);  //@op
                                        ops[top++] = c;  //@op
                                    } else out.append(c);  //@letter
                                }
                                while (top > 0) out.append(ops[--top]);  //@flush
                                return out.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            int prec(char c) {  //@prec
                                return c == '+' || c == '-' ? 1 : c == '*' || c == '/' ? 2 : c == '^' ? 3 : 0;  //@prec
                            }  //@prec

                        public:
                            string toPostfix(string& expr) {
                                string out, ops;  //@init
                                for (char c : expr) {  //@loop
                                    if (c == '(') ops.push_back(c);  //@open
                                    else if (c == ')') {  //@close
                                        while (ops.back() != '(') { out += ops.back(); ops.pop_back(); }  //@close
                                        ops.pop_back();  //@close
                                    } else if (prec(c) > 0) {  //@op
                                        while (!ops.empty() && ops.back() != '(' && (prec(ops.back()) > prec(c) || (prec(ops.back()) == prec(c) && c != '^'))) { out += ops.back(); ops.pop_back(); }  //@op
                                        ops.push_back(c);  //@op
                                    } else out += c;  //@letter
                                }
                                while (!ops.empty()) { out += ops.back(); ops.pop_back(); }  //@flush
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int prec(char c) {  //@prec
                            return c == '+' || c == '-' ? 1 : c == '*' || c == '/' ? 2 : c == '^' ? 3 : 0;  //@prec
                        }  //@prec

                        char* toPostfix(char* expr) {
                            int n = strlen(expr), w = 0, top = 0;
                            char* out = malloc(n + 1);  //@init
                            char* ops = malloc(n + 1);  //@init
                            for (int i = 0; i < n; i++) {  //@loop
                                char c = expr[i];  //@loop
                                if (c == '(') ops[top++] = c;  //@open
                                else if (c == ')') {  //@close
                                    while (ops[top - 1] != '(') out[w++] = ops[--top];  //@close
                                    top--;  //@close
                                } else if (prec(c) > 0) {  //@op
                                    while (top > 0 && ops[top - 1] != '(' && (prec(ops[top - 1]) > prec(c) || (prec(ops[top - 1]) == prec(c) && c != '^'))) out[w++] = ops[--top];  //@op
                                    ops[top++] = c;  //@op
                                } else out[w++] = c;  //@letter
                            }
                            while (top > 0) out[w++] = ops[--top];  //@flush
                            out[w] = '\\0';  //@ret
                            free(ops);  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("prec", "Binding strength of each operator."), ("init", "Output and a stack of waiting operators."), ("loop", "One pass over the formula."), ("open", "`(` blocks the operators below it until the matching `)`."), ("close", "Everything above the `(` is complete: move it to the output, then discard the `(`."), ("op", "Before `o` waits, every waiting operator that binds more tightly (or equally, if `o` groups left) is complete, so it goes to the output. An equal `^` stays, because `^` groups right."), ("letter", "Operands keep their order and go straight out."), ("flush", "Remaining operators complete in stack order."), ("ret", "The postfix string.")],
                complexity=["**Time O(n):** each operator is pushed and popped once. **Space O(n)** for the stack."],
            ),
        ],
        takeaways=[
            """
            - **Shunting-yard:** operands straight out; operators wait on a stack; pop while the top binds tighter (or
              equal and left-associative); `(` blocks, `)` flushes.
            - Right-associative operators (`^`) don't pop equals.
            - Precedence climbing is the recursive twin of shunting-yard.
            """
        ],
    )
