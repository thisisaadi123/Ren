import collections
class Solution:
    def countHidden(self, text, words):
        waiting = collections.defaultdict(list)
        for w in words:
            waiting[w[0]].append((w, 0))
        done = 0
        for c in text:
            bucket = waiting.pop(c, [])
            for w, i in bucket:
                i += 1
                if i == len(w):
                    done += 1
                else:
                    waiting[w[i]].append((w, i))
        return done
