class Solution:
    # Mistake: returns where the pointers meet inside the loop, skipping the second phase.
    def findRepeat(self, tickets):
        slow = fast = 0
        while True:
            slow = tickets[slow]
            fast = tickets[tickets[fast]]
            if slow == fast:
                return slow
