Crates on a conveyor are a linked list starting at `head`. A robot picks up the crates `k` at a time from the front, flips each batch around and puts it back in the same place, so within each batch the order is reversed. If fewer than `k` crates are left at the end, the robot leaves them as they are.

Return the head of the list after every full batch has been flipped. Rearrange the nodes themselves (not just their values) using O(1) extra memory.

{{examples}}

**Constraints**
- The list has `n` nodes, `1 ≤ n ≤ 10⁵`.
- `1 ≤ k ≤ n`
- `-10⁶ ≤ node value ≤ 10⁶`
