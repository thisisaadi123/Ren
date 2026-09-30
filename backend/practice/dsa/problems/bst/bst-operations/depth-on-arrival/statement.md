Keys arrive one at a time and each is inserted into a binary search tree that starts empty, in the usual way: start at the root, go left when the new key is smaller and right when it is larger, and attach it where the walk falls off.

Return an array whose `i`-th entry is the depth at which `keys[i]` was attached. The first key becomes the root at depth `1`; its children have depth `2`, and so on.

{{examples}}

**Constraints**
- `1 ≤ keys.length ≤ 10⁵`
- `-10⁹ ≤ keys[i] ≤ 10⁹`
- All keys are distinct.
