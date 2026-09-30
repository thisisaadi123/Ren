A desk calculator reads a whole line such as `3+5 * 2 - 8/3` and evaluates it with the usual rules: `*` and `/` before `+` and `-`, and otherwise left to right. Division truncates toward zero.

`expr` holds non-negative integers and the operators `+ - * /`, possibly with spaces between them. There are no parentheses and no negative signs in front of numbers. Return the value of `expr`.

{{examples}}

**Constraints**
- `1 ≤ expr.length ≤ 10⁵`
- `expr` contains only digits, spaces and `+ - * /`, and is a valid expression: numbers and operators alternate, starting and ending with a number, and no space splits a number.
- There is no division by zero.
- Every number, every intermediate result and the answer fit in a signed 32-bit integer.
