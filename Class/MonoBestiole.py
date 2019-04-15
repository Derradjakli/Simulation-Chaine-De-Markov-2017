import numpy as np
import matplotlib.pyplot as plt
from CdM import CdM
import pyAgrum.lib.ipython as gnb
import utils

class MonoBestiole(CdM):
    """classe definissant une mono-bestiole
    """

    def __init__(self,N,p,q):
        self.N=N
        self.p=p
        self.q=q
        super().__init__()

    def get_states(self):
        return range(1,self.N+1)

    def get_transition_distribution(self,state):
        N=self.N
        p=self.p
        q=self.q
        d=dict()
        if state==1:
            d[1]=1-p
            d[2]=p
            return d
        if state==N:
            d[N-1]=q
            d[N]=1-q
            return d
        d[state]=1-p-q
        d[state-1]=q
        d[state+1]=p
        return d

    def get_initial_distribution(self):
        d=dict()
        if self.N<3:
            d[1]=1-self.p
            d[2]=self.q
            return d
        d[int(self.N/2)+1]=1-self.p-self.q
        d[int(self.N/2)+2]=self.p
        d[int(self.N/2)]=self.q
        return d

m=MonoBestiole(2,0.5,0.5)
m.show_transition_graph(gnb)