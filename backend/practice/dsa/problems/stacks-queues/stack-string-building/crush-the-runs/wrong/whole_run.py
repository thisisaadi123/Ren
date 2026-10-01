class Solution:
    # Mistake: removes a whole run once it reaches k, even if it's longer than k.
    def crushRuns(self, s, k):
        stack = []
        for c in s:
            if stack and stack[-1][0] == c:
                stack[-1][1] += 1
            else:
                if stack and stack[-1][1] >= k:
                    stack.pop()
                    if stack and stack[-1][0] == c:
                        stack[-1][1] += 1
                        continue
                stack.append([c, 1])
        if stack and stack[-1][1] >= k:
            stack.pop()
        return "".join(c * n for c, n in stack)
