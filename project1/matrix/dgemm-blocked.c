#include <stdlib.h>
const char* dgemm_desc = "Blocked dgemm.";

/* This routine performs a dgemm operation
 *
 *  C := C + A * B
 *
 * where A, B, and C are lda-by-lda matrices stored in column-major format.
 * On exit, A and B maintain their input values.
 */

// using padding (this is the version documented in the report)
void square_dgemm(int n, double* A, double* B, double* C) {
    int s = 36; // block size
    int n_pad = ((n + s - 1) / s) * s; // padded n

    // use padded matrices
    double* A_pad = (double*)calloc(n_pad * n_pad, sizeof(double));
    double* B_pad = (double*)calloc(n_pad * n_pad, sizeof(double));

    // Copy data
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            A_pad[j * n_pad + i] = A[j * n + i];
            B_pad[j * n_pad + i] = B[j * n + i];
        }
    }

    // outer loop
    for (int i = 0; i < n_pad; i += s) {
        for (int j = 0; j < n_pad; j += s) {
            for (int k = 0; k < n_pad; k += s) {
                // block loop
                for (int ii = 0; ii < s; ii++) {
                    for (int kk = 0; kk < s; kk++) {
                      // precompute and load A_ik
                      double A_ik = A_pad[(k + kk) * n_pad + i + ii]; 
                      for (int jj = 0; jj < s; jj++) {
                          C[(j + jj) * n + i + ii] += A_ik * B_pad[(j + jj) * n_pad + k + kk];
                      }
                    }
                }
            }
        }
    }

    free(A_pad);
    free(B_pad);
}
