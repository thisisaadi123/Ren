A music app logs the genre id of every song played. Given the log `plays` and a number `k`, return the `k` genres that were played the most.

Order the answer by play count, highest first. If two genres were played the same number of times, the smaller genre id comes first.

{{examples}}

**Constraints**
- `1 ≤ plays.length ≤ 10⁵`
- `-10⁴ ≤ plays[i] ≤ 10⁴`
- `1 ≤ k ≤` the number of different genres in `plays`
