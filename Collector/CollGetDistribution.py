# -*- coding: utf-8 -*-


class CollGetDistribution:
  def __init__(self,eps,pas):
    self.eps=eps
    self.pas=pas
    self.iteration=0
    self.distribution=dict()
  def initialize(self, cdm, max_iter):
    """
    :param max_iter: le nombre max d'itération de la simulation
    Fonction appelée en début de simulation
    """
    self.iteration=0
    tab=cdm.get_states()
    d=cdm.get_initial_distribution()
    for t in tab:
      self.distribution[t]=0
    print("run({}): ".format(max_iter), end="", flush=True)

  def receive(self, cdm, iter, state):
    """
    Fonction appelée à chaque itération d'une simulation
    :param cdm: la CdM simulée
    :param iter: l'indice de l'itération
    :param state: l'état dans l'itération courante
    :return: True si on doit arrêter la simulation
    """
    tab=cdm.get_states()
    cpt=1.0
    max=0.0
    for t in tab:
      if t==state:
        cpt=abs(self.distribution[t]-(1+self.distribution[t]*(iter))/(1.0*(iter+1)))
        if cpt>max:
          max=cpt
        self.distribution[t]=(1+self.distribution[t]*(iter))/(1.0*(iter+1))
      else:
        cpt=abs(self.distribution[t]-(self.distribution[t])*((iter)/(1.0*(iter+1))))
        if cpt>max:
          max=cpt
        self.distribution[t]*=((iter)/(1.0*(iter+1)))
    try:
      if iter%self.pas==0:
        print(self.distribution)
    except:
      pass
    if max<self.eps:
      return True
    return False

  def finalize(self, cdm, iteration):
    """
    Fonction appelée à la fin de la simulation
    :param iteration: l'indice de la dernière itération
    """
    print(" <-- stop with {} iterations".format(iteration))


  def get_results(self, cdm):
    """
    Fonction appelée après la simulation afin de collecter les résultats
    :return: None si pas de résultats, sinon un dictionnaire contenant une clé et comme valeur un type simple ou un
    dictionnaire.
    """
    return self.distribution




