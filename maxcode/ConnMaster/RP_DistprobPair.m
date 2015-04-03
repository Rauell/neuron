function [p] = RP_DistprobPair(Dtemp, N1, N2, Ndiag, numCon)

%{
    This program will be used to connect neurons in a network based off of
    intersomatic distances of neurons in the network.

    Max Henderson
    February 19, 2014
    Drexel University
%}

%% Calculate connectivity based off exponential decaying function.
[averageDistance] = GetAverageDistance(N1, N2, Ndiag, Dtemp);
if Ndiag > 0,
    x = -averageDistance/(log(numCon/(N1*N1-N1))); 
else
    x = -averageDistance/(log(numCon/(N1*N2))); 
end
p = 0.33*exp(-Dtemp/x);

%% Readjust for diagonal.
for i = 1 : length(p),
   p(i,i) = 0; 
end