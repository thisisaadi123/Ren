class Solution:
    # Mistake: swaps values from both ends inward, walking from the head to each position: O(n^2).
    def flipStretch(self, head, left, right):
        def at(i):
            node = head
            for _ in range(i - 1):
                node = node.next
            return node
        i, j = left, right
        while i < j:
            a, b = at(i), at(j)
            a.val, b.val = b.val, a.val
            i += 1
            j -= 1
        return head
