def balanced(t):
    d = 0
    for c in t:
        if c == "(":
            d += 1
        elif c == ")":
            d -= 1
            if d < 0:
                return False
    return d == 0
def check(args, expected, actual):
    s = args["s"]
    if not isinstance(actual, str):
        return "the answer must be a string"
    i = 0
    for c in s:
        if i < len(actual) and actual[i] == c:
            i += 1
        elif c not in "()":
            return "every letter must stay, in order; only brackets may be removed"
    if i != len(actual):
        return "the answer isn't s with some brackets removed"
    if not balanced(actual):
        return "the brackets that remain aren't balanced"
    if len(actual) != len(expected):
        return "removed %d brackets, but %d is enough" % (len(s) - len(actual), len(s) - len(expected))
    return True
