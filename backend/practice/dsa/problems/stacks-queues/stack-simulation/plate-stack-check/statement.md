A dishwasher stacks clean plates one by one, in the order `washed`. At any moment, a waiter may take the **top** plate from the stack to serve. Every plate is numbered, and the numbers are distinct.

Given the order the plates were served in, `served`, return `true` if this could have happened, otherwise `false`.

{{examples}}

**Constraints**
- `1 ≤ washed.length ≤ 10⁵`
- `served` is a rearrangement of `washed`.
- `0 ≤ washed[i] ≤ 10⁹`, all distinct.
