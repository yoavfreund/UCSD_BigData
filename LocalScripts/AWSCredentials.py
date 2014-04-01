### AWS credentials: ####
# Change entries here to match your own #
# Get values for the first two entries from the "Security crediential" Tab
# Under in the menu under your name.
aws_access_key_id='Key ID'
aws_secret_access_key='Key'
# Get the Keypair in the EC2 Dashboard page.
keyPairFile="<~/.ssh/KeyFilename.pem>" # name of file keeping local key
key_name="key name" # name of keypair (not name of file where key is stored)
# Set the security group On the EC2 page (You will need to add IP addresses if
# you want to connect from a place previously unauthorized.
security_groups=['GroupName']
### End of AWS credentials ####
