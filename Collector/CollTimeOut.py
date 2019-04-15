# -*- coding: utf-8 -*-
import time

from Collector import Collector


class CollTimeOut(Collector):
  def __init__(self, max_duration):
    self.max_duration = max_duration
    self.start_time = 0
    self.duration = 0

  def initialize(self, cdm, max_iter):
    self.start_time = time.time()
    self.duration = 0

  def receive(self, cdm, iter, state):
    if iter % 100 == 0:
      self.duration = time.time() - self.start_time
      if self.duration > self.max_duration:
        print(" [Time Out]", end="", flush=True)
        return True
    return False

  def finalize(self, cdm, iteration):
    self.duration = time.time() - self.start_time
    print("Durée : {}s".format(self.duration))

  def get_results(self, cdm):
    return {"duration": self.duration}
  
from CdMSampler import CdMSampler
from MouseInMaze import MouseInMaze
m=MouseInMaze()
s=CdMSampler(m)
print("- Sampler sans collector")
print(s.run(10))
print("\n- Sampler avec CollProgresser (voir CollProgresser.py)")
from CollProgresser import CollProgresser
s.add_collector(CollProgresser(3,9))
print(s.run(67))
print("\n - Sampler avec CollProgresser et CollSinleStateCounter (voir CollSingleStateCounter.py)")
from CollSingleStateCounter import CollSingleStateCounter
s.add_collector(CollSingleStateCounter(m.get_states()[1]))
s.add_collector(CollSingleStateCounter(m.get_states()[4]))
print(s.run(150))
print("\n - Sampler avec CollProgresser, CollSinleStateCounter et ColTimeOut (voir CollTimeOut.py)")
from CollTimeOut import CollTimeOut
s.add_collector(CollTimeOut(1)) # time out de 1 seconde
print(s.run(150000000000))
