A queue of customers is stored as a linked list from `head` (the front of the queue). The customer standing `k`-th from the **back** gives up and leaves.

Remove that node (the last node is `1`st from the back) and return the head of the queue. Try to do it in a single pass.

{{examples}}

**Constraints**
- The list has `n` nodes, `1 ≤ n ≤ 10⁵`.
- `1 ≤ k ≤ n`
- `-10⁶ ≤ node value ≤ 10⁶`
