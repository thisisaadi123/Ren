People stand in a line, all facing the back of the line (toward larger indexes), and `heights[i]` is the height of person `i`. Person `i` can see person `j > i` when everyone standing **strictly between** them is shorter than both of them. Heights may repeat.

Return, for every person, how many people they can see.

{{examples}}

**Constraints**
- `1 ≤ heights.length ≤ 10⁵`
- `1 ≤ heights[i] ≤ 10⁹`
