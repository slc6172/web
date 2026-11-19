#include <iostream>
using namespace std;

int main() {
    int* p = nullptr;                        //@ nullptr:「不指向任何東西」的指標。宣告指標時如果還沒有對象,一定要設成 nullptr。
    if (p == nullptr) {                      //@ 使用指標之前先檢查它是不是空的。對空指標解參考(*p)會讓程式當掉。
        cout << "p 是空指標,不能使用 *p" << endl;
    }
    int x = 7;
    p = &x;
    if (p != nullptr) {
        cout << "現在 *p = " << *p << endl;
    }
    return 0;
}
