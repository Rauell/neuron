function [SPIKE, SPIKE_GRID] = Analysis_FR(directory_name, directory_name_1)

%{
    This function will determine the firing rate of neurons in a network. 

    Max Henderson
    6/22/15
    Drexel University
%}

%% Create proper variables.
N = 100;
FR = zeros(N, 20,3);

for i = 1:N,
    
    % Load all files...
    currentFile = strcat(directory_name, directory_name_1, int2str(i), '/networkConstants.txt');
    NC = load(currentFile);
    N = NC(1);
    inhib = NC(2);

    message = strcat('Percent complete........', int2str(i));
    disp(message)
    
    currentDir = strcat(directory_name, directory_name_1, int2str(i), '/');
    
    
end