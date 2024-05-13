from mpi4py import MPI
import numpy as np

# get comm, size, rank & host name
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
proc = MPI.Get_processor_name()

# 2D periodic cartesian topology
dims = MPI.Compute_dims(size, 2)
comm_cart = comm.Create_cart(dims, periods=[True, True], reorder=True)
coords = comm_cart.Get_coords(rank)
west, east = comm_cart.Shift(0, 1)  # Neighbors along the first dimension (x)
south, north = comm_cart.Shift(1, 1) 
print(f"Rank {rank} has coordinates {coords} and NESW neighbours {north}, {east}, {south}, {west}")

comm_cart.Barrier()

#exchange rank with neighbours without blocking
north_buf = np.zeros(1, dtype='i')
south_buf = np.zeros(1, dtype='i')
east_buf = np.zeros(1, dtype='i')
west_buf = np.zeros(1, dtype='i')
reqs = []
reqs.append(comm_cart.Irecv(north_buf, source=north, tag=1))
reqs.append(comm_cart.Irecv(south_buf, source=south, tag=2))
reqs.append(comm_cart.Irecv(east_buf, source=east, tag=3))
reqs.append(comm_cart.Irecv(west_buf, source=west, tag=4))
reqs.append(comm_cart.Isend(np.int32(rank), dest=north, tag=2))
reqs.append(comm_cart.Isend(np.int32(rank), dest=south, tag=1))
reqs.append(comm_cart.Isend(np.int32(rank), dest=east, tag=4))
reqs.append(comm_cart.Isend(np.int32(rank), dest=west, tag=3))

MPI.Request.waitall(reqs)
comm_cart.Barrier()

print(f"Rank {rank} has received from NESW neighbours {north_buf}, {east_buf}, {south_buf}, {west_buf}")

if rank == 0:
    print("\n2D grid of processes:")
    for i in range(dims[1]):
        for j in range(dims[0]):
            print(f"{comm_cart.Get_cart_rank([j, i]):3}", end=" ")
        print()
    print()
