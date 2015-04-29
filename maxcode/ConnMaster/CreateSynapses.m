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
SEE =  normrnd(connStruct.SEE(1), connStruct.SEE(2), connStruct.NE, connStruct.NE);
SEI =  normrnd(connStruct.SEI(1), connStruct.SEI(2), connStruct.NE, connStruct.NI);
SIE =  normrnd(connStruct.SIE(1), connStruct.SIE(2), connStruct.NI, connStruct.NE);
SII =  normrnd(connStruct.SII(1), connStruct.SII(2), connStruct.NI, connStruct.NI);
S   = [SEE SEI; SIE SII];
C   = S.*C;