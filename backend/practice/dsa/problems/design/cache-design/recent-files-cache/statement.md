An editor keeps a small cache of recently used files. Design the class `RecentFilesCache`:

- `RecentFilesCache(capacity)` creates an empty cache that holds at most `capacity` files.
- `open(fileId)` returns the size of the file if it's in the cache, or `-1` if it isn't. Opening a cached file counts as using it.
- `save(fileId, size)` stores the file with that size (replacing the old size if it's already cached), and counts as using it. If this adds a file to a full cache, first remove the file that was used longest ago.

Both methods must run in O(1) average time.

Tests are a list of calls. The first call creates the cache; the answer is what each call returns (`null` for the constructor and for `save`).

{{examples}}

**Constraints**
- `1 ≤ capacity ≤ 3000`
- `0 ≤ fileId ≤ 10⁴`
- `0 ≤ size ≤ 10⁵`
- At most `2 × 10⁵` calls to `open` and `save`.
