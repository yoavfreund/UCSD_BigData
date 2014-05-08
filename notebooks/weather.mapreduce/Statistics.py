"""
A module for computing simple statistics - mean, variance, covariance
s1: Statistics for a single random variable
s2: Statistics for two random variables
"""
from numpy import *
from random import random
import sys,copy,traceback

class s:
    """ compute the mean of a scaler """
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.n=0
        self.sum=0.0
        
    def accum(self,value):
        """ Add a value to the statistics """
        self.n += 1
        self.sum += value
    def compute(self):
        """ Returns the count and the mean """
        if self.n==0:
            return (0,0)
        self.mean = self.sum / self.n
        return (self.n,self.mean)
    def add(self,stat):
        """ add two statistics """
        self.n += stat.n
        self.sum += stat.sum

class VecStat:
    """ Compute first and second order statistics of vectors of a fixed size n """
    def __init__(self,n,compute_cov):
        self.compute_cov=compute_cov
        self.n=n
        # Create V: a list of length n
        self.V=[]  
        for i in range(n):
            self.V.append(s())

        if not self.compute_cov:
            self.Var=copy.deepcopy(self.V)
        else:
            # create a matrix to store 2nd order statistics
            self.Cov=[]
            for i in range(n):
                self.Cov.append(copy.deepcopy(self.V))

    def reset(self):
        n=self.n
        for i in range(n):
            self.V[i].reset()
            if not self.compute_cov:
                self.Var[i].reset()
            else:
                for j in range(n):
                    self.Cov[i][j].reset()
        
    def accum(self,U,f):
        """ accumulate statistics:
        U: vector of floats (length n)
        f: binary vector. 1 indicates that the corresponding valur in U is good
        """
        #check lengths of U and f
        if(len(U) != self.n):
            error='in Statistics.secOrdStat.accum: length of V='+str(self.n)+' not equal to length of U='+str(len(U))+'/n'
            sys.stderr.write(error)
            raise StandardError, error
        elif(len(f) != self.n):
            error='in Statistics.secOrdStat.accum: length of V='+str(self.n)+' not equal to length of U='+str(len(f))+'/n'
            sys.stderr.write(error)
            raise StandardError, error
        else:
            #do the work
            for i in range(self.n):
                if f[i]:
                    # update first order statistics
                    self.V[i].accum(U[i])
                    # update second order statistics
                    if not self.compute_cov:
                        self.Var[i].accum(U[i]**2)
                    else:
                        for j in range(self.n):
                            if f[j]:
                                self.Cov[i][j].accum(U[i]*U[j])

    def compute(self,k=5):
        """
        Compute the statistics. k (default 5) is the number of eigenvalues that are kept
        """
        n=self.n
        count=zeros(n)
        mean=zeros(n)
        std=zeros(n)

        # Compute means
        for i in range(n):
            (count[i],mean[i])=self.V[i].compute()

        if not self.compute_cov:
            for i in range(n):
                (c,mean_s2) = self.Var[i].compute()
                std[i]=sqrt(mean_s2 - mean[i]**2)
            return {'count':count,'mean':mean,'std':std}

        else:
            # Compute covariance matrix
            cov=zeros((n,n))
            for i in range(n):
                for j in range(n):
                    (k,mxy) = self.Cov[i][j].compute()
                    cov[i][j]=mxy - mean[i]*mean[j]
            for i in range(n):
                std[i]=sqrt(max(0,cov[i][i]))

            try:
                (eigvalues,eigvectors)=linalg.eig(cov)
                order=argsort(-abs(eigvalues))	# indexes of eigenvalues from largest to smallest
                eigvalues=eigvalues[order]		# order eigenvalues
                eigvectors=eigvectors[order]	# order eigenvectors
                eigvectors=eigvectors[1:k]		# keep only top k eigen-vectors
                for v in eigvectors:
                    v=v[order]     # order the elements in each eigenvector

            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stderr)
            
                eigvalues=None
                eigvectors=None
            return {'count':count,'mean':mean,'std':std,'eigvalues':eigvalues,'eigvectors':eigvectors}
        
    def add(self, s):
        """ add the statistics of s into self """
        n=self.n
        for i in range(n):
            self.V[i].add(s.V[i])
            for j in range(n):
                self.Cov[i][j].add(s.Cov[i][j])
    
##################################
if __name__=="__main__":
    #Test the module.
    
    n=2
    A=secOrdStat(2*n)

    for i in range(10000):
        A.accum(concatenate([random()*ones(n),random()*ones(n)*10]),ones(2*n))

    C=A.compute(3)
    print 'A.compute()=',C
    
