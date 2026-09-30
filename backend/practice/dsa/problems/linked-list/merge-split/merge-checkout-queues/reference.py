class Solution:
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

        lists = list(queues)
        if not lists:
            return None
        while len(lists) > 1:
            nxt = [merge(lists[i], lists[i + 1]) for i in range(0, len(lists) - 1, 2)]
            if len(lists) % 2:
                nxt.append(lists[-1])
            lists = nxt
        return lists[0]
