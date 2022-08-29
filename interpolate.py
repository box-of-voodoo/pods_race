import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

x = np.array([23, 24, 24, 25, 25])
y = np.array([13, 12, 14, 12, 13])

# append the starting x,y coordinates
x = np.r_[x, x[0]]
y = np.r_[y, y[0]]

# fit splines to x=f(u) and y=g(u), treating both as periodic. also note that s=0
# is needed in order to force the spline fit to pass through all the input points.
tck, u = interpolate.splprep([x, y], s=0, per=True)
print(tck)
print()
print(u)
# evaluate the spline fits for 1000 evenly spaced distance values
t = np.linspace(0, 1, 1000)
xi, yi = interpolate.splev(t, tck)

# plot the result
ax = plt.subplot(1, 3,1)
ax.plot(x, y, 'or')
ax.plot(xi, yi, '-b')
ax2 = plt.subplot(1,3,2)
normxi = (xi - np.min(xi))/(np.max(xi)-np.min(xi))
ax2.plot(normxi,'red')
gradxi = np.gradient(xi,t[1]-t[0])
normgxi = (gradxi - np.min(gradxi))/(np.max(gradxi)-np.min(gradxi))
ax2.plot(normgxi)
grad2xi = np.gradient(gradxi,t[1]-t[0])
n2gxi = (grad2xi - np.min(grad2xi))/(np.max(grad2xi)-np.min(grad2xi))
ax2.plot(n2gxi)

ax3 = plt.subplot(1,3,3)
z = np.array([xi,yi])
print("\n\n")
gradi = np.gradient(z,t[1]-t[0])

# print(gradi)
# print(gradi[0].shape)
ax3.plot(gradi[1][1])

plt.show()


