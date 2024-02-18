#!/bin/bash
#SBATCH -J check_e5_dataset
#SBATCH --nodes 10
#SBATCH --gpus 40
#SBATCH --constraint gpu
#SBATCH --account m1517_g
#SBATCH --time 01:30:00
#SBATCH -q regular

module use /global/common/software/m1517/teca/perlmutter_gpu/develop/modulefiles/
module load cpe-cuda # required for teca module to load
module swap gcc gcc/11.2.0 # fixes library not found issues with teca
module load teca

time srun -n 160 -G 40 teca_metadata_probe --input_file era5_combined_dataset_large.mcf
