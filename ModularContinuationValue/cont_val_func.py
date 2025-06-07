#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 22:37:36 2024

@author: saurabhchitnis
"""

# continuation-value function
def cubic_func(x, a, b, c, d):
    '''
    calculate a cubic poly o/p based on argument
    
    Parameters
    ----------
    x : np.array
        input.
    a : np.array
        coefficient of x with degree = 0.
    b : np.array
        coefficient of x with degree = 1.
    c : np.array
        coefficient of x with degree = 2.
    d : np.array
        coefficient of x with degree = 3.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    """Third-order polynomial function for continuation value approximation."""
    
    return a + b*x + c*(x**2) + d*(x**3)