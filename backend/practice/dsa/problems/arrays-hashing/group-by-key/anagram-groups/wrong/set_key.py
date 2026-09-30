class Solution:
    # Mistake: keys by the set of letters, so "aab" and "abb" end up together.
    def groupAnagrams(self, words):
        groups = collections.defaultdict(list)
        for w in words:
            groups["".join(sorted(set(w)))].append(w)
        return sorted(sorted(g) for g in groups.values())
