#!/bin/bash

#SBATCH -n 2 # Number of cores
#SBATCH -N 2 # Number of nodes
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --mem-per-cpu=1024
#SBATCH --open-mode=truncate

#SBATCH --constraint="EPYC_7763"

module load gcc
module list
srun ./helloworld