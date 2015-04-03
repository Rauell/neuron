function connStruct = CreateDistanceMatrices(connStruct, data)

%{
    This program will populate all distance fields depending on 3D data
    points of the neurons in the network.

    INPUT
    
    connStruct = Connectivity structure with several fields determining
    types of connectivity networks

    OUTPUT

    connStruct = Connectivity structure with several fields determining
    types of connectivity networks

    Max Henderson and Michael Royster
    Last updated: April 2, 2015
    Drexel University
%}

connStruct.Dz  = CalculatePeriodicDistances(connStruct.N, data, connStruct.L, 1); % Absolute distance differences
connStruct.Dxy = CalculatePeriodicDistances(connStruct.N, data, connStruct.L, 2); % Absolute distance differences
connStruct.D   = CalculatePeriodicDistances(connStruct.N, data, connStruct.L, 3); % Absolute distance differences

connStruct.DEEz = connStruct.Dz(1:connStruct.NE, 1:connStruct.NE); % NE-by-NE distance matrix of 1D distances
connStruct.DEIz = connStruct.Dz(1:connStruct.NE, connStruct.NE + 1:connStruct.N); % NE-by-NI distance matrix of 1D distances
connStruct.DIEz = connStruct.Dz(connStruct.NE + 1:connStruct.N, 1:connStruct.NE); % NI-by-NE distance matrix of 1D distances
connStruct.DIIz = connStruct.Dz(connStruct.NE + 1:connStruct.N, connStruct.NE + 1:connStruct.N); % NI-by-NI distance matrix of 1D distances

connStruct.DEExy = connStruct.Dxy(1:connStruct.NE, 1:connStruct.NE); % NE-by-NE distance matrix of 2D distances
connStruct.DEIxy = connStruct.Dxy(1:connStruct.NE, connStruct.NE + 1:connStruct.N); % NE-by-NI distance matrix of 2D distances
connStruct.DIExy = connStruct.Dxy(connStruct.NE + 1:connStruct.N, 1:connStruct.NE); % NI-by-NE distance matrix of 2D distances
connStruct.DIIxy= connStruct.Dxy(connStruct.NE + 1:connStruct.N, connStruct.NE + 1:connStruct.N); % NI-by-NI distance matrix of 2D distances

connStruct.DEE = connStruct.D(1:connStruct.NE, 1:connStruct.NE); % NE-by-NE distance matrix of 3D distances
connStruct.DEI = connStruct.D(1:connStruct.NE, connStruct.NE + 1:connStruct.N); % NE-by-NI distance matrix of 3D distances
connStruct.DIE = connStruct.D(connStruct.NE + 1:connStruct.N, 1:connStruct.NE); % NI-by-NE distance matrix of 3D distances
connStruct.DII = connStruct.D(connStruct.NE + 1:connStruct.N, connStruct.NE + 1:connStruct.N); % NI-by-NI distance matrix of 3D distances