#include <iostream>
using namespace std;

int main() {
    int maxValue, answer = 7, guess = 0, tries = 0;
    cout << "最大範圍是多少?";
    cin >> maxValue;
    cout << "猜一個 1 到 " << maxValue << " 的數字。" << endl;
    while (guess != answer) {
        cin >> guess;
        tries++;
        if (guess < 1 || guess > maxValue) {
            cout << "超出範圍了" << endl;
        } else if (guess < answer) {
            cout << "太小了" << endl;
        } else if (guess > answer) {
            cout << "太大了" << endl;
        }
    }
    cout << "答對了,共猜了 " << tries << " 次。" << endl;
    return 0;
}
