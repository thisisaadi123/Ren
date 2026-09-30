class Solution:
    def findRepeat(self, tickets):
        slow = fast = 0
        while True:
            slow = tickets[slow]
            fast = tickets[tickets[fast]]
            if slow == fast:
                break
        slow = 0
        while slow != fast:
            slow = tickets[slow]
            fast = tickets[fast]
        return slow
