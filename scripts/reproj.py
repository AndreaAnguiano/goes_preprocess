from netCDF4 import Dataset
from pyresample.geometry import AreaDefinition
import os


def reproj(nc_folder, band):
    os.chdir(nc_folder)
    full_direc = os.listdir(os.getcwd())
    nc_files = [ii for ii in full_direc if ii.endswith('.nc')]
    g16_data_file = nc_files[band]  # select .nc file
    g16nc = Dataset(g16_data_file, 'r')

    # GOES-R projection info and retrieving relevant constants
    area_id = 'GOES_R'
    description = 'FullDisk GOES-R Projection'
    proj_id = 'GOES_R'
    proj_info = g16nc.variables['goes_imager_projection']
    lon_origin = proj_info.longitude_of_projection_origin
    lat_origin = proj_info.latitude_of_projection_origin
    r_eq = proj_info.semi_major_axis
    r_pol = proj_info.semi_minor_axis
    sweep_angle = proj_info.sweep_angle_axis
    nsh = g16nc.variables['nominal_satellite_height'][:]
    projection = '+proj=geos +h={} +lat_0={} +lon_0={} +a={} +b={} +sweep={} +ellps=GRS80 +unit=m'.format(nsh*1000,lat_origin,lon_origin, r_eq, r_pol, sweep_angle)
    x = g16nc.variables['x'][:]
    y = g16nc.variables['y'][:]
    print(len(x), len(x))
    width = len(x)
    height = len(x)
    h = nsh*1000
    x_l = h * x[0]
    x_r = h * x[-1]
    y_l = h * y[-1]
    y_u = h * y[0]
    x_half = (x_r - x_l) / (len(x) - 1) / 2
    y_half = (y_l - y_u) / (len(x) - 1) / 2
    area_extent = (x_l-x_half, y_l-y_half, x_r+x_half, y_u+y_half)
    goesproj = AreaDefinition(area_id=area_id, description=description, proj_id=proj_id, projection=projection, width=width, height=height, area_extent=area_extent)

    area_id = 'IOA_D1'
    description = 'Dominio 1 Grupo IOA'
    proj_id = 'IOA_D1'
    projection = '+init=EPSG:4326'
    width = 2909
    height = 2058
    area_extent = (-123.3613, 4.1260, -74.8779, 38.4260)
    ioa1 = AreaDefinition(area_id=area_id, description=description, proj_id=proj_id, projection=projection, width=width, height=height, area_extent=area_extent)

    ioa_lon, ioa_lat = ioa1.get_lonlats()
    ioa_lon = ioa_lon[0, :]
    ioa_lat = ioa_lat[:, 0]

    return ioa_lat, ioa_lon, ioa1, goesproj

# reproj('/DATA/GOES/data/2019-09-17/')
