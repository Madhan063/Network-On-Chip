class Node:
    def __init__(self, id, number):

        self.Id = id
        self.number = number + 1
        self.links = []

def ConnectNodes(node1 : Node, node2 : Node):
    node1.links.append(node2.Id)
    node2.links.append(node1.Id)
    return
