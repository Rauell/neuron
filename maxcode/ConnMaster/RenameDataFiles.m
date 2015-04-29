function fileCount = RenameDataFiles(directory_name, connStruct, randYes)

%{
    This program will be used to reformat files that were originally 
    generated using the slicegen program.  This will determine how many
    total files are in the program, and rename them accordingly for easier
    access and use.

    INPUT

    directory_name = Name of directory containing neural files
    connStruct =  Connectivity structure with several fields determining
    types of connectivity networks
    randYes = Create random networks?

    OUTPUT

    fileCount = Number of total files to consider in the directory

    Max Henderson and Michael Royster
    Last updated : April 7th, 2015
    Drexel University
%}

%% Load the files in the directory to get neural distributions.
files = dir(directory_name);
fileIndex = find(~[files.isdir]);
fileCount = 0;
L = connStruct.L;

%% Go through each file and generate connectivity matrices.
for i = 1:length(fileIndex)
    
    fileName = files(fileIndex(i)).name;
    
    if length(fileName) > 16,
        
        if strcmp(fileName(1:17),'neuBlockwithColID'),

                % Iterate current file count... 
                fileCount = fileCount + 1

                % Load perturbed neurons with micrcolumnar ID...
                file_potentials = strcat(directory_name, '/', fileName); % --- file with neuron to reproduce
                data1 = single(textread( file_potentials , '%f',-1,'commentstyle','shell'));
                data1 = reshape(data1, 4, length(data1)/4)';
                
                % Seperate data1 into old and micro IDs...
                ID = data1(:,1);

                % Load YOUNG neurons...
                file_potentials = strcat(directory_name, '/neuBlock_', fileName(19:27), '_000.xyz'); % --- file with neuron to reproduce
                dataYoung = single(textread( file_potentials , '%f',-1,'commentstyle','shell'));
                dataYoung = reshape(dataYoung, 3, length(dataYoung)/3)';
                dataYoung = ScaleToMicrons(dataYoung, L);
                
                % Save distance results
                n1 = sprintf('%s/PosYoung%d.txt',directory_name, fileCount);        
                dlmwrite(n1, dataYoung);
                
                % Save microcolumnar IDs
                n1 = sprintf('%s/ID%d.txt',directory_name, fileCount);        
                dlmwrite(n1, ID);
               
                % Make (or don't) random networks..
                if randYes == 1,
                    dataRandom = L*rand(length(dataYoung), 3);
                    n1 = sprintf('%s/PosRand%d.txt',directory_name, fileCount);        
                    dlmwrite(n1, dataRandom);
                end
        end
        
    end
end