#!/bin/bash
#SBATCH --job-name=pi_scaling     # Job name    (default: sbatch)
#SBATCH --output=pi_scaling-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=pi_scaling-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=48       # Number of CPUs per task
#SBATCH --mem-per-cpu=2048       # Memory per CPU
#SBATCH --time=00:05:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

# Compile
make clean
make

# Run the program for OMP_NUM_THREADS equal to 1, 2, 4, 8, ..., 64, 128
for ((i=1; i<=48; i++))
do
  t=$i
  if [ $i -eq 0 ]
  then
    t=1
  fi
  N=$((t * 1000000))
  OMP_NUM_THREADS=$t
  echo "Running with OMP_NUM_THREADS=$OMP_NUM_THREADS and N=$N ..."
  export OMP_NUM_THREADS
  ./pi_serial $N # uncomment for weak scaling
  ./pi_omp_critical $N
  ./pi_omp_reduction $N
done
