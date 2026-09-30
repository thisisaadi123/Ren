class Solution:
    def reverseTrain(self, head):
        values = []
        while head:
            values.append(head.val)
            head = head.next
        new_head = None
        for v in values:  # pushing to the front reverses the order
            new_head = ListNode(v, new_head)
        return new_head
