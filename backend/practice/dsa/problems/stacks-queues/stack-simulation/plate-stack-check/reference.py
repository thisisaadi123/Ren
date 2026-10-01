class Solution:
    def couldHappen(self, washed, served):
        stack = []
        j = 0
        for plate in washed:
            stack.append(plate)
            while stack and stack[-1] == served[j]:
                stack.pop()
                j += 1
        return j == len(served)
