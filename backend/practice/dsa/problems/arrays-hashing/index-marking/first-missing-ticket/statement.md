A ticket machine should hand out ticket numbers `1, 2, 3, …`. `nums` lists what it actually printed today, in no order, including junk values (zero, negative or huge numbers).

Return the smallest positive integer that does **not** appear in `nums`.

Your solution must run in O(n) time and use O(1) extra space.

{{examples}}

**Constraints**
- `1 ≤ nums.length ≤ 10⁵`
- `-2³¹ ≤ nums[i] ≤ 2³¹ - 1`
