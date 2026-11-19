#include <iostream>
using namespace std;

void setZero(int* p) {                       //@ 參數是指標:呼叫的人要把「位址」交進來。
    *p = 0;                                  //@ 透過指標,改到外面那個變數本人。
}

int main() {
    int x = 9;
    setZero(&x);                             //@ &x:取得 x 的位址,交給函式。
    cout << x << endl;
    return 0;
}
