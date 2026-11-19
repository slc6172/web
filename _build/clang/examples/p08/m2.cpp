#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    for (int i = 1; i <= 9; i++) {           //@ 外層控制「第幾列」。
        for (int j = 1; j <= 9; j++) {       //@ 內層控制「第幾欄」。
            cout << setw(4) << i * j;        //@ setw(4):每個數字佔 4 格寬,右邊對齊,整張表就會整齊。
        }
        cout << endl;                        //@ 一列印完,換行。
    }
    return 0;
}
