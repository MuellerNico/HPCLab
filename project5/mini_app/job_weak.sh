#!/bin/bash
#SBATCH --job-name=weak      # Job name    (default: sbatch)
#SBATCH --output=weak-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=weak-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=64               # Number of tasks
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64 
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

for basenx in 64 128 256
do
    for i in 0 1 2 3
    do
    np=$((4**i))
    nx=$(($basenx*(2**i)))
        for rep in 1 2 3 4 5
        do
            echo "Running mini-app with $np processes on $nx x $nx grid..."
            if [ "$np" -eq 1 ]; then
                ./main $nx 1000 0.005  # Running without mpirun for a single process
            else
                mpirun -np $np ./main $nx 1000 0.005
            fi
        done
    done
done
echo "Done."