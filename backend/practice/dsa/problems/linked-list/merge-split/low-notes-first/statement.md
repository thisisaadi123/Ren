A melody is a linked list of pitches starting at `head`. For a warm-up exercise, all notes lower than `pivot` must be played first, followed by all the others, but the notes inside each of those two groups must keep the order they had in the melody.

Rearrange the nodes so every node with value `< pivot` comes before every node with value `≥ pivot`, keeping the relative order within each group, and return the head.

{{examples}}

**Constraints**
- The list has between `0` and `10⁵` nodes.
- `-10⁶ ≤ node value, pivot ≤ 10⁶`
