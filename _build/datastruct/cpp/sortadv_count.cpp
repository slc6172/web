#include <iostream>
#include <utility>
#include <vector>

long long cmp = 0;                           // 數比較次數

void bubbleSort(std::vector<int>& v) {
    int n = static_cast<int>(v.size());
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - 1 - i; ++j) {
            ++cmp;
            if (v[j] > v[j + 1]) {
                std::swap(v[j], v[j + 1]);
            }
        }
    }
}

void merge(std::vector<int>& v, std::vector<int>& tmp, int lo, int mid, int hi) {
    int i = lo, j = mid + 1, k = lo;
    while (i <= mid && j <= hi) {
        ++cmp;
        tmp[k++] = (v[i] <= v[j]) ? v[i++] : v[j++];
    }
    while (i <= mid) {
        tmp[k++] = v[i++];
    }
    while (j <= hi) {
        tmp[k++] = v[j++];
    }
    for (int p = lo; p <= hi; ++p) {
        v[p] = tmp[p];
    }
}

void mergeSort(std::vector<int>& v, std::vector<int>& tmp, int lo, int hi) {
    if (lo >= hi) {
        return;
    }
    int mid = lo + (hi - lo) / 2;
    mergeSort(v, tmp, lo, mid);
    mergeSort(v, tmp, mid + 1, hi);
    merge(v, tmp, lo, mid, hi);
}

void quickSort(std::vector<int>& v, int lo, int hi) {
    if (lo >= hi) {
        return;
    }
    int pivot = v[hi];
    int i = lo;
    for (int j = lo; j < hi; ++j) {
        ++cmp;
        if (v[j] < pivot) {
            std::swap(v[i], v[j]);
            ++i;
        }
    }
    std::swap(v[i], v[hi]);
    quickSort(v, lo, i - 1);
    quickSort(v, i + 1, hi);
}

std::vector<int> makeData(int n, bool sorted) {
    std::vector<int> v(n);
    unsigned int x = 12345;
    for (int i = 0; i < n; ++i) {
        x = x * 1103515245u + 12345u;        // 簡單的偽亂數(固定種子,結果每次一樣)
        v[i] = sorted ? i : static_cast<int>((x >> 16) % 10000);
    }
    return v;
}

int main() {
    const int n = 2000;
    std::vector<int> tmp(n);

    std::vector<int> a = makeData(n, false);
    cmp = 0;
    bubbleSort(a);
    std::cout << "bubble (random)  : " << cmp << "\n";

    a = makeData(n, false);
    cmp = 0;
    mergeSort(a, tmp, 0, n - 1);
    std::cout << "merge  (random)  : " << cmp << "\n";

    a = makeData(n, false);
    cmp = 0;
    quickSort(a, 0, n - 1);
    std::cout << "quick  (random)  : " << cmp << "\n";

    a = makeData(n, true);
    cmp = 0;
    quickSort(a, 0, n - 1);
    std::cout << "quick  (sorted)  : " << cmp << "\n";
}
