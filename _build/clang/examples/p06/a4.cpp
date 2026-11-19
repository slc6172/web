#include <iostream>
using namespace std;

int main() {
    int choice;
    cout << "請選擇:";
    cin >> choice;
    switch (choice) {
        case 1:
            cout << "查詢中" << endl;
            // fall through
        case 2:
            cout << "新增中" << endl;
            // fall through
        case 3:
            cout << "再見" << endl;
            // fall through
        default:
            cout << "沒有這個選項" << endl;
    }
    return 0;
}
