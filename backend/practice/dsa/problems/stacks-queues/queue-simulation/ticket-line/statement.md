People queue for concert tickets, and person `i` wants `wants[i]` tickets. Each second, the person at the front buys **one** ticket. If they still want more, they go to the back of the line; otherwise they leave.

Return how many seconds pass until person `k` (counting from `0` at the front) has bought all their tickets.

{{examples}}

**Constraints**
- `1 ≤ wants.length ≤ 10⁵`
- `1 ≤ wants[i] ≤ 10⁵`
- `0 ≤ k < wants.length`
