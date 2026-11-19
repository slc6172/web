#include <iostream>
using namespace std;

class BankAccount {                          //@ class:和 struct 幾乎一樣,差別是預設成員是 private(私有)。
private:                                     //@ private:只有這個類別自己的成員函式能碰的區域。
    int balance = 0;                         //@ 餘額藏在裡面,外面不能直接改。= 0 是預設的起始值。
public:                                      //@ public:外面也能使用的區域。
    void deposit(int amount) {
        if (amount > 0) {                    //@ 所有修改都要經過這裡,所以我們可以檢查:不允許存入負數。
            balance += amount;
        }
    }
    int getBalance() {                       //@ 提供一個「只讀」的視窗,讓外面看得到餘額。
        return balance;
    }
};

int main() {
    BankAccount acc;
    acc.deposit(500);
    acc.deposit(-100);                       //@ 這次存入是負數,deposit 會拒絕,餘額不變。
    cout << "餘額:" << acc.getBalance() << endl;
    return 0;
}
