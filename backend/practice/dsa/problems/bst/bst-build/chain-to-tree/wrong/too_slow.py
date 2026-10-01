class Solution:
    # Mistake: walks from the head to reach each middle value: O(n^2) in the worst case.
    def chainToTree(self, head):
        n = 0
        node = head
        while node:
            n += 1
            node = node.next

        def at(i):
            node = head
            for _ in range(i):
                node = node.next
            return node.val

        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            return TreeNode(at(mid), build(lo, mid - 1), build(mid + 1, hi))

        return build(0, n - 1)
