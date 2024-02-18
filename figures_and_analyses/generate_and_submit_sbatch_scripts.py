#!/usr/bin/env python3
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-N", "--nodes", type=int, help="Number of nodes", default=10)
parser.add_argument("-s","--season",type=str, help="Season",choices=["DJF","MAM","JJA","SON","annual","all"], default = "all")
parser.add_argument("-p","--procs-per-gpu",type=int, help="Number of processors per GPU", default = 8)
parser.add_argument("-n","--procs-per-node",type=int, help="Total number of processors per node", default = 64)
parser.add_argument("-a","--algorithm",type=str, help="ARTMIP Algorithm to use", choices=["teca_bard_v1.0.1", "guan_waliser"], default = "teca_bard_v1.0.1")
parser.add_argument("-l","--location",type=str, help="Location name", choices=["bloomington","dc","ok"], default = "bloomington")
parser.add_argument("-g","--gpus-per-node",type=int, help="Number of GPUs per node", default = 4)
parser.add_argument("-t","--time",type=int, help="Time (minutes) of SLURM request", default = 240)
parser.add_argument("-d","--output-dir",type=str, help="Output directory",default = "./composites")
parser.add_argument("-f", "--template_file",type=str, help="Template file",default = "generate_teca_bard_new_composites.sbatch.template")
parser.add_argument("-o","--output-template",type=str, help="Output template; must contain the {season}, {location}, and {algorithm} templates",default = "era5_{location}_AR_composites_{season}_{algorithm}.sbatch")
parser.add_argument("-r","--regex",type=str, help="Regex to use for finding files",default = "")

args = parser.parse_args()
num_nodes = args.nodes
season = args.season
procs_per_gpu = args.procs_per_gpu
procs_per_node = args.procs_per_node
gpus_per_node = args.gpus_per_node
algorithm = args.algorithm
location = args.location
time = args.time
output_dir = args.output_dir
template_file = args.template_file
output_file_template = args.output_template
input_regex = args.regex

if season == "all":
    seasons=["DJF","MAM","JJA","SON","annual"]
else:
    seasons = [season]

# read the template file
with open(template_file) as fin:
    file_contents = fin.read()

# make the output directory
os.makedirs(output_dir, exist_ok = True)

for season in seasons:
    # set the output file name
    output_file_name = output_file_template.format(season = season, algorithm = algorithm, location = location)
    output_file = os.path.join(output_dir, output_file_name)

    # template the output file
    output_contents = file_contents.format(
        season = season,
        algorithm = algorithm,
        time = time,
        num_nodes = num_nodes,
        num_procs = num_nodes*procs_per_node,
        num_srun_procs = num_nodes*procs_per_gpu*gpus_per_node,
        num_gpus = num_nodes * gpus_per_node,
        location = location,
        input_regex = input_regex,
    )

    with open(output_file, "w") as fout:
        fout.write(output_contents)

    os.chdir(output_dir)
    os.system(f"sbatch {output_file_name}")
    os.chdir("../")
