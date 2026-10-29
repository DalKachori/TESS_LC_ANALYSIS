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

lc_clean_flat, mask = lc_flat.remove_outliers(sigma=4, return_mask = True) 
# use sigma clipping with speicified sigma (values more than 3 median away will be removed) and returns mask
outliers = lc*mask

lc_clean_flat_fold = lc_clean_flat.fold(period = 3.690621) 
# folds the signal over itself (signal_time/orbit_period) number of times and averages it

lc_clean_flat_fold_bin = lc_clean_flat_fold.bin(time_bin_size = 0.005)
# Averages the data over a bin of width 0.01 / moving average

'''
Additional averaging will be required to discover the transit dip, which requires knowing/guessing the 
time period of orbit. This is when i realize I should have chosen a different subject (will do).
the fold function folds the signal over the width of one transit and takes the average.
'''

print(f"removed {np.sum(mask)} outliers")
'''
Before flattening ->
removes 1 outliers with sigma = 5
removes 4 outliers with sigma = 4
removes 104 outliers with sigma = 3

After Flattening ->
removes 3 outliers with sigma = 4
removes 101 outliers with sigma = 3
removes 2321 outliers with sigma = 2
'''
'''
Before Flatterning ->
the current subject does not seem to have too many obvious outliers, I decided to use sigma = 4 since it only removes
the most obvious ones without trying to clean up noise

After Flattening ->
now choosing sigma = 4 which removes 3 outliers. Based on the previous logic.
'''

lightcurve = lc_clean_flat_fold.flux.value 
phasetime = lc_clean_flat_fold.time.value

in_transit = lightcurve[(phasetime > -1.6327) & (phasetime < -1.5627)]
out_transit = lightcurve[(-1.6327 > phasetime) | (phasetime > -1.5627)]
# Extract flux signal during in transit and out transit time to calculate baseline

f_in = np.average(in_transit)
f_out = np.average(out_transit)

fractional_transit_depth = (f_out - f_in) / f_out # calculate fractional transit depth
print(fractional_transit_depth)
'''
the fractional transit depth turns out to be 42% shallower --- 0.000975 vs 0.00167 of the actual conclusion
the radius comes out to be ~ 1 Earth than ~ 1.34 Earths.
'''

plt.style.use(STYLE_FILE)

fig, ax = plt.subplots()
ax.plot(lc_clean_flat_fold_bin.time.value, lc_clean_flat_fold_bin.flux.value, markersize=2, label='cleaned flattened folded PDCSAP Flux')
fig.canvas.mpl_connect("button_press_event",
    lambda e: print(f"x={e.xdata:.5f}, y={e.ydata:.5f}") if e.inaxes else None)
'''
It is evident from the error curve that the raw function's original baseline had an upward bowl shape
'''

'''
It is evident that there seems to be a clear dip in the data at around -1.6 phase point
'''

'''
Now after binning, the dip is clearly visible and ready to be analyzed
'''

'''
after using a more refined bin width, visually determining the transit time gives 
Ingress phase = -1.6327
Egress phase  = -1.5627

which corressponds to a  transit time of 0.07d = ~101 minutes which agrees with popular conclusion.
'''

plt.savefig('clean_flat_fold_bin_lightcurve.png', dpi=300, bbox_inches='tight')
plt.show()
# -1.6327 -> -1.5902 -> -1.5627