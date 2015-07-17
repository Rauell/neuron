function [CIG] = Analysis_CIG(directory_name, directory_name_1)

%{
    This function will determine the connectivity between local neurons
    within various dimensions.

    Max Henderson
    6/1/15
    Drexel University
%}

%% Load connStruct object and populate with proper values.
connStruct = CreateConnectivityStructure();
connStruct = LoadParams(connStruct, directory_name);
curL = connStruct.L;
node = 13;
CIG = zeros(3, 100);

for i = 1:100,
    
    % Load all files...
    currentFile = strcat(directory_name, directory_name_1, int2str(i), '/C.txt');
    C = load(currentFile);
    currentFile = strcat(directory_name, directory_name_1, int2str(i), '/networkConstants.txt');
    NC = load(currentFile);
    inhib = NC(2);
    currentFile = strcat(directory_name, directory_name_1, int2str(i), '/Pos.txt');
    Pos = load(currentFile);

    message = strcat('Percent complete........', int2str(i));
    disp(message)
    
     % With connectivity, determine CIGx...
    CIG(1,i)  = GetCIG(Pos,       C, curL, node, inhib, 1);

    % With connectivity, determine CIGy...
    CIG(2,i)  = GetCIG(Pos,       C, curL, node, inhib, 2);
    
    % With connectivity, determine CIGz...
    CIG(3,i)  = GetCIG(Pos,       C, curL, node, inhib, 3);
    
end