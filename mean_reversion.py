#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:33:37 2019

@author: drb

Tool for determining the relationship between a security's distance from 
a selected moving average and the % returns that same following period, 
from close to close

Takes a .csv file in format from Yahoo Finance, converts to pandas dataframe
Plots returns over period as a function of % distance from MA


Variables to change are rows (days), ma_period, and future point 
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

rows = 500   
x_max = .03
x_min = 0
y_max = .03
y_min = -.02

def main():
    
    file = 'SPY3.csv'    # file name, for example
    #df = pd.read_csv(file, usecols=[0,1,2,3,4])
    df = pd.read_csv(file, nrows = rows, usecols=[0,1,2,3,4])  
    #print df.iloc[0:20]    # view data
    #print df.iloc[3,4]
        
    ma_period = 50   # (x) day moving avg   
    future_point = 25      # target date for returns
    master_arr = []   # 2D array for sorting, contains both dimensions of data
    
    for i in range(rows - (ma_period+1)):    # make sure index is within bounds
        if i >= ma_period:    # if at point in data where MA exists, given its size
            returns_point = round((df.iloc[future_point,4] - df.iloc[i,4])/df.iloc[i,4],3)   # Day i+MA - Day i close-close
            #returns_arr.append(returns_point)
            
            ma_point = round(np.average(df.iloc[(i-ma_period):ma_period,4]),3)    # find MA at point i
            point_ma_percentage = round(abs(df.iloc[i,4]-ma_point)/ma_point,3)  # % btwn price i, MA i
            #ma_percent_arr.append(point_ma_percentage)
            
            data_point = [point_ma_percentage, returns_point]  # create data point for 2d np array
            master_arr.append(data_point)
    master_arr = np.array(master_arr)
    #print master_arr
    #sorted_master = np.array((master_arr, key=lambda x:x[0]))   # sort 2D array by % from MA
    sorted_master = np.sort(master_arr)
    #print sorted_master


    sorted_returns = sorted_master[:,0]     # isolate data from master for plot
    sorted_percent_ma = sorted_master[:,1]

    plt.plot(sorted_percent_ma, sorted_returns, 'go')     # plot
    plt.axis([x_min, x_max, y_min, y_max])
    plt.show()

      
    return()

main()





