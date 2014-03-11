#!/usr/bin/python
from IPython.lib import passwd
import string,os,sys

filename='/home/ubuntu/.ipython/profile_nbserver/ipython_notebook_config.py'
password=passwd(sys.argv[1])
print 'inserting %s into file %s' % (password,filename)
input=open(filename,'r')
output=open(filename+'.py','w')
for line in input.readlines():
    if line.startswith('c.NotebookApp.password'):
        output.write("c.NotebookApp.password = u'"+password+"'\n")
    else:
        output.write(line)

os.rename(filename+'.py',filename)

print "=== END ==="

