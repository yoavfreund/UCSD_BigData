#!/usr/bin/env python
"""### A Script for Launching and managing an iPython notebook server on AWS ###
 # Written by Yoav Freund, March 2014

### Before you run this script ###
 Before running this script, you need to install boto on your local machine (not ec2).
 See https://pypi.python.org/pypi/boto. 
 You can use either "sudo pip install boto" or "sudo easy_install boto"

### Security credentials ###
 In order to launch a notebook you need to first establish credentials on AWS. Set these credentials
by editing the values in the section titled "AWS Credentials" below.

Here are the steps you need to follow to achieve this

 1. Open an AWS account  
 2. Create a key-pair so that  you can connect securely to your instances.  
 3. Create a Security group to define which IPs can connect to your instances and through which ports.
 You need to complete these steps only one time. Later sessions can use the same credentials. If you are registered to the
 class you will get a credit of $100 towards your use of AWS. To get this credit goto the page "consolidated billing" (xxxx) and send a request to the class instructor.
 
 #### Security credentials ####
 In order to start your EC2 Session you need two things:
 
 1. A key-pair
 2. A security group
 
 Before you try to connect to an EC2 instance make sure that the
 security group that you are using contains the IP address that you
 are connecting from. The security group estricts which IP addresses
 are allowed to connect to which ports. Best set using the AWS web
 interface.

 Google "my ip" will give you your current address. Then go to the EC2
 web interface and make sure that you have rules for connecting from
 your current address to all of the ports.

"""

from AWSCredentials import *

ami='ami-278a974e'              # Image configured for big data class
# AMI name: DataScienceEigenVector. These two lines updates 4/8/2014

# ### Definitions of procedures ###
import boto.ec2
import time
import subprocess
import sys,re,webbrowser,select
from string import rstrip
import argparse

# open connection
def open_connection(aws_access_key_id,
                    aws_secret_access_key):
    conn = boto.ec2.connect_to_region("us-east-1",
                                      aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key)
    print 'Created Connection=',conn
    return conn

#Get information about all current instances
def report_all_instances():
    reservations = conn.get_all_instances()
    instances=[]
    count=0
    instance_alive=-1 # points to a pending or running instance, -1 indicates none
    pending=True     # indicates whether instance_alive refers to a pending instance.

    print 'time: ',time.strftime('%H:%M:%S')

    for reservation in reservations:
        print '\nReservation: ',reservation
        for instance in reservation.instances:
            print 'instance no.=',count,'instance name=',instance,'DNS name = ',instance.public_dns_name
            print 'Instance state=',instance.state
            if instance_alive==-1:
                if instance.state =='running' and pending:
                    instance_alive=count # point to first running instance
                    pending=False
                elif instance.state =='pending' and pending:
                    instance_alive=count # point to first pending instance
                print 'ssh -i %s %s@%s' % (keyPairFile,login_id,instance.public_dns_name)
            instances.append(instance)
            count+=1

    return (instances,instance_alive)

def kill_all_notebooks():
    command=['scripts/CloseAllNotebooks.py']
    def emptyCallBack(line): return False
    Send_Command(command,emptyCallBack)

def set_password(password):
    if len(password)<6:
        sys.exit('Password must be at least 6 characters long')
    command=["scripts/SetNotebookPassword.py",password]
    def emptyCallBack(line): return False
    Send_Command(command,emptyCallBack)

def Send_Command(command,callback):
    init=time.time()
    
    ssh_process = subprocess.Popen(ssh+command,
                                   shell=False,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

    def dataWaiting(source):
        return select.select([source], [], [], 0) == ([source], [], [])

    endReached=False
    while not endReached:
        if dataWaiting(ssh_process.stdout):
            line=ssh_process.stdout.readline()
            if len(line)>0:
                print line,
                
                endReached = endReached | callback(line)

                matchEnd=re.match('=== END ===',line)
                if matchEnd:
                    endReached=True

        time.sleep(0.01)

def Launch_notebook(name=''):
    init=time.time()
    
    command=["scripts/launch_notebook.py",name,"2>&1"]

    def detect_launch_port(line):
        match=re.search('IPython\ Notebook\ is\ running\ at\:.*system\]\:(\d+)/',line)
        if match:
            port_no=match.group(1)
            print 'opening https://'+instance.public_dns_name+':'+port_no+'/'
            webbrowser.open('https://'+instance.public_dns_name+':'+port_no+'/')
            return True
        return False

    Send_Command(command,detect_launch_port)


if __name__ == "__main__":

    # parse parameters
    parser = argparse.ArgumentParser(description='launch an ec2 instance and then start an ipython notebook server')
    parser.add_argument('-c','--collection',
                        help='Choice of notebook collection (if non-existant=print out options)')
    parser.add_argument('-i','--create_image',
                        help='Create an AMI from the current state of the (first) instance')
    parser.add_argument('-p','--password',
                        help='Specify password for notebook (if missing=use existing password)')
    parser.add_argument('-t','--instance_type',default='t1.micro',
                        help='Type of instance to launch, Common choices are t1.micro,c1.medium,m3.xlarge, for more info see: https://aws.amazon.com//ec2/instance-types/')
#Some common choices:
#              vCPU     ECU	Memory (GiB)	Instance Storage (GB)	Linux/UNIX Usage
#----------------------------------------------------------------------------------------
#t1.micro	1	Variable    0.615	 EBS Only	        $0.020 per Hour
#c1.medium	2	5	    1.7	         1 x 350	        $0.145 per Hour
#m3.xlarge	4	13	    15	         2 x 40 SSD	        $0.450 per Hour
#----------------------------------------------------------------------------------------
    parser.add_argument('-k','--kill_all',dest='kill',action='store_true',default=False,
                        help='close all running notebook servers')

    args = vars(parser.parse_args())

    # print 'args=',args

    # open connection to aws
    print 'The regions you are connected to are:',boto.ec2.regions()
    try:
        conn=open_connection(aws_access_key_id,aws_secret_access_key)
    except:
        e = sys.exc_info()[0]
        print "Error: %s" % e
        sys.exit("failed to connect to AWS")

    #Get and print information about all current instances
    login_id='ubuntu'
    (instances,instance_alive) = report_all_instances()

    if instance_alive==-1: # if there is no instance that is pending or running, create one
        instance_type=args['instance_type']
        print 'launching an ec2 instance, instance type=',instance_type,', ami=',ami
        reservation=conn.run_instances(ami,
                                       key_name=key_name,
                                       instance_type=instance_type,
                                       security_groups=security_groups)
        print 'Launched Instance',reservation
        
        (instances,instance_alive) = report_all_instances()

    # choose an instance and check that it is running
    instance = instances[instance_alive]
    while instance.state != 'running':
        print '\r',time.strftime('%H:%M:%S'),instance.state,
        time.sleep(5)
    print '\n Instance Ready!',time.strftime('%H:%M:%S'),instance.state
    ssh=['ssh','-i',keyPairFile,('%s@%s' % (login_id,instance.public_dns_name))]
    print "To connect to instance, use:\n",' '.join(ssh)

    if(args['password'] != None):
        set_password(args['password'])
    
    if(args['kill']):
        print "closing all notebook servers"
        kill_all_notebooks()
        sys.exit()

    if(args['collection'] != None):
        Launch_notebook(args['collection'])

    if(args['create_image'] != None):
        print "creating a new AMI called",args['create_image']
        instance.create_image(args['create_image'])



