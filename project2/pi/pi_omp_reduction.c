#include <stdio.h> /* printf */
#include <stdlib.h> /* atol */
#include "walltime.h"

int main(int argc, char *argv[]) {
  long int N = 1000000;
  double sum;

  if ( argc > 1 ) N = atol(argv[1]);

  /* Parallelize with OpenMP using the reduction clause */
  const double time_start = walltime();
  const double h = 1./N;
  sum = 0.;
  #pragma omp parallel for reduction(+:sum)
  for (int i = 0; i < N; ++i) {
    const double x = (i + 0.5)*h;
    const double partial_sum = 4.0 / (1.0 + x*x);
    sum += partial_sum;
  }
  const double pi = sum*h;
  double time = walltime() - time_start;

  printf("pi = \%.15f, N = %9d, time = %.8f secs\n", pi, N, time);
  
  FILE* fptr = fopen("reduction.txt", "a");
  fprintf(fptr, "%.8f\n", time);
  fclose(fptr);  return 0;
}
