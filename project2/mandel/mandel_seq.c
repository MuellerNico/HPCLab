#include <stdio.h>
#include <stdlib.h>

#include <sys/time.h>
#include <time.h>
#include <unistd.h>

#include "consts.h"
#include "pngwriter.h"
#include "walltime.h"
#include <omp.h>

int main(int argc, char **argv) {
  png_data *pPng = png_create(IMAGE_WIDTH, IMAGE_HEIGHT);

  double x, y, x2, y2, cx, cy;

  double fDeltaX = (MAX_X - MIN_X) / (double)IMAGE_WIDTH;
  double fDeltaY = (MAX_Y - MIN_Y) / (double)IMAGE_HEIGHT;

  long nTotalIterationsCount = 0;

  long i, j;

  double time_start = walltime();
  // do the calculation
  cy = MIN_Y;
  #pragma omp parallel for reduction(+:nTotalIterationsCount)
  for (j = 0, cy = MIN_Y; j < IMAGE_HEIGHT; j++, cy += fDeltaY) {
    cx = MIN_X;
    for (i = 0, cx = MIN_X; i < IMAGE_WIDTH; i++, cx += fDeltaX) {
       // x and y are the real and imaginary parts of the complex number z = x + i * y
      x = cx; // z1
      y = cy; // z1
      x2 = x * x;
      y2 = y * y;
      // compute the orbit z, f(z), f^2(z), f^3(z), ...
      // count the iterations until the orbit leaves the circle |z|=2.
      // stop if the number of iterations exceeds the bound MAX_ITERS.
      int n = 0;
      // TODO
      // >>>>>>>> CODE IS MISSING
      while (x2 + y2 <= 4 && n < MAX_ITERS) {
              y = 2 * x * y + cy;
              x = x2 - y2 + cx;
              x2 = x * x;
              y2 = y * y;
              n++;
       }
       #pragma omp atomic
       nTotalIterationsCount += n;
      // <<<<<<<< CODE IS MISSING
      // n indicates if the point belongs to the mandelbrot set
      // plot the number of iterations at point (i, j)
      int c = ((long)n * 255) / MAX_ITERS;
      #pragma omp critical
      png_plot(pPng, i, j, c, c, c);
      //cx += fDeltaX;
      // keep track of total number of iterations
    }
    //cy += fDeltaY;
  }
  double time_end = walltime();

  // print benchmark data
  printf("Total time:                 %g seconds\n",
         (time_end - time_start));
  printf("Image size:                 %ld x %ld = %ld Pixels\n",
         (long)IMAGE_WIDTH, (long)IMAGE_HEIGHT,
         (long)(IMAGE_WIDTH * IMAGE_HEIGHT));
  printf("Total number of iterations: %ld\n", nTotalIterationsCount);
  printf("Avg. time per pixel:        %g seconds\n",
         (time_end - time_start) / (double)(IMAGE_WIDTH * IMAGE_HEIGHT));
  printf("Avg. time per iteration:    %g seconds\n",
         (time_end - time_start) / (double)nTotalIterationsCount);
  printf("Iterations/second:          %g\n",
         nTotalIterationsCount / (time_end - time_start));
  // assume there are 8 floating point operations per iteration
  printf("MFlop/s:                    %g\n",
         nTotalIterationsCount * 8.0 / (time_end - time_start) * 1.e-6);

  png_write(pPng, "mandel.png");
  return 0;
}
