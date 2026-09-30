class Solution:
    # Mistake: a node with two children takes the largest key of its LEFT side instead.
    def applyEdits(self, root, ops):
        def insert(node, k):
            if node is None:
                return TreeNode(k)
            if k < node.val:
                node.left = insert(node.left, k)
            elif k > node.val:
                node.right = insert(node.right, k)
            return node

        def delete(node, k):
            if node is None:
                return None
            if k < node.val:
                node.left = delete(node.left, k)
            elif k > node.val:
                node.right = delete(node.right, k)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                s = node.left
                while s.right:
                    s = s.right
                node.val = s.val
                node.left = delete(node.left, s.val)
            return node

        for kind, k in ops:
            root = insert(root, k) if kind == 1 else delete(root, k)
        return root
