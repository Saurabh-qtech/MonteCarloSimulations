#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 22:39:14 2024

@author: saurabhchitnis
"""

#import libraries
import numpy as np


# simulate geometric brownian motion path of underlying
def simulate_gbm_paths(S0, r, delta, sigma, T, dt, N, seed=123):
    '''
    Simulate geometric Brownian motion paths using Euler method under risk-neutral measure.

    Parameters
    ----------
    S0 : float
        Underlying price at t = 0.
    r : float
        risk free intererst rate.
    delta : float
        div yield.
    sigma : float
        implied volatility.
    T : float
        Time ti maturity.
    dt : float
        time step.
    N : int
        number of paths.
    seed : int, optional
        seed number for generating random numbers. The default is 123.

    Returns
    -------
    S : np.array
        Simulated Stock price.
    t : np.array
        time array.

    '''
    
    # set random seed
    np.random.seed(seed)
    # number of time steps
    M = int(T/dt)
    t = np.linspace(0, T, M+1)      # time vector
    
    # Generate random normal variates
    
    
    # Initialize stock paths array
    S = np.zeros((N, M+1))
    S[:, 0] = S0   # Stock price at t = 0
    
    # Simulate paths using risk-free rate r instead of μ
    for i in range(M):
        
        dW = np.random.standard_normal(N) * np.sqrt(dt)
        S[:, i+1] = S[:, i] + S[:, i] * (r - delta) * dt + sigma* S[:, i]*dW
        #S[:, i+1] = S[:, i] * np.exp((r - delta - 0.5*sigma**2)*dt + sigma*dW)
    
    # return 
    return S, t