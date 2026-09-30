class Solution:
    # Mistake: forgets to attach the even chain after the odd chain.
    def oddSeatsFirst(self, head):
        if head is None:
            return None
        odd, even = head, head.next
        while even and even.next:
            odd.next = even.next
            odd = odd.next
            even.next = odd.next
            even = even.next
        odd.next = None
        return head
