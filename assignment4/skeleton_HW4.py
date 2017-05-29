# Filename: HW4_skeleton.py
# Author: Florian Kaum
# Edited: 15.5.2017
# Edited: 19.5.2017 -- changed evth to HW4

import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math
import sys
from scipy.stats import multivariate_normal


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming
def plotGaussContour(mu, cov, xmin, xmax, ymin, ymax, title):
    npts = 100
    delta = 0.025
    stdev = np.sqrt(cov)  # make sure that stdev is positive definite

    x = np.arange(xmin, xmax, delta)
    y = np.arange(ymin, ymax, delta)
    # noinspection PyPep8Naming,PyPep8Naming
    X, Y = np.meshgrid(x, y)

    # matplotlib.mlab.bivariate_normal(X, Y, sigmax=1.0, sigmay=1.0, mux=0.0, muy=0.0, sigmaxy=0.0) -> use cov directly
    # noinspection PyPep8Naming
    Z = mlab.bivariate_normal(X, Y, stdev[0][0], stdev[1][1], mu[0], mu[1], cov[0][1])
    plt.plot([mu[0]], [mu[1]], 'r+')  # plot the mean as a single point
    # noinspection PyPep8Naming
    CS = plt.contour(X, Y, Z)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title(title)
    plt.show()
    return


# noinspection PyPep8Naming
def ecdf(realizations):
    x = np.sort(realizations)
    # noinspection PyPep8Naming
    Fx = np.linspace(0, 1, len(realizations))
    return Fx, x

def d(para, anchor):
    return np.linalg.norm(anchor - para)

def calcVarianz(ri, point, anchors, nrAnchor, nrSample):
    sigmas = []
    for i in range(nrAnchor):
        sigma_i = 0
        for j in range(nrSample):
            sigma_i += np.power(ri[j, i] - d(point, anchors[i]), 2)
        sigma_i /= nrSample
        sigmas.append(sigma_i)
    return sigmas

def calcLambda(ri, point, anchors, nrAnchor, nrSample):
    lambdas = []
    for i in range(nrAnchor):
        lambda_i = 0
        for j in range(nrSample):
            if ri[j, i] >= d(point, anchors[i]):
                lambda_i += 1 / (ri[j, i] - d(point, anchors[i]))
        lambda_i /= nrSample
        lambdas.append(lambda_i)
    return lambdas

def derivationOfPoint(x_i, y_i, x, y):
    derivationInX = -1 / 2 * np.power((np.power((x_i - x), 2) + np.power((y_i - y), 2)), 1 / 2) * 2 * (x_i - x)
    derivationInY = -1 / 2 * np.power((np.power((x_i - x), 2) + np.power((y_i - y), 2)), 1 / 2) * 2 * (y_i - y)

    return (derivationInX, derivationInY)

def jacobi(p_start, p_anchor):
    jacobi_mat = np.ndarray((p_anchor.shape[0], p_start.shape[0]))
    for i, anchor in enumerate(p_anchor):
        derivation = derivationOfPoint(anchor[0], anchor[1], p_start[0], p_start[1])
        jacobi_mat[i, 0] = derivation[0]
        jacobi_mat[i, 1] = derivation[1]

    return jacobi_mat

def ds(p_start, p_anchor):
    distances = np.ndarray((p_anchor.shape[0], 1))
    for i, anchor in enumerate(p_anchor):
        distances[i] = d(p_start, anchor)

    return distances


def LeastSquaresGN(p_anchor, p_start, r, max_iter, tol):

    while True :
        max_iter -= 1
        p_old = p_start
        jacobian_inv = np.dot(np.linalg.inv(np.dot(jacobi(p_start, p_anchor).T, jacobi(p_start, p_anchor))), jacobi(p_start, p_anchor).T)
        diffs = ((r - ds(p_start, p_anchor).transpose()).transpose())
        p_start = p_start - np.dot(jacobian_inv, diffs)
        if d(p_start, p_old) > tol or max_iter > 0:
            break
    return p_start

# START OF CI ASSIGNMENT 4
# -----------------------------------------------------------------------------------------------------------------------

# positions of anchors
p_anchor = np.array([[5, 5], [-5, 5], [-5, -5], [5, -5]])
NrAnchors = np.size(p_anchor, 0)

# true position of agent
p_true = np.array([[2, -4]])

# plot anchors and true position
plt.axis([-6, 6, -6, 6])
for i in range(0, NrAnchors):
    plt.plot(p_anchor[i, 0], p_anchor[i, 1], 'bo')
    plt.text(p_anchor[i, 0] + 0.2, p_anchor[i, 1] + 0.2, r'$p_{a,' + str(i) + '}$')
plt.plot(p_true[0, 0], p_true[0, 1], 'r*')
plt.text(p_true[0, 0] + 0.2, p_true[0, 1] + 0.2, r'$p_{true}$')
plt.xlabel("x/m")
plt.ylabel("y/m")
# plt.show()

# 1.2) maximum likelihood estimation of models---------------------------------------------------------------------------
# 1.2.1) finding the exponential anchor----------------------------------------------------------------------------------
# TODO
# insert plots

# 1.2.3) estimating the parameters for all scenarios---------------------------------------------------------------------

# scenario 1
data = np.loadtxt('HW4_1.data', skiprows=0)
NrSamples = np.size(data, 0)
# TODO
print("varianzen:   ", calcVarianz(data, p_true, p_anchor, NrAnchors, NrSamples))
print("Lambdas:     ", calcLambda(data, p_true, p_anchor, NrAnchors, NrSamples))
# scenario 2
data = np.loadtxt('HW4_2.data', skiprows=0)
NrSamples = np.size(data, 0)
# TODO

for i in range(4):
    plt.clf()
    plt.hist(data.transpose()[i])
    plt._show()


print("varianzen:   ", calcVarianz(data, p_true, p_anchor, NrAnchors, NrSamples))
print("Lambdas:     ", calcLambda(data, p_true, p_anchor, NrAnchors, NrSamples))
# scenario 3
data = np.loadtxt('HW4_3.data', skiprows=0)
NrSamples = np.size(data, 0)
# TODO
print("varianzen:   ", calcVarianz(data, p_true, p_anchor, NrAnchors, NrSamples))
print("Lambdas:     ", calcLambda(data, p_true, p_anchor, NrAnchors, NrSamples))
# 1.3) Least-Squares Estimation of the Position--------------------------------------------------------------------------
# 1.3.2) writing the function LeastSquaresGN()...(not here but in this file)---------------------------------------------
# TODO

# 1.3.3) evaluating the position estimation for all scenarios------------------------------------------------------------

# choose parameters
# tol = ... # tolerance
# maxIter = ...  # maximum number of iterations

# store all N estimated positions
p_estimated = np.zeros((NrSamples, 2))

for scenario in range(1, 5):
    if (scenario == 1):
        data = np.loadtxt('HW4_1.data', skiprows=0)
    elif (scenario == 2):
        data = np.loadtxt('HW4_2.data', skiprows=0)
    elif (scenario == 3):
        data = np.loadtxt('HW4_3.data', skiprows=0)
    elif (scenario == 4):
        # scenario 2 without the exponential anchor
        data = np.loadtxt('HW4_2.data', skiprows=0)
    NrSamples = np.size(data, 0)

    # perform estimation---------------------------------------
    # #TODO
    p_start = np.array([[1,1]]).transpose()
    for i in range(0, NrSamples):
        p_start = LeastSquaresGN(p_anchor, p_start, data[i], 20000, 0.5)
    # calculate error measures and create plots----------------
    # TODO
    print(p_start)

# 1.4) Numerical Maximum-Likelihood Estimation of the Position (scenario 3)----------------------------------------------
# 1.4.1) calculating the joint likelihood for the first measurement------------------------------------------------------
# TODO

# 1.4.2) ML-Estimator----------------------------------------------------------------------------------------------------

# perform estimation---------------------------------------
# TODO

# calculate error measures and create plots----------------
# TODO

# 1.4.3) Bayesian Estimator----------------------------------------------------------------------------------------------

# perform estimation---------------------------------------
# TODO

# calculate error measures and create plots----------------
# TODO
