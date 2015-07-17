function [] = MasterConnIO(directory_name, output_dir)

%{
    This program will be used to load all neural network data into our
    algorithms for determining neural network connectivity.  All I/O work
    will be down inside this function.

    INPUTS

    directory_name = Name of directory for neural files
    output_dir = Place to generate output files

    Max Henderson
    Last updated: April 29, 2015
    Drexel University
%}

%matlabpool
% Create connectivity structure and load in default parameters.
connStruct = CreateConnectivityStructure();
connStruct = LoadParams(connStruct, directory_name);
    
% Rename / generate data files.
connStruct.connDistribution = connStruct.connDistribution/sum(connStruct.connDistribution); % Normalize connectivity vector
fileCount = RenameDataFiles(directory_name, connStruct, connStruct.Rand);
clear connStruct

for i = 1 : fileCount,
    i
    % Create connectivity structure and load in default parameters.
    connStruct = CreateConnectivityStructure();
    connStruct = LoadParams(connStruct, directory_name);
    connStruct.connDistribution = connStruct.connDistribution/sum(connStruct.connDistribution); % Normalize connectivity vector
    data = strcat(directory_name, '/PosYoung', int2str(i), '.txt'); % --- file with neuron to reproduce
    data = load(data);
    ID = strcat(directory_name, '/ID', int2str(i), '.txt'); % --- file with neuron to reproduce
    ID = load(ID);
    connStruct.ID = ID;
    connStruct.N = length(data); % Get number of neurons in network
    connStruct.NE = GetInhibIndex(ID) - 1; % Get inhibitory index and use this to determine NE
    connStruct.NI = connStruct.N - connStruct.NE; % Use N and NE to determine NI
    [C, connStruct] = ConnectNeurons(connStruct, data);
    C = CreateSynapses(connStruct, C); % MPH creates connections with synaptic strengths 04/29/15
    WriteOutFiles(directory_name, connStruct, i, C, output_dir, data, ID)
    % Clear data for memory purposes
    clear connStruct
    connStruct = CreateConnectivityStructure();
    connStruct = LoadParams(connStruct, directory_name);
    %CIG = SanityCheck_CIG(C, data, connStruct);
    if connStruct.Rand == 1,
        CreateRandomNetworks(directory_name, i, connStruct, ID);
    end
    clear connStruct
    clear data
    clear ID
    clear C
end

disp('Finished!')