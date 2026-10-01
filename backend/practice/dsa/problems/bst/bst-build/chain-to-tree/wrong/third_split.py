class Solution:
    # Mistake: splits a third of the way in instead of in the middle, so big lists lean right.
    def chainToTree(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next

        def build(lo, hi):
            if lo > hi:
                return None
            mid = lo + (hi - lo) // 3
            return TreeNode(vals[mid], build(lo, mid - 1), build(mid + 1, hi))

        return build(0, len(vals) - 1)
