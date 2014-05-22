import random as r
class Hash:
    """ This class defines a random hash function. When an object from this class is initialized, 
        it's seed is chosen at random and fixed. When called with a any hashable value, the seed is appnded to the value
        and then a random number is generated using the combination of seed and value as it's seed"""
    def __init__(self,range=2):
        self.range=range
        r.seed()
        self.seed=int(1000000*r.random())
    def map(self,x,range=None):
        if range==None: range=self.range
        r.seed((self.seed,x))
        return r.randint(0,range-1)