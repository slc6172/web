#include <iostream>
#include <string>
using namespace std;

int main() {
    string token;
    while (cin >> token) {
        try {
            int n = stoi(token);
            cout << token << " -> " << n * 2 << endl;
        } catch (const exception& e) {
            cout << token << " 不是整數,略過" << endl;
        }
    }
    return 0;
}
