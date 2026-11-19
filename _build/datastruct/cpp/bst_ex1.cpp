#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
};

bool contains(const TreeNode* root, int val) {
    const TreeNode* cur = root;
    while (cur != nullptr) {
        if (val == cur->val) {
            return true;
        }
        cur = (val < cur->val) ? cur->left : cur->right;
    }
    return false;
}

int main() {
    TreeNode n1{1, nullptr, nullptr};
    TreeNode n7{7, nullptr, nullptr};
    TreeNode n3{3, &n1, nullptr};
    TreeNode n5{5, &n3, &n7};
    std::cout << contains(&n5, 3) << contains(&n5, 7) << contains(&n5, 4) << contains(nullptr, 1) << "\n";
}
