#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
};

// 用「迴圈」(不用遞迴)在二元搜尋樹裡找 val。
// 提示:從 root 出發,比較 val 和目前節點的值,往左或往右走,直到找到或走到 nullptr。
bool contains(const TreeNode* root, int val) {
    (void)root;
    (void)val;
    return false;
}

int main() {
    TreeNode n1{1, nullptr, nullptr};
    TreeNode n7{7, nullptr, nullptr};
    TreeNode n3{3, &n1, nullptr};
    TreeNode n5{5, &n3, &n7};
    std::cout << contains(&n5, 3) << contains(&n5, 7) << contains(&n5, 4) << contains(nullptr, 1) << "\n";   // 預期輸出 1100
}
