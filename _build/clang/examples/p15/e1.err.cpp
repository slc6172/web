#include <iostream>
#include <string>
using namespace std;

class Animal {
protected:
    string name;
public:
    Animal(string n) { name = n; }
};

int main() {
    Animal a("Rex");
    cout << a.name << endl;
    return 0;
}
