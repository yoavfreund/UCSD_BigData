#!/usr/bin/python
import sys,os
import subprocess as sp
import re

root='/home/ubuntu/'
filename=root+'scripts/NotebookCollections.md'

def printFile(filename):
    file=open(filename,'r')
    print '############### Available Notebook collections: ##############\n'
    for line in file.readlines():
        print line,
    file.close()
    return

def parseFile(filename):
    file=open(filename,'r')
    D={}
    for line in file.readlines():
        match=re.search(r'\#\#\#\#\s*__\[(\S+)\]__\s+(\S+)',line)
        if match:
            name=match.group(1); path=root+match.group(2)
            print name,path
            #check that the path exists.
            if not os.path.isdir(path):
                print 'Error: name=%s, path %s does not exist as a directory' % (name,path)
            else:
                D[name]=path
    file.close()
    return D


### Main ###

if len(sys.argv)<2:
    printFile(filename)
else:
    D=parseFile(filename)
    name=sys.argv[1]
    print name
    if name in D.keys():
        print 'Launching ',D[name] 
        os.chdir(D[name])
        sp.Popen(['ipython','notebook','--profile=nbserver','1>notebookKernel.out','2>notebookKernel.err','&'])
    else:
        print 'could not find a notebook collection called',name
        printFile(filename)
