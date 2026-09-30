class Solution {
public:
    int minDailyLimit(vector<int>& pages, int days) {
        auto daysNeeded = [&](int limit) {
            int used = 1, load = 0;
            for (int p : pages) {
                if (load + p > limit) {
                    used++;
                    load = 0;
                }
                load += p;
            }
            return used;
        };

        int lo = *max_element(pages.begin(), pages.end());
        int hi = accumulate(pages.begin(), pages.end(), 0);
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (daysNeeded(mid) <= days) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
};
