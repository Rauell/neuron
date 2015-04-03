function [averageDistance] = GetAverageDistance(N1, N2, Ndiag, Dtemp)

if Ndiag > 0,
    averageDistance = sum(sum(Dtemp))/(N1*N2 - Ndiag);
else
    averageDistance = sum(sum(Dtemp))/(N1*N2);
end