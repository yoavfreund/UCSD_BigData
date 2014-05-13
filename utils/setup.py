#!/usr/bin/env python
""" This is a script for collecting the credentials, 
choosing one of them, and creating a pickle file to hold them """

import pprint
import sys,os
from glob import glob
import AWS_keypair_management
import pickle

vault=os.environ['EC2_VAULT']
print 'files in'+ vault+'/* :\n','\n'.join(glob(vault+'/*'))

AWS_KM=AWS_keypair_management.AWS_keypair_management()
(Creds,bad_files) =AWS_KM.Get_Working_Credentials(vault)

print '\n Here are the credentials I found:'
pp=pprint.PrettyPrinter()
pp.pprint(Creds)

if len(Creds)>1:
    print "You have creds for ",\
        ' '.join(['(%1d),%s' % (i,Creds.keys()[i])\
                  for i in range(len(Creds.keys()))])
    ID_index=raw_input("Which one do you want to use? (index)? ")
    ID=Creds.keys()[int(ID_index)]
else:
    ID=Creds.keys()[0]

entry=Creds[ID]
print 'Using the 0 elements from \n',entry
key_id=entry['Creds'][0]['Access_Key_Id']
secret_key=entry['Creds'][0]['Secret_Access_Key']
# password=entry['Passwords'][0]

security_group=raw_input('What security group do you want to use? ')
security_groups=[security_group]

ssh_key_name=raw_input('What is your ssh key name? ')
ssh_key_pair_file='///'
while not os.path.isfile(ssh_key_pair_file):
    ssh_key_pair_file=raw_input('What is the name (full path) of your keypair file (extension .pem)')

print 'ID: %s, key_id: %s, secret_key: %s, password: %s' % (ID,key_id,secret_key,password)
print 'ssh_key_name:%s, ssh_key_pair_file:%s'%(ssh_key_name,ssh_key_pair_file)
print 'security groups',security_groups

with open(vault+'/Creds.pkl','wb') as pickle_file:
    pickle.dump({'ID':ID,'key_id':key_id,'secret_key':secret_key,\
                 'password':password,\
                 'ssh_key_name':ssh_key_name,\
                 'ssh_key_pair_file':ssh_key_pair_file,\
                 'security_groups':security_groups}
                ,pickle_file)

