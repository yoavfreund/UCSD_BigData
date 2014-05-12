from glob import glob
from string import strip
from os import chdir
from mrjob.emr import EMRJobRunner

def test_key_pair(Access_Key_Id,Secret_Access_Key):
    try:
        JobRunner = EMRJobRunner(aws_access_key_id=Access_Key_Id,aws_secret_access_key=Secret_Access_Key)
        return True
    except:
        return False
    
def Get_Working_Credentials(path):
    """ check all files in the path directory, find the files that 
    contain key-pairs in the format downloaded from AWS and check which
    of these AWS key pairs is active.
    """
    chdir(path)
    credentials_header='User Name,Access Key Id,Secret Access Key'
    Key_Table={}
    bad_key_files=[]
    for filename in glob('*'):
        with open(filename,'r') as file:
            header_line=strip(file.readline())
            if header_line==credentials_header:
                # print '"%s"'%header_line
                for line in file.readlines():
                    (User_Name,Access_Key_Id,Secret_Access_Key)=strip(line).split(',')
                    User_Name=User_Name[1:-1]
                    print filename,User_Name,Access_Key_Id,Secret_Access_Key
                    if test_key_pair(Access_Key_Id,Secret_Access_Key):
                        print "an active key pair"
                        if not User_Name in Key_Table.keys():
                            Key_Table[User_Name]=[]
                        Key_Table[User_Name].append({
                            'Access_Key_Id':Access_Key_Id,'Secret_Access_Key':Secret_Access_Key})
                    else:
                        print filename,"an inactive key pair"
                        bad_key_files.append(filename)
    return Key_Table,bad_key_files

def insert_creds_into_conf(keypair):
    try:
        template=open('/home/ubuntu/UCSD_BigData/utils/mrjob.conf.template').read()
        filled= template % (keypair['Access_Key_Id'],keypair['Secret_Access_Key'])
        open('/home/ubuntu/.mrjob.conf','wb').write(filled)
        return True
    except Exception, e:
        print e
        return False
