import traceback
from functools import wraps
from sys import stderr
"""this decorator is intended for decorating a function, not a
generator.  Therefor to use it in the context of mrjob, the generator
should call a function that handles a single input records, and that
function should be decorated.

The reason is that if a generator throws an exception it exits and
cannot process any more records.

"""
def ECatch(func):
    print type(func)
    f_name=func.__name__
    @wraps(func)
    def inner(self,*args,**kwargs):
        try:
            self.increment_counter(self.__class__.__name__,'total in '+f_name,1)
            return func(self,*args,**kwargs)
        except Exception as e:
            self.increment_counter(self.__class__.__name__,'errors in '+f_name,1)
            stderr.write('Error:')
            stderr.write(str(e))
            traceback.print_exc(file=stderr)
            stderr.write('Arguments were %s, %s\n'%(args,kwargs))
            pass
    return inner        