A trading screen shows how strong today's price is. The **streak** of a day is the number of consecutive days ending with that day (counting it) whose price was **at most** that day's price.

Implement `PriceStreak`:
- `PriceStreak()` starts with no days recorded.
- `record(price)` adds the next day's price and returns that day's streak.

{{examples}}

**Constraints**
- `1 ≤ price ≤ 10⁹`
- At most `10⁵` calls to `record`.
