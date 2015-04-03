function [] = WriteOutFiles(directory_name, connStruct, i, C)

%% Write out all data to be used in NEURON simulations.
save = connStruct.Dz;
n1 = sprintf('%s/Dz%d.txt',directory_name, i);        
dlmwrite(n1, save);

save = connStruct.DEEz;
n1 = sprintf('%s/DEEz%d.txt',directory_name, i);         
dlmwrite(n1, save);

save = connStruct.DEIz;
n1 = sprintf('%s/DEIz%d.txt',directory_name, i);         
dlmwrite(n1, save);

save = connStruct.DIEz;
n1 = sprintf('%s/DIEz%d.txt',directory_name, i);        
dlmwrite(n1, save);

save = connStruct.DIIz;
n1 = sprintf('%s/DIIz%d.txt',directory_name, i);        
dlmwrite(n1, save);

save = connStruct.Dxy;
n1 = sprintf('%s/Dxy%d.txt',directory_name, i);        
dlmwrite(n1, save);

save = connStruct.DEExy;
n1 = sprintf('%s/DEExy%d.txt',directory_name, i);       
dlmwrite(n1, save);

save = connStruct.DEIxy;
n1 = sprintf('%s/DEIxy%d.txt',directory_name, i);          
dlmwrite(n1, save);

save = connStruct.DIExy;
n1 = sprintf('%s/DIExy%d.txt',directory_name, i);         
dlmwrite(n1, save);

save = connStruct.DIIxy;
n1 = sprintf('%s/DIIxy%d.txt',directory_name, i);         
dlmwrite(n1, save);

save = connStruct.D;
n1 = sprintf('%s/D%d.txt',directory_name, i);          
dlmwrite(n1, save);

save = connStruct.DEE;
n1 = sprintf('%s/DEE%d.txt',directory_name, i);        
dlmwrite(n1, save);

save = connStruct.DEI;
n1 = sprintf('%s/DEI%d.txt',directory_name, i);          
dlmwrite(n1, save);

save = connStruct.DIE;
n1 = sprintf('%s/DIE%d.txt',directory_name, i);         
dlmwrite(n1, save);

save = connStruct.DII;
n1 = sprintf('%s/DII%d.txt',directory_name, i);         
dlmwrite(n1, save);

save = C;
n1 = sprintf('%s/C%d.txt',directory_name, i);         
dlmwrite(n1, save);