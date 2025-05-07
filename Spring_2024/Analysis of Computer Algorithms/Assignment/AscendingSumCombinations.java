import java.util.Scanner;

class AscendingSumParts {

    // Utility function to print an array arr[] of size 'n'
    public static void printCurrentPartition(int[] arr, int n) {
        // Will not print those partitions in which elements are the same
        for (int i = 0; i < n - 1; i++) {
            if (arr[i] == arr[i + 1]) {
                return;
            }
        }
        for (int i = n - 1; i > 0; i--) {
            System.out.print(arr[i] + "+");
        }
        System.out.println(arr[0]);
    }

    public static void allSumParts(int n) {
        int[] arr = new int[n]; // An array to store a partition
        int k = 0; // The index of the last element included in a partition
        arr[k] = n; // Set the initial value of the first split to the number itself

        // This loop first prints the current partition, then generates the next partition
        // It exits when the current partition contains only ones
        while (true) {
            // Print current partition
            printCurrentPartition(arr, k + 1);

            // Generate next partition

            // Find the rightmost value in arr[] that is not 1
            // Also update remainingValue so we know how much value can be accommodated
            int remainingValue = 0;
            while (k >= 0 && arr[k] == 1) {
                remainingValue += arr[k];
                k--;
            }

            // If k < 0, then all values are 1 so there are no more partitions
            if (k < 0) return;

            // Decrease the arr[k] found above and adjust remainingValue accordingly
            arr[k]--;
            remainingValue++;

            // If remainingValue is more, then the sorted order is violated
            // Divide remainingValue into values of size arr[k] and copy after arr[k]
            while (remainingValue > arr[k]) {
                arr[k + 1] = arr[k];
                remainingValue -= arr[k];
                k++;
            }

            // Copy remainingValue to next position and increment position
            arr[k + 1] = remainingValue;
            k++;
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the input : ");
        int n = scanner.nextInt(); // Read the input number 'n'
        allSumParts(n);
        scanner.close();
    }
}
