Before an exam you have `hours` hours and a stack of `books`, where `books[i]` is the number of pages in book `i`.

You pick a reading speed of `s` pages per hour. Each hour you read from **one** book: `s` pages, or the rest of the book if fewer than `s` pages remain (the rest of that hour is then wasted).

Return the smallest whole-number speed `s` that lets you finish every book within `hours` hours.

{{examples}}

**Constraints**
- `1 ≤ books.length ≤ 10⁴`
- `books.length ≤ hours ≤ 10⁹`
- `1 ≤ books[i] ≤ 10⁹`
