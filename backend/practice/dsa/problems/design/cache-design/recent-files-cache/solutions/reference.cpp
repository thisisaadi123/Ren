class RecentFilesCache {
    int capacity;
    list<pair<int, int>> order;  // front = most recent
    unordered_map<int, list<pair<int, int>>::iterator> where;

public:
    RecentFilesCache(int capacity) : capacity(capacity) {}

    int open(int fileId) {
        auto it = where.find(fileId);
        if (it == where.end()) return -1;
        order.splice(order.begin(), order, it->second);
        return it->second->second;
    }

    void save(int fileId, int size) {
        auto it = where.find(fileId);
        if (it != where.end()) {
            it->second->second = size;
            order.splice(order.begin(), order, it->second);
            return;
        }
        if ((int)order.size() == capacity) {
            where.erase(order.back().first);
            order.pop_back();
        }
        order.emplace_front(fileId, size);
        where[fileId] = order.begin();
    }
};
