from typing import NewType
from Node import *
from Topology import *

class TwoLayerNetwork:

    def __init__(self, l1Topology, l2Topology):
        self.L1Topo = l1Topology        # L1 Topology Info
        self.L2Topo = l2Topology        # L2 Topology Info
        # Network Names Dictionary
        self.networkNames = {'C': "Chain", 'R' : "Ring", 'M' : "Mesh", 'F' : "Folded-Torus", 'H' : "Hypercube", 'B' : "Butterfly"}
        # Count Dictionary to uniquely name different networks of same topology
        self.counts = {'C': 0, 'R' : 0, 'M' : 0, 'F' : 0, 'H' : 0, 'B' : 0}

    def createNetwork(self,netInfo, nodes_count, count_nodes = True, nodes = None):
        # netInfo - ['L', '4', '1'] (example format)
        if netInfo[0] in ['C','R','H']:
            if netInfo[0] == 'C':       # Chain Network
                net = Chain(int(netInfo[1]),'C'+str(self.counts['C']), nodes_count, nodes)
            elif netInfo[0] == 'R':     # Ring Network
                net = Ring(int(netInfo[1]), 'R'+str(self.counts['R']), nodes_count, nodes)
            else:     # Hypercube Network
                net = Hypercube(int(netInfo[1]), 'H'+str(self.counts['H']), nodes_count, nodes)
            nodes_count = nodes_count + int(netInfo[1]) if count_nodes else nodes_count
        elif netInfo[0] in ['M','F']:
            if netInfo[0] == "M":     # Mesh Network
                net = Mesh(int(netInfo[1]),int(netInfo[2]), 'M'+str(self.counts['M']), nodes_count, nodes)
            else:     # Folded-Torus Network
                net = FoldedTorus(int(netInfo[1]),int(netInfo[2]), 'F'+str(self.counts['F']), nodes_count, nodes)
            nodes_count = nodes_count + int(netInfo[1])*int(netInfo[2]) if count_nodes else nodes_count
        elif netInfo[0] == 'B':
            net = Butterfly(int(netInfo[1]), 'B'+str(self.counts['B']), nodes_count, nodes)
            nodes_count = nodes_count + int(netInfo[1]) if count_nodes else nodes_count
        else:                       # Un-Identified Network
            return "Unidentified Input. Please Input one of the topologies ['C', 'R', 'M', 'F', 'H', 'B']"
        self.counts[netInfo[0]] += 1
        net.ConnectNodes()
        return net, nodes_count
    # Function to initalize all the L2 networks
    def initalizeL2Networks(self):
        self.L2Nets = []
        nodes_count = 0
        for network in self.L2Topo:
            print(nodes_count)
            net, nodes_count = self.createNetwork(network, nodes_count, True, None)
            self.L2Nets.append(net)
    # Function to connect the head nodes of the initalized l2 network in the mentioned L1 network topology
    def BuildL1Topology(self):
        self.L1HeadNodes = []
        for i, network in zip(range(len(self.L2Topo)),self.L2Topo):
            if network[0] in ['C','R','H']:
                net = self.L2Nets[i]
                self.L1HeadNodes.append(net.nodes[net.getHeadNodeIndices()])
            elif network[0] in ['M', 'F', 'B']:
                net = self.L2Nets[i]
                x,y = net.getHeadNodeIndices()
                self.L1HeadNodes.append(net.nodes[y][x])

        self.L1Net = self.createNetwork(self.L1Topo[0], 0, count_nodes = False, nodes = self.L1HeadNodes)

    # Function that runs all the above described in appropriate order to create the 2 layer network
    def Create2LayerNetwork(self, verbose = False):
        self.initalizeL2Networks()
        self.BuildL1Topology()

        if verbose:
            print("\n##################### Topology Info #####################")
            print("L1 Topology: ",self.networkNames[self.L1Topo[0][0]])
            print("L2 Topology Of Each Node: ")
            for i, network in zip(range(len(self.L2Topo)),self.L2Topo):
                print("     Node {} Topology: {}".format(i,self.networkNames[network[0]]))
            print("######################################################\n")
            print("##################### Node Links #####################")
            for net in self.L2Nets:
                print("\n######################################################")
                net.printNetworkInfo()
                print("######################################################\n")

        # Writing output to file
        f = open('../outputs/Network.txt', "w")

        f.write("\n##################### Topology Info #####################\n")
        f.write("L1 Topology: " + self.networkNames[self.L1Topo[0][0]] + "\n")
        f.write("L2 Topology Of Each Node: \n")
        for i, network in zip(range(len(self.L2Topo)),self.L2Topo):
            f.write("     Node " + str(i) + " Topology: " + self.networkNames[network[0]] + "\n")
        f.write("######################################################\n")
        f.write("\n##################### Node Links #####################\n")
        for net in self.L2Nets:
            f.write("\n######################################################\n")
            f.write(net.printNetworkInfo(True))
            f.write("######################################################\n")
        f.close()


        # Writing Nodes output to file
        f = open('../outputs/Nodes_Info.txt', "w")

        f.write("\n------------------- Topology Info ------------------- \n")
        f.write("L1 Topology: " + self.networkNames[self.L1Topo[0][0]] + "\n")
        f.write("L2 Topology Of Each Node: \n")
        for i, network in zip(range(len(self.L2Topo)),self.L2Topo):
            f.write("     Node " + str(i) + " Topology: " + self.networkNames[network[0]] + "\n")
        f.write("------------------------------------------------------- \n")
        f.write("\n------------------------  Nodes ----------------------- \n")
        for net in self.L2Nets:
            if net.name in ["Chain", "Ring", "Hypercube"]:
                for i in range(len(net.nodes)):
                    f.write("Node Name:" + str(net.nodes[i].Id) + "\n")
                    f.write("Node ID:" + str(net.nodes[i].number) + "\n")
                    f.write("Links:" + str(len(net.nodes[i].links)) + "\n")
                    for j in range(1,len(net.nodes[i].links)+1):
                        f.write("Link "+str(j)+":"+str(net.nodes[i].links[j-1])+ "\n")
                    f.write("-----------------------------------------------------\n")
            else:
                nodes = [node for sub in net.nodes for node in sub]
                for i in range(len(nodes)):
                    f.write("Node Name:" + str(nodes[i].Id) + "\n")
                    f.write("Node ID:" + str(nodes[i].number) + "\n")
                    f.write("Links:" + str(len(nodes[i].links)) + "\n")
                    for j in range(1,len(nodes[i].links)+1):
                        f.write("Link "+str(j)+":"+str(nodes[i].links[j-1]) + "\n")
                    f.write("-----------------------------------------------------\n")
        f.close()
