#include<stdio.h>

int BinSearch(int arr[], int start, int end, int val) {
	int low = start;
	int high = end;
	int mid = 0;
	while (low <= high) {
		mid = high + (low - high) / 2;
		if (arr[mid] == val)
			return mid;
		else if (arr[mid] < val) {
			low = mid + 1;
		}
		else {
			high = mid - 1;
		}
	}
	return 0;
}

int main() {

	int arr[] = { 10, 11, 12, 13 };
	int val = 10;
	printf("%d\n", BinSearch(arr, 0, 3, 10));
	printf("%d\n", BinSearch(arr, 0, 3, 13));
	printf("%d\n", BinSearch(arr, 0, 3, 1));
	return 0;
}
