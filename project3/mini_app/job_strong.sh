#!/bin/bash
#SBATCH --job-name=PDE      # Job name    (default: sbatch)
#SBATCH --output=PDE-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=PDE-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=32       # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:10:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

# Compile
make clean
make

# Run for domain sizes 64, 128, 256, 512, 1024
for ((domain_size=64; domain_size<=1024; domain_size*=2))
do
  # Run the program for OMP_NUM_THREADS equal to 1, 2, 4, 8, 16
  for ((i=0; i<=4; i++))
  do
    OMP_NUM_THREADS=$((2**i))
    export OMP_NUM_THREADS
    echo "Running with OMP_NUM_THREADS=$OMP_NUM_THREADS, n=$domain_size"
    ./main $domain_size 1000 0.005
  done
done
