class Solution:
    def mergeLines(self, first, second):
        dummy = tail = ListNode()
        a, b = first, second
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next
