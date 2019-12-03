# importing all the libraries
from netCDF4 import Dataset
import numpy as np
from reproj import reproj
import os
from datetime import datetime, timedelta
from xarray import open_dataset
from pyresample import image


# defining the function for pre_process all the bands
def pre_processGOES(nc_folder, latbox, lonbox, path2save, date, bands):
    full_direc = os.listdir(nc_folder)  # creating a list of files in the given folder
    nc_files = [ii for ii in full_direc if ii.endswith('.nc')]  # creating a list with only NetCDF files in the given folder
    for band in range(0, len(nc_files)):  # iterating over all the bands
        g16_data_file = nc_files[band]  # selecting the NetCDF file according to the band
        g16nc = Dataset(os.path.join(nc_folder, g16_data_file) , 'r')  # opening the NetCDF file to read
        print('preprocessing band ', bands[band], g16_data_file)
        cmiValues = g16nc.variables['CMI'][:]  # selecting the CMI variable
        latValues, lonValues, newArea, oldArea = reproj(nc_folder, band)  #calling the reprojection function and assigning the variables
        fileName = 'band'+str(band)+'/'+'goes_'+'{0:02d}'.format(date.hour)+'.nc'  # creating the file name
        dataset = Dataset(os.path.join(path2save, fileName), 'w', format='NETCDF4', set_fill_off=True)  # creating the new netCDF file

        # adding dimensions
        dataset.createDimension('time', None)
        dataset.createDimension('lat', len(latValues))
        dataset.createDimension('lon', len(lonValues))

        # adding variables
        time = dataset.createVariable('time', 'f8', ('time',), zlib=True, shuffle=True, fill_value=0.)
        lon = dataset.createVariable('lon', 'f8', ('lon',), zlib=True, shuffle=True, least_significant_digit=4)
        lat = dataset.createVariable('lat', 'f8', ('lat',), zlib=True, shuffle=True, least_significant_digit=4)
        CMI = dataset.createVariable('CMI', 'f8', ('time', 'lat', 'lon'), fill_value=-1, zlib=True, shuffle=True, least_significant_digit=6)

        # adding variables atributtes
        lat.long_name = 'Latitude'
        lat.units = 'degrees_north'
        lat.standard_name = 'latitude'

        lon.long_name = 'Longitude'
        lon.units = 'degrees_east'
        lon.standard_name = 'longitude'

        time.long_name = 'Time'
        time.units = 'hours since ' + str(date.year) + '-' + str(date.month) + '-' + str(date.day) + ' 00:00:00'
        time.standard_name = 'time'
        time.axis = 'T'

        # assigning the values to the new variables
        CC = open_dataset(nc_files[0], mask_and_scale=True, decode_times=False)
        lat[:] = latValues[:]
        lon[:] = lonValues[:]
        time[:] = [date.hour]
        #  reprojecting the CMI variable to the new domain
        CMI[0, :, :] = image.ImageContainerNearest(np.round(cmiValues, decimals=6), oldArea, radius_of_influence=10000, nprocs=8).resample(newArea).image_data
        dataset.close()  # closing the new NetCDF
