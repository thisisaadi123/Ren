class Solution:
    # Mistake: finds each random target's position by walking from the head: O(n^2).
    def copyList(self, head):
        nodes, node = [], head
        while node:
            nodes.append(node)
            node = node.next
        new = [RandomNode(n.val) for n in nodes]
        for a, b in zip(new, new[1:]):
            a.next = b
        for i, n in enumerate(nodes):
            if n.random is not None:
                j, walk = 0, head
                while walk is not n.random:
                    walk, j = walk.next, j + 1
                new[i].random = new[j]
        return new[0] if new else None
