# -*- coding: utf-8 -*-
import numpy as np
import pyAgrum as gum
import pyAgrum.lib.ipython as gnb
from CdM import CdM
import random
import utils as uti

class Oie(CdM):
    def __init__(self,n,p,q): # il existe des cas extremes où on ne peut pas empecher la création de boucle si on ne biaise pas nos probas
        self.nbr_cases=n
        super().__init__()
        self.p=p
        self.q=q
        bl=True
        while(bl):
            bl=False
            L=[]
            Tmp=[]
            Tmp2=[]
            for i in range(n):
                Tmp2.append(i)
                cpt=0.1*q
                tmp=random.random()
                if tmp<cpt:
                    L.append(('p',0))
                cpt+=0.1*p
                if tmp<cpt and len(L)==i:
                    try:
                        j=random.choice(Tmp2[:-1]+[k[0] for k in Tmp if k[1]!=i])     
                    except:
                        bl=True
                        break
                    L.append(('g',j))
                cpt+=0.1*p
                if tmp<cpt and len(L)==i:
                    try:
                        j=random.randint(i+1,n-1)
                    except:
                        bl=True
                        break
                    L.append(('t',j))
                    Tmp.append((i,j))
                    Tmp2.pop(len(Tmp2)-1)         
                if tmp>=cpt and len(L)==i:
                    L.append(('x',0))
        self.case=L
            
    def get_states(self):
        return range(self.nbr_cases)
        
    def get_transition_distribution(self,state):
        n=self.nbr_cases
        d=dict()
        tab=self.get_states()
        if state==n-1:
            for i in range(1,n):
                d[i]=0
            d[0]=1
            return d
        L=self.case
        for i in tab:
            if i<state+1 or i>state+6:
                d[i]=0
            else:
                d[i]=1/(6.0)
        if state>n-8:
            for j in range(1,state-n+8):
                d[n-j-1]+=1/(6.0)
        for i in tab:
            if d[i]>0:
                if L[i][0]=='g':
                    d[L[i][1]]=d[i]
                    d[i]=0
                if L[i][0]=='t':
                    d[L[i][1]]=d[i]
                    d[i]=0
        return d

    def get_initial_distribution(self):
        return self.get_transition_distribution(0)


        
        
