#!/bin/bash

#optional arguments:
#  -h, --help            show this help message and exit
#  -N NODES, --nodes NODES
#                        Number of nodes
#  -s {DJF,MAM,JJA,SON,annual,all}, --season {DJF,MAM,JJA,SON,annual,all}
#                        Season
#  -p PROCS_PER_GPU, --procs-per-gpu PROCS_PER_GPU
#                        Number of processors per GPU
#  -n PROCS_PER_NODE, --procs-per-node PROCS_PER_NODE
#                        Total number of processors per node
#  -a {teca_bard_v1.0.1}, --algorithm {teca_bard_v1.0.1}
#                        ARTMIP Algorithm to use
#  -l {bloomington}, --location {bloomington}
#                        Location name
#  -g GPUS_PER_NODE, --gpus-per-node GPUS_PER_NODE
#                        Number of GPUs per node
#  -t TIME, --time TIME  Time (minutes) of SLURM request
#  -d OUTPUT_DIR, --output-dir OUTPUT_DIR
#                        Output directory
#  -o OUTPUT_TEMPLATE, --output-template OUTPUT_TEMPLATE
#                        Output template; must contain the {season},
#                        {location}, and {algorithm} templates
#

LOCATION="dc"
ALGORITHM="teca_bard_v1.0.1"

python3 generate_and_submit_sbatch_scripts.py \
    -N 4 \
    -n 192 \
    -t 15 \
    -d "/global/cfs/cdirs/m1517/cascade/taobrien/midwest_ar_composites/figures_and_analyses/composites_restriped_temporal_reduction/${LOCATION}_${ALGORITHM}" \
    -a ${ALGORITHM} \
    -l ${LOCATION} \
    -f "generate_composites_from_restriped_data.sbatch.template" \
    -r '/pscratch/sd/t/taobrien/midwest_ar_composites/era5_combined_north_america/era5_combined_north_america_.*\.nc' \
    -s all
    


