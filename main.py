import lightkurve as lk
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STYLE_FILE = BASE_DIR / "rose-pine-moon.mplstyle"

search_lcf = lk.search_lightcurve('L 98-59', mission = 'TESS', author = 'SPOC', exptime = 120)

lc = search_lcf[0].download()
lc = lc.normalize() #normalize the data
lc = lc.remove_nans() #removed missing data 

lc_flat = lc.flatten(window_length = 401) # Flatten the data / remove the long term trends using Savitzky-Golay filter 

lc_clean_flat, mask = lc_flat.remove_outliers(sigma=3, return_mask = True) 
# use sigma clipping with speicified sigma (values more than 3 median away will be removed) and returns mask

outliers = lc*mask

print(f"removed {np.sum(mask)} outliers")
'''
removes 1 outliers with sigma = 5
removes 4 outliers with sigma = 4
removes 104 outleirs with sigma = 3
'''
'''
the current subject does not seem to have too many obvious outliers, I decided to use sigma = 4 since it only removes
the most obvious ones without trying to clean up noise
'''

plt.style.use(STYLE_FILE)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
ax1.plot(lc_clean_flat.time.value, lc_clean_flat.flux.value, markersize=2, label='cleaned flattened PDCSAP Flux')
ax2.plot(lc_flat.time.value, lc_flat.flux.value - lc.flux.value, label = 'flattening error curve')

'''
It is evident from the error curve that the raw function's original baseline had an upward bowl shape
'''
plt.savefig('clean_flat_lightcurve.png', dpi=300, bbox_inches='tight')
plt.show()