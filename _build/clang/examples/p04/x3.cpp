#include <iostream>
#include <string>
using namespace std;

int main() {
    int age;
    string name;
    cout << "年齡:";
    cin >> age;
    cin.ignore(1000, '\n');
    cout << "全名:";
    getline(cin, name);
    cout << name << ",你 " << age << " 歲" << endl;
    return 0;
}
