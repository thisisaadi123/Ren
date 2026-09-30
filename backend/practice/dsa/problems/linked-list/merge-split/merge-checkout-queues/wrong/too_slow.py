class Solution:
    # Mistake: merges the queues one by one into a growing result: O(k * N).
    def mergeQueues(self, queues):
        def merge(a, b):
            dummy = ListNode(0)
            tail = dummy
            while a and b:
                if a.val <= b.val:
                    tail.next, a = a, a.next
                else:
                    tail.next, b = b, b.next
                tail = tail.next
            tail.next = a or b
            return dummy.next

        result = None
        for q in queues:
            result = merge(result, q)
        return result
