class Solution:
    # Mistake: uses strict comparisons on both sides, so equal lows are counted twice.
    def sumOfLows(self, prices):
        MOD = 10**9 + 7
        n = len(prices)
        left, right = [0] * n, [0] * n
        stack = []
        for i in range(n):
            while stack and prices[stack[-1]] >= prices[i]:
                stack.pop()
            left[i] = i - (stack[-1] if stack else -1)
            stack.append(i)
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and prices[stack[-1]] >= prices[i]:
                stack.pop()
            right[i] = (stack[-1] if stack else n) - i
            stack.append(i)
        return sum(p * l * r for p, l, r in zip(prices, left, right)) % MOD
