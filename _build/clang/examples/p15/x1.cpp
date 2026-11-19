#include <iostream>
using namespace std;

class Shape {
public:
    virtual double area() {
        return 0;
    }
};

class Circle : public Shape {
private:
    double r;
public:
    Circle(double radius) { r = radius; }
    double area() override {
        return 3.14159 * r * r;
    }
};

class Rectangle : public Shape {
private:
    double w, h;
public:
    Rectangle(double width, double height) { w = width; h = height; }
    double area() override {
        return w * h;
    }
};

int main() {
    Circle c(2);
    Rectangle r(3, 4);
    Shape* shapes[2] = {&c, &r};
    for (Shape* s : shapes) {
        cout << "面積:" << s->area() << endl;
    }
    return 0;
}
