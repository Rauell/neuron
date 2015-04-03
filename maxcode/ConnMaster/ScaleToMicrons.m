function data = ScaleToMicrons(data, L)

%{
    This program will determine the spatial positions of the neurons in a
    network determined by the length of the initial program simulation
    volume, L.

    Max Henderson
    May 29, 2014
    Drexel University
%}

maxims = max(max(data));
x = L/maxims;
data = data*x; %Scale back to MICRONS.