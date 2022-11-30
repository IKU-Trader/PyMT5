# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 23:16:46 2022

@author: IKU-Trader
"""


from datetime import datetime, timedelta, timezone
import calendar
import pytz

TIMEZONE_TOKYO = timezone(timedelta(hours=+9), 'Asia/Tokyo')

def timestamp2jst(utc_server):
    t = datetime.fromtimestamp(utc_server, TIMEZONE_TOKYO)
    if isSummerTime(t):
        dt = 1
    else:
        dt = 2
    t -= timedelta(hours=dt)
    return t

def isSummerTime(date_time):
    day0 = dayOfLastSunday(date_time.year, 3)
    tsummer0 = utcTime(date_time.year, 3, day0, 0, 0)
    day1 = dayOfLastSunday(date_time.year, 10)
    tsummer1 = utcTime(date_time.year, 10, day1, 0, 0)
    if date_time > tsummer0 and date_time < tsummer1:
        return True
    else:
        return False
    
def utcTime(year, month, day, hour, minute):
    local = datetime(year, month, day, hour, minute)
    return pytz.timezone('UTC').localize(local)    
    
    
def dayOfLastSunday(year, month):
    '''dow: Monday(0) - Sunday(6)'''
    dow = 6
    n = calendar.monthrange(year, month)[1]
    l = range(n - 6, n + 1)
    w = calendar.weekday(year, month, l[0])
    w_l = [i % 7 for i in range(w, w + 7)]
    return l[w_l.index(dow)]   