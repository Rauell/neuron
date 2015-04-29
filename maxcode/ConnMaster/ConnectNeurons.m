function [C, connStruct] = ConnectNeurons(connStruct, data)

%{
    This program will be used to create a single instance of a connectivity
    matrix for a particular neural network.

    INPUTS

    connStruct = Connectivity structure with several fields determining
    types of connectivity networks
    data = 3D data of neural positions

    OUTPUT

    C = Matrix of connections for the network
    connStruct = Connectivity structure with several fields determining
    types of connectivity networks

    Max Henderson and Michael Royster
    Last updated: April 7, 2015
    Drexel University
%}

%% Update connStruct.
connStruct.connDistribution = connStruct.connDistribution/sum(connStruct.connDistribution); % Normalize to 1
connStruct = CreateDistanceMatrices(connStruct, data);

% Connect E -> E
CEE = CreateConnectivityMatrix(connStruct, 1);

% Connect E -> I
CEI = CreateConnectivityMatrix(connStruct, 2);

% Connect I -> E
CIE = CreateConnectivityMatrix(connStruct, 3);

% Connect I -> I
CII = CreateConnectivityMatrix(connStruct, 4);

% Combine all connections....
C = [CEE CEI; CIE CII];