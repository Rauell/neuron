function avg = CheckTotalC(connStruct)

%{
    This program will check the number of total connections for various connectivity algorithms.
 
    INPUT
    
    connStruct = Connectivity structure with several fields determining
    types of connectivity networks

    OUTPUT

    avg : Average number of connections for a particular network

    Max Henderson and Michael Royster
    Last updated: May 5, 2015
    Drexel University
%}

avg = 0;
for i = 1 : 10000,
    
    avg = avg + sum(sum(Connections_Thresh(connStruct, 1, 7))); % This is the line to change for the particular connectivity to test
    
end
avg = avg/10000;