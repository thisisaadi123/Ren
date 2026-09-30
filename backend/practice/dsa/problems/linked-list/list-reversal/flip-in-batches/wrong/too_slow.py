class Solution:
    # Mistake: builds each batch by repeatedly walking to its last crate, O(k^2) per batch.
    def flipBatches(self, head, k):
        dummy = ListNode(0, head)
        before = dummy
        while True:
            probe = before
            for _ in range(k):
                probe = probe.next
                if probe is None:
                    return dummy.next
            after = probe.next
            tail = before
            for size in range(k, 0, -1):
                prev = tail
                node = tail.next
                for _ in range(size - 1):
                    prev, node = node, node.next
                prev.next = node.next
                node.next = tail.next
                tail.next = node
                tail = node
            before = tail
