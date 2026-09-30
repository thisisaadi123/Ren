// Level by level with an array queue, so a very deep tree can't overflow the stack.
int tallestBranch(struct TreeNode* root) {
    if (!root) return 0;
    int cap = 1024, head = 0, tail = 0, levels = 0;
    struct TreeNode** q = malloc(sizeof(struct TreeNode*) * cap);
    q[tail++] = root;
    while (head < tail) {
        levels++;
        int end = tail;
        for (; head < end; head++) {
            struct TreeNode* node = q[head];
            if (tail + 2 > cap) {
                cap *= 2;
                q = realloc(q, sizeof(struct TreeNode*) * cap);
            }
            if (node->left) q[tail++] = node->left;
            if (node->right) q[tail++] = node->right;
        }
    }
    free(q);
    return levels;
}
