#include <iostream>
#include <queue>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
};

void preorder(const TreeNode* node) {
    if (node == nullptr) {
        return;
    }
    std::cout << node->val << " ";
    preorder(node->left);
    preorder(node->right);
}

void inorder(const TreeNode* node) {
    if (node == nullptr) {
        return;
    }
    inorder(node->left);
    std::cout << node->val << " ";
    inorder(node->right);
}

void postorder(const TreeNode* node) {
    if (node == nullptr) {
        return;
    }
    postorder(node->left);
    postorder(node->right);
    std::cout << node->val << " ";
}

void levelOrder(const TreeNode* root) {
    if (root == nullptr) {
        return;
    }
    std::queue<const TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        const TreeNode* node = q.front();
        q.pop();
        std::cout << node->val << " ";
        if (node->left != nullptr) {
            q.push(node->left);
        }
        if (node->right != nullptr) {
            q.push(node->right);
        }
    }
}

void destroy(TreeNode* node) {
    if (node == nullptr) {
        return;
    }
    destroy(node->left);                     // 先刪子樹
    destroy(node->right);
    delete node;                             // 最後才刪自己(後序)
}

int main() {
    TreeNode* root = new TreeNode{1,
        new TreeNode{2, new TreeNode{4, nullptr, nullptr}, new TreeNode{5, nullptr, nullptr}},
        new TreeNode{3, new TreeNode{6, nullptr, nullptr}, new TreeNode{7, nullptr, nullptr}}};
    preorder(root);
    std::cout << "\n";
    inorder(root);
    std::cout << "\n";
    postorder(root);
    std::cout << "\n";
    levelOrder(root);
    std::cout << "\n";
    destroy(root);
}
