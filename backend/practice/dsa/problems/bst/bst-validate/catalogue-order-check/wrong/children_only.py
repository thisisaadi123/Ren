class Solution:
    # Mistake: only compares each node with its own two children.
    def isSearchTree(self, root):
        stack = [root]
        while stack:
            node = stack.pop()
            if node.left:
                if node.left.val >= node.val:
                    return False
                stack.append(node.left)
            if node.right:
                if node.right.val <= node.val:
                    return False
                stack.append(node.right)
        return True
