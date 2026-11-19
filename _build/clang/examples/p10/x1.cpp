#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "programming language";
    int count = 0;
    for (char ch : s) {
        if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
            count++;
        }
    }
    cout << "母音共有 " << count << " 個" << endl;
    return 0;
}
