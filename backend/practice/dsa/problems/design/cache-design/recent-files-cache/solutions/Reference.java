class RecentFilesCache {
    private final int capacity;
    // Access order: the eldest entry is the least recently used.
    private final LinkedHashMap<Integer, Integer> files = new LinkedHashMap<>(16, 0.75f, true);

    public RecentFilesCache(int capacity) {
        this.capacity = capacity;
    }

    public int open(int fileId) {
        Integer size = files.get(fileId);
        return size == null ? -1 : size;
    }

    public void save(int fileId, int size) {
        if (!files.containsKey(fileId) && files.size() == capacity) {
            files.remove(files.keySet().iterator().next());
        }
        files.put(fileId, size);
    }
}
