class Solution:
    def groupAnagrams(self, words):
        groups = []
        for w in words:
            for g in groups:
                if collections.Counter(g[0]) == collections.Counter(w):
                    g.append(w)
                    break
            else:
                groups.append([w])
        return sorted(sorted(g) for g in groups)
