import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.optimize import minimize

A = np.array([[-0.89, 1.00], [-0.62, -0.04], [-0.87, 0.63], [1.21, -0.42], [-1.86, 1.00]])
# T = np.array([1, 2, 3])
r = 0.0002451
# x = np.array([1, 2, 3])
m = 5
n = 2
# c = 299792458
# timp_curent = time.time()
D = np.array([2.90, 1.70, 1.76, 1.77, 2.71])

def f(x):
    return sum((np.linalg.norm(x-A) - D - r)**2)

res = minimize(f, np.array([1.2, 1.5]), method='BFGS', options={'disp': True})



print(A[:,0])

'''
def f1(x0, x1):
    pass

fig0 = plt.figure(0)
ax = plt.axes(projection='3d')
ix = np.linspace(-4, 4, 10  2)
iy = np.linspace(-4, 4, 10 ** 2)

X, Y = np.meshgrid(ix, iy)
plt.contour(X, Y, Z, 50)


X = A[:,0]
Y = A[:,1]
Z = D
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z)
plt.show()

'''