Two people list their free time as `a` and `b`: closed intervals `[start, end]`, each list sorted and non-overlapping. Return every slot where **both** are free, sorted by start. A slot may be a single point, like `[5, 5]`.

{{examples}}

**Constraints**
- `0 ≤ a.length, b.length ≤ 10⁵`
- `0 ≤ start ≤ end ≤ 10⁹`; within each list, every slot ends before the next starts.
