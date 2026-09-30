class Solution:
    # Mistake: re-walks the list for every query until it can shortcut, O(n) per query.
    def positionsAfter(self, head, steps):
        out = []
        for s in steps:
            seen = {}
            node, i = head, 0
            while i < s:
                if node in seen:
                    lam = i - seen[node]
                    left = (s - i) % lam
                    for _ in range(left):
                        node = node.next
                    break
                seen[node] = i
                node = node.next
                i += 1
                if node is None:
                    break
            out.append(node.val if node else -1)
        return out
