#!/bin/bash
#SBATCH --job-name=mandel      # Job name    (default: sbatch)
#SBATCH --output=mandel-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=mandel-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=128       # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:05:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

# Compile
make clean
make

# Run the program with 8 OpenMP threads
export OMP_NUM_THREADS=128
echo "[NO SCALING] Running with OMP_NUM_THREADS=$OMP_NUM_THREADS"
./mandel_seq