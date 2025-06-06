#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 22:49:56 2024

@author: saurabh
"""

#import libraries
import numpy as np
from sim_gbm_paths import *
from cont_val_func import *
from scipy.optimize import curve_fit


def american_option_price(S0, K, r, delta, sigma, T, dt, N, option_type='call', seed=123):
    '''
    calculate American option price using regression method I.

    Parameters
    ----------
    S0 : float
        Underlying price at t = 0.
    K : float
        option strike price.
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
    option_type : str, optional
        DESCRIPTION. The default is 'call'.
    seed : int, optional
        seed for random number generator. The default is 123.

    Returns
    -------
    option_price : float
        price of the option.

    '''
    
    # Simulate paths using risk-free rate
    S, t = simulate_gbm_paths(S0, r, delta, sigma, T, dt, N, seed)
    M = len(t) - 1
    
    # Initialize option values array
    V = np.zeros_like(S)
    
    # Set terminal payoff
    if option_type.lower() == 'call':  # call option
        V[:, -1] = np.maximum(S[:, -1] - K, 0)
    else:  # put option
        V[:, -1] = np.maximum(K - S[:, -1], 0)
    
    # Backward induction
    for i in range(M-1, 0, -1):
        
        # Current stock prices vector
        S_current = S[:, i]
        
        # Future discounted option values
        V_curr = V[:, i+1] * np.exp(-r*dt)
        
        # Fit continuation value function
        init_guess = np.zeros(4)  # initial guess
        popt, _ = curve_fit(cubic_func, S_current, V_curr,  p0=init_guess)  # fitted values
        
        
        # Calculate continuation values
        C_hat = cubic_func(S_current, *popt)
        
        # Calculate immediate exercise values
        if option_type.lower() == 'call': # american call
            exercise_value = np.maximum(S_current - K, 0)
        else:  # american put
            exercise_value = np.maximum(K - S_current, 0)
        
        # Update option values
        V[:, i] = np.maximum(exercise_value, C_hat)
    
    # Calculate option price

    #v0 =  np.sum(V[:, 0]) / N
    
    #return v0#*np.exp(-r*dt)
    

    if option_type.lower() == 'call':  # call option
        exercise_intial = S0 - K
    else:  # put option
        exercise_intial = K - S0

    option_price = np.maximum(exercise_intial, np.mean(V[:,1] * np.exp(-r*dt)) )
    
    return option_price

    
