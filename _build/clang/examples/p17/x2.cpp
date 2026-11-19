#include <iostream>
#include <memory>
#include <vector>
using namespace std;

class Animal {
public:
    virtual void speak() { cout << "(某種聲音)" << endl; }
    virtual ~Animal() {}
};

class Dog : public Animal {
public:
    void speak() override { cout << "汪汪!" << endl; }
};

class Cat : public Animal {
public:
    void speak() override { cout << "喵喵!" << endl; }
};

int main() {
    vector<unique_ptr<Animal>> zoo;
    zoo.push_back(make_unique<Dog>());
    zoo.push_back(make_unique<Cat>());
    for (auto& a : zoo) {
        a->speak();
    }
    return 0;
}
