A sound card keeps the latest samples in a fixed-size circular buffer. Implement `RingBuffer`:

- `RingBuffer(k)` makes an empty buffer that holds at most `k` items.
- `enqueue(x)` adds `x` at the back. Returns `true`, or `false` if the buffer is full (nothing changes).
- `dequeue()` removes the front item. Returns `true`, or `false` if the buffer is empty.
- `front()` returns the front item, or `-1` if the buffer is empty.
- `rear()` returns the back item, or `-1` if the buffer is empty.
- `isEmpty()` and `isFull()` report the buffer's state.

{{examples}}

**Constraints**
- `1 ≤ k ≤ 1000`
- `0 ≤ x ≤ 1000`
- At most `10⁵` calls in total.
