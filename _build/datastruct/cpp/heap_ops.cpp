#include <iostream>
#include <utility>
#include <vector>

void siftUp(std::vector<int>& h, int i) {
    while (i > 0) {
        int parent = (i - 1) / 2;
        if (h[parent] >= h[i]) {
            break;
        }
        std::swap(h[parent], h[i]);
        i = parent;
    }
}

void push(std::vector<int>& h, int val) {
    h.push_back(val);
    siftUp(h, static_cast<int>(h.size()) - 1);
}

void siftDown(std::vector<int>& h, int i) {
    int n = static_cast<int>(h.size());
    while (true) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        if (left < n && h[left] > h[largest]) {
            largest = left;
        }
        if (right < n && h[right] > h[largest]) {
            largest = right;
        }
        if (largest == i) {
            break;
        }
        std::swap(h[i], h[largest]);
        i = largest;
    }
}

int pop(std::vector<int>& h) {
    int top = h[0];
    h[0] = h.back();
    h.pop_back();
    if (!h.empty()) {
        siftDown(h, 0);
    }
    return top;
}

void print(const std::vector<int>& h) {
    for (int x : h) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}

int main() {
    std::vector<int> h;
    for (int v : {5, 3, 8, 1, 9, 2}) {
        push(h, v);
        std::cout << "push " << v << ": ";
        print(h);
    }
    std::cout << "pop " << pop(h) << ": ";
    print(h);
    std::cout << "pop " << pop(h) << ": ";
    print(h);
    std::cout << "剩下依序取出: ";
    while (!h.empty()) {
        std::cout << pop(h) << " ";
    }
    std::cout << "\n";
}
