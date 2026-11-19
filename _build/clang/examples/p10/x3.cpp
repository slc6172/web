#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "Hello";
    string r = "";
    for (int i = s.length() - 1; i >= 0; i--) {
        r += s[i];
    }
    cout << r << endl;
    return 0;
}
