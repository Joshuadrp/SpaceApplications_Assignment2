from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

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



# # Show which areas changed the most over time
# std_nbr = nbr.std(axis=0)
# plt.figure(figsize=(10, 8))
# im = plt.imshow(std_nbr, cmap='hot')
# plt.colorbar(im, label='NBR Variability')
# plt.xlabel('Pixel Column')
# plt.ylabel('Pixel Row')
# plt.title('Areas with Most Change Over Time\n(Bright = High change, Dark = Stable)')
# plt.tight_layout()
# plt.show()

# Burn Severity Thresholds
# unburned = np.sum(nbr < 0.1)
# low_sev = np.sum((nbr >= 0.1) & (nbr <= 0.27))
# moderate = np.sum((nbr > 0.27) & (nbr <= 0.66))
# high_sev = np.sum(nbr > 0.66)
