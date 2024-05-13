from mandelbrot_task import *
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpi4py import MPI # MPI_Init and MPI_Finalize automatically called
import numpy as np
import sys
import time

# some parameters
MANAGER = 0       # rank of manager
TAG_TASK      = 1 # task       message tag
TAG_TASK_DONE = 2 # tasks done message tag
TAG_DONE      = 3 # done       message tag

def manager(comm, tasks):
    """
    The manager.

    Parameters
    ----------
    comm : mpi4py.MPI communicator
        MPI communicator
    tasks : list of objects with a do_task() method perfroming the task
        List of tasks to accomplish

    Returns
    -------
    ... ToDo ...
    """
    # distribute tasks to workers
    ntasks = len(tasks)
    print(f"Manager has {ntasks} tasks to do")
    for i in range(1, comm.Get_size()):
        if ntasks > 0:
            comm.send(tasks.pop(0), dest=i, tag=TAG_TASK)
            ntasks -= 1
        else:
            break
    
    # receive results from workers
    TasksDoneByWorker = np.zeros(comm.Get_size(), dtype=int)
    while ntasks > 0:
        status = MPI.Status()
        task = comm.recv(source=MPI.ANY_SOURCE, tag=TAG_TASK_DONE)
        sender_rank = status.Get_source()
        print(f"Manager received task from worker {sender_rank}")
        TasksDoneByWorker[sender_rank] += 1

        if ntasks > 0:
            comm.send(tasks.pop(0), sender_rank, tag=TAG_TASK)
            ntasks -= 1
        else:
            comm.send(None, sender_rank, tag=TAG_DONE)

def worker(comm):
    """
    The worker.

    Parameters
    ----------
    comm : mpi4py.MPI communicator
        MPI communicator
    """
    while True:
        task = comm.recv(source=MANAGER, tag=TAG_TASK)
        if task is None:
            break
        task.do_work()
        comm.send((comm.Get_rank(), task), dest=MANAGER, tag=TAG_TASK_DONE)

def readcmdline(rank):
    """
    Read command line arguments

    Parameters
    ----------
    rank : int
        Rank of calling MPI process

    Returns
    -------
    nx : int
        number of gridpoints in x-direction
    ny : int
        number of gridpoints in y-direction
    ntasks : int
        number of tasks
    """
    # report usage
    if len(sys.argv) != 4:
        if rank == MANAGER:
            print("Usage: manager_worker nx ny ntasks")
            print("  nx     number of gridpoints in x-direction")
            print("  ny     number of gridpoints in y-direction")
            print("  ntasks number of tasks")
        sys.exit()

    # read nx, ny, ntasks
    nx = int(sys.argv[1])
    if nx < 1:
        sys.exit("nx must be a positive integer")
    ny = int(sys.argv[2])
    if ny < 1:
        sys.exit("ny must be a positive integer")
    ntasks = int(sys.argv[3])
    if ntasks < 1:
        sys.exit("ntasks must be a positive integer")

    return nx, ny, ntasks


if __name__ == "__main__":

    # get COMMON WORLD communicator, size & rank
    comm    = MPI.COMM_WORLD
    size    = comm.Get_size()
    my_rank = comm.Get_rank()

    # report on MPI environment
    if my_rank == MANAGER:
        print(f"MPI initialized with {size:5d} processes")

    # read command line arguments
    nx, ny, ntasks = readcmdline(my_rank)

    # start timer
    timespent = - time.perf_counter()

    # trying out ... YOUR MANAGER-WORKER IMPLEMENTATION HERE ...
    x_min = -2.
    x_max  = +1.
    y_min  = -1.5
    y_max  = +1.5
    M = mandelbrot(x_min, x_max, nx, y_min, y_max, ny, ntasks)
    tasks = M.get_tasks()
    if my_rank == MANAGER:
        TasksDoneByWorker = np.zeros(size, dtype=int)
        manager(comm, tasks)
        m = M.combine_tasks(tasks)
        plt.imshow(m.T, cmap="gray", extent=[x_min, x_max, y_min, y_max])
        plt.savefig("mandelbrot.png")
    else:
        worker(comm)
    
    """for task in tasks:
        task.do_work()
    m = M.combine_tasks(tasks)"""
    
    # stop timer
    timespent += time.perf_counter()

    # inform that done
    if my_rank == MANAGER:
        print(f"Run took {timespent:f} seconds")
        for i in range(size):
            if i == MANAGER:
                continue
            print(f"Process {i:5d} has done {TasksDoneByWorker[i]:10d} tasks")
        print("Done.")
