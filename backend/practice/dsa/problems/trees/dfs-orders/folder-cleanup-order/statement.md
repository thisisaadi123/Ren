A disk's folders form a binary tree, and each folder has a numeric tag. A cleanup tool deletes folders one by one, and a folder can be deleted only after **both** of its sub-folders' whole branches are gone. When it has a choice, the tool always finishes the left branch before starting the right one.

Return the tags in the order the tool deletes the folders. An empty tree gives an empty list.

{{examples}}

**Constraints**
- The tree has between `0` and `10⁵` folders.
- `-1000 ≤ tag ≤ 1000`
