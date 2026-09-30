A cross-section of rocky ground is drawn as columns of width 1, where `walls[i]` is the height of column `i`. Rain fills every dip until water would spill over a lower side; water runs off both ends.

Water that sits over neighbouring columns forms one **pool**, and a column that holds no water separates pools. Return the volume of the largest pool (in unit squares), or `0` if no water stays.

{{examples}}

**Constraints**
- `1 ≤ walls.length ≤ 10⁵`
- `0 ≤ walls[i] ≤ 10⁹`
