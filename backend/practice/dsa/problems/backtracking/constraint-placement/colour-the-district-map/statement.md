A city is split into `n` districts numbered `0` to `n - 1`. Each entry `[a, b]` of `borders` says districts `a` and `b` share a border. A mapmaker has `m` ink colours and wants to colour every district so that no two bordering districts get the same colour.

Return `true` if that is possible, otherwise `false`. Not every colour has to be used.

{{examples}}

**Constraints**
- `1 ≤ n ≤ 10`
- `0 ≤ borders.length ≤ n × (n − 1) / 2`
- `borders[i] = [a, b]` with `0 ≤ a, b < n` and `a ≠ b`
- No border is listed twice (in either direction).
- `1 ≤ m ≤ 4`
