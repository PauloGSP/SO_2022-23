% Read data from files
Nodes = importdata('Nodes2.txt');
Links = importdata('Links2.txt');
%Give server node id
servers = [20,30,65,78,103,107,122,131,173,177];
plotTopology(Nodes,Links,servers)
