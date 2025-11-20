from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np

my_tiffs = []
for i in range(1,51):
    dataset = gdal.Open(f'forest_monitoring/fake_forest_T{i}.tif')
    my_tiffs.append(dataset)

nir_band = []    #near-infrared reflectance
swir_band = []   #short-wave infrared reflectance

for i in my_tiffs:
    nir_band.append(i.GetRasterBand(1).ReadAsArray())
    swir_band.append(i.GetRasterBand(2).ReadAsArray())




