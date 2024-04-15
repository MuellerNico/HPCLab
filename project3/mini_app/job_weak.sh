#!/bin/bash
#SBATCH --job-name=PDE      # Job name    (default: sbatch)
#SBATCH --output=PDE-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=PDE-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=64        # Number of CPUs per task
#SBATCH --mem-per-cpu=2048        # Memory per CPU
#SBATCH --time=00:20:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

# Compile
make clean
make
for ((base_res=64; base_res<=256; base_res*=2))
do
  for ((i=0; i<=3; i++))
  do
    OMP_NUM_THREADS=$((4**i))
    domain_size=$((2**i*base_res))
    export OMP_NUM_THREADS
    echo "Running with OMP_NUM_THREADS=$OMP_NUM_THREADS, n=$domain_size"
    ./main $domain_size 1000 0.005
  done
done
