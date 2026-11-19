#include <iostream>
#include <climits>                      //@ climits 提供 INT_MAX 這類「型態上限」常數。
using namespace std;

int main() {
    unsigned int u = 4294967295u;       //@ unsigned int:只存 0 以上的整數,最大是 4294967295。
    cout << u << endl;
    u = u + 1;                          //@ 超過上限,繞回 0。unsigned 的這種行為是 C++ 明確規定的。
    cout << u << endl;
    int big = INT_MAX;                  //@ INT_MAX 是 int 的最大值 2147483647。
    cout << big << endl;
    big = big + 1;                      //@ 有號整數溢位在標準裡是「未定義行為」:結果沒有保證。常見的電腦上會繞到最小值。
    cout << big << endl;
    return 0;
}
