###This is a python implementation of the original MATLAB RMT code described in Cawse-Nicholson et al. (2013)

###The code accepts a spectroscopic image in the form rows x columns x bands
###And a noise covariance matrix 

import h5py
import numpy as np

#%matplotlib inline 
from matplotlib import pyplot as plt
from numpy import linalg as LA

def RMT(img,N):
    #print("Starting RMT")
    #Compute mean spectrum and the centered image covariance matrix
    (bands,cols,rows) = img.shape
    n1 = rows * cols
    #print(n1)
    R = np.reshape(img,(bands,n1)) #flatten the image to bands x pixels

    #print("RMT: calculate n")
    mm = np.nansum(R,axis=0)
    n = np.sum(mm>0)   #compute n separately to account for masked pixels

    #print("RMT: mean normalize")
    m = np.nansum(R,axis=1)/n #mean image spectrum
    M = np.tile(m,[n1,1])     #tile to easily remove the mean from each pixel
    M[M<0] = 0 #removing the mean from the masked values will result in negatives

    #print("RMT: replace nans")
    R[np.isnan(R)] = 0    #nans will cause problems in the covariance and eigenvalue computation
    N[np.isnan(N)] = 0
    RM = R.T-M
    S = np.matmul(RM.T,RM) / n;      #centered image covariance
    
    #Set constants as per the Cawse-Nicholson et al (2013) paper
    #print("RMT: set constants")
    a=0.5
    b=0.5
    alpha = 0.5
    mu = 1/n*np.power(np.sqrt(n-a)+np.sqrt(bands-b),2)
    sig = 1/n*(np.sqrt(n-a)+np.sqrt(bands-b))*np.power(1/np.sqrt(n-a)+1/np.sqrt(bands-b),1/3)
    s = np.power(-3/2 * np.log(4*np.sqrt(np.pi) * alpha/100),2/3)
    sigma = mu + s*sig

    #print("RMT: compute eigenvalues")
    #Compute eigenvalues and eigenvectors
    eval_S, evec_S = LA.eig(S)

    #print("RMT: real eigenvals")
    eval_S = np.real(eval_S) #we expect real eigenvalues given that S is symmetric, but python gives +0j as a default
    evec_S = np.real(evec_S)
    sortind = np.flipud(np.argsort(eval_S)) #sort eigenvalues in descending order
    eval_S = eval_S[sortind]
    evec_S = evec_S[:,sortind]

    #print("RMT: sort eigenvalues")
    eval_Pi, evec_Pi = LA.eig(S-N)
    eval_Pi = np.real(eval_Pi)
    evec_Pi = np.real(evec_Pi)
    sortind2 = np.flipud(np.argsort(eval_Pi)) #sort eigenvalues in descending order
    eval_Pi = eval_Pi[sortind2]
    evec_Pi = evec_Pi[:,sortind2]

    #print("RMT: compare to threshold")
    #Compare each eigenvalue with threshold
    X = np.empty([bands])
    for loop in range(bands):
        X[loop] = np.matmul(np.matmul(evec_Pi[:,loop].T,N),evec_S[:,loop])/np.matmul(evec_Pi[:,loop].T,evec_S[:,loop])

    #print("RMT: find K")
    #ID is the number of eigenvalues that exceed the threshold
    K = np.sum(eval_S > X.T*sigma)
    return K, n