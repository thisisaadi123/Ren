Every badge at a conference carries a number, written as the digit string `code`. The printer can't make new digits: it can only shuffle the digits of an existing badge.

Return the **smallest** number that is larger than `code` and uses exactly the same digits, each as many times as it appears in `code`. If no larger number can be made, return an empty string `""`.

{{examples}}

**Constraints**
- `1 ≤ code.length ≤ 10⁵`
- `code` contains only the digits `0`–`9` and doesn't start with `0`.
