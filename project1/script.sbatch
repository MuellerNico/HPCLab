#!/bin/bash

#SBATCH -n 1
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --mem-per-cpu=1024
#SBATCH --output="out.txt"
#SBATCH --open-mode=truncate

srun ./hello_world