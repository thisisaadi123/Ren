class Solution:
    # Mistake: serves at most one plate after each new plate is stacked.
    def couldHappen(self, washed, served):
        stack = []
        j = 0
        for plate in washed:
            stack.append(plate)
            if stack[-1] == served[j]:
                stack.pop()
                j += 1
        while stack and stack[-1] == served[j]:
            stack.pop()
            j += 1
        return j == len(served)
