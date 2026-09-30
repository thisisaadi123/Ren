A model railway is laid out as a linked list of track pieces starting at `head`. A careless builder may have connected the last piece back to one of the earlier pieces, making the train go round forever.

Return `true` if following `next` pointers from `head` ever revisits a node, and `false` if it reaches the end.

In the tests a list with a loop is written as `{"values": [...], "cycle_at": i}`: the last node points back to node `i` (`-1` means no loop). Your function receives only the head node.

{{examples}}

**Constraints**
- The list has between `0` and `10⁵` nodes.
- `-10⁵ ≤ node value ≤ 10⁵`
- `cycle_at` is `-1` or a valid node index.
