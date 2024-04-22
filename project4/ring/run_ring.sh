#!/bin/bash
#SBATCH --job-name=ring      # Job name    (default: sbatch)
#SBATCH --output=ring-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=ring-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=4                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=1         # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:05:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc openmpi
module list

# Compile
make clean
make

# Run the program with 4 MPI processes
mpirun ./ring_sum
