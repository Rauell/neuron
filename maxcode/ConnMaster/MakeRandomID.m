function [ID, NE] = MakeRandomID(N)

%{
    This program will create a matrix of microcolumnars ID values randomly,
    assuming that the first 80% of neurons are exc. and the last 20% are
    inhib.

    INPUT
    
    N = Total number of neurons in network

    OUTPUT

    ID = Matrix of random microcolumnar IDs
    NE = Number of excitory neurons

    Max Henderson and Michael Royster
    Last updated: April 2, 2015
    Drexel University
%}

%% Create microcolumnar ID matrix and populate.
ID = zeros(N,1); % matrix for storing IDs
p = 0.1; % probability that we start a new column
NE = ceil(0.8*N); % number of excitory neurons
currColumn = 1;
for i = 1 : NE,
    ID(i) = currColumn;
    if rand(1,1) < p,
        currColumn = currColumn + 1;
    end
end
ID(NE+1:N,1) = -1;