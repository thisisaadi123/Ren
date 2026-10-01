A café is open for `n` minutes. During minute `i`, `customers[i]` people are served. The owner is moody during minute `i` when `moody[i] = 1`, and then everyone served in that minute leaves unhappy. When `moody[i] = 0`, they leave happy.

Once a day, the owner can stay calm for `minutes` consecutive minutes, so nobody served in that stretch leaves unhappy.

Return the largest number of customers who can leave happy.

{{examples}}

**Constraints**
- `1 ≤ minutes ≤ n ≤ 10⁵`, where `n` is the length of both `customers` and `moody`.
- `0 ≤ customers[i] ≤ 1000`
- `moody[i]` is `0` or `1`.
