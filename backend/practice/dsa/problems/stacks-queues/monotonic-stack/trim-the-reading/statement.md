A meter shows the reading `num`, a string of digits. You must erase **exactly** `k` digits; the remaining digits keep their order and close up. Leading zeros in what's left are dropped.

Return the smallest reading you can get, as a string. If every digit is erased or only zeros remain, return `"0"`.

{{examples}}

**Constraints**
- `1 ≤ k ≤ num.length ≤ 10⁵`
- `num` contains only digits and has no leading zeros, unless it is `"0"` itself.
