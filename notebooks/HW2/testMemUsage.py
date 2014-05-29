import resource,sys
from numpy import random
logfile=sys.stderr

for i in range(9):
    v=random.rand(10**i)
    logfile.write('size of vector=%10d, memory size: %s bytes\n'\
          %(len(v),resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))