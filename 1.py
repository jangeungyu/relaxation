import numpy as np
from mpl_toolkits.mplot3d import Axes3D  
import matplotlib.pyplot as plt

def absoluteArgmax(arr):
    absolute = np.absolute(arr)
    a = absolute.argmax()
    b = absolute.shape[1]
    return (a//b, a%b)

def residualMax(box):
    side = len(box)
    residuals = np.zeros((side, side))
    for a in range(1, side-1):
        for b in range(1, side-1):
            residual = box[a-1][b] + box[a+1][b] + box[a][b-1] + box[a][b+1] - 4*box[a][b]
            residuals[a][b] = residual

    k = absoluteArgmax(residuals[1:side-1, 1:side-1])

    a = k[0] + 1
    b = k[1] + 1
    return ((a, b), residuals[a][b])

def relax(box):
    newBox = box.copy()
    k = residualMax(box)
    a = k[0][0]
    b = k[0][1]
    
    newBox[a][b] = box[a][b] + 0.25 * k[1]

    return newBox

def quasiResidualMax(box):
    side = len(box)
    residuals = np.zeros((side, side))
    for a in range(1, side-1):
        for b in range(1, side-1):
            residual = box[a-1][b] + box[a+1][b] + box[a][b-1] + box[a][b+1] - 4*box[a][b]
            residuals[a][b] = residual

    k = absoluteArgmax(residuals[2:side-2, 2:side-2])

    a = k[0] + 1
    b = k[1] + 1
    return ((a, b), residuals[a][b])
    


        



side = 16

box = np.zeros((side, side))

a = 0
for b in range(1, side-1):
    box[a][b] = 3

a = side - 1
for b in range(1, side-1):
    box[a][b] = 0

b = 0
for a in range(1, side-1):
    box[a][b] = 2

b = side - 1
for a in range(1, side-1):
    box[a][b] = 2


for a in range(1, side-1):
    k = 3 - 0.2 * a
    for b in range(1, side-1):
        box[a][b] = k


for i in range(100):
    box = relax(box)
    res = residualMax(box)
    print(i, ':', 'argmax of residual is', res[0], ', maximum of residual is', res[1])


def fun(x, y):
    return box[x][y]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = y = np.arange(0.0, 2.0, 2/15)
x = y = np.append(x, 2.)
X, Y = np.meshgrid(x, y)
Z = box

ax.plot_surface(X, Y, Z)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()

# To see the contour lines, type [plt.contour(X, Y, Z)] in the python shell
# and then type [plt.show()].
