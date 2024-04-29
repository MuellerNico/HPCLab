#!/bin/bash
#SBATCH --job-name=scaling      # Job name    (default: sbatch)
#SBATCH --output=scaling-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=scaling-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=64                # Number of tasks
#SBATCH --nodes=64
#SBATCH --ntasks-per-node=1       # 64 for scenario (i), 1 for scenario (ii)
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=1         # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=01:30:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc openmpi
module list

# Compile
make clean
make

for np in 1 2 4 8 16 32 64
do
    echo "Running powermethod with $np processes..."
    mpirun -np $np ./powermethod_rows 3 10000 3000 -0.000001
done
echo "Done."
