class Solution {
public:
    int tallestBranch(TreeNode* root) {
        int levels = 0;
        vector<TreeNode*> level;
        if (root) level.push_back(root);
        while (!level.empty()) {
            levels++;
            vector<TreeNode*> next;
            for (TreeNode* node : level) {
                if (node->left) next.push_back(node->left);
                if (node->right) next.push_back(node->right);
            }
            level.swap(next);
        }
        return levels;
    }
};
