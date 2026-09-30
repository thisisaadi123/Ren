A treasure map is a binary tree of caves; each cave holds a value that may be negative (a toll). A **route** visits a sequence of caves joined by parent–child links, never visiting a cave twice. It has at least one cave and need not pass through the root.

Return the largest total value of any route.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁵` caves.
- `-1000 ≤ value ≤ 1000`
