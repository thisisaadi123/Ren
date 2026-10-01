A server's uptime log `status` has a `1` for every minute it was online and a `0` for every minute it was down. An engineer can patch **at most `k`** of the down minutes, turning them into online minutes.

Return the length of the longest run of consecutive online minutes that can be produced.

{{examples}}

**Constraints**
- `1 ≤ status.length ≤ 10⁵`
- `status[i]` is `0` or `1`.
- `0 ≤ k ≤ status.length`
