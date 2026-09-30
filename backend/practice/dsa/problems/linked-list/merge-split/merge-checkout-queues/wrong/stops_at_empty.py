class Solution:
    # Mistake: repeatedly takes the smallest head, but stops as soon as any queue is empty.
    def mergeQueues(self, queues):
        heads = list(queues)
        dummy = ListNode(0)
        tail = dummy
        while heads and all(h is not None for h in heads):
            i = min(range(len(heads)), key=lambda j: heads[j].val)
            tail.next = heads[i]
            tail = tail.next
            heads[i] = heads[i].next
        for h in heads:
            if h is not None:
                tail.next = h
                break
        return dummy.next
