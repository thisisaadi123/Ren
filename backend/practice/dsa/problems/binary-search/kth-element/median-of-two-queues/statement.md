Two ticket queues report their customers' waiting times as sorted lists `a` and `b`. Return the median of all the waiting times together.

The median is the middle value of the combined sorted list, or the average of the two middle values when the total count is even.

Aim for O(log(m + n)) time.

{{examples}}

**Constraints**
- `0 ≤ a.length, b.length ≤ 10⁵`, and `a.length + b.length ≥ 1`
- `-10⁶ ≤ a[i], b[i] ≤ 10⁶`
- Both lists are sorted in non-decreasing order.
