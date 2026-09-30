class Solution:
    # Mistake: assumes any walk longer than 5000 steps must be going round a loop.
    def hasLoop(self, head):
        steps = 0
        while head:
            steps += 1
            if steps > 5000:
                return True
            head = head.next
        return False
