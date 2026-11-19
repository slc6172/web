#include <iostream>
#include <random>                            //@ random 提供亂數產生器。這一行先當成黑盒子用就好。
using namespace std;

int main() {
    mt19937 gen(random_device{}());                    //@ random_device 向作業系統要一個每次都不同的種子,所以每次玩答案都不一樣。
    int answer = gen() % 100 + 1;            //@ gen() 給一個很大的隨機整數;% 100 變成 0 到 99;+ 1 變成 1 到 100。
    int guess = 0, tries = 0;
    cout << "猜一個 1 到 100 的數字,你有 7 次機會。" << endl;
    while (tries < 7) {
        cout << "第 " << tries + 1 << " 次猜:";
        cin >> guess;
        tries++;
        if (guess == answer) {
            cout << "答對了!你用了 " << tries << " 次。" << endl;
            break;
        } else if (guess < answer) {
            cout << "太小了" << endl;
        } else {
            cout << "太大了" << endl;
        }
    }
    if (guess != answer) {
        cout << "機會用完了,答案是 " << answer << endl;
    }
    return 0;
}
