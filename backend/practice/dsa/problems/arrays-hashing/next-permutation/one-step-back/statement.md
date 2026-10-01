A DJ keeps a set of track ratings and plays them in the order `ratings`. Write out every distinct ordering of these ratings and sort the orderings in dictionary order: compare the first rating, then the second, and so on. Orderings that read the same are written once.

Return the ordering that comes **immediately before** `ratings`. If `ratings` is already the first ordering, return the last one instead.

{{examples}}

**Constraints**
- `1 ≤ ratings.length ≤ 10⁵`
- `0 ≤ ratings[i] ≤ 100`
