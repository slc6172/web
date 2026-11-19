#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> freq;
    string w;
    while (cin >> w) {                       //@ 讀得到東西就繼續;輸入結束(沒有東西可讀)時,條件變成假,迴圈結束。
        freq[w]++;                           //@ 這個字第一次出現:[] 會新增並從 0 開始,++ 變成 1;之後每出現一次就加 1。
    }
    for (auto& kv : freq) {
        cout << kv.first << " " << kv.second << endl;
    }
    return 0;
}
