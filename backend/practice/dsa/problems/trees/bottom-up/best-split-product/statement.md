A company's divisions form a binary tree, and each division has a positive revenue. The board will cut exactly **one** parent–child link, splitting the company into two parts; each part's revenue is the sum of its divisions.

Choose the cut that makes the **product** of the two parts' revenues as large as possible, and return that largest product modulo `10⁹ + 7`. (Maximise the true product, then take the remainder.)

{{examples}}

**Constraints**
- The tree has between `2` and `10⁵` divisions.
- `1 ≤ value ≤ 10⁴`
