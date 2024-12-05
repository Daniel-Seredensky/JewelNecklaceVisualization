from random import *
import numpy as np
from Calculator import Calculator as Calc
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from PIL import Image
import os
from JewelNecklaceVisualizer import JewelNecklace




def isZeros(arr):
  for x in arr:
    if x!=0:
      return False
  return True

class Map:

  def __init__(self,jList):
    self.answers = []
    self.person1MemoryBank = []
    self.person2MemoryBank = []
    self.jList = jList
    self.fracArr = [(x+1)/(len(jList)) for x,y in enumerate(jList)]
    calc = Calc(self.fracArr)
    self.dimension = jList.dimension
    self.canPlot3D = False
    self.canPlot4D = False
    self.coord_data = calc.Coords(self.dimension)
    if self.dimension==3:
      self.x = self.coord_data[:,0]
      self.y = self.coord_data[:,1]
      self.z = self.coord_data[:,2]
      self.canPlot3D = True
    if self.dimension==4:
      self.canPlot4D = True

  def plot3D(self):
    if self.canPlot3D:
      fig = go.Figure(data=[go.Scatter3d(x=self.x, y=self.y, z=self.z, mode = "markers",)])
      fig.update_traces(marker=dict(color="maroon",opacity=.75))
      fig.update_scenes(xaxis_title_text='x',
                        yaxis_title_text='y',
                        zaxis_title_text='z')
      fig.show()
    else:
      print("Cannot plot 3D map")

  def plot4D(self,plotType = "animation", getCords = False):
    def update(data,time):
        new_data = np.array([coord for coord in data if abs(coord[len(coord)-1])==time])
        return new_data
    if plotType == "animation":
      newpath = "/Users/daniel/Desktop/Projects/PythonFolder/JewelNecklaceVisualization/images"
      if os.path.exists(newpath):
        os.system('rm -rf ' + newpath)  #remove directory if exists
      os.makedirs(newpath)  #make a new directory
      if self.canPlot4D:
        seen = set()
        totalTs = []
        for t in self.coord_data[:,3]:
          if abs(t) not in seen:
            totalTs.append(abs(t))
            seen.add(abs(t))
        index = 0
        totalTs.sort(reverse=True)
        for t in totalTs:
          data = update(self.coord_data,t)
          x,y,z = data[:,0],data[:,1],data[:,2]
          fig= plt.figure()
          ax0 = fig.add_subplot(projection = "3d")
          fig.set_size_inches(6,6)
          ts = [abs(t) for t in data[:,3]]
          scatter = ax0.scatter(x,y,z,c=ts,cmap="magma")
          cax = ax0.inset_axes([0, .5, 0.05, 0.35])
          fig.colorbar(scatter,cax=cax,label = "time",shrink = .35)
          scatter.set_clim(min(totalTs),max(totalTs))
          ax0.set_xlabel("x")
          ax0.set_ylabel("y")
          ax0.set_zlabel("z")
          ax0.set_xlim(-1,1)
          ax0.set_ylim(-1,1)
          ax0.set_zlim(-1,1)
          plt.savefig(newpath+f"/{index}.png")
          index+=1
          plt.savefig(newpath+f"/{index}.png")
          index+=1
          plt.close()

        images = [Image.open(newpath+f"/{n}.png") for n in range(index)]
        images[0].save(newpath+'/4DPlot.gif', save_all=True, append_images=images[1:], duration=100, loop=0)

    elif plotType == "still":
      seen = set()
      totalTs = []
      for t in self.coord_data[:,3]:
        if abs(t) not in seen:
          totalTs.append(abs(t))
          seen.add(abs(t))
      index = 0
      totalTs.sort()
      shift = 0
      newData = []
      mapNonAns = np.array([])
      mapAns = np.array([])
      for w in totalTs:
        data = update(self.coord_data,w)
        for x,y,z,t in data:
          newData.append([x+shift,y+shift,z+shift,t])
          norm = [n**2 if n>0 else -(n**2) for n in (x,y,z,t)]
          postFunc = self.function(norm)
          if isZeros(postFunc):
            mapAns = np.append(mapAns,[[x+shift,y+shift,z+shift,t],[0,0,0,0]])
          else:
            mapNonAns = np.append(mapNonAns,[[x+shift,y+shift,z+shift,t],postFunc+[0]])
        shift+=1
      newData = np.array(newData)
      if getCords:
        return mapNonAns,mapAns
      x,y,z = newData[:,0],newData[:,1],newData[:,2]
      fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode = "markers",)])
      fig.update_traces(marker=dict(color="maroon",opacity=.75))
      fig.show()
    else:
      print("Cannot plot 4D map")


  def function(self,coord):
    if min(coord)<=0 and max(coord)<=0:
      return [-x for x in self.jList.toLengths()[0]]
    if min(coord)>=0 and max(coord)>=0:
      return self.jList.toLengths()[0]

    norm = [x for x in coord]
    sum = 0
    person1 = []
    person1Memory = []
    person2 = []
    person2Memory = []
    for x in norm:
      if x<0:
        answers = self.jList.toLengths(strt = sum,end = sum+abs(x))
        person1.append(answers[0])
        person1Memory.append(answers[1])
        sum+=abs(x)
      else:
        answers = self.jList.toLengths(strt = sum,end = sum+abs(x))
        person2.append(answers[0])
        person2Memory.append(answers[1])
        sum+=abs(x)
    person1 = np.array(person1)
    person2 = np.array(person2)

    newCords = [np.sum(person1[:,index])-np.sum(person2[:,index]) for index in range(len(self.jList.types))]
    if isZeros(newCords):
      self.answers.append(coord)
      self.person1MemoryBank.append(person1Memory)
      self.person2MemoryBank.append(person2Memory)
    return newCords


  def collapse(self):
    collapse_data = []
    for coord in self.coord_data:
      norm = [x**2 if x>0 else -(x**2) for x in coord]
      temp = self.function(norm)
      collapse_data.append(temp)
    self.col_data = np.array(collapse_data)     #col_data = the collapsed data
    if self.canPlot4D:
      x,y,z = self.col_data[:,0],self.col_data[:,1],self.col_data[:,2]
      fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode = "markers",)])
      fig.update_traces(marker=dict(color="maroon",opacity=.75))
      fig.update_scenes(xaxis_title_text='x',
                        yaxis_title_text='y',
                        zaxis_title_text='z')
      fig.show()
    if self.canPlot3D:
      x,y,z = self.col_data[:,0],self.col_data[:,1],[0 for x in range(len(self.col_data[:,0]))]
      fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode = "markers",)])
      fig.update_traces(marker=dict(color="maroon",opacity=.75))
      fig.update_scenes(xaxis_title_text='x',
                        yaxis_title_text='y',
                        zaxis_title_text='z')
      fig.show()


  def create_frame(self, transition_t, nonAns, mapAns, w_min, w_max):
      fig = plt.figure()
      ax = fig.add_subplot(projection="3d")
      fig.set_size_inches(6, 6)
      
      if len(nonAns) > 0:
          current_positions = []
          current_t_values = []
          for start, end in nonAns:
              current_pos = start + transition_t * (end - start)
              current_positions.append(current_pos[:3])
              current_t = start[3] + transition_t * (end[3] - start[3])
              current_t_values.append(current_t)
          
          current_positions = np.array(current_positions)
          scatter = ax.scatter(current_positions[:, 0],
                            current_positions[:, 1],
                            current_positions[:, 2],
                            c=current_t_values,
                            cmap="viridis",
                            alpha=0.5)
          
          cax = ax.inset_axes([0, .5, 0.05, 0.35])
          fig.colorbar(scatter, cax=cax, label="w", shrink=.35)
          scatter.set_clim(w_min, w_max)
      
      if len(mapAns) > 0:
          ans = mapAns.reshape(-1, 2, 4)
          for start, end in ans:
              current_pos = start + transition_t * (end - start)
              ax.scatter(current_pos[0], current_pos[1], current_pos[2],
                        color='black', alpha=0.9)
      
      ax.set_xlabel("x")
      ax.set_ylabel("y")
      ax.set_zlabel("z")
      return fig

  def save_frame(self, fig, path, index):
      plt.savefig(f"{path}/{index}.png")
      plt.close()

  def animateCollapse4D(self):
      mapNonAns, mapAns = self.plot4D(plotType="still", getCords=True)
      
      newpath = "/Users/daniel/Desktop/Projects/PythonFolder/JewelNecklaceVisualization/collapse_images"
      if os.path.exists(newpath):
          os.system('rm -rf '+newpath)
      os.makedirs(newpath)
      
      frames = 30
      hold_frames = 20
      index = 0
      
      if len(mapNonAns) > 0:
          nonAns = mapNonAns.reshape(-1, 2, 4)
          w_min = np.min(nonAns[:, 0, 3])
          w_max = np.max(nonAns[:, 0, 3])
      
      # Initial hold frames
      for _ in range(hold_frames):
          fig = self.create_frame(0, nonAns, mapAns, w_min, w_max)
          self.save_frame(fig, newpath, index)
          index += 1
      
      # Animation frames
      for frame in range(frames + 1):
          fig = self.create_frame(frame/frames, nonAns, mapAns, w_min, w_max)
          self.save_frame(fig, newpath, index)
          index += 1
      
      # Final hold frames
      for _ in range(hold_frames):
          fig = self.create_frame(1, nonAns, mapAns, w_min, w_max)
          self.save_frame(fig, newpath, index)
          index += 1
      
      images = [Image.open(f"{newpath}/{n}.png") for n in range(index)]
      images[0].save(f'{newpath}/collapse4D.gif', save_all=True, append_images=images[1:], duration=100, loop=0)


JN = JewelNecklace(14,"red","green","blue")
map = Map(JN)
map.animateCollapse4D()
JN.toImage("necklace")
JN.toImageWithAnswer("necklaceAnswer",map.answers[0])
print(JN)
print(map.answers[0])

