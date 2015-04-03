function C = Connections_Thresh(connStruct, choice, numCon)


%{
    This program will determine the connectivity between inhibitory neurons
    receiving input from nearby excitory neurons, as shown in Bock et al 2011
    and Hofer et al 2011.  We are relaxing this condition that this can be
    only between E and I and allowing for arbitrary neurons to connect in
    similar ways.

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
    Last updated March 25, 2015
%}

%% Initialize variables.
[N1, N2, Ndiag, Dtemp] = GetConDim(connStruct, choice);
prob = connStruct.threshProb(choice);
numCon = ceil(numCon/prob);
if Ndiag > 0,
    Dtemp = Dtemp + eye(N1)*10000000;
end
thresh = FindBestThresh(Dtemp, numCon, N1, N2);
C = (Dtemp < thresh).*(rand(N1,N2) < prob);