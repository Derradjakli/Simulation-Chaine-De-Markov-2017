# -*- coding: utf-8 -*-
import numpy as np
import pyAgrum as gum
import pyAgrum.lib.ipython as gnb
import time

import utils as uti


class CollTempsMoyen:
  def __init__(self,s):
    self.s=s
    self.tps=0
    self.iter=0
    self.t1=0
  
  def initialize(self, cdm, max_iter):
    """
    :param max_iter: le nombre max d'itération de la simulation
    Fonction appelée en début de simulation
    """
    self.t1=time.clock()


  def receive(self, cdm, iter, state):
    """
    Fonction appelée à chaque itération d'une simulation
    :param cdm: la CdM simulée
    :param iter: l'indice de l'itération
    :param state: l'état dans l'itération courante
    :return: True si on doit arrêter la simulation
    """
    if state==self.s:
      t2=time.clock()
      self.tps+=t2-self.t1
      self.iter+=1
      self.t1=t2
    return False

  def finalize(self, cdm, iteration):
    """
    Fonction appelée à la fin de la simulation
    :param iteration: l'indice de la dernière itération
    """
    self.tps/=(1.0*self.iter)

  def get_results(self, cdm):
    """
    Fonction appelée après la simulation afin de collecter les résultats
    :return: None si pas de résultats, sinon un dictionnaire contenant une clé et comme valeur un type simple ou un
    dictionnaire.
    """

    return {"temps moyen":self.tps,"nombre d'apparition":self.iter}
