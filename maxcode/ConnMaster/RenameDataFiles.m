function fileCount = RenameDataFiles(directory_name, connStruct)


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
                inhibIndex = GetInhibIndex(ID);
                
                % Save both the size of the network and the index wherein the
                % inhibitory neurons kick in.

                n = length(dataYoung);
                save = [n; inhibIndex];
                n1 = sprintf('%s/networkConstants%d.txt',directory_name, fileCount);
                edit 'n1';          
                dlmwrite(n1, save);
                
                % Save distance results
                n1 = sprintf('%s/PosYoung%d.txt',directory_name, fileCount);
                edit 'n1';          
                dlmwrite(n1, dataYoung);
                
                %dataRandom = L*rand(length(dataYoung), 3);
                n1 = sprintf('%s/ID%d.txt',directory_name, fileCount);
                edit 'n1';          
                dlmwrite(n1, ID);
               
        end
        
    end
end