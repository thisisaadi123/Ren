A post office sells stamps in the distinct values listed in `stamps`, and it never runs out of any value. To mail a parcel you must stick on stamps worth **exactly** `target` in total.

Return every different mix of stamps that does this. A mix is a multiset of values; write each one with its values in **non-decreasing** order. The mixes may be returned in any order, and if there is none, return an empty list.

{{examples}}

**Constraints**
- `1 ≤ stamps.length ≤ 30`
- `2 ≤ stamps[i] ≤ 40`
- All values in `stamps` are distinct.
- `1 ≤ target ≤ 40`
