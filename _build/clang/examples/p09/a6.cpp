#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v;                          //@ 空的 vector,之後想放多少都可以。
    int n, x;
    cout << "要輸入幾個數字?";
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> x;
        v.push_back(x);                     //@ 每讀入一個,就加到最後面。陣列做不到:長度要事先固定。
    }
    int best = v[0];
    for (int e : v) {
        if (e > best) {
            best = e;
        }
    }
    cout << "共 " << v.size() << " 個,最大的是 " << best << endl;
    return 0;
}
