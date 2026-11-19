#include <iostream>
using namespace std;

int main() {
    int choice;
    cout << "1 查詢  2 新增  3 離開,請選擇:";
    cin >> choice;
    switch (choice) {                    //@ switch 依 choice 的值「跳」到對應的 case。括號裡只能放整數或字元。
        case 1:
            cout << "查詢中" << endl;
            break;                       //@ break:做完就跳出 switch。沒有它,程式會繼續往下執行下一個 case。
        case 2:
            cout << "新增中" << endl;
            break;
        case 3:
            cout << "再見" << endl;
            break;
        default:                         //@ default:所有 case 都不符合時做這一段,像 if 的 else。
            cout << "沒有這個選項" << endl;
    }
    return 0;
}
