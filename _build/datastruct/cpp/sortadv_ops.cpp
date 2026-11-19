#include <iostream>
#include <utility>
#include <vector>

void merge(std::vector<int>& v, std::vector<int>& tmp, int lo, int mid, int hi) {
    int i = lo;
    int j = mid + 1;
    int k = lo;
    while (i <= mid && j <= hi) {
        if (v[i] <= v[j]) {
            tmp[k++] = v[i++];
        } else {
            tmp[k++] = v[j++];
        }
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

int partition(std::vector<int>& v, int lo, int hi) {
    int pivot = v[hi];
    int i = lo;
    for (int j = lo; j < hi; ++j) {
        if (v[j] < pivot) {
            std::swap(v[i], v[j]);
            ++i;
        }
    }
    std::swap(v[i], v[hi]);
    return i;
}

void quickSort(std::vector<int>& v, int lo, int hi) {
    if (lo >= hi) {
        return;
    }
    int p = partition(v, lo, hi);
    quickSort(v, lo, p - 1);
    quickSort(v, p + 1, hi);
}

void print(const std::vector<int>& v) {
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}

int main() {
    std::vector<int> data = {38, 27, 43, 3, 9, 82, 10};
    int n = static_cast<int>(data.size());

    std::vector<int> a = data;
    std::vector<int> tmp(a.size());
    mergeSort(a, tmp, 0, n - 1);
    print(a);

    std::vector<int> b = data;
    quickSort(b, 0, n - 1);
    print(b);
}
