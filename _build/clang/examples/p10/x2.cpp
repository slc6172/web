#include <iostream>
#include <string>
using namespace std;

int main() {
    string words[2] = {"level", "hello"};
    for (string w : words) {
        bool same = true;
        int n = w.length();
        for (int i = 0; i < n / 2; i++) {
            if (w[i] != w[n - 1 - i]) {
                same = false;
                break;
            }
        }
        cout << w << (same ? " 是回文" : " 不是回文") << endl;
    }
    return 0;
}
