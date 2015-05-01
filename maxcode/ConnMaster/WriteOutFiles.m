function [] = WriteOutFiles(directory_name, connStruct, i, C, directory_name1, Pos, ID)

%{
    This program will be used purely to write out files created in the main
    methods.

    INPUTS

    directory_name = Name of directory for neural files
    connStruct = Connectivity structure with several fields determining
    types of connectivity networks
    i = Current file count
    C = Matrix of connections of neurons in the current network
    randYes = Random network geometry?

    Max Henderson and Michael Royster
    Last updated: April 7, 2015
    Drexel University
%}

%% Create new directory to store all information.
directory_name2 = int2str(i);
directory_name = sprintf('%s/%s/%s/',directory_name, directory_name1, directory_name2);
mkdir(directory_name);

%% Write out all data to be used in NEURON simulations.
save = connStruct.Dz;
n1 = sprintf('%s/Dz.txt',directory_name);
dlmwrite(n1, save);

save = connStruct.DEEz;
n1 = sprintf('%s/DEEz.txt',directory_name);         
dlmwrite(n1, save);

save = connStruct.DEIz;
n1 = sprintf('%s/DEIz.txt',directory_name);         
dlmwrite(n1, save);

save = connStruct.DIEz;
n1 = sprintf('%s/DIEz.txt',directory_name);         
dlmwrite(n1, save);

save = connStruct.DIIz;
n1 = sprintf('%s/DIIz.txt',directory_name);     
dlmwrite(n1, save);

save = connStruct.Dxy;
n1 = sprintf('%s/Dxy.txt',directory_name);     
dlmwrite(n1, save);

save = connStruct.DEExy;
n1 = sprintf('%s/DEExy.txt',directory_name);     
dlmwrite(n1, save);

save = connStruct.DEIxy;
n1 = sprintf('%s/DEIxy.txt',directory_name);     
dlmwrite(n1, save);

save = connStruct.DIExy;
n1 = sprintf('%s/DEIxy.txt',directory_name);     
dlmwrite(n1, save);

save = connStruct.DIIxy;
n1 = sprintf('%s/DIIxy.txt',directory_name);     
dlmwrite(n1, save);

save = connStruct.D;
n1 = sprintf('%s/D.txt',directory_name);     
dlmwrite(n1, save);

save = connStruct.DEE;
n1 = sprintf('%s/DEE.txt',directory_name);     
dlmwrite(n1, save);

save = connStruct.DEI;
n1 = sprintf('%s/DEI.txt',directory_name);     
dlmwrite(n1, save);

save = connStruct.DIE;
n1 = sprintf('%s/DIE.txt',directory_name);     
dlmwrite(n1, save);

save = connStruct.DII;
n1 = sprintf('%s/DII.txt',directory_name);     
dlmwrite(n1, save);

save = C;
n1 = sprintf('%s/C.txt',directory_name);     
dlmwrite(n1, save);

save = Pos;
n1 = sprintf('%s/Pos.txt',directory_name);     
dlmwrite(n1, save);

save = ID;
n1 = sprintf('%s/ID.txt',directory_name);     
dlmwrite(n1, save);

inhibIndex = GetInhibIndex(ID);
save = [connStruct.N; inhibIndex; connStruct.L];
n1 = sprintf('%s/networkConstants.txt',directory_name);
dlmwrite(n1, save);