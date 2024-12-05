from Map import Map
from JewelNecklaceVisualizer import JewelNecklace



#Initialize the randomized JewelNecklace object at a given size
#Initialized with three differnet gem colors for visualization 
JN = JewelNecklace(14,"red","green","blue")


#Create a map of the current JewelNecklace to its corresponding discretized hypersphere
map = Map(JN)

#Animation of the collapse function being applied to the JewelNecklace sphere
#The black dots represent the points that turn into the answers for the problem
map.animateCollapse4D()

#Get an image of the JewelNecklace
JN.toImage("necklace")
#Get an image of the JewelNecklace with the answer to the problem visualized
JN.toImageWithAnswer("necklaceAnswer",map.answers[0])

##print to the terminal jewel necklace as a string and the answer to the problem as an array 
print(JN)
print(map.answers[0])


