#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CdM import CdM
import pyAgrum.lib.ipython as gnb
import numpy as np
from CollGetDistribution import CollGetDistribution
from CdMSampler import CdMSampler
import time
import matplotlib.pyplot as plt


class CdMConvergence:
    def __init__(self,cdm):
        self.cdm=cdm

    def point_fixe(self):
        t1=time.clock()
        if not self.cdm.is_ergodic():
            print("chaine non ergodique")
            raise ValueError
        M=self.cdm.get_transition_matrix()
        L=np.linalg.eig(M.transpose())
        for i in range(len(L[0])):
            if abs(L[0][i]-1)<10e-5:
                break
        t2=time.clock()
        return (L[1][i],None,t2-t1)   
     
    def convergence_pi(self,eps):
        t1=time.clock()
        p_tmp=self.cdm.distribution_to_vector(self.cdm.get_initial_distribution())
        M=self.cdm.get_transition_matrix()
        p=p_tmp
        p_tmp=p.dot(M)
        cpt=0
        tab_it=[cpt]
        tab_err=[np.linalg.norm(p_tmp-p)]
        while np.linalg.norm(p_tmp-p)>eps:
            p=p_tmp
            p_tmp=p.dot(M)
            cpt+=1
            tab_it.append(cpt)
            tab_err.append(np.linalg.norm(p_tmp-p))
        t2=time.clock()
        #plt.plot(tab_it,tab_err)
        #plt.legend(["erreur selon le nombre d'itération: convergence pi"])
        #plt.show()
        return (p,cpt,t2-t1)
    
    def convergence_matrice(self,eps):
        t1=time.clock()
        M=self.cdm.get_transition_matrix()
        M_Res=M
        M_tmp=M.dot(M)
        cpt=0
        tab_it=[cpt]
        tab_err=[np.linalg.norm(M_Res-M_tmp)]
        while np.linalg.norm(M_Res-M_tmp)>eps:
            M_Res=M_tmp
            M_tmp=M_tmp.dot(M)
            cpt+=1
            tab_err.append(np.linalg.norm(M_Res-M_tmp))
            tab_it.append(cpt)
        p=self.cdm.distribution_to_vector(self.cdm.get_initial_distribution())
        t2=time.clock()
        #plt.plot(tab_it,tab_err)
        #plt.legend(["erreur selon le nombre d'itération: convergence matrice"])
        #plt.show()
        return (p.dot(M_Res),cpt,t2-t1)
    
    def simulation(self,eps,sampler,max_iter):
        t1=time.clock() 
        col=CollGetDistribution(eps,0)
        sampler.add_collector(col)
        d=sampler.run(max_iter)
        nbr_iter=d["nbr_iterations"]
        tab=sampler.cdm.distribution_to_vector(d)
        t2=time.clock()
        return (tab,nbr_iter,t2-t1)
        
A=[]
B=[]
C=[]
X=[]
from Oie import Oie 
for i in range(20,40):
    m=Oie(3*i,0.7,0.4)
    sampler=CdMSampler(m)
    c=CdMConvergence(m)
    X.append(3*i)
    A.append(c.convergence_pi(1e-10)[2])
    B.append(c.convergence_matrice(1e-10)[2])
    C.append(c.simulation(1e-10,sampler,100000)[2])
plt.plot(X,A)
plt.plot(X,B)
plt.plot(X,C)
plt.legend(["convergence matrice","convergence pi","convergence simulation"])
plt.show()


print(m.is_ergodic())
print(CD.point_fixe())
print(CD.simulation(1e-10,sampler,100000))
print(CD.convergence_pi(10e-10))
print(CD.convergence_matrice(10e-10))
