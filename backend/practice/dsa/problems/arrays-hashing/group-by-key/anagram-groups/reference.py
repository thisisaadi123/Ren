class Solution:
    def groupAnagrams(self, words):
        groups = collections.defaultdict(list)
        for w in words:
            groups["".join(sorted(w))].append(w)
        return sorted(sorted(g) for g in groups.values())
