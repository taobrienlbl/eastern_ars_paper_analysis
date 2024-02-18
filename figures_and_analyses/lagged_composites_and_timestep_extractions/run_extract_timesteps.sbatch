#!/bin/bash
#SBATCH --job-name=extract_timesteps
#SBATCH --account=m4374
#SBATCH --qos=regular
#SBATCH --constraint=cpu
#SBATCH --time=00:30:00
#SBATCH --nodes=4
#SBATCH --image=obrientaiu/climate_python_minimal:py3.10

srun -n 512 --cpu_bind=cores shifter python3 -u /global/common/software/m4374/tmp/extract_ar_timesteps.py
