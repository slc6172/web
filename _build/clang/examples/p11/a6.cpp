#include <iostream>
#include <string>
using namespace std;

void greet(string name, string word = "你好") {   //@ 預設參數:呼叫時沒給這個參數,就用 "你好"。預設參數要放在最後面。
    cout << word << "," << name << endl;
}

int add(int a, int b) {
    return a + b;
}

double add(double a, double b) {                  //@ 多載:同樣叫 add,但參數型態不同,編譯器會依你傳的資料挑對的那一個。
    return a + b;
}

int main() {
    greet("Mina");
    greet("Leo", "早安");
    cout << add(2, 3) << endl;
    cout << add(1.5, 2.5) << endl;
    return 0;
}
