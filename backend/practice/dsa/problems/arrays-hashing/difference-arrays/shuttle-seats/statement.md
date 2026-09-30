A shuttle drives along a straight road, stopping at kilometre marks `0, 1, 2, …`, and never turns back. It has `capacity` seats.

Each trip `[passengers, from, to]` means a party of `passengers` gets on at mark `from` and gets off at mark `to`. People get off before new people get on at the same mark.

Return `true` if the shuttle can carry every trip without ever going over capacity.

{{examples}}

**Constraints**
- `1 ≤ trips.length ≤ 10⁵`
- `1 ≤ passengers ≤ 100`
- `0 ≤ from < to ≤ 10⁵`
- `1 ≤ capacity ≤ 10⁷`
