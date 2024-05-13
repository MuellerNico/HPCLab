#!/bin/bash
#SBATCH --job-name=strong      # Job name    (default: sbatch)
#SBATCH --output=strong-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=strong-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=16                # Number of tasks
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16 
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=1         # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:25:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc openmpi
module list

for ((warmup=0; warmup<10; warmup+=1))
do
    mpirun -np 16 ./main 128 1000 0.005
done
echo "Warmup finished."

for nx in 64 128 256 512 1024
do
    for np in 1 2 4 8 16
    do
        for rep in 1 2 3 4 5
        do
            echo "Running mini-app with $np processes on $nx x $nx grid..."
            mpirun -np $np ./main $nx 1000 0.005
        done
    done
done
echo "Done."