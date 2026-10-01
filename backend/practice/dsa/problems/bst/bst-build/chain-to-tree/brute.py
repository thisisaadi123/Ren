class Solution:
    def chainToTree(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next

        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi + 1) // 2
            return TreeNode(vals[mid], build(lo, mid - 1), build(mid + 1, hi))

        return build(0, len(vals) - 1)
