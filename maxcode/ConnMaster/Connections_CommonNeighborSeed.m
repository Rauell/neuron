function [C,p,pr,pnr] = Connections_CommonNeighborSeed(connStruct, choice, numCon)

%{
    This program will determine a connectivity matrix based off of
    distances between somas of neurons in a network.  This code is modified
    from similar code from Perin et al 2013.

    INPUT
    
    N : Number of neurons in the network.
    dist : Intersomatic distances between all neurons in network.

    OUTPUT

    conn : Resulting connectivity matrix.
    p : Probability of connection.
    pr : Probability of reciprocal connection.
    pnr : Probability of nonreciprocal connection.

    Max Henderson
    Last updated Sept. 14, 2014
    Drexel University
%}

N1 = GetConDim(connStruct, choice);

r=rand(N1)+eye(N1); %define random matrix with ones in diagonal

[~, p] = Connections_ExpX(connStruct, choice, numCon);

pr=p.^2; %reciprocal connection probability matrix

pnr = 2*p.*(1 - p);

C=r<p; %connectivity is defined by p