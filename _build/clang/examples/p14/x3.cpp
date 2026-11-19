#include <iostream>
using namespace std;

class BankAccount {
private:
    int balance = 0;
public:
    void deposit(int amount) {
        if (amount > 0) {
            balance += amount;
        }
    }
    bool withdraw(int amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            return true;
        }
        return false;
    }
    int getBalance() {
        return balance;
    }
};

int main() {
    BankAccount acc;
    acc.deposit(1000);
    if (acc.withdraw(300)) {
        cout << "提領成功,餘額 " << acc.getBalance() << endl;
    }
    if (!acc.withdraw(5000)) {
        cout << "餘額不足,餘額仍是 " << acc.getBalance() << endl;
    }
    return 0;
}
