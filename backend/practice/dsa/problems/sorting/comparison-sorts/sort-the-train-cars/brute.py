class Solution:
    def sortCars(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        vals.sort()
        dummy = tail = ListNode()
        for v in vals:
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next
