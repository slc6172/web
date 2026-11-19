#include <iostream>
using namespace std;

int main() {
    int answer = 42;
    int guess = 0, tries = 0;                //@ tries 記錄已經猜了幾次。
    cout << "猜一個 1 到 100 的數字,你有 7 次機會。" << endl;
    while (tries < 7) {                      //@ 兩個結束的理由:猜中(用 break 離開)或次數用完(條件不成立)。
        cout << "第 " << tries + 1 << " 次猜:";
        cin >> guess;
        tries++;
        if (guess == answer) {
            cout << "答對了!你用了 " << tries << " 次。" << endl;
            break;                           //@ 猜中了,不必再問,直接離開迴圈。
        } else if (guess < answer) {
            cout << "太小了" << endl;
        } else {
            cout << "太大了" << endl;
        }
    }
    if (guess != answer) {                   //@ 迴圈結束後再檢查:如果還沒猜中,就是次數用完了。
        cout << "機會用完了,答案是 " << answer << endl;
    }
    return 0;
}
