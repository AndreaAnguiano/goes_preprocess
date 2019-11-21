# goes_preprocess

This code is used to download and preprocess GOES data.

## GOES-R introduction
Geostationary Operational Environmental Satellite-16 (GOES-16)
We use **ABI L2+ Product Data**: "ABI" is for "Advanced Baseline Imager" on the GOES-16 satellite instrument, the specification "L2+Product Data" is the level of product advancement. [Link of available products](https://www.ncdc.noaa.gov/data-access/satellite-data/goes-r-series-satellites/glossary)

###### Available processing levels and domains

L1b-RadM Radiances Mesoescale
L1b-RadC Radiances CONUS
L1b-RadF Radiances Full Disk
L2-CMIPM Reflectance Mesoescale
L2-CMIPC Reflectance CONUS
L2-CMIPF Reflectance Full Disk

To see the coverage area for each domain: [GOES Image Viewer](https://www.star.nesdis.noaa.gov/GOES/index.php)

###### Available bands

C01 Blue [Visible]
C02 Red [Visible]
C03 Veggie [NIR]
C04 Cirrus [NIR]
C05 Snow/Ice [NIR]
C06 Cloud Particle [NIR]
C07 Shortwave Window [IR]
C08 Upper-Level Water Vapor [IR]
C09 Mid-Level Water Vapor [IR]
C10 Lower-Level Water Vapor [IR]
C11 Cloud Top Phase [IR]
C12 Ozone [IR]
C13 Clean Longwave Window [IR]
C14 Longwave Window [IR]
C15 Dirty Longwave Window [IR]
C16 C02 Longwave [IR]

We use the CMIP ABI L2 cloud and Moisture Imagery (single band) product with the bands [C01 C02 C03 C13]. Files are downloaded in netCDF format.

An example of a file name:

OR_ABI-L1b-RadM1-M3C01_G16_s20172511100550_e20172511101007_c20172511101048.nc

**OR** Data is operational and in real time.
**ABI-L1b-RadM1** is the product with the mesoescale 1 domain. C is for CONUS, F is por full disk, and M2 is for Mesoescale 2.
**M3C01** Mode is 3 and Channel 01.
**G16** GOES-16 (G17 for GOES-17).
**s20172511100550** scan start time sYYYYJJJHHMMSSm: year, day of year, hour, minute, second, tenth second.
**e20172511101007** scan end time sYYYYJJJHHMMSSm: year, day of year, hour, minute, second, tenth second.
**c20172511101048** scan file creation time sYYYYJJJHHMMSSm: year, day of year, hour, minute, second, tenth second.
