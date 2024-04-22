#include <mpi.h> // MPI
#include <stdio.h>

int main(int argc, char *argv[]) {

  // Initialize MPI, get size and rank
  int size, rank;
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);

  // IMPLEMENT: Ring sum algorithm
  int sum = rank; // initialize sum

  int in = 0; // value to receive
  int out = rank; // value to send

  for (int i = 0; i < size - 1; i++) {
    if (rank == 0) { // avoid deadlock by sending in a circular fashion
      MPI_Send(&out, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
      MPI_Recv(&in, 1, MPI_INT, size-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      sum += in;
      out = in;
    } else {
      MPI_Recv(&in, 1, MPI_INT, rank-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      MPI_Send(&out, 1, MPI_INT, (rank+1)%size, 0, MPI_COMM_WORLD);
      sum += in;
      out = in;
    }
  }

  printf("Process %i: Sum = %i, Size = %i\n", rank, sum, size);

  // Finalize MPI
  MPI_Finalize();

  return 0;
}
