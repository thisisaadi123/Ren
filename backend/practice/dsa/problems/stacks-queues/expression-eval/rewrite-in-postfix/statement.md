A compiler wants formulas in postfix order, where each operator comes right after its two operands. Rewrite the formula `expr` in postfix.

Operands are single lowercase letters. The operators, from loosest to tightest binding, are `+` and `-`, then `*` and `/`, then `^`. `+ - * /` group from the left (`a-b-c` is `(a-b)-c`), while `^` groups from the right (`a^b^c` is `a^(b^c)`). Parentheses override all of this and never appear in the output.

Return the postfix string, with no spaces.

{{examples}}

**Constraints**
- `1 ≤ expr.length ≤ 10⁵`
- `expr` contains only lowercase English letters and the characters `+-*/^()`.
- `expr` is a valid formula: operators always sit between two operands, and parentheses are balanced and never empty.
