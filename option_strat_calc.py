#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 7, 2020

@author: drb


Used to determine the historical theoretical prices of options 
Calculator is bs_model.py, also on my github
Will use last months volatililty annualized as vol figure
DTE will be (252/12) = 21 for monthly options  (approximation for each trading mo)
Strike prices will be first whole number above close, and " plus 5 (spread)
Risk-free rate is assumed in the model as 2% ***

Strategy is intended to NOT adjust dollar risk values based on 
present value of portfolio, but instead hold dollar risk constant 
(and thus vary percentages)

COLUMNS: Date Open High Low Close Adj_Close Volume

"""

import pandas as pd
import numpy as np
from bs_model import get_call 
import matplotlib.pyplot as plt


ROWS = 0   # time period (i.e. days, months)
ANNUALIZE = np.sqrt(12)


def main():
    file = 'SPY.csv'  # for example 
    #df = pd.read_csv(file, usecols=[0,1,2,3,4])
    df = pd.read_csv(file, nrows = ROWS, usecols=[0,1,2,3,4])  


    #vol_arr = []
    i = 1  # first row has no prior period vol data
    otm_percent = .05
    pv_start = 10000      # starting portfolio value in 1000s, used to allocate risk
    max_risk = .15     # percent of portfolio
    pv = pv_start      # value of portfolio, not used for risk allocation
    returns_list_dollars = []
    returns_list_percent = []
    pv_list = []
    market_return = round((df.iloc[ROWS-1,4] - df.iloc[1,4])/df.iloc[1,4],3)*100  # market return over period
    market_pv_list = []
    spread_list = []
    '''
    Generates list of returns in $, also in % terms, and tracks 
    portfolio value; also tracks historical volatility
    *** NEXT STEP is to price options using VIX
    '''
    for i in range(ROWS-1):
        market_return_period = (round((df.iloc[i,4]-df.iloc[i,1])/df.iloc[i,1],3))  # percent
        market_return_pv = (1+market_return_period) * pv   # new pv at EOP
        market_pv_list.append(market_return_pv)
        
        
        op = df.iloc[i-1,1]  # open price of prior period
        vol = np.std([df.iloc[i-1,2] - op, df.iloc[i-1,3] - op, df.iloc[i-1,4] - op]/op)
            # ^ vol of the period = stddev of High, Low, Close comp. to Open
        vol = round(vol*ANNUALIZE,3)
        #print "vol", vol
        s = round(df.iloc[i-1,4],2)    # stock price == Previous Close, S at option open
        price_target = (1+otm_percent)*s
        k_hi = round(price_target - (price_target % 1),2)
        k_lo = round(s - (s % 1),2)
        YTE = round((21.0/252),3)
        
        #vol_arr.append(vol)
        call_lo = round(get_call(s,k_lo,vol,YTE),2)
        call_hi = round(get_call(s,k_hi,vol,YTE),2)
        #print call_lo, call_hi
        price = (call_lo - call_hi)    # price to open spread, debit, in $
        close_price = df.iloc[i,4]    # no. i month's close price 
        break_even = s + price    # break even stock price
        max_profit_unit = k_hi - break_even    # difference in price values

        option_return_unit = min(max(close_price - break_even, -1*price),max_profit_unit)*100 # in $
        
        ''' Change PM style below - fixed or variable percent at risk % '''
        max_num_spreads = (max_risk * (pv_start) / (price*100)) 
        #max_num_spreads = (max_risk * (pv) / (price*100)) 
        max_num_spreads = max_num_spreads - (max_num_spreads % 1)    # max no. spreads given risk
        option_return = option_return_unit * max_num_spreads  # return for period in $
        option_return_percent = round((option_return/pv), 3)  # (chg in pv) / pv
        #print "or", option_return
        pv = round(pv + option_return,3)     # new portfolio value = old pv + change (in $)
        pv_list.append(pv)
        #print pv, "_______"
        returns_list_dollars.append(option_return)        # array of $ return figures
        returns_list_percent.append(option_return_percent)
        
    plt.plot(range(ROWS-1), pv_list, 'bo')     # plot
    #plt.plot(range(ROWS-1), market_return_list, 'go')     # plot

    plt.axis([0, (ROWS - (ROWS % 5)), min(pv_list), max(pv_list)])
    plt.show()

        
    
    return()


main()











