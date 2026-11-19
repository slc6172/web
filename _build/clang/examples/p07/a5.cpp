#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 10; i++) {
        if (i % 2 == 0) {
            continue;                    //@ continue:跳過這一圈剩下的內容,直接進入下一圈(偶數就略過)。
        }
        if (i > 7) {
            break;                       //@ break:立刻離開整個迴圈,後面的圈數都不做了。
        }
        cout << i << " ";
    }
    cout << endl;
    return 0;
}
