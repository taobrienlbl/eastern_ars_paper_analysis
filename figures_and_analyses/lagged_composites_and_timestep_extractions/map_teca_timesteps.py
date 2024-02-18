from pathlib import Path
import cftime
import netCDF4 as nc

def map_timestep_to_file(
    timestep : int,
    base_path : Path = Path("/pscratch/sd/t/taobrien/era5_combined_north_america_1979-2021/era5_combined_north_america/"),
    verify_step : bool = True):
    """ Map a timestep to the file it is in. 

    Parameters
    ----------

    timestep : int
        The timestep to map to a file.

    base_path : Path
        The base path to look for the file in.

    verify_step : bool
        If True, verify that the timestep is within the file. If False, do not verify.

    Returns
    -------

    Path, step
        A tuple containing the path to the file and the step within the file.
    
    """

    # use cftime to convert the timestep to a date
    units = "hours since 1979-01-01 00:00:00"
    calendar = "gregorian"
    step_date = cftime.num2pydate(timestep, units=units, calendar=calendar)

    # get the file name
    # files are named like era5_combined_north_america_2000-06-30-00Z.nc with one file per day (24 steps per file)
    file_name = f"era5_combined_north_america_{step_date.strftime('%Y-%m-%d')}-00Z.nc"

    # get the file path
    file_path = base_path / file_name

    # get the step within the file
    step = step_date.hour

    # verify that the step is within the file
    if verify_step:
        with nc.Dataset(file_path) as ds:
            tval = ds.variables["time"][step]
            units = ds.variables["time"].units
            calendar = ds.variables["time"].calendar
            file_step_date = cftime.num2pydate(tval, units=units, calendar=calendar)
            assert file_step_date == step_date, f"Step {step} file {file_path} yields date {file_step_date} which does not match expected date {step_date}."

    return file_path, step





