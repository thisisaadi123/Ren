class Solution:
    # Correct but quadratic: repeatedly walks to the end to pull off the last car.
    def reverseTrain(self, head):
        dummy = ListNode(0)
        tail = dummy
        while head:
            if head.next is None:
                tail.next, head = head, None
                break
            prev = head
            while prev.next.next:
                prev = prev.next
            tail.next = prev.next
            prev.next = None
            tail = tail.next
        return dummy.next
