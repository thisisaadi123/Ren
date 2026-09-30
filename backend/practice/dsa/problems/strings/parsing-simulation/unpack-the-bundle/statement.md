A sender packs a list of strings into one `bundle`. For each string, in order, it writes the string's length in decimal (with no leading zeros), then a `#`, then the string itself. The strings may contain any printable character, including `#` and digits, and may be empty.

For example, the list `["a#1", "", "hi"]` is packed as `3#a#10#2#hi`. Given the `bundle`, return the original list of strings, in order.

{{examples}}

**Constraints**
- `0 ≤ bundle.length ≤ 10⁵`
- `bundle` has printable ASCII characters (codes 32 to 126).
- `bundle` is a correct packing of some list of strings.
