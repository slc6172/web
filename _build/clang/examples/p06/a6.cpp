#include <iostream>
using namespace std;

int main() {
    int a = 17, b = 5;
    int bigger = (a > b) ? a : b;        //@ 三元運算子:條件 ? 成立時的值 : 不成立時的值。是 if/else 的簡寫,適合「二選一取值」。
    cout << "較大的數:" << bigger << endl;
    return 0;
}
