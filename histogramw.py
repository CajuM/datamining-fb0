#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
import numpy as np

d = open("data.txt")
x = []
y = []
z = []
for l in d:
    ll = l.split(' ')
    ts = int(ll[0]) * 24 * 3600 + int(ll[1])
    xx = int(ts / (7 * 24 * 3600))
    yy = ts % (7 * 24 * 3600)
    x.append(xx)
    y.append(yy)

x = np.array(x)
y = np.array(y)

print(x.max())
heatmap, xedges, yedges = np.histogram2d(x, y, bins=(len(np.unique(x)), 24 * 6))
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.imshow(np.rot90(heatmap), aspect='auto', extent=(x.min(), x.max(), y.min(), y.max()))
plt.plot(np.unique(x), np.full(np.unique(x).size, 6.5))
plt.plot(np.unique(x), np.full(np.unique(x).size, 16.5))
plt.colorbar()
plt.show()
plt.savefig('histogramw.png')
