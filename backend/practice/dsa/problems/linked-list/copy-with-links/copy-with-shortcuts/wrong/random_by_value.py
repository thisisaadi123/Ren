class Solution:
    # Mistake: finds each random target by VALUE, which picks the wrong clue when values repeat.
    def copyList(self, head):
        nodes, node = [], head
        while node:
            nodes.append(RandomNode(node.val))
            node = node.next
        for a, b in zip(nodes, nodes[1:]):
            a.next = b
        first = {}
        for c in nodes:
            first.setdefault(c.val, c)
        node, i = head, 0
        while node:
            nodes[i].random = first[node.random.val] if node.random else None
            node, i = node.next, i + 1
        return nodes[0] if nodes else None
