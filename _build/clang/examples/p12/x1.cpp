#include <iostream>
#include <string>
using namespace std;

void swapStr(string& a, string& b) {
    string temp = a;
    a = b;
    b = temp;
}

int main() {
    string s1 = "apple", s2 = "banana";
    swapStr(s1, s2);
    cout << s1 << " " << s2 << endl;
    return 0;
}
