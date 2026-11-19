#include <iostream>
using namespace std;

int main() {
    int age, student;
    cout << "年齡與是否學生(1 是、0 否):";
    cin >> age >> student;
    if (age >= 18) {
        if (student == 1) {              //@ 條件裡面還可以再放條件,這叫巢狀。只有外層成立才會進來檢查。
            cout << "學生票" << endl;
        } else {
            cout << "全票" << endl;
        }
    } else {
        cout << "兒童票" << endl;
    }
    return 0;
}
