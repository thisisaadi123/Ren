You have a drawer of gift cards with the values in `cards`; several cards can share a value. You want to hand over cards worth **exactly** `target`, using each physical card at most once.

Two bundles are the same if they contain the same number of cards of each value. Return every different bundle, each written in **non-decreasing** order. The bundles may be returned in any order, and if there is none, return an empty list.

{{examples}}

**Constraints**
- `1 ≤ cards.length ≤ 40`
- `1 ≤ cards[i] ≤ 50`
- `1 ≤ target ≤ 30`
