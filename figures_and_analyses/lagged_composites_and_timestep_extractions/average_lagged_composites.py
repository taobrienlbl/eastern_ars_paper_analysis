#!/usr/bin/env python3
import xarray as xr
import glob
from pathlib import Path
from simplempi.parfor import parfor, pprint

lagged_composite_base = Path("./era5_bloomington_ar_teca_bard_v1.0.1/")
lags = glob.glob(str(lagged_composite_base / "lag_*"))

# set the months in each season
seasons = {
    "annual": range(1, 13),
    "djf": [12, 1, 2],
    "mam": [3, 4, 5],
    "jja": [6, 7, 8],
    "son": [9, 10, 11]
}

# loop through the lags
for lag in parfor(lags):
    # get the lag
    lag_dir = Path(lag)
    lag = lag_dir.stem

    # get all the files in the lag directory
    files = sorted(lag_dir.glob("*.nc"))


    # get the month of each file
    months = [int(f.stem.split("_")[-2].split("-")[1]) for f in files]

    # loop through the seasons
    for season in seasons:
        pprint(f"Processing {lag}, {season}")
        # get the months in the season
        season_months = seasons[season]

        # get the indices of months that match the season
        month_inds = [i for i, m in enumerate(months) if m in season_months]

        # get the files in the season
        season_files = [files[i] for i in month_inds]

        # open the files
        ds = xr.open_mfdataset(season_files, combine="by_coords")

        # calculate the mean
        mean = ds.mean(dim="time")

        # set the output path
        mean_path = lagged_composite_base / f"era5_bloomington_ar_teca_bard_v1.0.1_{season}_{lag}.mean.nc"

        # save the mean
        mean.to_netcdf(mean_path)
