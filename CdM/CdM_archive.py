# -*- coding: utf-8 -*-
import numpy as np
import pyAgrum as gum
import pyAgrum.lib.ipython as gnb


import utils

class CdM:
  """
  Class virtuelle représentant une Chaîne de Markov
  """

  def __init__(self):
    """
    Constructeur. En particulier, initalise le dictionaire stateToIndex

    :warning: doit être appelé en fin de __init__ des classes filles
    avec ` super().__init__()`
    """
    d=dict()
    tab=self.get_states()
    n=len(tab)
    for i in range(n):
      d[tab[i]]=i
    self.stateToIndex=d
    
    pass

  def get_states(self):
    """
    :return: un ensemble d'états énumérable (list, n-uple, etc.)
    """
    raise NotImplementedError

  def get_transition_distribution(self, state):
    """
    :param state: état initial
    :return: un dictionnaire {etat:proba} représentant l'ensemble des états atteignables à partir de state et leurs
    probabilités
    """
    raise NotImplementedError

  def get_initial_distribution(self):
    """
    :return: un dictionnaire représentant la distribution à t=0 {etat:proba}
    """
    raise NotImplementedError

  def __len__(self):
    """
    permet d'utiliser len(CdM) pour avoir le nombre d'état d'un CdM

    :warning: peut être surchargée
    :return: le nombre d'état
    """
    return len(self.get_states())

  def show_transition_matrix(self):
    utils.show_matrix(self.get_transition_matrix())

  def distribution_to_vector(self,d):
    tab=self.get_states()
    L=[]
    for i in tab:
      if i not in d.keys(): #tous les états ne sont pas dans d: ceux pour lesquels la distribution donne 0 n'y sont pas représenté
        L.append(0)
      else:
        L.append(d[i])
    return np.array(L)

  def vector_to_distribution(self,L):
    tab=self.get_states()
    d=dict()
    n=len(tab)
    for i in range(n):
      d[tab[i]]=L[i]
    return d

  def show_distribution(self,d):
    print(self.distribution_to_vector(d))

  def get_transition_matrix(self):
      n=self.__len__()
      Res=np.array([[0.0]*n]*n)
      for i in range(n):
          d=self.get_transition_distribution(i+1)
          for j in d.keys():
              Res[i][j-1]=d[j] #attention ici on attribue à l'état i la case i-1
      return Res

  def get_transition_graph(self):
      G=self.get_transition_matrix()
      g=gum.DiGraph()
      n=len(G)
      for i in range(n):
          g.addNode()
          
      for i in range(n):
        for j in range(n):
          if G[i][j]!=0:
            g.addArc(i,j)
      return g

  def show_transition_graph(self,gnb):
      G=self.get_transition_matrix()
      s="""digraph {"""
      n=len(G)
      for i in range(n):
        s+=chr(i+1+ord('0'))+""" [label=\""""+chr(i+1+ord('0'))+"""\"];"""
      for i in range(n):
        for j in range(n):
          if G[i][j]!=0:
            s+=chr(i+1+ord('0'))+"""->"""+chr(j+1+ord('0'))+""" [label=\""""+str(G[i][j])+"""\"];"""
      s+="""}"""
      gnb.showDot(s)
      return
    
  def get_communication_classes(self):
    G=self.get_transition_matrix()
    n=len(G)
    L=[]
    for i in range(n):
      s=set()
      for j in range(n):
        if G[i][j]!=0:
          if G[j][i]!=0:
            s.add(j)
            s.add(i)
      L.append(s)
    return L

  def is_irreductible(self):
    L=self.get_communication_classes()
    for s in L:
      if not (s<=L[0] and s>=L[0]):
        return False
    return True

    """def get_absorbing_classes(self):
      L=self.get_communication_classes()"""


  
              








  

    
