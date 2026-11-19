#include <iostream>
using namespace std;

int add(int a, int b) {                     //@ 多個參數用逗號隔開,每個參數都要寫型態。
    return a + b;
}

int maxOf(int a, int b) {
    if (a > b) {
        return a;
    }
    return b;                               //@ 前面的 if 沒有 return,就會走到這裡。函式裡可以有多個 return。
}

int main() {
    cout << add(3, 4) << endl;
    cout << maxOf(7, 19) << endl;
    int total = add(10, maxOf(2, 6));       //@ 函式的回傳值就是一個值,可以直接放進別的運算式或當別的函式的參數。
    cout << total << endl;
    return 0;
}
