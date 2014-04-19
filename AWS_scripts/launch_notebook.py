#!/usr/bin/python
import sys,os
import subprocess as sp
import shlex
import re

root='/home/ubuntu/'
filename=root+'UCSD_BigData/AWS_scripts/NotebookCollections.md'

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
            #print name,path
            #check that the path exists.
            if not os.path.isdir(path):
                print 'Error: name=%s, path %s does not exist as a directory' % (name,path)
            else:
                D[name]=path
    file.close()
    return D


### Main ###

if len(sys.argv)<2:
    print 'not enough parameters:',sys.argv
    printFile(filename)
else:
    loc='none'
    name=sys.argv[1]
    DirectLink=re.match('@(\S+)',name)
    if DirectLink:
        loc= root+DirectLink.group(1)
        print 'Using direct link to location',loc
    else:
        D=parseFile(filename)
        if name in D.keys():
            loc=D[name]
            print 'Using collection link from',name,'to',loc
        else:
            print 'Could not find notebook directory, printing Collection' 
            printFile(filename)

    print 'Checking if ',loc,'exists as a directory',
    if not os.path.isdir(loc):
        print ' Directory does not exist!'
    else:
        print 'Launching ',loc
        os.chdir(loc)
#       command_line='ipython notebook --profile=nbserver &'
        command_line='ipython notebook --profile=nbserver'
        command = shlex.split(command_line)
        print 'current directory:',os.getcwd()
        print 'Command:',command
        sp.Popen(command)

