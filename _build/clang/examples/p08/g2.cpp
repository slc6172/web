#include <iostream>
using namespace std;

int main() {
    int answer = 42;
    int guess = 0;
    cout << "猜一個 1 到 100 的數字。" << endl;
    while (guess != answer) {                //@ 沒猜中就一直問。guess 一開始設成 0,確保第一次檢查時條件成立。
        cout << "你的猜測:";
        cin >> guess;
        if (guess == answer) {
            cout << "答對了!" << endl;
        } else if (guess < answer) {
            cout << "太小了" << endl;
        } else {
            cout << "太大了" << endl;
        }
    }
    return 0;
}
