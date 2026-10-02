Build a first-in, first-out **queue** using only stack operations: push to the top, look at the top, pop from the top, size and is-empty.

Implement `TwoStackQueue`:
- `TwoStackQueue()` starts empty.
- `push(x)` adds `x` to the back of the queue.
- `pop()` removes the item at the front and returns it.
- `peek()` returns the item at the front without removing it.
- `empty()` returns `true` if the queue is empty.

`pop` and `peek` are only called when the queue isn't empty.

{{examples}}

**Constraints**
- `1 ≤ x ≤ 10⁹`
- At most `10⁵` calls in total.
