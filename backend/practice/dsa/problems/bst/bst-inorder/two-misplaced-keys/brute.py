class Solution:
    def fixSwappedKeys(self, root):
        # Collect the nodes in order, sort the keys, and write them back in that order.
        nodes = []

        def walk(node):
            if node:
                walk(node.left)
                nodes.append(node)
                walk(node.right)

        walk(root)
        for node, v in zip(nodes, sorted(n.val for n in nodes)):
            node.val = v
        return root
