Fence posts stand along a line. `posts[i] = [x, y]` gives post `i`'s position `x` and height `y`, and the posts are sorted by position with no two at the same spot.

Two posts `i < j` can hold a banner if they are at most `k` apart: `x_j − x_i ≤ k`. The banner's value is `y_i + y_j + (x_j − x_i)`. Return the **largest value** of any banner. At least one pair of posts is close enough.

{{examples}}

**Constraints**
- `2 ≤ posts.length ≤ 10⁵`
- `-10⁸ ≤ x ≤ 10⁸`, strictly increasing along the list
- `-10⁸ ≤ y ≤ 10⁸`
- `0 ≤ k ≤ 2 × 10⁸`
- At least one pair satisfies `x_j − x_i ≤ k`.
