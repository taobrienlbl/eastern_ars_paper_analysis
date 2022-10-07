#!/usr/bin/env python3
import os
import argparse

from pandas import describe_option

parser = argparse.ArgumentParser()
parser.add_argument("-N", "--nodes", type=int, help="Number of nodes", default=4)
parser.add_argument("-s","--season",type=str, help="Season",choices=["DJF","MAM","JJA","SON","annual","all"], default = "all")
parser.add_argument("-p","--procs-per-gpu",type=int, help="Number of processors per GPU", default = 8)
parser.add_argument("-a","--algorithm",type=str, help="TECA Algorithm to use", choices=["teca_bard_v1.0.1"], default = "teca_bard_v1.0.1")
parser.add_argument("-t","--time",type=int, help="Time (minutes) of SLURM request", default = 240)
parser.add_argument("-d","--output-dir",type=str, help="Output directory",default = "./composites")
parser.add_argument("-o","--output-template",type=str, help="Output template; must contain the {season} and {algorithm} templates",default = "era5_bloomington_AR_composites_{season}_{algorithm}.sbatch")

args = parser.parse_args()
num_nodes = args.nodes
season = args.season
procs_per_gpu = args.procs_per_gpu
algorithm = args.algorithm
time = args.time
output_dir = args.output_dir
output_file_template = args.output_template

if season == "all":
    seasons=["DJF","MAM","JJA","SON","annual"]
else:
    seasons = [season]

# read the template file
with open("generate_teca_bard_composites.sbatch.template") as fin:
    file_contents = fin.read()

# make the output directory
os.makedirs(output_dir, exist_ok = True)

for season in seasons:
    # set the output file name
    output_file_name = output_file_template.format(season = season, algorithm = algorithm)
    output_file = os.path.join(output_dir, output_file_name)

    # template the output file
    output_contents = file_contents.format(
        season = season,
        algorithm = algorithm,
        time = time,
        num_nodes = num_nodes,
        num_procs = num_nodes*64,
        num_srun_procs = num_nodes*procs_per_gpu*4,
    )

    with open(output_file, "w") as fout:
        fout.write(output_contents)

    os.chdir(output_dir)
    os.system(f"sbatch {output_file_name}")
    os.chdir("../")