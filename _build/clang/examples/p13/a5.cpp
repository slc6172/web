#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> v = {5, 2, 9, 1, 7};
    auto it = find(v.begin(), v.end(), 9);   //@ find:在範圍裡找 9。找到就回傳指向它的「位置」,找不到就回傳 v.end()。
    if (it != v.end()) {                     //@ 和 v.end() 比較,就知道有沒有找到。
        cout << "找到了,索引 " << (it - v.begin()) << endl;   // it - v.begin() 是它離起點的距離,也就是索引。
    }
    cout << "共有 " << count(v.begin(), v.end(), 7) << " 個 7" << endl;    //@ count 算出某個值出現幾次。
    return 0;
}
