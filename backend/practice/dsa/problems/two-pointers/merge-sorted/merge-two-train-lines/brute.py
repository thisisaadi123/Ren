class Solution:
    def mergeLines(self, first, second):
        vals = []
        for node in (first, second):
            while node:
                vals.append(node.val)
                node = node.next
        dummy = tail = ListNode()
        for v in sorted(vals):
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next
