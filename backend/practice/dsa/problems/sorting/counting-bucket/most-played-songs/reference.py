import collections
class Solution:
    def mostPlayed(self, plays, k):
        count = collections.Counter(plays)
        buckets = [[] for _ in range(len(plays) + 1)]
        for song, c in count.items():
            buckets[c].append(song)
        out = []
        for c in range(len(plays), 0, -1):
            for song in sorted(buckets[c]):
                out.append(song)
                if len(out) == k:
                    return out
        return out
