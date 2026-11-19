#include <iostream>
using namespace std;

int main() {
    const double PI = 3.14159;    //@ const:常數。宣告時就要給值,之後不能再改。
    auto count = 42;              //@ auto:讓編譯器依照右邊的值自己決定型態。42 是整數,所以 count 是 int。
    auto price = 9.5;             //@ 9.5 有小數點,所以 price 是 double。
    cout << PI << endl;
    cout << count << endl;
    cout << price << endl;
    cout << sizeof(count) << " " << sizeof(price) << endl;   //@ sizeof 回報型態佔幾個位元組:int 通常是 4,double 通常是 8。
    return 0;
}
