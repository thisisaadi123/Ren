A shop wants its `items` shown in the order of its `guide` list. Items whose value appears in `guide` come first, in the same order as `guide` (repeats stay together). Items **not** in `guide` come after them, in increasing order.

Return the items in that order.

{{examples}}

**Constraints**
- `1 ≤ items.length, guide.length ≤ 10⁵`
- `0 ≤ items[i], guide[i] ≤ 10⁹`
- The values in `guide` are distinct.
