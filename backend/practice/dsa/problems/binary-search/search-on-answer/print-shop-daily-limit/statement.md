A print shop has a queue of jobs. Job `i` has `pages[i]` pages, and jobs must be printed in the order they arrive. A job can't be split across two days.

The shop sets one daily page limit and prints as many whole jobs as fit under it each day. Return the smallest daily limit that finishes every job within `days` days.

{{examples}}

**Constraints**
- `1 ≤ pages.length ≤ 5 × 10⁴`
- `1 ≤ pages[i] ≤ 500`
- `1 ≤ days ≤ pages.length`
