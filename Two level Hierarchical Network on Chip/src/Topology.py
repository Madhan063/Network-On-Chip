from Node import *
import math
import numpy as np

class Chain:

    def __init__(self, n, uns, nodes_count, nodes = None):
        self.name = "Chain"
        self.N = n  # Chain Dimension
        self.Uns = uns  # unique name string for naming the network nodes uniquely
        self.nodes = [Node(str(self.Uns) + '-' + str(i),nodes_count+i) for i in range(self.N)] if nodes == None else nodes     # Initializing Nodes
        self.headNode = self.N//2 if self.N > 2 else 0                  # Head node index in the nodes list

    # Function that returns dimensions of the Chain network
    def getDimensions(self):
        return self.N

    # Function that returns head node indices in the node array
    def getHeadNodeIndices(self):
        return self.headNode

    # Function to connect the initialized nodes to form a Chain network
    def ConnectNodes(self):
        ########### Single Node ###########
        if (self.N == 1):
            return
        ########### Chain ###########
        for i in range(self.N):
            # Inital Node
            if i == 0:
                self.nodes[i].links.append(self.nodes[i+1].Id)
            # Final Node
            elif i == self.N-1:
                self.nodes[i].links.append(self.nodes[i-1].Id)
            # Middle Nodes
            else:
                self.nodes[i].links.append(self.nodes[i+1].Id)
                #print(self.nodes[i+1].Id)
                self.nodes[i].links.append(self.nodes[i-1].Id)

    # Function to print the Chain network properties
    def printNetworkInfo(self,toFile = False):
        outputString = "Chain Dimensions: " + str(self.N) + "\n"
        outputString += "Head Node: " + str(self.headNode) + "\n"
        outputString += "Chain links:" + "\n"
        for i in range(self.N):
            outputString += self.nodes[i].Id + ": " + str(self.nodes[i].links) + "\n"
        if toFile:
            return outputString
        else:
            print(outputString)


class Ring:

    def __init__(self, n, uns, nodes_count, nodes = None):
        self.name = 'Ring'
        self.N = n  # Ring Dimension
        self.Uns = uns  # unique name string for naming the network nodes uniquely
        self.nodes = [Node(str(self.Uns)+"-"+str(i),nodes_count+i) for i in range(self.N)] if nodes == None else nodes     # Initializing Nodes
        self.headNode = 0                                               # Head node can be any node default value as 0

    # Function that returns dimensions of the Ring network
    def getDimensions(self):
        return self.N

    # Function that returns head node indices in the node array
    def getHeadNodeIndices(self):
        return self.headNode

    # Function to connect the initialized nodes to form a ring network
    def ConnectNodes(self):
        ########### Single Node ###########
        if (self.N == 1):
            return
        ########### Chain ###########
        elif (self.N == 2):
            self.nodes[0].links.append(self.nodes[1].Id)
            self.nodes[1].links.append(self.nodes[0].Id)
            return
        ########### Ring ###########
        for i in range(self.N):
            if i == 0:
                self.nodes[i].links.append(self.nodes[i+1].Id)
                self.nodes[i].links.append(self.nodes[self.N-1].Id)
            elif i == self.N-1:
                self.nodes[i].links.append(self.nodes[i-1].Id)
                self.nodes[i].links.append(self.nodes[0].Id)
            else:
                self.nodes[i].links.append(self.nodes[i+1].Id)
                self.nodes[i].links.append(self.nodes[i-1].Id)

    # Function to print the ring network properties
    def printNetworkInfo(self,toFile = False):
        outputString = "Ring Dimensions: " + str(self.N) + "\n"
        outputString += "Head Node: " + str(self.headNode) + "\n"
        outputString += "Ring links:" + "\n"
        for i in range(self.N):
            outputString += self.nodes[i].Id + ": " + str(self.nodes[i].links) + "\n"
        if toFile:
            return outputString
        else:
            print(outputString)

class Mesh:

    def __init__(self, x, y, uns, nodes_count, nodes = None):
        self.name = "Mesh"
        self.X, self.Y = x, y   # Mesh Dimensions
        self.Uns = uns  # unique name string for naming the network nodes uniquely
        self.nodes = [[Node(str(self.Uns)+"-"+str(j)+"-"+str(i),nodes_count+self.X*j+i) for i in range(self.X)] for j in range(self.Y)]  if nodes == None else nodes     # Initializing Nodes
        self.headNodeX = self.X//2 if self.X >= 3 else 0                                                # Head node X index
        self.headNodeY = self.Y//2 if self.Y >= 3 else 0                                                # Head node Y index

    # Function that returns dimensions of the mesh network
    def getDimensions(self):
        return self.X, self.Y

    # Function that returns head node indices in the node array
    def getHeadNodeIndices(self):
        return self.headNodeX, self.headNodeY

    # Function to connect the initalized nodes to form a mesh network
    def ConnectNodes(self):
        ########### Single Node ###########
        if (self.X == 1 and self.Y == 1):
            return
        ########### Chain along Y ###########
        elif (self.X == 1):
            for j in range(self.Y):
                # Top node
                if(j == 0):
                    self.nodes[j][0].links.append(self.nodes[j+1][0].Id)
                # Bottom node
                elif(j == self.Y-1):
                    self.nodes[j][0].links.append(self.nodes[j-1][0].Id)
                # Inbetween nodes
                else:
                    self.nodes[j][0].links.append(self.nodes[j-1][0].Id)
                    self.nodes[j][0].links.append(self.nodes[j+1][0].Id)
            return
        ########### Chain along X ###########
        elif (self.Y == 1):
            for i in range(self.X):
                # Leftmost node
                if(i == 0):
                    self.nodes[0][i].links.append(self.nodes[0][i+1].Id)
                # Rightmost node
                elif(i == self.X-1):
                    self.nodes[0][i].links.append(self.nodes[0][i-1].Id)
                # Inbetween nodes
                else:
                    self.nodes[0][i].links.append(self.nodes[0][i+1].Id)
                    self.nodes[0][i].links.append(self.nodes[0][i-1].Id)
            return
        ########### 2D Mesh ###########
        for j in range(self.Y):
            for i in range(self.X):
                ########### Mesh Corners ###########
                if(i == 0 and j == 0):                                      # Top leftmost node
                    self.nodes[j][i].links.append(self.nodes[j+1][i].Id)
                    self.nodes[j][i].links.append(self.nodes[j][i+1].Id)
                elif(i == 0 and j == self.Y - 1):                           # Bottom leftmost node
                    self.nodes[j][i].links.append(self.nodes[j][i+1].Id)
                    self.nodes[j][i].links.append(self.nodes[j-1][i].Id)
                elif(i == self.X-1 and j == 0):                             # Top rightmost node
                    self.nodes[j][i].links.append(self.nodes[j][i-1].Id)
                    self.nodes[j][i].links.append(self.nodes[j+1][i].Id)
                elif(i == self.X-1 and j == self.Y-1):                      # Bottom rightmost node
                    self.nodes[j][i].links.append(self.nodes[j][i-1].Id)
                    self.nodes[j][i].links.append(self.nodes[j-1][i].Id)
                ########### Mesh Edges ###########
                elif(i == 0 and (j > 0 and j < self.Y-1)):                  # Nodes on the leftmost edge
                    self.nodes[j][i].links.append(self.nodes[j+1][i].Id)
                    self.nodes[j][i].links.append(self.nodes[j-1][i].Id)
                    self.nodes[j][i].links.append(self.nodes[j][i+1].Id)
                elif(i == self.X-1 and (j > 0 and j < self.Y-1)):           # Nodes on the rightmost edge
                    self.nodes[j][i].links.append(self.nodes[j+1][i].Id)
                    self.nodes[j][i].links.append(self.nodes[j-1][i].Id)
                    self.nodes[j][i].links.append(self.nodes[j][i-1].Id)
                elif((i > 0 and i < self.X-1) and j == 0):                  # Nodes on the topmost edge
                    self.nodes[j][i].links.append(self.nodes[j][i+1].Id)
                    self.nodes[j][i].links.append(self.nodes[j][i-1].Id)
                    self.nodes[j][i].links.append(self.nodes[j+1][i].Id)
                elif((i > 0 and i < self.X-1) and j == self.Y-1):           # Nodes on the bottom-most edge
                    self.nodes[j][i].links.append(self.nodes[j][i+1].Id)
                    self.nodes[j][i].links.append(self.nodes[j][i-1].Id)
                    self.nodes[j][i].links.append(self.nodes[j-1][i].Id)
                ########### Inside the Mesh ###########
                else:
                    self.nodes[j][i].links.append(self.nodes[j][i+1].Id)
                    self.nodes[j][i].links.append(self.nodes[j][i-1].Id)
                    self.nodes[j][i].links.append(self.nodes[j+1][i].Id)
                    self.nodes[j][i].links.append(self.nodes[j-1][i].Id)

    # Function to print the mesh network properties
    def printNetworkInfo(self,toFile = False):
        outputString = "Mesh Dimensions: X = " + str(self.X) + " Y = " + str(self.Y) + "\n"
        outputString += "Head Node: X: "+ str(self.headNodeX) +" Y: " + str(self.headNodeY) + "\n"
        outputString += "Mesh links:" + "\n"
        for j in range(self.Y):
            for i in range(self.X):
                outputString += self.nodes[j][i].Id + ": " + str(self.nodes[j][i].links) + "\n"
        if toFile:
            return outputString
        else:
            print(outputString)

class FoldedTorus:

    def __init__(self, x, y, uns, nodes_count,nodes = None):
        self.name = "Folded-Torus"
        self.X, self.Y = x, y       # Folded Torus Dimensions
        self.Uns = uns  # unique name string for naming the network nodes uniquely
        self.nodes = [[Node(str(self.Uns)+"-"+str(i)+"-"+str(j),nodes_count+(self.X)*j+i) for i in range(self.X)] for j in range(self.Y)] if nodes == None else nodes      # Initializing Nodes
        print(len(self.nodes[0]))
        self.headNodeX = self.X//2 if self.X >= 3 else 0                # Head node X index
        self.headNodeY = self.Y//2 if self.Y >= 3 else 0                # Head node Y index

    # Function that returns dimensions of the Folded-Torus network
    def getDimensions(self):
        return self.X, self.Y

    # Function that returns head node indices in the node array
    def getHeadNodeIndices(self):
        return self.headNodeX, self.headNodeY

    # Function to connect the initalized nodes to form a Folded-Torus network
    def ConnectNodes(self):
        ########### Single Node ###########
        if (self.X == 1 and self.Y == 1):
            return
        ########### Two Nodes ###########
        elif ({self.X,self.Y} == {1,2}):
            if self.X == 1:
                self.nodes[0][0].links = [self.nodes[0][1].Id]
                self.nodes[0][1].links = [self.nodes[0][0].Id]
            else:
                self.nodes[0][0].links = [(self.nodes[1][0].Id)]
                self.nodes[1][0].links  = [(self.nodes[0][0].Id)]
        elif ({self.X,self.Y} == {1,3}):
            if self.X == 1:
                self.nodes[0][0].links = [(self.nodes[1][0].Id,self.nodes[2][0].Id)]
                self.nodes[1][0].links = [(self.nodes[2][0].Id,self.nodes[0][0].Id)]
                self.nodes[2][0].links = [(self.nodes[1][0].Id,self.nodes[0][0].Id)]
            else:
                self.nodes[0][0].links = [(self.nodes[0][2].Id,self.nodes[0][1].Id)]
                self.nodes[0][1].links = [(self.nodes[0][0].Id,self.nodes[0][2].Id)]
                self.nodes[0][2].links = [(self.nodes[0][0].Id,self.nodes[0][1].Id)]
        elif (self.X == 2 and self.Y == 2):
            self.nodes[0][0].links = [(self.nodes[1][0].Id,self.nodes[0][1].Id)]
            self.nodes[0][1].links = [(self.nodes[1][1].Id,self.nodes[0][0].Id)]
            self.nodes[1][0].links = [(self.nodes[1][1].Id,self.nodes[0][0].Id)]
            self.nodes[1][1].links = [(self.nodes[1][0].Id,self.nodes[0][1].Id)]
        elif ({self.X,self.Y} == {2,3}):
            if self.X == 2:
                self.nodes[0][0].links = [(self.nodes[0][1].Id,self.nodes[1][0].Id,self.nodes[2][0].Id)]
                self.nodes[0][1].links = [(self.nodes[0][0].Id,self.nodes[1][1].Id,self.nodes[2][1].Id)]
                self.nodes[1][0].links = [(self.nodes[0][0].Id,self.nodes[1][1].Id)]
                self.nodes[1][1].links = [(self.nodes[0][1].Id,self.nodes[1][0].Id)]
                self.nodes[2][0].links = [(self.nodes[0][0].Id,self.nodes[2][1].Id)]
                self.nodes[2][1].links = [(self.nodes[0][1].Id,self.nodes[2][0].Id)]
            else:
                self.nodes[0][0].links = [(self.nodes[1][0].Id,self.nodes[0][1].Id,self.nodes[0][2].Id)]
                self.nodes[1][0].links = [(self.nodes[0][0].Id,self.nodes[1][1].Id,self.nodes[1][2].Id)]
                self.nodes[0][1].links = [(self.nodes[0][0].Id,self.nodes[1][1].Id)]
                self.nodes[1][1].links = [(self.nodes[1][0].Id,self.nodes[0][1].Id)]
                self.nodes[0][2].links = [(self.nodes[0][0].Id,self.nodes[1][2].Id)]
                self.nodes[1][2].links = [(self.nodes[1][2].Id,self.nodes[0][2].Id)]
        elif (self.X == 3 and self.Y == 3):
            self.nodes[0][0].links = [(self.nodes[1][0].Id,self.nodes[0][1].Id,self.nodes[0][2].Id,self.nodes[2][0].Id)]
            self.nodes[0][1].links = [(self.nodes[1][1].Id,self.nodes[0][0].Id,self.nodes[2][1].Id)]
            self.nodes[0][2].links = [(self.nodes[2][2].Id,self.nodes[0][0].Id,self.nodes[1][2].Id)]
            self.nodes[1][0].links = [(self.nodes[1][1].Id,self.nodes[0][0].Id,self.nodes[1][2].Id)]
            self.nodes[1][1].links = [(self.nodes[1][0].Id,self.nodes[0][1].Id)]
            self.nodes[1][2].links = [(self.nodes[1][0].Id,self.nodes[0][2].Id)]
            self.nodes[2][0].links = [(self.nodes[2][1].Id,self.nodes[2][2].Id,self.nodes[0][0].Id)]
            self.nodes[2][1].links = [(self.nodes[2][0].Id,self.nodes[0][1].Id)]
            self.nodes[2][1].links = [(self.nodes[2][0].Id,self.nodes[0][2].Id)]
        else:
            ########### Folded Torus ###########
            for j in range(self.Y):
                for i in range(self.X):
                    ########### Corners ###########
                    if(i == 0 and j == 0):                  # Top leftmost node
                        self.nodes[j][i].links.append(self.nodes[j][i+1].Id)
                        self.nodes[j][i].links.append(self.nodes[j][i+2].Id)
                        self.nodes[j][i].links.append(self.nodes[j+1][i].Id)
                        self.nodes[j][i].links.append(self.nodes[j+2][i].Id)
                    elif(i == 0 and j == self.Y - 1):       # Bottom leftmost node
                        self.nodes[j][i].links.append(self.nodes[j][i+1].Id)
                        self.nodes[j][i].links.append(self.nodes[j][i+2].Id)
                        self.nodes[j][i].links.append(self.nodes[j-1][i].Id)
                        self.nodes[j][i].links.append(self.nodes[j-2][i].Id)
                    elif(i == self.X-1 and j == 0):         # Top rightmost node
                        self.nodes[j][i].links.append(self.nodes[j][i-1].Id)
                        self.nodes[j][i].links.append(self.nodes[j][i-2].Id)
                        self.nodes[j][i].links.append(self.nodes[j+1][i].Id)
                        self.nodes[j][i].links.append(self.nodes[j+2][i].Id)
                    elif(i == self.X-1 and j == self.Y-1):  # Bottom rightmost node
                        self.nodes[j][i].links.append(self.nodes[j][i-1].Id)
                        self.nodes[j][i].links.append(self.nodes[j][i-2].Id)
                        self.nodes[j][i].links.append(self.nodes[j-1][i].Id)
                        self.nodes[j][i].links.append(self.nodes[j-2][i].Id)
                    ########### Edges and Penultimate Edges ###########
                    elif((i in [0, 1, self.X-2, self.X-1]) and (j > 0 and j < self.Y-1)):
                        # Along X direction
                        if i == 0:                          # Node on the leftmost edge
                            self.nodes[j][i].links.append(self.nodes[j][i+1].Id)
                            self.nodes[j][i].links.append(self.nodes[j][i+2].Id)
                        elif i == 1:                        # Node on the penultimate leftmost edge
                            self.nodes[j][i].links.append(self.nodes[j][i-1].Id)
                            self.nodes[j][i].links.append(self.nodes[j][i+2].Id)
                        elif i == self.X-2:                 # Node on the penultimate rightmost edge
                            self.nodes[j][i].links.append(self.nodes[j][i+1].Id)
                            self.nodes[j][i].links.append(self.nodes[j][i-2].Id)
                        elif i == self.X-1:                 # Node on the rightmost edge
                            self.nodes[j][i].links.append(self.nodes[j][i-1].Id)
                            self.nodes[j][i].links.append(self.nodes[j][i-2].Id)
                        # Along Y direction
                        if (j == 1):
                            self.nodes[j][i].links.append(self.nodes[j-1][i].Id)
                            self.nodes[j][i].links.append(self.nodes[j+2][i].Id)
                        elif (j == self.Y-2):
                            self.nodes[j][i].links.append(self.nodes[j+1][i].Id)
                            self.nodes[j][i].links.append(self.nodes[j-2][i].Id)
                        else:
                            self.nodes[j][i].links.append(self.nodes[j-2][i].Id)
                            self.nodes[j][i].links.append(self.nodes[j+2][i].Id)

                    elif((i > 0 and i < self.X-1) and (j in [0, 1, self.Y-2, self.Y-1])):
                        # Along Y direction
                        if (j == 0):                        # Node on the topmost edge
                            self.nodes[j][i].links.append(self.nodes[j+1][i].Id)
                            self.nodes[j][i].links.append(self.nodes[j+2][i].Id)
                        elif j == 1:                        # Node on the penultimate topmost edge
                            self.nodes[j][i].links.append(self.nodes[j-1][i].Id)
                            self.nodes[j][i].links.append(self.nodes[j+2][i].Id)
                        elif j == self.Y-2:                 # Node on the penultimate bottom-most edge
                            self.nodes[j][i].links.append(self.nodes[j+1][i].Id)
                            self.nodes[j][i].links.append(self.nodes[j-2][i].Id)
                        elif (j == self.Y-1):               # Node on the bottom-most edge
                            self.nodes[j][i].links.append(self.nodes[j-1][i].Id)
                            self.nodes[j][i].links.append(self.nodes[j-2][i].Id)
                        # Along X direction
                        if (i == 1):
                            self.nodes[j][i].links.append(self.nodes[j][i-1].Id)
                            self.nodes[j][i].links.append(self.nodes[j][i+2].Id)
                        elif (i == self.X-2):
                            self.nodes[j][i].links.append(self.nodes[j][i+1].Id)
                            self.nodes[j][i].links.append(self.nodes[j][i-2].Id)
                        else:
                            self.nodes[j][i].links.append(self.nodes[j][i-2].Id)
                            self.nodes[j][i].links.append(self.nodes[j][i+2].Id)
                    ########### Inside the Torus ###########
                    else:
                        self.nodes[j][i].links.append(self.nodes[j][i+2].Id)
                        self.nodes[j][i].links.append(self.nodes[j][i-2].Id)
                        self.nodes[j][i].links.append(self.nodes[j+2][i].Id)
                        self.nodes[j][i].links.append(self.nodes[j-2][i].Id)
            return
    # Function to print the Folded-Torus network properties
    def printNetworkInfo(self,toFile = False):
        outputString = "Folded-Torus Dimensions: X = " + str(self.X) + " Y = " + str(self.Y) + "\n"
        outputString += "Head Node: X: "+ str(self.headNodeX) +" Y: " + str(self.headNodeY) + "\n"
        outputString += "links:" + "\n"
        for j in range(self.Y):
            for i in range(self.X):
                outputString += self.nodes[j][i].Id + ": " + str(self.nodes[j][i].links) + "\n"
        if toFile:
            return outputString
        else:
            print(outputString)

class Butterfly:

    def __init__(self,n, uns, nodes_count,nodes = None):
        assert n != 0 and (n & (n-1) == 0)
        self.name = "ButterFly"
        self.N = n
        self.stages = int(math.log2(self.N))
        self.Uns = uns  # unique name string for naming the network nodes uniquely
        self.nodes = [[Node(str(self.Uns)+"-"+str(j)+"-"+str(i),nodes_count+(self.stages)*j+i) for i in range(self.stages)] for j in range(self.N)] if nodes == None else nodes       # Initializing Nodes
        self.headNodeX = self.stages - 1                                                                                # Head node X index
        self.headNodeY = self.N//2 if self.N >= 3 else 0                                                                # Head node Y index

    # Function that returns dimensions of the Butterfly network
    def getDimensions(self):
        return self.N, self.stages

    # Function that returns head node indices in the node array
    def getHeadNodeIndices(self):
        return self.headNodeX, self.headNodeY

    def ConnectNodes(self):
        for i in range(self.stages-1):
            for j in range(self.N):
                flipping_bit_position = self.stages - 2 - i
                bit_value = (j & (1 << flipping_bit_position)) >> flipping_bit_position
                target_index = j - 2**flipping_bit_position if bit_value else j + 2**flipping_bit_position
                ConnectNodes(self.nodes[j][i], self.nodes[target_index][i+1])
                ConnectNodes(self.nodes[j][i], self.nodes[j][i+1])
        return
    # Function to print the Butterfly network properties
    def printNetworkInfo(self,toFile = False):
        outputString = "ButterFly Dimensions: Inputs = " + str(self.N) +" Stages = " + str(self.stages) + "\n"
        outputString += "Head Node: X: " + str(self.headNodeX) + " Y: " + str(self.headNodeY) + "\n"
        outputString += "links:" + "\n"
        for i in range(self.stages):
            for j in range(self.N):
                outputString += self.nodes[j][i].Id + ": " + str(self.nodes[j][i].links) + "\n"
        if toFile:
            return outputString
        else:
            print(outputString)

class Hypercube:

    def __init__(self, n, uns, nodes_count,nodes = None):
        self.name = 'Hypercube'
        self.N = n                     # Hypercube of 'n' nodes
        self.Uns = uns  # unique name string for naming the network nodes uniquely
        self.Dimension = int(math.log2(self.N))
        self.headNode = 0
        self.nodes = [Node(str(self.Uns)+"-"+format(i,'#0'+str(self.Dimension+2)+'b')[2::],nodes_count+i) for i in range(self.N)] if nodes == None else nodes     # Initializing Nodes

    # Function that returns dimensions of the Hypercube network
    def getDimensions(self):
        return self.N, self.Dimensions

    # Function that returns head node indices in the node array
    def getHeadNodeIndices(self):
        return self.headNode

    # Function to connect the initialized nodes to form a ring network
    def ConnectNodes(self):
        ########### Single Node ###########
        if(self.Dimension == 0):
            return
        ########### Hypercube #############
        else:
            for i in range(self.N):
                for j in range(self.Dimension):
                    self.nodes[i].links.append(self.nodes[int(i ^ pow(2,j))].Id)
            return
    # Function to print the Hypercube network properties
    def printNetworkInfo(self,toFile = False):
        outputString = "Hypercube Dimensions: " + str(self.N) + "\n"
        outputString += "Head Node: " + str(self.headNode) + "\n"
        outputString += "Hypercube links:" + "\n"
        for i in range(self.N):
            outputString += self.nodes[i].Id + ": " + str(self.nodes[i].links) + "\n"
        if toFile:
            return outputString
        else:
            print(outputString)


### TODO ###
# Folded-TORUS for dims - (1,1), (1,2), (2,1), (2,2), (3,2), (2,3), (3,3)

### Functions Verification ###
# Dims = [ (1,1), (1,2), (2,1), (2,2), (3,2), (2,3), (3,3), (4,3), (3,4), (4,4) ]
# for dim in Dims:
#     print("\n#################################################")
#     mesh = Mesh(dim[0], dim[1])
#     mesh.ConnectMeshNodes()
#     mesh.printMesh()
#     print("#################################################\n")

# for i in range(1,10):
#     rin = Ring(i)
#     print("\n#################################################")
#     rin.ConnectRingNodes()
#     rin.printRing()
#     print("#################################################\n")

# for i in range(1,10):
#     lin = Chain(i, "a")
#     print("\n#################################################")
#     lin.ConnectNodes()
#     lin.printNetworkInfo()
#     print("#################################################\n")

# Dims = [(4,4)]

# for dim in Dims:
#     print("\n#################################################")
#     ft = FoldedTorus(dim[0], dim[1])
#     ft.ConnectFTNodes()
#     ft.printFT()
#     print("#################################################\n")

# for n in [4, 8, 16]:
#     print("\n#################################################")
#     bt = Butterfly(n)
#     bt.ConnectButterFlyNodes()
#     bt.printButterFly()
#     print("#################################################\n")
