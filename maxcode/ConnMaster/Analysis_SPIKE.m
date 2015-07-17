function [SPIKE, SPIKE_GRID ] = Analysis_SPIKE(directory_name, directory_name_1)

%{
    This function will determine the synchronicity between various neurons.

    Max Henderson
    6/1/15
    Drexel University
%}

%% Load connStruct object and populate with proper values.
connStruct = CreateConnectivityStructure();
connStruct = LoadParams(connStruct, directory_name);
L = connStruct.L;
N = 100;
node = 12;
SPIKE_GRID1 = zeros(N, 20);
SPIKE_GRID2 = zeros(N, 20);
SPIKE_GRID3 = zeros(N, 20);
SPIKE = zeros(N, 20);
parfor i = 1:N,
    
    % Load all files...
    currentFile = strcat(directory_name, directory_name_1, int2str(i), '/networkConstants.txt');
    NC = load(currentFile);
    inhib = NC(2);
    currentFile = strcat(directory_name, directory_name_1, int2str(i), '/Pos.txt');
    Pos = load(currentFile);

    message = strcat('Percent complete........', int2str(i));
    disp(message)
    
    currentDir = strcat(directory_name, directory_name_1, int2str(i), '/');
    
    % Determine SPIKEx...
    SPIKE_GRID1(i,:) = Analysis_GetNetworkGridSPIKE(currentDir, Pos, L, node, inhib, 1);
    
    % Determine SPIKEy...
    SPIKE_GRID2(i,:) = Analysis_GetNetworkGridSPIKE(currentDir, Pos, L, node, inhib, 2);
    
    % Determine SPIKEz...
    SPIKE_GRID3(i,:) = Analysis_GetNetworkGridSPIKE(currentDir, Pos, L, node, inhib, 3);
    
    % Determine network SPIKE...
    SPIKE(i, :)       = Analysis_GetNetworkSPIKE(currentDir);
end

SPIKE_GRID = zeros(N, 20, 3);
SPIKE_GRID(:,:,1) = SPIKE_GRID1;
SPIKE_GRID(:,:,2) = SPIKE_GRID2;
SPIKE_GRID(:,:,3) = SPIKE_GRID3;
