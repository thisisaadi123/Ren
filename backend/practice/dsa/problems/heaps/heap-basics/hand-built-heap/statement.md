Build a min-heap without a library heap.

- `TaskHeap(items)` starts with every value in `items`.
- `push(x)` adds `x`.
- `pop()` removes and returns the smallest value, or `-1` if the heap is empty.
- `peek()` returns the smallest value without removing it, or `-1` if empty.
- `size()` returns how many values are stored.

{{examples}}

**Constraints**
- `0 ≤ items.length ≤ 10⁵`, `0 ≤ items[i], x ≤ 10⁹`
- At most `10⁵` calls after the constructor.
