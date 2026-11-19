#include <iostream>
#include <iomanip>                     //@ iomanip 提供格式化工具,例如 setw 與 setprecision。
using namespace std;

int main() {
    double price;
    int qty;
    cout << "單價與數量:";
    cin >> price >> qty;               //@ cin 會依變數的型態讀取:price 讀小數,qty 讀整數。
    cout << "預設輸出:" << price * qty << endl;
    cout << fixed << setprecision(2);  //@ fixed 加 setprecision(2):小數固定顯示 2 位。這兩個設定會一直有效,直到你再改它。
    cout << "固定兩位:" << price * qty << endl;
    cout << "[" << setw(8) << price << "]" << endl;   //@ setw(8):下一個輸出至少佔 8 格寬,不夠就在左邊補空格(只影響緊接著的那一個)。
    return 0;
}
