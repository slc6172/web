#include <iostream>
using namespace std;

int main() {
    int y = 2024;
    cout << y << ":" << ((y % 4 == 0 && y % 100 != 0) || y % 400 == 0) << endl;
    y = 1900;
    cout << y << ":" << ((y % 4 == 0 && y % 100 != 0) || y % 400 == 0) << endl;
    y = 2000;
    cout << y << ":" << ((y % 4 == 0 && y % 100 != 0) || y % 400 == 0) << endl;
    return 0;
}
