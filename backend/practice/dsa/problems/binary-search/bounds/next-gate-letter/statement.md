An airport labels its gates with lowercase letters. `gates` lists the open gates' letters in non-decreasing order (letters may repeat). You are at gate `current`.

Return the first open gate letter that comes strictly **after** `current` in the alphabet. If there is none, wrap around and return the first letter in `gates`.

{{examples}}

**Constraints**
- `2 ≤ gates.length ≤ 10⁴`
- `gates` is sorted in non-decreasing order and has at least two different letters.
- `current` is a single lowercase letter.
