function [EII, CII] = Connections_Inhib(connStruct, choice, numCon)

%{
    This program will determine the connectivity between inhibitory neurons
    as specified in Rieubland et al 2014 using the 'non-uniform random'
    model.

    INPUT
    
    
    
    OUTPUT

    EII : Electrical connections between inh. neurons in network.
    CII : Chemical connections between inh. neurons in network.

    Max Henderson
    May 19, 2014
    Drexel University
%}

%% Construct connectivity matrices for population and reformat Dz and Dxy.
Dz  = connStruct.DIIz;
Dxy = connStruct.DIIxy;
n = connStruct.NI;
EII = zeros(n);
CII = zeros(n);

%% Determine electrical synaptic connectivity.
for i = 1:n-1,
    for j = i + 1:n,
        EII(i,j) = Connections_IISingle(Dz(i,j), Dxy(i,j), 1);  % Connects neurons based on electrical probabilities
    end
end

%% Determine chemical synaptic connectivity.
for i = 1:n,
    for j = 1:n,
        CII(i,j) = Connections_IISingle(Dz(i,j), Dxy(i,j), 2);  % Connects neurons based on chemical probabilities
    end
end