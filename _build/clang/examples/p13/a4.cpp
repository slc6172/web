#include <iostream>
#include <vector>
#include <algorithm>                         //@ sort、find 等好用的演算法都在 <algorithm> 裡。
#include <functional>                        //@ greater 在 <functional> 裡。
using namespace std;

int main() {
    vector<int> v = {5, 2, 9, 1, 7};
    sort(v.begin(), v.end());                //@ 由小到大排序。v.begin() 是起點、v.end() 是終點,先照著抄:表示「整個 vector」。
    for (int x : v) cout << x << " ";
    cout << endl;
    sort(v.begin(), v.end(), greater<int>());    //@ 多加一個 greater<int>(),變成由大到小。
    for (int x : v) cout << x << " ";
    cout << endl;
    return 0;
}
