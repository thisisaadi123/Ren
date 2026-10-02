A scavenger trail is a linked list. Each clue (node) has a `val`, a `next` pointer to the following clue, and a `random` **shortcut** pointer that leads to any clue in the trail, or to nothing.

Return a **deep copy** of the trail: brand-new nodes with the same values, whose `next` and `random` pointers mirror the original's but point only at the new nodes. The original nodes must not appear in the copy.

The trail is written as a list of `[val, random]` pairs, one per clue in order, where `random` is the index of the clue the shortcut leads to, or `null`.

{{examples}}

**Constraints**
- The trail has between `0` and `10⁵` clues.
- `-10⁴ ≤ val ≤ 10⁴`
- Each `random` is `null` or the index of a clue in the trail.
