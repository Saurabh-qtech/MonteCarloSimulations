#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 22:49:56 2024

@author: saurabhchitnis
"""

#import libraries
import numpy as np
from sim_gbm_paths import *
from cont_val_func import *
from scipy.optimize import curve_fit


def american_option_price(S0, K, r, delta, sigma, T, dt, N, option_type='call', seed=123):
    '''
    calculate American option price using regression method II.

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
    
    # Set terminal payoff
    if option_type.lower() == 'call':  # call option
        g = np.maximum(S[:, -1] - K, 0)
        
    else:  # put option
        g = np.maximum(K - S[:, -1], 0)
    
    tau_k = M * np.ones(N)
    
    # Backward induction
    for i in range(M-1, 0, -1):
        
        # Current stock prices vector
        S_current = S[:, i]
        
        # get index of in-the-money
        if option_type.lower() == 'call':  # call option
            ITM_val = np.maximum(S_current - K, 0)
            
        else:  # put option
            ITM_val = np.maximum(K - S_current, 0)
           
        ITM_indices = np.where(ITM_val > 0)[0]
        
        S_opt_req = S_current[ITM_indices]
        
        # Future discounted option values
        g_opt_req = g[ITM_indices] * np.exp(-r*(tau_k[ITM_indices] - i) * dt)
        
        # Fit continuation value function
        init_guess = np.zeros(4)  # initial guess
        popt, _ = curve_fit(cubic_func, S_opt_req, g_opt_req,  p0=init_guess)  # fitted values
        
        # for in the money only
        
        for k in ITM_indices :
            
            C_hat = cubic_func(S_current[k], *popt)
            
            # immediate excersie values
            if option_type.lower() == 'call':        # american call
                exercise_value = np.maximum(S_current[k] - K, 0)
            else:                       # american put
                exercise_value = np.maximum(K - S_current[k], 0)
            
            # update g and tau_k
            if exercise_value >= C_hat :
                g[k] = exercise_value
                tau_k[k] = i
                
    # initialize C0_hat
    C0_hat = 0
    
    for k in range(N) :
        C0_hat += np.exp(-r*tau_k[k]*dt) * g[k]
    
    C0_hat = C0_hat / N

    if option_type.lower() == 'call':  # call option
        exercise_intial = S0 - K
    else:  # put option
        exercise_intial = K - S0

    option_price = np.maximum(exercise_intial, C0_hat )
    
    return option_price

    