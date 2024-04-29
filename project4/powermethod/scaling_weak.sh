#!/bin/bash
#SBATCH --job-name=scalingweak      # Job name    (default: sbatch)
#SBATCH --output=scalingweak-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=scalingweak-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=64                # Number of tasks
#SBATCH --nodes=64                  # 1 for scenario (i), 64 for scenario (ii)
#SBATCH --ntasks-per-node=1       # 64 for scenario (i), 1 for scenario (ii)
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=1         # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:30:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc openmpi
module list

# Compile
make clean
make

for i in 0 1 2 3 4 5 6
do
    n=$(echo "3000*(1.4142^$i)" | bc -l)
    np=$((2**i))
    echo "Running powermethod with $np processes and n = $n..."
    mpirun -np $np ./powermethod_rows 3 $n 3000 -0.000001
done
echo "Done."
