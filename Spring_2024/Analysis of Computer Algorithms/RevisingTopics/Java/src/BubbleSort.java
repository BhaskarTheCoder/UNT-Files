class BubbleSort{
    public static void main(String[] args) {
        int[] numberList = {7, 8, 3,2,1,4,5};
        for (int i = 0; i < numberList.length - 1; i++) { // no of the times the loop needs to be iterated.
            for (int j = 0; j < numberList.length - 1; j++) {
                if(numberList[j] > numberList[j+1]) {
                   int currentNumber = numberList[j];
                    numberList[j] = numberList[j+1];
                    numberList[j+1] = currentNumber;
                }
            }
        }
        for (int i = 0; i < numberList.length; i++) {
            System.out.println(numberList[i]);
        }
    }
}
