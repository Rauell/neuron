function C = Connections_Microcolumn(connStruct, choice, numCon)

%{
    This program will create a connectivity matrix connecting all neurons
    in the microcolumns, depending on the microcolumnar ID.

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
    Last updated March 30, 2015
%}

%% First connect all-to-all neurons within the column.
[N1, N2, Ndiag, Dtemp] = GetConDim(connStruct, choice);
C = zeros(N1, N2);
ID = connStruct.ID;
for i = 1 : length(Dtemp),
    C(i,find(ID == ID(i))) = 1;
end
if Ndiag > 0,
    for i = 1 : N1,
        
        C(i,i) = 0;
        
    end
end

%% Now, connect other neurons compared to x.
x = connStruct.x;
if numCon > 0,
    c = sum(sum(C)); % figure out total connections in network
    n = ceil(c*x); % x is a fractional number of new connections to add to farther off neurons
    PC = exp(-Dtemp/50) - C - eye(length(Dtemp)); % determine distant dependent connections
    RC = rand(length(Dtemp));
    P = PC - RC;
    [~,locs]=maxNvalues(P,n);
    for i = 1:n,
        C(locs(i,1), locs(i,2)) = 1;
    end
end