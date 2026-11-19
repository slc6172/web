#include <iostream>
using namespace std;

class Animal {
public:
    virtual void speak() {                   //@ virtual:告訴編譯器「這個函式,執行時要依物件真正的類別來決定」。
        cout << "(某種聲音)" << endl;
    }
};

class Dog : public Animal {
public:
    void speak() override {                  //@ override:明確表示「我要覆寫基底類別的 virtual 函式」。寫錯名字時編譯器會提醒。
        cout << "汪汪!" << endl;
    }
};

int main() {
    Dog d;
    d.speak();
    Animal* a = &d;
    a->speak();                              //@ 現在 a 雖然是 Animal 指標,實際指著 Dog,所以執行 Dog 的版本。這就是多型。
    return 0;
}
