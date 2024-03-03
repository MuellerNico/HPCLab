#!/bin/bash

#SBATCH -n 1 # Number of cores
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --mem-per-cpu=1024
#SBATCH --open-mode=truncate

#SBATCH --constraint="EPYC_7H12" # EPYC 7H12 for phase I, EPYC 7763 for phase II

sh mem_hierarchy.sh

