class Solution:
    # Mistake: breaks ties the same way on both sides, so equal readings are counted twice.
    def totalSwing(self, readings):
        n = len(readings)

        def counts(better):
            left, right = [0] * n, [0] * n
            stack = []
            for i in range(n):
                while stack and not better(readings[stack[-1]], readings[i]):
                    stack.pop()
                left[i] = i - (stack[-1] if stack else -1)
                stack.append(i)
            stack = []
            for i in range(n - 1, -1, -1):
                while stack and not better(readings[stack[-1]], readings[i]):
                    stack.pop()
                right[i] = (stack[-1] if stack else n) - i
                stack.append(i)
            return [l * r for l, r in zip(left, right)]

        as_max = counts(lambda a, b: a > b)
        as_min = counts(lambda a, b: a < b)
        return sum(v * (x - y) for v, x, y in zip(readings, as_max, as_min))
