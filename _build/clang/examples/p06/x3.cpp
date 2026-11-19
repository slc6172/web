#include <iostream>
using namespace std;

int main() {
    int a, b;
    char op;
    cout << "算式(例如 12 + 30):";
    cin >> a >> op >> b;
    switch (op) {
        case '+':
            cout << a + b << endl;
            break;
        case '-':
            cout << a - b << endl;
            break;
        case '*':
            cout << a * b << endl;
            break;
        case '/':
            cout << a / b << endl;
            break;
        default:
            cout << "不支援的運算子" << endl;
    }
    return 0;
}
