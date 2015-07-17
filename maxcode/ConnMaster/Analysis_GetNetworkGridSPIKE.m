function [data] = Analysis_GetNetworkGridSPIKE(currentDir, Pos, L, node, inhibIndex, dim)

%{
    This function will determine the synchronicity within a random grid
    block in the neural network.

    Max Henderson
    7/22/14
    Drexel University
%}

%% Get SPIKE distances.
stims = [5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100];
data = zeros(length(stims), 1);

for i = 1:length(stims),
    
    % Load current spike data.
    s = strcat(currentDir, 'spike_distance', int2str(stims(i)), '.txt');
    spikes = load(s);

    [SPIKE, num] = Analysis_GetGridSPIKE(spikes, Pos, dim, L, node, inhibIndex);

    sumNum = sum(sum(num));

    SPIKE = SPIKE.*num/sumNum;  % Normalize for size of grid chunks

    data(i) = sum(sum(SPIKE)); %/(n*n-numZero));
    
end