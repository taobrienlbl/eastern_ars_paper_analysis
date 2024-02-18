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

python3 generate_and_submit_sbatch_scripts.py \
    -N 10 \
    -t 240 \
    -d "/global/cfs/cdirs/m1517/cascade/taobrien/midwest_ar_composites/figures_and_analyses/composites_new_temporal_reduction/bloomington_teca_bard" \
    -s all
    


