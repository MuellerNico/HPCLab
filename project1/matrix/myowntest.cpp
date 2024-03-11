#include <iostream>
#include <cstdlib>
#include "dgemm-blocked.h" // Assuming "dgemm_blocked.h" is located in the "matrix" directory

//extern void dgemm_blocked(int n, double* A, double* B, double* C);

int main() {
    int n = 37; // Size of the matrices

    // Allocate memory for matrices A, B, and C
    double* A = (double*)malloc(n * n * sizeof(double));
    double* B = (double*)malloc(n * n * sizeof(double));
    double* C = (double*)malloc(n * n * sizeof(double));

    // Initialize matrices A and B
    for (int i = 0; i < n * n; i++) {
        A[i] = i + 1;
        B[i] = n * n - i;
    }

    // Call the dgemm_blocked function
    square_dgemm(n, A, B, C);

    // Print the result
    printf("Matrix C:\n");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%f ", C[i * n + j]);
        }
        printf("\n");
    }

    // Free the allocated memory
    free(A);
    free(B);
    free(C);

    return 0;
}