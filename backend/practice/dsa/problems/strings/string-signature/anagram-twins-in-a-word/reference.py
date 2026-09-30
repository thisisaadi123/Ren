class Solution:
    def anagramTwins(self, s):
        n, total = len(s), 0
        codes = [ord(c) - 97 for c in s]
        for L in range(1, n):
            cnt = [0] * 26
            for c in codes[:L]:
                cnt[c] += 1
            seen = collections.Counter()
            seen[tuple(cnt)] += 1
            for i in range(L, n):
                cnt[codes[i]] += 1
                cnt[codes[i - L]] -= 1
                seen[tuple(cnt)] += 1
            for c in seen.values():
                total += c * (c - 1) // 2
        return total
