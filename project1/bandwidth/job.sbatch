#!/bin/bash

#SBATCH -n 1 # Number of cores
#SBATCH -N 1 # Number of nodes
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --mem-per-cpu=8192
#SBATCH --open-mode=truncate

#SBATCH --constraint="EPYC_7763" # EPYC 7H12 for phase I, EPYC 7763 for phase II

module load gcc
module list

gcc -O3 -march=native -DSTREAM_ARRAY_SIZE=128000000 stream.c -o stream
srun ./stream

