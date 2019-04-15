# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 14:08:23 2018

@author: derradj
"""

import numpy as np
import pyAgrum as gum


def strongly_connected_components(graph,L,F):#prend en entré le graph, la liste des noeud et la liste de successeur de chaque noeud

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
  
def get_transition_graph(V): #prend la matrice de transition en parametre
    G=V
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
    return g,L,F

def get_communication_classes(L): #prend la matrice de transition en parametre
    G,L,F=get_transition_graph(L)
    L=strongly_connected_components(G,L,F)
    return L
def get_absorbing_classes(L):#parcours la marice de transition et les compos_fort_connex pour voir s'il y a des arc sortant de chaque composante vers une autre
    res=get_communication_classes(L)
    G=L    
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
V=[[0.5,0.5,0,0,0,0],[0.5,0,0,0.5,0,0],[0.25,0.25,0,0,0.25,0.25],[0,0,1,0,0,0,],[0,0,0,0,1,0],
 [0,0,0,0,0,1]]  #MouseinMaze
 
L=[[0.8,0.2,0],[0,0.8,0.2],[0.3,0,0.7]] #Feu rouge

graph,S,F=get_transition_graph(V)
print("composante fortement connexe\n",strongly_connected_components(graph,S,F))
print("classes absorbantes (sous chaine de markov)\n",get_absorbing_classes(V))
def is_irreductible(L):
      L=get_communication_classes(L)
      if (len(L)==1) :#il n'ya qu'une seule classe d'equivalence pour le graphe (i.e ujne seule composante fortement connexe)
          return True
      return False
      
print("irreductible\n",is_irreductible(V))
     
