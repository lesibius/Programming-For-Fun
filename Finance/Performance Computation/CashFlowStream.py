# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 08:50:41 2017

@author: clem
"""

from scipy import optimize as opt

class CashFlowStream:
    """
    The CashFlowStream classes allows to store a stream of cash flow for a given period
    """
    def __init__(self,v0,v1,ndays):
        """
        Parameters
        ----------
        v0: float
            Initial value of the portfolio
        v1: float
            Ending value of the portfolio
        ndays: float
            Number of days in the period
            
        Warnings
        --------
        All input values MUST be float. If an int is provided, an error in the value may
        occur
        """
        self.CashFlows = {}
        self.InitialValue = v0
        self.EndingValue = v1
        self.NDays = ndays
        
    def AddCashFlow(self,date,cf):
        """
        Add an external cash flow to the strem
        
        Parameters
        ----------
        date: float
            Number of days (or subperiod) at which the external cash flow occurs
        cf: float
            Value of the cash flow
        """
        self.CashFlows[date]=cf
        
    def _LossFunction(self,r):
        """
        Loss function to compute the Modified IRR
        
        Parameters
        ----------
        r: float array
            Array of one element (due to the minimize method of scipy.optimize)
            
        Returns
        -------
        type: float
            Loss value for the Modified IRR optimization
        """
        return (sum([cf * ((1.0 + r[0]) ** ((self.NDays - d)/self.NDays)) for d, cf in self.CashFlows.iteritems()]) + self.InitialValue * (1.0 + r[0]) - self.EndingValue) ** 2.0
        
    def ModifiedDietz(self):
        """
        Compute the Modified Dietz return
        
        Parameters
        ----------
        None
        
        Returns
        -------
        type: float
            Return computed through the Modified Dietz method
        """
        weigthedCF = sum([cf * ((self.NDays - d)/self.NDays) for d, cf in self.CashFlows.iteritems()])
        return (self.EndingValue - self.InitialValue - sum(self.CashFlows.values()))/(self.InitialValue + weigthedCF)
    
    def ModifiedIRR(self):
        """
        Compute the Modified IRR by minimizing a loss function (initial guess: Modified Dietz
        return)
        
        Parameters
        ----------
        None
        
        Returns
        -------
        type: float
            Modified IRR
        """
        initval = self.ModifiedDietz()
        return opt.minimize(self._LossFunction,[initval],method = 'Powell').x       
        
        
cf = CashFlowStream(100000.0,110550.0,30.0)
cf.AddCashFlow(5.0,10000.0)
print("Modified IRR = {}".format(cf.ModifiedIRR()))
print("Modified Dietz = {}".format(cf.ModifiedDietz()))
