import lightkurve as lk
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STYLE_FILE = BASE_DIR / "rose-pine-moon.mplstyle"

search_lcf = lk.search_lightcurve('L 98-59', mission = 'TESS', author = 'SPOC', exptime = 120)

print(search_lcf)

lc = search_lcf[0].download().remove_nans()

pdcsap = lc.select_flux('pdcsap_flux').normalize()
sap = lc.select_flux('sap_flux').normalize()


plt.style.use(STYLE_FILE)
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))

ax1.plot(sap.time.value, sap.flux.value, markersize=2, label='SAP Flux', alpha=0.5)
ax1.plot(pdcsap.time.value, pdcsap.flux.value, markersize=2, label='PDCSAP Flux', alpha=0.5)
ax1.set_ylabel('Normalized Flux')
ax1.legend()

ax2.plot(pdcsap.time.value, pdcsap.flux_err.value, '.', markersize=2, label='PDCSAP Error')
ax2.set_xlabel('Time (BTJD)')
ax2.set_ylabel('Flux Error')
ax2.legend()

plt.savefig('test_lightcurve.png', dpi=300, bbox_inches='tight')
plt.show()