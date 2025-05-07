import java.util.*;
/*
1 5 7 9 10 11 21 41 70 105 95 81 79 70 40 15 9 6 10 12 13 20 32 68 63 59 55 25 29 30 29
*/
public class Spiral2DArray {
    public static void main(String[] args) {
        Scanner scanInput = new Scanner(System.in);
        int[][] matrix = new int[5][6];
        int n = matrix.length;
        int m = matrix[0].length;

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m ; j++) {
                matrix[i][j] = scanInput.nextInt();
            }
        }
        int row_start = 0 ;
        int row_end = n - 1;
        int column_start = 0;
        int column_end = m - 1 ;
        
        while(row_start <= row_end && column_start <= column_end){
            for (int i = column_start; i <=column_end; i++) {
                System.out.print(matrix[row_start][i]+ " ");
            }
            row_start++;
            for (int i = row_start; i <=row_end; i++) {
                System.out.print(matrix[i][column_end]+ " ");
            }
            column_end--;
            for (int i = column_end; i >=column_start; i--) {
                System.out.print(matrix[row_end][i]+ " ");
            }
            row_end--;
            for (int i = row_end; i >=row_start; i--) {
                System.out.print(matrix[i][column_start]+ " ");
            }
            column_start++;
        }
        scanInput.close();
    }
}
