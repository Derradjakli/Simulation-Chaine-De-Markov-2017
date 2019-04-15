# -*- coding: utf-8 -*-
import numpy as np
import pyAgrum as gum
import pyAgrum.lib.ipython as gnb


import utils as uti

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
    uti.show_matrix(self.get_transition_matrix())

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
          d=self.distribution_to_vector(self.get_transition_distribution(self.get_states()[i]))
          for j in range(n):
              Res[i][j]=d[j] 
      return Res

  def get_transition_graph(self):
    G=self.get_transition_matrix()
    g=gum.DiGraph()
    n=len(G)
    L=[]
    for i in range(n):
        g.addNode()
        L.append(i) #contient tout les noeuds de 1 à n
    F=[]
    for i in range(n):
        S=[]
        for j in range(n):
            if G[i][j]!=0:
                g.addArc(i,j)
                S.append(j) #contient la liste de successeur de l'element i
        F.append(S) #va contenir en F[i] la liste des successeurs de i           
    return (g,L,F)

  def show_transition_graph(self,gnb):
      G=self.get_transition_matrix()
      s="""digraph {"""
      n=len(G)
      for i in range(n):
        s+=str(i+1)+""" [label=\""""+str(i+1)+"""\"];"""
      for i in range(n):
        for j in range(n):
          if G[i][j]!=0:
            s+=str(i+1)+"""->"""+str(j+1)+""" [label=\""""+str(G[i][j])+"""\"];"""
      s+="""}"""     
      gnb.showDot(s)
      return

  def strongly_connected_components(self,graph,L,F):#prend en entré le graph, la liste des noeud et la liste de successeur de chaque noeud

    """
    Tarjan's Algorithm (named for its discoverer, Robert Tarjan) is a graph theory algorithm
    for finding the strongly connected components of a graph.
    
    Based on: http://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
    """

    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    result = []
    
    def strongconnect(node):
        # set the depth index for this node to the smallest unused index
        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
    
        # Consider successors of `node`
        try:
            successors = F[node]
            
        except:
            successors = []

        for successor in successors:
            
            if successor not in lowlinks:
                # Successor has not yet been visited; recurse on it
                                
                strongconnect(successor)
                lowlinks[node] = min(lowlinks[node],lowlinks[successor])
            elif successor in stack:
                # the successor is in the stack and hence in the current strongly connected component (SCC)
                lowlinks[node] = min(lowlinks[node],index[successor])
        
        # If `node` is a root node, pop the stack and generate an SCC
        if lowlinks[node] == index[node]:
            connected_component = []
            
            while True:
                
                              
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            component = tuple(connected_component)
            # storing the result
            result.append(component)
            
    
    for node in L:
        if node not in lowlinks:
            strongconnect(node)
    
    return result 
  
  
  def get_communication_classes(self): #prend la matrice de transition en parametre
    (G,L,F)=self.get_transition_graph()
    L=self.strongly_connected_components(G,L,F)
    L=[[i for i in k] for k in L] #un bug fait qu'on a pour certaine classe le résultat sous la forme: (a,b,...,k,). cette ligne résout le problème.
    return L

  def get_absorbing_classes(self):#parcours la marice de transition et les compos_fort_connex pour voir s'il y a des arc sortant de chaque composante vers une autre
    res=self.get_communication_classes()
    G=self.get_transition_matrix()
    A=[]
    Absorbing_classes=[]
    for i in res:# Parcours la liste des composantes fortement connexe
        T=True 
        for j in i: #parcours une composante fortement connexe et je choisis un sommet 
            for t in res: #parcours les composante_fort_connex restantes
                if(t!=i):#i.e je suis dans une composante differente
                    for s in t:
                        if(G[j][s]!=0 and s!=t):#verifie s'il n'ya pas d'arc entre la composante actuel et les autres composantes
                            A.append(False)
                            T=False #je sors des 3 boucle car la composante est alors pas absorbante                           
                if(T==False):
                    break;#je ressors de la boucle
            if(T==False):
                break;
        A.append(T)
    for k in range(len(A)):
        if(A[k]==True): #recherche les composante fortement_connexe absorbante
            Absorbing_classes.append(res[k])
    
    return Absorbing_classes
  
  def is_irreductible(self): #L la matrice de transition
    L=self.get_communication_classes()
    if (len(L)==1) :#il n'ya qu'une seule classe d'equivalence pour le graphe (i.e ujne seule composante fortement connexe)
        return True
    return False 

  def is_ergodic(self): #on verifie si la chaine est irreductible et apériodique. Si c'est le cas, elle est ergodique puisqu'on a un nombre fini d'état, ce qui donne la recurence positive grâçe à l'apériodicité.
    if not self.is_irreductible():
      return False
    M=self.get_transition_matrix()
    n=len(M)
    Res=M
    tmp=[]
    L=[tmp]*n
    for i in range(n+1):
      for j in range(n):
        if Res[j][j]>0:
          L[j].append(i+1)
      Res=Res.dot(M)
    for k in L:
      if len(k)>1:
        p=uti.pgcd(k[0],k[1])
        i=0
        while(p>1 and i<len(k)):
          j=i+1
          while(p>1 and j<len(k)):
            p=uti.pgcd(p,uti.pgcd(k[i],k[j]))
            j+=1
          i+=1
        if p>1:
          return False              
    return True

    
