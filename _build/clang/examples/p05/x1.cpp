#include <iostream>
using namespace std;

int main() {
    int total = 3725;
    int h = total / 3600;
    int m = total % 3600 / 60;
    int s = total % 60;
    cout << total << " 秒 = " << h << " 時 " << m << " 分 " << s << " 秒" << endl;
    return 0;
}
