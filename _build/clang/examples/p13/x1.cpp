#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> freq;
    string w;
    while (cin >> w) {
        freq[w]++;
    }
    for (auto& kv : freq) {
        cout << kv.first << ": " << kv.second << endl;
    }
    return 0;
}
