import base64,pickle,zlib,sys
import pdb
"""
Functions for encoding and decoding arbitrary object into ascii 
so that they can be passed through the hadoop streaming interface.
"""

def loads(eVal):
    """ Decode a string into a value """
    return pickle.loads(zlib.decompress(base64.b64decode(eVal)))

def dumps(Value):
    """ Encode a value as a string """
    return base64.b64encode(zlib.compress(pickle.dumps(Value),9))

def load_line(line):
    (key,eVal)=line.split('\t')
    return(key,loads(eVal))

def dump_line(key,Value,out=sys.stdout):
    out.write(key,dumps(Value))

