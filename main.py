import lightkurve as lk
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STYLE_FILE = BASE_DIR / "rose-pine-moon.mplstyle"

search_lcf = lk.search_lightcurve('L 98-59', mission = 'TESS', author = 'SPOC', exptime = 120)

print(search_lcf)
lcf = search_lcf[0].download()
lc = lcf[0].normalize()

plt.style.use(STYLE_FILE)
plt.plot(lc.time.value, lc.flux.value, label='L 98-59')
plt.xlabel('Time (BTJD)')
plt.ylabel('Normalized Flux')
plt.legend()
plt.show()