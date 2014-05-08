import base64,pickle,zlib,sys
import pdb

def load(line):
    (key,eVal)=line.split('\t')
    Value=pickle.loads(zlib.decompress(base64.b64decode(eVal)))
    return(key,Value)
    
def dump(key,Value,out=sys.stdout):
    out.write("%s\t%s\n" % (key, base64.b64encode(zlib.compress(pickle.dumps(Value),9))))
