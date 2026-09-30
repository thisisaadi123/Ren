class Solution:
    def smallestLeafWord(self, root):
        # Give every node its parent, then climb from each leaf to the root.
        parent, leaves, todo = {id(root): None}, [], [root]
        node_of = {id(root): root}
        while todo:
            node = todo.pop()
            kids = [c for c in (node.left, node.right) if c]
            if not kids:
                leaves.append(node)
            for c in kids:
                parent[id(c)] = node
                todo.append(c)
        words = []
        for leaf in leaves:
            w, cur = "", leaf
            while cur is not None:
                w += "abcdefghijklmnopqrstuvwxyz"[cur.val]
                cur = parent[id(cur)]
            words.append(w)
        return min(words)
