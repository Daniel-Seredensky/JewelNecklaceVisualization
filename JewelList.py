from random import *
import numpy as np
from Jewel import Jewel


class JewelList():
  def __init__(self,n,*args):
      if n%2!=0:
        n+=1
      self.mapMemory = {} #contains coords as keys and its corresponding length tuple as a item
      self.types=[]  #type of jewels in the list
      for arg in args:
        self.types.append(arg)
      self.dimension = len(args)+1 #dimension of sphere the list produces
      self.start = 0
      self.JL = []   #Generated jewelLst with given length and jewel
      for num in range(n):
        self.JL.append(Jewel(args[randint(0,len(args)-1)]))
      self.evenList()

  def evenList(self):
    mem = self.toLengths()[1]
    for key, item, in mem.items():
      if item%2==1:
        self.JL.append(Jewel(key))

  def __str__(self):
    s = ""
    for jewel in range(len(self.JL)):
      s+= str(self.JL[jewel]) + " " + str(jewel+1) + ", "
    return s

  def __len__(self):
    return len(self.JL)

  def __iter__(self):
    return self
  

  def __next__(self):
    try:
      x = self.JL[self.start]
    except:
      self.start=0
      raise StopIteration
    self.start+=1
    return x

  def toLengths(self,strt=0,end=1):
    mem={}
    if end ==0:
      return [0 for x in range (len(self.types))],mem
    strt = abs(strt)
    end = abs(end)

    totals = [0 for x in range(len(self.types))]
    for index in range(int(strt*self.__len__()),int(end*self.__len__())):
      cur = self.JL[index].__str__()
      if cur not in mem:
        mem[cur]=1
        totals[self.types.index(cur)]+=1
      else:
        mem[cur]=mem[cur]+1
        totals[self.types.index(cur)]+=1
    return totals,mem
  


