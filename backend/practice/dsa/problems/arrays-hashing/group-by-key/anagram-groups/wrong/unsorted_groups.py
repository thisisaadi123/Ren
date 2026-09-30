class Solution:
    # Mistake: groups correctly but keeps the input order.
    def groupAnagrams(self, words):
        groups = collections.defaultdict(list)
        for w in words:
            groups["".join(sorted(w))].append(w)
        return list(groups.values())
