#include <iostream>
#include <string>
using namespace std;

void greet(string name) {                   //@ void:這個函式不回傳任何值,只負責「做一件事」。
    cout << "Hello, " << name << "!" << endl;
}

int main() {
    greet("Mina");
    greet("Leo");
    return 0;
}
