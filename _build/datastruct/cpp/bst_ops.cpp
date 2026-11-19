#include <iostream>

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

bool search(const TreeNode* node, int val) {
    if (node == nullptr) {
        return false;
    }
    if (val == node->val) {
        return true;
    }
    if (val < node->val) {
        return search(node->left, val);
    }
    return search(node->right, val);
}

TreeNode* minNode(TreeNode* node) {
    while (node->left != nullptr) {
        node = node->left;
    }
    return node;
}

TreeNode* erase(TreeNode* node, int val) {
    if (node == nullptr) {
        return nullptr;
    }
    if (val < node->val) {
        node->left = erase(node->left, val);
    } else if (val > node->val) {
        node->right = erase(node->right, val);
    } else {
        if (node->left == nullptr) {
            TreeNode* r = node->right;
            delete node;
            return r;
        }
        if (node->right == nullptr) {
            TreeNode* l = node->left;
            delete node;
            return l;
        }
        TreeNode* succ = minNode(node->right);
        node->val = succ->val;
        node->right = erase(node->right, succ->val);
    }
    return node;
}

void inorder(const TreeNode* node) {
    if (node == nullptr) {
        return;
    }
    inorder(node->left);
    std::cout << node->val << " ";
    inorder(node->right);
}

void preorder(const TreeNode* node) {
    if (node == nullptr) {
        return;
    }
    std::cout << node->val << " ";
    preorder(node->left);
    preorder(node->right);
}

void destroy(TreeNode* node) {
    if (node == nullptr) {
        return;
    }
    destroy(node->left);
    destroy(node->right);
    delete node;
}

int main() {
    TreeNode* root = nullptr;
    for (int v : {5, 3, 8, 1, 4, 7, 9, 2, 6}) {
        root = insert(root, v);
    }
    std::cout << "inorder:  ";
    inorder(root);
    std::cout << "\npreorder: ";
    preorder(root);
    std::cout << "\nsearch 4, 10: " << search(root, 4) << " " << search(root, 10) << "\n";

    root = erase(root, 2);                   // 葉節點
    std::cout << "erase 2 : ";
    preorder(root);
    root = erase(root, 7);                   // 只有一個子節點
    std::cout << "\nerase 7 : ";
    preorder(root);
    root = erase(root, 3);                   // 有兩個子節點
    std::cout << "\nerase 3 : ";
    preorder(root);
    root = erase(root, 5);                   // 根節點,有兩個子節點
    std::cout << "\nerase 5 : ";
    preorder(root);
    std::cout << "\ninorder:  ";
    inorder(root);
    std::cout << "\n";
    destroy(root);
}
