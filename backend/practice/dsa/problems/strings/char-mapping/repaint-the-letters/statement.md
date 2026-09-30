A sign is a row of tiles, each painted one of `m` colours. The colours are written as the first `m` lowercase letters, so the sign is a string. In one step you choose two colours `x` and `y` and repaint **every** tile that currently has colour `x` with colour `y`.

Given the current sign `s` and the target sign `t` of the same length, return `true` if `s` can be turned into `t` with any number of steps (possibly none).

{{examples}}

**Constraints**
- `1 ≤ m ≤ 26`
- `1 ≤ s.length = t.length ≤ 10⁵`
- `s` and `t` use only the first `m` lowercase English letters.
