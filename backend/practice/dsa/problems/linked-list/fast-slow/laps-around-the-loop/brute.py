class Solution:
    def positionsAfter(self, head, steps):
        out = []
        for s in steps:
            node = head
            for _ in range(s):
                node = node.next
                if node is None:
                    break
            out.append(node.val if node else -1)
        return out
