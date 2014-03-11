#!/usr/bin/python
import subprocess as sp
import re

ps = sp.Popen(["ps", "aufx"],stdout=sp.PIPE)

for line in ps.stdout.readlines():
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
