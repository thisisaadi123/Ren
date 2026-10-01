A file system uses absolute paths that start with `/`. In a path:

- `.` means the current folder, and `..` means the parent folder. Going up from the root stays at the root.
- Several slashes in a row act as one.
- Any other name, including `...`, is an ordinary folder name.

Return the **tidy** form of `path`: it starts with a single `/`, separates folders with one `/`, has no `.` or `..` parts, and doesn't end with `/` (unless it's just the root, `/`).

{{examples}}

**Constraints**
- `1 ≤ path.length ≤ 3 × 10⁴`
- `path` starts with `/` and has only English letters, digits, `.`, `/` and `_`.
