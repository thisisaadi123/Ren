class Solution:
    def findAltitudes(self, elevations, targets):
        return [elevations.index(t) if t in elevations else -1 for t in targets]
