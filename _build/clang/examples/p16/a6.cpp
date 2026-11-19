#include <iostream>
#include <stdexcept>                         //@ runtime_error 在 <stdexcept> 裡。
using namespace std;

double divide(double a, double b) {
    if (b == 0) {
        throw runtime_error("除數不能是 0");   //@ throw:自己丟出例外。函式在這裡立刻結束,把錯誤交給呼叫它的人處理。
    }
    return a / b;
}

int main() {
    try {
        cout << divide(10, 4) << endl;
        cout << divide(1, 0) << endl;
        cout << "這一行不會執行" << endl;
    } catch (const exception& e) {
        cout << "錯誤:" << e.what() << endl;
    }
    return 0;
}
