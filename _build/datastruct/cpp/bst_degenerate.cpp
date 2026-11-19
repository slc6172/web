#include <algorithm>
#include <iostream>
#include <vector>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
};

TreeNode* insert(TreeNode* node, int val) {
    if (node == nullptr) {
        return new TreeNode{val, nullptr, nullptr};
    }
    if (val < node->val) {
        node->left = insert(node->left, val);
    } else if (val > node->val) {
        node->right = insert(node->right, val);
    }
    return node;
}

int height(const TreeNode* node) {
    if (node == nullptr) {
        return 0;
    }
    return 1 + std::max(height(node->left), height(node->right));
}

void destroy(TreeNode* node) {
    if (node == nullptr) {
        return;
    }
    destroy(node->left);
    destroy(node->right);
    delete node;
}

int heightAfterInserting(const std::vector<int>& values) {
    TreeNode* root = nullptr;
    for (int v : values) {
        root = insert(root, v);
    }
    int h = height(root);
    destroy(root);
    return h;
}

int main() {
    std::cout << "4 2 6 1 3 5 7 -> height " << heightAfterInserting({4, 2, 6, 1, 3, 5, 7}) << "\n";
    std::cout << "1 2 3 4 5 6 7 -> height " << heightAfterInserting({1, 2, 3, 4, 5, 6, 7}) << "\n";
}
