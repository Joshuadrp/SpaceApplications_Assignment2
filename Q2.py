import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

water_data = pd.read_csv('water_monitoring.csv')

green_band = np.array(water_data['band3_green'])
red_band = np.array(water_data['band4_red'])
nir = np.array(water_data['band8_nir'])
dates = np.array(water_data['date'])

def ndti(red,green):
    return (red-green)/(red+green)

def ndwi(green,nir):
    return (green-nir)/(green+nir)

#Normalized Difference Turbidity Index
ndti_val = ndti(red=red_band,green=green_band)
#Normalized Difference Water Index
ndwi_val = ndwi(green=green_band,nir=nir)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

#1 Both parameters evolving over time

# NDTI plot
ax1.plot(dates, ndti_val, linewidth=2, marker='o', markersize=4, color='red')
ax1.set_xlabel('Date')
ax1.set_ylabel('NDTI')
ax1.set_title('NDTI Evolution Over Time')
ax1.tick_params(axis='x', rotation=90)

# NDWI plot
ax2.plot(dates, ndwi_val, linewidth=2, marker='o', markersize=4, color='blue')
ax2.set_xlabel('Date')
ax2.set_ylabel('NDWI')
ax2.set_title('NDWI Evolution Over Time')
ax2.tick_params(axis='x', rotation=90)

plt.tight_layout()
plt.show()

# Other parts of Q2 will be answered in the assignment PDF.



