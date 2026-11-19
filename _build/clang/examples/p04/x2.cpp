#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double price;
    int qty;
    cout << "單價與數量:";
    cin >> price >> qty;
    cout << fixed << setprecision(2);
    cout << "總價:" << price * qty << endl;
    return 0;
}
