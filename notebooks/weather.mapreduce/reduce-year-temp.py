#!/bin/env python
import os,sys,re,pickle, base64
from array import *
from numpy import *
import Statistics,coding

global k_eigen # the number of top eigen-vectors to keep.
k_eigen=10

def inRange(V,thr):
    f=zeros(len(V))
    for i in range(len(V)):
        f[i]= (abs(V[i])<thr)
    return f

def out(key):
    min_summary=min_stat.compute(k_eigen)
    max_summary=max_stat.compute(k_eigen)
    Value={'min_summary':min_summary, 'max_summary':max_summary,'years':years}
    coding.dump(key,Value)
    
global min_stat,max_stat,years
min_stat=Statistics.VecStat(366,1)
max_stat=Statistics.VecStat(366,1)
years=[]

current_lat=None
lat=None

for line in sys.stdin:
    (lat,Value)=coding.load(line)
    year=Value['year']
    Stat=Value['Stat']
    elat=Value['lat']    # the exact latitude (the key is lat rounded to 10 degrees)
    Xtemps=Value['Xtemps']
    Ntemps=Value['Ntemps']
    
    if(current_lat != lat and current_lat !=None):
        out(lat)
        min_stat.reset()
        max_stat.reset()
        years=[]

    current_lat=lat
    
    years.append(year)
    min_stat.accum(Ntemps,inRange(Ntemps,100))
    max_stat.accum(Xtemps,inRange(Xtemps,100))

if lat != None:
    out(lat) # dump out the last item.
