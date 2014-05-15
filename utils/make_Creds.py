# copy this file to your "Vault" directory and then edit the entries below
# according to your credentials.

# Credentials in order to use Amazon EC2 and EMR:
# 'launcher' - the credentials that are needed in order to launch and
#             use your own ec2 instance.
# 'mrjob' - The credentials needed to submit a job to EMR through mrjob
# 'admin' - The credentials needed to administrate a mrjob job flow.
#           This set is for administrators only, students can ignore them.

Creds={'launcher':{'ID':'',\
                   'key_id':'',\
                   'secret_key':'',\
                   'ssh_key_name':'',\
                   'ssh_key_pair_file':'',\
                   'security_groups':['']},
       'mrjob':{'ID':'',
                'key_id':'',\
                'secret_key':'',\
                # the locations on s3 that mrjob should use for logs
                # and for scratch space. You need to create the
                # buckets first, using s3cmd or the web interface to
                # s3.
                's3_logs':'s3://your.bucket/logs',\
                's3_scratch':'s3://your.bucket/scratch'\
            },
}

import pickle

with open('Creds.pkl','wb') as pickle_file:
    pickle.dump(Creds,pickle_file)

