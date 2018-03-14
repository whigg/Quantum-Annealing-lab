# -*- coding: utf-8 -*-
"""
@author: Jakub und PawKuk 
"""
import numpy as np
import matplotlib.pyplot as plt
import time

def getHeffnm(spins, beta, gamma, i, j, M, J):
    E = spins[i,j]*(spins[(i+1)%spins.shape[0],j]+spins[i-1,j])/M#*J[i,j]
    E += np.log(1/np.tanh(beta*gamma/M)) * spins[i,j] * (spins[i,(j+1)%spins.shape[1]] + spins[i,(j-1)%spins.shape[1]]) / (2*beta)
    return E
    
def getJ(N,M):
    J = np.zeros((N,M))
    for i in range (N-1):   
        J[i+1,i] = 1  
        J[i,i+1] = 1
    J[N-1,0] = 1
    J[0,M-1] = 1        
    return J

def flipSpin(spins,beta,gamma,tMax):
    magHistory = np.empty(tMax)
    magnetization = np.sum(spins)
    for i in range (tMax):
        n = np.random.randint(0, spins.shape[0])
        m = np.random.randint(0, spins.shape[1])      
        H = getHeffnm(spins, beta, gamma, n ,m , M, J)
        if np.random.random() < np.exp(-beta*H):  
            spins[n,m] *= spins[n,m]*-1
            magnetization -= 2*spins[n,m]
        magHistory[i] = magnetization
    return magHistory/(spins.shape[0]*spins.shape[1])

def plot(a, T, gamma, num):
    fig=plt.figure(figsize=(7,5))
    axis=fig.add_subplot(212)
    axis.imshow(a, cmap='Greys', interpolation='none', origin='upper', 
                extent=[T[0],T[T.size-1],gamma[0],gamma[gamma.size-1]],aspect="auto")
    plt.title("moduł magnetyzacji")
    axis.set_xlabel("T")
    axis.set_ylabel("Gamma")
    plt.show()
         
t0 = time.time()
k = 1
gammaMax = 1
TMax = 1
N = 10 
M = 10

J = getJ(M,N)
tMax = 1000
num = 50
Gamma = np.linspace(0.0001,gammaMax,num)

T = np.linspace(0.001, TMax, num)
Beta = 1/(k*T)
mag = np.empty((Gamma.size, Beta.size))

plt.close('all')
fig = plt.figure(figsize=(10,10))
axis=fig.add_subplot(211)
        
for b in range (Beta.size):
    for g in range (Gamma.size):
        spins = np.random.randint(0,2,(M,N)) * 2 - 1  ### matrix (MxN)  M^N>
        magHistory = flipSpin(spins,Beta[b],Gamma[g],tMax)         
        plt.title("magHistory")         
        plt.plot(magHistory, color=(0,0,(g+1)/Gamma.size), linewidth=1) #bardziej czarne - mniejsza gamma
        axis.set_xlabel("iteracja")
        axis.set_ylabel("magnetyzacja")
        mag[g][b] = magHistory[tMax-1]/tMax

plot(np.asarray(np.abs(mag)),T,Gamma,num)
print("Elapsed time = ", time.time() - t0)
    
