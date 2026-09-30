class Solution:
    def sortCars(self, head):
        def merge(a, b):
            dummy = tail = ListNode()
            while a and b:
                if a.val <= b.val:
                    tail.next, a = a, a.next
                else:
                    tail.next, b = b, b.next
                tail = tail.next
            tail.next = a or b
            return dummy.next
        def sort(h):
            if not h or not h.next:
                return h
            slow, fast = h, h.next
            while fast and fast.next:
                slow, fast = slow.next, fast.next.next
            mid, slow.next = slow.next, None
            return merge(sort(h), sort(mid))
        return sort(head)
