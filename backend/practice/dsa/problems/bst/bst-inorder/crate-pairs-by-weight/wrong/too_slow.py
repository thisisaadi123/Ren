class Solution:
    # Mistake: correct, but searches the tree for target - x from the root for every x: O(n * height).
    def countPairs(self, root, target):
        count, stack = 0, [root]
        while stack:
            node = stack.pop()
            if not node:
                continue
            stack.append(node.left)
            stack.append(node.right)
            want = target - node.val
            if want <= node.val:
                continue
            cur = root
            while cur and cur.val != want:
                cur = cur.left if want < cur.val else cur.right
            if cur:
                count += 1
        return count
