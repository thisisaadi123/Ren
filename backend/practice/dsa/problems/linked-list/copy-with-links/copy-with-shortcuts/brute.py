class Solution:
    def copyList(self, head):
        nodes = []
        node = head
        while node:
            nodes.append(node)
            node = node.next
        index = {id(n): i for i, n in enumerate(nodes)}
        new = [RandomNode(n.val) for n in nodes]
        for i, n in enumerate(nodes):
            if i + 1 < len(new):
                new[i].next = new[i + 1]
            if n.random is not None:
                new[i].random = new[index[id(n.random)]]
        return new[0] if new else None
