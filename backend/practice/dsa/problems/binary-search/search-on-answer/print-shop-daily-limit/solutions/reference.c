static int daysNeeded(int* pages, int pagesSize, int limit) {
    int used = 1, load = 0;
    for (int i = 0; i < pagesSize; i++) {
        if (load + pages[i] > limit) {
            used++;
            load = 0;
        }
        load += pages[i];
    }
    return used;
}

int minDailyLimit(int* pages, int pagesSize, int days) {
    int lo = 0, hi = 0;
    for (int i = 0; i < pagesSize; i++) {
        if (pages[i] > lo) lo = pages[i];
        hi += pages[i];
    }
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (daysNeeded(pages, pagesSize, mid) <= days) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
