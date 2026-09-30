class Solution:
    # Mistake: correct, but rescans whole subtrees for their min and max: O(n^2) on a long chain.
    def isSearchTree(self, root):
        def values(node):
            out, stack = [], [node]
            while stack:
                x = stack.pop()
                if x:
                    out.append(x.val)
                    stack.append(x.left)
                    stack.append(x.right)
            return out

        stack = [root]
        while stack:
            node = stack.pop()
            if node.left:
                if max(values(node.left)) >= node.val:
                    return False
                stack.append(node.left)
            if node.right:
                if min(values(node.right)) <= node.val:
                    return False
                stack.append(node.right)
        return True
