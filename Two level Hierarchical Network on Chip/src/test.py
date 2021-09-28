from TwoLayerNetwork import *

def readTopologyFiles(path):
    Topology = []
    with open(path, "r") as file:
        data = file.readlines()
        for line in data:
            Topology.append(line.split(', '))
        file.close()
    return Topology

L1 = readTopologyFiles("../inputs/L1Topology.txt")

L2 = readTopologyFiles("../inputs/L2Topology.txt")

layerNet = TwoLayerNetwork(L1, L2)
layerNet.Create2LayerNetwork(verbose=True)
