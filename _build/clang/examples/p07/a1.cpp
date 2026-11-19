#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 5; i++) {       //@ for 的小括號有三部分,用分號隔開:① 起點 int i = 1  ② 繼續的條件 i <= 5  ③ 每圈結束後做什麼 i++。
        cout << i << " ";
    }
    cout << endl;
    return 0;
}
