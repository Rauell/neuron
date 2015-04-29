function [] = MasterConnIO(directory_name, randYes)

%{
    This program will be used to load all neural network data into our
    algorithms for determining neural network connectivity.  All I/O work
    will be down inside this function.

    INPUTS

    directory_name = Name of directory for neural files
    randYes = Random network geometry?

    Max Henderson
    Last updated: April 29, 2015
    Drexel University
%}

%% Create connectivity structure and load in default parameters.
connStruct = CreateConnectivityStructure();
connStruct = LoadParams(connStruct, directory_name);

%% Rename / generate data files.
connStruct.connDistribution = connStruct.connDistribution/sum(connStruct.connDistribution); % Normalize connectivity vector
fileCount = RenameDataFiles(directory_name, connStruct, randYes);
for i = 1 : fileCount,
    i
    data = strcat(directory_name, '/PosYoung', int2str(i), '.txt'); % --- file with neuron to reproduce
    data = load(data);
    ID = strcat(directory_name, '/ID', int2str(i), '.txt'); % --- file with neuron to reproduce
    ID = load(ID);
    connStruct.ID = ID;
    connStruct.N = length(data); % Get number of neurons in network
    connStruct.NE = GetInhibIndex(ID) - 1; % Get inhibitory index and use this to determine NE
    connStruct.NI = connStruct.N - connStruct.NE; % Use N and NE to determine NI
    [C, connStruct] = ConnectNeurons(connStruct, data);
    directory_name1 = 'Young';
    C = CreateSynapses(connStruct, C); % MPH creates connections with synaptic strengths 04/29/15
    WriteOutFiles(directory_name, connStruct, i, C, directory_name1, data, ID)
    if randYes == 1, % This means create random files as well!
        data = strcat(directory_name, '/PosRand', int2str(i), '.txt'); % --- file with neuron to reproduce
        data = load(data);
        [C, connStruct] = ConnectNeurons(connStruct, data);
        directory_name1 = 'Rand';
        C = CreateSynapses(connStruct, C); % MPH creates connections with synaptic strengths 04/29/15
        WriteOutFiles(directory_name, connStruct, i, C, directory_name1, data, ID)
    end
end
disp('Finished!')