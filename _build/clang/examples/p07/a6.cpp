#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 3; i++) {       //@ 外層迴圈:控制「第幾列」。
        for (int j = 1; j <= 3; j++) {   //@ 內層迴圈:外層每跑一圈,內層從頭完整跑一遍,控制「第幾欄」。
            cout << i * j << "\t";       //@ \t 是跳到下一個定位點(對齊用)。
        }
        cout << endl;
    }
    return 0;
}
