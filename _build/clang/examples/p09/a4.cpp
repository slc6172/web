#include <iostream>
using namespace std;

int main() {
    int scores[5] = {80, 92, 75, 60, 88};
    for (int s : scores) {                  //@ 範圍 for:不用管索引,一個一個取出元素放進 s。讀起來就是「對 scores 裡的每一個 s」。
        cout << s << " ";
    }
    cout << endl;
    return 0;
}
