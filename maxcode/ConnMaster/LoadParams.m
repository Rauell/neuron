function connStruct = LoadParams(connStruct, directory_name)

%{
    This program will be used to load input parameters for constructing
    neural networks for simulations.

    INPUT

    directory_name = Name of directory containing neural files
    connStruct =  Connectivity structure with several fields determining
    types of connectivity networks

    OUTPUT

    connStruct = Connectivity structure with several fields determining
    types of connectivity networks

    Max Henderson and Michael Royster
    Last updated : April 13th, 2015
    Drexel University
%}

%% Load input parameters for connectivity.
params = strcat(directory_name, 'paramsCon.txt'); % --- file with neuron to reproduce
fileID = fopen(params);
params = textscan(fileID,'%s %f');
connStruct.gc = params{1,2}(1);
connStruct.connDistribution =  [params{1,2}(2) params{1,2}(3) params{1,2}(4) params{1,2}(5)];
connStruct.CEE = params{1,2}(6);
connStruct.CEI = params{1,2}(7);
connStruct.CIE = params{1,2}(8);
connStruct.CII = params{1,2}(9);
connStruct.CN = [params{1,2}(10) params{1,2}(11) params{1,2}(12) params{1,2}(13)];
connStruct.Dchoice = [params{1,2}(14) params{1,2}(15) params{1,2}(16) params{1,2}(17)];
connStruct.threshProb = [params{1,2}(18) params{1,2}(19) params{1,2}(20) params{1,2}(21)];
connStruct.L = params{1,2}(22);
connStruct.x = params{1,2}(23);