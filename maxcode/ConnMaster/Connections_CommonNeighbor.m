function C = Connections_CommonNeighbor(connStruct, choice, numCon)

%% First, get the 'seed' aka original connectivity matrix.
[C,p,pr,pnr] = Connections_CommonNeighborSeed(connStruct, choice, numCon);

%% Then, apply common neighbor law.
C = Reorganize(C,40,1,1,p,pr,pnr);