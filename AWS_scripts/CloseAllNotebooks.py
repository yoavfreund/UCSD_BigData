#!/usr/bin/python
import subprocess as sp
import re,os

if 'OSE_HOST' in os.environ.keys() and os.environ['OSE_HOST'] == 'POWER_MACOSX':
    ps=sp.Popen(["ps", "-x"],stdout=sp.PIPE)
else:
    ps = sp.Popen(["ps", "aufx"],stdout=sp.PIPE)

for line in ps.stdout.readlines():
    if 'OSE_HOST' in os.environ.keys() and os.environ['OSE_HOST'] == 'POWER_MACOSX':
            match=re.match('(\d+)\s.*ipython\ notebook',line)
    else:
        match=re.match('ubuntu\s+(\d+)\s.*ipython\ notebook',line)
    if match:
        print line,
        PID=match.group(1)
        print 'killing notebook process',PID
        kill=sp.call(['kill','-9',PID])
        if kill==0:
            print 'killed',PID
        else:
            print 'failed to kill',PID

print "=== END ==="
