from res import *
import matplotlib.pyplot as plt
import numpy as np

# Using zip function and Unpacking the values
# fuse_x, fuse_y = zip(*fuse)
# dwm_x, dwm_y = zip(*dwm)
# vive_x, vive_y = zip(*vive)

# plt.scatter(vive_x, vive_y) 
# plt.scatter(fuse_x, fuse_y)
# plt.scatter(dwm_x, dwm_y)
# plt.show()

fuse_error = []
dwm_error = []
for i in range(len(vive)):
    fuse_error.append(
        (((vive[i][0]) - fuse[i][0])**2 + ((vive[i][1]) - fuse[i][1])**2)**.5
    )
    dwm_error.append(
        (((vive[i][0]) - dwm[i][0])**2 + ((vive[i][1]) - dwm[i][1])**2)**.5
    )

print('max error')
print(np.max(fuse_error))
print(np.max(dwm_error))
print()
print('mean error')
print(np.mean(fuse_error))
print(np.mean(dwm_error))
