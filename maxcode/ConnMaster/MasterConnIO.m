function [] = MasterConnIO(directory_name)

%{
    This program will be used to load all neural network data into our
    algorithms for determining neural network connectivity.  All I/O work
    will be down inside this function.

    Max Henderson
    Last updated: March 5, 2015
    Drexel University
%}

%% Create connectivity structure and load in default parameters.
connStruct = CreateConnectivityStructure();
connStruct = LoadParams(connStruct, directory_name);

%% Rename / generate data files.
connStruct.connDistribution = connStruct.connDistribution/sum(connStruct.connDistribution); % Normalize connectivity vector
fileCount = RenameDataFiles(directory_name, connStruct);
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
    WriteOutFiles(directory_name, connStruct, i, C)
end
disp('Finished!')