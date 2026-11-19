#include <iostream>
#include <vector>

// 這個版本的插入排序是在「已排序的 v[0..i-1]」裡,從後面往前找 key 該放的位置。
// 請完成 while 的條件,以及迴圈之後把 key 放回去的那一行。
void insertionSort(std::vector<int>& v) {
    int n = static_cast<int>(v.size());
    for (int i = 1; i < n; ++i) {
        int key = v[i];
        int j = i - 1;
        while (false) {                      // 把 false 改成正確的條件(提示:要同時檢查 j 沒有越界、v[j] 比 key 大)
            v[j + 1] = v[j];
            --j;
        }
        // 把 key 放到正確的位置(提示:現在的 j 是第一個「不比 key 大」的位置)
    }
}

int main() {
    std::vector<int> v = {4, 3, 1, 2};
    insertionSort(v);
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << "\n";                       // 預期輸出 1 2 3 4
}
