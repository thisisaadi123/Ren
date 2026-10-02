Two tram lines are linked lists, `headA` and `headB`. At some stop they may merge into one shared track: from that stop on, both lists use the **same nodes**.

Return the first stop the two lines share, or `null` if they never meet.

In the tests, the second list is written as `{"values": [...], "join_at": i}` when its own stops are followed by stop `i` of the first list (counting from 0), and as a plain list when the lines never meet. Every stop has a different number.

{{examples}}

**Constraints**
- Each line has between `1` and `3 × 10⁴` stops of its own (the second line may have `0` of its own if it starts on the first line).
- `1 ≤ stop number ≤ 10⁵`, all different.
- The lists have no cycles.
