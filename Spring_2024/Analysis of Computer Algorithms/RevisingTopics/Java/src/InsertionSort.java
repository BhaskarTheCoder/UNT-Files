public class InsertionSort {
    public static void main(String[] args) {
        int[] numberList = {7, 8, 3,2,1,4,5};
        int minValue  = 0;
        for (int i = 0; i < numberList.length - 2; i++) {
            minValue = numberList[i];
            for (int j = i+1; j < numberList.length-2; j++) {
                if(minValue > numberList[j]){
                    minValue = numberList[j];
                }
            }
            int temp = numberList[i];
            numberList[i] = minValue;
            numberList[numberList.length] = temp;
        }
        // for (int i = 0; i < numberList.length; i++) {
        //     System.out.println(numberList[i]);
        // }
    }
}
