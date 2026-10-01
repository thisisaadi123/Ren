Comets fly along a line at the same speed. `comets[i]` gives comet `i`'s size (the absolute value) and direction (positive means right, negative means left), in order of position.

When two comets meet, the smaller one breaks apart; if they're the same size, both do. Comets moving the same way never meet.

Return the comets left after every collision, in order of position.

{{examples}}

**Constraints**
- `2 ≤ comets.length ≤ 10⁵`
- `-1000 ≤ comets[i] ≤ 1000`, and `comets[i] ≠ 0`.
