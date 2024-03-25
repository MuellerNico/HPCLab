#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "walltime.h"
#include <omp.h>

int main(int argc, char *argv[]) {
  int N = 2000000000;
  double up = 1.00000001;
  double Sn = 1.00000001;
  int n;

  /* allocate memory for the recursion */
  double *opt = (double *)malloc((N + 1) * sizeof(double));
  if (opt == NULL) {
    perror("failed to allocate problem size");
    exit(EXIT_FAILURE);
  }

  double time_start = walltime();
  // TODO: YOU NEED TO PARALLELIZE THIS LOOP
  #pragma omp parallel
  {
    int num_threads = omp_get_num_threads();
    int tid = omp_get_thread_num();
    long start_idx = (long)(N+1) * tid / num_threads;
    long end_idx = (long)(N+1) * (tid + 1) / num_threads;    
    double thread_Sn = pow(up, start_idx);
    //printf("Thread %d: start_idx = %ld, end_idx = %ld, thread_Sn = %.16g\n", tid, start_idx, end_idx, thread_Sn);
    // every thread just computes one section
    long i;
    for (i = start_idx; i < end_idx; ++i) {
      opt[i] = thread_Sn;
      thread_Sn *= up;
    }
  }
  Sn = opt[N-1] * up;

  printf("Parallel RunTime  :  %f seconds\n", walltime() - time_start);
  printf("Final Result Sn   :  %.17g \n", Sn);

  double temp = 0.0;
  for (n = 0; n <= N; ++n) {
    temp += opt[n] * opt[n];
  }
  printf("Result ||opt||^2_2 :  %f\n", temp / (double)N);
  printf("\n");

  return 0;
}
