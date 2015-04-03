function C = Connections_NN(connStruct, choice, numCon)
%{
    This program will take an input file containing 3D points for where the
    soma's of the neurons in the neural network will be placed.  In this 
    connectivity scheme, we will connect X nearest neighbors.

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

%% Find x nearest neighbors to connect for each neuron. 
[N1, N2, Ndiag, Dtemp] = GetConDim(connStruct, choice);
C = zeros(N1, N2);
if Ndiag > 0,
    Dtemp = Dtemp + eye(N1)*10000000;
end

for n = 1:numCon,
    [i, j] =  find(Dtemp == min(min(Dtemp)));
    if length(i) > 1,
        a = ceil(rand(1,1)*length(i));
        i = i(a);
        j = j(a);
    end
    C(i,j) = 1;
    Dtemp(i,j) = 10000000;
end