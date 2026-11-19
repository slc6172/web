#include <iostream>
using namespace std;                             //@ 之後可以省略 std::,直接寫 cout 與 endl。

int main() {
    // 這一行是註解,編譯器會直接略過
    cout << "Hello, C++!" << endl;
    cout << "我正在學 C++\n";                     //@ \n 也是換行,和 endl 效果相近。
    return 0;
}
