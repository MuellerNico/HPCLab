from mpi4py import MPI
import numpy as np

# get comm, size, rank & host name
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
proc = MPI.Get_processor_name()

# sum up and print all ranks from all processes
sum_ranks = comm.reduce(rank, op=MPI.SUM, root=0)
if rank == 0:
    print(f"Lower-case version: {sum_ranks}")

# same but faster upper-case version using buffers
#buf = np.array(rank, dtype='i')
buf = np.int32(rank)
sum_ranks = np.zeros(1, dtype='i')
comm.Reduce(buf, sum_ranks, op=MPI.SUM, root=0)
if rank == 0:
    print(f"Upper-case version: {sum_ranks[0]}")
