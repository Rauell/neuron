function [] = PlotSpikeTrainFromFileName(name, stim)

%% Read in the potentials across the neurons from the simulation.
file_potentials = strcat(name, 'raster.', int2str(stim), '.txt')
t = single(textread( file_potentials , '%f',-1,'commentstyle','shell'));
file_potentials = strcat(name, 'networkConstants.txt')
N = single(textread( file_potentials , '%f',-1,'commentstyle','shell'));
N = N(1);

%% Put into matrix form.
spikes = zeros(N);
spikeCount = ones(N,1);
for i = 1:length(t)/2,
    spikes(spikeCount(t(i*2-1)), t(i*2-1)) = t(i*2);
    spikeCount(t(i*2-1)) = spikeCount(t(i*2-1)) + 1;
end

%% Plot.
PlotSpikeTrains(spikes, N, 2000);