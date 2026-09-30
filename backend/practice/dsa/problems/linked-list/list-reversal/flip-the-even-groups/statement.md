Seats in a lecture hall are listed as a linked list from `head`. They are split into consecutive groups from the front: the first group has `1` node, the next `2`, then `3`, and so on. The last group takes whatever is left, so it may be smaller than planned.

Reverse the order of the nodes inside every group whose **actual** number of nodes is even; leave the other groups as they are. Return the head of the list.

{{examples}}

**Constraints**
- The list has between `1` and `10⁵` nodes.
- `0 ≤ node value ≤ 10⁵`
