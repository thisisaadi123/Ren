Numbered tiles are arranged in a circle; `ring[i]` is the number on tile `i`, and after the last tile comes tile `0` again. Starting from each tile and walking clockwise (increasing index, wrapping around), find the first tile whose number is **strictly bigger**.

Return that number for every tile, or `-1` if no tile on the ring is bigger.

{{examples}}

**Constraints**
- `1 ≤ ring.length ≤ 10⁵`
- `-10⁹ ≤ ring[i] ≤ 10⁹`
