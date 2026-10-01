A choir has four voices, written as the letters `S`, `A`, `T` and `B`, and `s` lists the singers in a row. The length of `s` is a multiple of `4`. The choir is **balanced** when each voice appears exactly `n / 4` times.

You may pick one contiguous piece of `s` (possibly empty) and change every singer in it to any voices you like. Return the length of the shortest piece that makes the choir balanced.

{{examples}}

**Constraints**
- `4 ≤ s.length ≤ 10⁵`, and `s.length` is a multiple of `4`.
- `s` has only the letters `S`, `A`, `T` and `B`.
