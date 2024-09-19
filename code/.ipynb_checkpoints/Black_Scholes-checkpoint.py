# -*- coding: utf-8 -*-
import numpy as np
from scipy.stats import norm
import pdb

class BS():
    
    def CallPrice(self, S, T, K, sigma, r):
        
        dp = (np.log(S/K) + (r+0.5*sigma**2)*T)/(np.sqrt(T)*sigma)
        dm = (np.log(S/K) + (r-0.5*sigma**2)*T)/(np.sqrt(T)*sigma)
        
        return S*norm.cdf(dp) - K*np.exp(-r*T)*norm.cdf(dm)
        
    def CallDelta(self, S, T, K, sigma, r):
        
        dp = (np.log(S/K) + (r+0.5*sigma**2)*T)/(np.sqrt(T)*sigma)
        
        return norm.cdf(dp)
    
    def CallGamma(self, S, T, K, sigma, r):
        
        dp = (np.log(S/K) + (r+0.5*sigma**2)*T)/(np.sqrt(T)*sigma)
        
        return norm.pdf(dp)/(S*sigma*np.sqrt(T))
