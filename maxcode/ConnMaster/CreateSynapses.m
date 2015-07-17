function [C] = CreateSynapses(connStruct, C)

%{
    This program will be used to construct a matrix of connectivity that
    has the synaptic strengths built-in.

    INPUT

    connStruct : Connectivity structure with several fields determining
    types of connectivity networks.
    C : Connectivity matrix

    OUTPUT

    C : Connectivity matrix, with adjusted synaptic values

    Max Henderson and Michael Royster
    Last updated: April 29, 2015
    Drexel University
%}

%% Create new matrix of connections that has synaptic strengths built-in.
if length(C) < 1000,
    SEE =  normrnd(connStruct.SEE_mean, connStruct.SEE_std, connStruct.NE, connStruct.NE);
    SEI =  normrnd(connStruct.SEI_mean, connStruct.SEI_std, connStruct.NE, connStruct.NI);
    SIE =  normrnd(connStruct.SIE_mean, connStruct.SIE_std, connStruct.NI, connStruct.NE);
    SII =  normrnd(connStruct.SII_mean, connStruct.SII_std, connStruct.NI, connStruct.NI);
    S   = [SEE SEI; SIE SII];
    C   = S.*C;
else
    for i = 1:length(C),
        for j = 1:length(C),
            s = GetSynapticStrength(i,j,connStruct);
            C(i,j) = s*C(i,j);
        end
    end
end