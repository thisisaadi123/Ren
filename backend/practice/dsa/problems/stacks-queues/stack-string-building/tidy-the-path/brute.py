import re


class Solution:
    def tidyPath(self, path):
        p = re.sub("/+", "/", path + "/")
        while True:
            q = p.replace("/./", "/")
            q = re.sub(r"/(?!\.\.?/)[^/]+/\.\./", "/", q, count=1)
            q = re.sub(r"^/\.\./", "/", q)
            if q == p:
                break
            p = q
        return p.rstrip("/") or "/"
