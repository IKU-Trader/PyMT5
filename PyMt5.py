# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:21:36 2022

@author: IKU-Trader
"""

import pandas as pd
import MetaTrader5 as mt5
from mt5_const import *
from time_utility import timestamp2jst
 
class PyMt5:
    def __init__(self, market):
        self.market = market
        if not mt5.initialize():
            print("initialize() failed")
            mt5.shutdown()
        #print('Version: ', mt5.version())
        pass
    
    def close(self):
        mt5.shutdown()
        pass
    
    def convert(self, data):
        if data is None:
            return [], [], {}
        
        timeJst = []
        timestamp = []
        o = []
        h = []
        l = []
        c = []
        v = []
        ohlcv = []
        ohlc = []
        for d in data:
            values = list(d)
            jst = timestamp2jst(values[0])
            timeJst.append(jst)
            timestamp.append(jst.timestamp())
            o.append(values[1])
            h.append(values[2])
            l.append(values[3])
            c.append(values[4])
            v.append(values[7])
            ohlc.append([values[1], values[2], values[3], values[4]])
            ohlcv.append([values[1], values[2], values[3], values[4]])
            
        dic = {}
        dic[TIMEJST] = timeJst
        dic[TIMESTAMP] = timestamp
        dic[OPEN] = o
        dic[HIGH] = h
        dic[LOW] = l
        dic[CLOSE] = c
        dic[VOLUME] = v
        return ohlc, ohlcv, dic
     
    def download(self, timeframe:str, size:int=99999):
        d = mt5.copy_rates_from_pos(self.market, TIMEFRAME[timeframe][0] , 0, size) 
        ohlc, ohlcv, dic = self.convert(d)
        return ohlc, ohlcv, dic

    def downloadRange(self, timeframe, begin_jst, end_jst):
        utc_from = self.jst2serverTime(begin_jst)
        utc_to = self.jst2serverTime(end_jst)
        d = mt5.copy_rates_range(self.stock, timeframeConstant(timeframe) , utc_from, utc_to) 
        data = self.convert2Array(d)
        return data
    
    def downloadTicks(self, timeframe, from_jst, size=100000):
        utc_from = self.jst2serverTime(from_jst)
        d = mt5.copy_ticks_from(self.stock, timeframeConstant(timeframe) , utc_from, size, mt5.COPY_TICKS_ALL) 
        data = self.convert2Array(d)
        return data

# -----
    
    
def test(size):
    server = PyMt5('DOWUSD')
    ohlc, ohlcv, dic =  server.download('M5', size=size) 
    print(ohlc)
    print(dic[TIMEJST])

    
if __name__ == "__main__":
    test(10)