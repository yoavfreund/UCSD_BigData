""" Insert credentials into mrjob configuration file """
import sys, os, pickle
                    
if 'EC2_VAULT' in os.environ.keys():
    vault=os.environ['EC2_VAULT']
else:  # If EC2_VAULT is not defined, we assume we are in an EC2 instance
    vault='/home/ubuntu/Vault'
try:
    vaultname=vault+'/Creds.pkl'
    def check(key,Dict ):
        if not key in Dict.keys():
            sys.exit('The file: '+vaultname+' Does not contain the key "'+\
                     key+'" in the correct place"')

    with open(vaultname) as file:
        Creds=pickle.load(file)

    check('mrjob',Creds)
    keypair=Creds['mrjob']
    template=open('mrjob.conf.template').read()

    check('key_id',keypair)
    check('secret_key',keypair)
    filled= template % (keypair['key_id'],keypair['secret_key'])
    # print 'filled=\n',filled
    home=os.environ['HOME']
    outfile = home+'/.mrjob.conf'
    open(outfile,'wb').write(filled)
    print 'Created the configuration file:',outfile
except Exception, e:
    print e


