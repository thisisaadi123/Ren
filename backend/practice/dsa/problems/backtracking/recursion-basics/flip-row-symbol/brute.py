class Solution:
    def symbolAt(self, n, k):
        row = "0"
        for _ in range(n - 1):
            row = "".join("01" if c == "0" else "10" for c in row)
        return int(row[k - 1])
