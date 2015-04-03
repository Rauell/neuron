function [C, c] = CreateConnectivityMatrix(connStruct, choice)

%{
    This program will determine the intersomatic distances between neurons
    in the network using periodic boundary conditions, assuming isotropic
    connectivity.

    INPUT
    
    connStruct = Connectivity structure with several fields determining
    types of connectivity networks
    typeConn = Type of connection for this subset of network
        1 = Random 
        2 = Exponential decay x
        3 = Nearest neighbor
        4 = Threshold 
        5 = Chemical inhib
        6 = Electrical inhib
        7 = Common neighbor
    choice = Defining whether we care about EE, EI, IE or II connections
        1 = EE
        2 = EI
        3 = IE
        4 = II

    OUTPUT

    C : matrix of connections between neurons

    Max Henderson and Michael Royster
    Last updated: March 16, 2015
    Drexel University
%}

c = GetNumberCon(connStruct, choice);

if choice == 1,
    
    typeConn = connStruct.CEE;
    
elseif choice == 2,
    
    typeConn = connStruct.CEI;
    
elseif choice == 3,
    
    typeConn = connStruct.CIE;
    
else
    
    typeConn = connStruct.CII;

end

if typeConn == 1, % Random connectivity...
    
    C = Connections_Random(connStruct, choice, c);
    
elseif typeConn == 2, % Exponential connectivity...
    
    C = Connections_ExpX(connStruct, choice, c);
    
elseif typeConn == 3, % Nearest neighbor connectivity...
    
    C = Connections_NN(connStruct, choice, c);
        
elseif typeConn == 4, % Threshold connectivity...
    
    C = Connections_Thresh(connStruct, choice, c);
    
elseif typeConn == 5, % Chemical II connectivity...
    
    [~, C] = Connections_Inhib(connStruct, choice, c);
    
elseif typeConn == 6, % Electrical II connectivity...
    
    [C, ~] = Connections_Inhib(connStruct, choice, c);
    
elseif typeConn == 7, % Common neighbor
    
    C = Connections_CommonNeighbor(connStruct, choice, c);
    
elseif typeConn == 8, % Microcolumnar connections
    
    C = Connections_Microcolumn(connStruct, choice, c);
    
else % Just a blank matrix for combination purposes later
    
    C = Connections_Blank(connStruct, choice, c);
    
end