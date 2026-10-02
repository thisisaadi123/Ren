Build a last-in, first-out **stack** using one queue and only queue operations: add to the back, look at or remove the front, size and is-empty.

Implement `QueueStack`:
- `QueueStack()` starts empty.
- `push(x)` puts `x` on top of the stack.
- `pop()` removes the top item and returns it.
- `top()` returns the top item without removing it.
- `empty()` returns `true` if the stack is empty.

`pop` and `top` are only called when the stack isn't empty.

{{examples}}

**Constraints**
- `1 ≤ x ≤ 10⁹`
- At most `3000` calls in total.
