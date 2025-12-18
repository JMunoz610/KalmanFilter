import control as ct
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

data = loadmat('data.mat')

t = np.squeeze(data['t'])
z = np.squeeze(data['z'])   # noisy measurment
ys = np.squeeze(data['ys']) # true measurment
u = np.squeeze(data['u'])
n = len(t)

Ac = np.array([[0,1,0],[0,0,1],[-6,-11,-6]])
Bc = np.array([[0],[0],[1]])
Cc = np.array([20,9,1])
Dc = np.array([0])

sysC = ct.ss(Ac,Bc,Cc,Dc)
sysD = ct.c2d(sysC,1)

A = sysD.A
B = sysD.B
C = sysD.C
D = sysD.D

x_ = np.zeros((3, n))    
xhat = np.zeros((3, n))  
x_[:, 0] = np.array([0, 0, 0])      # initial state
xhat[:, 0] = np.array([0, 0, 0])    # initial state estimate

P = 5*np.eye(3)     # error covariance for initial state guess
Q = 0.001*np.eye(3) # error covariance for dynamics (we trust this)
R = 10*np.eye(1);   # error covariance for measurements (we dont trust this)

for i in range(1, n):
    x_[:, i] = A @ xhat[:, i-1] + (B.flatten() * u[i-1])
    P = A @ P @ A.T + Q
    K = P @ C.T @ np.linalg.inv(C @ P @ C.T + R)
    xhat[:, i] = x_[:, i] + (K.flatten() * (z[i] - C @ x_[:, i]))
    P = (np.eye(3) - K @ C) @ P
    
yhat = C@xhat

plt.plot(t, ys, label='ys')
plt.plot(t, z, 'rs-', label='z')
plt.plot(t, yhat.T, 'gx-', label='yhat')

plt.xlabel('Time')
plt.ylabel('Output')
plt.legend()
plt.grid(True)
plt.show()