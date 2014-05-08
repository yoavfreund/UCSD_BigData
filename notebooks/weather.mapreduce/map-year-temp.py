#!/bin/env python
import os,sys,re,pickle,coding
from numpy import *

dir='/oasis/projects/nsf/csd181/yfreund/weather/processing'

pkl_file = open(dir+'/Stat2Lat.pkl', 'rb')
Stat2Lat=pickle.load(pkl_file)
pkl_file.close()

pkl_file = open(dir+'/Dates.pkl', 'rb')
Days=pickle.load(pkl_file)
pkl_file.close()

Xtemps=ones(366)*200     #initialize temperatures to be outside the range [-100,+100]
Ntemps=ones(366)*200
current_year=0
format=re.compile('\s*(\S{11})(\d{4})(\d{4})([-\s\d]{5})(.)(.)(.)([-\s\d]{5})(.)(.)(.)')
for line in sys.stdin:
    matchObj=re.match(format,line)
    if matchObj:
        (Stat,year,monthday,minT,minTM,minTQ,minTS,maxT,maxTM,maxTQ,maxTS)=matchObj.groups()
        minT=float(minT)/10
        maxT=float(maxT)/10
        lat=int(Stat2Lat[Stat])
        lat=(lat+4)/10*10   # group the stations by latitude: [-14:-5][-4:5][6:15][16:25]...
                            #                                     -10    0    10     20 ...
        if current_year != 0 and current_year != year:
            coding.dump(lat,{'year':current_year,'Stat':Stat,'lat':lat,'Xtemps':Xtemps,'Ntemps':Ntemps})
        current_year=year
        day=Days[monthday]
        Xtemps[day]=maxT
        Ntemps[day]=minT
    else:
        sys.stderr.write('map-temp:No Match with |',line)

#dump last one in file
coding.dump(lat,{'year':current_year,'Stat':Stat,'lat':lat,'Xtemps':Xtemps,'Ntemps':Ntemps})
