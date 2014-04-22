from boto.s3.connection import S3Connection
# To use boto you should first set up a file named .boto in your root directory
# and in it put your aws public and secret access keys: 
# (remove the # from the beginning of the following lines, d'oh!)
#[Credentials]
#aws_access_key_id = xxxxxxxxxxxxxxxxxxxx
#aws_secret_access_key = xxxxxxxxxxxxxxxxxxxxxx
import ../LocalScripts/AWSCredentials.py

conn=S3Connection()
rs = conn.get_all_buckets()
rs
b=rs[0]
b.set_acl('public-read')
b.get_acl()

pairs=b.get_all_keys()
pairs
type(pairs[0])

key=pairs[0]
key

file=open('test.tif','w')
key.get_contents_to_file(file)
file.close()
