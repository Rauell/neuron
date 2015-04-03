function C = Connections_Random(connStruct, choice, numCon)

%{
    This program will create a connectivity matrix with random
    connectivity.

    INPUT

    connStruct = Connectivity structure with several fields determining
    types of connectivity networks
    choice = Defining whether we care about EE, EI, IE or II connections
        1 = EE
        2 = EI
        3 = IE
        4 = II
    numCon =  Average number of connections for this subset of network

    OUTPUT

    C = N1 by N2 matrix of connections

    Max Henderson and Micheal Royster
    Drexel University
    Last updated March 23, 2015
%}

%% Make matrix of random connections.
[N1, N2, Ndiag] = GetConDim(connStruct, choice);
whatRand = numCon/(N1*N2 - Ndiag);
C = (rand(N1,N2) < whatRand);
if Ndiag > 0,
    for i = 1 : N1,
        
        C(i,i) = 0;
        
    end
end