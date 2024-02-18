#!/usr/bin/env python3
import os
import xarray as xr
import glob
import map_teca_timesteps
import simplempi
from pathlib import Path
import numpy as np

smpi = simplempi.simpleMPI(useMPI=True)

location = "bloomington"
detector = "teca_bard_v1.0.1"
season = "annual"

# load the list of AR timesteps
if smpi.rank == 0:
    ar_timstep_file = f"../era5_index_files/{location}_ars_{season}_era5_{detector}.txt"
    with open(ar_timstep_file) as f:
        ar_timesteps = [ int(l.rstrip()) for l in f.readlines()]
else:
    ar_timesteps = []

lags = np.arange(-5, 5.5, 0.5) * 24 # in hours
lags = lags.astype(int)

# scatter the list of timesteps
my_ar_timesteps = smpi.scatterList(ar_timesteps)

# loop through the timesteps and extract the data
for t in my_ar_timesteps:

    for lag in lags:
        l = t + lag

        smpi.pprint(f"Extracting timestep {l}")
        # map the timestep to a file
        file_path, step = map_teca_timesteps.map_timestep_to_file(l)

        # open the file and extract the data
        with xr.open_dataset(file_path, chunks = -1) as ds:
            ds = ds.isel(time=[step])
            # get the date from the file path
            # files are named like era5_combined_north_america_2000-06-30-00Z.nc
            date = file_path.stem.split("_")[-1]

            # set the output path
            output_path = Path(os.environ["SCRATCH"]) / Path(f"era5_{location}_ar_{detector}/lag_{lag:+04}/era5_{location}_ar_{detector}_{season}_{date}_{step}.nc")

            # make sure the output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # print the output path (absolute path for clarity)
            smpi.pprint(f"Writing to {output_path.absolute()}")

            # if lag isn't 0, only use the VIWVE and VIWVN variables
            #if lag != 0:
            #    ds = ds[["VIWVE", "VIWVN"]]

            # convert the IVT vector components to a scalar
            ds["IVT"] = np.sqrt(ds["VIWVE"]**2 + ds["VIWVN"]**2)
            # drop the vector components
            ds = ds.drop_vars(["VIWVE", "VIWVN"])

            # pull out just the 500 hPa levels
            ds = ds.sel(level=500)

            # get a list of variables that contain latitude and longitude
            var_list = [ v for v in ds.variables if "latitude" in ds[v].dims and "longitude" in ds[v].dims ]

            # set compression for all spatial variables
            encoding = {v: {"zlib": True, "complevel": 1} for v in var_list}
            
            # set the chunk size for all lat/lon variable; use 1 for all non-lat-lon dimensions
            for v in var_list:
                dims = ds[v].dims
                chunk_sizes = [1 if d not in ["latitude", "longitude"] else ds[d].size for d in dims]
                encoding[v]["chunksizes"] = tuple(chunk_sizes)


            # write the data to the output file, adding compression
            if os.path.exists(output_path):
                raise RuntimeError(f"{output_path} already exists")
            ds.to_netcdf(output_path, mode="w", format="NETCDF4", engine="netcdf4", encoding=encoding, unlimited_dims=["time"])
