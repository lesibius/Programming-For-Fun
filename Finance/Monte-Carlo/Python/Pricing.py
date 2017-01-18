# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 10:28:21 2017

@author: clem
"""

import math
import numpy.random
import scipy.stats
import matplotlib.pyplot as plt
import sklearn.utils as sku


class Path:
    """
    Class to represent the path of a random variable following a Brownian motion (e.g. stock price)
    """
    def __init__(self,s0,nPeriod,deltaT):
        """
        Parameters
        ----------
        s0: float
            Initial value of the random variable
        nPeriod: int
            Number of period to generate
        deltaT: float
            Inter-period time interval
            
        Returns
        -------
        None
        """
        self.NPeriod = nPeriod
        self.DeltaT = deltaT
        self.Values = [s0 for i in range(nPeriod)]
    
    def GetLastItem(self):
        """
        Returns the last value of the Path instance
        
        Parameters
        ----------
        None
        
        Returns
        -------
        type: float
            Last value of the Path instance
        """
        return self.Values[self.NPeriod-1]    
    
    def __setitem__(self,ind,item):
        """
        Set the value of an item in the Path value list        
        
        Parameters
        ----------
        ind: int
            Index in the random variable path list
        item:
            Value to set
            
        Returns
        -------
        None
        """
        self.Values[ind] = item
    
    def __getitem__(self,ind):
        """
        Returns a value of an item from the Path value list with the index provided
        
        Parameters
        ----------
        ind: int
            Index of the item to return
            
        Returns
        -------
        type: float
            Value of the random variable at the given index
        """
        return self.Values[ind]
    
    def GetItemByDate(self,date):
        """
        Return the value of the random variable at a given date
        
        Parameters
        ----------
        date: float
            Date for which the random variable value should be returned
            
        Returns
        -------
        type: float
            Value of the random variable at the selected date
        """
        frac, ind = math.modf(date / self.DeltaT)
        ind=int(ind)
        if frac < 0.000001:
            return self[ind]
        else:
            return frac*self[ind]+(1-frac)*self[ind+1]
            
    def Plot(self):
        """
        Plot a graph of the path
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        plt.plot([self.DeltaT * period for period in range(self.NPeriod)],self.Values)

class PathGenerator:
    """
    Class generating Path instances to price derivatives
    """
    def __init__(self,nPath,totaltime,deltaT,model, drift, vol,**kwargs):
        """
        Parameters
        ----------
        nPath: int
            Number of path to generate
        totaltime: float
            Total time of each path
        deltaT: float
            Time interval between two periods
        drift: float/function
            Drift of the Brownian motion
        model: str
            Name of the model to use. Currently, only "black-scholes" supported
        vol: float/function
            Volatility of the Brownian motion
        **kwargs: optional arguments to provide for certain model
        """
        self.TotalTime = totaltime
        self.NPath = nPath
        self.NPeriod = int(totaltime/deltaT)
        self.DeltaT = deltaT
        self.Drift = drift
        self.Vol = vol
        
        if model.lower() in ['bs','black-scholes','black scholes','merton','black-scholes-merton','black scholes merton']:           
            self.DriftFun = self._BSDriftFun
            self.VolFun = self._BSVolFun
            
    
    def _BSDriftFun(self,S,t,rt,sigmat):
        """
        Drift function used by the Black-Scholes-Merton model
        """
        return self.Drift * S
        
    def _BSVolFun(self,S,t,r,sigmat):
        """
        Volatility function used by the Black-Scholes-Merton model
        """
        return self.Vol * S * numpy.random.normal(0.0,1.0)
        
    def _initPaths(self,s0):
        """
        Init the attribute Paths as a list of Path instance
        
        Parameters
        ----------
        s0: float
            Initial value of the random variable
            
        Returns
        -------
        None
        """
        self.Paths = [Path(s0,self.NPeriod,self.DeltaT) for i in range(self.NPath)]
        
    def GeneratePaths(self,s0):
        """
        Generate the Path instance to price derivatives
        
        Parameters
        ----------
        s0: float
            Initial value of the random variable
            
        Returns
        -------
        None
        """
        self._initPaths(s0)
        for i in range(self.NPath):
            S = s0
            for j in range(self.NPeriod-1):
                t = (j+1)*self.DeltaT
                S = S + self.DriftFun(S,t,0.01,0) * self.DeltaT + self.VolFun(S,t,0.01,0) * math.sqrt(self.DeltaT)
                self.Paths[i][j+1] = S
                
    def Discount(self,date):
        """
        Returns the discount factor for a given date
        
        Warnings
        --------
        Only provide the discount factor, and do not implement r=f(t) yet        
        
        Parameters
        ----------
        date: float
            Date of the cash flow
            
        Returns
        -------
        type: float
            Discount factor for the selected date
        """
        return math.exp(-date * 0.01)
        
    def __getitem__(self,ind):
        """
        Return a Path instance from the path list
        
        Parameters
        ----------
        ind: int
            Index of the Path instance
            
        Returns
        -------
        type: Path  
            Path at the ind index
        """
        return self.Paths[ind]
        
    def __iter__(self):
        """
        Returns an iterable list of the Path instance
        
        Parameters
        ----------
        None
        
        Returns
        -------
        type: list
            List of Path instance
        """
        for path in self.Paths:
            yield path
        

class Option:
    """
    Option class
    """
    def __init__(self,payoff,underlying,expiry=None):
        """
        Parameters
        ----------
        payoff: function(Path -> float)
            Payoff function
        underlying: PathGenerator
            Underlying PathGenerator instance
        expiry: float (optional)
            Expiry date (or last expirty date) of the derivative
        """
        self.Underlying = underlying
        self.Payoff = payoff
        if expiry is None:
            self.Expiry = underlying.TotalTime
        else:
            self.Expiry = expiry
        
        
    def _GetValue(self,path):
        """
        Compute the value at expiry date of the option"
        
        Parameters
        ----------
        path: Path
            Path for which the value should be computed
            
        Returns
        -------
        type: float
            Value at expiry
        """
        return self.Payoff(path) * self.Underlying.Discount(self.Expiry)
        
    def Price(self,nbootstrap = 1000):
        """
        Compute the option price using simulations
        
        Parameters
        ----------
        None
        
        Returns
        -------
        type: float
            Option price at t = 0
        """
        tmpval = []
        for path in self.Underlying:
            tmpval.append(self._GetValue(path))
        #av = mean(tmpval)
        #st = (1.0/sqrt(self.Underlying.NPath))*numpy.std(tmpval)
        #Dirty bootstrap procedure. Fall far from the closed form solution for OTM put
        #But still better than without actually
        bootstrap = [mean(sku.resample(tmpval)) for i in range(nbootstrap)]
        av = mean(bootstrap)
        st = numpy.std(bootstrap)
        return [av - 1.96 * st, av ,av + 1.96 * st]


#Filled with some data ~ today
libor = 0.76944/100.0
S0 = 2267.89
r = 12.0 * math.log(1+libor/12.0)
sigma =0.06 #0.1177
K = 2250.0
t=1.0/12.0
nperiod = 1000

npath = 2000

pg = PathGenerator(npath,t,t/nperiod,'bs',r,sigma)
pg.GeneratePaths(S0)


plainvanillacall = Option(lambda x: max(x.GetLastItem() - K,0),pg)
plainvanillaput = Option(lambda x: max(K - x.GetLastItem(),0),pg)

print("Call price data: {}".format(plainvanillacall.Price()))
print("Put price data: {}".format(plainvanillaput.Price()))

N = lambda x: scipy.stats.norm.cdf(x)

d1 = (1.0/(sigma *math.sqrt(t))) * (math.log(S0/K)+(r+(sigma**2.0)/2.0)*t)
d2 = d1 - sigma * math.sqrt(t)
print("Closed form call: {}".format(S0 * N(d1) - K * math.exp(-r*t) * N(d2)))
print("Closed form put: {}".format(-S0 * N(-d1) + K * math.exp(-r*t) * N(-d2)))

from matplotlib.ticker import FuncFormatter

"""
plt.hist([p.GetLastItem() for p in pg.Paths],bins=10)

def to_percent(y,position):
    return str(100*y/npath) + '%'
    
formatter = FuncFormatter(to_percent)
plt.gca().yaxis.set_major_formatter(formatter)
"""

print(mean([p.GetLastItem() for p in pg.Paths]))
print(S0 * math.exp(r * plainvanillacall.Expiry))

pg.Paths[0].Plot()
#plt.gca().set_ylim([0,2500])
