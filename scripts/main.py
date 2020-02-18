import s3fs
import numpy as np
from datetime import datetime
import os
from pre_process import pre_processGOES

# Use the anonymous credentials to access public data
fs = s3fs.S3FileSystem(anon=True)

# List contents of GOES-16 bucket.
fs.ls('s3://noaa-goes16/')
# define path of data, product and date
data_path = '../../data/'
goes = 'noaa-goes16'
product = 'ABI-L2-CMIPF'

year = str(datetime.now().year)
day_of_year = "{0:03d}".format(datetime.now().timetuple().tm_yday)
scans_start_hour = "{0:02d}".format(datetime.now().hour)
file_path = os.path.join(goes, product, year, day_of_year, scans_start_hour)

# Note: the `s3://` is not required
files = np.array(fs.ls(file_path))
bands = ['C01', 'C03', 'C13']
filteredFiles = np.array([[f for f in files if 'M6C01' in f][0], [f for f in files if 'M6C03' in f][0], [f for f in files if 'M6C13' in f][0]])


# create the download paths
today_path = str(datetime.now().year) + '-' + '{0:02d}'.format(datetime.now().month) + '-'+'{0:02d}'.format(datetime.now().day)
print(os.path.abspath(os.path.join(data_path, today_path)))

abs_path = os.path.abspath(os.path.join(data_path, today_path))
post_process_path = os.path.join(abs_path, 'post_process')
print(abs_path)
if not os.path.exists(abs_path):
    os.mkdir(abs_path)
    print('Data directory created')
else:
    print('Data directory already exists')
# Download the files

[fs.get(filteredFiles[i], abs_path + '/' + filteredFiles[i].split('/')[-1]) for i in range(0, len(filteredFiles))]

if not os.path.exists(post_process_path):
    os.mkdir(post_process_path)
    [os.mkdir(os.path.join(post_process_path, 'band' + str(indx))) for indx in range(0, len(filteredFiles))]
    print('Daily directory created')
else:
    print('Daily directory already exists')

latbox = [18.2, 31]
lonbox = [-98, -83]

pre_processGOES(abs_path, latbox, lonbox, post_process_path, datetime.now(), bands)

[os.remove(f) for f in os.listdir(abs_path) if f != 'post_process']
