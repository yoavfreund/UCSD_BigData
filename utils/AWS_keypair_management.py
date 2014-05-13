from glob import glob
from string import strip
from os import chdir,getcwd
from mrjob.emr import EMRJobRunner
import json,pprint

import sys,os
#possible home directories for "UCSD_Big_data"
home_dirs=['/home/ubuntu','/Users/yoavfreund/BigData']

class AWS_keypair_management:
    def test_key_pair(self,Access_Key_Id,Secret_Access_Key):
        try:
            JobRunner = EMRJobRunner(aws_access_key_id=Access_Key_Id,aws_secret_access_key=Secret_Access_Key)
            return True
        except:
            return False

    def Get_Working_Credentials(self,path):
        """ check all files in the path directory, find the files that 
        contain key-pairs in the format downloaded from AWS and check which
        of these AWS key pairs is active.
        """
        old_dir=getcwd()
        chdir(path)
        credentials_header='User Name,Access Key Id,Secret Access Key'
        passwords_header='User Name,Password,Direct Signin Link'
        Key_Table={}
        bad_key_files=[]
        for filename in glob('*'):
            with open(filename,'r') as file:
                header_line=strip(file.readline())
                ######## Credentials ###########
                if header_line==credentials_header:
                    for line in file.readlines():
                        (User_Name,Access_Key_Id,Secret_Access_Key)=strip(line).split(',')
                        User_Name=User_Name[1:-1]
                        print filename,'AWS creds:',User_Name,Access_Key_Id
                        if self.test_key_pair(Access_Key_Id,Secret_Access_Key):
                            print "an active key pair"
                            if not User_Name in Key_Table.keys():
                                Key_Table[User_Name]={'Creds':[], 'Passwords':[]}
                            Key_Table[User_Name]['Creds'].append({
                                'Access_Key_Id':Access_Key_Id,'Secret_Access_Key':Secret_Access_Key})
                        else:
                            print filename,"an inactive key pair"
                            bad_key_files.append(filename)
                ######## Passwords ###########
                if header_line==passwords_header:
                    for line in file.readlines():
                        (User_Name,password,direct_url)=strip(line).split(',')
                        User_Name=User_Name[1:-1]
                        print filename,' Password for ',User_Name
                        if not User_Name in Key_Table.keys():
                            Key_Table[User_Name]={'Creds':[], 'Passwords':[]}
                        Key_Table[User_Name]['Passwords'].append(password)
        chdir(old_dir)
        return Key_Table,bad_key_files

        def insert_creds_into_conf(self,keypair):
            " Insert credentials into mrjob configuration file "
            try:
                template=open('/home/ubuntu/UCSD_BigData/utils/mrjob.conf.template').read()
                filled= template % (keypair['Access_Key_Id'],keypair['Secret_Access_Key'])
                open('/home/ubuntu/.mrjob.conf','wb').write(filled)
                return True
            except Exception, e:
                print e
                return False

if __name__=='__main__':
    import os, sys, pickle
    from glob import glob
    path=sys.argv[1]
    print 'scanning directory',path
    AWS_KM=AWS_keypair_management()
    (Creds,bad_files) = AWS_KM.Get_Working_Credentials(path)
    with open(path+'/Creds.jsn','wb') as file:
        json.dump(Creds,file)

    print Creds
    print '------------------------'

    pp=pprint.PrettyPrinter(stream=open(path+'/Creds.pprnt','wb'))
    pp.pprint(Creds)

    print 'Removing files with inactive keys:',bad_files

    for filename in bad_files:
        os.remove(path+'/'+filename)

    #create an AWS file for each ID:
    Template = open('AWSTemplate','r').read()
    for username in Creds.keys():
        file=open(path+'/AWS'+username+'.py','w')
        entry=Creds[username]
        awspair=entry['Creds'][0]
        (aws_id,aws_secret)=(awspair['Access_Key_Id'],awspair['Secret_Access_Key'])
        password=entry['Passwords'][0]
        file.write(Template%(username,aws_id,aws_secret,password))
        file.close()

    

