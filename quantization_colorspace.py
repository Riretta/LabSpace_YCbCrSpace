import numpy as np
import math

def rgb2lab ( inputColor ) :

   num = 0
   RGB = [0, 0, 0]

   for value in inputColor :
       value = float(value) / 255

       if value > 0.04045 :
           value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
       else :
           value = value / 12.92

       RGB[num] = value * 100
       num = num + 1

   XYZ = [0, 0, 0,]

   X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
   Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
   Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
   XYZ[ 0 ] = round( X, 4 )
   XYZ[ 1 ] = round( Y, 4 )
   XYZ[ 2 ] = round( Z, 4 )

   XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
   XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
   XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

   num = 0
   for value in XYZ :

       if value > 0.008856 :
           value = value ** ( 0.3333333333333333 )
       else :
           value = ( 7.787 * value ) + ( 16 / 116 )

       XYZ[num] = value
       num = num + 1

   Lab = [0, 0, 0]

   L = ( 116 * XYZ[ 1 ] ) - 16
   a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
   b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

   Lab [ 0 ] = round( L, 4 )
   Lab [ 1 ] = round( a, 4 )
   Lab [ 2 ] = round( b, 4 )

   return Lab


ycbcr_space = []
colors = []
for i in range(255):
    for j in range(255):
        for k in range(255):
            output = [0, 0, 0]
            output = rgb2lab([i, j, k])

            ##wiki##
            # output[0] = 16  + 1/256 * (   65.738  * i + 129.057 * j +  25.064  * k)
            # output[1] = 128 + 1 / 256 * (- 37.945 * i -   74.494  * j + 112.439 * k)
            # output[2] = 128 + 1 / 256 * (112.439 * i -   94.154  * j -  18.285 * k)

            ##https://github.com/ghanashyamprabhu/RGB2YCbCr_py/blob/master/source/RGB2YCbCr.py
            # output[:, :, 0] = np.trunc((0.257 * input[:, :, 0]) + (0.504 * input[:, :, 1]) + (0.098 * input[:, :, 2]) + 16)
            # output[:, :, 1] = np.trunc(((-0.148) * input[:, :, 0]) - (0.291 * input[:, :, 1]) + (0.439 * input[:, :, 2]) + 128)
            # output[:, :, 2] = np.trunc((0.439 * input[:, :, 0]) - (0.368 * input[:, :, 1]) - (0.071 * input[:, :, 2]) + 128)

            #https://stackoverflow.com/questions/34913005/color-space-mapping-ycbcr-to-rgb
            #remove if you want to quantize for LAB
            output[0] = math.trunc((.299 * i) + (.587 * j) + (.114 *k))
            output[1] = math.trunc(((-.1687) * i) - (.3313 * j) + (.5 * k) + 128)
            output[2] = math.trunc((.5 * i) - (.4187 * j) - (.0813 * k) + 128)

            colors.append((i/255.0,j/255.0,k/255.0))
            ycbcr_space.append(output)
ycbcr_space = np.array(ycbcr_space)

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(ycbcr_space[:,0],ycbcr_space[:, 1], ycbcr_space[:, 2],c =colors)
ax.set_xlabel('L Label')
ax.set_ylabel('a Label')
ax.set_zlabel('b Label')
plt.show()

import matplotlib.pyplot as plt
fig = plt.figure()
plt.scatter(ycbcr_space[:, 1], ycbcr_space[:, 2],c=colors)
plt.xlabel('Cb Label')
plt.ylabel('Cr Label')
plt.show()

# lab quantization
# H, xedges, yedges = np.histogram2d(ycbcr_space[:, 1], ycbcr_space[:, 2], bins=np.arange(-115,125,10))  
# YCbCr quantization
H, xedges, yedges = np.histogram2d(ycbcr_space[:, 1], ycbcr_space[:, 2], bins=np.arange(0,260,10))
import seaborn as sns
ax = sns.heatmap(H, linewidth=0.5, cmap="YlGnBu")
ax.invert_yaxis()
plt.show()

xylist = []
xlist = []
ylist = []
colors_h = []
for i in range(len(H)):
    for j in range(len(H)):
        if H[i, j] > 0:
            xy = [0,0]
            x = (xedges[i] + xedges[i+1])/2
            y = (yedges[j] + yedges[j+1])/2
            xy[0] = x
            xy[1] = y
            xlist.append(x)
            ylist.append(y)
            xylist.append(xy)

plt.scatter(xlist,ylist)
plt.show()

print(len(xylist))  #<- bin created
np.save('resources/pts_in_hull_ycbcr_500.npy',np.asarray(xylist))
