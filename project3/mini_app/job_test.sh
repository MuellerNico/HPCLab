#!/bin/bash
#SBATCH --job-name=PDE      # Job name    (default: sbatch)
#SBATCH --output=PDE-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=PDE-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=128        # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:20:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

# Compile
make clean
make

for((i=0; i<=10; i++))
do 
  OMP_NUM_THREADS=128
  export OMP_NUM_THREADS
  echo "Running with OMP_NUM_THREADS=$OMP_NUM_THREADS, n=$domain_size"
  ./main 2048 1000 0.005
done