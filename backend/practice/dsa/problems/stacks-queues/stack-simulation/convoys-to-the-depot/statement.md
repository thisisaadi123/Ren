Trucks drive along a one-lane road toward a depot at mile `depot`. Truck `i` starts at mile `position[i]` and drives at `speed[i]` miles per hour. A truck can never pass the truck ahead of it: if it catches up, even exactly at the depot, it slows down and the two drive on together as one **convoy**.

Return how many convoys arrive at the depot.

{{examples}}

**Constraints**
- `1 ≤ position.length == speed.length ≤ 10⁵`
- `1 ≤ depot ≤ 10⁶`
- `0 ≤ position[i] < depot`, all distinct.
- `1 ≤ speed[i] ≤ 10⁶`
