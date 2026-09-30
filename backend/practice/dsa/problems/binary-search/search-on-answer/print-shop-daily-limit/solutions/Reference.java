class Solution {
    public int minDailyLimit(int[] pages, int days) {
        int lo = 0, hi = 0;
        for (int p : pages) {
            lo = Math.max(lo, p);
            hi += p;
        }
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (daysNeeded(pages, mid) <= days) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    private int daysNeeded(int[] pages, int limit) {
        int used = 1, load = 0;
        for (int p : pages) {
            if (load + p > limit) {
                used++;
                load = 0;
            }
            load += p;
        }
        return used;
    }
}
