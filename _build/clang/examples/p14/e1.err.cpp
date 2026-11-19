#include <iostream>
using namespace std;

class BankAccount {
private:
    int balance = 0;
public:
    void deposit(int amount) {
        balance += amount;
    }
};

int main() {
    BankAccount acc;
    acc.balance = 1000000;
    cout << "我變有錢了" << endl;
    return 0;
}
