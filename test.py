import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# define input files here
input_file1 = 'data/CH2DOD/CH2DOD_cut_15-55.dpt'
input_file2 = 'data/CH2DOH/CH2DOH_15-95_lowP.dat'

# define output files here
output_file_diff = 'data/difference.dpt'  # difference
output_file1_new = input_file1.replace('.dpt', '_new.dpt')  # interpolated
output_file2_new = input_file2.replace('.dat', '_new.dpt')  # interpolated

# read data
xdata1, ydata1 = np.loadtxt(input_file1).T
xdata2, ydata2 = np.loadtxt(input_file2).T

print(f"data1 = {xdata1.shape}")
print(f"data2 = {xdata2.shape}")

#
#xmin1, xmax1 = xdata1.min(), xdata1.max()
#xmin2, xmax2 = xdata2.min(), xdata2.max()

# create interpolation functions
f1 = interp1d(xdata1, ydata1, bounds_error=False, fill_value=0e0)
f2 = interp1d(xdata2, ydata2, bounds_error=False, fill_value=0e0)

# create new common xdata
xdata_new = np.sort(np.unique(np.concatenate([xdata1, xdata2])))
ydata1_new = f1(xdata_new)
ydata2_new = f2(xdata_new)

# compute difference
ydata_diff = ydata2_new - ydata1_new

# save new data
print(f"saving difference to {output_file_diff}")
np.savetxt(output_file_diff, np.c_[xdata_new, ydata_diff], fmt='%15.8e')

print(f"saving new data to {output_file1_new} and {output_file2_new}")
np.savetxt(output_file1_new, np.c_[xdata_new, ydata1_new], fmt='%15.8e')

print(f"saving new data to {output_file2_new}")
np.savetxt(output_file2_new, np.c_[xdata_new, ydata2_new], fmt='%15.8e')

# set specific range to plot
#imin = np.argmin(np.abs(xdata_new - 43.67))
#imax = np.argmin(np.abs(xdata_new - 43.69))

# reset to full range
imin = 0
imax = -1

# plot difference
fig, axs = plt.subplots(2, 1, figsize=(20,10), sharex=True, sharey=True)
ax = axs[0]
ax.plot(xdata_new[imin:imax], ydata_diff[imin:imax], label='data2 - data1', marker=None)
ax.axhline(0e0, color='k', ls='--')
ax.autoscale()

# plot original data
ax = axs[1]
ax.plot(xdata_new[imin:imax], ydata1_new[imin:imax], label='data1 new',marker=None)
ax.plot(xdata_new[imin:imax], ydata2_new[imin:imax], label='data2 new',marker=None)
ax.autoscale()
ax.legend()

plt.tight_layout()
plt.show()
