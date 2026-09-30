class Solution:
    def removeBeads(self, head, bad):
        keep = []
        while head:
            if head.val != bad:
                keep.append(head.val)
            head = head.next
        new_head = None
        for v in reversed(keep):
            new_head = ListNode(v, new_head)
        return new_head
