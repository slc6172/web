#include <iostream>
using namespace std;

int main() {
    int age = 18;                      //@ int:整數。
    double height = 170.5;             //@ double:有小數點的數字。
    char grade = 'A';                  //@ char:單一個字元,要用單引號。
    bool passed = true;                //@ bool:只有 true(真)與 false(假)兩種值。
    cout << "年齡:" << age << endl;
    cout << "身高:" << height << endl;
    cout << "等級:" << grade << endl;
    cout << "及格:" << passed << endl; //@ bool 用 cout 印出來是數字:true 印成 1,false 印成 0。
    return 0;
}
