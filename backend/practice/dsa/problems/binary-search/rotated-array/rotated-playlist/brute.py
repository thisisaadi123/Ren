class Solution:
    def findTrack(self, playlist, target):
        return playlist.index(target) if target in playlist else -1
