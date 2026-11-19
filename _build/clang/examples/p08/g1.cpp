#include <iostream>
using namespace std;

int main() {
    int answer = 42;                         //@ 先把答案寫死,方便測試。等程式都正確了,再換成隨機的。
    int guess;
    cout << "猜一個 1 到 100 的數字:";
    cin >> guess;
    if (guess == answer) {
        cout << "答對了!" << endl;
    } else if (guess < answer) {
        cout << "太小了" << endl;
    } else {
        cout << "太大了" << endl;
    }
    return 0;
}
