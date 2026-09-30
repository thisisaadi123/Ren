A runner starts on the first node of a linked list `head` and each step moves along one `next` pointer. The list may end, or its last node may link back to an earlier node, forming a loop that the runner goes round forever.

For each `steps[i]`, return the value of the node the runner stands on after exactly `steps[i]` steps (after `0` steps they're on `head`). If the list has no loop and the runner would step past the last node, the answer is `-1`.

In the tests a looped list is written as `{"values": [...], "cycle_at": i}`: the last node links back to node `i` (`-1` means no loop).

{{examples}}

**Constraints**
- The list has between `1` and `10⁵` nodes.
- `0 ≤ node value ≤ 10⁹`
- `cycle_at` is `-1` or a valid node index.
- `1 ≤ steps.length ≤ 10⁵`
- `0 ≤ steps[i] ≤ 10¹⁵`
