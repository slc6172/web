#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {1, 2, 3, 4, 5};
    cout << "準備讀取 v.at(10)" << endl;
    cout << v.at(10) << endl;               //@ at() 會檢查索引。越界時,程式會立刻報錯停止,而不是默默讀到亂資料。
    cout << "這一行不會被執行" << endl;
    return 0;
}
