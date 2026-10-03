"""Drawing helpers shared by the binary-search solutions."""
from sol import Row, Vars


def lower_bound_walk(W, arr, target, strict=False, label=None):
    """Record the steps of `first index with arr[i] >= target` (or > target if strict). Returns the index."""
    lo, hi = 0, len(arr)
    cmp = ">" if strict else "≥"
    while lo < hi:
        mid = (lo + hi) // 2
        go_right = arr[mid] <= target if strict else arr[mid] < target
        st = {k: "dim" for k in range(len(arr)) if k < lo or k >= hi}
        st[mid] = "active"
        if go_right:
            text = f"lo={lo}, hi={hi}, mid={mid}: {arr[mid]} is not {cmp} {target}, so the answer is right of mid: lo = {mid + 1}."
        else:
            text = f"lo={lo}, hi={hi}, mid={mid}: {arr[mid]} {cmp} {target}, so mid might be the answer: hi = {mid}."
        W.step(text, Row(arr, st=st, ptr={"lo": lo, "mid": mid, "hi": hi} if hi < len(arr) else {"lo": lo, "mid": mid}, slots=True, label=label))
        if go_right:
            lo = mid + 1
        else:
            hi = mid
    return lo
