function [C, probConnection] = Connections_ExpX(connStruct, choice, numCon)

%{
    This program will create a connectivity matrix with exponentially
    decaying connectivity.

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

%% Determine connectivity matrix of neurons which depends on distances.
[N1, N2, Ndiag, Dtemp] = GetConDim(connStruct, choice);
[averageDistance] = GetAverageDistance(N1, N2, Ndiag, Dtemp);
if Ndiag > 0,
    x = -averageDistance/(log(numCon/(N1*N1-N1))); 
else
    x = -averageDistance/(log(numCon/(N1*N2))); 
end

c = numCon;
probConnection = exp(-Dtemp/x);
C = (probConnection > rand(N1, N2));
while abs((sum(sum(C))-c)/c) > 0.05,
    if ((sum(sum(C))-c)/c) > 0,
        x = x*(0.9);
    else
        x = x*(1.1);
    end
    probConnection = exp(-Dtemp/x);
    C = (probConnection > rand(N1, N2));
    if Ndiag > 0,
        C = C - diag(diag(C));
    end
end