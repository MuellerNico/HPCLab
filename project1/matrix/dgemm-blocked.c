const char* dgemm_desc = "Blocked dgemm.";

/* This routine performs a dgemm operation
 *
 *  C := C + A * B
 *
 * where A, B, and C are lda-by-lda matrices stored in column-major format.
 * On exit, A and B maintain their input values.
 */

// todo: use pragmas, vectorization
void square_dgemm(int n, double* A, double* B, double* C) {
  int s = 36; // this value is specific for the 32 kB L1d cache of the AMD EPYC 7763 processor
  if (n < s) {
    s = n;
  }
  for (int i = 0; i < n; i += s) {
    for (int j = 0; j < n; j += s) {
      for (int k = 0; k < n; k += s) {
        // block loop
        // adjust block size when close to the edge of the matrix
        if (i + s > n) {
          s = n - i;
        }
        if (j + s > n) {
          s = n - j;
        }
        if (k + s > n) {
          s = n - k;
        }
        for (int ii = i; ii < i + s; ++ii) {
          for (int jj = j; jj < j + s; ++jj) {
            for (int kk = k; kk < k + s; ++kk) {
              C[ii + jj * n] += A[ii + kk * n] * B[kk + jj * n];
            }
          }
        }
      }
    }
  }
}
