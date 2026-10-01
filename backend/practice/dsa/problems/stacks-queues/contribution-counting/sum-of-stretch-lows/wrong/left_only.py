class Solution:
    # Mistake: counts only how far each price reaches to the left.
    def sumOfLows(self, prices):
        MOD = 10**9 + 7
        stack, total = [], 0
        for i, p in enumerate(prices):
            while stack and prices[stack[-1]] >= p:
                stack.pop()
            total += p * (i - (stack[-1] if stack else -1))
            stack.append(i)
        return total % MOD
