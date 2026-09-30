A store records `sales[i]` for each day `i`. Managers ask many questions of the form "what were total sales from day `l` to day `r`, inclusive?"

For each query `[l, r]`, return the total. Answer the queries in order.

{{examples}}

**Constraints**
- `1 ≤ sales.length ≤ 10⁵`
- `-10⁹ ≤ sales[i] ≤ 10⁹`
- `1 ≤ queries.length ≤ 10⁵`
- `0 ≤ l ≤ r < sales.length`
