#include <iostream>
using namespace std;

int main() {
    for (int i = 0; i < 5; i++) {        //@ i < 5:從 0 開始、小於 5,剛好 5 圈(0、1、2、3、4)。
        cout << i << " ";
    }
    cout << endl;
    for (int i = 0; i <= 5; i++) {       //@ i <= 5:多了一圈(0 到 5 共 6 圈)。這就是「差一錯誤」。
        cout << i << " ";
    }
    cout << endl;
    return 0;
}
