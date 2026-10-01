A weather station logs hourly temperatures in `temps`. A display shows the readings of the last `k` hours at a time, and moves one hour forward each step.

Return the **highest** reading shown at every step, from the first full window to the last.

{{examples}}

**Constraints**
- `1 ≤ k ≤ temps.length ≤ 10⁵`
- `-10⁴ ≤ temps[i] ≤ 10⁴`
