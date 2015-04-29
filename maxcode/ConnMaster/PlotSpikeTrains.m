function [] = PlotSpikeTrains(spikeTrain, numNeurons, simTime)

%{
    This function will show the raster plot for a particular network
    simulation.

    Max Henderson
    1/4/14
    Drexel University
%}

spikeTrain = spikeTrain';
[l, w] = size(spikeTrain);
axis([0 simTime 0 numNeurons+1])
for i = 1:numNeurons,
    for j = 1:w,
        if spikeTrain(i,j) > 0,
            hold on
            line([spikeTrain(i,j); spikeTrain(i,j)], [i-0.5,i+0.5], 'LineWidth',2, 'Color', 'k')
        end
    end
end
%axis([500 1000 250 750])