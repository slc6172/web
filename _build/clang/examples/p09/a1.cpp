#include <iostream>
using namespace std;

int main() {
    int scores[5] = {80, 92, 75, 60, 88};   //@ 宣告一個能放 5 個 int 的陣列,並用大括號給初始值。方括號裡的 5 是「長度」。
    cout << scores[0] << endl;              //@ 索引從 0 開始!第一個元素是 scores[0],不是 scores[1]。
    cout << scores[4] << endl;              //@ 長度是 5,最後一個元素的索引是 4(長度減 1)。
    scores[2] = 77;                         //@ 用索引也能改值。
    cout << scores[2] << endl;
    return 0;
}
