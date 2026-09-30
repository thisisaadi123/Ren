A supermarket closes all but one checkout. Each of the `k` open queues is a linked list of ticket numbers in non-decreasing order, and `queues[i]` is the head of queue `i` (a queue may be empty).

Merge all the queues into a single linked list in non-decreasing order and return its head. Relink the existing nodes rather than creating new ones.

{{examples}}

**Constraints**
- `0 ≤ k = queues.length ≤ 10⁴`
- Each queue is in non-decreasing order.
- The total number of nodes across all queues is at most `10⁵`.
- `-10⁴ ≤ node value ≤ 10⁴`
