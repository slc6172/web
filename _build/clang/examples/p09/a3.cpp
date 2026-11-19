#include <iostream>
using namespace std;

int main() {
    int scores[5] = {80, 92, 75, 60, 88};
    int best = scores[0];                   //@ 先假設第一個就是最大的。
    for (int i = 1; i < 5; i++) {           //@ 從第二個開始,一個一個和目前的最大值比。
        if (scores[i] > best) {
            best = scores[i];
        }
    }
    cout << "最高分:" << best << endl;
    return 0;
}
