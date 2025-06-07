#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 22:36:38 2024

@author: saurabhchitnis

objective : Monte Carlo simulation for the valuation of American Options using the algorithm of regression method II:

"""

from sim_gbm_paths import *
from american_price import *
import pandas as pd
from tabulate import tabulate
import numpy as np

def main () :
    
    # initialize parameters of option
    S0 = 100
    r = 0.03
    delta = 0.025
    sigma = 0.75
    T = 1 
    K = 100
    N = 1000

    #Calculate prices for both time steps
    results = []
    for dt in [0.01, 0.001]:
        
        # calculate call price
        call_price = american_option_price(S0, K, r, delta, sigma, T, dt, N, 'call',123)
        
        # calculate put price
        put_price = american_option_price(S0, K, r, delta, sigma, T, dt, N, 'put',123)
        
        # save to resulats
        results.append([dt, call_price, put_price])
        



        
    # Create formatted output table
    df = pd.DataFrame(results, columns=['Δt', 'American Call', 'American Put'])
    df['Δt'] = df['Δt'].apply(lambda x: f'{x:.3f}')
    df['American Call'] = df['American Call'].apply(lambda x: f'{x:.6f}')
    df['American Put'] = df['American Put'].apply(lambda x: f'{x:.6f}')
       

    # print output
    print("\nMonte Carlo Simulation Results for American Options")
    print("Parameters:")
    print(f"S₀ = ${S0}, K = ${K}, r = {r}, δ = {delta}, σ = {sigma}, T = {T}, N = {N}")
    print("\nOption Prices:")
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    
    
main()
    



   
