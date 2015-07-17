function [fr_all, fr_e] = Analysis_GetNetworkFR(currentDir, inhibIndex, N)

%{
    This function will determine the synchronicity within a random grid
    block in the neural network.

    Max Henderson
    7/22/14
    Drexel University
%}

%% Get SPIKE distances.
stims = [5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100];
fr_all = zeros(length(stims), 1);
fr_e = zeros(length(stims), 1);

for i = 1:length(stims),
    
    % Load current spike data.
    s = strcat(currentDir, 'raster.', int2str(stims(i)), '.txt');
    spikes = load(s);

    fr_all(i) = length(spikes)/2;
    for 
    
end