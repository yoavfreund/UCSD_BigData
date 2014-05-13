import pickle
vault=''
with open(vault+'/RootCred.pkl','wb') as pickle_file:
    pickle.dump({'ID':ID,'key_id':key_id,'secret_key':secret_key,\
                 'password':password,\
                 'ssh_key_name':ssh_key_name,\
                 'ssh_key_pair_file':ssh_key_pair_file,\
                 'security_groups':security_groups}
                ,pickle_file)
