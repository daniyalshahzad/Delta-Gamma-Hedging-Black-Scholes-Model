# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from Black_Scholes import BS

import pdb

class hedge():
    
    def __init__(self, 
                 Tg=1, Kg=10, sigma = 0.2, 
                 Ndt = 101, Th=1.5, Kh=10,
                 sigma_real = 0.2, r=0, mu=0.05, S0 = 10,
                 k=0.005):
        
        self.Tg = Tg
        self.Kg = Kg
        self.Ndt = Ndt
        self.t = np.linspace(0,Tg, Ndt)
        self.dt = self.t[1]-self.t[0]

        self.Th = Th
        self.Kh = Kh 
        
        self.sigma=sigma
        self.sigma_real = sigma_real
        
        self.S0 = S0
        self.r = r
        self.mu = mu
        
        self.k = k
        
        self.BS = BS()
        
    def simulate_delta_hedge(self, batch_size = 256, units=10000):
        
        S = np.zeros((batch_size, self.Ndt))
        S[:,0] = self.S0
        
        M = np.zeros((batch_size, self.Ndt))
        M[:,0] = units*self.BS.CallPrice(S[:,0], self.Tg, self.Kg, self.sigma, self.r)
        
        alpha = np.zeros((batch_size, self.Ndt))
        alpha[:,0] = np.round(units*self.BS.CallDelta(S[:,0], self.Tg, self.Kg, self.sigma, self.r))

        M[:,0] -= alpha[:,0] * S[:,0] + np.abs(alpha[:,0])*self.k
        
        for i in range(self.Ndt-1):
            
            # new asset price
            dW = np.sqrt(self.dt) * np.random.randn(batch_size)
            S[:,i+1] = S[:,i] * np.exp((self.mu-0.5*self.sigma_real**2)*self.dt + 
                                       self.sigma_real*dW)
            
            if i < self.Ndt-2:
                # new hedge position
                alpha[:,i+1] = np.round(units*self.BS.CallDelta(S[:,i+1], self.Tg-self.t[i+1], 
                                                 self.Kg, self.sigma, self.r))
            
                M[:,i+1] = M[:,i]*np.exp(self.r*self.dt) \
                    - (alpha[:,i+1]-alpha[:,i])*S[:,i+1] \
                        - np.abs((alpha[:,i+1]-alpha[:,i]))*self.k
        
            else:
                M[:,i+1] = M[:,i]*np.exp(self.r*self.dt) \
                    + alpha[:,i]*S[:,i+1] - np.abs(alpha[:,i])*self.k\
                        - units*np.maximum(S[:,i+1]-self.Kg, np.zeros(batch_size))
                    
        return self.t, S, M, alpha
    
    def simulate_gamma_hedge(self, batch_size = 256, units=10000):
        
        S = np.zeros((batch_size, self.Ndt))
        S[:,0] = self.S0
        
        M = np.zeros((batch_size, self.Ndt))
        M[:,0] = units*self.BS.CallPrice(S[:,0], self.Tg, self.Kg, self.sigma, self.r)
        
        gamma_g = np.zeros((batch_size, self.Ndt))
        gamma_h = np.zeros((batch_size, self.Ndt))
        
        delta_g = np.zeros((batch_size, self.Ndt))
        delta_h = np.zeros((batch_size, self.Ndt))
        
        opt_h = np.zeros((batch_size, self.Ndt))
        
        opt_h[:,0] = self.BS.CallPrice(S[:,0], self.Th, self.Kh, self.sigma, self.r)
        delta_g[:,0] = self.BS.CallDelta(S[:,0], self.Tg, self.Kg, self.sigma, self.r)
        delta_h[:,0] = self.BS.CallDelta(S[:,0], self.Th, self.Kh, self.sigma, self.r)
        gamma_g[:,0] = self.BS.CallGamma(S[:,0], self.Tg, self.Kg, self.sigma, self.r)
        gamma_h[:,0] = self.BS.CallGamma(S[:,0], self.Th, self.Kh, self.sigma, self.r)
        
        alpha = np.zeros((batch_size, self.Ndt))
        alpha[:,0] = np.round(units*(-(gamma_g[:,0]*delta_h[:,0]/gamma_h[:,0])+delta_g[:,0]))
        
        gamma = np.zeros((batch_size, self.Ndt))
        gamma[:,0] = np.round(units*(gamma_g[:,0]/gamma_h[:,0]))

        M[:,0] -= alpha[:,0] * S[:,0] + np.abs(alpha[:,0])*self.k + gamma[:,0] * opt_h[:,0] + np.abs(gamma[:,0])*self.k
        
        for i in range(self.Ndt-1):
            
            # new asset price
            dW = np.sqrt(self.dt) * np.random.randn(batch_size)
            S[:,i+1] = S[:,i] * np.exp((self.mu-0.5*self.sigma_real**2)*self.dt + 
                                       self.sigma_real*dW)
            
            if i < self.Ndt-2:
                # new hedge position
                opt_h[:,i+1] = self.BS.CallPrice(S[:,i+1], self.Th-self.t[i+1], self.Kh, self.sigma, self.r)
                delta_g[:,i+1] = self.BS.CallDelta(S[:,i+1], self.Tg-self.t[i+1], self.Kg, self.sigma, self.r)
                delta_h[:,i+1] = self.BS.CallDelta(S[:,i+1], self.Th-self.t[i+1], self.Kh, self.sigma, self.r)
                gamma_g[:,i+1] = self.BS.CallGamma(S[:,i+1], self.Tg-self.t[i+1], self.Kg, self.sigma, self.r)
                gamma_h[:,i+1] = self.BS.CallGamma(S[:,i+1], self.Th-self.t[i+1], self.Kh, self.sigma, self.r)
        
                alpha[:,i+1] = np.round(units*(-(gamma_g[:,i+1]*delta_h[:,i+1]/gamma_h[:,i+1])+delta_g[:,i+1]))
                gamma[:,i+1] = np.round(units*(gamma_g[:,i+1]/gamma_h[:,i+1]))
            
                M[:,i+1] = M[:,i]*np.exp(self.r*self.dt) \
                    - (alpha[:,i+1]-alpha[:,i])*S[:,i+1] \
                        - np.abs((alpha[:,i+1]-alpha[:,i]))*self.k \
                            - (gamma[:,i+1]-gamma[:,i])*opt_h[:,i+1] \
                                - np.abs((gamma[:,i+1]-gamma[:,i]))*self.k
        
            else:
                opt_h[:,i+1] = self.BS.CallPrice(S[:,i+1], self.Th-self.Tg, self.Kh, self.sigma, self.r)
                M[:,i+1] = M[:,i]*np.exp(self.r*self.dt) \
                    + alpha[:,i]*S[:,i+1] - np.abs(alpha[:,i])*self.k \
                        + gamma[:,i]*opt_h[:,i+1] - np.abs(gamma[:,i])*self.k \
                            - units*np.maximum(S[:,i+1]-self.Kg, np.zeros(batch_size))
                    
        return self.t, S, M, alpha, gamma, opt_h, delta_g, delta_h
