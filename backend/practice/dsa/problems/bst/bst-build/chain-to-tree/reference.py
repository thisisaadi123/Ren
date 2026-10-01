class Solution:
    def chainToTree(self, head):
        n = 0
        node = head
        while node:
            n += 1
            node = node.next
        cur = [head]

        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            left = build(lo, mid - 1)
            root = TreeNode(cur[0].val, left)
            cur[0] = cur[0].next
            root.right = build(mid + 1, hi)
            return root

        return build(0, n - 1)
