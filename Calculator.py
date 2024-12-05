import numpy as np
from itertools import permutations

class Calculator:
  def __init__(self,array_length_fractions):
    self.test = [[x] for x in array_length_fractions]  #fractions array for the input list
    self.memory = {"1":self.test}         #map for all fractions less than equal to one in the fraction array, to a dimension
    self.filtered_combs = {}                           #map for all fractions exactly one in a dimension
    self.coords = {}                                   #map for all coords in any dimensional sphere
    self.pos_neg_combs = {}                            #map for quadrant combinations in a dimension

  def descent(self,n,dimension=2):
    newArr = []
    for x in self.memory["1"]:
      other_ratios=self.memory[str(dimension-1)]
      for y in other_ratios:
        if sum(x)+sum(y)<=1:
          temp = [num for num in y]+x
          newArr.append(temp)
          continue
        else:
          continue
    self.memory[str(dimension)]=newArr
    if dimension==n:
      return
    self.descent(n,dimension+1)

  def getAllCombs(self,n):
    return self.memory[str(n)]

  def posNegCombs(self,dimension):
    if dimension in self.pos_neg_combs:
      return self.pos_neg_combs[dimension]
    combs = []
    final = dimension**2
    for x in range(0,dimension+1):
      arr = [-1 for x in range(x)] + [1 for x in range(dimension-x)]
      combs+=[perm for perm in permutations(arr)]
    seen = set()
    filtered_combs = []
    for comb in combs:
      if comb not in seen:
        seen.add(comb)
        filtered_combs.append(list(comb))
      else:
        continue
    self.pos_neg_combs[dimension] = filtered_combs
    return filtered_combs

  def Coords(self,n):
    if n in self.coords:
      return self.coords[n]
    try:
      self.memory[str(n)]
    except KeyError:
      self.descent(n)
      self.Coords(n)
    self.filtered_combs[str(n)] = [comb for comb in self.memory[str(n)] if sum(comb)==1]
    combs = self.filtered_combs[str(n)]
    allPerms = []
    index = 0
    for comb in combs:
      [allPerms.append(i) for i in permutations(comb) if i not in allPerms]
    seen = set()
    newArr = []
    for perm in allPerms:
      temp = perm
      if temp not in seen:
        seen.add(temp)
        newArr.append(list(perm))
      continue
    pos_neg_combs = self.posNegCombs(n)
    allPerms = np.array(newArr)
    coord_data = np.empty(shape=(0,n))
    seen = set()
    for perm in allPerms:
      for comb in pos_neg_combs:
        temp = []
        index = 0
        for n in perm:
          if comb[index]<0:
            temp.append(-(n**(1/2)))
          else:
            temp.append(n**(1/2))
          index+=1
        if tuple(temp) not in seen:
          seen.add(tuple(temp))
          coord_data = np.append(coord_data,[temp],0)
        else:
          continue
    self.coords[n] = coord_data
    return coord_data

