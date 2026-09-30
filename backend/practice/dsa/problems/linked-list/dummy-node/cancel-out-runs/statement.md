A ledger is a linked list of transactions starting at `head`; each node holds an amount, which may be positive, negative or zero. The clerk copies the ledger onto a clean sheet, one node at a time, from front to back.

After copying each node, if the clean sheet now **ends with** one or more consecutive entries whose amounts add up to `0`, the clerk crosses out that whole run. (There is never more than one such run to choose from.) Return the head of the clean sheet once every node has been processed; it may be empty.

{{examples}}

**Constraints**
- The ledger has between `0` and `10⁵` nodes.
- `-1000 ≤ node value ≤ 1000`
