#include <stdio.h> /* printf */
#include <stdlib.h> /* atol */
#include "walltime.h"
#include <omp.h> // OpenMP

int main(int argc, char *argv[]) {
  long int N = 1000000;

  if ( argc > 1 ) N = atol(argv[1]);

  /* Parallelize with OpenMP using the critical directive */
  const double time_start = walltime();
  const double h = 1./N;
  double sum = 0.;
  #pragma omp parallel
  {
    double partial_sum = 0.;
    int nthreads = omp_get_num_threads();
    int tid = omp_get_thread_num();
    int i_beg = tid*N/nthreads;
    int i_end = (tid + 1)*N/nthreads;
    for (int i = i_beg; i < i_end; ++i){
      const double x = (i + 0.5)*h;
      partial_sum += 4.0 / (1.0 + x*x);
    }
    #pragma omp critical
    sum += partial_sum;
  }
  const double pi = sum*h;
  const double time = walltime() - time_start;

  printf("pi = \%.15f, N = %9d, time = %.8f secs\n", pi, N, time);
  
  FILE* fptr = fopen("critical.txt", "a");
  fprintf(fptr, "%.8f\n", time);
  fclose(fptr);
  return 0;
}
