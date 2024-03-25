#!/bin/bash
#SBATCH --job-name=quicksort      # Job name
#SBATCH --output=quicksort-%j.out # Output file
#SBATCH --error=quicksort-%j.err  # Error file
#SBATCH --ntasks=1               # Number of tasks
#SBATCH --constraint=EPYC_7763   # Select node with CPU
#SBATCH --cpus-per-task=128      # Number of CPUs per task
#SBATCH --mem-per-cpu=1024       # Memory per CPU
#SBATCH --time=00:15:00          # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

# Compile
make clean
make

# set threshold manually in .c file

for ((N=1000000; N<=1000000000; N*=10)) # problem size
do
  for ((i=0; i<=7; i++)) # number of threads
  do
    OMP_NUM_THREADS=$((2**i))
    echo "Running with OMP_NUM_THREADS=$OMP_NUM_THREADS, N=$N"
    export OMP_NUM_THREADS
    ./quicksort $N
  done
done