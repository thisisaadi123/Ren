A canteen has two kinds of lunch tray, `0` (vegetarian) and `1` (regular). Students wait in a queue, and `prefers[i]` is what student `i` wants. The trays sit in a stack; `trays[0]` is on top.

Each turn, the student at the front looks at the top tray. If it's what they want, they take it and leave. Otherwise they go to the back of the queue. This continues until no one in the queue wants the top tray.

Return how many students are left without lunch.

{{examples}}

**Constraints**
- `1 ≤ prefers.length == trays.length ≤ 10⁵`
- `prefers[i]` and `trays[i]` are `0` or `1`.
