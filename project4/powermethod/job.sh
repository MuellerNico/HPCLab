#!/bin/bash
#SBATCH --job-name=powermeth      # Job name    (default: sbatch)
#SBATCH --output=powermeth-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=powermeth-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=16                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=1         # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:10:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc openmpi
module list

# Compile
make clean
make

# Run the program with 16 MPI processes
mpirun ./powermethod_rows 3 1000 3000 0.0001
