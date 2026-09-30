def check(args, expected, actual):
    h = args["heights"]
    if type(actual) is not int or not 0 <= actual < len(h):
        return "the answer must be an index between 0 and %d" % (len(h) - 1)
    left = h[actual - 1] if actual > 0 else float("-inf")
    right = h[actual + 1] if actual + 1 < len(h) else float("-inf")
    if h[actual] > left and h[actual] > right:
        return True
    return "index %d (height %d) is not higher than both neighbours" % (actual, h[actual])
