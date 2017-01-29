# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:20:54 2017

@author: clem
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

#########################################################################################
#                          Abstract Animal Class (Prey and Predator Basis)
#########################################################################################

class Animal:
    """
    "Abstract" class to represent either a prey or a predator.
    
    Most of the Prey and Predator attributes and methods are defined at this level.
    """
    def __init__(self,x,y, pr_move = False):
        """
        Parameters
        ----------
        x : float
            X position of the animal
        y : float
            Y position of the animal
        """
        self.X = x
        self.Y = y
        self.Set_Movement(lambda x, y: {"dx": 0, "dy": 0})
        self.Record = pr_move
        self.Past_Move = np.array([[self.X,self.Y]])
        self.Set_Random_Generator(np.random.normal,np.random.normal)
        
    def Set_Movement(self,movement):
        """
        Set the movement of the Animal instance
        
        Parameters
        ----------
        movement: float -> float -> {"dx": float, "dy": float}
            Incremental movement function. The two arguments are provided by a
            random number generator (default = normal, see Set_Random_Generator)
            
        Returns
        -------
        None
        """
        self.Movement = movement
    
    def Set_Random_Generator(self,r1,r2):
        """
        Set the two random generators for the movement
        
        Parameters
        ----------
        r1: None -> float
            Random number generator (e.g. numpy.random.number)
        r2: None -> float
            Random number generator (e.g. numpy.random.number)
        """
        self.Rand1 = r1
        self.Rand2 = r2
    
    def Move(self):
        """
        Incremental movement + recording of the movement if required
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        dMov = self.Movement(self.Rand1(),self.Rand2())
        self.X = self.X + dMov["dx"]
        self.Y = self.Y + dMov["dy"]
        if self.Record:
            self.Past_Move = vstack((self.Past_Move,np.array([[self.X,self.Y]])))
    
    def Plot_Path(self):
        """
        Plot the movement of the animal.
        
        Parameters
        ----------
        None        
        
        Returns
        -------
        None
        """
        try:
            plt.plot(self.Past_Move[:,0],self.Past_Move[:,1])
        except:
            print("No record available")
    
    def __sub__(self,other):
        """
        Compute the distance between two Animal instances.
        Override the - operator
        
        Parameters
        ----------
        other: Animal
            Animal instance from which the distance should be computed
        
        Returns
        -------
        type: float
            Distance from other Animal to self
        """
        dist_x = (other.X - self.X) ** 2.0
        dist_y = (other.Y - self.Y) ** 2.0        
        return np.sqrt(dist_x + dist_y)

####################################################################################
#                               Predator Class (Implement Animal)
####################################################################################

class Predator(Animal):
    """
    Implementation of the "abstract" Animal class to instanciate a Predator.
    """
    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        Animal.__init__(self,0,0)
        
    def Catch_Prey(self,mp):
        """
        Ask the map in which the predator is whether the predator caught a prey
        or not.
        
        Parameters
        ----------
        mp: Map
            Map on which the predator move
            
        Returns
        -------
        type: bool
            True if the predator caught a prey
        """
        return mp.Catch_Prey(self)

####################################################################################
#                               Prey Class (Implement Animal)
####################################################################################

class Prey(Animal):
    """
    Implementation of the "abstract" class Animal to instanciate preys.
    """
    def __init__(self,x,y):
        """
        Parameters
        ----------
        x: float
            X axis original position
        y: float
            Y axis original position
        """
        Animal.__init__(self,x,y)

####################################################################################
#                               Map Class (Hold Preys and Predators)
####################################################################################

class Map:
    """
    Class to hold Predator and Prey instances
    """
    def __init__(self,n_preys,x_min,x_max,catch_distance = 15):
        """
        Instanciate a Predator and n_preys Prey instances. The Prey instances are
        placed randomly on the map, in a square which area is : (x_max-x_min)**2
        
        Parameters
        ----------
        n_preys: int
            Number of preys on the map
        x_min: float
            Min value (both X and Y axis) for the original position of preys 
        x_max: float
            Max value for the original position of preys
        catch_distance: float
            Minimal distance fom the prey for the predator to catch it
        """
        self.Predator = Predator()
        self.Preys = [Prey(np.random.uniform(x_min,x_max),np.random.uniform(x_min,x_max)) for i in range(n_preys)]
        self.Catch_Distance = catch_distance        
        
    def Set_Predator_Movement(self,movement):
        """
        Set the predator movement
        
        Parameters
        ----------
        movement: float -> float -> {"dx": float, "dy": float}
        
        Returns
        -------
        None
        """
        self.Predator.Set_Movement(movement)
    
    def Set_Predator_Generator(self,r1,r2):
        """
        Set the generator movement
        
        Parameters
        ----------
        r1: None -> float
            First random generator for the predator movement
        r2: None -> float
            Second random generator for the prey movement
            
        Returns
        -------
        None
        """
        self.Predator.Set_Random_Generator(r1,r2)
        
    def Set_Prey_Movement(self,movement):
        """
        Set the predator movement
        
        Parameters
        ----------
        movement: float -> float -> {"dx": float, "dy": float}
        
        Returns
        -------
        None
        """
        for p in self.Preys:
            p.Set_Movement(movement)
    
    def Set_Prey_Generator(self,r1,r2):
        """
        Set the generator movement
        
        Parameters
        ----------
        r1: None -> float
            First random generator for the predator movement
        r2: None -> float
            Second random generator for the prey movement
            
        Returns
        -------
        None
        """
        for p in self.Preys:
            p.Set_Random_Generator(r1,r2)
    
    def Catch_Prey(self,predator):
        """
        Check if the predator is able to catch a prey
        
        Parameters
        ----------
        predator: Predator
            Predator for which the test should be made
            
        Returns
        -------
        type: bool
            True if the predator is able to catch a prey
        """
        for p in self.Preys:
            if predator - p < self.Catch_Distance:
                return True
                
    def Set_Recorder(self,r_pred,r_prey):
        """
        Set the recorder for preys and the predator.
        
        Parameters
        ----------
        r_pred: bool
            True if the Predator instance movement should be recorded
        r_prey: bool
            True if Prey instances movement should be recorded
        """
        self.Predator.Record = r_pred
        for p in self.Preys:
            p.Record = r_prey
    
    def _One_Run(self):
        """
        One run of the map
        """
        self.Predator.Move()
        for p in self.Preys:
            p.Move()
            
    def Run(self,max_iter):
        """
        Run the map for a given number of iteration and returns a boolean if the
        predator caught a prey. The simulation stops when the predator catch the 
        prey.
        
        Parameters
        ----------
        max_iter: int
            Number of iteration before to stop the simulation
        
        Returns
        -------
        type: bool
            True if the predator caught a prey
        """
        for i in range(max_iter):
            self._One_Run()
            if self.Predator.Catch_Prey(self):
                print("Catching prey at iter {}".format(i))
                return True
        return False

###################################################################################
#                                   Main
###################################################################################

m = Map(100,-2000,2000,50)

mov = lambda x, y: {"dx": x * np.cos(y * 2.0 * np.pi), "dy": x * np.sin(y * 2.0 * np.pi)}
st.cauchy.a = 0
st.cauchy.b = 2
m.Set_Predator_Generator(st.cauchy.rvs,np.random.uniform)
m.Set_Predator_Movement(mov)
m.Set_Recorder(True,True)

movprey = lambda x, y: {"dx": x, "dy": y}
m.Set_Prey_Movement(movprey)

m.Run(2000)

m.Predator.Plot_Path()
for p in m.Preys:
    p.Plot_Path()
