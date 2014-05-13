# Credentials in order to use Amazon EC2 and EMR:
# 'launcher' - the credentials that are needed in order to launch and
#             use your own ec2 instance.
# 'mrjob' - The credentials needed to submit a job to EMR through mrjob
# 'admin' - The credentials needed to administrate a mrjob job flow.

Creds={'launcher':{'ID':ID,
                   'key_id':key_id,
                   'secret_key':secret_key,\
                   'ssh_key_name':ssh_key_name,\
                   'ssh_key_pair_file':ssh_key_pair_file,\
                   'security_groups':security_groups}
       'mrjob':{'ID':ID,
                'key_id':key_id,
                'secret_key':secret_key}
       'admin':{}
   }

import pickle,os
vault=os.environ['EC2_VAULT']

with open(vault+'/Cred.pkl','wb') as pickle_file:
    pickle.dump(Creds,pickle_file)

