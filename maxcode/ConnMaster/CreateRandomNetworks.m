function [] = CreateRandomNetworks(directory_name, i, connStruct, ID)
%{
    This fucntion will be used to make random geometries and connect the
    neurons according to connStruct.

    INPUT

    directory_name : Input directory with neural files
    i : current index which correlates to a particular microcolumnar
    network
    connStruct : Connectivity structure with several fields determining
    types of connectivity networks
    ID : File containing microcolumnar IDs for every neuron

    Max Henderson and Michael Royster
    Last updated: March 26, 2015
    Drexel University
%}

data = strcat(directory_name, '/PosRand', int2str(i), '.txt'); % --- file with neuron to reproduce
data = load(data);
[C, connStruct] = ConnectNeurons(connStruct, data);
directory_name1 = 'Rand';
C = CreateSynapses(connStruct, C); % MPH creates connections with synaptic strengths 04/29/15
WriteOutFiles(directory_name, connStruct, i, C, directory_name1, data, ID);
%CIG = SanityCheck_CIG(C, data, connStruct);