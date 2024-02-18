#!/usr/bin/env python3
import numpy as np
import xarray as xr
from pathlib import Path
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
# import animation libraries
from matplotlib.animation import FuncAnimation
import cmocean


# set the path to the lagged composites
lagged_composite_base = Path("./era5_bloomington_ar_teca_bard_v1.0.1/")

# set the seasons
seasons = ["annual", "djf", "mam", "jja", "son"]

# loop over seasons
for season in seasons:
    print(season)
    # get the files for the season
    files = sorted(lagged_composite_base.glob(f"*_{season}_lag_-*.mean.nc"))[::-1] + \
            sorted(lagged_composite_base.glob(f"*_{season}_lag_+*.mean.nc"))

    # get the lags from the file names
    lags = [int(f.stem.split("_")[-1].split('.')[0]) for f in files]

    # open the files, creating a new 'lag' dimension corresponding to teach file
    ds = xr.open_mfdataset(files, combine="nested", concat_dim="lag")

    # set the lag as a coordinate
    ds["lag"] = lags

    ivt = ds["IVT"]
    z500 = ds["Z"]

    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw=dict(projection=ccrs.PlateCarree()))

    # make a colorbar axis
    cbar_ax = fig.add_axes([0.2, 0.1, 0.6, 0.02])

    # pre-make the colorbar to avoid odd artefacts
    ivt_levels = np.arange(250, 1000, 50)
    ivt_cmap = 'magma_r'
    ivt.isel(lag=0).plot.contourf(
        ax=ax, transform=ccrs.PlateCarree(),
        cmap = ivt_cmap,
        levels = ivt_levels,
        cbar_kwargs = dict(orientation='horizontal', label="IVT (kg/m/s)"),
        cbar_ax = cbar_ax
    )


    def anim(i):
        ax.clear()

        # IVT
        ivt.isel(lag=i).plot(
            ax=ax, transform=ccrs.PlateCarree(),
            cmap = ivt_cmap,
            levels = ivt_levels,
            add_colorbar=False,
        )

        # Z500
        zplot = z500.isel(lag=i)/9.81
        zcplt = zplot.plot.contour(
            ax=ax, transform=ccrs.PlateCarree(),
            levels = np.arange(4800, 6000, 60),
            colors='k',
            add_colorbar=False)

        # add contour labels
        plt.clabel(zcplt, fmt="%1.0f")

        ax.coastlines()
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        # plot the lag (in days)
        lag_days = lags[i]/24
        ax.set_title(f"Lag {lag_days:2.1f} days")
        return ax

    # generate an animated gif
    anim = FuncAnimation(fig, anim, frames = len(lags), interval = 500)
    anim.save(f"lagged_composites_{season}.gif", writer="imagemagick")
    

    