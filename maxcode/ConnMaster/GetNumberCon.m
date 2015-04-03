function c = GetNumberCon(connStruct, choice)

%{
    This function will determine how many total connections will be in a
    particular subset of neurons based off of the global connectivity of
    the network (gc) and the proportion of global connections for this
    subset of neurons (proportion).  All this information will be contained
    inside the connStruct object.

    INPUT

    connStruct = Connectivity structure with several fields determining
    types of connectivity networks
    choice = Defining whether we care about EE, EI, IE or II connections
        1 = EE
        2 = EI
        3 = IE
        4 = II

    OUTPUT

    c : Number of connections for this subset of neurons.

    Max Henderson
    February 19, 2014
    Drexel University
%}

%% First, figure out respective variables depending on choice.
if choice == 1, % EE
    
    N1 = connStruct.NE;
    N2 = connStruct.NE;
    proportion = connStruct.connDistribution(1);
    Ndiag = connStruct.NE;
    
elseif choice == 2, % EI
    
    N1 = connStruct.NI;
    N2 = connStruct.NE;
    proportion = connStruct.connDistribution(2);
    Ndiag = 0;
    
elseif choice == 3, % IE
    
    N1 = connStruct.NE;
    N2 = connStruct.NI;
    proportion = connStruct.connDistribution(3);
    Ndiag = 0;
    
else % II
    
    N1 = connStruct.NI;
    N2 = connStruct.NI;
    proportion = connStruct.connDistribution(4);
    Ndiag = connStruct.NI;
    
end

%% Determine final number of connections for subset of neurons.
totalPossibleConn = N1*N2 - Ndiag;
c = ceil(connStruct.gc*proportion*totalPossibleConn);