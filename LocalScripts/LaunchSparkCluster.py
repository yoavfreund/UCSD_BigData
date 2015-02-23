#!/usr/bin/env python
"""### A Script for Launching and managing a Spark cluster on AWS ###
 # Written by Julaiti Alafate based on LaunchNotebookServer.py by Yoav Freund, February 2015

This script launch a Spark cluster on AWS using the default scripts in Spark official release.

### Security credentials ###
 In order to launch a Spark cluster you need to first establish credentials on AWS.
 Set these credentials by editing the values in the file ../../Vault/AWSCredentials.py

Here are the steps you need to follow to achieve this

 1. Open an AWS account  
 2. Create a key-pair so that  you can connect securely to your instances.  
 3. Create a Security group to define which IPs can connect to your instances and through which ports.
 You need to complete these steps only one time. Later sessions can use the same credentials. If you are registered to the
 class you will get a credit of $100 towards your use of AWS. To get this credit goto the page "consolidated billing" (xxxx) and send a request to the class instructor.
 
This script depends on Spark source code, specifically the ec2/ directory. You can download it from https://spark.apache.org/downloads.html.

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

# TODO #
    * Write a helper to generate spark setting configurations (i.e. $EC2_VAULT/SparkEC2.pkl)

"""

import pickle
import sys, os
import subprocess
import argparse


# TODO: this script intended to be used by the default Spark AMI and is not tested yet to work on other AMIs.
# ami='ami-18d33e70'             # Image configured for big data class

# Read Credentials 
try:
    vault=os.environ['EC2_VAULT']
    file=open(vault+'/Creds.pkl')
    ALL_Creds=pickle.load(file)
    Creds=ALL_Creds['launcher']
    # print Creds
    aws_access_key_id=Creds['key_id']
    aws_secret_access_key=Creds['secret_key']
    user_name=Creds['ID']
    keyPairFile=Creds['ssh_key_pair_file'] # name of local file storing keypair
    key_name=Creds['ssh_key_name']         # name of keypair on AWS
    security_groups=Creds['security_groups'] # security groups for controlling access
except Exception, e:
    print e
    sys.exit('could not read credentials')

# Read Spark EC2 settings
try:
    vault=os.environ['EC2_VAULT']
    file=open(vault+'/SparkEC2.pkl')
    ec2_settings=pickle.load(file)
    # print ec2_settings
    spark_path = ec2_settings["spark_path"]
    hdfs_size = ec2_settings["hdfs_size"]
    spot_price = ec2_settings.get("spot_price", "")
    zone = ec2_settings["zone"]
    region = ec2_settings["region"]
    cluster_name = ec2_settings["cluster_name"]
    instance_type = ec2_settings["instance_type"]
    slaves = ec2_settings["slaves"]
    ganglia = ec2_settings.get("ganglia", True)
except Exception, e:
    print e
    sys.exit('could not read Spark EC2 settings')


if __name__ == "__main__":

    # parse parameters
    parser = argparse.ArgumentParser(description='launch a Spark cluster on Amazon EC2 intances')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--launch', action='store_true',
        help="""Launch a new Spark cluster on Amazon EC2""")
    group.add_argument('-r', '--resume', action='store_true',
        help="""In case slave nodes launches fails, restart setup process on existing cluster.""")
    group.add_argument('-d', '--destroy', action='store_true',
        help="""Shutdown the cluster, delete all contents on the cluster, and remove all instances.""")
    group.add_argument('-g', '--login', action='store_true',
        help="""Login to the master node of the cluster""")
    group.add_argument('--stop', action='store_true',
        help="""Pause the cluster. Note that spot instances cannot be paused.""")
    group.add_argument('--restart', action='store_true',
        help="""Restart the stopped cluster.""")

    args = vars(parser.parse_args())

    # print 'args=',args

    env = ['AWS_SECRET_ACCESS_KEY=' + aws_secret_access_key, 'AWS_ACCESS_KEY_ID=' + aws_access_key_id]
    command = env + [os.path.join(spark_path, 'ec2/spark-ec2'), '-k', key_name, '-i', keyPairFile, '-r', region]
    conf = ['-z', zone, '-s', str(slaves), '-t', instance_type, '--ebs-vol-size=' + str(hdfs_size)]
    if spot_price:
        conf.append('--spot-price=' + spot_price)
    if not ganglia:
        conf.append('--no-ganglia')

    if args['launch']:
        subprocess.call(" ".join(command + conf + ['launch', cluster_name]), shell=True)

    if args['resume']:
        subprocess.call(" ".join(command + ['launch', '--resume', cluster_name]), shell=True)

    if args['stop']:
        subprocess.call(" ".join(command + ['stop', cluster_name]), shell=True)

    if args['restart']:
        subprocess.call(" ".join(command + ['start', cluster_name]), shell=True)

    if args['destroy']:
        subprocess.call(" ".join(command + ['stop', cluster_name]), shell=True)

    if args['login']:
        subprocess.call(" ".join(command + ['login', cluster_name]), shell=True)

