class Solution:
    def findLocker(self, lockers, target):
        return lockers.index(target) if target in lockers else -1
