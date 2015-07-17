function [data] = Analysis_GetNetworkSPIKE(currentDir)

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
    n = length(spikes);
    data(i,1) = sum(sum(triu(spikes)))/(n*(n-1)/2); %/(n*n-numZero));
    
end