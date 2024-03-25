/******************************************************************************
 * FILE: omp_bug4.c
 * DESCRIPTION:
 *   This very simple program causes a segmentation fault.
 ******************************************************************************/
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#define N 1024

int main(int argc, char *argv[]) {
  int nthreads, tid, i, j;
      std::vector<std::vector<float>> a(N, std::vector<float>(N, 0.0));

/* Fork a team of threads with explicit variable scoping */
#pragma omp parallel shared(nthreads) private(i, j, tid, a)
  {

    /* Obtain/print thread info */
    tid = omp_get_thread_num();
    if (tid == 0) {
      nthreads = omp_get_num_threads();
      printf("Number of threads = %d\n", nthreads);
    }
    printf("Thread %d starting...\n", tid);

    /* Each thread works on its own private copy of the array */
    for (i = 0; i < N; i++)
      for (j = 0; j < N; j++)
        (*a)[i][j] = tid + i + j;

    /* For confirmation */
    printf("Thread %d done. Last element= %f\n", tid, (*a)[N - 1][N - 1]);

  } /* All threads join master thread and disband */
}
