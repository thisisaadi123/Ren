Build the brain of a pocket calculator. `expr` is a line of non-negative integers, the operators `+ - * /`, parentheses and spaces. Evaluate it with the usual rules: parentheses first, then `*` and `/`, then `+` and `-`, each left to right. Division truncates toward zero.

A `-` may also act as a sign, but only at the very start of `expr` or right after a `(`, as in `-(2+3)` or `(-4)*5`. It negates the term that follows, so `-2*3` is `-6`.

Return the value of `expr`.

{{examples}}

**Constraints**
- `1 ≤ expr.length ≤ 10⁵`
- `expr` contains only digits, spaces, `+ - * /` and parentheses, and it is a valid expression: parentheses are balanced and never empty, every operator sits between two operands (apart from the sign `-` described above), and no space splits a number.
- There is no division by zero.
- Every number, every intermediate result and the answer fit in a signed 32-bit integer.
