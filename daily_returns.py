#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:33:37 2019

@author: drb

Trend measurement tool for security prices. Takes Yahoo Finance .csv
of returns history, provides data o


"""

# version 2 of spyscraper.py
# daily_returns was "change"
# added volalitity calculator

import pandas as pd
import numpy as np

rows = 300

def main():
    file = 'SPY3.csv'     # for example
    #df = pd.read_csv(file, usecols=[0,1,2,3,4])
    df = pd.read_csv(file, nrows = rows, usecols=[0,1,2,3,4])  
    #print df.iloc[0:20]
    #print df.iloc[3,4]
        
    i = 5
    j = i + 1
    daily_returns = []
    pos_streak = 0
    streak_arr = []
    # If streak difference between previous and last is positive
    
    for i in range(rows-1):
        diff = round((df.iloc[j,4] - df.iloc[i,4])/df.iloc[i,4],3)   #close - close change
        if (diff > 0):         
            pos_streak += 1
        if diff <= 0 and pos_streak > 0:                 # if neg/0 and streak >= 1
            streak_arr.append(pos_streak)    # add streak to arr
            pos_streak = 0                   # reset streak
        daily_returns.append(round(diff,3))
    if pos_streak>0:
        streak_arr.append(pos_streak)    # case: still in positive streak at end data set
    
    #print daily_returns
    print  streak_arr
    vol = round(np.std(daily_returns),3)
    #vol_annual = round(vol * np.sqrt(252),3)  >>> to annualize one day?
    print vol
    
    
    #print(df.head(5), change)
        
    
    return()

main()