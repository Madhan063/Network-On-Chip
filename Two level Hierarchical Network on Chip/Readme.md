# Two level Hierarchical Network on Chip

The goal of this project is to create a two-level hierarchical network on chip.

## Input

### L1Topology.txt 

Single line with the data - X, n, m

where X = C, R, M, F, H, B

- C : Chain
- R : Ring
- M : Mesh
- F : Folded Torus
- H : Hypercube of dimension 3 (8 nodes)
- B : Butterfly network

n : Number of nodes in the first dimension
m : Number of nodes in the second dimension (1 for C and R)

### L2Topology.txt

This file will have n x m lines with each line as the same syntax as the above.

## Output

Nodes_info.txt : Details about each node

Network.txt : Details about the two-layered network
