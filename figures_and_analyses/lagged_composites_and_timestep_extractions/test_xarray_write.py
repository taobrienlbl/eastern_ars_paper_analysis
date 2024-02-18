import os
from simplempi.parfor import parfor, pprint
import xarray as xr
import numpy as np
from pathlib import Path

nx = 1000
ny = 2000
nt = 50

mylist = range(128)

for item in parfor(mylist):
    # create a data array to write
    my_array = np.random.normal(size=[nt,ny,nx])
    my_da = xr.DataArray(my_array, dims = ["time", "y", "x"])
    ds = xr.Dataset()
    ds['randn'] = my_da

    # set the file name
    output_file = Path(os.environ["SCRATCH"]) / f"test_xarray_shifter/file_{item:03}.nc"

    # make sure the output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # get a list of variables that contain latitude and longitude
    var_list = [ v for v in ds.variables if "y" in ds[v].dims and "x" in ds[v].dims ]

    # set compression for all spatial variables
    encoding = {v: {"zlib": True, "complevel": 1} for v in var_list}
        
    # set the chunk size for all lat/lon variable; use 1 for all non-lat-lon dimensions
    for v in var_list:
        dims = ds[v].dims
        chunk_sizes = [1 if d not in ["y", "x"] else ds[d].size for d in dims]
        encoding[v]["chunksizes"] = tuple(chunk_sizes)


    # write the file to disk
    pprint(f"Writing {output_file}")
    ds.to_netcdf(output_file, mode="w", format="NETCDF4", engine="netcdf4", encoding=encoding, unlimited_dims=["time"])



