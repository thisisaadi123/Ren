class Solution:
    # Mistake: a poster starting exactly at the pin isn't counted as held.
    def fewestPins(self, posters):
        pins, at = 0, None
        for s, e in sorted(posters, key=lambda p: p[1]):
            if at is None or s >= at:
                pins += 1
                at = e
        return pins
