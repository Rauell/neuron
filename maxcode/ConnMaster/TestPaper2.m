function [] = TestPaper2(t)
t = load(t);
N = 343;
spikes = zeros(N);
spikeCount = ones(N,1);
for i = 1:length(t)/2,
spikes(spikeCount(t(i*2-1)), t(i*2-1)) = t(i*2);
spikeCount(t(i*2-1)) = spikeCount(t(i*2-1)) + 1;
end
PlotSpikeTrains(spikes, 343, 2000)