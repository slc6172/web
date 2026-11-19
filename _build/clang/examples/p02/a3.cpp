#include <iostream>                              //@ 引入「輸入輸出」工具箱。沒有這行,編譯器不認識 cout。

int main() {                                     //@ 每支程式都從 main 開始執行。大括號圈住它要做的事。
    std::cout << "Hello, C++!" << std::endl;     //@ cout 是「螢幕輸出」,<< 把右邊的東西送過去,endl 換行。整行以分號結束。
    std::cout << "我正在學 C++" << std::endl;    //@ 想印幾行,就寫幾個 cout 敘述。程式由上往下一行一行執行。
    return 0;                                    //@ 告訴作業系統「我順利結束了」,0 代表成功。
}                                                //@ 結尾的大括號,和 main 那行的左大括號成對。
