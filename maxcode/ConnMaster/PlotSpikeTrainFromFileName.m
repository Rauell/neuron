function [] = PlotSpikeTrainFromFileName(name, N)

%% Read in the potentials across the neurons from the simulation.
file_potentials = strcat(name);
t = single(textread( file_potentials , '%f',-1,'commentstyle','shell'))

%% Put into matrix form.
spikes = zeros(N);
spikeCount = ones(N,1);
for i = 1:length(t)/2,
    spikes(spikeCount(t(i*2-1)), t(i*2-1)) = t(i*2);
    spikeCount(t(i*2-1)) = spikeCount(t(i*2-1)) + 1;
end

%% Plot.
PlotSpikeTrains(spikes, N, 1000);