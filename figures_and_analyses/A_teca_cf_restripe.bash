#!/bin/bash
#SBATCH -C cpu
#SBATCH -N 40
#SBATCH -q regular
#SBATCH -J teca_cf_restripe
#SBATCH -t 00:60:00
#SBATCH -A m1517
#SBATCH -oe
#SBATCH -o teca_cf_restripe.%j.out

# load teca
module use /global/common/software/m1517/teca/perlmutter_cpu/develop/modulefiles/
module load teca

# set the output variables
export POINT_ARRAYS="T Z Q U V PV W VAR_2T SP TCW CAPE VIWVE VIWVN"

# set the MCF file
export MCF_FILE=/global/cfs/cdirs/m1517/cascade/taobrien/midwest_ar_composites/figures_and_analyses/era5_combined_dataset_large.mcf
#export MCF_FILE=/global/cfs/cdirs/m1517/cascade/taobrien/midwest_ar_composites/figures_and_analyses/era5_combined_dataset_large_test.mcf

# create the output directory
export OUT_DIR=${SCRATCH}/midwest_ar_composites/era5_combined_north_america/
mkdir -p ${OUT_DIR}

# use restripe to extract data for the north american continent and a bit into the pacific and atlantic oceans
time srun -n 1280 \
    teca_cf_restripe \
        --input_file=${MCF_FILE} \
        --output_file=${OUT_DIR}/era5_combined_north_america_%t%.nc \
        --file_layout=daily \
        --bounds 215 325 15 65 50 1000 \
        --point_arrays ${POINT_ARRAYS} \
        --normalize_coordinates \
        --verbose
#        --first_step 0 \
#        --last_step 1535 \




