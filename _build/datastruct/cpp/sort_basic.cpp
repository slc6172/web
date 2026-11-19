#include <iostream>
#include <utility>
#include <vector>

void bubbleSort(std::vector<int>& v) {
    int n = static_cast<int>(v.size());
    for (int i = 0; i < n - 1; ++i) {
        bool swapped = false;
        for (int j = 0; j < n - 1 - i; ++j) {
            if (v[j] > v[j + 1]) {
                std::swap(v[j], v[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) {
            break;
        }
    }
}

void selectionSort(std::vector<int>& v) {
    int n = static_cast<int>(v.size());
    for (int i = 0; i < n - 1; ++i) {
        int minIdx = i;
        for (int j = i + 1; j < n; ++j) {
            if (v[j] < v[minIdx]) {
                minIdx = j;
            }
        }
        std::swap(v[i], v[minIdx]);
    }
}

void insertionSort(std::vector<int>& v) {
    int n = static_cast<int>(v.size());
    for (int i = 1; i < n; ++i) {
        int key = v[i];
        int j = i - 1;
        while (j >= 0 && v[j] > key) {
            v[j + 1] = v[j];
            --j;
        }
        v[j + 1] = key;
    }
}

void print(const std::vector<int>& v) {
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}

int main() {
    std::vector<int> data = {5, 2, 9, 1, 7, 3};
    std::vector<int> a = data;
    std::vector<int> b = data;
    std::vector<int> c = data;
    bubbleSort(a);
    selectionSort(b);
    insertionSort(c);
    print(a);
    print(b);
    print(c);
}
