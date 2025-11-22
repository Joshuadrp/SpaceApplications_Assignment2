from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np

# Suppress GDAL warnings
gdal.UseExceptions()

my_tiffs = []
for i in range(1, 51):
    dataset = gdal.Open(f'forest_monitoring/fake_forest_T{i}.tif')
    my_tiffs.append(dataset)

nir_band = []  # Near-infrared reflectance
swir_band = []  # Short-wave infrared reflectance

for i in my_tiffs:
    nir_band.append(i.GetRasterBand(1).ReadAsArray())
    swir_band.append(i.GetRasterBand(2).ReadAsArray())

numpy_nir = np.array(nir_band)
numpy_swir = np.array(swir_band)

#1A Compute the normalised NBR for each pixel in the image.
def normalized_burn_ratio(nir, swir):
    """
    Calculate Normalized Burn Ratio (NBR)
    """
    return (nir - swir) / (nir + swir)
nbr = normalized_burn_ratio(numpy_nir, numpy_swir)
print(f"My NBR has a shape of: {nbr.shape}")

#1B Track time evolution of NBR at pixel level according to professor feedback(when and where it happened)
# After iterating the different tiff images, an interval was found for the start of the fire.
time = []
for i in range(13,28):
    time.append(i)
# NBR Evolution Plot
fig, axes = plt.subplots(3, 5)
for ax, t in zip(axes.flat, time):
    im = ax.imshow(nbr[t], cmap='RdYlGn', vmin=-1, vmax=1)
    ax.set_title(f'T{t}')
    ax.axis('off')
plt.tight_layout()
plt.show()

#2 Key times in the vegetation monitoring, map of the NBR index of the area at those times
key_times = [12, 19, 27]
titles = ['Before Fire', 'During Fire', 'After Fire']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, t, title in zip(axes, key_times, titles):
    ax.imshow(nbr[t], cmap='RdYlGn', vmin=-1, vmax=1)
    ax.set_title(f'{title} (T{t})')
    ax.axis('off')
plt.tight_layout()
plt.show()

#3 Check the data and warn the observer that something was happening with the vegetation in the forest.
def forrest_in_trouble(nbr):
    known_good = nbr[0]
    total_pixels = nbr.shape[1] * nbr.shape[2]
    there_is_fire = False

    for t in range(1, nbr.shape[0]):
        nbr_change = known_good - nbr[t]

        unburned = np.sum(nbr_change < 0.1)
        low_sev = np.sum((nbr_change >= 0.1) & (nbr_change <= 0.27))
        moderate = np.sum((nbr_change > 0.27) & (nbr_change <= 0.66))
        high_sev = np.sum(nbr_change > 0.66)

        unburned_percent = (unburned/total_pixels) * 100
        low_percent = (low_sev/total_pixels) * 100
        moderate_percent = (moderate/total_pixels) * 100
        high_percent = (high_sev/total_pixels) * 100

        if not there_is_fire:
            if high_percent > 0.1 or moderate_percent > 1.0 or low_percent > 3.0:
                there_is_fire = True
                print(f"FIRE DETECTED AT T{t}, TAKE ACTION!!")


forrest_in_trouble(nbr)


