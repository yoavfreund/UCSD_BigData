" Insert credentials into mrjob configuration file "
import sys, os, pickle

if 'EC2_VAULT' in os.environ.keys():
    vault=os.environ['EC2_VAULT']
else:  # If EC2_VAULT is not defined, we assume we are in an EC2 instance
    vault='/home/ubuntu/Vault'
try:
    with open(vault+'/Creds.pkl') as file:
        Creds=pickle.load(file)
    print 'Creds=',Creds
    keypair=Creds['mrjob']
    print 'keypair=',keypair
    template=open('mrjob.conf.template').read()
    filled= template % (keypair['key_id'],keypair['secret_key'])
    home=os.environ['HOME']
    outfile = home+'/.mrjob.conf'
    open(outfile,'wb').write(filled)
    print 'Created the configuration file:',outfile
except Exception, e:
    print e


