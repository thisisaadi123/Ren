You are inviting some of your cousins, whose ages are in `ages` (several cousins can share an age). Two cousins whose ages differ by **exactly** `k` years always argue, so they must never both be invited.

A guest list is any non-empty set of cousins with no such pair. Cousins are different people even when they share an age, so lists that differ in who is invited count separately. Return how many guest lists there are.

{{examples}}

**Constraints**
- `1 ≤ ages.length ≤ 18`
- `1 ≤ ages[i] ≤ 1000`
- `1 ≤ k ≤ 1000`
